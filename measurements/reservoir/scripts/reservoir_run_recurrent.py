#!/usr/bin/env python3
"""Recurrent-reservoir N/PVC run. Global bias, W_rec recurrence ON, delta input to the
input neurons, all 16 neurons recorded simultaneously. Between beats vleakn is raised
(reset) to discharge the membranes so every presentation starts from a silent state."""
import argparse
import queue
import time
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_data import get_beats, delta_encode

BIAS = "ofxCaravanViewer/bin/bias_synapse_characterization_reservoir_1.biases"
WREC = "ofxCaravanViewer/bin/reservoir_wrec.txt"


def load_wrec(path):
    c = []
    for l in open(path):
        l = l.strip()
        if l and not l.startswith("#"):
            s, d, cnt, e = (int(x) for x in l.split()[:4])
            c.append((s, d, cnt, e))
    return c


def present(b, events, T, in_neurons, reset_vl, op_vl, reset_ms=100):
    b.bias("vleakn", op_vl); time.sleep(0.05)                    # drop to operating (from prior kill)
    b.drain(max_lines=100000)
    times = {k: [] for k in range(16)}
    t0 = time.time()

    def collect(deadline):
        while time.time() < deadline:
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

    for tf, ch in events:
        collect(t0 + tf * T)
        exc = (ch == 0)
        for neu in in_neurons:
            b.route(0, neu, exc=exc)
            b.fire()
    collect(t0 + T + 0.2)
    b.bias("vleakn", reset_vl); time.sleep(0.05)                 # raise AFTER presentation: kill leftover recurrency
    return {k: np.array(times[k]) for k in range(16)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=20)
    ap.add_argument("--classes", default="NV")
    ap.add_argument("--thr", type=float, default=0.02)   # denser delta = more spikes/beat
    ap.add_argument("--tpresent", type=float, default=2.0)
    ap.add_argument("--in-neurons", default="0,1,2,3,4,5,6,7,8")
    ap.add_argument("--reset-vleakn", type=float, default=0.6)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--out", default="reservoir_spikes_nv_recurrent.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    in_neurons = [int(x) for x in args.in_neurons.split(",")]
    biases = load_biases(BIAS); op_vl = biases["vleakn"]
    X, y, meta = get_beats(records=tuple(args.records.split(",")),
                           n_per_class=args.n_per_class, classes=args.classes)
    if args.smoke:
        X, y = X[:4], y[:4]
    enc = [delta_encode(X[i], args.thr) for i in range(len(X))]
    wrec = load_wrec(WREC)
    print(f"recurrent run: {len(X)} beats, {len(wrec)} recur conns, in={in_neurons}, "
          f"reset vleakn {args.reset_vleakn}->{op_vl:.3f}")

    spikes = np.empty((16, len(X)), dtype=object)
    with BridgeSession() as b:
        b.apply_biases(biases); time.sleep(1.0)
        for syn, exc in ((0, True), (0, False), (1, True), (1, False)):
            b.program_weight(syn, args.weight, exc=exc)
        for s, d, c, e in wrec:
            b.send(f"SETRECUR {s} {d} {c} {e}")
        b.send("RECURCTRL 1"); time.sleep(0.3)
        for bi in range(len(X)):
            st = present(b, enc[bi], args.tpresent, in_neurons, args.reset_vleakn, op_vl)
            for k in range(16):
                spikes[k, bi] = st[k]
            tot = sum(len(st[k]) for k in range(16))
            act = [k for k in range(16) if len(st[k]) > 0]
            print(f"  beat {bi} (y={y[bi]}): {tot} spikes  active={act}")
        b.send("RECURCTRL 0")

    if not args.smoke:
        np.savez(args.out, spikes=spikes, labels=y, records=meta["records"],
                 neurons=np.arange(16), T=args.tpresent, coding="delta_recurrent",
                 classes=args.classes)
        print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
