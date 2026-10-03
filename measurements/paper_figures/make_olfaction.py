#!/usr/bin/env python3
"""Olfaction: where the energy goes, what a neuron-step costs, and what would have to
change. Writes olfaction_cost.pdf.

Three panels, one point each:
  (a) energy per decision, stacked by stage -- the shared digital read-out dominates both
      LIF substrates, so the analog/digital choice for the neurons barely moves the total
  (b) cost of ONE neuron-step -- the unit an analog neuron has to beat, and how the
      analog side spends it (rail + its own read-out) against the digital bar
  (c) the analog neuron block versus rail power -- where the break-even actually sits,
      and the floor the AER read-out imposes no matter how good the analog gets

All values measured on this die; see data/olfaction_*.json.

    python3 make_olfaction.py
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

E = K.E_CYCLE_J
T, N, TICKS, KCH = 0.15, 16, 150, 5
INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
C_AN, C_DIG, C_TREE, C_RO = "#0b7285", "#c0392b", "#6741d9", "#adb5bd"


def style():
    matplotlib.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5, "axes.labelsize": 7.5,
        "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "legend.frameon": False, "lines.solid_capstyle": "round",
    })


def load():
    fw = json.load(open(os.path.join(RES, "olfaction_four_way.json")))
    lif = json.load(open(os.path.join(RES, "olfaction_lif_residency_calc.json")))
    acc_q = json.load(open(os.path.join(RES, "olfaction_digital_quant_acc.json")))
    val = json.load(open(os.path.join(RES, "olfaction_validate.json")))
    emul = json.load(open(os.path.join(RES, "olfaction_emul_accuracy.json")))
    return fw, lif, acc_q, val, emul


def main():
    style()
    fw, lif, acc_q, val, emul = load()
    uj = lambda c: c * E * 1e6

    proj, enc = uj(fw["proj_cyc"]), uj(fw["enc_cyc"])
    kern, clf = uj(fw["kern_cyc"]), uj(fw["clf_cyc"])
    drain = uj(fw["drain_cyc"])
    rail = K.P_ANALOG_W * T * 1e6
    lif_sram = lif["cyc_per_step"]["SRAM-resident (dff2)"] * N * TICKS * E * 1e6
    tree16, tree8 = uj(fw["tree_q16_cyc"]), uj(118349)

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(7.09, 2.45))

    # ---- (a) energy per decision, stacked by stage --------------------------
    # Linear y, and only the two LIF substrates stacked: on a log axis the neuron and
    # I/O segments vanish, which hides exactly what the panel exists to show. The trees
    # are drawn as reference lines instead -- they are two orders of magnitude below and
    # would flatten the stack if bars.
    # split the shared block into INPUT and OUTPUT signal processing. Calling it all
    # "read-out" was wrong: 53% of it is the input projection, and none of it is the
    # LA/AER interface, which is the separate (much smaller) drain term below.
    s_in, s_out = (proj + enc) * KCH, (kern + clf) * KCH
    shared = s_in + s_out
    x = np.arange(2)
    a1.bar(x, [s_in, s_in], 0.66, color="#546e7a",
           label="input DSP: projection + encode")
    a1.bar(x, [s_out, s_out], 0.66, bottom=[s_in, s_in], color="#b0bec5",
           label="output DSP: kernel features + classifier")
    a1.bar(x, [drain * KCH, 0], 0.66, bottom=[shared, shared],
           color="#f59f00", label="AER interface (LA handshake)")
    a1.bar([0], [rail * KCH], 0.66, bottom=[shared + drain * KCH], color=C_AN,
           label="neurons: analog rail")
    a1.bar([1], [lif_sram * KCH], 0.66, bottom=[shared], color=C_DIG,
           label="neurons: digital emulation")
    a1.text(0, s_in * 0.5, "projection", ha="center", va="center",
            fontsize=5.8, color="white")
    a1.text(0, s_in + s_out * 0.5, "kernel\nfeatures", ha="center", va="center",
            fontsize=5.8, color=INK)
    for xi, ex, ac in ((0, (drain + rail) * KCH, val["centre"]["voted"][4]),
                       (1, lif_sram * KCH, emul["best"]["voted5"])):
        a1.text(xi, shared + ex + 700, f"{ac:.2f} voted", ha="center", fontsize=6.2)
    for e_t in (tree16 * KCH, tree8 * KCH):
        a1.axhline(e_t, color=C_TREE, ls="--", lw=0.9)
    a1.annotate(f"tree kernels\n{tree16*KCH:.0f}--{tree8*KCH:.0f} " + r"$\mu$J",
                xy=(1.40, tree8 * KCH), xytext=(1.62, 7200), fontsize=6.0, color=C_TREE,
                ha="center", va="bottom",
                arrowprops=dict(arrowstyle="->", lw=0.7, color=C_TREE))
    a1.set_xticks(x); a1.set_xticklabels(["analog\narray", "all-digital\nsame pipeline"],
                                         fontsize=6.5)
    a1.set_ylabel(r"energy per decision ($\mu$J)")
    a1.set_xlim(-0.60, 1.95); a1.set_ylim(0, 44000)
    a1.text(0.93, 0.55, "(a)", transform=a1.transAxes, fontsize=6.5, va="top")
    a1.legend(fontsize=5.5, loc="upper left", bbox_to_anchor=(-0.03, 1.01),
              labelspacing=0.30)
    a1.grid(axis="y", color=GRID, lw=0.4, alpha=0.6); a1.set_axisbelow(True)

    # ---- (b) the cost of one neuron-step ------------------------------------
    steps = N * TICKS
    dig_step = lif["cyc_per_step"]["SRAM-resident (dff2)"] * E * 1e9
    rail_step = rail * 1e3 / steps
    drain_step = drain * 1e3 / steps
    a2.bar([0], [dig_step], 0.5, color=C_DIG)
    a2.bar([1], [rail_step], 0.5, color=C_AN, label="analog rail")
    a2.bar([1], [drain_step], 0.5, bottom=[rail_step], color="#f59f00",
           label="AER read-out")
    a2.axhline(dig_step, color=C_DIG, ls="--", lw=0.8, alpha=0.8)
    a2.text(1.44, dig_step + 2.4, "bar to beat", fontsize=6.2, color=C_DIG,
            va="center", ha="left")
    a2.set_xticks([0, 1]); a2.set_xticklabels(["digital\nemulation", "analog\narray"],
                                              fontsize=6.5)
    a2.set_ylabel("energy per neuron-step (nJ)")
    a2.set_xlim(-0.6, 2.25); a2.set_ylim(0, 56)
    a2.text(0.90, 0.965, "(b)", transform=a2.transAxes, fontsize=6.5, va="top")
    a2.text(1, rail_step + drain_step + 1.4, f"{rail_step+drain_step:.1f} nJ",
            ha="center", fontsize=6.2, color=INK)
    a2.text(0, dig_step + 1.4, f"{dig_step:.1f} nJ", ha="center", fontsize=6.2, color=INK)
    a2.legend(fontsize=5.9, loc="upper left", bbox_to_anchor=(-0.02, 1.005))
    a2.grid(axis="y", color=GRID, lw=0.4, alpha=0.6); a2.set_axisbelow(True)

    # ---- (c) what would have to change: analog block vs rail power ----------
    p = np.logspace(np.log10(2e-6), np.log10(1.2e-3), 300)
    block = (p * T * 1e6) + drain
    a3.plot(p * 1e6, block, color=C_AN, lw=1.4, label="analog block")
    a3.axhline(lif_sram, color=C_DIG, ls="--", lw=1.0, label="digital emulation")
    a3.axhline(drain, color="#f59f00", ls=":", lw=1.0, label="AER read-out floor")
    be = (lif_sram - drain) / (T * 1e6)
    a3.plot([be * 1e6], [lif_sram], "o", ms=4, color=INK, zorder=5)
    a3.annotate(f"break-even\n{be*1e6:.0f} " + r"$\mu$W", xy=(be * 1e6, lif_sram),
                xytext=(be * 1e6 * 0.30, lif_sram * 1.55), fontsize=6.2, color=INK,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=INK))
    a3.axvline(K.P_ANALOG_W * 1e6, color=MUTED, ls="-", lw=0.7, alpha=0.8)
    a3.text(K.P_ANALOG_W * 1e6 * 0.90, 96, f"measured\n{K.P_ANALOG_W*1e6:.0f} "
            + r"$\mu$W", fontsize=6.2, color=MUTED, ha="right", va="center")
    a3.set_xscale("log"); a3.set_xlabel(r"analog rail power ($\mu$W)")
    a3.set_ylabel(r"neuron block, energy per chunk ($\mu$J)")
    a3.set_ylim(0, 145)
    a3.text(0.90, 0.965, "(c)", transform=a3.transAxes, fontsize=6.5, va="top")
    a3.legend(fontsize=5.9, loc="upper left", bbox_to_anchor=(-0.01, 1.01))
    a3.grid(color=GRID, lw=0.4, alpha=0.6); a3.set_axisbelow(True)

    fig.tight_layout(pad=0.45, w_pad=1.5)
    out = os.path.join(HERE, "olfaction_cost.pdf")
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")
    print(f"  (a) shared read-out {shared:.0f} uJ/decision on both LIF bars")
    print(f"  (b) digital bar {dig_step:.1f} nJ/step; analog {rail_step+drain_step:.1f} "
          f"(rail {rail_step:.1f} + I/O {drain_step:.1f})")
    print(f"  (c) break-even rail {be*1e6:.1f} uW; read-out floor {drain:.1f} uJ")


if __name__ == "__main__":
    main()
