#!/usr/bin/env python3
"""What does D_eff actually measure here? Two controls that pin its meaning.

CONTROL 1 -- the ceiling. Poisson trains with zero structure, at silicon's own
per-neuron rates, score D_eff ~68.9, and flat across 4.6-45.5 Hz. So D_eff is
maximised by NOISE rather than by richness: it measures decorrelation, and perfect
decorrelation is useless. Silicon's 16.91 and the model's 9.95 are both far below the
ceiling, and "higher is better" needs care on an axis whose maximum is noise.
The flatness also clears the estimator: sparsity at low rate leaves it un-inflated.

CONTROL 2 -- the noise floor. Present the SAME beat 51 times and every dimension the
covariance finds is trial-to-trial variability, because the stimulus stays fixed.
That reads D_eff ~19-20, against 16.91 measured across 160 DIFFERENT beats.

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_noise_ceiling.py

The second control is the one that bites: the array's trial-to-trial noise occupies as
many effective dimensions as its stimulus-driven response does. On this task D_eff
therefore stays out of stimulus-driven richness -- which also explains, with
no further mechanism, why it stayed unlinked to accuracy.

CAVEATS, and they are why this remains a preliminary analysis claim:
  * the repeat runs are at DIFFERENT bias sets from REF25 (43.7 and 32.1 Hz against
    35.6), so this is rate-comparable but not operating-point matched;
  * 51 trials against 160 beats, and D_eff grows with sample count (+2.2 units from
    60 to 160 here), so the noise figure is if anything UNDERSTATED at 51 -- which
    works against the comparison.
The decisive version is ~50 repeats of one beat at the REF25 operating point, about
27 minutes of bench time, which would allow the proper split
D_eff(signal) = PR(C_total - C_noise).
"""
import json
import numpy as np
from reservoir_demo_proj import corr_effdim, load

T, K, TAU = 2.0, 8, 0.02
REPEATS = ["repeatability_spikes.npz", "repeatability_feedproj.npz"]
TOTAL = "reservoir_spikes_ref25_expanded_2026-08-12.npz"


def rates(sp):
    n, m = sp.shape
    return np.array([sum(len(np.asarray(sp[j, b])) for b in range(m)) / m / T
                     for j in range(n)])


def poisson_like(r, m, seed):
    rng = np.random.default_rng(seed)
    sp = np.empty((len(r), m), dtype=object)
    for j, rj in enumerate(r):
        for b in range(m):
            sp[j, b] = np.sort(rng.random(rng.poisson(rj * T)) * T)
    return sp


def main():
    sp, _, _ = load(TOTAL)
    per = rates(sp)
    total = corr_effdim(sp, T, K, "exp", TAU)[2]
    out = {"total_deff": float(total), "total_rate": float(per.mean()),
           "n_beats": int(sp.shape[1])}

    print("CEILING -- structureless Poisson at silicon's rates, scaled")
    ceil = {}
    for s in (1.0, 0.55, 0.23, 0.13):
        d = float(np.mean([corr_effdim(poisson_like(per * s, sp.shape[1], k),
                                       T, K, "exp", TAU)[2] for k in range(3)]))
        ceil[f"{(per*s).mean():.1f}"] = d
        print(f"   {(per*s).mean():5.1f} Hz -> D_eff {d:6.2f}")
    out["ceiling"] = ceil

    print("\nFLOOR -- same beat repeated, so all variance is trial noise")
    fl = {}
    for p in REPEATS:
        d = np.load(p, allow_pickle=True)
        r = rates(d["spikes"])
        dn = corr_effdim(d["spikes"], T, K, "exp", TAU)[2]
        fl[p] = {"deff": float(dn), "rate": float(r.mean()),
                 "trials": int(d["spikes"].shape[1])}
        print(f"   {p:30s} {r.mean():5.1f} Hz -> NOISE D_eff {dn:6.2f} "
              f"({d['spikes'].shape[1]} trials)")
    out["floor"] = fl

    nf = np.mean([v["deff"] for v in fl.values()])
    print(f"\n   ceiling (noise, all dims)   ~{ceil[list(ceil)[0]]:.1f}")
    print(f"   NOISE FLOOR (same stimulus) ~{nf:.1f}")
    print(f"   silicon, 160 diff. beats     {total:.2f}   <-- AT OR BELOW the noise floor")
    print(f"   software model, matched      9.95")
    json.dump(out, open("data/deff_noise_ceiling.json", "w"), indent=2)
    print("\nwrote data/deff_noise_ceiling.json")


if __name__ == "__main__":
    raise SystemExit(main())
