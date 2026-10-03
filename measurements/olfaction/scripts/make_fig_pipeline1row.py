#!/usr/bin/env python3
"""One-row variant of the odor-classification pipeline figure
(reduced to its second row, per 2026-09-04 decision): one held-out chunk carried
through (a) the 8-channel MOx recording, (b) the sixteen projections with
level-crossing stimulus ticks, (c) the measured 16-neuron raster, (d) the
exponential-kernel read-out. Same data and chunk-picking rule as the repo-root
make_fig_odorclass.py; replayed from disk, hardware untouched.

Writes measurements/olfaction/figures/fig_pipeline_row.pdf. Run from the repo root:
    PYTHONPATH=measurements/olfaction/scripts ./.venv-meas/bin/python3 \
        measurements/olfaction/scripts/make_fig_pipeline1row.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupKFold

from olfaction_bias_bo import build, encoders, score
from make_fig_odorclass import (NPZ, CLASS2_PREF, DISPLAY, C_UP, C_DN,
                                pick_chunk, draw_row)

OUT = "measurements/olfaction/figures/fig_pipeline_row"


def main():
    d = np.load(NPZ, allow_pickle=True)
    sp = d["spikes"]
    Y, it = d["labels"], d["trial"]
    T, theta = float(d["T"]), float(d["theta"])
    names = [str(c) for c in d["classes"]]
    neurons = [int(k) for k in d["neurons"]]

    F, Y2, it2, _ = build("0.1s", theta, neurons)
    assert (Y2 == Y).all() and (it2 == it).all(), "npz and dataset disagree"

    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    _, pred = score(sp, Y, it, T, folds)
    nsp = np.array([[len(np.asarray(sp[i, j])) for j in range(len(Y))]
                    for i in range(len(neurons))])
    tot = nsp.sum(0)
    enc = encoders(F, theta, neurons)

    cls = next((c for c in CLASS2_PREF
                if c in names
                and sum(1 for j in range(len(Y))
                        if Y[j] == names.index(c) and pred[j] == Y[j]
                        and tot[j] > np.median(tot)) >= 3), None)
    assert cls is not None, "a class with enough healthy chunks is required"
    j = pick_chunk(cls, Y, pred, tot, it, names)
    print(f"row chunk: j={j} class={names[Y[j]]} trial={it[j]}, "
          f"spikes={tot[j]}, predicted {names[pred[j]]} (correct)")

    fig, axes = plt.subplots(1, 4, figsize=(7.16, 2.05))
    fig.subplots_adjust(left=0.062, right=0.995, bottom=0.16, top=0.90,
                        wspace=0.32)

    draw_row(axes, j, F, sp, Y, it, enc, T, theta, neurons, names)
    for a in axes:
        a.tick_params(axis="x", labelsize=6.5)
        a.set_xlabel("presentation time [ms]", fontsize=7)
        for spn in ("top", "right"):
            a.spines[spn].set_visible(False)

    for c, a in enumerate(axes):
        a.text(0.0, 1.045, f"({chr(97 + c)})", transform=a.transAxes,
               fontsize=7.5, va="bottom", ha="left", zorder=6)

    axb, yk = axes[1], len(neurons) - 0.3
    axb.plot([T * 1e3 + 2] * 2, [yk, yk + 0.35], lw=0.7, color=C_UP,
             solid_capstyle="butt", clip_on=False)
    axb.text(T * 1e3 + 3.2, yk + 0.18, "exc", fontsize=5.5, color=C_UP,
             va="center", ha="left", clip_on=False)
    axb.plot([T * 1e3 + 2] * 2, [yk - 0.55, yk - 0.2], lw=0.7, color=C_DN,
             solid_capstyle="butt", clip_on=False)
    axb.text(T * 1e3 + 3.2, yk - 0.38, "inh", fontsize=5.5, color=C_DN,
             va="center", ha="left", clip_on=False)

    fig.savefig(f"{OUT}.pdf")
    print(f"wrote {OUT}.pdf")


if __name__ == "__main__":
    main()
