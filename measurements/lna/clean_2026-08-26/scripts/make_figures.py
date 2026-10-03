#!/usr/bin/env python3
"""The two LNA figures: measured transfer and input-referred noise.

NO plot titles: the title lives in the caption.

  fig12_lna_transfer.pdf   measured transfer, BOTH operating points
  fig14_lna_noise.pdf      input-referred noise only, single panel
"""
import csv, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A

# OSCAR reorg: outputs go to measurements/lna/figures/, inputs to
# measurements/lna/data/ (was LNA/*.csv, wrote into an external build dir).
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "figures"))
LNA = os.path.abspath(os.path.join(HERE, "..", "..", "data"))

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300, "savefig.bbox": "tight",
    "font.size": 8, "axes.labelsize": 8.5, "legend.fontsize": 7.6,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.edgecolor": "#5c5f66", "xtick.color": "#5c5f66", "ytick.color": "#5c5f66",
    "axes.linewidth": 0.7, "grid.color": "#d7d9de", "grid.linewidth": 0.5,
    "legend.frameon": False, "font.family": "serif",
})
C_HI, C_LO, MUTED, WARN = "#2f6fd0", "#8a63d2", "#5c5f66", "#c2410c"

def style(ax):
    ax.grid(True, which="both", alpha=.55); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)


def fig12():
    """Transfer function, both operating points on one axis."""
    rows = [r for r in A.rd("transfer")
            if r["tag"].startswith("F") and not r["tag"].endswith("_guard")]
    f_hi = np.array([A.fnum(r, "freq_hz") for r in rows])
    vin = np.array([A.vin_true(r) for r in rows])
    g_hi = np.array([A.fnum(r, "vout_pp") for r in rows]) / vin
    gdb_hi = 20*np.log10(g_hi)

    # divide out the AC-coupled source, same rule as the earlier campaign
    with open(os.path.join(LNA, "lna_transfer_ref.csv")) as fh:
        rr = [r for r in csv.DictReader(fh)]
    rf = np.array([float(r["freq_hz"]) for r in rr])
    rg = np.array([float(r["gain"]) for r in rr])
    k = (rg > 0) & np.isfinite(rg); rf, rg = rf[k], rg[k]
    i = np.argsort(rf); rf, rg = rf[i], rg[i]
    shape = np.interp(np.log(f_hi), np.log(rf), rg/np.median(rg[(rf > 20) & (rf < 130)]))
    shape[f_hi > 130] = 1.0
    gdb_hi = gdb_hi - 20*np.log10(np.clip(shape, 1e-6, None))
    m = f_hi > 0.2

    # the earlier operating point, already corrected in the previous campaign
    with open(os.path.join(LNA, "lna_transfer_final.csv")) as fh:
        lo = [r for r in csv.DictReader(fh)]
    f_lo = np.array([float(r["freq_hz"]) for r in lo])
    gdb_lo = np.array([float(r["gain_db"]) for r in lo])
    snr = np.array([r.get("low_snr", "0") == "1" for r in lo])

    # the design's own testbench, AC sweep, circuit untouched
    with open(os.path.join(LNA, "lna_sim_ac.csv")) as fh:
        sim = [r for r in csv.DictReader(fh)]
    fs_ = np.array([float(r["freq_hz"]) for r in sim])
    gs_ = np.array([float(r["gain_db"]) for r in sim])
    ks = (fs_ >= 0.18) & (fs_ <= 460)

    fig, ax = plt.subplots(figsize=(3.45, 2.5))
    ax.semilogx(fs_[ks], gs_[ks], "-", lw=1.1, color="#3f3f46", alpha=.85,
                zorder=1, label="ngspice (simulation)  ($50.0$ dB)")
    ax.semilogx(f_hi[m], gdb_hi[m], "-o", lw=1.4, ms=3.2, color=C_HI,
                markeredgecolor="white", markeredgewidth=.5,
                label="high-gain (measured)  ($48.6$ dB)")
    ax.semilogx(f_lo[~snr], gdb_lo[~snr], "-s", lw=1.4, ms=3.0, color=C_LO,
                markeredgecolor="white", markeredgewidth=.5,
                label="low-gain (measured)  ($39.8$ dB)")
    ax.semilogx(f_lo[snr], gdb_lo[snr], ":s", lw=1.0, ms=2.6, color=C_LO, alpha=.55)
    for y in (48.55, 39.80):
        ax.axhline(y, ls="--", lw=.6, color=MUTED, zorder=0)
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("gain [dB]")
    ax.set_ylim(27, 53); ax.legend(loc="lower right", borderaxespad=0.4)
    style(ax)
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"fig12_lna_transfer.{e}"))
    plt.close(fig)
    print(f"fig12_lna_transfer.pdf  high {np.median(gdb_hi[(f_hi>20)&(f_hi<200)]):.2f} dB, "
          f"low {np.median(gdb_lo[(f_lo>20)&(f_lo<200)]):.2f} dB, "
          f"sim {np.median(gs_[(fs_>20)&(fs_<200)]):.2f} dB")


def fig14():
    """Input-referred noise only, single panel, no title."""
    gf = None
    rows = [r for r in A.rd("transfer")
            if r["tag"].startswith("F") and not r["tag"].endswith("_guard")]
    f = np.array([A.fnum(r, "freq_hz") for r in rows])
    vin = np.array([A.vin_true(r) for r in rows])
    g = np.array([A.fnum(r, "vout_pp") for r in rows]) / vin
    with open(os.path.join(LNA, "lna_transfer_ref.csv")) as fh:
        rr = [r for r in csv.DictReader(fh)]
    rf = np.array([float(r["freq_hz"]) for r in rr]); rg = np.array([float(r["gain"]) for r in rr])
    k = (rg > 0) & np.isfinite(rg); rf, rg = rf[k], rg[k]
    i = np.argsort(rf); rf, rg = rf[i], rg[i]
    sh = np.interp(np.log(f), np.log(rf), rg/np.median(rg[(rf > 20) & (rf < 130)]))
    sh[f > 130] = 1.0
    gf = (f, g/np.clip(sh, 1e-6, None))

    seg, P, nseg = 8192, None, 0
    for r in [x for x in A.rd("noise") if x["tag"].startswith("N")]:
        d = np.load(os.path.join(A.ROOT, r["raw_npz"])); v = d["v"].astype(float)
        v.flags.writeable = False
        w = np.hanning(seg)
        for j in range(0, len(v)-seg+1, seg//2):
            x = v[j:j+seg] - v[j:j+seg].mean()
            Aa = np.abs(np.fft.rfft(x*w))**2 * 2.0/(A.FS*(w**2).sum())
            P = Aa if P is None else P + Aa; nseg += 1
    P /= nseg
    fr = np.fft.rfftfreq(seg, 1.0/A.FS)
    asd = np.sqrt(P); m = (fr > 0.2) & (fr < 450); fr, asd = fr[m], asd[m]
    logA = np.log10(asd); kk = 101
    pad = np.pad(logA, kk//2, mode="edge")
    med = np.array([np.median(pad[i:i+kk]) for i in range(len(logA))])
    line = logA > med + np.log10(3.0)
    gi = np.exp(np.interp(np.log(fr), np.log(gf[0][np.argsort(gf[0])]),
                          np.log(gf[1][np.argsort(gf[0])])))
    asd_in = asd/gi

    fig, ax = plt.subplots(figsize=(3.45, 2.4))
    ax.loglog(fr[~line], asd_in[~line]*1e6, lw=1.0, color=C_HI)
    at1 = np.interp(1.0, fr[~line], asd_in[~line])*1e6
    floor = np.median(asd_in[(fr > 20) & (fr < 300) & ~line])*1e6
    ax.axhline(floor, ls="--", lw=.7, color=MUTED, zorder=0)
    ax.annotate(f"{floor:.2f}" + r"$\,\mu$V/$\sqrt{\mathrm{Hz}}$", xy=(0.42, floor),
                xytext=(0, 4), textcoords="offset points", ha="left", fontsize=7,
                color=MUTED)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel(r"input-referred noise [$\mu$V/$\sqrt{\mathrm{Hz}}$]")
    style(ax)
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"fig14_lna_noise.{e}"))
    plt.close(fig)
    print(f"fig14_lna_noise.pdf  {at1:.1f} uV/rtHz @1 Hz, floor {floor:.2f}, {nseg} averages")


def fig9():
    """Gain vs input level, single panel: all acquisition blocks pooled as one
    series of points (guards outlined), plus the log compression fit.
    The 2nd harmonic panel is dropped -- its numbers live in the text."""
    rows = [r for r in A.rd("gain_vs_level") if r["tag"][0] in "LS"] + \
           [r for r in A.rd("gain_crosscheck") if r["tag"][0] == "C"]
    if not rows:
        return print("fig9: no data yet")

    vall, gall, sall, dall = [], [], [], []
    for pref in "SLC":
        rs = [r for r in rows if r["tag"].startswith(pref)]
        if not rs:
            continue
        vt = np.array([A.vin_true(r) for r in rs])
        vall.append(vt * 1e6)
        gall.append(np.array([A.fnum(r, "vout_pp") for r in rs]) / vt)
        sall.append(np.array([A.fnum(r, "amp_se_v") for r in rs]))
        dall.append(np.array([r["tag"].endswith("_guard") for r in rs]))
    v = np.concatenate(vall); g = np.concatenate(gall)
    se = np.concatenate(sall); gd = np.concatenate(dall)
    # one point per input amplitude: the first block wins (S > L > C);
    # C's cross-checks at 100 and 150 uVpp duplicate S2 / L0 and are dropped
    seen, keep = set(), np.ones(len(v), dtype=bool)
    for i in range(len(v)):
        if gd[i]:
            continue
        kk = round(float(v[i]), 1)
        if kk in seen:
            keep[i] = False
        else:
            seen.add(kk)
    v, g, se = v[keep], g[keep], se[keep]
    gd = gd[keep]

    gdb = 20 * np.log10(g)
    sdb = 20 / np.log(10) * (se / (v * 1e-6)) / g          # se -> dB (rel. err)
    fig, ax = plt.subplots(figsize=(3.45, 2.4))
    o = np.argsort(v[~gd])
    ax.errorbar(v[~gd][o], gdb[~gd][o], yerr=sdb[~gd][o], fmt="o",
                ms=4.2, color=C_HI, elinewidth=0.8, capsize=1.8,
                markeredgecolor="white", markeredgewidth=0.6,
                label="measured", zorder=3)
    A_ = np.column_stack([np.ones_like(v[~gd]), np.log(v[~gd])])
    cf, *_ = np.linalg.lstsq(A_, gdb[~gd], rcond=None)
    xs = np.linspace(v.min(), v.max(), 200)
    ax.plot(xs, cf[0] + cf[1] * np.log(xs), "-", lw=1.0, color=MUTED, zorder=1,
            label=f"fit: {cf[1]:.2f} dB per e-fold")
    ax.set_xscale("log")
    ax.set_xlabel("input amplitude [µVpp]"); ax.set_ylabel("gain [dB]")
    ax.legend(loc="upper right", fontsize=7.2, handlelength=1.4,
              borderaxespad=0.3, labelspacing=0.3)
    ax.margins(y=0.12)
    style(ax)
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"gain_vs_level_highgain.{e}"))
    plt.close(fig)
    print(f"gain_vs_level_highgain.pdf  fit {cf[1]:.3f} dB per e-fold, "
          f"{(~gd).sum()} points + {gd.sum()} guards")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig12(); fig14(); fig9()
