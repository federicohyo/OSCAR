#!/usr/bin/env python3
"""Scan any one soma bias looking for the regime where the weight code is resolvable.

At the reservoir operating point a single EPSP drives the neuron into a burst, so the output
rate is ~350 Hz for every weight word that fires at all and 0 for the rest: the code cannot be
read off the rate. What the weight sweep needs is the integrating regime the f-I figure
describes -- ten-odd subthreshold EPSPs per output spike, output rate in the tens of Hz -- so
that the rate is proportional to delivered synaptic charge and therefore to the weight.

This sweeps one named bias and reports the output rate for several weight words, flagging
candidates that are both in the target rate band and monotonically ordered in the word.

    ./.venv-meas/bin/python3 synapse_bias_scan.py --scan vthrdn --values 0.75,0.80,0.85,0.90
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
    ap.add_argument("--scan", required=True, help="bias name to sweep, e.g. vthrdn / vleakn / vtaun")
    ap.add_argument("--values", required=True, help="comma-separated ladder for that bias")
    ap.add_argument("--weights", default="1,4,8,15")
    ap.add_argument("--rate", type=float, default=200.0)
    ap.add_argument("--spikes", type=int, default=200)
    ap.add_argument("--jexc", type=float, default=None, help="set all four JExcWn to this first")
    ap.add_argument("--band", default="3,120", help="target output rate band lo,hi (Hz)")
    ap.add_argument("--bias", default=None)
    args = ap.parse_args()

    ws = [int(x) for x in args.weights.split(",") if x.strip()]
    lo_b, hi_b = [float(x) for x in args.band.split(",")]
    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    if args.jexc is not None:
        for i in range(4):
            base[f"JExcWn{i}"] = args.jexc

    print(f"neuron {args.neuron}: sweeping {args.scan}, {args.rate:.0f} Hz in, "
          f"target band {lo_b:.0f}-{hi_b:.0f} Hz\n")

    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")
        time.sleep(0.2)
        for v in [float(x) for x in args.values.split(",")]:
            bb = dict(base)
            bb[args.scan] = v
            b.apply_biases(bb)
            time.sleep(0.8)
            row = {}
            for w in ws:
                row[w], _ = measure(b, args.syn, args.neuron, w, args.rate, args.spikes)
            vals = [row[w] for w in ws]
            in_band = sum(1 for x in vals if lo_b <= x <= hi_b)
            mono = all(vals[i] <= vals[i + 1] + 1e-9 for i in range(len(vals) - 1))
            cells = "  ".join(f"w{w:2d}={row[w]:7.1f}" for w in ws)
            tag = []
            if in_band == len(ws):
                tag.append("in-band")
            if mono:
                tag.append("monotonic")
            print(f"  {args.scan}={v:.3f}  {cells}   {' '.join(tag) if tag else ''}")
        b.send("MASK 65535")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
