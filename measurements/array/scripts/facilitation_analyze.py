#!/usr/bin/env python3
"""Analyze the Experiment (i) facilitation curve: P(fire | inter-pair spacing S).

Reads the per-trial CSV from coincidence_facilitation.py, reports P(fire | S) as
mean +- s.d. over the repeats, fits the recovery time constant on the descending
(facilitated -> rested) branch, and checks the reference-S drift monitor for slow drift.
"""
import argparse
import csv
import numpy as np


def load(path):
    rows = list(csv.DictReader(open(path)))
    return rows


def per_S(rows, block):
    """{S_ms: {repeat: p_fire}} for the given block type ('sweep' or 'ref')."""
    d = {}
    for r in rows:
        if r["block"] != block:
            continue
        S = float(r["S_ms"]); rep = int(r["repeat"]); fired = int(r["fired"])
        d.setdefault(S, {}).setdefault(rep, []).append(fired)
    out = {}
    for S, reps in d.items():
        out[S] = {rep: float(np.mean(v)) for rep, v in reps.items() if v}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trials_csv")
    args = ap.parse_args()
    rows = load(args.trials_csv)
    tag = rows[0]["tag"]; jexc0 = rows[0]["jexc0"]

    sweep = per_S(rows, "sweep")
    Ss = sorted(sweep)
    print(f"== facilitation curve (tag={tag}, JExcWn0={jexc0}) ==")
    print(f"{'S (ms)':>8}  {'P(fire) mean':>12}  {'s.d.':>6}  {'n_rep':>5}")
    means = {}
    for S in Ss:
        vals = list(sweep[S].values())
        m, sd = float(np.mean(vals)), float(np.std(vals))
        means[S] = m
        print(f"{S:>8.1f}  {m:>12.3f}  {sd:>6.3f}  {len(vals):>5}")

    # recovery time constant on the descending branch (from the peak S outward)
    S_peak = max(means, key=means.get)
    P_peak = means[S_peak]
    P_rest = means[max(Ss)]
    desc = [(S, means[S]) for S in Ss if S >= S_peak]
    print(f"\npeak P={P_peak:.3f} at S={S_peak:.0f} ms; rested P={P_rest:.3f} at S={max(Ss):.0f} ms")
    if len(desc) >= 3 and (P_peak - P_rest) > 0.15:
        xs = np.array([s for s, _ in desc]); ys = np.array([p for _, p in desc])
        # P(S) = P_rest + (P_peak-P_rest) exp(-(S-S_peak)/tau); solve tau by log-linear fit
        z = (ys - P_rest) / max(1e-6, (P_peak - P_rest))
        ok = z > 0.02
        if ok.sum() >= 2:
            tau = -np.polyfit(xs[ok] - S_peak, np.log(z[ok]), 1)[0]
            tau = 1.0 / tau if tau != 0 else float("inf")
            # S at half-recovery
            s_half = S_peak + tau * np.log(2)
            print(f"recovery tau ~= {tau:.1f} ms (half-recovery spacing ~= {s_half:.0f} ms)")
        else:
            print("recovery tau: not enough points above rested floor to fit")
    else:
        print("recovery tau: descending branch too flat to fit")

    # reference-S drift monitor
    ref = per_S(rows, "ref")
    ref = {S: v for S, v in ref.items() if any(len(rows) for rows in [v])}
    ref_vals = []
    for S in sorted(ref):
        for rep in sorted(ref[S]):
            ref_vals.append((rep, ref[S][rep]))
    if ref_vals:
        ps = [p for _, p in ref_vals]
        print(f"\nref-S drift monitor: {len(ps)} blocks, P range "
              f"[{min(ps):.2f}, {max(ps):.2f}], mean {np.mean(ps):.2f} +- {np.std(ps):.2f}")
        print("  (large spread here = session drift/hysteresis; interpret sweep with care)")


if __name__ == "__main__":
    raise SystemExit(main())
