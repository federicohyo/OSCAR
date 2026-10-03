#!/usr/bin/env python3
"""Stimulus for the pad-evoked run: 137 Hz tone bursts as the events,
direct playback (bench divider bypassed), one burst per period.

    ../.venv-meas/bin/python3 LNA/pad_evoked_stimulus.py

WHY BURSTS RATHER THAN THE SALINE STEP (2026-08-31, measured on the new die):
this die's amplifier parks its output DC ~19 mV off the ground rail as soon as
anything is driven (input-side rectification; idle 227 mV). A DC-step event
(the saline_stimulus.py replay, unity 1.15 mVpp) is squashed flat against that
floor -- folded records show the event window indistinguishable from noise. A
CONTINUOUS tone, by contrast, reads out clearly (2 mVpp in -> 212 mVpp visible
at the output, measured). The host thresholds the burst and injects spikes via
UART; the burst is the event marker, its amplitude is a marker only.

Layout of one period: [1.0 s silence][BURST][1.5 s silence]; N repeats,
MONO 44.1 kHz. Event window for scoring = the burst.

Outputs: pad_evoked_stimulus.wav + pad_evoked_timing.json (keys the loop
reads: wav_s, period_s, repeats, chip_vpp, event_on, event_off).
"""
import json, os, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

FS        = 44100
FS_FULL_VPP = 2.0 * 2**0.5          # jack full scale: ~1 Vrms sine == PCM +-1

BURST_HZ  = 137.0     # the measured-clean node (odor_stimulus.py rationale:
                      # clear of mains harmonics, in passband, incommensurate
                      # with the 1 kS/s readout)
BURST_S   = 0.40
BURST_VPP = 5.0e-3    # at the chip/jack; on chip1's healthy amp (~124x)
                      # -> ~600 mVpp events at ch1, keeping clear of the rail
PRE_S, POST_S = 1.0, 1.5
REPS      = 12


def main():
    tb = np.arange(int(BURST_S * FS)) / FS
    burst = np.sin(2 * np.pi * BURST_HZ * tb) * np.hanning(len(tb))
    burst *= (BURST_VPP / 2) / (FS_FULL_VPP / 2)          # volts -> PCM +-1
    one = np.concatenate([np.zeros(int(PRE_S * FS)), burst,
                          np.zeros(int(POST_S * FS))])
    period = len(one) / FS
    t0 = PRE_S                       # burst start, in-period
    pcm = np.tile(one, REPS)

    wav = os.path.join(HERE, "pad_evoked_stimulus.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes((np.clip(pcm, -1, 1) * 32767).astype("<i2").tobytes())
    tm = {"wav_s": len(pcm) / FS, "period_s": period, "repeats": REPS,
          "chip_vpp": BURST_VPP, "burst_hz": BURST_HZ,
          "t_mark": t0 + BURST_S / 2, "mark_hz": BURST_HZ, "mark_s": BURST_S,
          "event_on": t0, "event_off": t0 + BURST_S,
          "drive": "direct, no divider; jack level == chip level",
          "note": "137 Hz tone bursts ARE the events: on this die the amp DC "
                  "parks at the ground floor when driven; a continuous tone "
                  "still reads out, a DC step does not (measured 2026-08-31)"}
    with open(os.path.join(HERE, "pad_evoked_timing.json"), "w") as f:
        json.dump(tm, f, indent=2)
    print(f"{os.path.basename(wav)}: {REPS} x {period:.2f} s = {len(pcm)/FS:.1f} s, "
          f"burst {BURST_HZ:.0f} Hz {BURST_S*1e3:.0f} ms {BURST_VPP*1e3:.0f} mVpp, "
          f"event {t0:.2f}..{t0+BURST_S:.2f} s in-period")
    return 0


if __name__ == "__main__":
    sys.exit(main())
