#!/usr/bin/env python3
"""Generate Fig 13a: coincidence-detection membrane traces (neuron 14).

Four oscilloscope captures of the membrane, one per input interval Delta-t, aligned on the
first EPSP. Two subthreshold EPSPs summate in a Delta-t-graded way; at Delta-t=1 ms the
summed potential crosses the ~800 mV threshold and the comparator's positive feedback fires
a spike (green, reset at ~4 ms); at 2/3/4 ms it stays subthreshold and decays.

Data:   ../data/scopeCoinc/scope_{26,23,24,25}.csv  (Delta-t = 1,2,3,4 ms)
Output: ../figures/coinc_13a_membrane.pdf (+ .png)
Reproduce:  python gen_fig13a.py
"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib as mpl, matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "scopeCoinc")
FIGS = os.path.join(HERE, "..", "figures")

# Nature-style palette (matches coincidence_frontier.py / main.tex)
ANALOG, DIGITAL, INK, MUTED, GRID = "#1baf7a", "#e34948", "#0b0b0b", "#898781", "#e1e0d9"
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 6, "ytick.labelsize": 6,
    "legend.fontsize": 6, "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK,
    "ytick.labelcolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5,
    "ytick.major.size": 2.5, "legend.frameon": False, "lines.solid_capstyle": "round",
})

V_THRESH_MV = 800.0                      # comparator positive-feedback threshold (from traces)
# (file, Delta-t ms, fires); darker gray = closer Delta-t
TRACES = [("scope_26.csv", 1, True), ("scope_23.csv", 2, False),
          ("scope_24.csv", 3, False), ("scope_25.csv", 4, False)]
GRAYS = {2: "#3a3a3a", 3: "#6f6d68", 4: MUTED}


def load(f):
    d = np.genfromtxt(os.path.join(DATA, f), delimiter=",", skip_header=2)
    t, v = d[:, 0] * 1e3, d[:, 1] * 1e3
    m = ~np.isnan(v)
    return t[m], v[m]


def first_onset(t, v):
    base = np.median(v[:150])
    vs = np.convolve(v, np.ones(3) / 3, mode="same")
    return t[int(np.argmax(vs > base + 80))]     # first crossing baseline + 80 mV


def main():
    fig, ax = plt.subplots(figsize=(3.0, 2.3))
    ax.spines[["top", "right"]].set_visible(False)
    ax.axhline(V_THRESH_MV, color=MUTED, ls=":", lw=0.8)
    ax.text(30, V_THRESH_MV - 12, "threshold (pos. feedback)",
            fontsize=5.4, color=MUTED, ha="right", va="top")
    for f, dt, fires in TRACES:
        t, v = load(f)
        x = t - first_onset(t, v)
        w = (x >= -10) & (x <= 30)
        col = ANALOG if fires else GRAYS[dt]
        lbl = rf"$\Delta t{{=}}{dt}$ ms" + (r": summate $\to$ spike" if fires else "")
        ax.plot(x[w], v[w], color=col, lw=1.4 if fires else 1.0, label=lbl,
                zorder=3 if fires else 2)
    ax.set_xlim(-10, 30)
    ax.set_xlabel("time from first EPSP (ms)")
    ax.set_ylabel("membrane V (mV)")
    ax.legend(loc="upper right", handlelength=1.3, labelspacing=0.28)
    ax.set_title(r"coincidence: $\Delta t$-graded summation", fontsize=6.8, color=INK)
    plt.tight_layout()
    os.makedirs(FIGS, exist_ok=True)
    out = os.path.join(FIGS, "coinc_13a_membrane.pdf")
    plt.savefig(out); plt.savefig(out.replace(".pdf", ".png"), dpi=200)
    print("wrote", out)


if __name__ == "__main__":
    main()
