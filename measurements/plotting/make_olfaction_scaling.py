#!/usr/bin/env python3
"""How the array would scale: wide not deep, and where the digital toll amortises.
Writes olfaction_scaling.pdf.

  (a) counts-only accuracy against layer width, for the digital projection and for the
      projection performed by the synapse fabric. Depth is reported in the text rather
      than plotted: the markers sat on top of the 16-wide point where both curves and
      the reference line already meet
  (b) the amortisation: energy per chunk against accuracy, showing that a wider array
      with the fabric projection is both cheaper AND more accurate than the 16-neuron
      pipeline we measured, because it deletes the two expensive digital stages

Simulated in the firmware's fixed-point arithmetic (bit-exactness gated); the measured
16-neuron point and the tree are silicon.

    python3 make_olfaction_scaling.py
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import constants as K

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "data", "olfaction")
INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
# ONE encoding for the whole figure, so nothing has to be looked up twice:
#   COLOUR = substrate    analog (the array) vs digital (the core)
#   FILL   = provenance   filled = measured on silicon, hollow = simulated or projected
#   SHAPE  = substrate, redundantly: circles analog, squares digital
# The previous scheme spent a colour per point, which meant "red = measured" in one panel
# and a projection colour in the other; provenance now lives in the fill, where it can be
# read with the caption alongside.
C_AN, C_DIGI, C_MEAS = "#0b7285", "#6741d9", "#c0392b"


def mk(ax, x, y, shape, colour, measured, **kw):
    """One marker under the figure's encoding.

    The marker EDGE carries the substrate (teal analog, purple digital) and the FILL
    carries the provenance: red means measured on silicon, unfilled means simulated or
    projected. Keeping them on different channels lets a reader answer "which substrate"
    and "is this real" independently, which a single colour per point leaves undone."""
    return ax.plot(x, y, shape, ms=kw.pop("ms", 5), color=colour,
                   mfc=(C_MEAS if measured else "none"), mec=colour, mew=1.3, **kw)


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


def main():
    style()
    deep = json.load(open(os.path.join(RES, "olfaction_deep_sim.json")))
    fab = json.load(open(os.path.join(RES, "olfaction_fabric_width.json")))
    ref_pc, ref_v5 = deep["reference_kernel"]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.09, 2.6))

    # ---- (a) accuracy vs width ---------------------------------------------
    ff = [r for r in deep["sweep"] if r.get("depth") == 1 and not r.get("lateral")]
    ff.sort(key=lambda r: r["width"])
    w1 = [r["width"] for r in ff]
    v1 = [r["voted5"] for r in ff]
    e1 = [r["voted5_sd"] for r in ff]
    a1.errorbar(w1, v1, yerr=e1, fmt="o-", ms=3.5, lw=1.3, color=C_AN, capsize=2,
                mfc="none", mec=C_AN, mew=1.2,
                label="array, digital projection (sim)")
    wf = sorted(int(k) for k in fab)
    vf = [fab[str(k)]["voted5"] for k in wf]
    ef = [fab[str(k)]["voted5_sd"] for k in wf]
    a1.errorbar(wf, vf, yerr=ef, fmt="s--", ms=3.5, lw=1.3, color=C_AN, capsize=2,
                mfc="none", mec=C_AN, mew=1.2,
                label="array, fabric projection (sim)")
    # Two references for the SAME configuration -- 16 neurons plus the digital kernel
    # read-out -- one simulated and one measured, and they disagree by 0.144. Both are
    # drawn, because the sweeps are calibrated against the simulated one and a reader is
    # entitled to see that silicon undershoots it. Neither is counts-only, unlike the
    # sweeps; they mark targets on this axis rather than members of it.
    a1.axhline(ref_v5, color=MUTED, ls=(0, (4, 2)), lw=1.0)
    a1.text(130, ref_v5 + 0.012, "16w + kernel (sim)", fontsize=6.0,
            color=MUTED, ha="right")
    a1.axhline(K.OLF_ACC_ARRAY_V5, color=C_MEAS, ls=(0, (1, 2)), lw=1.0)
    a1.text(130, K.OLF_ACC_ARRAY_V5 + 0.010, "16w + kernel (measured)",
            fontsize=6.0, color=C_MEAS, ha="right")
    # COUNTS-ONLY, because that is what this axis and the sweeps report. Plotting the
    # with-kernel 0.756 here compared two different read-outs and made the simulation look
    # 0.144 optimistic about the sweep quantity; like for like it is 0.045, inside the
    # measurement's own spread.
    mk(a1, [16], [K.OLF_ACC_COUNTS_V5], "o", C_AN, True, zorder=5,
       label="16w counts-only, measured")
    a1.set_xscale("log", base=2); a1.set_xticks([8, 16, 32, 64, 128])
    a1.set_xticklabels([8, 16, 32, 64, 128])
    a1.set_xlabel("neurons in the layer"); a1.set_ylabel("voted accuracy (counts only)")
    a1.set_ylim(0.30, 0.96); a1.set_xlim(7.4, 150)
    a1.text(0.04, 0.04, "(a)", transform=a1.transAxes, fontsize=6.5)
    a1.legend(fontsize=5.5, loc="lower right", bbox_to_anchor=(1.03, 0.03),
              handletextpad=0.4, borderpad=0.2)
    a1.grid(color=GRID, lw=0.4, alpha=0.6); a1.set_axisbelow(True)

    draw_panel_b(a2)

    fig.tight_layout(pad=0.45, w_pad=1.6)
    out = os.path.join(HERE, "olfaction_scaling.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    print(f"wrote {out}")


def draw_panel_b(a2, tag="(b)", legend_ncol=1):
    """Panel (b) on any axes: energy vs accuracy per decision, measured points only.
    Also used standalone (--b-only) to render olfaction_scaling_b.pdf as the
    single-panel variant, so it stays consistent with the main figure."""
    # ---- (b) amortisation: energy vs accuracy, PER DECISION ----------------
    # per voted5 DECISION (5 chunks), so the energy axis and the accuracy axis describe
    # the same event. Quoting per-chunk energy against a voted-over-5 accuracy compares
    # two different things.
    E = K.E_CYCLE_J
    KCH = 5
    # (x, y, label, colour, shape, sd, measured)
    # MEASURED ONLY. The width projections and the multiplexing projection used to sit
    # here; both are simulation or arithmetic, and one of them (rail/16) turned out to be
    # 9.8x optimistic once the array's real parallelism was measured. The scaling argument
    # lives in panel (a), which is labelled simulation throughout, and in the text.
    pts = [(4834 * KCH, K.OLF_ACC_ARRAY_V5, "16 analog LIF\n+ RISC-V kernels", C_AN, "o",
            K.OLF_ACC_ARRAY_V5_SD, True),
           # The emulated-LIF pipeline -- the matched pair that isolates the substrate.
           # Withheld until it was run on the die; run 2026-08-18: all 7200 rows over the
           # three projection seeds returned spike times bit-identical to the host mirror
           # of the firmware arithmetic, and scoring them gives 0.822 +/- 0.042 exactly.
           # Energy is the measured SRAM-resident 51.9 cyc/neuron-step.
           (K.OLF_DEC_EMUL_UJ, K.OLF_ACC_EMUL_V5, "16 LIF emulated on RISC-V\n+ RISC-V kernels",
            C_DIGI, "s", K.OLF_ACC_EMUL_V5_SD, True),
           (K.OLF_CYC_MEASURED_Q16 * E * 1e6 * KCH, K.OLF_ACC_Q16_V5,
            "digital tree\non RISC-V", C_DIGI, "s", K.OLF_ACC_Q16_V5_SD, True)]

    # The hybrid tree, measured: every node comparison performed by one time-multiplexed
    # analog neuron. Both inputs are measurements -- accuracy from the on-chip run, energy
    # from the measured slot time -- so the point is only drawn when both exist.

    sco = os.path.join(RES, "olfaction_hybrid_score.json")
    slt = os.path.join(RES, "olfaction_hybrid_slot.json")
    if os.path.exists(sco) and os.path.exists(slt):
        hs, hl = json.load(open(sco)), json.load(open(slt))
        # ANALOG colour: what distinguishes it from the digital tree is that the node
        # comparisons are performed by the array. Filled, because it is measured.
        pts.append((hl["e_decision_J"] * 1e6, hs["analog"]["voted5"],
                    "hybrid tree, 1 analog\nneuron + digital routing", C_AN, "o",
                    hs.get("voted5_sd", 0.0), True))
        # 16-way multiplexing divides the rail term only; delivery, re-arm, the AER read
        # and the routing are per visit and stay unamortised. Drawn to show that it moves
        # the point by ~11x and still trails the digital tree.

    # EVERY point carries the spread its own data supports. Drawing one error bar and
    # leaving the rest bare invites precisely the comparison the spreads forbid: the tree
    # and the hybrid differ by 0.014 with standard deviations of 0.016 and 0.033.
    for x, y, lab, c, m, sd, meas in pts:
        mk(a2, [x], [y], m, c, meas, zorder=4)
        if sd:
            a2.errorbar([x], [y], yerr=sd, fmt="none", ecolor=c, elinewidth=1.0,
                        capsize=2.5, alpha=0.85, zorder=3)

    lp = {"digital tree\non RISC-V": (1.35, 0.013, "center", "bottom"),
          "128w, fabric\nprojection": (1.00, 0.013, "center", "bottom"),
          "64w, digital\nprojection": (1.00, 0.014, "center", "bottom"),
          "16 analog LIF\n+ RISC-V kernels": (1.18, -0.008, "left", "top"),
          "16 LIF emulated on RISC-V\n+ RISC-V kernels": (1.04, 0.010, "left", "bottom"),
          "hybrid tree, 1 analog\nneuron + digital routing": (1.55, 0.0, "left",
                                                               "center")}
    for x, y, lab, c, m, sd, meas in pts:
        fx, fy, ha, va = lp[lab]
        a2.text(x * fx, y + fy, lab, fontsize=6.0, color=c, ha=ha, va=va)
    a2.set_xscale("log"); a2.set_xlim(90, 400000); a2.set_ylim(0.70, 1.00)
    from matplotlib.lines import Line2D
    # The key states the two CHANNELS separately. Showing the substrates as a filled
    # circle and a filled diamond mixed all three variables into two swatches -- and once
    # a digital-core point was drawn as an unfilled circle it contradicted its own key.
    # Substrate swatches therefore vary only in colour, provenance swatches only in fill.
    key = [Line2D([], [], marker="o", ls="none", ms=5, mfc=C_MEAS, mec=C_AN, mew=1.3,
                  label="analog array"),
           Line2D([], [], marker="s", ls="none", ms=5, mfc=C_MEAS, mec=C_DIGI, mew=1.3,
                  label="digital core"),
           ]
    a2.legend(handles=key, fontsize=5.4, loc="lower left", ncol=legend_ncol,
              columnspacing=0.9, handletextpad=0.4, borderpad=0.2, labelspacing=0.3)
    a2.set_xlabel(r"energy per decision ($\mu$J), voted over 5 chunks")
    a2.set_ylabel("voted accuracy")
    if tag:
        a2.text(0.95, 0.05, tag, transform=a2.transAxes, fontsize=6.5)
    a2.grid(color=GRID, lw=0.4, alpha=0.6); a2.set_axisbelow(True)


def b_only():
    """Panel (b) on its own axes, single-column sized, for reference/micro/date/."""
    style()
    fig, ax = plt.subplots(1, 1, figsize=(3.5, 2.9))
    draw_panel_b(ax, tag=None)
    fig.tight_layout(pad=0.4)
    out = os.path.join(HERE, "olfaction_scaling_b.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    print(f"wrote {out}")


if __name__ == "__main__":
    import sys
    b_only() if "--b-only" in sys.argv else main()
