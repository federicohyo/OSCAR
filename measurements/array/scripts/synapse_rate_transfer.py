#!/usr/bin/env python3
"""Synapse rate-transfer: output firing rate vs input stimulation rate, per 4-bit weight word.

This measures the DIGITAL weight code end to end -- the core writes a weight word through
PROGRAM_SYNC, and we read the resulting synaptic gain off the AER output. It is deliberately
NOT a sweep of the analog weight bias JExcWn*: those four biases are held fixed at the loaded
operating point, so anything that moves is attributable to the programmed word.

For each (weight, input rate) point the target neuron is stimulated with a fixed number of
host-paced input spikes and its output spikes are counted over the actual elapsed window.
Points are visited in randomized order within each repeat, so slow drift (temperature, DAC
settling) does not alias into the weight axis and show up as a fake monotonic trend.

Guards, each of which has burned bench time before:
  * biases come from a per-neuron file via apply_bias_dict (never run_neuron_test's single-VREF
    path, which halves the NMOS biases);
  * only the target neuron is unmasked, so the AER bus cannot jam and inflate DROP/STALL;
  * DROPS/STALLS are tallied per point and written to the CSV -- a point with either nonzero is
    not a measurement of the array;
  * a warm-up burst is fired and discarded after every reprogram, because the first stimulation
    after a routing change is a settling transient;
  * an excitatory positive control runs before and after the sweep, so a dead run is
    distinguishable from a real zero.

Output CSV is one row per trial (not per mean), so the analysis can compute its own statistics:
  repeat, weight, input_hz, spikes_in, elapsed_s, out_spikes, out_hz, total_hz, drops, stalls

Example (the reference figure):
  ./.venv-meas/bin/python3 synapse_rate_transfer.py --syn 0 --neuron 5 \
      --weights 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 \
      --rates 100,200,400,600,800 --spikes 300 --repeats 5 \
      --out data/synapse/rate_transfer_n5.csv
"""

import argparse
import csv
import os
import random
import time

from meas_common import BridgeSession, load_biases, REPO_ROOT

# 50 MHz-retuned per-neuron operating point (synaptic efficacy is clock dependent, so the
# biases must come from the clock the sweep actually runs at).
BIAS_PATTERN = os.path.join(
    REPO_ROOT, "ofxCaravanViewer", "bin",
    "bias_synapse_characterization_super_n{k}_jul10.biases",
)


def drain(b, counts, acc):
    """Drain pending bridge output: tally per-neuron spikes and the chip's integrity flags."""
    import queue as _q
    while True:
        try:
            line = b.out_q.get_nowait()
        except _q.Empty:
            return
        if line.startswith("S "):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    nid = int(parts[1])
                except ValueError:
                    continue
                if 0 <= nid <= 15:
                    counts[nid] += 1
        elif line.startswith("DROPS "):
            try:
                acc["drops"] += int(line.split()[1])
            except (ValueError, IndexError):
                pass
        elif line.startswith("STALLS "):
            try:
                acc["stalls"] += int(line.split()[1])
            except (ValueError, IndexError):
                pass


def quiesce(b, quiet_s=0.4, max_s=8.0):
    """Drain and discard until no line has arrived for `quiet_s`. Returns spikes discarded.

    The bridge hands spikes to the host over USB in ~16 ms batches, so packets for spikes the
    chip emitted inside one measurement keep arriving well after it. Without this, a point's
    tail lands in the NEXT point's count and the sweep reports the previous weight word --
    which is exactly what made the first scans erratic and order-dependent.
    """
    counts = [0] * 16
    acc = {"drops": 0, "stalls": 0}
    last = time.perf_counter()
    deadline = last + max_s
    while time.perf_counter() < deadline:
        before = sum(counts)
        drain(b, counts, acc)
        if sum(counts) > before:
            last = time.perf_counter()
        elif time.perf_counter() - last >= quiet_s:
            break
        time.sleep(0.005)
    return sum(counts)


def inject(b, rate_hz, count, quiet_s=0.4):
    """Fire `count` host-paced input spikes at `rate_hz`; return (counts, elapsed_s, flags).

    `elapsed_s` is the measured injection window, not the nominal count/rate -- host pacing
    slips, and dividing by the nominal window would bias every rate differently.

    All output spikes are collected: after injection we keep draining until the link has been
    quiet for `quiet_s`, so the count is complete rather than truncated at an arbitrary tail.
    """
    counts = [0] * 16
    acc = {"drops": 0, "stalls": 0}
    quiesce(b, quiet_s=quiet_s)          # discard anything still in flight from before
    period = 1.0 / rate_hz
    t0 = time.perf_counter()
    next_t = t0
    for _ in range(count):
        now = time.perf_counter()
        if next_t > now:
            time.sleep(next_t - now)
        b.fire(1)
        next_t += period
        drain(b, counts, acc)
    elapsed = time.perf_counter() - t0
    # collect the rest of THIS point's spikes: drain until the link goes quiet
    last = time.perf_counter()
    deadline = last + 8.0
    while time.perf_counter() < deadline:
        before = sum(counts)
        drain(b, counts, acc)
        if sum(counts) > before:
            last = time.perf_counter()
        elif time.perf_counter() - last >= quiet_s:
            break
        time.sleep(0.005)
    return counts, elapsed, acc


def program(b, syn, neuron, weight, settle, warmup_spikes, warmup_hz):
    """Program a weight word, route it, and burn a warm-up burst (settling transient)."""
    b.program_weight(syn, weight, exc=True)   # P must precede S: route programming re-runs spikesetup
    b.route(syn, neuron, exc=True)
    b.monitor(neuron)
    time.sleep(settle)
    if warmup_spikes:
        inject(b, warmup_hz, warmup_spikes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--weights", default="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15")
    ap.add_argument("--rates", default="100,200,400,600,800")
    ap.add_argument("--spikes", type=int, default=300, help="input spikes per (weight,rate) point")
    ap.add_argument("--repeats", type=int, default=5, help="independent repeats -> error bars")
    ap.add_argument("--bias", default=None, help="bias file (default: per-neuron _jul10 50 MHz point)")
    ap.add_argument("--ifdcp", type=float, default=None)
    ap.add_argument("--jexc", type=float, default=None, help="override JExcWn0..3 weight-branch bias")
    ap.add_argument("--vleakn", type=float, default=None, help="override leak bias")
    ap.add_argument("--settle", type=float, default=0.3)
    ap.add_argument("--warmup", type=int, default=30, help="discarded warm-up spikes after reprogram")
    ap.add_argument("--seed", type=int, default=20260728)
    ap.add_argument("--no-shuffle", action="store_true", help="visit points in order (debug only)")
    ap.add_argument("--out", default="data/synapse/rate_transfer.csv")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    weights = [int(x) for x in args.weights.split(",") if x.strip()]
    rates = [float(x) for x in args.rates.split(",") if x.strip()]
    rng = random.Random(args.seed)

    bias_path = args.bias or BIAS_PATTERN.format(k=args.neuron)
    biases = load_biases(bias_path)
    if args.ifdcp is not None:
        biases["ifdcp"] = args.ifdcp
    if args.vleakn is not None:
        biases["vleakn"] = args.vleakn
    if args.jexc is not None:
        for i in range(4):
            biases[f"JExcWn{i}"] = args.jexc

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    npoints = len(weights) * len(rates) * args.repeats
    print(f"bias file : {bias_path}")
    print(f"sweep     : {len(weights)} weights x {len(rates)} rates x {args.repeats} repeats "
          f"= {npoints} points, {args.spikes} spikes each")

    with BridgeSession(verbose=args.verbose) as b, open(args.out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["repeat", "weight", "input_hz", "spikes_in", "elapsed_s",
                     "out_spikes", "out_hz", "total_hz", "drops", "stalls"])

        b.apply_biases(biases)
        time.sleep(1.0)
        b.send(f"MASK {1 << args.neuron}")     # stream only the target neuron: no AER jamming
        time.sleep(0.2)

        # --- positive control: max weight must produce output, else the run is meaningless ---
        program(b, args.syn, args.neuron, 15, args.settle, args.warmup, 200.0)
        pc, el, _ = inject(b, 400.0, 200)
        pc_hz = pc[args.neuron] / el
        print(f"positive control (w=15, 400 Hz in): n{args.neuron} = {pc_hz:.1f} Hz")
        if pc_hz <= 0.0:
            print("ABORT: positive control is silent -- the array is not responding. "
                  "Check biases / power cycle before trusting any zero in this sweep.")
            return 2

        t_start = time.time()
        done = 0
        for rep in range(args.repeats):
            order = [(w, r) for w in weights for r in rates]
            if not args.no_shuffle:
                rng.shuffle(order)
            last_w = None
            for w, rate in order:
                if w != last_w:
                    program(b, args.syn, args.neuron, w, args.settle, args.warmup, 200.0)
                    last_w = w
                counts, elapsed, acc = inject(b, rate, args.spikes)
                out_n = counts[args.neuron]
                out_hz = out_n / elapsed if elapsed > 0 else 0.0
                total_hz = sum(counts) / elapsed if elapsed > 0 else 0.0
                wr.writerow([rep, w, f"{rate:.1f}", args.spikes, f"{elapsed:.4f}",
                             out_n, f"{out_hz:.4f}", f"{total_hz:.4f}",
                             acc["drops"], acc["stalls"]])
                f.flush()
                done += 1
                eta = (time.time() - t_start) / done * (npoints - done)
                print(f"[{done:4d}/{npoints}] rep{rep} w={w:2d} in={rate:6.1f}Hz  "
                      f"out={out_hz:6.2f}Hz ({out_n:4d} spk / {elapsed:.2f}s)  "
                      f"drop={acc['drops']} stall={acc['stalls']}  ETA {eta/60:.1f}min")

        # --- closing positive control: catches drift that would poison the error bars ---
        program(b, args.syn, args.neuron, 15, args.settle, args.warmup, 200.0)
        pc2, el2, _ = inject(b, 400.0, 200)
        pc2_hz = pc2[args.neuron] / el2
        print(f"closing control  (w=15, 400 Hz in): n{args.neuron} = {pc2_hz:.1f} Hz "
              f"(opened at {pc_hz:.1f} Hz)")
        if pc_hz > 0 and abs(pc2_hz - pc_hz) / pc_hz > 0.25:
            print("WARNING: >25% drift between opening and closing control -- "
                  "the operating point moved during the sweep.")

        b.send("MASK 65535")

    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
