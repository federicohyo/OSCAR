#!/usr/bin/env python3
"""D_eff decomposition on REF25 -- three silicon acquisitions, and a model matched to the new one.

WHY v3. deff_decomp_v2 plots two silicon curves against software rows that run at
1.5-5.3 Hz. REF25 runs at 39 Hz. D_eff falls with rate in this pipeline, so putting
those on one axis compares a 2 Hz model against a 39 Hz array and the vertical gap
between them measures nothing. v3 adds the row that makes REF25's
comparison like-for-like: a software LIF whose per-neuron thresholds are bisected to
REF25's own per-neuron rates.

TWO MODEL CORRECTIONS FALL OUT OF DOING THAT, and both are physics the reference
model left out rather than fitting knobs:

1. THE REFERENCE IMPULSE MODEL CANNOT REACH REF25's RATES AT ALL. With instantaneous
   input jumps a LIF emits at most one spike per input event -- the jump crosses
   threshold once and resets -- so it caps at 22.5 Hz mean against silicon's 39.0,
   and 13 of 16 per-neuron targets are unreachable at any threshold. Silicon exceeds
   that bound: it emits up to 2.08x its input event count (n15), measured.
2. THAT GAIN IS NOT FREE-RUNNING. Measured on the bench at the REF25 bias point with
   no stimulus at all: 0.00 Hz on every one of the 16 neurons. The array is silent
   without input, so gain > 1 is the DPI synapse delivering charge over time rather than
   spontaneous activity.

So the model needs the DPI's synaptic tail, which `simulate(tau_syn=...)` already
implements and which deff_physical_mechanisms already calls "SYN DPI tail". At
tau_syn = 10 ms the bisection reaches REF25's rates with 1 of 16 neurons off target.

    ./.venv-meas/bin/python3 measurements/plotting/make_deff_v3.py
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", ".."))
sys.path.insert(0, REPO)
os.chdir(REPO)

from reservoir_demo_proj import corr_effdim, load

matplotlib.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
})

HERE = os.path.dirname(os.path.abspath(__file__))
K = 8
TAUS = np.array([0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
TAU_TABLE = 0.02
MATCH = os.path.join(REPO, "results", "deff_ref25_match.json")

SILICON = [
    ("Silicon REF25, 2026-08-12 (39 Hz, no lattice)",
     "reservoir_spikes_ref25_2026-08-12.npz", "#c0392b", "o-", 2.2),
    ("Silicon 2026-08-11 (23 Hz, no lattice)",
     "reservoir_spikes_nv_randproj_aug11.npz", "#e06666", "o--", 1.5),
    ("Silicon DIM 2026-07 (8.8 Hz, 11.99 ms lattice)",
     "reservoir_spikes_nv_randproj.npz", "#f0a0a0", "o:", 1.5),
]
SOFTWARE = [
    ("SW LIF, het. $\\tau$+$V_{th}$+$w$, + projection (5 Hz)",
     "sw_proj_allparam_mm0.65.npz", "#e8880c", "^-", 1.3),
    ("SW LIF, identical, + projection (2 Hz)", "sw_proj.npz", "#0b7285", "s-", 1.3),
    ("SW LIF, identical, shared input (1.5 Hz)", "sw_shared.npz", "0.55", ":", 1.2),
]


def rate_of(sp, T):
    n, nb = sp.shape
    return float(np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T
                          for j in range(n)]))


def main():
    fig, ax = plt.subplots(figsize=(4.2, 3.1))
    out = {}

    for label, npz, color, mk, lw in SILICON + SOFTWARE:
        if not os.path.exists(npz):
            print(f"  SKIP (missing) {npz}")
            continue
        sp, _, T = load(npz)
        eds = [corr_effdim(sp, T, K, "exp", t)[2] for t in TAUS]
        ax.plot(TAUS * 1000, eds, mk, color=color, lw=lw, ms=3.4, label=label)
        out[label] = {"npz": npz, "deff": eds, "deff20": eds[1],
                      "mean_rate_hz": rate_of(sp, T)}
        print(f"{label:52s} tau=20ms D_eff={eds[1]:5.1f}  rate={out[label]['mean_rate_hz']:5.1f} Hz")

    # The row that makes REF25's comparison mean something.
    if os.path.exists(MATCH):
        # tau_syn stays unmeasurable from spikes alone -- only the membrane current
        # would give it, and this bench reads spikes. So plot the ENVELOPE over
        # every tau_syn that can reach silicon's rates, and show that the gap is
        # independent of the parameter outside our measurement.
        mm = json.load(open(MATCH))
        keys = sorted(k for k in mm if k.startswith("tau_syn_"))
        band = np.array([mm[k]["deff"] for k in keys])
        lo, hi = band.min(axis=0), band.max(axis=0)
        best = mm[keys[int(np.argmax(band[:, 1]))]]        # most conservative row
        ax.fill_between(TAUS * 1000, lo, hi, color="#2a78d6", alpha=0.22, lw=0)
        ax.plot(TAUS * 1000, best["deff"], "D-", color="#2a78d6", lw=1.8, ms=3.4,
                label="SW LIF, DPI tail, matched to REF25 (36 Hz)")
        out["SW LIF matched to REF25"] = {k: mm[k] for k in keys}
        print(f"{'SW LIF, DPI tail, matched to REF25':52s} "
              f"tau=20ms D_eff={lo[1]:.1f}-{hi[1]:.1f} over tau_syn 10-30 ms")

        si20 = out[SILICON[0][0]]["deff20"]
        gmin, gmax = si20 - hi[1], si20 - lo[1]
        ax.annotate("", xy=(20, si20), xytext=(20, hi[1]),
                    arrowprops=dict(arrowstyle="<->", color="k", lw=1.0))
        ax.text(22, 0.5 * (si20 + hi[1]),
                f"gap {gmin:.1f}-{gmax:.1f}\n(rate-matched)", fontsize=6.4, va="center")
        out["gap_rate_matched_at_20ms"] = [float(gmin), float(gmax)]
        print(f"\nRATE-MATCHED GAP at tau=20 ms: {gmin:.1f}-{gmax:.1f} units "
              f"across every tau_syn that reaches silicon's rates")

    ax.set_xscale("log")
    ax.set_xticks(TAUS * 1000)
    ax.set_xticklabels([f"{t*1000:.0f}" for t in TAUS])
    ax.set_xlabel("read-out kernel $\\tau$ (ms)")
    ax.set_ylabel("effective dimensionality $D_{\\mathrm{eff}}$")
    ax.legend(fontsize=5.4, loc="upper right", frameon=False, labelspacing=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        p = os.path.join(HERE, f"deff_decomp_v3.{ext}")
        fig.savefig(p, dpi=300)
        print("wrote", p)
    json.dump(out, open(os.path.join(REPO, "results", "deff_decomp_v3.json"), "w"),
              indent=2)


if __name__ == "__main__":
    raise SystemExit(main())
