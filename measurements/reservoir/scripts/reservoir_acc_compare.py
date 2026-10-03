#!/usr/bin/env python3
"""Cross-acquisition accuracy: does the classification survive a new recording?

The reference analysis carries "every reservoir number here comes from a
single acquisition ... cross-acquisition reproducibility is a measurement we have
not made". The 2026-08-11 re-acquisition is that measurement, on the same 60
beats, the same per-neuron projection and the same read-out pipeline as the
2026-07 DIM recording -- but on the fixed read-out path (SRAM drain, on-chip
Timer0 stamps, lattice-free), a 25 MHz core, and 2.7x the drive.

Both are scored here through the IDENTICAL pipeline, inter-patient
(leave-one-record-out), so the comparison is like-for-like:

  * multi-tau exponential kernel bank (reservoir_a2.bank_feats)
  * StandardScaler + balanced LogisticRegression(C=0.1)
  * LeaveOneGroupOut over the source record

Also reported: the untrained gross-activity control from Section 4.2 -- the
array-wide event count for a beat, scored as an AUC. On recording ACC that cue
alone reaches 0.995, which is why the reference analysis keeps substrate claims off the
binary task; it is worth knowing where each of these recordings sits.

  PYTHONPATH=. ./.venv-meas/bin/python3 reservoir_acc_compare.py
"""
import json

import numpy as np
from sklearn.metrics import roc_auc_score

from reservoir_demo_proj import load
from reservoir_a2 import bank_feats, loro

RUNS = [
    ("2026-07 DIM (flash read-out, lattice)", "reservoir_spikes_nv_randproj.npz"),
    ("2026-08 re-acquisition (SRAM, no lattice)",
     "reservoir_spikes_nv_randproj_aug11.npz"),
]
T_BEAT = 2.0


def count_cue_auc(sp, y):
    tot = np.array([sum(len(np.asarray(sp[j, b])) for j in range(sp.shape[0]))
                    for b in range(sp.shape[1])], float)
    a = roc_auc_score(y, tot)
    return max(a, 1 - a)


def silent_split(sp, y):
    """Section 4.2's other control: how many neurons a beat leaves silent."""
    out = {}
    for cls in (0, 1):
        idx = [b for b in range(sp.shape[1]) if y[b] == cls]
        s = [sum(1 for j in range(sp.shape[0])
                 if len(np.asarray(sp[j, b])) == 0) for b in idx]
        out[cls] = (float(np.mean(s)), float(np.std(s)))
    return out


def main():
    res = {}
    for name, path in RUNS:
        d = np.load(path, allow_pickle=True)
        sp, y = d["spikes"], np.asarray(d["labels"])
        recs = np.asarray([str(r) for r in d["records"]])
        n, nb = sp.shape
        rate = np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T_BEAT
                        for j in range(n)])
        F = bank_feats(sp, T_BEAT)
        a, asd, f, fsd, pc = loro(F, y, recs)
        auc = count_cue_auc(sp, y)
        sil = silent_split(sp, y)
        res[name] = {"path": path, "acc": float(a), "acc_sd": float(asd),
                     "macroF1": float(f), "macroF1_sd": float(fsd),
                     "count_cue_auc": float(auc), "mean_rate_hz": float(rate),
                     "events_per_window": float(
                         sum(len(np.asarray(sp[j, b])) for j in range(n)
                             for b in range(nb)) / nb),
                     "silent_neurons_per_beat": sil}
        print(f"\n{name}")
        print(f"  {path}")
        print(f"  mean rate {rate:5.1f} Hz, {res[name]['events_per_window']:.0f} "
              f"events/window, {len(set(recs))} records")
        print(f"  inter-patient accuracy  {a:.3f} +/- {asd:.3f}   "
              f"macro-F1 {f:.3f} +/- {fsd:.3f}")
        print(f"  untrained count-cue AUC {auc:.3f}   "
              f"(1.0 = the task is solved by gross activity alone)")
        print(f"  silent neurons/beat: N {sil[0][0]:.1f}+/-{sil[0][1]:.1f}, "
              f"PVC {sil[1][0]:.1f}+/-{sil[1][1]:.1f}")

    (n0, r0), (n1, r1) = [(k, v) for k, v in res.items()]
    print("\n" + "=" * 70)
    print(f"accuracy  {r0['acc']:.3f}+/-{r0['acc_sd']:.3f}  ->  "
          f"{r1['acc']:.3f}+/-{r1['acc_sd']:.3f}   "
          f"(delta {r1['acc']-r0['acc']:+.3f})")
    print("Inter-patient s.d. is across held-out patients, so these overlap "
          "heavily;\nwith 5 records this comparison is descriptive, not a test.")
    json.dump(res, open("data/reservoir_acc_compare.json", "w"), indent=2)
    print("\nwrote data/reservoir_acc_compare.json")


if __name__ == "__main__":
    raise SystemExit(main())
