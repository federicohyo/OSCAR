#!/usr/bin/env python3
"""A0 software prototype: STRUCTURED, feature-aware input encoding (NEXT_STEPS_ACCURACY
sec.4-A0), scored offline against raw+RR and the random projection.

Instead of a random per-neuron projection (diverse but task-agnostic), each neuron is a
named morphological feature detector, encoded as FEW gated delta spikes fed to a software
LIF neuron:
  - P-wave      : all delta events in the P window (P present/absent -- key for S)
  - QRS up-slope: UP events only, gated to the Q->R window (delta UP == rising slope)
  - QRS down-sl.: DOWN events only, gated to the R->S window (== falling slope / width)
  - T-wave      : all delta events in the T window
  - RR / rhythm : 3 spikes at the neighbouring R-peaks on a real time axis (prematurity)
Device mismatch is emulated as per-neuron time-constant/threshold jitter that tiles each
feature. Win condition: structured reservoir inter-patient macro-F1 > raw+RR.

Fiducial windows are in resampled-128 index space for the win=(-90,144)@360Hz segmentation
(R-peak lands at index ~49): P~[8,30], QRS-up~[40,50], QRS-down~[49,60], T~[85,120].
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import numpy as np
from reservoir_data import get_beats, delta_encode, _gaussian_smooth
from reservoir_kernel import build_features
from reservoir_sw_lif import sim_lif
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

TAUS = [0.02, 0.04, 0.08, 0.16, 0.32]
K = 8
L = 128  # resampled beat length

# fiducial windows in resampled-128 index space (R-peak ~ index 49)
WIN = {"P": (8, 30), "QRSup": (40, 50), "QRSdown": (49, 60), "T": (85, 120)}

# 16-neuron structured bank: feature groups with per-neuron mismatch tiling (sigma, theta)
def build_spec():
    spec = []
    tiles = {  # (sigma, theta) tiles per feature -> device-mismatch-like diversity.
        # P/T are small deflections -> lower theta (denser events) so they drive the chip.
        "P":       [(2.0, 0.020), (3.5, 0.028), (1.0, 0.036)],
        "QRSup":   [(0.5, 0.030), (1.0, 0.040), (1.5, 0.050)],
        "QRSdown": [(0.5, 0.030), (1.0, 0.040), (1.5, 0.050)],
        "T":       [(2.5, 0.020), (4.0, 0.028), (1.5, 0.036)],
    }
    for feat, ts in tiles.items():
        for sigma, theta in ts:
            spec.append({"feature": feat, "win": WIN[feat], "sigma": sigma,
                         "theta": theta, "w_exc": 0.45})
    for scale in [1.0, 1.5, 0.75, 2.0]:  # 4 RR/rhythm neurons, different time scales
        # high weight so each neighbouring R-peak spike -> one output spike (faithful RR timing)
        spec.append({"feature": "RR", "scale": scale, "w_exc": 1.1})
    return spec  # 3*4 + 4 = 16


def amplify(events, mult, dt=0.002):
    """Multiplicatively boost drive: replace each input event with `mult` tightly-spaced
    spikes (dt apart, in T-fraction units). Preserves relative event counts (feature
    magnitude) and timing while raising the EPSP so weak features cross threshold while the
    biases stay untouched (the de-saturated neurons have headroom)."""
    if mult <= 1:
        return list(events)
    out = []
    for tf, ch in events:
        for j in range(mult):
            out.append((min(tf + j * dt, 1.0), ch))
    return out


def encode_neuron(beat, rr, spec):
    """Return the neuron's input delta events [(t_frac in [0,1], channel 0=UP/1=DOWN)]."""
    if spec["feature"] == "RR":
        prev_rr, next_rr = float(rr[0]), float(rr[1])
        rrmax = 2.0 / spec["scale"]
        peaks = [0.0, prev_rr / rrmax, (prev_rr + next_rr) / rrmax]  # neighbouring R-peaks
        # burst of NB UP spikes at each R-peak so a few input events summate to fire the
        # (de-saturated) neuron while preserving R-peak timing / prematurity
        NB, gap = 6, 0.004
        ev = []
        for t in peaks:
            if 0.0 <= t <= 1.0:
                ev += [(min(t + j * gap, 1.0), 0) for j in range(NB)]
        return ev
    w0, w1 = spec["win"]
    sm = _gaussian_smooth(np.asarray(beat, float), spec["sigma"])
    sub = sm[w0:w1]
    sub = (sub - sub.min()) / (sub.max() - sub.min() + 1e-9)  # renormalize WITHIN window
    ev_local = delta_encode(sub, spec["theta"])               # t_frac in [0,1] of the window
    # place events at their real fractional time in the full beat
    ev = [((w0 + tf * (w1 - w0)) / L, ch) for tf, ch in ev_local]
    if spec["feature"] == "QRSup":
        ev = [(tf, 0) for tf, ch in ev if ch == 0]    # rising slope -> excitatory
    elif spec["feature"] == "QRSdown":
        ev = [(tf, 0) for tf, ch in ev if ch == 1]    # falling slope -> excitatory (fire on |slope|)
    return ev


def run(spec, X, rr, T, mismatch, seed, w_exc=0.45, w_inh=0.45, tau_m=0.03):
    n, nb = len(spec), len(X)
    rng = np.random.default_rng(seed)
    taus = np.clip(tau_m * (1 + mismatch * rng.standard_normal(n)), 0.005, None)
    vths = np.clip(1.0 * (1 + mismatch * rng.standard_normal(n)), 0.3, None)
    spikes = np.empty((n, nb), dtype=object)
    for k in range(n):
        we = spec[k].get("w_exc", w_exc)
        tot = 0
        for bi in range(nb):
            ev = encode_neuron(X[bi], rr[bi], spec[k])
            st = sim_lif(ev, T, taus[k], vths[k], 0.0, 0.005, we, w_inh)
            spikes[k, bi] = st; tot += len(st)
        yield k, spikes, tot


def bank(spikes, T):
    return np.hstack([build_features(spikes, T, K, "exp", t) for t in TAUS])


def loro(F, y, g):
    yhat = np.empty_like(y); accs, f1s = [], []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr]); p = c.predict(F[te]); yhat[te] = p
        accs.append(accuracy_score(y[te], p)); f1s.append(f1_score(y[te], p, average="macro"))
    return np.mean(accs), np.std(accs), np.mean(f1s), np.std(f1s), f1_score(y, yhat, average=None)


def score(name, F, y, g):
    a, asd, f, fsd, pc = loro(F, y, g)
    print(f"  {name:22s} acc={a:.3f}±{asd:.3f}  macroF1={f:.3f}±{fsd:.3f}  "
          f"F1[N/S/V]={pc[0]:.2f}/{pc[1]:.2f}/{pc[2]:.2f}")
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="200,208,209,222,223,232,233")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--out", default="reservoir_spikes_nsv_structured.npz")
    args = ap.parse_args()

    X, y, meta = get_beats(records=tuple(args.records.split(",")),
                           n_per_class=args.n_per_class, classes="NSV")
    g = np.asarray(meta["records"]); rr = meta["rr"]; T = args.T
    spec = build_spec()
    print(f"=== A0 structured encoding, {len(y)} beats, classes {np.bincount(y)}, "
          f"{len(spec)} feature-neurons ===")
    print("  groups: " + ", ".join(f"{s['feature']}" for s in spec))

    results = {}
    for mm, tag in [(0.0, "identical"), (0.15, "+mismatch")]:
        spikes = None; counts = []
        for k, spikes, tot in run(spec, X, rr, T, mm, seed=0):
            counts.append(tot)
        results[tag] = spikes.copy()
        rate = np.mean(counts) / len(y)
        print(f"  [{tag}] mean {rate:.1f} out-spk/beat/neuron  (per-neuron tot {counts})")
        if not args.out.endswith("none") and tag == "+mismatch":
            np.savez(args.out, spikes=spikes, labels=y, records=meta["records"],
                     neurons=np.arange(len(spec)), T=T, coding="structured", classes="NSV")

    print("\n--- inter-patient LORO (linear readout) ---  (S-F1 is the target)")
    score("raw", X, y, g)
    score("raw + RR", np.hstack([X, rr]), y, g)
    Fi = bank(results["identical"], T)
    Fm = bank(results["+mismatch"], T)
    # morphology-only reservoir = first 12 neurons (P/QRSup/QRSdown/T), drop lossy RR neurons
    morph = np.array([i for i, s in enumerate(spec) if s["feature"] != "RR"])
    Fmorph = bank(results["+mismatch"][morph], T)
    score("struct (identical)", Fi, y, g)
    score("struct (+mismatch)", Fm, y, g)
    score("struct+mm + RR", np.hstack([Fm, rr]), y, g)
    score("morph-only + RR", np.hstack([Fmorph, rr]), y, g)
    print("\nWIN CONDITION: struct macroF1 > raw+RR (0.503), and struct S-F1 >> raw S-F1 (0.00).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
