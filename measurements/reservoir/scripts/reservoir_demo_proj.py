#!/usr/bin/env python3
"""Comparison figure: shared-input feedforward reservoir (every neuron sees the same
delta stream) vs. per-neuron input projection (each neuron sees its own fixed random
projection of the beat). Shows, for the same example beat, (top) the 16-neuron raster,
(middle) the 16x16 neuron-neuron response-correlation matrix, and (bottom, spanning)
effective dimensionality vs. readout-kernel time constant. The projection decorrelates
the substrate and lifts effective dimensionality past the shared-input ceiling.
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reservoir_kernel import build_features
from sklearn.preprocessing import StandardScaler

matplotlib.rcParams.update({"pdf.fonttype": 42, "font.size": 9})

# Recordings ACC and DIM (reservoir_datasets.py). They are DIFFERENT acquisitions,
# not two read-outs of one: ACC carries 49 events/window and DIM 282 on the same
# beats. Do not quote a statistic from one against the other.
NO_PROJ = "reservoir_spikes_nv_delta.npz"      # ACC: shared input, plain feedforward delta
WITH_PROJ = "reservoir_spikes_nv_randproj.npz"  # DIM: per-neuron input projection


def load(npz):
    d = np.load(npz, allow_pickle=True)
    return d["spikes"], d["labels"], float(d["T"])


def corr_effdim(spikes, T, K, shape, tau):
    """16x16 neuron response-correlation matrix and participation-ratio eff-dim
    at a given readout kernel."""
    n = spikes.shape[0]
    X = build_features(spikes, T, K, shape, tau)
    sig = np.stack([X[:, j * K:(j + 1) * K].ravel() for j in range(n)])
    R = np.corrcoef(sig)
    off = R[~np.eye(n, dtype=bool)]
    ev = np.clip(np.linalg.eigvalsh(np.cov(StandardScaler().fit_transform(X).T)), 0, None)
    pr = (ev.sum() ** 2) / np.square(ev).sum()
    return R, float(np.mean(np.abs(off))), float(pr)


def pick_normal(labels, spikes):
    idxs = [i for i in range(len(labels)) if labels[i] == 0]
    tot = [sum(len(spikes[k][i]) for k in range(spikes.shape[0])) for i in idxs]
    return idxs[int(np.argmax(tot))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-proj", default=NO_PROJ)
    ap.add_argument("--with-proj", default=WITH_PROJ)
    ap.add_argument("--sw-proj", default="sw_proj.npz", help="SW identical-LIF + projection")
    ap.add_argument("--sw-shared", default="sw_shared.npz", help="SW identical-LIF + shared input")
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--tau-mat", type=float, default=0.02, help="tau (s) for corr matrices")
    ap.add_argument("--out", default="measurements/array/figures/reservoir_demo_proj.pdf")
    args = ap.parse_args()

    conds = [("Shared input\n(no projection)", *load(args.no_proj)),
             ("Per-neuron\ninput projection", *load(args.with_proj))]
    # same example Normal beat index in both (identical loader order / beat set)
    bi = pick_normal(conds[0][2], conds[0][1])  # (name, spikes, labels, T)

    taus = np.array([0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
    fig = plt.figure(figsize=(7.2, 6.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.9, 1.7, 1.5], hspace=0.42, wspace=0.28)

    corr_stats = []
    for col, (name, spikes, labels, T) in enumerate(conds):
        n = spikes.shape[0]
        # (a) raster for the same Normal beat
        ax = fig.add_subplot(gs[0, col])
        for k in range(n):
            st = np.asarray(spikes[k][bi], dtype=float) * 1000.0
            if len(st):
                ax.vlines(st, k + 0.6, k + 1.4, color="tab:blue", lw=0.9)
        ax.set_ylim(0.5, n + 0.5); ax.set_xlim(0, T * 1000)
        ax.set_yticks([1, 4, 8, 12, 16])
        ax.set_title(name, fontsize=10)
        if col == 0:
            ax.set_ylabel("neuron")
        ax.set_xlabel("time (ms)", fontsize=8)

        # (b) neuron-neuron correlation matrix at tau-mat
        R, mc, pr = corr_effdim(spikes, T, args.K, "exp", args.tau_mat)
        corr_stats.append((name, mc, pr))
        ax = fig.add_subplot(gs[1, col])
        im = ax.imshow(np.abs(R), vmin=0, vmax=1, cmap="magma")
        ax.set_title(rf"$\langle|\rho|\rangle={mc:.2f}$,  eff-dim$={pr:.0f}$", fontsize=9)
        ax.set_xticks([0, 5, 10, 15]); ax.set_yticks([0, 5, 10, 15])
        if col == 0:
            ax.set_ylabel("neuron")
        ax.set_xlabel("neuron", fontsize=8)
        if col == 1:
            cax = ax.inset_axes([1.06, 0.0, 0.05, 1.0])
            fig.colorbar(im, cax=cax).set_label(r"$|\rho_{ij}|$", fontsize=8)

    # (c) eff-dim vs readout kernel tau: decomposition shared -> projection -> mismatch
    ax = fig.add_subplot(gs[2, :])
    curves = [
        ("HW chip: variations + projection", args.with_proj, "tab:red", "o-"),
        ("SW LIF: identical + projection", args.sw_proj, "tab:orange", "s-"),
        ("HW chip: shared input (no proj.)", args.no_proj, "0.45", "o--"),
        ("SW LIF: shared input (no proj.)", args.sw_shared, "0.7", ":"),
    ]
    for label, npz, color, mk in curves:
        try:
            sp, _, T = load(npz)
        except FileNotFoundError:
            continue
        eds = [corr_effdim(sp, T, args.K, "exp", t)[2] for t in taus]
        ax.plot(taus * 1000, eds, mk, color=color, lw=1.6, ms=4, label=label)
    ax.axhline(8, color="k", ls=":", lw=0.9)
    ax.text(taus[0] * 1000 * 1.03, 7.6, "shared-input ceiling ($\\approx$8)",
            ha="left", va="top", fontsize=7.5)
    ax.set_xscale("log")
    ax.set_xticks(taus * 1000)
    ax.set_xticklabels([f"{t*1000:.0f}" for t in taus])
    ax.set_xlabel("readout kernel $\\tau$ (ms)")
    ax.set_ylabel("effective dim.")
    ax.legend(fontsize=8, loc="upper right", frameon=False)
    ax.set_ylim(bottom=0)

    fig.savefig(args.out, bbox_inches="tight")
    fig.savefig(args.out.replace(".pdf", ".png"), dpi=150, bbox_inches="tight")
    print("wrote", args.out)
    for name, mc, pr in corr_stats:
        print(f"  {name.replace(chr(10),' '):30s} |rho|={mc:.3f} eff-dim={pr:.1f} "
              f"(exp tau={args.tau_mat*1000:.0f}ms)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
