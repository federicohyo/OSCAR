#!/usr/bin/env python3
"""Score the hybrid tree from the measured node decisions.

Walks the ensemble using the analog outcome at every node visit instead of the arithmetic
test, and reports the three rungs so the analog cost is attributable:

  (i)   full-precision digital        -- the reference baseline
  (ii)  same model, array representation, executed DIGITALLY -- the algorithm's ceiling
  (iii) same model, executed with the analog comparisons     -- this measurement

Only the (ii) -> (iii) gap is the substrate's cost. Also reports per-node disagreement
between the analog decision and what the arithmetic test would have returned, which is
the quantity the tolerance simulation budgeted at 10%.

Partial runs are scoreable: nodes not yet measured fall back to the arithmetic test and
are reported as such, so a checkpoint mid-run still gives a number with a stated caveat.

    ./.venv-meas/bin/python3 olfaction_hybrid_score.py
"""
import argparse, json
import numpy as np

from olfaction_hybrid_model import acc, predict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="data/olfaction_hybrid_model.json")
    ap.add_argument("--chip", default="data/olfaction_hybrid_chip.npz")
    ap.add_argument("--out", default="data/olfaction_hybrid_score.json")
    args = ap.parse_args()
    m = json.load(open(args.model))
    z = np.load(args.chip, allow_pickle=True)
    fire, nodes = z["fire"], m["nodes"]
    B = np.array(m["test_bursts"], dtype=int)
    Y = np.array(m["test_labels"]); it = np.array(m["test_trial"])
    nc = len(m["classes"])
    inter = [i for i, n in enumerate(nodes) if not n["leaf"]]
    done = [i for i in inter if (fire[i] >= 0).all()]
    print(f"{len(done)}/{len(inter)} nodes measured on chip "
          f"({100*len(done)/len(inter):.0f}%)")

    ref = np.array([[int(B[j][nodes[i]["f"]] >= nodes[i]["switch"]) for j in range(len(B))]
                    for i in inter])
    meas = fire[inter]
    ok = meas >= 0
    dis = float((meas[ok] != ref[ok]).mean())
    print(f"analog vs arithmetic node decisions: {dis*100:.2f}% disagree "
          f"({int((meas[ok] != ref[ok]).sum())} of {int(ok.sum())} comparisons)")

    def fire_fn(i, j):
        v = fire[i, j]
        return bool(v) if v >= 0 else bool(B[j][nodes[i]["f"]] >= nodes[i]["switch"])

    p3 = predict(nodes, m["roots"], np.array(m["test_ordinal"]), nc, fire=fire_fn)
    a3, v3 = acc(p3, Y, it, nc)
    d1, d2 = m["digital_full"], m["digital_snapped"]
    print(f"\n(i)   full-precision digital        per-chunk {d1['per_chunk']:.3f}"
          f"  voted5 {d1['voted5']:.3f}")
    print(f"(ii)  array representation, digital  per-chunk {d2['per_chunk']:.3f}"
          f"  voted5 {d2['voted5']:.3f}")
    print(f"(iii) executed on the analog array   per-chunk {a3:.3f}  voted5 {v3:.3f}")
    print(f"\n  representation costs  {d1['voted5']-d2['voted5']:+.3f} voted")
    print(f"  the analog substrate  {v3-d2['voted5']:+.3f} voted")

    # per-level disagreement: the levels were placed independently, so a drifted one
    # shows up here rather than as a diffuse accuracy loss
    print("\n  level | nodes | comparisons | disagree")
    per = {}
    for L in sorted({nodes[i]["level"] for i in inter}):
        g = [c for c, i in enumerate(inter) if nodes[i]["level"] == L]
        mk = ok[g]
        if not mk.any():
            continue
        d = float((meas[g][mk] != ref[g][mk]).mean())
        per[str(L)] = d
        print(f"  {L:5d} | {len(g):5d} | {int(mk.sum()):11d} | {d*100:6.2f}%")

    # Uncertainty on the voted number, so it can be plotted beside points that carry one.
    # Bootstrap over TRIALS, not chunks: the five chunks voted into one decision are not
    # five independent samples. 30 trials give a voted resolution of 1/30 = 0.033, which is
    # the scale any comparison against this number has to respect.
    rng = np.random.default_rng(0)
    tr_ids = np.unique(it)
    ok_tr = np.array([np.bincount(p3[it == j], minlength=nc).argmax() == Y[it == j][0]
                      for j in tr_ids])
    bs = [ok_tr[rng.integers(0, len(ok_tr), len(ok_tr))].mean() for _ in range(4000)]
    ci = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    sd = float(np.std(bs))
    print(f"  voted5 {v3:.3f}, bootstrap over {len(tr_ids)} trials: "
          f"95% CI [{ci[0]:.3f}, {ci[1]:.3f}], sd {sd:.3f}")

    json.dump(dict(nodes_measured=len(done), nodes_total=len(inter),
                   voted5_ci=ci, voted5_sd=sd, n_trials=int(len(tr_ids)),
                   node_disagreement=dis, per_level_disagreement=per,
                   digital_full=d1, digital_snapped=d2,
                   analog=dict(per_chunk=a3, voted5=v3)),
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
