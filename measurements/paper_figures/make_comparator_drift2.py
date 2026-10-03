#!/usr/bin/env python3
"""Drift and repair on two dies, one level x run heatmap per die.
Writes comparator_drift2.pdf -- ISCAS Fig. 2.

Both dies run the SAME six reference counts [4, 6, 9, 11, 18, 26] and the same
firmware procedure; the columns are consecutive selfheal_sweep runs.

  (a) die 1: five days after its calibration the ladder has drifted off the
      reference (first two columns: natural drift, incl. the near-merge of the
      two lowest levels that the validity checks refused); the next three
      columns hold the fresh reference with an injected -0.9 mV step on the
      level referenced at 9 (bold cell, repaired x3).
  (b) die 2: one continuous session from the naive start under die-1 bias files,
      through the per-die trims that re-spread the ladder onto the reference
      (shaded columns), to the injected episodes. The bottom four levels hold;
      the top two wander upward within minutes until the highest leaves the
      probe range (hatched oor cells, excluded at derive).

    python3 make_comparator_drift2.py
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "..", "results")
if not os.path.isdir(RES):
    RES = os.path.join(HERE, "..", "..", "results")
INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
REF = [4, 6, 9, 11, 18, 26]                          # rows keyed by reference count
DIE1 = ["base", "base2", "inj", "inj2", "inj3"]
DIE2 = ["base", "trim1", "trim2", "trim3", "trim4",
        "inj1", "inj2", "inj3", "injlow1", "injlow2", "injlow3", "final",
        "watch1", "watch2", "watch3", "watch4", "watch5", "watch6"]
BREAK_AT = ("final", "watch1")     # ~2 h and a power cycle between these runs


def style():
    matplotlib.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5, "axes.labelsize": 7.5,
        "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK, "legend.frameon": False,
    })


def load(names, tag):
    out = []
    for nm in names:
        suffix = f"_{nm}_aug24.json" if tag == "die1" else f"_{nm}_chip2_aug24.json"
        p = os.path.join(RES, f"selfheal{suffix}")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        out.append((nm, d["prov_unix_time"], [c.get("meas") for c in d["calls"]]))
    return out


def heatmap(ax, runs, norm, rows_labelled=True, inj_teal=None,
            inj_red=None, shade=None, break_at=None):
    """One level x run heatmap. meas==0 (oor) -> hatched cell labelled oor.
    inj_teal/inj_red: run names whose level-referenced-at-9 column carried a
    deliberate injection (red = refused, teal = repaired). shade: (first, last)
    run names to mark as the per-die trim region."""
    names = [nm for nm, _, _ in runs]
    mins = [(t - runs[0][1]) / 60.0 for _, t, _ in runs]
    M = np.array([[np.nan if m[i] == 0 else m[i]
                   for m in (meas for _, _, meas in runs)]
                  for i in range(6)], dtype=float)
    ax.imshow(M, aspect="auto", cmap="viridis", norm=norm,
              interpolation="nearest", origin="upper")
    for r in range(6):
        for c in range(len(names)):
            v = M[r, c]
            if v != v:
                ax.add_patch(plt.Rectangle((c - .5, r - .5), 1, 1, facecolor="white",
                                           hatch="///", edgecolor=MUTED, lw=0,
                                           zorder=3))
                ax.text(c, r, "oor", ha="center", va="center", fontsize=4.4,
                        color="#444", zorder=4)
            else:
                hot = (r == 2 and (names[c] in (inj_teal or ())
                                   or names[c] in (inj_red or ())))
                ax.text(c, r, f"{int(v)}", ha="center", va="center", fontsize=5.0,
                        color="white" if (v < 8 or v > 26) else INK,
                        fontweight="bold" if hot else "normal", zorder=4)
    ax.set_yticks(range(6))
    if rows_labelled:
        ax.set_yticklabels([f"$N^\\star$={r}" for r in REF], fontsize=5.8)
    else:
        ax.set_yticklabels([str(r) for r in REF], fontsize=5.8)
    ax.set_xticks(range(len(names)))
    lab = {"base": "drift-1", "base2": "drift-2", "inj": "inj-1",
           "inj2": "inj-2", "inj3": "inj-3", "injlow1": "inj-1'",
           "injlow2": "inj-2'", "injlow3": "inj-3'",
           "watch1": "w1", "watch2": "w2", "watch3": "w3",
           "watch4": "w4", "watch5": "w5", "watch6": "w6"}
    ax.set_xticklabels([lab.get(n, n) for n in names], fontsize=5.0, rotation=45,
                       ha="right")
    if break_at and break_at[0] in names and break_at[1] in names:
        bx = (names.index(break_at[0]) + names.index(break_at[1])) / 2
        ax.axvline(bx, color="white", lw=2.5, zorder=6)
        ax.axvline(bx, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=7)
        ax.text(bx + 0.55, -0.92, "after power cycle", fontsize=5.0,
                color=MUTED, clip_on=False)
    for nm, col in [((inj_red or ()), "#c0392b"), ((inj_teal or ()), "#0b7285")]:
        for n in nm:
            if n in names:
                ax.scatter(names.index(n), -0.38, marker="v", s=13, color=col,
                           clip_on=False, zorder=5)
    if shade:
        a, b = names.index(shade[0]), names.index(shade[1])
        ax.axvspan(a - .5, b + .5, color="#f2e3c9", alpha=0.45, zorder=1)
        label = shade[2] if len(shade) > 2 else "per-die bias trims"
        ax.text((a + b) / 2, -0.92, label, fontsize=5.2,
                ha="center", color="#8a6d1a", clip_on=False)
    ax.set_xticks(np.arange(-.5, len(names), 1), minor=True)
    ax.set_yticks(np.arange(-.5, 6, 1), minor=True)
    ax.grid(which="minor", color="white", lw=0.5)
    ax.tick_params(which="minor", length=0)
    ax.set_xlim(-.5, len(names) - .5)
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)
    return M


def main():
    style()
    norm = Normalize(vmin=0, vmax=33)
    r1 = load(DIE1, "die1")
    r2 = load(DIE2, "die2")

    # ---- panel (a): die 1, saved alone (the (a)/(b) labels live in LaTeX) ----
    # width chosen so both panels come out at the same rendered height when the
    # minipages scale them to 0.295 / 0.685 of \textwidth
    f1 = plt.figure(figsize=(2.11, 2.3))
    g1 = f1.add_gridspec(1, 1, left=0.265, right=0.99, top=0.84, bottom=0.26)
    a1 = f1.add_subplot(g1[0])
    heatmap(a1, r1, norm, rows_labelled=True,
            inj_teal=["inj", "inj2", "inj3"],
            shade=("base", "base2", "drift after calib."))
    f1.savefig(os.path.join(HERE, "comparator_drift2_a.pdf"),
               bbox_inches="tight", pad_inches=0.01)

    # ---- panel (b): die 2, with the colour bar --------------------------------
    f2 = plt.figure(figsize=(4.9, 2.3))
    g2 = f2.add_gridspec(1, 2, width_ratios=[1, 0.035],
                         left=0.075, right=0.99, top=0.84, bottom=0.26,
                         wspace=0.14)
    a2 = f2.add_subplot(g2[0])
    cax = f2.add_subplot(g2[1])
    heatmap(a2, r2, norm, rows_labelled=False,
            inj_red=["inj1", "inj2", "inj3"],
            inj_teal=["injlow1", "injlow2", "injlow3"],
            shade=("trim1", "trim4"), break_at=BREAK_AT)
    cb = f2.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="viridis"),
                     cax=cax)
    cb.set_label("measured $N^{*}$", fontsize=6.4)
    cb.ax.tick_params(labelsize=5.6, length=2)
    cb.outline.set_visible(False)
    f2.savefig(os.path.join(HERE, "comparator_drift2_b.pdf"),
               bbox_inches="tight", pad_inches=0.01)
    print(f"wrote comparator_drift2_a/b.pdf ({len(r1)} die-1 runs, "
          f"{len(r2)} die-2 runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
