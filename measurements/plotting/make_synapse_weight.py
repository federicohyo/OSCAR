#!/usr/bin/env python3
"""Figure: the 4-bit synaptic weight code, measured through the on-chip programming path.

Reads data/synapse/onset_<tag>.json (written by
measurements/array/scripts/synapse_onset.py) and renders
weight_code.pdf.

The measured quantity is the excitatory branch bias at which a given weight word just brings
the neuron to threshold. Because the branches run in weak inversion, current is exponential
in gate voltage, so this onset voltage is a logarithmic readout of the word's delivered
synaptic charge:  V_onset(w) = V0 - nUT*ln(A(w)).  A binary code (A = w) is therefore a
straight line against log w with slope -nUT; a code whose branches are all the same size
(A = popcount(w)) collapses onto five levels instead of sixteen.

Panel (a): onset per single-bit word -- each branch's own strength, against the binary ideal.
Panel (b): onset for all 15 non-zero words, against both models.

Usage:  ../../.venv-meas/bin/python3 make_synapse_weight.py [--tag n5]
"""

import argparse
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
# fonttype 42 (TrueType) -- Type 3 fonts are rejected by several publisher
# pipelines, so emit TrueType-embedded PDFs
matplotlib.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42})
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
# OSCAR reorg: this file lived in measurements/plotting/ (3 levels deep);
# it is now measurements/plotting/ (2 levels deep). ROOT is the repo root.
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Okabe-Ito, assigned in fixed order and kept from cycling; validated for CVD separation.
C_MEAS = "#0072B2"   # measured
C_BIN = "#D55E00"    # binary-code model
C_UNARY = "#009E73"  # equal-branch (popcount) model
INK = "#222222"
MUTED = "#666666"


def load(tag):
    path = os.path.join(ROOT, "data", "synapse", f"onset_{tag}.json")
    with open(path) as f:
        return json.load(f)


def series(block, words, sigma_floor=0.0):
    """Return (words, means, stds) for the words that produced an onset.

    The onset search is a bisection, so repeats on a stable chip can agree exactly and report
    zero spread. That is a statement about repeatability rather than about resolution: nothing finer
    than the bisection tolerance was ever probed. `sigma_floor` (half the tolerance) keeps the
    error bars and the distinguishable-level count honest about that limit.
    """
    ws, ms, ss = [], [], []
    for w in words:
        rec = block.get(str(w))
        if rec and rec.get("mean") is not None:
            ws.append(w)
            ms.append(rec["mean"])
            ss.append(max(rec["std"] or 0.0, sigma_floor))
    return ws, ms, ss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="n5")
    ap.add_argument("--ladder-tag", default="n5_ladder",
                    help="second run, measured with the calibrated bias ladder applied")
    ap.add_argument("--panels", default="ab", choices=["ab", "b"],
                    help="'ab' = the reference two-panel figure; "
                         "'b'  = the all-words panel alone")
    ap.add_argument("--out", default="weight_code.pdf")
    args = ap.parse_args()

    d = load(args.tag)
    sigma_floor = 0.5 * float(d.get("tol", 0.002))
    nut = d.get("nUT_volts")
    delta = nut * math.log(2) if nut else None
    try:
        dl = load(args.ladder_tag)
    except FileNotFoundError:
        dl = None
        print(f"note: no onset_{args.ladder_tag}.json -- plotting the equal-bias code only")

    if args.panels == "ab":
        fig, (axa, axb) = plt.subplots(1, 2, figsize=(7.0, 2.9))
    else:
        # same natural width and the same bottom margin in inches as
        # neuron_fi_reference.pdf, so the two panels' x-axes align when the
        # figure places them side by side, bottom-aligned
        fig = plt.figure(figsize=(3.6, 2.9))
        axb = fig.add_axes([0.1722, 0.1793, 0.7978, 0.7607])
        axa = None

    # ---- (a) per-branch onset -------------------------------------------------
    if axa is not None:
        bw, bm, bs = series(d.get("branches", {}), [1, 2, 4, 8], sigma_floor)
        bits = [w.bit_length() - 1 for w in bw]
        # express every branch relative to bit 0, so "binary" is a straight descending line
        v0 = dict(zip(bits, bm)).get(0, bm[0] if bm else 0.0)
        rel = [(m - v0) * 1000 for m in bm]
        err = [s * 1000 for s in bs]

        axa.bar(bits, rel, yerr=err, capsize=3, width=0.6, color=C_MEAS,
                edgecolor="white", linewidth=1.0, label="measured", zorder=3)
        if delta:
            axa.plot(range(4), [-(j) * delta * 1000 for j in range(4)], "o--", color=C_BIN,
                     markersize=6, linewidth=2, label="binary ideal", zorder=4)
        axa.axhline(0, color=MUTED, linewidth=0.8, zorder=1)
        axa.set_xticks(range(4))
        axa.set_xlabel("weight bit")
        axa.set_ylabel("onset bias re. bit 0 (mV)")
        axa.set_title("(a) the four branches", fontsize=10, color=INK)
        axa.legend(frameon=False, fontsize=8, loc="lower left")
        axa.grid(axis="y", color="#e6e6e6", linewidth=0.7, zorder=0)
        axa.set_axisbelow(True)
        for s in ("top", "right"):
            axa.spines[s].set_visible(False)

    # ---- (b) all 15 non-zero words, equal biases vs calibrated ladder ----------
    cw, cm, cs = series(d.get("code_equal", {}), list(range(1, 16)), sigma_floor)
    # plot every curve relative to its own w=1, so the two conditions share an origin
    # and the comparison is of SHAPE, which is what the code claim is about
    def rel_to_w1(ws, ms):
        anchor = dict(zip(ws, ms)).get(1, ms[0] if ms else 0.0)
        return [(m - anchor) * 1000 for m in ms]

    axb.errorbar(cw, rel_to_w1(cw, cm), yerr=[s * 1000 for s in cs], fmt="o",
                 color=C_UNARY, markersize=5, capsize=2, linewidth=1.5,
                 label="equal branch biases", zorder=4)

    if dl:
        lw, lm, ls_ = series(dl.get("code_ladder") or dl.get("code_equal", {}),
                             list(range(1, 16)), sigma_floor)
        axb.errorbar(lw, rel_to_w1(lw, lm), yerr=[s * 1000 for s in ls_], fmt="s",
                     color=C_MEAS, markersize=5, capsize=2, linewidth=1.5,
                     label="calibrated bias ladder", zorder=5)

    if nut:
        xs = list(range(1, 16))
        axb.plot(xs, [-nut * math.log(w) * 1000 for w in xs], "--", color=C_BIN,
                 linewidth=2, label=r"binary ideal  $A=w$", zorder=3)

    axb.set_xlabel("programmed weight word")
    axb.set_ylabel("onset bias re. $w=1$ (mV)")
    # the single-panel variant carries its subject in the figure sub-caption,
    # so the title can sit outside the axes
    if axa is not None:
        axb.set_title("(b) all 15 non-zero words", fontsize=10, color=INK)
    axb.set_xticks([1, 4, 8, 12, 15])
    ylo, yhi = axb.get_ylim()
    axb.set_ylim(ylo, yhi + 48)          # headroom so the legend clears the w=8 point
    axb.legend(frameon=False, fontsize=8, loc="upper left", handlelength=1.6,
               borderaxespad=0.2, labelspacing=0.3)
    axb.grid(color="#e6e6e6", linewidth=0.7, zorder=0)
    axb.set_axisbelow(True)
    for s in ("top", "right"):
        axb.spines[s].set_visible(False)

    if axa is not None:
        fig.tight_layout()
    out = os.path.join(HERE, args.out)
    fig.savefig(out, bbox_inches="tight" if axa is not None else None)
    print("wrote", out)

    # ---- numbers the caption and text quote ----------------------------------
    print("\n--- numbers for the reference analysis ---")
    if nut:
        print(f"nUT = {nut*1000:.1f} mV; one doubling of branch current = {delta*1000:.1f} mV")
    if axa is not None and bm:
        spread = (max(bm) - min(bm)) * 1000
        print(f"branch mismatch: onsets span {spread:.1f} mV "
              f"(binary would need {3*delta*1000:.1f} mV between bit 0 and bit 3)"
              if delta else f"branch mismatch: onsets span {spread:.1f} mV")
    def code_quality(ws, ms, ss, label):
        """Two separate things a weight code has to get right.

        RESOLUTION -- how many efficacy levels can be told apart at all. Onsets are sorted by
        value (not by word) and grouped while they stay within their combined +/-1 sigma, so
        this is a statement about the analog range, independent of which word sits where.

        ORDER -- whether a larger word actually means a stronger synapse. Counting |differences|
        while walking w upward would credit non-monotonic scatter as resolution, which is
        backwards: a code that jumps around defeats any resolution. So monotonicity
        is reported separately, and the effective bits below are only meaningful alongside it.
        """
        if not ms:
            return
        # resolution: cluster the onsets by value
        vals = sorted(zip(ms, ss))
        levels = 1
        last_m, last_s = vals[0]
        for m, s in vals[1:]:
            if abs(m - last_m) > (s + last_s):
                levels += 1
                last_m, last_s = m, s
        # order: every step up in w lowers or holds the onset (stronger synapse = lower onset)
        pairs = sorted(zip(ws, ms))
        breaks = [(a[0], b[0]) for a, b in zip(pairs, pairs[1:]) if b[1] > a[1] + (2 * sigma_floor)]
        # +1 for w=0 (synaptic drive at zero), always distinguishable
        print(f"{label}:")
        print(f"    resolution : {levels} resolvable levels over the 15 non-zero words "
              f"-> {math.log2(levels + 1):.2f} effective bits (nominal 4)")
        if breaks:
            print(f"    order      : NOT monotonic in w -- {len(breaks)} inversions, "
                  f"e.g. {breaks[:4]}")
        else:
            print("    order      : monotonic in w (no inversion beyond the noise floor)")

    code_quality(cw, cm, cs, "equal branch biases")
    if dl:
        lw, lm, ls_ = series(dl.get("code_ladder") or dl.get("code_equal", {}),
                             list(range(1, 16)), sigma_floor)
        code_quality(lw, lm, ls_, "calibrated bias ladder")


if __name__ == "__main__":
    main()
