#!/usr/bin/env python3
"""Put the MEASURED trial-to-trial variability on the simulation's axis.

repeatability_run.py measures the CV of the spike COUNT across 50 repeats of one
beat. deff_physical_mechanisms.py sweeps a THRESHOLD jitter. Those are different
quantities, so the bench number is compared with the sweep through a bridge. This
script converts: for each threshold jitter it reports the count CV that jitter
induces, so the measurement can be placed on the sweep and the residual it
actually closes can be read off.

Measuring the induced CV by repeating one beat falls short at this operating
point -- the model sits at DIM's 1.8-15.4 Hz, and the beat the bench repeated
carries 92 UP against 92 DOWN events, which nearly cancel and evoke nothing.
Instead the same 60 beats are presented twice under two INDEPENDENT jitter draws:
for a given beat the signal is identical in both, so var(A-B) = 2*var_jitter
isolates the jitter, so model and bench can work at different operating points.

  PYTHONPATH=. ./.venv-meas/bin/python3 repeatability_vs_sim.py

KNOWN ISSUE: the multi-seed sweep in main() is unstable -- the second and third
bisection of an identical configuration collapse to the lower bound, which every
component reproduces correctly in isolation and which remains under diagnosis. The
numbers reported in bench/deff_residual_mechanisms.md therefore come from the
single-bisection path (induced_cv against one operating point, data/
jitter_to_countcv.json) and from the already-validated JIT rows of
deff_physical_mechanisms.py. Hold main()'s table until this is fixed.
"""
import json

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_datasets import DIM
from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import fit_lattice, isis
from deff_physical_sim import build_jump, simulate
from deff_physical_mechanisms import (NN, NB, T_BEAT, K, bisect_to_rates,
                                      flatten_events, silicon_rates, unflatten)

DT = 0.00025
JITTERS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.35]
NSEED = 3


def measured():
    d = np.load("repeatability_spikes.npz", allow_pickle=True)
    sp, ntr = d["spikes"], int(d["trials"])
    neurons = [int(k) for k in d["neurons"]]
    print("MEASURED -- one beat repeated 50x, 25 MHz, base biases")
    print(f"{'neuron':>6s} {'mean':>8s} {'CV':>7s} {'Fano':>7s} {'Hz':>7s}")
    cvs, fanos = [], []
    for k in neurons:
        c = np.array([len(np.asarray(sp[k, t])) for t in range(1, ntr)], float)
        if c.mean() <= 0:
            continue
        cvs.append(c.std(ddof=1) / c.mean())
        fanos.append(c.var(ddof=1) / c.mean())
        print(f"{k:6d} {c.mean():8.1f} {cvs[-1]*100:6.1f}% {fanos[-1]:7.2f} "
              f"{c.mean()/T_BEAT:7.1f}")
    cvs, fanos = np.array(cvs), np.array(fanos)
    print(f"median count CV {np.median(cvs)*100:.1f}%  median Fano "
          f"{np.median(fanos):.2f}  (Fano<1 = sub-Poisson, MORE repeatable "
          f"than Poisson)")
    return float(np.median(cvs)), float(np.median(fanos))


def induced_cv(up, dn, vth, jz, seed):
    rng = np.random.default_rng(seed)
    got = []
    for _ in range(2):
        vu = np.repeat(vth, NB)
        if jz > 0:
            vu = vu * rng.normal(1.0, jz, NN * NB).clip(0.15, None)
        spk = simulate(up, dn, vu, dt=DT)
        got.append(np.array([[len(spk[k * NB + b]) for b in range(NB)]
                             for k in range(NN)], float))
    a, b = got
    out = []
    for k in range(NN):
        m = 0.5 * (a[k] + b[k])
        if m.mean() > 0:
            out.append(np.sqrt(np.mean((a[k] - b[k]) ** 2) / 2.0) / m.mean())
    return float(np.median(out)) if out else float("nan")


def main():
    med_cv, med_fano = measured()

    sp_si = load(DIM.path)[0]
    targets = silicon_rates(sp_si)
    grid = fit_lattice(isis(sp_si))[0]
    rho_si = corr_effdim(sp_si, T_BEAT, K, "exp", 0.02)[1]
    d20_si = corr_effdim(sp_si, T_BEAT, K, "exp", 0.02)[2]
    d320_si = corr_effdim(sp_si, T_BEAT, K, "exp", 0.32)[2]

    with open("reservoir_input_proj.json") as f:
        proj = {int(c["neuron"]): c for c in json.load(f)["proj"]}
    X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"],
                                 shift=proj[k]["shift"], theta=proj[k]["theta"])
               for i in range(NB)] for k in range(NN)}
    up, dn = build_jump(flatten_events(evs), T_BEAT, DT, int(round(T_BEAT / DT)))

    print(f"\n{'thr jitter':>11s} {'count CV':>9s} {'<|rho|>':>9s} "
          f"{'Deff@20':>8s} {'Deff@320':>9s} {'residual':>9s}")
    rows = []
    for jz in JITTERS:
        cv_l, rho_l, d20_l, d320_l = [], [], [], []
        for s in range(NSEED):
            vs = (np.random.default_rng(900 + s).normal(1.0, jz, NN * NB)
                  .clip(0.15, None)) if jz > 0 else None
            vth = bisect_to_rates(up, dn, targets, dict(dt=DT), vth_scale=vs)[0]
            vu = np.repeat(vth, NB) * (vs if vs is not None else 1.0)
            spm = unflatten(simulate(up, dn, vu, dt=DT), lattice=grid,
                            rng=np.random.default_rng(100 + s))
            cv_l.append(induced_cv(up, dn, vth, jz, 1300 + s))
            rho_l.append(corr_effdim(spm, T_BEAT, K, "exp", 0.02)[1])
            d20_l.append(corr_effdim(spm, T_BEAT, K, "exp", 0.02)[2])
            d320_l.append(corr_effdim(spm, T_BEAT, K, "exp", 0.32)[2])
        row = (jz, float(np.mean(cv_l)), float(np.mean(rho_l)),
               float(np.mean(d20_l)), float(np.mean(d320_l)))
        rows.append(row)
        print(f"{jz*100:10.0f}% {row[1]*100:8.1f}% {row[2]:9.3f} {row[3]:8.2f} "
              f"{row[4]:9.2f} {d20_si-row[3]:+9.2f}")
    print(f"{'SILICON':>11s} {med_cv*100:8.1f}%*{rho_si:9.3f} {d20_si:8.2f} "
          f"{d320_si:9.2f} {0.0:+9.2f}")
    print("  * bench ran at 25 MHz / 15-98 Hz; the model sits at DIM's 10 MHz /")
    print("    1.8-15.4 Hz. CV generally falls with rate, so the measured value")
    print("    is a LOWER bound on what DIM's quieter neurons would show.")

    cv = np.array([r[1] for r in rows])
    jzs = np.array([r[0] for r in rows])
    res = np.array([d20_si - r[3] for r in rows])
    if np.all(np.diff(cv) > 0):
        jz_at = float(np.interp(med_cv, cv, jzs))
        res_at = float(np.interp(med_cv, cv, res))
        print(f"\nAt the measured {med_cv*100:.1f}% count CV the model needs "
              f"{jz_at*100:.0f}% threshold jitter,")
        print(f"leaving {res_at:+.2f} of the {res[0]:+.2f} residual "
              f"({100*(res[0]-res_at)/res[0]:.0f}% closed).")
    else:
        jz_at = res_at = float("nan")
        print("\ncount CV not monotone in jitter -- not interpolating")

    json.dump({"measured_count_cv": med_cv, "measured_fano": med_fano,
               "jitter_at_measured_cv": jz_at, "residual_at_measured_cv": res_at,
               "sim": [{"jitter": r[0], "count_cv": r[1], "rho": r[2],
                        "deff20": r[3], "deff320": r[4]} for r in rows],
               "silicon": {"rho": float(rho_si), "deff20": float(d20_si),
                           "deff320": float(d320_si)}},
              open("data/repeatability_vs_sim.json", "w"), indent=2)
    print("\nwrote data/repeatability_vs_sim.json")


if __name__ == "__main__":
    raise SystemExit(main())
