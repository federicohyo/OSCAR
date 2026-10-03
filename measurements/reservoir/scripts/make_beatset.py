#!/usr/bin/env python3
"""Freeze one beat set to an .npz so every run uses EXACTLY the same beats.

`get_beats` is seeded, but the beat pool is assembled in the order the records are
passed, and `rng.choice` then samples from that pool -- so the same seed with the
records in a different order yields DIFFERENT beats. That silently confounded the
feedforward (0.987) vs virtual-diagonal comparison: same records, same n_per_class,
same seed, different beats (Jul 5 drew record 106 fifteen times, a later run seven).

Freeze it once, load it everywhere:

    ./.venv-meas/bin/python3 make_beatset.py --out beats_nv_30.npz \
        --records 106,119,208,221,233 --n-per-class 30 --classes NV

    ./.venv-meas/bin/python3 reservoir_run.py --beats beats_nv_30.npz ...
    ./.venv-meas/bin/python3 reservoir_run_recur_collapse.py --beats beats_nv_30.npz ...

The encoding (--thr) is deliberately NOT frozen here: it is a knob of the experiment,
not of the dataset. Keep it identical across runs you intend to compare.
"""
import argparse
import numpy as np

from reservoir_data import get_beats


def load_beatset(path):
    """Return (X, y, meta) exactly as get_beats would."""
    d = np.load(path, allow_pickle=True)
    meta = {"records": d["records"], "classes": str(d["classes"]),
            "k": int(d["k"]), "fs": int(d["fs"]), "length": int(d["length"])}
    if "rr" in d.files:
        meta["rr"] = d["rr"]
    return d["X"], d["y"], meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="106,119,208,221,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NV")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="beats_nv_30.npz")
    args = ap.parse_args()

    X, y, meta = get_beats(records=tuple(args.records.split(",")),
                           n_per_class=args.n_per_class,
                           classes=args.classes, seed=args.seed)
    np.savez(args.out, X=X, y=y, records=meta["records"], classes=meta["classes"],
             k=meta["k"], fs=meta["fs"], length=meta["length"], rr=meta["rr"],
             seed=args.seed, records_arg=args.records)

    import collections
    print(f"wrote {args.out}: {X.shape[0]} beats x {X.shape[1]} samples")
    print(f"  classes={meta['classes']}  per-class k={meta['k']}  seed={args.seed}")
    print(f"  label counts : {np.bincount(y).tolist()}")
    print(f"  record counts: {dict(collections.Counter(meta['records'].tolist()))}")
    print(f"  first 12 records: {meta['records'][:12].tolist()}")
    print("\nPass this file to every run you intend to compare.")


if __name__ == "__main__":
    main()
