#!/usr/bin/env python3
"""Spiking chip-faithful NARMA + Memory-Capacity simulation, to (a) confirm a 16-NEURON SPIKING
reservoir can do NARMA (the rate ESN did; the chip is spiking with few neurons + count readout),
and (b) pre-find the operating point the on-chip BIAS TUNING must hit, expressed as the two RC
properties we can measure directly on silicon:

  Memory Capacity  MC = sum_k corr^2( linear readout of x(t) , u(t-k) )   [how far back it remembers]
  NARMA NRMSE      nonlinear temporal prediction (needs MC + nonlinearity)

Chip model: 16 LIF neurons, membrane state carried ACROSS frames (no reset = feedforward memory),
per-neuron input gain (device mismatch / bias spread), SETRECUR-style recurrence (neuron k fires
-> inject W_rec[j,k] next step; self-loops give sustained memory). Feature = per-frame SPIKE COUNT
per neuron (exactly what the chip's AER returns). Readout = ridge. Compares ff (no recurrence) vs
rec, and sweeps the knobs that map to biases: tau_m (vleakn/vtaun), input gain, recurrence gain.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np


def narma(u, n):
    y = np.zeros_like(u)
    for t in range(len(u) - 1):
        s = y[max(0, t - n + 1):t + 1].sum()
        y[t + 1] = (0.3 * y[t] + 0.05 * y[t] * s +
                    (1.5 * u[t - (n - 1)] * u[t] if t >= n - 1 else 0.0) + 0.1)
    return y


def run_reservoir(u, N, tau_m, vth, tref, in_gain, rho, dens, frame_steps, seed,
                  dt=1.0, w_in=1.0, self_frac=0.5, bias=0.0):
    """Spiking LIF reservoir over len(u) frames; returns per-frame spike counts (n_frames, N).
    Membrane carried across frames. Input u(t) injected as graded current in-frame, scaled by a
    per-neuron gain (mismatch). Recurrence W_rec scaled to spectral radius rho, with a fraction
    self_frac put on self-loops (sustained memory). rho=0 -> feedforward."""
    rng = np.random.default_rng(seed)
    gains = in_gain * (0.5 + rng.random(N))                 # per-neuron input diversity (mismatch)
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < dens)
    np.fill_diagonal(W, 0.0)
    sr = np.max(np.abs(np.linalg.eigvals(W))) if N > 1 else 0.0
    W = (W * (rho * (1 - self_frac) / sr)) if sr > 1e-9 else W * 0.0
    np.fill_diagonal(W, rho * self_frac)                    # excitatory self-loops = memory
    decay = np.exp(-dt / tau_m)
    v = np.zeros(N); last = np.full(N, -1e9); prev = np.zeros(N)
    counts = np.zeros((len(u), N))
    step = 0
    for t in range(len(u)):
        drive = bias + gains * u[t] * w_in                  # resting bias + input current this frame
        for _ in range(frame_steps):
            tt = step * dt
            v = v * decay + drive + W @ prev
            v = np.maximum(v, 0.0)
            ref = (tt - last) < tref
            v[ref] = 0.0
            fired = (v >= vth) & (~ref)
            counts[t, fired.nonzero()[0]] += 1
            v[fired] = 0.0
            last[fired] = tt
            prev = fired.astype(float)
            step += 1
    return counts


def nrmse(p, y):
    return np.sqrt(np.mean((p - y) ** 2) / (np.var(y) + 1e-12))


def ridge_fit(Xtr, ytr, lam=1e-3):
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ ytr)


def ridge_pred(W, X):
    return np.hstack([X, np.ones((len(X), 1))]) @ W


def memory_capacity(X, u, kmax, cut, wash=100):
    """MC_k = corr^2 between a linear readout of X and u(t-k); returns array over k and its sum.
    Train the readout on [wash, cut), test on [cut, end)."""
    mc = []
    for k in range(kmax + 1):
        tgt = np.roll(u, k)
        tgt[:k] = 0.0
        W = ridge_fit(X[wash:cut], tgt[wash:cut])
        p = ridge_pred(W, X[cut:])
        t = tgt[cut:]
        c = np.corrcoef(p, t)[0, 1]
        mc.append(0.0 if np.isnan(c) else c ** 2)
    return np.array(mc), float(np.sum(mc))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--L", type=int, default=2400)
    ap.add_argument("--frame-steps", type=int, default=20)
    ap.add_argument("--narma-n", type=int, default=2)
    args = ap.parse_args()
    rng = np.random.default_rng(0)
    u = rng.uniform(0, 0.5, args.L)
    y = narma(u, args.narma_n)
    cut = args.L // 2

    print(f"Spiking chip-sim: N={args.N}, frame_steps={args.frame_steps}, NARMA-{args.narma_n}, "
          f"L={args.L}. Per-frame spike-count features, ridge readout.\n")
    print(f"{'tau_m':>6} {'in_gain':>7} {'bias':>5} {'rho':>5} | {'sp/frm':>7} {'MC_sum':>7} | "
          f"{'NARMA NRMSE':>12}")
    for tau_m in (20.0, 40.0, 80.0):                    # in dt units; frame=20 -> tau ~1-4 frames
        for in_gain in (0.4, 0.8, 1.5):
            for bias in (0.02, 0.05):
              for rho in (0.0, 0.9):
                counts = run_reservoir(u, args.N, tau_m, 1.0, 2.0, in_gain, rho, 0.3,
                                       args.frame_steps, seed=1, bias=bias)
                spf = counts.sum() / args.L / args.N              # mean spikes per frame per neuron
                mc_k, mc = memory_capacity(counts, u, 15, cut)
                Wr = ridge_fit(counts[100:cut], y[100:cut])
                e = nrmse(ridge_pred(Wr, counts[cut:]), y[cut:])
                tag = "ff " if rho == 0 else "rec"
                print(f"{tau_m:6.0f} {in_gain:7.2f} {bias:5.2f} {tag:>5} | {spf:7.2f} {mc:7.2f} | {e:12.3f}")
    print("\nGoal: an operating point where rec has higher MC_sum AND lower NARMA NRMSE than ff, "
          "with neurons active but not saturated (meanHz in a mid band). That point's tau_m/gain/"
          "rho map to the bias targets (vleakn/vtaun, input weight, SETRECUR count).")


if __name__ == "__main__":
    raise SystemExit(main())
