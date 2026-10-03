#!/usr/bin/env python3
"""N/S/V (3-class) comparison: raw ECG vs shared-input reservoir vs per-neuron-projection
reservoir vs BOTH combined (shared + projection stacked = 32 virtual neurons).

The decisive non-saturated test: on binary N/PVC one neuron already solves the task, so
the projection only ever bought dimensionality. On the harder 3-class task the extra
dimensionality can convert to accuracy -- and, since mismatch-diversity (shared input) and
input-decorrelation (projection) are roughly independent mechanisms, stacking both should
help most.

For each feature source we report the three readout operating points (accuracy-optimal
single kernel, joint multi-tau bank with nested-CV C, dimensionality-optimal single kernel),
inter-patient (leave-one-record-out), plus A1a (single-neuron replicate: does diversity
help?) and A4 (mean neuron |corr| and effective dimensionality).
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_kernel import build_features
from reservoir_data import get_beats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (LeaveOneGroupOut, GridSearchCV,
                                     StratifiedKFold, cross_val_predict)
from sklearn.metrics import accuracy_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]
CGRID = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
K = 8


def mk(C=1.0):
    return make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=5000, class_weight="balanced", C=C))


def loro(X, y, g, C=1.0):
    a = []
    for tr, te in LeaveOneGroupOut().split(X, y, g):
        c = mk(C); c.fit(X[tr], y[tr]); a.append(accuracy_score(y[te], c.predict(X[te])))
    return float(np.mean(a)), float(np.std(a))


def beat(X, y):
    a = [accuracy_score(y, cross_val_predict(mk(), X, y,
         cv=StratifiedKFold(5, shuffle=True, random_state=s))) for s in range(5)]
    return float(np.mean(a)), float(np.std(a))


def effdim(X):
    ev = np.clip(np.linalg.eigvalsh(np.cov(StandardScaler().fit_transform(X).T)), 0, None)
    return float((ev.sum() ** 2) / np.square(ev).sum())


def feats(spikes_list, T, tau):
    """single-kernel features, concatenated across one or more spike arrays."""
    return np.hstack([build_features(sp, T, K, "exp", tau) for sp in spikes_list])


def bank(spikes_list, T):
    return np.hstack([build_features(sp, T, K, "exp", t) for sp in spikes_list for t in TAUS])


def nested_bank(spikes_list, T, y, g):
    Xb = bank(spikes_list, T)
    accs = []
    for tr, te in LeaveOneGroupOut().split(Xb, y, g):
        gs = GridSearchCV(mk(), {"logisticregression__C": CGRID},
                          cv=LeaveOneGroupOut(), scoring="accuracy")
        gs.fit(Xb[tr], y[tr], groups=g[tr])
        accs.append(accuracy_score(y[te], gs.predict(Xb[te])))
    return float(np.mean(accs)), float(np.std(accs)), effdim(Xb)


def oppoints(spikes_list, T, y, g, n_neu):
    rows = [(t, *loro(feats(spikes_list, T, t), y, g), effdim(feats(spikes_list, T, t))) for t in TAUS]
    ao = max(rows, key=lambda r: r[1])
    do = max(rows, key=lambda r: r[3])
    jm, js, jd = nested_bank(spikes_list, T, y, g)
    bmt = beat(bank(spikes_list, T), y)
    return dict(ao=ao, do=do, joint=(jm, js, jd), beat_bank=bmt)


def a1a_a4(spikes_list, T, y, g, tau):
    """A1a single-neuron replicate & A4 corr/eff-dim at a fixed kernel."""
    Xn = [build_features(sp, T, K, "exp", tau) for sp in spikes_list]  # per-source blocks
    X = np.hstack(Xn)
    n = X.shape[1] // K
    def cols(idx): return np.concatenate([np.arange(j*K, (j+1)*K) for j in idx])
    single = np.array([loro(X[:, cols([k])], y, g)[0] for k in range(n)])
    bk = int(np.argmax(single))
    rep = loro(np.tile(X[:, cols([bk])], (1, n)), y, g)[0]
    full = loro(X, y, g)[0]
    sig = np.stack([X[:, cols([j])].ravel() for j in range(n)])
    R = np.corrcoef(sig); off = R[~np.eye(n, dtype=bool)]
    return dict(single_best=float(single.max()), replicate=rep, full=full,
                corr=float(np.mean(np.abs(off))), effdim=effdim(X), n=n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shared", default="reservoir_spikes_nsv_delta.npz")
    ap.add_argument("--proj", default="reservoir_spikes_nsv_randproj.npz")
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    args = ap.parse_args()

    ds = np.load(args.shared, allow_pickle=True)
    dp = np.load(args.proj, allow_pickle=True)
    y = ds["labels"]; g = np.asarray(ds["records"]); T = float(ds["T"])
    assert np.array_equal(y, dp["labels"]), "shared/proj beat-order mismatch"
    assert np.array_equal(g, np.asarray(dp["records"])), "record-order mismatch"
    ncls = len(np.unique(y)); chance = 1.0 / ncls
    print(f"=== N/S/V 3-class ({ncls}-class, chance={chance:.3f}), {len(y)} beats, "
          f"classes {np.bincount(y)} ===\n")

    Xr, yr, _ = get_beats(records=tuple(args.records.split(",")),
                          n_per_class=args.n_per_class, classes="NSV")
    assert np.array_equal(yr, y), "raw loader order mismatch"
    rb, rbs = beat(Xr, y); rl, rls = loro(Xr, y, g)
    print(f"[raw ECG] beat={rb:.3f}+/-{rbs:.3f}  inter-patient={rl:.3f}+/-{rls:.3f}\n")

    sources = [("shared input", [ds["spikes"]]),
               ("projection",   [dp["spikes"]]),
               ("BOTH (shared+proj)", [ds["spikes"], dp["spikes"]])]
    print(f"{'source':20s} | acc-opt(tau) dim | JOINT bank dim | dim-opt(tau) acc | beat(bank)")
    for name, spl in sources:
        r = oppoints(spl, T, y, g, None)
        ao, do, (jm, js, jd), (bm, bs) = r["ao"], r["do"], r["joint"], r["beat_bank"]
        print(f"{name:20s} | {ao[1]:.3f}+/-{ao[2]:.3f}({ao[0]*1e3:.0f}) {ao[3]:4.1f} "
              f"| {jm:.3f}+/-{js:.3f} {jd:4.1f} | {do[3]:4.1f}({do[0]*1e3:.0f}) {do[1]:.3f} "
              f"| {bm:.3f}+/-{bs:.3f}")

    print("\n[A1a diversity / A4 dim] at exp tau=80ms:")
    for name, spl in sources:
        a = a1a_a4(spl, T, y, g, 0.08)
        verdict = "DIVERSITY HELPS" if a["full"] > a["replicate"] + 0.02 else "no clear diversity gain"
        print(f"  {name:20s} n={a['n']:2d}  single-best={a['single_best']:.3f} "
              f"replicate={a['replicate']:.3f} full={a['full']:.3f} -> {verdict} "
              f"| corr={a['corr']:.3f} eff-dim={a['effdim']:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
