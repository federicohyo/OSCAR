#!/usr/bin/env python3
"""Three-panel silicon figure: stimulus / LNA output / neuron spikes, FOLDED ON
THE SPIKES, with the per-repeat LNA traces kept so panel (b) can show the median
and its spread rather than a single average.

TIME BASES. The spike file carries the chip's own Timer0 clock; the LNA trace and
the injections carry host time. They are related by fitting host = a*chip + b on
spike bursts matched to injection groups -- not by anchoring on the first spike.
Anchoring failed: the neuron fires spontaneously at ~0.7 Hz and RECORD starts
before the warm-up, so the first logged spike is spontaneous and has no injection
behind it. Using it shifted the whole raster by ~0.19 s and made the spikes appear
to precede the stimulus that caused them.

Panel (c) is a raster, not a membrane trace: the readout ADC is single-channel, so
the amplifier and the membrane cannot be watched at once, and the loop needs the
amplifier.

HOST-IN-THE-LOOP: the core has no path to the LNA output, so the host thresholds
the amplifier and injects the spikes. The chip amplifies and the chip spikes; the
decision between them is made off-die.
"""
import csv, json, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LNA  = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FS = 1000.0
GAP = 0.30                      # silence longer than this separates two bursts

# --- TIMEBASE CORRECTIONS, both measured, both applied to the raster ---------
# (1) The detector thresholds a 25-sample TRAILING mean, whose group delay is
#     (25-1)/2 = 12 ms. The LNA trace and everything derived from it therefore lag
#     physical time by that much; the injections, taken from the same samples, do
#     stay aligned. Uncorrected this alone puts the spikes 12 ms early against the amplifier.
# (2) Injecting takes time. Measured host BURST -> spike line back at the
#     host: 29.6 ms median over 20 trials (sd 2.3 ms). That is the full round trip;
#     the outbound half is what delays the spike relative to the host's decision.
#     Splitting it needs a chip-side echo of command receipt, so half is
#     used and the residual uncertainty is of the same order (~7 ms).
SMOOTH_DELAY_S = 0.012
ROUND_TRIP_S   = 0.0296
OUTBOUND_S     = 0.0044   # MEASURED on the membrane pass (injection -> membrane
                          # spike, both on the host clock, 30 matched, median 4.4 ms).
                          # The round trip is asymmetric: the outbound write is fast and
                          # the ~25 ms remainder is the FTDI read-latency timer on the way
                          # back. Halving the round trip, as done before, over-corrected.

tm = json.load(open(os.path.join(LNA, "odor_timing.json")))
P, reps = tm["period_s"], tm["repeats"]
EVL = tm["event_off"] - tm["event_on"]
rows = list(csv.DictReader(open(os.path.join(LNA, "odor_stimulus.csv"))))
key = [k for k in rows[0] if "chip" in k][0]
ts = np.array([float(r["t_s"]) for r in rows]); vs = np.array([float(r[key]) for r in rows])

d = np.load(os.path.join(LNA, "odor_neuron_loop.npz"))
tr, fr = d["trace"], d["fires"]
tl, cl = tr[:, 0], tr[:, 1]
sp_c = np.array([float(l.split("\t")[2]) for l in
                 open(os.path.join(LNA, "odor_neuron_spikes.txt")) if not l.startswith("#")])/1e6
sp_c -= sp_c[0]

# --- map chip time -> host time --------------------------------------------
bstart = np.concatenate([[sp_c[0]], sp_c[1:][np.diff(sp_c) > GAP]])
gstart = np.concatenate([[fr[0, 0]], fr[1:, 0][np.diff(fr[:, 0]) > GAP]])
pairs = []
for b in bstart:                                   # nearest injection group, within 0.4 s
    j = int(np.argmin(np.abs(gstart - (b + fr[0, 0]))))
    if abs(gstart[j] - (b + fr[0, 0])) < 0.45:
        pairs.append((b, gstart[j]))
pairs = np.array(pairs)
a, b0 = np.polyfit(pairs[:, 0], pairs[:, 1], 1)
sp_h = a*sp_c + b0
resid = pairs[:, 1] - (a*pairs[:, 0] + b0)
print(f"chip->host fit on {len(pairs)} matched bursts: scale {a:.6f}, "
      f"offset {b0:.3f} s, residual {resid.std()*1e3:.1f} ms rms")
print(f"  {len(bstart)} spike bursts, {len(gstart)} injection groups")

# --- phase from the SPIKES --------------------------------------------------
bh = a*bstart + b0
k = np.round((bh - bh[0])/P)
slope, icept = np.polyfit(k, bh, 1)
print(f"burst period from the spikes: {slope:.4f} s (stimulus {P:.4f} s), "
      f"jitter {np.std(bh - (slope*k + icept))*1e3:.0f} ms rms")
t0 = icept                                        # host time of burst 0

def phase(x):                                     # seconds relative to burst onset
    return ((x - t0 + P/2) % P) - P/2

# --- per-repeat LNA traces, folded on that phase ----------------------------
grid = np.arange(-0.35, 0.65, 1.0/FS)
lna, used = [], []
for i in range(-1, reps + 2):
    c = t0 + i*P
    if c + grid[0] < tl[0] or c + grid[-1] > tl[-1]: continue
    # only periods in which the stimulus was actually playing: the recording runs
    # ~3 s past the end of the WAV, and those periods contribute a flat trace that
    # would drag the median and inflate the spread off pure noise.
    if c > tm["wav_s"] - 0.2: continue
    lna.append(np.interp(c + grid, tl, cl)); used.append(i)
lna = np.vstack(lna)
lna = lna - np.median(lna[:, grid < -0.20], axis=1, keepdims=True)
med = np.median(lna, axis=0)
q1, q3 = np.percentile(lna, 25, axis=0), np.percentile(lna, 75, axis=0)
sd = lna.std(axis=0)
print(f"per-repeat LNA traces kept: {lna.shape[0]} x {lna.shape[1]} samples")

# spikes occur OUTBOUND_S after the host decided, and the LNA trace lags physical
# time by SMOOTH_DELAY_S, so the raster moves later by the sum of the two
sp_h = sp_h + OUTBOUND_S + SMOOTH_DELAY_S
sp_ph = phase(sp_h); sp_rep = np.floor((sp_h - t0 + P/2)/P).astype(int); sp_rep -= sp_rep.min()
inj_ph = phase(fr[:, 0])
drv = np.interp(grid + tm["event_on"], ts, vs, left=vs[0], right=0.0)

# --- what the chip ACTUALLY received ---------------------------------------
# The intended stimulus differs from what arrives: the signal passes the sound card
# and the divider first. Rather than assume it is faithful, recover it by inverting the
# measured amplifier response on the median output. In 1-25 Hz the LNA is a single
# pole at the measured 1.53 Hz corner with gain ~268x, inverting; the control loop
# additionally averaged over 25 ms, so that boxcar is part of the forward path and
# is divided out too. The band stops at 25 Hz because the boxcar's first null is at
# 40 Hz and dividing near it amplifies noise while adding little signal.
FC, GAIN, BOX = 1.53, 268.0, 0.025
nn = len(grid); ff = np.fft.rfftfreq(nn, 1.0/FS)
Hl = -GAIN*(1j*ff/FC)/(1 + 1j*ff/FC)
Hb = np.sinc(ff*BOX)
bandr = (ff >= 1.0) & (ff <= 25.0)
Ymed = np.fft.rfft(med)
Xr = np.zeros_like(Ymed); Xr[bandr] = Ymed[bandr]/(Hl[bandr]*Hb[bandr])
rec_in = np.fft.irfft(Xr, nn)
Idl = np.fft.rfft(drv - drv.mean()); Ib = np.zeros_like(Idl); Ib[bandr] = Idl[bandr]
drv_b = np.fft.irfft(Ib, nn)
kk_ = np.dot(rec_in, drv_b)/np.dot(drv_b, drv_b)
rr_ = np.corrcoef(rec_in, drv_b)[0, 1]
print(f"recovered chip input vs intended: r = {rr_:+.3f}, amplitude x{kk_:.2f} "
      f"(sound card + divider deliver {100*(kk_-1):+.0f}% vs nominal)")

MUT = "#5c5f66"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUT, "xtick.color": MUT,
    "ytick.color": MUT, "axes.linewidth": .8, "grid.color": "#d7d9de",
    "legend.frameon": False, "font.family": "serif", "savefig.bbox": "tight"})
fig, ax = plt.subplots(3, 1, figsize=(3.45, 4.5), sharex=True,
                       gridspec_kw={"height_ratios": [1, 1.15, 1.05]})
# Only the RECOVERED trace is drawn: it is what the chip actually received, and it
# carries the correct timing relative to the spikes. The intended waveform is kept
# in the archive (drive_bandlimited) and quoted numerically rather than overlaid --
# drawn together the ~30 ms detection latency reads as a misalignment.
ax[0].plot(grid, rec_in*1e6, lw=1.1, color="#1f4fd8")
ax[0].set_ylabel(r"$V_{sen}$ ($\mu$V)", color="#1f4fd8")
ax[0].tick_params(axis="y", labelcolor="#1f4fd8")
for row in lna:
    ax[1].plot(grid, row*1e3, lw=.5, color="#c62828", alpha=.28)
ax[1].fill_between(grid, (med-sd)*1e3, (med+sd)*1e3, color="#c62828", alpha=.22, lw=0)
ax[1].plot(grid, med*1e3, lw=1.4, color="#8c1010")
ax[1].set_ylabel(r"$V_{LNA}^{out}$ (mV)", color="#c62828")
ax[1].tick_params(axis="y", labelcolor="#c62828")
kk = (sp_ph >= -0.35) & (sp_ph <= 0.65)
ax[2].plot(sp_ph[kk], sp_rep[kk] + 1, "|", ms=5.5, mew=1.1, color="#137a5f")
ax[2].set_ylabel("repeat", color="#137a5f")
ax[2].tick_params(axis="y", labelcolor="#137a5f")
ax[2].set_ylim(0.3, sp_rep.max() + 1.7)
ax[2].set_xlabel("time from spike-burst onset (s)")
for a_, lab in zip(ax, ("(a)", "(b)", "(c)")):
    a_.grid(alpha=.5); a_.set_axisbelow(True); a_.set_xlim(-0.35, 0.65)
    a_.annotate(lab, xy=(0.012, 0.06), xycoords="axes fraction", fontsize=9,
                fontweight="bold", color="#1b1b1f")
    for s_ in ("top", "right"): a_.spines[s_].set_visible(False)
fig.tight_layout()
for e in ("png", "pdf"):
    fig.savefig(os.path.join(ROOT, "figures", f"odor_neuron_chain.{e}"), dpi=200)
np.savez_compressed(os.path.join(ROOT, "raw", "odor_neuron", "loop.npz"),
    trace=tr, fires=fr, spikes_chip_s=sp_c, spikes_host_s=sp_h, spike_phase_s=sp_ph,
    spike_repeat=sp_rep, inj_phase_s=inj_ph, lna_trials=lna, lna_grid=grid,
    lna_median=med, lna_sd=sd, lna_q1=q1, lna_q3=q3, drive=drv,
    drive_bandlimited=drv_b, drive_recovered=rec_in, recover_gain=kk_, recover_r=rr_, chip_host_scale=a,
    chip_host_offset=b0, t0=t0, period_s=P, reps=reps, repeat_index=np.array(used))
print(f"median LNA peak {med.max()*1e3:+.1f} mV at t = {grid[int(np.argmax(med))]:+.3f} s; "
      f"spread there {sd[int(np.argmax(med))]*1e3:.1f} mV")
print(f"timebase: raster shifted +{(OUTBOUND_S+SMOOTH_DELAY_S)*1e3:.0f} ms "
      f"({SMOOTH_DELAY_S*1e3:.0f} ms detector group delay + "
      f"{OUTBOUND_S*1e3:.0f} ms outbound command latency)")
print(f"spikes {len(sp_h)} over {sp_rep.max()+1} repeats; "
      f"{(np.abs(sp_ph) <= 0.15).sum()} within +-150 ms of burst onset")
print("figures/odor_neuron_chain.png + .pdf")
