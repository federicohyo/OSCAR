#!/usr/bin/env python3
"""Positive control: a task where dimensionality > 1 is PROVABLY required (XOR).

The ECG N/V task is threshold-solvable (1 bit/neuron ~ 0.94), so raising reservoir
dimensionality offers no gain there. Before concluding "dimensionality stays flat on
this chip", we must show our pipeline (D_eff + kernel scorer) CAN detect the benefit when
a task genuinely needs it. XOR is the textbook case: it needs more than one dimension, so no single
projection suffices, so a D_eff = 1 reservoir MUST fall short and a diverse one CAN succeed.

Design (hardware-mappable):
  - Each trial carries two bits (a, b), encoded as a burst of UP events in window A
    ([0.2,0.7]s) if a=1, and in window B ([1.0,1.5]s) if b=1. T = 2 s, like the ECG runs.
  - A bank of N LIF neurons integrates both windows. DIVERSITY is a spread of firing
    THRESHOLDS (vth) across neurons -- the on-chip analogue is a vthrdn ladder. A low-vth
    neuron computes ~OR (fires if either burst), a high-vth neuron computes ~AND (fires
    only if both). OR and AND together make XOR linearly separable.
  - Sweep the threshold spread 0 -> wide. Spread 0 = identical neurons = D_eff 1.

Tasks: XOR (needs dim>1), OR and AND (linearly separable, dim 1 suffices) as controls.
Same scorer as the hardware study: exp kernel K=8, 4 taus, StandardScaler + balanced
LogisticRegression(C=0.1). Grouped CV by a synthetic "record" so folds are honest.

    ./.venv-meas/bin/python3 reservoir_synthtask.py
"""
import argparse
import numpy as np
from reservoir_sw_lif import sim_lif
from reservoir_dimensionality import state_matrix, d_eff
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score

K, TAUS = 8, [0.04, 0.08, 0.16, 0.32]
# Both bits drive ONE coincident window so their bursts SUM on the membrane: the
# integrated drive is proportional to (a+b). That is what lets a threshold ladder
# compute OR (fire if a+b>=1) vs AND (fire only if a+b>=2), and hence XOR = OR AND NOT AND.
# If the two bits drove separate, well-separated windows they would sum below threshold
# and diversity would give XOR -- the design forces summation instead.
WIN = (0.35, 0.55)


def make_trials(n_per_cell, T, burst, jitter, rng):
    """Return (events_list, bits_ab, labels_dict, groups). Balanced over the 4 cells."""
    ev, ab, grp = [], [], []
    lo, hi = WIN
    for a in (0, 1):
        for b in (0, 1):
            for rep in range(n_per_cell):
                e = []
                for bit in (a, b):           # both bits deposit into the SAME window
                    if bit:
                        ts = rng.uniform(lo, hi, burst) + jitter * rng.standard_normal(burst)
                        e += [(float(np.clip(t, 0, T)) / T, 0) for t in ts]  # UP/exc
                ev.append(e)
                ab.append((a, b))
                grp.append(rep)              # group = repetition index, NOT the cell
    ab = np.array(ab)
    labels = {"XOR": (ab[:, 0] ^ ab[:, 1]),
              "OR":  (ab[:, 0] | ab[:, 1]),
              "AND": (ab[:, 0] & ab[:, 1])}
    # Group by repetition: every fold holds out one noisy repetition of ALL FOUR corners,
    # so all input patterns are in training and we test linear separability + noise
    # generalisation -- the correct "does the reservoir make XOR separable?" question.
    return ev, ab, labels, np.array(grp)


def simulate(ev, N, T, vth_spread, tau_m, tref, w, rng, vth0=1.0):
    """N LIF neurons, thresholds spread linearly by vth_spread (0 = identical)."""
    if N == 1 or vth_spread == 0:
        vths = np.full(N, vth0)
    else:
        vths = vth0 * (1.0 + vth_spread * np.linspace(-1, 1, N))
    vths = np.clip(vths, 0.2, None)
    sp = np.empty((N, len(ev)), dtype=object)
    for k in range(N):
        for bi, e in enumerate(ev):
            sp[k, bi] = sim_lif(e, T, tau_m, vths[k], 0.0, tref, w, w)
    return sp


def score(sp, y, g, feat="kernel", T=2.0):
    if feat == "kernel":
        F = np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])
    elif feat == "counts":
        F = np.array([[len(sp[i, b]) for i in range(sp.shape[0])] for b in range(sp.shape[1])], float)
    else:  # firebit
        F = np.array([[1.0 if len(sp[i, b]) else 0.0 for i in range(sp.shape[0])] for b in range(sp.shape[1])])
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        if len(set(y[tr])) < 2:            # a held-out cell can leave a single class in the split
            continue
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); accs.append(accuracy_score(y[te], c.predict(F[te])))
    return float(np.mean(accs)) if accs else float("nan")


SIGN_PATTERNS = [(0, 1), (1, 0), (0, 0)]   # (chan_a, chan_b): 0=exc, 1=inh -- matches HW


def signed_trial_events(a, b, chan_a, chan_b, T, burst, jitter, rng, win=(0.35, 0.55)):
    """One coincident window; bit a -> channel chan_a, bit b -> chan_b (0 exc, 1 inh).
    Mirrors reservoir_run_xor.py signed mode so the SW baseline uses the SAME mechanism."""
    lo, hi = win
    e = []
    for bit, ch in ((a, chan_a), (b, chan_b)):
        if bit:
            ts = rng.uniform(lo, hi, burst) + jitter * rng.standard_normal(burst)
            e += [(float(np.clip(t, 0, T)) / T, ch) for t in ts]
    return sorted(e, key=lambda x: x[0])


def simulate_signed(ab, N, T, tau_m, tref, w_exc, w_inh, burst, jitter, rng):
    """N LIF neurons, each with a fixed (chan_a, chan_b) sign pattern; identical LIF params
    (no mismatch). Diversity is the exc/inh routing of the two bits (a hardware projection)."""
    patt = [SIGN_PATTERNS[i % len(SIGN_PATTERNS)] for i in range(N)]
    sp = np.empty((N, len(ab)), dtype=object)
    for k in range(N):
        ca, cb = patt[k]
        for bi, (a, b) in enumerate(ab):
            ev = signed_trial_events(int(a), int(b), ca, cb, T, burst, jitter, rng)
            sp[k, bi] = sim_lif(ev, T, tau_m, 1.0, 0.0, tref, w_exc, w_inh)
    return sp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signed", action="store_true",
                    help="XOR via exc/inh signed routing (matches the on-chip mechanism), "
                         "instead of the threshold-ladder sweep.")
    ap.add_argument("--w-inh", type=float, default=0.34, help="inhibitory weight (signed mode)")
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--per-cell", type=int, default=20, help="trials per (a,b) cell")
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--burst", type=int, default=12, help="UP events per active window")
    ap.add_argument("--jitter", type=float, default=0.05, help="burst time jitter (s)")
    ap.add_argument("--tau-m", type=float, default=0.05)
    ap.add_argument("--tref", type=float, default=0.005)
    ap.add_argument("--w", type=float, default=0.34)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    ev, ab, labels, g = make_trials(args.per_cell, args.T, args.burst, args.jitter, rng)

    if args.signed:
        # Software mirror of the on-chip exc/inh XOR mechanism: identical neurons (matched
        # devices), diversity is the exc/inh routing of the two bits.
        sp = simulate_signed(ab, args.n, args.T, args.tau_m, args.tref,
                             args.w, args.w_inh, args.burst, args.jitter, rng)
        De = d_eff(state_matrix(sp, args.T))
        xk = score(sp, labels["XOR"], g, "kernel", args.T)
        xc = score(sp, labels["XOR"], g, "counts", args.T)
        print(f"SW signed exc/inh XOR (matches HW mechanism): {args.n} identical LIF, "
              f"burst={args.burst}, w_exc={args.w} w_inh={args.w_inh}")
        print(f"  D_eff = {De:.2f}/{args.n}   XOR kernel = {xk:.3f}   XOR counts = {xc:.3f}")
        print("  (identical neurons -> all dimensionality comes from exc/inh routing, "
              "not from mismatch)")
        return

    print(f"synthetic 2-bit task: {len(ev)} trials, {args.n} LIF neurons, "
          f"burst={args.burst}, tau_m={args.tau_m*1e3:.0f}ms, tref={args.tref*1e3:.0f}ms\n")
    print("Sweep threshold spread (diversity). Note vs XOR: OR/AND are linearly separable")
    print("(1 dimension suffices), XOR is not (needs >=2 diverse dimensions).\n")
    print(f"{'spread':>7s} {'D_eff':>6s} | "
          f"{'XOR_ker':>8s} {'XOR_cnt':>8s} {'XOR_bit':>8s} | "
          f"{'OR_ker':>7s} {'AND_ker':>8s}")
    for spread in (0.0, 0.1, 0.2, 0.4, 0.7):
        sp = simulate(ev, args.n, args.T, spread, args.tau_m, args.tref, args.w, rng)
        De = d_eff(state_matrix(sp, args.T))
        xk = score(sp, labels["XOR"], g, "kernel", args.T)
        xc = score(sp, labels["XOR"], g, "counts", args.T)
        xb = score(sp, labels["XOR"], g, "firebit", args.T)
        ok = score(sp, labels["OR"], g, "kernel", args.T)
        ak = score(sp, labels["AND"], g, "kernel", args.T)
        print(f"{spread:7.2f} {De:6.2f} | {xk:8.3f} {xc:8.3f} {xb:8.3f} | {ok:7.3f} {ak:8.3f}")

    print("\nExpected if the pipeline is sound: XOR accuracy is ~chance at spread 0 "
          "(D_eff~1) and rises with D_eff; OR/AND stay high throughout (dim 1 is enough).")


if __name__ == "__main__":
    main()
