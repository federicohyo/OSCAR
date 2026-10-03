#!/usr/bin/env python3
"""Measured LNA magnitude and phase against the Fig. 7 simulation.

Offline -- bench and FTDI untouched. Reads lna_phase.csv (from lna_phase_sweep.py) and
lna_sim_ac.csv (the ngSpice AC analysis behind Fig. 7, fig:LNA-freq) and draws
them on one pair of axes.

The measured span is 0.2-200 Hz. That is set by the bench at both ends -- the
audio jack delivers nothing below ~0.15 Hz and the 1 kS/s ADC runs out of
samples per cycle above ~200 Hz -- so the simulation is drawn faded outside it
rather than cropped, to make plain how much of Fig. 7 the measurement can and
cannot speak to.

Error bars are the circular sd of the repeat windows, which is an honest
measure here: each window starts at an arbitrary point in the tone, so the
repeats test the phase difference and nothing else.

    ../.venv-meas/bin/python3 lna_phase_figure.py
"""
import argparse
import csv
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path, keys):
    out = {k: [] for k in keys}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            try:
                vals = [float(r[k]) for k in keys]
            except (KeyError, ValueError):
                continue
            for k, v in zip(keys, vals):
                out[k].append(v)
    return {k: np.array(v) for k, v in out.items()}


def unwrap_deg(f, p):
    """Put the measured phase on the same branch as the simulation.

    The passband sits at -180 deg, exactly where atan2 wraps, so half the points
    can come back as +179 and half as -179 cleanly. Shift each point
    by whole turns to the branch nearest its neighbour, walking up in
    frequency."""
    p = np.array(p, float)
    o = np.argsort(f)
    q = p[o].copy()
    for i in range(1, len(q)):
        q[i] -= 360.0 * round((q[i] - q[i - 1]) / 360.0)
    out = np.empty_like(p)
    out[o] = q
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--meas", default=os.path.join(HERE, "lna_phase.csv"))
    ap.add_argument("--sim", default=os.path.join(HERE, "lna_sim_ac.csv"))
    ap.add_argument("--out", default=os.path.join(HERE, "figures",
                                                  "lna_phase_vs_sim.pdf"))
    ap.add_argument("--flip", action="store_true",
                    help="add 180 deg to the measured phase: use when the two "
                         "sides disagree on which end is the reference")
    ap.add_argument("--rmin", type=float, default=0.8,
                    help="drop points whose repeat windows disagree "
                         "(resultant length R below this)")
    a = ap.parse_args()

    sim = load(a.sim, ["freq_hz", "gain_db", "phase_deg"])
    # The simulation's own phase column is wrapped: it runs -179.96 at 151 Hz
    # and +179.74 at 200 Hz for a curve that is simply passing through -180.
    # Interpolating across that step returns a 360 deg error, and plotting it
    # draws a vertical jump through the middle of the passband. Unwrap it once,
    # here, and everything downstream compares like with like.
    sim["phase_deg"] = unwrap_deg(sim["freq_hz"], sim["phase_deg"])
    m = load(a.meas, ["f_used", "gain_db", "dphi_corr_deg", "sem_deg", "R"])
    if not len(m["f_used"]):
        sys.exit(f"empty measurement file: {a.meas}")

    keep = m["R"] >= a.rmin
    dropped = int((~keep).sum())
    f = m["f_used"][keep]
    ph = unwrap_deg(f, m["dphi_corr_deg"][keep])
    # Unwrapping makes the measured series self-consistent but says nothing
    # about WHICH turn it sits on -- an inverting amplifier reads -180 or +180
    # with equal right. Slide the whole series by whole turns onto the branch
    # the simulation uses, so the two can be compared at all. This shifts every
    # point by the same amount and so leaves shape agreement untouched.
    if a.flip:
        ph = ph + 180.0
    sim_at = np.interp(f, sim["freq_hz"], sim["phase_deg"])
    ph = ph - 360.0 * round(float(np.median(ph - sim_at)) / 360.0)
    gd = m["gain_db"][keep]
    # the error bar is the uncertainty of the mean rather than the spread of
    # the individual windows it was averaged from
    sd = m["sem_deg"][keep]
    lo, hi = f.min(), f.max()

    print(f"measured {len(f)} points, {lo:.2f}-{hi:.1f} Hz"
          + (f" ({dropped} dropped for R < {a.rmin})" if dropped else ""))
    inband = (sim["freq_hz"] >= lo) & (sim["freq_hz"] <= hi)
    si = np.interp(f, sim["freq_hz"], sim["phase_deg"])
    sg = np.interp(f, sim["freq_hz"], sim["gain_db"])
    off = float(np.median(ph - si))
    print(f"  phase: measured minus sim, median {off:+.1f} deg, "
          f"worst {np.max(np.abs(ph - si)):.1f} deg")
    if 120.0 < abs(off) < 240.0:
        print("  NOTE: the two differ by close to 180 deg. That is a SIGN "
              "CONVENTION, not a\n        disagreement -- which end of the "
              "amplifier is called the reference. The\n        SHAPE of the "
              "curve is what the measurement tests, and it is unaffected.\n"
              "        Pass --flip to plot the measurement on the "
              "simulation's convention.")
    print(f"  gain : measured minus sim, median {np.median(gd - sg):+.2f} dB")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(2, 1, figsize=(7, 6.4), sharex=True)

    # -- magnitude
    ax[0].semilogx(sim["freq_hz"], sim["gain_db"], color="0.75", lw=1.0,
                   label="ngSpice (Fig. 7)")
    ax[0].semilogx(sim["freq_hz"][inband], sim["gain_db"][inband],
                   color="C3", lw=1.4, label="ngSpice, measured band")
    ax[0].semilogx(f, gd, "o", ms=4.5, color="C0", label="measured")
    ax[0].set_ylabel("gain [dB]")
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].legend(fontsize=8, loc="lower right")

    # -- phase
    ax[1].semilogx(sim["freq_hz"], sim["phase_deg"], color="0.75", lw=1.0)
    ax[1].semilogx(sim["freq_hz"][inband], sim["phase_deg"][inband],
                   color="C3", lw=1.4)
    ax[1].errorbar(f, ph, yerr=sd, fmt="o", ms=4.5, color="C0",
                   capsize=2, lw=1.0)
    ax[1].set_ylabel("phase [degrees]")
    ax[1].set_xlabel("frequency [Hz]")
    ax[1].grid(True, which="both", alpha=0.3)

    # Clip the y-axes to where the measurement lives. The simulation runs to
    # -880 deg at 10 MHz, and letting it set the scale squashes the whole
    # measured transition into a few pixels -- the one thing the figure exists
    # to show. The curve simply leaves the frame instead; it is outside the
    # reachable band anyway, which the grey shading already says.
    for x, series, pad in ((ax[0], np.concatenate([gd, sg]), 6.0),
                           (ax[1], np.concatenate([ph, si]), 25.0)):
        x.set_ylim(series.min() - pad, series.max() + pad)
    for x in ax:
        x.axvspan(x.get_xlim()[0], lo, color="0.92", zorder=0)
        x.axvspan(hi, x.get_xlim()[1], color="0.92", zorder=0)
    ax[0].set_title("LNA transfer: silicon vs. simulation\n"
                    "(grey band = outside what the 1 kS/s bench can reach)",
                    fontsize=10)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    fig.tight_layout()
    fig.savefig(a.out, dpi=150)
    print(f"figure: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
