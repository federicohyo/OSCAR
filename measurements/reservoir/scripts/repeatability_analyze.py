#!/usr/bin/env python3
"""Does the array vary enough between trials to be the D_eff residual?

Pre-registered readout (fixed in repeatability_run.py before the run):

    per-neuron CV of the 2 s spike count across repeats of ONE identical beat

    ~20%  -> the per-trial excitability jitter that closes the Section 4.3
             residual in simulation is physically supported
    ~3%   -> it is not; 3% is what Section 4.2's ~1 mV onset-bias repeatability
             implies via nU_T = 31.1 mV

Also reported:
  * trial-0 exclusion check -- the post-routing settling transient (Section 3.3)
  * DAC-reload control -- the same bias file is re-applied mid-block, so a step
    at that trial measures DAC programming rather than the neuron
  * drift vs white -- lag-1 autocorrelation and a linear trend over the block.
    Slow drift (1/f, temperature) is autocorrelated; independent per-trial noise
    is uncorrelated.
  * the excitability jitter IMPLIED by the measured count CV, which is what the
    simulation's jitter parameter has to match

  PYTHONPATH=. ./.venv-meas/bin/python3 repeatability_analyze.py
"""
import json
import sys

import numpy as np

NU_T_MV = 31.1          # measured, Section 4.2


def block_stats(counts):
    """counts: (n_trials,) for one neuron, transient already dropped."""
    c = np.asarray(counts, dtype=float)
    n = len(c)
    mean, sd = c.mean(), c.std(ddof=1) if n > 1 else 0.0
    cv = sd / mean if mean > 0 else np.nan
    # lag-1 autocorrelation: slow drift is correlated, white jitter is uncorrelated
    if n > 3 and sd > 0:
        a = c - mean
        r1 = float(np.sum(a[:-1] * a[1:]) / np.sum(a * a))
    else:
        r1 = np.nan
    # linear trend over the block, expressed as % of the mean across the block
    if n > 3:
        t = np.arange(n)
        slope = np.polyfit(t, c, 1)[0]
        trend = slope * (n - 1) / mean * 100 if mean > 0 else np.nan
    else:
        trend = np.nan
    return mean, sd, cv, r1, trend


def main(path="repeatability_spikes.npz"):
    d = np.load(path, allow_pickle=True)
    sp, wall = d["spikes"], d["wall"]
    neurons = [int(k) for k in d["neurons"]]
    reload_at = int(d["reload_at"])
    interleave = bool(d["interleave"])
    ntr = int(d["trials"])
    print(f"{path}: {len(neurons)} neurons x {ntr} trials "
          f"({'interleaved' if interleave else 'blocked'}), "
          f"beat {int(d['beat_index'])} (label {int(d['beat_label'])}, "
          f"record {str(d['beat_record'])}), {int(d['clk_mhz'])} MHz")

    counts = np.array([[len(np.asarray(sp[k, t])) for t in range(ntr)]
                       for k in neurons], dtype=float)

    # --- trial 0: the routing transient, set aside by pre-registration ---------
    t0, rest = counts[:, 0], counts[:, 1:]
    live = rest.mean(axis=1) > 0
    if live.any():
        d0 = (t0[live] - rest[live].mean(axis=1)) / rest[live].mean(axis=1) * 100
        print(f"\ntrial 0 vs the rest: {np.mean(d0):+.1f}% on average "
              f"(range {np.min(d0):+.0f}% to {np.max(d0):+.0f}%) -- set aside")

    print(f"\n{'neuron':>6s} {'mean':>7s} {'sd':>6s} {'CV':>7s} {'lag-1 r':>8s} "
          f"{'trend':>8s} {'jitter needed':>14s}")
    print("-" * 62)
    rows = {}
    for i, k in enumerate(neurons):
        c = rest[i]
        if c.mean() <= 0:
            print(f"{k:6d} {'silent':>7s}")
            continue
        mean, sd, cv, r1, trend = block_stats(c)
        # a count CV of x implies an excitability (threshold) jitter of roughly the
        # same relative size, since rate is monotone in threshold near this point
        rows[k] = dict(mean=mean, sd=sd, cv=cv, lag1=r1, trend_pct=trend)
        print(f"{k:6d} {mean:7.2f} {sd:6.2f} {cv*100:6.1f}% {r1:8.2f} "
              f"{trend:+7.1f}% {cv*100:13.1f}%")

    cvs = np.array([r["cv"] for r in rows.values()])
    lag1 = np.array([r["lag1"] for r in rows.values()])
    print("-" * 62)
    print(f"median CV across {len(cvs)} live neurons: {np.median(cvs)*100:.1f}%  "
          f"(range {cvs.min()*100:.1f}-{cvs.max()*100:.1f}%)")
    print(f"median lag-1 autocorrelation: {np.nanmedian(lag1):+.2f}  "
          f"(>0 = slow drift, ~0 = white)")

    # --- what the measurement implies for the two hypotheses -----------------
    med = float(np.median(cvs))
    mv = NU_T_MV * np.log(1 + med)
    print(f"\nimplied bias-referred wander: {mv:.2f} mV "
          f"(nU_T = {NU_T_MV} mV, Section 4.2)")
    print(f"  the D_eff residual needs ~20% -> "
          f"{'SUPPORTED' if med > 0.12 else 'NOT SUPPORTED'} by this measurement")
    print(f"  Section 4.2's ~1 mV repeatability implies ~3.3% -> measured "
          f"{med*100:.1f}%")

    # --- DAC reload control ---------------------------------------------------
    if reload_at > 0 and not interleave and reload_at < ntr - 1:
        pre = rest[:, :reload_at - 1]
        post = rest[:, reload_at:]
        ok = (pre.mean(axis=1) > 0) & (post.mean(axis=1) > 0)
        if ok.any():
            step = (post[ok].mean(axis=1) - pre[ok].mean(axis=1)) / pre[ok].mean(axis=1) * 100
            print(f"\nDAC-reload control (same file re-applied before trial "
                  f"{reload_at}):")
            print(f"  mean step {np.mean(step):+.1f}%, |max| {np.max(np.abs(step)):.1f}% "
                  f"-- a large step here would mean DAC programming rather than the neuron")

    # --- cross-neuron correlation (PASS B) -----------------------------------
    if interleave:
        z = (rest - rest.mean(axis=1, keepdims=True))
        sd_ = rest.std(axis=1, keepdims=True)
        good = (sd_[:, 0] > 0)
        z = z[good] / sd_[good]
        R = np.corrcoef(z)
        off = R[~np.eye(R.shape[0], dtype=bool)]
        print(f"\nPASS B -- cross-neuron correlation of per-round fluctuations:")
        print(f"  mean {np.mean(off):+.3f}  (>0 = COMMON-MODE/temperature, "
              f"~0 = PER-DEVICE/1-f)")
        print(f"  simulation says common-mode drift LOWERS D_eff, so a positive "
              f"value closes the temperature story")

    out = {"median_cv": med, "cvs": {str(k): rows[k]["cv"] for k in rows},
           "median_lag1": float(np.nanmedian(lag1)),
           "implied_mv": float(mv), "interleave": interleave,
           "per_neuron": {str(k): rows[k] for k in rows}}
    with open("data/repeatability.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/repeatability.json")


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
