#!/usr/bin/env python3
"""Hybrid recurrent reservoir, one-neuron-at-a-time with collapse.

For each input neuron k (with its OWN correct per-neuron bias, as in feedforward),
recurrence is ON: stimulate neuron k with the ECG delta trace, let the recurrent
cascade run through W_rec, and record ALL neurons -- but collapse every spike into a
single trace attributed to input neuron k (the responding neurons are at k's bias, so
we fold their activity into k's response rather than trusting their identity). vleakn
is reset high between beats for a silent start. Different inputs trigger different
cascades -> the 16 collapsed traces decorrelate (dimensionality expansion) while every
stimulated neuron stays correctly biased.
"""
import argparse
import queue
import time
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_data import get_beats, delta_encode
from reservoir_run import BIAS_PATTERN

WREC = "ofxCaravanViewer/bin/reservoir_wrec.txt"


def load_wrec(path):
    c = []
    for l in open(path):
        l = l.strip()
        if l and not l.startswith("#"):
            s, d, cnt, e = (int(x) for x in l.split()[:4])
            c.append((s, d, cnt, e))
    return c


def present(b, kin, events, T, reset_vl, op_vl):
    """Stimulate neuron kin with delta; record EACH neuron's response separately (16
    traces) so the recurrent spread across the array is kept (no collapse)."""
    b.bias("vleakn", op_vl); time.sleep(0.05)       # drop to operating point (from prior kill)
    b.drain(max_lines=100000)
    times = {j: [] for j in range(16)}
    lost = {"drops": 0, "stalls": 0}   # the chip's own integrity flags for this beat
    t0 = time.time()

    def collect(dl):
        while time.time() < dl:
            try:
                line = b.out_q.get(timeout=0.003)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3:
                    try:
                        times[int(p[1])].append(time.time() - t0)
                    except (ValueError, KeyError):
                        pass
            elif line.startswith("DROPS ") or line.startswith("STALLS "):
                # A beat with either nonzero is NOT a measurement of the array: the
                # readout lost spikes (drops) or throttled it (stalls). Contended-AER
                # spike loss is exactly what collapsed this reservoir before.
                p = line.split()
                if len(p) == 2:
                    try:
                        lost["drops" if p[0] == "DROPS" else "stalls"] += int(p[1])
                    except ValueError:
                        pass

    for tf, ch in events:
        collect(t0 + tf * T)
        exc = (ch == 0)
        b.route(0, kin, exc=exc)
        b.fire()
    collect(t0 + T + 0.2)
    b.bias("vleakn", reset_vl); time.sleep(0.05)    # raise AFTER presentation: kill leftover recurrency
    return {j: np.array(times[j]) for j in range(16)}, lost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias-pattern", default=None,
                    help="per-neuron bias files, e.g. '.../super_n{k}_jul10.biases'; "
                         "default is the module BIAS_PATTERN")
    ap.add_argument("--beats", default=None,
                    help="frozen beat set from make_beatset.py; overrides "
                         "--records/--n-per-class/--classes")
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=15)
    ap.add_argument("--classes", default="NV")
    ap.add_argument("--thr", type=float, default=0.02)
    ap.add_argument("--tpresent", type=float, default=2.0)
    ap.add_argument("--neurons", default=",".join(map(str, range(16))))
    ap.add_argument("--reset-vleakn", type=float, default=0.6)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--out", default="reservoir_spikes_nv_recur_collapse.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",")]
    bias_pattern = args.bias_pattern or BIAS_PATTERN
    print(f"biases: {bias_pattern}")
    if args.beats:
        # Frozen beat set: the ONLY way to guarantee two runs see identical beats.
        # get_beats is seeded, but its pool is built in record-argument order, so the
        # same seed with a different order returns different beats.
        from make_beatset import load_beatset
        X, y, meta = load_beatset(args.beats)
        print(f"beats: loaded {len(X)} from {args.beats} "
              f"(records/n-per-class/classes args ignored)")
    else:
        X, y, meta = get_beats(records=tuple(args.records.split(",")),
                               n_per_class=args.n_per_class, classes=args.classes)
    if args.smoke:
        X, y = X[:4], y[:4]; neurons = neurons[:3]
    enc = [delta_encode(X[i], args.thr) for i in range(len(X))]
    wrec = load_wrec(WREC)
    integrity = {"drops": 0, "stalls": 0, "beats": 0, "dirty_beats": 0}
    print(f"recur-collapse: {len(X)} beats x {len(neurons)} input-neurons, {len(wrec)} conns")

    # virtual reservoir: 16 response traces per stimulated input neuron -> up to 256 traces
    spikes = np.empty((len(neurons) * 16, len(X)), dtype=object)
    with BridgeSession() as b:
        for ni, k in enumerate(neurons):
            bias = load_biases(bias_pattern.format(k=k)); op_vl = bias["vleakn"]
            b.apply_biases(bias); b.monitor(k); time.sleep(0.8)
            print(f"  --> stimulating + monitoring neuron {k} on scope")
            for syn, exc in ((0, True), (0, False), (1, True), (1, False)):
                b.program_weight(syn, args.weight, exc=exc)
            # load W_rec EXCLUDING connections that feed back into the stimulated neuron k,
            # so k fires cleanly (feedforward-calibrated) while its spikes spread to the rest.
            b.send("RECURCTRL 2")   # clear
            for s, d, c, e in wrec:
                if d != k:
                    b.send(f"SETRECUR {s} {d} {c} {e}")
            b.send("RECURCTRL 1"); time.sleep(0.2)
            tot = 0
            for bi in range(len(X)):
                st, lost = present(b, k, enc[bi], args.tpresent, args.reset_vleakn, op_vl)
                integrity["drops"] += lost["drops"]
                integrity["stalls"] += lost["stalls"]
                integrity["beats"] += 1
                if lost["drops"] or lost["stalls"]:
                    integrity["dirty_beats"] += 1
                for j in range(16):
                    spikes[ni * 16 + j, bi] = st[j]
                    tot += len(st[j])
            print(f"  input-neuron {k}: {tot} spikes over {len(X)} beats (16 response traces)")
        b.send("RECURCTRL 0")

    d, st, nb, db = (integrity["drops"], integrity["stalls"],
                     integrity["beats"], integrity["dirty_beats"])
    print(f"\nreadout integrity: {nb} beats, {db} with loss  (drops={d}, stalls={st})")
    if db:
        print("  !! Those beats are NOT measurements of the array: the readout lost")
        print("     spikes or back-pressured it. Mask neurons, or lower the firing rate.")
        print("     Contended-AER spike loss is what collapsed this reservoir before.")
    else:
        print("  clean: every beat free-running, no spikes lost")

    if not args.smoke:
        np.savez(args.out, spikes=spikes, labels=y, records=meta["records"],
                 neurons=np.arange(len(neurons) * 16), T=args.tpresent,
                 coding="delta_virtual", classes=args.classes,
                 n_input=len(neurons))
        print("wrote", args.out, f"({spikes.shape[0]} virtual-reservoir traces x {len(X)} beats)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
