#!/usr/bin/env python3
"""Does a small DECISION TREE readout beat the kernel+LogReg readout on the array's
measured spikes? Offline replay of data/olfaction/olf_validate/*.npz (the silicon
acquisitions behind the paper's 0.756 / 0.789 rows), identical protocol:
GroupKFold(5) by trial over the 150 chunks, voted accuracy over the 5 chunks of
each trial. The LogReg control must reproduce the paper numbers, which validates
the harness before any tree number is trusted.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_tree_readout.py
"""
import glob, json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_iso_compare import kernel, vote_acc

MODELS = {
    "LogReg (paper)": lambda: make_pipeline(
        StandardScaler(),
        LogisticRegression(C=0.1, max_iter=5000, class_weight="balanced")),
    "tree depth3":    lambda: DecisionTreeClassifier(max_depth=3, random_state=0),
    "tree depth5":    lambda: DecisionTreeClassifier(max_depth=5, random_state=0),
    "HGB 6x8":        lambda: HGB(max_iter=6, max_leaf_nodes=8, random_state=0),
    "HGB 10x8":       lambda: HGB(max_iter=10, max_leaf_nodes=8, random_state=0),
    "MLP 32":         lambda s=0: make_pipeline(StandardScaler(),
        MLPClassifier((32,), activation="relu", alpha=1e-3, max_iter=3000,
                      random_state=s)),
    "MLP 64":         lambda s=0: make_pipeline(StandardScaler(),
        MLPClassifier((64,), activation="relu", alpha=1e-3, max_iter=3000,
                      random_state=s)),
    "MLP 32,16":      lambda s=0: make_pipeline(StandardScaler(),
        MLPClassifier((32, 16), activation="relu", alpha=1e-3, max_iter=3000,
                      random_state=s)),
}
MLP_SEEDS = (0, 1, 2)          # MLPs are stochastic; average out seed luck

def features(sp, Y, T):
    """Three spike-derived feature sets, escalating in how much timing they keep."""
    n, nb = sp.shape
    counts = np.array([[len(sp[k, j]) for k in range(n)] for j in range(nb)]) / T
    first = np.full((nb, n), T, dtype=float)          # first-spike latency, T if silent
    for k in range(n):
        for j in range(nb):
            s = np.asarray(sp[k, j], dtype=float)
            if s.size:
                first[j, k] = s.min()
    kern = np.nan_to_num(kernel(sp, T))
    return {"counts": counts, "counts+first": np.hstack([counts, first]), "kernel": kern}

def main():
    files = sorted(glob.glob("data/olfaction/olf_validate/*.npz"))
    assert files, "no archived spikes found"
    table = {}
    for f in files:
        tag = f.split("/")[-1].replace(".npz", "")     # e.g. centre_r0
        z = np.load(f, allow_pickle=True)
        sp, Y, it, T = z["spikes"], z["labels"], z["trial"], float(z["T"])
        folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
        for fname, X in features(sp, Y, T).items():
            for mname, mk in MODELS.items():
                seeds = MLP_SEEDS if mname.startswith("MLP") else (None,)
                pcs, v5s = [], []
                for s in seeds:
                    pred = np.zeros(len(Y), dtype=int)
                    for tr, te in folds:
                        m = mk(s) if s is not None else mk()
                        m.fit(X[tr], Y[tr]); pred[te] = m.predict(X[te])
                    pcs.append(float((pred == Y).mean()))
                    v5s.append(vote_acc(pred, Y, it, 5))
                pc, v5 = float(np.mean(pcs)), float(np.mean(v5s))
                table.setdefault(tag.rsplit("_r", 1)[0], {}).setdefault(fname, {}) \
                     .setdefault(mname, []).append((pc, v5))

    for tag, per_feat in sorted(table.items()):
        print(f"\n=== {tag} (mean +/- sd over 3 re-acquisitions) ===")
        print(f"  {'features':<14}{'model':<17}{'per-chunk':>10}{'voted5':>16}")
        for fname, per_model in per_feat.items():
            for mname, reps in per_model.items():
                a = np.array(reps)
                print(f"  {fname:<14}{mname:<17}{a[:,0].mean():>9.3f} "
                      f"{a[:,1].mean():>8.3f} +/-{a[:,1].std():>5.3f}")
    json.dump({t: {f: {m: v for m, v in mm.items()} for f, mm in ff.items()}
               for t, ff in table.items()},
              open("data/olfaction_tree_readout.json", "w"), indent=1)
    print("\nwrote data/olfaction_tree_readout.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
