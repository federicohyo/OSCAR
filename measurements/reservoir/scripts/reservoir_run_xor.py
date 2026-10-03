#!/usr/bin/env python3
"""Run the synthetic 2-bit XOR task ON THE CHIP (Phase 1: natural mismatch diversity).

The software positive control (reservoir_synthtask.py) showed XOR needs D_eff > 1: at
D_eff = 1 it is at chance, and accuracy rises with neuron diversity. This presents the same
stimulus to the real 16-neuron array -- each trial's two bits are coincident UP bursts that
sum on the membrane (drive ~ a+b) -- and asks whether the chip's *device mismatch* (which
gives D_eff ~ 2 at the _jul10 bias point, measured) is enough to make XOR separable.

Same presentation as the reservoir runs: one neuron at a time, its bias file loaded once,
the identical stimulus replayed for every neuron (diversity is in the neurons, not the
input). Output spikes saved raw; scored offline with the canonical kernel pipeline, CV
grouped by repetition (never by (a,b) cell).

    CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 reservoir_run_xor.py \
        --bias-pattern 'ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases' \
        --out reservoir_spikes_xor_50mhz_jul10.npz
"""
import argparse
import os
import time
import numpy as np

from meas_common import BridgeSession, load_biases
from reservoir_run import present_delta
from reservoir_synthtask import make_trials

DEFAULT_NEURONS = list(range(16))

# Signed encoding using BOTH synapses. exc and inh bits share ONE coincident window so
# they compete on the membrane in real time (like delta coding's interleaved UP/DOWN) --
# the membrane rectifies at 0, so inhibition must act DURING excitation to cancel it, not
# before. chan 0 -> excitatory synapse, chan 1 -> inhibitory synapse.
WIN_INH = (0.35, 0.55)
WIN_EXC = (0.35, 0.55)


def signed_events(a, b, chan_a, chan_b, burst, jitter, T, rng):
    """Build a time-sorted event list where bit a drives synapse-channel chan_a and bit b
    drives chan_b. chan 1 (inhibitory) events land in the early window, chan 0 (excitatory)
    in the late window, so inhibition acts before excitation."""
    e = []
    for bit, chan in ((a, chan_a), (b, chan_b)):
        if not bit:
            continue
        lo, hi = WIN_INH if chan == 1 else WIN_EXC
        ts = rng.uniform(lo, hi, burst) + jitter * rng.standard_normal(burst)
        e += [(float(np.clip(t, 0, T)) / T, chan) for t in ts]
    return sorted(e, key=lambda x: x[0])


# Per-neuron sign patterns (chan_a, chan_b): a-exc/b-inh detects (1,0); a-inh/b-exc
# detects (0,1); both-exc is an OR/AND summation unit for richness.
SIGN_PATTERNS = [(0, 1), (1, 0), (0, 0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias-pattern", required=True,
                    help="per-neuron bias file pattern with {k}")
    ap.add_argument("--neurons", default=",".join(map(str, DEFAULT_NEURONS)))
    ap.add_argument("--per-cell", type=int, default=15, help="trials per (a,b) cell (x4)")
    ap.add_argument("--T", type=float, default=1.2, help="presentation time (s)")
    ap.add_argument("--burst", type=int, default=10, help="UP events per active bit")
    ap.add_argument("--jitter", type=float, default=0.05)
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--inh-syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--mode", choices=["sum", "signed"], default="signed",
                    help="sum: both bits to exc syn (needs threshold diversity). "
                         "signed: bit->exc/inh per neuron pattern (XOR via inhibition).")
    ap.add_argument("--out", default="reservoir_spikes_xor.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",")]
    rng = np.random.default_rng(args.seed)
    _, ab, labels, groups = make_trials(args.per_cell, args.T, args.burst, args.jitter, rng)
    y_xor = labels["XOR"].astype(int)
    # per-neuron sign pattern (only used in signed mode)
    patt = [SIGN_PATTERNS[i % len(SIGN_PATTERNS)] for i in range(len(neurons))]

    def encode(bi, chan_a, chan_b):
        a, b_ = int(ab[bi, 0]), int(ab[bi, 1])
        if args.mode == "sum":                       # both bits -> exc, coincident
            return signed_events(a, b_, 0, 0, args.burst, args.jitter, args.T, rng)
        return signed_events(a, b_, chan_a, chan_b, args.burst, args.jitter, args.T, rng)

    if args.smoke:
        idx = np.concatenate([np.where((ab[:, 0] * 2 + ab[:, 1]) == c)[0][:3] for c in range(4)])
        ab = ab[idx]; y_xor = y_xor[idx]; groups = groups[idx]
        neurons = neurons[:4]; patt = patt[:4]

    print(f"XOR on-chip ({args.mode}): {len(ab)} trials, {len(neurons)} neurons, "
          f"burst={args.burst}, T={args.T}s, weight={args.weight}  -> {args.out}")

    arr = np.empty((len(neurons), len(ab)), dtype=object)
    for i in range(len(neurons)):
        for bi in range(len(ab)):
            arr[i, bi] = np.array([])
    done = []

    def save_ckpt():
        tmp = args.out + ".tmp.npz"
        np.savez(tmp, spikes=arr, labels=y_xor, records=groups, groups=groups,
                 bits_ab=ab, patterns=np.array(patt), neurons=np.array(neurons),
                 T=args.T, coding=f"xor_{args.mode}", done_neurons=np.array(done, dtype=int))
        os.replace(tmp, args.out)

    corners = {(0, 0): "00", (0, 1): "01", (1, 0): "10", (1, 1): "11"}
    with BridgeSession() as b:
        for i, k in enumerate(neurons):
            ca, cb = patt[i]
            b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
            b.monitor(k); time.sleep(0.8)
            b.program_weight(args.syn, args.weight, exc=True)
            b.program_weight(args.inh_syn, args.weight, exc=False)
            by_corner = {c: [] for c in corners}
            tot = 0
            for bi in range(len(ab)):
                st = present_delta(b, k, encode(bi, ca, cb), args.T, args.syn, args.inh_syn)
                arr[i, bi] = st
                by_corner[(int(ab[bi, 0]), int(ab[bi, 1]))].append(len(st))
                tot += len(st)
            done.append(int(k))
            mc = {c: (np.mean(v) if v else 0.0) for c, v in by_corner.items()}
            pat = f"a->{'inh' if ca else 'exc'},b->{'inh' if cb else 'exc'}"
            print(f"  n{k:2d} [{pat}]: {tot} spk | by corner "
                  f"00->{mc[(0,0)]:.1f} 01->{mc[(0,1)]:.1f} 10->{mc[(1,0)]:.1f} 11->{mc[(1,1)]:.1f}"
                  + ("  [DEAD]" if tot == 0 else ""))
            if not args.smoke:
                save_ckpt()
                print(f"    [checkpoint] {len(done)}/{len(neurons)} -> {args.out}")

    if not args.smoke:
        print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
