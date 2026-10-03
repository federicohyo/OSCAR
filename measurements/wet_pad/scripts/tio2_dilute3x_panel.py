#!/usr/bin/env python3
"""The 3x-diluted re-run: two injections that recover.

scope_20260829_103015.csv, 1 kHz, 29.3 s, biases
data/biases/LNA_chip0_pad_wet_diluted3x.biases (lna_iref = 1.157 V).

CHANNEL: ch2 = output of the PAD amplifier, input the exposed TiO2 pad. That is
the measurement and the only trace here. ch1 (the connector-fed amplifier) is NOT
usable as a control on this bench -- the two channels cross-talk inside the ESP
digitiser, so ch1 follows ch2 whatever the pad does. It is not plotted.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "measurements/wet_pad/data/scope_20260829_103015.csv"
OUT = "measurements/wet_pad/figures/tio2_dilute3x"
FS = 1000.0
GAIN = 268.0                   # measured at Viref = 1.079 V, NOT at the 1.157 V here
TS = 1.0                       # type scale, set by build()

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_PAD, C_EVT = "#c05621", "#9b2c2c"

d = np.genfromtxt(CSV, delimiter=",", names=True)
t = (d["sample_index"] - d["sample_index"][0]) / FS
pad = d["volts_ch2"]

T1, T2 = 4.308, 16.985


# The raw trace swings tens of mV sample to sample, so "back within 10 % of the
# step" is a threshold buried in the noise, and the raw median sits a few mV above
# the trace's actual centre. Judge both the baseline and the recovery on a 21 ms
# smoothed trace, against the spread of that same trace over a quiet stretch.
SM = np.convolve(pad, np.ones(21) / 21, "same")
QUIET = (t >= 20) & (t < 29)
BASE = np.median(SM[QUIET])
SIG = SM[QUIET].std()
# The smoothed baseline still wanders a few mV over tens of seconds, so a 3-sigma
# band is finer than the trace is stationary. Call it recovered at a flat 20 mV --
# about 10 sigma, and 5-10 % of either step.
TOL = 0.020
THR = BASE - TOL


def event(a, hold=0.10):
    """Depth below baseline, and when the trace has SETTLED back at it.

    Each injection is a short burst rather than one dip, so the first sample back
    above threshold is too generous -- it is satisfied between dips of one burst.
    Settled means back within TOL of baseline and staying there for `hold`
    seconds."""
    m = (t >= a - 0.05) & (t < a + 2.0)
    x, tt = SM[m], t[m]
    i = np.argmin(x)
    k = int(hold * FS)
    run = np.convolve((x > THR).astype(float), np.ones(k), "valid")
    j = np.where(run[i:] >= k - 0.5)[0]
    return 1e3 * (BASE - pad[m].min()), 1e3 * (tt[i + j[0]] - tt[i])


D1, R1 = event(4.30)
D2, R2 = event(16.98)


def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9 * TS)


def build(figw, figh, fontscale, standalone=True):
    global TS
    TS = fontscale
    cap = (lambda x: x) if standalone else (lambda x: None)
    nm = (lambda long, short: long if standalone else short)
    fig = plt.figure(figsize=(figw, figh))
    gs = fig.add_gridspec(1, 3, wspace=0.16,
                          left=0.052 if standalone else 0.085, right=0.988,
                          top=0.775 if standalone else 0.90,
                          bottom=0.125 if standalone else 0.145)

    def head(ax, name, caption):
        ax.set_title(name, loc="left", color=INK, fontsize=12.5 * TS,
                     fontweight="bold", pad=24 if caption else 8)
        if caption:
            ax.text(0.0, 1.015, caption, transform=ax.transAxes, color=INK2,
                    fontsize=9.5 * TS)

    # ---- 1: the whole record ------------------------------------------------
    ax = fig.add_subplot(gs[0])
    ax.plot(t, pad, color=C_PAD, lw=0.6)
    ax.axhline(BASE, color=INK2, lw=0.8, ls="--", alpha=0.6)
    if standalone:
        ax.text(8.0, 1.02, "baseline %.4f V" % BASE, color=INK2,
                fontsize=8.5 * TS, ha="left", va="bottom")
    for tt, lab, dep in ((T1, "1", D1), (T2, "2", D2)):
        ax.axvline(tt, color=C_EVT, lw=1.0, alpha=0.55)
        ax.text(tt + 0.4, 1.02, "%s\n%+.0f mV" % (lab, -dep), color=C_EVT,
                fontsize=9 * TS, fontweight="bold", va="bottom", linespacing=1.3)
    ax.set_xlim(0, t[-1])
    ax.set_ylim(1.00, 1.53)
    ax.set_ylabel("pad-amplifier output  (V)", color=INK2, fontsize=10.5 * TS)
    ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
    dress(ax)
    head(ax, "1 — two injections",
         cap("graded, and the baseline comes back both times"))

    # ---- 2, 3: the two events ----------------------------------------------
    for k, (tc, dep, rec, name, sub) in enumerate(
            [(T1, D1, R1, "2 — first injection", "the smaller aliquot"),
             (T2, D2, R2, "3 — second injection", "the larger aliquot")], start=1):
        ax = fig.add_subplot(gs[k])
        m = (t >= tc - 0.10) & (t < tc + 0.50)
        ax.plot((t[m] - tc) * 1e3, pad[m], color=C_PAD, lw=1.3)
        ax.axhline(BASE, color=INK2, lw=0.8, ls="--", alpha=0.6)
        lo = BASE - dep / 1e3
        ax.annotate("", xy=(-60, lo), xytext=(-60, BASE),
                    arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2))
        ax.text(-52, (BASE + lo) / 2, "%+.0f mV" % -dep, color=INK2,
                fontsize=9.5 * TS, va="center", fontweight="bold")
        ax.axvspan(0, rec, color=C_EVT, alpha=0.09, lw=0)
        ax.text(rec + 15, lo + 0.02, nm("settled back\nin %.0f ms",
                                        "settled\nin %.0f ms") % rec,
                color=C_EVT, fontsize=9 * TS, fontweight="bold",
                va="bottom", linespacing=1.3)
        ax.set_xlim(-100, 500)
        ax.set_ylim(1.00, 1.53)
        ax.set_xlabel("time from the dip  (ms)", color=INK2, fontsize=10 * TS)
        dress(ax)
        head(ax, name, cap("%s: %+.0f mV, no residual offset" % (sub, -dep)))
        if k == 1 and standalone:
            ax.annotate("50 Hz mains hum on the droplet\n(the hand and the needle "
                        "make it worse)", xy=(120, 1.425), xytext=(175, 1.34),
                        fontsize=8.5 * TS, color=INK2, linespacing=1.3,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))

    if not standalone:
        return fig
    fig.suptitle("TiO₂ pad, saline diluted 3× and the biases moved off the clamp",
                 x=0.052, y=0.975, ha="left", fontsize=14.5 * TS,
                 fontweight="bold", color=INK)
    fig.text(0.052, 0.905, "scope_20260829_103015.csv, one continuous 1 kHz record, "
             "lna_iref = 1.157 V.  Two injections into the droplet: both are graded, "
             "both recover, nothing saturates.",
             ha="left", fontsize=9.5 * TS, color=INK2)
    return fig


def build_long(figw=7.16, figh=2.6):
    """Two-column layout for the ISCAS27 paper: the whole record spans both
    columns, the two injection zooms sit in it as insets (left, right)."""
    global TS
    TS = 0.72
    fig = plt.figure(figsize=(figw, figh))
    ax = fig.add_axes([0.065, 0.17, 0.925, 0.77])

    ax.plot(t, pad, color=C_PAD, lw=0.5)
    ax.axhline(BASE, color=INK2, lw=0.7, ls="--", alpha=0.6)
    ax.text(t[-1] - 0.3, 1.50, "baseline %.4f V" % BASE, color=INK2,
            fontsize=8.5 * TS, ha="right", va="bottom",
            bbox=dict(fc="white", ec="none", pad=0.6), zorder=6)
    for tt in (T1, T2):
        ax.axvline(tt, color=C_EVT, lw=0.8, alpha=0.5)
    ax.set_xlim(0, t[-1])
    ax.set_ylim(1.02, 1.97)              # headroom above the trace: the insets
    ax.set_yticks([1.1, 1.2, 1.3, 1.4, 1.5])
    ax.set_ylabel("pad-amplifier output  (V)", color=INK2, fontsize=10.5 * TS)
    ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
    dress(ax)
    ax.text(0.995, 0.015, "(a)", transform=ax.transAxes, fontsize=10.5 * TS,
            va="bottom", ha="right")

    for tag, x0, tc, dep, rec in (("(b)", 0.085, T1, D1, R1),
                                  ("(c)", 0.565, T2, D2, R2)):
        axi = ax.inset_axes([x0, 0.665, 0.415, 0.33], facecolor="white")
        axi.set_zorder(5)
        axi.patch.set_alpha(1.0)
        m = (t >= tc - 0.10) & (t < tc + 0.50)
        axi.plot((t[m] - tc) * 1e3, pad[m], color=C_PAD, lw=0.9)
        axi.axhline(BASE, color=INK2, lw=0.7, ls="--", alpha=0.6)
        lo = BASE - dep / 1e3
        axi.annotate("", xy=(-60, lo), xytext=(-60, BASE),
                     arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.0))
        axi.text(-52, (BASE + lo) / 2, "%+.0f mV" % -dep, color=INK2,
                 fontsize=9.5 * TS, va="center", fontweight="bold")
        axi.axvspan(0, rec, color=C_EVT, alpha=0.09, lw=0)
        axi.text(rec + 18, lo + 0.02, "settled in %.0f ms" % rec, color=C_EVT,
                 fontsize=9 * TS, va="bottom", fontweight="bold")
        axi.set_xlim(-100, 500)
        axi.set_ylim(1.00, 1.53)
        axi.set_xlabel("ms from the dip", color=INK2, fontsize=9.5 * TS)
        axi.tick_params(labelsize=8 * TS, colors=INK2, length=2.5)
        axi.text(0.97, 0.03, tag, transform=axi.transAxes,
                 fontsize=10.5 * TS, va="bottom", ha="right")
        for s in axi.spines.values():
            s.set_edgecolor(MUTED)
    return fig


for stem, figw, figh, ts, alone, exts in [
        (OUT, 15.0, 5.4, 1.0, True, ("png", "pdf")),
        (OUT + "_report", 9.6, 4.4, 1.25, False, ("pdf",))]:
    fig = build(figw, figh, ts, standalone=alone)
    for ext in exts:
        fig.savefig("%s.%s" % (stem, ext), dpi=150, facecolor="white")
        print("wrote %s.%s" % (stem, ext))
    plt.close(fig)

# ISCAS27 two-column variant with the zooms as insets inside the long record
fig = build_long()
for ext in ("png", "pdf"):
    p = "measurements/wet_pad/figures/fig17_tio2_dilute3x.%s" % ext
    fig.savefig(p, dpi=150, facecolor="white")
    print("wrote", p)
plt.close(fig)

print("\nbaseline %.4f V; smoothed baseline spread %.1f mV rms, "
      "settling threshold %.4f V (%.0f mV, %.1f sigma)"
      % (BASE, 1e3 * SIG, THR, 1e3 * TOL, TOL / SIG))
for lab, tc, dep, rec in (("1", T1, D1, R1), ("2", T2, D2, R2)):
    print("injection %s at %6.3f s: %+7.1f mV out, settled in %3.0f ms"
          " | provisional input-referred (/%.0f, wrong Viref): %+.0f uV"
          % (lab, tc, -dep, rec, GAIN, -1e3 * dep / GAIN))
