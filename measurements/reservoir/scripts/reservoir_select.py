#!/usr/bin/env python3
"""Which subset of reservoir neurons is worth keeping -- reported honestly.

Dropping neurons whose leave-one-out dAcc is negative, then reporting the surviving
subset's accuracy on the SAME cross-validation folds, is selection bias: the subset was
chosen using the test folds. With 4 records / 60 beats that bias is large.

So this reports two numbers:

  OPTIMISTIC  subset chosen on all data, scored on the same folds. This is the number
              you get if you eyeball dAcc and drop neurons. Upper bound / illusion.
  NESTED      for each outer test record, the subset is chosen using ONLY the other
              records, then evaluated on the held-out one. This is what neuron
              selection actually buys you.

Selection is greedy backward elimination on the inner folds (drop the neuron whose
removal most improves inner accuracy; stop once removals stop helping).

    ./.venv-meas/bin/python3 reservoir_select.py --npz reservoir_spikes...npz
"""
import argparse
import numpy as np
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score

K, TAUS = 8, [0.04, 0.08, 0.16, 0.32]


def clf():
    return make_pipeline(StandardScaler(),
                         LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))


def blocks_of(sp, T):
    """Per-neuron feature block: list of (n_beats, K*len(TAUS))."""
    n = sp.shape[0]
    full = np.hstack([build_features(sp, T, K, "exp", t) for t in TAUS])  # (beats, n*K*ntau)
    out = []
    for i in range(n):
        cols = np.concatenate([np.arange(j * n * K + i * K, j * n * K + (i + 1) * K)
                               for j in range(len(TAUS))])
        out.append(full[:, cols])
    return out


def acc_cv(blocks, subset, y, g):
    """LOGO accuracy over the groups present in y/g, using only `subset` neurons."""
    if not subset:
        return 0.0
    F = np.hstack([blocks[i] for i in subset])
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = clf(); c.fit(F[tr], y[tr])
        accs.append(accuracy_score(y[te], c.predict(F[te])))
    return float(np.mean(accs))


def greedy_backward(blocks, subset, y, g, verbose=False):
    """Drop the neuron whose removal most improves CV accuracy; repeat while it helps."""
    cur = list(subset)
    best = acc_cv(blocks, cur, y, g)
    while len(cur) > 1:
        cands = [(acc_cv(blocks, [j for j in cur if j != i], y, g), i) for i in cur]
        a, i = max(cands)
        if a <= best + 1e-12:
            break
        cur = [j for j in cur if j != i]
        best = a
        if verbose:
            print(f"    drop n{i} -> {best:.3f} ({len(cur)} left)")
    return cur, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_delta_50mhz_jul10.npz")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y, recs, T = d["spikes"], np.asarray(d["labels"]), np.asarray(d["records"]), float(d["T"])
    done = [int(k) for k in d["done_neurons"]] if "done_neurons" in d.files else list(range(spikes.shape[0]))
    sp = spikes[:len(done), :]
    n = len(done)
    blocks = blocks_of(sp, T)
    allidx = list(range(n))

    full = acc_cv(blocks, allidx, y, recs)
    print(f"{args.npz}: {n} neurons {done}, {sp.shape[1]} beats, {len(set(recs))} records")
    print(f"\nall {n} neurons:            acc {full:.3f}")

    # --- OPTIMISTIC: select on everything, score on the same folds -------------
    keep, opt = greedy_backward(blocks, allidx, y, recs, verbose=True)
    print(f"\nOPTIMISTIC (biased) subset {[done[i] for i in keep]}: acc {opt:.3f}")
    print("  ^ chosen using the same folds it is scored on -- do NOT report this.")

    # --- NESTED: selection inside each outer fold ------------------------------
    outer, chosen = [], []
    for tr, te in LeaveOneGroupOut().split(np.zeros((len(y), 1)), y, recs):
        sub, _ = greedy_backward([b[tr] for b in blocks], allidx, y[tr], recs[tr])
        F = np.hstack([blocks[i] for i in sub])
        c = clf(); c.fit(F[tr], y[tr])
        outer.append(accuracy_score(y[te], c.predict(F[te])))
        chosen.append([done[i] for i in sub])
    print(f"\nNESTED (honest): acc {np.mean(outer):.3f} +/- {np.std(outer):.3f}")
    for r, (a, s) in enumerate(zip(outer, chosen)):
        print(f"  fold {r}: acc {a:.3f}   kept {s}")
    votes = {k: sum(k in s for s in chosen) for k in done}
    print(f"\nkept in how many of {len(chosen)} folds: "
          + ", ".join(f"n{k}:{v}" for k, v in sorted(votes.items(), key=lambda kv: -kv[1])))
    print("Neurons kept in every fold are robustly useful; kept in 0-1 are the retune targets.")


if __name__ == "__main__":
    main()
