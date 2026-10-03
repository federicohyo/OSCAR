#!/usr/bin/env python3
"""Build the replay stimulus for the pad-to-neuron chain, from real pad data.

    ../.venv-meas/bin/python3 saline_stimulus.py

Same trick as odor_stimulus.py, with one change that matters: the input shape is
not a synthetic mimic of a published trace but the measured saline injection of
Fig. 16/17 -- the second injection of scope_20260829_103015.csv (the dilute3x
run, biases LNA_chip0_pad_wet_diluted3x.biases, lna_iref = 1.157 V): -398 mV at
the pad-amplifier output, settled back within 20 mV after 106 ms.

What the detector in odor_neuron_loop*.py fires on is a POSITIVE excess of the
amplifier output over its trailing baseline, and the amplifier inverts. To keep
that loop bit-identical, the waveform is replayed with its sign flipped
(--same-sign to keep the physical sign): on silicon the output excursion is
upward, exactly as in the odor runs. The figure panel (a) draws the recorded,
physical sign; the flip is stated in the caption.

The recorded trace is an OUTPUT -- the true surface-potential step high-passed
once by the pad amplifier (fc = 1.53 Hz) and scaled by its gain. Replaying that
trace electrically into the connector-fed amplifier would high-pass it a second
time. Instead the input-referred surface step is recovered first (divide the
recorded spectrum by H(f) = -G(jf/fc)/(1+jf/fc) on a --band interval, exactly
the make_fig10 recovery), and it is THAT signal that is played. The amplifier
then re-applies one high-pass and the replayed output should reproduce the
recorded event -- the self-check below simulates the replay and scores it.

G = 268 is the gain measured at V_iref = 1.079 V, not the 1.157 V of the
recording (flagged in tio2_dilute3x_panel.py), so the absolute input-referred
amplitude is provisional; the default --chip-vpp 1.50 mVpp replays the event at
unity under that gain. At the high-gain setting the clean input ceiling is
~0.9 mVpp -- if the replay must stay in the verified-linear span, lower
--chip-vpp (e.g. --chip-vpp 0.0009) or lower the gain (V_iref) on the bench.

Outputs:
    saline_stimulus.wav    bench playback, same marker layout as odor_stimulus
    saline_timing.json     same keys the loop scripts read
    saline_event.csv       the windowed event: recorded output (raw + 21 ms
                           smoothed) and the replayed chip input
"""
import argparse, csv, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from odor_stimulus import write_wav, preemphasis, FS_WAV

CSV = os.path.join(HERE, "..", "data",
                   "scope_20260829_103015.csv")
FS = 1000.0            # the scope record
GAIN, FC = 268.0, 1.53 # measured pad-amp gain (at the OTHER V_iref) and corner
TAP_S = 0.010          # edge taper on the windowed stimulus


def load_event(csv_path, t_event, pre, post):
    d = np.genfromtxt(csv_path, delimiter=",", names=True)
    t = (d["sample_index"] - d["sample_index"][0]) / FS
    pad = d["volts_ch2"]                    # pad-amplifier output, V
    sm = np.convolve(pad, np.ones(21) / 21, "same")
    m = (t >= t_event - pre) & (t < t_event + post)
    tt = t[m] - t_event                     # 0 at the dip
    raw = pad[m] - np.median(
        sm[m][tt < -0.05])                  # baseline = pre-event median, raw kept
    out = sm[m] - np.median(sm[m][tt < -0.05])
    return tt, out, raw                     # out = smoothed, baseline-subtracted


def input_refer(tt, out, f_lo, f_hi, gain=GAIN, fc=FC):
    """Recover the surface-potential step from the recorded output.

    out(f) = -gain (jf/fc)/(1+jf/fc) in(f); divide on [f_lo, f_hi], zero
    outside, so the replay's own high-pass restores the recorded shape."""
    n = len(out)
    fr = np.fft.rfftfreq(n, 1.0 / FS)
    H = -gain * (1j * fr / fc) / (1 + 1j * fr / fc)
    Y = np.fft.rfft(out)
    X = np.zeros_like(Y)
    band = (fr >= f_lo) & (fr <= f_hi)
    X[band] = Y[band] / H[band]
    return np.fft.irfft(X, n)               # volts, at the pad surface


def taper(v, fs, s=TAP_S):
    k = max(1, int(s * fs))
    w = np.ones(len(v))
    rmp = 0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)
    w[:k], w[-k:] = rmp, rmp[::-1]
    return v * w


def selfcheck(tt, out_recorded, v_chip_played, gain=GAIN, fc=FC):
    """Simulate the replay: played chip input through one amp high-pass, and
    compare with the recorded event in the same window."""
    n = len(tt)
    fr = np.fft.rfftfreq(n, 1.0 / FS)
    H = gain * (1j * fr / fc) / (1 + 1j * fr / fc)          # signed magnitude
    y = np.fft.irfft(np.fft.rfft(v_chip_played) * H, n)     # signed |H|
    # The bench plays the sign-flipped step, and the amplifier inverts, so the
    # replayed output excursion is UPWARD while the recorded one was downward.
    # Compare like with like: replayed physical output vs the flipped record.
    a, b = -y, -out_recorded
    a -= np.median(a[tt < -0.05]); b = b - np.median(b[tt < -0.05])
    r = float(np.corrcoef(a, b)[0, 1]); pk = float(a.max() / b.max())
    print(f"self-check: replayed vs recorded (sign-aligned) r = {r:.3f}; "
          f"replayed peak {a.max()*1e3:.0f} mV out vs recorded {b.max()*1e3:.0f} mV")
    return r, pk


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", default=CSV)
    ap.add_argument("--event-time", type=float, default=16.985,
                    help="dip time of the injection in the record [s]")
    ap.add_argument("--pre", type=float, default=0.35)
    ap.add_argument("--post", type=float, default=1.15)
    ap.add_argument("--band", type=float, nargs=2, default=(0.35, 40.0),
                    help="inversion band [Hz]")
    ap.add_argument("--chip-vpp", type=float, default=None,
                    help="peak-to-peak at the chip input [V]. Default: unity "
                         "replay -- the input-referred step's own span "
                         "(~1.15 mVpp). At the high-gain setting the clean "
                         "input ceiling is ~0.9 mVpp: lower this or V_iref.")
    ap.add_argument("--repeats", type=int, default=10)
    ap.add_argument("--same-sign", action="store_true",
                    help="play the physically-signed step (the loop detector "
                         "will NOT fire: it needs an upward output excursion)")
    ap.add_argument("--preemph", action="store_true", default=True)
    ap.add_argument("--no-preemph", dest="preemph", action="store_false")
    ap.add_argument("--stem", default=os.path.join(HERE, "saline_stimulus"))
    a = ap.parse_args()

    tt, out, raw = load_event(a.csv, a.event_time, a.pre, a.post)
    v_in = input_refer(tt, out, *a.band)
    print(f"event @ {a.event_time:.3f} s: recorded dip {1e3*out.min():+.0f} mV "
          f"-> input-referred step {1e6*v_in.max():.0f} uV (G={GAIN:.0f} "
          f"assumed; provisional at this V_iref)")

    v_play = v_in if a.same_sign else -v_in
    v_play = taper(v_play, FS)
    v_play = v_play - v_play.mean()
    chip_vpp = a.chip_vpp or float(np.ptp(v_play))    # unity replay by default
    v_play = v_play / (np.ptp(v_play) / 2) * (chip_vpp / 2)

    r, pk = selfcheck(tt, out, v_play if not a.same_sign else -v_play)
    print(f"chip input: {chip_vpp*1e6:.0f} uVpp"
          + (" (unity replay)" if a.chip_vpp is None else " (requested)"))

    # upsample to the WAV rate, optional source pre-emphasis (as odor_stimulus)
    t44 = np.arange(0, tt[-1], 1.0 / FS_WAV)
    v44 = np.interp(t44, tt, v_play)
    if a.preemph:
        ref = os.path.join(HERE, "lna_transfer_ref.csv")
        if os.path.exists(ref):
            v44 = preemphasis(t44, v44, ref)
            print("pre-emphasis: source response divided out")
        else:
            print("pre-emphasis skipped (no lna_transfer_ref.csv)")

    os.environ["ODOR_REPEATS"] = str(a.repeats)
    jack, fs_amp, (t_mark, t_stim, dur, period, reps) = write_wav(
        a.stem + ".wav", t44, v44, chip_vpp)
    ev_on = t_stim + a.pre                  # dip position within each period
    print(f"wav: jack {jack:.4f} Vpp ({fs_amp:.4f} full scale), "
          f"{reps} repeats x {period:.3f} s = {dur:.2f} s total")
    with open(HERE + "/saline_timing.json", "w") as f:
        json.dump({"t_mark": t_mark, "mark_hz": 137.0, "mark_s": 0.05,
                   "t_odor": t_stim, "wav_s": dur, "period_s": period,
                   "repeats": reps, "chip_vpp": chip_vpp,
                   "event_on": ev_on, "event_off": ev_on + 0.106,
                   "source_csv": os.path.basename(a.csv),
                   "source_event_s": a.event_time,
                   "note": "replayed pad event; sign flipped so the inverting "
                           "amp gives an upward excursion"}, f, indent=2)

    with open(HERE + "/saline_event.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "pad_out_recorded_mv", "pad_out_smoothed_mv",
                    "surface_input_uv", "chip_input_played_mv"])
        for i in range(len(tt)):
            w.writerow([f"{tt[i]:.4f}", f"{1e3*raw[i]:.3f}",
                        f"{1e3*out[i]:.3f}", f"{1e6*v_in[i]:.3f}",
                        f"{1e3*v_play[i]:.6f}"])
    print("csv: saline_event.csv | timing: saline_timing.json | "
          f"replay shape check r={r:.3f} peak={pk:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
