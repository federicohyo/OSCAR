#!/usr/bin/env python3
"""Would the mismatch ladder's parallelism pay? Node VISITS per level decide it.

Eleven neurons sit in range at one global setting, but they cluster rather than switching at eleven
different counts: mismatch piles 8-10 of them at N=1 and leaves one or two stragglers
higher (olfaction_mismatch_ladder.py). So the array offers wide parallelism at exactly one
level and zero at the others, and whether that is worth an executor rewrite depends on how
much of the tree's work lands on the wide level.

That payoff is limited. Level 1 carries about an eighth of the visits, because "is this feature above
its lowest quantile" is nearly always true and the tree has little use for it; the visits
concentrate on the middle and upper thresholds, which are one neuron wide. Amdahl then
caps the speed-up near 1.1x, with zero accuracy compensation -- the six-level mismatch
ladder reaches the same ceiling one time-multiplexed neuron already reaches.

The transferable form: mismatch hands you a distribution beyond your choice, and here it is
anti-correlated with where the algorithm spends its visits. For mismatch to pay as a
resource, the spread has to land where the work is.

    ./.venv-meas/bin/python3 olfaction_mismatch_payoff.py
"""
import argparse, json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB

import olfaction_hybrid_model as M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--switch", default="1,2,5,6,14,28",
                    help="switching counts three global settings supply")
    ap.add_argument("--width", default="1:8",
                    help="neurons available per level, 'level:n' comma separated; "
                         "levels not listed are one neuron wide")
    ap.add_argument("--out", default="data/olfaction_mismatch_payoff.json")
    args = ap.parse_args()
    SW = [int(x) for x in args.switch.split(",")]
    W = {s: 1 for s in SW}
    for kv in args.width.split(","):
        k, n = kv.split(":"); W[int(k)] = int(n)

    Ftr, Ytr, Fte, Yte, ite, names = M.load(); nc = len(names)
    ladder = list(range(1, len(SW) + 1))
    ordinal, burst, _ = M.quantiser(Ftr, ladder, SW)
    Qtr, Qte, Bte = ordinal(Ftr), ordinal(Fte), burst(Fte)
    g = HGB(max_iter=10, max_leaf_nodes=8, random_state=0).fit(Qtr, Ytr)
    nodes, roots = M.extract(g, ladder, SW)
    M.check(nodes, roots, Qte, Bte, nc)
    a, v = M.acc(M.predict(nodes, roots, Qte, nc), Yte, ite, nc)

    visits = {s: 0 for s in SW}
    for x in Qte:
        for r in roots:
            i = r
            while not nodes[i]["leaf"]:
                nd = nodes[i]; visits[nd["switch"]] += 1
                i = nd["right"] if x[nd["f"]] > nd["thr"] else nd["left"]
    tot = sum(visits.values())
    serial = sum(visits[s] / W[s] for s in SW)
    frac_wide = max(visits[s] / tot for s in SW if W[s] > 1) if any(
        W[s] > 1 for s in SW) else 0.0
    print(f"ladder {SW}: ceiling per-chunk {a:.3f} voted5 {v:.3f}")
    print(f"\n{'level':>6} {'width':>6} {'visits':>8} {'share':>7} {'serial':>8}")
    for s in SW:
        print(f"{s:>6} {W[s]:>6} {visits[s]:>8} {visits[s]/tot:>6.1%} "
              f"{visits[s]/W[s]:>8.0f}")
    print(f"\nspeed-up {tot/serial:.2f}x -- the wide level carries {frac_wide:.1%} "
          f"of the visits")
    json.dump(dict(switch=SW, width=W, visits={str(k): v for k, v in visits.items()},
                   speedup=tot / serial, per_chunk=a, voted5=v,
                   wide_level_share=frac_wide), open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
