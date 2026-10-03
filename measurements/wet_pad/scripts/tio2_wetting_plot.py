#!/usr/bin/env python3
"""Annotate the TiO2-pad wetting / saline-injection run.

ch1 = LNA output, ch2 = LNA input pin (the pad node) -- per LNA_bringup.sh.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "measurements/wet_pad/data/scope_20260829_094236.csv"
OUT = "measurements/wet_pad/figures/tio2_wetting_20260829_094236.png"

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_OUT, C_IN = "#2b6cb0", "#c05621"      # ch1 output (blue), ch2 pad node (orange)
C_EVT = "#9b2c2c"

d = np.genfromtxt(CSV, delimiter=",", names=True)
# board_seconds is quantised to 10 ms; sample_index is the honest 1 kHz clock
t = (d["sample_index"] - d["sample_index"][0]) / 1000.0
ch1, ch2 = d["volts"], d["volts_ch2"]
fs = 1000.0

# --- AC activity on the pad node: the wetting fingerprint ---------------------
# Running rms about a 0.2 s moving mean (so >~5 Hz survives), smoothed over 0.5 s.
# The dominant line in it is 58.4 Hz mains-ish pickup (checked by FFT).
def boxcar(x, sec):
    k = int(sec * fs)
    return np.convolve(x, np.ones(k) / k, mode="same")

ac = ch2 - boxcar(ch2, 0.2)
hum = np.sqrt(np.maximum(boxcar(ac ** 2, 0.5), 0.0))
edge = int(0.6 * fs)                      # convolve("same") edge artefacts
hum[:edge] = np.nan; hum[-edge:] = np.nan

def env(x, w):
    """min/max envelope so a 1 kHz trace stays honest when drawn 72 s wide."""
    n = len(x) // w
    r = x[: n * w].reshape(n, w)
    return r.min(1), r.max(1)

W = 25
n = len(t) // W
te = t[: n * W].reshape(n, W).mean(1)

EVENTS = [
    (16.6, 19.2, "contact tests\n(pad touched, then lifted)", MUTED, 0),
    (25.3, 26.3, "", MUTED, 0),
    (38.13, 39.3, "1. WETTING\ndroplet lands", C_EVT, 1),
    (44.3, 46.9, "2. SALINE INJECTION\npad node ramps to the rail", C_EVT, 0),
    (56.6, 58.4, "output-side bump\n(pad node unchanged)", MUTED, 1),
]

fig = plt.figure(figsize=(14, 10.5))
gs = fig.add_gridspec(4, 3, height_ratios=[1.15, 1.15, 0.85, 1.0],
                      hspace=0.45, wspace=0.22,
                      left=0.07, right=0.985, top=0.905, bottom=0.06)

def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9)

def bands(ax, label=True):
    for a, b, txt, col, _ in EVENTS:
        ax.axvspan(a, b, color=col, alpha=0.10 if col == C_EVT else 0.07, lw=0)
        ax.axvline(a, color=col, lw=1.4 if col == C_EVT else 1.0,
                   ls="-" if col == C_EVT else ":", alpha=0.9)

# ---- pane 1: LNA output, full run -------------------------------------------
ax = fig.add_subplot(gs[0, :])
lo, hi = env(ch1, W)
ax.fill_between(te, lo, hi, color=C_OUT, lw=0, alpha=0.85)
bands(ax)
ax.set_ylabel("volts", color=INK2, fontsize=10)
ax.set_title("ch1 — LNA output", loc="left", color=INK, fontsize=11.5, fontweight="bold")
ax.set_xlim(0, t[-1]); ax.set_ylim(0.3, 1.9)
dress(ax)
for a, b, txt, col, row in EVENTS:
    if txt:
        ax.text((a + b) / 2, 1.93 + 0.20 * row, txt, ha="center", va="bottom", fontsize=8.5,
                color=col if col == C_EVT else INK2,
                fontweight="bold" if col == C_EVT else "normal", linespacing=1.3)

# ---- pane 2: pad node, full run ---------------------------------------------
ax = fig.add_subplot(gs[1, :])
lo, hi = env(ch2, W)
ax.fill_between(te, lo, hi, color=C_IN, lw=0, alpha=0.85)
bands(ax)
ax.axhline(1.809, color=C_EVT, lw=1.0, ls="--", alpha=0.7)
ax.text(1.0, 1.815, "VDD rail 1.81 V", color=C_EVT, fontsize=8.5, va="bottom")
ax.set_ylabel("volts", color=INK2, fontsize=10)
ax.set_title("ch2 — LNA input pin = the TiO₂ pad node", loc="left",
             color=INK, fontsize=11.5, fontweight="bold")
ax.set_xlim(0, t[-1]); ax.set_ylim(0.0, 1.95)
dress(ax)

# ---- pane 3: the 58.4 Hz pickup envelope ------------------------------------
ax = fig.add_subplot(gs[2, :])
ax.plot(t, hum * 1e3, color=C_IN, lw=1.4)
bands(ax)
ax.set_ylabel("mV rms", color=INK2, fontsize=10)
ax.set_xlabel("time since start of file  (s)", color=INK2, fontsize=10)
ax.set_title("AC pickup on the pad node (running rms, >5 Hz; the line is 58.4 Hz) — "
             "the dry pad is an antenna, water kills it", loc="left", color=INK, fontsize=11.5, fontweight="bold")
ax.set_xlim(0, t[-1])
dress(ax)
ax.annotate("~140 mV rms\n(dry, floating)", xy=(6, 140), xytext=(2, 152),
            fontsize=8.5, color=INK2)
ax.annotate("~5 mV rms", xy=(50, 5), xytext=(50, 60), fontsize=8.5, color=INK2,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))

# ---- pane 4: three zooms ----------------------------------------------------
ZOOMS = [
    (37.3, 40.3, "1. wetting  —  t ≈ 38.13 s"),
    (43.5, 48.0, "2. injection  —  ramp 44.3 → 46.9 s"),
    (56.0, 59.0, "output bump  —  t ≈ 56.6 s"),
]
for j, (a, b, ttl) in enumerate(ZOOMS):
    ax = fig.add_subplot(gs[3, j])
    m = (t >= a) & (t < b)
    ax.plot(t[m], ch1[m], color=C_OUT, lw=0.7, alpha=0.85)
    ax.plot(t[m], ch2[m], color=C_IN, lw=0.7, alpha=0.85)
    ax.set_xlim(a, b); ax.set_ylim(0.0, 1.95)
    ax.set_title(ttl, loc="left", color=INK, fontsize=10, fontweight="bold")
    ax.set_xlabel("s", color=INK2, fontsize=9)
    if j == 0:
        ax.set_ylabel("volts", color=INK2, fontsize=10)
    dress(ax)
    for ea, eb, _, col, _r in EVENTS:
        if a <= ea <= b:
            ax.axvline(ea, color=col, lw=1.2, ls="--", alpha=0.8)
    ax.text(0.97, 0.06, "ch1 out", transform=ax.transAxes, ha="right",
            color=C_OUT, fontsize=8.5, fontweight="bold")
    ax.text(0.97, 0.15, "ch2 pad", transform=ax.transAxes, ha="right",
            color=C_IN, fontsize=8.5, fontweight="bold")

fig.suptitle("TiO₂ pad wetting + saline injection  —  scope_20260829_094236.csv "
             "(1 kHz, 72.7 s)", x=0.07, ha="left", fontsize=14,
             fontweight="bold", color=INK)
fig.savefig(OUT, dpi=140, facecolor="white")
print("wrote", OUT)

# ---- numbers quoted in the writeup ------------------------------------------
def seg(v, a, b):
    m = (t >= a) & (t < b)
    return np.median(v[m]), (v[m] - np.median(v[m])).std()
for lab, a, b in [("dry 0-13 s", 0, 13), ("wet 40-44 s", 40, 44), ("post-inj 48-56 s", 48, 56)]:
    print("%-18s ch1 %.3f +/-%.4f   ch2 %.3f +/-%.4f   hum %.1f mVrms"
          % (lab, *seg(ch1, a, b), *seg(ch2, a, b),
             1e3 * np.nanmedian(hum[(t >= a) & (t < b)])))
