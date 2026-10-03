#!/usr/bin/env python3
"""Odour identity vs pulse duration -- reproducing Dennler et al. Fig. 3D, then pricing it.

Their protocol, followed here: train on 50 ms data features taken from 1000 ms pulses,
test on pulses of 10-1000 ms. The classifier training set holds long pulses only, so
the accuracy-vs-duration curve is a genuine generalisation test, and it IS the
accuracy-versus-latency curve the cost argument needs.

Feature: a 50 ms chunk of the 8 sensor channels, prestimulus-baseline normalised. The
reference reports the un-normalised version "approaches random classification for low
concentrations", so the normalisation is load-bearing rather than cosmetic.

Classes follow the reference campaign: 2H, EB, Eu, IA and Blank, with b1/b2 (two identical pure
solvent samples) merged into Blank.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_identity.py
"""
import argparse, json
import numpy as np
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FS = 1000.0
P_ANALOG_W, E_CYCLE_J = 0.43e-3, 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480


def cycle_starts(Th):
    """Upward mean-crossings of the cycled heater = the phase reference.

    The 50 ms feature only works if it is PHASE-LOCKED to the hotplate cycle: the
    classifier is reading the sensor's response to a known temperature ramp, so a
    window at an arbitrary offset averages over different points of that ramp and
    throws the structure away. Measured here: channels 5-8 cycle at 20.0 Hz, period
    50.0 ms, while 1-4 are held at 400 C -- so one cycle IS one feature."""
    c = int(np.argmax(Th.max(0) - Th.min(0)))          # most strongly cycled channel
    x = Th[:, c] - Th[:, c].mean()
    return np.flatnonzero((x[:-1] <= 0) & (x[1:] > 0)) + 1


def chunks(X, Th, t, dur_s, wl_s, pre=(-0.4, -0.05), phase_locked=True, tail=0.05):
    """One-heater-cycle chunks inside the odour period, normalised by each trial's own
    prestimulus baseline. Phase-locked to that trial's own heater cycle."""
    w = int(wl_s * FS)
    base = X[:, (t >= pre[0]) & (t < pre[1]), :].mean(axis=1, keepdims=True)
    R = (X - base) / np.abs(base)
    # The sensor response OUTLASTS the pulse -- the reference campaign reports odour offset
    # detected ~106 ms after a pulse ends -- so the decision legitimately uses the
    # tail. With it a 50 ms pulse yields a chunk that can be voted on.
    lo, hi = 0.0, min(dur_s + tail, t[-1])
    F, trial = [], []
    for i in range(len(X)):
        if phase_locked:
            cs = cycle_starts(Th[i])
            starts = [a for a in cs if a + w < len(t) and lo <= t[a] and t[a + w] <= hi]
        else:
            starts = [a for a in range(0, len(t) - w, max(1, w // 2))
                      if lo <= t[a] and t[a + w] <= hi]
        if not starts:
            starts = [int((0.0 - t[0]) * FS)]
        for a in starts:
            F.append(R[i, a:a + w, :].ravel())
            trial.append(i)
    return np.array(F), np.array(trial)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="data_olfaction/olfaction_pulses.npz")
    ap.add_argument("--wl", type=float, default=0.050)
    ap.add_argument("--events", type=float, default=20.0)
    ap.add_argument("--tail", type=float, default=0.20,
                    help="evaluate this long past pulse end; the response outlasts it")
    ap.add_argument("--no-phase", action="store_true",
                    help="ablate the heater-phase alignment")
    ap.add_argument("--out", default="data/olfaction_identity.json")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    classes = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    dur = np.array([m[0] for m in meta])
    # merge the two solvent controls into one Blank class, as the reference campaign does
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(classes[k], classes[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])
    print(f"{len(X)} trials, {len(names)} classes {names}, chance {1/len(names):.3f}")

    tr = dur == "1.0s"
    Ftr, itr = chunks(X[tr], Th[tr], t, 1.0, args.wl, phase_locked=not args.no_phase)
    ytr = Y[tr][itr]
    clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=10, gamma="scale"))
    clf.fit(Ftr, ytr)
    print(f"trained on {len(Ftr)} chunks from {tr.sum()} 1000 ms pulses\n")

    e_read = (DRAIN_FIXED + args.events * DRAIN_MARGINAL) * E_CYCLE_J
    e_arr = P_ANALOG_W * args.wl + e_read
    print(f"E_array/decision {e_arr*1e6:.1f} uJ at a {args.wl*1000:.0f} ms window\n")
    print(f"{'pulse':>7} {'n trials':>9} {'n chunks':>9} {'per-chunk':>10} "
          f"{'vote (k)':>12} {'k':>8}")
    res = {}
    for D in ("0.01s", "0.02s", "0.05s", "0.1s", "0.2s", "0.5s", "1.0s"):
        m = dur == D
        if m.sum() == 0:
            continue
        ds = float(D.rstrip("s"))
        F, it = chunks(X[m], Th[m], t, ds, args.wl, phase_locked=not args.no_phase,
                       tail=args.tail)
        if len(F) == 0:
            continue
        pred = clf.predict(F)
        truth = Y[m][it]
        acc = float((pred == truth).mean())
        # PER-TRIAL majority vote over that trial's chunks. This is the reference campaign's
        # "prediction over time" evaluation, and it is also exactly the averaging that
        # is FREE to the array and costs the digital path one kernel run per vote.
        votes, tacc = [], []
        for j in np.unique(it):
            sel = it == j
            v = np.bincount(pred[sel], minlength=len(names)).argmax()
            tacc.append(v == truth[sel][0]); votes.append(int(sel.sum()))
        pacc = float(np.mean(tacc)); k = float(np.mean(votes))
        res[D] = {"acc_per_chunk": acc, "acc_per_trial_vote": pacc,
                  "mean_votes": k, "n_trials": int(m.sum()), "n_chunks": len(F),
                  "duration_s": ds, "E_array_J": e_arr,
                  "E_array_J_total": P_ANALOG_W * max(ds, args.wl) + k * e_read}
        print(f"{D:>7} {m.sum():9d} {len(F):9d} {acc:10.3f} {pacc:12.3f} {k:8.1f}")
    json.dump({"window_s": args.wl, "classes": names, "per_duration": res},
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
