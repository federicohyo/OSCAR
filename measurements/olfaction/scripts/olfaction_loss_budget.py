#!/usr/bin/env python3
"""Where does the array's accuracy go? A staged loss budget, same folds throughout.

The array reaches 0.647 per-chunk where the digital baseline reaches 0.880. That gap is
NOT one thing, and knowing which part is which decides what to fix. So walk the signal
path, handing the SAME digital classifier progressively less information:

    full 400-D feature      what the digital baseline sees
    16 projected courses    the 400 -> 16 random projection the chip's input imposes
    delta event counts      what actually arrives at the synapses
    (measured array)        after the analog neurons

Measured 2026-08-13, olfaction_spikes_array_iso.npz:

                                     feat  per-chunk  voted5
    full 400-D feature (baseline)     400      0.880   0.967
    16 projected time courses         800      0.773   0.900     projection -0.107
    delta event counts                 32      0.767   0.867     encoder    -0.006
    array kernel read-out (measured)  128      0.647   0.833     array      -0.120

Two conclusions. (1) The delta encoder is essentially LOSSLESS here (-0.006), which is a
real result for level-crossing coding on this signal. (2) The projection bottleneck and
the analog array cost about the same per chunk -- so the array is not merely starved by
its input, it loses as much again on its own. But under voting the array's loss collapses
to -0.034 while the projection's stays at -0.067: the array's contribution is largely
NOISE, which averaging removes, and the projection's is lost INFORMATION, which it cannot.
So the ranked fix is more effective input dimensions (time-multiplex projections), then
more votes.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_loss_budget.py
"""
import argparse, json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB
from sklearn.model_selection import GroupKFold

from olfaction_identity import chunks
from olfaction_iso_compare import vote_acc
from olfaction_run_array import encode

FS = 1000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data_olfaction/olfaction_pulses.npz")
    ap.add_argument("--duration", default="0.1s")
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--neurons", type=int, default=16)
    ap.add_argument("--out", default="data/olfaction_loss_budget.json")
    args = ap.parse_args()

    d = np.load(args.src, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == args.duration
    F, it = chunks(X[m], Th[m], t, float(args.duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    folds = list(GroupKFold(n_splits=5).split(F, Y, it))

    def sc(Fx):
        Fx = np.nan_to_num(Fx); p = np.zeros(len(Y), int)
        for tr, te in folds:
            p[te] = HGB(max_iter=10, max_leaf_nodes=8,
                        random_state=0).fit(Fx[tr], Y[tr]).predict(Fx[te])
        return float((p == Y).mean()), vote_acc(p, Y, it, 5), int(Fx.shape[1])

    # the per-neuron projections, built exactly as olfaction_run_array does
    proj = np.stack([F.reshape(len(F), 50, 8)
                     @ np.random.default_rng(100 + k).normal(0, 1, 8)
                     for k in range(args.neurons)], 1)
    proj = (proj - proj.mean((0, 2), keepdims=True)) / (proj.std((0, 2), keepdims=True) + 1e-9)
    ec = np.zeros((len(F), 2 * args.neurons))
    for j in range(len(F)):
        for k in range(args.neurons):
            e = encode(proj[j, k], args.theta)
            ec[j, 2 * k] = sum(1 for _, c in e if c == 0)
            ec[j, 2 * k + 1] = sum(1 for _, c in e if c == 1)

    stages = [("full 400-D feature (baseline)", F),
              ("16 projected time courses", proj.reshape(len(F), -1)),
              ("delta event counts", ec)]
    print(f"{len(Y)} chunks / {len(np.unique(it))} trials, chance {1/len(names):.3f}\n")
    print(f"{'stage':<34} {'feat':>5} {'per-chunk':>10} {'voted5':>8} {'d(chunk)':>9}")
    res, prev = {}, None
    for nm, Fx in stages:
        pc, v5, nf = sc(Fx)
        dl = "" if prev is None else f"{pc - prev:+9.3f}"
        print(f"{nm:<34} {nf:5d} {pc:10.3f} {v5:8.3f} {dl:>9}")
        res[nm] = {"per_chunk": pc, "voted5": v5, "n_features": nf}
        prev = pc
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"\ncompare the measured array from data/olfaction_iso_compare.json")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
