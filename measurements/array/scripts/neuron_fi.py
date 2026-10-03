#!/usr/bin/env python3
"""Neuron f-I transfer curve: free-running firing rate vs the charging bias ifdcp.

No stimulation; synapses off (JExcWn=0). Sweeps ifdcp from a quiet (high) value
down toward strong charging, sampling per-neuron output rate over the AER path.
Produces a clean f-I curve for a representative neuron plus the 16-neuron spread.

Output CSV columns: step, ifdcp_v, total_hz, n0_hz..n15_hz

Example:
  python neuron_fi.py --ifdcp-start 1.47 --ifdcp-stop 1.20 --ifdcp-step 0.005 \
      --settle 1.0 --sample 2.0 --out neuron_fi.csv
"""

import argparse
import csv
import os
import time

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "ifdcp_vs_vleakn_plot.json")


def frange_desc(start: float, stop: float, step: float):
    """Descending inclusive range using integer-mV stepping (avoids fp drift)."""
    n = int(round((start - stop) / step))
    for i in range(n + 1):
        yield round(start - i * step, 6)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ifdcp-start", type=float, default=1.47)
    ap.add_argument("--ifdcp-stop", type=float, default=1.20)
    ap.add_argument("--ifdcp-step", type=float, default=0.005)
    ap.add_argument("--vleakn", type=float, default=None, help="override leak bias")
    ap.add_argument("--settle", type=float, default=1.0)
    ap.add_argument("--sample", type=float, default=2.0)
    ap.add_argument("--out", default="neuron_fi.csv")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    biases = load_biases(PRESET)
    if args.vleakn is not None:
        biases["vleakn"] = args.vleakn

    with BridgeSession(verbose=args.verbose) as b, open(args.out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["step", "ifdcp_v", "total_hz"] + [f"n{i}_hz" for i in range(16)])
        b.apply_biases(biases)
        time.sleep(args.settle)

        for step, ifdcp in enumerate(frange_desc(args.ifdcp_start, args.ifdcp_stop, args.ifdcp_step), 1):
            b.bias("ifdcp", ifdcp)
            time.sleep(args.settle)
            res = b.sample_spikes(args.sample)
            pn = res["per_neuron_hz"]
            row = [step, f"{ifdcp:.4f}", f"{res['total_hz']:.3f}"] + [f"{pn[i]:.3f}" for i in range(16)]
            wr.writerow(row)
            f.flush()
            active = sum(1 for i in range(16) if pn[i] > 0.5)
            print(f"ifdcp={ifdcp:.4f}  total={res['total_hz']:.1f} Hz  active_neurons={active}")

    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
