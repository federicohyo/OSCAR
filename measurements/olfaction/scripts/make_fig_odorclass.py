#!/usr/bin/env python3
"""Make the classification-pipeline figure.

Two held-out chunks, one row each -- eucalyptol (top) and another odor
(bottom) -- carried through the four stages of the measured pipeline:

  (a) the 8-channel MOx recording of one 50 ms heater cycle,
  (b) the encoding, ALL sixteen neurons, one row each: the z-scored random
      projection trace on the row baseline, with the spikes its level
      crossings emit as green (excitatory) / red (inhibitory) ticks,
  (c) the measured 16-neuron spike raster (data/olfaction/olf_validate/centre_r0.npz,
      the centre bias point),
  (d) the exponential-kernel traces of all 16 neurons (tau = 50 ms) in light
      grey, the median-event neuron highlighted; the read-out samples each
      trace at four epochs (vertical dashed lines); the highlighted neuron's
      four samples are marked. Per neuron: 4 epochs x 2 tau = 16 x 4 x 2
      features in all.

No hardware needed; everything is replayed from disk.

    PYTHONPATH=. ./.venv-meas/bin/python3 make_fig_odorclass.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from olfaction_bias_bo import build, encoders, score
from olfaction_iso_compare import kernel

NPZ = "data/olfaction/olf_validate/centre_r0.npz"
OUT = "measurements/olfaction/figures/odorclass_pipeline"
CLASS1 = "Eu"                          # top row
CLASS2_PREF = ["IA", "EB", "2H"]       # bottom row: first of these available
T_CHUNK = 0.05        # 50 ms heater cycle, native
C_UP, C_DN = "#1a9850", "#d73027"
C_HI = "#e08214"      # highlighted neuron in panel (d)


def pick_chunk(cls, Y, pred, tot, it, names):
    """Bulk of the class, correctly classified, healthy spiking -> median one."""
    ci = names.index(cls)
    cand = [j for j in range(len(Y))
            if Y[j] == ci and pred[j] == Y[j] and tot[j] > np.median(tot)]
    return cand[len(cand) // 2]


DISPLAY = {"2H": "2-hexanone", "EB": "ethyl butyrate", "Eu": "eucalyptol",
           "IA": "isoamyl acetate", "Blank": "blank"}


def draw_row(ax, j, F, sp, Y, it, enc, T, theta, neurons, names):
    """Draw the four pipeline panels for chunk j into the row `ax`."""
    zbase = DISPLAY.get(names[Y[j]], names[Y[j]])

    # (a) raw 8-channel chunk
    Fj = F[j].reshape(50, 8)
    tms = np.arange(50) / 50 * T_CHUNK * 1e3
    for c in range(8):
        z = (Fj[:, c] - Fj[:, c].mean()) / (Fj[:, c].std() + 1e-9)
        ax[0].plot(tms, z + c * 5, lw=0.5, color=plt.cm.viridis(c / 8))
    ax[0].set_xlim(0, 50)
    ax[0].set_yticks([c * 5 for c in range(8)])
    ax[0].set_yticklabels([f"ch{c}" for c in range(8)], fontsize=6)
    ax[0].set_ylabel(zbase, fontsize=6.5, labelpad=2)

    # (b) encoding: one row per neuron (same order as panel (c)) --
    #     z-scored projection trace on the row baseline; event ticks on it
    tms_p = np.arange(50) / 50 * T * 1e3                    # as played out
    SCL, SLEN = 0.30, 0.28
    for ri, kb in enumerate(neurons):                       # n0 at the bottom
        y0 = float(ri)
        wb = np.random.default_rng(100 + kb).normal(0, 1, 8)  # encoders()'s seeding
        sb = F[j].reshape(50, 8) @ wb
        sb = (sb - sb.mean()) / (sb.std() + 1e-9)
        evb = enc[kb][j]
        ax[1].plot([0, T * 1e3], [y0, y0], lw=0.25, color="0.90", zorder=1)
        for u in [t * T * 1e3 for t, c in evb if c == 0]:   # exc ticks
            ax[1].plot([u, u], [y0, y0 + SLEN], lw=0.55,
                       color=C_UP, solid_capstyle="butt", zorder=2)
        for v in [t * T * 1e3 for t, c in evb if c == 1]:   # inh ticks
            ax[1].plot([v, v], [y0 - SLEN, y0], lw=0.55,
                       color=C_DN, solid_capstyle="butt", zorder=2)
        ax[1].plot(tms_p, sb * SCL + y0, lw=0.45, color="k", zorder=3)
    ax[1].set_ylim(-0.6, len(neurons) - 0.4)
    ax[1].set_xlim(0, T * 1e3)
    ax[1].set_yticks(range(0, 16, 5))
    ax[1].set_yticklabels([f"n{i}" for i in range(0, 16, 5)], fontsize=6)

    # (c) measured raster
    st = [np.clip(np.asarray(sp[i, j], dtype=float), 0, T) for i in range(len(neurons))]
    for i, tsr in enumerate(st):
        if len(tsr):
            ax[2].plot(tsr * 1e3, [i] * len(tsr), "|", ms=4, mew=0.7, color="k")
    ax[2].set_xlim(0, T * 1e3)
    ax[2].set_ylim(-0.6, len(neurons) - 0.4)
    ax[2].set_yticks(range(0, 16, 5))
    ax[2].set_yticklabels([f"n{i}" for i in range(0, 16, 5)], fontsize=6)

    # (d) kernel traces (tau = 50 ms); the median-event neuron highlighted
    evc = np.array([len(enc[kb][j]) for kb in neurons])
    khi = int(np.argsort(evc)[len(neurons) // 2])
    tK = np.linspace(0, T, 400)
    tau_show, grid = 0.050, np.linspace(T / 4, T, 4)
    for i, tsr in enumerate(st):
        if len(tsr):
            dK = tK[None, :] - tsr[:, None]
            Ktr = np.exp(-np.where(dK >= 0, dK, np.inf) / tau_show).sum(0)
        else:
            Ktr = np.zeros_like(tK)
        hi_n = (i == khi)
        ax[3].plot(tK * 1e3, Ktr + i * 6, lw=0.9 if hi_n else 0.4,
                   color=C_HI if hi_n else "0.72",
                   zorder=4 if hi_n else 1)
    for g in grid:                                        # the 4 sample epochs
        ax[3].axvline(g * 1e3, lw=0.3, color="0.55", ls=(0, (2, 2)), zorder=0)
    if len(st[khi]):
        # the highlighted neuron's spikes, and its FAST kernel (tau=10 ms):
        # the slow kernel saturates at this rate and hides the timing
        ax[3].plot(st[khi] * 1e3, [khi * 6 - 0.4] * len(st[khi]), "|", ms=3,
                   mew=0.5, color="k", zorder=5)
        dKf = tK[None, :] - st[khi][:, None]
        Ktrf = np.exp(-np.where(dKf >= 0, dKf, np.inf) / 0.010).sum(0)
        ax[3].plot(tK * 1e3, Ktrf + khi * 6, lw=0.7, color=C_HI,
                   ls=(0, (1.5, 1.2)), zorder=6)
        dG = grid[None, :] - st[khi][:, None]
        gvals = np.exp(-np.where(dG >= 0, dG, np.inf) / tau_show).sum(0)
        ax[3].plot(grid * 1e3, gvals + khi * 6, "o", ms=3.4, mfc="none",
                   mec="k", mew=0.8, zorder=7)
    ax[3].set_xlim(0, T * 1e3)
    ax[3].set_yticks([i * 6 for i in range(0, 16, 5)])
    ax[3].set_yticklabels([f"n{i}" for i in range(0, 16, 5)], fontsize=6)


def main():
    d = np.load(NPZ, allow_pickle=True)
    sp = d["spikes"]                      # (16, 150) object array, seconds
    Y, it = d["labels"], d["trial"]
    T, theta = float(d["T"]), float(d["theta"])
    names = [str(c) for c in d["classes"]]
    neurons = [int(k) for k in d["neurons"]]

    F, Y2, it2, _ = build("0.1s", theta, neurons)
    assert (Y2 == Y).all() and (it2 == it).all(), "npz and dataset disagree"

    # --- pick the two demo chunks (same rule): the named class, correctly
    #     classified by the actual pipeline, with healthy spiking -------------
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    _, pred = score(sp, Y, it, T, folds)
    nsp = np.array([[len(np.asarray(sp[i, j])) for j in range(len(Y))]
                    for i in range(len(neurons))])
    tot = nsp.sum(0)
    enc = encoders(F, theta, neurons)

    j1 = pick_chunk(CLASS1, Y, pred, tot, it, names)
    cls2 = next((c for c in CLASS2_PREF
                 if c in names
                 and sum(1 for j in range(len(Y))
                         if Y[j] == names.index(c) and pred[j] == Y[j]
                         and tot[j] > np.median(tot)) >= 3), None)
    assert cls2 is not None, "need a second class with enough healthy chunks"
    j2 = pick_chunk(cls2, Y, pred, tot, it, names)
    for tag, jj in ((names[Y[j1]], j1), (names[Y[j2]], j2)):
        print(f"row chunk: j={jj} class={tag} trial={it[jj]}, "
              f"spikes={tot[jj]}, predicted {names[pred[jj]]} (correct)")

    fig, axes = plt.subplots(2, 4, figsize=(7.16, 4.5))
    fig.subplots_adjust(left=0.078, right=0.995, bottom=0.09, top=0.94,
                        wspace=0.32, hspace=0.42)

    for r, jj in enumerate((j1, j2)):
        draw_row(axes[r], jj, F, sp, Y, it, enc, T, theta, neurons, names)
        for a in axes[r]:
            a.tick_params(axis="x", labelsize=6.5)
            for spn in ("top", "right"):
                a.spines[spn].set_visible(False)

    # panel letter tags above the axes frames (descriptions live in the caption)
    for c, a in enumerate(axes[0]):
        a.text(0.0, 1.045, f"({chr(97 + c)})", transform=a.transAxes,
               fontsize=7.5, va="bottom", ha="left", zorder=6)

    # x-labels only on the bottom row
    for a in axes[0]:
        a.set_xticklabels([])
    for a in axes[1]:
        a.set_xlabel("presentation time [ms]", fontsize=7)

    # tick-polarity key, once, on the top row of panel (b)
    axb, yk = axes[0, 1], len(neurons) - 0.3
    axb.plot([T * 1e3 + 2] * 2, [yk, yk + 0.35], lw=0.7, color=C_UP,
             solid_capstyle="butt", clip_on=False)
    axb.text(T * 1e3 + 3.2, yk + 0.18, "exc", fontsize=5.5, color=C_UP,
             va="center", ha="left", clip_on=False)
    axb.plot([T * 1e3 + 2] * 2, [yk - 0.55, yk - 0.2], lw=0.7, color=C_DN,
             solid_capstyle="butt", clip_on=False)
    axb.text(T * 1e3 + 3.2, yk - 0.38, "inh", fontsize=5.5, color=C_DN,
             va="center", ha="left", clip_on=False)

    fig.savefig(f"{OUT}.pdf")
    fig.savefig(f"{OUT}.png", dpi=220)
    print(f"wrote {OUT}.pdf / .png")


if __name__ == "__main__":
    main()
