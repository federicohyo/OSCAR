#!/usr/bin/env python3
"""Is the 150 uVpp gain bump real, or block-to-block drift?

The main ladder read 296.3x at 150 uVpp (twice, 0.07% apart). The low-end block,
45 minutes later, read 280.3x at 100 uVpp -- and the main ladder itself read
277.4x at 300 uVpp. So 150 uVpp stands ~6% above BOTH its neighbours, but the
neighbours were measured in different blocks.

This measures 100 / 150 / 200 / 100 uVpp back to back in ONE block. Within a
block the guard has been 0.06-2.8%, far below the 6% in question, so a bump that
survives here is a property of the amplifier and one that vanishes was drift.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_meas import Session, guard, DIVIDER

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FREQ, SETTLE, WINDOW = 88.57, 60.0, 12.0
VINS = [0.000100, 0.000150, 0.000200, 0.000100]

with Session(ROOT, "gain_crosscheck") as s:
    rows = []
    for i, vin in enumerate(VINS):
        tag = f"C{i}_{vin*1e6:.0f}uVpp" + ("_guard" if i == len(VINS)-1 else "")
        r, row = s.point(tag, FREQ, vin / DIVIDER, settle=SETTLE, window=WINDOW)
        rows.append(row)
        print(f"  {vin*1e6:4.0f} uVpp -> out {r['vpp']*1e3:7.2f} mVpp  "
              f"gain(nominal) {float(row['gain']):6.1f}x  h2 {row['h2']}  "
              f"DC {row['dc_v']}  +-{float(row['amp_se_v'])*1e3:.2f}mV", flush=True)

ok, spread = guard(rows)
print(f"\nguard at 100 uVpp: {rows[0]['gain']}x vs {rows[-1]['gain']}x  "
      f"spread {spread:.1f}%  -> {'PASS' if ok else 'FAIL'}")
print("(quantisation-corrected gains come out of analyze.py)")
