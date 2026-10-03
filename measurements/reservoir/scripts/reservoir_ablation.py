#!/usr/bin/env python3
"""Offline 'variation as computation' ablations on recorded raw reservoir spikes.
Every arm is a feature-source variant sharing a FIXED kernel, classifier and
inter-patient CV split (per ABLATION_TODO.md rigor protocol).

  A0  full 16-neuron reservoir (reference)
  A1a homogeneous surrogate: replicate ONE neuron x16 at matched feature dimension
  A2  diversity dose-response: accuracy vs k neurons (informative-first / least / random)
  A6  neuron-identity shuffle: break the neuron->slot mapping at test time

  python reservoir_ablation.py --npz reservoir_spikes_nv_delta.npz --shape exp --tau 0.08
"""

import argparse
import numpy as np
from reservoir_kernel import build_features, cv_acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_delta.npz")
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--shape", default="exp")
    ap.add_argument("--tau", type=float, default=0.08)
    ap.add_argument("--mode", default="patient", choices=["patient", "beat"])
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y = d["spikes"], d["labels"]
    T = float(d["T"]); groups = d["records"]
    n = spikes.shape[0]; K = args.K
    Xf = build_features(spikes, T, K, args.shape, args.tau)   # (nbeats, n*K)
    print(f"{args.npz}: {n} neurons, {spikes.shape[1]} beats, coding={d['coding']}, "
          f"kernel={args.shape} tau={args.tau*1000:.0f}ms, {args.mode} CV")

    def cols(idx):
        return np.concatenate([np.arange(k * K, (k + 1) * K) for k in idx])

    def acc(idx):
        return cv_acc(Xf[:, cols(idx)], y, groups, args.mode)

    # A0 reference
    m, s = acc(range(n))
    print(f"\nA0  full {n}-neuron reservoir            : {m:.3f} +/- {s:.3f}")

    # per-neuron single-neuron accuracy -> ranking proxy for 'informative/diverse'
    single = np.array([acc([k])[0] for k in range(n)])
    order = np.argsort(single)[::-1]           # most-informative first
    print("    per-neuron single acc:", {int(k): round(float(single[k]), 2) for k in range(n)})

    # A1a homogeneous surrogate: best neuron replicated to matched dimension
    bk = int(order[0])
    Xrep = Xf[:, cols([bk] * n)]               # n identical blocks -> same dim, no diversity
    m, s = cv_acc(Xrep, y, groups, args.mode)
    print(f"A1a replicate neuron {bk:2d} x{n} (matched dim): {m:.3f} +/- {s:.3f}   "
          f"[if << A0, diversity computes]")

    # A2 dose-response
    print("A2  dose-response (accuracy vs k neurons):")
    rng = np.random.default_rng(0)
    for k in sorted(set([1, 2, 4, 8, n])):
        hi = acc(order[:k])[0]
        lo = acc(order[-k:])[0]
        rd = np.mean([acc(rng.choice(n, k, replace=False))[0] for _ in range(10)])
        print(f"     k={k:2d}: informative-first={hi:.3f}  least-first={lo:.3f}  random={rd:.3f}")

    # A6 neuron-identity shuffle: permute neuron->slot ordering (breaks stable filters
    # only meaningfully when done between train/test; here we report the fully-permuted
    # feature block ordering as a coarse control -- a proper per-fold shuffle is a TODO).
    perm = rng.permutation(n)
    m, s = cv_acc(Xf[:, cols(perm)], y, groups, args.mode)
    print(f"A6  neuron-slot permuted (coarse control): {m:.3f} +/- {s:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
