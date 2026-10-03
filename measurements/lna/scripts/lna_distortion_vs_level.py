#!/usr/bin/env python3
"""Is the LNA's 1.7% second harmonic the chip, or the sound card?

Probe on the LNA OUTPUT. Hold the frequency fixed and step the drive down,
then read h2 at each level. The two candidate causes predict opposite things:

  amplifier headroom  ->  h2 falls roughly IN PROPORTION to amplitude.
      The output sits at 1.37 V DC with only ~70 mV to the 1.78 V rail while
      the bottom has 1.03 V of room. That asymmetry compresses the positive
      half and nothing else, which is what makes an even harmonic. Back the
      drive off and the peak leaves the rail, so the mechanism switches off.

  sound card         ->  h2 stays CONSTANT as a ratio.
      A distorting source hands the same fractional distortion to the
      amplifier whatever the level, and the amplifier passes it through.

Only levels at or BELOW the sweep's 0.25 Vpp are used: at 0.5 Vpp the output
would need 1368 mVpp about 1.37 V, i.e. a 2.05 V peak against a 1.78 V rail --
that is hard clipping, and it would answer a different question.

Windows are long because the point of interest is small: at the lowest level
h2 is ~1.5 mV against ~19.5 mV of node noise, so it needs ~30 s of coherent
averaging to land within 10%.

Read-only on the chip -- no FTDI, no DAC writes. Biases stay as loaded.

  ../.venv-meas/bin/python3 lna_distortion_vs_level.py
"""

import argparse
import csv
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_audio_sweep import (Scope, AudioOut, make_wav, longest_contiguous,
                             sine_fit, decommensurate, VDD)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--freq", type=float, default=88.57,
                    help="fixed test frequency (decommensurate with 1 kS/s)")
    ap.add_argument("--levels", default="0.25,0.177,0.125,0.088,0.0625",
                    help="jack Vpp levels, high to low; must not exceed 0.25")
    ap.add_argument("--vin-at-025", type=float, default=0.007,
                    help="chip input Vpp when the jack is at 0.25 Vpp")
    ap.add_argument("--window", type=float, default=30.0)
    ap.add_argument("--settle", type=float, default=3.0)
    ap.add_argument("--trim", type=float, default=1.0)
    ap.add_argument("--out", default="lna_distortion_vs_level.csv")
    ap.add_argument("--png", default="figures/lna_distortion_vs_level.png")
    args = ap.parse_args()

    f0 = decommensurate(args.freq)
    levels = [float(x) for x in args.levels.split(",")]
    if max(levels) > 0.2500001:
        sys.exit("levels above 0.25 Vpp would drive the output into the rail")

    wavdir = "wavs_dist"
    os.makedirs(wavdir, exist_ok=True)
    print(f"probe must be on the LNA OUTPUT.  f = {f0:g} Hz, "
          f"{len(levels)} levels, ~{len(levels)*(args.settle+args.window+args.trim)/60:.1f} min\n")

    scope = Scope()
    audio = AudioOut()
    rows = []
    try:
        for lvl in levels:
            wav = os.path.join(wavdir, f"d_{f0:.2f}hz_{lvl:g}vpp.wav")
            if not os.path.exists(wav):
                make_wav(wav, f0, lvl, min_dur=args.settle + args.window + args.trim + 3)
            audio.play(wav)
            scope.drain(args.settle)
            # a stream hiccup can leave longest_contiguous() with fewer samples
            # than the trim discards; retry rather than crash on an empty array
            n = int(args.trim / 0.001)
            t = v = None
            for attempt in range(4):
                tt, vv = longest_contiguous(*scope.collect(args.window + args.trim))
                if len(vv) > n + 2000:
                    t, v = tt[n:], vv[n:]
                    break
                print(f"    short segment ({len(vv)} samples), retrying "
                      f"[{attempt+1}/4]")
            if v is None:
                print("    giving up on this level")
                continue
            r = sine_fit(t, v, f0)
            vin = args.vin_at_025 * lvl / 0.25
            se = r["resid_rms"] * math.sqrt(2.0 / r["n"])
            h2_amp = r["h2"] * r["amp"]
            peak = r["dc"] + r["amp"]
            rows.append((lvl, vin, r["vpp"], r["amp"], r["dc"], peak,
                         VDD - peak, r["h2"], r["h3"], h2_amp, se, r["n"]))
            print(f"  jack {lvl:6.4f} Vpp (chip {vin*1e3:5.2f} mVpp): "
                  f"out {r['vpp']*1e3:7.1f} mVpp  peak {peak:.3f} V  "
                  f"headroom {(VDD-peak)*1e3:5.0f} mV  "
                  f"h2 {r['h2']:.4f} ({h2_amp*1e3:5.2f} mV +/-{se*1e3:.2f})  h3 {r['h3']:.4f}")
    except KeyboardInterrupt:
        print("\ninterrupted; keeping what we have")
    finally:
        audio.stop()
        scope.close()

    if not rows:
        return 1
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["jack_vpp", "vin_pp", "vout_pp", "amp_v", "dc_v", "peak_v",
                    "headroom_v", "h2", "h3", "h2_amp_v", "amp_se_v", "n"])
        w.writerows([[f"{x:.6g}" if isinstance(x, float) else x for x in r] for r in rows])

    a = np.array([r[3] for r in rows])
    h2 = np.array([r[7] for r in rows])
    # a repeated level may be present as a consistency guard, so order by
    # amplitude rather than by row for the headline ratio
    hi, lo = int(np.argmax(a)), int(np.argmin(a))
    dup = [i for i, r in enumerate(rows) if abs(r[0] - rows[0][0]) < 1e-9]
    if len(dup) > 1:
        g = [rows[i][2] / rows[i][1] for i in dup]
        print(f"\nrepeat guard: same drive measured {len(dup)}x -> gain "
              + ", ".join(f"{x:.1f}x" for x in g)
              + f"   spread {100*(max(g)-min(g))/np.mean(g):.1f}%")
        if 100 * (max(g) - min(g)) / np.mean(g) > 10:
            print("  *** THE TWO REPEATS DISAGREE -- the bench moved during the run; "
                  "do not trust this data ***")
    print("\n--- verdict ---")
    print(f"amplitude fell {a[hi]/a[lo]:.2f}x;  h2 changed {h2[hi]/h2[lo]:.2f}x")
    print("  h2 ratio ~= amplitude ratio  -> AMPLIFIER headroom")
    print("  h2 ratio ~= 1.0              -> SOUND CARD")
    # slope of log h2 vs log amplitude: 1 = proportional, 0 = constant
    good = (h2 > 0) & (a > 0)
    if good.sum() >= 3:
        k = np.polyfit(np.log(a[good]), np.log(h2[good]), 1)[0]
        print(f"\n  fitted slope d(log h2)/d(log A) = {k:+.2f}")
        print(f"  ({'amplifier' if k > 0.5 else 'sound card' if abs(k) < 0.3 else 'mixed/unclear'})")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        ax[0].loglog(a * 1e3, h2 * 100, "o-", ms=6)
        ax[0].loglog(a * 1e3, h2[0] * 100 * (a / a[0]), "--", c="C2",
                     label="if amplifier headroom (h2 $\\propto$ A)")
        ax[0].axhline(h2[0] * 100, ls=":", c="C3", label="if sound card (h2 constant)")
        ax[0].set_xlabel("output amplitude [mV]"); ax[0].set_ylabel("2nd harmonic [%]")
        ax[0].grid(True, which="both", alpha=.3); ax[0].legend(fontsize=8)
        ax[0].set_title(f"distortion vs drive, {f0:g} Hz")
        hd = np.array([r[6] for r in rows])
        ax[1].plot(hd * 1e3, h2 * 100, "o-", ms=6)
        ax[1].set_xlabel("headroom to the 1.78 V rail [mV]"); ax[1].set_ylabel("2nd harmonic [%]")
        ax[1].grid(alpha=.3); ax[1].set_title("distortion vs headroom")
        fig.tight_layout(); fig.savefig(args.png, dpi=150)
        print(f"\nplot: {args.png}")
    except Exception as e:
        print(f"plot skipped: {e}")
    print(f"data: {args.out}")


if __name__ == "__main__":
    sys.exit(main())
