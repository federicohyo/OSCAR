#!/usr/bin/env python3
"""Restore the recurrence gap on SHD five/nine by stacking M PARALLEL 16-neuron reservoirs
into one linear readout (total 16*M features), as suggested: 16 physical neurons fall short of the
headroom for recurrence to beat leaky-feedforward, but M independent reservoirs do.

On-chip realisation: TIME-MULTIPLEX the same 16 neurons across M passes, each pass with a
different recurrent connectivity (SETRECUR pattern) / random projection, and concatenate the
per-pass feature vectors offline -> an effective 16*M-neuron reservoir with a single linear
readout. This tells us the M needed on-chip.

Speaker-independent (train shd_train, test shd_test). Reports the ff vs rec gap vs M."""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from shd_reservoir import load_binned, SP
from shd_matched_ceiling import pool_channels, fit_eval, reservoir_pooled


def stacked(Xpool, N, rho, a_leak, in_scale, M, seed0):
    """Concatenate M independent reservoir passes (different seeds) -> (n, 2*N*M)."""
    return np.hstack([reservoir_pooled(Xpool, N, rho, a_leak, in_scale, seed0 + m)
                      for m in range(M)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-leak", type=float, default=0.1)
    ap.add_argument("--in-scale", type=float, default=0.5)
    ap.add_argument("--rho", type=float, default=1.2)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--reps", type=int, default=4, help="independent draws for mean+/-std")
    args = ap.parse_args()

    Xtr, ytr = load_binned(f"{SP}/shd_train.h5", [5, 9], 100000, 50, 1.0, seed=1)
    Xte, yte = load_binned(f"{SP}/shd_test.h5", [5, 9], 100000, 50, 1.0, seed=2)
    Ptr, Pte = pool_channels(Xtr, 16), pool_channels(Xte, 16)
    rate_tr, rate_te = Ptr.sum(1), Pte.sum(1)

    print(f"SHD five/nine spk-indep. Stack M parallel N={args.N} reservoirs "
          f"(a_leak={args.a_leak}, in_scale={args.in_scale}, rho={args.rho}).")
    print(f"static rate pooled(16) = {fit_eval(rate_tr, ytr, rate_te, yte, 0.1):.3f}\n")
    print(f"{'M':>3} {'tot_neu':>7} | {'ff':>13} {'rec':>13} {'gap':>8} | "
          f"{'rate+ff':>13} {'rate+rec':>13} {'gap':>8}")
    for M in (1, 2, 4, 8, 16):
        ff_a, rc_a, ff_c, rc_c = [], [], [], []
        for r in range(args.reps):
            s0 = 1 + r * 100
            Ftr0 = stacked(Ptr, args.N, 0.0, args.a_leak, args.in_scale, M, s0)
            Fte0 = stacked(Pte, args.N, 0.0, args.a_leak, args.in_scale, M, s0)
            Ftr1 = stacked(Ptr, args.N, args.rho, args.a_leak, args.in_scale, M, s0)
            Fte1 = stacked(Pte, args.N, args.rho, args.a_leak, args.in_scale, M, s0)
            ff_a.append(fit_eval(Ftr0, ytr, Fte0, yte, 1.0))
            rc_a.append(fit_eval(Ftr1, ytr, Fte1, yte, 1.0))
            ff_c.append(fit_eval(np.hstack([rate_tr, Ftr0]), ytr, np.hstack([rate_te, Fte0]), yte, 0.5))
            rc_c.append(fit_eval(np.hstack([rate_tr, Ftr1]), ytr, np.hstack([rate_te, Fte1]), yte, 0.5))
        m = lambda x: (np.mean(x), np.std(x))
        (fa, fas), (ra, ras), (fc, fcs), (rc, rcs) = m(ff_a), m(rc_a), m(ff_c), m(rc_c)
        print(f"{M:3d} {args.N*M:7d} | {fa:.3f}+/-{fas:.3f} {ra:.3f}+/-{ras:.3f} {ra-fa:+8.3f} | "
              f"{fc:.3f}+/-{fcs:.3f} {rc:.3f}+/-{rcs:.3f} {rc-fc:+8.3f}")


if __name__ == "__main__":
    raise SystemExit(main())
