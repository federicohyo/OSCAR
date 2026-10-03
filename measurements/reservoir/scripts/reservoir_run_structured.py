#!/usr/bin/env python3
"""A0 on silicon: STRUCTURED feature-aware encoding, feedforward, one neuron at a time.

Same protocol as reservoir_run_randproj.py (per-neuron bias, host-paced delta replay, recurrence off, checkpoint per neuron) but each physical neuron k is driven by its assigned
morphological feature detector (reservoir_structured.build_spec / encode_neuron): P-wave,
QRS up-slope, QRS down-slope, T-wave, or RR/rhythm -- as few gated delta spikes. Validated
in software (macro-F1 0.55, V-F1 0.93); this measures it on the analog array.
"""
import argparse
import os
import time
import numpy as np

from meas_common import BridgeSession, load_biases
from reservoir_data import get_beats
from reservoir_run import INTEGRITY, present_delta
from reservoir_run_randproj import save_ckpt
from reservoir_structured import build_spec, encode_neuron, amplify

BIAS_DIR = "ofxCaravanViewer/bin"


def bias_path(k):
    """Prefer structured-tuned bias (super_n{k}_struct.biases), then the projection-tuned
    (_feedproj), then the base super_n{k}.biases."""
    for suf in ("_struct", "_feedproj", ""):
        p = f"{BIAS_DIR}/bias_synapse_characterization_super_n{k}{suf}.biases"
        if os.path.exists(p):
            return p
    return f"{BIAS_DIR}/bias_synapse_characterization_super_n{k}.biases"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NSV")
    ap.add_argument("--syn", type=int, default=0, help="excitatory (UP) synapse")
    ap.add_argument("--inh-syn", type=int, default=0, help="inhibitory (DOWN) synapse")
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--spike-mult", type=int, default=1, help="repeat each input event N times (optional drive boost; 1 = raw structured, matches GUI tuning)")
    ap.add_argument("--tpresent", type=float, default=2.0)
    ap.add_argument("--out", default="reservoir_spikes_nsv_structured_hw.npz")
    ap.add_argument("--beats-npz", default=None,
                    help="load beats (X_raw, rr, labels, records) from this npz instead of "
                         "re-downloading via get_beats -- guarantees identical beats to a prior run")
    ap.add_argument("--resume", action="store_true",
                    help="if --out already exists, reuse neurons already collected there "
                         "(skip re-firing them) and continue with the rest")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    spec = build_spec()
    neurons = list(range(len(spec)))
    if args.beats_npz:
        b = np.load(args.beats_npz, allow_pickle=True)
        # Accept both layouts: the ad-hoc one this flag was written for (X_raw/labels) and
        # make_beatset.py's frozen set (X/y), which is the one to use for anything meant to
        # be compared against another run.
        X = b["X_raw"] if "X_raw" in b.files else b["X"]
        y = np.asarray(b["labels"] if "labels" in b.files else b["y"])
        rr = b["rr"]
        meta = {"records": np.asarray(b["records"])}
        print(f"loaded {len(X)} beats from {args.beats_npz} (no re-download)")
    else:
        X, y, meta = get_beats(records=tuple(args.records.split(",")),
                               n_per_class=args.n_per_class, classes=args.classes)
        rr = meta["rr"]
    T = args.tpresent
    if args.smoke:
        X, y, rr = X[:4], y[:4], rr[:4]
        neurons = neurons[:6]

    # per-neuron structured encoding (x spike-mult to lift weak features over threshold)
    enc = {k: [amplify(encode_neuron(np.asarray(X[bi], float), rr[bi], spec[k]), args.spike_mult)
               for bi in range(len(X))] for k in neurons}
    ev_mean = np.mean([len(e) for k in neurons for e in enc[k]])
    print(f"coding=structured_hw beats={len(X)} neurons={len(neurons)} feats="
          f"{[spec[k]['feature'] for k in neurons]} T={T:.2f}s  in-events/beat mean {ev_mean:.0f}"
          f"  (-> {args.out})")

    arr = np.empty((len(neurons), len(X)), dtype=object)
    for i in range(len(neurons)):
        for bi in range(len(X)):
            arr[i, bi] = np.array([])
    done = []
    if args.resume and os.path.exists(args.out):
        prev = np.load(args.out, allow_pickle=True)
        pdone = [int(k) for k in prev["done_neurons"]]
        psp = prev["spikes"]
        if psp.shape == arr.shape:
            for i, k in enumerate(neurons):
                if k in pdone:
                    arr[i] = psp[i]
            done = [k for k in neurons if k in pdone]
            print(f"[resume] {len(done)}/{len(neurons)} neurons reused from {args.out}: {done}")
        else:
            print(f"[resume] shape mismatch (prev {psp.shape} vs {arr.shape}); starting fresh")
    with BridgeSession() as b:
        for i, k in enumerate(neurons):
            if k in done:                      # --resume: already collected, keep its data
                print(f"  neuron {k:2d} [{spec[k]['feature']:8s}]: reused from checkpoint (skip)")
                continue
            bp = bias_path(k)
            b.apply_biases(load_biases(bp))
            b.monitor(k)
            time.sleep(0.8)
            tuned = "_struct" if "_struct" in bp else ("_feedproj" if "_feedproj" in bp else "base")
            print(f"  --> neuron {k} feature={spec[k]['feature']:8s} bias={tuned} (scope)")
            b.program_weight(args.syn, args.weight, exc=True)
            b.program_weight(args.inh_syn, args.weight, exc=False)
            tot = 0
            for bi in range(len(X)):
                st = present_delta(b, k, enc[k][bi], T, args.syn, args.inh_syn)
                arr[i, bi] = st
                tot += len(st)
                if args.smoke:
                    print(f"    beat {bi} (y={y[bi]}): {len(enc[k][bi])} in -> {len(st)} out")
            done.append(int(k))
            print(f"  neuron {k:2d} [{spec[k]['feature']:8s}]: {tot} spikes over {len(X)} beats"
                  + ("  [DEAD]" if tot == 0 else ""))
            if not args.smoke:
                save_ckpt(args.out, arr, y, meta["records"], neurons, T, args.classes,
                          done, coding="structured_hw",
                          bias_files=[bias_path(n) for n in neurons])
                print(f"    [checkpoint] {len(done)}/{len(neurons)} -> {args.out}")

    if not args.smoke:
        dz, sz = INTEGRITY["drops"], INTEGRITY["stalls"]
        print(f"readout integrity: drops={dz}, stalls={sz}"
              + ("  <-- NOT a clean measurement of the array" if (dz or sz)
                 else "  (clean)"))
        print("wrote", args.out, f"({len(done)}/{len(neurons)} neurons x {len(X)} beats)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
