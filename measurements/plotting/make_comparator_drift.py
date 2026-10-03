#!/usr/bin/env python3
"""Comparator drift: hours matter, minutes do not. Writes comparator_drift.pdf.

The calibrated ladder does not hold indefinitely, and the way it fails decides how a
hybrid has to be operated. Two independent measurements, on the same axes:

  LONG TIMESCALE -- transfer matrices, p(fire | N) over ALL N in 0..32, acquired hours
  apart. The switching count of every upper level moves upward; levels 1-4 do not move at
  all.

  SHORT TIMESCALE -- during a five-hour execution each level's switching count was
  measured immediately before and immediately after its own block of node evaluations.
  Those brackets are the short horizontal segments: nine of ten are flat.

Together they say the ladder is stable across a working block and shifts across a
session, which is an operational instruction rather than a curiosity: re-measure the
transfer immediately before a run that depends on the switch values, and do not reuse one
from earlier in the day. A run that did reuse one had two levels wrong by four and five
counts, and those two levels produced all of its error.

Only levels whose switch is resolvable are drawn; a level that stops firing within the
probe window has no count to plot and is marked instead.

    python3 make_comparator_drift.py
"""
import datetime as dt
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "..", "results")
if not os.path.isdir(RES):
    RES = os.path.join(HERE, "..", "..", "results")
INK, MUTED, GRID = "#1a1a1a", "#8a8a8a", "#d8d8d8"
LADDER = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
T0 = dt.datetime(2026, 8, 16, 18, 42)          # calibration finished


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


def strict(path):
    """First count that fires EVERY repetition, per level; None if never.

    Returns None for the whole acquisition if it is still being written -- the transfer
    dumps its JSON after each level, so a run in progress has a valid file with only some
    of the ladder in it, and half a ladder plotted as a line would misread as drift."""
    t = json.load(open(path))
    if any(str(L) not in t.get("p", {}) for L in LADDER):
        return None
    return {L: next((n for n, q in zip(t["N"], t["p"][str(L)]) if q >= 1.0), None)
            for L in LADDER}


def hours(ts):
    return (dt.datetime.fromtimestamp(ts) - T0).total_seconds() / 3600.0


def main():
    style()
    # --- the three transfer acquisitions, with the times they were measured ----
    acq = []
    for tag, path, when in (
            # A and B are earlier acquisitions, kept because the transfer writes to one
            # path and each run overwrites it; these copies keep the drift recoverable.
            ("A", os.path.join(RES, "olfaction_hybrid_transfer_A.json"),
             dt.datetime(2026, 8, 16, 18, 52)),
            ("B", os.path.join(RES, "olfaction_hybrid_transfer_B.json"),
             dt.datetime(2026, 8, 17, 0, 5)),
            ("C", os.path.join(RES, "olfaction_hybrid_transfer.json"), None)):
        if not os.path.exists(path):
            continue
        if when is None:                      # the live one: date it by its own archive
            raw = os.path.join(RES, "olfaction_hybrid_transfer_raw.npz")
            when = (dt.datetime.fromtimestamp(np.load(raw)["t0"][0])
                    if os.path.exists(raw) else None)
            if when is None:
                continue
        sw = strict(path)
        if sw is None:
            print(f"  {tag}: acquisition incomplete, skipped")
            continue
        acq.append((tag, (when - T0).total_seconds() / 3600.0, sw))
    print(f"{len(acq)} transfer acquisitions: "
          + ", ".join(f"{t} at +{h:.1f} h" for t, h, _ in acq))

    # --- the within-run brackets, placed at the times their groups actually ran -
    run2 = json.load(open(os.path.join(RES, "olfaction_hybrid_chip_run2.json")))
    z = np.load(os.path.join(RES, "olfaction_hybrid_chip_run2.npz"), allow_pickle=True)
    lv = np.asarray(z["node_level"])
    raw2 = np.load(os.path.join(RES, "olfaction_hybrid_chip_run2_raw.npz"))
    t2 = raw2["t0"]
    order = sorted(set(int(x) for x in lv))          # run 2 executed ASCENDING
    nch = len(t2) // max(len(lv), 1)
    spans, i0 = {}, 0
    for L in order:
        n = int((lv == L).sum()) * nch
        spans[L] = (hours(t2[i0]), hours(t2[min(i0 + n, len(t2)) - 1]))
        i0 += n

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.09, 2.7),
                                 gridspec_kw={"width_ratios": [1.5, 1]})
    cm = plt.cm.viridis(np.linspace(0.05, 0.88, len(LADDER)))

    # ---- (a) switching count against wall-clock time -------------------------
    for L, c in zip(LADDER, cm):
        xs = [h for _, h, s in acq if s[L] is not None]
        ys = [s[L] for _, _, s in acq if s[L] is not None]
        if xs:
            a1.plot(xs, ys, "o-", ms=4, lw=1.1, color=c, zorder=3)
            # Levels 1-4 sit one count apart and their labels stay merged; they
            # are also the flat ones, so the cluster is annotated once instead.
            # labels are attached per FINAL VALUE below, because drift can merge two
            # levels onto the same count and two labels would then sit on top of
            # each other -- which is also exactly the collision worth pointing out
        b = run2.get("switch_track", {}).get(str(L), {})
        if b.get("before") is not None and L in spans:
            x0, x1 = spans[L]
            a1.plot([x0, x1], [b["before"], b.get("after", b["before"])], "-",
                    lw=2.6, color=c, alpha=0.55, solid_capstyle="butt", zorder=2)
        elif L in spans:
            x0, x1 = spans[L]
            a1.plot([(x0 + x1) / 2], [33], "x", ms=4, color=c, zorder=3)
            a1.annotate("stopped\nfiring", ((x0 + x1) / 2, 33),
                        textcoords="offset points", xytext=(0, -9), ha="center",
                        va="top", fontsize=5.0, color=c)
    # one label per distinct final count; levels that have merged share it
    last = acq[-1][2]
    groups = {}
    for L, c in zip(LADDER, cm):
        if L > 4 and last.get(L) is not None:
            groups.setdefault(last[L], []).append((L, c))
    for val, members in groups.items():
        names = ", ".join(f"lvl{L}" for L, _ in members)
        col = members[-1][1]
        merged = len(members) > 1
        a1.annotate(names + ("  (merged)" if merged else ""), (acq[-1][1], val),
                    textcoords="offset points", xytext=(6, 0), ha="left", va="center",
                    fontsize=5.4, color="#c0392b" if merged else col,
                    fontweight="bold" if merged else "normal")
    for _, h, _ in acq:
        a1.axvline(h, color=MUTED, lw=0.5, ls=(0, (1, 3)))
    a1.annotate("lvl1\u20134: flat", (acq[-1][1], 2.5), textcoords="offset points",
                xytext=(6, 0), ha="left", va="center", fontsize=5.4, color=MUTED)
    a1.text(0.02, 0.97, "dots: transfer matrices, all $N$\nbars: switch measured either "
            "side of\nthat level's own block of nodes",
            transform=a1.transAxes, fontsize=5.6, color=MUTED, va="top", linespacing=1.35)
    a1.set_xlabel("hours since calibration")
    a1.set_ylabel("switching count $N^{*}$")
    hmax = max(h for _, h, _ in acq)
    a1.set_ylim(0, 37); a1.set_xlim(-0.7, hmax + 3.2)     # room for the right-hand labels
    a1.set_title("(a) the ladder over a session", fontsize=7.5, loc="left")

    # ---- (b) between sessions vs within a run --------------------------------
    if len(acq) >= 2:
        w = 0.38
        x = np.arange(len(LADDER))
        between, within = [], []
        for L in LADDER:
            a, b = acq[0][2][L], acq[-1][2][L]
            between.append((b - a) if (a is not None and b is not None) else np.nan)
            t = run2.get("switch_track", {}).get(str(L), {})
            within.append((t["after"] - t["before"])
                          if t.get("before") is not None and t.get("after") is not None
                          else np.nan)
        span = acq[-1][1] - acq[0][1]
        a2.bar(x - w / 2, between, w, color="#c0392b",
               label=f"between sessions ({span:.0f} h apart)")
        a2.bar(x + w / 2, within, w, color="#0b7285", label="within a run (its own block)")
        for i, v in enumerate(between):
            if v != v:
                a2.text(i - w / 2, 0.15, "n/a", fontsize=5.0, ha="center", color="#c0392b")
        for i, v in enumerate(within):
            if v != v:
                a2.text(i + w / 2, 0.15, "n/a", fontsize=5.0, ha="center", color="#0b7285")
        a2.axhline(0, color=MUTED, lw=0.6)
        a2.set_xticks(x); a2.set_xticklabels([str(L) for L in LADDER])
        a2.set_xlabel("bias file (nominal level)")
        a2.set_ylabel(r"change in $N^{*}$ (counts)")
        a2.set_title("(b) hours matter, minutes do not", fontsize=7.5, loc="left")
        a2.legend(fontsize=5.8, loc="upper left")

    for ax in (a1, a2):
        ax.grid(color=GRID, lw=0.4, alpha=0.7); ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, f"comparator_drift.{ext}"), dpi=200,
                    bbox_inches="tight")
    print("wrote comparator_drift.pdf / .png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
