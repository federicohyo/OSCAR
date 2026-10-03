#!/usr/bin/env python3
"""A realistic extracellular spike train for the LNA input.

    ../.venv-meas/bin/python3 spike_stimulus.py --uvpp 400

Builds an extracellular action potential, repeats it at a physiological rate,
and writes a WAV scaled so the chip sees the requested amplitude.

WAVEFORM. The extracellular potential near a firing neuron follows roughly the
second time-derivative of the membrane potential, which gives the familiar
triphasic shape: a small positive foot, a large fast negative trough as the
sodium current flows in, then a slower positive repolarisation hump. Modelled
here as a sum of three Gaussians whose widths and spacing are the parameters --
trough 0.30 ms FWHM, hump at +0.55 ms and 45% of the trough, foot 8%. That is a
textbook shape, not a recording; --template loads a real one (CSV: t_s, v_uv)
if you have it, and everything downstream is unchanged.

AMPLITUDE is peak-to-peak, trough to hump, default 400 uVpp -- inside the
linearity verified on this chip from 400 uVpp to 7 mVpp.

TIME-STRETCH, and why it is not optional here. A 1 ms spike carries its energy
around 1-2 kHz. The amplifier passes that happily, but the pixhawk digitiser
runs at 1 kS/s, so a real-time spike arrives as a single sample and everything
drawn from it would be an alias. Stretching by --stretch (default 50) puts the
trough at 15 ms FWHM and the spectrum near 30 Hz, inside both the measured
passband and the Nyquist limit, and preserves the shape exactly. State it in
any caption: this is a shape-preserving time dilation, the same kind of stated
departure as the amplitude scaling in odor_stimulus.py.

    --stretch 1   gives the real-time spike. The LNA will amplify it correctly
                  and the pixhawk CANNOT record it. Use that only with a fast
                  scope on the output.

LEVEL. The jack-to-chip ratio is passed in (--ratio, measured, default 0.50),
NOT taken from the 0.25 Vpp -> 7 mVpp anchor in README_MEASUREMENTS: that
anchor is wrong by a factor of ~15 and using it drives ~18x too hard, which is
enough to push a stimulus meant for 0.55 mVpp past this chip's ~8 mVpp
saturation onset. spike_record.py re-measures the ratio at run time rather than
trusting any stored number, and that is the number to believe.

32-BIT AUDIO, deliberately. 400 uVpp at the chip is ~1.5 mVpp at the jack,
which in a 16-bit WAV is about 17 LSB peak -- 4 bits of resolution on the
waveform, and the quantisation noise lands in band. Written as 32-bit PCM the
problem disappears.

Outputs:
    spike_stimulus.wav      the train, for pw-play
    spike_template.csv      t_s, v_uv           one spike, as generated
    spike_stimulus.json     everything needed to recover the timing later
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FS_WAV = 44100
FULL_SCALE_VRMS = 1.0        # same assumption as sine_out.sh; --ratio absorbs
                             # any error in it, because the ratio is measured
                             # against this same nominal scale


def extracellular_spike(fs, stretch=1.0, trough_fwhm_ms=0.30,
                        hump_delay_ms=0.55, hump_fwhm_ms=0.60, hump_frac=0.45,
                        foot_delay_ms=-0.25, foot_fwhm_ms=0.25, foot_frac=0.08,
                        pad_ms=0.35):
    """One extracellular action potential, unit peak-to-peak.

    Three Gaussians: the negative trough, the slower positive repolarisation
    hump after it, and the small positive foot before it. Times are given for
    the real spike and multiplied by `stretch`."""
    g = lambda t, t0, fwhm: np.exp(-4 * math.log(2) * ((t - t0) / fwhm) ** 2)
    s = stretch
    trough_w = trough_fwhm_ms * s * 1e-3
    total = (foot_delay_ms - 2 * foot_fwhm_ms,
             hump_delay_ms + 2 * hump_fwhm_ms + pad_ms)
    t0, t1 = (total[0] * s * 1e-3, total[1] * s * 1e-3)
    n = int(round((t1 - t0) * fs))
    t = t0 + np.arange(n) / fs
    v = (-g(t, 0.0, trough_w)
         + hump_frac * g(t, hump_delay_ms * s * 1e-3, hump_fwhm_ms * s * 1e-3)
         + foot_frac * g(t, foot_delay_ms * s * 1e-3, foot_fwhm_ms * s * 1e-3))
    v = v - v[0]
    v = v / np.ptp(v)                      # unit peak-to-peak, trough to hump
    return t - t0, v


def load_template(path, fs, stretch):
    """A real spike from CSV (t_s, v_uv), resampled onto the WAV grid."""
    import csv as _csv
    tt, vv = [], []
    with open(path) as fh:
        for r in _csv.DictReader(fh):
            tt.append(float(r["t_s"])); vv.append(float(r["v_uv"]))
    tt = np.asarray(tt) * stretch
    vv = np.asarray(vv)
    n = int(round((tt[-1] - tt[0]) * fs))
    grid = tt[0] + np.arange(n) / fs
    v = np.interp(grid, tt, vv)
    v = v - v[0]
    return grid - grid[0], v / np.ptp(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--uvpp", type=float, default=400.0,
                    help="spike amplitude at the CHIP, peak-to-peak, in uV")
    ap.add_argument("--rate", type=float, default=3.7,
                    help="firing rate of the train in Hz. NOT 4.0: at a 250 ms "
                         "interval, 60 Hz mains is exactly 15 cycles, so every "
                         "sweep starts on the same mains phase and the hum adds "
                         "coherently through the average instead of falling as "
                         "1/sqrt(N). Measured on synthetic data, that inflated "
                         "the recovered gain by 54%%. Keep 50/rate and 60/rate "
                         "well away from integers")
    ap.add_argument("--repeats", type=int, default=120,
                    help="spikes in the file. The output is ~90 mVpp against "
                         "~12 mV rms of node noise, so the single spike is "
                         "visible but ugly; averaging N of them buys sqrt(N)")
    ap.add_argument("--stretch", type=float, default=50.0,
                    help="time dilation. 1 = real time, which the 1 kS/s "
                         "digitiser cannot record")
    ap.add_argument("--ratio", type=float, default=0.50,
                    help="measured jack-to-chip ratio at the nominal scale")
    ap.add_argument("--template", default="", help="CSV t_s,v_uv of a real spike")
    ap.add_argument("--jitter", type=float, default=0.15,
                    help="fractional jitter on the inter-spike interval, so "
                         "the train is not perfectly periodic (0 = a metronome)")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--wav", default=os.path.join(HERE, "spike_stimulus.wav"))
    a = ap.parse_args()

    if a.template:
        t, v = load_template(a.template, FS_WAV, a.stretch)
        src = os.path.basename(a.template)
    else:
        t, v = extracellular_spike(FS_WAV, stretch=a.stretch)
        src = "synthetic triphasic"

    chip_vpp = a.uvpp * 1e-6
    jack_vpp = chip_vpp / a.ratio
    amp_fs = (jack_vpp / 2) / (FULL_SCALE_VRMS * math.sqrt(2))
    if amp_fs > 1.0:
        sys.exit(f"needs {amp_fs:.2f} of full scale -- lower --uvpp")

    for line_hz in (50.0, 60.0):
        cyc = line_hz / a.rate
        if abs(cyc - round(cyc)) < 0.06:
            print(f"  WARNING: {line_hz:g} Hz mains is {cyc:.2f} cycles per "
                  f"interval -- near-integer, so hum will survive the average. "
                  f"Move --rate.")
    period = 1.0 / a.rate
    spike_n = len(v)
    if spike_n / FS_WAV > period:
        sys.exit(f"the spike is {spike_n/FS_WAV*1e3:.0f} ms but the interval is "
                 f"{period*1e3:.0f} ms -- lower --rate or --stretch")

    rng = np.random.default_rng(a.seed)
    total_n = int(round(a.repeats * period * FS_WAV)) + spike_n
    train = np.zeros(total_n)
    onsets = []
    for k in range(a.repeats):
        c = k * period
        if a.jitter:
            c += rng.uniform(-a.jitter, a.jitter) * period
        i = int(round(max(c, 0.0) * FS_WAV))
        if i + spike_n > total_n:
            break
        train[i:i + spike_n] += v
        onsets.append(i / FS_WAV)

    # Unit-peak-to-peak template -> the requested chip amplitude. Scale by the
    # TEMPLATE's span rather than the train's, so overlapping spikes (if any) stay
    # quietly rescale every spike.
    train = train * (2 * amp_fs)           # v spans 1.0 peak-to-peak
    peak = float(np.max(np.abs(train)))
    if peak > 1.0:
        sys.exit(f"train peaks at {peak:.2f} of full scale -- lower --uvpp")

    import soundfile as sf
    sf.write(a.wav, train.astype(np.float32), FS_WAV, subtype="PCM_32")

    with open(os.path.join(HERE, "spike_template.csv"), "w") as fh:
        fh.write("t_s,v_uv\n")
        for tt, vv in zip(t, v * a.uvpp):
            fh.write(f"{tt:.6f},{vv:.4f}\n")
    meta = {"uvpp_chip": a.uvpp, "rate_hz": a.rate, "repeats": len(onsets),
            "stretch": a.stretch, "ratio": a.ratio, "jack_vpp": jack_vpp,
            "amp_fs": amp_fs, "period_s": period, "onsets_s": onsets,
            "spike_s": spike_n / FS_WAV, "fs_wav": FS_WAV, "source": src,
            "wav": os.path.basename(a.wav)}
    with open(os.path.join(HERE, "spike_stimulus.json"), "w") as fh:
        json.dump(meta, fh, indent=2)

    trough_ms = 0.30 * a.stretch
    print(f"spike: {src}, stretched {a.stretch:g}x")
    print(f"  one spike {spike_n/FS_WAV*1e3:7.1f} ms   trough FWHM "
          f"{trough_ms:.1f} ms   dominant ~{1/(2*trough_ms*1e-3):.0f} Hz")
    print(f"  {a.uvpp:.0f} uVpp at the chip  ->  jack {jack_vpp*1e3:.3f} mVpp "
          f"({amp_fs:.5f} of full scale, ratio {a.ratio:g})")
    print(f"  train: {len(onsets)} spikes at {a.rate:g} Hz = "
          f"{total_n/FS_WAV:.1f} s"
          + (f", jitter +-{a.jitter*100:.0f}%" if a.jitter else ""))
    if a.stretch == 1:
        print("  WARNING: real time. The 1 kS/s pixhawk cannot record this -- "
              "it needs a fast scope on the output.")
    exp_out = a.uvpp * 1e-6 * 235
    print(f"  expected LNA output ~{exp_out*1e3:.0f} mVpp at 235x, against "
          f"~12 mV rms node noise (single-spike SNR ~{exp_out/0.012:.0f})")
    print(f"\nwav: {a.wav}\njson: spike_stimulus.json\ntemplate: spike_template.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
