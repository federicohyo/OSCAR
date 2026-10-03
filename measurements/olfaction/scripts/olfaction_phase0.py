#!/usr/bin/env python3
"""Phase 0: does correlated vs anti-correlated survive a delta encoder, and does it
need one? Scored as a function of modulation frequency, with every control alongside.

The task is temporal BY CONSTRUCTION -- both classes deliver identical quantities of
both gases and differ only in inter-channel phase (olfaction.md). So:

  * the RATE control must sit at chance. A deviation points to the encoder or the split
    leaking and nothing else in the table means anything.
  * the RAW control is the honest "do you need the spike encoding at all" test, the
    counterpart of the ECG count cue that turned out to solve that task unaided.
  * SHUFFLED labels give the chance floor at this group count, which departs from 0.5 when
    there are only ~12 groups.

Grouping is by GAS PAIR rather than by trial: the power is in groups, and the ECG work spent
a day relearning that. A pair seen in training stays out of test.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_phase0.py
"""
import argparse
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FS = 1000.0
T0_EXTRACT = -1.0          # window start of the npz, s


def preprocess(X, t, win, hp_ms):
    """Per-channel fractional change from each trial's own pre-stimulus baseline, then
    high-pass. MOx resistances span three decades across channels so the normalisation
    is mandatory, and the recovery tail is slow enough that the high-pass is needed;
    otherwise the delta encoder fires mostly on the ramp rather than on the odour."""
    base = X[:, t < -0.05, :].mean(axis=1, keepdims=True)
    r = (X - base) / np.abs(base)
    if hp_ms:
        k = int(hp_ms * FS / 1000.0)
        ker = np.ones(k) / k
        sm = np.stack([[np.convolve(r[i, :, c], ker, mode="same")
                        for c in range(r.shape[2])] for i in range(r.shape[0])])
        r = r - np.transpose(sm, (0, 2, 1))
    m = (t >= win[0]) & (t < win[1])
    return r[:, m, :]


def delta_kernel_feats(r, theta, taus=(0.002, 0.005, 0.02, 0.08), K=96):
    """Level-crossing encode each channel, then an exponential kernel sampled at K
    points.

    K and the tau set differ from the ECG pipeline's. K=8 over 1.5 s is one sample per
    187 ms, which cannot represent a 60 Hz modulation at all -- inheriting it made the
    high-frequency rows uninformative rather than negative. K=96 gives ~16 ms
    resolution, and tau=2 ms resolves a 60 Hz period."""
    n, T, C = r.shape
    out = np.zeros((n, C * len(taus) * K * 2), dtype=np.float64)
    for i in range(n):
        col = 0
        for c in range(C):
            x = r[i, :, c]
            lvl = np.floor(x / theta)
            d = np.diff(lvl, prepend=lvl[0])
            up = np.where(d > 0, d, 0.0)          # UP level crossings
            dn = np.where(d < 0, -d, 0.0)         # DOWN level crossings
            for ev in (up, dn):
                for tau in taus:
                    a = np.exp(-1.0 / (tau * FS))
                    s = np.zeros(T)
                    acc = 0.0
                    for k in range(T):
                        acc = acc * a + ev[k]
                        s[k] = acc
                    idx = np.linspace(0, T - 1, K).astype(int)
                    out[i, col:col + K] = s[idx]
                    col += K
    return out


def score(F, y, groups, seed=0, shuffle=False):
    # Some kernel features are near-constant across trials; the scaler's divide then
    # overflows and hands the classifier inf. Guard rather than silently drop.
    F = np.nan_to_num(np.asarray(F, dtype=np.float64), nan=0.0, posinf=0.0, neginf=0.0)
    rng = np.random.default_rng(seed)
    yy = rng.permutation(y) if shuffle else y
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, yy, groups):
        if len(np.unique(yy[tr])) < 2 or len(te) == 0:
            continue
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, class_weight="balanced",
                                             max_iter=4000))
        m.fit(F[tr], yy[tr])
        accs.append((m.predict(F[te]) == yy[te]).mean())
    return float(np.mean(accs)), float(np.std(accs)), len(accs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="data_olfaction/olfaction_corr_acorr.npz")
    ap.add_argument("--win", default="0,1.5", help="analysis window (s); stimulus is 0-0.95 s")
    ap.add_argument("--hp-ms", type=float, default=100.0, help="high-pass window, 0 disables")
    ap.add_argument("--theta", type=float, default=0.02, help="level-crossing threshold")
    ap.add_argument("--out", default="data/olfaction_phase0.json")
    args = ap.parse_args()
    win = tuple(float(x) for x in args.win.split(","))

    d = np.load(args.npz, allow_pickle=True)
    X, y, meta = d["X"], d["y"], d["meta"]
    t = np.arange(X.shape[1]) / FS + T0_EXTRACT
    conds = np.array([m[0] for m in meta])
    freqs = np.array([m[1] for m in meta])
    groups = np.array([f"{min(m[2],m[3])}|{max(m[2],m[3])}" for m in meta])
    order = sorted(set(freqs), key=lambda s: float(s.replace("Hz", "")))

    print(f"window {win} s, high-pass {args.hp_ms:.0f} ms, theta {args.theta}")
    print(f"{len(X)} trials, {len(set(groups))} gas pairs (CV groups)\n")
    print(f"{'freq':>6} {'n':>4} {'grp':>4} | {'RATE (must be chance)':>21} "
          f"{'RAW traces':>16} {'DELTA+kernel':>16} {'shuffled':>15}")
    res = {}
    for cond in sorted(set(conds)):
        print(f"\n--- {cond} ---")
        for f in order:
            m = (freqs == f) & (conds == cond)
            if m.sum() == 0:
                continue
            r = preprocess(X[m], t, win, args.hp_ms)
            yy, gg = y[m], groups[m]
            rate = r.mean(axis=1)
            raw = r[:, ::4, :].reshape(len(r), -1)              # 250 Hz: above Nyquist for 60 Hz
            dk = delta_kernel_feats(r, args.theta)
            a_rate = score(rate, yy, gg)
            a_raw = score(raw, yy, gg)
            a_dk = score(dk, yy, gg)
            a_sh = score(dk, yy, gg, shuffle=True)
            res[f"{cond}|{f}"] = {"rate": a_rate, "raw": a_raw, "delta_kernel": a_dk,
                                  "shuffled": a_sh, "n": int(m.sum()), "groups": a_dk[2]}
            print(f"{f:>6} {m.sum():4d} {a_dk[2]:4d} | {a_rate[0]:8.3f} +/- {a_rate[1]:.3f}  "
                  f"{a_raw[0]:6.3f} +/- {a_raw[1]:.3f}  {a_dk[0]:6.3f} +/- {a_dk[1]:.3f}  "
                  f"{a_sh[0]:6.3f} +/- {a_sh[1]:.3f}")
    json.dump({"win": win, "hp_ms": args.hp_ms, "theta": args.theta, "per_freq": res},
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
