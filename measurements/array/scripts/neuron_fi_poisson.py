#!/usr/bin/env python3
"""Neuron f-I transfer curve driven by on-chip Poisson synaptic input.

One neuron at a time (so the RISC-V never has to service more than one firing
neuron), a single excitatory synapse (weight 15) is stimulated by the on-chip
RISC-V Poisson generator at a mean input rate swept from 1 to 100 Hz; the neuron's
output firing rate is sampled over the AER path. Aggregated across the array, the
result is the mean output rate with a +/-1 sigma shaded band (device mismatch) vs
the Poisson input rate.

Example:
  python neuron_fi_poisson.py \
      --biases ofxCaravanViewer/bin/bias_synapse_characterization_super.biases \
      --syn 0 --weight 15 --freqs 1,2,5,10,15,20,30,50,70,100 --sample 4 \
      --out neuron_fi_poisson.csv
"""

import argparse
import csv
import os
import queue
import time
from collections import Counter

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_super.biases")


def dominant_index(b, seconds):
    """During the current stimulation, return the most active output index."""
    c = Counter()
    b.drain(max_lines=100000)
    end = time.time() + seconds
    while time.time() < end:
        try:
            line = b.out_q.get(timeout=0.05)
        except queue.Empty:
            continue
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3:
                try:
                    c[int(p[1])] += 1
                except ValueError:
                    pass
    return (c.most_common(1)[0][0], sum(c.values())) if c else (None, 0)


def collect_binned(b, out_idx, seconds, nbins):
    """Collect spikes on out_idx over `seconds`; return a per-bin firing rate list
    (rate in each seconds/nbins sub-window). The spread across bins gives the
    Poisson-driven temporal variability -> mean +/- std for a single neuron."""
    t0 = time.time()
    times = []
    b.drain(max_lines=100000)
    end = t0 + seconds
    while time.time() < end:
        try:
            line = b.out_q.get(timeout=0.05)
        except queue.Empty:
            continue
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3:
                try:
                    if int(p[1]) == out_idx:
                        times.append(time.time() - t0)
                except ValueError:
                    pass
    binw = seconds / nbins
    counts = [0] * nbins
    for t in times:
        counts[min(nbins - 1, int(t / binw))] += 1
    return [c / binw for c in counts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--bias-pattern", default=None,
                    help="if set, apply this per-neuron bias file (with '{k}') before "
                         "sweeping each neuron, e.g. "
                         "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}.biases")
    ap.add_argument("--neurons", default="0-15")
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--freqs", default="1,2,5,10,15,20,30,50,70,100",
                    help="Poisson input rates (Hz)")
    ap.add_argument("--sample", type=float, default=4.0, help="sample window per point (s)")
    ap.add_argument("--bins", type=int, default=10, help="sub-bins per point for mean/std")
    ap.add_argument("--jexc", type=float, default=None,
                    help="override all JExcWn (super biases are subthreshold for one synapse)")
    ap.add_argument("--settle", type=float, default=0.5)
    ap.add_argument("--out", default="neuron_fi_poisson.csv")
    ap.add_argument("--plot", default="measurements/array/figures/neuron_fi_poisson.pdf")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    neurons = []
    for part in args.neurons.split(","):
        if "-" in part:
            a, b_ = part.split("-")
            neurons.extend(range(int(a), int(b_) + 1))
        elif part.strip():
            neurons.append(int(part))
    freqs = [float(x) for x in args.freqs.split(",")]

    biases = load_biases(args.biases)
    if args.jexc is not None:
        for i in range(4):
            biases[f"JExcWn{i}"] = args.jexc
    rows = []
    perbin = {}   # (k, f) -> list of per-bin output rates
    out_of = {}   # k -> responding output index
    with BridgeSession(verbose=args.verbose) as b:
        b.apply_biases(biases)
        time.sleep(1.0)
        b.program_weight(args.syn, args.weight, exc=True)
        time.sleep(0.2)

        for k in neurons:
            if args.bias_pattern:
                per = load_biases(args.bias_pattern.format(k=k))
                if args.jexc is not None:
                    for i in range(4):
                        per[f"JExcWn{i}"] = args.jexc
                b.apply_biases(per)
                time.sleep(0.8)
            b.route(args.syn, k, exc=True)
            b.monitor(k)
            time.sleep(0.2)
            # find the responding output index at the top input rate; the route->
            # readout mapping is identity, so fall back to index k for low-firing
            # neurons rather than skipping them (they still count in the aggregate).
            b.poisson(max(freqs))
            out_idx, n = dominant_index(b, 3.0)
            b.poisson_stop()
            time.sleep(0.3)
            if out_idx is None or n < 2:
                out_idx = k
            b.monitor(k)   # keep neuron k on the analog monitor pin for the whole sweep
            print(f"==> MONITOR neuron {k:2d} on scope (readout idx {out_idx}) -- sweeping f-I ...",
                  flush=True)
            import statistics as _st
            for f in freqs:
                b.poisson(f)
                time.sleep(args.settle)
                bin_rates = collect_binned(b, out_idx, args.sample, args.bins)
                b.poisson_stop()
                time.sleep(0.15)
                for br in bin_rates:
                    rows.append((k, f, br))
                perbin[(k, f)] = bin_rates
                out_of[k] = out_idx
                m = _st.mean(bin_rates)
                s = _st.pstdev(bin_rates)
                print(f"    in={f:6.1f} Hz  out={m:6.2f} +/- {s:4.2f} Hz")

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["neuron", "input_hz", "output_hz"])
        w.writerows(rows)
    print("wrote", args.out)
    save_npz(args, neurons, freqs, perbin, out_of)
    make_plot(args.out, args.plot)
    return 0


def save_npz(args, neurons, freqs, perbin, out_of):
    """Save a structured .npz so any plot can be made offline without re-running
    the chip. rates[n, f, bin] = output firing rate (Hz); NaN where a point is
    missing. Also stores per-(neuron,freq) mean and std for convenience."""
    import numpy as np
    npz_path = os.path.splitext(args.out)[0] + ".npz"
    nb = args.bins
    rates = np.full((len(neurons), len(freqs), nb), np.nan, dtype=float)
    for ni, k in enumerate(neurons):
        for fi, fr in enumerate(freqs):
            br = perbin.get((k, fr))
            if br is not None:
                rates[ni, fi, :len(br)] = br[:nb]
    mean = np.nanmean(rates, axis=2)
    std = np.nanstd(rates, axis=2)
    np.savez(
        npz_path,
        neurons=np.array(neurons),
        freqs=np.array(freqs, dtype=float),
        rates=rates,                       # [n_neurons, n_freqs, n_bins]
        mean=mean,                         # [n_neurons, n_freqs]
        std=std,                           # [n_neurons, n_freqs]
        out_idx=np.array([out_of.get(k, k) for k in neurons]),
        syn=args.syn, weight=args.weight, sample_s=args.sample, bins=nb,
        bias_pattern=str(args.bias_pattern), biases=str(args.biases),
    )
    print("wrote", npz_path)


def make_plot(csv_path, plot_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    matplotlib.rcParams.update({"pdf.fonttype": 42})

    df = pd.read_csv(csv_path)
    g = df.groupby("input_hz")["output_hz"]
    freqs = sorted(df["input_hz"].unique())
    mean = np.array([g.get_group(f).mean() for f in freqs])
    std = np.array([g.get_group(f).std(ddof=0) for f in freqs])
    neuron_ids = sorted(df["neuron"].unique())
    n_neurons = len(neuron_ids)
    band = "mismatch" if n_neurons > 1 else "variability"

    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    # per-neuron curves (heterogeneity across the array)
    if n_neurons > 1:
        for k in neuron_ids:
            sub = df[df["neuron"] == k].groupby("input_hz")["output_hz"].mean()
            ax.plot(sub.index, sub.values, color="0.6", linewidth=0.5, alpha=0.6, zorder=1)
        ax.plot([], [], color="0.6", linewidth=0.5, label=f"per-neuron ($n={n_neurons}$)")
    ax.plot(freqs, mean, color="tab:blue", linewidth=1.5, marker="o", ms=3, label="mean", zorder=3)
    ax.fill_between(freqs, mean - std, mean + std, color="tab:blue", alpha=0.25,
                    label=rf"$\pm 1\sigma$ ({band})", zorder=2)
    ax.set_xlabel("Poisson input rate (Hz)", fontsize=11)
    ax.set_ylabel("Output firing rate (Hz)", fontsize=11)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(plot_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(plot_path)[0] + ".png", dpi=150, bbox_inches="tight")
    print("plot ->", plot_path)


if __name__ == "__main__":
    raise SystemExit(main())
