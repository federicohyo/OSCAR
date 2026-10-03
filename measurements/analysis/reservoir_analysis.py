#!/usr/bin/env python3
"""Full offline analysis of a recorded reservoir-spike npz: kernel sweep (A8),
reservoir vs raw baseline, A1a replicate-one-neuron, A2 dose-response, A4 diversity,
A5 software random-feature baseline. Inter-patient (leave-one-record-out) primary.
Prints all numbers for the paper logbook."""
import argparse
import numpy as np
from reservoir_kernel import build_features, cv_acc
from reservoir_data import get_beats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, LeaveOneGroupOut, cross_val_predict
from sklearn.metrics import accuracy_score


def mk():
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, class_weight="balanced"))


def loro(F, y, g):
    a = []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = mk(); c.fit(F[tr], y[tr]); a.append(accuracy_score(y[te], c.predict(F[te])))
    return float(np.mean(a)), float(np.std(a)), [round(x, 2) for x in a]


def beat(F, y):
    a = [accuracy_score(y, cross_val_predict(mk(), F, y,
         cv=StratifiedKFold(5, shuffle=True, random_state=s))) for s in range(5)]
    return float(np.mean(a)), float(np.std(a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", required=True)
    ap.add_argument("--records", required=True)
    ap.add_argument("--classes", required=True)
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--K", type=int, default=8)
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y = d["spikes"], d["labels"]
    T = float(d["T"]); g = np.asarray(d["records"]); n = spikes.shape[0]
    ncls = len(np.unique(y)); chance = 1.0 / ncls
    print(f"=== {args.npz}: {n} neurons x {spikes.shape[1]} beats, classes {np.bincount(y)}, "
          f"coding={d['coding']}, {ncls}-class chance={chance:.3f} ===")

    print("\n[A8] kernel sweep (inter-patient, StratifiedGroupKFold):")
    best = (0.0, None)
    for shape in ["exp", "gauss", "ricker", "box"]:
        row = []
        for tau in [0.02, 0.04, 0.08, 0.16, 0.32]:
            m, _ = cv_acc(build_features(spikes, T, args.K, shape, tau), y, g, "patient")
            row.append(m)
            if m > best[0]:
                best = (m, (shape, tau))
        print(f"  {shape:>7}: " + " ".join(f"{v:.3f}" for v in row))
    bshape, btau = best[1]
    print(f"  best: {best[0]:.3f} @ {bshape} tau={btau*1000:.0f}ms")

    X = build_features(spikes, T, args.K, bshape, btau)
    bm, bs = beat(X, y); lm, ls, acc = loro(X, y, g)
    print(f"\n[reservoir] beat={bm:.3f}+/-{bs:.3f}  inter-patient={lm:.3f}+/-{ls:.3f}  per-record={acc}")

    Xr, yr, _ = get_beats(records=tuple(args.records.split(",")),
                          n_per_class=args.n_per_class, classes=args.classes)
    assert np.array_equal(yr, y), "loader order mismatch"
    rbm, rbs = beat(Xr, y); rlm, rls, racc = loro(Xr, y, g)
    print(f"[raw ECG ] beat={rbm:.3f}+/-{rbs:.3f}  inter-patient={rlm:.3f}+/-{rls:.3f}  per-record={racc}")

    K = args.K
    def cols(idx):
        return np.concatenate([np.arange(j * K, (j + 1) * K) for j in idx])
    single = np.array([loro(X[:, cols([k])], y, g)[0] for k in range(n)])
    order = np.argsort(single)[::-1]; bk = int(order[0])
    m, s, _ = loro(np.tile(X[:, cols([bk])], (1, n)), y, g)
    verdict = "DIVERSITY HELPS" if lm > m + 0.02 else "no clear diversity effect"
    print(f"\n[A1a] replicate neuron {bk} x{n}: {m:.3f}+/-{s:.3f}  (full={lm:.3f}) -> {verdict}")

    print("[A2] dose-response (inter-patient):")
    rng = np.random.default_rng(0)
    for k in sorted(set([1, 2, 4, 8, n])):
        hi = loro(X[:, cols(order[:k])], y, g)[0]
        lo = loro(X[:, cols(order[-k:])], y, g)[0]
        rd = np.mean([loro(X[:, cols(rng.choice(n, k, replace=False))], y, g)[0] for _ in range(8)])
        print(f"   k={k:2d}: informative={hi:.3f} least={lo:.3f} random={rd:.3f}")

    sig = np.stack([X[:, cols([j])].ravel() for j in range(n)])
    R = np.corrcoef(sig); off = R[~np.eye(n, dtype=bool)]
    ev = np.linalg.eigvalsh(np.cov(StandardScaler().fit_transform(X).T))
    PR = (ev.sum() ** 2) / np.square(ev).sum()
    print(f"\n[A4] mean|neuron corr|={np.mean(np.abs(off)):.3f}  eff-dim={PR:.1f}/{X.shape[1]}")

    accs5 = []
    for seed in range(10):
        rr = np.random.default_rng(seed)
        W = rr.standard_normal((n * K, Xr.shape[1])) / np.sqrt(Xr.shape[1])
        bb = rr.standard_normal(n * K)
        accs5.append(loro(np.tanh(Xr @ W.T + bb), y, g)[0])
    print(f"[A5] software random features: {np.mean(accs5):.3f}+/-{np.std(accs5):.3f}  "
          f"(reservoir={lm:.3f}, raw={rlm:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
