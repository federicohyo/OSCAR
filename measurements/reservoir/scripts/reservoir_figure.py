#!/usr/bin/env python3
"""Phase-1 demonstration figure: for a Normal and a PVC beat, show (top) the ECG
stimulus, (middle) the 16-neuron spike raster it evokes, and (bottom) the continuous
reservoir state the RISC-V reconstructs by convolving each spike train with an
exponential kernel. Two columns contrast the classes -> the states are visibly
different, which is what the linear readout exploits.
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams.update({"pdf.fonttype": 42, "font.size": 9})


def reconstruct(spike_times, T, tau, dt):
    """Exponential-kernel filtered spike train sampled on [0,T]."""
    t = np.arange(0, T, dt)
    x = np.zeros_like(t)
    for ts in spike_times:
        m = t >= ts
        x[m] += np.exp(-(t[m] - ts) / tau)
    return t, x


def pick(labels, spikes, want):
    """Index of the beat of class `want` with the most total spikes (clearest)."""
    idxs = [i for i in range(len(labels)) if labels[i] == want]
    tot = [sum(len(spikes[k][i]) for k in range(16)) for i in idxs]
    return idxs[int(np.argmax(tot))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_delta.npz")
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NV")
    ap.add_argument("--tau", type=float, default=0.08, help="readout kernel tau (s)")
    ap.add_argument("--dt", type=float, default=0.004)
    ap.add_argument("--out", default="measurements/array/figures/reservoir_demo.pdf")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, labels, T = d["spikes"], d["labels"], float(d["T"])
    # re-derive the beat waveforms from the deterministic loader (same order)
    from reservoir_data import get_beats
    beats, y, _ = get_beats(records=tuple(args.records.split(",")),
                            n_per_class=args.n_per_class, classes=args.classes)
    assert np.array_equal(y, labels), "loader order mismatch with npz"
    beats_i = {"Normal": pick(labels, spikes, 0), "PVC": pick(labels, spikes, 1)}

    fig, axes = plt.subplots(3, 2, figsize=(7.0, 5.2),
                             gridspec_kw={"height_ratios": [1.1, 2.2, 1.6]})
    tms = np.linspace(0, T * 1000, beats.shape[1])
    for col, (name, bi) in enumerate(beats_i.items()):
        # (a) ECG stimulus
        ax = axes[0, col]
        ax.plot(tms, beats[bi], color="k", lw=1.2)
        ax.set_title(f"{name} beat", fontsize=11)
        ax.set_xlim(0, T * 1000); ax.set_yticks([])
        ax.set_ylabel("ECG" if col == 0 else "")
        ax.tick_params(labelbottom=False)

        # (b) 16-neuron raster
        ax = axes[1, col]
        for k in range(16):
            st = np.asarray(spikes[k][bi], dtype=float) * 1000.0
            if len(st):
                ax.vlines(st, k + 0.6, k + 1.4, color="tab:blue", lw=1.0)
        ax.set_ylim(0.5, 16.5); ax.set_xlim(0, T * 1000)
        ax.set_yticks([1, 4, 8, 12, 16])
        ax.set_ylabel("neuron" if col == 0 else "")
        ax.tick_params(labelbottom=False)

        # (c) kernel-reconstructed reservoir state: one line per neuron
        ax = axes[2, col]
        colors = plt.cm.tab20(np.linspace(0, 1, 16))
        for k in range(16):
            t, x = reconstruct(np.asarray(spikes[k][bi], dtype=float), T, args.tau, args.dt)
            if x.max() > 0:  # draw only active neurons; silent ones sit at 0
                ax.plot(t * 1000, x, color=colors[k], lw=1.0)
        ax.set_xlim(0, T * 1000)
        ax.set_ylabel(r"state $x_i(t)$" if col == 0 else "")
        ax.set_xlabel("time (ms)")
        ax.set_ylim(bottom=0)

    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    fig.savefig(args.out.replace(".pdf", ".png"), dpi=150, bbox_inches="tight")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
