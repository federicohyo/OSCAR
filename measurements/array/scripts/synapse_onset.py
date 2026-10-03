#!/usr/bin/env python3
"""Characterize the 4-bit weight code by THRESHOLD BIAS rather than by firing rate.

Why onset bias rather than firing rate. At every soma operating point reachable on this die the neuron's rate
response to synaptic drive is a cliff: below threshold it emits nothing, and the moment the
delivered charge crosses threshold it fires at close to the input rate (~900 Hz at 800 Hz in).
Lowering the leak to buy temporal summation makes the neuron free-run instead (w=0 fires at
several hundred Hz). So the rate carries one bit -- fired / silent -- and a weight sweep
read out by rate can only ever produce the staircase of zeros and saturations seen in the
first scans. That is a property of the neuron rather than the synapse.

What to do instead. A sharp threshold is an excellent null detector. For each weight word we
find the excitatory branch bias V at which that word just makes the neuron fire. Because the
branches run in weak inversion, current is exponential in gate voltage,

    I(V) = I0 exp(V / nUT)

so a word delivering k times the unit current reaches the same threshold current at a bias
lower by exactly nUT*ln(k):

    V_onset(w) = V0 - nUT * ln( A(w) )

where A(w) is the word's delivered charge in units of one branch. The onset voltage is thus a
LOGARITHMIC READOUT of synaptic efficacy, graded and precise even where the rate stays blunt, and
a plot of V_onset against log w is a straight line of slope -nUT exactly when the code is
linear in w -- i.e. exactly when the branches are binary weighted.

Three stages:

  branches -- onset of each single-bit word (1,2,4,8) => each branch's own offset, i.e. the
              device mismatch between the four weight branches;
  slope    -- onset of words with 1,2,3,4 equal branches (1,3,7,15) => nUT, from the shift
              per doubling of delivered current;
  code     -- onset of all 16 words, before and after applying a calibrated bias ladder that
              makes the branch currents 1:2:4:8.

Everything is repeated, so every onset carries an error bar.
"""

import argparse
import csv
import json
import math
import os
import random
import time

from meas_common import BridgeSession, load_biases
from synapse_rate_transfer import BIAS_PATTERN, inject, program

JCH = [f"JExcWn{i}" for i in range(4)]


def set_branches(b, volts, settle=0.08):
    """Write only the four weight-branch biases (fast: avoids re-writing all 24 channels)."""
    for name, v in zip(JCH, volts):
        b.bias(name, float(v))
    time.sleep(settle)


def fires(b, neuron, volts, rate, spikes, min_spikes, quiet_s):
    """One fire / no-fire decision at a given branch bias.

    The weight word and its route are staged ONCE per word by the caller and left alone: only
    the branch biases move during a bisection, so re-issuing P/S/M and paying its settling
    time on every step would triple the cost of the search for nothing.
    """
    set_branches(b, volts)
    counts, el, acc = inject(b, rate, spikes, quiet_s=quiet_s)
    return counts[neuron] >= min_spikes, counts[neuron], acc


def find_onset(b, syn, neuron, weight, base_volts, offsets, lo, hi, tol, rate, spikes,
               min_spikes, quiet_s=0.25, verbose=False):
    """Bisect the common-mode branch bias for the lowest V at which `weight` fires.

    `offsets` shifts each branch relative to the common-mode value, which is how a calibrated
    binary ladder is applied. Returns None if the word does not fire even at `hi`.
    """
    def volts(v):
        return [min(1.7, max(0.0, v + o)) for o in offsets]

    program(b, syn, neuron, weight, 0.25, 0, 200.0)   # stage the word once for the whole search

    ok_hi, n_hi, _ = fires(b, neuron, volts(hi), rate, spikes, min_spikes, quiet_s)
    if not ok_hi:
        return None, n_hi
    ok_lo, n_lo, _ = fires(b, neuron, volts(lo), rate, spikes, min_spikes, quiet_s)
    if ok_lo:
        return lo, n_lo          # already firing at the bottom of the range
    a, c = lo, hi
    while c - a > tol:
        m = 0.5 * (a + c)
        ok, _, _ = fires(b, neuron, volts(m), rate, spikes, min_spikes, quiet_s)
        if ok:
            c = m
        else:
            a = m
        if verbose:
            print(f"      bisect w={weight:2d}  [{a:.4f},{c:.4f}]")
    return 0.5 * (a + c), n_hi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--rate", type=float, default=800.0)
    ap.add_argument("--spikes", type=int, default=300)
    ap.add_argument("--min-spikes", type=int, default=10, help="output spikes counted as 'fired'")
    ap.add_argument("--lo", type=float, default=0.355)
    ap.add_argument("--hi", type=float, default=0.475)
    ap.add_argument("--quiet", type=float, default=0.25, help="link-quiet time ending a count")
    ap.add_argument("--tol", type=float, default=0.002)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--bias", default=None)
    ap.add_argument("--stages", default="branches,slope,code",
                    help="comma list of stages to run")
    ap.add_argument("--ladder", default=None,
                    help="JSON file of per-branch offsets to apply in the 'code' stage")
    ap.add_argument("--outdir", default="data/synapse")
    ap.add_argument("--tag", default="n5")
    ap.add_argument("--seed", type=int, default=20260728)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    os.makedirs(args.outdir, exist_ok=True)
    base = load_biases(args.bias or BIAS_PATTERN.format(k=args.neuron))
    rng = random.Random(args.seed)
    results = {"neuron": args.neuron, "rate_hz": args.rate, "spikes": args.spikes,
               "min_spikes": args.min_spikes, "tol": args.tol, "repeats": args.repeats}

    csv_path = os.path.join(args.outdir, f"onset_{args.tag}.csv")
    with BridgeSession(verbose=args.verbose) as b, open(csv_path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["stage", "repeat", "weight", "onset_v", "offsets"])

        b.send(f"MASK {1 << args.neuron}")     # only the measured neuron streams
        time.sleep(0.2)
        b.apply_biases(base)
        time.sleep(1.0)

        zero = [0.0, 0.0, 0.0, 0.0]

        def zero_control(stage, offsets):
            """w = 0 baseline for this stage's bracket.

            At leak biases below vleakn = 0.225 V the soma free-runs, and spontaneous
            activity then reads as synaptic response, so a bracket is only usable if the
            silent word stays silent across all of it. `find_onset` returns None when the
            word stays silent even at `hi`, which is the pass condition; any voltage it
            returns is the bias at which spontaneous firing starts and therefore a hard
            floor on every onset measured in this stage.
            """
            v, n = find_onset(b, args.syn, args.neuron, 0, base, offsets,
                              args.lo, args.hi, args.tol, args.rate, args.spikes,
                              args.min_spikes, args.quiet, args.verbose)
            wr.writerow([stage + "_zeroctl", 0, 0, "" if v is None else f"{v:.4f}",
                         ";".join(f"{o:.4f}" for o in offsets)])
            f.flush()
            if v is None:
                print(f"  [w=0 control] silent across [{args.lo:.3f},{args.hi:.3f}] V -- "
                      f"bracket clean (max count {n})")
            else:
                print(f"  [w=0 control] FIRES from {v:.4f} V -- spontaneous activity "
                      f"contaminates this bracket above that bias")
            return v

        def sweep(stage, words, offsets, label):
            print(f"\n--- {label} ---")
            table = {w: [] for w in words}
            for rep in range(args.repeats):
                order = list(words)
                rng.shuffle(order)
                for w in order:
                    t_pt = time.time()
                    v, n = find_onset(b, args.syn, args.neuron, w, base, offsets,
                                      args.lo, args.hi, args.tol, args.rate, args.spikes,
                                      args.min_spikes, args.quiet, args.verbose)
                    table[w].append(v)
                    wr.writerow([stage, rep, w, "" if v is None else f"{v:.4f}",
                                 ";".join(f"{o:.4f}" for o in offsets)])
                    f.flush()
                    shown = "never fired" if v is None else f"{v:.4f} V"
                    print(f"  rep{rep} w={w:2d}  onset {shown}   [{time.time()-t_pt:.0f}s]")
            return table

        def summarize(table):
            out = {}
            for w, vals in table.items():
                good = [v for v in vals if v is not None]
                if not good:
                    out[w] = {"mean": None, "std": None, "n": 0}
                    continue
                m = sum(good) / len(good)
                sd = (sum((x - m) ** 2 for x in good) / len(good)) ** 0.5 if len(good) > 1 else 0.0
                out[w] = {"mean": m, "std": sd, "n": len(good)}
            return out

        if "branches" in stages:
            results["zero_control_branches"] = zero_control("branches", zero)
            t = sweep("branches", [1, 2, 4, 8], zero, "per-branch onset (single-bit words)")
            s = summarize(t)
            results["branches"] = {str(k): v for k, v in s.items()}
            print("\n  branch onsets (lower = stronger branch):")
            live = {w: s[w]["mean"] for w in (1, 2, 4, 8) if s[w]["mean"] is not None}
            if live:
                ref = min(live.values())
                for w in (1, 2, 4, 8):
                    m, sd = s[w]["mean"], s[w]["std"]
                    if m is None:
                        print(f"    bit {w.bit_length()-1}: never fired")
                    else:
                        print(f"    bit {w.bit_length()-1}: {m:.4f} +/- {sd:.4f} V   "
                              f"(+{(m-ref)*1000:5.1f} mV vs strongest)")

        if "slope" in stages:
            results["zero_control_slope"] = zero_control("slope", zero)
            t = sweep("slope", [1, 3, 7, 15], zero,
                      "onset vs number of equal branches (gives nUT)")
            s = summarize(t)
            results["slope_raw"] = {str(k): v for k, v in s.items()}
            pts = [(math.log(bin(w).count("1")), s[w]["mean"])
                   for w in (1, 3, 7, 15) if s[w]["mean"] is not None]
            if len(pts) >= 2:
                n = len(pts)
                sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
                sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
                slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
                nut = -slope
                results["nUT_volts"] = nut
                results["delta_per_octave_mV"] = nut * math.log(2) * 1000
                print(f"\n  fit: V_onset = V0 - nUT*ln(k branches)")
                print(f"  nUT = {nut*1000:.1f} mV  ->  a doubling of current needs "
                      f"{nut*math.log(2)*1000:.1f} mV")

        if "code" in stages:
            offsets = zero
            if args.ladder:
                with open(args.ladder) as lf:
                    offsets = json.load(lf)["offsets"]
                print(f"\napplying calibrated ladder offsets: "
                      f"{['%.4f' % o for o in offsets]}")
            results["zero_control_code"] = zero_control("code", offsets)
            t = sweep("code", list(range(1, 16)), offsets,
                      "onset of all 15 non-zero weight words")
            s = summarize(t)
            key = "code_ladder" if args.ladder else "code_equal"
            results[key] = {str(k): v for k, v in s.items()}

        b.send("MASK 65535")

    json_path = os.path.join(args.outdir, f"onset_{args.tag}.json")
    with open(json_path, "w") as jf:
        json.dump(results, jf, indent=2)
    print(f"\nwrote {csv_path}\nwrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
