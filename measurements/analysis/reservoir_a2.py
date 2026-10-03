#!/usr/bin/env python3
"""A2 software prototype: SEQUENTIAL multi-beat presentation (NEXT_STEPS_ACCURACY sec.4-A2).

A short sequence of consecutive beats is placed on a REAL time axis (actual RR gaps
preserved), delta-encoded, and driven into a bank of software LIF neurons whose membrane
time constants are tiled from short (cross-beat memory off) to long (fading memory across
beats). A premature beat (supraventricular, S) arrives while the preceding beat's long-tau
membrane is still elevated, so the reservoir STATE at the target encodes rhythm context --
information a single-beat pipeline leaves out.

Decisive control: memory bank (tau up to ~0.5 s) vs. memory-free bank (all tau = 30 ms).
If long-tau lifts S-F1 above short-tau, the reservoir is using cross-beat timing.
Baselines: single target beat alone, and raw+RR. Metric: inter-patient LORO macro/per-class F1.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_data import get_beat_sequences, delta_encode
from reservoir_kernel import build_features
from reservoir_sw_lif import sim_lif
from reservoir_structured import build_spec, encode_neuron as encode_morph
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

K = 8
WIN_SEC = (-90 / 360.0, 144 / 360.0)   # beat morphology spans -0.25..+0.40 s around its R-peak


def composite(seq, T, t_target, dt):
    """Lay each beat's morphology on a real-time grid at its true R-peak time -> one
    multi-beat signal carrying morphology AND inter-beat gaps. Overlaps sum (crowding)."""
    n = int(round(T / dt))
    grid = np.zeros(n)
    span = WIN_SEC[1] - WIN_SEC[0]
    for t_off, m in seq:
        wlen = len(m)
        t0 = t_target + t_off + WIN_SEC[0]
        idx = np.round((t0 + np.arange(wlen) / wlen * span) / dt).astype(int)
        ok = (idx >= 0) & (idx < n)
        np.add.at(grid, idx[ok], np.asarray(m)[ok])
    lo, hi = grid.min(), grid.max()
    return (grid - lo) / (hi - lo + 1e-9)


def encode_seq(seq, T, t_target, dt, theta):
    """Rhythm encoding: one UP spike per beat R-peak on the real time axis. A long-tau
    LIF then fires only when consecutive R-peaks fall within its memory window (a premature
    beat arriving before the prior EPSP decays) -- so output encodes prematurity; a short-
    tau LIF cannot summate across the RR gap. theta unused (kept for signature)."""
    return [((t_target + t_off) / T, 0) for t_off, _ in seq if 0 <= (t_target + t_off) / T <= 1]


def run_bank(seqs, taus, thetas, T, t_target, dt, w_exc=0.34, w_inh=0.34):
    """Bank of LIF neurons (one per (tau,theta)) all driven by the same composite delta
    stream; returns spikes (n_neurons, n_beats) of output spike times."""
    n, nb = len(taus), len(seqs)
    spikes = np.empty((n, nb), dtype=object)
    # encode once per neuron-theta (theta may vary), reuse across beats
    for k in range(n):
        tot = 0
        for bi in range(nb):
            ev = encode_seq(seqs[bi], T, t_target, dt, thetas[k])
            st = sim_lif(ev, T, taus[k], 1.0, 0.0, 0.005, w_exc, w_inh)
            spikes[k, bi] = st; tot += len(st)
        yield k, spikes, tot


def bank_feats(spikes, T):
    return np.hstack([build_features(spikes, T, K, "exp", t) for t in [0.04, 0.08, 0.16, 0.32]])


def loro(F, y, g):
    yhat = np.empty_like(y); a, f = [], []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); p = c.predict(F[te]); yhat[te] = p
        a.append(accuracy_score(y[te], p)); f.append(f1_score(y[te], p, average="macro"))
    return np.mean(a), np.std(a), np.mean(f), np.std(f), f1_score(y, yhat, average=None)


def score(name, F, y, g):
    a, asd, f, fsd, pc = loro(F, y, g)
    print(f"  {name:26s} acc={a:.3f}±{asd:.3f}  macroF1={f:.3f}±{fsd:.3f}  "
          f"F1[N/S/V]={pc[0]:.2f}/{pc[1]:.2f}/{pc[2]:.2f}")
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--n-before", type=int, default=2)
    ap.add_argument("--n-after", type=int, default=1)
    ap.add_argument("--T", type=float, default=3.0)
    ap.add_argument("--t-target", type=float, default=2.0)
    ap.add_argument("--dt", type=float, default=0.002)
    ap.add_argument("--w-exc", type=float, default=0.06, help="low -> graded (integrating) regime")
    args = ap.parse_args()

    seqs, y, meta = get_beat_sequences(records=tuple(args.records.split(",")),
                                       classes="NSV", n_per_class=args.n_per_class,
                                       n_before=args.n_before, n_after=args.n_after)
    g = np.asarray(meta["records"]); rr = meta["rr"]
    print(f"=== A2 sequential multi-beat: {len(y)} targets, classes {np.bincount(y)}, "
          f"seq={args.n_before}+1+{args.n_after} beats on real time axis (T={args.T}s) ===")

    # neuron banks: 16 neurons.  MEMORY = tau tiled 0.03..0.5s;  NO-MEMORY = all 0.03s
    thetas = np.tile([0.06, 0.08, 0.10, 0.12], 4)
    tau_mem = np.repeat(np.geomspace(0.03, 0.5, 4), 4)
    tau_nomem = np.full(16, 0.03)

    banks = {}
    for tag, taus in [("memory", tau_mem), ("no-memory", tau_nomem)]:
        for k, sp, tot in run_bank(seqs, taus, thetas, args.T, args.t_target, args.dt,
                                   w_exc=args.w_exc, w_inh=args.w_exc):
            pass
        banks[tag] = sp.copy()
        print(f"  [{tag}] mean {np.mean([len(sp[i, b]) for i in range(16) for b in range(len(y))]):.1f} out-spk/beat/neuron")

    print("\n--- inter-patient LORO (linear readout) ---  (target: S-F1)")
    score("raw + RR", np.hstack([np.array([np.asarray(t) for t in meta['target']]), rr]), y, g)
    Fm = bank_feats(banks["memory"], args.T)
    Fn = bank_feats(banks["no-memory"], args.T)
    score("A2 no-memory (tau=30ms)", Fn, y, g)
    score("A2 memory (tau<=0.5s)", Fm, y, g)
    score("A2 memory + RR", np.hstack([Fm, rr]), y, g)

    # --- combined A0 morphology (on target beat) + A2 rhythm-memory (on sequence) ---
    morph_spec = [s for s in build_spec() if s["feature"] != "RR"]   # 12 morphology detectors
    targets = meta["target"]
    msp = np.empty((len(morph_spec), len(y)), dtype=object)
    for k, spec in enumerate(morph_spec):
        we = spec.get("w_exc", 0.45)
        for bi in range(len(y)):
            ev = encode_morph(np.asarray(targets[bi], float), rr[bi], spec)
            msp[k, bi] = sim_lif(ev, args.T, 0.03, 1.0, 0.0, 0.005, we, we)
    Fmorph = np.hstack([build_features(msp, args.T, K, "exp", t) for t in [0.02, 0.04, 0.08]])
    print("  " + "-" * 40)
    score("A0-morph (target only)", Fmorph, y, g)
    score("A0-morph + A2-memory", np.hstack([Fmorph, Fm]), y, g)
    score("A0-morph + A2-memory + RR", np.hstack([Fmorph, Fm, rr]), y, g)
    print("\nKEY: does A2-memory S-F1 > A2-no-memory S-F1 (cross-beat rhythm used), "
          "and does A0+A2 beat raw+RR?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
