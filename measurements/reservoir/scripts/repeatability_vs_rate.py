#!/usr/bin/env python3
"""Separate counting noise from COHERENT excitability jitter, without matching rates.

The first repeatability run was criticised, correctly, for sitting at a higher
firing rate than the DIM recording it is meant to inform. Matching the rate turned
out to lie beyond the available knobs (the weight word is a cliff rather than
a dial -- see bench/deff_residual_mechanisms.md), so this analysis removes the
need to match it.

THE IDEA. The two candidate sources of trial-to-trial spread scale differently
with the mean count N:

    counting statistics       var = F * N          (CV = sqrt(F/N), falls with N)
    coherent excitability     var = (c*N)^2        (CV = c,         flat in N)

A per-trial threshold/gain wobble multiplies the whole trial's response together,
so its standard deviation grows in PROPORTION to N; spike-counting noise grows
only as sqrt(N). Fitting

    var(N) = F * N + c^2 * N^2

to the 16 neurons -- which span a 6.7x range of rate at one operating point --
therefore separates them, and returns `c`, the coherent fractional jitter, as a
number that does NOT depend on which rate the array happens to sit at.

`c` is exactly the quantity the D_eff simulation needs: data/jitter_to_countcv
.json says the model requires a coherent count CV of 25-35% to close the residual.
If the fitted c is far below that, the jitter explanation is ruled out at every rate, and
the operating-point objection to the bench run is answered rather than dodged.

  PYTHONPATH=. ./.venv-meas/bin/python3 repeatability_vs_rate.py [npz]
"""
import json
import sys

import numpy as np

T_BEAT = 2.0
DIM_HZ = np.array([4.93, 3.11, 11.64, 15.43, 2.56, 1.82, 12.53, 4.36,
                   11.13, 8.86, 12.28, 11.51, 3.06, 12.02, 4.44, 8.03])


def fit_var(N, V):
    """Least squares for var = F*N + c^2*N^2, with F,c^2 >= 0."""
    A = np.stack([N, N ** 2], axis=1)
    sol, *_ = np.linalg.lstsq(A, V, rcond=None)
    F, q = float(sol[0]), float(sol[1])
    return max(F, 0.0), np.sqrt(max(q, 0.0))


def main(path="repeatability_feedproj.npz"):
    d = np.load(path, allow_pickle=True)
    sp, ntr = d["spikes"], int(d["trials"])
    neurons = [int(k) for k in d["neurons"]]
    print(f"{path}: {len(neurons)} neurons x {ntr-1} scored trials, "
          f"{int(d['clk_mhz'])} MHz, w={int(d['weight'])}")
    print(f"bias: {str(d['bias_pattern']).split('/')[-1]}\n")

    N, V, rows = [], [], []
    print(f"{'neuron':>6s} {'mean N':>8s} {'sd':>7s} {'CV':>7s} {'Fano':>7s} {'Hz':>7s}")
    for k in neurons:
        c = np.array([len(np.asarray(sp[k, t])) for t in range(1, ntr)], float)
        if c.mean() <= 0:
            print(f"{k:6d} {'silent':>8s}")
            continue
        m, v = c.mean(), c.var(ddof=1)
        N.append(m); V.append(v)
        rows.append((k, m, np.sqrt(v), np.sqrt(v) / m, v / m))
        print(f"{k:6d} {m:8.1f} {np.sqrt(v):7.2f} {np.sqrt(v)/m*100:6.1f}% "
              f"{v/m:7.2f} {m/T_BEAT:7.1f}")
    N, V = np.array(N), np.array(V)

    F, c = fit_var(N, V)
    print(f"\nfit  var = F*N + (c*N)^2   over {len(N)} neurons spanning "
          f"N = {N.min():.0f}-{N.max():.0f} ({N.max()/N.min():.1f}x)")
    print(f"  F (Fano, counting term)      = {F:.2f}")
    print(f"  c (coherent jitter fraction) = {c*100:.1f}%")

    # bootstrap over neurons
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(N), len(N))
        bs.append(fit_var(N[i], V[i]))
    bs = np.array(bs)
    flo, fhi = np.percentile(bs[:, 0], [2.5, 97.5])
    clo, chi = np.percentile(bs[:, 1], [2.5, 97.5])
    print(f"  bootstrap 95% CI: F [{flo:.2f}, {fhi:.2f}]   "
          f"c [{clo*100:.1f}%, {chi*100:.1f}%]")

    # what the D_eff simulation demands
    try:
        need = json.load(open("data/jitter_to_countcv.json"))
        need_min = min(need.values())
        print(f"\nthe D_eff residual needs a COHERENT count CV of "
              f"{need_min*100:.0f}-35% (data/jitter_to_countcv.json)")
        verdict = "SUPPORTED" if clo > need_min else "NOT SUPPORTED"
        print(f"  measured coherent term c = {c*100:.1f}% "
              f"(upper 95% bound {chi*100:.1f}%)  ->  {verdict}")
    except FileNotFoundError:
        pass

    # counting-only prediction at DIM's counts, for reference
    dim_n = DIM_HZ * T_BEAT
    pred = np.sqrt(F / dim_n + c ** 2)
    print(f"\npredicted count CV at DIM's own rates (1.8-15.4 Hz): "
          f"{pred.min()*100:.0f}-{pred.max()*100:.0f}% "
          f"(median {np.median(pred)*100:.0f}%)")
    print("  -- of which the COHERENT part is the rate-independent "
          f"{c*100:.1f}%; the rest is counting noise, which the simulation "
          "showed\n     does not close the residual at any magnitude.")

    json.dump({"path": path, "F": F, "c": c,
               "F_ci95": [float(flo), float(fhi)],
               "c_ci95": [float(clo), float(chi)],
               "per_neuron": [{"neuron": int(r[0]), "mean": r[1], "sd": r[2],
                               "cv": r[3], "fano": r[4]} for r in rows],
               "pred_cv_at_dim_rates": pred.tolist()},
              open("data/repeatability_vs_rate.json", "w"), indent=2)
    print("\nwrote data/repeatability_vs_rate.json")


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
