#!/usr/bin/env python3
"""The 09:51:21 re-run: ch2 (the pad node) goes to VDD again, in 0.8 s.

ch1 = LNA output, ch2 = LNA input pin (the pad node) -- per LNA_bringup.sh.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "measurements/wet_pad/data/scope_20260829_%s.csv"
CSV = DATA % "095121"
OUT = "measurements/wet_pad/figures/tio2_rerun_20260829_095121.png"
RAIL = 1.809

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_OUT, C_IN, C_EVT = "#2b6cb0", "#c05621", "#9b2c2c"

def load(p):
    d = np.genfromtxt(p, delimiter=",", names=True)
    return (d["sample_index"] - d["sample_index"][0]) / 1000.0, d["volts"], d["volts_ch2"]

t, ch1, ch2 = load(CSV)
fs = 1000.0

def boxcar(x, sec):
    k = int(sec * fs)
    return np.convolve(x, np.ones(k) / k, mode="same")

ac = ch2 - boxcar(ch2, 0.2)
rms = np.sqrt(np.maximum(boxcar(ac ** 2, 0.5), 0.0))
edge = int(0.6 * fs)
rms[:edge] = np.nan; rms[-edge:] = np.nan

T_TOUCH, T_RAIL = 9.95, 10.97

def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9)

def marks(ax):
    ax.axvspan(T_TOUCH, T_RAIL, color=C_EVT, alpha=0.10, lw=0)
    ax.axvline(T_TOUCH, color=C_EVT, lw=1.4)
    ax.axvline(T_RAIL, color=C_EVT, lw=1.0, ls="--")

fig = plt.figure(figsize=(14, 9.5))
gs = fig.add_gridspec(4, 2, height_ratios=[1.0, 1.15, 0.8, 1.15],
                      hspace=0.5, wspace=0.2,
                      left=0.075, right=0.985, top=0.905, bottom=0.06)

ax = fig.add_subplot(gs[0, :])
ax.plot(t, ch1, color=C_OUT, lw=0.5)
marks(ax); dress(ax)
ax.set_xlim(0, t[-1]); ax.set_ylim(0.3, 1.85)
ax.set_ylabel("volts", color=INK2, fontsize=10)
ax.set_title("ch1 — LNA output", loc="left", color=INK, fontsize=11.5, fontweight="bold")
ax.text(T_TOUCH, 1.88, "contact  t = 9.95 s", color=C_EVT, fontsize=9,
        fontweight="bold", ha="center", va="bottom")
ax.text(T_RAIL, 1.88, "pad node at VDD  t = 10.97 s", color=C_EVT, fontsize=9,
        fontweight="bold", ha="left", va="bottom")

ax = fig.add_subplot(gs[1, :])
ax.plot(t, ch2, color=C_IN, lw=0.5)
ax.axhline(RAIL, color=C_EVT, lw=1.0, ls="--", alpha=0.7)
ax.text(0.15, RAIL + 0.012, "VDD rail 1.809 V", color=C_EVT, fontsize=8.5, va="bottom")
marks(ax); dress(ax)
ax.set_xlim(0, t[-1]); ax.set_ylim(0.4, 1.9)
ax.set_ylabel("volts", color=INK2, fontsize=10)
ax.set_title("ch2 — LNA input pin = the TiO₂ pad node", loc="left",
             color=INK, fontsize=11.5, fontweight="bold")
ax.annotate("damp pad, 1.42 V\n27 mV rms of 58.4 Hz", xy=(5, 1.42), xytext=(2.0, 0.62),
            fontsize=8.5, color=INK2,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
ax.annotate("pinned, 5 mV rms — amplifier input out of range",
            xy=(14, RAIL), xytext=(11.6, 1.45), fontsize=8.5, color=INK2,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))

ax = fig.add_subplot(gs[2, :])
ax.plot(t, rms * 1e3, color=C_IN, lw=1.4)
marks(ax); dress(ax)
ax.set_xlim(0, t[-1])
ax.set_ylabel("mV rms", color=INK2, fontsize=10)
ax.set_xlabel("time since start of file  (s)", color=INK2, fontsize=10)
ax.set_title("AC pickup on the pad node (running rms, >5 Hz)", loc="left",
             color=INK, fontsize=11.5, fontweight="bold")

ax = fig.add_subplot(gs[3, 0])
m = (t >= 9.6) & (t < 11.6)
ax.plot(t[m], ch1[m], color=C_OUT, lw=0.8)
ax.plot(t[m], ch2[m], color=C_IN, lw=0.8)
ax.axhline(RAIL, color=C_EVT, lw=0.9, ls="--", alpha=0.7)
marks(ax); dress(ax)
ax.set_xlim(9.6, 11.6); ax.set_ylim(0.3, 1.9)
ax.set_ylabel("volts", color=INK2, fontsize=10)
ax.set_xlabel("s", color=INK2, fontsize=9)
ax.set_title("zoom — 0.2 s bang, then a 0.8 s climb to the rail",
             loc="left", color=INK, fontsize=10.5, fontweight="bold")
ax.text(0.97, 0.10, "ch2 pad", transform=ax.transAxes, ha="right",
        color=C_IN, fontsize=9, fontweight="bold")
ax.text(0.97, 0.19, "ch1 out", transform=ax.transAxes, ha="right",
        color=C_OUT, fontsize=9, fontweight="bold")

# --- ch2 state across the whole morning --------------------------------------
ax = fig.add_subplot(gs[3, 1])
FILES = ["094145", "094155", "094158", "094232", "094236",
         "094617", "095116", "095121"]
lab, med, frac = [], [], []
for f in FILES:
    try:
        _, _, c2 = load(DATA % f)
    except OSError:
        continue
    lab.append("%s:%s:%s" % (f[:2], f[2:4], f[4:]))
    med.append(np.median(c2))
    frac.append(100.0 * (c2 > 1.79).mean())
x = np.arange(len(lab))
ax.bar(x, med, color=[C_EVT if p > 50 else C_IN for p in frac], width=0.62)
ax.axhline(RAIL, color=C_EVT, lw=1.0, ls="--", alpha=0.7)
dress(ax)
ax.set_xticks(x); ax.set_xticklabels(lab, rotation=45, ha="right", fontsize=8)
ax.set_ylim(0, 1.95)
ax.set_ylabel("median ch2  (V)", color=INK2, fontsize=10)
ax.set_title("pad node across the session — red = sat at VDD",
             loc="left", color=INK, fontsize=10.5, fontweight="bold")
for xi, p in zip(x, frac):
    ax.text(xi, 0.06, "%.0f%%" % p, ha="center", fontsize=7.5, color="white"
            if p > 50 else INK2, fontweight="bold")

fig.suptitle("TiO₂ pad re-run  —  scope_20260829_095121.csv (1 kHz, 16.3 s)",
             x=0.075, ha="left", fontsize=14, fontweight="bold", color=INK)
fig.savefig(OUT, dpi=140, facecolor="white")
print("wrote", OUT)
