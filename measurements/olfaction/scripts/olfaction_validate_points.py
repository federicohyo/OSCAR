#!/usr/bin/env python3
"""Re-acquire the operating points that matter, ARCHIVING THE SPIKES, and score them
per-chunk and voted at every depth.

Why this exists. The BO evaluated 13 points x 3 reps x 150 chunks and kept only a scalar
per-chunk accuracy: `score()` returns the predictions and the caller discarded them, so
voted accuracy -- one line away and free -- was left uncomputed, and the spikes were left
unwritten. Recovering it requires going back to the chip. F. Corradi, on being
shown the gap: "then we probably need to save the spikes..." Quite.

So this takes the points worth keeping (the incumbent, the BO's best, and any others
named), re-acquires each with --reps, writes every rep's spikes to disk, and reports
per-chunk plus voted k=1..5 with a spread over reps. Scoring is identical to
olfaction_iso_compare.py, so the numbers drop straight into the comparison against the
digital baseline (0.880 per-chunk / 0.967 voted5).

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_validate_points.py
"""
import argparse, json, os, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_run import INTEGRITY
from olfaction_bias_bo import (aer_scan, apply_offsets, build, encoders, measure, score,
                               AERLatch)
from olfaction_iso_compare import vote_acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", default="data/olfaction_bias_bo_reps3.json")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--tpresent", type=float, default=0.15)
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--top", type=int, default=2, help="also validate the N best live points")
    ap.add_argument("--bias-pattern",
                    default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--spike-dir", default="data/olfaction/olf_validate")
    ap.add_argument("--out", default="data/olfaction_validate.json")
    args = ap.parse_args()
    neurons = list(range(16))
    os.makedirs(args.spike_dir, exist_ok=True)

    st = json.load(open(args.state))
    hist = st["history"]
    zero = {k: 0.0 for k in ("d_vleakn", "d_vthrdn", "d_exc", "d_inh")}
    pts = [("centre", zero)]
    live = sorted([h for h in hist if h["live"] >= 14], key=lambda h: -h["acc"])
    for n, h in enumerate(live[:args.top]):
        pts.append((f"bo_best{n+1}", h["x"]))
    print(f"validating {len(pts)} points x {args.reps} reps, spikes -> {args.spike_dir}")

    F, Y, it, names = build("0.1s", args.theta, neurons)
    enc = encoders(F, args.theta, neurons)
    idx = np.arange(len(F))
    from sklearn.model_selection import GroupKFold
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    base = {k: load_biases(args.bias_pattern.format(k=k)) for k in neurons}

    res = {}
    with BridgeSession() as b:
        ok, bad, _ = aer_scan(b, neurons, base, tag="opening")
        if not ok:
            raise AERLatch(f"opening scan misaddressed: {bad}")
        for tag, off in pts:
            accs, votes, rates, lives = [], [], [], []
            for rep in range(args.reps):
                sp, dd, ds = measure(b, neurons, base, enc, off, idx,
                                     args.tpresent, args.weight, mon=None)
                cnt = np.array([[len(sp[k, j]) for k in range(len(neurons))]
                                for j in range(len(idx))]) / args.tpresent
                a, pred = score(sp, Y, it, args.tpresent, folds)
                accs.append(a); rates.append(float(cnt.mean()))
                lives.append(int((cnt.mean(0) > 0).sum()))
                votes.append([vote_acc(pred, Y, it, kk) for kk in range(1, 6)])
                np.savez(f"{args.spike_dir}/{tag}_r{rep}.npz", spikes=sp, labels=Y,
                         trial=it, neurons=np.array(neurons), nproj=1,
                         classes=np.array(names), T=args.tpresent, duration="0.1s",
                         theta=args.theta, offsets=json.dumps(off),
                         **provenance(bias_files=[args.bias_pattern.format(k=k)
                                                  for k in neurons],
                                      task=f"olfaction_validate_{tag}"))
            v = np.array(votes)
            res[tag] = {"offsets": off, "acc": float(np.mean(accs)),
                        "acc_sd": float(np.std(accs)), "acc_reps": accs,
                        "voted": v.mean(0).tolist(), "voted_sd": v.std(0).tolist(),
                        "rate": float(np.mean(rates)), "live": int(min(lives))}
            o = ", ".join(f"{k[2:]} {vv*1000:+.0f}" for k, vv in off.items())
            print(f"\n{tag}  ({o} mV)")
            print(f"  {res[tag]['rate']:.1f} Hz, {res[tag]['live']}/16 live, "
                  f"per-chunk {res[tag]['acc']:.3f} +/- {res[tag]['acc_sd']:.3f}")
            print(f"  voted k=1..5: " + "  ".join(
                f"{m:.3f}+/-{s:.3f}" for m, s in zip(res[tag]["voted"], res[tag]["voted_sd"])))
            json.dump(res, open(args.out, "w"), indent=2)
        ok, bad, _ = aer_scan(b, neurons, base, tag="closing")
        if not ok:
            raise AERLatch(f"CLOSING scan misaddressed: {bad} -- results suspect")
    print(f"\nintegrity: drops={INTEGRITY['drops']} stalls={INTEGRITY['stalls']}")
    print(f"digital baseline: 0.880 per-chunk, 0.967 voted5")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
