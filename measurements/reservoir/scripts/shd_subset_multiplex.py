#!/usr/bin/env python3
"""DECIDER v2 for SHD-on-chip recurrence. Aggregating 700->16 (pool or random group) destroys
the per-channel timing recurrence exploits. Hardware-faithful alternative: each pass routes 16
INDIVIDUAL cochlea channels (a subset, NO summing) straight to the 16 chip inputs -- preserving
their exact spike timing -- and across M passes covers 16*M distinct channels. Concatenate the
per-pass reservoir features into one linear readout. This should recover the full-700 recurrence
gap far better than aggregation, at feasible M.

Compares three input encodings at matched budget, speaker-independent:
  pool     : contiguous 700->16 sum (baseline, kills the gap)
  subset   : M passes, 16 distinct channels each, no summing (the candidate)
If subset gives rec>ff beyond error bars at feasible M -> SHD-on-chip viable (goes first)."""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from shd_reservoir import load_binned, SP
from shd_matched_ceiling import pool_channels, fit_eval, reservoir_pooled


def subset_pass(Xseq, chans):
    """Route the given 16 channels straight through (no summing). (n,T,700)->(n,T,16)."""
    return Xseq[:, :, chans].astype(np.float32)


def stacked_subset(Xseq, order, N, rho, a_leak, in_scale, M, seed0):
    feats = []
    for m in range(M):
        chans = order[m * 16:(m + 1) * 16]
        P = subset_pass(Xseq, chans)
        feats.append(reservoir_pooled(P, N, rho, a_leak, in_scale, seed0 + m))
    return np.hstack(feats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-leak", type=float, default=0.3)
    ap.add_argument("--in-scale", type=float, default=1.0)
    ap.add_argument("--rho", type=float, default=1.1)
    ap.add_argument("--reps", type=int, default=4)
    args = ap.parse_args()

    Xtr, ytr = load_binned(f"{SP}/shd_train.h5", [5, 9], 100000, 50, 1.0, seed=1)
    Xte, yte = load_binned(f"{SP}/shd_test.h5", [5, 9], 100000, 50, 1.0, seed=2)
    print(f"SHD five/nine spk-indep. Subset-multiplex: M passes x 16 individual channels "
          f"(no summing), N=16/pass, a_leak={args.a_leak}, rho={args.rho}. gap = rec - ff.\n")
    print(f"{'M':>3} {'chans_seen':>10} | {'ff':>13} {'rec':>13} {'gap':>8}")
    for M in (1, 2, 4, 8, 16, 32, 43):        # 43*16=688 ~ all 700 channels
        ff, rc = [], []
        for r in range(args.reps):
            rng = np.random.default_rng(1 + r * 50)
            order = rng.permutation(700)      # random but fixed per rep; same on train & test
            need = M * 16
            order = np.resize(order, need) if need > 700 else order[:need]
            s0 = 1 + r * 50
            Ftr0 = stacked_subset(Xtr, order, 16, 0.0, args.a_leak, args.in_scale, M, s0)
            Fte0 = stacked_subset(Xte, order, 16, 0.0, args.a_leak, args.in_scale, M, s0)
            Ftr1 = stacked_subset(Xtr, order, 16, args.rho, args.a_leak, args.in_scale, M, s0)
            Fte1 = stacked_subset(Xte, order, 16, args.rho, args.a_leak, args.in_scale, M, s0)
            ff.append(fit_eval(Ftr0, ytr, Fte0, yte, 0.5))
            rc.append(fit_eval(Ftr1, ytr, Fte1, yte, 0.5))
        fm, fs, rm, rs = np.mean(ff), np.std(ff), np.mean(rc), np.std(rc)
        print(f"{M:3d} {min(M*16,700):10d} | {fm:.3f}+/-{fs:.3f} {rm:.3f}+/-{rs:.3f} {rm-fm:+8.3f}")
    print("\nGrowing positive gap beyond error bars -> SHD-on-chip recurrence viable via "
          "subset input-multiplexing (SHD goes first).")


if __name__ == "__main__":
    raise SystemExit(main())
