#!/usr/bin/env python3
"""Output noise of the LNA, clean setup — long quiet record, raw traces kept.

The tone stays off. The sound card is left IDLE rather than merely silent: this afternoon a
zero-amplitude WAV still raised the noise 24 -> 179 mV rms, because activating
the output stage was itself the fault (see ../debug/). So this block asserts the
absence of any player rather than assuming it.

Several separate blocks are taken instead of one long stretch so that a
disturbance can be localised and dropped rather than contaminating everything.
Input-referred noise is computed offline in analyze.py, dividing by the measured
gain(f) from the transfer block.
"""
import os, subprocess, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_meas import Session

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NBLOCK, BLOCKSEC = 8, 30.0

busy = subprocess.run(["pgrep", "-x", "pw-play"], capture_output=True).returncode == 0
if busy:
    sys.exit("ABORT: pw-play is running. The noise record must be taken with the "
             "sound card idle -- activating it is itself a noise source.")
print(f"sound card idle confirmed. {NBLOCK} x {BLOCKSEC:.0f} s quiet blocks "
      f"({NBLOCK*BLOCKSEC/60:.1f} min)\n", flush=True)

with Session(ROOT, "noise") as s:
    for i in range(NBLOCK):
        _, row = s.capture_only(f"N{i:02d}_quiet", 0.0, BLOCKSEC, note="no drive, card idle")
        d = np.load(os.path.join(ROOT, row["raw_npz"]))
        v = d["v"]
        print(f"  block {i+1}/{NBLOCK}: {len(v)} samples  DC {v.mean():.4f} V  "
              f"rms {v.std()*1e3:6.2f} mV  ptp {v.ptp()*1e3:5.0f} mV  "
              f"at-rail {100*np.mean(v>=1.775):.2f}%", flush=True)

print("\ndone -- analyse with analyze.py (needs the transfer block for gain(f))")
