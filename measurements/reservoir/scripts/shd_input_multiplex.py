#!/usr/bin/env python3
"""DECIDER for SHD-on-chip recurrence: contiguous 700->16 pooling destroys the recurrence gap
(shd_reconcile.py knob C), because averaging 44 adjacent cochlea channels smooths away the fine
temporal structure recurrence exploits. Fix on a fixed input count: TIME-MULTIPLEX the INPUT
projection -- run M passes, each assigning the 700 channels to the 16 chip inputs by a DIFFERENT
random grouping (a routing table per pass, fully hardware-realizable: each chip input = sum of
its assigned channels' spikes), then concatenate the per-pass reservoir features into one linear
readout. M different random 16-dim views of the 700 channels recover the information one
contiguous pooling threw away, so the recurrence gap should return and grow with M.

If rec > ff beyond error bars at feasible M (speaker-independent), SHD-on-chip is viable and
goes first. Reports the gap vs M."""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from shd_reservoir import load_binned, SP
from shd_matched_ceiling import fit_eval, reservoir_pooled


def random_group(Xseq, n_pool, seed):
    """Assign each of the 700 channels to one of n_pool chip inputs at random (a routing
    table); chip input j = sum of its assigned channels' spikes. (n,T,700)->(n,T,n_pool)."""
    rng = np.random.default_rng(seed)
    assign = rng.integers(0, n_pool, Xseq.shape[-1])
    out = np.zeros((*Xseq.shape[:2], n_pool), np.float32)
    for j in range(n_pool):
        cols = np.where(assign == j)[0]
        if cols.size:
            out[:, :, j] = Xseq[:, :, cols].sum(axis=2)
    return out


def stacked(Xseq, N, rho, a_leak, in_scale, M, seed0):
    """M passes, each a different random 700->16 grouping + reservoir; concat features."""
    feats = []
    for m in range(M):
        P = random_group(Xseq, 16, 1000 + seed0 + m)      # routing table for this pass
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
    print(f"SHD five/nine spk-indep. Time-multiplex M random 700->16 groupings, N=16/pass "
          f"(a_leak={args.a_leak}, rho={args.rho}). gap = rec - ff.\n")
    print(f"{'M':>3} {'inputs_seen':>11} | {'ff':>13} {'rec':>13} {'gap':>8}")
    for M in (1, 2, 4, 8, 16):
        ff, rc = [], []
        for r in range(args.reps):
            s0 = 1 + r * 50
            Ftr0 = stacked(Xtr, 16, 0.0, args.a_leak, args.in_scale, M, s0)
            Fte0 = stacked(Xte, 16, 0.0, args.a_leak, args.in_scale, M, s0)
            Ftr1 = stacked(Xtr, 16, args.rho, args.a_leak, args.in_scale, M, s0)
            Fte1 = stacked(Xte, 16, args.rho, args.a_leak, args.in_scale, M, s0)
            ff.append(fit_eval(Ftr0, ytr, Fte0, yte, 0.5))
            rc.append(fit_eval(Ftr1, ytr, Fte1, yte, 0.5))
        fm, fs, rm, rs = np.mean(ff), np.std(ff), np.mean(rc), np.std(rc)
        print(f"{M:3d} {16*M:11d} | {fm:.3f}+/-{fs:.3f} {rm:.3f}+/-{rs:.3f} {rm-fm:+8.3f}")
    print("\nIf gap grows positive & beyond error bars with M -> SHD-on-chip recurrence viable "
          "via input-multiplexing (SHD goes first).")


if __name__ == "__main__":
    raise SystemExit(main())
