#!/usr/bin/env python3
"""Phase-1 reservoir readout: train a linear classifier on the reservoir states and
compare to a raw-ECG baseline. Proves the analog reservoir makes the temporal beat
classification linearly separable.
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (StratifiedKFold, StratifiedGroupKFold,
                                     cross_val_predict)
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.decomposition import PCA

matplotlib.rcParams.update({"pdf.fonttype": 42, "font.size": 9})

SEEDS = [0, 1, 2, 3, 4]  # repeats for mean +/- std


def _one(X, y, groups, mode, seed):
    """One CV pass. mode='beat' -> stratified beat-level (leaky, upper bound);
    mode='patient' -> inter-patient (record-wise) StratifiedGroupKFold."""
    n_cls = len(np.unique(y))
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=5000, class_weight="balanced"))
    if mode == "beat":
        cv = StratifiedKFold(5, shuffle=True, random_state=seed)
        kw = {}
    else:
        ng = len(np.unique(groups))
        cv = StratifiedGroupKFold(min(5, ng), shuffle=True, random_state=seed)
        kw = {"groups": groups}
    pred = cross_val_predict(clf, X, y, cv=cv, method="predict", **kw)
    proba = cross_val_predict(clf, X, y, cv=cv, method="predict_proba", **kw)
    acc = accuracy_score(y, pred)
    f1 = f1_score(y, pred, average="binary" if n_cls == 2 else "macro")
    try:
        auc = (roc_auc_score(y, proba[:, 1]) if n_cls == 2
               else roc_auc_score(y, proba, multi_class="ovr", average="macro"))
    except ValueError:
        auc = float("nan")
    return acc, f1, auc, pred


def evaluate(X, y, groups, name, mode):
    res = [_one(X, y, groups, mode, s) for s in SEEDS]
    accs = np.array([r[0] for r in res]); f1s = np.array([r[1] for r in res])
    aucs = np.array([r[2] for r in res])
    tag = "F1" if len(np.unique(y)) == 2 else "mF1"
    print(f"  {name:34s} acc={accs.mean():.3f}+/-{accs.std():.3f}  "
          f"{tag}={f1s.mean():.3f}+/-{f1s.std():.3f}  AUC={aucs.mean():.3f}+/-{aucs.std():.3f}")
    return accs.mean(), accs.std(), res[0][3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default="reservoir_states.csv")
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NV", help="NV or NSV")
    ap.add_argument("--out", default="measurements/array/figures/reservoir_ecg.pdf")
    args = ap.parse_args()
    cls_names = list(args.classes)

    df = pd.read_csv(args.states)
    y = df["label"].to_numpy()
    X = df.drop(columns=["label"]).to_numpy().astype(float)
    print(f"states: {X.shape[0]} beats x {X.shape[1]} features; classes {np.bincount(y)}")
    print(f"total reservoir spikes: {int(X.sum())}, mean/beat {X.sum()/len(X):.1f}")

    # re-derive per-beat patient/record groups from the deterministic loader
    from reservoir_data import get_beats
    Xr, yr, meta = get_beats(records=tuple(args.records.split(",")),
                             n_per_class=args.n_per_class, classes=args.classes)
    groups = None
    if np.array_equal(yr, y):
        groups = np.asarray(meta["records"])
        print(f"patients (records): {sorted(set(groups.tolist()))}")
    else:
        print("  WARNING: loader order/labels differ from states -> patient-CV unavailable")

    print(f"\n== reservoir readout (mean +/- std over {len(SEEDS)} repeats) ==")
    evaluate(X, y, groups, "reservoir  [beat-level CV, LEAKY]", "beat")
    if groups is not None:
        r_acc, r_std, r_pred = evaluate(X, y, groups, "reservoir  [INTER-PATIENT CV]", "patient")
    else:
        r_acc, r_std, r_pred = 0.0, 0.0, _one(X, y, None, "beat", 0)[3]

    print("== raw-ECG baseline ==")
    evaluate(Xr, y, groups, "raw ECG  [beat-level CV, LEAKY]", "beat")
    if groups is not None:
        evaluate(Xr, y, groups, "raw ECG  [INTER-PATIENT CV]", "patient")

    # figure: confusion matrix + PCA separability
    ncl = len(cls_names)
    fig, ax = plt.subplots(1, 2, figsize=(6.2, 2.8))
    cm = confusion_matrix(y, r_pred)
    ax[0].imshow(cm, cmap="Blues")
    for (i, j), v in np.ndenumerate(cm):
        ax[0].text(j, i, str(v), ha="center", va="center",
                   color="white" if v > cm.max() / 2 else "black")
    ax[0].set_xticks(range(ncl)); ax[0].set_yticks(range(ncl))
    ax[0].set_xticklabels(cls_names); ax[0].set_yticklabels(cls_names)
    ax[0].set_xlabel("predicted"); ax[0].set_ylabel("true")
    ax[0].set_title(f"reservoir  acc={r_acc:.2f}")

    P = PCA(2).fit_transform(StandardScaler().fit_transform(X))
    colors = ["tab:blue", "tab:green", "tab:red", "tab:purple"]
    markers = ["o", "s", "^", "D"]
    for lab in range(ncl):
        ax[1].scatter(P[y == lab, 0], P[y == lab, 1], s=14, c=colors[lab],
                      marker=markers[lab], alpha=0.7, label=cls_names[lab])
    ax[1].set_xlabel("PC1"); ax[1].set_ylabel("PC2")
    ax[1].set_title("reservoir-state separability"); ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    fig.savefig(args.out.replace(".pdf", ".png"), dpi=150, bbox_inches="tight")
    print("\nwrote", args.out, "(confusion + PCA from inter-patient reservoir preds)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
