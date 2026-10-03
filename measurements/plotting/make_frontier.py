#!/usr/bin/env python3
"""Regenerate ecg_frontier.pdf.

Differences from the original `reservoir_frontier.py::make_figure` in the repo root:

  1. MEASURED energy axis. The original used a literature-order E_cycle = 100 pJ
     estimate. We now have measured supply-rail power: the analog
     array draws 0.43 mW on aVDD and the RV32I draws 9.3 mW on DVDD at 25 MHz,
     i.e. 372 pJ/cycle. The analog point is additionally charged its own STATIC
     power over the whole 2 s beat window, which is the dominant term and which
     the old estimate left out entirely.
  2. Panel (a) redesigned for readability: taller axes, points labelled directly
     instead of via a cramped inset legend, and the two ratios that matter
     annotated explicitly.
  3. Honest inclusion of OP3. On the measured axis the multiply-free tree is
     ~42x cheaper than the analog array at the same accuracy (COUNTED OP3 basis,
     constants.OP3_CYC_TOTAL; the ~580x this originally said came from a
     hard-coded 4000 cyc/beat estimate that was low by 13.8x -- retracted, kept out of use
     reinstate). The analog substrate's cost win is only against reproducing
     ITSELF numerically (OP2), and unlike OP2 the tree baseline stays fixed
     with dt at all.

Reads reservoir_frontier.json (copied into this folder); every accuracy number
comes from that file.

Usage:  python3 make_frontier.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import constants as K

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- measured hardware constants (single source of truth: constants.py) -----
P_ANALOG_W = K.P_ANALOG_W    # measured aVDD, array at max firing rate
P_CORE_W   = K.P_CORE_W      # measured DVDD, RV32I at 25 MHz
F_CLK      = K.F_CLK
E_CYCLE_J  = K.E_CYCLE_J     # 372 pJ/cycle, MEASURED

# The digital path is plotted on the MEASURED SRAM-resident cost (481 cyc/neuron-step,
# Timer0 microbenchmark), which is the basis the reference analysis quotes throughout. The
# idealised 1-CPI instruction count (153 cyc) is shown alongside as an explicit lower
# bound that favours the digital baseline. Before this change the figure was plotted on
# the idealised basis while the text quoted the measured one.
IDEAL_TO_MEASURED = K.CYC_STEP_SRAM / K.CYC_STEP_IDEAL      # 3.14x

INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
C_ANALOG, C_NUMERIC, C_TREE = "#0b7285", "#c0392b", "#6741d9"


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
        "legend.frameon": False,
        "lines.solid_capstyle": "round",
    })


def main():
    style()
    d = json.load(open(os.path.join(HERE, "reservoir_frontier.json")))
    acc, cost, sweep = d["accuracy"], d["cost"], d["dt_sweep"]
    T_BEAT = cost["t_beat"]

    # ---- measured energy per inference (mJ) --------------------------------
    # Task F: MEASURED read-out basis (105 cyc/call + 480 cyc/event) rather than the
    # 200 cyc/spike estimate the json still carries.
    aer_cyc  = K.aer_cycles_per_beat(cost["op1_mean_spikes_per_beat"])
    e_analog = K.analog_energy_J(aer_cyc) * 1e3
    # Task I: COUNTED basis (op3_count.py) rather than the json 4000-cycle estimate.
    e_tree   = K.OP3_CYC_TOTAL * E_CYCLE_J * 1e3
    e_ref    = cost["op4_ref_cycles_per_beat"] * E_CYCLE_J * 1e3

    # OP2 on the two bases. The json carries the idealised 1-CPI count; the measured
    # SRAM-resident cost is that scaled by 481/153, both at dt = 1 ms.
    e_num       = K.numeric_energy_J(1e-3, K.CYC_STEP_SRAM) * 1e3      # measured, plotted
    e_num_ideal = K.numeric_energy_J(1e-3, K.CYC_STEP_IDEAL) * 1e3     # lower bound
    dt_floor       = K.DT_STAR_MEASURED
    dt_floor_ideal = K.DT_STAR_IDEAL
    e_num_floor = K.numeric_energy_J(dt_floor, K.CYC_STEP_SRAM) * 1e3

    # ---- regression assertions: the basis stays fixed ---------------
    K.selfcheck(e_analog)
    assert abs(dt_floor * 1e6 - 308) < 1.0, dt_floor
    assert abs(dt_floor_ideal * 1e6 - 98) < 1.0, dt_floor_ideal
    assert abs(e_num / e_analog - 6.55) < 0.05, e_num / e_analog
    assert abs(e_num_floor / e_analog - 21.3) < 0.2, e_num_floor / e_analog
    assert abs(e_analog / e_tree - 42.5) < 1.0, e_analog / e_tree
    assert abs(K.crossover_dt(K.CYC_STEP_SRAM, e_analog * 1e-3) * 1e3 - 6.55) < 0.1

    PTS = [
        ("OP1_analog_reservoir", e_analog, "OP1  analog array + RISC-V read-out",
         C_ANALOG, "o"),
        ("OP2_numeric_LIF", e_num, "OP2  same reservoir, numeric on RV32I",
         C_NUMERIC, "s"),
        ("OP3_edge_GBM", e_tree, "OP3  edge trees (no multiply)", C_TREE, "^"),
        ("OP4_cpu_ref", e_ref, "OP4  CPU reference", MUTED, "D"),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.09, 3.35),
                                   gridspec_kw={"wspace": 0.30})
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)

    # ================= panel (a): accuracy vs MEASURED energy ==============
    ax1.set_xscale("log")
    ax1.set_xlim(3e-4, 400)
    ax1.set_ylim(0.28, 1.06)

    band_lo = max(acc[k]["ci_lo"] for k, *_ in PTS)
    band_hi = min(acc[k]["ci_hi"] for k, *_ in PTS)
    ax1.axhspan(band_lo, band_hi, color=MUTED, alpha=0.11, lw=0, zorder=0)
    ax1.text(6.0, 0.50, "all four accuracies coincide\n(95% CIs overlap)",
             fontsize=6.2, color=MUTED, va="center", ha="left", linespacing=1.35)

    handles = []
    for key, e_mJ, label, col, mark in PTS:
        a, sd = acc[key]["acc"], acc[key]["acc_sd"]
        ax1.errorbar(e_mJ, a, yerr=sd, fmt="none", ecolor=col,
                     elinewidth=1.1, capsize=2.2, capthick=1.1, alpha=0.85, zorder=2)
        h, = ax1.plot(e_mJ, a, mark, ms=7.0, mfc=col, mec="white", mew=0.8,
                      color=col, ls="none", label=label, zorder=3)
        handles.append(h)

    # OP2 on the idealised 1-CPI instruction count: an explicit lower bound that
    # favours the digital baseline. Open marker, joined to the measured point.
    a2 = acc["OP2_numeric_LIF"]["acc"]
    ax1.plot([e_num_ideal, e_num], [a2, a2], "-", color=C_NUMERIC, lw=0.8,
             alpha=0.45, zorder=2)
    h_ideal, = ax1.plot(e_num_ideal, a2, "s", ms=6.0, mfc="white", mec=C_NUMERIC,
                        mew=1.1, ls="none", zorder=3,
                        label=r"OP2  idealised 1-CPI count (lower bound)")
    handles.append(h_ideal)
    ax1.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.02, 1.03),
               fontsize=6.3, labelspacing=0.42, handletextpad=0.5, borderpad=0.2)

    # the analog array's cost is independent of dt -- draw that as a guide line
    ax1.axvline(e_analog, color=C_ANALOG, ls=":", lw=0.9, alpha=0.7, zorder=1)

    # ratio 1: the SUBSTRATE comparison (same dynamics, physics vs numerics)
    y_arrow = 0.375
    ax1.annotate("", xy=(e_num, y_arrow), xytext=(e_analog, y_arrow),
                 arrowprops=dict(arrowstyle="<->", lw=0.9, color=INK,
                                 shrinkA=0, shrinkB=0))
    ax1.text((e_analog * e_num) ** 0.5, y_arrow + 0.014,
             rf"same dynamics: ${e_num/e_analog:.1f}\times$" "\n"
             rf"(${e_num_floor/e_analog:.0f}\times$ at $\Delta t^\star$)",
             fontsize=6.2, ha="center", va="bottom", color=INK, linespacing=1.3)

    # ratio 2: the TASK comparison -- honest, and fair to the array
    y_arrow2 = 0.325
    ax1.annotate("", xy=(e_analog, y_arrow2), xytext=(e_tree, y_arrow2),
                 arrowprops=dict(arrowstyle="<->", lw=0.9, color=C_TREE,
                                 shrinkA=0, shrinkB=0))
    ax1.text((e_tree * e_analog) ** 0.5, y_arrow2 - 0.008,
             rf"task-matched digital: ${e_analog/e_tree:.0f}\times$ cheaper",
             fontsize=6.2, ha="center", va="top", color=C_TREE)

    # where the numeric path goes as dt shrinks (the mechanism, panel b)
    ax1.annotate("", xy=(e_num_floor, acc["OP2_numeric_LIF"]["acc"]),
                 xytext=(e_num * 1.35, acc["OP2_numeric_LIF"]["acc"]),
                 arrowprops=dict(arrowstyle="->", lw=1.0, color=C_NUMERIC, alpha=0.75))
    ax1.text(e_num_floor * 1.3, acc["OP2_numeric_LIF"]["acc"],
             r"$\Delta t\!\rightarrow\!\Delta t^\star$",
             fontsize=6.2, color=C_NUMERIC, ha="left", va="center")

    ax1.set_xlabel("measured energy per inference (mJ)\n"
                   "372 pJ/cycle (9.3 mW / 25 MHz) · analog charged 0.43 mW × 2 s")
    ax1.set_ylabel("inter-patient accuracy (LORO, N/S/V)")
    ax1.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    ax1.grid(axis="y", ls=":", lw=0.5, color=GRID, zorder=0)
    ax1.tick_params(length=2.5)

    # ================= panel (b): the O(N/dt) mechanism ====================
    inv_dt = [1.0 / s["dt"] for s in sweep]
    # MEASURED SRAM-resident basis (primary), and the idealised 1-CPI lower bound.
    lat_ms = [K.numeric_cycles_per_beat(s["dt"], K.CYC_STEP_SRAM) / F_CLK * 1e3
              for s in sweep]
    lat_ms_ideal = [K.numeric_cycles_per_beat(s["dt"], K.CYC_STEP_IDEAL) / F_CLK * 1e3
                    for s in sweep]
    aer_ms = aer_cyc / F_CLK * 1e3

    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.axhline(T_BEAT * 1e3, color=INK, ls=(0, (4, 2)), lw=1.0, zorder=2)
    # the band between the two bases is instruction fetch and nothing else
    ax2.fill_between(inv_dt, lat_ms_ideal, lat_ms, color=C_NUMERIC, alpha=0.13,
                     lw=0, zorder=1)
    ax2.plot(inv_dt, lat_ms_ideal, "--", color=C_NUMERIC, lw=1.0, alpha=0.75, zorder=3)
    ax2.plot(inv_dt, lat_ms, "-", color=C_NUMERIC, lw=1.8, zorder=3)
    ax2.plot(inv_dt, lat_ms, "s", color=C_NUMERIC, mfc=C_NUMERIC, mec="white",
             mew=0.7, ms=4.5, zorder=4)
    ax2.axhline(aer_ms, color=C_ANALOG, lw=2.0, zorder=3)
    ax2.axvline(1.0 / dt_floor, color=MUTED, ls=":", lw=0.9, zorder=1)
    ax2.axvline(1.0 / dt_floor_ideal, color=MUTED, ls=":", lw=0.7, alpha=0.6, zorder=1)

    ax2.set_xlabel(r"temporal-resolution demand  $1/\Delta t$  (Hz)")
    ax2.set_ylabel(f"compute latency per beat (ms) @ {F_CLK/1e6:.0f} MHz")
    ax2.grid(which="both", ls=":", lw=0.5, color=GRID, zorder=0)
    ax2.tick_params(which="both", length=2.5)

    ax2.text(inv_dt[-1] * 0.85, lat_ms[-1] * 1.9,
             r"numeric, measured: $\propto N/\Delta t$",
             fontsize=6.6, color=C_NUMERIC, ha="right")
    ax2.text(inv_dt[-1] * 0.85, lat_ms_ideal[-1] * 0.42,
             "idealised 1-CPI count\n(lower bound)",
             fontsize=6.0, color=C_NUMERIC, ha="right", va="top",
             alpha=0.85, linespacing=1.25)
    ax2.text(inv_dt[0] * 1.15, T_BEAT * 1e3 * 1.30,
             "real-time budget (2 s beat)", fontsize=6.4, color=INK)
    ax2.text(inv_dt[0] * 1.15, aer_ms * 1.40,
             r"analog: flat in $\Delta t$ (physics, $O(1)$)",
             fontsize=6.4, color=C_ANALOG)
    ax2.text(1.0 / dt_floor * 0.88, min(lat_ms_ideal) * 0.40,
             rf"$\Delta t^\star$ = {dt_floor*1e6:.0f} µs",
             fontsize=6.4, color=MUTED, ha="right")

    for ax, letter in ((ax1, "a"), (ax2, "b")):
        ax.text(-0.16, 1.06, letter, transform=ax.transAxes,
                fontsize=9.5, fontweight="bold", va="top")

    base = os.path.join(HERE, "ecg_frontier")
    fig.savefig(base + ".pdf", bbox_inches="tight")
    fig.savefig(base + ".png", dpi=350, bbox_inches="tight")
    print(f"wrote {base}.pdf / .png")
    print(f"  OP1 analog        {e_analog:9.4f} mJ   acc {acc['OP1_analog_reservoir']['acc']:.3f}")
    print(f"  OP2 numeric MEAS  {e_num:9.4f} mJ   acc {acc['OP2_numeric_LIF']['acc']:.3f}"
          f"   ({e_num/e_analog:.1f}x)   [481 cyc/step, plotted]")
    print(f"  OP2 numeric IDEAL {e_num_ideal:9.4f} mJ"
          f"                  ({e_num_ideal/e_analog:.1f}x)   [153 cyc/step, lower bound]")
    print(f"  OP3 trees         {e_tree:9.4f} mJ   acc {acc['OP3_edge_GBM']['acc']:.3f}"
          f"   ({e_analog/e_tree:.0f}x cheaper than OP1)")
    print(f"  OP4 ref           {e_ref:9.4f} mJ   acc {acc['OP4_cpu_ref']['acc']:.3f}")
    print(f"  OP2 at dt*        {e_num_floor:9.4f} mJ   ({e_num_floor/e_analog:.1f}x)")
    print(f"  dt* measured      {dt_floor*1e6:9.1f} us   |  idealised {dt_floor_ideal*1e6:.1f} us")
    print("  all regression assertions passed")


if __name__ == "__main__":
    main()
