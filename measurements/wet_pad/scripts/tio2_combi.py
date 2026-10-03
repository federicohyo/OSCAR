#!/usr/bin/env python3
"""TiO2 wet-transduction panels.

Two output PDFs, side by side in one figure row:
  fig16_tio2_wetting    -- (a) wetting of the TiO2 pad
                           (scope_20260829_094236.csv, ch2 = pad amp);
                           NO pickup inset (it covered the signal), the
                           138 -> 7 mV rms numbers are a text note.
  fig17_tio2_dilute3x   -- (b) the 3x-diluted saline record
                           (scope_20260829_103015.csv), shorter with
                           larger fonts; injection zooms (c), (d) sit
                           high, clear of the trace.

Panel letters (a)/(b) come from subcaptions, so they are left undrawn
here; only the inner zoom tags (c)/(d) are.  Both figures are drawn at
their exact print size (4.8 and 2.3 in wide, 1.75 in tall), so fonts are
final-size -- keep the same scale as the panel linewidths.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WET_CSV = "measurements/wet_pad/data/scope_20260829_094236.csv"
DIL_CSV = "measurements/wet_pad/data/scope_20260829_103015.csv"
OUT_A = "measurements/wet_pad/figures/fig16_tio2_wetting"
OUT_B = "measurements/wet_pad/figures/fig17_tio2_dilute3x"
FS = 1000.0
TS = 0.85                     # printed at final size

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_PAD, C_EVT = "#c05621", "#9b2c2c"


def load(csv):
    d = np.genfromtxt(csv, delimiter=",", names=True)
    t = (d["sample_index"] - d["sample_index"][0]) / FS
    return t, d["volts_ch2"]


def boxcar(x, sec):
    k = int(sec * FS)
    return np.convolve(x, np.ones(k) / k, mode="same")


def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9 * TS)


def small(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.grid(True, color="#ececec", lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=7.5 * TS, length=2.5)


# ------------------------------------------------------------ wetting run
tw, padw = load(WET_CSV)
rmsw = np.sqrt(np.maximum(boxcar((padw - boxcar(padw, 0.2)) ** 2, 0.5), 0.0))
edge = int(0.6 * FS)
rmsw[:edge] = np.nan
rmsw[-edge:] = np.nan
T_DROP = 38.13
HUM_DRY = 1e3 * np.nanmedian(rmsw[(tw >= 0) & (tw < 13)])
HUM_WET = 1e3 * np.nanmedian(rmsw[(tw >= 40) & (tw < 44)])

figA = plt.figure(figsize=(2.3, 1.75))
ax = figA.add_axes([0.205, 0.19, 0.76, 0.75])
m = (tw >= 36.5) & (tw < 40.5)
ax.plot(tw[m], padw[m], color=C_PAD, lw=1.0)
ax.set_xlim(36.5, 40.5)
ax.set_ylim(-1.15, 1.95)
ax.set_yticks([0.0, 0.5, 1.0, 1.5])
ax.axvline(T_DROP, color=C_EVT, lw=1.2)
ax.text(T_DROP + 0.06, -0.02, "droplet lands\nt = 38.13 s", color=C_EVT,
        fontsize=8.5 * TS, fontweight="bold", va="top", ha="left",
        linespacing=1.3)
ax.set_ylabel("pad-amp output  (V)", color=INK2, fontsize=10.5 * TS)
ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
dress(ax)

for ext in ("png", "pdf"):
    p = "%s.%s" % (OUT_A, ext)
    figA.savefig(p, dpi=150, facecolor="white")
    print("wrote", p)

# ------------------------------------------------------ dilute-3x run
td, padd = load(DIL_CSV)
T1, T2 = 4.308, 16.985
SM = np.convolve(padd, np.ones(21) / 21, "same")
QUIET = (td >= 20) & (td < 29)
BASE = np.median(SM[QUIET])
THR = BASE - 0.020


def event(a, hold=0.10):
    m = (td >= a - 0.05) & (td < a + 2.0)
    x, tt = SM[m], td[m]
    i = np.argmin(x)
    k = int(hold * FS)
    run = np.convolve((x > THR).astype(float), np.ones(k), "valid")
    j = np.where(run[i:] >= k - 0.5)[0]
    return 1e3 * (BASE - padd[m].min()), 1e3 * (tt[i + j[0]] - tt[i])


D1, R1 = event(4.30)
D2, R2 = event(16.98)

figB = plt.figure(figsize=(4.8, 1.75))
ax = figB.add_axes([0.105, 0.19, 0.885, 0.72])
ax.plot(td, padd, color=C_PAD, lw=0.5)
ax.axhline(BASE, color=INK2, lw=0.7, ls="--", alpha=0.6)
ax.text(td[-1] - 0.3, 1.30, "baseline %.4f V" % BASE, color=INK2,
        fontsize=8.5 * TS, ha="right", va="bottom",
        bbox=dict(fc="white", ec="none", pad=0.6), zorder=6)
for tt in (T1, T2):
    ax.axvline(tt, color=C_EVT, lw=0.8, alpha=0.5)
ax.set_xlim(0, td[-1])
ax.set_ylim(1.02, 2.06)              # headroom above the trace: the insets
ax.set_yticks([1.1, 1.2, 1.3, 1.4, 1.5])
ax.set_ylabel("pad-amp output  (V)", color=INK2, fontsize=10.5 * TS)
ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
dress(ax)

for tag, x0, tc, dep, rec in (("(c)", 0.075, T1, D1, R1),
                              ("(d)", 0.560, T2, D2, R2)):
    axi = ax.inset_axes([x0, 0.68, 0.405, 0.29], facecolor="white")
    axi.set_zorder(5)
    axi.patch.set_alpha(1.0)
    mm = (td >= tc - 0.10) & (td < tc + 0.50)
    axi.plot((td[mm] - tc) * 1e3, padd[mm], color=C_PAD, lw=0.9)
    axi.axhline(BASE, color=INK2, lw=0.7, ls="--", alpha=0.6)
    lo = BASE - dep / 1e3
    axi.annotate("", xy=(-60, lo), xytext=(-60, BASE),
                 arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.0))
    if tag == "(c)":
        # step label at the 1 V line, below the dip
        axi.text(-52, 1.02, "%+.0f mV" % -dep, color=INK2,
                 fontsize=9.5 * TS, va="bottom", fontweight="bold")
    else:
        # step label stacked on the "settled in" text, right of the dip
        axi.text(rec + 18, lo + 0.135, "%+.0f mV" % -dep, color=INK2,
                 fontsize=9.5 * TS, va="bottom", ha="left",
                 fontweight="bold")
    axi.axvspan(0, rec, color=C_EVT, alpha=0.09, lw=0)
    axi.text(rec + 18, lo + 0.02, "settled in %.0f ms" % rec, color=C_EVT,
             fontsize=9 * TS, va="bottom", fontweight="bold")
    axi.set_xlim(-100, 500)
    axi.set_ylim(1.00, 1.53)
    axi.set_xlabel("ms from the dip", color=INK2, fontsize=9.5 * TS,
                   labelpad=0.5)
    small(axi)
    # tag above the inset, at its top right corner
    axi.text(1.0, 1.03, tag, transform=axi.transAxes,
             fontsize=10 * TS, va="bottom", ha="right", fontweight="bold")

for ext in ("png", "pdf"):
    p = "%s.%s" % (OUT_B, ext)
    figB.savefig(p, dpi=150, facecolor="white")
    print("wrote", p)
