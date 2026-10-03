#!/usr/bin/env python3
"""Diagnose the post-reflash P(fire)=0 on the coincidence detectors, testing the two
likely non-tuning causes before any bias hunting:
  (a) wrong bias set  -> re-apply the Jul-4 coincidence set (default: the _1 variant,
      collected closest to coincidence_array.csv), selectable via --biases;
  (b) unprogrammed synapse weights / route post-reflash -> (re)program weight+route
      explicitly and report whether the neuron then responds.

Gentle on the link: few reps per probe. Does NOT tune biases (guardrail) -- it only
tests the two config hypotheses and reports per-neuron coincidence vs baseline P(fire).
"""
import argparse, os, time
import numpy as np
from meas_common import BridgeSession, load_biases, REPO_ROOT
from coincidence_array import wait_fire, detect_output

BIAS_1 = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_coincidence_1.biases")
BIAS_0 = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_coincidence.biases")


def p_fire(b, first, second, neuron, dt_us, out_idx, trials, window_s, silence_s=0.0):
    fires = 0
    for _ in range(trials):
        b.drain(max_lines=100000)
        b.coincidence(first, second, neuron, dt_us)
        if wait_fire(b, out_idx, window_s):
            fires += 1
        if silence_s:
            time.sleep(silence_s)
    return fires / trials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--biases", default=BIAS_1, help="bias set (default: coincidence_1)")
    ap.add_argument("--neurons", default="14")
    ap.add_argument("--syn-a", type=int, default=0)
    ap.add_argument("--syn-b", type=int, default=2, help="avoid REC_SYN=1 by default")
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--trials", type=int, default=15)
    ap.add_argument("--window", type=float, default=0.03)
    ap.add_argument("--silence-ms", type=float, default=500.0, help="recovery between pairs")
    ap.add_argument("--recur-off", action="store_true", help="send RECURCTRL 0 (recurrency=0)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    neurons = [int(x) for x in args.neurons.split(",")]
    cw = 0.045 + args.window
    sil = args.silence_ms / 1000.0
    print(f"Diagnose coincidence: biases={os.path.basename(args.biases)}, "
          f"syn {args.syn_a}+{args.syn_b} w={args.weight}, silence={args.silence_ms:.0f}ms, "
          f"recur_off={args.recur_off}, neurons {neurons}")

    with BridgeSession(verbose=args.verbose) as b:
        b.apply_biases(load_biases(args.biases)); time.sleep(1.0)
        if args.recur_off:
            b.send("RECURCTRL 0"); time.sleep(0.2)
        print(f"{'neuron':>6} {'out_idx':>7} {'P_1syn':>7} {'P_coinc(0)':>10} {'P_base(40ms)':>12} {'contrast':>8}")
        for n in neurons:
            b.program_weight(args.syn_a, args.weight, exc=True)
            b.program_weight(args.syn_b, args.weight, exc=True); time.sleep(0.2)
            b.route(args.syn_a, n, exc=True); b.route(args.syn_b, n, exc=True)
            b.monitor(n); time.sleep(0.2)
            out_idx = detect_output(b, args.syn_a, args.syn_b, n, reps=15)
            if out_idx is None:
                print(f"{n:>6} {'NONE':>7}  (no output on coincidence -> weights/route/bias too weak)")
                continue
            p1 = p_fire(b, args.syn_a, args.syn_b, n, 60000.0, out_idx, args.trials, cw, sil)
            pc = p_fire(b, args.syn_a, args.syn_b, n, 0.0, out_idx, args.trials, cw, sil)
            pb = p_fire(b, args.syn_a, args.syn_b, n, 40000.0, out_idx, args.trials, cw, sil)
            print(f"{n:>6} {out_idx:>7} {p1:>7.2f} {pc:>10.2f} {pb:>12.2f} {pc-pb:>8.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
