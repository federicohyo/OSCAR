#!/usr/bin/env python3
"""Three-odor classification on the analog array, from the measured silicon
spikes behind the capacity curve (data/olfaction/olf_validate/, 9 acquisitions:
centre, bo_best1, bo_best2 x 3 reps).

    ./.venv-meas/bin/python3 measurements/olfaction/scripts/make_fig_olfaction.py   (from repo root)

Pipeline is olfaction_class_curve.py verbatim, k=3 only: reference readout
(exponential kernel + LogReg), GroupKFold by trial, majority vote over a
trial's 5 chunks.  Typical statistic = mean over ALL C(5,3) subsets and all
9 acquisitions, exactly the reference value 0.877 -- asserted
against data/olfaction/olfaction_class_curve.json before drawing.

DRAWN AT PRINT SIZE (3.45 x 0.85 in, two 5-row panels), single column,
keep the same scale.
Outputs fig19_olfaction_3odor.pdf (+ .png preview) in the figures directory,
and caches the per-subset scores in data/olfaction/olfaction_k3.json.
"""
import glob, itertools, json, os, sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))  # measurements/olfaction/scripts -> repo root
sys.path.insert(0, HERE)
from olfaction_iso_compare import kernel, vote_acc  # noqa: E402

OUT = os.path.join(REPO, "measurements", "olfaction", "figures",
                   "fig19_olfaction_3odor")
CACHE = os.path.join(REPO, "data", "olfaction", "olfaction_k3.json")

INK, MUTED, GRID = "#1c1c1c", "#8a8a8a", "#e6e6e6"
C_AN = "#0b7285"                      # the analog teal
SHORT = {"2H": "2H", "Blank": "Bl", "EB": "EB", "Eu": "Eu", "IA": "IA"}


def predictions(sp, Y, it, T, C):
    """CV predictions for the chunks belonging to subset C (curve script verbatim)."""
    m = np.isin(Y, C)
    K = np.nan_to_num(kernel(sp[:, m], T))
    Ys, its = Y[m], it[m]
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Ys), 1)), Ys, its))
    pred = np.zeros(len(Ys), dtype=int)
    for tr, te in folds:
        p = make_pipeline(StandardScaler(),
            LogisticRegression(C=0.1, max_iter=5000, class_weight="balanced"))
        p.fit(K[tr], Ys[tr]); pred[te] = p.predict(K[te])
    return Ys, its, pred


def scores():
    files = sorted(glob.glob(os.path.join(REPO, "data/olfaction/olf_validate/*.npz")))
    assert files, "archived spikes required"
    out = {}
    for f in files:
        z = np.load(f, allow_pickle=True)
        sp, Y, it, T = z["spikes"], z["labels"], z["trial"], float(z["T"])
        names = [str(c) for c in z["classes"]]
        for C in itertools.combinations(range(5), 3):
            Ys, its, pred = predictions(sp, Y, it, T, C)
            key = "+".join(SHORT[names[c]] for c in C)
            pc = float((pred == Ys).mean())
            v5 = vote_acc(pred, Ys, its, 5)
            out.setdefault(f, {})[key] = dict(pc=pc, v5=v5)
        print(".", end="", flush=True)
    print()
    json.dump(out, open(CACHE, "w"), indent=1)
    return out


def main():
    matplotlib.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.0, "axes.labelsize": 7.0,
        "xtick.labelsize": 6.0, "ytick.labelsize": 5.5,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "legend.frameon": False, "lines.solid_capstyle": "round",
    })
    out = scores()

    # sanity: reproduce the reference typical statistic before drawing
    allv5 = [s["v5"] for per in out.values() for s in per.values()]
    allpc = [s["pc"] for per in out.values() for s in per.values()]
    ref = json.load(open(os.path.join(REPO, "data/olfaction/olfaction_class_curve.json")))
    assert abs(np.mean(allv5) - ref["3"]["typical"]["v5"]) < 1e-9, "v5 mismatch"
    assert abs(np.mean(allpc) - ref["3"]["typical"]["pc"]) < 1e-9, "pc mismatch"
    print(f"typical k=3: pc {np.mean(allpc):.4f}  v5 {np.mean(allv5):.4f} "
          f"({len(allv5)} subset x acquisition scores)")

    # per-subset means, sorted best last (top of the plot)
    subs = sorted({k for per in out.values() for k in per})
    mean = {s: np.mean([per[s]["v5"] for per in out.values() if s in per])
            for s in subs}
    subs.sort(key=lambda s: mean[s])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(3.45, 0.85), sharex=True)
    rng = np.random.default_rng(7)
    lo = min(min(s["v5"] for s in per.values()) for per in out.values())
    m = np.mean(allv5)
    for ax, group in ((a1, subs[:5]), (a2, subs[5:])):
        for y, s in enumerate(group):
            v = [per[s]["v5"] for per in out.values() if s in per]
            ax.plot(v, y + rng.uniform(-0.22, 0.22, len(v)), "o", ms=2.6,
                    mfc=C_AN, mec="none", alpha=0.30, zorder=3)
            ax.plot([mean[s]], [y], "|", ms=8, mew=1.3, color=C_AN, zorder=4)
        ax.axvline(1 / 3, color=MUTED, lw=0.7, ls="--", zorder=2)
        ax.axvline(m, color=C_AN, lw=0.7, ls=":", zorder=2)
        ax.set_xlim(min(0.24, lo - 0.03), 1.03)
        ax.set_ylim(-0.7, len(group) - 0.3)
        ax.set_yticks(range(len(group)))
        ax.set_yticklabels(group)
        ax.grid(True, color=GRID, lw=0.5, axis="x")
        ax.set_axisbelow(True)
        for sp_ in ("top", "right"):
            ax.spines[sp_].set_visible(False)
        for sp_ in ("left", "bottom"):
            ax.spines[sp_].set_color(MUTED)
    a2.text(1 / 3 + 0.015, 4.55, "chance 1/3", fontsize=5.5, color=MUTED,
            ha="left", va="top", rotation=90)
    a2.text(m - 0.015, 4.55, f"mean {m:.2f}", fontsize=5.5, color=C_AN,
            ha="right", va="top", rotation=90)
    a1.set_ylabel("")
    fig.supxlabel("voted accuracy, three-odor task", fontsize=7.0, y=0.02)
    fig.tight_layout(pad=0.3, w_pad=1.2)
    fig.savefig(OUT + ".pdf", bbox_inches="tight")
    fig.savefig(OUT + ".png", bbox_inches="tight", dpi=200)
    print("wrote", OUT + ".pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
