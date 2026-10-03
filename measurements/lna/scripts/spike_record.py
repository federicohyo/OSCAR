#!/usr/bin/env python3
"""Play the spike train into the LNA and recover it from the output.

    CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 spike_record.py --uvpp 400

    ch1 = LNA output      ch2 = the input side (see --divider)

A single 400 uVpp spike comes out at ~90 mVpp against ~12 mV rms of noise on
that node -- visible, but too ugly to show anyone. So the train is repeated and
the recorded sweeps are AVERAGED, which is what electrophysiology does with the
same problem and for the same reason: the spike is identical every time and the
noise is not, so N repeats buy sqrt(N).

WHY IT MEASURES THE LEVEL INSTEAD OF TRUSTING IT. The jack-to-chip ratio is not
a constant of the bench -- it drifted 0.48 -> 0.55 across one morning, because
it folds in the sound card's output level and not just the divider. So this
plays a large sine first, reads the ratio off ch2 where ch2 is well above its
own noise, and only then builds the train. A stored ratio is how a stimulus
meant for 0.55 mVpp ends up at 9.8 mVpp, past this chip's saturation onset.

ALIGNMENT is by matched filter, not by playback timing. pw-play's latency is
0.32-0.36 s here and jitters by more than a second, and the sound card's clock
and the digitiser's clock are independent, so a train that is exactly periodic
in the file is not exactly periodic in the recording. Each spike is found
individually by correlating against the known template, so clock drift costs
nothing.

POLARITY is measured, not assumed: the correlation is tried both ways and the
larger response wins. An inverting amplifier is expected and is not an error.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lna_audio_sweep import (make_wav, AudioOut, decommensurate, halfwave_fit,
                             sine_fit, BOARD_DT)
from lna_bringup_check import Scope2

FS = 1.0 / BOARD_DT
PY = sys.executable


def measure_ratio(sc, audio, wavdir, jack_vpp, f_nom, settle, window, divider):
    """jack level -> volts at the chip, read where ch2 is well above its noise."""
    f0 = decommensurate(f_nom)
    wav = os.path.join(wavdir, f"cal_{f0:.2f}hz_{jack_vpp:.4f}vpp.wav")
    if not os.path.exists(wav):
        make_wav(wav, f0, jack_vpp, min_dur=settle + 3 * window + 4)
    audio.play(wav)
    sc.drain(settle)
    vals = []
    for _ in range(3):
        t, c1, c2 = sc.collect2(window)
        fit = halfwave_fit(t, c2, f0)
        if fit:
            vals.append(fit["vpp"])
    audio.stop()
    if not vals:
        return None
    at_chip = float(np.median(vals)) * divider
    return at_chip / jack_vpp


def matched_filter(v, tmpl):
    """Correlation of `v` with `tmpl`, both mean-removed, normalised."""
    a = v - v.mean()
    b = tmpl - tmpl.mean()
    b = b / (np.linalg.norm(b) or 1.0)
    return np.correlate(a, b, mode="valid")


def find_spikes(v, tmpl, period_n, expect):
    """Peak positions of the matched filter, and the polarity that won."""
    c = matched_filter(v, tmpl)
    pol = 1.0 if c.max() >= -c.min() else -1.0
    cc = c * pol
    idx, guard = [], int(period_n * 0.6)
    work = cc.copy()
    for _ in range(expect):
        i = int(np.argmax(work))
        if work[i] <= 0:
            break
        idx.append(i)
        work[max(0, i - guard):i + guard] = -np.inf
    return sorted(idx), pol, cc


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--uvpp", type=float, default=400.0)
    ap.add_argument("--rate", type=float, default=4.0)
    ap.add_argument("--repeats", type=int, default=120)
    ap.add_argument("--stretch", type=float, default=50.0)
    ap.add_argument("--divider", type=float, default=1.0,
                    help="chip input = this times ch2. 1.0 when ch2 is on the "
                         "amplifier input; the resistive ratio when it is "
                         "upstream of the divider")
    ap.add_argument("--cal-jack-vpp", type=float, default=1.0,
                    help="level for the ratio measurement -- large, so ch2 is "
                         "far above its own 4 mV of noise")
    ap.add_argument("--cal-hz", type=float, default=20.0)
    ap.add_argument("--ratio", type=float, default=0.0,
                    help="skip the calibration and use this ratio")
    ap.add_argument("--settle", type=float, default=12.0)
    ap.add_argument("--out", default=os.path.join(HERE, "spike_record.npz"))
    ap.add_argument("--png", default=os.path.join(HERE, "figures",
                                                  "spike_recovered.png"))
    a = ap.parse_args()

    subprocess.run(["pkill", "-f", "[p]w-play"], capture_output=True)
    try:
        sc = Scope2()
    except Exception as e:
        sys.exit(f"ERROR: no scope server on 127.0.0.1:5555 ({e})\n"
                 "       start it with:\n"
                 "         ../.venv-meas/bin/python3 "
                 "../ofxLPM/scope-pixhawk/tools/server.py")
    wavdir = os.path.join(HERE, "wavs_spike")
    os.makedirs(wavdir, exist_ok=True)
    audio = AudioOut()

    # -------------------------------------------------- 1. the level
    if a.ratio > 0:
        ratio = a.ratio
        print(f"[1/3] ratio: {ratio:.4f} (given, not measured)")
    else:
        print(f"[1/3] ratio: measuring at {a.cal_hz:g} Hz, "
              f"{a.cal_jack_vpp:g} Vpp jack")
        ratio = measure_ratio(sc, audio, wavdir, a.cal_jack_vpp, a.cal_hz,
                              a.settle, 4.0, a.divider)
        if not ratio:
            sys.exit("ERROR: ch2 saw nothing during the ratio measurement")
        print(f"      jack -> chip = {ratio:.4f}   "
              f"({a.uvpp:g} uVpp needs {a.uvpp*1e-6/ratio*1e3:.3f} mVpp at the jack)")

    # -------------------------------------------------- 2. build and play
    print(f"[2/3] building the train and playing it")
    r = subprocess.run(
        [PY, os.path.join(HERE, "spike_stimulus.py"),
         "--uvpp", str(a.uvpp), "--rate", str(a.rate),
         "--repeats", str(a.repeats), "--stretch", str(a.stretch),
         "--ratio", f"{ratio:.6f}"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ERROR: spike_stimulus.py failed:\n{r.stdout}{r.stderr}")
    for line in r.stdout.strip().splitlines():
        print("      " + line)
    meta = json.load(open(os.path.join(HERE, "spike_stimulus.json")))

    audio.play(os.path.join(HERE, meta["wav"]))
    sc.drain(2.0)                                   # skip the playback latency
    dur = meta["repeats"] * meta["period_s"] + 2.0
    t, c1, c2 = sc.collect2(dur)
    audio.stop()
    print(f"      recorded {len(c1)} samples, {t[-1]-t[0]:.1f} s")

    # -------------------------------------------------- 3. average
    tt, tv = [], []
    with open(os.path.join(HERE, "spike_template.csv")) as fh:
        next(fh)
        for line in fh:
            x, y = line.split(",")
            tt.append(float(x)); tv.append(float(y))
    tt, tv = np.asarray(tt), np.asarray(tv)
    n_t = int(round((tt[-1] - tt[0]) * FS))
    tmpl = np.interp(np.arange(n_t) / FS, tt, tv)   # template on the 1 kHz grid

    period_n = int(round(meta["period_s"] * FS))
    idx, pol, cc = find_spikes(c1, tmpl, period_n, meta["repeats"])
    print(f"[3/3] matched filter found {len(idx)} spikes, polarity "
          f"{'INVERTING' if pol < 0 else 'non-inverting'}")
    if len(idx) < 5:
        sys.exit("ERROR: too few spikes found -- is the drive reaching the chip?")

    pre = int(0.25 * n_t)
    seg = []
    for i in idx:
        s0, s1 = i - pre, i - pre + n_t + 2 * pre
        if s0 < 0 or s1 > len(c1):
            continue
        w = c1[s0:s1]
        seg.append(w - np.median(w[:pre]))           # baseline from before it
    seg = np.asarray(seg)
    avg = seg.mean(axis=0)
    t_seg = (np.arange(len(avg)) - pre) / FS

    # Amplitude by projecting the average onto the template, not by its
    # peak-to-peak. Anything left in the average that is NOT spike-shaped --
    # residual hum above all -- lands in the residual instead of being read as
    # signal. Peak-to-peak cannot tell them apart, and on synthetic data with
    # mains coherent to the repetition rate it read the gain 54% high.
    ref = np.interp(t_seg, tt, tv, left=0.0, right=0.0)
    ref = ref - ref.mean()
    scale = float(np.dot(avg - avg.mean(), ref) / np.dot(ref, ref))
    fit_resid = float(np.std(avg - avg.mean() - scale * ref))
    single_pp = float(np.median([np.ptp(s) for s in seg]))
    avg_pp = float(np.ptp(avg))
    resid = seg - avg
    noise_1 = float(resid.std())
    print(f"      single-sweep {single_pp*1e3:7.2f} mVpp,  "
          f"average of {len(seg)}: {avg_pp*1e3:7.2f} mVpp")
    print(f"      noise per sweep {noise_1*1e3:.2f} mV rms  ->  "
          f"{noise_1/math.sqrt(len(seg))*1e3:.3f} mV in the average")
    print(f"      SNR  single {single_pp/noise_1:5.1f}  ->  "
          f"averaged {avg_pp/(noise_1/math.sqrt(len(seg))):6.0f}")
    gain = abs(scale) * 1e6                       # template is in uV
    print(f"      gain on the spike: {gain:.0f}x = "
          f"{20*math.log10(gain):.2f} dB   (template projection)")
    print(f"      peak-to-peak of the average would say "
          f"{avg_pp/(a.uvpp*1e-6):.0f}x -- the gap is whatever survives the "
          f"average without being spike-shaped")
    print(f"      unmodelled residual in the average: {fit_resid*1e3:.3f} mV rms")

    np.savez(a.out, t_seg=t_seg, avg=avg, sweeps=seg, template_t=tt,
             template_uv=tv, ratio=ratio, polarity=pol, uvpp=a.uvpp,
             gain=gain, n=len(seg), raw_t=t, raw_ch1=c1, raw_ch2=c2,
             meta=json.dumps(meta))
    print(f"\ndata: {a.out}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(3, 1, figsize=(7.5, 8))
        ax[0].plot(tt * 1e3, tv, color="C3", lw=1.4)
        ax[0].set_ylabel("input [$\\mu$V]")
        ax[0].set_title(f"{a.uvpp:.0f} $\\mu$Vpp extracellular spike, "
                        f"{meta['stretch']:g}x time-stretched", fontsize=10)
        for s in seg[:40]:
            ax[1].plot(t_seg * 1e3, s * 1e3, color="0.75", lw=0.5)
        ax[1].plot(t_seg * 1e3, avg * 1e3, color="C0", lw=1.6)
        ax[1].set_ylabel("LNA output [mV]")
        ax[1].legend(["single sweeps", f"average of {len(seg)}"], fontsize=8)
        ref = avg / gain * 1e6
        ax[2].plot(t_seg * 1e3, ref, color="C0", lw=1.4, label="recovered")
        ax[2].plot(tt * 1e3, tv * pol, color="C3", lw=1.2, ls="--",
                   label="input" + (" (inverted)" if pol < 0 else ""))
        ax[2].set_ylabel("input-referred [$\\mu$V]")
        ax[2].set_xlabel("time [ms]")
        ax[2].legend(fontsize=8)
        for x in ax:
            x.grid(True, alpha=0.3)
        os.makedirs(os.path.dirname(a.png), exist_ok=True)
        fig.tight_layout()
        fig.savefig(a.png, dpi=150)
        print(f"figure: {a.png}")
    except Exception as e:
        print(f"plot skipped: {e}")
    finally:
        sc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
