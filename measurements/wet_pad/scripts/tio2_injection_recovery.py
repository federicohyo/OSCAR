#!/usr/bin/env python3
"""One large saline injection, and the several seconds it takes to come back.

scope_20260829_110950-saline-injection&recovery.csv, 1 kHz, 31.4 s.

CHANNEL: ch2 = output of the PAD amplifier, input the exposed TiO2 pad. ch1 is
not plotted -- the two scope channels cross-talk inside the ESP front end, so the
connector-fed amplifier is not a control for this one.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = ("measurements/wet_pad/data/"
       "scope_20260829_110950-saline-injection&recovery.csv")
OUT = "measurements/wet_pad/figures/tio2_injection_recovery"
FS = 1000.0
TS = 1.0

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_PAD, C_EVT, C_FIT = "#c05621", "#9b2c2c", "#2b6cb0"

d = np.genfromtxt(CSV, delimiter=",", names=True)
t = (d["sample_index"] - d["sample_index"][0]) / FS
pad = d["volts_ch2"]


def smooth(x, k):
    """Boxcar, with the convolve('same') edge artefacts blanked."""
    y = np.convolve(x, np.ones(k) / k, mode="same")
    y[:k] = np.nan
    y[-k:] = np.nan
    return y


# 101 ms nulls the 50 Hz mains pickup and still resolves a multi-second recovery
SM = smooth(pad, 101)
PRE = (t >= 1) & (t < 8)
BASE = np.nanmedian(SM[PRE])
SIG = np.nanstd(SM[PRE])

reg = (t > 8.5) & (t < 12)
I = int(np.nanargmin(np.where(reg, SM, np.nan)))
T_MIN = t[I]
T_ON = t[np.where((t > 8) & (SM < BASE - 0.020))[0][0]]
DEPTH_RAW = 1e3 * (BASE - pad.min())
DEPTH_SM = 1e3 * (BASE - SM[I])
FALL = 1e3 * (T_MIN - T_ON)


def settle(tol, hold=0.5):
    ok = np.nan_to_num(SM, nan=-9.0) > BASE - tol
    k = int(hold * FS)
    run = np.convolve(ok[I:].astype(float), np.ones(k), "valid")
    return t[I + np.where(run >= k - 0.5)[0][0]] - T_MIN


S20, S10 = settle(0.020), settle(0.010)
RESID = 1e3 * (np.nanmedian(SM[(t >= 25) & (t < 31)]) - BASE)


def tail_tau(a, b):
    m = (t > T_MIN + a) & (t < T_MIN + b)
    y = BASE - SM[m]
    ok = y > 0.005
    q = np.polyfit(t[m][ok] - T_MIN, np.log(y[ok]), 1)
    return -1.0 / q[0], np.exp(q[1])


TAU_E, A_E = tail_tau(0.3, 6.0)
TAU_L, A_L = tail_tau(1.0, 9.0)


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
    gs = fig.add_gridspec(1, 3, wspace=0.20,
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
    ax.plot(t, pad, color=C_PAD, lw=0.5, alpha=0.55)
    ax.plot(t, SM, color=C_PAD, lw=1.6)
    ax.axhline(BASE, color=INK2, lw=0.9, ls="--", alpha=0.7)
    ax.axvspan(T_MIN, T_MIN + S20, color=C_EVT, alpha=0.08, lw=0)
    ax.axvline(T_ON, color=C_EVT, lw=1.3)
    ax.text(T_ON + 0.4, 0.93, "saline in\nt = %.2f s" % T_ON, color=C_EVT,
            fontsize=9 * TS, fontweight="bold", va="bottom", linespacing=1.3)
    ax.text(T_MIN + S20 + 0.8, BASE - 0.17,
            nm("back within 20 mV\nafter %.1f s", "within 20 mV\nafter %.1f s") % S20,
            color=C_EVT, fontsize=9 * TS, fontweight="bold", va="top",
            linespacing=1.3)
    ax.set_xlim(0, t[-1])
    ax.set_ylim(0.85, 1.66)
    ax.set_ylabel("pad-amplifier output  (V)", color=INK2, fontsize=10.5 * TS)
    ax.set_xlabel("time in the run  (s)", color=INK2, fontsize=10 * TS)
    dress(ax)
    head(ax, "1 — one injection", cap("baseline %.4f V, and it comes all the way back"
                                      % BASE))

    # ---- 2: the edge --------------------------------------------------------
    ax = fig.add_subplot(gs[1])
    m = (t >= T_ON - 0.4) & (t < T_ON + 1.6)
    ax.plot((t[m] - T_ON) * 1e3, pad[m], color=C_PAD, lw=0.7, alpha=0.55)
    ax.plot((t[m] - T_ON) * 1e3, SM[m], color=C_PAD, lw=1.8)
    ax.axhline(BASE, color=INK2, lw=0.9, ls="--", alpha=0.7)
    ax.annotate("", xy=(-250, BASE - DEPTH_RAW / 1e3), xytext=(-250, BASE),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2))
    ax.text(-230, BASE - DEPTH_RAW / 2e3, "%+.0f mV" % -DEPTH_RAW, color=INK2,
            fontsize=9.5 * TS, va="center", fontweight="bold")
    ax.axvspan(0, FALL, color=C_EVT, alpha=0.10, lw=0)
    ax.annotate("falls in\n%.0f ms" % FALL, xy=(FALL / 2, 0.995),
                xytext=(640, 0.90), color=C_EVT, fontsize=9 * TS,
                fontweight="bold", va="bottom", linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color=C_EVT, lw=1))
    ax.set_xlim(-400, 1600)
    ax.set_ylim(0.85, 1.66)
    ax.set_xlabel("time from the injection  (ms)", color=INK2, fontsize=10 * TS)
    dress(ax)
    head(ax, "2 — the edge", cap("fast in, and far past the linear range"))

    # ---- 3: the recovery ---------------------------------------------------
    # The rising edge itself, on the same volts axis as the other two panels, so
    # it can be read against them. Just the trace and the baseline: the fitted
    # time constants are quoted in the text, not drawn over the data.
    ax = fig.add_subplot(gs[2])
    m = (t > T_MIN - 0.4) & (t < T_MIN + 12)
    ax.plot(t[m] - T_MIN, pad[m], color=C_PAD, lw=0.5, alpha=0.5)
    ax.plot(t[m] - T_MIN, SM[m], color=C_PAD, lw=1.8)
    ax.axhline(BASE, color=INK2, lw=0.9, ls="--", alpha=0.7)
    ax.text(11.8, BASE + 0.015, "baseline", color=INK2, fontsize=8.5 * TS,
            ha="right", va="bottom")
    ax.set_xlim(-0.4, 12)
    ax.set_ylim(0.85, 1.66)
    ax.set_xlabel("time from the minimum  (s)", color=INK2, fontsize=10 * TS)
    dress(ax)
    head(ax, "3 — the recovery", cap("the whole rising edge, all the way back"))

    if not standalone:
        return fig
    fig.suptitle("TiO₂ pad: one saline injection, and the recovery",
                 x=0.052, y=0.975, ha="left", fontsize=14.5 * TS,
                 fontweight="bold", color=INK)
    fig.text(0.052, 0.905, "scope_20260829_110950-saline-injection&recovery.csv, "
             "one continuous 1 kHz record.  Thin trace raw, thick trace smoothed over "
             "101 ms (which nulls the 50 Hz mains pickup on the droplet).",
             ha="left", fontsize=9.5 * TS, color=INK2)
    return fig


for stem, figw, figh, ts, alone, exts in [
        (OUT, 15.0, 5.4, 1.0, True, ("png", "pdf")),
        (OUT + "_report", 9.6, 4.4, 1.25, False, ("pdf",))]:
    fig = build(figw, figh, ts, standalone=alone)
    for ext in exts:
        fig.savefig("%s.%s" % (stem, ext), dpi=150, facecolor="white")
        print("wrote %s.%s" % (stem, ext))
    plt.close(fig)

print("\nbaseline %.4f V, pre-injection spread %.2f mV rms (101 ms smoothing)" % (BASE, 1e3 * SIG))
print("injection at %.2f s; minimum at %.2f s -> falls in %.0f ms" % (T_ON, T_MIN, FALL))
print("depth %.0f mV raw, %.0f mV smoothed" % (DEPTH_RAW, DEPTH_SM))
print("settles to 20 mV in %.2f s, to 10 mV in %.2f s; residual after %+.1f mV"
      % (S20, S10, RESID))
print("tail tau %.2f s over 0.3-6 s, %.2f s over 1-9 s -- not a single exponential"
      % (TAU_E, TAU_L))
