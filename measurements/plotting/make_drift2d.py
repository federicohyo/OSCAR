#!/usr/bin/env python3
"""Drift and repair on two dies as ONE compact 2D heatmap (replaces the
full-width two-panel comparator_drift2_a/b.pdf and the 3D attempt).

Both dies' runs are concatenated along x: die 1 (5 runs: five-day drift,
then three injected-and-repaired episodes) then die 2 (18 runs: naive start
on die-1 bias files, per-die trims, refused + repaired injections, power
cycle, idle watching). Rows are the six ladder levels keyed by their
reference count; cells show the measured switching count; oor = out of
range (hatched). The whole bench session spans ~2.3 h --- the five-day
drift is BEFORE the first column.

    python3 make_drift2d.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42,
                            "font.family": "sans-serif",
                            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                            "font.size": 7.0, "axes.labelsize": 7.0,
                            "xtick.labelsize": 6.0, "ytick.labelsize": 6.0,
                            "axes.linewidth": 0.6, "axes.edgecolor": "#8a8a8a",
                            "xtick.color": "#8a8a8a", "ytick.color": "#8a8a8a",
                            "xtick.labelcolor": "#1a1a1a",
                            "ytick.labelcolor": "#1a1a1a",
                            "axes.labelcolor": "#1a1a1a",
                            "text.color": "#1a1a1a", "legend.frameon": False})
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "data", "olfaction")
INK, MUTED = "#1a1a1a", "#8a8a8a"
REF = [4, 6, 9, 11, 18, 26]
DIE1 = ["base", "base2", "inj", "inj2", "inj3"]
DIE2 = ["base", "trim1", "trim2", "trim3", "trim4",
        "inj1", "inj2", "inj3", "injlow1", "injlow2", "injlow3", "final",
        "watch1", "watch2", "watch3", "watch4", "watch5", "watch6"]


def load(names, tag):
    out = []
    for nm in names:
        suffix = f"_{nm}_aug24.json" if tag == "die1" else f"_{nm}_chip2_aug24.json"
        p = os.path.join(RES, f"selfheal{suffix}")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        out.append((nm, [c.get("meas") for c in d["calls"]]))
    return out


LAB = {"base": "drift-1", "base2": "drift-2", "inj": "inj-1", "inj2": "inj-2",
       "inj3": "inj-3", "injlow1": "inj-1'", "injlow2": "inj-2'",
       "injlow3": "inj-3'", "trim1": "t1", "trim2": "t2", "trim3": "t3",
       "trim4": "t4", "final": "fin", "watch1": "w1", "watch2": "w2",
       "watch3": "w3", "watch4": "w4", "watch5": "w5", "watch6": "w6"}


def main():
    r1, r2 = load(DIE1, "die1"), load(DIE2, "die2")
    runs = r1 + r2
    names = [nm for nm, _ in runs]
    M = np.array([[np.nan if m[i] == 0 else m[i] for m in (meas for _, meas in runs)]
                   for i in range(6)], dtype=float)
    norm = Normalize(vmin=0, vmax=33)

    fig = plt.figure(figsize=(3.5, 2.55))
    ax = fig.add_axes([0.115, 0.29, 0.815, 0.63])
    cax = fig.add_axes([0.115, 0.07, 0.815, 0.018])
    ax.imshow(M, aspect="auto", cmap="viridis", norm=norm,
              interpolation="nearest", origin="upper")
    for r in range(6):
        for c, (nm, meas) in enumerate(runs):
            v = M[r, c]
            if v != v:
                ax.add_patch(plt.Rectangle((c - .5, r - .5), 1, 1, facecolor="white",
                                           hatch="///", edgecolor=MUTED, lw=0, zorder=3))
                ax.text(c, r, "oor", ha="center", va="center", fontsize=3.6,
                        color="#444", zorder=4)
            else:
                hot = (r == 2 and (nm in ("inj", "inj2", "inj3", "injlow1",
                                          "injlow2", "injlow3", "inj1", "inj2", "inj3")))
                ax.text(c, r, f"{int(v)}", ha="center", va="center", fontsize=4.6,
                        color="white" if (v < 8 or v > 26) else INK,
                        fontweight="bold" if hot else "normal", zorder=4)

    ax.set_yticks(range(6))
    ax.set_yticklabels([f"$N^\\star$={r}" for r in REF], fontsize=5.6)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([LAB.get(n, n) for n in names], fontsize=4.6, rotation=45,
                       ha="right")

    # die boundary, trim band, power cycle, injection markers
    zsplit = len(r1) - 0.5
    ax.axvline(zsplit, color="white", lw=2.5, zorder=6)
    ax.axvline(zsplit, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=7)
    ax.text(len(r1) / 2 - 0.5, -1.05, "die 1", fontsize=5.6, ha="center", color=INK)
    ax.text(len(r1) + len(r2) / 2 - 0.5, -1.05, "die 2", fontsize=5.6, ha="center",
            color=INK)
    a, b = names.index("trim1"), names.index("trim4")
    ax.axvspan(a - .5, b + .5, color="#f2e3c9", alpha=0.45, zorder=1)
    ax.text((a + b) / 2, -1.05, "trims", fontsize=5.0, ha="center", color="#8a6d1a")
    zw = names.index("watch1") - 0.5
    ax.axvline(zw, color="white", lw=2.5, zorder=6)
    ax.axvline(zw, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=7)
    ax.text(zw - 0.3, -1.05, "pwr", fontsize=4.6, ha="right", color=MUTED)
    names1 = [nm for nm, _ in r1]
    names2 = [nm for nm, _ in r2]
    for die, nms, col in ((1, ("inj", "inj2", "inj3"), "#0b7285"),
                          (2, ("injlow1", "injlow2", "injlow3"), "#0b7285"),
                          (2, ("inj1", "inj2", "inj3"), "#c0392b")):
        seq = names1 if die == 1 else names2
        off = 0 if die == 1 else len(r1)
        for n in nms:
            if n in seq:
                ax.scatter(off + seq.index(n), -0.45, marker="v", s=12,
                           color=col, clip_on=False, zorder=5)

    ax.set_xticks(np.arange(-.5, len(names), 1), minor=True)
    ax.set_yticks(np.arange(-.5, 6, 1), minor=True)
    ax.grid(which="minor", color="white", lw=0.5)
    ax.tick_params(which="minor", length=0)
    ax.set_xlim(-.5, len(names) - .5)
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)

    cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="viridis"),
                      cax=cax, orientation="horizontal")
    cb.set_label("measured $N^{*}$ (input spikes)", fontsize=6.0)
    cb.ax.tick_params(labelsize=5.2, length=2)
    cb.outline.set_visible(False)

    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, f"comparator_drift2d.{ext}"), dpi=300,
                    bbox_inches="tight")
    print(f"wrote comparator_drift2d.pdf/.png ({len(r1)} die-1 + {len(r2)} die-2 runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
