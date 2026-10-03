import argparse
#!/usr/bin/env python3
"""The analog spike-count comparator, calibrated on silicon. Writes comparator_cal.pdf.

This is the primitive the hybrid decision tree needs: a neuron that fires only after it
has received at least N input spikes, with N set by a bias. It replaces a digital compare
in the tree's decision node, so it has to be graded and it has to be programmable -- a
single fixed threshold is not enough.

  (a) MECHANISM. The membrane after a burst of N input spikes, at four calibration
      points. Sub-threshold and monotone in N: the neuron integrates the burst rather
      than responding to the first spike, which is what makes a count comparator possible
      at all. AER cannot see any of this -- it is one bit, and reads 0 across the whole
      panel -- so this is a scope measurement (/dev/ttyACM0).
  (b) TRANSFER. p(fire | N) for every level in the ladder, over ALL N in 0..32 rather
      than only the ladder points -- the tree presents every count, and measuring only
      the ladder values once hid five switches that were up to three counts off. Each
      curve is a step at its own count: the family IS the programmable comparator.
  (c) CALIBRATION MAP. The switching count against the two knobs. JExc sets how far each
      input spike climbs, so it spreads the low levels; vleakn sets rest relative to
      threshold and carries the top of the ladder. Tuning vleakn alone -- the obvious
      thing -- crushes levels 1..8 into half a millivolt against the free-run edge, where
      they are not separable; that failed run is why the axes are split this way.

Data: data/olfaction_comparator_tune.json (placement) and
data/olfaction_hybrid_transfer.json (the transfer matrix), n14, 25 MHz. This is the
ladder the hybrid tree of Section~\ref{par:hybridrun} actually executed against, measured
after the bench was moved; the earlier ten-level ladder is superseded and its drift is
the comparator-drift figure.

    python3 make_comparator.py
"""
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
C_J = "#0b7285"


def style():
    matplotlib.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5, "axes.labelsize": 7.5,
        "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
        "axes.linewidth": 0.6, "axes.edgecolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "axes.labelcolor": INK, "text.color": INK,
        "legend.frameon": False, "lines.solid_capstyle": "round",
    })


PANELS = "abc"   # "ac" = drop the p(fire) panel and relabel the map as (b)
OUT = "comparator_cal"
TRANSFER = None   # override the transfer matrix (figure provenance)


def merged():
    """The calibration map and the graded ramps on ONE x axis (N): left y =
    Delta J_exc (the knob that walks the switching count), right y = membrane
    above rest (scope ramps at four of those settings). Replaces the separate
    graded-integration and calibration-map panels in the calibration map."""
    style()
    import collections
    d = json.load(open(os.path.join(RES, "olfaction_comparator_tune.json")))
    xf = json.load(open(TRANSFER or os.path.join(RES, "olfaction_hybrid_transfer.json")))
    LEV = np.array(d["levels"], dtype=float)
    tr = d["trace"]
    park = collections.Counter(t["vleakn"] for t in tr).most_common(1)[0][0]
    lv = [L for L in xf["levels"] if xf["p"][str(L)][0] <= 0.05]
    swm = {L: next((n for n, q in zip(xf["N"], xf["p"][str(L)]) if q >= 1.0), None)
           for L in lv}

    fig, ax = plt.subplots(1, 1, figsize=(2.55, 2.42))
    axr = ax.twinx()

    # ---- right axis: membrane above rest at four parked settings (scope) ----
    pl = {int(k): (v["vleakn"], v["djexc"]) for k, v in d.get("placed", {}).items()
          if int(k) in lv}
    at_park = {L: dj for L, (vl, dj) in pl.items() if abs(vl - park) < 1e-9}
    want = tuple(at_park[L] for L in sorted(at_park, reverse=True)[:4])
    lvl_of = {round(dj, 6): L for L, dj in at_park.items()}
    seen, sel = set(), []
    for t in tr:
        k = round(t["djexc"], 6)
        if (abs(t["vleakn"] - park) < 1e-9 and k not in seen
                and any(abs(t["djexc"] - w) < 1e-9 for w in want)):
            seen.add(k); sel.append(t)
    sel.sort(key=lambda t: t["djexc"])
    cm = plt.cm.viridis(np.linspace(0.15, 0.8, len(sel)))
    top = 0.0
    for t, c in zip(sel, cm):
        v = np.array(t["vmem"], dtype=float)
        m = np.array(t["p"]) == 0.0
        sN = swm.get(lvl_of.get(round(t["djexc"], 6)))
        axr.plot(LEV[m], v[m], "o-", ms=2.4, lw=1.0, color=c,
                 label=rf"{t['djexc']*1000:+.1f} mV", zorder=3)
        top = max(top, float(np.max(v[m])))
        if sN:   # the ramp's switch, marked just under the firing band
            axr.plot(sN, 0.965, "v", ms=3.2, color=c, clip_on=False, zorder=4,
                     transform=axr.get_xaxis_transform())
    axr.set_ylim(-8, top * 1.25)
    axr.axhspan(top, top * 1.25, color="#f1f3f5", zorder=0)
    axr.text(32, top * 1.12, r"above $\theta$: fires", fontsize=5.6,
             color=MUTED, va="center", ha="right")
    axr.axhline(0, color=GRID, lw=0.6, zorder=1)
    axr.set_ylabel("membrane above rest (mV)")
    axr.legend(fontsize=5.4, loc="upper left", bbox_to_anchor=(0.0, 0.92),
               title=r"$\Delta J_{\rm exc}$", title_fontsize=5.4, handletextpad=0.4)

    # ---- left axis: the calibration map, replotted as (N*, Delta J_exc) ----
    def sw(t):
        q = [n for n, p in zip(d["levels"], t["p"]) if p >= 0.5]
        return q[0] if q and t["p0"] <= 0.3 else None

    u = {}
    for t in tr:
        if abs(t["vleakn"] - park) < 1e-9 and sw(t):
            u.setdefault(round(t["djexc"] * 1000, 3), sw(t))
    jx = sorted(u.items())
    RED = "#c0392b"      # the knob axis: red, matching the drift-figure injections
    ax.plot([n for _, n in jx], [j for j, _ in jx], "d:", ms=2.8, lw=1.0,
            color=RED, zorder=2)
    ax.set_ylabel(r"$\Delta J_{\rm exc}$ from base (mV)", color=RED)
    ax.tick_params(axis="y", colors=RED)
    ax.spines["left"].set_color(RED)

    # ---- shared x axis ----
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 8, 16, 32])
    ax.set_xticklabels(["1", "2", "4", "8", "16", "32"])
    ax.set_xlim(0.9, 34)
    ax.set_xlabel("input spikes in burst, $N$")
    ax.grid(True, color=GRID, lw=0.4, alpha=0.7)
    ax.set_axisbelow(True)
    for a, sp in ((ax, ("top",)), (axr, ("top",))):
        for s in sp:
            a.spines[s].set_visible(False)

    fig.tight_layout(pad=0.5)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, f"{OUT}.{ext}"), dpi=300)
    print(f"wrote {OUT}.pdf/.png (merged map+ramps)")
    return 0


def main():
    style()
    d = json.load(open(os.path.join(RES, "olfaction_comparator_tune.json")))
    xf = json.load(open(TRANSFER or os.path.join(RES, "olfaction_hybrid_transfer.json")))
    LEV = np.array(d["levels"], dtype=float)
    tr = d["trace"]
    # the parked vleakn is whatever most of the trace was taken at, not the CLI default
    import collections
    park = collections.Counter(t["vleakn"] for t in tr).most_common(1)[0][0]
    NS = np.array(xf["N"], dtype=float)
    # the ladder is what the transfer found usable: a level that fires with no input is
    # not a comparator, and one whose file failed verification is not on disk at all
    lv = [L for L in xf["levels"] if xf["p"][str(L)][0] <= 0.05]
    swm = {L: next((n for n, q in zip(xf["N"], xf["p"][str(L)]) if q >= 1.0), None)
           for L in lv}
    print(f"ladder {lv} switching at {[swm[L] for L in lv]}")

    if PANELS == "abc":
        fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(7.09, 2.35))
    elif PANELS == "ac":
        fig, (a1, a3) = plt.subplots(1, 2, figsize=(4.85, 2.35))
        a2 = plt.figure().add_subplot(1, 1, 1)   # discarded
    elif PANELS == "a":
        fig, a1 = plt.subplots(1, 1, figsize=(2.55, 2.30))
        a2 = plt.figure().add_subplot(1, 1, 1)
        a3 = plt.figure().add_subplot(1, 1, 1)
    else:   # "b" -- the calibration map alone
        fig, a3 = plt.subplots(1, 1, figsize=(2.55, 2.30))
        a1 = plt.figure().add_subplot(1, 1, 1)
        a2 = plt.figure().add_subplot(1, 1, 1)

    # ---- (a) membrane vs N, sub-threshold ---------------------------------
    # Only points where the neuron did NOT fire: once it spikes, "peak membrane" is the
    # spike amplitude (~490 mV) and no longer measures integration.
    # Settings the LADDER actually uses, taken from the placement record rather than
    # chosen for a pretty ramp. Deeper settings give longer sub-threshold ramps --
    # everything at or below -1.5 mV never reaches threshold across all 32 counts -- but a
    # curve with no switch point reads as a comparator that does not work, and no level is
    # placed there. One curve per level ties this panel to (b).
    # Keyed on (vleakn, dJExc), not dJExc alone: lvl24 and lvl32 share dJExc = +0.0 and
    # are distinguished only by vleakn, so a dJExc-only map silently labelled the parked
    # lvl24 curve with lvl32's switching count.
    pl = {int(k): (v["vleakn"], v["djexc"]) for k, v in d.get("placed", {}).items()
          if int(k) in lv}
    at_park = {L: dj for L, (vl, dj) in pl.items() if abs(vl - park) < 1e-9}
    want = tuple(at_park[L] for L in sorted(at_park, reverse=True)[:4])
    lvl_of = {round(dj, 6): L for L, dj in at_park.items()}
    # dedupe by dJExc: step 3 re-probes (park, 0.0) as its first point, so the raw trace
    # holds two entries at the same knob setting and the legend showed "+0.0 mV" twice
    seen, sel = set(), []
    for t in tr:
        k = round(t["djexc"], 6)
        if (abs(t["vleakn"] - park) < 1e-9 and k not in seen
                and any(abs(t["djexc"] - w) < 1e-9 for w in want)):
            seen.add(k); sel.append(t)
    sel.sort(key=lambda t: t["djexc"])
    cm = plt.cm.viridis(np.linspace(0.15, 0.8, len(sel)))
    top = 0.0
    for t, c in zip(sel, cm):
        v = np.array(t["vmem"], dtype=float)
        m = np.array(t["p"]) == 0.0
        # The switch quoted is the TRANSFER's, measured over every count and shared with
        # panel (b). The placement sweep only probed the ladder values, so its own first
        # firing point is an upper bound on the same number, not a second measurement.
        L0 = lvl_of.get(round(t["djexc"], 6))
        sN = swm.get(L0)
        a1.plot(LEV[m], v[m], "o-", ms=2.6, lw=1.0, color=c,
                label=rf"{t['djexc']*1000:+.1f} mV"
                      + (rf", $N^{{*}}{{=}}${sN}" if sN else ""))
        top = max(top, float(np.max(v[m])))
        # the first N that fired: the ramp has left the sub-threshold regime, and its
        # measured "peak" from here on is the spike, not the integrated burst
        if sN:
            a1.plot(sN, 1.0, "v", ms=3.4, color=c, clip_on=False,
                    transform=a1.get_xaxis_transform())
    a1.axhspan(top, top * 1.25, color="#f1f3f5", zorder=0)
    a1.text(32, top * 1.12, r"above $\theta$: fires", fontsize=5.6,
            color=MUTED, va="center", ha="right")
    a1.set_ylim(-8, top * 1.25)
    a1.axhline(0, color=GRID, lw=0.6)
    a1.set_xscale("log"); a1.set_xticks([1, 2, 4, 8, 16, 32])
    a1.set_xticklabels(["1", "2", "4", "8", "16", "32"])
    a1.set_xlabel("input spikes in burst, $N$")
    a1.set_ylabel("membrane above rest (mV)")
    if PANELS in ("abc", "ac"):
        a1.set_title("(a) graded integration (scope)", fontsize=7.5, loc="left", pad=18)
    a1.legend(fontsize=5.4, loc="upper left", bbox_to_anchor=(0.0, 0.90),
              title=r"$\Delta J_{\rm exc}$", title_fontsize=5.4)

    # ---- (b) p(fire | N) for every calibrated level ------------------------
    cm = plt.cm.plasma(np.linspace(0.05, 0.85, len(lv)))
    X0 = 0.62                       # the N=0 control, parked left of the log axis
    for L, c in zip(lv, cm):
        p = np.array(xf["p"][str(L)], dtype=float)
        x = np.where(NS == 0, X0, NS)
        a2.plot(x, p, "-", lw=1.1, color=c)
        # alternate the label height: adjacent switches (18 and 21) sit close enough on
        # a log axis that same-row labels overlap
        dy = 4 if lv.index(L) % 2 == 0 else 12
        a2.annotate(f"{swm[L]}", (swm[L], 1.0), textcoords="offset points",
                    xytext=(0, dy), ha="center", fontsize=5.4, color=c)
    a2.axvline(0.78, color=MUTED, lw=0.5, ls=(0, (1, 2)))
    a2.set_xscale("log"); a2.set_xticks([X0, 1, 2, 4, 8, 16, 32])
    a2.set_xticklabels(["0", "1", "2", "4", "8", "16", "32"])
    a2.set_xlim(0.55, 45); a2.set_ylim(-0.06, 1.26)
    # headroom for the labels, but a probability axis must not read past 1
    a2.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    a2.set_xlabel("input spikes in burst, $N$")
    a2.set_ylabel(r"$p(\mathrm{fire})$")
    a2.set_title(rf"(b) {len(lv)} programmed thresholds", fontsize=7.5, loc="left",
                 pad=18)

    # ---- (c) calibration map ------------------------------------------------
    def sw(t):
        q = [n for n, p in zip(d["levels"], t["p"]) if p >= 0.5]
        return q[0] if q and t["p0"] <= 0.3 else None

    def series(pairs):
        u = {}
        for x, y in pairs:
            u.setdefault(round(x, 3), y)
        return sorted(u.items())

    jx = series((t["djexc"] * 1000, sw(t)) for t in tr
                if abs(t["vleakn"] - park) < 1e-9 and sw(t))
    a3.plot([x for x, _ in jx], [y for _, y in jx], "o-", ms=2.8, lw=1.0, color=C_J,
            label=r"$\Delta J_{\rm exc}$")
    a3.set_yscale("log"); a3.set_yticks([1, 2, 4, 8, 16, 32])
    a3.set_yticklabels(["1", "2", "4", "8", "16", "32"])
    a3.set_xlabel(r"$\Delta J_{\rm exc}$ from base (mV)", color=C_J)
    a3.tick_params(axis="x", colors=C_J)
    a3.set_ylabel("switching count $N^{*}$")
    if PANELS in ("abc", "ac"):
        a3.set_title("(c) calibration map" if PANELS == "abc" else "(b) calibration map",
                     fontsize=7.5, loc="left", y=1.20)
    a3.legend(fontsize=5.6, loc="lower left")

    for ax in (a1, a2, a3):
        ax.grid(True, color=GRID, lw=0.4, alpha=0.7)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    fig.tight_layout(pad=0.5, w_pad=1.4)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(HERE, f"{OUT}.{ext}"), dpi=300)
    print("wrote comparator_cal.pdf / .png")
    print(f"levels in the figure: {lv}")


if __name__ == "__main__":
    _ap = argparse.ArgumentParser()
    _ap.add_argument("--panels", default="abc", choices=["abc", "ac", "a", "b", "m"])
    _ap.add_argument("--out", default="comparator_cal")
    _ap.add_argument("--transfer", default=None)
    _a = _ap.parse_args()
    PANELS, OUT, TRANSFER = _a.panels, _a.out, _a.transfer
    if _a.panels == "m":
        raise SystemExit(merged())
    raise SystemExit(main())
