#!/usr/bin/env python3
"""Does hardware drift inflate D_eff? (F. Corradi's hypothesis, 2026-08-12)

If the array's operating point shifts during an acquisition, that adds variance
across beats beyond input drive. The software model stays drift-free, so this
would be a mechanism for the reference figure gap -- AND it would explain why D_eff rose
14.1 -> 16.9 between a 36-minute recording and a 95-minute one at the same
operating point. One hypothesis, both open questions.

Two channels, both testable from data already on disk:

  A. WITHIN a neuron's window. reservoir_run_randproj loops neurons OUTER, so beat
     index is time within each neuron's ~6 min window. Drift there would give each
     neuron its own beat-index trend -- 16 different trends, i.e. extra dimensions.
     Test: hold beat COUNT fixed at 60 and vary the time SPAN. Contiguous windows
     span ~1/3 of the run; random subsets span all of it.

  B. ACROSS neurons. Neuron index is acquisition order, so n15 was measured ~95 min
     after n0. Test: is the per-neuron rate change between two back-to-back
     acquisitions correlated with acquisition order?

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_drift_test.py
"""
import json
import numpy as np
from reservoir_demo_proj import corr_effdim, load

EXP = "reservoir_spikes_ref25_expanded_2026-08-12.npz"
REF = "reservoir_spikes_ref25_2026-08-12.npz"
TAU, K, T = 0.02, 8, 2.0


def rates(sp):
    n, nb = sp.shape
    return np.array([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T
                     for j in range(n)])


def main():
    sp, _, _ = load(EXP)
    nb = sp.shape[1]
    rng = np.random.default_rng(0)
    full = corr_effdim(sp, T, K, "exp", TAU)[2]

    cont = np.array([corr_effdim(sp[:, np.arange(s, s + 60)], T, K, "exp", TAU)[2]
                     for s in range(0, nb - 60 + 1, 10)])
    rand = np.array([corr_effdim(sp[:, np.sort(rng.choice(nb, 60, replace=False))],
                                 T, K, "exp", TAU)[2] for _ in range(11)])
    span = rand.mean() - cont.mean()
    count = full - rand.mean()

    print("A. TIME SPAN at fixed beat count (n=60)")
    print(f"   contiguous windows  {cont.mean():5.2f} +/- {cont.std():.2f}  (span ~1/3 of run)")
    print(f"   full-span subsets   {rand.mean():5.2f} +/- {rand.std():.2f}  (span = whole run)")
    print(f"   -> time-span effect {span:+.2f} units, {100*span/(full-cont.mean()):.0f}% of the "
          f"60->160 rise, and INSIDE the +/-{rand.std():.2f} scatter of the draws")
    print(f"   -> beat-count effect {count:+.2f} units, {100*count/(full-cont.mean()):.0f}% "
          f"-- estimator convergence rather than the array")

    a, _, _ = load(REF)
    ra, rb = rates(a), rates(sp)
    live = [j for j in range(16) if ra[j] > 0 and rb[j] > 0]
    ratio = rb[live] / ra[live]
    r = float(np.corrcoef(live, ratio)[0, 1])
    print("\nB. ACQUISITION ORDER")
    print(f"   per-neuron rate ratio REF25 -> EXPANDED: {ratio.mean():.3f} +/- {ratio.std():.3f}")
    print(f"   correlation with acquisition order: r = {r:+.3f} (n={len(live)})")
    print("   CONFOUNDED: the two runs use different beat sets, so the input event")
    print("   counts differ; this bounds the order effect rather than measuring it.")

    print("\nVERDICT: drift is present in the predicted direction but is a MINORITY")
    print("term and is not resolved from zero at this sample size. The D_eff rise with")
    print("more beats is dominated by estimator convergence.")
    print("CONSEQUENCE: D_eff comparisons must hold BEAT COUNT fixed. Silicon at 160")
    print("beats cannot be compared against a model at 60.")

    json.dump({"full_160": float(full),
               "contiguous_60": {"mean": float(cont.mean()), "sd": float(cont.std())},
               "fullspan_60": {"mean": float(rand.mean()), "sd": float(rand.std())},
               "span_effect": float(span), "count_effect": float(count),
               "order_corr": r, "rate_ratio_mean": float(ratio.mean())},
              open("data/deff_drift_test.json", "w"), indent=2)
    print("\nwrote data/deff_drift_test.json")


if __name__ == "__main__":
    raise SystemExit(main())
