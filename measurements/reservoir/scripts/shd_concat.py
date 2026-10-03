"""Fair test: does the reservoir's TEMPORAL state ADD discriminative info on top of the static
rate vector? (Removes the confound that the reservoir randomly compresses 700 channels.)
Compare: rate | rate + feedforward-reservoir | rate + recurrent-reservoir.
If rate+recurrent > rate+feedforward > rate, temporal & recurrence genuinely add."""
import warnings; warnings.filterwarnings("ignore")
import sys, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from shd_reservoir import load_binned, reservoir, SP, C

classes = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [5, 9]
maxper = int(sys.argv[2]) if len(sys.argv) > 2 else 150
N = 300
Xseq, y = load_binned(f"{SP}/shd_train.h5", classes, maxper, 50, 1.0)
static = Xseq.sum(axis=1)                         # (n, 700) rate vector
print(f"SHD {classes}: n={len(y)}, per-class {np.bincount(y)}")


def acc(Z, seeds=range(4)):
    Z = StandardScaler().fit_transform(Z)
    a = [(cross_val_predict(LogisticRegression(max_iter=2000, C=0.5), Z, y,
          cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean() for s in seeds]
    return np.mean(a), np.std(a)


m, s = acc(static); print(f"  rate only                    {m:.3f} ± {s:.3f}")
for rho, role in [(0.0, "+ feedforward reservoir"), (1.1, "+ RECURRENT reservoir")]:
    ms = []
    for sd in range(4):
        R = reservoir(Xseq, N, rho, 0.3, 1.0, sd)
        ms.append(acc(np.hstack([static, R]), seeds=[0, 1])[0])
    print(f"  rate {role:<26} {np.mean(ms):.3f} ± {np.std(ms):.3f}")
