#!/usr/bin/env python3
"""Gain vs input amplitude at 88.57 Hz, clean setup.

Levels are re-scaled for the new operating point: at ~290x the 1.78 V rail caps
the input near 1 mVpp, so the paper's 0.4-7 mVpp ladder no longer fits. The
first point is repeated last as the repeat guard; <10% spread gates the rest of
the campaign.

88.57 Hz is deliberately not a round number -- a commensurate frequency freezes
the 1 kS/s sampling phase (see README_MEASUREMENTS.md).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_meas import Session, guard, DIVIDER

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FREQ, SETTLE, WINDOW = 88.57, 60.0, 8.0
VINS = [0.00015, 0.00030, 0.00050, 0.00070, 0.00090, 0.00015]   # Vpp at the chip

with Session(ROOT, "gain_vs_level") as s:
    _, q = s.point("quiet_before", FREQ, 0.0, settle=20.0, window=WINDOW, note="no drive")
    print(f"QUIET  DC {q['dc_v']} V  noise-at-{FREQ}Hz {float(q['vout_pp'])*1e3:.2f} mVpp  "
          f"resid {float(q['resid_rms_v'])*1e3:.1f} mV rms", flush=True)
    rows = []
    for i, vin in enumerate(VINS):
        jack = vin / DIVIDER
        tag = f"L{i}_{vin*1e6:.0f}uVpp" + ("_guard" if i == len(VINS)-1 else "")
        r, row = s.point(tag, FREQ, jack, settle=SETTLE, window=WINDOW)
        rows.append(row)
        print(f"  {vin*1e6:4.0f} uVpp in (jack {jack:.5f}) -> out {r['vpp']*1e3:7.2f} mVpp "
              f"gain {float(row['gain']):6.1f}x ({row['gain_db']} dB)  DC {row['dc_v']}  "
              f"peak {row['peak_v']}  h2 {row['h2']}  +-{float(row['amp_se_v'])*1e3:.2f}mV  "
              f"rail {float(row['frac_at_rail'])*100:.1f}%  {row['flag']}", flush=True)
    s.point("quiet_after", FREQ, 0.0, settle=20.0, window=WINDOW, note="no drive")

ok, spread = guard(rows)
print(f"\nrepeat guard: {rows[0]['gain']}x vs {rows[-1]['gain']}x  spread {spread:.1f}%  "
      f"-> {'PASS' if ok else 'FAIL -- do not start the long sweeps'}")
