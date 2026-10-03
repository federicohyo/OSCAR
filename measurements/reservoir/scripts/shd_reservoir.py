"""SHD (Spiking Heidelberg Digits): does a RECURRENT reservoir on the spike STREAM beat a
STATIC rate vector -- i.e. does temporal processing pay off on a genuinely temporal, already-
spike-encoded task? (The clean test recurrence fell short on static vowel because vowel has too little
time axis; SHD does.) Binary digit subset, like the vowel pairs.

Models, all with a high-precision float readout, 5-fold CV, few seeds:
  static rate + linear   : sum spikes/channel over time (700-dim), throw away time
  static rate + MLP      : same features, trained nonlinear readout
  reservoir rho=0        : feed the binned spike stream frame-by-frame, zero memory (control)
  reservoir rho=0.9/1.1  : RECURRENT -- fading memory over the stream
"""
import warnings; warnings.filterwarnings("ignore")
import argparse, os
import numpy as np
import h5py
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold

SP = "/tmp/claude-1000/-storage-tue-avlsi2024-sw/96404b72-8c75-4a39-a6ef-3074c64831f1/scratchpad"
C = 700               # cochlea channels


def load_binned(h5path, classes, max_per, T, tmax, seed=0):
    f = h5py.File(h5path, "r")
    lab = f["labels"][:]
    rng = np.random.default_rng(seed)
    idx = []
    for c in classes:
        w = np.where(lab == c)[0]
        idx.append(rng.choice(w, min(max_per, len(w)), replace=False))
    idx = np.concatenate(idx); rng.shuffle(idx)
    y = np.array([classes.index(lab[i]) for i in idx])
    times = f["spikes"]["times"]; units = f["spikes"]["units"]
    Xseq = np.zeros((len(idx), T, C), dtype=np.float32)
    for k, i in enumerate(idx):
        t = np.asarray(times[i]); u = np.asarray(units[i]).astype(int)
        tb = np.clip((t / tmax * T).astype(int), 0, T - 1)
        np.add.at(Xseq[k], (tb, u), 1.0)
    return Xseq, y


def cv(Z, clf, y, seeds=range(3)):
    Z = StandardScaler().fit_transform(Z)
    a = [(cross_val_predict(clf, Z, y, cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean()
         for s in seeds]
    return np.mean(a), np.std(a)


def reservoir(Xseq, N, rho, a_leak, in_scale, seed):
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.05)
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    W = W * (rho / sr) if sr > 0 else W
    W_in = rng.standard_normal((N, C)) * in_scale / np.sqrt(C)
    n, T, _ = Xseq.shape
    feats = np.zeros((n, 2 * N), dtype=np.float32)
    for i in range(n):
        x = np.zeros(N); acc = np.zeros(N)
        seq = Xseq[i]
        for t in range(T):
            x = (1 - a_leak) * x + a_leak * np.tanh(W_in @ seq[t] + W @ x)
            acc += x
        feats[i] = np.concatenate([x, acc / T])
    return feats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="0,1", help="two SHD labels (0-9 EN digits, 10-19 DE)")
    ap.add_argument("--max-per", type=int, default=150)
    ap.add_argument("--T", type=int, default=50)
    ap.add_argument("--tmax", type=float, default=1.0)
    ap.add_argument("--N", type=int, default=300)
    args = ap.parse_args()
    classes = [int(c) for c in args.classes.split(",")]

    keys = h5py.File(f"{SP}/shd_train.h5", "r")["extra"]["keys"][:]
    print(f"SHD classes {classes} = {[keys[c].decode() for c in classes]}")
    Xseq, y = load_binned(f"{SP}/shd_train.h5", classes, args.max_per, args.T, args.tmax)
    n = len(y)
    print(f"n={n}, per-class {np.bincount(y)}, binned to (T={args.T}, C={C}), "
          f"mean spikes/sample {Xseq.sum(axis=(1,2)).mean():.0f}\n")

    static = Xseq.sum(axis=1)                       # (n, 700) rate vector -- time thrown away
    print(f"{'model':<34} {'accuracy':>14}")
    m, s = cv(static, LogisticRegression(max_iter=2000, C=0.1), y); print(f"{'static rate + linear':<34} {m:.3f} ± {s:.3f}")
    m, s = cv(static, MLPClassifier((64,), max_iter=800, alpha=1e-2, random_state=0), y); print(f"{'static rate + MLP(64)':<34} {m:.3f} ± {s:.3f}")
    for rho, role in [(0.0, "feedforward (no memory)"), (0.9, "RECURRENT"), (1.1, "RECURRENT (edge)")]:
        ms = []
        for sd in range(4):                          # 4 reservoir draws x 2 CV seeds -> proper std
            Z = reservoir(Xseq, args.N, rho, 0.3, 1.0, sd)
            ms.append(cv(Z, LogisticRegression(max_iter=2000, C=1.0), y, seeds=[0, 1])[0])
        print(f"{'reservoir rho=' + str(rho) + ' + linear':<34} {np.mean(ms):.3f} ± {np.std(ms):.3f}   {role}")


if __name__ == "__main__":
    main()
