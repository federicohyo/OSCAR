#!/usr/bin/env python3
"""Bring the LNA to its working point and prove it is there.

Called by LNA_bringup.sh -- run that rather than this, unless the firmware is already
flashed and the clock already engaged.

    ch1 = LNA output        ch2 = LNA input (amplifier pin 4)

Four steps:

  1. BIASES + SETTLE. Applies a named .biases file over the FTDI (all 24 DAC
     channels, NMOS/PMOS references as neuron_bridge does it) and then waits.
     The output DC needs ~35-40 s after any bias change; measure sooner and the
     gain scatters 30-50% while looking entirely plausible (lna_settling.csv).

  2. NOISE, no drive. Records ch1 with the audio path silent. The pass/fail
     number is the BROADBAND rms with the mains lines removed: 50/60 Hz and
     their harmonics are room pickup rather than the amplifier. Total rms and
     peak-to-peak are printed too, because they are what a scope shows.

     A quiet output leaves the amplifier's health open -- a dead LNA is
     quiet and sits at ~1.80 V. Hence the DC check alongside.

  3. GAIN at three tones, small drive. Coherent least-squares sine fit on ch1
     at the known drive frequency rather than a peak-to-peak or percentile spread:
     with the tone off this node already carries ~50-66 mVpp of hum, which a
     spread estimator turns into a fake ~19 dB gain floor. Test frequencies are
     nudged off any simple ratio with the 1 kS/s sampler (decommensurate());
     100.000 Hz sampled at 1000 S/s repeats the same 10 phases forever.

  4. INPUT CALIBRATION, large drive, LAST. What the chip is actually fed is too weak to
     be read at the level step 3 drives it: gain is ~220x, so a clean output
     (<800 mVpp) needs ~3 mVpp in, and ch2 carries ~4 mV rms of its own noise
     on an 0.805 mV/step unipolar ADC. So the jack->chip ratio is measured
     where ch2 is well resolved -- a large tone, ~400 mVpp at the input -- and
     applied to the small drive. The divider is resistive, so the ratio holds;
     measuring it PER FREQUENCY also divides out the sound card's own roll-off.

     It runs last on purpose: a large tone slams the output into the rail, and
     the recovery would contaminate step 3's DC.

     ch2 is AC-coupled and swings about 0 V, so the unipolar ADC keeps only its
     positive half -- fitted with halfwave_fit() rather than sine_fit().

Read-only on the chip apart from the DAC write in step 1. It writes whatever
the .biases file holds, which is why the file matters: several files in this
tree switch the amplifier off (lna_iref/TUNEp/VB1/VB2/VREF) despite their names.
"""
import argparse
import json
import math
import os
import socket
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lna_audio_sweep import (Scope, longest_contiguous, sine_fit, halfwave_fit,
                             make_wav, AudioOut, decommensurate, BOARD_DT)
from lna_freq_sweep import apply_bias_dict
from lna_gain_tune import DACs

FS = 1.0 / BOARD_DT
DEAD_DC_V = 1.75        # output DC above this = amplifier off (dead reads 1.80)
MIN_GAIN_X = 10.0       # below this it stops behaving as an amplifier
MAX_H2_PCT = 5.0        # above this the output is clipping, so the gain is a lie
MAX_SPREAD_PCT = 10.0   # repeat-to-repeat gain spread that still counts as settled


class Scope2(Scope):
    """Three-field variant of the stream: 't,ch1,ch2' instead of 't,v'.

    Subclassed rather than changed in place: lna_audio_sweep.Scope is imported
    by every other measurement script here."""

    def _read(self):
        rec = []
        try:
            chunk = self.sk.recv(65536)
        except (socket.timeout, TimeoutError):
            return rec
        if not chunk:
            raise RuntimeError("scope server closed the connection")
        self.buf += chunk
        *done, self.buf = self.buf.split(b"\n")
        for ln in done:
            if self._first:            # truncated fragment -- discard
                self._first = False
                continue
            q = ln.decode(errors="replace").strip().split(",")
            if len(q) >= 3:
                try:
                    rec.append((float(q[0]), float(q[1]), float(q[2])))
                except ValueError:
                    pass
        return rec

    def collect2(self, seconds):
        """Longest gap-free run of both channels, on a reconstructed 1 ms axis.

        longest_contiguous() is reused verbatim by handing it the sample INDEX
        as its value column -- what comes back is the surviving index range,
        which then slices both channels identically."""
        rec = []
        t0 = time.time()
        while time.time() - t0 < seconds:
            rec.extend(self._read())
        if len(rec) < 20:
            raise RuntimeError(f"scope stalled ({len(rec)} samples in {seconds:.1f} s)")
        a = np.asarray(rec, dtype=float)
        t, idx = longest_contiguous(a[:, 0], np.arange(len(a), dtype=float))
        i = idx.astype(int)
        return t, a[i, 1], a[i, 2]


def mains_excluded_rms(v, mains=(50.0, 60.0), nperseg=4096, band=(0.2, 500.0)):
    """Broadband rms of `v` with the mains lines and their harmonics removed.

    Returns (rms_excluding_mains, rms_of_the_mains_lines_alone)."""
    from scipy.signal import welch
    nps = int(min(nperseg, max(256, len(v) // 4)))
    fr, pxx = welch(v - v.mean(), fs=FS, nperseg=nps, noverlap=nps // 2,
                    window="hann", detrend="linear")
    df = float(fr[1] - fr[0])
    line = np.zeros_like(fr, bool)
    for f_line in mains:
        for h in range(1, int(FS / 2 / f_line) + 1):
            line |= np.abs(fr - h * f_line) < max(0.5, 3 * FS / nps)
    inband = (fr >= band[0]) & (fr <= band[1])
    # Sum x df, rather than trapz over the surviving bins: dropping the mains bins from
    # the array leaves a ~1.5 Hz hole that trapz then spans with a straight line
    # between the two flanks of the peak -- which adds most of the hum back.
    # Measured 14.90 mV with mains masked against a 13.62 mV total that included
    # it. The rectangular rule over a masked spectrum is exact for Welch.
    rms = lambda m: math.sqrt(float(np.sum(pxx[m])) * df) if m.sum() else float("nan")
    return rms(inband & ~line), rms(inband & line)


def play_and_fit(sc, audio, wavdir, f0, jack_vpp, settle, window, reps, fit_fn,
                 chan, min_dur_extra=3.0):
    """Play one tone and fit `reps` back-to-back windows of one channel.

    Repeats are the guard the bench rule asks for: an unsettled node, or a
    playback hiccup, shows up as scatter between windows rather than as one
    plausible off number."""
    # The duration is in the NAME: the file must outlast settle+windows, and a
    # cache keyed on (freq, level) alone would hand a longer run a short file.
    # pw-play relaunches when one ends, and the ~100 ms gap that leaves cost 17%
    # of the amplitude the one time it landed inside a window.
    min_dur = settle + reps * window + min_dur_extra
    wav = os.path.join(
        wavdir, f"tone_{f0:.2f}hz_{jack_vpp:.5f}vpp_{min_dur:.0f}s.wav")
    if not os.path.exists(wav):     # leave a file pw-play may hold open untouched
        make_wav(wav, f0, jack_vpp, min_dur=min_dur)
    audio.play(wav)
    sc.drain(settle)                # drains the socket instead of sleeping on it
    fits = []
    for _ in range(reps):
        t, c1, c2 = sc.collect2(window)
        f = fit_fn(t, c1 if chan == 1 else c2, f0)
        if f is not None:
            fits.append(f)
    if not fits:
        return None, []
    med = sorted(fits, key=lambda f: f["vpp"])[len(fits) // 2]
    return med, [f["vpp"] for f in fits]


def spread_pct(vals, robust=False):
    """Repeat-to-repeat scatter as a percentage of the median.

    max-min is the honest statistic for 3 windows, where one bad one moves the
    median. With 5 or more the median already rejects a single outlier, so
    max-min then reports a scatter that has been corrected for and fires the
    warning on every run -- which just trains you to ignore it. `robust` uses
    the MAD instead, scaled so it reads as a standard deviation for clean data:
    it stays small when only the median matters and one window misbehaved."""
    v = np.asarray(vals, dtype=float)
    m = float(np.median(v))
    if not m:
        return float("nan")
    if robust and len(v) >= 5:
        return float(1.4826 * np.median(np.abs(v - m))) / m * 100
    return (float(v.max()) - float(v.min())) / m * 100


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bias", default=os.path.join(
        HERE, "biases", "bias_LNA_50dB-neuron9-16Hz.biases"),
        help="operating point to load (all 24 DAC channels)")
    ap.add_argument("--settle", type=float, default=40.0,
                    help="seconds to settle after the bias write "
                         "(README: 35-40 s; 30 is the shortest defensible)")
    ap.add_argument("--noise-s", type=float, default=30.0,
                    help="silent capture length for the noise check")
    ap.add_argument("--noise-limit-mv", type=float, default=55.0,
                    help="pass/alert on the mains-masked output rms")
    ap.add_argument("--freqs", default="80,100,150", help="test tones in Hz")
    ap.add_argument("--tone-s", type=float, default=4.0, help="fit window")
    ap.add_argument("--reps", type=int, default=3, help="fit windows per tone")
    ap.add_argument("--cal-reps", type=int, default=5,
                    help="fit windows per calibration tone. More than --reps: "
                         "ch2 is the noisy side, and the median of an odd "
                         "number of windows is what absorbs a bad one")
    ap.add_argument("--tone-settle", type=float, default=4.0,
                    help="settle before each tone after the first")
    ap.add_argument("--first-settle", type=float, default=30.0,
                    help="settle before the FIRST tone: the drive level change "
                         "moves the output DC, the frequency changes do not")
    ap.add_argument("--jack-vpp", type=float, default=0.007,
                    help="drive for the gain pass, Vpp at the jack. 0.007 puts "
                         "~760 mVpp on the output at ~220x, h2 < 0.5%%")
    ap.add_argument("--cal-jack-vpp", type=float, default=1.0,
                    help="drive for the input calibration, Vpp at the jack -- "
                         "large, so ch2 is far above its own noise")
    ap.add_argument("--ratio", type=float, default=0.0,
                    help="skip the calibration pass and use this jack->chip "
                         "ratio instead")
    ap.add_argument("--skip-bias", action="store_true",
                    help="measure only; leave the DACs alone")
    ap.add_argument("--json", default="", help="also write the results here")
    a = ap.parse_args()

    freqs = [float(x) for x in a.freqs.split(",") if x.strip()]
    res = {"bias": a.bias, "jack_vpp": a.jack_vpp,
           "t": time.strftime("%Y-%m-%d %H:%M:%S")}
    ok = True
    warn = []

    # ---------------------------------------------------- scope server
    # The bench rule: check it, leaving starting to the operator.
    try:
        sc = Scope2()
    except Exception as e:
        sys.exit(f"ERROR: scope server on 127.0.0.1:5555 is unreachable ({e})\n"
                 "       start it with:\n"
                 "         ../.venv-meas/bin/python3 "
                 "../ofxLPM/scope-pixhawk/tools/server.py")
    print("scope server: connected on 127.0.0.1:5555 "
          "(ch1 = LNA output, ch2 = LNA input)")

    # ---------------------------------------------------- 1. biases
    if a.skip_bias:
        print("\n[1/4] biases: SKIPPED (--skip-bias); the DACs hold whatever "
              "was written last")
    else:
        with open(a.bias) as f:
            biases = json.load(f)
        print(f"\n[1/4] biases: {os.path.basename(a.bias)} "
              f"({len(biases)} channels)")
        print("      amplifier channels (these five switch it OFF if wrong):")
        for k in ("lna_iref", "TUNEp", "VB1", "VB2", "VREF"):
            print(f"        {k:<11}{biases.get(k, float('nan')):8.3f}")
        dacs = DACs()
        try:
            apply_bias_dict(dacs, biases)
        finally:
            dacs.close()
        print(f"      applied; settling {a.settle:.0f} s "
              f"(the output DC moves for ~40 s after any bias change)")
        sc.drain(a.settle)

    # ---------------------------------------------------- 2. noise
    subprocess.run(["pkill", "-f", "[p]w-play"], capture_output=True)
    print(f"\n[2/4] noise: {a.noise_s:.0f} s of ch1 with the drive silent")
    t, c1, c2 = sc.collect2(a.noise_s)
    dc = float(c1.mean())
    rms_all = float(c1.std())
    pp = float(np.percentile(c1, 95) - np.percentile(c1, 5))
    rms_ex, rms_hum = mains_excluded_rms(c1)
    print(f"      {len(c1)} samples, {t[-1]-t[0]:.1f} s contiguous")
    print(f"      output DC              {dc:8.4f} V")
    print(f"      rms, mains excluded    {rms_ex*1e3:8.2f} mV   <- the check")
    print(f"      rms, everything        {rms_all*1e3:8.2f} mV")
    print(f"      mains lines alone      {rms_hum*1e3:8.2f} mV   (room pickup)")
    print(f"      peak-to-peak (p5-p95)  {pp*1e3:8.2f} mV")
    noise_ok = rms_ex * 1e3 < a.noise_limit_mv
    print(f"      -> noise {'PASS' if noise_ok else 'FAIL'}: "
          f"{rms_ex*1e3:.2f} mV rms vs {a.noise_limit_mv:.0f} mV limit")
    if dc > DEAD_DC_V:
        warn.append(f"output DC {dc:.3f} V is at the rail -- a dead amplifier "
                    f"is quiet AND parked at ~1.80 V, so a low noise number "
                    f"here proves nothing")
    ok &= noise_ok
    res["noise"] = {"dc_v": dc, "rms_excl_mains_mv": rms_ex * 1e3,
                    "rms_total_mv": rms_all * 1e3,
                    "rms_mains_mv": rms_hum * 1e3, "pp_mv": pp * 1e3,
                    "limit_mv": a.noise_limit_mv, "pass": bool(noise_ok)}

    wavdir = os.path.join(HERE, "wavs_bringup")
    os.makedirs(wavdir, exist_ok=True)
    audio = AudioOut()
    out_fits, cal = {}, {}
    try:
        # ------------------------------------------------ 3. output pass
        print(f"\n[3/4] gain, output pass: {len(freqs)} tones at "
              f"{a.jack_vpp:.5f} Vpp (jack), {a.reps} x {a.tone_s:.0f} s each")
        print("      freq      out Vpp    spread   h2      resid      DC")
        print("      [Hz]        [mV]       [%]    [%]      [mV]      [V]")
        for i, f_nom in enumerate(freqs):
            f0 = decommensurate(f_nom)     # 100.000 Hz aliases at 1000 S/s
            fit, vals = play_and_fit(
                sc, audio, wavdir, f0, a.jack_vpp,
                a.first_settle if i == 0 else a.tone_settle,
                a.tone_s, a.reps, sine_fit, chan=1)
            if fit is None:
                print(f"      {f_nom:6.1f}   fit failed")
                ok = False
                continue
            sp = spread_pct(vals)
            h2 = fit["h2"] * 100 if np.isfinite(fit["h2"]) else float("nan")
            print(f"      {f_nom:6.1f}  {fit['vpp']*1e3:9.2f} {sp:8.1f} "
                  f"{h2:6.2f}  {fit['resid_rms']*1e3:8.2f} {fit['dc']:8.3f}")
            out_fits[f_nom] = (f0, fit, sp, h2)
            if fit["resid_rms"] > 0.25 * fit["vpp"] / 2:
                warn.append(f"{f_nom:g} Hz fit residual "
                            f"{fit['resid_rms']*1e3:.1f} mV against a "
                            f"{fit['vpp']/2*1e3:.1f} mV amplitude -- what is "
                            f"on this node carries more than the tone")
            if sp > MAX_SPREAD_PCT:
                warn.append(f"{f_nom:g} Hz output scattered {sp:.1f}% between "
                            f"repeats -- still settling, or a playback hiccup")
            if np.isfinite(h2) and h2 > MAX_H2_PCT:
                warn.append(f"{f_nom:g} Hz second harmonic {h2:.1f}% -- the "
                            f"output is clipping, so its gain is a lie. "
                            f"Lower --jack-vpp")

        # ------------------------------------------------ 4. input pass
        if a.ratio > 0:
            print(f"\n[4/4] input calibration: SKIPPED, using --ratio "
                  f"{a.ratio:.4f}")
            for f_nom in freqs:
                cal[f_nom] = a.ratio
        else:
            print(f"\n[4/4] input calibration: same tones at "
                  f"{a.cal_jack_vpp:.3f} Vpp (jack), read on ch2.")
            print("      Large on purpose -- ch2 carries ~4 mV rms of its own "
                  "noise on an\n      0.805 mV/step ADC, so the ~3 mVpp the "
                  "gain pass delivers is unreadable\n      there. The divider "
                  "is resistive, so the ratio carries over. The output\n"
                  "      is railed throughout this pass and is not read.")
            print("      freq       in Vpp    spread   jack->chip ratio")
            print("      [Hz]         [mV]      [%]")
            for f_nom in freqs:
                f0 = decommensurate(f_nom)
                fit, vals = play_and_fit(
                    sc, audio, wavdir, f0, a.cal_jack_vpp, a.tone_settle,
                    a.tone_s, a.cal_reps, halfwave_fit, chan=2)
                if fit is None:
                    print(f"      {f_nom:6.1f}   no signal on ch2")
                    warn.append(f"ch2 saw nothing at {f_nom:g} Hz -- is the "
                                f"probe on the amplifier input (pin 4)?")
                    continue
                r = fit["vpp"] / a.cal_jack_vpp
                sp = spread_pct(vals, robust=True)
                print(f"      {f_nom:6.1f}  {fit['vpp']*1e3:9.2f} {sp:8.1f}"
                      f"        {r:.4f}")
                cal[f_nom] = r
                # The ratio multiplies straight into the gain, so scatter here
                # carries real weight. Any other sound playing while this runs --
                # a notification, a browser tab -- lands in the same window and
                # shows up exactly like this.
                if sp > MAX_SPREAD_PCT:
                    warn.append(f"{f_nom:g} Hz input calibration scattered "
                                f"{sp:.1f}% between repeats -- something else "
                                f"was using the audio device, or ch2 is near "
                                f"its noise floor. The {f_nom:g} Hz gain "
                                f"carries that error")
    finally:
        audio.stop()
        sc.close()

    # ---------------------------------------------------- verdict
    print("\n" + "=" * 62)
    print("GAIN  (output Vpp / input Vpp, both measured on the chip's pins)")
    print("      freq     in Vpp     out Vpp      gain      gain")
    print("      [Hz]       [mV]        [mV]       [x]      [dB]")
    rows, gains = [], []
    for f_nom in freqs:
        if f_nom not in out_fits or f_nom not in cal:
            continue
        f0, fit, sp, h2 = out_fits[f_nom]
        vin = cal[f_nom] * a.jack_vpp
        g = fit["vpp"] / vin if vin > 0 else float("nan")
        gdb = 20 * math.log10(g) if g > 0 else float("nan")
        print(f"      {f_nom:6.1f} {vin*1e3:10.3f} {fit['vpp']*1e3:11.2f} "
              f"{g:9.1f} {gdb:9.2f}")
        rows.append({"f_nom": f_nom, "f_used": f0, "vin_pp": vin,
                     "vout_pp": fit["vpp"], "gain": g, "gain_db": gdb,
                     "ratio": cal[f_nom], "h2_pct": h2, "spread_pct": sp,
                     "resid_rms_mv": fit["resid_rms"] * 1e3, "dc_v": fit["dc"]})
        gains.append(g)
    res["gain"] = rows

    clipped = [r for r in rows if np.isfinite(r["h2_pct"])
               and r["h2_pct"] > MAX_H2_PCT]
    if rows and len(clipped) == len(rows):
        warn.append("every tone clipped -- the gain figures above stop being "
                    "gain. Lower --jack-vpp and re-run")
        ok = False

    # A resistive divider is flat and the sound card is flat over 80-150 Hz, so
    # the input Vpp should track the output Vpp across the three tones. When the
    # output is flat while the input moves, it is the ch2 fit that moved rather than the
    # amplifier -- say which, or the number gets read as a frequency response.
    if len(rows) > 1:
        out_sp = spread_pct([r["vout_pp"] for r in rows])
        in_sp = spread_pct([r["vin_pp"] for r in rows])
        if in_sp > 3 * max(out_sp, 1.0) and in_sp > MAX_SPREAD_PCT:
            warn.append(f"the output is flat across the three tones "
                        f"({out_sp:.1f}%) but the measured input stays "
                        f"({in_sp:.1f}%) -- that is the ch2 calibration "
                        f"moving rather than the amplifier's transfer. Trust the "
                        f"tone with the smallest calibration spread, or pin "
                        f"one ratio with --ratio")

    if gains:
        gmed = float(np.median(gains))
        print(f"\n      median {gmed:.1f}x = {20*math.log10(gmed):.2f} dB, "
              f"spread across the three tones {spread_pct(gains):.1f}%")
        res["gain_median_x"] = gmed
        res["gain_median_db"] = 20 * math.log10(gmed)
        if gmed < MIN_GAIN_X:
            warn.append(f"{gmed:.1f}x is below the amplifier floor -- check lna_iref / "
                        f"TUNEp / VB1 / VB2 / VREF in the bias file")
            ok = False
    else:
        print("      no gain point survived")
        ok = False
    print(f"\nNOISE {res['noise']['rms_excl_mains_mv']:.2f} mV rms "
          f"(mains excluded) vs {a.noise_limit_mv:.0f} mV limit -> "
          f"{'PASS' if res['noise']['pass'] else 'FAIL'}")
    print("=" * 62)

    for w in warn:
        print(f"WARNING: {w}")
    res["warnings"] = warn
    res["pass"] = bool(ok)

    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=2)
        print(f"json: {a.json}")

    print(f"\n=== LNA bring-up: {'OK' if ok else 'NOT OK'} ===")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
