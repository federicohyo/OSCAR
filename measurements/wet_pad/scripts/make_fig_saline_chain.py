#!/usr/bin/env python3
"""The pad-to-neuron chain figure, twin of make_fig10_silicon_full.py.

    ../.venv-meas/bin/python3 make_fig_saline_chain.py

    (a) the real recorded event: the second saline injection of
        scope_20260829_103015.csv at the wetted TiO2 pad (via saline_event.csv,
        written by saline_stimulus.py);
    (b) the connector-fed amplifier's output when that event, input-referred
        and sign-flipped, is replayed through it -- folded repeats from the
        CLEAN acquisition (a --dry dual run: neuron injection is off, so its
        spikes stay out of the amplifier channel -- the same reason
        the reference figure(b) is a single-channel run);
    (c) the membrane of neuron 9, recorded simultaneously with the events that
        drove it (the live dual run), one representative repeat dark, the rest
        faint, with the integrate-and-fire inset.

Bench runs this figure consumes:

    ../.venv-meas/bin/python3 saline_stimulus.py
    CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 odor_neuron_loop_dual.py \
        --wav saline_stimulus.wav --timing saline_timing.json \
        --bias <your.biases> --syn <K> --dry --out saline_amp_clean.npz
    CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 odor_neuron_loop_dual.py \
        --wav saline_stimulus.wav --timing saline_timing.json \
        --bias <your.biases> --syn <K> --out saline_chain_dual.npz

The dry run records zero fires, so panel (b) folds on event onsets re-detected
offline from the raw channel with the run's own detector (25 ms box, 1.2 s
trailing median, 40 mV); the -12 ms smoother group delay is subtracted.
"""
import argparse, csv, json, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FS, SMOOTH_DELAY = 1000.0, 0.012

MUT = "#5c5f66"
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUT, "xtick.color": MUT,
    "ytick.color": MUT, "axes.linewidth": .8, "grid.color": "#d7d9de",
    "legend.frameon": True, "legend.framealpha": .9, "legend.edgecolor": "#d7d9de",
    "font.family": "serif", "savefig.bbox": "tight"})
BLUE, RED, GRN = "#1f4fd8", "#c62828", "#137a5f"

BENCH_HINT = """data needed. On the bench, in LNA/:
  ../.venv-meas/bin/python3 saline_stimulus.py
  CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 odor_neuron_loop_dual.py \\
      --wav saline_stimulus.wav --timing saline_timing.json \\
      --bias <your.biases> --syn <K> --dry --out saline_amp_clean.npz
  CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 odor_neuron_loop_dual.py \\
      --wav saline_stimulus.wav --timing saline_timing.json \\
      --bias <your.biases> --syn <K> --out saline_chain_dual.npz
  then re-run this script."""


def load_event_csv(path):
    rows = list(csv.DictReader(open(path)))
    t = np.array([float(r["t_s"]) for r in rows])
    raw = np.array([float(r["pad_out_recorded_mv"]) for r in rows])
    sm = np.array([float(r["pad_out_smoothed_mv"]) for r in rows])
    return t, raw, sm


def detect_onsets(t, v, period, thresh_mv=40.0, smooth_s=0.025, base_s=1.20):
    """The loop's detector, replayed on the record. Onsets of upward excess."""
    nsm, nbl = max(1, int(smooth_s * FS)), max(1, int(base_s * FS))
    cu = np.convolve(v, np.ones(nsm) / nsm, "same")
    on, last = [], -1e9
    for i in range(nbl, len(v) - nsm):
        base = np.median(v[i - nbl:i])
        if (cu[i] - base) * 1e3 > thresh_mv and t[i] - last > 0.6 * period:
            on.append(t[i] - SMOOTH_DELAY); last = t[i]
    return on


def fold(t, v, onsets, grid):
    out = []
    for c in onsets:
        if c + grid[0] < t[0] or c + grid[-1] > t[-1]:
            continue
        out.append(np.interp(c + grid, t, v))
    return np.vstack(out) if out else np.zeros((0, len(grid)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--event", default=os.path.join(HERE, "saline_event.csv"))
    ap.add_argument("--loop", default=os.path.join(HERE, "saline_amp_clean.npz"),
                    help="npz of the --dry dual run (clean amplifier channel)")
    ap.add_argument("--dual", default=os.path.join(HERE, "saline_chain_dual.npz"),
                    help="npz of the live dual run (membrane)")
    ap.add_argument("--timing", default=os.path.join(HERE, "saline_timing.json"))
    ap.add_argument("--grid", type=float, nargs=2, default=(-0.40, 1.20))
    ap.add_argument("--thresh", type=float, default=40.0,
                    help="offline onset threshold above trailing median, mV")
    ap.add_argument("--inset", type=float, nargs=2, default=None,
                    help="inset window in s from onset (default: auto)")
    args = ap.parse_args()
    for p in (args.event, args.loop, args.dual, args.timing):
        if not os.path.exists(p):
            sys.exit(f"{p}: required\n{BENCH_HINT}")

    tm = json.load(open(args.timing))
    P = tm["period_s"]
    grid = np.arange(args.grid[0], args.grid[1], 1.0 / FS)

    # --- (a) the real event --------------------------------------------------
    ta, araw, asm = load_event_csv(args.event)

    # --- (b) replayed amplifier output, clean run ----------------------------
    loop = np.load(args.loop, allow_pickle=True)
    rw = loop["raw"]
    tb = rw[:, 0] - rw[0, 0]                       # board clock, per-sample
    ch1 = rw[:, 2]
    if loop["fires"].size:
        ons = sorted(loop["fires"][:, 0].tolist())
    else:
        ons = detect_onsets(tb, ch1, P, thresh_mv=args.thresh)
    L = fold(tb, ch1, ons, grid)
    L -= np.median(L[:, grid < -0.20], axis=1, keepdims=True)
    lmed, lsd = np.median(L, axis=0), L.std(axis=0)

    # --- (c) the membrane, live dual run (as make_fig10) ---------------------
    dual = np.load(args.dual, allow_pickle=True)
    draw = dual["raw"]
    tmb = draw[:, 0] - draw[0, 0] + draw[0, 1]
    vmb = draw[:, 3]
    _f = dual["fires"][:, 0]
    if len(_f) == 0:
        sys.exit(f"{args.dual}: zero fires -- was this run really live (rather than --dry)?")
    _ev = [[_f[0]]]
    for _x in _f[1:]:
        (_ev[-1] if _x - _ev[-1][-1] < 0.5 else _ev.append([]) or _ev[-1]).append(_x)
    _ons = [e[0] for e in _ev
            if e[0] + grid[0] >= tmb[0] and e[0] + grid[-1] <= tmb[-1]]
    M = np.vstack([np.interp(c + grid, tmb, vmb) for c in _ons])

    drp = [float(z["drops"]) for z in (loop, dual) if "drops" in z]
    stl = [float(z["stalls"]) for z in (loop, dual) if "stalls" in z]
    print(f"clean repeats {L.shape[0]}, membrane repeats {M.shape[0]}, "
          f"period {P:.3f} s")
    print(f"stream health: drops {drp} stalls {stl}"
          + ("" if all(d == 0 for d in drp + stl) else "  <-- not zero, see the bench rule"))

    fig, ax = plt.subplots(3, 1, figsize=(3.45, 4.6), sharex=True)

    ax[0].plot(ta, araw, lw=.6, color=BLUE, alpha=.35)
    ax[0].plot(ta, asm, lw=1.2, color=BLUE, label=r"$V_{pad}^{rec}$ (mV)")
    ax[0].set_ylabel(r"$V_{pad}^{rec}$ (mV)", color=BLUE)
    ax[0].tick_params(axis="y", labelcolor=BLUE)

    for row in L:
        ax[1].plot(grid, row * 1e3, lw=.45, color=RED, alpha=.25)
    if len(L):
        ax[1].fill_between(grid, (lmed - lsd) * 1e3, (lmed + lsd) * 1e3,
                           color=RED, alpha=.20, lw=0)
        ax[1].plot(grid, lmed * 1e3, lw=1.3, color="#8c1010",
                   label=r"$V_{LNA}^{out}$ (mV)")
    ax[1].set_ylabel(r"$V_{LNA}^{out}$ (mV)", color=RED)
    ax[1].tick_params(axis="y", labelcolor=RED)

    for row in M:
        ax[2].plot(grid, row, lw=.5, color=GRN, alpha=.28)
    _thr_c = 0.5 * (np.median(M[:, grid < -0.20]) + M.max())
    _nspk = [int(((r[1:-1] > r[:-2]) & (r[1:-1] >= r[2:]) & (r[1:-1] > _thr_c)).sum())
             for r in M]
    _rep = int(np.argmax(_nspk))
    print(f"spikes per repeat {_nspk}; representative = repeat {_rep}")
    ax[2].plot(grid, M[_rep], lw=1.0, color="#0b4f3d", label=r"$V_{mem}$ (V)")
    ax[2].set_ylabel(r"$V_{mem}$ (V)", color=GRN)
    ax[2].tick_params(axis="y", labelcolor=GRN)
    ax[2].set_xlabel("Time from event onset (s)")

    for a_, lab, lloc in zip(ax, ("(a)", "(b)", "(c)"),
                             ("upper right", "upper right", "upper left")):
        a_.grid(alpha=.5); a_.set_axisbelow(True)
        a_.set_xlim(args.grid[0], args.grid[1])
        a_.legend(loc=lloc, fontsize=6.8, handlelength=1.3, borderaxespad=0.3)
        a_.annotate(lab, xy=(0.014, 0.06), xycoords="axes fraction", fontsize=9,
                    fontweight="bold", color="#1b1b1f")
        for s_ in ("top", "right"):
            a_.spines[s_].set_visible(False)

    # --- inset: integrate-and-fire detail, auto window -----------------------
    def spikes_of(row):
        k = np.flatnonzero((row[1:-1] > row[:-2]) &
                           (row[1:-1] >= row[2:]) & (row[1:-1] > _thr_c)) + 1
        return grid[k]
    spk = spikes_of(M[_rep])
    spk_in = spk[(spk > -0.02) & (spk < 0.8)]
    if len(spk_in):
        t_first = float(spk_in[0])
        t_next = float(spk_in[1]) if len(spk_in) > 1 else t_first + 0.12
        if args.inset:
            INS_T0, INS_T1 = args.inset
        else:
            INS_T0 = max(grid[0] + 0.005, t_first - 0.03)
            INS_T1 = min(grid[-1] - 0.005,
                         t_next + 0.02 if t_next - t_first > 0.02 else t_first + 0.14)
        axi = ax[2].inset_axes([0.33, 0.575, 0.66, 0.40], facecolor="white")
        axi.set_zorder(5); axi.patch.set_alpha(1.0)
        _m = (grid >= INS_T0) & (grid <= INS_T1)
        for row in M:
            axi.plot(grid[_m] * 1e3, row[_m], lw=.4, color=GRN, alpha=.22)
        axi.plot(grid[_m] * 1e3, M[_rep][_m], lw=.9, color="#0b4f3d")
        axi.set_xlim(INS_T0 * 1e3, INS_T1 * 1e3)
        axi.tick_params(labelsize=5.0, length=2, pad=1)
        axi.yaxis.tick_right()
        axi.annotate("ms", xy=(0.985, 0.06), xycoords="axes fraction", ha="right",
                     va="bottom", fontsize=5.5, color=MUT)
        axi.grid(alpha=.35); axi.set_axisbelow(True)
        for s_ in axi.spines.values():
            s_.set_edgecolor(MUT); s_.set_linewidth(.6)
        _y0, _y1 = M[:, _m].min(), M[:, _m].max()
        ax[2].add_patch(Rectangle((INS_T0, _y0), INS_T1 - INS_T0, _y1 - _y0,
                                  fill=False, ec=MUT, lw=.6, ls=(0, (3, 2)),
                                  alpha=.55, zorder=1))
        _in = spk_in[(spk_in >= INS_T0) & (spk_in <= INS_T1)]
        print(f"inset {INS_T0*1e3:+.0f}..{INS_T1*1e3:+.0f} ms, "
              f"{len(_in)} spikes in the representative repeat, ISI "
              f"{', '.join('%.0f' % x for x in np.diff(_in) * 1e3)} ms")
    else:
        print("no membrane spikes inside the event window -- inset skipped; "
              "check the operating point before trusting this figure")

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(HERE, "figures", f"fig_saline_chain.{ext}"), dpi=200)
    # panel (a) replays the recorded magnitudes
    print(f"panel (a): recorded dip {asm.min():+.0f} mV (smoothed), "
          f"{araw.min():+.0f} mV (raw)")
    if len(L):
        print(f"panel (b): replayed median peak {lmed.max()*1e3:+.1f} mV at "
              f"{grid[int(np.argmax(lmed))]:+.3f} s over {len(L)} repeats")
    print("figures/fig_saline_chain.png + .pdf")


if __name__ == "__main__":
    main()
