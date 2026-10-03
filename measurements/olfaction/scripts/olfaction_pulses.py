#!/usr/bin/env python3
"""Extract the odour-identity pulse trials -- the task the paper gets 100% on.

Dennler et al. Fig. 3D: 5-way identity (2H, EB, Eu, IA, Blank), RBF-SVM on 50 ms data
features, 100% from 1000 ms down to 50 ms pulses. Their 50 ms feature is PHASE-LOCKED
to the 50 ms hotplate cycle, so the condition matters: LconstRcycle25ms and
LconstRcycle100ms cycle the right bank, Lcycle25msRcycle25ms cycles both.

We keep the heater-temperature channels too (T_heat_*), because the cycle phase is
what the features align to and we cannot reconstruct it from resistance alone.

    ./.venv-meas/bin/python3 olfaction_pulses.py
"""
import argparse, io, os, re, zipfile
import numpy as np, pandas as pd

ZIP = "data_olfaction/scoping/Dataset-FastMachineOlfaction.zip"
IDX = "Dataset-FastMachineOlfaction/Enose/index.csv"
CH = [f"R_gas_{i}" for i in range(1, 9)]
TH = [f"T_heat_{i}" for i in range(1, 9)]
KIND = re.compile(r"\d+_[^_]+_(corr|acorr|pulse|plume)_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", default="LconstRcycle25ms")
    ap.add_argument("--t0", type=float, default=-500.0)
    ap.add_argument("--t1", type=float, default=1500.0)
    ap.add_argument("--per-cell", type=int, default=15, help="trials per (duration, gas)")
    ap.add_argument("--out", default="data_olfaction/olfaction_pulses.npz")
    args = ap.parse_args()

    z = zipfile.ZipFile(ZIP)
    idx = pd.read_csv(io.BytesIO(z.read(IDX)))
    p = idx[(idx["kind"] == "pulse") & (idx["condition"] == args.condition)
            & (idx["concentration"] == 100)]
    # the short-duration cells only exist at a few durations; take them all, and cap
    # the 1.0 s cell so it does not dominate
    sel = (p.groupby(["shape", "gas1"], group_keys=False)
             .apply(lambda d: d.sample(min(len(d), args.per_cell), random_state=0)))
    print(f"{len(sel)} pulse trials, {args.condition}")
    print(sel.groupby(["shape", "gas1"]).size().unstack(fill_value=0).to_string())

    paths = {n.split("/")[-1]: n for n in z.namelist()
             if n.endswith(".csv") and "/._" not in n and "index" not in n}
    n_samp = int(args.t1 - args.t0)
    X, T, y, meta = [], [], [], []
    for i, r in enumerate(sel.itertuples()):
        cand = [k for k in paths if k.startswith(f"{r.trial_idx:05d}_")]
        if not cand:
            continue
        d = pd.read_csv(io.BytesIO(z.read(paths[cand[0]])))
        t = d["time_ms"].values
        m = (t >= args.t0) & (t < args.t1)
        g = d.loc[m, CH].values.astype(np.float32)
        h = d.loc[m, [c for c in TH if c in d.columns]].values.astype(np.float32)
        if g.shape[0] < n_samp - 5:
            continue
        X.append(g[:n_samp]); T.append(h[:n_samp])
        y.append(str(r.gas1)); meta.append((str(r.shape), str(r.gas1), int(r.trial_idx)))
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(sel)}")
    X, T = np.stack(X), np.stack(T)
    classes = sorted(set(y)); yi = np.array([classes.index(v) for v in y])
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez_compressed(args.out, X=X, T=T, y=yi, classes=np.array(classes),
                        meta=np.array(meta, dtype=object), t0=args.t0, fs_hz=1000.0)
    print(f"\nwrote {args.out}: X {X.shape}, {len(classes)} classes {classes}")
    print("per class:", {c: int((yi == k).sum()) for k, c in enumerate(classes)})


if __name__ == "__main__":
    raise SystemExit(main())
