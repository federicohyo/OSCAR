#!/usr/bin/env python3
"""Does spending neurons on more THRESHOLD LEVELS buy accuracy? Settled on the 1.0 s set.

The question comes from the reference figure. Time-multiplexing sixteen neurons leaves unchanged
accuracy -- the same comparisons are made against the same thresholds -- but sixteen
neurons could instead hold sixteen distinct levels, and the array's representation costs
0.100 voted, which is exactly the quantity more levels would attack.

WHY THE 0.1 s SET IS PASSED OVER. That is the reference campaign's test split, and it has 30 trials. Voted
accuracy over 30 trials moves in steps of 0.033, so 0.900 and 1.000 are three trials
apart; a first attempt there produced a non-monotonic sweep (6 levels beating 8, 10 and
12) with bootstrap intervals that overlapped completely. The measurement was not capable
of answering the question.

WHAT THIS DOES INSTEAD. The 1.0 s pulses have 90 trials of 23 chunks. Grouped 5-fold CV
by trial gives every trial a turn in the test set, and each trial's chunks are partitioned
into consecutive blocks of five so the statistic stays the reference campaign's voted-over-5 --
about 360 voted decisions rather than 30. The quantiser cuts are fit on the TRAINING
chunks of each fold, so the levels stay clear of the test trials.

Uncertainty is a CLUSTER bootstrap over trials rather than over decisions: four voted decisions
cut from one trial are correlated, and treating them as independent would
shrink the interval beyond what the data supports.

    ./.venv-meas/bin/python3 olfaction_hybrid_levels.py
"""
import argparse, json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB
from sklearn.model_selection import GroupKFold

from olfaction_identity import chunks

KCH = 5                      # the reference campaign's voting block


def load_long(npz="data_olfaction/olfaction_pulses.npz"):
    d = np.load(npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / 1000.0 + float(d["t0"]) / 1000.0
    dur = np.array([m[0] for m in meta])
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])
    m = dur == "1.0s"
    F, it = chunks(X[m], Th[m], t, 1.0, 0.05, tail=0.2)
    return F, Y[m][it], it, names


def quant(Ftr, Fte, nlev):
    """Per-feature quantile cuts fit on TRAIN only; value -> how many cuts it exceeds."""
    if nlev is None:
        return Ftr, Fte
    pr = np.linspace(1.0, nlev, nlev) / (nlev + 1.0)
    cuts = np.percentile(Ftr, pr * 100.0, axis=0)
    q = lambda F: (F[None, :, :] > cuts[:, None, :]).sum(axis=0).astype(np.int16)
    return q(Ftr), q(Fte)


def voted_blocks(pred, y, trial, nc):
    """Majority vote over consecutive blocks of KCH chunks inside each trial."""
    ok, owner = [], []
    for j in np.unique(trial):
        s = np.flatnonzero(trial == j)
        for b in range(len(s) // KCH):
            g = s[b * KCH:(b + 1) * KCH]
            ok.append(np.bincount(pred[g], minlength=nc).argmax() == y[g][0])
            owner.append(j)
    return np.array(ok), np.array(owner)


def cluster_boot(ok, owner, rng, n=4000):
    """Resample TRIALS, not decisions: blocks cut from one trial are not independent."""
    tr = np.unique(owner)
    idx = {j: np.flatnonzero(owner == j) for j in tr}
    out = np.empty(n)
    for i in range(n):
        pick = rng.integers(0, len(tr), len(tr))
        out[i] = np.concatenate([ok[idx[tr[k]]] for k in pick]).mean()
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--levels", default="4,6,8,10,12,16,20,24,32")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--out", default="data/olfaction_hybrid_levels.json")
    args = ap.parse_args()
    F, Y, it, names = load_long(); nc = len(names)
    rng = np.random.default_rng(0)
    print(f"{len(F)} chunks over {len(np.unique(it))} trials, {nc} classes, "
          f"{args.folds}-fold grouped CV, voting blocks of {KCH}")
    levels = [int(x) for x in args.levels.split(",")] + [None]
    res = {}
    print(f"\n{'levels':>7} | {'per-chunk':>9} | {'voted5':>7} | "
          f"{'95% CI (cluster bootstrap)':>26} | {'decisions':>9}")
    for nlev in levels:
        P = np.empty(len(F), dtype=int)
        for tr_i, te_i in GroupKFold(n_splits=args.folds).split(F, Y, groups=it):
            Qtr, Qte = quant(F[tr_i], F[te_i], nlev)
            g = HGB(max_iter=10, max_leaf_nodes=8, random_state=0).fit(Qtr, Y[tr_i])
            P[te_i] = g.predict(Qte)
        ok, owner = voted_blocks(P, Y, it, nc)
        lo, hi = cluster_boot(ok, owner, rng)
        tag = "full" if nlev is None else str(nlev)
        res[tag] = dict(per_chunk=float((P == Y).mean()), voted5=float(ok.mean()),
                        ci=[lo, hi], decisions=int(len(ok)))
        star = "  <-- 10 calibrated levels" if nlev == 10 else (
            "  (full precision)" if nlev is None else "")
        print(f"{tag:>7} | {(P==Y).mean():9.3f} | {ok.mean():7.3f} | "
              f"{f'[{lo:.3f}, {hi:.3f}]':>26} | {len(ok):9d}{star}")

    a, b = res["10"], res["20"]
    sep = a["ci"][1] < b["ci"][0]
    print(f"\n10 -> 20 levels: {b['voted5']-a['voted5']:+.3f} voted, "
          f"CIs {'SEPARATE' if sep else 'overlap'}")
    res["_verdict"] = dict(delta_10_to_20=b["voted5"] - a["voted5"], separated=bool(sep))
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
