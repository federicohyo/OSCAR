#!/usr/bin/env python3
"""Gain vs frequency, 0.2 Hz .. 400 Hz, clean setup.

Drive is held at a constant small amplitude so the amplifier stays linear across
the whole band at the new ~290x operating point.

Frequencies are deliberately irrational-looking: a round frequency lands a whole
number of samples per cycle on the 1 kS/s grid and freezes the sampling phase,
which biases the fit (README_MEASUREMENTS.md, trap 2).

The window grows at low frequency -- a coherent fit needs several whole cycles,
and below ~1 Hz an 8 s window does not contain one.

NOTE ON THE DRIVE CORRECTION: the audio jack is AC-coupled with a ~0.93 Hz
corner, so the raw curve below ~20 Hz is the sound card, not the amplifier.
Correcting it needs a reference pass with a probe on the divider output -- which
is exactly the instrument whose earth caused this afternoon's ground loop. So
this block measures the RAW chain and the correction reuses the previous
campaign's `lna_transfer_ref.csv` shape. See ../README.md for that assumption.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_meas import Session, guard, DIVIDER

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
VIN, SETTLE = 0.00050, 60.0        # 0.5 mVpp at the chip

FREQS = [0.2125, 0.3099, 0.4518, 0.6586, 0.9602, 1.3999, 2.0410, 2.9757,
         4.3383, 6.3247, 9.2231, 13.4467, 19.6053, 28.5843, 41.6733,
         60.7563, 88.5700, 129.1379, 188.2637, 274.4491, 400.1237]

def window_for(f):
    return min(60.0, max(8.0, 6.0 / f))

with Session(ROOT, "transfer") as s:
    s.point("quiet_before", 88.57, 0.0, settle=20.0, window=8.0, note="no drive")
    rows = []
    order = FREQS + [FREQS[0]]           # repeat the first frequency as the guard
    for i, f in enumerate(order):
        jack = VIN / DIVIDER
        w = window_for(f)
        tag = f"F{i:02d}_{f:.4f}Hz" + ("_guard" if i == len(order)-1 else "")
        r, row = s.point(tag, f, jack, settle=SETTLE, window=w)
        rows.append(row)
        print(f"  {f:9.4f} Hz  win {w:4.1f}s -> out {r['vpp']*1e3:8.2f} mVpp  "
              f"gain {float(row['gain']):7.1f}x ({row['gain_db']:>7} dB)  DC {row['dc_v']}  "
              f"h2 {row['h2']}  +-{float(row['amp_se_v'])*1e3:.2f}mV  "
              f"rail {float(row['frac_at_rail'])*100:.1f}%  {row['flag']}", flush=True)
    s.point("quiet_after", 88.57, 0.0, settle=20.0, window=8.0, note="no drive")

ok, spread = guard(rows)
print(f"\nrepeat guard at {FREQS[0]} Hz: {rows[0]['gain']}x vs {rows[-1]['gain']}x  "
      f"spread {spread:.1f}%  -> {'PASS' if ok else 'FAIL'}")
