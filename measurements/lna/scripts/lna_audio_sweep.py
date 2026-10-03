#!/usr/bin/env python3
"""LNA transfer function from the audio jack, 0.1 Hz .. 400 Hz.

READ-ONLY on the chip: this script leaves the FTDI closed and the DACs untouched
DAC. The biases are whatever you loaded (LNA_chip0_110_audio_0.25.biases);
it only plays tones and listens to the scope broadcast server.

Drive path:   audio jack -> voltage divider -> LNA input
              jack level is set the way sine_out.sh sets it (0.25 Vpp
              digital), the divider brings that to --vin-pp at the chip.

Measurement:  coherent sine fit at the KNOWN drive frequency, on the
              pixhawk board clock (a clean 1 ms grid, 1000 S/s).
              rather than a p5-p95 spread: with the tone off the node already
              carries ~66 mVpp of mains hum and ADC spikes, which would
              floor the stopband at a fake ~19 dB. The fit rejects
              everything outside f0 and reports the leftover as
              `resid_rms`, so every point carries its own error bar.
              Harmonics 2f and 3f are fitted alongside, so clipping shows
              up as h2/h3 instead of hiding inside the amplitude.

Two passes are needed for a real answer below ~20 Hz -- the audio jack is
AC-coupled, so its own high-pass is in series with the amplifier:

  1. probe on the LNA OUTPUT :  lna_audio_sweep.py --out lna_transfer_out.csv
  2. probe on the DIVIDER OUT :  lna_audio_sweep.py --ref --out lna_transfer_ref.csv
  3. divide                   :  lna_audio_sweep.py --divide lna_transfer_out.csv lna_transfer_ref.csv

Pass 2 measures what the chip is actually being fed at each frequency, so
pass 3 cancels the jack and the divider and leaves the LNA alone. That also fixes
the sub-20 Hz decade as the sound card's roll-off rather than the amp's.

Prereqs: the scope server must be running (127.0.0.1:5555). The GUI and
neuron_bridge.py may stay open -- the FTDI is left untouched. Leave
the mixer volume: the --vin-pp calibration rides on its current setting.
"""

import argparse
import csv
import json
import math
import os
import signal
import socket
import subprocess
import sys
import time
import wave

import numpy as np

SCOPE_SERVER = ("127.0.0.1", 5555)
FULL_SCALE_VRMS = 1.0          # same assumption as sine_out.sh
BOARD_DT = 0.001               # pixhawk stream: exact 1 ms grid
VDD = 1.78


# ----------------------------------------------------------------- audio

def make_wav(path, freq, vpp, min_dur, fs=44100):
    """Whole number of cycles, and long enough that a single playback covers
    the whole measurement.

    pw-play is relaunched each time the file ends, and the relaunch leaves a
    ~100 ms silent gap. A gap inside the measurement window cost 17% of the
    amplitude on the first 100 Hz trial (567 vs 680 mVpp), so the file must
    outlast settle+window rather than loop during it.

    Amplitude uses sine_out.sh's formula exactly -- the divider calibration
    was taken with that level, so it must stay fixed here."""
    amp = min((vpp / 2) / (FULL_SCALE_VRMS * math.sqrt(2)), 1.0)
    n = int(fs * max(min_dur, 4.0 / freq))
    per = max(1, round(fs / freq))
    n = max(per, n - n % per)
    t = np.arange(n) / fs
    pcm = (32767 * amp * np.sin(2 * math.pi * freq * t)).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(pcm.tobytes())
    return amp


class AudioOut:
    def __init__(self):
        self.proc = None

    def play(self, wav):
        self.stop()
        self.proc = subprocess.Popen(
            ["bash", "-c", 'while :; do pw-play -- "$1" || exit 1; done', "_", wav],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)

    def stop(self):
        if self.proc is not None:
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
                self.proc.wait(timeout=2)
            except Exception:
                pass
            self.proc = None


# ----------------------------------------------------------------- scope

class Scope:
    """Reader for the scope broadcast server.

    Yields (board_time, volts). The first line after connecting is dropped:
    the first recv lands mid-line and the fragment parses as a plausible
    sample with a garbage timestamp (seen as a 2245 s jump in the clock)."""

    def __init__(self, server=SCOPE_SERVER):
        self.sk = socket.create_connection(server, timeout=5.0)
        self.sk.settimeout(1.0)
        self.buf = b""
        self._first = True
        self.drain(0.5)

    def close(self):
        try:
            self.sk.close()
        except OSError:
            pass

    def _read(self):
        rec = []
        try:
            chunk = self.sk.recv(65536)
        except socket.timeout:
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
            if len(q) >= 2:
                try:
                    rec.append((float(q[0]), float(q[1])))
                except ValueError:
                    pass
        return rec

    def drain(self, seconds):
        t0 = time.time()
        while time.time() - t0 < seconds:
            self._read()

    def collect(self, seconds):
        """Collect for `seconds` of host time; return (t_board, volts)."""
        rec = []
        t0 = time.time()
        while time.time() - t0 < seconds:
            rec.extend(self._read())
        if len(rec) < 20:
            raise RuntimeError(f"scope stalled ({len(rec)} samples in {seconds:.1f} s)")
        a = np.asarray(rec, dtype=float)
        return a[:, 0], a[:, 1]


def longest_contiguous(t, v):
    """Longest gap-free run, with a time axis that does not depend on the
    printed clock's resolution.

    The pixhawk prints its clock as %+.6E -- 7 significant digits. Once its
    uptime passes 10^4 s that format resolves only 10 ms, so ten consecutive
    1 ms samples carry an IDENTICAL timestamp and a per-sample dt test sees
    zero everywhere and returns 1-sample runs. Below 10^4 s it happens to give
    exactly 1 ms, which is why this only appears after ~2.8 h of uptime.

    So: use the board clock only to find real GAPS (which are far larger than
    its quantisation), and reconstruct time inside a run from the sample index,
    since the device streams a steady 1 kS/s grid. The run's board-clock span
    is then checked against the index span to catch dropped samples."""
    t = np.asarray(t, float)
    if len(t) < 3:
        return np.arange(len(t)) * BOARD_DT, v
    quant = 10.0 ** (math.floor(math.log10(max(abs(t[-1]), 1.0))) - 6)
    d = np.diff(t)
    gap = np.abs(d) > max(20 * BOARD_DT, 5 * quant)
    edges = np.concatenate(([0], np.flatnonzero(gap) + 1, [len(t)]))
    i0, i1 = max(zip(edges[:-1], edges[1:]), key=lambda e: e[1] - e[0])
    n = i1 - i0
    span_board = t[i1 - 1] - t[i0]
    span_idx = (n - 1) * BOARD_DT
    if span_idx > 1.0 and abs(span_board - span_idx) > max(0.02 * span_idx, 5 * quant):
        # the clock and the sample count disagree: samples were dropped, and an
        # index-based axis would slew the phase. Fall back to the board clock.
        return t[i0:i1], v[i0:i1]
    return np.arange(n) * BOARD_DT, v[i0:i1]


# ------------------------------------------------------------------- fit

def sine_fit(t, v, f0, nharm=3):
    """Least squares at the KNOWN drive frequency, plus harmonics and a
    linear trend (the node drifts slowly; the trend term keeps the LF
    points from absorbing the drift into the fundamental).

    Returns dict with fundamental amplitude (zero-to-peak), phase, DC,
    harmonic ratios and the residual rms."""
    t = t - t[0]
    # Only harmonics BELOW Nyquist may be fitted. Above it they alias, and at
    # f0 > fs/3 the 2f and 3f aliases land on the same frequency, making their
    # columns collinear -- the solve then returns huge cancelling coefficients
    # (h2 = h3 = 7.2e6 was seen at 400 Hz). The fundamental survives that, but
    # the harmonic ratios are meaningless, so they are left out of the report.
    nyq = 0.5 / BOARD_DT
    nfit = max(1, min(nharm, int(nyq / f0 - 1e-9)))
    cols = [np.ones_like(t), t]
    for h in range(1, nfit + 1):
        cols += [np.sin(2 * math.pi * h * f0 * t), np.cos(2 * math.pi * h * f0 * t)]
    M = np.column_stack(cols)
    c, *_ = np.linalg.lstsq(M, v, rcond=None)
    resid = v - M @ c
    amps = [math.hypot(c[2 + 2 * i], c[3 + 2 * i]) for i in range(nfit)]
    a1 = amps[0]
    nharm = nfit
    return {
        "amp": a1,
        "vpp": 2 * a1,
        "phase_deg": math.degrees(math.atan2(c[3], c[2])),
        "sin_cos": (float(c[2]), float(c[3])),
        "dc": float(np.mean(v)),
        "drift_mv_s": c[1] * 1e3,
        "h2": amps[1] / a1 if nharm > 1 and a1 > 0 else float("nan"),
        "h3": amps[2] / a1 if nharm > 2 and a1 > 0 else float("nan"),
        "nharm_fitted": nharm,
        "resid_rms": float(np.sqrt(np.mean(resid ** 2))),
        "vmin": float(v.min()),
        "vmax": float(v.max()),
        "n": len(v),
    }


def clipped_sine_fit(t, v, f0, lo=0.0, hi=VDD):
    """Fit a sine that the ADC has CLIPPED, using every sample.

    Thresholding to "the part above zero" and fitting that is biased: near the
    threshold a sample is kept only when noise pushed it up, so the estimate
    inflates. Measured on the jack at 1 Vpp it read 1083 mVpp while every sample
    stayed below 509 mV. The bias grows as noise approaches the signal, i.e. it is
    worst at the low frequencies the reference pass exists to measure -- it
    would flatten the roll-off it is meant to reveal.

    So fit the clipping itself: model = clip(A sin + B cos + C, lo, hi) against
    all samples. The clamped samples are information too -- they say the signal
    was below the floor at that instant."""
    from scipy.optimize import least_squares
    T = t - t[0]
    sn, cs = np.sin(2 * math.pi * f0 * T), np.cos(2 * math.pi * f0 * T)

    def resid(p):
        return np.clip(p[0] * sn + p[1] * cs + p[2], lo, hi) - v

    a0 = max(float(np.percentile(v, 99)), 1e-4)
    best = None
    for ph in (0.0, math.pi / 2):                 # two starts: phase stays outside the pre-fit observable
        p0 = [a0 * math.cos(ph), a0 * math.sin(ph), 0.0]
        try:
            r = least_squares(resid, p0, method="lm", max_nfev=4000)
        except Exception:
            continue
        if best is None or r.cost < best.cost:
            best = r
    if best is None:
        return None
    a1 = math.hypot(best.x[0], best.x[1])
    rr = float(np.sqrt(np.mean(best.fun ** 2)))
    unclamped = int((v > lo + 1e-4).sum())
    if unclamped < 60:
        return None
    return {
        "amp": a1, "vpp": 2 * a1, "dc": float(best.x[2]),
        "drift_mv_s": 0.0, "h2": float("nan"), "h3": float("nan"),
        "nharm_fitted": 1, "resid_rms": rr,
        "vmin": float(v.min()), "vmax": float(v.max()),
        "n": len(v), "kept_frac": unclamped / len(v),
    }


def halfwave_fit(t, v, f0, adc_floor=0.0005):
    """Amplitude of a sine that the unipolar ADC has chopped at 0 V.

    The pixhawk reads 0 V and up. A signal with zero DC offset -- the audio
    jack is AC-coupled, so its output swings about 0 -- loses its whole
    negative half. The positive half survives untouched, so fit only the
    samples clear of the floor. Verified on synthetic data against the
    measured 0.7 mV noise of that node: 0.04% at 250 mVpp, 0.5% at 30 mVpp,
    and it gives up below ~10 mVpp, where too little stands above the noise."""
    a99 = float(np.percentile(v, 99))
    thr = max(4 * adc_floor, 0.10 * a99)
    m = v > thr
    if m.sum() < 60:
        return None
    T, V = t[m], v[m]
    M = np.column_stack([np.sin(2 * math.pi * f0 * T),
                         np.cos(2 * math.pi * f0 * T), np.ones_like(T)])
    c, *_ = np.linalg.lstsq(M, V, rcond=None)
    resid = V - M @ c
    a1 = math.hypot(c[0], c[1])
    rms = float(np.sqrt(np.mean(resid ** 2)))
    # Phase, on the same convention as sine_fit: atan2(cos-coeff, sin-coeff),
    # measured against t[0] of the array handed in. Half-wave rectification does
    # leave the fundamental's phase unchanged -- the chopped-off half stays outside
    # the fit -- so this is the input's phase even though the amplitude estimate
    # needs the care documented above.
    return {
        "amp": a1, "vpp": 2 * a1, "dc": float(np.mean(v)),
        "phase_deg": math.degrees(math.atan2(c[1], c[0])),
        "sin_cos": (float(c[0]), float(c[1])),
        "drift_mv_s": 0.0, "h2": float("nan"), "h3": float("nan"),
        "nharm_fitted": 1, "resid_rms": rms,
        "vmin": float(v.min()), "vmax": float(v.max()),
        "n": int(m.sum()), "kept_frac": float(m.mean()),
    }


def decommensurate(f, fs=1.0 / BOARD_DT):
    """Nudge a test frequency off any simple ratio with the sample rate.

    At 1000 S/s a 100.000 Hz tone is sampled at exactly 10 samples per cycle
    and the SAME 10 phases repeat endlessly -- the sampler misses the rest of
    the waveform. Measured: 100.00 Hz gave 11 distinct phases and 8.1% spread
    over three trials; 97.30 Hz gave 1001 phases and 0.5%. Harmless for an
    unclipped sine (least squares is exact from 3 phases) but ruinous for the
    clipped fit, which needs the waveform near its zero crossing and its peak.

    f0/fs = N/100000 with N = round(100*f0), so the phase pattern repeats every
    100000/gcd(N,100000) samples. 100000 = 2^5 * 5^5, so choosing N coprime to
    10 -- last digit 1, 3, 7 or 9 -- makes the period maximal.

    Only applied above 10 Hz; below that a cycle spans 100+ samples and the
    phase coverage is ample regardless."""
    if f <= 10.0:
        return f
    n = int(round(f * 100))
    while n % 10 not in (1, 3, 7, 9):
        n += 1
    return n / 100.0


# ----------------------------------------------------------------- sweep

FIELDS = ["freq_hz", "vin_pp", "vpp_out", "gain", "gain_db", "amp_mv",
          "dc_v", "vmin_v", "vmax_v", "resid_mv", "amp_err_pct", "h2", "h3",
          "drift_mv_s", "n_samples", "n_cut", "clip"]


def drop_dropouts(t, v, f0, block_s=0.05):
    """Cut samples where playback fell silent (envelope collapses).

    Only meaningful when a block holds at least a cycle, so it is skipped
    below 5 Hz -- where a 100 ms gap is negligible against the period."""
    if f0 < 5.0:
        return t, v, 0
    bs = max(10, int(block_s / BOARD_DT))
    nb = len(v) // bs
    if nb < 4:
        return t, v, 0
    env = np.array([np.ptp(v[i * bs:(i + 1) * bs]) for i in range(nb)])
    keep = env > 0.5 * np.median(env)
    if keep.all():
        return t, v, 0
    m = np.repeat(keep, bs)
    m = np.concatenate([m, np.ones(len(v) - len(m), bool)])
    return t[m], v[m], int((~keep).sum() * bs)


def measure_point(scope, audio, wavdir, f0, args, label=""):
    settle = min(max(2.0 / f0, args.settle_min), args.settle_max)
    window = min(max(4.0 / f0, args.window_min), args.window_max)

    wav = os.path.join(wavdir, f"tone_{f0:.4f}hz_{args.jack_vpp:g}vpp.wav")
    if not os.path.exists(wav):
        make_wav(wav, f0, args.jack_vpp, min_dur=settle + window + args.trim + 3.0)
    audio.play(wav)

    # let the input stabilise, then cut the leading transient outright
    scope.drain(settle)
    t, v = longest_contiguous(*scope.collect(window + args.trim))
    ntrim = int(args.trim / BOARD_DT)
    if len(v) > ntrim + 100:
        t, v = t[ntrim:], v[ntrim:]
    t, v, ndrop = drop_dropouts(t, v, f0)

    # A node at zero DC offset is chopped by the unipolar ADC; a normal fit
    # would then read the clamped stub rather than the signal. Detect and switch.
    clamped = float((v <= 0.0005).mean())
    r = None
    if clamped > 0.10:
        r = clipped_sine_fit(t, v, f0)
        if r is not None:
            r["mode"] = f"clipfit({100*clamped:.0f}%clamped)"
    if r is None:
        r = sine_fit(t, v, f0)
        r["mode"] = ""
    r["ndrop"] = ndrop

    gain = r["vpp"] / args.vin_pp
    r["freq_hz"] = f0
    r["gain"] = gain
    r["gain_db"] = 20 * math.log10(gain) if gain > 0 else float("nan")
    # A coherent fit averages uncorrelated noise down over N samples, so the
    # error bar on the amplitude is resid*sqrt(2/N) -- rather than amp/resid, which
    # would condemn a perfectly good point just because the node is noisy.
    r["amp_se"] = r["resid_rms"] * math.sqrt(2.0 / r["n"])
    r["amp_err_pct"] = 100.0 * r["amp_se"] / r["amp"] if r["amp"] > 0 else float("nan")
    r["clip"] = r.get("mode", "")
    headroom = min(VDD - (r["dc"] + r["amp"]), (r["dc"] - r["amp"]))
    if not r["clip"] and headroom < 0.05:
        r["clip"] = "NEAR-RAIL"
    if (r["h2"] > 0.10) or (r["h3"] > 0.10):   # NaN compares False -- intended
        r["clip"] = (r["clip"] + " DIST").strip()
    if r["amp"] < 5 * r["amp_se"]:
        r["clip"] = (r["clip"] + " WEAK").strip()
    if r["ndrop"]:
        r["clip"] = (r["clip"] + f" CUT{r['ndrop']}").strip()

    print(f"  {label}{f0:8.3f} Hz -> {r['vpp']*1e3:8.2f} mVpp "
          f"+/-{r['amp_err_pct']:4.1f}%  {r['gain_db']:7.2f} dB   "
          f"DC {r['dc']:.3f} V  hd {headroom*1e3:4.0f} mV  "
          f"h2 {r['h2']:.3f} h3 {r['h3']:.3f}  {r['clip']}")
    return r


def row_of(r, vin_pp):
    return {
        "freq_hz": f"{r['freq_hz']:.4f}", "vin_pp": f"{vin_pp:.5f}",
        "vpp_out": f"{r['vpp']:.6f}", "gain": f"{r['gain']:.4f}",
        "gain_db": f"{r['gain_db']:.3f}", "amp_mv": f"{r['amp']*1e3:.4f}",
        "dc_v": f"{r['dc']:.4f}", "vmin_v": f"{r['vmin']:.4f}",
        "vmax_v": f"{r['vmax']:.4f}", "resid_mv": f"{r['resid_rms']*1e3:.4f}",
        "amp_err_pct": f"{r['amp_err_pct']:.3f}", "h2": f"{r['h2']:.4f}",
        "h3": f"{r['h3']:.4f}", "drift_mv_s": f"{r['drift_mv_s']:.3f}",
        "n_samples": r["n"], "n_cut": r.get("ndrop", 0), "clip": r["clip"],
    }


def do_divide(out_csv, ref_csv, png, anchor_hz=100.0, anchor_vin=0.007):
    """Correct the transfer function for the drive path's own response.

    The reference may be taken at a different jack level than the sweep (more
    level = better SNR where the jack attenuates), so only its SHAPE is used:
    the reference is normalised at `anchor_hz`, where the input is known to be
    `anchor_vin` from the bench measurement. That makes the result independent
    of the reference's absolute level."""
    def load(p):
        with open(p) as f:
            return {round(float(r["freq_hz"]), 4): r for r in csv.DictReader(f)}
    o, rf = load(out_csv), load(ref_csv)
    common = sorted(set(o) & set(rf))
    if not common:
        sys.exit("the two passes have disjoint frequency sets")
    # the reference runs on decommensurate frequencies, so interpolate it
    # (log-log: both axes are naturally logarithmic here) onto the sweep's.
    rfk = np.array(sorted(rf))
    rfv = np.array([float(rf[k]["vpp_out"]) for k in rfk])
    ok = rfv > 0
    def ref_at(f):
        return float(np.exp(np.interp(math.log(f), np.log(rfk[ok]), np.log(rfv[ok]))))
    common = sorted(k for k in o if rfk[ok].min() <= k <= rfk[ok].max())
    if not common:
        sys.exit("the two passes have disjoint frequency ranges")
    ref_anchor = ref_at(anchor_hz)
    print(f"anchor: {anchor_hz:g} Hz, reference reads {ref_anchor*1e3:.2f} mVpp there, "
          f"chip input is {anchor_vin*1e3:g} mVpp -> scale {anchor_vin/ref_anchor:.5f}\n")
    print(f"{'freq':>10} {'Vout pp':>10} {'Vin pp':>10} {'gain':>8} {'dB':>8}")
    rows = []
    for f0 in common:
        vo = float(o[f0]["vpp_out"])
        vi = ref_at(f0) / ref_anchor * anchor_vin
        g = vo / vi if vi > 0 else float("nan")
        db = 20 * math.log10(g) if g > 0 else float("nan")
        rows.append((f0, vo, vi, g, db))
        print(f"{f0:10.3f} {vo*1e3:9.2f}m {vi*1e3:9.3f}m {g:8.2f} {db:8.2f}")
    dst = os.path.splitext(out_csv)[0] + "_corrected.csv"
    with open(dst, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["freq_hz", "vpp_out", "vpp_in_measured", "gain", "gain_db"])
        for r in rows:
            w.writerow([f"{r[0]:.4f}", f"{r[1]:.6f}", f"{r[2]:.6f}",
                        f"{r[3]:.4f}", f"{r[4]:.3f}"])
    print(f"\ncorrected transfer -> {dst}")
    plot([(r[0], r[4]) for r in rows], png, "LNA transfer (audio path divided out)")


def plot(pairs, png, title):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"plot skipped: {e}")
        return
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.semilogx([p[0] for p in pairs], [p[1] for p in pairs], "o-", ms=4)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("gain [dB]")
    ax.grid(True, which="both", alpha=0.3)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(png, dpi=150)
    print(f"plot: {png}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fmin", type=float, default=0.1)
    ap.add_argument("--fmax", type=float, default=400.0)
    ap.add_argument("--ppd", type=int, default=6, help="points per decade")
    ap.add_argument("--jack-vpp", type=float, default=0.25,
                    help="digital level at the jack, as sine_out.sh takes it")
    ap.add_argument("--vin-pp", type=float, default=0.007,
                    help="measured Vpp at the chip input, after the divider")
    ap.add_argument("--ref", action="store_true",
                    help="reference pass: probe is on the DIVIDER OUTPUT rather than the LNA")
    ap.add_argument("--divide", nargs=2, metavar=("OUT_CSV", "REF_CSV"),
                    help="combine two passes into the corrected transfer function")
    ap.add_argument("--trim", type=float, default=1.0,
                    help="seconds of the window discarded before fitting")
    ap.add_argument("--settle-min", type=float, default=2.5)
    ap.add_argument("--settle-max", type=float, default=15.0)
    ap.add_argument("--window-min", type=float, default=2.0)
    ap.add_argument("--window-max", type=float, default=45.0)
    ap.add_argument("--ref-freq", type=float, default=100.0,
                    help="sanity point measured first (0 disables)")
    ap.add_argument("--out", default="")
    ap.add_argument("--png", default="")
    ap.add_argument("--wavdir", default="")
    args = ap.parse_args()

    if args.divide:
        return do_divide(args.divide[0], args.divide[1],
                         args.png or "lna_transfer_corrected.png",
                         args.ref_freq or 100.0, args.vin_pp)

    out_csv = args.out or ("lna_transfer_ref.csv" if args.ref else "lna_transfer_out.csv")
    png = args.png or os.path.join("figures", os.path.splitext(os.path.basename(out_csv))[0] + ".png")
    os.makedirs("figures", exist_ok=True)
    if os.path.exists(out_csv):
        sys.exit(f"{out_csv} exists -- move it or pass --out; refusing to append")
    wavdir = args.wavdir or f"wavs_{args.jack_vpp:g}vpp"
    os.makedirs(wavdir, exist_ok=True)

    decades = math.log10(args.fmax / args.fmin)
    npts = max(2, int(round(decades * args.ppd)) + 1)
    freqs = [decommensurate(args.fmin * 10 ** (decades * i / (npts - 1)))
             for i in range(npts)]

    est = sum(min(max(2.0 / f, args.settle_min), args.settle_max) + args.trim +
              min(max(4.0 / f, args.window_min), args.window_max) for f in freqs)
    node = "DIVIDER OUTPUT (reference pass)" if args.ref else "LNA OUTPUT"
    print(f"probe should be on: {node}")
    print(f"jack {args.jack_vpp:g} Vpp -> chip {args.vin_pp*1e3:g} mVpp")
    print(f"{npts} points, {args.fmin:g}..{args.fmax:g} Hz, ~{est/60:.1f} min "
          f"(+{len(freqs)*1.0:.0f} s of wav generation)")
    print(f"-> {out_csv}\n")

    subprocess.run(["systemctl", "--user", "stop", "sine_out"], capture_output=True)
    subprocess.run(["pkill", "-f", "[s]ine_out.sh"], capture_output=True)

    scope = Scope()
    audio = AudioOut()
    f = open(out_csv, "w", newline="")
    log = csv.DictWriter(f, FIELDS)
    log.writeheader()
    rows = []
    try:
        if args.ref_freq > 0:
            print("sanity point first (should reproduce the level you saw by hand):")
            r = measure_point(scope, audio, wavdir, args.ref_freq, args, label="ref ")
            log.writerow(row_of(r, args.vin_pp))
            f.flush()
            print()

        print("sweep:")
        for f0 in freqs:
            r = measure_point(scope, audio, wavdir, f0, args)
            log.writerow(row_of(r, args.vin_pp))
            f.flush()
            rows.append((f0, r["gain_db"]))
    except KeyboardInterrupt:
        print("\ninterrupted -- partial results kept")
    finally:
        audio.stop()
        scope.close()
        f.close()

    if rows:
        plot(rows, png, f"{'divider output' if args.ref else 'LNA output'}  "
                        f"(jack {args.jack_vpp:g} Vpp)")
    print(f"data: {out_csv}")
    if not args.ref:
        print("\nNOTE: the audio jack is AC-coupled. Points below ~20 Hz include the")
        print("jack's own high-pass, not just the amplifier. Move the probe to the")
        print("divider output and re-run with --ref, then --divide, to get the")
        print("amplifier alone.")


if __name__ == "__main__":
    sys.exit(main())
