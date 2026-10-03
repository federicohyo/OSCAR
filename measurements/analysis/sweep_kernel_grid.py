#!/usr/bin/env python3
"""Does the kernel read-out's grid density / tau set change the Table-II accuracy?

Replays the three archived acquisitions of the centre bias point
(data/olfaction/olf_validate/centre_r{0,1,2}.npz) through the stock scorer with
different kernel settings. Same folds (GroupKFold on trial), same classifier
(StandardScaler + balanced LogisticRegression(C=0.1)) as olfaction_bias_bo.score.

    PYTHONPATH=. ./.venv-meas/bin/python3 sweep_kernel_grid.py
"""
import numpy as np
from sklearn.model_selection import GroupKFold
from olfaction_iso_compare import kernel, vote_acc
from olfaction_bias_bo import score

REPS = [f"data/olfaction/olf_validate/centre_r{r}.npz" for r in range(3)]


def main():
    reps = []
    for f in REPS:
        d = np.load(f, allow_pickle=True)
        reps.append((d["spikes"], d["labels"], d["trial"], float(d["T"])))
    sp0, Y, it, T = reps[0]
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))

    configs = (
        [("counts (K=1)", (None,), 1)]                      # plain counts baseline
        + [(f"taus={taus}, K={K}", taus, K)
           for taus in ((0.050,), (0.010, 0.050), (0.005, 0.010, 0.050, 0.150))
           for K in (1, 2, 4, 8, 16)]
    )
    print(f"{'config':38s} {'per-chunk':>16s} {'voted5':>16s}")
    for name, taus, K in configs:
        accs, v5 = [], []
        for sp, Yr, itr, _ in reps:
            if taus == (None,):
                # counts: one feature per neuron = spikes/T  (the kernel at
                # g=T with tau>>T is the same thing, up to scale)
                n, nb = sp.shape
                Kf = np.array([[len(np.asarray(sp[i, j])) / T
                                for i in range(n)] for j in range(nb)])
            else:
                Kf = np.nan_to_num(kernel(sp, T, taus=taus, K=K))
            # score() refits its own kernel, so inline its body on Kf:
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import make_pipeline
            from sklearn.preprocessing import StandardScaler
            pred = np.zeros(len(Yr), dtype=int)
            for tr, te in folds:
                m = make_pipeline(StandardScaler(),
                                  LogisticRegression(C=0.1, max_iter=5000,
                                                     class_weight="balanced"))
                m.fit(Kf[tr], Yr[tr]); pred[te] = m.predict(Kf[te])
            accs.append(float((pred == Yr).mean()))
            v5.append(vote_acc(pred, Yr, itr, 5))
        print(f"{name:38s} {np.mean(accs):.3f} +/- {np.std(accs):.3f}   "
              f"{np.mean(v5):.3f} +/- {np.std(v5):.3f}")


if __name__ == "__main__":
    main()
