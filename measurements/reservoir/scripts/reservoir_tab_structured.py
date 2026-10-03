#!/usr/bin/env python3
"""Reproduce every row of the structured-reservoir table (3-class N/S/V, inter-patient LORO,
linear readout) from the committed npz files, so the reference campaign table is verifiable offline.

Rows: raw ECG / raw+RR / RR-only (static feature baselines), the random-projection
reservoir (HW), and the structured feature-aware reservoir (SW and HW). Reservoir rows
use the multi-tau exponential readout bank; all rows use the same balanced C=0.1 logistic
readout under leave-one-record-out. Also prints the S-class record distribution.

macro-F1 is the mean over held-out records of each record's macro-F1 (per-record LORO);
the per-class F1_{N,S,V} are pooled across all held-out predictions -- so macro-F1 need
not equal the unweighted mean of the printed per-class F1.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from reservoir_kernel import build_features
from reservoir_data import get_beats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]; K = 8
CANON = ("200", "208", "209", "222", "223", "232", "233")


def bank(sp, T):
    return np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])


def loro(F, y, g):
    yhat = np.empty_like(y); accs, f1s = [], []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); p = c.predict(F[te]); yhat[te] = p
        accs.append(accuracy_score(y[te], p)); f1s.append(f1_score(y[te], p, average="macro"))
    pc = f1_score(y, yhat, average=None)               # pooled per-class
    return np.mean(f1s), np.std(f1s), pc


def row(name, F, y, g):
    f, fsd, pc = loro(F, y, g)
    print(f"  {name:28s} macro-F1={f:.4f}±{fsd:.4f}  "
          f"F1_N={pc[0]:.3f}  F1_S={pc[1]:.3f}  F1_V={pc[2]:.3f}")


def main():
    hw = np.load("reservoir_spikes_nsv_structured_hw.npz", allow_pickle=True)  # NSV
    y = np.asarray(hw["labels"]); g = np.asarray(hw["records"])
    X, y2, meta = get_beats(records=CANON, n_per_class=30, classes="NSV"); rr = meta["rr"]
    assert np.array_equal(y, y2) and np.array_equal(g, np.asarray(meta["records"])), "MISALIGNED"
    recs = list(dict.fromkeys(g.tolist()))

    sc = {r: int(np.sum((g == r) & (y == 1))) for r in recs}
    nS = sum(1 for r in recs if sc[r] > 0)
    print(f"=== S-class distribution (label 1) over {len(recs)} records ===")
    print(f"  per-record S beats: {sc}")
    print(f"  S present in {nS}/{len(recs)} records; {max(sc.values())}/{sum(sc.values())} "
          f"S beats from record {max(sc, key=sc.get)}")

    print("\n=== the reference table rows (macro-F1 = per-record LORO mean; per-class F1 pooled) ===")
    row("raw ECG", X, y, g)
    row("raw ECG + RR", np.hstack([X, rr]), y, g)
    row("RR features only", rr, y, g)
    # the reference campaign's random-projection HW row is the tuned2 bias point (matches the reference table exactly)
    rp = np.load("reservoir_spikes_nsv_randproj_tuned2.npz", allow_pickle=True)
    row("reservoir, random proj. HW", bank(rp["spikes"], float(rp["T"])), y, g)
    sw = np.load("reservoir_spikes_nsv_structured.npz", allow_pickle=True)
    row("reservoir, structured SW", bank(sw["spikes"], float(sw["T"])), y, g)
    row("reservoir, structured HW", bank(hw["spikes"], float(hw["T"])), y, g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
