#!/usr/bin/env python3
"""Can depth or width let a COUNTS-only read-out replace the digital kernel filter?

A first pass at 8+8 said no, but that search was far too small to conclude anything: one
weight seed, twelve operating points, no lateral recurrence. This sweeps depth (1-3
layers), width (8-64 neurons) and lateral recurrence in the last layer. The chip has 16
neurons; the larger cases are a question about what a next tape-out would need, not about
what this die can run.

The pure-Python fixed-point LIF cannot sweep this, so the loop is vectorised here and
GATED on bit-exactness against olfaction_emul_accuracy.lif_fixed, which is itself the
mirror of the firmware's lif_steps_ram(). The gate runs first and the sweep refuses to
proceed if it fails -- a fast LIF that is not the firmware's LIF would answer a different
question than the one asked.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_deep_sim.py
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
from olfaction_emul_accuracy import lif_fixed

FS = 1000.0
M32 = 0xFFFFFFFF


def lif_vec(drive, decay, vth, refr_ticks):
    """Vectorised mirror of lif_fixed(): identical Q16 shift-add decay, int32 wrapping,
    hard reset, refractory counter. The shift-add loop computes (|v| * decay) mod 2^32,
    which is an exact int64 product masked to 32 bits."""
    n, T = drive.shape
    v = np.zeros(n, dtype=np.int64)
    refr = np.zeros(n, dtype=np.int64)
    out = np.zeros((n, T), dtype=np.int8)
    for t in range(T):
        neg = v < 0
        a = np.where(neg, -v, v).astype(np.int64) & M32
        r = (a * np.int64(decay)) & M32
        vv = (r >> 16).astype(np.int64)
        vv = np.where(neg, -vv, vv)
        vv = vv + drive[:, t]
        vv = np.where(vv < 0, 0, vv)
        inref = refr > 0
        fire = (~inref) & (vv >= vth)
        refr = np.where(inref, refr - 1, np.where(fire, refr_ticks, refr))
        vv = np.where(inref | fire, 0, vv)
        out[:, t] = fire
        v = vv
    return out


def gate():
    """Refuse to run the sweep unless the fast LIF reproduces the firmware mirror exactly."""
    rng = np.random.default_rng(0)
    D = rng.integers(-30000, 30000, (6, 150)).astype(np.int64)
    for decay, vth, refr in ((60000, 65536, 125), (64000, 32768, 10), (52000, 65536, 2)):
        ref = lif_fixed(D, decay, 0, vth, refr)
        fast = lif_vec(D, decay, vth, refr)
        for u in range(D.shape[0]):
            a = np.round(np.asarray(ref[u]) * 1000).astype(int)
            b = np.flatnonzero(fast[u])
            if not (len(a) == len(b) and np.all(a == b)):
                return False, f"decay={decay} vth={vth} refr={refr} unit {u}"
    return True, "bit-exact on 18 unit-configs"


def build(theta, duration="0.1s"):
    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    return F, Y, it, names


def input_drive(F, n, T, theta, w, seed, digital_proj=True):
    nch = len(F)
    D = np.zeros((n * nch, T), dtype=np.int64)
    rng = np.random.default_rng(seed)
    Wp = rng.normal(0, 1, (n, 8))
    for k in range(n):
        for j in range(nch):
            s3 = F[j].reshape(50, 8)
            sig = s3 @ Wp[k]
            for tf, ch in encode((sig - sig.mean()) / (sig.std() + 1e-9), theta):
                i = min(T - 1, int(tf * T))
                D[k * nch + j, i] += w if ch == 0 else -w
    return D


def score(Fx, Y, it, folds):
    Fx = np.nan_to_num(Fx); pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, max_iter=5000,
                                             class_weight="balanced"))
        m.fit(Fx[tr], Y[tr]); pred[te] = m.predict(Fx[te])
    return float((pred == Y).mean()), vote_acc(pred, Y, it, 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--T", type=float, default=0.15)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--out", default="data/olfaction_deep_sim.json")
    args = ap.parse_args()
    Tt = int(round(args.T * 1000))

    ok, msg = gate()
    print(f"bit-exactness gate: {'PASS' if ok else 'FAIL'} -- {msg}")
    if not ok:
        raise SystemExit("fast LIF is not the firmware's LIF; refusing to sweep")

    F, Y, it, names = build(args.theta)
    nch = len(Y)
    folds = list(GroupKFold(n_splits=5).split(np.zeros((nch, 1)), Y, it))
    P = dict(decay=64000, jump=20000, vth=32768, refr=10)
    print(f"{nch} chunks / {len(np.unique(it))} trials, chance {1/len(names):.3f}\n")

    res = []
    print(f"{'arch':<26} {'units':>6} {'Hz':>7} {'per-chunk':>16} {'voted5':>16}")

    def run(width, depth, lateral, seeds):
        pcs, v5s, rates = [], [], []
        for sd in range(seeds):
            D = input_drive(F, width, Tt, args.theta, P["jump"], 100 + 991 * sd)
            g = lif_vec(D, P["decay"], P["vth"], P["refr"])
            for L in range(depth - 1):
                rng = np.random.default_rng(500 + 7 * L + sd)
                W = (rng.integers(0, 2, (width, width)) * 2 - 1) * rng.integers(1, 4, (width, width))
                D2 = np.zeros_like(D)
                for u in range(width):
                    acc = np.zeros((nch, Tt), dtype=np.int64)
                    for k in range(width):
                        if W[u, k]:
                            acc += int(W[u, k]) * g[k * nch:(k + 1) * nch]
                    D2[u * nch:(u + 1) * nch] = acc * (P["jump"] // 3)
                g = lif_vec(D2, P["decay"], P["vth"], P["refr"])
            if lateral:                      # one recurrent pass within the last layer
                rng = np.random.default_rng(9001 + sd)
                W = (rng.integers(0, 2, (width, width)) * 2 - 1)
                np.fill_diagonal(W, 0)
                D3 = np.zeros_like(D)
                for u in range(width):
                    acc = np.zeros((nch, Tt), dtype=np.int64)
                    for k in range(width):
                        if W[u, k]:
                            acc += int(W[u, k]) * g[k * nch:(k + 1) * nch]
                    D3[u * nch:(u + 1) * nch] = (acc * (P["jump"] // 4)
                                                 + D[u * nch:(u + 1) * nch])
                g = lif_vec(D3, P["decay"], P["vth"], P["refr"])
            cnt = g.sum(1).reshape(width, nch).T / args.T
            rates.append(cnt.mean())
            a = score(cnt, Y, it, folds)
            pcs.append(a[0]); v5s.append(a[1])
        return (float(np.mean(pcs)), float(np.std(pcs)),
                float(np.mean(v5s)), float(np.std(v5s)), float(np.mean(rates)))

    # reference: the digital kernel filter on a 16-wide feedforward layer
    D = input_drive(F, 16, Tt, args.theta, P["jump"], 100)
    g = lif_vec(D, P["decay"], P["vth"], P["refr"])
    sp = np.empty((16, nch), dtype=object)
    for k in range(16):
        for j in range(nch):
            sp[k, j] = np.flatnonzero(g[k * nch + j]) / 1000.0
    ref = score(kernel(sp, args.T), Y, it, folds)
    print(f"{'REFERENCE 16w kernel':<26} {16:6d} {'--':>7} {ref[0]:16.3f} {ref[1]:16.3f}")
    res.append(dict(arch="reference_kernel_16", per_chunk=ref[0], voted5=ref[1]))

    for width, depth, lat in itertools.product((8, 16, 32, 64), (1, 2, 3), (False, True)):
        if width >= 32 and depth == 3:
            continue                              # keep the sweep inside a few minutes
        pc, pcs_, v5, v5s_, r = run(width, depth, lat, args.seeds)
        tag = f"{width}w x {depth}L" + (" +lat" if lat else "")
        print(f"{tag:<26} {width:6d} {r:7.1f} {pc:9.3f} +/-{pcs_:.3f} "
              f"{v5:9.3f} +/-{v5s_:.3f}")
        res.append(dict(arch=tag, width=width, depth=depth, lateral=lat, rate=r,
                        per_chunk=pc, per_chunk_sd=pcs_, voted5=v5, voted5_sd=v5s_))
    best = max((x for x in res if "reference" not in x["arch"]), key=lambda x: x["voted5"])
    print(f"\nBEST counts-only: {best['arch']}  {best['per_chunk']:.3f} / "
          f"{best['voted5']:.3f} voted")
    print(f"  kernel reference {ref[0]:.3f} / {ref[1]:.3f}   "
          f"gap {best['voted5']-ref[1]:+.3f} voted")
    json.dump({"reference_kernel": ref, "sweep": res}, open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
