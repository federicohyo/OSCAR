#!/usr/bin/env python3
"""Per-class metrics and a majority-class floor for a recorded reservoir dataset.

Accuracy alone hides two things on these beat sets. They are class-balanced by construction,
so the majority-class floor is 1/n_classes -- worth printing, because a reader cannot infer it
from an accuracy number alone and inter-patient folds are *not* balanced within a held-out
record. And a three-class macro accuracy can sit comfortably above chance while one class is
never predicted at all, which sensitivity and PPV expose immediately.

Deliberately separate from reservoir_analysis.py / reservoir_frontier.py: those reproduce the
manuscript's numbers and are not to be perturbed. This only adds columns beside them, using
the same features, the same read-out and the same leave-one-record-out protocol.

    ./.venv-meas/bin/python3 reservoir_class_metrics.py \
        --npz data/ecg25/reservoir_spikes_nv_delta_25mhz.npz --tau 0.08
"""

import argparse
import collections
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from reservoir_kernel import build_features


def clf():
    return make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=5000, class_weight="balanced"))


def loro_predictions(F, y, g):
    """Out-of-fold predictions under leave-one-record-out, plus per-record accuracy."""
    pred = np.empty_like(y)
    per_record = {}
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = clf().fit(F[tr], y[tr])
        p = c.predict(F[te])
        pred[te] = p
        per_record[str(g[te][0])] = float(accuracy_score(y[te], p))
    return pred, per_record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True)
    ap.add_argument("--tau", type=float, default=0.08, help="read-out kernel time constant")
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--shape", default="exp")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes = d["spikes"]
    y = np.asarray(d["labels"])
    g = np.asarray(d["records"])
    T = float(d["T"])
    names = {2: ["N", "V"], 3: ["N", "S", "V"]}.get(len(np.unique(y)),
                                                    [str(i) for i in np.unique(y)])

    F = build_features(spikes, T, args.K, args.shape, args.tau)
    pred, per_record = loro_predictions(F, y, g)

    counts = collections.Counter(y.tolist())
    majority = max(counts.values()) / len(y)
    cm = confusion_matrix(y, pred, labels=sorted(counts))

    print(f"=== {args.npz} ===")
    print(f"  {len(y)} beats, classes {dict(counts)}, kernel {args.shape} tau={args.tau}")
    print(f"  overall LORO accuracy      : {accuracy_score(y, pred):.3f}")
    print(f"  majority-class floor       : {majority:.3f}  "
          f"(balanced by construction; per-record folds are not)")
    print(f"  per-record accuracy        : "
          f"{np.mean(list(per_record.values())):.3f} +/- {np.std(list(per_record.values())):.3f}")
    print("\n  class   support   sensitivity      PPV")
    per_class = {}
    for i, lab in enumerate(sorted(counts)):
        tp = cm[i, i]
        support = cm[i].sum()
        predicted = cm[:, i].sum()
        # Sensitivity is undefined with no true instances, PPV with no predictions; a class
        # that is never predicted is exactly what this table exists to make visible.
        sens = tp / support if support else float("nan")
        ppv = tp / predicted if predicted else float("nan")
        per_class[names[i]] = {"support": int(support), "predicted": int(predicted),
                               "sensitivity": float(sens), "ppv": float(ppv)}
        ppv_s = f"{ppv:.3f}" if predicted else "  n/a (never predicted)"
        print(f"  {names[i]:>5}   {support:7d}       {sens:.3f}   {ppv_s}")

    print("\n  confusion matrix (rows = true, cols = predicted):")
    print("        " + "".join(f"{n:>6}" for n in names))
    for i, n in enumerate(names):
        print(f"  {n:>5} " + "".join(f"{v:6d}" for v in cm[i]))

    doc = {"npz": args.npz, "tau": args.tau, "K": args.K, "shape": args.shape,
           "accuracy": float(accuracy_score(y, pred)), "majority_floor": float(majority),
           "per_record": per_record, "per_class": per_class,
           "confusion": cm.tolist(), "class_names": names}
    if "prov_clk_mhz" in d.files:
        doc["prov"] = {k: d[k].item() for k in d.files if k.startswith("prov_")}
    if args.out:
        with open(args.out, "w") as f:
            json.dump(doc, f, indent=2)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
