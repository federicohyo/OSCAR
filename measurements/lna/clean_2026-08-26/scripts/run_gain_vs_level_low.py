#!/usr/bin/env python3
"""Extend the gain-vs-amplitude ladder DOWNWARD, into the small-signal corner.

The main block spans 150-900 uVpp: only 6x, because the 1.78 V rail caps the top
at this ~272x operating point. The range can only be widened from below.

How far down is set by the fit's own error bar rather than by taste. In the main block
`amp_se` held at 0.24-0.32 mV regardless of level, so at an output of A mVpp the
fractional error is ~0.25/A. At 50 uVpp the output is ~14 mVpp, giving ~1.7% --
still a real measurement. Below that it degrades quickly, so 40 uVpp is the floor.

Appends to the SAME block/CSV as the main ladder, with its own repeat guard.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_meas import Session, guard, DIVIDER

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FREQ, SETTLE, WINDOW = 88.57, 60.0, 12.0     # longer window: small signal, more averaging
VINS = [0.000040, 0.000070, 0.000100, 0.000040]

with Session(ROOT, "gain_vs_level") as s:
    rows = []
    for i, vin in enumerate(VINS):
        jack = vin / DIVIDER
        tag = f"S{i}_{vin*1e6:.0f}uVpp" + ("_guard" if i == len(VINS)-1 else "")
        r, row = s.point(tag, FREQ, jack, settle=SETTLE, window=WINDOW)
        rows.append(row)
        se_pct = 100*float(row["amp_se_v"])/r["vpp"] if r["vpp"] > 0 else float("nan")
        print(f"  {vin*1e6:4.0f} uVpp in -> out {r['vpp']*1e3:7.2f} mVpp  "
              f"gain {float(row['gain']):6.1f}x ({row['gain_db']} dB)  "
              f"h2 {row['h2']}  +-{float(row['amp_se_v'])*1e3:.2f}mV ({se_pct:.1f}%)  "
              f"DC {row['dc_v']}  {row['flag']}", flush=True)

ok, spread = guard(rows)
print(f"\nlow-end repeat guard: {rows[0]['gain']}x vs {rows[-1]['gain']}x  "
      f"spread {spread:.1f}%  -> {'PASS' if ok else 'FAIL'}")
