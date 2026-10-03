#!/usr/bin/env python3
"""Which neurons can be comparators AT THE SAME global bias?

The bias DACs are array-wide, so a "level" is one operating point for all 16 neurons at
once. Whether the tree can use more than one neuron therefore stays separate from "can this
neuron be tuned" -- each one can, separately -- but on "can several be in range
simultaneously". Mismatch decides it, and on this die it first decided badly: at every
setting where n14 comparates, n5, n11 and n2 fire with input at zero.

So screen the whole array instead of guessing a subset.

WHY THIS ONE IS AER-ONLY, against the standing rule to tune on the scope. The monitor mux
puts ONE neuron on the pin at a time, so sixteen membranes are watched one burst at a time, since a single
pass; a scope-based screen would cost sixteen passes. And the question here is binary and
one AER can answer honestly: a free-running neuron fires with input at zero, which is exactly
what p(fire | N=0) reports, and a neuron that stays silent by the top of the alphabet is
out of range whatever its membrane is doing. The scope earns its place on the next step --
resolving a graded ramp between those two extremes -- and the monitor is pinned to one
candidate here so that trace stays watchable while the screen runs.

Two probes per (setting, neuron) rather than a full transfer, so screening sixteen costs about
what a four-neuron ladder did.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_array_screen.py
"""
import argparse, glob, json, re, time

from meas_common import BridgeSession, load_biases
from olfaction_graded_hunt import Scope

BIAS = "ofxCaravanViewer/bin/comparator_n14_lvl{L}.biases"


def burst_all(b, ks, n, reps, wait, settle=0.30):
    """p(fire) for every neuron at burst size n. Routed one at a time -- the input path
    latches a single 4-bit address, fan-out off -- but read unmasked, so the
    cost of another neuron is one more burst rather than another acquisition.

    THE ROUTE MUST SETTLE BEFORE THE WINDOW OPENS. Programming a weight re-runs
    spikesetup, which pulses the LA lines, and those pulses can drive the neuron. Draining
    30 ms after routing left such a spike inside the counting window, so eight neurons
    read p(fire | N=0) = 1 and were called free-running -- while the scope showed them
    sitting quiet, 50 mV below threshold, spiking flush off. The route is therefore
    allowed to settle and the link is drained AFTER it, so the window contains only what
    the burst caused. The calibration script stays clear of this bug because it programs once
    in setup(), outside the measurement loop."""
    hit = {k: 0 for k in ks}
    for _ in range(reps):
        for k in ks:
            b.program_weight(0, 15, exc=True)
            b.route(0, k, exc=True)
            time.sleep(settle)
            b.drain(max_lines=100000)          # flush anything the routing caused
            if n > 0:
                b.send(f"BURST {n}")
            time.sleep(wait)
            c = [0] * 16
            for _ in range(3):
                b.drain(c)
                time.sleep(0.02)
            hit[k] += 1 if c[k] > 0 else 0
    return {k: hit[k] / reps for k in ks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default=",".join(str(i) for i in range(16)))
    ap.add_argument("--levels", default="")
    ap.add_argument("--quieter", default="",
                    help="generate settings QUIETER than a base file instead of reading "
                         "files: 'lvl32:0,2,4,6,8,10' steps vleakn up by those mV. Higher "
                         "vleakn is more leak, so a lower resting potential and a less "
                         "excitable array -- which is the direction that brought neurons "
                         "INTO range: 1 in range at lvl8, 2 at lvl24, 3 at lvl32.")
    ap.add_argument("--nmax", type=int, default=32)
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--wait", type=float, default=0.25)
    ap.add_argument("--monitor", type=int, default=7,
                    help="neuron pinned to the scope pin; the mux carries one at a time")
    ap.add_argument("--out", default="data/olfaction_array_screen.json")
    args = ap.parse_args()
    ks = [int(x) for x in args.neurons.split(",")]
    gen = {}
    if args.quieter:
        base_tag, offs = args.quieter.split(":")
        base = load_biases(BIAS.format(L=int(base_tag.replace("lvl", ""))))
        for mv in [float(x) for x in offs.split(",")]:
            bi = dict(base)
            bi["vleakn"] = round(base["vleakn"] + mv / 1000.0, 5)
            gen[f"{base_tag}+{mv:g}mV"] = bi
        levels = list(gen)
    else:
        levels = ([int(x) for x in args.levels.split(",")] if args.levels else
                  sorted(int(re.search(r"lvl(\d+)", f).group(1))
                         for f in glob.glob(BIAS.format(L="*"))))
    sc = Scope()
    rec = {"neurons": ks, "settings": levels, "reps": args.reps,
           "monitor": args.monitor, "screen": {}}
    print(f"screening {len(ks)} neurons at {len(levels)} settings "
          f"(probes at N=0 and N={args.nmax}); scope pinned to n{args.monitor}")
    print(f"{'setting':>12} | {'in range':>8} | {'free':>4} | which are in range")
    with BridgeSession() as b:
        b.send(f"MASK {sum(1 << k for k in ks)}")
        for L in levels:
            b.apply_biases(gen[L] if gen else load_biases(BIAS.format(L=L)))
            b.monitor(args.monitor)
            time.sleep(0.85)
            p0 = burst_all(b, ks, 0, args.reps, args.wait)
            pm = burst_all(b, ks, args.nmax, args.reps, args.wait)
            good = [k for k in ks if p0[k] <= 0.05 and pm[k] >= 0.95]
            free = [k for k in ks if p0[k] > 0.05]
            dead = [k for k in ks if p0[k] <= 0.05 and pm[k] < 0.95]
            rec["screen"][str(L)] = dict(p0={str(k): p0[k] for k in ks},
                                         pmax={str(k): pm[k] for k in ks},
                                         in_range=good, free_running=free, silent=dead)
            print(f"{str(L):>12} | {len(good):>8} | {len(free):>4} | {good}")
            json.dump(rec, open(args.out, "w"), indent=2)
    sc.stop()
    best = max(rec["screen"].items(), key=lambda kv: len(kv[1]["in_range"]))
    rec["best"] = dict(setting=best[0], neurons=best[1]["in_range"])
    json.dump(rec, open(args.out, "w"), indent=2)
    print(f"\nbest setting: {best[0]} with {len(best[1]['in_range'])} in range: "
          f"{best[1]['in_range']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
