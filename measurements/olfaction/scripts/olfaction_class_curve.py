#!/usr/bin/env python3
"""The array's capacity curve: voted accuracy vs number of odour classes, on the
measured silicon spikes of data/olfaction/olf_validate/ (9 acquisitions: centre,
bo_best1, bo_best2 x 3 reps), reference readout (exponential kernel + LogReg),
reference protocol (GroupKFold by trial over 150 chunks, voted over the 5 chunks
of a trial).

Two statistics per class count k:
  typical    -- mean +/- sd over ALL C(5,k) subsets and all 9 acquisitions
  data-pick  -- NESTED subset selection: for each test fold, the subset is
                chosen by vote on the other four folds' predictions only, then
                scored on the held-out fold. Selecting the best subset on the
                full data and reporting it would inflate the top of the curve.
Also records the best subset per k (pooled mean) for the figure annotation --
marked data-picked, not used for the data-pick statistic.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_class_curve.py
"""
import glob, itertools, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_iso_compare import kernel, vote_acc

def predictions(sp, Y, it, T, C):
    """CV predictions for the chunks belonging to subset C of classes."""
    m = np.isin(Y, C)
    K = np.nan_to_num(kernel(sp[:, m], T))
    Ys, its = Y[m], it[m]
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Ys), 1)), Ys, its))
    pred = np.zeros(len(Ys), dtype=int)
    for tr, te in folds:
        p = make_pipeline(StandardScaler(),
            LogisticRegression(C=0.1, max_iter=5000, class_weight="balanced"))
        p.fit(K[tr], Ys[tr]); pred[te] = p.predict(K[te])
    return Ys, its, pred, folds

def main():
    files = sorted(glob.glob("data/olfaction/olf_validate/*.npz"))
    assert files, "no archived spikes"
    out = {}
    # per_acq[file][k][subset] = (Ys, its, pred, folds)
    for f in files:
        z = np.load(f, allow_pickle=True)
        sp, Y, it, T = z["spikes"], z["labels"], z["trial"], float(z["T"])
        names = [str(c) for c in z["classes"]]
        per_k = {}
        for k in (2, 3, 4, 5):
            subs = {}
            for C in itertools.combinations(range(5), k):
                Ys, its, pred, folds = predictions(sp, Y, it, T, C)
                subs[tuple(names[c] for c in C)] = (Ys, its, pred, folds)
            per_k[k] = subs
        out[f] = per_k
        print(".", end="", flush=True)
    print()

    res = {}
    for k in (2, 3, 4, 5):
        typ_pc, typ_v5, pick_pc, pick_v5 = [], [], [], []
        subset_scores = {}
        for f, per_k in out.items():
            for sub, (Ys, its, pred, folds) in per_k[k].items():
                pc = float((pred == Ys).mean()); v5 = vote_acc(pred, Ys, its, 5)
                typ_pc.append(pc); typ_v5.append(v5)
                subset_scores.setdefault(sub, []).append((pc, v5))
            # nested data-pick: choose the subset on folds != f, score fold f
            npc, nv5 = [], []
            for fi in range(5):
                best_sub, best_score = None, -1
                for sub, (Ys, its, pred, folds) in per_k[k].items():
                    tr = np.concatenate([te for g, (_, te) in enumerate(folds) if g != fi])
                    s = vote_acc(pred[tr], Ys[tr], its[tr], 5)
                    if s > best_score:
                        best_sub, best_score = sub, s
                Ys, its, pred, folds = per_k[k][best_sub]
                te = folds[fi][1]
                npc.append(float((pred[te] == Ys[te]).mean()))
                nv5.append(vote_acc(pred[te], Ys[te], its[te], 5))
            pick_pc.append(float(np.mean(npc))); pick_v5.append(float(np.mean(nv5)))
        best = max(subset_scores.items(), key=lambda kv: np.mean([r[1] for r in kv[1]]))
        res[k] = dict(
            typical=dict(pc=float(np.mean(typ_pc)), pc_sd=float(np.std(typ_pc)),
                         v5=float(np.mean(typ_v5)), v5_sd=float(np.std(typ_v5))),
            data_pick=dict(pc=float(np.mean(pick_pc)), pc_sd=float(np.std(pick_pc)),
                           v5=float(np.mean(pick_v5)), v5_sd=float(np.std(pick_v5))),
            best_subset=list(best[0]),
            best_subset_v5=float(np.mean([r[1] for r in best[1]])),
            best_subset_flag="data-picked (optimistic) -- use data_pick for claims")
        print(f"k={k}: typical {res[k]['typical']['v5']:.3f} +/- {res[k]['typical']['v5_sd']:.3f}"
              f"   data-pick {res[k]['data_pick']['v5']:.3f} +/- {res[k]['data_pick']['v5_sd']:.3f}"
              f"   (best subset {','.join(best[0])}: {res[k]['best_subset_v5']:.3f}, data-picked)")
    json.dump(res, open("data/olfaction_class_curve.json", "w"), indent=1)
    print("wrote data/olfaction_class_curve.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
