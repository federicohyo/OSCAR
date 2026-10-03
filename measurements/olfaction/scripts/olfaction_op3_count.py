#!/usr/bin/env python3
"""Exact rv32i cycle count for the olfaction OP3 kernel.

Same method as op3_count.py for the ECG tree: block costs transcribed from the
disassembly of firmware/olfaction_kernel/olfaction_kernel.c compiled at
-march=rv32i -O2, driven by trip counts measured on the REAL fitted model and REAL
test features. cycles = instructions + 1 extra per load (VexRiscv load = 2 cycles).

This exists because the first figure quoted for this kernel was an ESTIMATE of 19,200
cycles, and it overshot by more than 2x in the array's favour. An estimate standing
in for a count is what produced the retracted 580x.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_op3_count.py
"""
import json
import numpy as np

# ---- block costs, transcribed from the disassembly ------------------------
# .L5 + .L17  one node visit; BOTH branch directions cost the same
WALK_I, WALK_L = 17, 5
# .L2         one leaf accumulate + tree-loop bookkeeping
LEAF_I, LEAF_L = 11, 1
# .L27 + .L26 per-feature normalise head and tail (address, load, subtract, store)
NORM_I, NORM_L = 14 + 6, 4
# .L24        shift-add multiply, ONE iteration per bit of the multiplier
MUL_I, MUL_L = 7, 0


def cyc(i, l):
    return i + l                      # load costs 2 cycles


e_read0 = (105 + 20 * 480) * 372e-12


def main():
    st = json.load(open("data/olfaction_model_stats.json"))
    visits = st["visits_mean"]
    n_trees = st["n_trees"]
    n_used = st["distinct_features"]

    # multiplier bit length: the smul loop iterates once per bit of recip[ch], a Q8.8
    # reciprocal. Measured from the real per-channel baselines.
    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X = d["X"]; t = np.arange(X.shape[1]) / 1000.0 + float(d["t0"]) / 1000.0
    base = np.abs(X[:, (t >= -0.4) & (t < -0.05), :].mean(axis=1))
    # Scale the reciprocal so it carries ~16 bits of MANTISSA. A Q8.8 reciprocal of a
    # ~1e5 ohm baseline underflows to 1, which would price the multiply at ~1 iteration
    # and silently understate the kernel -- a fixed-point bug rather than a cheap kernel.
    recip = np.array([max(1, int((1 << 40) // max(int(v), 1))) for v in base.ravel()])
    recip = recip >> np.maximum(0, np.array([int(v).bit_length() - 16 for v in recip]))
    bits = float(np.mean([int(v).bit_length() for v in recip]))

    walk = visits * cyc(WALK_I, WALK_L)
    leaf = n_trees * cyc(LEAF_I, LEAF_L)
    norm = n_used * (cyc(NORM_I, NORM_L) + bits * cyc(MUL_I, MUL_L))
    total = walk + leaf + norm
    # A competent implementation avoids the per-decision normalisation entirely by
    # pre-scaling the 746 thresholds per TRIAL instead of 94 features per DECISION.
    # That is the cheapest honest OP3 and therefore the array-unfavourable one.
    total_prescaled = walk + leaf

    print(f"model: {n_trees} trees, {visits:.1f} node visits/decision, "
          f"{n_used} of 400 features normalised")
    print(f"multiplier bit length (measured): {bits:.1f} -> {bits:.1f} shift-add iters\n")
    print(f"{'stage':34s} {'cycles':>9} {'share':>7}")
    for nm, v in (("node traversal", walk), ("leaf accumulate", leaf),
                  ("lazy feature normalisation", norm)):
        print(f"{nm:34s} {v:9,.0f} {100*v/total:6.1f}%")
    print(f"{'TOTAL, normalising per decision':34s} {total:9,.0f}")
    print(f"{'TOTAL, thresholds pre-scaled':34s} {total_prescaled:9,.0f}   <- the cheapest honest OP3")
    E = total_prescaled * 372e-12
    print(f"\n-> {E*1e6:.1f} uJ/decision at 372 pJ/cycle")
    print(f"   (first estimate was 19,200 cyc = 7.1 uJ; ECG tree is 55,328 = 20.6 uJ)")
    print(f"\n   ARRAY READ-OUT ALONE is {e_read0*1e6:.2f} uJ/decision = "
          f"{e_read0/E:.1f}x the ENTIRE digital kernel.")

    P = 0.43e-3
    e_read = e_read0
    print(f"\n{'decisions/s':>12} {'E_array@430uW':>14} {'E_array@100uW':>14} {'verdict'}")
    for f in (10, 20, 35, 50):
        a430, a100 = P / f + e_read, 100e-6 / f + e_read
        print(f"{f:11d}/s {a430*1e6:13.1f}u {a100*1e6:13.1f}u   "
              f"430uW {'win' if a430 < E else 'lose'} {max(a430,E)/min(a430,E):.2f}x | "
              f"100uW {'win' if a100 < E else 'lose'} {max(a100,E)/min(a100,E):.2f}x")
    json.dump({"visits": visits, "n_trees": n_trees, "n_used": n_used,
               "mul_bits": bits, "walk": walk, "leaf": leaf, "norm": norm,
               "total_cycles": total, "E_J": E},
              open("data/olfaction_op3_count.json", "w"), indent=2)
    print("\nwrote data/olfaction_op3_count.json")


if __name__ == "__main__":
    raise SystemExit(main())
