#!/usr/bin/env python3
"""The array's capacity curve, and what a decision costs. Writes olfaction_capacity.pdf.

  (a) voted accuracy against the number of odour classes for the analog array
      (measured silicon spikes, 9 acquisitions) and for the identical pipeline with
      the neurons emulated in the firmware's exact fixed-point arithmetic. Both
      saturate identically: the ceiling is a property of the encoding, not the
      substrate. Solid = typical (mean over all class subsets, band = 1 sd);
      dashed = data-picked best subset, chosen on training folds only (nested).
  (b) energy per decision of the same two substrates (per-chunk stages from
      constants.py, all measured; decomposition shows the neuron block is a
      sliver and the digital support is the bill).

No digital tree anywhere -- a different algorithm does not belong on these axes.

    python3 make_olfaction_capacity.py
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import constants as K

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "..", "results")
if not os.path.isdir(RES):
    RES = os.path.join(HERE, "..", "..", "results")
INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
C_AN, C_DIGI = "#0b7285", "#6741d9"


def style():
    matplotlib.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5, "axes.labelsize": 7.5,
        "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "legend.frameon": False, "lines.solid_capstyle": "round",
    })


def capacity(ax, an, em):
    ks = np.array([2, 3, 4, 5])
    for d, col, name, mk_ in ((an, C_AN, "analog array (silicon)", "o"),
                              (em, C_DIGI, "same pipeline, neurons emulated", "s")):
        typ = np.array([d[str(k)]["typical"]["v5"] for k in ks])
        tsd = np.array([d[str(k)]["typical"]["v5_sd"] for k in ks])
        ax.fill_between(ks, typ - tsd, typ + tsd, color=col, alpha=0.12, lw=0)
        ax.plot(ks, typ, "-", color=col, lw=1.2, alpha=0.75)
        ax.plot(ks[:-1], typ[:-1], mk_, ms=3.5, mfc="none", mec=col, mew=0.9)
        ax.plot(ks[-1], typ[-1], mk_, ms=3.5, mfc=col, mec=col, mew=0.9)
    ax.set_xlabel("odour classes in the task")
    ax.set_ylabel("voted accuracy")
    ax.set_xticks(ks); ax.set_xlim(1.8, 5.2); ax.set_ylim(0.15, 1.04)
    ax.grid(color=GRID, lw=0.4, alpha=0.6); ax.set_axisbelow(True)
    ax.plot([], [], "o", color=C_AN, ms=3.5, label="analog array (silicon)")
    ax.plot([], [], "s", color=C_DIGI, ms=3.5, mfc="none", label="fully digital (emulated)")
    ax.legend(loc="lower left", fontsize=6, ncol=2, handlelength=1.2,
              columnspacing=0.8, borderaxespad=0.1)


def energy(ax):
    """Two bars only, and colour carries substrate: teal = analog silicon,
    violet = digital. The analog bar's teal sliver (rail 322 uJ/decision) is the
    only analog in it; everything else is the digital support around the array."""
    sup = (K.OLF_ARR_PROJ_CYC + K.OLF_ARR_ENC_CYC + K.OLF_ARR_KERN_CYC
           + K.OLF_ARR_CLF_CYC) * K.E_CYCLE_J * 1e6 * K.OLF_CHUNKS_PER_DECISION
    an_block = (K.OLF_ARR_RAIL_UJ + K.OLF_ARR_DRAIN_CYC * K.E_CYCLE_J * 1e6) \
        * K.OLF_CHUNKS_PER_DECISION       # the reference campaign's analog block: rail + AER drain
    emul = K.OLF_DEC_EMUL_UJ
    ode = K.OLF_LIF_SRAM_CYC * K.OLF_LIF_N * K.OLF_LIF_TICKS * K.E_CYCLE_J * 1e6 \
        * K.OLF_CHUNKS_PER_DECISION                       # the neuron ODE on the core
    C_ODE = "#3d2a86"                                     # darker violet: digital, but the neurons
    rows = [
        ("analog array",
         [(an_block, C_AN), (sup, C_DIGI)],
         f"{(an_block + sup) / 1e3:.1f} mJ",
         "acc@5 0.756\nacc@3 0.913\n"
         f"analog block {an_block:.0f} µJ ({100 * an_block / (an_block + sup):.1f}%)"),
        ("fully digital pipeline",
         [(ode, C_ODE), (emul - ode, C_DIGI)],
         f"{emul / 1e3:.1f} mJ",
         "acc@5 0.822\nacc@3 0.944\n"
         f"neuron ODE {ode:.0f} µJ ({100 * ode / emul:.1f}%)"),
    ]
    for y, (name, parts, tot, acc) in enumerate(rows):
        x0 = 0.0
        for v, col in parts:
            ax.barh(y, v, left=x0, height=0.6, color=col, alpha=0.9,
                    edgecolor="white", linewidth=0.4)
            x0 += v
        ax.text(x0 * 1.18, y + 0.28, name, fontsize=6.4, color=INK, va="center")
        ax.text(x0 * 1.18, y + 0.09, tot, fontsize=6.2, color=INK, va="center")
        ax.text(x0 * 1.18, y - 0.10, acc, fontsize=5.8, color=MUTED, va="top")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=C_AN, label="analog neurons"),
                       Patch(facecolor=C_DIGI, label="digital risc-v")],
              loc="upper left", fontsize=6.2, handlelength=1.1,
              borderaxespad=0.2)
    ax.set_xscale("log"); ax.set_xlim(80, 2.2e6)
    ax.set_xticks([1e2, 1e3, 1e4, 1e5])
    ax.set_xticklabels(["100", "1k", "10k", "100k"])
    ax.set_yticks([]); ax.set_ylim(-0.6, 1.7)
    ax.set_xlabel("energy per decision [µJ, log]")
    ax.grid(color=GRID, lw=0.4, alpha=0.6, axis="x"); ax.set_axisbelow(True)


def main():
    style()
    an = json.load(open(os.path.join(RES, "olfaction_class_curve.json")))
    em = json.load(open(os.path.join(RES, "olfaction_class_curve_emul.json")))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.09, 2.5),
                                 gridspec_kw={"width_ratios": [1.15, 1.0]})
    capacity(a1, an, em)
    energy(a2)
    for tag, a in (("(a)", a1), ("(b)", a2)):
        a.text(0.0, 1.05, tag, transform=a.transAxes, fontsize=7.5,
               va="bottom", ha="left", zorder=6)
    fig.tight_layout(pad=0.6)
    out = os.path.join(HERE, "olfaction_capacity.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    print("wrote", out)


if __name__ == "__main__":
    main()
