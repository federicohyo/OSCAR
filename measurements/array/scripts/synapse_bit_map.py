#!/usr/bin/env python3
"""Which JExcWn bias drives which weight bit, and how strong is each branch?

The 16-word sweep at the reservoir operating point is not monotonic: words 7, 13 and 15 fire
while 8-12 and 14 are silent. Reading the firing words as bit sets,

    {0,1,2} fire   {0,2,3} fire   {0,1,3} silent   {1,2,3} silent

so the words that fire are exactly those containing bits 0 AND 2 -- i.e. the branches are not
in a 1:2:4:8 ratio at this bias point, they are near-equal with device mismatch, and the word
behaves like an unequal thermometer code. That is a claim about the hardware, so it needs a
direct measurement rather than an inference from four words.

Two stages:

  onset  -- with all four branches at the same bias V, sweep V and find where the single-bit
            word w=1 starts firing. That calibrates a "low" bias (no branch alone can fire)
            and a "high" bias (one branch alone can fire).

  map    -- hold three branches low and raise one, then test each single-bit word 1,2,4,8.
            Whichever word responds is the bit that bias controls, and the rate at a common
            bias is that branch's relative efficacy.
"""

import argparse
import time

from meas_common import BridgeSession, load_biases
from synapse_rate_transfer import BIAS_PATTERN, inject, program


def measure(b, syn, neuron, weight, rate, spikes, settle=0.35):
    program(b, syn, neuron, weight, settle, 20, 200.0)
    counts, el, acc = inject(b, rate, spikes)
    return (counts[neuron] / el if el > 0 else 0.0), acc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--rate", type=float, default=200.0)
    ap.add_argument("--spikes", type=int, default=200)
    ap.add_argument("--onset", default="0.38,0.40,0.42,0.44,0.46,0.48,0.50,0.52",
                    help="bias ladder for the w=1 onset scan")
    ap.add_argument("--lo", type=float, default=None, help="skip onset scan, use this low bias")
    ap.add_argument("--hi", type=float, default=None, help="skip onset scan, use this high bias")
    ap.add_argument("--bias", default=None)
    args = ap.parse_args()

    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))

    def set_j(b, values):
        bb = dict(base)
        for i, v in enumerate(values):
            bb[f"JExcWn{i}"] = v
        b.apply_biases(bb)
        time.sleep(0.8)

    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")   # only the measured neuron streams
        time.sleep(0.2)

        lo, hi = args.lo, args.hi
        if lo is None or hi is None:
            print(f"--- onset scan: single-bit word w=1, all four branches at the same bias, "
                  f"{args.rate:.0f} Hz in ---")
            onset = None
            prev = None
            for v in [float(x) for x in args.onset.split(",")]:
                set_j(b, [v] * 4)
                hz, acc = measure(b, args.syn, args.neuron, 1, args.rate, args.spikes)
                print(f"  JExcWn={v:.3f}  w=1 -> {hz:8.1f} Hz   drop={acc['drops']} stall={acc['stalls']}")
                if onset is None and hz > 0:
                    onset = v
                    lo = prev if prev is not None else v - 0.02
                prev = v
            if onset is None:
                print("w=1 never fired across the ladder; extend --onset upward.")
                return 2
            hi = onset
            print(f"\nonset of a single branch: JExcWn={hi:.3f}  (low bias = {lo:.3f})")

        print(f"\n--- bit map: one branch at {hi:.3f}, the other three at {lo:.3f} ---")
        print("a bias that drives bit j should light up ONLY the word w=2^j\n")
        table = {}
        for j in range(4):
            vals = [lo] * 4
            vals[j] = hi
            set_j(b, vals)
            row = {}
            for w in (1, 2, 4, 8):
                hz, _ = measure(b, args.syn, args.neuron, w, args.rate, args.spikes)
                row[w] = hz
            table[j] = row
            cells = "  ".join(f"w={w:2d}:{row[w]:8.1f}" for w in (1, 2, 4, 8))
            live = [w for w in (1, 2, 4, 8) if row[w] > 0]
            print(f"  JExcWn{j} high   {cells}   responds: {live}")

        print(f"\n--- relative branch efficacy: all four at {hi:.3f}, single-bit words ---")
        set_j(b, [hi] * 4)
        eff = {}
        for w in (1, 2, 4, 8):
            hz, _ = measure(b, args.syn, args.neuron, w, args.rate, args.spikes)
            eff[w] = hz
        ref = max(eff.values()) or 1.0
        for w in (1, 2, 4, 8):
            print(f"  w={w:2d} (bit {w.bit_length()-1})  {eff[w]:8.1f} Hz   "
                  f"relative {eff[w]/ref:5.2f}   (binary code would want "
                  f"{w/8:5.2f} of the bit-3 branch)")

        b.send("MASK 65535")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
