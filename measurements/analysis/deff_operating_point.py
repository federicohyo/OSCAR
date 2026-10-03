#!/usr/bin/env python3
"""Task G: does operating-point dispersion explain the D_eff gap?

PREMISE TEST FIRST. The brief proposed matching the SILENCING FRACTION ("5/16
silent on these beats"). That handle does not exist: no recording in this repo has
a silent neuron. On the dataset Table 4 is computed from
(reservoir_spikes_nv_randproj.npz) all 16 neurons are active, the quietest at
3.62 spikes/beat. The same holds for the N/S/V structured recording (min 2.93)
and the N/PVC delta recording (min 0.86, one neuron below 1/beat). So the
interpretive note that "silicon's 18.1 is carried by eleven active neurons" is
also wrong -- it is carried by all sixteen.

The MECHANISM behind the brief's hypothesis survives that, and is worth testing on
its own terms. Silicon's per-neuron rates are strongly bimodal:

    3.6 5.1 6.2 8.4 8.8 9.9 | 17.8 21.9 22.1 23.0 23.3 24.0 24.6 25.1 27.3 30.9

-- six neurons in a low-rate cluster and ten in a high-rate cluster, an 8.5x
range. That is neurons sitting at genuinely different points on the f-I curve, not
a symmetric scatter around one operating point, which is what a Gaussian on tau
and V_th produces. So the right handle is the RATE DISTRIBUTION, matched by
quantile, not a dispersion statistic and not a silencing fraction.

Method: bisect each SW neuron's threshold so that, in rank order, its mean output
rate matches the corresponding silicon neuron's. Threshold is monotone in rate
over the whole range, so every target is reachable (unlike tau -- see round 2).
Then recompute D_eff and <|rho|> through the unchanged corr_effdim.

PROVENANCE:
  MEASURED   per-neuron mean output rate of the array (reservoir_spikes_nv_randproj.npz)
  DERIVED    per-neuron threshold, bisected to reproduce that rate
  SIMULATED  tau and weight uniform; the projection is the same one the array got
"""
import json

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from reservoir_datasets import DIM        # this analysis is recording DIM only
from reservoir_sw_lif import sim_lif

K = 8
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
T_BEAT = 2.0
TAU_M, TREF, W_EXC, W_INH = 0.02, 0.005, 0.34, 0.34
VTH_LO, VTH_HI = 0.02, 40.0


def per_neuron_rates(sp):
    n, nb = sp.shape
    return np.array([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb
                     for j in range(n)])


def sim_neuron(evs, vth):
    return [sim_lif(ev, T_BEAT, TAU_M, vth, 0.0, TREF, W_EXC, W_INH) for ev in evs]


def rate_at(evs, vth):
    return np.mean([len(s) for s in sim_neuron(evs, vth)])


def bisect_vth(evs, target, iters=20):
    lo, hi = VTH_LO, VTH_HI
    r_lo, r_hi = rate_at(evs, lo), rate_at(evs, hi)
    if not (min(r_lo, r_hi) <= target <= max(r_lo, r_hi)):
        best = lo if abs(r_lo - target) < abs(r_hi - target) else hi
        return best, (r_lo if best == lo else r_hi), False
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        r = rate_at(evs, mid)
        if (r < target) == (r_lo < target):
            lo, r_lo = mid, r
        else:
            hi, r_hi = mid, r
    v = 0.5 * (lo + hi)
    return v, rate_at(evs, v), True


def main():
    hw_sp, _, T = load(DIM.path)
    tgt = np.sort(per_neuron_rates(hw_sp))[::-1]          # MEASURED, rank-ordered
    print("MEASURED silicon per-neuron rate (spk/beat), sorted:")
    print("  " + " ".join(f"{v:.1f}" for v in tgt))
    print(f"  range {tgt.min():.1f}-{tgt.max():.1f} ({tgt.max()/tgt.min():.1f}x), "
          f"CV {tgt.std()/tgt.mean():.3f}, silent {int((tgt==0).sum())}/16\n")

    proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
    b = np.load("beats_nv60_orig.npz", allow_pickle=True)
    X, y, recs = b["X"], b["y"], b["records"]

    # per-neuron event streams, identical to what sw_proj.npz used
    evs = {}
    for k in range(16):
        p = proj[k]
        evs[k] = [delta_encode_proj(X[i], sigma=p["sigma"], shift=p["shift"],
                                    theta=p["theta"]) for i in range(len(X))]

    # rank-match: neuron with the most drive gets the highest target
    base = np.array([rate_at(evs[k], 1.0) for k in range(16)])
    order = np.argsort(base)[::-1]
    vths, ach, ok = np.zeros(16), np.zeros(16), []
    print("quantile-matching thresholds to the measured rate distribution:")
    for rank, k in enumerate(order):
        v, r, good = bisect_vth(evs[k], tgt[rank])
        vths[k], ach[k] = v, r
        ok.append(good)
        print(f"  n{k:02d} target {tgt[rank]:5.1f} -> vth {v:7.3f}  achieved {r:5.1f}"
              + ("" if good else "   [unreachable]"))

    print(f"\nachieved rate CV {ach.std()/ach.mean():.3f} vs measured "
          f"{tgt.std()/tgt.mean():.3f}   (reachable {sum(ok)}/16)")

    sp = np.empty((16, len(X)), dtype=object)
    for k in range(16):
        for i, s in enumerate(sim_neuron(evs[k], vths[k])):
            sp[k, i] = s
    np.savez("sw_proj_opdispersion.npz", spikes=sp, labels=y, records=recs,
             neurons=np.arange(16), T=T_BEAT, coding="swlif_opmatched",
             classes="NV", vths=vths, target_rates=tgt, achieved_rates=ach)

    print("\n=== D_eff / <|rho|> at tau = 20 ms, and the tau sweep ===")
    rows = [("SW LIF identical, +proj", "sw_proj.npz"),
            ("SW LIF het. tau+Vth+w 65%", "sw_proj_allparam_mm0.65.npz"),
            ("SW LIF operating-point matched", "sw_proj_opdispersion.npz"),
            ("SILICON", DIM.path)]
    hdr = "  ".join(f"{t*1e3:5.0f}" for t in TAUS)
    print(f"{'condition':34s} {'<|rho|>':>8s}  {hdr}")
    out = {}
    for nm, f in rows:
        s, _, TT = load(f)
        _, rho, _ = corr_effdim(s, TT, K, "exp", 0.02)
        c = [float(corr_effdim(s, TT, K, "exp", t)[2]) for t in TAUS]
        out[nm] = {"rho": rho, "deff": c}
        print(f"{nm:34s} {rho:8.2f}  " + "  ".join(f"{v:5.1f}" for v in c))
    json.dump(out, open("data/deff_operating_point.json", "w"), indent=2)
    i20 = TAUS.index(0.02)
    b0 = out["SW LIF identical, +proj"]["deff"][i20]
    bm = out["SW LIF operating-point matched"]["deff"][i20]
    si = out["SILICON"]["deff"][i20]
    print(f"\nAt tau=20 ms: identical {b0:.1f} -> op-matched {bm:.1f} | silicon {si:.1f}")
    print(f"  operating-point dispersion carries {100*(bm-b0)/(si-b0):+.0f}% of the gap")


if __name__ == "__main__":
    raise SystemExit(main())
