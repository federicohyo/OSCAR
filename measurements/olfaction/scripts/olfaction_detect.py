#!/usr/bin/env python3
"""Accuracy versus latency for both substrates -- on odour DETECTION, not phase.

Why detection rather than corr/acorr. A window shorter than one modulation period is too short to
contain a phase relationship, so the corr/acorr task has a hard latency floor at ~1
period (100 ms at 10 Hz) and "decide faster, then average" stays out of reach for it. That is
a property of the task definition rather than any substrate, and the sliding-window
attempt duly returned chance at every window length.

Detection avoids that floor. "Is this odour open right now" is answerable from a short
causal window, the olfactometer's valve trace gives per-sample ground truth at 1 kHz,
and it is what a filament-tracking nose actually computes. So the accuracy-latency
trade-off is real here and can be measured.

The two substrates pay for that trade-off differently, which is the whole argument:

    ARRAY    P_analog x T + read-out. Continuous power, so making MORE decisions in a
             given time costs nothing extra -- averaging is free.
    DIGITAL  E_OP3 per decision. Averaging k decisions costs k times as much.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_detect.py

HONESTY NOTES. (1) Windows from one trial are correlated, so they stay in one CV
fold and the k-averaged column is an UPPER bound. (2) E_OP3 is the ECG tree kernel; a
task-matched count under op3_count.py discipline is owed before any of this is quoted.
"""
import argparse
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FS, T0 = 1000.0, -1.0
P_ANALOG_W, E_CYCLE_J = 0.43e-3, 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480
E_OP3_J = 55328 * E_CYCLE_J


def build(X, V, t, wl_s, vcol, stim=(0.05, 0.95), max_per_trial=40, seed=0):
    """Causal windows ending at the decision time; label = valve state at that time."""
    rng = np.random.default_rng(seed)
    w = int(wl_s * FS)
    base = X[:, t < -0.05, :].mean(axis=1, keepdims=True)
    R = (X - base) / np.abs(base)
    ok = np.flatnonzero((t >= stim[0]) & (t <= stim[1]))
    ok = ok[ok >= w]
    F, Y, G = [], [], []
    for i in range(len(X)):
        idx = rng.choice(ok, size=min(max_per_trial, len(ok)), replace=False)
        for a in idx:
            seg = R[i, a - w:a, :]
            # Remove the WINDOW mean per channel. This keeps the features from being the
            # slow response envelope, which is near-constant inside a 5-100 ms window
            # and carries nothing about the instantaneous valve state. Keep the
            # derivative too: the sensor lags, so the slope leads the level.
            seg = seg - seg.mean(0, keepdims=True)
            step = max(1, w // 16)
            sh = seg[::step][:16]
            dv = np.diff(seg, axis=0)[::step][:16]
            F.append(np.concatenate([sh.ravel(), dv.ravel()]))
            Y.append(1 if V[i, a, vcol] > 0.01 else 0)
            G.append(i)
    n = min(len(f) for f in F)
    return np.array([f[:n] for f in F]), np.array(Y), np.array(G)


def score(F, y, groups, pair_of):
    accs = []
    gp = np.array([pair_of[g] for g in groups])
    for tr, te in LeaveOneGroupOut().split(F, y, gp):
        if len(np.unique(y[tr])) < 2 or len(np.unique(y[te])) < 2:
            continue
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, class_weight="balanced", max_iter=3000))
        m.fit(F[tr], y[tr])
        accs.append((m.predict(F[te]) == y[te]).mean())
    return (float(np.mean(accs)), float(np.std(accs))) if accs else (np.nan, np.nan)


def k_average(p, k):
    from math import comb
    p = min(max(p, 1e-6), 1 - 1e-6)
    s = sum(comb(k, i) * p**i * (1 - p)**(k - i) for i in range(k // 2 + 1, k + 1))
    if k % 2 == 0:
        s += 0.5 * comb(k, k // 2) * p**(k // 2) * (1 - p)**(k // 2)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="data_olfaction/olfaction_stream.npz")
    ap.add_argument("--freqs", default="5Hz,10Hz,20Hz,40Hz,60Hz")
    ap.add_argument("--events", type=float, default=20.0)
    ap.add_argument("--out", default="data/olfaction_detect.json")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    X, V, meta = d["X"], d["V"], d["meta"]
    valves = list(d["valves"])
    t = np.arange(X.shape[1]) / FS + T0
    freqs = np.array([m[1] for m in meta])
    pair = {i: f"{min(m[2],m[3])}|{max(m[2],m[3])}" for i, m in enumerate(meta)}

    e_read = (DRAIN_FIXED + args.events * DRAIN_MARGINAL) * E_CYCLE_J
    print(f"valves {valves} | array read-out {e_read*1e6:.1f} uJ/decision, "
          f"OP3 {E_OP3_J*1e6:.1f} uJ/decision\n")
    res = {}
    for f in args.freqs.split(","):
        m = np.flatnonzero(freqs == f)
        g1 = [v for v in valves if v == meta[m[0]][2]]
        if not g1:
            continue
        vcol = valves.index(g1[0])
        print(f"--- {f}: detect '{g1[0]}' open, {len(m)} trials ---")
        print(f"{'window':>8} {'rate':>8} {'acc':>16} {'k=5 (UB)':>10} "
              f"{'E_array':>10} {'E_OP3':>9} {'ratio':>7}")
        res[f] = {}
        for wl in (0.005, 0.010, 0.020, 0.050, 0.100):
            F, y, G = build(X[m], V[m], t, wl, vcol)
            po = {i: pair[m[i]] for i in range(len(m))}
            a, s = score(F, y, G, po)
            if np.isnan(a):
                continue
            e_arr = P_ANALOG_W * wl + e_read
            print(f"{wl*1000:7.0f}m {1/wl:7.0f}/s {a:9.3f} +/- {s:.3f} "
                  f"{k_average(a,5):10.3f} {e_arr*1e6:9.1f}u {E_OP3_J*1e6:8.1f}u "
                  f"{E_OP3_J/e_arr:6.2f}x")
            res[f][str(wl)] = {"acc": a, "sd": s, "rate_hz": 1/wl,
                               "E_array_J": e_arr, "E_op3_J": E_OP3_J,
                               "advantage": E_OP3_J/e_arr}
        print()
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
