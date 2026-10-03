#!/usr/bin/env python3
"""Freeze an emulated-LIF stimulus for olfaction_emul_run.py, one projection seed.

The runner sends a frozen array rather than deriving the stimulus on the measurement
path, ever since a rebuild inside the runner produced event counts the identical
standalone code did not. The frozen cur is checked against the unit-weight build here,
and --check verifies that regenerating the ORIGINAL seed reproduces the published
stimulus bit for bit -- which is what licenses freezing the remaining two seeds of the
olfaction_emul_accuracy.py protocol (100 + 7919*r for r = 0, 1, 2) at all.

    ./.venv-meas/bin/python3 olfaction_emul_freeze.py --seed 8019 \
        --out data/olfaction_emul_stimulus_seed8019.npz
    ./.venv-meas/bin/python3 olfaction_emul_freeze.py --seed 100 --check
"""
import argparse
import numpy as np

from olfaction_emul_accuracy import build, drive_matrix

THETA, NNEUR, TTICKS = 0.25, 16, 150
DECAY, W, VTH, REFR = 64000, 20000, 32768, 10


def freeze(seed0, out):
    F, Y, it, enc, names = build(THETA, NNEUR, seed0)
    nchunk = len(Y)
    cur = drive_matrix(enc, NNEUR, nchunk, TTICKS, W, W)
    assert np.all(cur % W == 0), "weighted drive is not a multiple of the weight"
    # numpy's temporary elision can turn `ev = cur // W` into an IN-PLACE divide when
    # cur's refcount allows it -- line-traced here destroying cur between statements.
    # Divide into a copy, never into cur.
    ev = cur.copy()
    ev //= W                                    # the unit-weight build, for the check
    assert np.max(np.abs(ev)) <= 127, "event count exceeds int8"
    if out:
        np.savez(out, ev=ev, cur=cur, decay=DECAY, w=W, vth=VTH, refr=REFR,
                 labels=Y, trial=it, nchunk=nchunk, T=TTICKS)
        print(f"wrote {out}: {nchunk} chunks x {NNEUR} neurons, T={TTICKS}")
    return ev, cur, Y, it, nchunk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=100)
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true",
                    help="compare against data/olfaction_emul_stimulus.npz instead "
                         "of writing (--out ignored)")
    args = ap.parse_args()
    ev, cur, Y, it, nchunk = freeze(args.seed, None if args.check else args.out)
    if args.check:
        z = np.load("data/olfaction_emul_stimulus.npz")
        same = (np.array_equal(ev, z["ev"]) and np.array_equal(cur, z["cur"])
                and np.array_equal(Y, z["labels"]) and np.array_equal(it, z["trial"])
                and nchunk == int(z["nchunk"]))
        print(f"seed {args.seed} against frozen stimulus: "
              f"{'IDENTICAL' if same else 'DIFFERS'}")
        if not same:
            raise SystemExit("freeze step does not reproduce the verified stimulus")


if __name__ == "__main__":
    main()
