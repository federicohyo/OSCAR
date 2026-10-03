#!/usr/bin/env python3
"""XOR on-chip (signed exc/inh) with PER-NEURON on-chip-burst drive CALIBRATION.

Root cause fix for silent high-threshold neurons (e.g. n3): the original runner fires host-paced
single spikes (~5 ms apart) that don't summate, so a high-threshold neuron never crosses. Here
each bit is delivered as an ON-CHIP burst (`fire(N)` = N spikes fired rapidly on-die, which
summate), with N CALIBRATED per neuron to a target output (small N for hot neurons like n5,
~40 for n3). exc/inh are INTERLEAVED in small chunks so the XOR cancellation still happens on the
membrane. One neuron at a time (its own `_jul10` bias). Raw spikes saved -> score offline with
data/plots/score_xor_dimcurve.py (XOR rises with #neurons; OR control flat).

    ./.venv-meas/bin/python3 reservoir_run_xor_cal.py \
        --bias-pattern 'ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases' \
        --per-cell 12 --out data/xor_dim/xor_cal_rep0.npz
"""
import argparse, os, time, queue
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_synthtask import make_trials

SIGN_PATTERNS = [(0, 1), (1, 0), (0, 0)]     # (chan_a, chan_b): 0=exc, 1=inh


def collect(b, k, until, t0, times):
    while time.time() < until:
        try:
            line = b.out_q.get(timeout=0.002)
        except queue.Empty:
            continue
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3 and p[1].isdigit() and int(p[1]) == k:
                times.append(time.time() - t0)


def present_cal(b, k, a, bit_b, ca, cb, N, T, chunk=4):
    """Deliver bit a (chan ca) and bit b (chan cb) as interleaved on-chip bursts totalling ~N
    spikes each, then read neuron k over [0,T]. Returns spike times (s)."""
    b.drain(max_lines=200000)
    times = []
    t0 = time.time()
    rounds = max(1, N // chunk)
    for _ in range(rounds):
        if a:
            b.route(0, k, exc=(ca == 0)); b.fire(chunk)
        if bit_b:
            b.route(0, k, exc=(cb == 0)); b.fire(chunk)
    collect(b, k, t0 + T, t0, times)
    return np.array(times)


def calibrate(b, k, T, target, nmax=64, chunk=4):
    """Ramp on-chip burst N until a full exc drive gives >= target output spikes (capped nmax)."""
    N = chunk
    while N <= nmax:
        st = present_cal(b, k, 1, 1, 0, 0, N, T, chunk)   # both bits exc = max drive
        if len(st) >= target:
            return N, len(st)
        N += chunk
    return nmax, len(st)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias-pattern", required=True)
    ap.add_argument("--neurons", default=",".join(map(str, range(16))))
    ap.add_argument("--per-cell", type=int, default=12)
    ap.add_argument("--T", type=float, default=1.2)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--calib-target", type=int, default=6, help="min output spikes at full drive")
    ap.add_argument("--chunk", type=int, default=4)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="data/xor_dim/xor_cal.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",")]
    patt = [SIGN_PATTERNS[i % len(SIGN_PATTERNS)] for i in range(len(neurons))]
    rng = np.random.default_rng(args.seed)
    _, ab, labels, groups = make_trials(args.per_cell, args.T, 10, 0.05, rng)
    y_xor = labels["XOR"].astype(int)
    if args.smoke:
        idx = np.concatenate([np.where((ab[:, 0]*2+ab[:, 1]) == c)[0][:3] for c in range(4)])
        ab, y_xor, groups = ab[idx], y_xor[idx], groups[idx]
        neurons, patt = neurons[:4], patt[:4]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    arr = np.empty((len(neurons), len(ab)), object)
    for i in range(len(neurons)):
        for bi in range(len(ab)):
            arr[i, bi] = np.array([])
    done, ncal = [], []

    def save():
        tmp = args.out + ".tmp.npz"
        np.savez(tmp, spikes=arr, labels=y_xor, records=groups, groups=groups, bits_ab=ab,
                 patterns=np.array(patt), neurons=np.array(neurons), T=args.T,
                 coding="xor_signed_cal", done_neurons=np.array(done, int),
                 ncal=np.array(ncal, int))
        os.replace(tmp, args.out)

    print(f"XOR-cal on-chip: {len(ab)} trials, {len(neurons)} neurons, target>={args.calib_target} spk -> {args.out}")
    with BridgeSession() as b:
        for i, k in enumerate(neurons):
            ca, cb = patt[i]
            b.apply_biases(load_biases(args.bias_pattern.format(k=k)))
            b.monitor(k); time.sleep(0.7)
            b.program_weight(0, args.weight, exc=True)
            b.program_weight(0, args.weight, exc=False)
            Ncal, cal_out = calibrate(b, k, args.T, args.calib_target, chunk=args.chunk)
            ncal.append(Ncal)
            by = {c: [] for c in [(0, 0), (0, 1), (1, 0), (1, 1)]}
            tot = 0
            for bi in range(len(ab)):
                st = present_cal(b, k, int(ab[bi, 0]), int(ab[bi, 1]), ca, cb, Ncal, args.T, args.chunk)
                arr[i, bi] = st
                by[(int(ab[bi, 0]), int(ab[bi, 1]))].append(len(st))
                tot += len(st)
            done.append(int(k))
            mc = {c: (np.mean(v) if v else 0.0) for c, v in by.items()}
            pat = f"a->{'inh' if ca else 'exc'},b->{'inh' if cb else 'exc'}"
            print(f"  n{k:2d} [{pat}] Ncal={Ncal:2d}(cal_out={cal_out}): {tot} spk | "
                  f"00={mc[(0,0)]:.1f} 01={mc[(0,1)]:.1f} 10={mc[(1,0)]:.1f} 11={mc[(1,1)]:.1f}"
                  + ("  [DEAD]" if tot == 0 else ""))
            if not args.smoke:
                save()
    if not args.smoke:
        save(); print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
