#!/usr/bin/env python3
"""Which neurons actually add dimensionality (and accuracy) to the reservoir?

A reservoir only helps if its neurons span independent directions. Three failure modes,
each with a different fix:

  SILENT     - barely fires             -> raise excitability (vleakn up / ifdcp down)
  SATURATED  - fires flat-out, no modulation by the input -> lower excitability / more inh
  REDUNDANT  - fires, but its response is a near-copy of another neuron -> retune tau/thr
               so it occupies a different timescale

Metrics (all offline, on the raw-spike .npz):

  D_eff  participation ratio of the neuron x neuron correlation matrix,
         PR = (sum lambda)^2 / sum lambda^2 = n^2 / ||C||_F^2 for a correlation matrix.
         "Effective number of independent neurons". D_eff == n means perfectly
         decorrelated; D_eff == 1 means every neuron is the same neuron.

  dPR    leave-one-out change in D_eff. <= 0 means the neuron adds nothing new.
  dAcc   leave-one-out change in LOGO accuracy. The thing we actually care about.
  maxr   largest |correlation| with any OTHER neuron. High = redundant.
  cv     coefficient of variation of the neuron's binned rate. ~0 = saturated or silent.

    ./.venv-meas/bin/python3 reservoir_dimensionality.py --npz reservoir_spikes...npz
"""
import argparse
import numpy as np
from reservoir_kernel import build_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score

K, TAUS = 8, [0.04, 0.08, 0.16, 0.32]


def loro_acc(F, y, g):
    accs = []
    for tr, te in LeaveOneGroupOut().split(F, y, g):
        c = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000, class_weight="balanced", C=0.1))
        c.fit(F[tr], y[tr])
        accs.append(accuracy_score(y[te], c.predict(F[te])))
    return float(np.mean(accs))


def feats(sp, T, idx):
    """Kernel features for a subset of neuron rows."""
    return np.hstack([build_features(sp[idx, :], T, K, "exp", t) for t in TAUS])


def state_matrix(sp, T):
    """(n_beats*K, n_neurons): each neuron's binned response, stacked over beats.

    Uses a single mid-range tau so the correlation reflects response shape rather than the
    multi-tau replication (which would make every neuron look correlated with itself).
    """
    n_neu, n_beats = sp.shape
    F = build_features(sp, T, K, "exp", 0.08)          # (n_beats, n_neu*K)
    S = F.reshape(n_beats, n_neu, K).transpose(0, 2, 1).reshape(n_beats * K, n_neu)
    return S


def d_eff(S):
    """Participation ratio of the neuron-neuron correlation matrix."""
    sd = S.std(axis=0)
    live = sd > 1e-12
    if live.sum() < 2:
        return float(live.sum())
    Z = (S[:, live] - S[:, live].mean(axis=0)) / sd[live]
    C = (Z.T @ Z) / Z.shape[0]
    lam = np.linalg.eigvalsh(C)
    lam = np.clip(lam, 0, None)
    return float(lam.sum() ** 2 / np.sum(lam ** 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npz", default="reservoir_spikes_nv_delta_50mhz_jul10.npz")
    ap.add_argument("--skip-acc", action="store_true", help="skip leave-one-out accuracy (slow)")
    args = ap.parse_args()

    d = np.load(args.npz, allow_pickle=True)
    spikes, y, recs, T = d["spikes"], np.asarray(d["labels"]), d["records"], float(d["T"])
    done = [int(k) for k in d["done_neurons"]] if "done_neurons" in d.files else list(range(spikes.shape[0]))
    sp = spikes[:len(done), :]
    n = len(done)
    print(f"{args.npz}: {n} neurons {done}, {sp.shape[1]} beats, T={T}s\n")

    S = state_matrix(sp, T)
    full_pr = d_eff(S)
    full_acc = None if args.skip_acc else loro_acc(feats(sp, T, np.arange(n)), y, recs)

    # cumulative: does D_eff keep growing as neurons are added?
    print("cumulative (neurons added in order)")
    print(f"{'k':>3s} {'neuron':>7s} {'D_eff':>7s} {'D_eff/k':>8s} {'acc':>7s}")
    for k in range(1, n + 1):
        idx = np.arange(k)
        pr = d_eff(S[:, idx])
        acc = "" if args.skip_acc else f"{loro_acc(feats(sp, T, idx), y, recs):7.3f}"
        print(f"{k:3d} {done[k-1]:7d} {pr:7.2f} {pr/k:8.2f} {acc}")

    # per-neuron diagnostics
    sd = S.std(axis=0)
    mean = S.mean(axis=0)
    cv = np.where(mean > 1e-9, sd / np.maximum(mean, 1e-9), 0.0)
    Zsd = np.where(sd > 1e-12, sd, 1.0)
    Z = (S - mean) / Zsd
    C = np.abs((Z.T @ Z) / Z.shape[0])
    np.fill_diagonal(C, 0.0)
    maxr = C.max(axis=1) if n > 1 else np.zeros(n)

    print(f"\nfull reservoir: D_eff = {full_pr:.2f} / {n} neurons"
          + ("" if args.skip_acc else f"   acc = {full_acc:.3f}"))
    print("\nper-neuron (leave-one-out)")
    print(f"{'neuron':>6s} {'spikes':>7s} {'N/beat':>7s} {'V/beat':>7s} {'|N-V|':>6s} "
          f"{'cv':>5s} {'maxr':>5s} {'dPR':>6s} {'dAcc':>6s}  flag")
    Nb = np.where(y == 0)[0]
    Vb = np.where(y == 1)[0]
    rows = []
    for i in range(n):
        keep = np.array([j for j in range(n) if j != i])
        pr_wo = d_eff(S[:, keep]) if keep.size >= 2 else 0.0
        dPR = full_pr - pr_wo
        if args.skip_acc:
            dAcc = np.nan
        else:
            dAcc = full_acc - loro_acc(feats(sp, T, keep), y, recs)
        tot = sum(len(sp[i, b]) for b in range(sp.shape[1]))
        nN = np.mean([len(sp[i, b]) for b in Nb])
        nV = np.mean([len(sp[i, b]) for b in Vb])
        flag = []
        if tot == 0 or nN + nV < 2:
            flag.append("SILENT")
        if cv[i] < 0.35 and tot > 0:
            flag.append("SATURATED?")
        if maxr[i] > 0.9:
            flag.append("REDUNDANT")
        if dPR <= 0.05 and not flag:
            flag.append("no-new-dim")
        rows.append((i, dPR, dAcc))
        print(f"{done[i]:6d} {tot:7d} {nN:7.1f} {nV:7.1f} {abs(nN-nV):6.1f} "
              f"{cv[i]:5.2f} {maxr[i]:5.2f} {dPR:6.2f} "
              f"{'   nan' if args.skip_acc else f'{dAcc:6.3f}'}  {','.join(flag)}")

    print("\nretune candidates (lowest dPR first): "
          + ", ".join(f"n{done[i]}" for i, dPR, _ in sorted(rows, key=lambda r: r[1])[:5]))
    print("SILENT -> more excitable; SATURATED -> less excitable / more inhibition;")
    print("REDUNDANT -> change its timescale (vtaun/vthrdn) so it decorrelates.")


if __name__ == "__main__":
    main()
