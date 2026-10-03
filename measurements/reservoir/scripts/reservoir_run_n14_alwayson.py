#!/usr/bin/env python3
"""Record ONLY neuron 14 as the ALWAYS-ON-INHIBITED unit for the XOR set, to stack onto the
existing 15-neuron data (bits_ab order is fixed across reps, so alignment is trivial). n14 is
biased to fire TONICALLY at rest (high on corner 00); both bits route to its INHIBITORY synapse
(a-inh, b-inh), so 01/10/11 are suppressed -> a clean 'detect-absence' / ~NOT(a+b) axis that adds
the dimensionality the XOR readout needed.

Uses bias_synapse_characterization_super_n14_jul10_inh.biases. Same trial structure (per-cell,
window) as reservoir_run_xor so the row stacks directly. Prints per-corner counts to verify the
00>01,10>11 ordering before we commit it.

    ./.venv-meas/bin/python3 reservoir_run_n14_alwayson.py --reps 3 --out data/xor_dim/n14_alwayson.npz
"""
import argparse, os, time, queue
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_synthtask import make_trials

BIAS = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n14_jul10_inh.biases"
K = 14
WIN = (0.35, 0.55)


def present_n14(b, a, bit_b, T, burst, jitter, rng):
    """n14 fires tonically over [0,T]; for each active bit, fire an INHIBITORY burst in WIN to
    suppress it. Record n14's spike times over the whole trial."""
    b.drain(max_lines=200000)
    times = []
    t0 = time.time()

    def collect(until):
        while time.time() < until:
            try:
                line = b.out_q.get(timeout=0.002)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3 and p[1].isdigit() and int(p[1]) == K:
                    times.append(time.time() - t0)

    lo, hi = WIN
    events = []
    for bit in (a, bit_b):
        if bit:
            for _ in range(burst):
                events.append(float(np.clip(rng.uniform(lo, hi) + jitter * rng.standard_normal(), 0, T)))
    events.sort()
    for tf in events:
        collect(t0 + tf)
        b.route(0, K, exc=False)          # INHIBITORY synapse
        b.fire()
    collect(t0 + T)
    return np.array(times)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--per-cell", type=int, default=12)
    ap.add_argument("--T", type=float, default=1.2)
    ap.add_argument("--burst", type=int, default=10)
    ap.add_argument("--jitter", type=float, default=0.05)
    ap.add_argument("--weight", type=int, default=15, help="inhibitory synapse weight")
    ap.add_argument("--bias", default=BIAS, help="n14 bias file")
    ap.add_argument("--out", default="data/xor_dim/n14_alwayson.npz")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rng = make_trials  # placeholder to avoid lint; real rng below
    rng = np.random.default_rng(0)
    _, ab, labels, groups = make_trials(args.per_cell, args.T, args.burst, args.jitter, rng)
    y = labels["XOR"].astype(int)
    ntr = len(ab)
    rows = []      # per rep: (16?, ntr) -- we only fill n14
    per_rep = np.empty((args.reps, ntr), dtype=object)

    print(f"n14 always-on-inhibited: {ntr} trials x {args.reps} reps, bias={args.bias}")
    with BridgeSession() as b:
        b.send("RECURCTRL 0"); time.sleep(0.2)
        b.apply_biases(load_biases(args.bias)); b.monitor(K); time.sleep(1.0)
        b.program_weight(0, args.weight, exc=False)      # inhibitory synapse
        # quick rest check: tonic rate with zero input
        b.drain(max_lines=200000); s = b.sample_spikes(1.0)
        print(f"  tonic rest rate (no input): {s['counts'][K]} Hz, clean={s['clean']}")
        for r in range(args.reps):
            by = {c: [] for c in [(0, 0), (0, 1), (1, 0), (1, 1)]}
            for bi in range(ntr):
                st = present_n14(b, int(ab[bi, 0]), int(ab[bi, 1]), args.T, args.burst, args.jitter,
                                 np.random.default_rng(1000 + r * 100 + bi))
                per_rep[r, bi] = st
                by[(int(ab[bi, 0]), int(ab[bi, 1]))].append(len(st))
            mc = {c: np.mean(v) for c, v in by.items()}
            print(f"  rep{r}: 00={mc[(0,0)]:.1f} 01={mc[(0,1)]:.1f} 10={mc[(1,0)]:.1f} 11={mc[(1,1)]:.1f}"
                  f"   (want 00 highest, 11 lowest)")
            np.savez(args.out + ".tmp.npz", n14=per_rep, labels=y, bits_ab=ab, groups=groups,
                     T=args.T, reps=args.reps, coding="n14_alwayson_inh")
            os.replace(args.out + ".tmp.npz", args.out)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
