#!/usr/bin/env python3
"""Validate the TEMPORAL-XOR TASK with a rate ESN before engineering the spiking/chip version.

Single input channel. Bit a -> a pulse in an early window, bit b -> a pulse in a late window,
separated by a gap. Label = a XOR b = "exactly one pulse". The readout reads only the FINAL
reservoir state (NOT a time-accumulator -- an accumulator would just count pulses and could
never do XOR anyway, but final-state makes the memory requirement explicit): to know XOR the
network must remember whether the EARLY window had a pulse when it reaches the end. With a
short leak, feedforward (rho=0) has forgotten the early pulse by the end -> chance on XOR.
Recurrence (rho>0) carries it -> XOR solvable by a linear readout. Sweep rho and leak.

If rec solves XOR and ff is at chance here, the task is valid; then we build the spiking
(self-latching SETRECUR) version toward the same regime."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold


def make_stream(n_per_cell, T, ta, tb, rng, amp=1.0, width=3):
    """(n,T,1) input: pulse of `width` frames at ta if a, at tb if b. Returns X, y_xor, y_or."""
    ab = []
    for a in (0, 1):
        for b in (0, 1):
            ab += [(a, b)] * n_per_cell
    ab = np.array(ab)
    X = np.zeros((len(ab), T, 1), np.float32)
    for i, (a, b) in enumerate(ab):
        if a:
            X[i, ta:ta + width, 0] += amp
        if b:
            X[i, tb:tb + width, 0] += amp
    return X, (ab[:, 0] ^ ab[:, 1]).astype(int), (ab[:, 0] | ab[:, 1]).astype(int)


def esn_final(X, N, rho, a_leak, in_scale, seed):
    """Reservoir final-state (last frame) features -> (n, N). No accumulator: pure memory test."""
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.2)
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    W = W * (rho / sr) if sr > 0 else W
    W_in = rng.standard_normal((N, 1)) * in_scale
    n, T, _ = X.shape
    out = np.zeros((n, N), np.float32)
    for i in range(n):
        x = np.zeros(N)
        for t in range(T):
            x = (1 - a_leak) * x + a_leak * np.tanh(W_in @ X[i, t] + W @ x)
        out[i] = x
    return out


def acc5(Z, y):
    Z = StandardScaler().fit_transform(Z)
    a = [(cross_val_predict(LogisticRegression(max_iter=3000, C=1.0), Z, y,
          cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean() for s in range(3)]
    return np.mean(a), np.std(a)


def main():
    T, ta, tb = 40, 4, 30           # early pulse frame 4, late pulse frame 30 (gap 26 frames)
    X, yx, yo = make_stream(40, T, ta, tb, np.random.default_rng(0))
    print(f"Temporal-XOR rate-ESN task: T={T}, pulse_a@{ta}, pulse_b@{tb} (gap {tb-ta} frames), "
          f"n={len(yx)}, final-state readout\n")
    print(f"{'a_leak':>7} {'rho':>5} | {'XOR':>13} {'OR':>13}")
    for a_leak in (0.3, 0.6, 1.0):
        for rho in (0.0, 0.9, 1.2, 1.5):
            zs = [esn_final(X, 64, rho, a_leak, 1.0, s) for s in range(3)]
            xr = np.mean([acc5(z, yx)[0] for z in zs]); xs = np.std([acc5(z, yx)[0] for z in zs])
            orr = np.mean([acc5(z, yo)[0] for z in zs])
            print(f"{a_leak:7.2f} {rho:5.1f} | {xr:.3f}+/-{xs:.3f}   {orr:.3f}")
    print("\nExpected: at short leak (a_leak high), rho=0 XOR ~0.5 (forgot early pulse), "
          "rho>0 XOR high; OR high throughout.")


if __name__ == "__main__":
    raise SystemExit(main())
