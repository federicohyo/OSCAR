#!/usr/bin/env python3
"""TiO2 water-pad characterisation, three panels in one row.

One continuous record: scope_20260829_094236.csv (1 kHz, 72.7 s).
  1. wetting       -- the droplet lands, and the pad stops being an antenna
  2. stable point  -- the output settles and stays quiet
  3. saline        -- salt goes in, and the output steps up to the rail

CHANNELS (there are two amplifiers on the die):
  ch2 = output of the PAD amplifier -- its input is the exposed TiO2 pad.
        This is the only trace plotted here; it is the measurement.
  ch1 = output of the second amplifier, whose input is the PCB jack driven
        from the PC. Nothing is played into it during this run, so it carries
        only noise and speaks to the pad's behaviour. Left out of the plot.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "measurements/wet_pad/data/scope_20260829_094236.csv"
OUT = "measurements/wet_pad/figures/tio2_three_panel"
RAIL = 1.809
FS = 1000.0          # sample rate
TS = 1.0             # type scale, set by build()

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_PAD, C_EVT = "#c05621", "#9b2c2c"

d = np.genfromtxt(CSV, delimiter=",", names=True)
# board_seconds is quantised to 10 ms; sample_index is the honest 1 kHz clock
t = (d["sample_index"] - d["sample_index"][0]) / FS
pad = d["volts_ch2"]


def boxcar(x, sec):
    k = int(sec * FS)
    return np.convolve(x, np.ones(k) / k, mode="same")


# Running rms about a 0.2 s moving mean (so >~5 Hz survives), smoothed 0.5 s.
# The dominant line in it is 58.4 Hz mains pickup (checked by FFT).
rms = np.sqrt(np.maximum(boxcar((pad - boxcar(pad, 0.2)) ** 2, 0.5), 0.0))
edge = int(0.6 * FS)
rms[:edge] = np.nan
rms[-edge:] = np.nan

T_DROP, T_SALT_A, T_SALT_B = 38.13, 44.30, 46.90
LVL = np.median(pad[(t >= 40.0) & (t < 44.0)])
HUM_DRY = 1e3 * np.nanmedian(rms[(t >= 0) & (t < 13)])
HUM_WET = 1e3 * np.nanmedian(rms[(t >= 40) & (t < 44)])
V0 = np.median(pad[(t >= 44.0) & (t < 44.3)])


def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9 * TS)


def small(ax):
    """Inset styling."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.grid(True, color="#ececec", lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=7 * TS)


def panel(fig, gs, k, a, b, name, caption, ylim=(0.0, 1.95)):
    """caption=None drops the sub-heading: inside the report the LaTeX caption
    already says all of it, and the space is worth more than the repetition."""
    ax = fig.add_subplot(gs[k])
    m = (t >= a) & (t < b)
    ax.plot(t[m], pad[m], color=C_PAD, lw=1.2)
    ax.set_xlim(a, b)
    ax.set_ylim(*ylim)
    ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
    dress(ax)
    ax.set_title(name, loc="left", color=INK, fontsize=12.5 * TS,
                 fontweight="bold", pad=24 if caption else 8)
    if caption:
        ax.text(0.0, 1.015, caption, transform=ax.transAxes, color=INK2,
                fontsize=9.5 * TS)
    return ax


def build(figw, figh, fontscale, standalone=True, wetting_only=False):
    """Draw the row. fontscale scales every font, so the same design renders both as a
    standalone image and, smaller and with proportionally larger type, inside the
    LaTeX report where it is shrunk to the text width."""
    global TS
    TS = fontscale
    fig = plt.figure(figsize=(figw, figh))
    cap = (lambda x: x) if standalone else (lambda x: None)
    # inside the report the panels are a third as wide, so they get short names
    nm = (lambda long, short: long if standalone else short)
    gs = fig.add_gridspec(1, 1 if wetting_only else 3, wspace=0.14,
                          left=0.19 if wetting_only else (0.052 if standalone else 0.085),
                          right=0.975 if wetting_only else 0.988,
                          top=0.775 if standalone else 0.90,
                          bottom=0.125 if standalone else 0.145)

    # ---------------------------------------------------------------- 1. wetting
    ax = panel(fig, gs, 0, 36.5, 40.5, "" if wetting_only else "1 — wetting",
               cap("dry, the pad is an antenna; water lands and that stops"),
               ylim=(-1.15, 1.95))
    ax.set_yticks([0.0, 0.5, 1.0, 1.5])
    ax.axvline(T_DROP, color=C_EVT, lw=1.4)
    ax.text(T_DROP + 0.06, 1.88, "droplet lands\nt = 38.13 s", color=C_EVT,
            fontsize=9 * TS, fontweight="bold", va="top", linespacing=1.3)
    ax.set_ylabel("pad-amplifier output  (V)", color=INK2, fontsize=10.5 * TS)

    ins = ax.inset_axes([0.28, 0.08, 0.68, 0.235])
    mi = (t >= 30) & (t < 50)
    ins.plot(t[mi], 1e3 * rms[mi], color=C_PAD, lw=1.2)
    ins.axvline(T_DROP, color=C_EVT, lw=1.0)
    ins.set_xlim(30, 50)
    ins.set_ylim(0, 170)
    ins.set_yticks([0, 70, 140])
    ins.set_xticks([30, 35, 40, 45, 50])
    small(ins)
    ins.text(0.0, 1.05, nm("58 Hz pickup, 30–50 s:  %.0f → %.0f mV rms",
                           "pickup, %.0f → %.0f mV rms") % (HUM_DRY, HUM_WET),
             transform=ins.transAxes, color=INK2, fontsize=8 * TS,
             bbox=dict(fc="white", ec="none", pad=1.5))

    if wetting_only:
        return fig

    # --------------------------------------------------------- 2. the stable point
    ax = panel(fig, gs, 1, 38.5, 44.3,
               nm("2 — it settles, and stays quiet", "2 — settling"),
               cap("output holds %.3f V for 5 s; %.0f mV rms" % (LVL, HUM_WET)))
    ax.axhline(LVL, color=C_PAD, lw=0.9, ls="--", alpha=0.6)
    ax.annotate("settled to within 20 mV\n1.0 s after the droplet",
                xy=(39.15, LVL), xytext=(39.5, 1.86), fontsize=8.5 * TS, color=INK2,
                va="top", linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))

    ins = ax.inset_axes([0.10, 0.06, 0.53, 0.26])
    mi = (t >= 41.0) & (t < 43.0)
    ins.plot(t[mi], 1e3 * (pad[mi] - LVL), color=C_PAD, lw=0.7)
    ins.set_xlim(41, 43)
    ins.set_ylim(-40, 40)
    ins.set_yticks([-30, 0, 30])
    ins.set_xticks([41, 42, 43])
    small(ins)
    ins.text(0.0, 1.05, nm("same trace, 20× closer  (mV about the level)",
                           "20× closer  (mV)"),
             transform=ins.transAxes, color=INK2, fontsize=8 * TS,
             bbox=dict(fc="white", ec="none", pad=1.5))

    # -------------------------------------------------------------- 3. saline in
    ax = panel(fig, gs, 2, 44.0, 48.0,
               nm("3 — saline, and the output signal", "3 — saline"),
               cap("the salt drives the output +%.0f mV, up to the rail"
                   % (1e3 * (RAIL - V0))))
    ax.axhline(RAIL, color=C_EVT, lw=1.0, ls="--", alpha=0.7)
    ax.text(47.95, RAIL + 0.02, "positive rail 1.809 V", color=C_EVT,
            fontsize=8.5 * TS, va="bottom", ha="right")
    ax.axvspan(T_SALT_A, T_SALT_B, color=C_EVT, alpha=0.055, lw=0)
    ax.axvline(T_SALT_A, color=C_EVT, lw=1.4)
    ax.text(T_SALT_A + 0.07, 0.10, "saline in\n44.3 → 46.9 s", color=C_EVT,
            fontsize=9 * TS, fontweight="bold", va="bottom", linespacing=1.3)
    ax.annotate("", xy=(44.62, RAIL), xytext=(44.62, V0),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2))
    ax.text(44.72, (RAIL + V0) / 2, "+%.0f mV\nin 2.6 s" % (1e3 * (RAIL - V0)),
            color=INK2, fontsize=9 * TS, va="center", linespacing=1.3)
    if standalone:
        ax.text(0.97, 0.34, "then it stays on the rail:\n99.8 % of the next 25 s,\n"
                            "5 mV rms — the output is\nsaturated, so a bigger salt\n"
                            "step would not show",
                transform=ax.transAxes, ha="right", va="top", color=INK2,
                fontsize=8.5 * TS, linespacing=1.4)

    if not standalone:
        return fig
    fig.suptitle("TiO₂ water pad — output of the on-chip pad amplifier (scope ch2)",
                 x=0.052, y=0.975, ha="left", fontsize=14.5 * TS,
                 fontweight="bold", color=INK)
    fig.text(0.052, 0.905, "one continuous 1 kHz record, scope_20260829_094236.csv."
             "   The second amplifier (ch1, jack input) is not driven here and is not shown.",
             ha="left", fontsize=9.5 * TS, color=INK2)

    return fig


# The standalone row is the wetlab handoff figure; the report keeps only its first
# panel -- the saline phase of this record is a saturation (Sec. 4.6) and the good
# saline measurements are their own figures.
for stem, figw, figh, ts, alone, wet1, exts in [
        (OUT, 15.0, 5.4, 1.0, True, False, ("png", "pdf")),
        (OUT + "_report", 5.4, 4.2, 1.0, False, True, ("pdf",))]:
    fig = build(figw, figh, ts, standalone=alone, wetting_only=wet1)
    for ext in exts:
        fig.savefig("%s.%s" % (stem, ext), dpi=150, facecolor="white")
        print("wrote %s.%s" % (stem, ext))
    plt.close(fig)

# ------------------------------------------------- numbers for the handoff note
print("\npad-amplifier output (ch2)")
for lab, a, b in [("dry       0-13 s", 0, 13),
                  ("wet      40-44 s", 40, 44),
                  ("saline   48-72 s", 48, 72)]:
    m = (t >= a) & (t < b)
    print("  %-17s %.4f V   %5.1f mV rms   peak-to-peak %.3f V"
          % (lab, np.median(pad[m]), 1e3 * np.nanmedian(rms[m]), pad[m].ptp()))
print("  droplet at %.2f s, settled to within 20 mV of %.3f V in 1.02 s" % (T_DROP, LVL))
print("  saline %.3f -> %.3f V  (+%.0f mV in 2.6 s), then %.1f %% of samples on the rail"
      % (V0, RAIL, 1e3 * (RAIL - V0), 100 * (pad[t >= 48] > 1.79).mean()))
