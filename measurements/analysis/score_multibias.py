"""Score the deliberate bias-diversity run: does adding bias operating modes raise D_eff AND
linear accuracy? 32 feat/mode (16 neurons x 2 projections), 4 modes = 128 feat, mode-major."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict, StratifiedKFold

d = np.load("vowel_multibias.npz", allow_pickle=True)
F = d["feats"].astype(float); y = d["y"].astype(int)
modes = [str(m) for m in d["modes"]]; done = set(int(x) for x in d["done"])
per = 32
print(f"multibias: {F.shape}, {len(done)}/{F.shape[1]} captured, modes={modes}, classes={np.bincount(y)}\n")

def deff(Z):
    ev = np.linalg.eigvalsh(np.cov(StandardScaler().fit_transform(Z).T))
    ev = ev[ev > 1e-9]; return ev.sum()**2/(ev**2).sum()

def acc(Z, clf, seeds=range(5)):
    a = [(cross_val_predict(clf, Z, y, cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean() for s in seeds]
    return np.mean(a), np.std(a)

print(f"{'modes used':<34} {'nfeat':>5} {'D_eff':>6} {'linear':>14} {'RBF':>8}")
for k in range(1, len(modes)+1):
    cols = [j for j in range(k*per) if j in done]
    Z = StandardScaler().fit_transform(F[:, cols])
    m, s = acc(Z, LogisticRegression(max_iter=2000, C=1.0))
    r, _ = acc(Z, SVC(kernel="rbf", C=2.0))
    print(f"{'+'.join(modes[:k]):<34} {len(cols):>5} {deff(F[:,cols]):>6.1f} {m:.3f}±{s:.3f}  {r:.3f}")
