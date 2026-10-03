#!/usr/bin/env python3
"""Compute the per-branch bias ladder that turns the weight word into a real binary code.

The four weight branches on this die are the same size: their measured single-bit onsets sit
within a few millivolts of each other (bit 3 is the exception, ~35 mV weaker). So programming
word w delivers popcount(w) units of charge rather than w, and the "4-bit"
code has five distinguishable levels instead of sixteen.

Binary weighting has to be created in the bias domain instead. In weak inversion a branch's
current is I_j = I* exp((V_j - V_j_onset)/nUT), so setting

    V_j = V + (V_j_onset - V_0_onset) + j * nUT * ln 2

makes branch j carry 2^j times the current branch 0 carries, for any common-mode V. The first
term cancels each branch's own mismatch; the second builds the binary ratio. Delivered charge
is then A(w) = w exactly, and the onset of word w becomes linear in ln w.

Reads data/synapse/onset_<tag>.json and writes data/synapse/ladder_<tag>.json.
"""

import argparse
import json
import math
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="n5")
    ap.add_argument("--dir", default="data/synapse")
    ap.add_argument("--nut", type=float, default=None,
                    help="override nUT in volts (default: the fitted value in the JSON)")
    args = ap.parse_args()

    src = os.path.join(args.dir, f"onset_{args.tag}.json")
    with open(src) as f:
        d = json.load(f)

    nut = args.nut if args.nut is not None else d.get("nUT_volts")
    if not nut:
        raise SystemExit(f"nUT absent from {src}; run the 'slope' stage first or pass --nut")
    delta = nut * math.log(2)

    br = d.get("branches") or {}
    onsets = {}
    for j in range(4):
        rec = br.get(str(1 << j))
        if not rec or rec.get("mean") is None:
            raise SystemExit(f"no measured onset for bit {j}; rerun the 'branches' stage")
        onsets[j] = rec["mean"]

    ref = onsets[0]
    offsets = [(onsets[j] - ref) + j * delta for j in range(4)]

    out = {
        "tag": args.tag,
        "nUT_volts": nut,
        "delta_per_octave_volts": delta,
        "branch_onsets": {str(j): onsets[j] for j in range(4)},
        "offsets": offsets,
    }
    dst = os.path.join(args.dir, f"ladder_{args.tag}.json")
    with open(dst, "w") as f:
        json.dump(out, f, indent=2)

    print(f"nUT = {nut*1000:.1f} mV, one octave = {delta*1000:.1f} mV\n")
    print("branch   onset (V)   mismatch (mV)   binary step (mV)   offset (mV)")
    for j in range(4):
        print(f"  bit {j}   {onsets[j]:.4f}      {(onsets[j]-ref)*1000:+7.1f}"
              f"          {j*delta*1000:+7.1f}        {offsets[j]*1000:+7.1f}")
    print(f"\nwrote {dst}")


if __name__ == "__main__":
    main()
