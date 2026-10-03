#!/usr/bin/env python3
"""Fold and score the odor response. Offline -- re-runs from the saved raw record.

ALIGNMENT: on the signal, not the sync marker. `odor_bench.py` locks a comb of
137 Hz marker bursts, and at this drive level that fails silently: scaling the
stimulus down to 0.55 mVpp scaled the marker down with it, leaving an envelope
only 3.7x above its own floor with 2 of 10 bursts detectable. Two consecutive
runs returned offsets 0.248 s apart -- both with "good" comb scores of 6.6-7.0x,
and with the event deflection changing sign between them.

Correlating the whole 1.6 s period against the expected response instead uses
the entire stimulus rather than a 50 ms burst, and locks at r = 0.96.

The expected response is the drive passed through a single pole at the MEASURED
1.53 Hz corner, then band-limited 1-40 Hz to match the analysis band. The odor
event lives at 2-20 Hz; the band-pass also removes the 272 Hz bench interferer,
which matters here because 272 Hz x 1.6 s = 435.0 cycles per period -- so close
to an integer that it is period-locked and does NOT average away over repeats.
"""
import csv, json, os, sys
import numpy as np
from scipy.signal import butter, filtfilt, medfilt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
LNA  = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FS, HP_HZ, BAND = 1000.0, 1.53, (1.0, 40.0)


def expected(drive, n):
    """Drive -> LNA output shape: one pole at the measured corner, then the band."""
    al = 1.0/(1.0 + 2*np.pi*HP_HZ/FS)
    x = np.tile(drive, 3); y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = al*(y[i-1] + x[i] - x[i-1])
    b, a = butter(4, [BAND[0]/(FS/2), BAND[1]/(FS/2)], "band")
    e = filtfilt(b, a, -y[n:2*n])          # the amplifier inverts
    return e - e.mean()


def main():
    raw = np.load(os.path.join(LNA, "odor_bench_trials.npz"))
    if "raw_v" not in raw.files:
        sys.exit("that npz has no raw record -- re-run odor_bench.py")
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

    b, a = butter(4, [BAND[0]/(FS/2), BAND[1]/(FS/2)], "band")
    sig = filtfilt(b, a, medfilt(v, 7) - v.mean())

    best = (-9.0, 0)
    for off in range(n):
        idx = off + n*np.arange(reps); idx = idx[idx + n <= len(sig)]
        if len(idx) < reps - 1: continue
        ac = np.mean([sig[i:i+n] for i in idx], axis=0); ac -= ac.mean()
        r = float(np.dot(ac, tmpl)/np.sqrt(np.dot(ac, ac)*np.dot(tmpl, tmpl)))
        if r > best[0]: best = (r, off)
    r, off = best
    idx = off + n*np.arange(reps); idx = idx[idx + n <= len(sig)]
    T = np.vstack([sig[i:i+n] for i in idx])
    mean = T.mean(0); mean -= mean.mean(); sem = T.std(0)/np.sqrt(len(T))
    gain = float(np.dot(mean, tmpl)/np.dot(tmpl, tmpl))

    # t = 0 at the EVENT onset (event_on) rather than at t_odor -- t_odor is the record's
    # own reference point and sits 0.17 s after the event actually begins.
    tt = tp - tm["event_on"]
    ev = (tt >= 0) & (tt <= tm["event_off"] - tm["event_on"])
    pre = (tt < -0.05) & (tt > -0.30)
    pk = mean[ev][np.argmax(np.abs(mean[ev]))]
    resid = mean - gain*tmpl

    print(f"aligned on the signal: offset {off/FS:.3f} s, r = {r:+.3f}, {len(T)} repeats")
    print(f"  event deflection : {pk*1e3:+7.2f} mV  ({'UP' if pk>0 else 'DOWN'})")
    print(f"  baseline         : {mean[pre].std()*1e3:6.2f} mV rms   SNR {abs(pk)/mean[pre].std():.1f}x")
    print(f"  implied gain     : {gain:6.1f}x   (sine-measured ~268x at 88.57 Hz)")
    print(f"  residual         : {resid.std()*1e3:6.2f} mV rms "
          f"({100*np.var(resid)/np.var(mean):.0f}% of variance unexplained)")

    np.savez_compressed(os.path.join(ROOT, "raw", "odor", "odor_response.npz"),
                        t=tt, mean=mean, sem=sem, trials=T, template=tmpl, gain=gain,
                        r=r, offset_s=off/FS, raw_v=v, chip_vpp=tm["chip_vpp"],
                        period_s=P, reps=reps, hp_hz=HP_HZ, band=BAND)
    w = (tt >= -0.30) & (tt <= 0.60)
    with open(os.path.join(ROOT, "derived", "odor_response.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["t_s", "vout_mean_v", "vout_sem_v", "expected_v", "n_repeats"])
        for A_, B_, C_, D_ in zip(tt[w], mean[w], sem[w], (gain*tmpl)[w]):
            wr.writerow([f"{A_:.4f}", f"{B_:.7f}", f"{C_:.7f}", f"{D_:.7f}", len(T)])
    return tt, mean, sem, gain, tmpl, r, drive, ts, vs, tp, w


if __name__ == "__main__":
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    tt, mean, sem, gain, tmpl, r, drive, ts, vs, tp, w = main()
    MUT = "#5c5f66"
    plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUT, "xtick.color": MUT,
        "ytick.color": MUT, "axes.linewidth": .8, "grid.color": "#d7d9de",
        "legend.frameon": False, "font.family": "serif", "savefig.bbox": "tight"})
    fig, ax = plt.subplots(2, 1, figsize=(3.45, 3.4), sharex=True)
    ax[0].plot(tt[w], drive[w]*1e6, lw=1.1, color="#3f3f46")
    ax[0].set_ylabel(r"input [$\mu$V]")
    ax[1].plot(tt[w], (gain*tmpl)[w]*1e3, lw=1.0, color="#8a63d2", label="expected")
    ax[1].plot(tt[w], mean[w]*1e3, lw=1.3, color="#2f6fd0", label=f"measured ($r={r:.2f}$)")
    ax[1].fill_between(tt[w], (mean-sem)[w]*1e3, (mean+sem)[w]*1e3, color="#2f6fd0", alpha=.3)
    ax[1].set_ylabel("LNA out [mV]"); ax[1].set_xlabel("time from event onset [s]")
    ax[1].legend(loc="upper right", fontsize=7.2)
    for x in ax:
        x.grid(alpha=.5); x.set_axisbelow(True)
        for sp in ("top", "right"): x.spines[sp].set_visible(False)
    fig.tight_layout()
    for e in ("png", "pdf"):
        fig.savefig(os.path.join(ROOT, "figures", f"odor_response.{e}"), dpi=200)
    print("\nfigures/odor_response.png + .pdf")
