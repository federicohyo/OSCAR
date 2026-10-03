#!/usr/bin/env python3
"""Control: is the output EVOKED by the synapse, or is the neuron free-running?

The JExcWn ladder produced ~360 Hz output at every weight word once the bias passed ~0.43,
which is exactly what a neuron driven by static current looks like -- the weight word would
then be irrelevant and the "graded" window meaningless. This measures, at each candidate bias,
the neuron's rate with NO input spikes at all (baseline) alongside its rate under stimulation,
so evoked = stimulated - baseline can be separated from free-run.

A bias point is only usable for weight-code characterization if baseline ~ 0.
"""

import argparse
import time

from meas_common import BridgeSession, load_biases
from synapse_rate_transfer import BIAS_PATTERN, inject, program, drain


def measure_baseline(b, neuron, window_s):
    """Count output spikes over `window_s` with no stimulation at all."""
    counts = [0] * 16
    acc = {"drops": 0, "stalls": 0}
    drain(b, [0] * 16, {"drops": 0, "stalls": 0})
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < window_s:
        drain(b, counts, acc)
        time.sleep(0.005)
    el = time.perf_counter() - t0
    return counts[neuron] / el


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--rate", type=float, default=800.0)
    ap.add_argument("--spikes", type=int, default=200)
    ap.add_argument("--jexc", default="0.39,0.41,0.43,0.45,0.50")
    ap.add_argument("--weights", default="1,15")
    ap.add_argument("--window", type=float, default=0.5)
    ap.add_argument("--vleakn", type=float, default=None)
    ap.add_argument("--bias", default=None, help="bias file (default: per-neuron _jul10)")
    ap.add_argument("--keep-jexc", action="store_true",
                    help="do not override JExcWn0..3; measure the bias file's own ladder")
    args = ap.parse_args()

    ws = [int(x) for x in args.weights.split(",") if x.strip()]
    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    if args.vleakn is not None:
        base["vleakn"] = args.vleakn

    print(f"neuron {args.neuron}: baseline (no input) vs stimulated at {args.rate:.0f} Hz")
    print("a usable bias point has baseline ~ 0\n")

    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")
        time.sleep(0.2)
        ladder = [None] if args.keep_jexc else [float(x) for x in args.jexc.split(",")]
        for jv in ladder:
            biases = dict(base)
            if jv is not None:
                for i in range(4):
                    biases[f"JExcWn{i}"] = jv
            b.apply_biases(biases)
            time.sleep(0.8)
            # baseline with the route staged but nothing fired
            program(b, args.syn, args.neuron, ws[-1], 0.3, 0, 200.0)
            bl = measure_baseline(b, args.neuron, args.window)
            cells = []
            for w in ws:
                program(b, args.syn, args.neuron, w, 0.3, 30, 200.0)
                counts, el, _ = inject(b, args.rate, args.spikes)
                cells.append(f"w{w:2d}: stim={counts[args.neuron] / el:7.1f}")
            verdict = "FREE-RUN" if bl > 5.0 else "ok"
            tag = "file  " if jv is None else f"{jv:.3f}"
            print(f"JExcWn={tag}  baseline={bl:7.1f} Hz  " + "  ".join(cells) + f"   {verdict}")
        b.send("MASK 65535")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
