#!/usr/bin/env python3
"""Closing the D_eff scalar is not the same as reproducing the array.

deff_physical_mechanisms.py finds one condition that closes the Section 4.3
residual: per-trial excitability jitter at 20% lands at D_eff 18.0 against
silicon's 18.1. Taken alone that would read as "the residual is trial-to-trial
excitability variation, mechanism found".

It is not, and this script is the test that says so. A mechanism that genuinely
reproduces the array has to match the whole kernel sweep and the mean pairwise
correlation, not one point of one curve. Three statistics, paired-bootstrapped
over beats:

    D_eff at tau = 20 ms   the reference analysis's number, which jitter matches
    D_eff at tau = 320 ms  the long-kernel tail, which it does not
    <|rho|>                mean pairwise neuron correlation

  PYTHONPATH=. ./.venv-meas/bin/python3 deff_identifiability.py

Writes data/deff_identifiability.json.
"""
import json

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_datasets import DIM
from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import apply_lattice, fit_lattice, isis
from deff_physical_sim import build_jump, simulate
from deff_physical_mechanisms import (NN, NB, T_BEAT, K, bisect_to_rates,
                                      flatten_events, silicon_rates, unflatten)

N_BOOT = 200
DT = 0.00025
TAU_LO, TAU_HI = 0.02, 0.32


def stats(sp, idx=None):
    """(mean |pairwise rho|, D_eff at 20 ms, D_eff at 320 ms)."""
    s = sp if idx is None else sp[:, idx]
    _, rho, d_lo = corr_effdim(s, T_BEAT, K, "exp", TAU_LO)
    d_hi = corr_effdim(s, T_BEAT, K, "exp", TAU_HI)[2]
    return float(rho), float(d_lo), float(d_hi)


def main():
    sp_si, _, _ = load(DIM.path)
    targets = silicon_rates(sp_si)
    grid, _ = fit_lattice(isis(sp_si))

    with open("reservoir_input_proj.json") as f:
        proj = {int(c["neuron"]): c for c in json.load(f)["proj"]}
    X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(NB)]
           for k in range(NN)}
    up, dn = build_jump(flatten_events(evs), T_BEAT, DT, int(round(T_BEAT / DT)))

    conds = {
        "baseline": dict(jit=0.0),
        "JIT 20% (closes the scalar)": dict(jit=0.20),
        "JIT 50% (matches <|rho|>)": dict(jit=0.50),
    }
    models = {}
    for name, c in conds.items():
        vs = None
        if c["jit"]:
            vs = np.random.default_rng(900).normal(1.0, c["jit"], NN * NB).clip(0.15, None)
        kw = dict(dt=DT)
        vth, _ = bisect_to_rates(up, dn, targets, kw, vth_scale=vs)
        vth_u = np.repeat(vth, NB)
        if vs is not None:
            vth_u = vth_u * vs
        spk = simulate(up, dn, vth_u, **kw)
        models[name] = unflatten(spk, lattice=grid, rng=np.random.default_rng(100))

    r_si, lo_si, hi_si = stats(sp_si)
    print(f"{'condition':30s} {'<|rho|>':>9s} {'Deff@20ms':>11s} {'Deff@320ms':>12s}")
    print("-" * 66)
    print(f"{'SILICON':30s} {r_si:9.3f} {lo_si:11.2f} {hi_si:12.2f}")
    for name, sp in models.items():
        r, lo, hi = stats(sp)
        print(f"{name:30s} {r:9.3f} {lo:11.2f} {hi:12.2f}")

    rng = np.random.default_rng(0)
    out = {"silicon": {"rho": r_si, "deff20": lo_si, "deff320": hi_si}, "conditions": {}}
    print("\npaired bootstrap of (silicon - condition), 95% CI:")
    print(f"{'condition':30s} {'d<|rho|>':>18s} {'dDeff@20ms':>18s} {'dDeff@320ms':>18s}")
    print("-" * 88)
    for name, sp in models.items():
        d = {"rho": [], "d20": [], "d320": []}
        for _ in range(N_BOOT):
            idx = rng.integers(0, NB, NB)
            a = stats(sp_si, idx); b = stats(sp, idx)
            d["rho"].append(a[0] - b[0])
            d["d20"].append(a[1] - b[1])
            d["d320"].append(a[2] - b[2])
        row, cells = {}, []
        for key in ("rho", "d20", "d320"):
            v = np.array(d[key])
            lo_, hi_ = np.percentile(v, [2.5, 97.5])
            excl = "*" if (lo_ > 0 or hi_ < 0) else " "
            row[key] = {"mean": float(v.mean()), "ci95": [float(lo_), float(hi_)],
                        "excludes_zero": bool(lo_ > 0 or hi_ < 0)}
            cells.append(f"[{lo_:+.2f},{hi_:+.2f}]{excl}")
        out["conditions"][name] = row
        print(f"{name:30s} " + " ".join(f"{c:>18s}" for c in cells))
    print("\n* = 95% CI excludes zero, i.e. the model is distinguishable from "
          "silicon on that statistic.")

    with open("data/deff_identifiability.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/deff_identifiability.json")


if __name__ == "__main__":
    raise SystemExit(main())
