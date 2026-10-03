#!/usr/bin/env python3
"""The ladder built from MISMATCH: switching count of every usable neuron, per setting.

The bias DACs are array-wide, so one setting is one operating point for all 16 neurons.
The screen showed 11 of them sit in range simultaneously (silent with input at zero, firing by
the top of the burst alphabet). Whether that is a ladder or just eleven copies of the same
comparator depends on one thing: do they switch at DIFFERENT counts? Mismatch is the only
thing that could separate them, since the bias is shared.

If they do, the tree gets its levels from devices instead of from bias reloads, and every
level is live at once -- which is what makes pipelining real, because the 30 ms membrane
re-arm of one neuron overlaps the bursts of the others rather than serialising behind
them.

BISECTION rather than a full transfer. The switch is monotone in N, so log2(33) ~ 6 probes find
it instead of 33. Eleven neurons then cost about 2.5 minutes per setting rather than 24.
The N=0 control is still measured explicitly at every neuron, because a free-running
neuron would bisect to 1 and look like the finest comparator in the array.

ROUTE SETTLING. Programming a weight re-runs spikesetup and pulses the LA lines; draining
too soon after leaves such a pulse inside the counting window. That artefact previously
made eight quiet neurons read as free-running -- the scope showed them 50 mV below
threshold rather than spiking -- so the route is allowed to settle and the link drained after it.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_mismatch_ladder.py
"""
import argparse, json, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from olfaction_graded_hunt import Scope

BIAS = "ofxCaravanViewer/bin/comparator_n14_lvl{L}.biases"
MULTI = "ofxCaravanViewer/bin/comparator_multi_{L}.biases"


def bias_path(L):
    return MULTI.format(L=L) if str(L).isalpha() else BIAS.format(L=L)


def pfire(b, k, n, reps, wait, settle=0.30):
    """p(fire) for neuron k at burst size n, with the route settled first."""
    hit = 0
    for _ in range(reps):
        b.program_weight(0, 15, exc=True)
        b.route(0, k, exc=True)
        time.sleep(settle)
        b.drain(max_lines=100000)
        if n > 0:
            b.send(f"BURST {n}")
        time.sleep(wait)
        c = [0] * 16
        for _ in range(3):
            b.drain(c)
            time.sleep(0.02)
        hit += 1 if c[k] > 0 else 0
    return hit / reps


def find_switch(b, k, nmax, reps, wait):
    """Smallest N that fires every repetition, by bisection. None if it free-runs or
    never fires."""
    if pfire(b, k, 0, reps, wait) > 0.05:
        return None, "free-runs"
    if pfire(b, k, nmax, reps, wait) < 1.0:
        return None, "silent"
    lo, hi = 1, nmax                       # hi always fires, lo-1 stays silent
    while lo < hi:
        mid = (lo + hi) // 2
        if pfire(b, k, mid, reps, wait) >= 1.0:
            hi = mid
        else:
            lo = mid + 1
    return lo, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default="1,2,4,5,6,7,9,11,13,14,15")
    ap.add_argument("--settings", default="A,B")
    ap.add_argument("--nmax", type=int, default=32)
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--wait", type=float, default=0.25)
    ap.add_argument("--monitor", type=int, default=7)
    ap.add_argument("--out", default="data/olfaction_mismatch_ladder.json")
    args = ap.parse_args()
    ks = [int(x) for x in args.neurons.split(",")]
    settings = [x if x.isalpha() else int(x) for x in args.settings.split(",")]
    sc = Scope()
    rec = {"neurons": ks, "settings": [str(s) for s in settings], "reps": args.reps,
           "switch": {}}
    print(f"{len(ks)} neurons x {len(settings)} settings, bisection over N<={args.nmax}")

    with BridgeSession() as b:
        b.send(f"MASK {sum(1 << k for k in ks)}")
        for S in settings:
            b.apply_biases(load_biases(bias_path(S)))
            b.monitor(args.monitor)
            time.sleep(0.85)
            row, why = {}, {}
            for k in ks:
                sw, st = find_switch(b, k, args.nmax, args.reps, args.wait)
                row[str(k)] = sw
                why[str(k)] = st
            rec["switch"][str(S)] = row
            rec.setdefault("state", {})[str(S)] = why
            vals = sorted(v for v in row.values() if v is not None)
            print(f"  setting {S}: " + " ".join(f"n{k}:{row[str(k)]}" for k in ks))
            print(f"    -> {len(vals)} levels, distinct {sorted(set(vals))}")
            json.dump(rec, open(args.out, "w"), indent=2)
    sc.stop()

    allv = sorted({v for S in rec["switch"].values()
                   for v in S.values() if v is not None})
    print(f"\ncombined distinct levels across settings: {allv}  (n={len(allv)})")
    rec["combined_levels"] = allv
    rec.update({k: str(v) for k, v in provenance(
        bias_files=[bias_path(s) for s in settings], task="mismatch_ladder").items()})
    json.dump(rec, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
