#!/usr/bin/env python3
"""Find the quietest array operating point that still classifies -- the array's
counterpart of choosing the cheapest digital baseline that matches accuracy.

At the reference point the array runs at 108 Hz mean and emits 260 events per 150 ms
decision. The read-out costs 105 + 480 per event, so 260 events is 46.5 uJ -- more than
the entire measured digital kernel (31.7 uJ) before the analog rail is charged at all.
An embedded design keeps away from it there.

CRITERION, fixed before the sweep runs: minimise energy per decision
(P_analog*T + (105 + 480*events)*E_cycle) subject to accuracy within one standard
deviation of the best point observed. Higher vleakn is quieter (measured 2026-08-13:
lower vleakn = MORE active).

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_bias_sweep.py
"""
import argparse, json, time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from meas_common import BridgeSession, load_biases
from reservoir_run import INTEGRITY, present_delta
from olfaction_identity import chunks
from olfaction_run_array import encode

FS = 1000.0
P_ANALOG_W, E_CYCLE_J = 0.43e-3, 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480
E_OP3_J = 85215 * E_CYCLE_J          # measured Q16 digital kernel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offsets", default="0,0.010,0.020,0.030,0.040")
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--tpresent", type=float, default=0.15)
    ap.add_argument("--pattern", default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--out", default="data/olfaction_bias_sweep.json")
    args = ap.parse_args()
    neurons = list(range(16))

    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    dur = np.array([m[0] for m in meta]); m = dur == "0.1s"
    F, it = chunks(X[m], Th[m], t, 0.1, 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    keep = np.array([np.flatnonzero(it == j)[0] for j in np.unique(it)])
    F, Y = F[keep], Y[keep]
    enc = {}
    for k in neurons:
        w = np.random.default_rng(100 + k).normal(0, 1, 8)
        enc[k] = []
        for j in range(len(F)):
            s = F[j].reshape(50, 8) @ w
            s = (s - s.mean()) / (s.std() + 1e-9)
            enc[k].append(encode(s, args.theta))

    base = {k: load_biases(args.pattern.format(k=k)) for k in neurons}
    res = {}
    print(f"{len(F)} trials, criterion: min energy s.t. accuracy within 1 sd of best\n")
    print(f"{'d_vleakn':>9} {'mean Hz':>8} {'ev/dec':>7} {'live':>5} {'acc':>14} "
          f"{'E_array':>9} {'vs OP3':>8}")
    with BridgeSession() as b:
        for off in [float(x) for x in args.offsets.split(",")]:
            arr = np.zeros((len(neurons), len(F)))
            for i, k in enumerate(neurons):
                bi = dict(base[k]); bi["vleakn"] = bi["vleakn"] + off
                b.send(f"MASK {1 << k}")
                b.apply_biases(bi); b.monitor(k); time.sleep(0.7)
                b.program_weight(0, 15, exc=True); b.program_weight(0, 15, exc=False)
                for j in range(len(F)):
                    arr[i, j] = len(present_delta(b, k, enc[k][j], args.tpresent, 0, 0))
            rate = arr.T / args.tpresent
            per = rate.mean(0); ev = rate.sum(1).mean() * args.tpresent
            live = int((per > 0).sum())
            accs = []
            for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(rate, Y):
                mdl = make_pipeline(StandardScaler(),
                                    LogisticRegression(C=1, max_iter=3000,
                                                       class_weight="balanced"))
                mdl.fit(rate[tr], Y[tr]); accs.append((mdl.predict(rate[te]) == Y[te]).mean())
            a, sd = float(np.mean(accs)), float(np.std(accs))
            E = P_ANALOG_W * args.tpresent + (DRAIN_FIXED + DRAIN_MARGINAL * ev) * E_CYCLE_J
            res[f"{off:.3f}"] = dict(mean_hz=float(per.mean()), events=float(ev), live=live,
                                     acc=a, acc_sd=sd, E_J=float(E), ratio=float(E_OP3_J / E))
            print(f"{off*1000:+8.0f}m {per.mean():8.1f} {ev:7.0f} {live:5d} "
                  f"{a:8.3f} +/-{sd:.3f} {E*1e6:8.1f}u {E_OP3_J/E:7.2f}x")
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"\nintegrity: drops={INTEGRITY['drops']} stalls={INTEGRITY['stalls']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
