#!/usr/bin/env python3
"""LNA transfer function: sweep the computer-audio sine 1 Hz..20 kHz and
measure the output Vpp on the pixhawk scope stream.

Self-contained: loads a .biases file over the FTDI (all 23 DAC channels,
same NMOS/PMOS references as neuron_bridge), plays each test tone out of
the audio jack with pw-play, and reads Vpp from the scope server
(127.0.0.1:5555, fallback /dev/ttyACM0) via ScopeClient.

The scope samples ~1 kS/s, so above ~200 Hz the cycles are not resolved --
but the samples still cover the sine's phase quasi-uniformly, so the
p5..p95 spread remains a good amplitude estimator. What degrades is the
ability to VERIFY the frequency on the scope side; the generator is
trusted there. Amplitude caveat: the audio jack is AC-coupled, so the
first point near 1 Hz may be attenuated by the output high-pass corner.

Before running:
  - pkill -f '[n]euron_bridge.py' ; close the GUI      (exclusive FTDI)
  - systemctl --user stop sine_out                     (done by the script too)

Usage (from LNA/):
  ../.venv-meas/bin/python3 lna_freq_sweep.py
  ../.venv-meas/bin/python3 lna_freq_sweep.py --fmin 50 --fmax 200 --ppd 2   # quick

Outputs:
  lna_transfer.csv    freq_hz, vin_pp, vpp_out, gain, gain_db, n_samples
  lna_transfer.png    Bode magnitude plot (if matplotlib is present)
"""

import argparse
import csv
import json
import math
import os
import signal
import struct
import subprocess
import sys
import time
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lna_gain_tune import DACs, ScopeClient

BIAS_TABLE = [
    (1, 0b000, "vtaup"), (1, 0b001, "vthrdp"), (1, 0b010, "vepulseextp"), (1, 0b011, "vipulseextp"),
    (2, 0b000, "vleakn"), (2, 0b001, "vtaun"), (2, 0b010, "vrefn"), (2, 0b011, "free"),
    (3, 0b000, "lna_iref"), (3, 0b001, "JInhWp1"), (3, 0b010, "JInhWp2"), (3, 0b011, "JInhWp3"),
    (4, 0b000, "JExcWn0"), (4, 0b001, "JExcWn1"), (4, 0b010, "JExcWn2"), (4, 0b011, "JExcWn3"),
    (5, 0b000, "VREF"), (5, 0b001, "VB1"), (5, 0b010, "VB2"), (5, 0b011, "TUNEp"),
    (6, 0b000, "buffermonp"), (6, 0b001, "JInhWp0"), (6, 0b010, "vthrdn"), (6, 0b011, "ifdcp"),
]
BIAS_LOOKUP = {name.lower(): (dac, addr, name) for dac, addr, name in BIAS_TABLE}
NMOS = ("vleakn", "vtaun", "vrefn", "jexcwn0", "jexcwn1", "jexcwn2", "jexcwn3")
VREFP, VREFN = 1.79, 0.89

FULL_SCALE_VRMS = 1.0


def apply_bias_dict(dacs, biases):
    for name, volts in biases.items():
        m = BIAS_LOOKUP.get(str(name).lower())
        if m is None:
            continue
        dac_id, addr, real = m
        try:
            v = float(volts)
        except (TypeError, ValueError):
            continue
        if 0 <= v <= VREFN and real.lower() in NMOS:
            dacs.set_voltage(dac_id, addr, v, vref=VREFN)
        elif 0 <= v <= VREFP:
            if real == "lna_iref":
                dacs.power_up(dac_id, addr)
            dacs.set_voltage(dac_id, addr, v, vref=VREFP)


def make_wav(path, freq, vpp, fs=44100):
    amp = min((vpp / 2) / (FULL_SCALE_VRMS * math.sqrt(2)), 1.0)
    dur = min(max(8.0 / freq, 2.0), 10.0)
    n = int(fs * dur)
    n -= n % max(1, round(fs / freq))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(b"".join(
            struct.pack("<h", int(32767 * amp * math.sin(2 * math.pi * freq * i / fs)))
            for i in range(n)))
    return amp * math.sqrt(2) * 2 * FULL_SCALE_VRMS


class AudioOut:
    def __init__(self):
        self.proc = None

    def play(self, wav):
        self.stop()
        self.proc = subprocess.Popen(
            ["bash", "-c", 'while :; do pw-play -- "$1"; done', "_", wav],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)

    def stop(self):
        if self.proc is not None:
            try:
                os.killpg(self.proc.pid, signal.SIGTERM)
                self.proc.wait(timeout=2)
            except Exception:
                pass
            self.proc = None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--biases", default="../ofxCaravanViewer/bin/data/LNA_chip0_110_audio_1.5.biases")
    ap.add_argument("--vin-pp", type=float, default=1.5)
    ap.add_argument("--fmin", type=float, default=1.0)
    ap.add_argument("--fmax", type=float, default=20000.0)
    ap.add_argument("--ppd", type=int, default=8, help="points per decade")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--window", type=float, default=0.0, help="fixed measurement window seconds (0 = auto from freq)")
    ap.add_argument("--settle", type=float, default=0.8)
    ap.add_argument("--out", default="lna_transfer.csv")
    ap.add_argument("--png", default="lna_transfer.png")
    args = ap.parse_args()

    subprocess.run(["systemctl", "--user", "stop", "sine_out"],
                   capture_output=True)

    with open(args.biases) as f:
        biases = json.load(f)
    print(f"biases: {args.biases} ({len(biases)} channels)")
    dacs = DACs()
    apply_bias_dict(dacs, biases)
    time.sleep(0.3)

    scope = ScopeClient()
    print(f"scope: streaming from {scope.source}")

    decades = math.log10(args.fmax / args.fmin)
    npts = max(2, int(round(decades * args.ppd)) + 1)
    freqs = [args.fmin * 10 ** (decades * i / (npts - 1)) for i in range(npts)]

    wavdir = os.path.join(os.path.dirname(os.path.abspath(args.out)) or ".", "wavs")
    os.makedirs(wavdir, exist_ok=True)

    new = not os.path.exists(args.out)
    out = open(args.out, "a", newline="")
    log = csv.writer(out)
    if new:
        log.writerow(["freq_hz", "vin_pp", "vpp_out", "gain", "gain_db", "n_samples"])

    audio = AudioOut()
    rows = []
    try:
        for f0 in freqs:
            wav = os.path.join(wavdir, f"tone_{f0:.1f}hz.wav")
            vin_true = make_wav(wav, f0, args.vin_pp) if not os.path.exists(wav) else args.vin_pp
            audio.play(wav)
            time.sleep(args.settle)
            window = args.window if args.window > 0 else min(max(8.0 / f0, 0.6), 6.0)
            vpps = []
            for _ in range(args.reps):
                v, n, _ = scope.vpp(window)
                vpps.append(v)
            vpp = sorted(vpps)[len(vpps) // 2]
            gain = vpp / vin_true if vin_true else float("nan")
            gdb = 20 * math.log10(gain) if gain > 0 else float("nan")
            rows.append((f0, vpp, gain, gdb))
            log.writerow([f"{f0:.2f}", f"{vin_true:.4f}", f"{vpp:.5f}",
                          f"{gain:.3f}", f"{gdb:.2f}", n])
            out.flush()
            print(f"  {f0:9.1f} Hz -> {vpp*1e3:8.1f} mVpp   {gdb:7.2f} dB")
    except KeyboardInterrupt:
        print("\ninterrupted; keeping partial results")
    finally:
        audio.stop()
        scope.close()
        dacs.close()
        out.close()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.semilogx([r[0] for r in rows], [r[3] for r in rows], "o-", ms=3)
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("gain [dB]")
        ax.grid(True, which="both", alpha=0.3)
        ax.set_title(f"LNA transfer  ({os.path.basename(args.biases)}, Vin {args.vin_pp:g} Vpp)")
        fig.tight_layout()
        fig.savefig(args.png, dpi=150)
        print(f"plot: {args.png}")
    except Exception as e:
        print(f"plot skipped: {e}")
    print(f"data: {args.out}")


if __name__ == "__main__":
    sys.exit(main())
