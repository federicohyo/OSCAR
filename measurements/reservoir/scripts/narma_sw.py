#!/usr/bin/env python3
"""NARMA: the canonical reservoir-computing MEMORY benchmark, as the clean recurrence positive
control. The target y(t) depends on the last n inputs/outputs, so predicting it from the input
stream u(t) with a LINEAR readout PROVABLY requires memory: a feedforward (memoryless / short-
leak) reservoir cannot, a recurrent one can. Regression metric = NRMSE (lower is better).

NARMA-n:  y(t+1) = 0.3 y(t) + 0.05 y(t) * sum_{i=0}^{n-1} y(t-i) + 1.5 u(t-(n-1)) u(t) + 0.1
u(t) ~ U[0, 0.5]. (n=2 is the simplest; n=10 the classic.)

Shows NRMSE(recurrent) << NRMSE(feedforward), and the gap widens with memory order n. If this
holds, NARMA is the on-chip recurrence task: stream u(t) to the chip, read spike features per
step, ridge readout, compare RECURCTRL 0 (ff) vs SETRECUR (rec)."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np


def narma(u, n):
    y = np.zeros_like(u)
    for t in range(len(u) - 1):
        lo = max(0, t - n + 1)
        s = y[lo:t + 1].sum()
        y[t + 1] = 0.3 * y[t] + 0.05 * y[t] * s + 1.5 * u[t - (n - 1)] * u[t] + 0.1 if t >= n - 1 \
            else 0.3 * y[t] + 0.05 * y[t] * s + 0.1
    return y


def esn_states(u, N, rho, a_leak, in_scale, seed):
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.2)
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    W = W * (rho / sr) if sr > 0 else W
    W_in = rng.standard_normal((N, 1)) * in_scale
    x = np.zeros(N); X = np.zeros((len(u), N))
    for t in range(len(u)):
        x = (1 - a_leak) * x + a_leak * np.tanh(W_in[:, 0] * u[t] + W @ x)
        X[t] = x
    return X


def nrmse(pred, targ):
    return np.sqrt(np.mean((pred - targ) ** 2) / (np.var(targ) + 1e-12))


def ridge_eval(Xtr, ytr, Xte, yte, lam=1e-6):
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
    W = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ ytr)
    Bte = np.hstack([Xte, np.ones((len(Xte), 1))])
    return nrmse(Bte @ W, yte)


def main():
    rng = np.random.default_rng(0)
    L, wash = 3000, 200
    print("NARMA memory benchmark (rate ESN, N=64, ridge readout). NRMSE lower=better.\n")
    print(f"{'NARMA-n':>8} {'a_leak':>7} | {'ff NRMSE':>18} {'rec NRMSE':>18} {'improve':>8}")
    for n in (2, 5, 10):
        u = rng.uniform(0, 0.5, L)
        y = narma(u, n)
        cut = L // 2
        for a_leak in (0.3, 0.7):
            ff, rc = [], []
            for s in range(4):
                for rho, bucket in ((0.0, ff), (0.95, rc)):
                    X = esn_states(u, 64, rho, a_leak, 1.0, s)
                    e = ridge_eval(X[wash:cut], y[wash:cut], X[cut:], y[cut:])
                    bucket.append(e)
            fm, rm = np.mean(ff), np.mean(rc)
            print(f"{n:8d} {a_leak:7.2f} | {fm:.3f}+/-{np.std(ff):.3f}      "
                  f"{rm:.3f}+/-{np.std(rc):.3f}      {(fm-rm)/fm*100:+6.0f}%")
    print("\nExpected: recurrent NRMSE well below feedforward, gap widening with n "
          "(more memory needed). This is the textbook memory result -> valid recurrence control.")


if __name__ == "__main__":
    raise SystemExit(main())
