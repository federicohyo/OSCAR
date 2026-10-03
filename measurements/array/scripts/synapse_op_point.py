#!/usr/bin/env python3
"""Find a bias point where the 4-bit weight code is GRADED, not a binary switch.

At the reservoir operating point (`_jul10`) the synapse is tuned for maximum drive: weight
words 1..8 sit under the leak floor and produce exactly zero output, while w=15 fires the
neuron once per input spike (gain saturated at 1). Neither end is a measurement of the code.

A graded code needs, for every weight word w:

    leak floor / R  <  A(w)          the EPSP train out-runs the leak, so out_hz > 0
    A(15)           <  theta         one EPSP alone stays below firing, so out_hz < R

i.e. the per-branch efficacy A must sit in a window bounded below by the leak and above by
the threshold. This scans the excitatory branch bias JExcWn0..3 (moved together, which
preserves the binary ratio between branches) at a fixed high input rate, and reports for each
candidate how many of the probe weights land strictly inside the window.

    ./.venv-meas/bin/python3 synapse_op_point.py --neuron 5 --rate 800
"""

import argparse
import os
import time

from meas_common import BridgeSession, load_biases, REPO_ROOT
from synapse_rate_transfer import BIAS_PATTERN, inject, program


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--rate", type=float, default=800.0)
    ap.add_argument("--spikes", type=int, default=200)
    ap.add_argument("--probe-weights", default="1,2,4,8,15")
    ap.add_argument("--jexc", default="0.26,0.28,0.30,0.32,0.34,0.36,0.38",
                    help="JExcWn0..3 ladder (NMOS: higher V = more current)")
    ap.add_argument("--vleakn", type=float, default=None)
    ap.add_argument("--vthrdn", type=float, default=None)
    ap.add_argument("--bias", default=None)
    ap.add_argument("--settle", type=float, default=0.3)
    args = ap.parse_args()

    probes = [int(x) for x in args.probe_weights.split(",") if x.strip()]
    ladder = [float(x) for x in args.jexc.split(",") if x.strip()]
    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    if args.vleakn is not None:
        base["vleakn"] = args.vleakn
    if args.vthrdn is not None:
        base["vthrdn"] = args.vthrdn

    print(f"neuron {args.neuron}, input {args.rate:.0f} Hz, {args.spikes} spikes/point")
    print(f"graded window: 0 < out_hz < {args.rate:.0f} Hz (saturation = fires on every input)\n")

    best = []
    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")
        time.sleep(0.2)
        for jv in ladder:
            biases = dict(base)
            for i in range(4):
                biases[f"JExcWn{i}"] = jv
            b.apply_biases(biases)
            time.sleep(0.8)
            row = {}
            for w in probes:
                program(b, args.syn, args.neuron, w, args.settle, 30, 200.0)
                counts, elapsed, acc = inject(b, args.rate, args.spikes)
                row[w] = counts[args.neuron] / elapsed if elapsed > 0 else 0.0
            graded = sum(1 for w in probes if 0.0 < row[w] < 0.9 * args.rate)
            cells = "  ".join(f"w{w:2d}={row[w]:7.1f}" for w in probes)
            print(f"JExcWn={jv:.3f}  {cells}   graded {graded}/{len(probes)}")
            best.append((graded, jv, row))
        b.send("MASK 65535")

    best.sort(key=lambda t: (-t[0], t[1]))
    top = best[0]
    print(f"\nbest: JExcWn={top[1]:.3f} with {top[0]}/{len(probes)} probe weights in the "
          f"graded window")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
