#!/usr/bin/env python3
"""How long does the neuron take to return to rest after a hard drive?

Every anomalously high reading in the JExcWn scans landed on the point immediately after a
w=15 stage, and the "free-running" baselines were erratic rather than bias-ordered. Both are
symptoms of one thing: after strong stimulation the neuron keeps firing for a while, so a
measurement taken too soon reports the PREVIOUS weight word, not the one just programmed.

This drives the neuron hard, then watches its output in consecutive short bins with no input,
and reports when it falls silent. That dwell time is what the sweep must wait between points.
"""

import argparse
import time

from meas_common import BridgeSession, load_biases
from synapse_rate_transfer import BIAS_PATTERN, inject, program, drain


def bins_after_drive(b, neuron, nbins, bin_s):
    """Return per-bin output rate with no stimulation, immediately after the caller drove it."""
    out = []
    for _ in range(nbins):
        counts = [0] * 16
        acc = {"drops": 0, "stalls": 0}
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < bin_s:
            drain(b, counts, acc)
            time.sleep(0.005)
        el = time.perf_counter() - t0
        out.append(counts[neuron] / el)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--bias", default=None)
    ap.add_argument("--jexc", type=float, default=None)
    ap.add_argument("--drive-rate", type=float, default=400.0)
    ap.add_argument("--drive-spikes", type=int, default=200)
    ap.add_argument("--bins", type=int, default=12)
    ap.add_argument("--bin-s", type=float, default=0.5)
    args = ap.parse_args()

    biases = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    if args.jexc is not None:
        for i in range(4):
            biases[f"JExcWn{i}"] = args.jexc

    with BridgeSession() as b:
        b.send(f"MASK {1 << args.neuron}")
        time.sleep(0.2)
        b.apply_biases(biases)
        time.sleep(1.0)

        print(f"drive: w=15, {args.drive_spikes} spikes @ {args.drive_rate:.0f} Hz")
        program(b, args.syn, args.neuron, 15, 0.3, 0, 200.0)
        counts, el, _ = inject(b, args.drive_rate, args.drive_spikes)
        print(f"during drive: {counts[args.neuron] / el:.1f} Hz\n")

        print("after drive, no input at all:")
        for i, hz in enumerate(bins_after_drive(b, args.neuron, args.bins, args.bin_s)):
            t = (i + 1) * args.bin_s
            print(f"  t=+{t:4.1f}s  {hz:7.1f} Hz" + ("   <- silent" if hz == 0 else ""))

        print("\nnow reprogram to w=0 (no synaptic drive) and watch again:")
        program(b, args.syn, args.neuron, 15, 0.3, 0, 200.0)
        inject(b, args.drive_rate, args.drive_spikes)
        program(b, args.syn, args.neuron, 0, 0.3, 0, 200.0)
        for i, hz in enumerate(bins_after_drive(b, args.neuron, args.bins, args.bin_s)):
            t = (i + 1) * args.bin_s
            print(f"  t=+{t:4.1f}s  {hz:7.1f} Hz" + ("   <- silent" if hz == 0 else ""))

        b.send("MASK 65535")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
