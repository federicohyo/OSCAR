#!/usr/bin/env python3
"""Figure: the neuron as a continuous-time coincidence detector, membrane only.

Single-panel companion of the coincidence-membrane figure (repo-root
coincidence_frontier.py): the oscilloscope membrane of the analog neuron for
two input spikes at four commanded intervals (Delta-t = 1/2/3/4 ms), aligned
on the first EPSP. The Delta-t-graded EPSP summation crosses the 800 mV
positive-feedback threshold only at the shortest interval; at 2--4 ms the
second EPSP arrives after the first has partly leaked away and the membrane
stays sub-threshold. The measured P(spike)-vs-Delta-t panel of the original
figure is deliberately NOT included: this reference needs the membrane physics
only. Trace set, colours and threshold are imported from
coincidence_frontier.py, which stays the single source of truth.

Data: data/array/scopeCoinc/scope_{23,24,25,26}.csv

Usage (from the repo root):  ./.venv-meas/bin/python3 measurements/plotting/make_coincidence_membrane.py
"""

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
import coincidence_frontier as CF      # SCOPE_TRACES, GRAYS_13A, V_THRESH_MV, colours


def load_coinc(name):
    """13a membrane trace; same parsing as coincidence_frontier.load_coinc but
    with a ROOT-anchored path so this script runs from its own directory."""
    path = os.path.join(ROOT, CF.SCOPE_COINC, name)
    rows = [r for r in list(csv.reader(open(path)))[2:]
            if len(r) >= 2 and r[1] != ""]
    t = np.array([float(r[0]) for r in rows])
    v = np.array([float(r[1]) for r in rows]) * 1e3
    return t * 1e3, v          # ms, mV


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib as mpl, matplotlib.pyplot as plt
    mpl.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7, "axes.labelsize": 7, "xtick.labelsize": 6, "ytick.labelsize": 6,
        "legend.fontsize": 5.6, "axes.linewidth": 0.6, "axes.edgecolor": CF.MUTED,
        "xtick.color": CF.MUTED, "ytick.color": CF.MUTED, "xtick.labelcolor": CF.INK,
        "ytick.labelcolor": CF.INK, "axes.labelcolor": CF.INK, "text.color": CF.INK,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5,
        "ytick.major.size": 2.5, "legend.frameon": False, "lines.solid_capstyle": "round",
    })

    fig, ax = plt.subplots(figsize=(2.7, 2.55))
    ax.spines[["top", "right"]].set_visible(False)
    ax.axhline(CF.V_THRESH_MV, color=CF.MUTED, ls=":", lw=0.8)
    ax.text(30, CF.V_THRESH_MV - 12, "threshold (pos. feedback)", fontsize=5.0,
            color=CF.MUTED, ha="right", va="top")
    for f, dtms, fires in CF.SCOPE_TRACES:
        t, v = load_coinc(f)
        x = t - CF.first_onset(t, v)
        w = (x >= -10) & (x <= 30)
        col = CF.ANALOG if fires else CF.GRAYS_13A[dtms]
        lbl = rf"$\Delta t{{=}}{dtms}$ ms" + (r"$\,\to$ spike" if fires else "")
        ax.plot(x[w], v[w], color=col, lw=1.3 if fires else 0.95, label=lbl,
                zorder=3 if fires else 2)
        if fires:
            xw, vw = x[w], v[w]
            pk = int(np.argmax(vw))
            ax.plot(xw[pk], vw[pk], marker="o", ms=3.5, color=col,
                    mec="white", mew=0.5, zorder=5)
            ax.annotate("spike", xy=(xw[pk], vw[pk]),
                        xytext=(-6.5, vw[pk] + 5),
                        fontsize=6.0, color=col, ha="left", va="center",
                        arrowprops=dict(arrowstyle="-", color=col, lw=0.6,
                                        shrinkA=0, shrinkB=1.5), zorder=5)
        elif dtms == 2:
            # one input spike's contribution (Delta J_exc) drawn on the darkest
            # sub-threshold trace: a double arrow from rest to the first EPSP peak
            xw, vw = x[w], v[w]
            rest = float(np.median(vw[xw < -1]))
            band = (xw > 0.15) & (xw < 1.3)
            p1 = int(np.where(band)[0][np.argmax(vw[band])])
            xa = -1.0
            ax.annotate("", xy=(xa, vw[p1]), xytext=(xa, rest),
                        arrowprops=dict(arrowstyle="<->", color=col, lw=0.8),
                        zorder=5)
            ax.plot([xa, xw[p1]], [vw[p1], vw[p1]], color=col,
                    ls=(0, (2, 2)), lw=0.5, zorder=4)
            ax.text(xa - 0.5, (rest + vw[p1]) / 2, r"$\Delta J_{\rm exc}$",
                    fontsize=6.0, color=col, ha="right", va="center")
    ax.set_xlim(-10, 30)
    ax.set_xlabel("time from first EPSP (ms)")
    ax.set_ylabel(r"$V_{mem}$ (mV)")
    ax.legend(loc="upper right", handlelength=1.2, labelspacing=0.22)
    ax.grid(True, which="major", ls=":", lw=0.5, color=CF.GRID, zorder=0)

    fig.tight_layout()
    base = os.path.join(HERE, "coincidence_membrane")
    fig.savefig(base + ".pdf", bbox_inches="tight")
    fig.savefig(base + ".png", dpi=350, bbox_inches="tight")
    plt.close(fig)

    _, vs = load_coinc(CF.SCOPE_TRACES[0][0])
    _, vb = load_coinc(CF.SCOPE_TRACES[-1][0])
    print(f"wrote {base}.pdf/.png  (Delta-t=1 ms: Vmax={vs.max():.0f} mV, spikes; "
          f"Delta-t=4 ms: Vmax={vb.max():.0f} mV, sub-threshold)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
