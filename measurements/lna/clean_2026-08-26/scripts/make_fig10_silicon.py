#!/usr/bin/env python3
"""Silicon counterpart of the reference figure panels (a) and (b): the odor stimulus at the
chip input and the measured LNA output.

Panel (c) of the reference figure is the neuron membrane; that leg is still pending
measured, so this figure carries (a) and (b) only.

Two departures from analyze_odor.py, both for display only:
  * the fold uses a LOW-PASS (40 Hz) rather than the 1-40 Hz band, so the output
    keeps its real DC level and the axis can be absolute, as in the reference figure. The
    1-40 Hz band is still what FINDS the alignment -- that is the step that has
    to be robust, and it is unchanged.
  * the record is shown in absolute time, 0-0.8 s, matching the reference axis.
"""
import csv, json, os, sys
import numpy as np
from scipy.signal import butter, filtfilt, medfilt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LNA  = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FS = 1000.0
sys.path.insert(0, HERE)
from analyze_odor import expected, BAND

raw = np.load(os.path.join(LNA, "odor_bench_trials.npz"))
v = raw["raw_v"].astype(float)
tm = json.load(open(os.path.join(LNA, "odor_timing.json")))
P, reps = tm["period_s"], tm["repeats"]
rows = list(csv.DictReader(open(os.path.join(LNA, "odor_stimulus.csv"))))
key = [k for k in rows[0] if "chip" in k][0]
ts = np.array([float(r["t_s"]) for r in rows])
vs = np.array([float(r[key]) for r in rows])
n = int(round(P*FS)); tp = np.arange(n)/FS
drive = np.interp(tp, ts, vs, left=vs[0], right=0.0); drive[tp > ts[-1]] = 0.0
tmpl = expected(drive, n)

vm = medfilt(v, 7)
bb, ab = butter(4, [BAND[0]/(FS/2), BAND[1]/(FS/2)], "band")
sig = filtfilt(bb, ab, vm - vm.mean())
bl, al = butter(4, BAND[1]/(FS/2), "low")
disp = filtfilt(bl, al, vm)

best = (-9.0, 0)
for off in range(n):
    idx = off + n*np.arange(reps); idx = idx[idx + n <= len(sig)]
    if len(idx) < reps - 1: continue
    ac = np.mean([sig[i:i+n] for i in idx], axis=0); ac -= ac.mean()
    r = float(np.dot(ac, tmpl)/np.sqrt(np.dot(ac, ac)*np.dot(tmpl, tmpl)))
    if r > best[0]: best = (r, off)
r, off = best
idx = off + n*np.arange(reps); idx = idx[idx + n <= len(sig)]
D = np.vstack([disp[i:i+n] for i in idx])
mean, sem = D.mean(0), D.std(0)/np.sqrt(len(D))
print(f"alignment r = {r:+.3f}, offset {off/FS:.3f} s, {len(D)} repeats")
print(f"output DC {mean.mean()*1e3:.1f} mV, swing {(mean.max()-mean.min())*1e3:.1f} mVpp")
print(f"input swing {(drive.max()-drive.min())*1e6:.0f} uVpp")

w = tp <= 0.8
BLUE, RED, MUT = "#1f4fd8", "#c62828", "#5c5f66"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUT, "xtick.color": MUT,
    "ytick.color": MUT, "axes.linewidth": .8, "grid.color": "#d7d9de",
    "legend.frameon": True, "legend.framealpha": .9, "legend.edgecolor": "#d7d9de",
    "font.family": "serif", "savefig.bbox": "tight"})
fig, ax = plt.subplots(2, 1, figsize=(3.45, 3.3), sharex=True)
ax[0].plot(tp[w], drive[w]*1e6, lw=1.0, color=BLUE, label=r"$V_{in}$ ($\mu$V)")
ax[0].set_ylabel(r"$V_{sen}$ ($\mu$V)", color=BLUE)
ax[0].tick_params(axis="y", labelcolor=BLUE)
ax[1].plot(tp[w], mean[w]*1e3, lw=1.0, color=RED, label=r"$V_{LNA}^{out}$ (mV)")
ax[1].fill_between(tp[w], (mean-sem)[w]*1e3, (mean+sem)[w]*1e3, color=RED, alpha=.25, lw=0)
ax[1].set_ylabel(r"$V_{LNA}^{out}$ (mV)", color=RED)
ax[1].tick_params(axis="y", labelcolor=RED)
ax[1].set_xlabel("Time (s)")
# legend placement is per-panel: (a)'s trough occupies lower-right and (b)'s
# post-event dip occupies lower-right too, so they go to the free corners.
for a_, lab, loc in zip(ax, ("(a)", "(b)"), ("lower left", "upper right")):
    a_.grid(alpha=.55); a_.set_axisbelow(True)
    a_.legend(loc=loc, fontsize=7)
    a_.set_xlim(0, 0.8); a_.margins(y=0.16)
    a_.annotate(lab, xy=(0.012, 0.88), xycoords="axes fraction",
                fontsize=9, fontweight="bold", color="#1b1b1f")
    for sp in ("top", "right"): a_.spines[sp].set_visible(False)
fig.tight_layout()
for e in ("png", "pdf"):
    fig.savefig(os.path.join(ROOT, "figures", f"fig10_silicon_ab.{e}"), dpi=200)
print("wrote fig10_silicon_ab.png/.pdf")
