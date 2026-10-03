#!/usr/bin/env python3
"""f-I transfer curve (Poisson input) with three membrane-potential scope insets.

Main axes: output firing rate vs Poisson input rate (mean +/- std across time bins),
from neuron_fi_poisson_n14.csv. Three insets show the membrane potential captured on
the scope at low / mid / high input rate, with arrows to their operating points.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import pandas as pd

matplotlib.rcParams.update({"pdf.fonttype": 42, "font.size": 9})

DATA = "data/array"
CSV = "neuron_fi_poisson_n14.csv"
OUT = "measurements/array/figures/neuron_fi_insets.pdf"

# (scope file, label) for low / mid / high input rate
INSETS = [
    ("scope_14_neu14_if.csv", "low"),
    ("scope_17_neu14_if.csv", "mid"),
    ("scope_20_neu14_if.csv", "high"),
]
WIN_MS = 200.0  # scope zoom window


def load_scope(path):
    d = np.genfromtxt(path, delimiter=",", skip_header=2)
    return d[:, 0] * 1e3, d[:, 1] * 1e3  # ms, mV


def out_rate_of(t, v):
    base = np.median(v)
    above = v > base + 400
    return int(np.sum((~above[:-1]) & (above[1:]))) / ((t[-1] - t[0]) / 1000.0)


def input_for_output(freqs, mean, target):
    """Interpolate the input rate at which the f-I curve reaches `target` output."""
    for i in range(len(freqs) - 1):
        if (mean[i] - target) * (mean[i + 1] - target) <= 0 and mean[i + 1] != mean[i]:
            f = (target - mean[i]) / (mean[i + 1] - mean[i])
            return freqs[i] + f * (freqs[i + 1] - freqs[i])
    return freqs[-1] if target >= mean[-1] else freqs[0]


def main():
    df = pd.read_csv(CSV)
    g = df.groupby("input_hz")["output_hz"]
    freqs = np.array(sorted(df["input_hz"].unique()))
    mean = np.array([g.get_group(f).mean() for f in freqs])
    std = np.array([g.get_group(f).std(ddof=0) for f in freqs])

    fig = plt.figure(figsize=(5.4, 4.2))
    ax = fig.add_axes([0.10, 0.09, 0.86, 0.50])   # main f-I (bottom)
    ax.plot(freqs, mean, color="tab:blue", lw=1.6, marker="o", ms=3.5, zorder=3)
    ax.fill_between(freqs, mean - std, mean + std, color="tab:blue", alpha=0.25, zorder=2)
    ax.set_xlabel("Poisson input rate (Hz)", fontsize=10)
    ax.set_ylabel("Output rate (Hz)", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(alpha=0.25, lw=0.5)
    ax.set_xlim(-12, max(freqs) * 1.05)
    ax.set_ylim(-1, max(mean) * 1.18)

    # Pre-load the three traces (centred window) and use a common y-range so one
    # scale bar applies to all and the insets are directly comparable.
    traces = []
    for fname, tag in INSETS:
        t, v = load_scope(os.path.join(DATA, fname))
        rate = out_rate_of(t, v)
        in_hz = input_for_output(freqs, mean, rate)
        tc = 0.5 * (t[0] + t[-1])
        m = (t >= tc - WIN_MS / 2) & (t <= tc + WIN_MS / 2)
        traces.append((tag, in_hz, t[m] - t[m][0], v[m]))
    gymin = min(vv.min() for _, _, _, vv in traces)
    gymax = max(vv.max() for _, _, _, vv in traces)
    pad = 0.10 * (gymax - gymin)
    gymin, gymax = gymin - pad, gymax + pad

    inset_x = [0.10, 0.40, 0.70]
    for (tag, in_hz, tt, vv), ix in zip(traces, inset_x):
        axi = fig.add_axes([ix + 0.02, 0.70, 0.24, 0.22])
        axi.plot(tt, vv, color="tab:red", lw=0.7)
        axi.set_xlim(0, WIN_MS)
        axi.set_ylim(gymin, gymax)
        axi.set_xticks([]); axi.set_yticks([])
        for s in axi.spines.values():
            s.set_edgecolor("#888888")
        axi.set_title(f"{tag}: {in_hz:.0f} Hz input", fontsize=8, pad=2)
        if ix == inset_x[0]:
            # L-shaped scale bar: 100 mV (vertical) x 50 ms (horizontal)
            x0, y0 = 10.0, gymin + 0.06 * (gymax - gymin)
            axi.plot([x0, x0], [y0, y0 + 100], color="k", lw=1.3)
            axi.plot([x0, x0 + 50], [y0, y0], color="k", lw=1.3)
            axi.text(x0 - 5, y0 + 50, "100 mV", fontsize=7, rotation=90, va="center", ha="right")
            axi.text(x0 + 25, y0 - 0.07 * (gymax - gymin), "50 ms", fontsize=7, va="top", ha="center")
        # arrow from inset down to the operating point on the curve
        oi = float(np.interp(in_hz, freqs, mean))
        con = ConnectionPatch(
            xyA=(0.5, 0.0), coordsA=axi.transAxes,
            xyB=(in_hz, oi), coordsB=ax.transData,
            arrowstyle="-|>", color="#555555", lw=0.8, zorder=5)
        fig.add_artist(con)
        ax.plot([in_hz], [oi], "o", color="tab:red", ms=5, zorder=6)

    fig.savefig(OUT, bbox_inches="tight")
    fig.savefig(os.path.splitext(OUT)[0] + ".png", dpi=160, bbox_inches="tight")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
