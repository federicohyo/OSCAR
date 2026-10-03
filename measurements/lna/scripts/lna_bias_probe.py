#!/usr/bin/env python3
"""Gain vs lna_iref: does more OTA current buy back the missing 10 dB?

    ./.venv-meas/bin/python3 LNA/lna_iref_gain_sweep.py

lna_iref sets the gate of the input-pair current mirror (PMOS: lower voltage =
more current). More current raises the OTA's transconductance and therefore its
open-loop gain, which pushes the closed-loop gain closer to the ideal C1/C2.

This is a test of the explanation in the draft, not just a tuning knob:

  * if the gain climbs toward C1/C2 = 369x (51.4 dB), the measured shortfall was
    INSUFFICIENT LOOP GAIN and is recoverable by biasing -- the parasitic-C2
    story in README_MEASUREMENTS.md would then be wrong and must be rewritten.
  * if the gain saturates well below 369x however much current is supplied, the
    ratio itself is what limits, and the parasitic explanation stands.

Method notes:
  * ONE continuous tone plays for the whole sweep. Only the bias changes, so the
    ~40 s output-DC settling that follows a *drive* change does not apply; each
    point still gets --settle seconds for the bias itself to take effect.
  * the test amplitude is deliberately small (0.875 mVpp), because at 369x a
    3.5 mVpp input would demand 1.3 Vpp out and rail. Small enough that even the
    best case stays linear, large enough for the coherent fit.
  * the first bias value is measured again at the end as a repeat guard.
"""

import argparse
import csv
import math
import os
import signal
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from lna_audio_sweep import Scope, longest_contiguous, sine_fit, make_wav
from meas_common import BridgeSession

FREQ = 88.57
TEST_VPP = 0.000875              # at the chip, via the divider
JACK_VPP = 0.25 * TEST_VPP / 0.007
C1_OVER_C2 = (132 * 70) / (5 * 5)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bias", default="lna_iref", help="which bias channel to sweep")
    ap.add_argument("--values", default="1.079,0.98,0.88,0.78,0.68,0.58,0.48,1.079",
                    help="volts, in order; last repeats the first as a guard")
    ap.add_argument("--settle", type=float, default=35.0)
    ap.add_argument("--window", type=float, default=8.0)
    ap.add_argument("--out", default=os.path.join(HERE, "lna_bias_probe.csv"))
    args = ap.parse_args()

    vals = [float(x) for x in args.values.split(",")]
    wav = os.path.join(HERE, "wavs_dist", f"iref_{FREQ:.2f}hz.wav")
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    if not os.path.exists(wav):
        make_wav(wav, FREQ, JACK_VPP, min_dur=30.0)

    print(f"tone {FREQ} Hz, {TEST_VPP*1e3:.3f} mVpp at the chip (jack {JACK_VPP:.4f} Vpp)")
    print(f"{len(vals)} bias points, ~{len(vals)*(args.settle+args.window)/60:.1f} min")
    print(f"ideal C1/C2 = {C1_OVER_C2:.1f}x ({20*math.log10(C1_OVER_C2):.2f} dB)\n")

    player = subprocess.Popen(["bash", "-c", 'while :; do pw-play -- "$1"; done', "_", wav],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              start_new_session=True)
    rows = []
    scope = None
    try:
        with BridgeSession() as br:
            scope = Scope()
            for i, v in enumerate(vals):
                br.bias(args.bias, v)
                time.sleep(args.settle)
                scope.drain(0.5)
                t, y = longest_contiguous(*scope.collect(args.window))
                r = sine_fit(t, y, FREQ)
                gain = r["vpp"] / TEST_VPP
                se = r["resid_rms"] * math.sqrt(2.0 / r["n"])
                peak, trough = r["dc"] + r["amp"], r["dc"] - r["amp"]
                flag = "NEAR-RAIL" if (peak > 1.78 - 0.03 or trough < 0.03) else ""
                rows.append((v, r["vpp"], gain, 20 * math.log10(gain) if gain > 0 else float("nan"),
                             r["dc"], peak, r["h2"], se, flag))
                print(f"  {args.bias} {v:5.3f} V -> {r['vpp']*1e3:8.2f} mVpp  gain {gain:7.1f}x "
                      f"({20*math.log10(gain):5.2f} dB)  DC {r['dc']:.3f}  peak {peak:.3f}  "
                      f"h2 {r['h2']:.3f} {flag}")
    except KeyboardInterrupt:
        print("\ninterrupted")
    finally:
        try:
            os.killpg(os.getpgid(player.pid), signal.SIGTERM)
        except Exception:
            pass
        if scope is not None:
            scope.close()

    if not rows:
        return 1
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bias_v", "vout_pp", "gain", "gain_db", "dc_v", "peak_v",
                    "h2", "amp_se_v", "flag"])
        for r in rows:
            w.writerow([f"{r[0]:.4f}", f"{r[1]:.6f}", f"{r[2]:.2f}", f"{r[3]:.3f}",
                        f"{r[4]:.4f}", f"{r[5]:.4f}", f"{r[6]:.4f}", f"{r[7]:.6f}", r[8]])

    same = [r for r in rows if abs(r[0] - rows[0][0]) < 1e-9]
    if len(same) > 1:
        g = [r[2] for r in same]
        spread = 100 * (max(g) - min(g)) / float(np.mean(g))
        print(f"\nrepeat guard: {', '.join(f'{x:.1f}x' for x in g)}  spread {spread:.1f}%")
        if spread > 10:
            print("  *** repeats disagree -- do not trust this sweep ***")

    best = max(rows, key=lambda r: r[2])
    print(f"\nbest: {args.bias} {best[0]:.3f} V -> {best[2]:.1f}x ({best[3]:.2f} dB)")
    print(f"      that is {100*best[2]/C1_OVER_C2:.1f}% of the ideal C1/C2 ratio")
    print("\nVERDICT: ", end="")
    if best[2] > 0.75 * C1_OVER_C2:
        print("gain recovers toward C1/C2 -- the shortfall was LOOP GAIN,\n"
              "         and the parasitic-C2 explanation in the draft must be rewritten.")
    elif best[2] > 1.3 * rows[0][2]:
        print("gain improves substantially but stays well below C1/C2 --\n"
              "         partly loop gain, partly the ratio. Both belong in the draft.")
    else:
        print("more current buys little -- the capacitor ratio is what limits,\n"
              "         so the parasitic-C2 explanation stands.")
    print(f"\ndata: {os.path.basename(args.out)}")


if __name__ == "__main__":
    sys.exit(main())
