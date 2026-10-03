#!/usr/bin/env python3
"""Does ANY 16-neuron operating point give a clean recurrent>feedforward gap on SHD five/nine
(speaker-independent, 700->16 pooled)? The default point showed no gap; the recurrence value
only appears when feedforward's intrinsic (leaky-membrane) memory is SHORTER than the task's
discriminative timescale, so recurrence supplies the needed memory. Sweep membrane leak
(a_leak: high=short memory), spectral radius (rho), and input scale; report the rec-ff gap.
This localises the target regime to tune the CHIP toward (short membrane tau + recurrence)."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from shd_reservoir import load_binned, SP
from shd_matched_ceiling import pool_channels, fit_eval, reservoir_pooled

classes = [5, 9]
Xtr, ytr = load_binned(f"{SP}/shd_train.h5", classes, 100000, 50, 1.0, seed=1)
Xte, yte = load_binned(f"{SP}/shd_test.h5", classes, 100000, 50, 1.0, seed=2)
Ptr, Pte = pool_channels(Xtr, 16), pool_channels(Xte, 16)
rate_tr, rate_te = Ptr.sum(1), Pte.sum(1)
SEEDS = 5

print(f"SHD {classes} spk-indep, N=16, pool 700->16. Gap = rec - ff (reservoir-alone).\n")
print(f"{'a_leak':>7} {'in_scl':>7} | {'ff(rho=0)':>10} {'rec(rho=1.1)':>13} {'gap':>7} | "
      f"{'ff+rate':>8} {'rec+rate':>9} {'gap':>7}")
for a_leak in (0.05, 0.1, 0.2, 0.4, 0.7, 1.0):
    for in_scale in (0.5, 1.0, 2.0):
        res = {}
        for rho in (0.0, 1.1):
            alone, concat = [], []
            for s in range(SEEDS):
                Rtr = reservoir_pooled(Ptr, 16, rho, a_leak, in_scale, s)
                Rte = reservoir_pooled(Pte, 16, rho, a_leak, in_scale, s)
                alone.append(fit_eval(Rtr, ytr, Rte, yte, 1.0))
                concat.append(fit_eval(np.hstack([rate_tr, Rtr]), ytr,
                                       np.hstack([rate_te, Rte]), yte, 0.5))
            res[rho] = (np.mean(alone), np.mean(concat))
        ff_a, ff_c = res[0.0]; rc_a, rc_c = res[1.1]
        print(f"{a_leak:7.2f} {in_scale:7.1f} | {ff_a:10.3f} {rc_a:13.3f} {rc_a-ff_a:+7.3f} | "
              f"{ff_c:8.3f} {rc_c:9.3f} {rc_c-ff_c:+7.3f}")
