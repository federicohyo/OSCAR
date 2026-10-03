#!/usr/bin/env python3
"""Input-referred noise of the LNA, measured on silicon.

Probe on the LNA OUTPUT, no drive playing. Record the output for a long
stretch, take its power spectral density, and divide by the measured gain at
each frequency to refer the noise back to the input:

    S_in(f) = S_out(f) / G(f)^2

The gain curve comes from `lna_transfer_final.csv` (the sweep with the audio
path divided out), interpolated in log-log. Referring the noise to the input
is only meaningful where the gain is actually known -- below ~0.2 Hz the drive
delivered nothing and there is no measured gain, so nothing is reported there.

What the measurement can and cannot separate:

  * the ADC's own noise is NOT a limit here. On a passive node it contributes
    ~0.70 mV rms against the LNA output's ~19.5 mV rms -- 0.13% of the power,
    so what we record is the amplifier, not the instrument. (Quantisation
    alone is 0.805 mV / sqrt(12) = 0.23 mV rms.)

  * MAINS HUM IS NOT AMPLIFIER NOISE. 50/60 Hz and their harmonics are pickup
    from the room, and they dominate the total rms. They are reported
    separately and excluded from the broadband figure, because quoting them as
    the LNA's noise would be wrong by a wide margin.

  * the amplifier's slow settling (~40 s, seen in the drift test) lands in the
    lowest bins. Below ~0.05 Hz the "noise" is really that drift.

Comparison target: the ISCAS27 draft quotes a SPICE noise peak of
200 uV/sqrt(Hz) at ~1 Hz (`IEEEConf.tex`, sec. Low-Noise Amplifier).

Read-only on the chip -- no FTDI, no DAC writes.

  ../.venv-meas/bin/python3 lna_input_referred_noise.py --seconds 180
"""

import argparse
import csv
import math
import os
import subprocess
import sys

import numpy as np

_trapz = getattr(np, "trapezoid", None) or np.trapz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_audio_sweep import Scope, longest_contiguous, BOARD_DT

FS = 1.0 / BOARD_DT


def load_gain(path):
    f, g = [], []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            f.append(float(r["freq_hz"]))
            g.append(float(r["gain"]))
    f, g = np.array(f), np.array(g)
    o = np.argsort(f)
    return f[o], g[o]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seconds", type=float, default=180.0)
    ap.add_argument("--gain-csv", default="lna_transfer_final.csv")
    ap.add_argument("--nperseg", type=int, default=32768)
    ap.add_argument("--mains", type=float, default=60.0)
    ap.add_argument("--out", default="lna_noise.csv")
    ap.add_argument("--png", default="figures/lna_noise.png")
    args = ap.parse_args()

    subprocess.run(["pkill", "-f", "[p]w-play"], capture_output=True)
    gf, gg = load_gain(args.gain_csv)
    print(f"gain curve: {len(gf)} points, {gf.min():.2f}-{gf.max():.1f} Hz, "
          f"passband {np.median(gg[(gf>=4)&(gf<=280)]):.1f}x")
    print(f"recording {args.seconds:.0f} s of LNA output with NO drive...\n")

    sc = Scope()
    sc.drain(2.0)
    t, v = longest_contiguous(*sc.collect(args.seconds))
    sc.close()
    print(f"got {len(v)} samples, {(t[-1]-t[0]):.1f} s, DC {v.mean():.4f} V, "
          f"rms about the mean {v.std()*1e3:.2f} mV")

    from scipy.signal import welch
    nps = min(args.nperseg, len(v) // 4)
    fr, pxx = welch(v - v.mean(), fs=FS, nperseg=nps, noverlap=nps // 2,
                    window="hann", detrend="linear")
    asd_out = np.sqrt(pxx)                        # V/sqrt(Hz) at the output
    print(f"PSD: nperseg={nps} -> {FS/nps:.4f} Hz resolution, "
          f"{len(v)//(nps//2)-1} averages")

    # mains lines are pickup, not amplifier noise -- flag and exclude them
    line = np.zeros_like(fr, bool)
    for h in range(1, int(FS / 2 / args.mains) + 1):
        line |= np.abs(fr - h * args.mains) < max(0.5, 3 * FS / nps)
    for h in range(1, int(FS / 2 / 50.0) + 1):     # 50 Hz too, in case
        line |= np.abs(fr - h * 50.0) < max(0.5, 3 * FS / nps)

    gain_at = lambda f: np.exp(np.interp(np.log(f), np.log(gf), np.log(gg)))
    band = (fr >= gf.min()) & (fr <= gf.max()) & (fr > 0)
    asd_in = np.full_like(asd_out, np.nan)
    asd_in[band] = asd_out[band] / gain_at(fr[band])

    print("\n  freq      out ASD      gain     input-referred ASD")
    for probe in (0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 100.0, 300.0):
        if not (gf.min() <= probe <= gf.max()):
            continue
        i = np.argmin(np.abs(fr - probe))
        tag = "  <- mains" if line[i] else ""
        print(f"  {fr[i]:7.3f} Hz  {asd_out[i]*1e6:9.1f} uV/sqrt(Hz)  "
              f"{gain_at(fr[i]):6.1f}x  {asd_in[i]*1e6:8.3f} uV/sqrt(Hz){tag}")

    ok = band & ~line & np.isfinite(asd_in)
    for lo, hi in ((0.2, 1.0), (1.0, 10.0), (10.0, 100.0), (0.2, 300.0)):
        m = ok & (fr >= lo) & (fr <= hi)
        if m.sum() < 2:
            continue
        rms_in = math.sqrt(_trapz(asd_in[m] ** 2, fr[m]))
        rms_out = math.sqrt(_trapz(asd_out[m] ** 2, fr[m]))
        print(f"  integrated {lo:5.1f}-{hi:5.1f} Hz (mains excluded): "
              f"out {rms_out*1e3:7.3f} mV rms   input-referred {rms_in*1e6:8.2f} uV rms")

    m = ok & (fr >= 0.2) & (fr <= 300)
    print(f"\ntotal rms about the mean (everything, incl. mains): {v.std()*1e3:.2f} mV out"
          f"  ~= {v.std()/np.median(gg[(gf>=4)&(gf<=280)])*1e6:.0f} uV in")
    mm = band & line
    if mm.sum():
        print(f"mains lines alone contribute "
              f"{math.sqrt(_trapz(asd_out[mm]**2, fr[mm]))*1e3:.2f} mV rms at the output "
              f"-- that is room pickup, not the amplifier")

    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["freq_hz", "asd_out_v_rthz", "gain", "asd_in_v_rthz", "is_mains_line"])
        for i in np.flatnonzero(band):
            w.writerow([f"{fr[i]:.5f}", f"{asd_out[i]:.6e}", f"{gain_at(fr[i]):.3f}",
                        f"{asd_in[i]:.6e}", int(line[i])])
    print(f"\ndata: {args.out}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 1, figsize=(9, 8))
        ax[0].loglog(fr[band], asd_out[band] * 1e6, lw=.8, color="0.5")
        ax[0].set_ylabel("output noise [$\\mu$V/$\\sqrt{Hz}$]")
        ax[0].grid(True, which="both", alpha=.3); ax[0].set_title("LNA output noise, no drive")
        b2 = band & ~line
        ax[1].loglog(fr[b2], asd_in[b2] * 1e6, lw=.9, color="C0", label="measured (mains removed)")
        ax[1].axhline(200, ls="--", c="C3", lw=1.2, label="SPICE 200 $\\mu$V/$\\sqrt{Hz}$ @1 Hz (ISCAS27)")
        ax[1].set_xlabel("frequency [Hz]"); ax[1].set_ylabel("input-referred [$\\mu$V/$\\sqrt{Hz}$]")
        ax[1].grid(True, which="both", alpha=.3); ax[1].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(args.png, dpi=150)
        print(f"plot: {args.png}")
    except Exception as e:
        print(f"plot skipped: {e}")


if __name__ == "__main__":
    sys.exit(main())
