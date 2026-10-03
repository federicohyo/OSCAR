#!/usr/bin/env python3
"""The pad-evoked spiking response, chip1.

    ../.venv-meas/bin/python3 LNA/make_fig_pad_evoked.py   (from repo root)

Data: scope_20260831_123139_single_payed_back_chip1_v1.csv -- the recorded
saline event replayed at 10 mVpp into the pad-amplifier input,
one event every 4 s; the GUI's Pad-Evoked mode thresholds the amplifier
output (downward, trailing-median -150 mV) and injects AER spikes into
neuron 11; ch2 watches its membrane.

DRAWING (Federico, 2026-08-31): all 15 repetitions folded onto the event
onset, thin bright traces, ONE repetition (a median-count one) overdrawn in
ink -- the overlay IS the repeatability claim.  Left column: pad-amplifier
output over the spike raster, same folded time.  Right column: the soma
circuit (tikz asset, from the earlier build's neuron_circuit.tikz) with the
highlighted repetition's membrane below it, the event window in the same
green as the left panels.

Drawn at exact print size (3.45 x 2.45 in) for a single-column figure --
keep the same scale.
Outputs fig18_pad_evoked_chip1.pdf (+ .png preview) in the figures directory.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import signal as sg

CSV = "measurements/wet_pad/data/scope_20260831_123139_single_payed_back_chip1_v1.csv"
OUT = "measurements/wet_pad/figures/fig18_pad_evoked_chip1"
FS = 1000.0
TS = 0.85

INK, INK2, MUTED = "#1c1c1c", "#5a5a5a", "#b8b8b8"
C_THR, C_SH = "#c05621", "#dbe7db"
FAINT = "#b9c6cf"          # the thin bright overlay traces

W0, W1 = -0.50, 1.05       # folded window about the detection onset [s]
VW0, VW1 = 0.0, 0.15        # Vmem mini-plot window [s] (onset zoom)


def dress(ax):
    ax.grid(True, color="#e6e6e6", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9 * TS)


d = np.genfromtxt(CSV, delimiter=",", names=True)
t = (d["sample_index"] - d["sample_index"][0]) / FS      # trap-4: index rather than clock
v1, v2 = d["volts"], d["volts_ch2"]

base1 = np.median(v1)
down = v1 < base1 - 0.30
segs, on_ = [], None
for k in range(1, len(t)):
    if down[k] and on_ is None: on_ = k
    if on_ is not None and (not down[k] or k == len(t) - 1):
        segs.append([t[on_], t[k]]); on_ = None
merged = []
for s in segs:
    if merged and s[0] - merged[-1][1] < 1.5: merged[-1][1] = s[1]
    else: merged.append(list(s))
segs = merged
assert len(segs) == 15, f"expected 15 events, got {len(segs)}"

above = v2 > 0.95
spk_all = t[np.flatnonzero((~above[:-1]) & above[1:]) + 1]

# per-repetition: folded ch1 trace + spike list
reps = []
for a, b in segs:
    m = (t >= a + W0) & (t <= a + W1)
    fold_t = t[m] - a
    reps.append(dict(ft=fold_t, ch1=v1[m],
                     spk=spk_all[(spk_all >= a) & (spk_all <= a + W1)] - a))
counts = [len(r["spk"]) for r in reps]
hero = 9    # repetition 10, mid-raster (counts: 7 spikes, inside the 5-9
            # spread): the one whose membrane is drawn in the right column
print(f"spikes/repetition: {counts}; highlighting #{hero + 1} ({counts[hero]})")

fig = plt.figure(figsize=(3.45, 2.45))

# ---- left column: amplifier output over the spike raster --------------------
ax0 = fig.add_axes([0.19, 0.615, 0.42, 0.345])
ax1 = fig.add_axes([0.19, 0.225, 0.42, 0.345])

# DISPLAY SCALE (2026-09-02, Federico): the replay was driven harder than
# the wet event (10 mVpp at the input vs ~1.5 mV input-referred) so the
# step is unambiguous on this die; the analog trace is displayed scaled to
# the amplitude of the recorded event (-398 mV, the reference figure) so both panels
# read the same level.  Detection, folding, spikes and membrane all remain
# computed on the unscaled data; only this display is scaled.
K_DISP = 0.398 / (base1 - v1[down].min())
for i, r in enumerate(reps):
    if i == hero: continue
    ax0.plot(r["ft"], base1 + K_DISP * (r["ch1"] - base1), lw=0.35,
             color=FAINT, alpha=0.9)
r = reps[hero]
ax0.plot(r["ft"], base1 + K_DISP * (r["ch1"] - base1), lw=1.0, color=INK)
ax0.axhline(base1, lw=0.8, color=INK2, ls=":")
ax0.axhline(base1 - K_DISP * 0.150, lw=0.8, color=C_THR, ls="--")
ax0.axvspan(0.0, 1.0, color=C_SH, lw=0, zorder=-1)
ax0.annotate("trailing median", (W1 - 0.06, 1.35), fontsize=7.5 * TS,
             color=INK2, ha="right")
ax0.annotate("detection thr.", (W1 - 0.06, 1.10), fontsize=7.5 * TS,
             color=C_THR, ha="right")
ax0.set_ylabel("LNA out  (V)", color=INK2, fontsize=10.5 * TS)
ax0.set_ylim(0.84, 1.52)
ax0.set_xlim(W0, W1)
ax0.tick_params(labelbottom=False)

# ---- raster, same folded time -----------------------------------------------
for i, r in enumerate(reps):
    ink = i == hero
    ax1.vlines(r["spk"], i + 0.72, i + 1.28,
               color=(INK if ink else "#8fa3b0"), lw=(1.0 if ink else 0.6))
ax1.axvspan(0.0, 1.0, color=C_SH, lw=0, zorder=-1)
ax1.set_ylim(0.35, len(reps) + 0.65)
ax1.set_yticks([1, 5, 10, 15])
ax1.set_ylabel("repetition", color=INK2, fontsize=10.5 * TS)
ax1.set_xlabel("time from detection onset  (s)", color=INK2, fontsize=10 * TS)
ax1.set_xlim(W0, W1)
dress(ax0); dress(ax1)

# ---- right column: the neuron, and its membrane -----------------------------
# The top-right cell is left EMPTY here: the soma circuit is overlaid as
# vector art -- rasterising it blurs the thin circuit lines.  Below it, the
# membrane.
axv = fig.add_axes([0.71, 0.235, 0.26, 0.215])
a = segs[hero][0]
z = (t >= a + VW0) & (t <= a + VW1)
axv.plot(t[z] - a, v2[z], lw=0.8, color=INK)
axv.axvspan(0.0, 1.0, color=C_SH, lw=0, zorder=-1)
axv.set_xlim(VW0, VW1)
axv.set_ylim(0.0, 1.5)          # full supply scale, per Federico
axv.set_yticks([0.0, 0.7, 1.5])
axv.set_yticklabels(["0", "0.7", "1.5"])
axv.set_xticks([0.0, 0.1, 0.2])
axv.set_ylabel("$V_{mem}$ (V)", color=INK2, fontsize=8 * TS, labelpad=1)
axv.set_xlabel("time (s)", color=INK2, fontsize=8 * TS)
dress(axv)
axv.tick_params(labelsize=7 * TS)

fig.savefig(OUT + ".pdf")
fig.savefig(OUT + ".png", dpi=200)
print(f"saved {OUT}.pdf (+png)")

# ---- text numbers (the reference analysis + abstract) -----------------------------------
inside, leads = 0, []
for (a, b), r in zip(segs, reps):
    inside += len(r["spk"])
    if len(r["spk"]): leads.append(r["spk"][0])
quiet = np.ones(len(t), bool)
for a, b in segs: quiet &= ~((t >= a) & (t <= b + 0.5))
b30, a30 = sg.butter(4, 30.0, "hp", fs=FS)
h1 = sg.filtfilt(b30, a30, v1)
sq = np.zeros(len(t), bool)
for s in spk_all: sq |= (t >= s - 0.05) & (t <= s + 0.05)
print(f"spikes {inside}/{len(spk_all)} inside events; rest {np.median(v2[quiet])*1e3:.0f} mV; "
      f"top ~{np.percentile(v2[~quiet],99.5)*1e3:.0f} mV; lead {np.median(leads)*1e3:.0f} ms; "
      f"spikes/event {inside/len(segs):.1f} (range {min(counts)}-{max(counts)})")
print(f"spike->LNA coupling (>30 Hz): {h1[sq].std()*1e3:.1f} mV rms around spikes, "
      f"{h1[quiet].std()*1e3:.1f} mV rms in quiet")
