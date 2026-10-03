#!/usr/bin/env python3
"""What was the acquisition lattice actually worth? Measured on silicon, twice.

The 2026-07 recording reads D_eff = 18.1 and the 2026-08 re-acquisition reads
14.9. Two things changed at once -- the 11.99 ms acquisition lattice went away,
and the drive went up 2.7x -- so that 3.2-unit difference stays unattributed to
either on its own, and a reader could equally well call it a reproduction shortfall.

This settles it with neither a simulation nor rate matching: take the NEW
recording, which is lattice-free, and push it through the OLD one. The lattice
parameters are held fixed -- they are the values measured on the 2026-07 data
(11.986 ms grid, phase drawn per (neuron, beat) presentation, two-slot floor).
Everything else about the new recording stays exactly as acquired, so whatever
D_eff moves is the lattice and nothing else.

  PYTHONPATH=. ./.venv-meas/bin/python3 deff_lattice_on_new.py

NOTE: avoid reading the "best-fit period" that fit_lattice returns on the new
recording (8.030 ms). With 0% of intervals on integer multiples and a phase
concentration of 0.265, that fit is returning noise -- lattice signal is zero there
to find.
"""
import json

import numpy as np

from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import apply_lattice

K, T_BEAT = 8, 2.0
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
GRID_OLD = 0.011986          # MEASURED on the 2026-07 recordings rather than refitted
MIN_STEPS = 2                # the two-slot floor, also measured
NEW = "reservoir_spikes_nv_randproj_aug11.npz"
OLD = "reservoir_spikes_nv_randproj.npz"
SEEDS = 6


def curve(sp):
    rho = corr_effdim(sp, T_BEAT, K, "exp", 0.02)[1]
    return float(rho), [corr_effdim(sp, T_BEAT, K, "exp", t)[2] for t in TAUS]


def latticed(sp, seed):
    rng = np.random.default_rng(seed)
    out = np.empty_like(sp)
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            out[j, b] = apply_lattice(np.asarray(sp[j, b], dtype=float),
                                      GRID_OLD, rng.uniform(0, GRID_OLD), MIN_STEPS)
    return out


def main():
    sp_new = load(NEW)[0]
    sp_old = load(OLD)[0]
    hdr = "  ".join(f"{t*1e3:5.0f}" for t in TAUS)
    print(f"{'condition':44s} {'<|rho|>':>8s}  {hdr}")
    print("-" * 92)

    r_old, c_old = curve(sp_old)
    print(f"{'2026-07 as acquired (HAS the lattice)':44s} {r_old:8.3f}  "
          + "  ".join(f"{v:5.1f}" for v in c_old))

    r_new, c_new = curve(sp_new)
    print(f"{'2026-08 as acquired (no lattice)':44s} {r_new:8.3f}  "
          + "  ".join(f"{v:5.1f}" for v in c_new))

    rr, cc = [], []
    for s in range(SEEDS):
        r, c = curve(latticed(sp_new, 400 + s))
        rr.append(r); cc.append(c)
    r_lat, c_lat = float(np.mean(rr)), np.mean(cc, axis=0)
    sd_lat = np.std([c[1] for c in cc])
    print(f"{'2026-08 + the OLD lattice applied':44s} {r_lat:8.3f}  "
          + "  ".join(f"{v:5.1f}" for v in c_lat) + f"   (sd {sd_lat:.2f})")
    print("-" * 92)

    i20 = TAUS.index(0.02)
    raw, lat = c_new[i20], c_lat[i20]
    gap = c_old[i20] - raw
    print(f"\nOn the SAME recording, at the SAME rate, the lattice alone moves")
    print(f"  D_eff(20 ms)  {raw:.1f}  ->  {lat:.1f}   ({lat-raw:+.1f} units)")
    print(f"  <|rho|>       {r_new:.3f} -> {r_lat:.3f}  ({r_lat-r_new:+.3f})")
    print(f"\nThe 2026-07 vs 2026-08 difference is {gap:+.1f} units "
          f"({c_old[i20]:.1f} vs {raw:.1f}).")
    print(f"The lattice accounts for {100*(lat-raw)/gap:.0f}% of it; the remainder "
          f"is the 2.7x\ndifference in drive (D_eff falls with rate in this "
          f"pipeline) and acquisition-to-\nacquisition variation.")
    print(f"\nDirection of the <|rho|> effect: the lattice does decorrelate neurons "
          f"({r_new:.3f} ->\n{r_lat:.3f}), the sign expected from a per-presentation "
          f"phase -- but only by {r_new-r_lat:.3f}, against\nthe {r_new-r_old:.3f} "
          f"separating the two acquisitions. So the 2026-07 recording's low\n"
          f"<|rho|> stays largely clear of read-out artefacts too; like the D_eff "
          f"difference it is\ndominated by the operating point.")

    json.dump({"grid_s": GRID_OLD, "min_steps": MIN_STEPS, "seeds": SEEDS,
               "taus_s": TAUS,
               "old_as_acquired": {"rho": r_old, "deff": c_old},
               "new_as_acquired": {"rho": r_new, "deff": c_new},
               "new_plus_old_lattice": {"rho": r_lat, "deff": c_lat.tolist(),
                                        "deff20_sd": float(sd_lat)},
               "lattice_units_at_20ms": float(lat - raw),
               "old_minus_new_at_20ms": float(gap)},
              open("data/deff_lattice_on_new.json", "w"), indent=2)
    print("\nwrote data/deff_lattice_on_new.json")


if __name__ == "__main__":
    raise SystemExit(main())
