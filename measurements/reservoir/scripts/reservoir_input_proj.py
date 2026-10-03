#!/usr/bin/env python3
"""Generate a FIXED per-neuron input-projection config and save it, so the same
projection is applied to every beat (train and test) -- a reproducible random-feature
projection of the ECG in the continuous signal domain, decorrelating the input each
neuron sees.

Per neuron k: {sigma_k (Gaussian smoothing width, samples), shift_k (time shift,
fraction of the beat), theta_k (delta threshold; lower -> more spikes)}.
Encoding: x_k = shift(gaussian_smooth(ECG, sigma_k), shift_k) -> delta_encode(x_k, theta_k).
"""
import argparse
import json
import numpy as np

OUT = "reservoir_input_proj.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16, help="number of neurons")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sigma", default="0.5,6.0", help="Gaussian width range (samples)")
    ap.add_argument("--shift", default="-0.08,0.08", help="time-shift range (fraction of beat)")
    ap.add_argument("--theta", default="0.02,0.05", help="delta threshold range")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    s0, s1 = (float(x) for x in args.sigma.split(","))
    h0, h1 = (float(x) for x in args.shift.split(","))
    t0, t1 = (float(x) for x in args.theta.split(","))
    cfg = []
    for k in range(args.n):
        cfg.append({
            "neuron": k,
            "sigma": round(float(rng.uniform(s0, s1)), 3),      # Gaussian smoothing width
            "shift": round(float(rng.uniform(h0, h1)), 4),       # time shift (fraction of beat)
            "theta": round(float(rng.uniform(t0, t1)), 4),       # delta threshold
        })
    with open(args.out, "w") as f:
        json.dump({"seed": args.seed, "n": args.n, "proj": cfg}, f, indent=2)
    print(f"wrote {args.out}: {args.n} per-neuron projections")
    for c in cfg:
        print(f"  n{c['neuron']:2d}: sigma={c['sigma']:.2f} shift={c['shift']:+.3f} theta={c['theta']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
