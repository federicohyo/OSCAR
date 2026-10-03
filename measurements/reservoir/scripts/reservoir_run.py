#!/usr/bin/env python3
"""Phase-1 feedforward reservoir run (one neuron at a time).

In a feedforward reservoir the 16 neurons do not interact, so each can be stimulated
and recorded independently, then the state vectors assembled offline -- identical to
simultaneous fan-out, but with no AER saturation (only one neuron active at a time)
and no firmware change. For each beat and each reservoir neuron we inject the beat's
time-stretched Poisson-rate profile (piecewise constant), bin the neuron's output
spikes over time, and concatenate across neurons into a feature vector. The analog
membrane (heterogeneous tau, device mismatch) does the temporal nonlinear filtering.
"""

import argparse
import csv
import os
import queue
import time

import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_data import get_beats, encode_rate

# per-neuron tuned biases (JExc gain trimmed per neuron for a graded 20-200 Hz response)
# CLOCK TRAP -- read this before running at anything but 10 MHz.
#
# This default set was tuned on the 10 MHz crystal (2026-07-04) and it is what the
# ACC / DIM / NSV recordings in the reference analysis were taken with. Its JInhWp[0:3] sit
# at 1.77-1.78 V, which for a PMOS bias is OFF: inhibition is essentially disabled,
# which is fine at 10 MHz where excitatory efficacy is high. Synaptic efficacy falls
# as the core clock rises (the reference analysis), so running THIS set at
# 50 MHz is exactly the failure mode that section documents.
#
# The retuned 50 MHz set is the _jul10 one (2026-07-12), JInhWp ~ 1.27-1.29 V. It is
# not the default because changing the default would silently re-point every existing
# script at a different operating point. Pass it explicitly:
#
#   CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 reservoir_run.py \
#       --bias-pattern 'ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases'
#
BIAS_PATTERN = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}.biases"
BIAS_PATTERN_50MHZ = ("ofxCaravanViewer/bin/"
                      "bias_synapse_characterization_super_n{k}_jul10.biases")
DEFAULT_NEURONS = list(range(16))


def rate_profile(beat, nsteps, f_min, f_max):
    """Downsample a 128-sample beat to nsteps piecewise-constant Poisson rates (Hz)."""
    r = encode_rate(beat, f_min, f_max)
    idx = np.linspace(0, len(r) - 1, nsteps).round().astype(int)
    return r[idx]


def present_beat(b, neuron, rates, t_step):
    """Drive the piecewise-constant rate profile on `neuron`; return per-step output
    spike counts (len == len(rates))."""
    b.drain(max_lines=100000)
    times = []
    t0 = time.time()
    for i, rate in enumerate(rates):
        b.poisson(float(rate))
        step_end = t0 + (i + 1) * t_step
        while time.time() < step_end:
            try:
                line = b.out_q.get(timeout=0.02)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3:
                    try:
                        if int(p[1]) == neuron:
                            times.append(time.time() - t0)
                    except ValueError:
                        pass
    b.poisson_stop()
    return np.array(times)  # raw output spike times (s, rel. to onset)


# Chip-reported readout integrity for the whole run. Nonzero means the readout lost
# spikes (drops) or back-pressured the array (stalls), so the counts are not a
# measurement of the neurons. The old readout reported neither -- and was in fact
# capturing about one spike in seven (diagonal: 4660 spikes then vs 31956 now).
INTEGRITY = {"drops": 0, "stalls": 0}

# Task O. Until round 5 this counter was only PRINTED, at the end of the run, after
# hours of acquisition -- so a run that lost spikes from neuron 0 onward completed,
# was saved, and looked like data. It is now a hard abort on the first nonzero
# report, because a run with drops or stalls is not a measurement of the array and
# no amount of downstream analysis repairs it. Set RESERVOIR_ALLOW_DROPS=1 only when
# you are deliberately characterising the loss itself.
ALLOW_DROPS = os.environ.get("RESERVOIR_ALLOW_DROPS", "0") == "1"


class ReadoutIntegrityError(RuntimeError):
    """The chip reported dropped or stalled events; the acquisition is not valid."""


class BiasClockMismatch(RuntimeError):
    """A 10 MHz-tuned bias set was about to be used at a higher core clock."""


def check_bias_clock_pairing(pattern):
    """Refuse the Section 4.6 trap: a 10 MHz bias set at a higher clock.

    Synaptic efficacy falls as the core clock rises, so the 2026-07-04 set (whose
    JInhWp sits at ~1.78 V, i.e. inhibition OFF) is only valid on the crystal. The
    check is on the FILENAME, which is what actually distinguishes the two sets;
    it is a guard rail, not a measurement. Override with RESERVOIR_ALLOW_BIAS_CLOCK=1
    if you are deliberately reproducing an old acquisition at a new clock.
    """
    clk = int(os.environ.get("CARAVAN_CLK_MHZ", "50"))
    # Two ways to be recognised as retuned. The tag list is the original by-convention
    # rule. The clock stamp is stronger and cannot be spoofed by an old file: a set
    # written by reservoir_ratetune.py embeds the clock it was tuned at, so it is
    # valid at that clock and refused at any other.
    retuned = (any(tag in pattern for tag in ("_jul10", "_struct", "_feedproj"))
               or f"_{clk}mhz" in pattern.lower())
    if clk != 10 and not retuned and os.environ.get("RESERVOIR_ALLOW_BIAS_CLOCK") != "1":
        raise BiasClockMismatch(
            f"CARAVAN_CLK_MHZ={clk} with the 10 MHz-tuned bias set\n  {pattern}\n"
            f"whose JInhWp[0:3] are at ~1.78 V (PMOS OFF -- inhibition disabled). "
            f"Synaptic efficacy is clock-dependent; this "
            f"pairing is the documented failure mode, not a valid operating point.\n"
            f"Use --bias-pattern '{BIAS_PATTERN_50MHZ}', or set CARAVAN_CLK_MHZ=10, "
            f"or RESERVOIR_ALLOW_BIAS_CLOCK=1 to override deliberately.")


def _check_integrity():
    d, s = INTEGRITY["drops"], INTEGRITY["stalls"]
    if (d or s) and not ALLOW_DROPS:
        raise ReadoutIntegrityError(
            f"readout integrity lost: drops={d}, stalls={s}. The recorded counts are "
            f"not a measurement of the array. Reduce the array's rate (mask, lower "
            f"drive) or raise the clock; set RESERVOIR_ALLOW_DROPS=1 to override.")


def _collect_until(b, neuron, deadline, times, t0):
    """Drain output spikes on `neuron` until wall-clock `deadline`.

    Records BOTH the host arrival time and the chip's Timer0 timestamp (`abs_us`,
    wrap-corrected by the bridge). The host time alone is useless for spike timing:
    the FTDI batches bytes on a ~16 ms latency timer, so every packet in a batch is
    parsed microseconds apart no matter when the neuron actually fired -- that made
    real spikes look like exact duplicates. The chip timestamp is the ground truth;
    the host time is kept only to anchor it to the start of the presentation.
    """
    while True:
        now = time.time()
        if now >= deadline:
            return
        try:
            line = b.out_q.get(timeout=min(0.005, max(0.0, deadline - now)))
        except queue.Empty:
            continue
        if line.startswith("DROPS ") or line.startswith("STALLS "):
            q = line.split()
            if len(q) == 2:
                try:
                    INTEGRITY["drops" if q[0] == "DROPS" else "stalls"] += int(q[1])
                    _check_integrity()
                except ValueError:
                    pass
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3:
                try:
                    if int(p[1]) == neuron:
                        times.append((time.time() - t0, int(p[2])))
                except ValueError:
                    pass


def _chip_times(samples):
    """(host_rel, abs_us) pairs -> spike times in seconds since presentation start.

    Chip timestamps carry the true spacing but an unknown offset to `t0`; host times
    carry the offset but are quantised by USB batching. Anchor the chip clock with the
    smallest observed host-minus-chip lag (the least-delayed packet), which preserves
    the exact on-chip intervals and places them on the host timeline.
    """
    if not samples:
        return np.array([])
    chip = np.array([s[1] for s in samples], dtype=np.float64) * 1e-6
    host = np.array([s[0] for s in samples], dtype=np.float64)
    return chip + np.min(host - chip)


def present_delta(b, neuron, events, T, exc_syn, inh_syn):
    """Host-paced replay of a delta-coded event list (t_frac, channel) on `neuron`:
    UP -> excitatory synapse, DOWN -> inhibitory synapse. Returns raw output spike times."""
    b.drain(max_lines=100000)
    times = []
    t0 = time.time()
    cur = None
    for tf, chan in events:
        _collect_until(b, neuron, t0 + tf * T, times, t0)
        if chan != cur:
            b.route(exc_syn if chan == 0 else inh_syn, neuron, exc=(chan == 0))
            cur = chan
        b.fire()
    _collect_until(b, neuron, t0 + T + 0.2, times, t0)
    return _chip_times(times)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias-pattern", default=None,
                    help="per-neuron bias files, e.g. '.../super_n{k}_jul10.biases'; "
                         "default is the module BIAS_PATTERN")
    ap.add_argument("--beats", default=None,
                    help="frozen beat set from make_beatset.py; overrides "
                         "--records/--n-per-class/--classes")
    ap.add_argument("--records", default="100,208,119,233")
    ap.add_argument("--n-per-class", type=int, default=50)
    ap.add_argument("--classes", default="NV", help="NV (binary) or NSV (3-class)")
    ap.add_argument("--neurons", default=",".join(map(str, DEFAULT_NEURONS)))
    ap.add_argument("--coding", default="poisson", choices=["poisson", "delta"])
    ap.add_argument("--syn", type=int, default=0, help="excitatory (UP) synapse")
    ap.add_argument("--inh-syn", type=int, default=0, help="inhibitory (DOWN) synapse for delta")
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--nsteps", type=int, default=16, help="poisson: rate steps per beat")
    ap.add_argument("--tstep", type=float, default=0.06, help="poisson: seconds per rate step")
    ap.add_argument("--fmin", type=float, default=20.0)
    ap.add_argument("--fmax", type=float, default=200.0)
    ap.add_argument("--thr", type=float, default=0.04, help="delta: level-crossing threshold")
    ap.add_argument("--tpresent", type=float, default=2.0, help="delta: presentation time (s)")
    ap.add_argument("--out", default="reservoir_spikes.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    from reservoir_data import delta_encode
    neurons = [int(x) for x in args.neurons.split(",")]
    bias_pattern = args.bias_pattern or BIAS_PATTERN
    check_bias_clock_pairing(bias_pattern)
    print(f"biases: {bias_pattern}")
    if args.beats:
        # Frozen beat set: the ONLY way to guarantee two runs see identical beats.
        # get_beats is seeded, but its pool is built in record-argument order, so the
        # same seed with a different order returns different beats.
        from make_beatset import load_beatset
        X, y, meta = load_beatset(args.beats)
        print(f"beats: loaded {len(X)} from {args.beats} "
              f"(records/n-per-class/classes args ignored)")
    else:
        X, y, meta = get_beats(records=tuple(args.records.split(",")),
                               n_per_class=args.n_per_class, classes=args.classes)
    if args.smoke:
        X, y = X[:4], y[:4]
        neurons = neurons[:3]

    if args.coding == "poisson":
        T = args.nsteps * args.tstep
        enc = [rate_profile(X[bi], args.nsteps, args.fmin, args.fmax) for bi in range(len(X))]
    else:
        T = args.tpresent
        enc = [delta_encode(X[bi], args.thr) for bi in range(len(X))]
        print(f"delta events/beat: mean {np.mean([len(e) for e in enc]):.0f}")

    print(f"coding={args.coding} beats={len(X)} neurons={neurons} T={T:.2f}s/beat "
          f"(raw spikes -> {args.out}; kernel/tau swept offline)")
    def save_ckpt(arr, done):
        """Atomically write the (possibly partial) npz after each neuron."""
        tmp = args.out + ".tmp.npz"
        np.savez(tmp, spikes=arr, labels=y, records=meta["records"],
                 neurons=np.array(neurons), T=T, coding=args.coding,
                 classes=args.classes, done_neurons=np.array(done, dtype=int),
                 **provenance(bias_files=[bias_pattern.format(k=k) for k in neurons],
                              thr=args.thr, weight=args.weight, syn=args.syn,
                              inh_syn=args.inh_syn, tpresent=args.tpresent,
                              beats_file=args.beats or ""))
        os.replace(tmp, args.out)

    # pre-allocate with empty arrays so a partial checkpoint is always well-formed
    arr = np.empty((len(neurons), len(X)), dtype=object)
    for i in range(len(neurons)):
        for bi in range(len(X)):
            arr[i, bi] = np.array([])
    done = []
    with BridgeSession() as b:
        for i, k in enumerate(neurons):         # neurons OUTER: load each neuron's bias once
            b.apply_biases(load_biases(bias_pattern.format(k=k)))
            b.monitor(k)                         # route neuron k's membrane to the scope pin
            time.sleep(0.8)
            print(f"  --> monitoring neuron {k} on scope")
            b.program_weight(args.syn, args.weight, exc=True)
            if args.coding == "delta":
                b.program_weight(args.inh_syn, args.weight, exc=False)
            else:
                b.route(args.syn, k, exc=True)
            tot = 0
            for bi in range(len(X)):
                if args.coding == "poisson":
                    st = present_beat(b, k, enc[bi], args.tstep)
                else:
                    st = present_delta(b, k, enc[bi], T, args.syn, args.inh_syn)
                arr[i, bi] = st
                tot += len(st)
                if args.smoke:
                    print(f"  neuron {k:2d} beat {bi} (y={y[bi]}): {len(st)} spk "
                          f"t={np.round(st, 2).tolist()}")
            done.append(int(k))
            print(f"  neuron {k:2d}: {tot} spikes over {len(X)} beats"
                  + ("  [DEAD]" if tot == 0 else ""))
            if not args.smoke:                   # checkpoint after EVERY neuron (atomic)
                save_ckpt(arr, done)
                print(f"    [checkpoint] {len(done)}/{len(neurons)} neurons -> {args.out}")

    dz, sz = INTEGRITY["drops"], INTEGRITY["stalls"]
    print(f"\nreadout integrity: drops={dz}, stalls={sz}"
          + ("  <-- NOT a clean measurement of the array"
             if (dz or sz) else "  (clean: nothing lost, array free-running)"))

    if not args.smoke:
        print("wrote", args.out, f"({len(done)}/{len(neurons)} neurons x {len(X)} beats raw spikes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
