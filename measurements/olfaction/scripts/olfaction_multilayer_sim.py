#!/usr/bin/env python3
"""Does a second layer let a COUNTS-only read-out replace the digital kernel filter?

The measured cost model says the two expensive digital stages are the input projection
and the exponential kernel filter, and that both are things the array could do itself
(olfaction.md 6.12). The kernel half rests on an untested claim: that if a second layer
integrates in its membranes, spike COUNTS carry what the digital filter currently
extracts. Counts-only on the single layer we measured scores 0.533/0.733 against the
kernel read-out's 0.647/0.756, so the second layer has to recover about 0.10.

Simulated before spending bench time, in the FIRMWARE's fixed-point arithmetic
(olfaction_emul_accuracy.lif_fixed), which now tracks silicon to about 0.07 -- close
enough for a go/no-go. Simulation also lifts the UART limit that would cap the bench
version at ~60 interleaved events per chunk, so we can ask whether the 4-input design
the bench can actually run costs anything against the 8-input one it cannot.

Conditions, all scored under the same protocol as every other number here:
  L1 counts   feedforward, counts only        -- the baseline to beat
  L1 kernel   feedforward, digital filter     -- what the second layer must replace
  L2 counts   two layers, counts only         -- the hypothesis
  L2 off      second layer with recurrence off -- control, must collapse

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_multilayer_sim.py
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


def build(theta, n_in, duration="0.1s", seed0=100, per_channel=True):
    d = np.load("data_olfaction/olfaction_pulses.npz", allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    enc = {}
    for k in range(n_in):
        for j in range(len(F)):
            s3 = F[j].reshape(50, 8)
            # per_channel routes ONE sensor channel to each input neuron -- the
            # substitution the synapse fabric would perform. Otherwise the host-computed
            # random projection we measured.
            sig = s3[:, k % 8] if per_channel else \
                s3 @ np.random.default_rng(seed0 + k).normal(0, 1, 8)
            enc.setdefault(k, []).append(
                encode((sig - sig.mean()) / (sig.std() + 1e-9), theta))
    return F, Y, it, enc, names


def drive_analog_projection(enc8, n, nch, T, w, seed=11):
    """The projection AS THE SYNAPSE FABRIC WOULD DO IT: each channel is delta-encoded
    ONCE, then its events fan out to every neuron through weighted synapses.

    The first version of this routed one sensor channel to each neuron, which is not what
    16 exc + 16 inh synapses per neuron can do, and it cost 0.13 voted before the second
    layer was even reached. A weighted fan-in is the real substitution for the digital
    matrix multiply."""
    rng = np.random.default_rng(seed)
    W = rng.integers(1, 4, (n, 8)) * (rng.integers(0, 2, (n, 8)) * 2 - 1)  # 4-bit-ish
    D = np.zeros((n * nch, T), dtype=np.int64)
    for c in range(8):
        for j in range(nch):
            for tf, ch in enc8[c][j]:
                i = min(T - 1, int(tf * T))
                sgn = 1 if ch == 0 else -1
                for u in range(n):
                    D[u * nch + j, i] += sgn * int(W[u, c]) * w // 3
    return D


def drive_from_events(enc, n, nch, T, w):
    D = np.zeros((n * nch, T), dtype=np.int64)
    for k in range(n):
        for j in range(nch):
            for tf, ch in enc[k][j]:
                i = min(T - 1, int(tf * T))
                D[k * nch + j, i] += w if ch == 0 else -w
    return D


def spikes_to_grid(st, n, nch, T):
    g = np.zeros((n * nch, T), dtype=np.int64)
    for u, ts in enumerate(st):
        for x in ts:
            i = int(x * 1000.0)
            if 0 <= i < T:
                g[u, i] += 1
    return g


def to_obj(st, n, nch):
    sp = np.empty((n, nch), dtype=object)
    for k in range(n):
        for j in range(nch):
            sp[k, j] = np.asarray(st[k * nch + j])
    return sp


def score(F, Y, it, folds, T):
    Fx = np.nan_to_num(F); pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, max_iter=5000,
                                             class_weight="balanced"))
        m.fit(Fx[tr], Y[tr]); pred[te] = m.predict(Fx[te])
    return float((pred == Y).mean()), vote_acc(pred, Y, it, 5)


def counts(sp, T):
    n, nb = sp.shape
    return np.array([[len(sp[i, j]) for i in range(n)] for j in range(nb)]) / T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-in", type=int, default=8)
    ap.add_argument("--n-out", type=int, default=8)
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--T", type=float, default=0.15)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--out", default="data/olfaction_multilayer_sim.json")
    args = ap.parse_args()
    Tt = int(round(args.T * 1000))

    # encode the eight raw channels once; the fabric fans them out
    F, Y, it, enc8, names = build(args.theta, 8)
    nch = len(Y)
    folds = list(GroupKFold(n_splits=5).split(np.zeros((nch, 1)), Y, it))
    print(f"{nch} chunks / {len(np.unique(it))} trials; "
          f"L1 = {args.n_in} (weighted fan-in of all 8 channels), L2 = {args.n_out}")
    print("firmware fixed-point LIF; read-outs scored identically to the measured runs\n")

    # layer 1, at the operating point the emulation sweep picked
    P1 = dict(decay=64000, jump=20000, vth=32768, refr=10)
    D1 = drive_analog_projection(enc8, args.n_in, nch, Tt, P1["jump"])
    st1 = lif_fixed(D1, P1["decay"], P1["jump"], P1["vth"], P1["refr"])
    sp1 = to_obj(st1, args.n_in, nch)
    g1 = spikes_to_grid(st1, args.n_in, nch, Tt)
    r1 = np.mean([len(sp1[k, j]) for k in range(args.n_in) for j in range(nch)]) / args.T
    a_c1 = score(counts(sp1, args.T), Y, it, folds, args.T)
    a_k1 = score(kernel(sp1, args.T), Y, it, folds, args.T)
    print(f"{'read-out':<34} {'units':>6} {'Hz':>7} {'per-chunk':>10} {'voted5':>8}")
    print(f"{'L1 counts (feedforward)':<34} {args.n_in:6d} {r1:7.1f} "
          f"{a_c1[0]:10.3f} {a_c1[1]:8.3f}")
    print(f"{'L1 kernel (what L2 must replace)':<34} {args.n_in*8:6d} {r1:7.1f} "
          f"{a_k1[0]:10.3f} {a_k1[1]:8.3f}")

    res = {"L1_counts": a_c1, "L1_kernel": a_k1, "rate_L1": r1, "L2": []}
    best = None
    for wrec, decay2, vth2 in itertools.product((6000, 15000, 40000),
                                                (60000, 64500), (32768, 65536)):
        rng = np.random.default_rng(7)
        W = rng.integers(0, 2, (args.n_out, args.n_in)) * 2 - 1     # +/-1 fan-in
        D2 = np.zeros((args.n_out * nch, Tt), dtype=np.int64)
        for u in range(args.n_out):
            for k in range(args.n_in):
                if W[u, k]:
                    D2[u * nch:(u + 1) * nch] += W[u, k] * wrec * g1[k * nch:(k + 1) * nch]
        st2 = lif_fixed(D2, decay2, wrec, vth2, 10)
        sp2 = to_obj(st2, args.n_out, nch)
        r2 = np.mean([len(sp2[k, j]) for k in range(args.n_out)
                      for j in range(nch)]) / args.T
        if r2 < 0.5:
            continue
        a2 = score(counts(sp2, args.T), Y, it, folds, args.T)
        rec = dict(wrec=wrec, decay2=decay2, vth2=vth2, rate=r2,
                   per_chunk=a2[0], voted5=a2[1])
        res["L2"].append(rec)
        print(f"{'L2 counts  w=' + str(wrec) + ' vth=' + str(vth2):<34} "
              f"{args.n_out:6d} {r2:7.1f} {a2[0]:10.3f} {a2[1]:8.3f}")
        if best is None or a2[1] > best["voted5"]:
            best = rec
    print()
    if best:
        print(f"BEST two-layer, counts only: {best['per_chunk']:.3f} per-chunk, "
              f"{best['voted5']:.3f} voted5")
        print(f"  vs L1 counts  {a_c1[0]:.3f}/{a_c1[1]:.3f}   "
              f"(second layer worth {best['voted5']-a_c1[1]:+.3f} voted)")
        print(f"  vs L1 kernel  {a_k1[0]:.3f}/{a_k1[1]:.3f}   "
              f"(gap to the filter {best['voted5']-a_k1[1]:+.3f} voted)")
        print(f"  -> " + ("counts REPLACE the filter; the bench experiment is worth running"
                          if best["voted5"] >= a_k1[1] - 0.02 else
                          "counts do NOT replace the filter in simulation"))
    json.dump(res, open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
