#!/usr/bin/env python3
"""Ceiling probe (NEXT_STEPS_ACCURACY.md sec.3) + RR-feature test (sec.4-A1) on the
3-class N/S/V task, all offline on existing spikes.

Answers two questions, apples-to-apples (identical split, RR given to raw too):
  (1) CEILING PROBE: does a strong NONLINEAR classifier on the reservoir states beat
      raw ECG?  beats -> info is present, fix the READOUT; doesn't -> info MISSING, fix
      the REPRESENTATION.
  (2) RR FEATURES: do de-Chazal RR/rhythm features lift accuracy on S, and does the
      reservoir add anything on top of raw+RR?  Win condition: res+RR > raw+RR.

Primary metric: inter-patient (leave-one-record-out) macro-F1 + per-class F1 (S is the
failure mode). Beat-level is leakage-prone; inter-patient is the honest number.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_kernel import build_features
from reservoir_data import get_beats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]
K = 8
CLASS_NAMES = ["N", "S", "V"]


def bank(sp, T):
    return np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])


def lin():
    return make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))


def rf():
    return RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=0)


def mlp():
    return make_pipeline(StandardScaler(),
                         MLPClassifier(hidden_layer_sizes=(64,), max_iter=3000, random_state=0))


CLFS = {"linear": lin, "rf": rf, "mlp": mlp}


def loro(F, y, g, clf_factory):
    """Inter-patient LORO: per-fold acc & macro-F1 (mean/sd) + pooled per-class F1."""
    yhat = np.empty_like(y)
    accs, f1s = [], []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = clf_factory(); c.fit(F[tr], y[tr]); p = c.predict(F[te])
        yhat[te] = p
        accs.append(accuracy_score(y[te], p))
        f1s.append(f1_score(y[te], p, average="macro"))
    perclass = f1_score(y, yhat, average=None)
    return np.mean(accs), np.std(accs), np.mean(f1s), np.std(f1s), perclass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shared", default="reservoir_spikes_nsv_delta_fresh.npz")
    ap.add_argument("--proj", default="reservoir_spikes_nsv_randproj_tuned2.npz")
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--clfs", default="linear,rf,mlp")
    args = ap.parse_args()

    ds = np.load(args.shared, allow_pickle=True)
    dp = np.load(args.proj, allow_pickle=True)
    y = ds["labels"]; g = np.asarray(ds["records"]); T = float(ds["T"])
    assert np.array_equal(y, dp["labels"]), "shared/proj beat mismatch"
    Xr, yr, meta = get_beats(records=tuple(args.records.split(",")),
                             n_per_class=args.n_per_class, classes="NSV")
    assert np.array_equal(yr, y), "raw loader order mismatch"
    RR = meta["rr"]
    print(f"=== N/S/V ceiling probe + RR (inter-patient LORO), {len(y)} beats, "
          f"classes {np.bincount(y)}, RR={meta['rr_names']} ===")

    Bs, Bp = bank(ds["spikes"], T), bank(dp["spikes"], T)
    feats = {
        "RR-only":        RR,
        "raw":            Xr,
        "raw + RR":       np.hstack([Xr, RR]),
        "res-shared":     Bs,
        "res-shared + RR": np.hstack([Bs, RR]),
        "res-proj":       Bp,
        "res-proj + RR":  np.hstack([Bp, RR]),
        "res-both":       np.hstack([Bs, Bp]),
        "res-both + RR":  np.hstack([Bs, Bp, RR]),
    }
    clfs = [c for c in args.clfs.split(",") if c in CLFS]
    for clf in clfs:
        print(f"\n--- classifier: {clf} ---   (acc | macro-F1 | per-class F1 N/S/V)")
        for name, F in feats.items():
            a, asd, f, fsd, pc = loro(F, y, g, CLFS[clf])
            print(f"  {name:16s} acc={a:.3f}±{asd:.3f}  macroF1={f:.3f}±{fsd:.3f}  "
                  f"F1[N/S/V]={pc[0]:.2f}/{pc[1]:.2f}/{pc[2]:.2f}")
    print("\nKEY: ceiling probe = does rf/mlp on res-* beat raw? "
          "win = res+RR macroF1 > raw+RR macroF1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
