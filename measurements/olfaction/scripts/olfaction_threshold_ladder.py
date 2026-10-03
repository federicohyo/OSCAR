#!/usr/bin/env python3
"""Spread the 16 neurons' thresholds into a bank of distinct comparator levels.

The hybrid tree (olfaction.md 6.15-6.16) uses the array as a bank of threshold
comparators while the RISC-V walks the tree. The comparators are sharp enough --
measured 1.8% per-comparison error against a 10% budget -- but they cluster: at
the reference biases n2 fires at one input spike (zero dynamic range), n1 and n5
both switch between 1 and 2, and only n11 sits as high as 4-5. A bank of near-identical
comparators are too coarse for a tree's thresholds, and quantising to 16 distinct levels
is what costs only 0.045 voted.

So bisect vthrdn per neuron until neuron k switches at input level k+1: fires reliably
at its level, stays silent one level below. Higher vthrdn raises the threshold (the
quieter direction, bench_bias_lint.QUIETER_IF).

A neuron that stays unplaced -- because it silences before reaching its level, or
still fires at level zero at the bottom of the range -- is reported rather than forced.
The bank is only as good as the levels actually achieved, and pretending otherwise would
put a fictitious threshold into the tree.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_threshold_ladder.py
"""
import argparse, json, os, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance


def p_fire(b, k, n, hz, reps):
    got = 0
    for _ in range(reps):
        b.drain(max_lines=100000)
        c = b.inject_spikes(hz, n)
        got += 1 if int(c[k]) > 0 else 0
    return got / reps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default=",".join(map(str, range(16))))
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--hz", type=float, default=400.0)
    ap.add_argument("--span", type=float, default=0.150, help="vthrdn search half-range (V)")
    ap.add_argument("--iters", type=int, default=8)
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--write", default="ofxCaravanViewer/bin/bias_ladder_25mhz_n{k}.biases")
    ap.add_argument("--out", default="data/olfaction_threshold_ladder.json")
    args = ap.parse_args()
    neurons = [int(x) for x in args.neurons.split(",")]

    # CHARACTERISE, then assign. Forcing each neuron to a preassigned level and bisecting
    # vthrdn held for 1/16: at weight 15 one input spike already fires almost any neuron and
    # +/-150 mV of threshold leaves that unchanged. Charge per spike is the coarse knob, so
    # sweep the weight, find where each neuron switches, and hand out the levels the array
    # can actually reach.
    def switch_level(b, k, nmax=16):
        """Smallest N with P(fire|N) >= 0.9, by binary search; nmax+1 if it never fires."""
        if p_fire(b, k, 1, args.hz, args.reps) >= 0.9:
            return 1
        if p_fire(b, k, nmax, args.hz, args.reps) < 0.9:
            return nmax + 1
        lo, hi = 1, nmax
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if p_fire(b, k, mid, args.hz, args.reps) >= 0.9:
                hi = mid
            else:
                lo = mid
        return hi

    res, placed = {}, 0
    weights = [1, 2, 3, 4, 6, 8, 15]
    print(f"{'n':>3} | switching level at weight " + " ".join(f"{w:>3}" for w in weights))
    table = {}
    with BridgeSession() as b:
        for k in neurons:
            base = load_biases(args.bias_pattern.format(k=k))
            b.send(f"MASK {1 << k}")
            b.apply_biases(base); b.monitor(k); time.sleep(0.5)
            row = {}
            for w in weights:
                b.program_weight(0, w, exc=True); b.route(0, k, exc=True); time.sleep(0.03)
                row[w] = switch_level(b, k)
            table[k] = row
            print(f"{k:3d} | " + " ".join(f"{row[w]:>3}" for w in weights)
                  + ("   (>16 = never fires)" if max(row.values()) > 16 else ""))

    # assign: each level 1..16 to the (neuron, weight) that switches closest to it, one
    # neuron per level
    want = list(range(1, len(neurons) + 1))
    free = set(neurons)
    for lvl in want:
        best_k, best_w, best_d = None, None, 99
        for k in free:
            for w, sl in table[k].items():
                if abs(sl - lvl) < best_d:
                    best_k, best_w, best_d = k, w, abs(sl - lvl)
        if best_k is None:
            continue
        ok = best_d == 0
        placed += ok
        res[best_k] = dict(level=lvl, weight=best_w, switch=table[best_k][best_w],
                           err=best_d, placed=bool(ok))
        free.discard(best_k)
    print()
    print(f"{'level':>6} {'neuron':>7} {'weight':>7} {'switches at':>12}  verdict")
    for k, v in sorted(res.items(), key=lambda x: x[1]["level"]):
        print(f"{v['level']:6d} {k:7d} {v['weight']:7d} {v['switch']:12d}  "
              + ("exact" if v["placed"] else f"off by {v['err']}"))
    cov = sorted({v["switch"] for v in res.values() if v["switch"] <= 16})
    print(f"\ndistinct levels the array can actually provide: {cov}  ({len(cov)} of 16)")
    json.dump({"table": {str(k): v for k, v in table.items()},
               "assignment": {str(k): v for k, v in res.items()},
               "distinct_levels": cov}, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    raise SystemExit(0)

    print(f"\n{placed}/{len(neurons)} levels placed")
    print("the hybrid needs distinct levels; unplaced neurons cannot serve as tree nodes")
    json.dump({"ladder": res, "placed": placed,
               **provenance(bias_files=[args.bias_pattern.format(k=k) for k in neurons],
                            task="threshold_ladder")}, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
