#!/usr/bin/env python3
"""GATE: did the fast readout recover the virtual reservoir's clean diagonal?

Background. The recurrent / virtual-256 reservoir collapsed (feedforward 0.987 ->
0.58 simultaneous / 0.77 virtual) not because dimensionality failed to help, but
because the old readout held a neuron's `req` ~250 ms per spike: with 15 neurons
contending for the shared AER bus, the target neuron's spikes were dropped. Even the
CLEAN DIAGONAL -- each neuron read out under the bias tuned for it, which should
equal the feedforward case -- degraded to 0.833.

The SRAM drain services a handshake in ~50 us, so that drop mechanism is gone, and
the collection now asserts the chip's own integrity flags (drops/stalls == 0).

This script recomputes the diagonal with the SAME pipeline as reservoir_a2.py --
exponential kernel features (K=8, tau in {0.04,0.08,0.16,0.32}), StandardScaler +
LogisticRegression(C=0.1, balanced), leave-one-record-out CV -- so the number is
comparable to the historical 0.833 / 0.987.

  recovers toward ~0.987 -> contention was the blocker; proceed to powered N/S/V.
  stays around  ~0.83    -> contention was NOT the (only) blocker; STOP.

NOTE this is N vs V, the BINARY task, which is saturated (a single neuron can solve
it). A high diagonal proves the READOUT is fixed. It leaves open whether mismatch
dimensionality converts to accuracy -- that needs the hard 3-class N/S/V run.
"""
import argparse
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, f1_score

from reservoir_kernel import build_features

K = 8
TAUS = [0.04, 0.08, 0.16, 0.32]


def feats(spikes, T):
    return np.hstack([build_features(spikes, T, K, "exp", t) for t in TAUS])


def loro(F, y, g):
    """Leave-one-record-out: a beat's record never appears in its own training set."""
    accs = []
    yhat = np.empty_like(y)
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr])
        p = c.predict(F[te])
        yhat[te] = p
        accs.append(accuracy_score(y[te], p))
    return float(np.mean(accs)), float(np.std(accs)), f1_score(y, yhat, average="macro")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_recur_collapse.npz")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y, recs = d["spikes"], d["labels"], d["records"]
    neurons, T = d["neurons"], float(d["T"])
    n_in = int(d["n_input"]) if "n_input" in d.files else spikes.shape[0] // 16

    # trace index = ni*16 + j  (ni = stimulated-neuron index, j = readout neuron)
    # The DIAGONAL is j == neurons[ni]: each neuron read out at its own tuned bias.
    stim = np.array(sorted(set(int(x) for x in neurons))) if neurons.size == spikes.shape[0] else np.arange(n_in)
    stim = np.arange(n_in)
    diag_idx = [ni * 16 + ni for ni in range(n_in)]      # neurons list is 0..15 in order

    print(f"{args.npz}: {spikes.shape[0]} traces x {spikes.shape[1]} beats, "
          f"T={T}s, classes={d['classes']}, {len(set(recs))} records")
    print(f"labels: {np.bincount(y)} (class counts)\n")

    for name, idx in (("clean diagonal (16 traces)", diag_idx),
                      ("full virtual reservoir (all)", list(range(spikes.shape[0])))):
        F = feats(spikes[idx, :], T)
        a, sd, f1 = loro(F, y, recs)
        # non-empty traces: a dead neuron contributes nothing but a constant column
        alive = sum(1 for i in idx if any(len(spikes[i, b]) for b in range(spikes.shape[1])))
        print(f"{name:30s} acc={a:.3f} +/- {sd:.3f}  macroF1={f1:.3f}  "
              f"({alive}/{len(idx)} traces non-silent, {F.shape[1]} features)")

    print()
    print("reference: feedforward 0.987  |  virtual diagonal under the OLD readout 0.833")
    print("GATE: recovery toward 0.987 => contention was the blocker -> run powered N/S/V.")
    print("      still ~0.83            => contention was not the only blocker -> STOP.")
    print()
    print("Caveat: N-vs-V is saturated (one neuron can solve it). This gates the READOUT,")
    print("not the dimensionality->accuracy claim. And n=1 pass: no accuracy should be")
    print("quoted without mean +/- std over >=3 repeats.")


if __name__ == "__main__":
    main()
