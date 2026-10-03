#!/usr/bin/env python3
"""On-chip temporal coincidence-detection experiment.

Two inputs are delivered to one neuron (synA and synB, or the same synapse twice)
separated by a RISC-V-timed interval dt. In the coincidence regime -- one input
alone subthreshold, two coincident inputs suprathreshold -- the neuron fires only
when the two EPSPs summate within the membrane integration window. Sweeping dt maps
out that window (output firing probability vs dt); sweeping the leak bias vleakn
(membrane time constant) tunes its width.

Bias regime (tune in the GUI, save a preset like the synfire biases): a SINGLE input
EPSP must be subthreshold while TWO coincident EPSPs cross threshold, biased near
threshold so analog noise makes P_fire graded rather than a hard step.

Modes:
  --mode regime   sweep JExcWn and report single-input vs coincident P_fire (find the regime)
  --mode window   sweep dt (and optionally vleakn) -> coincidence window CSV + plot

Example:
  python coincidence_run.py --mode regime --syn-a 0 --syn-b 1 --neuron 14
  python coincidence_run.py --mode window --syn-a 0 --syn-b 1 --neuron 14 \
      --jexc 0.55 --dt-min -25 --dt-max 25 --dt-step 2 --trials 30 \
      --vleakn 0.24,0.26,0.28 --out coincidence.csv
"""

import argparse
import csv
import os
import queue
import time

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "efficacysearch.json")


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


def dominant_after_coinc(b, syn_a, syn_b, neuron, reps=8, window_s=0.05):
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
    # window_s is a CONSTANT listen window (same for every dt) so the measurement
    # sensitivity is independent of dt. The caller sizes it to exceed max|dt| + a
    # response margin so both inputs' effects are always captured.
    fires = 0
    for _ in range(trials):
        b.drain(max_lines=100000)
        b.coincidence(first, second, neuron, dt_us)
        if wait_fire(b, out_idx, window_s):
            fires += 1
    return fires / trials


def p_fire_single(b, syn, neuron, out_idx, trials, window_s):
    """One input alone (via a huge-dt coincidence with both on the same synapse the
    second input lands 50 ms later, well outside the window, so this measures the
    single-EPSP response)."""
    fires = 0
    for _ in range(trials):
        b.drain(max_lines=100000)
        # Fire just one input by staging syn->neuron and sending a single spike.
        b.route(syn, neuron, exc=True)
        b.fire(1)
        if wait_fire(b, out_idx, window_s):
            fires += 1
    return fires / trials


def mode_regime(b, args, out_idx):
    print(f"{'JExcWn':>8} {'single':>8} {'coinc dt=0':>12}")
    for jx in [round(x, 3) for x in frange(args.jexc_lo, args.jexc_hi, args.jexc_step)]:
        for i in range(4):
            b.bias(f"JExcWn{i}", jx)
        time.sleep(0.3)
        ps = p_fire_single(b, args.syn_a, args.neuron, out_idx, args.trials, args.window)
        pc = p_fire_coinc(b, args.syn_a, args.syn_b, args.neuron, 0.0, out_idx, args.trials, args.window)
        flag = "  <== coincidence regime" if (ps < 0.2 and pc > 0.8) else ""
        print(f"{jx:8.3f} {ps:8.2f} {pc:12.2f}{flag}")


def mode_window(b, args, out_idx):
    dts = [round(x, 3) for x in frange(args.dt_min, args.dt_max, args.dt_step)]
    vleakns = [float(x) for x in args.vleakn.split(",")] if args.vleakn else [None]
    # Constant listen window (same for every dt) sized to cover the firmware busy-wait
    # of the largest |dt| plus a response margin, so measurement sensitivity is dt-independent.
    max_dt_s = max(abs(args.dt_min), abs(args.dt_max)) / 1000.0
    const_window = max_dt_s + args.window
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vleakn", "dt_ms", "p_fire"])
        for vl in vleakns:
            if vl is not None:
                b.bias("vleakn", vl)
                time.sleep(0.5)
            for dt_ms in dts:
                # signed dt: negative -> synB first
                if dt_ms >= 0:
                    first, second = args.syn_a, args.syn_b
                else:
                    first, second = args.syn_b, args.syn_a
                pf = p_fire_coinc(b, first, second, args.neuron, abs(dt_ms) * 1000.0,
                                  out_idx, args.trials, const_window)
                w.writerow([vl if vl is not None else "", f"{dt_ms:.3f}", f"{pf:.4f}"])
                f.flush()
                print(f"vleakn={vl}  dt={dt_ms:+.1f} ms  P_fire={pf:.2f}")
    make_plot(args.out, args.plot)


def frange(lo, hi, step):
    n = int(round((hi - lo) / step))
    return [lo + i * step for i in range(n + 1)]


def make_plot(csv_path, plot_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    matplotlib.rcParams.update({"pdf.fonttype": 42})
    df = pd.read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(3.6, 2.5))
    groups = df.groupby("vleakn") if df["vleakn"].notna().any() and (df["vleakn"] != "").any() else [(None, df)]
    cmap = plt.get_cmap("viridis")
    gl = list(df.groupby("vleakn")) if df["vleakn"].astype(str).str.len().gt(0).any() else [("", df)]
    for i, (vl, g) in enumerate(gl):
        g = g.sort_values("dt_ms")
        label = f"$V_{{leakn}}$={vl}" if str(vl) else None
        ax.plot(g["dt_ms"], g["p_fire"], marker="o", ms=3,
                color=cmap(i / max(1, len(gl) - 1)), label=label)
    ax.set_xlabel(r"Inter-input interval $\Delta t$ (ms)", fontsize=11)
    ax.set_ylabel("P(output spike)", fontsize=11)
    ax.tick_params(labelsize=10)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.25, linewidth=0.5)
    if any(str(vl) for vl, _ in gl):
        ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(plot_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(plot_path)[0] + ".png", dpi=150, bbox_inches="tight")
    print(f"Plot -> {plot_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["regime", "window"], default="window")
    ap.add_argument("--syn-a", type=int, default=0)
    ap.add_argument("--syn-b", type=int, default=1)
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--jexc", type=float, default=None, help="fixed JExcWn (window mode)")
    ap.add_argument("--vleakn", default=None, help="comma list of vleakn for the window family")
    # regime scan
    ap.add_argument("--jexc-lo", type=float, default=0.45)
    ap.add_argument("--jexc-hi", type=float, default=0.65)
    ap.add_argument("--jexc-step", type=float, default=0.02)
    # dt sweep
    ap.add_argument("--dt-min", type=float, default=-25.0, help="ms")
    ap.add_argument("--dt-max", type=float, default=25.0, help="ms")
    ap.add_argument("--dt-step", type=float, default=2.0, help="ms")
    ap.add_argument("--trials", type=int, default=30)
    ap.add_argument("--window", type=float, default=0.03, help="response window (s)")
    ap.add_argument("--out", default="coincidence.csv")
    ap.add_argument("--plot", default="measurements/array/figures/coincidence_window.pdf")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    biases = load_biases(args.biases)
    if args.jexc is not None:
        for i in range(4):
            biases[f"JExcWn{i}"] = args.jexc

    with BridgeSession(verbose=args.verbose) as b:
        b.apply_biases(biases)
        time.sleep(1.0)
        b.program_weight(args.syn_a, args.weight, exc=True)
        b.program_weight(args.syn_b, args.weight, exc=True)
        b.monitor(args.neuron)
        time.sleep(0.3)
        out_idx = dominant_after_coinc(b, args.syn_a, args.syn_b, args.neuron)
        if out_idx is None:
            print("No output detected at dt=0 — raise efficacy or check biases.")
            return 1
        print(f"Responding output index: {out_idx}")
        if args.mode == "regime":
            mode_regime(b, args, out_idx)
        else:
            mode_window(b, args, out_idx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
