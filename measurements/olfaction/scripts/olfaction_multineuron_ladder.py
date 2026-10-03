#!/usr/bin/env python3
"""Build the ladder from MISMATCH across neurons instead of from bias reloads.

The bias DACs on this die are ARRAY-WIDE -- 24 channels shared by all 16 neurons -- so
"give each neuron its own level" is not something the hardware can do: loading a level
sets the operating point for everything. What it can do is better. At one global setting
the neurons switch at DIFFERENT counts because they are mismatched, so a single setting
yields as many levels as there are usable neurons, and two settings yield twice that.

That turns the ladder from a sequence of reloads into a small number of parked operating
points, which is what makes pipelining real: within a setting every neuron is live at
once, so one neuron's 30 ms membrane re-arm overlaps the others' bursts instead of
serialising behind them.

This measures the raw material: for each candidate bias setting, p(fire | N) over all N
for every neuron, unmasked so all of them are read at once. The output is a table of
(setting, neuron) -> switching count, from which two settings can be chosen whose
combined counts spread best over the burst alphabet.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_multineuron_ladder.py
"""
import argparse, glob, json, os, re, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from olfaction_graded_hunt import Scope

BIAS = "ofxCaravanViewer/bin/comparator_n14_lvl{L}.biases"
MULTI = "ofxCaravanViewer/bin/comparator_multi_{L}.biases"


def bias_path(L):
    """Settings are named either by n14's ladder (an integer) or by the multi-neuron
    operating points A/B, which are the two global settings at which more than one neuron
    is simultaneously in range."""
    return MULTI.format(L=L) if str(L).isalpha() else BIAS.format(L=L)


def probe_all(b, k_list, n, reps, wait):
    """One burst per neuron per rep, unmasked: every neuron is read at its own address.

    Routed one at a time because the input path latches a single 4-bit neuron address --
    fan-out stays off on this die -- but the READ is shared, so the cost of adding a
    neuron is one more burst rather than one more acquisition."""
    hit = {k: 0 for k in k_list}
    for _ in range(reps):
        for k in k_list:
            b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.03)
            b.drain(max_lines=100000)
            if n > 0:
                b.send(f"BURST {n}")
            time.sleep(wait)
            c = [0] * 16
            for _ in range(3):
                b.drain(c); time.sleep(0.02)
            hit[k] += 1 if c[k] > 0 else 0
    return {k: hit[k] / reps for k in k_list}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default="14,5,11,2")
    ap.add_argument("--levels", default="", help="bias files to try (default: all on disk)")
    ap.add_argument("--nmax", type=int, default=32)
    ap.add_argument("--reps", type=int, default=6)
    ap.add_argument("--wait", type=float, default=0.25)
    ap.add_argument("--out", default="data/olfaction_multineuron_ladder.json")
    args = ap.parse_args()
    ks = [int(x) for x in args.neurons.split(",")]
    if args.levels:
        levels = [x if x.isalpha() else int(x) for x in args.levels.split(",")]
    else:
        levels = sorted(int(re.search(r"lvl(\d+)", f).group(1))
                        for f in glob.glob(BIAS.format(L="*")))
    NS = list(range(0, args.nmax + 1))
    sc = Scope()
    rec = {"neurons": ks, "settings": levels, "N": NS, "reps": args.reps, "p": {}}
    print(f"{len(levels)} bias settings x {len(ks)} neurons x {len(NS)} counts, "
          f"{args.reps} reps -- neurons {ks}")

    with BridgeSession() as b:
        b.send(f"MASK {sum(1 << k for k in ks)}")     # all candidates readable at once
        for L in levels:
            b.apply_biases(load_biases(bias_path(L))); time.sleep(0.85)
            rows = {k: [] for k in ks}
            for n in NS:
                p = probe_all(b, ks, n, args.reps, args.wait)
                for k in ks:
                    rows[k].append(p[k])
            rec["p"][str(L)] = {str(k): rows[k] for k in ks}
            sw = {}
            for k in ks:
                r = rows[k]
                sw[k] = next((n for n, q in zip(NS, r) if q >= 1.0), None) \
                    if r[0] <= 0.05 else None       # free-runner: outside the comparator role
            print(f"  setting lvl{L:<3d} -> switches " +
                  " ".join(f"n{k}:{sw[k]}" for k in ks))
            rec.setdefault("switch", {})[str(L)] = {str(k): sw[k] for k in ks}
            json.dump(rec, open(args.out, "w"), indent=2)
    sc.stop()

    # which pair of settings gives the best-spread eight levels?
    S = rec["switch"]
    best = None
    for i, A in enumerate(levels):
        for B in levels[i + 1:]:
            v = sorted(x for k in ks for x in (S[str(A)][str(k)], S[str(B)][str(k)])
                       if x is not None)
            if len(v) < 4:
                continue
            gaps = np.diff(v)
            score = (len(v), float(np.min(gaps)) if len(gaps) else 0.0)
            if best is None or score > best[0]:
                best = (score, A, B, v)
    if best:
        (nlev, mingap), A, B, v = best
        print(f"\nbest pair: lvl{A} + lvl{B} -> {nlev} levels {v}, min gap {mingap:.0f}")
        rec["best_pair"] = dict(a=A, b=B, levels=v, n=nlev, min_gap=mingap)
    json.dump(rec, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
