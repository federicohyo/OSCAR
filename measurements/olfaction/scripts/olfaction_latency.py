#!/usr/bin/env python3
"""Accuracy versus latency, and the energy that follows -- the olfactory cost frontier.

F. Corradi's reframing, 2026-08-13, and it is the right one. Asking "is the task
solvable at 21 decisions/s" was the wrong question. The right one is a TRADE-OFF:

    a short decision window is cheap and inaccurate; a long one is accurate and slow.

and the two substrates pay for it completely differently:

    ARRAY    energy = P_analog x T  + read-out.  Averaging k decisions costs the same
             as one decision over the same total time -- the array is burning
             continuous power either way, so repetition is FREE to it.
    DIGITAL  energy = k x E_OP3.  Every decision is a full kernel run, so averaging k
             of them costs k times as much.

That asymmetry is the entire cost argument, and it is why the comparison has to be
made AT MATCHED ACCURACY rather than at a fixed decision rate. If the array reaches a
given accuracy with short windows and averaging, it wins even where a single one of
its decisions is worse than a single digital one.

So: sweep the decision window, measure accuracy, and price both substrates at each
point using the constants the reference analysis already pins.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_latency.py

CAVEAT held throughout: windows drawn from one trial are NOT independent, so they stay
in one CV fold, and the averaging-over-k model below assumes independence it does not
have. The k-averaged accuracies are therefore an UPPER bound on what averaging buys,
and are labelled as such.
"""
import argparse
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FS = 1000.0
T0 = -1.0

# from measurements/plotting/constants.py -- the same numbers the cost frontier uses
P_ANALOG_W = 0.43e-3
E_CYCLE_J = 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480
E_OP3_J = 55328 * E_CYCLE_J          # the ECG tree kernel; a task-matched count is owed


def windows(X, V, t, wlen_s, stride_s, stim=(0.05, 0.95)):
    """Chop each trial into causal windows inside the stimulus, keeping the trial index
    so that CV can hold all windows of a trial together."""
    n, _, C = X.shape
    w = int(wlen_s * FS)
    s = max(1, int(stride_s * FS))
    starts = [i for i in range(0, len(t) - w)
              if stim[0] <= t[i] and t[i + w] <= stim[1]]
    starts = starts[::s]
    if not starts:
        return None, None, None
    F, trial = [], []
    base = X[:, t < -0.05, :].mean(axis=1, keepdims=True)
    R = (X - base) / np.abs(base)
    for i in range(n):
        for a in starts:
            seg = R[i, a:a + w, :]
            # cheap, causal, fixed-size descriptor: mean, slope and range per channel
            F.append(np.concatenate([seg.mean(0), seg[-1] - seg[0], seg.ptp(0)]))
            trial.append(i)
    return np.array(F), np.array(trial), len(starts)


def score(F, y, groups):
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, y, groups):
        if len(np.unique(y[tr])) < 2:
            continue
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, class_weight="balanced", max_iter=4000))
        m.fit(F[tr], y[tr])
        accs.append((m.predict(F[te]) == y[te]).mean())
    return float(np.mean(accs)), float(np.std(accs))


def k_average(acc, k):
    """Accuracy of a majority vote over k INDEPENDENT decisions of accuracy `acc`.
    Independence is false here (same trial), so this is an upper bound."""
    from math import comb
    p = min(max(acc, 1e-6), 1 - 1e-6)
    return sum(comb(k, i) * p**i * (1 - p)**(k - i) for i in range((k // 2) + 1, k + 1)) \
        + (0.5 * comb(k, k // 2) * p**(k // 2) * (1 - p)**(k // 2) if k % 2 == 0 else 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="data_olfaction/olfaction_stream.npz")
    ap.add_argument("--freqs", default="5Hz,10Hz,20Hz")
    ap.add_argument("--events-per-decision", type=float, default=20.0)
    ap.add_argument("--out", default="data/olfaction_latency.json")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    X, y, meta = d["X"], d["y"], d["meta"]
    V = d["V"] if "V" in d.files else None
    t = np.arange(X.shape[1]) / FS + T0
    freqs = np.array([m[1] for m in meta])
    pair = np.array([f"{min(m[2],m[3])}|{max(m[2],m[3])}" for m in meta])

    e_read = (DRAIN_FIXED + args.events_per_decision * DRAIN_MARGINAL) * E_CYCLE_J
    print(f"array read-out {e_read*1e6:.1f} uJ/decision at {args.events_per_decision:.0f} events; "
          f"OP3 {E_OP3_J*1e6:.1f} uJ/decision\n")

    res = {}
    for f in args.freqs.split(","):
        m = freqs == f
        print(f"--- {f} ({m.sum()} trials) ---")
        print(f"{'window':>8} {'rate':>7} {'n win':>6} {'acc/decision':>14} "
              f"{'acc, k=5 (UB)':>14} {'E_array':>10} {'E_OP3':>10}")
        res[f] = {}
        for wl in (0.010, 0.020, 0.050, 0.100, 0.200, 0.400):
            F, trial, nw = windows(X[m], None, t, wl, wl)
            if F is None:
                continue
            yy = y[m][trial]
            gg = pair[m][trial]
            a, s = score(F, yy, gg)
            ub = k_average(a, 5)
            e_arr = P_ANALOG_W * wl + e_read
            print(f"{wl*1000:7.0f}m {1/wl:6.0f}/s {nw:6d} {a:9.3f} +/- {s:.3f} "
                  f"{ub:14.3f} {e_arr*1e6:9.1f}u {E_OP3_J*1e6:9.1f}u")
            res[f][f"{wl}"] = {"acc": a, "sd": s, "acc_k5_upper": ub,
                               "rate_hz": 1 / wl, "n_windows": nw,
                               "E_array_J": e_arr, "E_op3_J": E_OP3_J}
        print()
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
