#!/usr/bin/env python3
"""Regenerate camera-ready figures for the reference campaign from the raw sweep CSVs at repo root.

Run from measurements/array/figures/:
    python3 make_figures.py
"""
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 7,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42,
})

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def fig_weight_vs_rate():
    """Output firing rate of one representative neuron as a joint function of the
    excitatory weight bias and the input stimulation rate, shown as a heatmap so the
    threshold-like onset boundary is legible (the overlaid-line version was cluttered)."""
    df = pd.read_csv(os.path.join(ROOT, "Jexc_spikerate_w1_lab20260422.csv"))
    neuron_cols = [c for c in df.columns if c.startswith("n") and c.endswith("_hz")]

    # Pick the neuron with the cleanest signal: most non-zero cells, then highest peak.
    def score(col):
        return (int((df[col] > 0).sum()), float(df[col].max()))
    best = max(neuron_cols, key=score)

    pivot = df.pivot_table(values=best, index="input_hz", columns="JexcWn0_v", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    im = ax.pcolormesh(
        pivot.columns.to_numpy(), pivot.index.to_numpy(), pivot.to_numpy(),
        shading="nearest", cmap="viridis", vmin=0,
    )
    ax.set_xlabel(r"Excitatory synaptic weight bias $J_{ExcWn0}$ (V)")
    ax.set_ylabel("Input stimulation rate (Hz)")
    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label(f"Output rate,\nneuron {best[1:-3]} (Hz)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "weight_vs_rate.pdf"))
    plt.close(fig)


def fig_bias_mismatch():
    df = pd.read_csv(os.path.join(ROOT, "ifdcp_vleakn_home20260421.csv"))
    neuron_cols = [c for c in df.columns if c.startswith("n") and c.endswith("_hz")]

    fig, axes = plt.subplots(4, 4, figsize=(6.9, 5.6), sharex=True, sharey=True)
    axes = axes.flatten()
    vmax = df[neuron_cols].to_numpy().max()

    im = None
    for idx, col in enumerate(neuron_cols):
        ax = axes[idx]
        pivot = df.pivot_table(values=col, index="vleakn_v", columns="ifdcp_v", aggfunc="mean")
        im = ax.pcolormesh(
            pivot.columns.to_numpy(), pivot.index.to_numpy(), pivot.to_numpy(),
            shading="auto", cmap="viridis", vmin=0, vmax=vmax,
        )
        ax.set_title(col.replace("_hz", ""), fontsize=10, pad=2)
        ax.tick_params(labelsize=8)

    for ax in axes[12:]:
        ax.set_xlabel(r"$I_{fdcp}$ (V)", fontsize=10)
    for ax in axes[0::4]:
        ax.set_ylabel(r"$V_{leakn}$ (V)", fontsize=10)

    fig.subplots_adjust(right=0.88, wspace=0.15, hspace=0.35)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    cb = fig.colorbar(im, cax=cbar_ax)
    cb.set_label("Firing rate (Hz)", fontsize=10)
    cb.ax.tick_params(labelsize=9)
    fig.savefig(os.path.join(HERE, "bias_mismatch_heatmap.pdf"), bbox_inches="tight")
    plt.close(fig)

    # Companion: overlay each of the 16 neurons' firing-rate-vs-ifdcp tuning curve at a
    # single vleakn slice. Device mismatch then reads directly off the plot as the spread
    # of onset/peak positions across the otherwise-identical neurons -- far more meaningful
    # than collapsing everything into a mean +/- sigma band (which was flat and uninformative).
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize

    # Choose the vleakn slice that best separates the neurons (largest across-neuron spread).
    per_slice = df.groupby("vleakn_v").apply(
        lambda g: g.groupby("ifdcp_v")[neuron_cols].mean().max().std()
    )
    vleakn_fixed = per_slice.idxmax()
    sl = df[np.isclose(df["vleakn_v"], vleakn_fixed)]

    fig2, ax2 = plt.subplots(figsize=(3.4, 2.7))
    norm = Normalize(vmin=0, vmax=len(neuron_cols) - 1)
    cmap = plt.get_cmap("viridis")
    for i, col in enumerate(neuron_cols):
        curve = sl.groupby("ifdcp_v", as_index=False)[col].mean().sort_values("ifdcp_v")
        ax2.plot(curve["ifdcp_v"], curve[col], color=cmap(norm(i)), linewidth=1.0)
    ax2.set_xlabel(r"$I_{fdcp}$ (V)")
    ax2.set_ylabel("Firing rate (Hz)")
    ax2.set_title(rf"16 neurons, $V_{{leakn}}$ = {vleakn_fixed:.3f} V", fontsize=8)
    ax2.grid(alpha=0.25, linewidth=0.5)
    sm = cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar2 = fig2.colorbar(sm, ax=ax2, pad=0.02, ticks=[0, 5, 10, 15])
    cbar2.set_label("Neuron index")
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "bias_mismatch_mean_std.pdf"))
    plt.close(fig2)


if __name__ == "__main__":
    fig_weight_vs_rate()
    fig_bias_mismatch()
    print("Figures written to", HERE)
