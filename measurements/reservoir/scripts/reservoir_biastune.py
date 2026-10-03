#!/usr/bin/env python3
"""Phase-0 reservoir bias tuning: find a (vleakn, ifdcp) operating point where the
16 neurons show maximum heterogeneity (a diverse mix of firing / near-threshold /
quiet nodes) -- the raw material for a reservoir. Reducing vleakn lowers the leak so
neurons begin to fire, at different thresholds due to device mismatch.

Measures the resting per-neuron firing rate (no stimulation) across a vleakn (and
optionally ifdcp) sweep and scores diversity. Save the chosen point as a .biases file
in the GUI (or via set_bias) once identified.

Example:
  python reservoir_biastune.py --vleakn 0.26,0.24,0.22,0.20,0.18,0.16,0.14,0.12,0.10
"""

import argparse
import csv
import os
import time

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "bin",
                      "bias_synapse_characterization_super_n14.biases")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--biases", default=PRESET)
    ap.add_argument("--vleakn", default="0.26,0.24,0.22,0.20,0.18,0.16,0.14,0.12,0.10")
    ap.add_argument("--ifdcp", default=None, help="optional ifdcp list (default: keep preset)")
    ap.add_argument("--rest-s", type=float, default=4.0, help="resting-rate sample window (s)")
    ap.add_argument("--settle", type=float, default=1.0)
    ap.add_argument("--out", default="reservoir_biastune.csv")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    biases = load_biases(args.biases)
    vls = [float(x) for x in args.vleakn.split(",")]
    ids = [float(x) for x in args.ifdcp.split(",")] if args.ifdcp else [biases.get("ifdcp", 1.78)]

    rows = []
    with BridgeSession(verbose=args.verbose) as b:
        b.apply_biases(biases)
        time.sleep(1.0)
        print(f"{'ifdcp':>6} {'vleakn':>7} {'n_act':>6} {'mean':>6} {'std':>6} {'max':>6}   per-neuron (Hz)")
        for idc in ids:
            b.bias("ifdcp", idc)
            for vl in vls:
                b.bias("vleakn", vl)
                time.sleep(args.settle)
                res = b.sample_spikes(args.rest_s)
                pn = res["per_neuron_hz"]
                rates = [pn[i] for i in range(16)]
                active = [r for r in rates if r > 0.5]
                n_act = len(active)
                mean = sum(active) / n_act if n_act else 0.0
                import statistics as st
                std = st.pstdev(rates) if any(rates) else 0.0
                nz = {i: round(rates[i], 1) for i in range(16) if rates[i] > 0.3}
                rows.append([idc, vl] + [round(r, 3) for r in rates])
                print(f"{idc:6.2f} {vl:7.3f} {n_act:6d} {mean:6.1f} {std:6.1f} {max(rates):6.1f}   {nz}")

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ifdcp", "vleakn"] + [f"n{i}_hz" for i in range(16)])
        w.writerows(rows)
    print("\nwrote", args.out)
    print("Pick the row with a good spread (mix of firing rates across neurons), "
          "high 'std' and a moderate 'n_act' (not all-on, not all-off).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
