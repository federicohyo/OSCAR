#!/usr/bin/env python3
"""Temporal-XOR SW positive control: the task engineered so RECURRENCE is provably required.

Two bits are presented at DIFFERENT times -- bit a in an early window, bit b in a late window,
separated by a GAP. The label is a XOR b. XOR needs the a*b interaction, which needs both bits
'present' at once; but they never overlap in time, so the network must CARRY bit a's trace
across the gap to combine it with bit b. If the membrane time constant is SHORT (gap >> tau_m),
a leaky feedforward network forgets a before b arrives -> it cannot compute the interaction ->
chance on XOR. Spike-triggered recurrence (mirroring the chip's firmware SETRECUR: a spike
re-injects into connected neurons) SUSTAINS a's activation until b arrives -> XOR becomes
separable. Same XOR-via-exc/inh routing as the static on-chip XOR, plus the temporal gap.

Expected: feedforward ~ chance on T-XOR, recurrent solves it; and when the gap is SMALL
(<= tau_m) even feedforward works (memory not needed) -- the negative control on the mechanism.

    ./.venv-meas/bin/python3 txor_sw.py
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score

K, TAUS = 8, [0.05, 0.1, 0.2, 0.4]
# a-exc/b-inh detects corner (1,0); a-inh/b-exc detects (0,1); a-exc/b-exc is an OR/AND
# summation unit. The mix makes XOR linearly separable at the population level.
SIGN_PATTERNS = [(0, 1), (1, 0), (0, 0)]   # (chan_a, chan_b): 0=exc, 1=inh


def make_txor_trials(n_per_cell, T, win_a, win_b, burst, jitter, rng):
    """Trials: bit a -> burst in win_a, bit b -> burst in win_b (temporally separated).
    Returns (bits_ab, groups). Events are built per-neuron in the sim (sign-dependent)."""
    ab, grp = [], []
    for a in (0, 1):
        for b in (0, 1):
            for rep in range(n_per_cell):
                ab.append((a, b)); grp.append(rep)
    return np.array(ab), np.array(grp)


def _burst(active, win, burst, jitter, T, rng):
    if not active:
        return np.empty(0)
    lo, hi = win
    ts = rng.uniform(lo, hi, burst) + jitter * rng.standard_normal(burst)
    return np.clip(ts, 0, T)


def sim_net(ab, N, T, win_a, win_b, tau_m, vth, tref, w_exc, w_inh,
            rho, dens, burst, jitter, rng, dt=0.001):
    """Discrete-time recurrent LIF network. Each neuron has a fixed (chan_a, chan_b) sign
    pattern; bit a drives it in win_a via chan_a, bit b in win_b via chan_b (0=exc,1=inh).
    Recurrence: a spike at step t re-injects W_rec[j,k] into v[j] at step t+1 (SETRECUR-style).
    rho = spectral radius of W_rec (0 = feedforward). Returns spikes[N, n_trials] (spike times)."""
    patt = [SIGN_PATTERNS[i % len(SIGN_PATTERNS)] for i in range(N)]
    # recurrent weight matrix, scaled to spectral radius rho
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < dens)
    np.fill_diagonal(W, 0.0)
    sr = np.max(np.abs(np.linalg.eigvals(W))) if N > 1 else 0.0
    W = W * (rho / sr) if sr > 1e-9 else W * 0.0
    decay = np.exp(-dt / tau_m)
    nsteps = int(round(T / dt))
    out = np.empty((N, len(ab)), dtype=object)
    for bi, (a, b) in enumerate(ab):
        # build per-neuron injected-current time series
        jump = np.zeros((N, nsteps + 1))
        for j in range(N):
            ca, cb = patt[j]
            for act, ch, win in ((a, ca, win_a), (b, cb, win_b)):
                for t in _burst(act, win, burst, jitter, T, rng):
                    idx = min(nsteps, int(round(t / dt)))
                    jump[j, idx] += w_exc if ch == 0 else -w_inh
        v = np.zeros(N); last = np.full(N, -1e9)
        spikes = [[] for _ in range(N)]
        prev_spiked = np.zeros(N)
        for i in range(nsteps):
            t = i * dt
            v = v * decay + jump[:, i] + (W @ prev_spiked)
            v = np.maximum(v, 0.0)                       # rectify
            ref = (t - last) < tref
            v[ref] = 0.0
            fired = (v >= vth) & (~ref)
            for j in np.where(fired)[0]:
                spikes[j].append(t); last[j] = t
            v[fired] = 0.0
            prev_spiked = fired.astype(float)
        for j in range(N):
            out[j, bi] = np.array(spikes[j])
    return out


def score(sp, y, g, T):
    F = np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        if len(set(y[tr])) < 2:
            continue
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); accs.append(accuracy_score(y[te], c.predict(F[te])))
    return float(np.mean(accs)) if accs else float("nan"), sum(len(sp[j, b]) for j in range(sp.shape[0]) for b in range(sp.shape[1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--per-cell", type=int, default=20)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--tau-m", type=float, default=0.05, help="membrane tau (s); short vs gap")
    ap.add_argument("--tref", type=float, default=0.01)
    ap.add_argument("--w", type=float, default=0.5)
    ap.add_argument("--w-inh", type=float, default=0.5)
    ap.add_argument("--burst", type=int, default=8)
    ap.add_argument("--jitter", type=float, default=0.02)
    ap.add_argument("--dens", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    # windows: bit a early, bit b late, separated by a gap much larger than tau_m
    win_a = (0.2, 0.4)
    win_b_far = (1.5, 1.7)     # gap ~1.1s >> tau_m: memory REQUIRED
    win_b_near = (0.45, 0.65)  # gap ~0.05s ~ tau_m: memory NOT required (mechanism control)
    ab, g = make_txor_trials(args.per_cell, args.T, win_a, win_b_far, args.burst, args.jitter, rng)
    y_xor = (ab[:, 0] ^ ab[:, 1]).astype(int)
    y_or = (ab[:, 0] | ab[:, 1]).astype(int)

    print(f"Temporal-XOR SW: N={args.n}, tau_m={args.tau_m*1e3:.0f}ms, T={args.T}s, "
          f"burst={args.burst}, w={args.w}/{args.w_inh}")
    print(f"win_a={win_a} win_b_far={win_b_far} (gap~1.1s>>tau) | "
          f"win_b_near={win_b_near} (gap~tau)\n")
    print(f"{'condition':<26} {'rho':>4} {'XOR':>7} {'OR':>7} {'spikes':>8}")
    for label, win_b in (("FAR gap (memory needed)", win_b_far),
                         ("NEAR gap (memory not needed)", win_b_near)):
        for rho, role in ((0.0, "ff"), (1.2, "rec")):
            sp = sim_net(ab, args.n, args.T, win_a, win_b, args.tau_m, 1.0, args.tref,
                         args.w, args.w_inh, rho, args.dens, args.burst, args.jitter,
                         np.random.default_rng(args.seed + 100))
            axor, tot = score(sp, y_xor, g, args.T)
            aor, _ = score(sp, y_or, g, args.T)
            print(f"{label:<26} {role:>4} {axor:7.3f} {aor:7.3f} {tot:8d}")
    print("\nExpected: FAR gap -> ff XOR ~chance, rec XOR high (recurrence supplies the memory);")
    print("NEAR gap -> ff XOR already high (leaky membrane bridges the small gap).")


if __name__ == "__main__":
    raise SystemExit(main())
