#!/usr/bin/env python3
"""Reconcile the matched-ceiling result with SHD_reservoir_result.md Result 3.

The doc found rate < rate+feedforward < rate+recurrent (+0.012/+0.018) with RANDOM 5-fold CV,
N=300, FULL 700 channels. My matched run (speaker-independent, N<=16, 700->16 pooled) shows no
recurrence gap. That changed THREE knobs at once. This isolates which knob kills the gap by
changing one at a time, always using the fair rate (+) reservoir readout (compression-controlled).

Knobs: CV = {random 5-fold, speaker-independent} ; input = {full 700, pooled 16} ; N = {300, 16}.
Reports rate+ff vs rate+rec for each config -> which change removes the recurrence gain."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from shd_reservoir import load_binned, reservoir, SP
from shd_matched_ceiling import pool_channels, reservoir_pooled

CLASSES = [5, 9]
SEEDS = 4


def randcv(Z, y, C):
    Z = StandardScaler().fit_transform(Z)
    return np.mean([(cross_val_predict(LogisticRegression(max_iter=2000, C=C), Z, y,
                    cv=StratifiedKFold(5, shuffle=True, random_state=s)) == y).mean()
                    for s in (0, 1)])


def splitfit(Ztr, ytr, Zte, yte, C):
    sc = StandardScaler().fit(Ztr)
    return (LogisticRegression(max_iter=2000, C=C).fit(sc.transform(Ztr), ytr)
            .predict(sc.transform(Zte)) == yte).mean()


def res(X, N, rho, full):
    return (reservoir(X, N, rho, 0.3, 1.0, 0) if full
            else reservoir_pooled(X, N, rho, 0.3, 1.0, 0))


def gap_random(X, y, N, full):
    """random CV on the train pool only (mirrors the doc). rate (+) reservoir."""
    rate = X.sum(1) if full else pool_channels(X, 16).sum(1) if X.shape[-1] == 700 else X.sum(1)
    Xin = X if full else pool_channels(X, 16)
    rate = Xin.sum(1)
    out = {}
    for rho, role in ((0.0, "ff"), (1.1, "rec")):
        accs = []
        for s in range(SEEDS):
            R = (reservoir(Xin, N, rho, 0.3, 1.0, s) if full
                 else reservoir_pooled(Xin, N, rho, 0.3, 1.0, s))
            accs.append(randcv(np.hstack([rate, R]), y, 0.5))
        out[role] = (np.mean(accs), np.std(accs))
    return out


def gap_split(Xtr, ytr, Xte, yte, N, full):
    Itr = Xtr if full else pool_channels(Xtr, 16)
    Ite = Xte if full else pool_channels(Xte, 16)
    rtr, rte = Itr.sum(1), Ite.sum(1)
    out = {}
    for rho, role in ((0.0, "ff"), (1.1, "rec")):
        accs = []
        for s in range(SEEDS):
            Rtr = (reservoir(Itr, N, rho, 0.3, 1.0, s) if full
                   else reservoir_pooled(Itr, N, rho, 0.3, 1.0, s))
            Rte = (reservoir(Ite, N, rho, 0.3, 1.0, s) if full
                   else reservoir_pooled(Ite, N, rho, 0.3, 1.0, s))
            accs.append(splitfit(np.hstack([rtr, Rtr]), ytr, np.hstack([rte, Rte]), yte, 0.5))
        out[role] = (np.mean(accs), np.std(accs))
    return out


def main():
    Xtr, ytr = load_binned(f"{SP}/shd_train.h5", CLASSES, 100000, 50, 1.0, seed=1)
    Xte, yte = load_binned(f"{SP}/shd_test.h5", CLASSES, 100000, 50, 1.0, seed=2)
    print("SHD five/nine, rate (+) reservoir (compression-controlled). gap = rec - ff.\n")
    print(f"{'config':<44} {'ff':>13} {'rec':>13} {'gap':>8}")

    def show(name, out):
        (fa, fs), (ra, rs) = out["ff"], out["rec"]
        print(f"{name:<44} {fa:.3f}+/-{fs:.3f} {ra:.3f}+/-{rs:.3f} {ra-fa:+8.3f}")

    # doc config: random CV, N=300, full 700 (on the train pool, like shd_concat.py)
    show("A. random-CV  N=300  full-700  (doc)", gap_random(Xtr, ytr, 300, True))
    # knob 1: speaker-independent, else same
    show("B. split      N=300  full-700", gap_split(Xtr, ytr, Xte, yte, 300, True))
    # knob 2: pooled input, N=300
    show("C. split      N=300  pooled-16", gap_split(Xtr, ytr, Xte, yte, 300, False))
    # knob 3: N=16 too (my matched config)
    show("D. split      N=16   pooled-16 (matched)", gap_split(Xtr, ytr, Xte, yte, 16, False))
    # extra: random-CV but pooled-16 N=300 -> is it the pooling or the split?
    show("E. random-CV  N=300  pooled-16", gap_random(Xtr, ytr, 300, False))


if __name__ == "__main__":
    raise SystemExit(main())
