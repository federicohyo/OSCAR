#!/usr/bin/env python3
"""Array-wide f-I transfer curve (all 16 neurons, per-neuron biases) with the
three neuron-14 membrane-potential scope insets kept for the neural dynamics.

Main axes: output firing rate vs Poisson input rate for all 16 neurons
(thin grey per-neuron curves) with the array mean +/- 1 sigma (device-mismatch)
band; neuron 14 highlighted because the insets are its captures. Three insets
show neuron 14's membrane potential at low / mid / high input rate with arrows to
its operating points. Reproduces the layout of plot_fi_insets.py but on the
16-neuron sweep (neuron_fi_allneurons.csv), so the single figure shows both the
across-array heterogeneity and the underlying integrate-and-fire dynamics.
"""

import argparse
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import pandas as pd

matplotlib.rcParams.update({"pdf.fonttype": 42, "font.size": 9})

DATA = "data/array"
CSV = "neuron_fi_allneurons.csv"
OUT = "measurements/array/figures/neuron_fi_all16_insets.pdf"
HILITE = 14  # neuron whose scope traces are shown as insets
STYLE = "default"  # "iscas" = open spines + geometry matched to weight_code_words.pdf

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
    """Interpolate the input rate at which a curve reaches `target` output."""
    for i in range(len(freqs) - 1):
        if (mean[i] - target) * (mean[i + 1] - target) <= 0 and mean[i + 1] != mean[i]:
            f = (target - mean[i]) / (mean[i + 1] - mean[i])
            return freqs[i] + f * (freqs[i + 1] - freqs[i])
    return freqs[-1] if target >= mean[-1] else freqs[0]


def curve(df, freqs, neuron=None):
    sub = df if neuron is None else df[df["neuron"] == neuron]
    g = sub.groupby("input_hz")["output_hz"]
    return np.array([g.get_group(f).mean() for f in freqs])


def main():
    df = pd.read_csv(os.path.join(DATA, CSV))
    freqs = np.array(sorted(df["input_hz"].unique()))
    neuron_ids = sorted(df["neuron"].unique())
    n_neurons = len(neuron_ids)

    # array aggregate mean +/- 1 sigma (across all per-neuron, per-bin samples)
    g = df.groupby("input_hz")["output_hz"]
    mean = np.array([g.get_group(f).mean() for f in freqs])
    std = np.array([g.get_group(f).std(ddof=0) for f in freqs])
    n14 = curve(df, freqs, HILITE)

    if STYLE == "iscas":
        fig = plt.figure(figsize=(3.6, 3.4))
        ax = fig.add_axes([0.1722, 0.1529, 0.7978, 0.500])
    else:
        fig = plt.figure(figsize=(5.4, 4.2))
        ax = fig.add_axes([0.10, 0.09, 0.86, 0.50])   # main f-I (bottom)

    # encoding band used for ECG (20-200 Hz); irrelevant to the ISCAS paper,
    # whose task is olfaction, so the variant leaves it out
    if STYLE != "iscas":
        ax.axvspan(20, 200, color="tab:orange", alpha=0.10, zorder=0)

    # per-neuron curves (heterogeneity across the array)
    for k in neuron_ids:
        ax.plot(freqs, curve(df, freqs, k), color="0.65", lw=0.5, alpha=0.7, zorder=1)
    ax.plot([], [], color="0.65", lw=0.5, label=f"per-neuron ($n={n_neurons}$)")

    # array mean +/- 1 sigma
    ax.fill_between(freqs, mean - std, mean + std, color="tab:blue", alpha=0.22,
                    label=r"mean $\pm 1\sigma$ (mismatch)", zorder=2)
    ax.plot(freqs, mean, color="tab:blue", lw=1.6, marker="o", ms=3.0, label="array mean", zorder=3)

    # highlight the neuron whose dynamics the insets show
    ax.plot(freqs, n14, color="tab:red", lw=1.3, ls="--", zorder=4,
            label=f"neuron {HILITE} (insets)")

    ax.set_xlabel("Poisson input rate (Hz)", fontsize=10)
    ax.set_ylabel("Output rate (Hz)", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(alpha=0.25, lw=0.5)
    ax.set_xlim(-12, max(freqs) * 1.05)
    ax.set_ylim(-1, float(np.nanmax([mean.max() + std.max(), n14.max()])) * 1.15)
    if STYLE == "iscas":
        for _s in ("top", "right"):
            ax.spines[_s].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")

    # Pre-load the three neuron-14 traces (centred window), common y-range.
    traces = []
    for fname, tag in INSETS:
        t, v = load_scope(os.path.join(DATA, fname))
        rate = out_rate_of(t, v)
        in_hz = input_for_output(freqs, n14, rate)   # map onto neuron 14's own curve
        tc = 0.5 * (t[0] + t[-1])
        m = (t >= tc - WIN_MS / 2) & (t <= tc + WIN_MS / 2)
        traces.append((tag, in_hz, t[m] - t[m][0], v[m]))
    gymin = min(vv.min() for _, _, _, vv in traces)
    gymax = max(vv.max() for _, _, _, vv in traces)
    pad = 0.10 * (gymax - gymin)
    gymin, gymax = gymin - pad, gymax + pad

    inset_x = [0.10, 0.40, 0.70]
    for (tag, in_hz, tt, vv), ix in zip(traces, inset_x):
        iy, ih = (0.735, 0.200) if STYLE == "iscas" else (0.70, 0.22)
        axi = fig.add_axes([ix + 0.02, iy, 0.24, ih])
        axi.plot(tt, vv, color="tab:red", lw=0.7)
        axi.set_xlim(0, WIN_MS)
        axi.set_ylim(gymin, gymax)
        axi.set_xticks([]); axi.set_yticks([])
        for s in axi.spines.values():
            s.set_edgecolor("#888888")
        if ix == inset_x[0]:
            # L-shaped scale bar: 100 mV (vertical) x 50 ms (horizontal)
            x0, y0 = 10.0, gymin + 0.06 * (gymax - gymin)
            axi.plot([x0, x0], [y0, y0 + 100], color="k", lw=1.3)
            axi.plot([x0, x0 + 50], [y0, y0], color="k", lw=1.3)
            axi.text(x0 - 5, y0 + 50, "100 mV", fontsize=7, rotation=90, va="center", ha="right")
            axi.text(x0 + 25, y0 - 0.07 * (gymax - gymin), "50 ms", fontsize=7, va="top", ha="center")
        # arrow from inset down to neuron 14's operating point on its curve
        oi = float(np.interp(in_hz, freqs, n14))
        con = ConnectionPatch(
            xyA=(0.5, 0.0), coordsA=axi.transAxes,
            xyB=(in_hz, oi), coordsB=ax.transData,
            arrowstyle="-|>", color="#555555", lw=0.8, zorder=5)
        fig.add_artist(con)
        ax.plot([in_hz], [oi], "o", color="tab:red", ms=5, zorder=6)

    bb = None if STYLE == "iscas" else "tight"
    fig.savefig(OUT, bbox_inches=bb)
    fig.savefig(os.path.splitext(OUT)[0] + ".png", dpi=160, bbox_inches=bb)
    print("wrote", OUT)


if __name__ == "__main__":
    _ap = argparse.ArgumentParser()
    _ap.add_argument("--out", default=OUT)
    _ap.add_argument("--style", default="default", choices=["default", "iscas"])
    _a = _ap.parse_args()
    OUT, STYLE = _a.out, _a.style
    main()
