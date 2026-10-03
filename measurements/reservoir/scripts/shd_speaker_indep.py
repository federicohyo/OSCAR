"""SHD SPEAKER-INDEPENDENT eval: fit on shd_train, test on shd_test (held-out speakers).
Removes the optimistic speaker-mixing of random CV. Same models as before; the reservoir
weights are random-but-fixed (same seed -> identical W on train and test), only the readout
is fit on train. Reports test accuracy (mean +/- std over reservoir seeds)."""
import warnings; warnings.filterwarnings("ignore")
import sys, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from shd_reservoir import load_binned, reservoir, SP, C

N = 400


def fit_eval(Ztr, ytr, Zte, yte, clf):
    sc = StandardScaler().fit(Ztr)
    clf.fit(sc.transform(Ztr), ytr)
    return (clf.predict(sc.transform(Zte)) == yte).mean()


def run(classes, max_train, seeds=3):
    Xtr, ytr = load_binned(f"{SP}/shd_train.h5", classes, max_train, 50, 1.0, seed=1)
    Xte, yte = load_binned(f"{SP}/shd_test.h5", classes, 100000, 50, 1.0, seed=2)
    print(f"\n=== classes {classes}  (train n={len(ytr)} {np.bincount(ytr).tolist()}, "
          f"test n={len(yte)} {np.bincount(yte).tolist()}) ===")
    str_, ste = Xtr.sum(1), Xte.sum(1)                    # static rate vectors

    a = fit_eval(str_, ytr, ste, yte, LogisticRegression(max_iter=2000, C=0.1))
    print(f"  static rate + linear             {a:.3f}")
    a = fit_eval(str_, ytr, ste, yte, MLPClassifier((64,), max_iter=800, alpha=1e-2, random_state=0))
    print(f"  static rate + MLP(64)            {a:.3f}")

    for rho, role in [(0.0, "feedforward"), (1.1, "RECURRENT")]:
        alone, concat = [], []
        for s in range(seeds):
            Rtr = reservoir(Xtr, N, rho, 0.3, 1.0, s)     # same seed -> same W on train & test
            Rte = reservoir(Xte, N, rho, 0.3, 1.0, s)
            alone.append(fit_eval(Rtr, ytr, Rte, yte, LogisticRegression(max_iter=2000, C=1.0)))
            concat.append(fit_eval(np.hstack([str_, Rtr]), ytr, np.hstack([ste, Rte]), yte,
                                   LogisticRegression(max_iter=2000, C=0.5)))
        print(f"  reservoir {role:<11} alone     {np.mean(alone):.3f} ± {np.std(alone):.3f}")
        print(f"  rate + {role:<11} reservoir  {np.mean(concat):.3f} ± {np.std(concat):.3f}")


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "5,9"
    mt = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
    run([int(x) for x in task.split(",")], mt)
