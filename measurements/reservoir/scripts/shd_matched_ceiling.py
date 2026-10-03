#!/usr/bin/env python3
"""SW ceiling for the ON-CHIP SHD five/nine experiment, matched to the chip's constraints.

The on-chip demo pools the 700 SHD cochlea channels down to <=16 chip inputs and runs a
16-neuron reservoir with a LINEAR readout, feedforward (RECURCTRL 0) vs recurrent (firmware
SETRECUR). This script establishes the SW ceiling under THOSE constraints so the on-chip
number has an honest reference, and -- critically -- checks whether the recurrent>feedforward
gap SURVIVES the 700->16 pooling + 16-neuron bottleneck. If the gap dies here, it cannot
appear on-chip, saving bench time.

Speaker-INDEPENDENT: fit on shd_train, test on shd_test (held-out speakers), the honest split.

Three tiers, all with a linear readout:
  static rate (16-dim pooled)  -- time averaged out, the temporal-processing control
  N=16 rate ESN, rho=0 (ff)    -- leaky membrane memory only (chip's RECURCTRL 0)
  N=16 rate ESN, rho>0 (rec)   -- + network recurrence (chip's SETRECUR)
Plus the UNCONSTRAINED N=400 ESN as the upper bound for context.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from shd_reservoir import load_binned, reservoir, SP, C


def pool_channels(Xseq, n_pool):
    """(n, T, 700) -> (n, T, n_pool) by summing contiguous cochlea bands. The on-chip
    analogue: each chip input neuron receives the merged spikes of a contiguous band."""
    n, T, ch = Xseq.shape
    edges = np.linspace(0, ch, n_pool + 1).astype(int)
    out = np.zeros((n, T, n_pool), dtype=np.float32)
    for j in range(n_pool):
        out[:, :, j] = Xseq[:, :, edges[j]:edges[j + 1]].sum(axis=2)
    return out


def fit_eval(Ztr, ytr, Zte, yte, C_reg=1.0):
    sc = StandardScaler().fit(Ztr)
    clf = LogisticRegression(max_iter=2000, C=C_reg).fit(sc.transform(Ztr), ytr)
    return (clf.predict(sc.transform(Zte)) == yte).mean()


def reservoir_pooled(Xpool, N, rho, a_leak, in_scale, seed):
    """Rate/tanh ESN on the POOLED input (C_in = Xpool.shape[-1]); mirrors shd_reservoir.reservoir
    but with the pooled channel count as the input dimension."""
    rng = np.random.default_rng(seed)
    Cin = Xpool.shape[-1]
    W = rng.standard_normal((N, N)) * (rng.random((N, N)) < 0.15)
    sr = np.max(np.abs(np.linalg.eigvals(W)))
    W = W * (rho / sr) if sr > 0 else W
    W_in = rng.standard_normal((N, Cin)) * in_scale / np.sqrt(Cin)
    n, T, _ = Xpool.shape
    feats = np.zeros((n, 2 * N), dtype=np.float32)
    for i in range(n):
        x = np.zeros(N); acc = np.zeros(N)
        seq = Xpool[i]
        for t in range(T):
            x = (1 - a_leak) * x + a_leak * np.tanh(W_in @ seq[t] + W @ x)
            acc += x
        feats[i] = np.concatenate([x, acc / T])
    return feats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="5,9")
    ap.add_argument("--n-pool", type=int, default=16)
    ap.add_argument("--T", type=int, default=50)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--rho", type=float, default=1.1)
    ap.add_argument("--seeds", type=int, default=5)
    args = ap.parse_args()
    classes = [int(x) for x in args.classes.split(",")]

    Xtr, ytr = load_binned(f"{SP}/shd_train.h5", classes, 100000, args.T, 1.0, seed=1)
    Xte, yte = load_binned(f"{SP}/shd_test.h5", classes, 100000, args.T, 1.0, seed=2)
    print(f"SHD {classes} speaker-independent: train n={len(ytr)} {np.bincount(ytr).tolist()}, "
          f"test n={len(yte)} {np.bincount(yte).tolist()}, pool 700->{args.n_pool}, T={args.T}\n")

    Ptr, Pte = pool_channels(Xtr, args.n_pool), pool_channels(Xte, args.n_pool)

    # --- static rate controls (pooled 16-dim, and full 700-dim for reference) ---
    a = fit_eval(Ptr.sum(1), ytr, Pte.sum(1), yte, 0.1)
    print(f"  static rate pooled({args.n_pool})      + linear   {a:.3f}")
    a = fit_eval(Xtr.sum(1), ytr, Xte.sum(1), yte, 0.1)
    print(f"  static rate full(700)      + linear   {a:.3f}   (unpooled reference)")

    # --- matched N=16 ESN on 16 pooled inputs: ff vs rec (THE gap that must survive) ---
    print(f"\n  matched N={args.N} ESN on {args.n_pool} pooled inputs (linear readout):")
    for rho, role in [(0.0, "feedforward"), (args.rho, "RECURRENT")]:
        alone, concat = [], []
        for s in range(args.seeds):
            Rtr = reservoir_pooled(Ptr, args.N, rho, 0.3, 1.0, s)
            Rte = reservoir_pooled(Pte, args.N, rho, 0.3, 1.0, s)
            alone.append(fit_eval(Rtr, ytr, Rte, yte, 1.0))
            concat.append(fit_eval(np.hstack([Ptr.sum(1), Rtr]), ytr,
                                   np.hstack([Pte.sum(1), Rte]), yte, 0.5))
        print(f"    reservoir {role:<11} alone         {np.mean(alone):.3f} +/- {np.std(alone):.3f}")
        print(f"    rate + {role:<11} reservoir     {np.mean(concat):.3f} +/- {np.std(concat):.3f}")

    # --- unconstrained N=400 full-700 ESN: the upper bound ---
    print(f"\n  unconstrained N=400 ESN on full 700 (upper bound):")
    for rho, role in [(0.0, "feedforward"), (1.1, "RECURRENT")]:
        acc = []
        for s in range(args.seeds):
            Rtr = reservoir(Xtr, 400, rho, 0.3, 1.0, s)
            Rte = reservoir(Xte, 400, rho, 0.3, 1.0, s)
            acc.append(fit_eval(Rtr, ytr, Rte, yte, 1.0))
        print(f"    reservoir {role:<11} alone         {np.mean(acc):.3f} +/- {np.std(acc):.3f}")


if __name__ == "__main__":
    main()
