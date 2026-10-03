#!/usr/bin/env python3
"""Iso-accuracy comparison: analog array vs the measured digital kernel, same chunks,
same folds, same voting.

F. Corradi, 2026-08-13: "we need a way to pump up accuracy not making the array cheaper,
we want to do ISO accuracy comparisons." Right. Energy is only meaningful at matched
accuracy, so this script builds the accuracy axis first and prices it second.

TWO PROTOCOL BUGS this replaces, both of which flattered the digital side:

  1. ONE CHUNK vs FIVE. chunks() emits one chunk per 50 ms heater cycle, so a 0.1 s
     pulse plus its 0.2 s tail gives five. The digital number (0.900 per-chunk, 1.000
     voted) votes over all five; the first array run used a single pass without voting.
  2. DIFFERENT SPLITS. The digital baseline trains on 1.0 s pulses and tests on 0.1 s
     (Dennler's generalisation protocol); the array run did CV inside 0.1 s. Here BOTH
     substrates get the same folds on the same chunks. the reference-protocol version needs
     a 1.0 s array acquisition and is still in progress -- see olfaction.md.

Chunks of one trial stay together across folds (GroupKFold on trial), so voting is
evaluated only on held-out trials.

ENERGY, per trial-level decision made from k chunks. The 16 neurons are a physical
array and drain together, so the only time multiplexing is over the M projections:
each chunk costs M sequential presentations of T and M drain calls.
    array    k * (P_analog * M * T + (M*105 + 480*events) * E_cycle)
    digital  k * E_OP3                                    (85215 cycles, measured Q16)
Note this makes M=3 at T=0.05 cost the SAME rail as M=1 at T=0.15: real-time
presentation pays for the multiplexing rather than saving anything on top of it.
Running the neurons sequentially on the bench is an instrument limit (one unmasked
neuron at a time) rather than the architecture, so the parallel assumption is the right one --
it is the same assumption E_readout was defined under for ECG.
Both scale linearly in k, so the ratio at FIXED k is constant -- the comparison only
means something at MATCHED ACCURACY, i.e. at the k each substrate needs to reach a
given accuracy. Note the digital figure leaves sensor/ADC power out of scope, while the array's
P_analog effectively includes; that asymmetry favours the array and stays uncorrected.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_iso_compare.py
"""
import argparse, json
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_identity import chunks

FS = 1000.0
P_ANALOG_W, E_CYCLE_J = 0.43e-3, 372e-12
DRAIN_FIXED, DRAIN_MARGINAL = 105, 480
E_OP3_J = 85215 * E_CYCLE_J


def counts(sp, T):
    n, nb = sp.shape
    return np.array([[len(np.asarray(sp[i, j])) / T for i in range(n)] for j in range(nb)])


def kernel(sp, T, taus=(0.010, 0.050), K=4):
    """Exponential kernel over the spike times, sampled at K points in the window.
    Counts throw the timing away; the array's whole claim is that timing carries
    something, so this is the read-out that lets it show."""
    n, nb = sp.shape
    grid = np.linspace(T / K, T, K)
    out = np.zeros((nb, n * len(taus) * K))
    for j in range(nb):
        c = 0
        for i in range(n):
            st = np.asarray(sp[i, j], dtype=float)
            for tau in taus:
                for g in grid:
                    d = g - st
                    out[j, c] = np.exp(-d[d >= 0] / tau).sum() if len(st) else 0.0
                    c += 1
    return out


def vote_acc(pred, y, trial, k):
    """Majority vote over the first k chunks of each trial."""
    ok = []
    for tr in np.unique(trial):
        m = np.flatnonzero(trial == tr)[:k]
        v = np.bincount(pred[m], minlength=int(y.max()) + 1).argmax()
        ok.append(v == y[m[0]])
    return float(np.mean(ok))


def run(F, Y, trial, model, folds):
    pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        m = model()
        m.fit(F[tr], Y[tr])
        pred[te] = m.predict(F[te])
    return pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="olfaction_spikes_array_iso.npz")
    ap.add_argument("--src", default="data_olfaction/olfaction_pulses.npz")
    ap.add_argument("--out", default="data/olfaction_iso_compare.json")
    args = ap.parse_args()

    a = np.load(args.npz, allow_pickle=True)
    sp, Y, trial, T = a["spikes"], a["labels"], a["trial"], float(a["T"])
    names = [str(c) for c in a["classes"]]

    d = np.load(args.src, allow_pickle=True)
    X, Th, meta = d["X"], d["T"], d["meta"]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == str(a["duration"])
    Fd, itd = chunks(X[m], Th[m], t, float(str(a["duration"]).rstrip("s")), 0.05, tail=0.2)
    assert len(Fd) == len(Y) and (itd == trial).all(), "chunk order differs from the run"

    M = int(a["nproj"]) if "nproj" in a.files else 1
    ev = counts(sp, T).sum(1).mean() * T
    E_arr1 = P_ANALOG_W * M * T + (M * DRAIN_FIXED + DRAIN_MARGINAL * ev) * E_CYCLE_J
    folds = list(GroupKFold(n_splits=5).split(Fd, Y, trial))
    lin = lambda: make_pipeline(StandardScaler(),
                                LogisticRegression(C=0.1, max_iter=5000,
                                                   class_weight="balanced"))
    hgb = lambda: HGB(max_iter=10, max_leaf_nodes=8, random_state=0)

    reps = {
        "array counts":  (counts(sp, T), lin),
        "array kernel":  (kernel(sp, T), lin),
        "digital HGB":   (Fd, hgb),
    }
    print(f"{len(Y)} chunks / {len(np.unique(trial))} trials, {len(names)} classes, "
          f"chance {1/len(names):.3f}")
    print(f"array: {sp.shape[0]} units (M={M} proj x {sp.shape[0]//max(M,1)} neurons), "
          f"T={T*1000:.0f} ms, {ev:.0f} events/chunk")
    print(f"       rail {P_ANALOG_W*M*T*1e6:.1f} uJ + read-out "
          f"{(M*DRAIN_FIXED + DRAIN_MARGINAL*ev)*E_CYCLE_J*1e6:.1f} uJ "
          f"= {E_arr1*1e6:.1f} uJ/chunk;  digital {E_OP3_J*1e6:.1f} uJ/chunk\n")
    hdr = "  ".join(f"k={k}" for k in range(1, 6))
    print(f"{'read-out':>14} {'feat':>5} {'per-chunk':>10}   voted {hdr}")
    res = {}
    for nm, (F, mdl) in reps.items():
        p = run(np.nan_to_num(F), Y, trial, mdl, folds)
        pc = float((p == Y).mean())
        vs = [vote_acc(p, Y, trial, k) for k in range(1, 6)]
        res[nm] = {"per_chunk": pc, "voted": vs, "n_features": int(F.shape[1])}
        print(f"{nm:>14} {F.shape[1]:5d} {pc:10.3f}         "
              + "  ".join(f"{v:.3f}" for v in vs))

    print(f"\n{'':>14} energy per trial-level decision at each k (uJ)")
    print(f"{'array':>14} " + "  ".join(f"{E_arr1*k*1e6:6.1f}" for k in range(1, 6)))
    print(f"{'digital':>14} " + "  ".join(f"{E_OP3_J*k*1e6:6.1f}" for k in range(1, 6)))

    print("\nISO-ACCURACY: cheapest k reaching each target, and the energy there")
    print(f"{'target':>8} {'array k':>8} {'E_array':>9} {'dig k':>6} {'E_dig':>9} {'ratio':>7}")
    iso = {}
    best = res["array kernel"]["voted"]
    for tgt in (0.6, 0.7, 0.8, 0.9, 0.95, 1.0):
        ka = next((k for k in range(1, 6) if best[k - 1] >= tgt), None)
        kd = next((k for k in range(1, 6) if res["digital HGB"]["voted"][k - 1] >= tgt), None)
        if ka is None or kd is None:
            print(f"{tgt:8.2f} {'--' if ka is None else ka:>8} {'':>9} "
                  f"{'--' if kd is None else kd:>6}   "
                  + ("array never reaches it" if ka is None else "digital never reaches it"))
            continue
        ea, ed = E_arr1 * ka, E_OP3_J * kd
        iso[str(tgt)] = {"k_array": ka, "E_array_J": ea, "k_dig": kd,
                         "E_dig_J": ed, "ratio": ed / ea}
        print(f"{tgt:8.2f} {ka:8d} {ea*1e6:8.1f}u {kd:6d} {ed*1e6:8.1f}u {ed/ea:6.2f}x")

    json.dump({"per_readout": res, "iso": iso, "events_per_chunk": float(ev),
               "E_array_per_chunk_J": float(E_arr1), "E_op3_J": float(E_OP3_J)},
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
