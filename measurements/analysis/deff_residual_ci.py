#!/usr/bin/env python3
"""How well determined is the unexplained D_eff residual?

The reference analysis reports a residual of 1.4 D_eff units: silicon
reaches 18.1 where the best model (operating-point matched thresholds + the
measured 11.99 ms acquisition lattice) reaches 16.7. Before any further mechanism
is proposed to account for those 1.4 units, the residual needs an uncertainty,
and it has never had one.

Two facts make that uncertainty large:

  1. D_eff is a participation ratio of a 128-dimensional covariance (16 neurons
     x K=8 kernel samples) estimated from 60 beats, so the covariance has rank at
     most 59. The estimate is NOT converged in beat count -- subsampling shows it
     still climbing at ~1 unit per 3 beats at nb=60.

  2. The residual is a DIFFERENCE of two participation ratios scored on the same
     beats, so its uncertainty is a paired bootstrap over beats -- the same test
     the reference analysis already uses for the accuracy tie -- and not
     the marginal spread of either estimate.

A third term, which the first version of this script missed: the model condition
draws a lattice phase per (neuron, beat) presentation, so one model realisation
is one draw. We average over LATTICE_SEEDS realisations and propagate that
spread into the paired interval.

  PYTHONPATH=. ./.venv-meas/bin/python3 deff_residual_ci.py

Writes data/deff_residual_ci.json.

PROVENANCE:
  MEASURED   silicon spike trains (recording DIM), the 11.986 ms lattice period
  DERIVED    per-neuron thresholds (bisected in deff_operating_point.py)
  SIMULATED  the lattice phase draws
"""
import json

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_datasets import DIM
from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import build_condition, fit_lattice, isis, K, T_BEAT

TAU = 0.02
N_BOOT = 300
LATTICE_SEEDS = 8


def deff(sp, idx=None):
    return corr_effdim(sp if idx is None else sp[:, idx], T_BEAT, K, "exp", TAU)[2]


def load_model_inputs():
    op = np.load("sw_proj_opdispersion.npz", allow_pickle=True)
    with open("reservoir_input_proj.json") as f:
        proj = {int(c["neuron"]): c for c in json.load(f)["proj"]}
    X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(len(X))]
           for k in range(16)}
    return op["vths"], evs


def main():
    sp_si, _, _ = load(DIM.path)
    n, nb = sp_si.shape
    grid, _ = fit_lattice(isis(sp_si))
    vths, evs = load_model_inputs()

    print(f"recording DIM: {n} neurons x {nb} beats -> {n*K} feature dims, "
          f"covariance rank ceiling {min(nb-1, n*K)}")
    print(f"lattice period {grid*1e3:.3f} ms\n")

    # --- 1. is the estimator converged in beat count? ------------------------
    rng = np.random.default_rng(0)
    print("subsample convergence of D_eff (silicon, mean +/- sd over 40 draws):")
    conv = {}
    for frac in (0.5, 0.7, 0.85, 1.0):
        m = max(8, int(round(frac * nb)))
        vals = [deff(sp_si, rng.choice(nb, m, replace=False)) for _ in range(40)]
        conv[m] = [float(np.mean(vals)), float(np.std(vals))]
        print(f"  {m:3d} beats: {np.mean(vals):6.2f} +/- {np.std(vals):.2f}")
    slope = (conv[nb][0] - conv[int(round(0.85 * nb))][0]) / (nb - int(round(0.85 * nb)))
    print(f"  -> still rising at {slope:.2f} D_eff units per beat at nb={nb}\n")

    # --- 2. how much does one lattice realisation matter? --------------------
    models = [build_condition(evs, vths, lattice=grid,
                              rng=np.random.default_rng(100 + s), min_steps=2)
              for s in range(LATTICE_SEEDS)]
    d_mo_seeds = np.array([deff(m) for m in models])
    print(f"model D_eff over {LATTICE_SEEDS} lattice-phase seeds: "
          f"{d_mo_seeds.mean():.2f} +/- {d_mo_seeds.std():.2f} "
          f"(range {d_mo_seeds.min():.2f}-{d_mo_seeds.max():.2f})")

    d_si = deff(sp_si)
    print(f"silicon D_eff {d_si:.2f}   ->  residual "
          f"{d_si - d_mo_seeds.mean():+.2f} on the seed mean\n")

    # --- 3. paired bootstrap over beats, averaging the model over seeds ------
    diffs = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, nb, nb)
        a = deff(sp_si, idx)
        b = np.mean([deff(m, idx) for m in models])
        diffs.append(a - b)
    diffs = np.array(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    print(f"PAIRED bootstrap of the residual (n={N_BOOT}, model averaged over "
          f"{LATTICE_SEEDS} seeds):")
    print(f"  point estimate  {d_si - d_mo_seeds.mean():+.2f}")
    print(f"  bootstrap mean  {diffs.mean():+.2f}   95% CI [{lo:+.2f}, {hi:+.2f}]")
    print(f"  P(residual <= 0) = {float((diffs <= 0).mean()):.3f}")
    print(f"\n  The residual is resolvable but its MAGNITUDE is not: the interval "
          f"spans\n  a factor of {hi/max(lo,1e-9):.0f}. Any mechanism adding "
          f"anywhere in [{lo:.1f}, {hi:.1f}] units\n  is consistent with it, which "
          f"is why closing the gap cannot by itself\n  identify the mechanism.")

    out = {
        "tau_s": TAU, "n_boot": N_BOOT, "lattice_seeds": LATTICE_SEEDS,
        "deff_silicon": float(d_si),
        "deff_model_seed_mean": float(d_mo_seeds.mean()),
        "deff_model_seed_sd": float(d_mo_seeds.std()),
        "residual_point": float(d_si - d_mo_seeds.mean()),
        "residual_boot_mean": float(diffs.mean()),
        "residual_ci95": [float(lo), float(hi)],
        "p_residual_le_0": float((diffs <= 0).mean()),
        "subsample_convergence": conv,
        "provenance": {
            "deff_silicon": "MEASURED (recording DIM)",
            "thresholds": "DERIVED, deff_operating_point.py",
            "lattice_phases": "SIMULATED",
        },
    }
    with open("data/deff_residual_ci.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/deff_residual_ci.json")


if __name__ == "__main__":
    raise SystemExit(main())
