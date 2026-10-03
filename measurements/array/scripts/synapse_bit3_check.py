#!/usr/bin/env python3
"""Is the MSB weight branch dead, or just weaker than the other three?

The bit map found that JExcWn0/1/2 each drive their own weight bit with near-equal efficacy,
but JExcWn3 at the same bias produced no output for any word. Two very different explanations:

  dead   -- the bit-3 branch or its programming path reads as damaged, so word bit 3 contributes nothing and
            the usable code is 3 bits;
  weak   -- the branch simply needs a higher gate bias to reach the same current, in which
            case raising JExcWn3 alone recovers it.

This sweeps JExcWn3 upward with the other three branches held low and the word fixed at
w=8 (bit 3 alone). If the branch is alive anywhere in the DAC's range, it fires here.
"""

import argparse
import time

from meas_common import BridgeSession, load_biases
from synapse_bit_map import measure
from synapse_rate_transfer import BIAS_PATTERN


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--rate", type=float, default=200.0)
    ap.add_argument("--spikes", type=int, default=200)
    ap.add_argument("--lo", type=float, default=0.40, help="bias for the other three branches")
    ap.add_argument("--sweep", default="0.42,0.45,0.48,0.51,0.54,0.57,0.60,0.65,0.70",
                    help="JExcWn3 ladder")
    ap.add_argument("--bit", type=int, default=3)
    ap.add_argument("--bias", default=None)
    args = ap.parse_args()

    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    word = 1 << args.bit

    print(f"neuron {args.neuron}: sweeping JExcWn{args.bit} with the other branches at "
          f"{args.lo:.3f}, word w={word} (bit {args.bit} alone), {args.rate:.0f} Hz in\n")

    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")
        time.sleep(0.2)
        fired = False
        for v in [float(x) for x in args.sweep.split(",")]:
            bb = dict(base)
            for i in range(4):
                bb[f"JExcWn{i}"] = args.lo
            bb[f"JExcWn{args.bit}"] = v
            b.apply_biases(bb)
            time.sleep(0.8)
            hz, acc = measure(b, args.syn, args.neuron, word, args.rate, args.spikes)
            # control: the full word 15 at the same biases, so a silent bit-3 is
            # distinguishable from a silent neuron
            hz15, _ = measure(b, args.syn, args.neuron, 15, args.rate, args.spikes)
            print(f"  JExcWn{args.bit}={v:.3f}  w={word:2d} -> {hz:8.1f} Hz    "
                  f"(w=15 control {hz15:8.1f} Hz)   drop={acc['drops']} stall={acc['stalls']}")
            if hz > 0:
                fired = True

        b.send("MASK 65535")

    print()
    if fired:
        print(f"bit {args.bit} is ALIVE -- it just needs a higher gate bias than the others.")
    else:
        print(f"bit {args.bit} never fired anywhere in the swept range, while the w=15 control "
              f"did.\nThe branch contributes nothing: the usable code is {args.bit} bits.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
