#!/usr/bin/env python3
"""SW validation for NARMA on-chip: does a SELF-LOOP (diagonal-recurrence) reservoir — matching
the chip's time-multiplexed self-recurrent units (no cross-coupling) — have enough memory +
nonlinearity to do NARMA, and does recurrence beat feedforward? Bank of N leaky units with
DIVERSE leak/gain/self-weight, driven by a continuous u(t) stream; per-step state -> ridge -> y;
NRMSE, feedforward (self=0) vs recurrent (self>0). If rec NRMSE << ff, the on-chip plan is sound.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np


def narma(u, n):
    y = np.zeros_like(u)
    for t in range(len(u) - 1):
        s = y[max(0, t - n + 1):t + 1].sum()
        y[t + 1] = (0.3 * y[t] + 0.05 * y[t] * s +
                    (1.5 * u[t - (n - 1)] * u[t] if t >= n - 1 else 0.0) + 0.1)
    return y


def selfloop_states(u, N, self_w, seed, leak_lo=0.2, leak_hi=0.9):
    """N self-recurrent units, DIVERSE per unit: x_k(t)=(1-a_k)x_k(t-1)+a_k*tanh(g_k*u(t)+w_k*x_k(t-1)).
    self_w=0 -> feedforward (leaky only). HIGH leak (a->1) = short per-step memory (models a long
    on-chip timestep, membrane decays between steps -> ff forgets, only recurrence carries memory).
    Returns (len(u), N)."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(leak_lo, leak_hi, N)         # diverse leak (per-step decay)
    g = rng.uniform(0.5, 2.0, N)                 # diverse input gain
    w = self_w * rng.uniform(0.5, 1.0, N)        # diverse self-loop strength
    X = np.zeros((len(u), N)); x = np.zeros(N)
    for t in range(len(u)):
        x = (1 - a) * x + a * np.tanh(g * u[t] + w * x)
        X[t] = x
    return X


def nrmse(p, y):
    return np.sqrt(np.mean((p - y) ** 2) / (np.var(y) + 1e-12))


def ridge_eval(Xtr, ytr, Xte, yte, lam=1e-4):
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    W = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ ytr)
    return nrmse(np.hstack([Xte, np.ones((len(Xte), 1))]) @ W, yte)


def main():
    rng = np.random.default_rng(0); L, wash = 2400, 200
    u = rng.uniform(0, 0.5, L); cut = L // 2
    print("SW self-loop reservoir, N=13. NRMSE lower=better. Sweep leak regime (high leak = short")
    print("per-step ff memory = long on-chip timestep). rec helps only when ff is memory-limited.\n")
    for leak_lo, leak_hi, tag in ((0.2, 0.9, "slow leak (long ff memory)"),
                                  (0.6, 0.95, "medium"),
                                  (0.85, 0.99, "fast leak (short ff memory ~ long timestep)")):
        print(f"--- {tag}  a in [{leak_lo},{leak_hi}] ---")
        print(f"{'NARMA-n':>8} | {'ff NRMSE':>16} {'rec NRMSE':>16} {'improve':>8}")
        for n in (2, 5, 10):
            y = narma(u, n)
            ff, rc = [], []
            for s in range(4):
                Xff = selfloop_states(u, 13, 0.0, s, leak_lo, leak_hi)
                Xrc = selfloop_states(u, 13, 1.2, s, leak_lo, leak_hi)
                ff.append(ridge_eval(Xff[wash:cut], y[wash:cut], Xff[cut:], y[cut:]))
                rc.append(ridge_eval(Xrc[wash:cut], y[wash:cut], Xrc[cut:], y[cut:]))
            fm, rm = np.mean(ff), np.mean(rc)
            print(f"{n:8d} | {fm:.3f} +/- {np.std(ff):.3f}   {rm:.3f} +/- {np.std(rc):.3f}   "
                  f"{(fm-rm)/fm*100:+5.0f}%")
        print()
    print("Pick the regime where rec NRMSE << ff -> that's the on-chip timestep/leak operating point.")


if __name__ == "__main__":
    raise SystemExit(main())
