#!/usr/bin/env python3
"""Phase 2, Experiment (i): the facilitation-gating curve P(fire | inter-pair spacing S).

Turns the reference campaign's qualitative "absolute firing is facilitation-gated" into a measured
P(fire)-vs-pair-spacing curve on real silicon. Delta-t is pinned at the measured peak
(-0.25 ms on n14 -> maximal within-pair summation) so the ONLY variable is the rest
interval S between successive coincidence probes. Raising JExcWn0 (synaptic gain) is
predicted to move the detector toward single-pair (rested, large-S) firing.

Design (see the phase-2 protocol, Experiment (i)):
  * S is the INDEPENDENT variable and is set by the recent history of pair spacing, so
    each S is measured as a TRAIN (block) at fixed spacing -- NOT trial-randomized (that
    would destroy the very quantity). We randomize the ORDER of the S-blocks per repeat.
  * A fixed reference-S block (--s-ref, default 50 ms) runs before every sweep block as a
    slow-drift monitor: if P(fire | S_ref) wanders over the session, we see it.
  * Within a block, the first --warmup pairs reach the steady facilitation state for that
    spacing and are DISCARDED; the rest are recorded.
  * One JExcWn0 per invocation (checkpointed, stop-on-trouble). Run base first, then higher.

Reuses the bridge primitives + coincidence_array helpers; does not rebuild them.
"""
import argparse
import csv
import os
import time
import numpy as np

from meas_common import BridgeSession, load_biases, REPO_ROOT
from coincidence_array import wait_fire, detect_output

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_coincidence.biases")


def block_at_S(b, first, second, neuron, dt_us, out_idx, S_s, window_s, warmup, trials):
    """Deliver a train of coincidence pairs spaced by (window_s + S_s), discard the first
    `warmup` (settle to this spacing's steady facilitation state), record the next `trials`.
    Returns the list of recorded fired booleans."""
    outcomes = []
    total = warmup + trials
    for i in range(total):
        b.drain(max_lines=100000)
        b.coincidence(first, second, neuron, dt_us)
        fired = 1 if wait_fire(b, out_idx, window_s) else 0
        if i >= warmup:
            outcomes.append(fired)
        if S_s > 0:
            time.sleep(S_s)          # inter-pair rest (the swept spacing)
    return outcomes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--syn-a", type=int, default=0)
    ap.add_argument("--syn-b", type=int, default=1)
    ap.add_argument("--weight", type=int, default=15, help="4-bit per-synapse weight")
    ap.add_argument("--jexc0", type=float, default=None,
                    help="override JExcWn0 (synaptic gain) for the weight sweep; "
                         "default = use the preset value")
    ap.add_argument("--peak-dt-ms", type=float, default=-0.25,
                    help="fixed within-pair Delta-t at the measured peak")
    ap.add_argument("--s-grid-ms", default="2,5,10,15,20,30,50,100,300",
                    help="inter-pair rest intervals S to sweep (ms, comma-separated); dense "
                         "across the measured 10-50 ms recovery transition, rested anchors "
                         "at 100/300 ms (P already ~0 by 50 ms on n14)")
    ap.add_argument("--s-ref-ms", type=float, default=50.0,
                    help="fixed reference S, run before each sweep block as a drift monitor")
    ap.add_argument("--window-ms", type=float, default=30.0,
                    help="response window (ms); matches coincidence_finegrid.py so the "
                         "output-spike latency is not clipped. True onset-to-onset spacing "
                         "= window + S.")
    ap.add_argument("--warmup", type=int, default=15,
                    help="pairs per block to settle to steady facilitation (discarded)")
    ap.add_argument("--trials", type=int, default=50, help="recorded pairs per sweep block")
    ap.add_argument("--ref-trials", type=int, default=20, help="recorded pairs per ref block")
    ap.add_argument("--ref-warmup", type=int, default=8)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--settle", type=float, default=3.0)
    ap.add_argument("--min-pfast", type=float, default=0.5,
                    help="pre-check gate: STOP if P(fire) at the fastest spacing is below "
                         "this. Set 0 to force a run (diagnostics).")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="base", help="label for output files / rows")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    S_grid = [float(x) for x in args.s_grid_ms.split(",")]
    window_s = args.window_ms / 1000.0
    n = args.neuron
    dt_us = abs(args.peak_dt_ms) * 1000.0
    # dt<0 -> syn_b leads syn_a (matches coincidence_finegrid.py convention)
    if args.peak_dt_ms >= 0:
        first, second = args.syn_a, args.syn_b
    else:
        first, second = args.syn_b, args.syn_a

    biases = load_biases(args.biases)
    if args.jexc0 is not None:
        biases["JExcWn0"] = args.jexc0
    jexc0 = biases["JExcWn0"]

    trials_path = os.path.join(args.outdir, f"facilitation_{args.tag}_n{n}_trials.csv")
    summ_path = os.path.join(args.outdir, f"facilitation_{args.tag}_n{n}_summary.csv")

    print(f"Facilitation curve: neuron {n}, JExcWn0={jexc0:.4f} (tag={args.tag}), "
          f"Delta-t={args.peak_dt_ms:+.2f} ms fixed, S grid {S_grid} ms, "
          f"{args.repeats} repeats x {args.trials} trials/block, ref S={args.s_ref_ms} ms")

    with BridgeSession(verbose=args.verbose) as b:
        print("Applying biases + forcing recurrence OFF (feedforward)...")
        b.apply_biases(biases); time.sleep(args.settle)
        b.send("RECURCTRL 0"); time.sleep(0.2)
        b.program_weight(args.syn_a, args.weight, exc=True)
        b.program_weight(args.syn_b, args.weight, exc=True); time.sleep(0.3)
        b.route(args.syn_a, n, exc=True); b.route(args.syn_b, n, exc=True)
        b.monitor(n); time.sleep(0.3)

        out_idx = detect_output(b, args.syn_a, args.syn_b, n, reps=15)
        if out_idx is None:
            print(f"STOP: neuron {n} produced NO OUTPUT at dt=0 (JExcWn0={jexc0:.4f}). "
                  f"Escalate to the user; not hunting biases here.")
            return 2
        print(f"  neuron {n}: output index={out_idx}")

        # --- health / contrast pre-check: facilitated (small S) vs rested (large S) ---
        p_fast = np.mean(block_at_S(b, first, second, n, dt_us, out_idx,
                                    min(S_grid) / 1000.0, window_s, 15, 20))
        p_slow = np.mean(block_at_S(b, first, second, n, dt_us, out_idx,
                                    max(S_grid) / 1000.0, window_s, 5, 20))
        print(f"  pre-check: P(fire)@S={min(S_grid):.0f}ms={p_fast:.2f} (facilitated), "
              f"P(fire)@S={max(S_grid):.0f}ms={p_slow:.2f} (rested), "
              f"contrast={p_fast - p_slow:+.2f}")
        if p_fast < args.min_pfast:
            print(f"STOP: even at the fastest spacing P(fire)={p_fast:.2f}<0.5 -- neuron not "
                  f"reliably driven at JExcWn0={jexc0:.4f}. Escalate to the user.")
            return 3

        ft = open(trials_path, "w", newline=""); wt = csv.writer(ft)
        wt.writerow(["tag", "neuron", "jexc0", "repeat", "block", "S_ms", "trial", "fired"])
        fs = open(summ_path, "w", newline=""); ws = csv.writer(fs)
        ws.writerow(["tag", "neuron", "jexc0", "repeat", "block", "S_ms",
                     "trials", "fires", "p_fire"])

        def record(rep, block, S_ms, outcomes):
            for ti, o in enumerate(outcomes):
                wt.writerow([args.tag, n, f"{jexc0:.5f}", rep, block, f"{S_ms:.1f}", ti, o])
            fires = int(sum(outcomes)); pf = fires / max(1, len(outcomes))
            ws.writerow([args.tag, n, f"{jexc0:.5f}", rep, block, f"{S_ms:.1f}",
                         len(outcomes), fires, f"{pf:.4f}"])
            ft.flush(); fs.flush()
            return pf

        t0 = time.time()
        for rep in range(args.repeats):
            order = list(S_grid)
            rng.shuffle(order)
            print(f"  repeat {rep+1}/{args.repeats}, S order: "
                  f"{[f'{s:.0f}' for s in order]}")
            for S_ms in order:
                # drift-monitor reference block first
                ref_out = block_at_S(b, first, second, n, dt_us, out_idx,
                                     args.s_ref_ms / 1000.0, window_s,
                                     args.ref_warmup, args.ref_trials)
                pref = record(rep, "ref", args.s_ref_ms, ref_out)
                # the swept spacing
                out = block_at_S(b, first, second, n, dt_us, out_idx,
                                 S_ms / 1000.0, window_s, args.warmup, args.trials)
                pf = record(rep, "sweep", S_ms, out)
                print(f"    S={S_ms:>6.0f}ms  P={pf:.2f}   (ref@{args.s_ref_ms:.0f}ms "
                      f"P={pref:.2f})   [{time.time()-t0:.0f}s]")

        ft.close(); fs.close()

    print(f"\nwrote {trials_path} (per-trial) and {summ_path} (summary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
