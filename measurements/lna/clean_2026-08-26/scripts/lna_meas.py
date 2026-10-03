#!/usr/bin/env python3
"""Measurement harness for the clean-setup LNA campaign (2026-08-26).

Every point saves the RAW scope trace, not just the fit -- the previous campaign
saved fits only, and `README_MEASUREMENTS.md` lists that as an open item ("If a
reviewer wants a waveform, it needs re-measuring").

READ-ONLY on the chip: opens no FTDI and writes no DAC. The GUI and
neuron_bridge.py keep the device. Audio out + scope server in, nothing else.
"""
import csv, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LNA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, LNA)
from lna_audio_sweep import (Scope, AudioOut, longest_contiguous, sine_fit,
                             make_wav, FULL_SCALE_VRMS, BOARD_DT, VDD)

DIVIDER = 0.028          # original resistive divider: 0.25 Vpp jack -> 7 mVpp at chip
FS = 1.0 / BOARD_DT

FIELDS = ["tag", "block", "utc", "freq_hz", "jack_vpp", "divider", "vin_pp",
          "settle_s", "window_s", "vout_pp", "gain", "gain_db", "dc_v", "peak_v",
          "trough_v", "h2", "h3", "resid_rms_v", "amp_se_v", "drift_mv_s",
          "n_samples", "frac_at_rail", "frac_at_zero", "raw_npz", "flag"]


class Session:
    """One measurement session writing into a dated archive directory."""

    def __init__(self, root, block, wavdir=None):
        self.root, self.block = root, block
        self.rawdir = os.path.join(root, "raw", block)
        os.makedirs(self.rawdir, exist_ok=True)
        self.csv = os.path.join(root, "derived", f"{block}.csv")
        self.wavdir = wavdir or os.path.join(root, "..", "..", "_wavs")
        os.makedirs(self.wavdir, exist_ok=True)
        self.scope, self.audio, self.rows = None, AudioOut(), []
        if not os.path.exists(self.csv):
            os.makedirs(os.path.dirname(self.csv), exist_ok=True)
            with open(self.csv, "w", newline="") as f:
                csv.writer(f).writerow(FIELDS)

    def __enter__(self):
        self.scope = Scope(); self.scope.drain(1.0); return self

    def __exit__(self, *a):
        self.audio.stop()
        if self.scope: self.scope.close()

    # -- one measured point -------------------------------------------------
    def point(self, tag, freq, jack_vpp, settle=60.0, window=8.0, note=""):
        """Play a tone (or silence when jack_vpp == 0), settle, capture, fit, archive."""
        if jack_vpp > 0:
            wav = os.path.join(self.wavdir, f"{freq:.4f}hz_{jack_vpp:.5f}vpp.wav")
            if not os.path.exists(wav):
                make_wav(wav, freq, jack_vpp, min_dur=settle + window + 15.0)
            self.audio.play(wav)
        else:
            self.audio.stop()
        time.sleep(settle)
        self.scope.drain(0.5)
        t, y = longest_contiguous(*self.scope.collect(window))
        return self._record(tag, freq, jack_vpp, settle, window, t, y, note)

    def capture_only(self, tag, freq, window, note=""):
        """Capture without changing the drive (no re-settling)."""
        self.scope.drain(0.3)
        t, y = longest_contiguous(*self.scope.collect(window))
        return self._record(tag, freq, float("nan"), 0.0, window, t, y, note)

    def _record(self, tag, freq, jack_vpp, settle, window, t, y, note):
        r = sine_fit(t, y, freq) if freq > 0 else None
        vin = jack_vpp * DIVIDER if jack_vpp == jack_vpp else float("nan")
        npz = os.path.join(self.rawdir, f"{tag}.npz")
        np.savez_compressed(npz, t=t, v=y, freq_hz=freq, jack_vpp=jack_vpp,
                            divider=DIVIDER, vin_pp=vin, settle_s=settle,
                            window_s=window, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            note=note)
        rail = float(np.mean(y >= VDD - 0.005)); zero = float(np.mean(y <= 0.005))
        if r is None:
            row = dict(zip(FIELDS, [tag, self.block, time.strftime("%H:%M:%S"), freq,
                                    jack_vpp, DIVIDER, vin, settle, window] + [""]*11 +
                                   [len(y), rail, zero, os.path.relpath(npz, self.root), note]))
        else:
            gain = r["vpp"] / vin if vin and vin == vin and vin > 0 else float("nan")
            peak, trough = r["dc"] + r["amp"], r["dc"] - r["amp"]
            flag = note
            if rail > 0.001 or peak > VDD - 0.02: flag = (flag + " NEAR-RAIL").strip()
            row = dict(zip(FIELDS, [
                tag, self.block, time.strftime("%H:%M:%S"), f"{freq:.4f}", f"{jack_vpp:.5f}",
                DIVIDER, f"{vin:.6f}", settle, window, f"{r['vpp']:.6f}",
                f"{gain:.2f}", f"{20*math.log10(gain):.3f}" if gain == gain and gain > 0 else "",
                f"{r['dc']:.4f}", f"{peak:.4f}", f"{trough:.4f}", f"{r['h2']:.4f}",
                f"{r['h3']:.4f}", f"{r['resid_rms']:.6f}",
                f"{r['resid_rms']*math.sqrt(2.0/r['n']):.6f}", f"{r['drift_mv_s']:.3f}",
                len(y), f"{rail:.4f}", f"{zero:.4f}", os.path.relpath(npz, self.root), flag]))
        with open(self.csv, "a", newline="") as f:
            csv.DictWriter(f, FIELDS).writerow(row)      # checkpoint after EVERY point
        self.rows.append(row)
        return r, row


def guard(rows, key="gain", tol=10.0):
    """Repeat-guard: first and last point must agree. Returns (ok, spread_pct)."""
    g = [float(r[key]) for r in rows if r.get(key) not in ("", None)]
    if len(g) < 2: return True, 0.0
    a, b = g[0], g[-1]
    spread = 100.0 * abs(a - b) / (0.5 * (a + b))
    return spread <= tol, spread
