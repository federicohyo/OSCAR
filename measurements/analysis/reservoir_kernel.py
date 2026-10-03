#!/usr/bin/env python3
"""Offline readout-kernel sweep on recorded raw reservoir spikes.

Builds linear-readout features by convolving each neuron's output spike train with a
kernel and sampling it at K points, then sweeps kernel SHAPE (exp / gauss / ricker
[Mexican-hat] / box) and time-constant tau -- entirely offline, no hardware. Reports
mean accuracy under inter-patient (record-wise) cross-validation with repeats.

  python reservoir_kernel.py --npz reservoir_spikes_nv_delta.npz
"""

import argparse
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (StratifiedKFold, StratifiedGroupKFold,
                                     cross_val_predict)
from sklearn.metrics import accuracy_score, f1_score

SEEDS = [0, 1, 2, 3, 4]


def build_features(spikes, T, K, shape, tau):
    """spikes: object array (n_neurons, n_beats) of spike-time arrays -> (n_beats, n_neurons*K)."""
    n_neu, n_beats = spikes.shape
    tk = (np.arange(K) + 0.5) * T / K
    F = np.zeros((n_beats, n_neu * K))
    for j in range(n_neu):
        for b in range(n_beats):
            st = np.asarray(spikes[j, b], dtype=float)
            if st.size == 0:
                continue
            d = tk[:, None] - st[None, :]              # (K, nspikes), time since each spike
            if shape == "exp":
                k = np.where(d >= 0, np.exp(-d / tau), 0.0)
            elif shape == "gauss":
                k = np.exp(-(d ** 2) / (2 * tau ** 2))
            elif shape == "ricker":                    # Mexican hat (DoG)
                k = (1 - (d / tau) ** 2) * np.exp(-(d ** 2) / (2 * tau ** 2))
            elif shape == "box":
                k = (np.abs(d) <= tau / 2).astype(float)
            else:
                raise ValueError(shape)
            F[b, j * K:(j + 1) * K] = k.sum(axis=1)
    return F


def cv_acc(X, y, groups, mode):
    accs = []
    for seed in SEEDS:
        clf = make_pipeline(StandardScaler(),
                            LogisticRegression(max_iter=5000, class_weight="balanced"))
        if mode == "beat" or groups is None:
            cv = StratifiedKFold(5, shuffle=True, random_state=seed)
            pred = cross_val_predict(clf, X, y, cv=cv)
        else:
            ng = len(np.unique(groups))
            cv = StratifiedGroupKFold(min(5, ng), shuffle=True, random_state=seed)
            pred = cross_val_predict(clf, X, y, cv=cv, groups=groups)
        accs.append(accuracy_score(y, pred))
    return float(np.mean(accs)), float(np.std(accs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_delta.npz")
    ap.add_argument("--K", type=int, default=8, help="samples per neuron")
    ap.add_argument("--shapes", default="exp,gauss,ricker,box")
    ap.add_argument("--taus", default="0.02,0.04,0.08,0.16,0.32", help="tau (s)")
    ap.add_argument("--mode", default="patient", choices=["patient", "beat"])
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y = d["spikes"], d["labels"]
    T = float(d["T"]); groups = d["records"] if "records" in d else None
    tot = sum(len(np.asarray(spikes[j, b])) for j in range(spikes.shape[0])
              for b in range(spikes.shape[1]))
    print(f"{args.npz}: {spikes.shape[0]} neurons x {spikes.shape[1]} beats, "
          f"{tot} spikes, coding={d['coding']}, classes {np.bincount(y)}, CV={args.mode}")

    taus = [float(x) for x in args.taus.split(",")]
    shapes = args.shapes.split(",")
    print(f"\n{'shape':>8} | " + " ".join(f"tau={t*1000:>4.0f}ms" for t in taus))
    best = (0, None)
    for shape in shapes:
        row = []
        for tau in taus:
            X = build_features(spikes, T, args.K, shape, tau)
            m, s = cv_acc(X, y, groups, args.mode)
            row.append(f"{m:.3f}")
            if m > best[0]:
                best = (m, (shape, tau))
        print(f"{shape:>8} | " + "   ".join(f"{v:>8}" for v in row))
    print(f"\nbest: acc={best[0]:.3f} at shape={best[1][0]} tau={best[1][1]*1000:.0f}ms "
          f"({args.mode} CV, {len(SEEDS)} repeats)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
