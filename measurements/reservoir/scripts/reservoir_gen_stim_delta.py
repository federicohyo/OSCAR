#!/usr/bin/env python3
"""Generate per-neuron projected delta-trace files for GUI bias tuning.

For each neuron k, apply its fixed input projection (reservoir_input_proj.json) to a
representative beat and delta-encode it, then write reservoir_delta_proj_n{k}.txt in the
same "t_ms channel" format the bridge's Stim-N loop reads. Looping neuron k's own
projected trace (feedforward, recurrence off) reproduces exactly the per-neuron drive of
reservoir_run_randproj.py, so tuning the bias on-scope matches the experiment.
"""
import argparse
import json
import numpy as np
from reservoir_data import get_beats, delta_encode_proj

OUTDIR = "ofxCaravanViewer/bin"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="reservoir_input_proj.json")
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--T-ms", type=int, default=2000)
    ap.add_argument("--klass", type=int, default=0, help="representative beat class (0=Normal)")
    ap.add_argument("--outdir", default=OUTDIR)
    args = ap.parse_args()

    proj = {int(c["neuron"]): c for c in json.load(open(args.config))["proj"]}
    X, y, _ = get_beats(records=tuple(args.records.split(",")), n_per_class=30, classes="NV")
    beat = X[np.where(y == args.klass)[0][0]]   # first beat of the chosen class

    for k, p in sorted(proj.items()):
        ev = delta_encode_proj(beat, sigma=p["sigma"], shift=p["shift"], theta=p["theta"])
        path = f"{args.outdir}/reservoir_delta_proj_n{k}.txt"
        with open(path, "w") as f:
            f.write(f"# t_ms channel(0=UP/exc,1=DOWN/inh)  T_ms={args.T_ms}  "
                    f"n{k} sigma={p['sigma']:.2f} shift={p['shift']:+.3f} theta={p['theta']:.3f}\n")
            for tf, ch in ev:
                f.write(f"{tf*args.T_ms:.1f} {ch}\n")
        print(f"  n{k:2d}: {len(ev):3d} events -> {path}")
    print(f"wrote 16 per-neuron projected delta traces to {args.outdir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
