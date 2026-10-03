#!/usr/bin/env python3
"""Find a quieter operating point using the CALIBRATED weight ladder, not vleakn.

F. Corradi, 2026-08-13: "maybe we can play with the weights values -- we did calibrate
them in the paper." Right, and it is the better knob.

At the reference point the four weight branches sit within 10 mV of each other, so the
word delivers popcount(w): five levels, non-monotonic at the carries, and w<=7 drops
most of the array silent ([[weight-code-is-popcount-not-binary]]). Useless as a dial.
The published calibration fixes that. In weak inversion I_j = I* exp((V_j - V_j0)/nUT),
so setting

    V_j = V_cm + (V_j0 - V_00) + j * nUT * ln2

cancels each branch's mismatch and builds the binary ratio, and delivered charge becomes
A(w) = w exactly. Word w then spans 1..15 monotonically. Since the reference delivers
popcount(15) = 4 units, w in {1,2,3,4} is a 1/4x .. 1x drive dial at the SAME common
mode -- which is what "fewer spikes" needs, without touching leak or threshold.

LIMIT, stated because it bounds the result: the ladder (data/synapse/ladder_n5_25mhz)
was measured on n5 ONLY. The octave term nUT*ln2 = 21.5 mV is device physics and is
shared; the mismatch term is n5's. On the other 15 neurons the ladder is therefore
partially calibrated, and each neuron keeps its own reference common mode V_cm = its own
JExcWn0. Inhibition gets the binary term only -- its branch onsets were never measured --
and PMOS polarity inverts the sign.

WHY THE WEIGHT AND NOT THE LEAK (measured 2026-08-13). The rate here is EVOKED: ~16
output spikes from 29 input events per presentation. Cutting it with vleakn fails --
probed at +60 mV it silenced 6/16 neurons and at +90 mV 9/16, while the rate only fell
108 -> 45 Hz, never near the 20 Hz the simulation wants. Leak and threshold remove
RESPONSIVENESS; only the weight scales charge per event while leaving the neuron able to
answer its input. So the ladder is the rate knob for this task.

CRITERION: maximise accuracy first (F. Corradi: "we need a way to pump up accuracy not
making the array cheaper"), report energy alongside. Scored exactly like
olfaction_iso_compare.py -- all 150 chunks, grouped folds, kernel read-out, voted -- so
every row is directly comparable to the digital 0.880 / 0.967.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_weight_sweep.py
"""
import argparse, json, math, time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from meas_common import BridgeSession, load_biases
from reservoir_run import INTEGRITY, present_delta
from olfaction_identity import chunks
from olfaction_run_array import encode
from olfaction_iso_compare import kernel, vote_acc

FS = 1000.0
P_ANALOG_W, E_CYCLE_J = 0.43e-3, 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480
E_OP3_J = 85215 * E_CYCLE_J          # measured Q16 digital kernel


def ladder(path="data/synapse/ladder_n5_25mhz.json"):
    d = json.load(open(path))
    return d["offsets"], d["nUT_volts"]


def apply_ladder(b0, off, exc=True):
    """Branch biases for a common mode taken from the neuron's own reference bit-0."""
    return [b0 + o if exc else b0 - o for o in off]


def load_task(theta, neurons):
    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == "0.1s"
    F, it = chunks(X[m], Th[m], t, 0.1, 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    enc = {}
    for k in neurons:
        w = np.random.default_rng(100 + k).normal(0, 1, 8)
        e = []
        for j in range(len(F)):
            s = F[j].reshape(50, 8) @ w
            e.append(encode((s - s.mean()) / (s.std() + 1e-9), theta))
        enc[k] = e
    return F, Y, it, enc, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", default="1,2,4,8")
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--tpresent", type=float, default=0.15)
    ap.add_argument("--pattern", default="ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    ap.add_argument("--out", default="data/olfaction_weight_sweep.json")
    args = ap.parse_args()
    neurons = list(range(16))

    off, nut = ladder()
    F, Y, it, enc, names = load_task(args.theta, neurons)
    base = {k: load_biases(args.pattern.format(k=k)) for k in neurons}
    print(f"ladder n5_25mhz: nUT {nut*1000:.1f} mV, octave {nut*math.log(2)*1000:.1f} mV, "
          f"offsets {[round(o*1000,1) for o in off]} mV")
    folds = list(GroupKFold(n_splits=5).split(F, Y, it))
    print(f"{len(F)} chunks / {len(np.unique(it))} trials, {len(names)} classes {names}")
    print(f"digital baseline on these folds: 0.880 per-chunk, 0.967 voted5")
    print(f"measured at w=15 (reference point): 0.647 / 0.833, 108 Hz\n")
    print(f"{'w':>3} {'mean Hz':>8} {'ev/chk':>7} {'live':>5} "
          f"{'per-chunk':>10} {'voted5':>8} {'E_array':>9}")

    res = {}
    with BridgeSession() as b:
        for w in [int(x) for x in args.words.split(",")]:
            sp = [[None] * len(F) for _ in neurons]
            for i, k in enumerate(neurons):
                bi = dict(base[k])
                e0 = bi["JExcWn0"]; i0 = bi.get("JInhWp0", bi["JExcWn0"])
                for j, v in enumerate(apply_ladder(e0, off, exc=True)):
                    bi[f"JExcWn{j}"] = v
                for j, v in enumerate(apply_ladder(i0, [jj * nut * math.log(2)
                                                        for jj in range(4)], exc=False)):
                    if f"JInhWp{j}" in bi:
                        bi[f"JInhWp{j}"] = v
                b.send(f"MASK {1 << k}")
                b.apply_biases(bi); b.monitor(k); time.sleep(0.7)
                b.program_weight(0, w, exc=True); b.program_weight(0, w, exc=False)
                for j in range(len(F)):
                    sp[i][j] = present_delta(b, k, enc[k][j], args.tpresent, 0, 0)
            cnt = np.array([[len(sp[i][j]) for i in range(len(neurons))]
                            for j in range(len(F))]) / args.tpresent
            per = cnt.mean(0); ev = cnt.sum(1).mean() * args.tpresent
            spa = np.empty((len(neurons), len(F)), dtype=object)
            for i in range(len(neurons)):
                for j in range(len(F)):
                    spa[i, j] = np.asarray(sp[i][j])
            K = np.nan_to_num(kernel(spa, args.tpresent))
            pred = np.zeros(len(Y), dtype=int)
            for tr, te in folds:
                mdl = make_pipeline(StandardScaler(),
                                    LogisticRegression(C=0.1, max_iter=5000,
                                                       class_weight="balanced"))
                mdl.fit(K[tr], Y[tr]); pred[te] = mdl.predict(K[te])
            pc = float((pred == Y).mean()); v5 = vote_acc(pred, Y, it, 5)
            E = P_ANALOG_W * args.tpresent + (DRAIN_FIXED + DRAIN_MARGINAL * ev) * E_CYCLE_J
            res[str(w)] = dict(charge_units=w, mean_hz=float(per.mean()), events=float(ev),
                               live=int((per > 0).sum()), per_chunk=pc, voted5=v5,
                               E_J=float(E), per_neuron_hz=per.tolist())
            print(f"{w:3d} {per.mean():8.1f} {ev:7.0f} {int((per>0).sum()):5d} "
                  f"{pc:10.3f} {v5:8.3f} {E*1e6:8.1f}u")
            json.dump(res, open(args.out, "w"), indent=2)
            np.savez(f"olfaction_spikes_w{w}.npz", spikes=spa, labels=Y, trial=it,
                     neurons=np.array(neurons), nproj=1, classes=np.array(names),
                     T=args.tpresent, duration="0.1s", theta=args.theta, weight=w)
    print(f"\nintegrity: drops={INTEGRITY['drops']} stalls={INTEGRITY['stalls']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
