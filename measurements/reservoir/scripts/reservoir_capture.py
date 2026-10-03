#!/usr/bin/env python3
"""Capture full spike timing for a few ECG beats across all 16 reservoir neurons,
for the demonstration figure (ECG stimulus -> 16-neuron raster -> kernel-reconstructed
state traces). Uses the per-neuron tuned biases, one neuron at a time.
"""

import argparse
import time
import numpy as np

from meas_common import BridgeSession, load_biases
from reservoir_data import get_beats, encode_rate
from reservoir_run import BIAS_PATTERN, rate_profile

import queue


def present_times(b, neuron, rates, t_step):
    """Drive the rate profile on `neuron`; return spike times (s, rel. to onset)."""
    b.drain(max_lines=100000)
    times = []
    t0 = time.time()
    for i, rate in enumerate(rates):
        b.poisson(float(rate))
        step_end = t0 + (i + 1) * t_step
        while time.time() < step_end:
            try:
                line = b.out_q.get(timeout=0.02)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3:
                    try:
                        if int(p[1]) == neuron:
                            times.append(time.time() - t0)
                    except ValueError:
                        pass
    b.poisson_stop()
    return times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=3)
    ap.add_argument("--nsteps", type=int, default=16)
    ap.add_argument("--tstep", type=float, default=0.06)
    ap.add_argument("--fmin", type=float, default=20.0)
    ap.add_argument("--fmax", type=float, default=200.0)
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--out", default="reservoir_capture.npz")
    args = ap.parse_args()

    X, y, meta = get_beats(records=tuple(args.records.split(",")),
                           n_per_class=args.n_per_class)
    T = args.nsteps * args.tstep
    profiles = np.array([rate_profile(X[i], args.nsteps, args.fmin, args.fmax)
                         for i in range(len(X))])

    # spikes[k] -> list (len=n_beats) of arrays of spike times
    spikes = {k: [None] * len(X) for k in range(16)}
    with BridgeSession() as b:
        for k in range(16):
            b.apply_biases(load_biases(BIAS_PATTERN.format(k=k)))
            time.sleep(0.8)
            b.program_weight(args.syn, args.weight, exc=True)
            b.route(args.syn, k, exc=True)
            for bi in range(len(X)):
                spikes[k][bi] = np.array(present_times(b, k, profiles[bi], args.tstep))
            print(f"  neuron {k:2d}: "
                  + " ".join(str(len(spikes[k][bi])) for bi in range(len(X))))

    # save as object arrays
    np.savez(args.out,
             beats=X, labels=y, profiles=profiles, T=T,
             fs=meta["fs"], tstep=args.tstep, nsteps=args.nsteps,
             spikes=np.array([[spikes[k][bi] for bi in range(len(X))]
                              for k in range(16)], dtype=object))
    print("wrote", args.out, f"({len(X)} beats, labels {np.bincount(y)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
