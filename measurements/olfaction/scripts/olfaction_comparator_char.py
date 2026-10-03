#!/usr/bin/env python3
"""How good a comparator is one analog neuron? The number the hybrid tree turns on.

The hybrid (olfaction.md 6.15) uses the array as a bank of threshold comparators while
the RISC-V walks the tree. Simulation says that tolerates a LOT of imprecision: with
thresholds quantised to the 16 levels an array can offer, up to 10% of node comparisons
may branch the wrong way for only 0.033 voted accuracy, because a wrong branch in one of
50 boosted trees is outvoted by the other 49. So the whole architecture rests on one
measured quantity -- the chip's per-comparison error rate -- rather than on building the
tree first.

Method: drive one neuron with N input spikes and record whether it fires inside the
window. Repeat over N to trace P(fire | N), whose transition width IS the comparator's
resolution. A node whose feature sits farther from its threshold than that width is
decided reliably; one inside it is a coin toss. The error rate for a given margin then
follows from the fitted curve.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_comparator_char.py
"""
import argparse, json, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default="1,2,5,11")
    ap.add_argument("--nmax", type=int, default=14)
    ap.add_argument("--reps", type=int, default=24)
    ap.add_argument("--hz", type=float, default=400.0)
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--out", default="data/olfaction_comparator.json")
    args = ap.parse_args()
    neurons = [int(x) for x in args.neurons.split(",")]

    res = {}
    with BridgeSession() as b:
        for k in neurons:
            b.send(f"MASK {1 << k}")
            b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
            b.monitor(k); time.sleep(0.7)
            b.program_weight(0, 15, exc=True)
            b.route(0, k, exc=True); time.sleep(0.05)
            curve = []
            for n in range(1, args.nmax + 1):
                fired = 0
                for _ in range(args.reps):
                    b.drain(max_lines=100000)
                    c = b.inject_spikes(args.hz, n)
                    fired += 1 if int(c[k]) > 0 else 0
                curve.append(fired / args.reps)
            res[k] = curve
            p = np.array(curve)
            # transition width: inputs where the answer sits between reliably yes and no
            amb = int(((p > 0.1) & (p < 0.9)).sum())
            print(f"neuron {k:2d}: P(fire|N) = " + " ".join(f"{x:.2f}" for x in curve)
                  + f"   ambiguous over {amb}/{args.nmax} input levels")

    print()
    allp = np.array([res[k] for k in neurons])
    amb = ((allp > 0.1) & (allp < 0.9)).mean(1)
    print(f"transition width: {amb.mean()*100:.0f}% of input levels are ambiguous "
          f"(per-neuron {np.round(amb*100).astype(int).tolist()}%)")
    # if a node's margin is uniform over the input range, the error rate is the chance of
    # landing in the ambiguous band times the coin-toss loss there
    err = amb.mean() * 0.5
    print(f"implied per-comparison error for uniformly distributed margins: "
          f"{err*100:.1f}%")
    print(f"the tree tolerates 10% for -0.033 voted -> "
          + ("WITHIN BUDGET" if err <= 0.10 else "OVER BUDGET"))
    json.dump({"curves": res, "n_levels": args.nmax, "reps": args.reps,
               "ambiguous_frac": amb.tolist(), "implied_error": float(err),
               **provenance(bias_files=[args.bias_pattern.format(k=k) for k in neurons],
                            task="comparator_characterisation")},
              open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
