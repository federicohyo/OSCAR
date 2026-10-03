#!/usr/bin/env python3
"""Regenerate the three readout operating points in main.tex Table tab:resproj for each
feature source: accuracy-optimal (single long tau), dimensionality-optimal (single short
tau), and the JOINT multi-tau readout bank (nested leave-one-record-out CV over C).

Inter-patient = leave-one-record-out (LORO). eff-dim = participation ratio of the
standardised feature covariance. Run in .venv-meas.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut, GridSearchCV
from sklearn.metrics import accuracy_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]
CGRID = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
K = 8

SOURCES = [
    ("HW array, shared input", "reservoir_spikes_nv_delta.npz"),
    ("HW array, +projection",  "reservoir_spikes_nv_randproj.npz"),
    ("SW LIF, +projection",    "sw_proj.npz"),
    ("SW LIF, shared input",   "sw_shared.npz"),
]


def mk(C=1.0):
    return make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=5000, class_weight="balanced", C=C))


def loro(X, y, g, C=1.0):
    a = []
    for tr, te in LeaveOneGroupOut().split(X, y, g):
        c = mk(C); c.fit(X[tr], y[tr]); a.append(accuracy_score(y[te], c.predict(X[te])))
    return float(np.mean(a)), float(np.std(a))


def effdim(X):
    ev = np.clip(np.linalg.eigvalsh(np.cov(StandardScaler().fit_transform(X).T)), 0, None)
    return float((ev.sum() ** 2) / np.square(ev).sum())


def nested_bank(sp, T, y, g):
    """Multi-tau bank + nested-LORO C selection. Returns acc mean/std and bank eff-dim."""
    Xb = np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])
    accs = []
    for tr, te in LeaveOneGroupOut().split(Xb, y, g):
        gs = GridSearchCV(mk(), {"logisticregression__C": CGRID},
                          cv=LeaveOneGroupOut(), scoring="accuracy")
        gs.fit(Xb[tr], y[tr], groups=g[tr])
        accs.append(accuracy_score(y[te], gs.predict(Xb[te])))
    return float(np.mean(accs)), float(np.std(accs)), effdim(Xb)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="*", help="override npz list")
    args = ap.parse_args()
    srcs = SOURCES
    print(f"{'source':24s} | acc-opt (tau)        dim | JOINT bank         dim | dim-opt (tau)       acc")
    for name, npz in srcs:
        d = np.load(npz, allow_pickle=True)
        sp, y, g, T = d["spikes"], d["labels"], np.asarray(d["records"]), float(d["T"])
        rows = []
        for tau in TAUS:
            X = build_features(sp, T, K, "exp", tau)
            m, s = loro(X, y, g); rows.append((tau, m, s, effdim(X)))
        ao = max(rows, key=lambda r: r[1])   # accuracy-optimal
        do = max(rows, key=lambda r: r[3])   # dimensionality-optimal
        jm, js, jd = nested_bank(sp, T, y, g)
        print(f"{name:24s} | {ao[1]:.3f}+/-{ao[2]:.3f} ({ao[0]*1e3:.0f}) {ao[3]:4.1f} "
              f"| {jm:.3f}+/-{js:.3f} {jd:4.1f} "
              f"| {do[3]:4.1f} ({do[0]*1e3:.0f}) {do[1]:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
