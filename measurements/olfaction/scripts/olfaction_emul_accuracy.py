#!/usr/bin/env python3
"""Accuracy of the DIGITAL emulation of the array, in the firmware's own arithmetic.

The paper's "digital, same pipeline emulated" row quoted 0.867 +/- 0.037, taken from a
FLOAT LIF at a hand-chosen operating point (olfaction_sim_sweep.py) -- and that model
over-predicts the measured array by more than 0.10, so the number was flagged optimistic.
The firmware does not use floats: lif_steps_ram() runs a Q16 shift-add decay on int32 with
a hard reset and a refractory counter. This mirrors that loop exactly, so the emulated row
is computed in the arithmetic that would actually run.

This needs no bench time. The emulation is deterministic fixed-point: executing it on the
RISC-V is bit-identical to executing it here, so the chip could only confirm the
arithmetic, not the accuracy. What it does need is the same fairness the array got --- its
operating point swept and the best taken, scored under the same protocol (all 150 chunks,
GroupKFold by trial, kernel read-out, voted over 5) and repeated over projection seeds.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_emul_accuracy.py
"""
import argparse, itertools, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_identity import chunks
from olfaction_iso_compare import kernel, vote_acc
from olfaction_run_array import encode

FS = 1000.0
M32 = 0xFFFFFFFF


def lif_fixed(drive, decay, jump, vth, refr_ticks):
    """Bit-exact mirror of firmware lif_steps_ram(): Q16 shift-add decay, int32 wrapping,
    hard reset to 0, refractory counter. `drive` is the per-tick input in the same Q16
    units as `jump` in the firmware (there a constant; here the encoded stimulus)."""
    n, T = drive.shape
    out = [[] for _ in range(n)]
    for u in range(n):
        v = 0; refr = 0
        for t in range(T):
            neg = v < 0
            a = (-v if neg else v) & M32
            b = decay & M32
            r = 0
            while b:                                  # the software shift-add multiply
                if b & 1:
                    r = (r + a) & M32
                a = (a << 1) & M32
                b >>= 1
            vv = -((r >> 16) & M32) if neg else ((r >> 16) & M32)
            vv = int(np.int32(np.uint32(vv & M32)))
            vv += int(drive[u, t])
            if vv < 0:
                vv = 0
            if refr > 0:
                refr -= 1; vv = 0
            elif vv >= vth:
                out[u].append(t / 1000.0); vv = 0; refr = refr_ticks
            v = vv
    return out


def build(theta, nneur, seed0, duration="0.1s"):
    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    enc = {}
    for k in range(nneur):
        w = np.random.default_rng(seed0 + k).normal(0, 1, 8)
        e = []
        for j in range(len(F)):
            s = F[j].reshape(50, 8) @ w
            e.append(encode((s - s.mean()) / (s.std() + 1e-9), theta))
        enc[k] = e
    return F, Y, it, enc, names


def drive_matrix(enc, nneur, nchunk, T, w_exc, w_inh):
    """Encoder events -> per-tick Q16 current, the emulation's stimulus."""
    D = np.zeros((nneur * nchunk, T), dtype=np.int64)
    for k in range(nneur):
        for j in range(nchunk):
            for tf, ch in enc[k][j]:
                i = min(T - 1, int(tf * T))
                D[k * nchunk + j, i] += w_exc if ch == 0 else -w_inh
    return D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--neurons", type=int, default=16)
    ap.add_argument("--T", type=float, default=0.15)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--out", default="data/olfaction_emul_accuracy.json")
    args = ap.parse_args()
    T = int(round(args.T * 1000))

    seeds = [100 + 7919 * r for r in range(args.repeats)]
    data = [build(args.theta, args.neurons, s) for s in seeds]
    _, Y, it, _, names = data[0]
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    nchunk = len(Y)
    print(f"{nchunk} chunks / {len(np.unique(it))} trials, {args.neurons} units, "
          f"{args.repeats} projection seeds")
    print("firmware arithmetic: Q16 shift-add decay, int32, hard reset, refractory\n")
    print(f"{'decay':>7} {'w_exc':>7} {'vth':>8} {'refr':>5} {'Hz':>7} "
          f"{'per-chunk':>15} {'voted5':>15}")

    grid = dict(decay=[52000, 60000, 64000], w=[3000, 8000, 20000],
                vth=[32768, 65536], refr=[2, 10])
    res, best = [], None
    for decay, w, vth, refr in itertools.product(*grid.values()):
        pcs, v5s, rates = [], [], []
        for (F, Yr, itr, enc, _) in data:
            D = drive_matrix(enc, args.neurons, nchunk, T, w, w)
            st = lif_fixed(D, decay, w, vth, refr)
            sp = np.empty((args.neurons, nchunk), dtype=object)
            for k in range(args.neurons):
                for j in range(nchunk):
                    sp[k, j] = np.asarray(st[k * nchunk + j])
            rates.append(np.mean([len(sp[k, j]) for k in range(args.neurons)
                                  for j in range(nchunk)]) / args.T)
            K = np.nan_to_num(kernel(sp, args.T))
            pred = np.zeros(len(Yr), dtype=int)
            for tr, te in folds:
                mdl = make_pipeline(StandardScaler(),
                                    LogisticRegression(C=0.1, max_iter=5000,
                                                       class_weight="balanced"))
                mdl.fit(K[tr], Yr[tr]); pred[te] = mdl.predict(K[te])
            pcs.append(float((pred == Yr).mean())); v5s.append(vote_acc(pred, Yr, itr, 5))
        rec = dict(decay=decay, w=w, vth=vth, refr=refr, rate=float(np.mean(rates)),
                   per_chunk=float(np.mean(pcs)), per_chunk_sd=float(np.std(pcs)),
                   voted5=float(np.mean(v5s)), voted5_sd=float(np.std(v5s)))
        res.append(rec)
        if rec["rate"] > 1:
            print(f"{decay:7d} {w:7d} {vth:8d} {refr:5d} {rec['rate']:7.1f} "
                  f"{rec['per_chunk']:8.3f}+/-{rec['per_chunk_sd']:.3f} "
                  f"{rec['voted5']:8.3f}+/-{rec['voted5_sd']:.3f}")
        if best is None or rec["voted5"] > best["voted5"]:
            best = rec
    print(f"\nBEST emulated: voted5 {best['voted5']:.3f} +/- {best['voted5_sd']:.3f}, "
          f"per-chunk {best['per_chunk']:.3f} +/- {best['per_chunk_sd']:.3f} "
          f"at {best['rate']:.0f} Hz")
    print(f"  (float-sim figure now superseded: 0.867 +/- 0.037)")
    print(f"  measured array: 0.756 +/- 0.042 voted5;  digital tree Q16: 0.953 +/- 0.016")
    json.dump({"best": best, "grid": res, "superseded_float_sim": 0.867},
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
