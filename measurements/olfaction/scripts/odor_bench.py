#!/usr/bin/env python3
"""Play the odor stimulus into the real LNA and record its output.

    ../.venv-meas/bin/python3 odor_bench.py

Read-only on the chip: the FTDI stays closed and DACs untouched, so the biases
stay exactly as loaded.

The stimulus WAV holds N repeats back to back and is played ONCE. That matters:
`pw-play`'s start latency jitters by more than a second and each relaunch leaves
a ~100 ms silent gap, so per-playback alignment is best avoided. With one continuous
playback the repeat period is exact, and the only unknown is a single global
offset -- recovered by correlating the marker band against a comb of N pulses
spaced one period apart. Averaging over the whole record makes that estimate far
sharper than any single-trial detection, and it stays stable between repeats.

The node carries single-sample ADC glitches of a few hundred millivolts. They
are broadband, so they land in the marker band too and would otherwise lift the
detector's floor above the burst; a 7-tap median filter removes them before
detection. The average itself is computed from the unfiltered samples.

Outputs:
    odor_bench.csv          t_s (0 = odor onset), vout mean, sd, n
    odor_bench_trials.npz   every folded repeat
"""

import argparse
import csv
import json
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_audio_sweep import Scope, longest_contiguous, BOARD_DT

HERE = os.path.dirname(os.path.abspath(__file__))
FS = 1.0 / BOARD_DT


def marker_envelope(t, v, mark_hz):
    """Envelope of the recording in the marker band, glitches removed."""
    from scipy.signal import medfilt
    vm = medfilt(np.asarray(v, float), 7)
    z = (vm - float(np.mean(vm))) * np.exp(-2j * math.pi * mark_hz * t)
    k = max(3, int(0.010 * FS))
    return np.abs(np.convolve(z, np.ones(k) / k, mode="same"))


def find_offset(env, period, reps, mark_s):
    """Offset of the FIRST marker, by correlating against a comb of N pulses.

    Scanning one period and summing the envelope at every repeat position makes
    the estimate immune to a single bad repeat and averages the noise down."""
    P = int(round(period * FS))
    w = max(3, int(mark_s * FS))
    best, best_score = 0, -1.0
    for off in range(P):
        idx = off + P * np.arange(reps)
        idx = idx[idx + w < len(env)]
        if len(idx) < max(2, reps // 2):
            continue
        score = float(np.mean([env[i:i + w].mean() for i in idx]))
        if score > best_score:
            best, best_score = off, score
    floor = float(np.median(env))
    return best / FS, best_score / (floor or 1.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--wav", default=os.path.join(HERE, "odor_stimulus.wav"))
    ap.add_argument("--timing", default=os.path.join(HERE, "odor_timing.json"))
    ap.add_argument("--pre", type=float, default=0.35)
    ap.add_argument("--post", type=float, default=0.75)
    ap.add_argument("--latency", type=float, default=3.0)
    ap.add_argument("--settle", type=float, default=4.0)
    ap.add_argument("--out", default=os.path.join(HERE, "odor_bench.csv"))
    args = ap.parse_args()

    tm = json.load(open(args.timing))
    period, reps = tm["period_s"], tm["repeats"]
    lead = tm["t_odor"] - tm["t_mark"]
    print(f"{reps} repeats x {period:.3f} s in one playback ({tm['wav_s']:.1f} s)")
    print(f"marker {tm['mark_hz']:g} Hz, odor onset {lead:.3f} s after it, "
          f"chip drive {tm['chip_vpp']*1e3:.2f} mVpp\n")

    subprocess.run(["pkill", "-x", "pw-play"], capture_output=True)
    scope = Scope()
    scope.drain(args.settle)
    p = subprocess.Popen(["pw-play", "--", args.wav],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    try:
        t, v = longest_contiguous(*scope.collect(tm["wav_s"] + args.latency + 1.0))
    finally:
        try:
            p.wait(timeout=2)
        except Exception:
            p.kill()
        subprocess.run(["pkill", "-x", "pw-play"], capture_output=True)
        scope.close()

    t = t - t[0]
    v = np.asarray(v, float)
    print(f"recorded {len(v)} samples ({t[-1]:.2f} s), DC {np.mean(v):.4f} V")

    # Clipping gate. The odor event is near-unipolar and the amplifier inverts,
    # so it drives the output UP, toward the rail -- exactly where headroom is
    # scarce. A clipped record still folds into a plausible-looking curve with a
    # plausible SNR, which is how a whole afternoon was lost earlier today, so
    # this is checked before anything is derived from the trace.
    RAIL = 1.78
    frac_hi = float(np.mean(v >= RAIL - 0.005))
    frac_lo = float(np.mean(v <= 0.005))
    print(f"  headroom: vmax {v.max():.4f} V, vmin {v.min():.4f} V, "
          f"{frac_hi*100:.2f}% at the rail, {frac_lo*100:.2f}% at 0 V")
    if frac_hi > 0.0005 or frac_lo > 0.0005:
        sys.exit(f"ABORT: {frac_hi*100:.2f}% of samples are against the rail. "
                 f"The response is clipped and every number derived from it would "
                 f"be biased rather than merely noisy. Re-run odor_stimulus.py with a "
                 f"smaller --chip-vpp (currently {tm['chip_vpp']*1e3:.2f} mVpp).")

    env = marker_envelope(t, v, tm["mark_hz"])
    off, snr = find_offset(env, period, reps, tm["mark_s"])
    print(f"first marker at {off:.3f} s, comb score {snr:.1f}x the envelope floor")
    if snr < 1.8:
        sys.exit("marker comb is unlocked -- is the amplifier passing signal?")

    npre, npost = int(args.pre * FS), int(args.post * FS)
    P = int(round(period * FS))
    folds = []
    for k in range(reps):
        i0 = int(round((off + lead) * FS)) + k * P
        if i0 - npre < 0 or i0 + npost >= len(v):
            continue
        seg = np.array(v[i0 - npre: i0 + npost], dtype=float)
        folds.append(seg - float(np.mean(seg[: int(0.15 * FS)])))
    if not folds:
        sys.exit("every repeat overlaps the record edge")

    A = np.vstack(folds)
    mean, sd = A.mean(axis=0), A.std(axis=0)
    tt = (np.arange(A.shape[1]) - npre) / FS
    ev = (tt >= 0) & (tt <= tm["event_off"] - tm["event_on"])
    pre = tt < -0.05

    print(f"\n{len(folds)} repeats folded")
    print(f"  baseline noise  : {np.std(mean[pre])*1e3:6.2f} mV rms "
          f"(single repeat {np.mean(sd[pre])*1e3:.2f} mV)")
    peak = float(mean[ev][int(np.argmax(np.abs(mean[ev])))])
    print(f"  event deflection: {peak*1e3:+7.2f} mV peak  "
          f"({'UP - inverting, as reference' if peak > 0 else 'DOWN'})")
    print(f"  SNR on the event: {abs(peak) / (float(np.std(mean[pre])) or 1):.1f}x")
    print(f"  per-repeat spread over the event: {np.mean(sd[ev])*1e3:.2f} mV rms")
    print(f"  headroom used at the peak: {abs(peak)*1e3:.1f} mV of "
          f"{(RAIL - float(np.mean(v)))*1e3:.0f} mV available above the DC level")

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "vout_mean_v", "vout_sd_v", "n_repeats"])
        for a, b, c in zip(tt, mean, sd):
            w.writerow([f"{a:.4f}", f"{b:.7f}", f"{c:.7f}", len(folds)])
    np.savez(os.path.join(HERE, "odor_bench_trials.npz"), t=tt, trials=A,
             raw_t=t, raw_v=v, offset_s=off, comb_score=snr,
             period_s=period, reps=reps, lead_s=lead,
             chip_vpp=tm["chip_vpp"], mark_hz=tm["mark_hz"])
    print(f"\ndata: {os.path.basename(args.out)} + odor_bench_trials.npz "
          f"(raw record included -- re-fold offline with the bench idle)")


if __name__ == "__main__":
    sys.exit(main())
