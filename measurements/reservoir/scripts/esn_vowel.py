"""Can a RECURRENT reservoir (SW ESN) + high-precision readout reach the 2-layer MLP on vowel?

Vowel is a STATIC 10-D vector (LPC coeffs) -- with a static time axis -- so to give recurrence
something to do we present the 10 features as a length-10 scalar SEQUENCE and let the reservoir
integrate it. The decisive control is spectral radius rho: rho=0 is a pure FEEDFORWARD random
nonlinear expansion (memory off), rho>0 is genuinely RECURRENT. If recurrence helps, rho>0 beats
rho=0. Readout is high-precision float (ridge / logistic) -- the opposite of the chip's noisy
spike-count readout.

Anchors (same 5-fold CV): linear 0.77, RBF 0.97, MLP-2(64,32) 0.99 on the raw 10 features.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn import datasets as skd

d = skd.fetch_openml("vowel", version=2, as_frame=True, parser="liac-arff")
X = d.frame[[f"Feature_{i}" for i in range(10)]].to_numpy(float); yy = d.frame["Class"].to_numpy()
m = np.isin(yy, ["hYd", "had"]); X = StandardScaler().fit_transform(X[m]); y = (yy[m] == "had").astype(int)
n, F = X.shape


def esn_features(X, N, rho, a, in_scale, seed):
    """Present each sample's F features as an F-step scalar sequence through a leaky-tanh ESN.
    Returns [final_state, mean_state] concatenated (2N features per sample)."""
    rng = np.random.default_rng(seed)
    W_in = rng.uniform(-1, 1, (N, 1)) * in_scale
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.1)   # 10% dense
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    if sr > 0:
        W = W * (rho / sr)
    feats = np.zeros((len(X), 2 * N))
    for i, u in enumerate(X):
        x = np.zeros(N); acc = np.zeros(N)
        for t in range(F):
            x = (1 - a) * x + a * np.tanh(W_in[:, 0] * u[t] + W @ x)
            acc += x
        feats[i] = np.concatenate([x, acc / F])
    return feats


def cv(Z, seeds=range(5)):
    Z = StandardScaler().fit_transform(Z)
    acc = [(cross_val_predict(LogisticRegression(max_iter=3000, C=1.0), Z, y,
            cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean() for s in seeds]
    return np.mean(acc), np.std(acc)


print("ESN on vowel (10 feats as a 10-step sequence), high-precision float readout")
print(f"{'N':>4} {'rho':>5} {'a':>4} {'in':>4}   {'accuracy':>14}   role")
best = (0, None)
for N in (100, 300, 500):
    for rho, role in [(0.0, "feedforward (no memory)"), (0.9, "RECURRENT"), (1.1, "RECURRENT (edge)")]:
        for a in (0.5,):
            for insc in (0.5,):
                # average the reservoir over a few random draws to reduce ESN-instance variance
                ms = []
                for sd in range(3):
                    Z = esn_features(X, N, rho, a, insc, seed=sd)
                    ms.append(cv(Z, seeds=[0, 1])[0])
                mean = np.mean(ms)
                print(f"{N:>4} {rho:>5.1f} {a:>4.1f} {insc:>4.1f}   {mean:.3f}          {role}")
                if mean > best[0]:
                    best = (mean, (N, rho, a, insc))
print(f"\nbest ESN: {best[0]:.3f} at N,rho,a,in = {best[1]}")
print("anchors (raw 10 feat): linear 0.77 | RBF 0.97 | MLP-2(64,32) 0.99")
