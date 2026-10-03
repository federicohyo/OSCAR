#!/usr/bin/env python3
"""Task B: is the D_eff gap an artifact of the Section 7 read-out path?

D_eff = 18.1 was measured on data acquired with the flash-resident read-out and
host-arrival timestamps. Two properties of that path can inflate a participation
ratio without the substrate doing anything: a per-neuron dead time decorrelates
neurons that would otherwise fire together, and 16 ms timestamp quantisation
smears the states against a 20 ms kernel. Both are testable today, no silicon.

Method: take the heterogeneous SW LIF (which sits at D_eff ~10) and push it
through a model of the acquisition path, stage by stage, then recompute D_eff
with the SAME corr_effdim/build_features the hardware row uses.

The dead time is DERIVED from the recorded data rather than assumed: we sweep the
blanking interval and report which value reproduces the measured event count, and
we cross-check that against the reference analysis's ~250 ms REQ-hold figure.

  ./.venv-meas/bin/python3 deff_acquisition_ablation.py

SUPERSEDED IN PART (round 5, deff_refractory_ablation.py). This script's
conclusion -- "the read-out path is ruled out" -- is too strong, and the
reference analysis no longer makes it. Both results here stand: 16 ms UNIFORM timestamp
quantisation moves D_eff by -1%, and a 250 ms blanking dead time is excluded by
the 282 events/window this recording carries. Neither tests what the acquisition
actually did. Every interval in this recording lies on an 11.986 ms lattice whose
phase is set PER PRESENTATION, with a two-period floor at 23.97 ms; that is not
uniform quantisation, and a 24 ms per-neuron dead time caps a neuron at 83
events/window and the array at 1335, so the 282 argument never excluded it.
Applying the measured lattice carries 60% of the rate-matched residual.
"""
import json

import numpy as np

from reservoir_datasets import DIM
from reservoir_demo_proj import corr_effdim, load

K = 8
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
TAU_TABLE = 0.02
FTDI_FRAME = 0.016            # s, FTDI latency-timer frame


def stats(sp, T):
    n, nb = sp.shape
    per = np.array([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb
                    for j in range(n)])
    isis = []
    for j in range(n):
        for b in range(nb):
            st = np.sort(np.asarray(sp[j, b], dtype=float))
            if st.size > 1:
                isis.extend(np.diff(st))
    isis = np.array(isis) if isis else np.array([np.nan])
    return dict(total_per_beat=float(per.sum()), rate_cv=float(per.std() / per.mean()),
                isi_min=float(np.nanmin(isis)), isi_med=float(np.nanmedian(isis)))


def apply_deadtime(sp, dead):
    """Per-neuron blanking: after a recorded spike, suppress everything for `dead`
    seconds. This is the structure a REQ hold imposes -- not random dropping."""
    out = np.empty_like(sp)
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            st = np.sort(np.asarray(sp[j, b], dtype=float))
            keep, last = [], -np.inf
            for t in st:
                if t - last >= dead:
                    keep.append(t); last = t
            out[j, b] = np.array(keep)
    return out


def apply_quantise(sp, q=FTDI_FRAME):
    out = np.empty_like(sp)
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            st = np.asarray(sp[j, b], dtype=float)
            out[j, b] = np.round(st / q) * q
    return out


def apply_random_drop(sp, keep_frac, seed=0):
    """Sensitivity control: does ANY event loss at this retention do it, or is the
    dead-time STRUCTURE what matters?"""
    rng = np.random.default_rng(seed)
    out = np.empty_like(sp)
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            st = np.asarray(sp[j, b], dtype=float)
            out[j, b] = st[rng.random(st.size) < keep_frac] if st.size else st
    return out


def deff_curve(sp, T):
    return [float(corr_effdim(sp, T, K, "exp", t)[2]) for t in TAUS]


def main():
    hw_sp, _, T = load(DIM.path)   # recording DIM; the 282 events/window are ITS
    sw_sp, _, _ = load("sw_proj_tauonly_mm0.65.npz")
    hw_s, sw_s = stats(hw_sp, T), stats(sw_sp, T)
    print("=== recorded (silicon, Section 7 path) vs heterogeneous SW LIF ===")
    for nm, s in (("silicon", hw_s), ("SW het.", sw_s)):
        print(f"  {nm:8s} events/beat {s['total_per_beat']:6.1f}  rate CV {s['rate_cv']:.3f}  "
              f"ISI min {s['isi_min']*1e3:7.1f} ms  median {s['isi_med']*1e3:6.1f} ms")

    # --- derive the dead time from the data ---------------------------------
    print("\n=== dead-time sweep on the SW LIF: which blanking reproduces silicon? ===")
    target = hw_s["total_per_beat"]
    rows = []
    for dead in [0.0, 0.005, 0.010, 0.020, 0.040, 0.080, 0.125, 0.250]:
        s = stats(apply_deadtime(sw_sp, dead), T) if dead else sw_s
        rows.append((dead, s["total_per_beat"]))
        print(f"  dead {dead*1e3:6.1f} ms -> {s['total_per_beat']:6.1f} events/beat"
              + ("   <-- silicon = %.1f" % target if abs(s['total_per_beat']-target) ==
                 min(abs(r[1]-target) for r in rows) else ""))
    best = min(rows, key=lambda r: abs(r[1] - target))[0]
    print(f"  closest match: {best*1e3:.1f} ms blanking")
    print(f"  NOTE the reference analysis's ~250 ms REQ hold would leave at most "
          f"{16*2.0/0.250:.0f} events/beat across 16 neurons; silicon recorded {target:.1f}.")

    # --- the ablation -------------------------------------------------------
    print("\n=== D_eff through the acquisition model (tau sweep) ===")
    dead_ret = stats(apply_deadtime(sw_sp, best), T)["total_per_beat"] / sw_s["total_per_beat"]
    conds = [
        ("SW het., raw", sw_sp),
        (f"  + dead time {best*1e3:.0f} ms", apply_deadtime(sw_sp, best)),
        (f"  + dead time + 16 ms quantisation", apply_quantise(apply_deadtime(sw_sp, best))),
        (f"  [control] random drop to {dead_ret*100:.0f}%", apply_random_drop(sw_sp, dead_ret)),
        ("SILICON (recorded)", hw_sp),
    ]
    out = {}
    hdr = "  ".join(f"{t*1e3:5.0f}" for t in TAUS)
    print(f"{'condition':38s} {hdr}")
    for nm, sp in conds:
        c = deff_curve(sp, T)
        out[nm.strip()] = c
        print(f"{nm:38s} " + "  ".join(f"{v:5.1f}" for v in c))

    i20 = TAUS.index(TAU_TABLE)
    base = out["SW het., raw"][i20]
    full = out[f"+ dead time + 16 ms quantisation"][i20]
    sil = out["SILICON (recorded)"][i20]
    print(f"\nAt tau = {TAU_TABLE*1e3:.0f} ms:  SW het. {base:.1f}  ->  "
          f"+acquisition {full:.1f}  |  silicon {sil:.1f}")
    print(f"  acquisition model accounts for {100*(full-base)/(sil-base):+.0f}% of the "
          f"SW->silicon gap")
    json.dump({"taus_s": TAUS, "curves": out, "dead_time_s": best,
               "silicon_events_per_beat": target},
              open("data/deff_acquisition_ablation.json", "w"), indent=2)
    print("wrote data/deff_acquisition_ablation.json")


if __name__ == "__main__":
    raise SystemExit(main())
