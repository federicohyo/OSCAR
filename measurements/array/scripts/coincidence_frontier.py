#!/usr/bin/env python3
"""the coincidence-frontier figure: MEASURED on-silicon continuous-time coincidence primitive on
neuron 14 -- a 2-panel figure of the membrane physics only. The cost argument (O(N/dt)
digital integration vs O(1) analog) lives with the RESERVOIR frontier (fig:frontier) rather than
here: for an isolated two-spike coincidence the right digital baseline is a
timestamp-and-subtract (O(1), us-precise), so this figure keeps clear of any cost/dominance claim.

Panels (single-EPSP-per-input primitive, firmware commit da5168a):
  (a) Oscilloscope membrane traces, four commanded intervals (Delta-t = 1/2/3/4 ms) aligned
      on the first EPSP: Delta-t-graded EPSP summation crossing the 800 mV positive-feedback
      threshold only at the shortest interval (spike at 1 ms; sub-threshold at 2/3/4 ms).
  (b) Measured P(spike) vs COMMANDED Delta-t (weight 15, 80 trials/pt, 0.25 ms grid,
      rapid-probe 10 ms inter-pair): a flat P~=1 plateau (~3.8 ms FWHM), sharp ~1.5/ms edges,
      zero baseline beyond +-2.5 ms.

Two honest scope notes (stated in the caption):
  * The abscissa is the COMMANDED interval: the execute-in-place (SPI-flash) stimulus path
    floors the delivered interval at ~1 ms, so true Delta-t=0 is out of reach and
    sub-millisecond membrane resolution is claimed (it is bounded by the RISC-V I/O rather than
    measured).
  * Absolute spiking is FACILITATION-GATED: a well-rested pair stays silent (a 150 ms-rested
    sweep gave peak P=0); rapid repetition primes the membrane. The Delta-t-graded summation
    is the continuous-time computation; the spike is its facilitation-gated read-out.
"""
import warnings; warnings.filterwarnings("ignore")
import csv
import json
import os
import numpy as np
MEAS_CSV = "data/array/coincidence_finegrid_n14_fixedfw.csv"  # n14 w15, coincidence_1 biases, fixed-firmware sweep
DATA = "measurements/array/figures"
SCOPE = "data/array"
SCOPE_COINC = "data/array/scopeCoinc"   # 13a membrane traces (fixed firmware)
# panel (a) membrane traces: (file, Delta-t ms, fires); aligned on first EPSP
SCOPE_TRACES = [("scope_26.csv", 1, True), ("scope_23.csv", 2, False),
                ("scope_24.csv", 3, False), ("scope_25.csv", 4, False)]
GRAYS_13A = {2: "#3a3a3a", 3: "#6f6d68", 4: "#898781"}
N_ARRAY = 16                                         # fabricated analog array size
V_THRESH_MV = 800.0                                  # comparator positive-feedback threshold (from traces)


# ---------------- measured analog Delta-t selectivity (neuron 14) -------------------
def load_measured():
    rows = list(csv.DictReader(open(MEAS_CSV)))
    d = sorted((float(r["dt_ms"]), float(r["p_fire"]), int(r["trials"])) for r in rows)
    return (np.array([x[0] for x in d]), np.array([x[1] for x in d]), int(d[0][2]))


def selectivity_stats(dt, p, trials):
    peak = float(p.max()); peak_dt = float(dt[p.argmax()])
    base = float(np.median(p[np.abs(dt) >= 7]))
    half = 0.5 * (peak + base)
    inside = dt[p >= half]
    fwhm = float(inside.max() - inside.min()) if inside.size else float("nan")
    slope = float(np.abs(np.gradient(p, dt)).max())          # steepest edge, /ms
    return dict(peak=peak, peak_dt_ms=peak_dt, baseline=base, fwhm_ms=fwhm,
                edge_slope_per_ms=slope, trials=trials,
                window_lo_ms=float(inside.min()), window_hi_ms=float(inside.max()))


def load_scope(name):
    rows = list(csv.reader(open(os.path.join(SCOPE, name))))[2:]
    t = np.array([float(r[0]) for r in rows]); v = np.array([float(r[1]) for r in rows]) * 1e3
    return t * 1e3, v          # ms, mV


def load_coinc(name):
    """13a membrane trace from data/scopeCoinc/ (skips the blank-voltage first sample)."""
    rows = [r for r in list(csv.reader(open(os.path.join(SCOPE_COINC, name))))[2:]
            if len(r) >= 2 and r[1] != ""]
    t = np.array([float(r[0]) for r in rows]); v = np.array([float(r[1]) for r in rows]) * 1e3
    return t * 1e3, v          # ms, mV


def first_onset(t, v):
    base = np.median(v[:150]); vs = np.convolve(v, np.ones(3) / 3, mode="same")
    return t[int(np.argmax(vs > base + 80))]          # first crossing baseline + 80 mV


def main():
    dt, p, trials = load_measured()
    sel = selectivity_stats(dt, p, trials)
    print(f"=== MEASURED n14 Delta-t selectivity ({MEAS_CSV}, {len(dt)} pts, {trials} trials) ===")
    print(f"  peak P={sel['peak']:.2f} at Delta-t={sel['peak_dt_ms']:+.2f} ms, baseline={sel['baseline']:.2f}")
    print(f"  window [{sel['window_lo_ms']:+.2f},{sel['window_hi_ms']:+.2f}] ms (FWHM {sel['fwhm_ms']:.2f} ms), "
          f"edge {sel['edge_slope_per_ms']:.2f}/ms")
    print("  NOTE: absolute firing is facilitation-gated (150 ms-rested sweep gave peak P=0); "
          "the Delta-t-selectivity is the measured property, the spike is its facilitation-gated read-out.")

    # NOTE: the digital O(N/dt) cost argument lives with the reservoir frontier (fig:frontier);
    # here an isolated 2-spike coincidence is cheap digitally (timestamp-and-subtract).

    # scope membrane traces (physics backbone)
    ts, vs = load_coinc("scope_26.csv"); tb, vb = load_coinc("scope_25.csv")
    print(f"\n=== scope membrane (physics): Delta-t=1 ms Vmax={vs.max():.0f} mV (spike), "
          f"Delta-t=4 ms Vmax={vb.max():.0f} mV (sub-threshold)")

    out = dict(
        measured_selectivity=sel, source_csv=MEAS_CSV, n_array=N_ARRAY,
        facilitation_gated=True, single_pair_rested_pfire=0.0,
        cost_note="the O(N/dt)-vs-O(1) integration-cost argument lives with the reservoir "
                  "frontier (fig:frontier); this figure is membrane physics only",
        scope=dict(spike_file="scope_26.csv", sub_file="scope_25.csv",
                   spike_vmax_mv=float(vs.max()), sub_vmax_mv=float(vb.max())),
    )
    with open("coincidence_frontier.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote coincidence_frontier.json")
    make_figure()
    return 0


# ------------------------------- figure ---------------------------------------------
ANALOG, DIGITAL, INK, MUTED, GRID = "#1baf7a", "#e34948", "#0b0b0b", "#898781", "#e1e0d9"


def make_figure(results_json="coincidence_frontier.json"):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib as mpl, matplotlib.pyplot as plt
    mpl.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 6, "ytick.labelsize": 6,
        "legend.fontsize": 5.6, "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK,
        "ytick.labelcolor": INK, "axes.labelcolor": INK, "text.color": INK,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5,
        "ytick.major.size": 2.5, "legend.frameon": False, "lines.solid_capstyle": "round",
    })
    d = json.load(open(results_json))
    sel = d["measured_selectivity"]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(5.0, 2.5))
    for ax in (axA, axB):
        ax.spines[["top", "right"]].set_visible(False)

    # (a) scope membrane: 4 traces, Delta-t-graded summation; threshold 800 mV (pos. feedback)
    axA.axhline(V_THRESH_MV, color=MUTED, ls=":", lw=0.8)
    axA.text(30, V_THRESH_MV - 12, "threshold (pos. feedback)", fontsize=5.0,
             color=MUTED, ha="right", va="top")
    for f, dtms, fires in SCOPE_TRACES:
        t, v = load_coinc(f); x = t - first_onset(t, v); w = (x >= -10) & (x <= 30)
        col = ANALOG if fires else GRAYS_13A[dtms]
        lbl = rf"$\Delta t{{=}}{dtms}$ ms" + (r"$\,\to$ spike" if fires else "")
        axA.plot(x[w], v[w], color=col, lw=1.3 if fires else 0.95, label=lbl,
                 zorder=3 if fires else 2)
    axA.set_xlim(-10, 30)
    axA.set_xlabel("time from first EPSP (ms)"); axA.set_ylabel("membrane V (mV)")
    axA.legend(loc="upper right", handlelength=1.2, labelspacing=0.22)
    axA.set_title(r"membrane: $\Delta t$-graded summation", fontsize=6.6, color=INK)

    # (b) measured Delta-t selectivity: few-ms window, fixed firmware (rapid probe). The ~1 ms
    #     firmware delivery floor (actual Delta-t = commanded + ~1 ms) is noted in the caption.
    mdt, mp, mtr = load_measured()
    axB.axvspan(sel["window_lo_ms"], sel["window_hi_ms"], color=ANALOG, alpha=0.10, lw=0)
    axB.plot(mdt, mp, "-o", color=ANALOG, lw=1.3, ms=3, mec="white", mew=0.4)
    axB.set_xlim(-5, 5)
    axB.set_xlabel(r"commanded interval $\Delta t$ (ms)")
    axB.set_ylabel("P(spike)  [rapid probe]")
    axB.set_title(f"$\\Delta t$-selectivity: FWHM {sel['fwhm_ms']:.1f} ms, edge {sel['edge_slope_per_ms']:.1f}/ms",
                  fontsize=6.6, color=INK)

    for ax, L in ((axA, "a"), (axB, "b")):
        ax.text(-0.26, 1.04, L, transform=ax.transAxes, fontsize=8, fontweight="bold",
                va="bottom", ha="left")
        ax.grid(True, which="major", ls=":", lw=0.5, color=GRID, zorder=0)
    fig.tight_layout(w_pad=1.6)
    base = "measurements/array/figures/coincidence_frontier"
    fig.savefig(base + ".pdf", bbox_inches="tight")
    fig.savefig(base + ".png", dpi=350, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {base}.{{pdf,png}} (2-panel: membrane / measured selectivity)")


if __name__ == "__main__":
    raise SystemExit(main())
