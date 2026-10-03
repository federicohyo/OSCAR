#!/usr/bin/env python3
"""Trial-to-trial repeatability of the array on ONE repeated beat.

WHY THIS EXISTS. The reference analysis leaves ~1.4 D_eff units unexplained.
Simulation (deff_physical_mechanisms.py) shows the only mechanism that closes that
number is per-trial excitability jitter -- each neuron's threshold redrawn per
presentation -- and it needs ~20% of it. Two physical stories could supply that:

    1/f (flicker) noise   per-device, independent between neurons  -> RAISES D_eff
    temperature drift     common-mode across a 0.21 mm^2 die       -> LOWERS D_eff

Both are currently FITTED parameters. This script measures the thing directly, by
presenting the SAME beat many times and watching how much each neuron's response
moves. Nothing about the ECG task needs a second beat: the question is entirely
about repeatability.

PRE-REGISTERED READOUT (fixed before the run, so the analysis cannot drift):

    per-neuron CV of the spike count over the 2 s window, across trials

  ~20%  -> the jitter fit is physically supported
  ~3%   -> the jitter fit is dead, and the residual needs another explanation
           (3% is what Section 4.2's ~1 mV onset-bias repeatability implies, via
           nU_T = 31.1 mV: exp(1/31.1) - 1 = 3.3%)

Those differ by 6x, so even a noisy CV from 50 trials separates them.

PASS B (separate invocation, --interleave) visits the 16 neurons in rounds instead
of blocks, so that fluctuations can be correlated ACROSS neurons at a common time.
Mean cross-neuron correlation ~0 => per-device (1/f-compatible); substantially
positive => common-mode (temperature), which the simulation says moves D_eff the
wrong way.

CONDITIONS, and how they differ from the DIM recording being explained:
  SAME       per-neuron projected delta encoder (reservoir_input_proj.json), the
             base per-neuron bias family, weight 15, exc+inh on synapse 0, T = 2 s
  DIFFERENT  25 MHz core clock (DIM was 10 MHz) -- confirmed with the user, this is
             how the bench is set up today; and the FIXED read-out path (SRAM
             drain, on-chip Timer0 timestamps) instead of DIM's flash-resident
             read-out with host-arrival times. The latter is deliberate: the old
             path stamps spikes onto an 11.99 ms lattice whose phase is redrawn per
             presentation, which would inject its own trial-to-trial variance into
             exactly the quantity being measured here.

  pkill -f neuron_bridge.py
  PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 repeatability_run.py

PROVENANCE: everything saved here is MEASURED on the fabricated die.
"""
import argparse
import json
import os
import queue
import time

import numpy as np

from meas_common import BridgeSession, load_biases
from reservoir_data import delta_encode_proj
from reservoir_run import INTEGRITY, present_delta

BIAS_PATTERN = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}.biases"
PROJ_CONFIG = "reservoir_input_proj.json"
BEATSET = "beats_nv60_orig.npz"
T_BEAT = 2.0
NN = 16


def drain_quiet(b, quiet_s=0.25, timeout_s=6.0):
    """Drain until the link has been silent for `quiet_s`.

    NOT a fixed sleep. A fixed tail drain lets trial k inherit trial k-1's late
    packets, which presents exactly as trial-to-trial variability -- the quantity
    this script measures. See the host-queue-backlog note in the repo memory.
    """
    t0 = time.time()
    last = time.time()
    while time.time() - t0 < timeout_s:
        try:
            line = b.out_q.get(timeout=0.02)
        except queue.Empty:
            if time.time() - last >= quiet_s:
                return
            continue
        last = time.time()
        if line.startswith("DROPS ") or line.startswith("STALLS "):
            p = line.split()
            if len(p) == 2:
                try:
                    INTEGRITY["drops" if p[0] == "DROPS" else "stalls"] += int(p[1])
                except ValueError:
                    pass


def load_proj(path):
    with open(path) as f:
        return {int(c["neuron"]): c for c in json.load(f)["proj"]}


def pick_beat(beatset, want_label=0, index=None):
    d = np.load(beatset, allow_pickle=True)
    X, y = d["X"], d["y"]
    recs = d["records"] if "records" in d else np.array(["?"] * len(X))
    if index is None:
        index = int(np.where(y == want_label)[0][0])
    return X[index], int(index), int(y[index]), str(recs[index])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=50,
                    help="scored trials per neuron (one extra is run and discarded)")
    ap.add_argument("--neurons", default=",".join(str(i) for i in range(NN)))
    ap.add_argument("--beat-index", type=int, default=None)
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--inh-syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--reload-at", type=int, default=25,
                    help="re-apply the SAME bias file before this trial, as a "
                         "DAC-programming repeatability control (-1 disables)")
    ap.add_argument("--interleave", action="store_true",
                    help="PASS B: visit neurons in rounds instead of blocks, so "
                         "fluctuations can be correlated across neurons in time")
    ap.add_argument("--bias-pattern", default=BIAS_PATTERN,
                    help="per-neuron bias files. Default is the base family; the "
                         "DIM recording's own bias_path() prefers the _feedproj "
                         "family, which is what the retake uses.")
    ap.add_argument("--out", default="repeatability_spikes.npz")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",") if x != ""]
    beat, bidx, blabel, brec = pick_beat(BEATSET, index=args.beat_index)
    proj = load_proj(PROJ_CONFIG)
    enc = {k: delta_encode_proj(beat, sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                theta=proj[k]["theta"]) for k in neurons}

    print(f"beat index {bidx} (label {blabel}, record {brec}) from {BEATSET}")
    print(f"per-neuron encoded events: "
          f"{ {k: len(enc[k]) for k in neurons} }")
    print(f"{len(neurons)} neurons x {args.trials} scored trials "
          f"({'interleaved rounds' if args.interleave else 'blocked'})\n")

    ntr = args.trials + 1                      # trial 0 is the routing transient
    spikes = np.empty((NN, ntr), dtype=object)
    wall = np.full((NN, ntr), np.nan)
    for i in range(NN):
        for t in range(ntr):
            spikes[i, t] = np.array([])

    def do_trial(b, k, t):
        drain_quiet(b)
        wall[k, t] = time.time()
        st = present_delta(b, k, enc[k], T_BEAT, args.syn, args.inh_syn)
        spikes[k, t] = st
        return st

    def setup_neuron(b, k):
        b.send(f"MASK {1 << k}")               # only k streams: no AER jamming
        b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
        b.monitor(k)
        time.sleep(0.8)
        b.program_weight(args.syn, args.weight, exc=True)
        b.program_weight(args.inh_syn, args.weight, exc=False)

    def save():
        np.savez(args.out, spikes=spikes, wall=wall, neurons=np.array(neurons),
                 trials=ntr, T=T_BEAT, beat_index=bidx, beat_label=blabel,
                 beat_record=brec, weight=args.weight, reload_at=args.reload_at,
                 interleave=bool(args.interleave),
                 clk_mhz=int(os.environ.get("CARAVAN_CLK_MHZ", "?")),
                 bias_pattern=args.bias_pattern,
                 note=("trial 0 per neuron is the post-routing settling transient "
                       "and must be discarded; readout is the FIXED path (SRAM "
                       "drain, on-chip Timer0 stamps), not DIM's flash/host path"))

    t_start = time.time()
    with BridgeSession() as b:
        if args.interleave:
            for t in range(ntr):
                for k in neurons:
                    setup_neuron(b, k)          # bias reload every visit, by design
                    st = do_trial(b, k, t)
                    print(f"  round {t:3d} neuron {k:2d}: {len(st):3d} spk", flush=True)
                save()
                print(f"  [checkpoint] round {t+1}/{ntr} -> {args.out}", flush=True)
        else:
            for k in neurons:
                setup_neuron(b, k)
                counts = []
                for t in range(ntr):
                    if args.reload_at > 0 and t == args.reload_at:
                        # same file, same values: any step here is DAC programming,
                        # not the neuron
                        b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
                        time.sleep(0.5)
                    st = do_trial(b, k, t)
                    counts.append(len(st))
                c = np.array(counts[1:], dtype=float)   # drop the transient
                cv = c.std() / c.mean() if c.mean() > 0 else np.nan
                print(f"  neuron {k:2d}: mean {c.mean():6.2f} spk  sd {c.std():5.2f}  "
                      f"CV {cv*100:5.1f}%   (trial0 {counts[0]}, discarded)", flush=True)
                save()
                print(f"    [checkpoint] {neurons.index(k)+1}/{len(neurons)} "
                      f"-> {args.out}", flush=True)

    d, s = INTEGRITY["drops"], INTEGRITY["stalls"]
    print(f"\nreadout integrity: drops={d}, stalls={s}"
          + ("   <-- NOT a clean measurement" if (d or s) else "   (clean)"))
    print(f"elapsed {(time.time()-t_start)/60:.1f} min -> {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
