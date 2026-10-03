#!/usr/bin/env python3
"""Per-neuron coincidence detection window characterization.

Sweeps Δt for each of the 16 neurons to map P(fire) vs inter-input interval,
revealing device-mismatch-induced variation in coincidence window widths.
Inspired by Sheik, Chicca & Indiveri (IJCNN 2012).

Usage:
    # Full 16-neuron sweep (~12 min)
    python coincidence_array.py --biases ofxCaravanViewer/bin/bias_synapse_characterization_coincidence.biases

    # Quick sanity on one neuron
    python coincidence_array.py --neurons 14 --trials 20

    # With vleakn family on one neuron
    python coincidence_array.py --neurons 14 --vleakn 0.24,0.25,0.26,0.27,0.28
"""

import argparse
import csv
import os
import queue
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_coincidence.biases")

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 7,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6,
})


# ── helpers ──────────────────────────────────────────────────────────────────

def wait_fire(b, out_idx, window_s):
    """After a stimulus, return True if out_idx spikes within window_s."""
    fired = False
    end = time.time() + window_s
    while time.time() < end:
        try:
            line = b.out_q.get(timeout=0.02)
        except queue.Empty:
            continue
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3:
                try:
                    if int(p[1]) == out_idx:
                        fired = True
                except ValueError:
                    pass
    return fired


def detect_output(b, syn_a, syn_b, neuron, reps=30, window_s=0.05):
    """Fire coincident pairs and return the most frequently responding output index."""
    from collections import Counter
    c = Counter()
    for _ in range(reps):
        b.drain(max_lines=100000)
        b.coincidence(syn_a, syn_b, neuron, 0.0)
        end = time.time() + window_s
        while time.time() < end:
            try:
                line = b.out_q.get(timeout=0.02)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3:
                    try:
                        c[int(p[1])] += 1
                    except ValueError:
                        pass
    return c.most_common(1)[0][0] if c else None


def p_fire_coinc(b, first, second, neuron, dt_us, out_idx, trials, window_s):
    """Measure P(fire) for a given Δt in µs. Constant window_s for all dt."""
    fires = 0
    for _ in range(trials):
        b.drain(max_lines=100000)
        b.coincidence(first, second, neuron, dt_us)
        if wait_fire(b, out_idx, window_s):
            fires += 1
    return fires / trials


def compute_fwhm(dts, pfs):
    """Compute the full-width at half-maximum of the P(fire) curve.
    Returns (width_ms, left_ms, right_ms) or (nan, nan, nan) if not measurable."""
    peak = max(pfs)
    if peak < 0.3:
        return float('nan'), float('nan'), float('nan')
    half = peak / 2.0
    # Find left crossing
    left = dts[0]
    for i in range(len(pfs) - 1):
        if pfs[i] < half <= pfs[i + 1]:
            # Linear interpolation
            frac = (half - pfs[i]) / (pfs[i + 1] - pfs[i]) if pfs[i + 1] != pfs[i] else 0
            left = dts[i] + frac * (dts[i + 1] - dts[i])
            break
    # Find right crossing
    right = dts[-1]
    for i in range(len(pfs) - 1, 0, -1):
        if pfs[i] < half <= pfs[i - 1]:
            frac = (half - pfs[i]) / (pfs[i - 1] - pfs[i]) if pfs[i - 1] != pfs[i] else 0
            right = dts[i] + frac * (dts[i - 1] - dts[i])
            break
    return abs(right - left), left, right


# ── plotting ─────────────────────────────────────────────────────────────────

def plot_overlaid_curves(csv_path, out_base):
    """All 16 neurons' P(fire) vs Δt on one axis."""
    import pandas as pd
    df = pd.read_csv(csv_path)
    if "vleakn" in df.columns:
        df = df[df["vleakn"].isna() | (df["vleakn"] == "")]

    neurons = sorted(df["neuron"].unique())
    cmap = plt.get_cmap("tab20")

    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    for i, n in enumerate(neurons):
        g = df[df["neuron"] == n].sort_values("dt_ms")
        ax.plot(g["dt_ms"], g["p_fire"], marker="o", ms=2.5, linewidth=1.0,
                color=cmap(n / 16.0), label=f"n{n}", alpha=0.85)

    ax.set_xlabel(r"Inter-input interval $\Delta t$ (ms)")
    ax.set_ylabel(r"$P(\mathrm{spike})$")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.15, linewidth=0.3)
    ax.legend(ncol=4, fontsize=5.5, frameon=False, loc="upper right",
              bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    for ext in (".pdf", ".png"):
        fig.savefig(out_base + "_curves" + ext, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_base}_curves.pdf")


def plot_window_widths(csv_path, out_base):
    """Bar chart of W₅₀ (FWHM) per neuron."""
    import pandas as pd
    df = pd.read_csv(csv_path)
    if "vleakn" in df.columns:
        df = df[df["vleakn"].isna() | (df["vleakn"] == "")]

    neurons = sorted(df["neuron"].unique())
    widths = []
    for n in neurons:
        g = df[df["neuron"] == n].sort_values("dt_ms")
        dts = g["dt_ms"].values.tolist()
        pfs = g["p_fire"].values.tolist()
        w, _, _ = compute_fwhm(dts, pfs)
        widths.append(w)

    valid = [w for w in widths if not np.isnan(w)]
    mean_w = np.mean(valid) if valid else 0
    std_w = np.std(valid) if valid else 0

    fig, ax = plt.subplots(figsize=(3.6, 2.2))
    colors = [plt.get_cmap("tab20")(n / 16.0) for n in neurons]
    bars = ax.bar(neurons, widths, color=colors, edgecolor="white", linewidth=0.3)

    # Mark neurons with no measurable window
    for i, w in enumerate(widths):
        if np.isnan(w):
            ax.text(neurons[i], 0.2, "×", ha="center", va="bottom",
                    fontsize=8, color="#999999")

    ax.axhline(mean_w, color="#444444", ls="--", lw=0.8, alpha=0.7)
    ax.text(15.5, mean_w + 0.2, f"μ={mean_w:.1f} ms\nσ={std_w:.1f} ms",
            fontsize=6.5, va="bottom", ha="right",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cccccc", alpha=0.9))

    ax.set_xlabel("Neuron index")
    ax.set_ylabel(r"Coincidence window $W_{50}$ (ms)")
    ax.set_xticks(range(16))
    ax.grid(axis="y", alpha=0.15, linewidth=0.3)
    fig.tight_layout()
    for ext in (".pdf", ".png"):
        fig.savefig(out_base + "_widths" + ext, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_base}_widths.pdf")


def plot_vleakn_family(csv_path, out_base):
    """Family of P(fire) vs Δt curves parametrized by vleakn (single neuron)."""
    import pandas as pd
    df = pd.read_csv(csv_path)
    if "vleakn" not in df.columns or df["vleakn"].isna().all():
        return
    df = df[df["vleakn"].notna() & (df["vleakn"] != "")]
    if df.empty:
        return

    df["vleakn"] = df["vleakn"].astype(float)
    vls = sorted(df["vleakn"].unique())
    cmap = plt.get_cmap("viridis")

    fig, ax = plt.subplots(figsize=(3.6, 2.5))
    for i, vl in enumerate(vls):
        g = df[df["vleakn"] == vl].sort_values("dt_ms")
        ax.plot(g["dt_ms"], g["p_fire"], marker="o", ms=2.5, linewidth=1.0,
                color=cmap(i / max(1, len(vls) - 1)),
                label=rf"$V_{{leakn}}$={vl:.3f}")

    ax.set_xlabel(r"Inter-input interval $\Delta t$ (ms)")
    ax.set_ylabel(r"$P(\mathrm{spike})$")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.15, linewidth=0.3)
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    for ext in (".pdf", ".png"):
        fig.savefig(out_base + "_vleakn" + ext, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_base}_vleakn.pdf")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="Per-neuron coincidence window characterization")
    ap.add_argument("--neurons", default=",".join(str(i) for i in range(16)),
                    help="Comma-separated neuron indices (default: 0-15)")
    ap.add_argument("--syn-a", type=int, default=0)
    ap.add_argument("--syn-b", type=int, default=1)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--dt-min", type=float, default=-15.0, help="ms")
    ap.add_argument("--dt-max", type=float, default=15.0, help="ms")
    ap.add_argument("--dt-step", type=float, default=1.0, help="ms")
    ap.add_argument("--trials", type=int, default=30)
    ap.add_argument("--window", type=float, default=0.03, help="response window (s)")
    ap.add_argument("--vleakn", default=None,
                    help="Comma list of vleakn for τ_mem family (single neuron only)")
    ap.add_argument("--out", default="coincidence_array.csv")
    ap.add_argument("--plot-dir",
                    default="measurements/array/figures")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--jexc-boost", type=float, default=0.0,
                    help="Add this delta (V) to all JExcWn biases")
    args = ap.parse_args()

    neurons = [int(x) for x in args.neurons.split(",") if x.strip()]
    dts_ms = []
    v = args.dt_min
    while v <= args.dt_max + 1e-9:
        dts_ms.append(round(v, 3))
        v += args.dt_step

    # Constant listen window: covers max|dt| + response margin
    max_dt_s = max(abs(args.dt_min), abs(args.dt_max)) / 1000.0
    const_window = max_dt_s + args.window

    biases = load_biases(args.biases)
    if args.jexc_boost != 0:
        for i in range(4):
            k = f"JExcWn{i}"
            if k in biases:
                biases[k] = min(0.7, biases[k] + args.jexc_boost)
                print(f"  {k} boosted to {biases[k]:.4f}")
    plot_base = os.path.join(args.plot_dir, "coincidence_array")

    with BridgeSession(verbose=args.verbose) as b:
        # Apply biases and program both synapses
        print("Applying biases...")
        b.apply_biases(biases)
        time.sleep(1.0)
        b.program_weight(args.syn_a, args.weight, exc=True)
        b.program_weight(args.syn_b, args.weight, exc=True)
        time.sleep(0.3)

        with open(args.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["neuron", "vleakn", "dt_ms", "p_fire"])

            for nidx, neuron in enumerate(neurons):
                # Set up routes and monitor for this neuron
                b.route(args.syn_a, neuron, exc=True)
                b.route(args.syn_b, neuron, exc=True)
                b.monitor(neuron)
                time.sleep(0.3)

                # Detect which output index fires for this neuron
                out_idx = detect_output(b, args.syn_a, args.syn_b, neuron)
                if out_idx is None:
                    print(f"  n{neuron:2d}: NO OUTPUT at dt=0 — skipping")
                    continue
                print(f"  n{neuron:2d}: output index={out_idx}, sweeping Δt...")

                for dt_ms in dts_ms:
                    if dt_ms >= 0:
                        first, second = args.syn_a, args.syn_b
                    else:
                        first, second = args.syn_b, args.syn_a
                    pf = p_fire_coinc(b, first, second, neuron,
                                      abs(dt_ms) * 1000.0,
                                      out_idx, args.trials, const_window)
                    w.writerow([neuron, "", f"{dt_ms:.3f}", f"{pf:.4f}"])
                    f.flush()
                    print(f"    dt={dt_ms:+6.1f} ms  P={pf:.2f}")

                print(f"  n{neuron:2d}: done ({nidx + 1}/{len(neurons)})")

            # Optional: vleakn family on the first neuron
            if args.vleakn:
                vls = [float(x) for x in args.vleakn.split(",")]
                neuron = neurons[0]
                b.route(args.syn_a, neuron, exc=True)
                b.route(args.syn_b, neuron, exc=True)
                b.monitor(neuron)
                time.sleep(0.3)
                out_idx = detect_output(b, args.syn_a, args.syn_b, neuron)
                if out_idx is None:
                    print(f"  vleakn sweep: n{neuron} no output, skipping")
                else:
                    for vl in vls:
                        b.bias("vleakn", vl)
                        time.sleep(0.5)
                        print(f"  vleakn={vl:.3f}, n{neuron}:")
                        for dt_ms in dts_ms:
                            if dt_ms >= 0:
                                first, second = args.syn_a, args.syn_b
                            else:
                                first, second = args.syn_b, args.syn_a
                            pf = p_fire_coinc(b, first, second, neuron,
                                              abs(dt_ms) * 1000.0,
                                              out_idx, args.trials, const_window)
                            w.writerow([neuron, f"{vl:.4f}", f"{dt_ms:.3f}", f"{pf:.4f}"])
                            f.flush()
                            print(f"    dt={dt_ms:+6.1f} ms  P={pf:.2f}")
                    # Restore original vleakn
                    b.bias("vleakn", biases.get("vleakn", 0.26))

    print(f"\nWrote {args.out}")

    # Generate plots
    print("Generating figures...")
    plot_overlaid_curves(args.out, plot_base)
    plot_window_widths(args.out, plot_base)
    if args.vleakn:
        plot_vleakn_family(args.out, plot_base)

    # Print summary table
    import pandas as pd
    df = pd.read_csv(args.out)
    df_main = df[df["vleakn"].isna() | (df["vleakn"] == "")]
    print(f"\n{'Neuron':>8}  {'W₅₀ (ms)':>10}  {'Peak P':>8}")
    print("-" * 30)
    for n in sorted(df_main["neuron"].unique()):
        g = df_main[df_main["neuron"] == n].sort_values("dt_ms")
        dts = g["dt_ms"].values.tolist()
        pfs = g["p_fire"].values.tolist()
        w50, _, _ = compute_fwhm(dts, pfs)
        peak = max(pfs)
        w_str = f"{w50:.1f}" if not np.isnan(w50) else "N/A"
        print(f"  n{n:2d}      {w_str:>10}  {peak:8.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
