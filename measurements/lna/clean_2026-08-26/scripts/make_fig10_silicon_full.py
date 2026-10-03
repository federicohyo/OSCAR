#!/usr/bin/env python3
"""Silicon counterpart of Fig. 10, all three panels: input, LNA output, membrane.

Panel (c) is the real membrane trace, not a raster, and it carries no timing
correction: the membrane and the injection commands are both on the host clock,
so no chip-to-host mapping enters. That also made the outbound command latency
directly measurable -- 4.4 ms median over 30 matched injections, against the
14.8 ms that halving the 29.6 ms round trip had implied. The round trip is
asymmetric; most of it is the FTDI read-latency timer on the way back.

Panels (a) and (b) come from the closed-loop run of 2026-08-26 20:17. Panel (c)
now comes from the LATER two-channel run (odor_neuron_loop_dual.npz, 23:0x),
where the amplifier and the membrane were recorded at the same time -- the whole
point of the second scope channel.

Panel (b) is deliberately NOT taken from that same two-channel run. With the
neuron firing, its spikes couple into the amplifier output: >30 Hz RMS on the LNA
channel is 34.8 mV during events against 11.5 mV outside them, a 3x rise that is
absent from the single-channel recording. Panel (b) therefore keeps the clean
acquisition and panel (c) takes the membrane, which is what the second channel
was needed for.

The two runs are separate closed loops with DIFFERENT injection schedules, so
they are no longer aligned on a shared train. Both lock to the same 1.6 s
stimulus period (circular concentration R = 0.98 in the new run), and both panels
are folded on event onset, so the alignment is to the stimulus, not to each other.

The membrane axis carries a small residual offset: ch2 is stamped by the scope
board clock and the injections by the host clock, tied together at the first
sample batch, which leaves a few ms of unknown skew -- immaterial against the
1 s window drawn here, but not zero.

(b) is corrected by -12 ms, the group delay of the detector's 25-sample trailing
mean, so it sits in physical time alongside the others.
"""
import csv, json, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LNA  = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FS, SMOOTH_DELAY = 1000.0, 0.012

tm = json.load(open(os.path.join(LNA, "odor_timing.json")))
P = tm["period_s"]
loop = np.load(os.path.join(LNA, "odor_neuron_loop.npz"))
tr, fr = loop["trace"], loop["fires"]
tl, cl = tr[:, 0] - SMOOTH_DELAY, tr[:, 1]
t0L = fr[0, 0]

dual = np.load(os.path.join(LNA, "odor_neuron_loop_dual.npz"), allow_pickle=True)
draw = dual["raw"]
# col 0 is the scope board clock, one stamp per sample; col 1 is the host stamp of
# a whole batch and repeats, so it cannot be the axis. Tie the board clock to the
# run's time base at the first batch.
tmb = draw[:, 0] - draw[0, 0] + draw[0, 1]
vmb = draw[:, 3]                    # ch2 = membrane monitor of neuron 9
t0M = dual["fires"][0, 0]           # first injection of the first event

grid = np.arange(-0.35, 0.65, 1.0/FS)
def fold(t, v, t0, nmax=12):
    out = []
    for i in range(-1, nmax):
        c = t0 + i*P
        if c + grid[0] < t[0] or c + grid[-1] > t[-1]: continue
        if c > t0 + 9.6 + 0.1: continue
        out.append(np.interp(c + grid, t, v))
    return np.vstack(out)

L = fold(tl, cl, t0L); L -= np.median(L[:, grid < -0.20], axis=1, keepdims=True)
lmed, lsd = np.median(L, axis=0), L.std(axis=0)
# The membrane is folded on the two-channel run's OWN event onsets, not on
# t0 + i*P: fold()'s uniform stepping and its 9.6 s cutoff (sized for the older
# ten-repeat run) kept only 7 of the 9 events, and its i = -1 row is the window
# BEFORE the first event -- a flat trace with no spike in it, which among spiking
# repeats reads as a failed trial rather than as the pre-stimulus baseline it is.
_f = dual["fires"][:, 0]
_ev = [[_f[0]]]
for _x in _f[1:]:
    (_ev[-1] if _x - _ev[-1][-1] < 0.5 else _ev.append([]) or _ev[-1]).append(_x)
_ons = [e[0] for e in _ev
        if e[0] + grid[0] >= tmb[0] and e[0] + grid[-1] <= tmb[-1]]
M = np.vstack([np.interp(c + grid, tmb, vmb) for c in _ons])
mmed = np.median(M, axis=0)
print(f"LNA repeats {L.shape[0]} (single-channel run), "
      f"membrane repeats {M.shape[0]} (two-channel run)")

# recovered input, as before
FC, GAIN, BOX = 1.53, 268.0, 0.025
nn = len(grid); ff = np.fft.rfftfreq(nn, 1.0/FS)
Hl = -GAIN*(1j*ff/FC)/(1 + 1j*ff/FC); Hb = np.sinc(ff*BOX)
band = (ff >= 1.0) & (ff <= 25.0)
Y = np.fft.rfft(lmed); X = np.zeros_like(Y); X[band] = Y[band]/(Hl[band]*Hb[band])
rec = np.fft.irfft(X, nn)

MUT = "#5c5f66"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUT, "xtick.color": MUT,
    "ytick.color": MUT, "axes.linewidth": .8, "grid.color": "#d7d9de",
    "legend.frameon": True, "legend.framealpha": .9, "legend.edgecolor": "#d7d9de",
    "font.family": "serif", "savefig.bbox": "tight"})
BLUE, RED, GRN = "#1f4fd8", "#c62828", "#137a5f"
fig, ax = plt.subplots(3, 1, figsize=(3.45, 4.6), sharex=True)
ax[0].plot(grid, rec*1e6, lw=1.0, color=BLUE, label=r"$V_{in}$ ($\mu$V)")
ax[0].set_ylabel(r"$V_{sen}$ ($\mu$V)", color=BLUE); ax[0].tick_params(axis="y", labelcolor=BLUE)
for row in L: ax[1].plot(grid, row*1e3, lw=.45, color=RED, alpha=.25)
ax[1].fill_between(grid, (lmed-lsd)*1e3, (lmed+lsd)*1e3, color=RED, alpha=.20, lw=0)
ax[1].plot(grid, lmed*1e3, lw=1.3, color="#8c1010", label=r"$V_{LNA}^{out}$ (mV)")
ax[1].set_ylabel(r"$V_{LNA}^{out}$ (mV)", color=RED); ax[1].tick_params(axis="y", labelcolor=RED)
# NO median here. Spikes do not align sample-by-sample across repeats, so a
# median across them reads ~0.36 V while individual spikes reach 1.13 V -- it
# would understate the membrane by a factor of three. The published panel shows a
# single transient; one representative repeat is drawn dark, the rest faint. All
# nine repeats of the two-channel run are drawn.
for row in M: ax[2].plot(grid, row, lw=.5, color=GRN, alpha=.28)
# Most spikes, not tallest sample: every repeat reaches the same peak within
# 30 mV, so argmax over amplitude picks essentially at random.
_thr_c = 0.5 * (np.median(M[:, grid < -0.20]) + M.max())
_nspk = [int(((r[1:-1] > r[:-2]) & (r[1:-1] >= r[2:]) & (r[1:-1] > _thr_c)).sum())
         for r in M]
_rep = int(np.argmax(_nspk))
print(f"spikes per repeat {_nspk}; representative = repeat {_rep}")
ax[2].plot(grid, M[_rep], lw=1.0, color="#0b4f3d", label=r"$V_{mem}$ (V)")
ax[2].set_ylabel(r"$V_{mem}$ (V)", color=GRN); ax[2].tick_params(axis="y", labelcolor=GRN)
ax[2].set_xlabel("Time from event onset (s)")
# (c)'s legend goes upper-LEFT: the inset now occupies the upper right
for a_, lab, lloc in zip(ax, ("(a)", "(b)", "(c)"),
                         ("upper right", "upper right", "upper left")):
    a_.grid(alpha=.5); a_.set_axisbelow(True); a_.set_xlim(-0.35, 0.65)
    a_.legend(loc=lloc, fontsize=6.8, handlelength=1.3, borderaxespad=0.3)
    a_.annotate(lab, xy=(0.014, 0.06), xycoords="axes fraction", fontsize=9,
                fontweight="bold", color="#1b1b1f")
    for s_ in ("top", "right"): a_.spines[s_].set_visible(False)
# --- inset: the integrate-and-fire detail --------------------------------------
# This was withheld once, and the reason is worth keeping. At the earlier
# operating point the chip's own timestamps put 210 of 215 within-burst
# interspike intervals at 1.368 ms exactly -- ~731 Hz, which is the AER drain
# period, so the neuron was at or past the readout limit. A 1 kHz digitiser
# samples that 1.4 times per spike and returns an alias, not a measurement:
# 1000-731 = 269 Hz beat, an apparent spike every 3.7 ms. The first inset drew
# the beat.
#
# The fix was the neuron, not the instrument. Raising JExcWn0-3 by 0.0020 from
# the file value moved it off the floor: 16 Hz out for 40 Hz in, interspike
# interval ~60 ms. At 1 kHz that is ~60 samples per interval, and the charging
# ramp between spikes is resolved rather than inferred. The inset is a
# measurement again.
INSET = True
# --- the inset itself, as in the simulated Fig. 10 ---------------------------
# Both faults that blocked this are gone: the membrane is now recorded during the
# live run, on the same instrument as the amplifier channel, so the baseline
# matches the panel it sits in and the neuron is driven by real event-time
# injections rather than a 2 Hz single-spike trigger.
#
# The window is chosen to show what the panel cannot at 1 s across: the neuron
# rests, is driven through threshold in a burst, resets, and recovers. It is NOT
# zoomed to a single interspike interval: within a burst the ISI is 3-4 ms and the
# digitiser runs at 1 kHz, so an interval holds three or four samples and the
# sub-threshold ramp that Fig. 10 draws from simulation is simply not resolved
# here. Zooming further would draw an interpolation, not a measurement.
if INSET:
    INS_T0, INS_T1 = 0.090, 0.230   # one reset, one full ramp, the next spike
    # Sits over the flat post-event stretch of the panel, opaque so the resting line
    # behind it does not read as part of the inset.
    # Headroom is made ABOVE the traces rather than taken from beside them: the
    # spikes now run out to +0.31 s, so an inset parked on the right half would
    # sit on top of real data and hide it behind its own white patch.
    axi = ax[2].inset_axes([0.33, 0.575, 0.66, 0.40], facecolor="white")
    axi.set_zorder(5); axi.patch.set_alpha(1.0)
    _m = (grid >= INS_T0) & (grid <= INS_T1)
    for row in M:
        axi.plot(grid[_m]*1e3, row[_m], lw=.4, color=GRN, alpha=.22)
    axi.plot(grid[_m]*1e3, M[_rep][_m], lw=.9, color="#0b4f3d")
    axi.set_xlim(INS_T0*1e3, INS_T1*1e3)
    axi.tick_params(labelsize=5.0, length=2, pad=1)
    axi.set_yticks([0.5, 1.0])
    axi.yaxis.tick_right()          # keep the labels off the panel's own spikes
    axi.annotate("ms", xy=(0.985, 0.06), xycoords="axes fraction", ha="right",
                 va="bottom", fontsize=5.5, color=MUT)
    axi.grid(alpha=.35); axi.set_axisbelow(True)
    for s_ in axi.spines.values():
        s_.set_edgecolor(MUT); s_.set_linewidth(.6)
    # A plain rectangle, drawn UNDER the traces, rather than indicate_inset_zoom():
    # that draws its box across the full data range of the inset, whose top edge then
    # runs straight through the inset itself, and hangs four connector lines across
    # the panel.
    ax[2].set_ylim(0.28, 1.78)
    _y0, _y1 = M.min(), M.max()
    ax[2].add_patch(Rectangle((INS_T0, _y0), INS_T1 - INS_T0, _y1 - _y0,
                              fill=False, ec=MUT, lw=.6, ls=(0, (3, 2)),
                              alpha=.55, zorder=1))
    _ins_spk = np.flatnonzero((M[_rep][1:-1] > M[_rep][:-2]) &
                              (M[_rep][1:-1] >= M[_rep][2:]) & (M[_rep][1:-1] > _thr_c)) + 1
    _ins_spk = grid[_ins_spk]
    _ins_spk = _ins_spk[(_ins_spk >= INS_T0) & (_ins_spk <= INS_T1)]
    print(f"inset {INS_T0*1e3:+.0f}..{INS_T1*1e3:+.0f} ms, {len(_ins_spk)} spikes in the "
          f"representative repeat, ISI "
          f"{', '.join('%.0f'%x for x in np.diff(_ins_spk)*1e3)} ms")

fig.tight_layout()
for e in ("png", "pdf"):
    fig.savefig(os.path.join(ROOT, "figures", f"fig10_silicon_full.{e}"), dpi=200)
    fig.savefig(os.path.join(LNA, "ISCAS27", "IEEE_PAD_SkyWater_2026", "figures",
                             f"fig10_silicon_full.{e}"), dpi=200)
np.savez_compressed(os.path.join(ROOT, "raw", "odor_neuron", "membrane.npz"),
    grid=grid, lna_trials=L, lna_median=lmed, lna_sd=lsd, mem_trials=M, mem_median=mmed,
    recovered_input=rec, period_s=P, smooth_delay_s=SMOOTH_DELAY)
rest = np.median(mmed[grid < -0.20])
print(f"membrane rest {rest:.3f} V; per-repeat peaks "
      f"{np.round([r.max() for r in M],2)}")
print(f"membrane peak, max over repeats {max(r.max() for r in M):.3f} V")
print(f"LNA median peak {lmed.max()*1e3:+.1f} mV at {grid[int(np.argmax(lmed))]:+.3f} s")

print("figures/fig10_silicon_full.png + .pdf (archive + paper figures/)")
