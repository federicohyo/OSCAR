#!/usr/bin/env python3
"""Feedforward reservoir with a FIXED per-neuron INPUT PROJECTION (one neuron at a time).

Same feedforward, one-at-a-time protocol as reservoir_run.py (per-neuron tuned bias,
recurrence off, AER contention off), but instead of driving every neuron with the SAME
delta-coded ECG, each neuron k is stimulated with ITS OWN projection of the beat:

    x_k(t) = shift( gaussian_smooth(ECG, sigma_k), shift_k )   -> delta_encode(x_k, theta_k)

The per-neuron {sigma_k, shift_k, theta_k} are read from a fixed, pre-generated config
(reservoir_input_proj.json, produced by reservoir_input_proj.py and applied identically
to every beat, train and test -- leakage-free). This is a random-feature projection in the
continuous-signal domain that decorrelates the input each neuron sees, which the offline
diagnostics (A4) identified as the true bottleneck: filtering the SAME correlated spike
train with different kernels stays correlated, so the decorrelation must be injected at
the INPUT. Goal: push effective dimensionality (A4 participation ratio) past ~8 WITHOUT
recurrence, sidestepping the AER-readout-contention wall entirely.

Output npz is the same format as reservoir_run.py, so reservoir_analysis.py / reservoir_kernel.py
consume it unchanged (coding="delta_randproj").
"""

import argparse
import json
import os
import time

import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_data import get_beats, delta_encode_proj
from reservoir_run import INTEGRITY, present_delta

BIAS_DIR = "ofxCaravanViewer/bin"
DEFAULT_NEURONS = list(range(16))


def bias_path(k):
    """Prefer the feedforward-projection-tuned per-neuron bias if it exists
    (super_n{k}_feedproj.biases), else the original super_n{k}.biases."""
    fp = f"{BIAS_DIR}/bias_synapse_characterization_super_n{k}_feedproj.biases"
    base = f"{BIAS_DIR}/bias_synapse_characterization_super_n{k}.biases"
    return fp if os.path.exists(fp) else base


def save_ckpt(out, arr, y, records, neurons, T, classes, done, coding="delta_randproj",
              bias_files=()):
    """Atomically write the (possibly partial) npz. `done` = list of neuron ids fully
    collected so far; pending rows hold empty arrays. Write-to-tmp + rename so
    an interrupted write leaves the checkpoint intact.

    `bias_files` goes into the provenance header along with the core clock, the flashed
    firmware hash and the working-tree state -- see run_provenance.py for why."""
    tmp = out + ".tmp.npz"
    np.savez(tmp, spikes=arr, labels=y, records=records, neurons=np.array(neurons),
             T=T, coding=coding, classes=classes, done_neurons=np.array(done, dtype=int),
             **provenance(bias_files=bias_files, coding_arg=coding))
    os.replace(tmp, out)


def load_proj(path):
    """Load the fixed per-neuron input-projection config -> {neuron: {sigma,shift,theta}}.
    Accepts the generated .json (also tries a .conf sibling if the given path is missing)."""
    if not os.path.exists(path):
        alt = os.path.splitext(path)[0] + ".conf"
        if os.path.exists(alt):
            path = alt
        else:
            raise FileNotFoundError(f"projection config not found: {path} (nor {alt})")
    with open(path) as f:
        cfg = json.load(f)
    proj = {int(c["neuron"]): c for c in cfg["proj"]}
    print(f"loaded projection {path}: seed={cfg.get('seed')} n={cfg.get('n')} "
          f"({len(proj)} per-neuron projections)")
    return proj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NV", help="NV (binary) or NSV (3-class)")
    ap.add_argument("--beats", default=None,
                    help="frozen beat set from make_beatset.py; overrides --records/"
                         "--n-per-class/--classes so this run is beat-matched to a "
                         "feedforward baseline (apples-to-apples).")
    ap.add_argument("--bias-pattern", default=None,
                    help="per-neuron bias file pattern with {k}, e.g. "
                         "'ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases'. "
                         "Overrides the _feedproj/_super default so randproj can reuse the "
                         "exact biases of a feedforward run (isolates input projection).")
    ap.add_argument("--neurons", default=",".join(map(str, DEFAULT_NEURONS)))
    ap.add_argument("--config", default="reservoir_input_proj.json",
                    help="fixed per-neuron input-projection config (json)")
    ap.add_argument("--syn", type=int, default=0, help="excitatory (UP) synapse")
    ap.add_argument("--inh-syn", type=int, default=0, help="inhibitory (DOWN) synapse")
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--tpresent", type=float, default=2.0, help="presentation time (s)")
    ap.add_argument("--out", default="reservoir_spikes_nv_randproj.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",")]
    proj = load_proj(args.config)
    for k in neurons:
        if k not in proj:
            raise KeyError(f"no projection for neuron {k} in {args.config}")

    if args.beats:
        from make_beatset import load_beatset
        X, y, meta = load_beatset(args.beats)
        print(f"beats: loaded {len(X)} from {args.beats} "
              f"(records/n-per-class/classes args ignored)")
    else:
        X, y, meta = get_beats(records=tuple(args.records.split(",")),
                               n_per_class=args.n_per_class, classes=args.classes)
    if args.smoke:
        X, y = X[:4], y[:4]
        neurons = neurons[:3]

    T = args.tpresent
    # per-neuron projected delta encoding: enc[k][bi] = event list for neuron k, beat bi
    enc = {}
    for k in neurons:
        p = proj[k]
        enc[k] = [delta_encode_proj(X[bi], sigma=p["sigma"], shift=p["shift"],
                                    theta=p["theta"]) for bi in range(len(X))]
    ev_mean = np.mean([len(e) for k in neurons for e in enc[k]])
    print(f"coding=delta_randproj beats={len(X)} neurons={neurons} T={T:.2f}s/beat "
          f"per-neuron-projected delta events/beat: mean {ev_mean:.0f}  (-> {args.out})")

    # pre-allocate with empty arrays so a partial checkpoint is always well-formed
    arr = np.empty((len(neurons), len(X)), dtype=object)
    for i in range(len(neurons)):
        for bi in range(len(X)):
            arr[i, bi] = np.array([])
    done = []
    with BridgeSession() as b:
        for i, k in enumerate(neurons):         # neurons OUTER: load each neuron's bias once
            # Stream ONLY the neuron being recorded. _collect_until already filters
            # by address host-side; the aim here is bandwidth headroom.
            # The UART ceiling is 24*f_MHz events/s (600/s at 25 MHz),
            # and 16 neurons free-running at tens of Hz sits right at it, which
            # shows up as DROPS/STALLS and aborts the run.
            b.send(f"MASK {1 << k}")
            bp = args.bias_pattern.format(k=k) if args.bias_pattern else bias_path(k)
            b.apply_biases(load_biases(bp))
            b.monitor(k)                         # route neuron k's membrane to the scope pin
            time.sleep(0.8)
            p = proj[k]
            tuned = os.path.basename(bp)
            print(f"  --> neuron {k}: sigma={p['sigma']:.2f} shift={p['shift']:+.3f} "
                  f"theta={p['theta']:.3f} bias={tuned} (monitoring on scope)")
            b.program_weight(args.syn, args.weight, exc=True)
            b.program_weight(args.inh_syn, args.weight, exc=False)
            tot = 0
            for bi in range(len(X)):
                st = present_delta(b, k, enc[k][bi], T, args.syn, args.inh_syn)
                arr[i, bi] = st
                tot += len(st)
                if args.smoke:
                    print(f"  neuron {k:2d} beat {bi} (y={y[bi]}): {len(st)} spk "
                          f"t={np.round(st, 2).tolist()}")
            done.append(int(k))
            print(f"  neuron {k:2d}: {tot} spikes over {len(X)} beats"
                  + ("  [DEAD]" if tot == 0 else ""))
            if not args.smoke:                   # checkpoint after EVERY neuron (atomic)
                save_ckpt(args.out, arr, y, meta["records"], neurons, T,
                          args.classes, done,
                          bias_files=[args.bias_pattern.format(k=n) if args.bias_pattern
                                      else bias_path(n) for n in neurons])
                print(f"    [checkpoint] {len(done)}/{len(neurons)} neurons -> {args.out}")

    if not args.smoke:
        dz, sz = INTEGRITY["drops"], INTEGRITY["stalls"]
        print(f"readout integrity: drops={dz}, stalls={sz}"
              + ("  <-- NOT a clean measurement of the array" if (dz or sz)
                 else "  (clean)"))
        print("wrote", args.out, f"({len(done)}/{len(neurons)} neurons x {len(X)} beats raw spikes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
