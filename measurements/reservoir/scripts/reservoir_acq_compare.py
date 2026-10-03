#!/usr/bin/env python3
"""Is the new acquisition free of the artefact that contaminated the old one?

The manuscript's Section 4.3 decomposition currently attributes 2.4 of its 4.1
rate-matched D_eff units to the ACQUISITION rather than to the array: every
inter-event interval in all three 2026-07 ECG recordings lies on an 11.99 ms
lattice whose phase is redrawn per presentation, with a two-slot floor at 23.97
ms. That lattice is the flash-resident read-out plus host-arrival timestamps.

The 2026-08-11 re-acquisition runs on the fixed path -- SRAM-resident drain, 21-bit
on-chip Timer0 timestamps -- so the lattice should be absent. If it is, the largest
modelled term in the decomposition disappears and Fig. 11 can be regenerated on an
acquisition whose D_eff belongs to the array.

This script runs the SAME lattice test the old recordings failed
(deff_refractory_ablation.premise_test) against old and new, side by side.

  PYTHONPATH=. ./.venv-meas/bin/python3 reservoir_acq_compare.py [new.npz]
"""
import sys

import numpy as np

from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import fit_lattice, isis, trial_phase_concentration

K, T_BEAT = 8, 2.0
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
OLD = "reservoir_spikes_nv_randproj.npz"


def describe(path):
    sp, y, T = load(path)
    n, nb = sp.shape
    d = isis(sp)
    g, res = fit_lattice(d)
    steps = np.round(d / g).astype(int)
    hist = {int(k): int((steps == k).sum()) for k in range(1, 6)}
    frac_int = float(np.mean(np.abs(d / g - np.round(d / g)) < 0.15))
    per = np.array([sum(len(np.asarray(sp[j, b])) for b in range(nb))
                    / nb / T_BEAT for j in range(n)])
    mins = np.array([min([np.min(np.diff(np.sort(np.asarray(sp[j, b]))))
                          for b in range(nb)
                          if len(np.asarray(sp[j, b])) > 1] or [np.nan])
                     for j in range(n)])
    rho = corr_effdim(sp, T_BEAT, K, "exp", 0.02)[1]
    curve = [corr_effdim(sp, T_BEAT, K, "exp", t)[2] for t in TAUS]

    print(f"\n=== {path} ===")
    print(f"  {n} neurons x {nb} beats,  events/window "
          f"{sum(len(np.asarray(sp[j,b])) for j in range(n) for b in range(nb))/nb:.0f}")
    print(f"  rates {per.min():.1f}-{per.max():.1f} Hz (median {np.median(per):.1f}), "
          f"CV across neurons {per.std()/per.mean():.2f}")
    print(f"  best-fit lattice period      {g*1e3:.3f} ms "
          f"(mean |residual| {res*100:.1f}% of a period)")
    print(f"  intervals within 15% of an integer multiple: {frac_int*100:.0f}%")
    print(f"  lattice-step histogram k<=5  {hist}")
    print(f"  per-trial phase concentration {trial_phase_concentration(sp, g):.3f} "
          f"(1.0 = one lattice per trial)")
    print(f"  per-neuron min ISI {np.nanmin(mins)*1e3:.1f}-{np.nanmax(mins)*1e3:.1f} ms "
          f"(spread {np.nanstd(mins)/np.nanmean(mins)*100:.1f}%)")
    print(f"  <|rho|> {rho:.3f}   D_eff(tau) " + "  ".join(f"{c:.1f}" for c in curve))
    return dict(period_ms=g * 1e3, frac_int=frac_int,
                phase=trial_phase_concentration(sp, g), rho=rho, curve=curve,
                min_isi_spread=float(np.nanstd(mins) / np.nanmean(mins)))


def main(new="reservoir_spikes_nv_randproj_aug11.npz"):
    o = describe(OLD)
    n = describe(new)
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    print(f"  integer-multiple fraction   old {o['frac_int']*100:.0f}%   "
          f"new {n['frac_int']*100:.0f}%")
    print(f"  per-trial phase concentr.   old {o['phase']:.3f}   new {n['phase']:.3f}")
    print(f"  per-neuron min-ISI spread   old {o['min_isi_spread']*100:.1f}%  "
          f"new {n['min_isi_spread']*100:.1f}%")
    gone = (n["frac_int"] < 0.7) or (n["phase"] < 0.5)
    print("\n  the 11.99 ms acquisition lattice is "
          + ("GONE from the new recording -- the largest modelled term in the "
             "Section 4.3\n  decomposition does not apply to it, and Fig. 11 can be "
             "regenerated on it."
             if gone else
             "STILL PRESENT -- do not treat the new\n  recording as artefact-free; "
             "investigate before regenerating Fig. 11."))


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
