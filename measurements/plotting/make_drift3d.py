#!/usr/bin/env python3
"""Drift and repair on two dies as ONE 3D waterfall (replaces the two-panel
heatmap comparator_drift2_a/b.pdf).

One curve per selfheal run: x = ladder level (1..6), y = measured switching
count, z = elapsed time since the first die-1 run. The runs were all taken
in one bench session (~2.3 h); the five-day drift is BEFORE the first run.
The reference ladder is the dashed curve at the back; out-of-range levels
plot as open markers at 33.

Phases (same semantics as the old heatmaps):
  die 1: five-day drift (base, base2) red; injected-and-repaired (inj x3) teal
  die 2: naive start dark red; per-die trims amber; injected (refused) red;
         injected-and-repaired teal; idle watching gray; power cycle between
         watch0 and watch1 (white gap line on z).

    python3 make_drift3d.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42,
                            "font.family": "sans-serif",
                            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"]})
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "data", "olfaction")
INK, MUTED = "#1a1a1a", "#8a8a8a"
REF = [4, 6, 9, 11, 18, 26]
DIE1 = ["base", "base2", "inj", "inj2", "inj3"]
DIE2 = ["base", "trim1", "trim2", "trim3", "trim4",
        "inj1", "inj2", "inj3", "injlow1", "injlow2", "injlow3", "final",
        "watch1", "watch2", "watch3", "watch4", "watch5", "watch6"]
PHASE = {  # run-name prefix -> (colour, legend label); order = legend order
    "base":   ("#c0392b", "die 1: five-day drift"),
    "inj":    ("#0b7285", "injected, repaired"),
    "trim":   ("#b9770e", "die 2: per-die trims"),
    "inj1":   ("#a04040", "injected, refused"),
    "inj2":   ("#a04040", None),
    "inj3":   ("#a04040", None),
    "injlow": ("#0b7285", None),
    "final":  ("#1a1a1a", None),
    "watch":  ("#8a8a8a", "die 2: idle watching"),
}


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


def phase_of(die, nm):
    if die == "die1":
        return "base" if nm.startswith("base") else "inj"
    for k in ("injlow", "inj1", "inj2", "inj3", "inj", "trim", "watch", "final", "base"):
        if nm.startswith(k):
            return k
    return "base"


def main():
    r1, r2 = load(DIE1, "die1"), load(DIE2, "die2")
    t0 = r1[0][1]

    fig = plt.figure(figsize=(3.5, 3.0))
    ax = fig.add_subplot(projection="3d")
    ax.view_init(elev=17, azim=-63)

    drawn = set()
    for die, runs in (("die1", r1), ("die2", r2)):
        for nm, t, meas in runs:
            ph = phase_of(die, nm)
            col, lab = PHASE[ph]
            z = (t - t0) / 3600.0
            xs = np.arange(1, 7)
            ys = np.array([(m if (m and 0 < m <= 32) else 33) for m in meas], dtype=float)
            ok = np.array([(m is not None and 0 < m <= 32) for m in meas])
            lbl = lab if lab and lab not in drawn else None
            if lbl:
                drawn.add(lab)
            ax.plot(xs[ok], ys[ok], z, "-", lw=0.8, color=col, alpha=0.9,
                    label=lbl, zorder=3)
            ax.plot(xs[ok], ys[ok], z, "o", ms=2.2, color=col, zorder=4)
            ax.plot(xs[~ok], ys[~ok], z, "x", ms=3.2, mew=0.9, color=col, zorder=4)

    # the reference ladder: dashed, at the back, above everything
    zback = (max(t for _, t, _ in r1 + r2) - t0) / 3600.0 + 0.25
    ax.plot(np.arange(1, 7), REF, zback, "--", lw=1.3, color=INK, zorder=2,
            label="reference ladder")
    for x, r in zip(range(1, 7), REF):
        ax.plot([x, x], [r, r], [0, zback], ":", lw=0.5, color=MUTED, alpha=0.5,
                zorder=1)

    # die boundary + power-cycle gap on the time axis
    zsplit = (r2[0][1] - t0) / 3600.0 - 0.06
    ax.plot([1, 6], [33.5, 33.5], zsplit, "-", lw=1.6, color="white", zorder=5)
    ax.plot([1, 6], [33.5, 33.5], zsplit, ":", lw=0.7, color=MUTED, zorder=6)
    zw = (next(t for nm, t, _ in r2 if nm == "watch1") - t0) / 3600.0
    ax.plot([1, 6], [33.5, 33.5], zw, ":", lw=0.7, color=MUTED, zorder=6)

    ax.text(1.0, 36, zsplit * 0.45, "die 1", fontsize=6, color=MUTED)
    ax.text(1.0, 36, (zsplit + (r2[-1][1] - t0) / 3600.0) / 2 + 0.1, "die 2",
            fontsize=6, color=MUTED)

    ax.set_xticks(range(1, 7))
    ax.set_xlabel("ladder level")
    ax.set_ylabel("measured $N^{*}$")
    ax.set_zlabel("time (h)")
    ax.set_ylim(0, 36)
    ax.set_yticks([0, 8, 16, 24, 32])
    ax.tick_params(labelsize=6, pad=1)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_tick_params(pad=0, labelsize=6)
        axis._axinfo["grid"]["linewidth"] = 0.3
        axis._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.6)
    ax.legend(fontsize=5.2, loc="upper left", frameon=False,
              bbox_to_anchor=(-0.05, 1.12), handlelength=1.4, labelspacing=0.25)
    ax.set_box_aspect((1.6, 2.2, 0.8))

    fig.tight_layout(pad=0.2)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, f"comparator_drift3d.{ext}"), dpi=300)
    print(f"wrote comparator_drift3d.pdf/.png ({len(r1)} die-1 + {len(r2)} die-2 runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
