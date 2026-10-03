#!/usr/bin/env python3
"""Paired significance test for the N/S/V comparison.

The marginal mean+/-s.d. across held-out records overstates the uncertainty of the
reservoir-vs-baseline DIFFERENCE, because a hard patient hurts both. The correct test is
PAIRED across held-out records: per-record accuracy (and macro-F1), reservoir minus
baseline, tested with Wilcoxon signed-rank + a paired bootstrap 95% CI of the mean
difference. Uses the measured-HW structured reservoir (the reference campaign's headline feature source)
vs raw and raw+RR.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from scipy.stats import wilcoxon, norm
from reservoir_data import get_beats
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]; K = 8
HW = "reservoir_spikes_nsv_structured_hw.npz"   # recording NSV (reservoir_datasets.py)
RECORDS = "200,208,209,222,223,232,233"


def n_for_power(dz, power=0.8, alpha=0.05):
    """Paired-t records needed: n ~ (z_{1-a/2}+z_{1-b})^2 / dz^2."""
    if dz == 0 or np.isnan(dz):
        return float("inf")
    return (norm.ppf(1 - alpha / 2) + norm.ppf(power)) ** 2 / dz ** 2


def bank(spikes, T):
    return np.hstack([build_features(spikes, T, K, "exp", t) for t in TAUS])


def per_record(F, y, g):
    """Return dict record-id -> (accuracy, macro-F1) from leave-one-record-out."""
    out = {}
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); p = c.predict(F[te])
        rec = g[te][0]
        out[rec] = (accuracy_score(y[te], p), f1_score(y[te], p, average="macro"))
    return out


def paired(a, b, recs, name):
    """a, b: dict rec->metric for reservoir and baseline. Paired Wilcoxon + bootstrap CI."""
    da = np.array([a[r] for r in recs]); db = np.array([b[r] for r in recs])
    d = da - db
    # Wilcoxon signed-rank (two-sided); guard the all-zero / n<... edge cases
    try:
        w, p = wilcoxon(da, db, zero_method="wilcox", alternative="two-sided")
    except ValueError:
        w, p = float("nan"), 1.0
    rng = np.random.default_rng(0)
    boot = [np.mean(d[rng.integers(0, len(d), len(d))]) for _ in range(20000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    n_fav = int(np.sum(d > 0)); n_tie = int(np.sum(d == 0))
    dz = d.mean() / d.std(ddof=1) if d.std(ddof=1) > 0 else float("nan")
    sig = "SIGNIFICANT" if (lo > 0 or hi < 0) else "n.s."
    print(f"  {name:26s} mean diff {d.mean():+.3f}  95%CI [{lo:+.3f},{hi:+.3f}] {sig}  "
          f"Wilcoxon p={p:.3f}  dz={dz:+.2f}  ({n_fav}/{len(d)} favour, {n_tie} tie)")
    print(f"       n for 80%%/90%% power @a=.05: {n_for_power(dz,.8,.05):.0f}/{n_for_power(dz,.9,.05):.0f}"
          f"  (have {len(d)});  per-record diff: "
          + " ".join(f"{r}:{x:+.2f}" for r, x in zip(recs, d)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default=HW)
    ap.add_argument("--records", default=RECORDS)
    ap.add_argument("--n-per-class", type=int, default=30)
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    sp = d["spikes"]; y = np.asarray(d["labels"]); g = np.asarray(d["records"]); T = float(d["T"])
    if "X_raw" in d:                          # self-contained npz (full-set SW run)
        X = d["X_raw"]; rr = d["rr"]
    else:                                      # re-derive raw + RR from the deterministic loader
        X, y2, meta = get_beats(records=tuple(args.records.split(",")),
                                n_per_class=args.n_per_class, classes="NSV")
        rr = meta["rr"]
        assert np.array_equal(y, y2) and np.array_equal(g, np.asarray(meta["records"])), \
            "beat ordering mismatch between npz and get_beats"
    recs = list(dict.fromkeys(g))  # unique records, stable order

    Fstruct = bank(sp, T)
    sources = {"raw": X, "raw+RR": np.hstack([X, rr]), "struct-HW": Fstruct}
    pr = {name: per_record(F, y, g) for name, F in sources.items()}

    print(f"=== N/S/V, {len(y)} beats, {len(recs)} records {recs} ===")
    print("per-record ACCURACY:")
    for name in sources:
        accs = np.array([pr[name][r][0] for r in recs])
        print(f"  {name:12s} mean {accs.mean():.3f}+/-{accs.std():.3f}")
    print("per-record MACRO-F1:")
    for name in sources:
        f1s = np.array([pr[name][r][1] for r in recs])
        print(f"  {name:12s} mean {f1s.mean():.3f}+/-{f1s.std():.3f}")

    print("\nPAIRED test on per-record ACCURACY (reservoir - baseline):")
    paired({r: pr["struct-HW"][r][0] for r in recs}, {r: pr["raw"][r][0] for r in recs}, recs, "struct-HW vs raw")
    paired({r: pr["struct-HW"][r][0] for r in recs}, {r: pr["raw+RR"][r][0] for r in recs}, recs, "struct-HW vs raw+RR")
    print("PAIRED test on per-record MACRO-F1 (reservoir - baseline):")
    paired({r: pr["struct-HW"][r][1] for r in recs}, {r: pr["raw"][r][1] for r in recs}, recs, "struct-HW vs raw")
    paired({r: pr["struct-HW"][r][1] for r in recs}, {r: pr["raw+RR"][r][1] for r in recs}, recs, "struct-HW vs raw+RR")
    nsrec = sum(1 for r in recs if 1 in np.unique(y[g == r]))
    print(f"\nNote: n={len(recs)} records -> Wilcoxon two-sided floor p~{2**-(len(recs)-1):.4f} "
          f"(all same sign). S class present in {nsrec} records (bounds any S-specific claim).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
