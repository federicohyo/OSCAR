#!/usr/bin/env python3
"""Phase 0 step 1: pull the correlated / anti-correlated pulse-train trials out of the
Dryad archive into one compact npz.

Dataset: Dennler et al., "High-speed odour sensing using miniaturised electronic nose",
Read-only, kept unmodified;
the 14.7 GB archive stays out of version control here (see .gitignore).

WHY THIS TASK. Two odours are pulsed either in phase (`corr`) or in antiphase
(`acorr`) at a commanded modulation frequency. The stimulus control, verified on the
valve traces before any analysis:

    corr   EB total 250.0  IA total 250.0   corr(EB,IA) = +1.000
    acorr  EB total 250.0  IA total 250.0   corr(EB,IA) = -0.333

Both classes deliver *exactly the same amount of each gas*, so a rate code over the
window carries ZERO information about the class, and any classifier that succeeds is
necessarily using temporal structure. That is true by construction of the stimulus
rather than by argument, which is what makes this the olfactory analogue of the XOR
control.

Trials are 35 s at 1 kHz with 8 MOx channels; only the stimulus window is kept, so the
output is ~100 MB rather than the ~4 GB the raw trials would take.

    ./.venv-meas/bin/python3 olfaction_extract.py            # one condition, balanced
    ./.venv-meas/bin/python3 olfaction_extract.py --all-conditions
"""
import argparse
import io
import os
import re
import zipfile

import numpy as np
import pandas as pd

ZIP = "data_olfaction/scoping/Dataset-FastMachineOlfaction.zip"
IDX = "Dataset-FastMachineOlfaction/Enose/index.csv"
CH = [f"R_gas_{i}" for i in range(1, 9)]
# valve control values: the olfactometer's own record of WHICH odour was
# open WHEN, at 1 kHz. This is dense per-sample ground truth and it turns a
# trial-labelled benchmark into a streaming detection task.
VALVE = ["EB", "IA", "Eu", "2H", "b1", "b2"]
KIND_RE = re.compile(r"\d+_[^_]+_(corr|acorr|pulse|plume)_")


def kind_of(path):
    """Match on the delimited field, not a substring -- '_corr_' occurs inside
    '_acorr_' and a naive filter silently returns only anti-correlated trials."""
    m = KIND_RE.match(path.split("/")[-1])
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", default="LconstRcycle25ms")
    ap.add_argument("--all-conditions", action="store_true")
    ap.add_argument("--t0", type=float, default=-1000.0, help="window start, ms re odour onset")
    ap.add_argument("--t1", type=float, default=6000.0, help="window end, ms")
    ap.add_argument("--out", default="data_olfaction/olfaction_corr_acorr.npz")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    z = zipfile.ZipFile(ZIP)
    idx = pd.read_csv(io.BytesIO(z.read(IDX)))
    conds = sorted(idx["condition"].unique()) if args.all_conditions else [args.condition]
    paths = {n.split("/")[-1]: n for n in z.namelist()
             if n.endswith(".csv") and "/._" not in n and "index" not in n}

    rng = np.random.default_rng(args.seed)
    sel = []
    for cond in conds:
        sub = idx[(idx["condition"] == cond) & (idx["kind"].isin(["corr", "acorr"]))].copy()
        # match acorr to the gas pairs corr actually has, unordered, so the two
        # classes are separable by features beyond which odours were present
        pairs = {frozenset((r.gas1, r.gas2)) for r in
                 sub[sub["kind"] == "corr"].itertuples()}
        sub["pair"] = [frozenset((r.gas1, r.gas2)) for r in sub.itertuples()]
        sub = sub[sub["pair"].isin(pairs)]
        for freq, g in sub.groupby("shape"):
            c = g[g["kind"] == "corr"]
            a = g[g["kind"] == "acorr"]
            n = min(len(c), len(a))
            if n == 0:
                continue
            # stratify the acorr draw across gas pairs so every one contributes
            a = (a.groupby("pair", group_keys=False)
                   .apply(lambda d: d.sample(min(len(d), max(1, n // max(1, a['pair'].nunique()))),
                                             random_state=args.seed))
                 )
            a = a.sample(min(n, len(a)), random_state=args.seed)
            c = c.sample(min(n, len(c)), random_state=args.seed)
            sel.append(pd.concat([c, a]))
    sel = pd.concat(sel, ignore_index=True)
    print(f"selected {len(sel)} trials over {len(conds)} condition(s)")
    print(sel.groupby(["condition", "shape", "kind"]).size().unstack(fill_value=0).to_string())

    X, V, y, meta = [], [], [], []
    miss = 0
    for i, r in enumerate(sel.itertuples()):
        fn = f"{r.trial_id}.csv" if f"{r.trial_id}.csv" in paths else None
        if fn is None:
            cand = [k for k in paths if k.startswith(f"{r.trial_idx:05d}_")]
            fn = cand[0] if cand else None
        if fn is None:
            miss += 1
            continue
        d = pd.read_csv(io.BytesIO(z.read(paths[fn])))
        have_v = [c for c in VALVE if c in d.columns]
        t = d["time_ms"].values
        m = (t >= args.t0) & (t < args.t1)
        g = d.loc[m, CH].values.astype(np.float32)
        if g.shape[0] < int(args.t1 - args.t0) - 5:      # short/ragged trial
            miss += 1
            continue
        v = d.loc[m, have_v].values.astype(np.float32)
        X.append(g[:int(args.t1 - args.t0)])
        V.append(v[:int(args.t1 - args.t0)])
        y.append(1 if r.kind == "acorr" else 0)
        meta.append((r.condition, r.shape, r.gas1, r.gas2, int(r.trial_idx)))
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(sel)}")

    X = np.stack(X)
    V = np.stack(V)
    y = np.array(y)
    meta = np.array(meta, dtype=object)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    np.savez_compressed(args.out, X=X, V=V, y=y, meta=meta, channels=CH,
                        valves=np.array(have_v),
                        t0=args.t0, t1=args.t1, fs_hz=1000.0,
                        classes=np.array(["corr", "acorr"]))
    print(f"\nwrote {args.out}: X {X.shape} (trials, samples, channels), "
          f"{X.nbytes/1e6:.0f} MB in memory, {miss} skipped")
    print(f"class balance: corr {int((y==0).sum())}  acorr {int((y==1).sum())}")


if __name__ == "__main__":
    raise SystemExit(main())
