#!/usr/bin/env python3
"""Present the olfaction identity task to the analog array.

PURPOSE: establish an OPERATING POINT at which the analog rail can be measured during
inference, and produce the array accuracy figure for this task, which does not exist.

ALL CHUNKS, and why it matters (2026-08-13). The first version of this script kept one
representative chunk per trial to keep the run short. That silently broke the
comparison. chunks() returns one chunk per 50 ms heater cycle, so a 0.1 s pulse with
its 0.2 s tail yields FIVE per trial, and the digital baseline classifies each chunk
(0.900) and votes over the five to reach 1.000. Scoring a one-chunk array against a
five-chunk-voted digital number is not the same measurement, and it conceded the cost
argument for free: voting k chunks costs the digital side k x E_OP3, while the array
pays P_analog x T continuously, so repetition is nearly free to it. That asymmetry is
the whole point (olfaction_latency.py). So present every chunk and keep the trial index,
which the scorer needs both to vote and to keep a trial's chunks inside one CV fold.

ENCODING. Each neuron sees its own fixed random projection of the 8 MOx channels,
delta-encoded: UP crossings drive the excitatory synapse, DOWN the inhibitory. Same
shape as reservoir_run_randproj.py for ECG, so the two are comparable, and the
projection is fixed and applied identically to every trial -- no leakage.

TIME-MULTIPLEXED PROJECTIONS (--nproj, 2026-08-13). Sixteen neurons means sixteen
1-D projections of a 400-D feature, and olfaction_loss_budget.py prices that bottleneck
at -0.107 per-chunk / -0.067 voted -- as much as the analog array itself costs. Unlike
the array's own loss, which is noise and averages away under voting, this is lost
INFORMATION and no amount of repetition recovers it. So run each neuron over M different
projections in sequence and treat each (neuron, projection) as its own read-out unit:
M x 16 effective dimensions from 16 devices, at M times the presentations.

Paired with --tpresent 0.05, which is the honest presentation time: a chunk is one 50 ms
heater cycle, and presenting it over 150 ms burned 3x the continuous rail power for
nothing. Real-time presentation makes the M=3 run cost the same bench time as the old
M=1 run did.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_run_array.py
"""
import argparse, json, os, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_run import INTEGRITY, present_delta
from olfaction_identity import chunks

FS = 1000.0


def encode(sig_t, theta):
    """Level-crossing encode a 1-D time course -> [(t_frac, channel)]."""
    lvl = np.floor(sig_t / theta)
    d = np.diff(lvl, prepend=lvl[0])
    ev = []
    n = len(sig_t)
    for i in np.flatnonzero(d != 0):
        for _ in range(min(int(abs(d[i])), 4)):     # cap: one edge per ms is the floor
            ev.append((i / n, 0 if d[i] > 0 else 1))
    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="data_olfaction/olfaction_pulses.npz")
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--duration", default="0.1s", help="pulse duration to present")
    ap.add_argument("--tpresent", type=float, default=0.05,
                    help="presentation time (s); 0.05 = real time for a 50 ms chunk")
    ap.add_argument("--nproj", type=int, default=3,
                    help="projections time-multiplexed per neuron (effective dims = 16*M)")
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--neurons", default=",".join(map(str, range(16))))
    ap.add_argument("--max-per-trial", type=int, default=0,
                    help="cap chunks per trial (0 = all five; the iso setting)")
    ap.add_argument("--out", default="olfaction_spikes_array.npz")
    args = ap.parse_args()
    neurons = [int(x) for x in args.neurons.split(",")]

    d = np.load(args.npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    dur = np.array([m[0] for m in meta])
    m = dur == args.duration
    F, it = chunks(X[m], Th[m], t, float(args.duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    if args.max_per_trial:
        keep = np.concatenate([np.flatnonzero(it == j)[:args.max_per_trial]
                               for j in np.unique(it)])
        F, Y, it = F[keep], Y[keep], it[keep]

    # time course per (chunk, neuron): the feature re-read as 50 samples
    print(f"{len(F)} chunks over {len(np.unique(it))} trials, "
          f"{len(neurons)} neurons, classes {names}")
    steps = 50
    # one encoder per (neuron, projection); the seed makes the projection set fixed
    enc = {}
    for k in neurons:
        for pj in range(args.nproj):
            w = np.random.default_rng(100 + k + 1000 * pj).normal(0, 1, 8)
            e = []
            for j in range(len(F)):
                sig = F[j].reshape(steps, 8) @ w
                e.append(encode((sig - sig.mean()) / (sig.std() + 1e-9), args.theta))
            enc[(k, pj)] = e
    ev = np.mean([len(e) for v in enc.values() for e in v])
    print(f"{len(neurons)} neurons x {args.nproj} projections = "
          f"{len(neurons)*args.nproj} read-out units")
    print(f"delta events per presentation: mean {ev:.0f}   T={args.tpresent}s")

    nu = len(neurons) * args.nproj
    arr = np.empty((nu, len(F)), dtype=object)
    for i in range(nu):
        for j in range(len(F)):
            arr[i, j] = np.array([])
    u_neuron = np.repeat(neurons, args.nproj)
    u_proj = np.tile(np.arange(args.nproj), len(neurons))
    with BridgeSession() as b:
        for i, k in enumerate(neurons):
            b.send(f"MASK {1 << k}")
            b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
            b.monitor(k); time.sleep(0.8)
            b.program_weight(0, args.weight, exc=True)
            b.program_weight(0, args.weight, exc=False)
            tot = 0
            for pj in range(args.nproj):
                u = i * args.nproj + pj
                for j in range(len(F)):
                    st = present_delta(b, k, enc[(k, pj)][j], args.tpresent, 0, 0)
                    arr[u, j] = st; tot += len(st)
            print(f"  neuron {k:2d}: {tot:5d} spikes over "
                  f"{args.nproj}x{len(F)} presentations"
                  + ("   [DEAD]" if tot == 0 else ""))
    dz, sz = INTEGRITY["drops"], INTEGRITY["stalls"]
    print(f"readout integrity: drops={dz} stalls={sz}" + ("  <-- NOT clean" if dz or sz else "  (clean)"))
    np.savez(args.out, spikes=arr, labels=Y, trial=it, neurons=np.array(neurons),
             unit_neuron=u_neuron, unit_proj=u_proj, nproj=args.nproj,
             classes=np.array(names), T=args.tpresent, duration=args.duration,
             theta=args.theta,
             **provenance(bias_files=[args.bias_pattern.format(k=k) for k in neurons],
                          task="olfaction_identity", tpresent=args.tpresent))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
