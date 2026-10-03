#!/usr/bin/env python3
"""Powered N/S/V evaluation (NEXT_STEPS_ACCURACY step 1-2): expand to ~30 MIT-BIH records
(all S-bearing + V-rich, balanced N/S/V), run the STRUCTURED feature encoding in software
(chip-independent) over the full set, and save a self-contained npz for the paired test.

Records are chosen so >=12 are S-bearing (the lever for the macro-F1 / S-class result) and
V coverage is adequate -- not by padding more beats onto the same few records.
"""
import warnings; warnings.filterwarnings("ignore")
import argparse
import re
import numpy as np
from reservoir_data import get_beats
from reservoir_structured import build_spec, run as struct_run


def parse_counts(path="record_probe.out"):
    counts = {}
    for line in open(path):
        m = re.match(r"^(\d{3}): N=\s*(\d+) S=\s*(\d+) V=\s*(\d+)", line)
        if m:
            counts[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return counts


def select_records(counts, n_total=30, s_min=10):
    """All S-bearing (S>=s_min) records, then fill with the highest-V remaining records."""
    s_bear = sorted([r for r, (n, s, v) in counts.items() if s >= s_min],
                    key=lambda r: -counts[r][1])
    rest = sorted([r for r in counts if r not in s_bear], key=lambda r: -counts[r][2])
    sel = s_bear + rest[:max(0, n_total - len(s_bear))]
    return sorted(sel), s_bear


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-total", type=int, default=30)
    ap.add_argument("--n-per-class", type=int, default=400)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--out", default="reservoir_spikes_nsv_structured_sw_full.npz")
    args = ap.parse_args()

    counts = parse_counts()
    records, s_bear = select_records(counts, args.n_total)
    print(f"selected {len(records)} records ({len(s_bear)} S-bearing): {','.join(records)}")

    X, y, meta = get_beats(records=tuple(records), n_per_class=args.n_per_class, classes="NSV")
    g = np.asarray(meta["records"]); rr = meta["rr"]; T = args.T
    urec = sorted(set(g.tolist()))
    print(f"balanced dataset: {len(y)} beats, classes {np.bincount(y)}, "
          f"{len(urec)} records present after balancing")
    # per-record class presence (records with >=1 of each class matter for per-record macro-F1)
    multi = sum(1 for r in urec if len(np.unique(y[g == r])) >= 2)
    print(f"records with >=2 classes present: {multi}/{len(urec)}")

    spec = build_spec()
    spikes = None
    for k, spikes, tot in struct_run(spec, X, rr, T, mismatch=0.0, seed=0):
        pass
    rate = np.mean([len(spikes[i, b]) for i in range(len(spec)) for b in range(len(y))])
    print(f"structured SW encoding done: mean {rate:.1f} out-spk/beat/neuron")

    np.savez(args.out, spikes=spikes, labels=y, records=g, neurons=np.arange(len(spec)),
             T=T, coding="structured_sw_full", classes="NSV", X_raw=X, rr=rr,
             record_list=np.array(records))
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
