#!/usr/bin/env python3
"""Regenerate every LNA figure from the saved CSVs. No bench, no chip.

    ../.venv-meas/bin/python3 make_lna_figures.py

Rebuilds, in order:
  lna_transfer_final.csv + figures/lna_transfer_final.png   (the headline)
  figures/lna_gain_vs_level.png   gain vs input amplitude, 400 uV .. 7 mV
  figures/lna_settling.png        the ~40 s settling that invalidated two runs
  figures/lna_noise.png           input-referred noise vs the SPICE prediction
  figures/lna_transfer_out.png    the raw sweep (amp + sound card)
  figures/lna_transfer_ref.png    the sound card's own response
  figures/lna_distortion_vs_level.png, figures/lna_gain_400uv.png

Inputs (all committed alongside):
  lna_transfer_out.csv        LNA output vs frequency, 7 mVpp in
  lna_transfer_ref.csv        the drive itself, probe on the jack, 1 Vpp
  lna_gain_vs_level_ALL.csv   every gain-vs-amplitude point, valid + discarded
  lna_settling.csv            output DC and gain vs time after a drive change
  lna_noise.csv               output noise ASD, gain, input-referred, mains flag

The correction applied in step 1 is the one judgement call in the whole chain,
so it is spelled out rather than buried:

  * below 0.2 Hz the jack delivers nothing measurable (0.00 mVpp at 0.1 Hz),
    so those points are DROPPED rather than reported as a number.
  * above 130 Hz the reference's own clipped-fit degrades as samples/cycle
    falls under ~8 (0.98 of plateau at 129 Hz -> 0.49 at 400 Hz). An audio
    output cannot roll off at 200 Hz, so the drive is taken as FLAT there and
    the reference's plateau is used instead of its measured value.
  * the 100.000 Hz anchor row of the out-sweep is dropped: at exactly 10
    samples/cycle the sampling phase freezes (11 distinct phases) and that
    point scattered +/-0.8 dB where its neighbours held +/-0.07 dB.
"""

import csv
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
VIN0 = 0.007          # bench-measured chip input at the 100 Hz anchor
RAIL = 1.78


def rd(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(f))


# ------------------------------------------------- 1. corrected transfer
def transfer():
    out = rd("lna_transfer_out.csv")
    ref = {round(float(r["freq_hz"]), 4): r for r in rd("lna_transfer_ref.csv")}
    rk = np.array(sorted(ref))
    rv = np.array([float(ref[k]["vpp_out"]) for k in rk])
    plateau = np.median(rv[(rk >= 5) & (rk <= 130)])
    ok = rv > 0

    def ref_at(f):
        if f > 130.0:
            return plateau
        return float(np.exp(np.interp(math.log(f), np.log(rk[ok]), np.log(rv[ok]))))

    rows = []
    for r in out:
        f = float(r["freq_hz"])
        if abs(f - 100.0) < 1e-9 or f < 0.2:
            continue
        drive_frac = ref_at(f) / plateau
        vin = drive_frac * VIN0
        vo = float(r["vpp_out"])
        g = vo / vin
        weak = drive_frac < 0.8          # the jack, not the amplifier
        rows.append((f, vo, vin, g, 20 * math.log10(g), weak))

    with open(os.path.join(HERE, "lna_transfer_final.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["freq_hz", "vpp_out", "vpp_in", "gain", "gain_db", "low_snr"])
        for r in rows:
            w.writerow([f"{r[0]:.4f}", f"{r[1]:.6f}", f"{r[2]:.6f}",
                        f"{r[3]:.3f}", f"{r[4]:.3f}", int(r[5])])

    f = np.array([r[0] for r in rows]); g = np.array([r[4] for r in rows])
    bad = np.array([bool(r[5]) for r in rows])
    lead = np.flatnonzero(~bad)[0] if (~bad).any() else len(f)   # leading weak-drive run
    pb = (f >= 4) & (f <= 280); G = g[pb].mean()
    lo = f[(f < 4) & (g < G - 3)]
    i = np.searchsorted(f, lo.max())
    fc = 10 ** (math.log10(f[i-1]) + (G - 3 - g[i-1]) / (g[i] - g[i-1]) *
                (math.log10(f[i]) - math.log10(f[i-1])))

    fig, ax = plt.subplots(figsize=(8, 5))
    # ONE line, no shading. The uncorrected trace lives in
    # figures/lna_transfer_out.png. The points below ~1 Hz carry roughly
    # +/-1 dB rather than +/-0.1 dB because the jack was barely driving there;
    # that is recorded in the low_snr column of lna_transfer_final.csv and
    # belongs in the caption, not on the axes.
    ax.semilogx(f, g, "o-", ms=5, lw=1.6, color="C0")
    ax.axhline(G, ls="--", c="0.55", lw=1)
    ax.axhline(G - 3, ls=":", c="0.55", lw=1)
    ax.axvline(fc, ls=":", c="C3", lw=1.2)
    ax.text(fc * 1.15, g.min() + 0.5, f"$-3$ dB\n{fc:.2f} Hz", color="C3", fontsize=9)
    ax.text(6, G - 1.1, f"{G:.1f} dB  ({10**(G/20):.0f}$\\times$)", color="0.25", fontsize=10)
    ax.set_ylim(min(g) - 1.5, G + 1.5)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("gain [dB]")
    ax.grid(True, which="both", alpha=.3)
    ax.set_title("LNA measured transfer function")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"lna_transfer_final.{ext}"), dpi=150)
    plt.close(fig)
    print(f"transfer: passband {G:.2f} dB ({10**(G/20):.1f}x) +/-{g[pb].std():.2f}, "
          f"-3 dB at {fc:.2f} Hz  -> lna_transfer_final.csv/.png")


# ------------------------------------------------- 2. gain vs amplitude
def gain_vs_level():
    rows = [r for r in rd("lna_gain_vs_level_ALL.csv") if int(r["valid"])]
    vin = np.array([float(r["vin_pp"]) for r in rows])
    gain = np.array([float(r["gain"]) for r in rows])
    u = np.unique(vin)
    mean = np.array([gain[vin == x].mean() for x in u])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    ax[0].semilogx(vin * 1e3, gain, "o", ms=6, alpha=.6, label="individual runs")
    ax[0].semilogx(u * 1e3, mean, "-", lw=1.5, color="C3", label="mean")
    ax[0].axhline(mean.mean(), ls=":", c="0.5")
    ax[0].set_xlabel("input amplitude [mVpp]"); ax[0].set_ylabel("gain [x]")
    ax[0].set_ylim(0, max(gain) * 1.25); ax[0].grid(True, which="both", alpha=.3)
    ax[0].legend(fontsize=8); ax[0].set_title("gain vs input amplitude, 88.57 Hz")
    ax[1].loglog(vin * 1e3, vin * gain * 1e3, "o-", ms=6)
    ax[1].set_xlabel("input amplitude [mVpp]"); ax[1].set_ylabel("output [mVpp]")
    ax[1].grid(True, which="both", alpha=.3); ax[1].set_title("output vs input (linearity)")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"lna_gain_vs_level.{ext}"), dpi=150)
    print(f"gain vs level: {len(rows)} valid points, {vin.min()*1e3:.3f}-{vin.max()*1e3:.2f} mVpp, "
          f"gain {gain.min():.1f}-{gain.max():.1f}x  -> lna_gain_vs_level.png")


# ------------------------------------------------- 3. settling
def settling():
    rows = rd("lna_settling.csv")
    t = np.array([float(r["t_s"]) for r in rows])
    g = np.array([float(r["gain"]) for r in rows])
    dc = np.array([float(r["dc_v"]) for r in rows])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t, g, "o-", ms=5, color="C0"); ax.set_xlabel("time after drive change [s]")
    ax.set_ylabel("gain [x]", color="C0"); ax.tick_params(axis="y", labelcolor="C0")
    ax.axvline(40, ls=":", c="C3"); ax.text(42, g.min() + .5, "settled (~40 s)", color="C3", fontsize=9)
    a2 = ax.twinx(); a2.plot(t, dc, "s--", ms=4, color="C2")
    a2.set_ylabel("output DC [V]", color="C2"); a2.tick_params(axis="y", labelcolor="C2")
    ax.grid(alpha=.3); ax.set_title("LNA settling after a drive change (fixed 3.5 mVpp in)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "lna_settling.png"), dpi=150)
    print(f"settling: {g[0]:.1f}x at t={t[0]:.0f}s -> {g[-1]:.1f}x settled; "
          f"DC {dc[0]:.3f}->{dc[-1]:.3f} V  -> lna_settling.png")


# ------------------------------------------------- 4. noise
def noise():
    rows = rd("lna_noise.csv")
    f = np.array([float(r["freq_hz"]) for r in rows])
    ao = np.array([float(r["asd_out_v_rthz"]) for r in rows])
    ai = np.array([float(r["asd_in_v_rthz"]) for r in rows])
    ln = np.array([int(r["is_mains_line"]) for r in rows], bool)
    fig, ax = plt.subplots(2, 1, figsize=(9, 8))
    ax[0].loglog(f, ao * 1e6, lw=.8, color="0.5")
    ax[0].set_ylabel("output noise [$\\mu$V/$\\sqrt{Hz}$]")
    ax[0].grid(True, which="both", alpha=.3); ax[0].set_title("LNA output noise, no drive")
    ax[1].loglog(f[~ln], ai[~ln] * 1e6, lw=.9, color="C0", label="measured (mains removed)")
    ax[1].axhline(200, ls="--", c="C3", lw=1.2,
                  label="SPICE 200 $\\mu$V/$\\sqrt{Hz}$ @1 Hz (reference)")
    ax[1].set_xlabel("frequency [Hz]")
    ax[1].set_ylabel("input-referred [$\\mu$V/$\\sqrt{Hz}$]")
    ax[1].grid(True, which="both", alpha=.3); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "lna_noise.png"), dpi=150)
    plt.close(fig)

    # reference version: input-referred only, single panel
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.loglog(f[~ln], ai[~ln] * 1e6, lw=1.1, color="C0")
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("input-referred noise [$\\mu$V/$\\sqrt{\\mathrm{Hz}}$]")
    ax.grid(True, which="both", alpha=.3)
    ax.set_title("Measured input-referred noise")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIG, f"lna_noise_input_referred.{ext}"), dpi=150)
    plt.close(fig)
    i1 = np.argmin(np.abs(f - 1.0))
    i30 = np.argmin(np.abs(f - 30.0))
    print(f"noise: {ai[i1]*1e6:.1f} uV/sqrt(Hz) at 1 Hz, {ai[i30]*1e6:.1f} at 30 Hz "
          f"-> lna_noise.png + lna_noise_input_referred.png/.pdf")


# ------------------------------------------------- 5. supporting figures
def supporting():
    """The raw sweep, the drive, and the distortion/level runs.

    These are evidence rather than results, but they must regenerate too --
    otherwise a `rm -rf figures/` loses them, which is exactly what happened
    once already."""
    for csvname, title, ylab, xcol, ycol in (
            ("lna_transfer_out.csv", "LNA output vs frequency (uncorrected, 7 mVpp in)",
             "gain [dB]", "freq_hz", "gain_db"),
            ("lna_transfer_ref.csv", "the drive itself: audio jack at 1 Vpp",
             "measured drive [dB re 7 mVpp]", "freq_hz", "gain_db")):
        rows = rd(csvname)
        x = np.array([float(r[xcol]) for r in rows])
        y = np.array([float(r[ycol]) for r in rows])
        m = np.isfinite(x) & np.isfinite(y) & (x > 0)
        o = np.argsort(x[m])
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.semilogx(x[m][o], y[m][o], "o-", ms=4)
        ax.set_xlabel("frequency [Hz]"); ax.set_ylabel(ylab)
        ax.grid(True, which="both", alpha=.3); ax.set_title(title)
        fig.tight_layout()
        out = os.path.join(FIG, os.path.splitext(csvname)[0] + ".png")
        fig.savefig(out, dpi=150); plt.close(fig)
        print(f"supporting: {os.path.basename(out)}")

    for csvname, title in (("lna_distortion_vs_level.csv", "h2/h3 and headroom vs drive"),
                           ("lna_gain_400uv.csv", "the 400 uVpp point (with repeat guard)")):
        rows = rd(csvname)
        a = np.array([float(r["amp_v"]) for r in rows])
        h2 = np.array([float(r["h2"]) for r in rows])
        hd = np.array([float(r["headroom_v"]) for r in rows])
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        ax[0].loglog(a * 1e3, h2 * 100, "o-", ms=6)
        ax[0].set_xlabel("output amplitude [mV]"); ax[0].set_ylabel("2nd harmonic [%]")
        ax[0].grid(True, which="both", alpha=.3); ax[0].set_title(title)
        ax[1].plot(hd * 1e3, h2 * 100, "o-", ms=6)
        ax[1].set_xlabel("headroom to the 1.78 V rail [mV]"); ax[1].set_ylabel("2nd harmonic [%]")
        ax[1].grid(alpha=.3); ax[1].set_title("distortion vs headroom")
        fig.tight_layout()
        out = os.path.join(FIG, os.path.splitext(csvname)[0] + ".png")
        fig.savefig(out, dpi=150); plt.close(fig)
        print(f"supporting: {os.path.basename(out)}")


if __name__ == "__main__":
    transfer(); gain_vs_level(); settling(); noise(); supporting()
    # the sim-vs-silicon comparison rebuilds from lna_sim_ac.csv (saved ngspice
    # output); pass --run-spice to that script to regenerate the simulation
    import subprocess
    subprocess.run([sys.executable, os.path.join(HERE, "lna_sim_vs_meas.py")], check=False)
    print("\nall figures regenerated from CSV only -- no bench needed.")
