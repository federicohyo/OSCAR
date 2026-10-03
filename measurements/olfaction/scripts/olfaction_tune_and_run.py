#!/usr/bin/env python3
"""Tune the array to the simulated-optimal evoked rate, then acquire the task there.

olfaction_sim_sweep.py says the measured operating point (108 Hz mean evoked) is not
where this task is best solved: accuracy peaks near 20 Hz at 0.760 +/- 0.026 per-chunk
against the 0.647 measured, and PLATEAUS over a wide range around it. Quieter is both
more accurate and cheaper here -- accuracy and energy point the same way, which is not
what I assumed earlier today.

Two stages so the bench time goes where it matters:
  1. CALIBRATE. Bisect a common vleakn offset until the mean evoked rate hits --target,
     probing on a handful of chunks. vleakn is the rate knob and HIGHER is quieter on
     this die (bench_bias_lint.QUIETER_IF, and [[silent-neurons-can-be-saturated]]).
  2. ACQUIRE. Present all 150 chunks at the chosen offset and save spikes, so
     olfaction_iso_compare.py scores it against the digital baseline unchanged.

The calibration probe reports per-neuron rate and how many neurons went silent. Silence
is not a free win: a neuron pushed under threshold contributes nothing, and the protocol
(bench/PROTOCOL.md) treats it as a blocker rather than a quiet operating point.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_tune_and_run.py
"""
import argparse, json, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_run import INTEGRITY, present_delta
from olfaction_identity import chunks
from olfaction_run_array import encode

FS = 1000.0


def build(duration, theta, neurons, npz="data_olfaction/olfaction_pulses.npz"):
    d = np.load(npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    enc = {}
    for k in neurons:
        w = np.random.default_rng(100 + k).normal(0, 1, 8)
        enc[k] = [encode((F[j].reshape(50, 8) @ w - (F[j].reshape(50, 8) @ w).mean())
                         / ((F[j].reshape(50, 8) @ w).std() + 1e-9), theta)
                  for j in range(len(F))]
    return F, Y, it, enc, names


def probe(b, neurons, base, enc, off, idx, T):
    """Mean evoked rate over a few chunks at a common vleakn offset."""
    tot, per = 0, []
    for k in neurons:
        bi = dict(base[k]); bi["vleakn"] = bi["vleakn"] + off
        b.send(f"MASK {1 << k}")
        b.apply_biases(bi); b.monitor(k); time.sleep(0.6)
        b.program_weight(0, 15, exc=True); b.program_weight(0, 15, exc=False)
        n = sum(len(present_delta(b, k, enc[k][j], T, 0, 0)) for j in idx)
        per.append(n / (len(idx) * T)); tot += n
    return float(np.mean(per)), per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, default=20.0, help="mean evoked rate, Hz")
    ap.add_argument("--tol", type=float, default=0.20, help="relative tolerance")
    ap.add_argument("--duration", default="0.1s")
    ap.add_argument("--tpresent", type=float, default=0.15)
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--n-probe", type=int, default=8)
    ap.add_argument("--max-probes", type=int, default=7)
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--out", default="olfaction_spikes_array_tuned.npz")
    ap.add_argument("--calib-out", default="data/olfaction_ratetune.json")
    args = ap.parse_args()
    neurons = list(range(16))

    F, Y, it, enc, names = build(args.duration, args.theta, neurons)
    base = {k: load_biases(args.bias_pattern.format(k=k)) for k in neurons}
    idx = np.linspace(0, len(F) - 1, args.n_probe).astype(int)
    print(f"{len(F)} chunks / {len(np.unique(it))} trials; target {args.target:.0f} Hz "
          f"+/-{args.tol*100:.0f}%  (measured reference point: 108.3 Hz)")

    lo, hi, hist = 0.0, 0.120, []          # higher vleakn = quieter on this die
    chosen, rate = None, None
    with BridgeSession() as b:
        for i in range(args.max_probes):
            off = 0.5 * (lo + hi)
            r, per = probe(b, neurons, base, enc, off, idx, args.tpresent)
            ns = sum(1 for x in per if x == 0)
            hist.append({"offset_V": off, "rate_hz": r, "silent": ns})
            print(f"  probe {i+1}: vleakn {off*1000:+6.1f} mV -> {r:7.1f} Hz"
                  f"   silent {ns}/16")
            if abs(r - args.target) / args.target <= args.tol and ns == 0:
                chosen, rate = off, r
                break
            if r > args.target:
                lo = off                    # still too hot -> quieter -> larger offset
            else:
                hi = off
        if chosen is None:
            chosen = min(hist, key=lambda h: (h["silent"] > 0,
                                              abs(h["rate_hz"] - args.target)))["offset_V"]
            rate = next(h["rate_hz"] for h in hist if h["offset_V"] == chosen)
            print(f"  did not converge; taking the closest non-silent probe: "
                  f"{chosen*1000:+.1f} mV -> {rate:.1f} Hz")
        json.dump({"target": args.target, "chosen_offset_V": chosen, "rate_hz": rate,
                   "history": hist}, open(args.calib_out, "w"), indent=2)
        print(f"\nacquiring {len(F)} chunks at vleakn {chosen*1000:+.1f} mV "
              f"({rate:.1f} Hz)\n")

        arr = np.empty((len(neurons), len(F)), dtype=object)
        for i in range(len(neurons)):
            for j in range(len(F)):
                arr[i, j] = np.array([])
        for i, k in enumerate(neurons):
            bi = dict(base[k]); bi["vleakn"] = bi["vleakn"] + chosen
            b.send(f"MASK {1 << k}")
            b.apply_biases(bi); b.monitor(k); time.sleep(0.8)
            b.program_weight(0, 15, exc=True); b.program_weight(0, 15, exc=False)
            tot = 0
            for j in range(len(F)):
                st = present_delta(b, k, enc[k][j], args.tpresent, 0, 0)
                arr[i, j] = st; tot += len(st)
            print(f"  neuron {k:2d}: {tot:5d} spikes" + ("   [DEAD]" if tot == 0 else ""))
    dz, sz = INTEGRITY["drops"], INTEGRITY["stalls"]
    print(f"readout integrity: drops={dz} stalls={sz}"
          + ("  <-- NOT clean" if dz or sz else "  (clean)"))
    np.savez(args.out, spikes=arr, labels=Y, trial=it, neurons=np.array(neurons),
             nproj=1, classes=np.array(names), T=args.tpresent,
             duration=args.duration, theta=args.theta,
             vleakn_offset_V=chosen, tuned_rate_hz=rate,
             **provenance(bias_files=[args.bias_pattern.format(k=k) for k in neurons],
                          task="olfaction_identity_tuned", tpresent=args.tpresent))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
