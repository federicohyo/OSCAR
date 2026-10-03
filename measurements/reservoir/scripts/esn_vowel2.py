"""Follow-up: (1) find the recurrent-reservoir CEILING on vowel by sweeping N; (2) control for
the encoding -- does recurrence still help when the readout sees ALL features feedforward?"""
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


def reservoir(X, N, rho, a, in_scale, seed, seq=True):
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.1)
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    W = W * (rho / sr) if sr > 0 else W
    D = 1 if seq else F                       # scalar-per-step sequence, or full vector per step
    W_in = rng.uniform(-1, 1, (N, D)) * in_scale
    feats = np.zeros((len(X), 2 * N))
    T = F if seq else F                        # same #steps
    for i, u in enumerate(X):
        x = np.zeros(N); acc = np.zeros(N)
        for t in range(T):
            drive = W_in[:, 0] * u[t] if seq else W_in @ u
            x = (1 - a) * x + a * np.tanh(drive + W @ x)
            acc += x
        feats[i] = np.concatenate([x, acc / T])
    return feats


def cv(Z, seeds=range(3)):
    Z = StandardScaler().fit_transform(Z)
    return np.mean([(cross_val_predict(LogisticRegression(max_iter=3000), Z, y,
            cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean() for s in seeds])


print("(1) CEILING: sweep reservoir size N at edge-of-chaos rho=1.1 (sequential encoding)")
for N in (500, 1000, 1500, 2000):
    ms = [cv(reservoir(X, N, 1.1, 0.5, 0.5, sd)) for sd in range(3)]
    print(f"   N={N:>4}  acc {np.mean(ms):.3f} ± {np.std(ms):.3f}")

print("\n(2) ENCODING CONTROL: full 10-vector fed EVERY step (readout can see all feats even at rho=0)")
for rho, role in [(0.0, "feedforward"), (0.9, "recurrent")]:
    ms = [cv(reservoir(X, 500, rho, 0.5, 0.5, sd, seq=False)) for sd in range(3)]
    print(f"   rho={rho:.1f} ({role:>11})  acc {np.mean(ms):.3f} ± {np.std(ms):.3f}")

print("\nanchors: linear 0.77 | RBF 0.97 | MLP-2 0.99 | (seq ESN best so far 0.894 @N=500,rho=1.1)")
