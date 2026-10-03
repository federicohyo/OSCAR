#!/usr/bin/env python3
"""Build the odor stimulus used to reproduce the LNA-neuron input trace on silicon.

    ../.venv-meas/bin/python3 odor_stimulus.py

The original synthetic trace behind the reference figure lives outside either repo,
so this regenerates a trace matching its reference shape: a resting baseline,
a fast negative-going onset, a slower continued decline through the plateau,
and a fast return to baseline, with band-limited noise on top. Read off
the LNA-neuron input figure:

    total record        0.8 s
    event onset         ~0.33 s      offset ~0.565 s   (0.235 s long)
    baseline            ~-3 uV, noise ~+/-1.5 uV
    plateau             -11 uV falling to -16 uV
    swing               ~13 uV peak-to-peak

Two deliberate departures, both stated in the caption:

**Amplitude is scaled up.** 13 uVpp at the input would give ~1.3 mV at the LNA
output, against ~19.5 mV rms of noise on that node -- unmeasurable. The shape is
preserved exactly and the amplitude scaled to `--chip-vpp` (default 3 mVpp),
inside the linearity verified from 400 uVpp to 7 mVpp, so the scaling is a pure
gain change rather than a change of regime.

**Timescale is 1:1 with the reference.** The event's content lands around 2-20 Hz,
inside the measured passband, so time compression stays off. The one
consequence worth naming: a 0.235 s plateau has content near 4 Hz and below,
where the AC-coupled source departs from flat (0.96 of plateau at 3 Hz, 0.84 at
1.4 Hz). `--preemph` divides the stimulus by the source's measured response
(lna_transfer_ref.csv) so what arrives at the chip is the intended waveform.

Outputs:
    odor_stimulus.csv     t_s, v_norm (unit peak-to-peak), v_chip_v
    odor_stimulus.wav     for the bench, scaled so the chip sees --chip-vpp
    odor_stimulus_ref.pwl    for ngspice at the reference ~13 uVpp
    odor_stimulus_chip.pwl   for ngspice at the bench amplitude
"""

import argparse
import csv
import math
import os
import struct
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FS_WAV = 44100
VPP_AT_025 = 0.007            # chip input when the jack is driven at 0.25 Vpp
FULL_SCALE_VRMS = 1.0         # same assumption as sine_out.sh


def odor_trace(fs, dur=0.8, t_on=0.330, t_off=0.565, seed=3):
    """Synthetic odor response matching the reference trace's shape.

    Returns volts in the reference's own units (microvolts), so the shape can be
    compared with the figure directly before any scaling."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(dur * fs)) / fs
    # The time axis stays read-only. Under CPython 3.14 a local array
    # can momentarily look like a temporary to NumPy's in-place elision, and an
    # expression such as `(t - 0.313)` is then computed INTO t -- silently
    # shifting the whole time base (observed here: t[0] went 0 -> -0.313, and
    # the 0.8 s record became 0.49 s). Marking it read-only turns that into a
    # loud error instead of corrupt data.
    t.flags.writeable = False
    v = np.full_like(t, -3.0)                       # resting baseline, uV

    m = (t >= t_on) & (t < t_off)
    te = t[m] - t_on
    span = t_off - t_on
    # fast onset onto a plateau, then a slower continued decline, as reference
    onset = 1.0 - np.exp(-te / 0.012)
    decline = 0.45 * (te / span)
    v[m] = -3.0 - (8.0 * onset + 5.0 * decline * onset)

    # fast return to baseline (the reference trace snaps back in ~10 ms)
    m2 = t >= t_off
    v[m2] = -3.0 + (v[m][-1] + 3.0) * np.exp(-(t[m2] - t_off) / 0.010)

    # a small pre-onset bump is visible in the reference trace
    v += 1.6 * np.exp(-0.5 * ((t - 0.313) / 0.012) ** 2)

    # band-limited noise (~+/-1.5 uV, rolled off above ~40 Hz)
    n = rng.normal(0, 1.0, len(t))
    k = max(1, int(fs / 80))
    n = np.convolve(n, np.ones(k) / k, mode="same")
    n *= 1.5 / (n.std() or 1.0)
    out = v + n
    # Both returned arrays are locked read-only for the same reason `t` is:
    # a caller's local array with a single reference can be chosen as the
    # in-place target of NumPy's temporary elision, so an innocuous expression
    # like `v - v.mean()` silently rewrites the data it was meant to read.
    # (Observed: the trace shifted by its own mean, -2.78 -> +2.72 uV.)
    t.flags.writeable = False
    out.flags.writeable = False
    return t, out


def preemphasis(t, v, ref_csv):
    """Divide the stimulus by the source's measured frequency response.

    The audio source is AC-coupled; without this the low-frequency part of the
    plateau arrives attenuated and the event droops more than the amplifier
    alone would make it droop."""
    rows = list(csv.DictReader(open(ref_csv)))
    rf = np.array([float(r["freq_hz"]) for r in rows])
    rv = np.array([float(r["vpp_out"]) for r in rows])
    ok = rv > 0
    rf, rv = rf[ok], rv[ok]
    plateau = np.median(rv[(rf >= 5) & (rf <= 130)])
    resp = rv / plateau

    n = len(v)
    mu = float(v.mean())
    V = np.fft.rfft(v - mu)
    fr = np.fft.rfftfreq(n, t[1] - t[0])
    H = np.ones_like(fr)
    band = fr > 0
    H[band] = np.exp(np.interp(np.log(np.clip(fr[band], rf.min(), rf.max())),
                               np.log(rf), np.log(resp)))
    H = np.clip(H, 0.15, 1.0)          # cap the boost at ~6.5x
    return np.fft.irfft(V / H, n) + mu


MARK_HZ, MARK_S, LEAD_S, GAP_S, TAIL_S = 137.0, 0.05, 0.10, 0.35, 0.30


def write_wav(path, t, v_chip, chip_vpp, pad=None):
    """WAV whose playback puts `v_chip` on the chip input.

    Layout:  [LEAD silence][MARK burst][GAP silence][odor][TAIL silence]

    The stimulus is a one-shot, so the recording has to be aligned to it. Host
    playback timing is good to only a few tens of ms -- comparable to the
    features being measured -- so a short marker burst is written at a known
    offset before the event and the recording is aligned on that instead. The
    marker is at the same amplitude as the stimulus, so it comes through the
    amplifier as an unmistakable burst while holding the operating point.

    137 Hz deliberately: clear of the mains line and its harmonics (which carry
    ~15 mV rms at this node), inside the measured passband, and incommensurate
    with the 1 kS/s readout."""
    jack_vpp = 0.25 * chip_vpp / VPP_AT_025
    amp_fs = (jack_vpp / 2) / (FULL_SCALE_VRMS * math.sqrt(2))
    if amp_fs > 1.0:
        sys.exit(f"needs {amp_fs:.2f} full scale -- reduce --chip-vpp")
    span = float(np.ptp(v_chip)) or 1.0
    mu = float(v_chip.mean())
    x = (v_chip - mu) / (span / 2)                     # +/-1

    reps = int(os.environ.get("ODOR_REPEATS", "1"))
    tm = np.arange(int(MARK_S * FS_WAV)) / FS_WAV
    mark = np.sin(2 * np.pi * MARK_HZ * tm)
    mark *= np.hanning(len(mark))                      # click-free at either edge
    one = np.concatenate([np.zeros(int(LEAD_S * FS_WAV)), mark,
                          np.zeros(int(GAP_S * FS_WAV)), x,
                          np.zeros(int(TAIL_S * FS_WAV))])
    # One playback containing every repeat, back to back. Playing a single WAV
    # repeatedly instead would introduce two errors: pw-play's start latency
    # jitters by more than a second, and each relaunch leaves a ~100 ms silent
    # gap. With one continuous playback the period is exact, so the recording
    # can be folded on it and the latency is bracketed rather than known.
    x = np.tile(one, reps)
    pcm = np.clip(x * amp_fs, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(FS_WAV)
        w.writeframes((pcm * 32767).astype("<i2").tobytes())
    t_mark = LEAD_S + MARK_S / 2.0            # marker CENTRE
    t_odor = LEAD_S + MARK_S + GAP_S
    period = len(one) / FS_WAV
    return jack_vpp, amp_fs, (t_mark, t_odor, len(pcm) / FS_WAV, period, reps)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--chip-vpp", type=float, default=0.003,
                    help="peak-to-peak amplitude at the chip input [V]")
    ap.add_argument("--preemph", action="store_true", default=True,
                    help="pre-compensate the source's measured response")
    ap.add_argument("--no-preemph", dest="preemph", action="store_false")
    ap.add_argument("--repeats", type=int, default=10,
                    help="repeats concatenated into ONE playback")
    args = ap.parse_args()

    # high-rate trace for the WAV
    t, v_uv = odor_trace(FS_WAV)
    if args.preemph:
        ref = os.path.join(HERE, "lna_transfer_ref.csv")
        if os.path.exists(ref):
            v_uv = preemphasis(t, v_uv, ref)
            print("pre-emphasis: source response divided out")
        else:
            print("pre-emphasis skipped (no lna_transfer_ref.csv)")

    span_uv = float(np.ptp(v_uv))
    mu = float(v_uv.mean())
    v_chip = (v_uv - mu) / (span_uv / 2) * (args.chip_vpp / 2)
    print(f"stimulus: {t[-1]:.2f} s, reference swing {span_uv:.1f} uVpp "
          f"-> scaled to {args.chip_vpp*1e3:.2f} mVpp at the chip "
          f"({args.chip_vpp/ (span_uv*1e-6):.0f}x)")

    os.environ.setdefault("ODOR_REPEATS", str(args.repeats))
    jack, fs_amp, (t_mark, t_odor, dur, period, reps) = write_wav(
        os.path.join(HERE, "odor_stimulus.wav"), t, v_chip, args.chip_vpp)
    print(f"wav: jack {jack:.4f} Vpp ({fs_amp:.4f} full scale), "
          f"{reps} repeats x {period:.3f} s = {dur:.2f} s total")
    print(f"     sync marker centre at {t_mark:.3f} s ({MARK_HZ:g} Hz, {MARK_S*1e3:.0f} ms), "
          f"odor onset at {t_odor:.3f} s")
    with open(os.path.join(HERE, "odor_timing.json"), "w") as f:
        import json
        json.dump({"t_mark": t_mark, "mark_hz": MARK_HZ, "mark_s": MARK_S,
                   "t_odor": t_odor, "wav_s": dur, "period_s": period,
                   "repeats": reps, "chip_vpp": args.chip_vpp,
                   "event_on": 0.330, "event_off": 0.565}, f, indent=2)

    # decimated copy for the CSV and the ngspice PWL (1 kS/s is plenty here)
    step = FS_WAV // 1000
    td, vd, vc = t[::step], v_uv[::step], v_chip[::step]
    with open(os.path.join(HERE, "odor_stimulus.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "v_reference_uv", "v_chip_v"])
        for a, b, c in zip(td, vd, vc):
            w.writerow([f"{a:.6f}", f"{b:.4f}", f"{c:.9f}"])

    # Two PWL files, because the two legs need different amplitudes:
    #   _ref : the reference ~13 uVpp. With zero SPICE noise, this
    #          reproduces the reference figure directly and stays linear.
    #   _chip  : the bench amplitude. At the simulated 315x, 3 mVpp would
    #            demand 0.95 Vpp out and the SIMULATED amplifier saturates --
    #            which is a property of the simulated gain rather than the stimulus.
    vp = (vd - float(np.mean(vd))) * 1e-6          # reference units -> volts
    with open(os.path.join(HERE, "odor_stimulus_ref.pwl"), "w") as f:
        for a, c in zip(td, vp):
            f.write(f"{a:.6f} {c:.9e}\n")
    with open(os.path.join(HERE, "odor_stimulus_chip.pwl"), "w") as f:
        for a, c in zip(td, vc):
            f.write(f"{a:.6f} {c:.9e}\n")
    print(f"csv + pwl: {len(td)} points at 1 kS/s")
    print("\nfiles: odor_stimulus.csv / .wav / .pwl")


if __name__ == "__main__":
    sys.exit(main())
