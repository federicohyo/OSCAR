#!/usr/bin/env python3
"""The emulated-array capacity curve, twin of olfaction_class_curve.py: the 16 LIF
neurons simulated in the FIRMWARE's exact fixed-point arithmetic (lif_fixed =
lif_steps_ram), best operating point of olfaction_emul_accuracy.json
(decay 64000, w 20000, vth 32768, refr 10, 3 projection seeds). Same chunks,
same kernel+LogReg readout, same GroupKFold/voted5 protocol, same subset
statistics (typical + nested data-pick). The k=5 pooled number must reproduce
the reference campaign's emulated row (0.822 +/- 0.042) -- that is the replica check.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_class_curve_emul.py
"""
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_emul_accuracy import build, drive_matrix, lif_fixed
from olfaction_iso_compare import kernel, vote_acc
import itertools

BEST = dict(decay=64000, w=20000, vth=32768, refr=10)
SEEDS = [100 + 7919 * r for r in range(3)]
THETA, T_PRESENT = 0.25, 0.15

def emulated_spikes(seed):
    """One projection seed -> spike object array (16 x 150 chunks), best op. point."""
    F, Y, it, enc, names = build(THETA, 16, seed)
    nchunk = len(Y)
    T = int(round(T_PRESENT * 1000))
    D = drive_matrix(enc, 16, nchunk, T, BEST["w"], BEST["w"])
    st = lif_fixed(D, BEST["decay"], BEST["w"], BEST["vth"], BEST["refr"])
    sp = np.empty((16, nchunk), dtype=object)
    for k in range(16):
        for j in range(nchunk):
            sp[k, j] = np.asarray(st[k * nchunk + j])
    return sp, Y, it, names

def main():
    sp_seeds, names = [], None
    for s in SEEDS:
        sp, Y, it, nm = emulated_spikes(s)
        sp_seeds.append((sp, Y, it)); names = nm
        print(".", end="", flush=True)
    print(" emulation done (3 seeds)")

    res = {}
    for k in (2, 3, 4, 5):
        typ_pc, typ_v5, pick_pc, pick_v5 = [], [], [], []
        subset_scores = {}
        per_seed = []
        for sp, Y, it in sp_seeds:
            subs = {}
            for C in itertools.combinations(range(5), k):
                m = np.isin(Y, C)
                K = np.nan_to_num(kernel(sp[:, m], T_PRESENT))
                Ys, its = Y[m], it[m]
                folds = list(GroupKFold(n_splits=5).split(
                    np.zeros((len(Ys), 1)), Ys, its))
                pred = np.zeros(len(Ys), dtype=int)
                for tr, te in folds:
                    p = make_pipeline(StandardScaler(),
                        LogisticRegression(C=0.1, max_iter=5000,
                                           class_weight="balanced"))
                    p.fit(K[tr], Ys[tr]); pred[te] = p.predict(K[te])
                subs[tuple(names[c] for c in C)] = (Ys, its, pred, folds)
            per_seed.append(subs)
            for sub, (Ys, its, pred, folds) in subs.items():
                pc = float((pred == Ys).mean()); v5 = vote_acc(pred, Ys, its, 5)
                typ_pc.append(pc); typ_v5.append(v5)
                subset_scores.setdefault(sub, []).append((pc, v5))
            npc, nv5 = [], []
            for fi in range(5):
                best_sub, best_score = None, -1
                for sub, (Ys, its, pred, folds) in subs.items():
                    tr = np.concatenate([te for g, (_, te) in enumerate(folds) if g != fi])
                    s = vote_acc(pred[tr], Ys[tr], its[tr], 5)
                    if s > best_score:
                        best_sub, best_score = sub, s
                Ys, its, pred, folds = subs[best_sub]
                te = folds[fi][1]
                npc.append(float((pred[te] == Ys[te]).mean()))
                nv5.append(vote_acc(pred[te], Ys[te], its[te], 5))
            pick_pc.append(float(np.mean(npc))); pick_v5.append(float(np.mean(nv5)))
        best = max(subset_scores.items(), key=lambda kv: np.mean([r[1] for r in kv[1]]))
        res[k] = dict(
            typical=dict(pc=float(np.mean(typ_pc)), pc_sd=float(np.std(typ_pc)),
                         v5=float(np.mean(typ_v5)), v5_sd=float(np.std(typ_v5))),
            data_pick=dict(pc=float(np.mean(pick_pc)), pc_sd=float(np.std(pick_pc)),
                           v5=float(np.mean(pick_v5)), v5_sd=float(np.std(pick_v5))),
            best_subset=list(best[0]),
            best_subset_v5=float(np.mean([r[1] for r in best[1]])))
        print(f"k={k}: typical {res[k]['typical']['v5']:.3f} +/- {res[k]['typical']['v5_sd']:.3f}"
              f"   data-pick {res[k]['data_pick']['v5']:.3f} +/- {res[k]['data_pick']['v5_sd']:.3f}"
              f"   (best {','.join(best[0])}: {res[k]['best_subset_v5']:.3f})")
    replica = res[5]["typical"]["v5"]
    print(f"\nreplica check: emulated 5-class voted5 = {replica:.3f} "
          f"(reference row 0.822 +/- 0.042) -> {'OK' if abs(replica - 0.822) < 0.085 else 'MISMATCH'}")
    json.dump(res, open("data/olfaction/olfaction_class_curve_emul.json", "w"), indent=1)
    print("wrote data/olfaction/olfaction_class_curve_emul.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
