#!/usr/bin/env python3
"""Regenerate deff_decomp.pdf (Fig. 11) for the MICPRO manuscript.

Task 2 of the pre-submission fix list. The published figure decomposed the
dimensionality expansion as shared-input -> per-neuron projection -> "mismatch",
where the last step was the contrast between *simulated identical software LIF*
and *silicon*. That contrast attributes to mismatch everything that differs
between the two substrates, not just parameter spread.

This version adds the tight control the claim needs: the same software LIF with
HETEROGENEOUS parameters, run through the identical feature pipeline (same
per-neuron input projection, same exponential read-out kernel, 16 neurons x K=8
kernel sample points = 128 dimensions). Two spreads are shown:

  * tau only, 65% relative spread -- isolates heterogeneous membrane time
    constants, the mechanism the manuscript names;
  * tau + threshold + weight, 65% -- the most generous parameter-mismatch model
    we can give the software LIF.

65% is the measured coefficient of variation of the per-neuron firing rate on
this die (newchipexploration/chipparams.py: RATE_CV, from the measured per-neuron
rates). The 15% variants used elsewhere in the repo are also computed by
constants-free re-run; see data/deff_tau_controls.json.

Reuses corr_effdim/load from reservoir_demo_proj -- the SAME implementation the
hardware row uses, not a reimplementation.

Run from the repo root:  python3 measurements/paper_figures/make_deff.py
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# the npz files and the shared D_eff implementation live at the repo root
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
TAU_TABLE = 0.02          # the tau Table 4 tabulates

CURVES = [
    # recording DIM (../../../reservoir_datasets.py) -- NOT the accuracy recording
    ("Silicon array, + projection", "reservoir_spikes_nv_randproj.npz", "#c0392b", "o-", 1.9),
    ("SW LIF, heterogeneous $\\tau$+$V_{th}$+$w$, + projection",
     "sw_proj_allparam_mm0.65.npz", "#e8880c", "^-", 1.4),
    ("SW LIF, heterogeneous $\\tau$ only, + projection",
     "sw_proj_tauonly_mm0.65.npz", "#6741d9", "v-", 1.4),
    ("SW LIF, identical, + projection", "sw_proj.npz", "#0b7285", "s-", 1.4),
    ("SW LIF, identical, shared input", "sw_shared.npz", "0.55", ":", 1.2),
]


def main():
    fig, ax = plt.subplots(figsize=(3.6, 2.75))
    vals = {}
    for label, npz, color, mk, lw in CURVES:
        sp, _, T = load(npz)
        eds = [corr_effdim(sp, T, K, "exp", t)[2] for t in TAUS]
        vals[label] = eds
        ax.plot(TAUS * 1000, eds, mk, color=color, lw=lw, ms=3.4, label=label)
        at20 = corr_effdim(sp, T, K, "exp", TAU_TABLE)[2]
        print(f"{label:52s} tau=20ms  D_eff={at20:5.1f}")

    # the gap the parameter-mismatch models do not close
    i20 = int(np.argmin(np.abs(TAUS - TAU_TABLE)))
    hw = vals[CURVES[0][0]][i20]
    best_sw = vals[CURVES[1][0]][i20]
    ax.annotate("", xy=(TAU_TABLE * 1000, hw), xytext=(TAU_TABLE * 1000, best_sw),
                arrowprops=dict(arrowstyle="<->", lw=0.9, color="#1a1a1a"))
    ax.text(TAU_TABLE * 1000 * 1.12, (hw + best_sw) / 2,
            "not explained by\nparameter spread",
            fontsize=6.3, va="center", ha="left", linespacing=1.25)

    ax.set_xscale("log")
    ax.set_xticks(TAUS * 1000)
    ax.set_xticklabels([f"{t*1000:.0f}" for t in TAUS])
    ax.set_xlabel("read-out kernel $\\tau$ (ms)")
    ax.set_ylabel("effective dimensionality $D_{\\mathrm{eff}}$")
    ax.legend(fontsize=5.9, loc="upper right", frameon=False, labelspacing=0.35)
    ax.set_ylim(bottom=0)
    ax.spines[["top", "right"]].set_visible(False)

    out = os.path.join(HERE, "deff_decomp.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), dpi=300, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
