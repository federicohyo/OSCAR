#!/usr/bin/env python3
"""Generate per-neuron STRUCTURED stimulus traces for GUI bias tuning.

For each of the 16 structured feature-detector neurons (reservoir_structured.build_spec),
encode a representative beat with that neuron's feature-aware encoder and write it to
reservoir_delta_proj_n{k}.txt -- the file the Stim-N button loops. Pressing Stim-N then
drives the neuron with exactly the structured stimulus reservoir_run_structured.py uses,
so on-scope tuning transfers. Overwrites the random-projection Stim-N traces (regenerate
those with reservoir_gen_stim_delta.py if needed).
"""
import argparse
import numpy as np
from reservoir_structured import build_spec, encode_neuron

OUTDIR = "ofxCaravanViewer/bin"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--klass", type=int, default=0, help="representative beat class (0=N), single-beat mode only")
    ap.add_argument("--beats-npz", default=None,
                    help="load the EXACT collection beats (X_raw, rr) from this npz and emit a "
                         "per-neuron weak->strong MULTI-BEAT trace so on-scope tuning matches the "
                         "amplitude spread the collection actually presents")
    ap.add_argument("--n-beats", type=int, default=6, help="beats per multi-beat trace (npz mode)")
    ap.add_argument("--pctl", default="15,30,45,60,75,90",
                    help="feature-strength percentiles (over non-empty beats) to sample, npz mode")
    ap.add_argument("--T-ms", type=int, default=2000, help="ms per beat")
    ap.add_argument("--outdir", default=OUTDIR)
    args = ap.parse_args()

    spec = build_spec()

    if args.beats_npz:
        d = np.load(args.beats_npz, allow_pickle=True)
        X = d["X_raw"]; rr = d["rr"]
        N = len(X)
        pctls = [float(p) for p in args.pctl.split(",")][:args.n_beats]
        print(f"multi-beat mode: {N} beats from {args.beats_npz}, {len(pctls)} beats/trace "
              f"at percentiles {pctls} of per-neuron feature strength")
        for k, s in enumerate(spec):
            encs = [encode_neuron(np.asarray(X[bi], float), rr[bi], s) for bi in range(N)]
            cnt = np.array([len(e) for e in encs])
            nz = np.where(cnt > 0)[0]
            order = nz[np.argsort(cnt[nz])]                       # weak -> strong (non-empty)
            picks = [int(order[int(round(p / 100 * (len(order) - 1)))]) for p in pctls]
            path = f"{args.outdir}/reservoir_delta_proj_n{k}.txt"
            with open(path, "w") as f:
                f.write(f"# t_ms channel(0=UP/exc,1=DOWN/inh)  T_ms={args.T_ms}  "
                        f"n{k} STRUCTURED feature={s['feature']}  MULTI-BEAT "
                        f"beats={picks} events={[int(cnt[b]) for b in picks]} (weak->strong)\n")
                for i, bi in enumerate(picks):                    # concat beats on one time axis
                    for tf, ch in encs[bi]:
                        f.write(f"{(i + tf) * args.T_ms:.1f} {ch}\n")
            print(f"  n{k:2d} [{s['feature']:7s}] beats {picks} "
                  f"events {[int(cnt[b]) for b in picks]} -> {path}")
        print(f"\nwrote 16 MULTI-BEAT structured Stim-N traces to {args.outdir}/  (loop spans "
              f"{args.n_beats}x{args.T_ms}ms weak->strong; tune so each neuron fires on the "
              f"stronger beats, save super_n{{k}}_struct.biases)")
        return 0

    # legacy single-beat mode (needs wfdb download)
    from reservoir_data import get_beats
    X, y, meta = get_beats(records=tuple(args.records.split(",")), n_per_class=30, classes="NSV")
    i = int(np.where(y == args.klass)[0][0])
    beat, rr = np.asarray(X[i], float), meta["rr"][i]
    for k, s in enumerate(spec):
        ev = encode_neuron(beat, rr, s)
        path = f"{args.outdir}/reservoir_delta_proj_n{k}.txt"
        with open(path, "w") as f:
            f.write(f"# t_ms channel(0=UP/exc,1=DOWN/inh)  T_ms={args.T_ms}  "
                    f"n{k} STRUCTURED feature={s['feature']}\n")
            for tf, ch in ev:
                f.write(f"{tf*args.T_ms:.1f} {ch}\n")
        print(f"  n{k:2d} [{s['feature']:7s}] {len(ev):3d} events -> {path}")
    print(f"wrote 16 structured Stim-N traces to {args.outdir}/  (Stim-N now loops the "
          f"structured stimulus; tune each neuron suprathreshold, save super_n{{k}}_struct.biases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
