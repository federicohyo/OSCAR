#!/usr/bin/env python3
"""The odor chain on silicon, end to end, from one 2-channel recording.

    ../.venv-meas/bin/python3 odor_chain_figure.py

Reads what odor_neuron_loop_dual.py saved -- no bench, no chip -- and produces
figures/odor_chain_dual.png plus the numbers that go with it:

  panel 1  the stimulus that was played (the WAV itself)
  panel 2  ch1, the LNA output, with the trailing baseline, the detection
           threshold, and every injection the host decided to make
  panel 3  ch2, the membrane monitor of neuron 9, with the chip's own AER
           spike times underneath

TIME BASE. Nothing is aligned on playback start: pw-play's start latency jitters
by more than a second. The 137 Hz, 50 ms mark at t_mark = 0.125 s of every period
is found in ch1 itself and everything is referred to that.

THE EVENT WINDOW COMES FROM THE WAV, not from odor_timing.json. That file's
event_on/event_off (0.330-0.565 s) describe the SPICE/paper stimulus; in the WAV
that is actually played the odor content of each period runs 0.50-1.26 s and
peaks at 1.05 s. Scoring against the json window reports 0% and looks like a
broken chain -- it is a mismatched clock, not a mismatched result.

SPIKE ALIGNMENT. The spike file's t = 0 is its own first spike. Neuron 9 is
quiescent without input (measured: 0 AER spikes in the idle gate window), so the
first recorded spike is the answer to the first injection, and that is what the
two clocks are pinned on.
"""
import json, os, sys
import numpy as np
import wave
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(HERE, "odor_neuron_loop_dual.npz")
OUT = os.path.join(HERE, "figures", "odor_chain_dual.png")


def wav_period(path, P):
    w = wave.open(path)
    fs = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768.0
    one = int(round(P * fs))
    return fs, x[:one], np.arange(one) / fs


def event_window(seg, fs):
    """Where the odor content actually is: low-frequency energy above 30% of peak."""
    n = len(seg)
    f = np.fft.rfftfreq(n, 1 / fs)
    lo = np.abs(np.fft.irfft(np.fft.rfft(seg) * (f < 20), n))
    k = max(1, int(0.02 * fs))
    lo = np.convolve(lo, np.ones(k) / k, "same")
    a = np.flatnonzero(lo > 0.3 * lo.max())
    return a[0] / fs, a[-1] / fs, float(np.argmax(lo)) / fs


def mark_phase(t, v, fs, P, mark_hz):
    """Phase of the 137 Hz mark within the period, using every repeat at once.

    Thresholding the mark envelope and taking crossings is brittle -- with the
    neuron injecting, ch1 carries more energy and a 4-sigma threshold silently
    misses marks (7 of 10 found, apparent spacing 2.4 s instead of 1.6 s). The
    period is known exactly, so fold on it instead: all ten marks then add.
    """
    n = len(v)
    f = np.fft.rfftfreq(n, 1 / fs)
    m = np.abs(np.fft.irfft(np.fft.rfft(v - v.mean()) * (np.abs(f - mark_hz) < 6.0), n))
    k = max(1, int(0.02 * fs))
    m = np.convolve(m, np.ones(k) / k, "same")
    nb = int(round(P * fs))
    idx = np.clip(((t - t[0]) % P / P * nb).astype(int), 0, nb - 1)
    prof = np.bincount(idx, weights=m, minlength=nb) / np.maximum(np.bincount(idx, minlength=nb), 1)
    ph = float(np.argmax(prof)) / nb * P
    snr = prof.max() / np.median(prof)
    return (ph + t[0]) % P, snr


def main():
    d = np.load(NPZ, allow_pickle=True)
    tm = json.load(open(os.path.join(HERE, "odor_timing.json")))
    P = float(d["period_s"])
    raw, fires, trace = d["raw"], d["fires"], d["trace"]
    # col 0 is the scope board clock (one stamp per sample); col 1 is the host
    # stamp of the whole batch and repeats, so it cannot be the time axis.
    t = raw[:, 0] - raw[0, 0] + raw[0, 1]
    ch1, ch2 = raw[:, 2], raw[:, 3]
    fs = 1.0 / np.median(np.diff(t))

    mph, snr = mark_phase(t, ch1, fs, P, tm["mark_hz"])
    if snr < 3.0:
        print(f"timing mark not visible in ch1 (snr {snr:.1f}) -- cannot align"); return 1
    lat = (mph - tm["t_mark"]) % P

    fsw, seg, tsw = wav_period(os.path.join(HERE, "odor_stimulus.wav"), P)
    ev_on, ev_off, ev_pk = event_window(seg, fsw)

    spk = np.atleast_2d(np.loadtxt(str(d["spikes_file"]), comments="#"))
    # The file's microsecond column is NOT zero-based despite its header (this run
    # starts at 14.994 s): it is the wrap-corrected chip clock, whose origin is the
    # bridge, not the recording. Only differences are meaningful, so pin the first
    # spike to the first injection -- neuron 9 is quiescent without input (0 AER
    # spikes in the idle gate), so that spike is the answer to that injection.
    st = (spk[:, 2] - spk[0, 2]) / 1e6 + (fires[0, 0] if len(fires) else 0.0)

    chance = (ev_off - ev_on) / P
    sph = (st - lat) % P
    inside = ((sph >= ev_on) & (sph <= ev_off)).sum()
    fph = (fires[:, 0] - lat) % P
    f_in = ((fph >= ev_on) & (fph <= ev_off)).sum()

    print(f"timing mark at phase {mph:.3f} s (snr {snr:.1f}); pw-play latency {lat:.3f} s")
    print(f"event window from the WAV: {ev_on:.3f}-{ev_off:.3f} s, peak {ev_pk:.3f} s"
          f"  (chance = {100*chance:.0f}% of the period)")
    print(f"injections inside the event: {f_in}/{len(fires)}")
    print(f"chip spikes inside the event: {inside}/{len(st)}  ({100*inside/len(st):.0f}%"
          f" vs {100*chance:.0f}% by chance)")
    print(f"ch1 {ch1.mean():.4f} V dc, {np.ptp(ch1)*1e3:.0f} mVpp;  "
          f"ch2 {ch2.mean():.4f} V dc, {np.ptp(ch2)*1e3:.0f} mVpp")

    # ---- figure ----------------------------------------------------------
    t0, t1 = lat + 3 * P, lat + 6 * P          # three settled periods
    fig, ax = plt.subplots(3, 1, figsize=(11, 7.5), sharex=True,
                           gridspec_kw={"height_ratios": [1, 1.4, 1.4]})

    reps = int(np.ceil((t1 - t0) / P)) + 2
    tw = np.concatenate([tsw + lat + (3 + i) * P for i in range(reps)])
    xw = np.tile(seg, reps)
    ax[0].plot(tw, xw * 1e3, lw=0.5, color="0.35")
    ax[0].set_ylabel("stimulus\n(WAV, mV)")
    ax[0].set_title("odor -> LNA -> neuron 9, on silicon "
                    f"(host-in-the-loop; {tm['chip_vpp']*1e6:.0f} uVpp at the chip)")

    m = (t >= t0 - 0.05) & (t <= t1 + 0.05)
    ax[1].plot(t[m], ch1[m] * 1e3, lw=0.6, color="tab:blue", label="ch1  LNA output")
    tt = trace[:, 0]
    mt = (tt >= t0 - 0.05) & (tt <= t1 + 0.05)
    ax[1].plot(tt[mt], trace[mt, 2] * 1e3, lw=1.0, color="k", label="trailing baseline")
    ax[1].plot(tt[mt], (trace[mt, 2] + float(d["thresh_mv"]) / 1e3) * 1e3,
               lw=1.0, ls="--", color="tab:red", label="threshold")
    fm = (fires[:, 0] >= t0) & (fires[:, 0] <= t1)
    for x in fires[fm, 0]:
        ax[1].axvline(x, color="tab:orange", lw=0.8, alpha=0.8)
    ax[1].plot([], [], color="tab:orange", lw=0.8, label="injection (host decision)")
    ax[1].set_ylabel("LNA output (mV)")
    ax[1].legend(loc="upper right", fontsize=8, ncol=2)

    ax[2].plot(t[m], ch2[m] * 1e3, lw=0.6, color="tab:green", label="ch2  membrane, neuron 9")
    sm = (st >= t0) & (st <= t1)
    y = ch2[m].min() * 1e3 - 30
    ax[2].plot(st[sm], np.full(sm.sum(), y), "|", ms=12, color="k",
               label=f"AER spikes ({len(st)} total)")
    ax[2].set_ylabel("membrane (mV)")
    ax[2].set_xlabel("time (s), same clock for all three panels")
    ax[2].legend(loc="upper right", fontsize=8)

    for a in ax:
        for i in range(3, 7):
            a.axvspan(lat + i * P + ev_on, lat + i * P + ev_off,
                      color="tab:olive", alpha=0.12, lw=0)
    ax[0].set_xlim(t0, t1)
    fig.text(0.995, 0.005, "shaded = odor event (measured on the WAV)",
             ha="right", fontsize=8, color="0.4")
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
