#!/usr/bin/env python3
"""Score the ON-CHIP emulated-LIF spike times from olfaction_emul_run.py.

The runner verified every row bit-exactly against lif_fixed() as it went, so this can
only confirm -- the point of running at all is that the reference figure emulated point can then
be drawn as measured on silicon rather than computed. Scoring is exactly the pipeline of
olfaction_emul_accuracy.py: exponential kernel, GroupKFold by trial, StandardScaler +
logistic regression, majority vote over 5 chunks; one projection seed per input file,
mean +/- s.d. across seeds, same as the computed row's protocol.

    ./.venv-meas/bin/python3 olfaction_emul_onchip_score.py \
        data/olfaction_emul_onchip.json data/olfaction_emul_onchip_seed8019.json ...
"""
import argparse, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_iso_compare import kernel, vote_acc


def score_one(path):
    d = json.load(open(path))
    nneur, nchunk, T = d["nneur"], d["nchunk"], d["T"]
    Y, it = np.array(d["labels"]), np.array(d["trial"])
    assert len(d["times"]) == nneur * nchunk, path
    assert d["agree"], f"{path}: rows did not all match the host mirror"
    sp = np.empty((nneur, nchunk), dtype=object)
    for k in range(nneur):
        for j in range(nchunk):
            sp[k, j] = np.asarray(d["times"][k * nchunk + j], dtype=float) / 1000.0
    K = np.nan_to_num(kernel(sp, T / 1000.0))
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        mdl = make_pipeline(StandardScaler(),
                            LogisticRegression(C=0.1, max_iter=5000,
                                               class_weight="balanced"))
        mdl.fit(K[tr], Y[tr]); pred[te] = mdl.predict(K[te])
    return float((pred == Y).mean()), float(vote_acc(pred, Y, it, 5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", default=None)
    args = ap.parse_args()

    pcs, v5s = [], []
    for path in args.inputs:
        pc, v5 = score_one(path)
        pcs.append(pc); v5s.append(v5)
        print(f"  {path}: per-chunk {pc:.3f}, voted5 {v5:.3f}")
    if len(pcs) > 1:
        print(f"ON SILICON emulated LIF ({len(pcs)} seeds): "
              f"per-chunk {np.mean(pcs):.3f} +/- {np.std(pcs):.3f}, "
              f"voted5 {np.mean(v5s):.3f} +/- {np.std(v5s):.3f}")
    print("computed (olfaction_emul_accuracy.py, 3 seeds): "
          "per-chunk 0.691 +/- 0.028, voted5 0.822 +/- 0.042")
    out = dict(per_chunk=pcs, voted5=v5s,
               per_chunk_mean=float(np.mean(pcs)), voted5_mean=float(np.mean(v5s)),
               sources=args.inputs)
    dst = "data/olfaction_emul_onchip_scored.json"
    json.dump(out, open(dst, "w"), indent=2)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
