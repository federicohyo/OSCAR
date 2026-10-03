#!/usr/bin/env python3
"""Fine-grid, high-trial coincidence sweep on ONE neuron (Phase 1b, Task A).

Sharpens the grid-quantized Delta-t discrimination of Fig.~\\ref{fig:frontier2} on real
silicon: a sub-millisecond Delta-t grid densest across the window transition band, with
>=100 trials/point, saving ALL raw per-trial outcomes (not just p_fire) so the
discrimination Monte Carlo uses measured per-trial noise. Stock biases only -- if the
neuron is not in a clean graded regime (baseline P(fire) not ~0.5, or no sharp
transition), it STOPS and reports rather than hunting biases.

Reuses the existing bridge primitives and coincidence_array helpers; does not rebuild them.
"""
import argparse
import csv
import time
import numpy as np

from meas_common import BridgeSession, load_biases, REPO_ROOT
from coincidence_array import wait_fire, detect_output
import os

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_coincidence.biases")


def fine_grid(pos_dense_max=3.0):
    """Delta-t grid (ms): dense (0.25 ms) across the core window, medium (0.5 ms) on the
    approach, sparse baseline anchors far out. `pos_dense_max` extends the dense band on
    the positive side to cover a wider coincidence window (default 3.0 ms = the original
    ~2.5 ms n14 case; pass ~6.5 for the scope-tuned 4-5 ms cliff operating point)."""
    hi = max(3.0, float(pos_dense_max))
    seg = []
    seg += [-20.0, -15.0, -10.0, -7.0]            # far-negative baseline anchors
    seg += list(np.arange(-5.0, -3.0, 0.5))       # negative approach
    seg += list(np.arange(-3.0, hi + 0.001, 0.25))  # core window (dense)
    seg += list(np.arange(hi + 0.5, hi + 2.01, 0.5))  # positive approach beyond dense band
    seg += [hi + 3.5, hi + 5.5, hi + 10.5, hi + 15.5]  # far-positive baseline anchors
    return sorted(set(round(float(x), 3) for x in seg))


def trials_at(b, first, second, neuron, dt_us, out_idx, trials, window_s, silence_s):
    """Per-trial fired booleans for one Delta-t. Each trial = two coincidence spikes,
    a short response window, then `silence_s` of quiet so the neuron/RISC-V fully recover
    before the next pair (avoids the saturation that narrows the apparent window)."""
    outcomes = []
    for _ in range(trials):
        b.drain(max_lines=100000)
        b.coincidence(first, second, neuron, dt_us)
        outcomes.append(1 if wait_fire(b, out_idx, window_s) else 0)
        time.sleep(silence_s)
    return outcomes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--syn-a", type=int, default=0)
    ap.add_argument("--syn-b", type=int, default=1)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--trials", type=int, default=40)
    ap.add_argument("--window", type=float, default=0.03, help="response window (s)")
    ap.add_argument("--silence-ms", type=float, default=150.0,
                    help="quiet time between coincidence pairs (recovery, anti-saturation)")
    ap.add_argument("--settle", type=float, default=3.0,
                    help="seconds to wait after biases are set (settle transient)")
    ap.add_argument("--warmup", type=int, default=15,
                    help="initial coincidence pairs to fire and discard (skip transient)")
    ap.add_argument("--out-trials", default="coincidence_finegrid_trials.csv")
    ap.add_argument("--out-summary", default="coincidence_finegrid.csv")
    ap.add_argument("--pos-dense-ms", type=float, default=3.0,
                    help="extend the dense (0.25 ms) band on the +dt side out to this many ms")
    ap.add_argument("--inherit", action="store_true",
                    help="measure the chip's live latched state AS-IS: skip the bias write "
                         "(use the DACs as currently latched); weight+route still programmed")
    ap.add_argument("--force", action="store_true",
                    help="collect the sweep even if the graded-regime check fails (e.g. a weak/"
                         "facilitation-gated peak); records the window as-is instead of STOP")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    dts_ms = fine_grid(args.pos_dense_ms)
    max_dt_s = max(abs(dts_ms[0]), abs(dts_ms[-1])) / 1000.0
    const_window = max_dt_s + args.window
    silence_s = args.silence_ms / 1000.0
    per_trial = const_window + silence_s
    biases = load_biases(args.biases)
    n = args.neuron

    print(f"Fine-grid coincidence: neuron {n}, {len(dts_ms)} Delta-t points "
          f"({min(dts_ms):+.1f}..{max(dts_ms):+.1f} ms), {args.trials} trials/pt, "
          f"{args.silence_ms:.0f} ms silence/pair (~{len(dts_ms)*args.trials*per_trial/60:.0f} min)")

    with BridgeSession(verbose=args.verbose) as b:
        if args.inherit:
            print("INHERIT biases: using the DACs AS CURRENTLY LATCHED (no apply_biases); "
                  "still setting recurrence OFF + weight + route below.")
        else:
            print("Applying biases + forcing recurrence OFF (feedforward)...")
            b.apply_biases(biases); time.sleep(args.settle)   # let biases settle (transient)
        b.send("RECURCTRL 0"); time.sleep(0.2)      # recurrency = 0 (feedforward only)
        b.program_weight(args.syn_a, args.weight, exc=True)
        b.program_weight(args.syn_b, args.weight, exc=True); time.sleep(0.3)
        b.route(args.syn_a, n, exc=True); b.route(args.syn_b, n, exc=True)
        b.monitor(n); time.sleep(0.3)

        out_idx = detect_output(b, args.syn_a, args.syn_b, n, reps=15)
        if out_idx is None:
            print(f"STOP: neuron {n} produced NO OUTPUT at dt=0. "
                  f"Escalate to the user for bias tuning; not hunting biases here.")
            return 2
        print(f"  neuron {n}: output index={out_idx}")

        # discard the initial stimulation transient (warm-up, not recorded)
        if args.warmup > 0:
            print(f"  warm-up: discarding {args.warmup} initial pairs...")
            trials_at(b, args.syn_a, args.syn_b, n, 0.0, out_idx, args.warmup,
                      const_window, silence_s)

        # --- graded-regime sanity (with recovery silence): low baseline, reliable peak ---
        base_pos = np.mean(trials_at(b, args.syn_a, args.syn_b, n, 20000.0, out_idx, 12, const_window, silence_s))
        base_neg = np.mean(trials_at(b, args.syn_b, args.syn_a, n, 20000.0, out_idx, 12, const_window, silence_s))
        peak = np.mean(trials_at(b, args.syn_a, args.syn_b, n, 0.0, out_idx, 12, const_window, silence_s))
        base = 0.5 * (base_pos + base_neg)
        print(f"  regime check: baseline P(fire)@|dt|=20ms = {base:.2f} "
              f"(+{base_pos:.2f}/-{base_neg:.2f}), peak@dt=0 = {peak:.2f}, "
              f"contrast = {peak-base:.2f}")
        # A clean coincidence detector: reliable peak, and a LOW baseline (single-input
        # gating). A high baseline (over-excitable, one input alone fires) is the bad case.
        if not (peak >= 0.75 and base <= 0.60 and (peak - base) >= 0.35):
            if not args.force:
                print(f"STOP: neuron {n} not in a clean graded regime "
                      f"(need peak>=0.75, baseline<=0.60, contrast>=0.35). "
                      f"Escalate to the user for bias tuning; not hunting biases here.")
                return 3
            print(f"  --force: regime check not met (peak={peak:.2f}, base={base:.2f}); "
                  f"collecting the window as-is anyway.")

        # --- fine-grid sweep, saving per-trial outcomes ---
        ft = open(args.out_trials, "w", newline=""); wt = csv.writer(ft)
        wt.writerow(["neuron", "dt_ms", "trial", "fired"])
        fs = open(args.out_summary, "w", newline=""); ws = csv.writer(fs)
        ws.writerow(["neuron", "dt_ms", "trials", "fires", "p_fire"])
        t0 = time.time()
        for k, dt_ms in enumerate(dts_ms):
            if dt_ms >= 0:
                first, second = args.syn_a, args.syn_b
            else:
                first, second = args.syn_b, args.syn_a
            outcomes = trials_at(b, first, second, n, abs(dt_ms) * 1000.0, out_idx,
                                 args.trials, const_window, silence_s)
            for ti, o in enumerate(outcomes):
                wt.writerow([n, f"{dt_ms:.3f}", ti, o])
            fires = int(sum(outcomes)); pf = fires / len(outcomes)
            ws.writerow([n, f"{dt_ms:.3f}", len(outcomes), fires, f"{pf:.4f}"])
            ft.flush(); fs.flush()
            if k % 5 == 0 or dt_ms == dts_ms[-1]:
                print(f"    [{k+1:>3}/{len(dts_ms)}] dt={dt_ms:+6.2f} ms  P={pf:.2f}  "
                      f"({time.time()-t0:.0f}s)")
        ft.close(); fs.close()

    print(f"\nwrote {args.out_trials} (per-trial) and {args.out_summary} (summary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
