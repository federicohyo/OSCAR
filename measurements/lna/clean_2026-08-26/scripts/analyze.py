#!/usr/bin/env python3
"""Rebuild the three figures from the archived CSVs and raw traces. No bench.

    /storage/tue/avlsi2024-sw/.venv-meas/bin/python3 analyze.py

  figures/gain_vs_frequency.png   the transfer function
  figures/noise.png               output + input-referred noise ASD
  figures/gain_vs_level.png       gain and distortion vs input amplitude

Everything traces back to raw/<block>/<tag>.npz, one file per measured point.
"""
import csv, math, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FIG = os.path.join(ROOT, "figures"); os.makedirs(FIG, exist_ok=True)
FS, RAIL = 1000.0, 1.78

# One fixed hue order, assigned by entity and kept from cycling (dataviz rule).
INK, MUTED, GRID = "#1b1b1f", "#5c5f66", "#d7d9de"
C_MEAS, C_REF, C_WARN = "#2f6fd0", "#8a63d2", "#c2410c"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 200, "savefig.bbox": "tight",
    "font.size": 9, "axes.labelsize": 9.5, "axes.titlesize": 10,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.linewidth": 0.8,
    "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
})

def rd(block):
    p = os.path.join(ROOT, "derived", f"{block}.csv")
    if not os.path.exists(p): return []
    with open(p) as f: return [r for r in csv.DictReader(f)]

def fnum(r, k):
    try: return float(r[k])
    except (ValueError, KeyError, TypeError): return float("nan")


WAVDIR = os.path.abspath(os.path.join(ROOT, "..", "..", "_wavs"))
_drive_cache = {}
_drive_table = None

def true_drive(freq_hz, jack_vpp):
    """The drive amplitude the sound card was ACTUALLY given, not the nominal.

    make_wav() quantises to 16-bit PCM, and at these levels the tone is only tens
    of counts tall: the 40 uVpp point is 16 counts. Measured against the files,
    the delivered fundamental is systematically LOW -- -3.8% at the smallest
    amplitude, -0.16% at the largest. Dividing by the nominal vin therefore
    UNDER-states gain, worst exactly where the signal is smallest.

    So the true amplitude is fitted out of the WAV itself, at the same frequency
    the chip was driven at, and used as the x-axis. Returns nominal if the file
    falls back to nominal (and says so once).
    """
    key = (round(freq_hz, 4), round(jack_vpp, 6))
    if key in _drive_cache: return _drive_cache[key]

    # 1st choice: the snapshot in setup/. The WAVs themselves live OUTSIDE this
    # archive (~270 MB), so this table is what keeps the correction from silently
    # vanish on any other machine and quietly un-correct the low-end gains by
    # up to 4%.
    global _drive_table
    if _drive_table is None:
        _drive_table = {}
        cal = os.path.join(ROOT, "setup", "drive_calibration.csv")
        if os.path.exists(cal):
            with open(cal) as fh:
                for r in csv.DictReader(fh):
                    _drive_table[(round(float(r["freq_hz"]), 4),
                                  round(float(r["jack_vpp_nominal"]), 6))] = \
                        float(r["jack_vpp_true"])
    if key in _drive_table:
        _drive_cache[key] = _drive_table[key]
        return _drive_table[key]

    path = os.path.join(WAVDIR, f"{freq_hz:.4f}hz_{jack_vpp:.5f}vpp.wav")
    val = jack_vpp
    if os.path.exists(path):
        import wave
        with wave.open(path) as w:
            sr, n = w.getframerate(), w.getnframes()
            x = np.frombuffer(w.readframes(min(n, sr*20)), dtype="<i2").astype(float)
        t = np.arange(len(x)) / sr
        M = np.column_stack([np.sin(2*np.pi*freq_hz*t), np.cos(2*np.pi*freq_hz*t),
                             np.ones_like(t)])
        c, *_ = np.linalg.lstsq(M, x, rcond=None)
        val = 2*np.hypot(c[0], c[1])/32767 * np.sqrt(2.0)
    else:
        print(f"  *** WARNING: no drive calibration and no WAV for {freq_hz:.4f} Hz / "
              f"{jack_vpp:.5f} Vpp -- NOMINAL used, gain under-stated by up to 4% ***")
    _drive_cache[key] = val
    return val


def vin_true(r):
    """Chip-input amplitude with the PCM-quantisation bias removed."""
    j, f = fnum(r, "jack_vpp"), fnum(r, "freq_hz")
    if not (j == j and j > 0): return float("nan")
    return true_drive(f, j) * fnum(r, "divider")


def style(ax):
    ax.grid(True, which="both", alpha=.5); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)


# ---------------------------------------------------------- 1. transfer
def transfer():
    rows = [r for r in rd("transfer") if r["tag"].startswith("F") and not r["tag"].endswith("_guard")]
    if not rows: return print("transfer: no data yet")
    f = np.array([fnum(r, "freq_hz") for r in rows])
    vout = np.array([fnum(r, "vout_pp") for r in rows])
    se = np.array([fnum(r, "amp_se_v") for r in rows])
    vin = np.array([vin_true(r) for r in rows])          # quantisation-corrected
    g = vout / vin
    gdb = 20*np.log10(g)
    egdb = 20*np.log10(1 + se/(g*vin))          # 1-sigma from the fit residual

    plateau = np.median(gdb[(f > 20) & (f < 200)])

    # --- drive-path correction -------------------------------------------
    # The audio jack is AC-coupled (~0.93 Hz corner), so the raw curve below
    # ~20 Hz is the sound card in series with the amplifier. The reference pass is reused
    # could be taken this session (the probe that would measure it is the one
    # whose earth caused the ground loop), so the PREVIOUS campaign's reference
    # SHAPE is reused. Only its shape is used, normalised on its own plateau.
    # Above 130 Hz its clipped fit degrades, and an audio output rolls off well above
    # 200 Hz, so the drive is taken as flat there -- same rule as before.
    gdb_c, fc_c = None, float("nan")
    ref = os.path.join(ROOT, "..", "..", "lna_transfer_ref.csv")
    if os.path.exists(ref):
        with open(ref) as fh:
            rr = [r for r in csv.DictReader(fh)]
        rf = np.array([float(r["freq_hz"]) for r in rr])
        rg = np.array([float(r["gain"]) for r in rr])
        keep = (rg > 0) & np.isfinite(rg)
        rf, rg = rf[keep], rg[keep]
        i = np.argsort(rf); rf, rg = rf[i], rg[i]
        rplat = np.median(rg[(rf > 20) & (rf < 130)])
        shape = np.interp(np.log(f), np.log(rf), rg / rplat)
        shape[f > 130] = 1.0                  # documented: drive is flat up there
        shape = np.clip(shape, 1e-6, None)
        gdb_c = gdb - 20*np.log10(shape)
        ok = f > 0.2                          # below 0.2 Hz the jack delivers nothing
        b = ok & (f < 20)
        if b.sum() >= 2:
            j = np.argsort(f[b])
            fc_c = np.interp(plateau - 3.0, gdb_c[b][j], f[b][j])

    below = f < 20
    fc = float("nan")
    if below.sum() >= 2:
        i = np.argsort(f[below])
        fc = np.interp(plateau - 3.0, gdb[below][i], f[below][i])

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    if gdb_c is not None:
        m = f > 0.2
        ax.semilogx(f[m], gdb_c[m], "-", lw=1.8, color=C_MEAS, zorder=4,
                    label="amplifier (drive path divided out)")
        ax.plot(f[m], gdb_c[m], "o", ms=5, color=C_MEAS, zorder=5,
                markeredgecolor="white", markeredgewidth=.7)
        ax.semilogx(f, gdb, "--", lw=1.3, color=C_REF, zorder=3,
                    label="raw chain (incl. sound card)")
    else:
        ax.semilogx(f, gdb, "-", lw=1.6, color=C_MEAS, zorder=3, label="raw chain")
        ax.errorbar(f, gdb, yerr=egdb, fmt="o", ms=5, color=C_MEAS, lw=0,
                    elinewidth=1, capsize=2, ecolor=C_MEAS, zorder=4,
                    markeredgecolor="white", markeredgewidth=.7)
    ax.axhline(plateau, ls="--", lw=1, color=MUTED, zorder=1)
    ax.annotate(f"{plateau:.1f} dB  ({10**(plateau/20):.0f}×)",
                xy=(f.max()*.55, plateau), xytext=(0, 6), textcoords="offset points",
                ha="right", color=INK, fontsize=9.5)
    fshow = fc_c if fc_c == fc_c else fc
    if fshow == fshow:
        ax.axvline(fshow, ls=":", lw=1.2, color=C_WARN, zorder=2)
        ax.annotate(f"−3 dB\n{fshow:.2f} Hz", xy=(fshow, plateau-16), xytext=(6, 0),
                    textcoords="offset points", color=C_WARN, fontsize=8.5, va="center")
    ax.set_xlabel("frequency [Hz]"); ax.set_ylabel("gain [dB]")
    ax.set_title(f"LNA transfer function, {vin[0]*1e6:.0f} µVpp input", loc="left")
    ax.legend(loc="lower right", fontsize=8.5)
    style(ax)
    fig.savefig(os.path.join(FIG, "gain_vs_frequency.png"))
    fig.savefig(os.path.join(FIG, "gain_vs_frequency.pdf")); plt.close(fig)
    print(f"gain_vs_frequency.png: plateau {plateau:.2f} dB ({10**(plateau/20):.1f}x), "
          f"-3 dB raw {fc:.3f} Hz, corrected {fc_c:.3f} Hz, {len(f)} points")
    # Noise is referred through the AMPLIFIER's gain rather than the raw chain's:
    # below ~20 Hz the raw curve is mostly the sound card, and dividing by it
    # would inflate the input-referred noise by the sound card's own roll-off.
    return (f, 10**(gdb_c/20)) if gdb_c is not None else (f, g)


# ------------------------------------------------------- 2. gain vs level
def gain_vs_level():
    """Both sub-blocks: the main ladder (L, 18:03-18:09) and the low-end
    extension (S, 18:46-18:50). They were taken ~45 min apart with the transfer
    sweep in between, so they are plotted as SEPARATE series -- see the offset
    discussion in ../README.md. Merging them into one curve would invent a
    level dependence that is partly elapsed time."""
    rows = [r for r in rd("gain_vs_level") if r["tag"][0] in "LS"] + \
           [r for r in rd("gain_crosscheck") if r["tag"][0] == "C"]
    if not rows: return print("gain_vs_level: no data yet")

    def pack(pref):
        rs = [r for r in rows if r["tag"].startswith(pref)]
        vt = np.array([vin_true(r) for r in rs])
        return (vt*1e6,
                np.array([fnum(r, "vout_pp") for r in rs]) / vt,
                np.array([fnum(r, "amp_se_v") for r in rs]),
                np.array([fnum(r, "h2") for r in rs])*100,
                np.array([r["tag"].endswith("_guard") for r in rs]))

    fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.0))
    series = [("S", "low-end block (18:46)", C_REF),
              ("C", "cross-check block (18:55)", "#0f766e"),
              ("L", "main ladder (18:03)", C_MEAS)]
    allg = []
    for pref, lab, col in series:
        v, g, se, h2, gd = pack(pref)
        if len(v) == 0: continue
        allg.append(g)
        o = np.argsort(v[~gd])
        ax[0].errorbar(v[~gd][o], g[~gd][o], yerr=(se/(v*1e-6))[~gd][o], fmt="o-",
                       ms=6, lw=1.5, color=col, elinewidth=1, capsize=2,
                       markeredgecolor="white", markeredgewidth=.7, label=lab, zorder=3)
        ax[0].plot(v[gd], g[gd], "D", ms=7, color=col, markeredgecolor=C_WARN,
                   markeredgewidth=1.3, zorder=4)
        o2 = np.argsort(v[~gd])
        ax[1].plot(v[~gd][o2], h2[~gd][o2], "o-", ms=6, lw=1.5, color=col,
                   markeredgecolor="white", markeredgewidth=.7, label=lab, zorder=3)

    # Gain falls with drive. Across all blocks the fit is gain = a + b*ln(vin),
    # r = -0.64; the output DC is uncorrelated with gain (r = +0.01), so the trend is
    # compression rather than operating-point wander. Residual scatter ~2.5% is the
    # block-to-block reproducibility limit.
    va = np.concatenate([pack(pr)[0] for pr, _, _ in series if len(pack(pr)[0])])
    ga = np.concatenate([pack(pr)[1] for pr, _, _ in series if len(pack(pr)[0])])
    A_ = np.column_stack([np.ones_like(va), np.log(va)])
    cf, *_ = np.linalg.lstsq(A_, ga, rcond=None)
    xs = np.linspace(va.min(), va.max(), 100)
    ax[0].plot(xs, cf[0] + cf[1]*np.log(xs), "-", lw=1, color=MUTED, zorder=1,
               label=f"fit: {cf[1]:.1f}× per e-fold")
    ax[0].set_xscale("log"); ax[1].set_xscale("log")
    ax[0].set_xlabel("input amplitude [µVpp]"); ax[0].set_ylabel("gain [×]")
    ax[0].set_title("gain vs input amplitude", loc="left")
    ax[0].legend(loc="upper right", fontsize=8.2, handlelength=1.6,
                 borderaxespad=0.5, labelspacing=0.35)
    ax[0].annotate("outlined diamonds = repeat guard", xy=(0.02, 0.03),
                   xycoords="axes fraction", ha="left", fontsize=7.5, color=MUTED)
    ax[0].margins(y=0.14)
    style(ax[0])
    ax[1].set_xlabel("input amplitude [µVpp]")
    ax[1].set_ylabel("2nd harmonic [% of fundamental]")
    ax[1].set_title("distortion vs input amplitude", loc="left")
    ax[1].legend(loc="upper left", fontsize=8.5); style(ax[1])
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "gain_vs_level.png"))
    fig.savefig(os.path.join(FIG, "gain_vs_level.pdf")); plt.close(fig)
    g = np.concatenate(allg)
    print(f"gain_vs_level.png: {len(g)} points over "
          f"{np.concatenate([pack(p)[0] for p,_,_ in series]).max()/np.concatenate([pack(p)[0] for p,_,_ in series]).min():.0f}x "
          f"of input, gain {g.min():.1f}-{g.max():.1f}x")


# ------------------------------------------------------------- 3. noise
def noise(gain_f=None):
    """Output and input-referred noise from the quiet blocks.

    Narrowband interferers are detected GENERICALLY -- as bins standing well above
    a running median of their own neighbourhood rather than by assuming they are mains.
    On this bench they sit elsewhere: the strongest lines sit at ~4.2, 9.7, 87.4 and
    271.9 Hz, and mains-only flagging left every one of them in the "broadband"
    floor.
    """
    rows = [r for r in rd("noise") if r["tag"].startswith("N")]
    if not rows: return print("noise: no data yet")
    seg, P, nseg = 8192, None, 0
    for r in rows:
        d = np.load(os.path.join(ROOT, r["raw_npz"])); v = d["v"].astype(float)
        v.flags.writeable = False               # numpy in-place-elision guard
        w = np.hanning(seg)
        for i in range(0, len(v) - seg + 1, seg // 2):
            x = v[i:i+seg] - v[i:i+seg].mean()
            A = np.abs(np.fft.rfft(x*w))**2 * 2.0 / (FS * (w**2).sum())
            P = A if P is None else P + A
            nseg += 1
    P /= max(nseg, 1)
    f = np.fft.rfftfreq(seg, 1.0/FS)
    asd_out = np.sqrt(P)
    m = (f > 0.2) & (f < 450)
    f, asd_out = f[m], asd_out[m]

    # running-median line detector (generic rather than mains-specific)
    logA = np.log10(asd_out); k = 101
    pad = np.pad(logA, k//2, mode="edge")
    med = np.array([np.median(pad[i:i+k]) for i in range(len(logA))])
    line = logA > med + np.log10(3.0)           # >3x the local floor

    if gain_f is not None:
        gf, gg = gain_f
        i = np.argsort(gf)
        gi = np.exp(np.interp(np.log(f), np.log(gf[i]), np.log(gg[i])))
    else:
        gi = np.full_like(f, np.nan)
    asd_in = asd_out / gi

    fig, ax = plt.subplots(2, 1, figsize=(6.8, 6.6), sharex=True)
    ax[0].loglog(f, asd_out*1e6, lw=.8, color=MUTED, label="measured")
    ax[0].loglog(f[line], asd_out[line]*1e6, ".", ms=3.5, color=C_WARN,
                 label=f"narrowband lines ({line.sum()} bins)")
    ax[0].set_ylabel("output noise [µV/√Hz]")
    ax[0].set_title(f"LNA noise, {nseg} averages, sound card idle", loc="left")
    ax[0].legend(loc="lower left", fontsize=8); style(ax[0])

    ax[1].loglog(f[~line], asd_in[~line]*1e6, lw=1.1, color=C_MEAS)
    ax[1].set_xlabel("frequency [Hz]"); ax[1].set_ylabel("input-referred [µV/√Hz]")
    ax[1].set_title("input-referred, lines removed (÷ corrected amplifier gain)", loc="left")
    style(ax[1])
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "noise.png"))
    fig.savefig(os.path.join(FIG, "noise.pdf")); plt.close(fig)

    tp = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    band = (f > 1.0) & (f < 300) & ~line
    tot = np.sqrt(tp(asd_in[band]**2, f[band]))
    at1 = np.interp(1.0, f[~line], asd_in[~line])
    at10 = np.interp(10.0, f[~line], asd_in[~line])
    floor = np.median(asd_in[(f > 20) & (f < 300) & ~line])
    print(f"noise.png: input-referred {at1*1e6:.1f} uV/rtHz @1 Hz, {at10*1e6:.2f} @10 Hz, "
          f"floor {floor*1e6:.2f} uV/rtHz (20-300 Hz)")
    print(f"           {tot*1e6:.0f} uV rms over 1-300 Hz, lines excluded; "
          f"{nseg} averages, {line.sum()} line bins")
    top = np.argsort(asd_out*line)[::-1][:6]
    print("           strongest lines: " +
          ", ".join(f"{f[i]:.2f} Hz" for i in sorted(top, key=lambda j: f[j])))
    return f, asd_in, line


if __name__ == "__main__":
    gf = transfer()
    gain_vs_level()
    noise(gf)
