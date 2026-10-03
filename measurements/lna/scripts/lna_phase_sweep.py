#!/usr/bin/env python3
"""LNA phase (and magnitude) response on silicon -- the measured Fig. 7.

    ch1 = one probe (pin 2)      ch2 = the other (pin 4)

The point of measuring phase: it needs zero amplitude calibration. Phase is the
difference between two channels sampled on the same tick, so the divider ratio,
the sound card's true full scale and the ADC's gain all cancel exactly. The
jack->chip anchor that was wrong by 15x cannot touch this number. It also gives
the high-pass corner independently -- sim puts -3 dB near 1.6 Hz, the measured
magnitude curve says 0.49 Hz, and the corner and the phase transition are locked
together, so the phase settles it independently of any single level.

Three modes:

  --through   BOTH probes on the SAME node. Any phase difference measured then
              is instrumental rather than the amplifier: the firmware converts ch1
              (PC4, pin 2) and then ch2 (PC3, pin 4) back to back, ~47 us apart,
              and labels both with one timestamp. That puts -360*f*tau into
              every reading. Sweep, fit a straight line, and the slope IS tau.
              The line must go through the origin with a NEGATIVE slope -- if it
              does not, something else is wrong and the sweep is not worth
              running.

  --pilot     Three frequencies, many repeats. Answers "does phase repeat on
              this bench?" in ten minutes, before an hour is spent on a sweep.
              Also re-measures one point after a long settle, to see whether the
              ~40 s output-DC settling that ruins GAIN also moves PHASE.

  (default)   The sweep: 0.2 .. 200 Hz, log spaced.

Method, all three modes: coherent least-squares fit at the known drive
frequency, on both channels out of the same sample pair. Amplitude comes from the fit
rather than a peak-to-peak or percentile spread.

Two subtle points:

  * EACH WINDOW STARTS AT AN ARBITRARY POINT IN THE TONE, so the individual
    phases are meaningless across windows -- only their DIFFERENCE is stable.
    So the repeats are combined as unit phasors of the difference: the mean
    direction is the answer and the resultant length R is the error bar (R = 1
    is perfect agreement). Averaging the raw angles would be off at the
    +/-180 deg wrap, which is exactly where the passband sits.

  * A DROPPED SAMPLE SLEWS PHASE DIRECTLY, and it is the one defect that
    produces a plausible off angle. Every window is required to come back on
    the reconstructed uniform 1 ms grid; anything else is discarded rather than fitted.

The frequency band is set at both ends by the bench rather than the amplifier:
below ~0.15 Hz the audio jack delivers nothing (it is AC-coupled -- see
lna_transfer_ref.csv, which is dead at 0.1 Hz and 16 dB down at 0.2 Hz), and
above ~200 Hz the 1 kS/s ADC runs out of samples per cycle. The HF roll-off and
the phase margin in Fig. 7 are out of reach with this setup.
"""
import argparse
import csv
import math
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lna_audio_sweep import (sine_fit, halfwave_fit, make_wav, AudioOut,
                             decommensurate, BOARD_DT)
from lna_bringup_check import Scope2

FS = 1.0 / BOARD_DT
FIRMWARE_SKEW_US = 46.9      # 480+12 ADC cycles at 10.5 MHz (ADCPRE = /8).
                             # NOTE: the pixhawk-scope header comment still says
                             # "~25 us" -- that is stale, from when the
                             # prescaler was /4. adc_init's own comment agrees
                             # with 47 us.
SWEEP_HZ = [0.2, 0.3, 0.5, 0.8, 1.3, 2.0, 3.2, 5.0, 8.0, 13.0, 20.0, 32.0,
            50.0, 80.0, 130.0, 200.0]
PILOT_HZ = [0.5, 5.0, 50.0]
# The amplifier compresses around 950 mVpp out, and README_MEASUREMENTS puts
# saturation onset near 780 mVpp (8 mVpp in at 97.7x). Aim well below that: a
# compressed output has the phase of a limiter -- flat at 180 deg -- and it
# looks perfectly repeatable while it does it (R = 0.999).
TARGET_OUT_VPP = 0.600
ACCEPT_OUT = (0.45, 0.80)    # bounds rather than a ratio band: near the knee the
                             # output barely responds to level, so a generous
                             # band accepts a saturated point


def uniform_grid(t):
    """Did this window come back on the reconstructed 1 ms grid?

    longest_contiguous() rebuilds the time axis from the sample index when the
    board clock and the sample count agree, and falls back to the raw board
    clock when the measured ones differ -- i.e. when samples were dropped. For phase the
    fallback is useless, so treat it as a rejected window."""
    return (len(t) > 100 and abs(float(t[0])) < 1e-9
            and np.allclose(np.diff(t), BOARD_DT, atol=1e-9))


def fit_channel(t, v, f0):
    """Fit whichever way this node needs.

    A node sitting at ~0 V with its negative half clipped is AC-coupled and has
    been chopped by the unipolar ADC -- the amplifier INPUT, and also the
    divider output if the through-jumper is fitted there. A node riding on a DC
    level is an ordinary sine -- the amplifier OUTPUT. Deciding from the data
    means the script is agnostic to which probe is on which pin."""
    if float(np.percentile(v, 5)) < 0.005 and float(v.mean()) < 0.15:
        return halfwave_fit(t, v, f0), "chopped"
    return sine_fit(t, v, f0), "sine"


def measure(sc, audio, wavdir, f0, jack_vpp, settle, window, reps):
    """Play one tone; return the phase DIFFERENCE and both amplitudes.

    Returns None if too few windows survived."""
    wav = os.path.join(wavdir, f"ph_{f0:.3f}hz_{jack_vpp:.5f}vpp_"
                               f"{settle + reps*window + 4:.0f}s.wav")
    if not os.path.exists(wav):
        make_wav(wav, f0, jack_vpp, min_dur=settle + reps * window + 4.0)
    audio.play(wav)
    sc.drain(settle)

    phasors, a1s, a2s, kinds, rejected = [], [], [], set(), 0
    for _ in range(reps):
        t, c1, c2 = sc.collect2(window)
        if not uniform_grid(t):
            rejected += 1
            continue
        f1, k1 = fit_channel(t, c1, f0)
        f2, k2 = fit_channel(t, c2, f0)
        if f1 is None or f2 is None:
            rejected += 1
            continue
        kinds.add(f"ch1:{k1}"); kinds.add(f"ch2:{k2}")
        # Only the DIFFERENCE is stable across windows -- each acquisition
        # starts at an arbitrary point in the tone.
        d = math.radians(f1["phase_deg"] - f2["phase_deg"])
        phasors.append(complex(math.cos(d), math.sin(d)))
        a1s.append(f1["vpp"]); a2s.append(f2["vpp"])
    if len(phasors) < 2:
        return None
    z = np.mean(phasors)
    R = float(abs(z))
    # Two different numbers, and confusing them overstates the error by 4x at
    # n=16: circ_sd is how much INDIVIDUAL windows scatter, while the answer is
    # their mean, whose uncertainty falls as 1/sqrt(n). Report the standard
    # error as the error bar and keep the spread for diagnosis.
    circ_sd = math.degrees(math.sqrt(-2.0 * math.log(max(R, 1e-12))))
    sem = circ_sd / math.sqrt(len(phasors))
    return {
        "dphi_deg": math.degrees(math.atan2(z.imag, z.real)),
        "R": R, "circ_sd_deg": circ_sd, "sem_deg": sem, "n": len(phasors),
        "rejected": rejected,
        "vout_pp": float(np.median(a1s)), "vin_pp": float(np.median(a2s)),
        "kinds": ",".join(sorted(kinds)),
    }


def find_drive(sc, audio, wavdir, f0, start_jack, target, settle, window):
    """Scale the jack level until the output lands near `target` Vpp.

    No fixed level can work across three decades: the sound card rolls off below
    ~5 Hz and the amplifier's own gain climbs through its corner over the same
    span, so a level that is right at 20 Hz drives nothing at 0.3 Hz and clips
    at 5 Hz. Two proportional steps get inside 40% from anywhere."""
    jack = float(np.clip(start_jack, 2e-4, 1.0))
    for _ in range(6):
        # reps=2 rather than 1: measure() needs two windows to form a mean direction
        # and returns None below that. Called with reps=1 it ALWAYS returned
        # None, so the search read "silent" at every level and quadrupled
        # the drive to full scale -- which railed the amplifier and produced a
        # pilot that measured a limiter instead of an amplifier.
        r = measure(sc, audio, wavdir, f0, jack, settle, window, 2)
        if r is None or r["vout_pp"] <= 0:
            jack = min(jack * 4, 1.0)
            continue
        if ACCEPT_OUT[0] <= r["vout_pp"] <= ACCEPT_OUT[1]:
            return jack, r["vout_pp"]
        # Proportional step. Above the knee this overshoots downward, which is
        # the safe direction -- the output there is nearly independent of the
        # level, so a step computed from it is an underestimate of how far
        # down we need to go.
        jack = float(np.clip(jack * target / r["vout_pp"], 2e-4, 1.0))
    return jack, float("nan")


def preflight_wiring(sc, audio, wavdir, min_gain_db=20.0):
    """Refuse to sweep when both probes are on the same node.

    This happens in practice: a through-calibration leaves both probes tied
    together, and if the jumper is not removed the sweep still runs, still
    reports R = 1.000, and returns a phase of 0.00 deg at every frequency. That
    looks like a clean measurement of an amplifier outside the circuit.

    Two independent tells, both free:
      * the amplifier INPUT is AC-coupled and rests near 0 V, so the unipolar
        ADC chops it -- fit_channel calls it "chopped". Two "sine" channels
        means neither probe is on the input.
      * a 5 Hz tone must come out ~50 dB bigger than it went in. Same-node
        wiring gives 0.1-0.2 dB, which is the ADC's own channel mismatch.
    """
    f0 = decommensurate(5.0)
    r = measure(sc, audio, wavdir, f0, 0.01, 8.0, 4.0, 2)
    if r is None:
        return False, "no usable window at 5 Hz -- is the drive reaching the chip?"
    gdb = (20 * math.log10(r["vout_pp"] / r["vin_pp"])
           if r["vin_pp"] > 0 else float("nan"))
    what = (f"ch1 {r['vout_pp']*1e3:.1f} mVpp, ch2 {r['vin_pp']*1e3:.1f} mVpp, "
            f"{gdb:+.2f} dB between them, dphi {r['dphi_deg']:+.2f} deg "
            f"[{r['kinds']}]")
    if not np.isfinite(gdb) or gdb < min_gain_db:
        return False, (
            f"the two probes sit away from the amplifier.\n       {what}\n"
            f"       Expected ~50 dB and a chopped ch2. A fraction of a dB with "
            f"zero phase is\n       what one node read twice looks like -- "
            f"check the through-jumper is removed\n       and that pin 4 is "
            f"back on the amplifier input.")
    return True, what


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--through", action="store_true",
                    help="both probes on ONE node: measure the ADC skew")
    ap.add_argument("--pilot", action="store_true",
                    help="3 frequencies, many repeats: does phase repeat?")
    ap.add_argument("--freqs", default="", help="override the frequency list")
    ap.add_argument("--skew-us", type=float, default=FIRMWARE_SKEW_US,
                    help="inter-channel skew to correct out. The CSV keeps the "
                         "raw phase too, so a later through-cal can be applied "
                         "offline without re-measuring")
    ap.add_argument("--divider", type=float, default=1.0,
                    help="set when ch2 probes UPSTREAM of the input divider: "
                         "the true chip input is this ratio times ch2. Affects "
                         "the reported gain ONLY -- a resistive divider adds no "
                         "phase, so every phase column is untouched by it")
    ap.add_argument("--target-vpp", type=float, default=TARGET_OUT_VPP)
    ap.add_argument("--jack-vpp", type=float, default=0.0,
                    help="fixed jack level; 0 = search per frequency "
                         "(--through defaults to a fixed level)")
    ap.add_argument("--settle", type=float, default=12.0,
                    help="settle after a level change before the real windows")
    ap.add_argument("--search-settle", type=float, default=5.0)
    ap.add_argument("--reps", type=int, default=0,
                    help="windows per point; 0 = adaptive (more where the "
                         "input is small)")
    ap.add_argument("--out", default="",
                    help="default depends on the mode, so a through-cal or a "
                         "pilot cannot silently overwrite a finished sweep")
    a = ap.parse_args()
    if not a.out:
        a.out = ("lna_phase_through.csv" if a.through else
                 "lna_phase_pilot.csv" if a.pilot else "lna_phase.csv")

    if a.freqs:
        freqs = [float(x) for x in a.freqs.split(",") if x.strip()]
    elif a.pilot:
        freqs = PILOT_HZ
    elif a.through:
        freqs = [1.0, 2.0, 5.0, 13.0, 32.0, 80.0, 130.0, 200.0]
    else:
        freqs = SWEEP_HZ

    subprocess.run(["pkill", "-f", "[p]w-play"], capture_output=True)
    try:
        sc = Scope2()
    except Exception as e:
        sys.exit(f"ERROR: scope server on 127.0.0.1:5555 is unreachable ({e})\n"
                 "       start the external bench scope server first")
    wavdir = os.path.join(HERE, "wavs_phase")
    os.makedirs(wavdir, exist_ok=True)
    audio = AudioOut()

    mode = "THROUGH (skew calibration)" if a.through else (
           "PILOT" if a.pilot else "SWEEP")
    print(f"=== LNA phase, mode: {mode} ===")
    print(f"    {len(freqs)} points, skew correction "
          f"{a.skew_us:.1f} us ({'measuring it' if a.through else 'assumed'})")

    if not a.through:
        # With ch2 upstream of the divider its reading is larger, so the
        # measured ch1/ch2 ratio is smaller than the amplifier's gain. Even a
        # 15:1 divider leaves ~27 dB, so 15 dB still separates "across the
        # amplifier" from "one node read twice" (which gives 0.2 dB).
        ok, what = preflight_wiring(sc, audio, wavdir,
                                    min_gain_db=15.0 if a.divider != 1.0 else 20.0)
        if not ok:
            audio.stop(); sc.close()
            sys.exit(f"ERROR: {what}")
        print(f"    wiring OK: {what}")

    rows = []
    try:
        for f_nom in freqs:
            f0 = decommensurate(f_nom)          # 100.000 Hz aliases at 1 kS/s
            window = float(np.clip(5.0 / f0, 4.0, 30.0))
            # Above the corner the gain is ~300x, so a clean output means only
            # ~3 mVpp at the input -- a few ADC steps against ch2's own 4 mV of
            # noise. Windows are cheap up there (4 s is hundreds of cycles), so
            # buy the phase precision back by averaging more of them. Below the
            # corner the gain is low, the input is large, and 3 windows is
            # plenty -- which is lucky, since that is where they cost 25 s each.
            reps = a.reps or (5 if f0 < 5 else 16)
            if a.jack_vpp > 0 or a.through:
                jack = a.jack_vpp or 0.05
                got = float("nan")
            else:
                jack, got = find_drive(sc, audio, wavdir, f0, 0.05,
                                       a.target_vpp, a.search_settle,
                                       min(window, 4.0))
            r = measure(sc, audio, wavdir, f0, jack, a.settle, window, reps)
            if r is None:
                print(f"  {f_nom:7.2f} Hz   no usable window")
                continue
            if r["vout_pp"] > ACCEPT_OUT[1]:
                print(f"  {f_nom:7.2f} Hz   output {r['vout_pp']*1e3:.0f} mVpp "
                      f"is above the {ACCEPT_OUT[1]*1e3:.0f} mVpp linear "
                      f"ceiling -- COMPRESSED, so this phase is the limiter's")
            raw = r["dphi_deg"]
            corr = ((raw + 360.0 * f0 * a.skew_us * 1e-6 + 180) % 360) - 180
            r.update(f_nom=f_nom, f_used=f0, jack_vpp=jack, window_s=window,
                     dphi_raw_deg=raw, dphi_corr_deg=corr,
                     skew_us=a.skew_us,
                     vin_chip_pp=r["vin_pp"] * a.divider,
                     divider=a.divider,
                     gain_db=20 * math.log10(r["vout_pp"]
                                             / (r["vin_pp"] * a.divider))
                     if r["vin_pp"] > 0 else float("nan"))
            rows.append(r)
            print(f"  {f_nom:7.2f} Hz  jack {jack:7.4f}  in {r['vin_pp']*1e3:8.2f} "
                  f"out {r['vout_pp']*1e3:8.2f} mV  dphi {corr:8.2f} deg  "
                  f"+-{r['sem_deg']:.2f} (spread {r['circ_sd_deg']:.1f}, "
                  f"R {r['R']:.3f})  "
                  f"n {r['n']}{'/rej ' + str(r['rejected']) if r['rejected'] else ''}")
    except KeyboardInterrupt:
        print("\ninterrupted; keeping what was measured")
    finally:
        audio.stop()
        sc.close()

    if not rows:
        sys.exit("nothing measured")

    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "f_nom", "f_used", "jack_vpp", "vin_pp", "vin_chip_pp", "divider",
            "vout_pp", "gain_db",
            "dphi_raw_deg", "dphi_corr_deg", "skew_us", "R", "sem_deg",
            "circ_sd_deg",
            "n", "rejected", "window_s", "kinds"])
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in w.fieldnames})
    print(f"\ndata: {a.out}")

    if a.through:
        # Both probes see one signal, so the true difference is zero and what is
        # left is -360*f*tau. Straight line through the origin; a positive slope
        # or a large intercept means something other than sampling skew.
        f = np.array([r["f_used"] for r in rows])
        d = np.array([r["dphi_raw_deg"] for r in rows])
        slope = float(np.sum(f * d) / np.sum(f * f))          # forced origin
        tau_us = -slope / 360.0 * 1e6
        icept, m = np.polyfit(f, d, 1)[::-1]
        resid = d - slope * f
        print(f"\nthrough-calibration:")
        print(f"  forced-origin slope {slope:+.5f} deg/Hz  ->  skew "
              f"{tau_us:+.1f} us   (firmware says {FIRMWARE_SKEW_US:.1f})")
        print(f"  free fit: slope {m:+.5f} deg/Hz, intercept {icept:+.3f} deg")
        print(f"  residual about the origin-line: {resid.std():.3f} deg rms")
        if slope > 0:
            print("  -> POSITIVE slope: that is not sampling skew. Check the "
                  "jumper actually ties pin 2 and pin 4 together.")
        print(f"\n  re-run the sweep with:  --skew-us {tau_us:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
