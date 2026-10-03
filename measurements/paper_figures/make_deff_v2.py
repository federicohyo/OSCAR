#!/usr/bin/env python3
"""Fig. 11, regenerated on TWO silicon acquisitions instead of one.

The published figure carries a single silicon curve, recording DIM (2026-07-05),
taken with the flash-resident read-out and host-arrival timestamps. Section 4.3
later established that every inter-event interval in that recording lies on an
11.99 ms acquisition lattice with a per-presentation phase, and that applying the
same lattice to a software neuron carries 2.4 of the 4.1 rate-matched D_eff units
the decomposition was trying to explain.

The 2026-08-11 re-acquisition uses the fixed read-out (SRAM-resident drain, 21-bit
on-chip Timer0 timestamps). reservoir_acq_compare.py confirms the lattice is absent
from it: 0% of intervals fall on integer multiples (against 100%), per-trial phase
concentration 0.265 (against 0.998), and the shortest ISI now varies 1.2-7.5 ms
across neurons instead of sitting at a uniform 23.97 ms.

Plotting both is the honest presentation: it shows the reader what the acquisition
was worth, and it converts the manuscript's "single acquisition" limitation into a
measurement.

CAVEAT CARRIED INTO THE CAPTION: the two acquisitions differ in read-out path AND
in drive (old 1.8-15.4 Hz, new 10.8-68.0 Hz), and D_eff falls with rate in this
pipeline, so the 18.1 -> 14.9 difference is NOT attributable to the lattice alone.

  ./.venv-meas/bin/python3 measurements/paper_figures/make_deff_v2.py
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", ".."))
sys.path.insert(0, REPO)
os.chdir(REPO)

from reservoir_demo_proj import corr_effdim, load

matplotlib.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
})

HERE = os.path.dirname(os.path.abspath(__file__))
K = 8
TAUS = np.array([0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
TAU_TABLE = 0.02

CURVES = [
    ("Silicon, 2026-07 (flash read-out, 11.99 ms lattice)",
     "reservoir_spikes_nv_randproj.npz", "#c0392b", "o--", 1.6),
    ("Silicon, 2026-08 (SRAM read-out, no lattice)",
     "reservoir_spikes_nv_randproj_aug11.npz", "#c0392b", "o-", 2.1),
    ("SW LIF, heterogeneous $\\tau$+$V_{th}$+$w$, + projection",
     "sw_proj_allparam_mm0.65.npz", "#e8880c", "^-", 1.3),
    ("SW LIF, heterogeneous $\\tau$ only, + projection",
     "sw_proj_tauonly_mm0.65.npz", "#6741d9", "v-", 1.3),
    ("SW LIF, identical, + projection", "sw_proj.npz", "#0b7285", "s-", 1.3),
    ("SW LIF, identical, shared input", "sw_shared.npz", "0.55", ":", 1.2),
]


def main():
    fig, ax = plt.subplots(figsize=(3.9, 2.9))
    out = {}
    for label, npz, color, mk, lw in CURVES:
        if not os.path.exists(npz):
            print(f"  SKIP (missing) {npz}")
            continue
        sp, _, T = load(npz)
        eds = [corr_effdim(sp, T, K, "exp", t)[2] for t in TAUS]
        rho = corr_effdim(sp, T, K, "exp", TAU_TABLE)[1]
        n, nb = sp.shape
        rate = np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T
                        for j in range(n)])
        ax.plot(TAUS * 1000, eds, mk, color=color, lw=lw, ms=3.4, label=label)
        out[label] = {"npz": npz, "deff": eds, "deff20": eds[1],
                      "rho": float(rho), "mean_rate_hz": float(rate)}
        print(f"{label:52s} tau=20ms D_eff={eds[1]:5.1f}  <|rho|>={rho:.3f}  "
              f"rate={rate:.1f} Hz")

    ax.set_xscale("log")
    ax.set_xticks(TAUS * 1000)
    ax.set_xticklabels([f"{t*1000:.0f}" for t in TAUS])
    ax.set_xlabel("read-out kernel $\\tau$ (ms)")
    ax.set_ylabel("effective dimensionality $D_{\\mathrm{eff}}$")
    ax.legend(fontsize=5.6, loc="upper right", frameon=False, labelspacing=0.32)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        p = os.path.join(HERE, f"deff_decomp_v2.{ext}")
        fig.savefig(p, dpi=300)
        print("wrote", p)
    with open(os.path.join(REPO, "results", "deff_decomp_v2.json"), "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    raise SystemExit(main())
