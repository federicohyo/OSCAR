#!/usr/bin/env python3
"""MIT-BIH (PhysioNet) beat loader/encoder for the reservoir-computing pipeline.

Downloads MIT-BIH Arrhythmia records via wfdb, segments beats around annotated
R-peaks, resamples to a fixed length, normalizes amplitude to [0,1], and labels
them (AAMI-style, binary Normal vs. PVC/ventricular to start). Provides an
amplitude -> Poisson-rate encoder for on-chip stimulation.
"""

import numpy as np
import wfdb

# AAMI-style symbol groups.
NORMAL = set("NLRej")   # normal + BBB + nodal/atrial escapes
SUPRA = set("AaJS")     # supraventricular ectopic (APB, aberrated, nodal, SVPB)
VENTRIC = set("VE")     # PVC + ventricular escape

# class label maps: string selects which classes and their integer labels
CLASS_SETS = {
    "NV": [("N", NORMAL, 0), ("V", VENTRIC, 1)],
    "NSV": [("N", NORMAL, 0), ("S", SUPRA, 1), ("V", VENTRIC, 2)],
}


# All QRS (beat) annotation symbols -- used to build the R-peak sequence for RR
# intervals (rhythm), independent of which classes we keep for training.
BEAT_SYMS = set("NLRejAaJSVEF/fQ?Brn")
RR_NAMES = ("prev_rr", "next_rr", "rr_ratio", "local_avg_rr")


def _rr_features(samps, syms, fs, win=10):
    """Per-beat-annotation RR features (de Chazal-style rhythm features), computed from
    consecutive QRS R-peaks: prev-RR, next-RR, prev-RR / local-average-RR, local-avg-RR.
    Returns an (n_beat_ann, 4) array plus the ann indices those rows correspond to."""
    beat_pos = [i for i, sy in enumerate(syms) if sy in BEAT_SYMS]
    b = np.asarray(samps)[beat_pos].astype(float) / fs      # R-peak times (s)
    n = len(b)
    prev = np.full(n, np.nan); nxt = np.full(n, np.nan)
    prev[1:] = b[1:] - b[:-1]
    nxt[:-1] = b[1:] - b[:-1]
    loc = np.full(n, np.nan)
    for p in range(n):
        w = prev[max(0, p - win):min(n, p + win + 1)]
        w = w[~np.isnan(w)]
        loc[p] = w.mean() if w.size else np.nan
    ratio = prev / loc
    rr = np.column_stack([prev, nxt, ratio, loc])
    return rr, beat_pos


def get_beats(records=("100", "208", "119", "233"), win=(-90, 144), fs=360,
              length=128, n_per_class=150, seed=0, classes="NV"):
    """Return X (n, length) normalized beat windows, y (integer class), metadata.
    `classes` in {"NV","NSV"}; win = (samples before, after) R-peak at fs=360 Hz.
    meta["rr"] = (n, 4) RR/rhythm features aligned with X/y (names in meta["rr_names"])."""
    groups = CLASS_SETS[classes]
    rng = np.random.default_rng(seed)
    beats, labels, recs, rrs = [], [], [], []
    for rec in records:
        sig, fields = wfdb.rdsamp(rec, pn_dir="mitdb")
        ann = wfdb.rdann(rec, "atr", pn_dir="mitdb")
        x = sig[:, 0]  # lead MLII
        rr_rec, beat_pos = _rr_features(ann.sample, ann.symbol, fs)
        pos_of = {i: p for p, i in enumerate(beat_pos)}   # ann index -> beat position
        for i, (s, sym) in enumerate(zip(ann.sample, ann.symbol)):
            a, b = s + win[0], s + win[1]
            if a < 0 or b >= len(x):
                continue
            lab = next((L for _, syms, L in groups if sym in syms), None)
            if lab is None:
                continue
            seg = x[a:b].astype(float)
            # resample to fixed length
            seg = np.interp(np.linspace(0, len(seg) - 1, length),
                            np.arange(len(seg)), seg)
            # per-beat normalize to [0,1]
            lo, hi = seg.min(), seg.max()
            seg = (seg - lo) / (hi - lo + 1e-9)
            beats.append(seg)
            labels.append(lab)
            recs.append(rec)
            p = pos_of.get(i)
            rrs.append(rr_rec[p] if p is not None else np.full(4, np.nan))
    beats, labels, recs = np.array(beats), np.array(labels), np.array(recs)
    rrs = np.array(rrs, dtype=float)
    # impute edge-beat NaNs with column medians (deterministic; few beats)
    for c in range(rrs.shape[1]):
        col = rrs[:, c]
        col[np.isnan(col)] = np.nanmedian(col)
    # balance across all present classes
    class_labels = sorted({L for _, _, L in groups})
    idxs = [np.where(labels == c)[0] for c in class_labels]
    k = min([n_per_class] + [len(ix) for ix in idxs])
    sel = np.concatenate([rng.choice(ix, k, replace=False) for ix in idxs])
    rng.shuffle(sel)
    return beats[sel], labels[sel], {"fs": fs, "length": length, "classes": classes,
                                     "k": k, "records": recs[sel], "rr": rrs[sel],
                                     "rr_names": RR_NAMES}


def get_beat_sequences(records=("200", "208", "209", "222", "223", "232", "233"),
                       classes="NSV", n_per_class=30, seed=0, n_before=2, n_after=1,
                       win=(-90, 144), fs=360, length=128):
    """Like get_beats, but per TARGET beat returns a sequence of consecutive beats with
    their REAL inter-beat timing (for A2 sequential presentation). Each sequence element
    is (t_off_sec, morph128) where t_off_sec is the neighbour R-peak time relative to the
    target R-peak. meta['rr'] and meta['target'] (the target's own morph) are aligned.
    Only target beats with the full n_before+n_after neighbours (all windowable) are kept."""
    groups = CLASS_SETS[classes]
    rng = np.random.default_rng(seed)
    seqs, labels, recs, rrs, targ = [], [], [], [], []
    for rec in records:
        sig, _ = wfdb.rdsamp(rec, pn_dir="mitdb")
        ann = wfdb.rdann(rec, "atr", pn_dir="mitdb")
        x = sig[:, 0]
        rr_rec, beat_pos = _rr_features(ann.sample, ann.symbol, fs)
        bsamp = np.asarray(ann.sample)[beat_pos]
        bsym = [ann.symbol[i] for i in beat_pos]
        # precompute each beat's normalized morphology (None if not fully windowable)
        morph = []
        for s in bsamp:
            a, b = s + win[0], s + win[1]
            if a < 0 or b >= len(x):
                morph.append(None); continue
            seg = x[a:b].astype(float)
            seg = np.interp(np.linspace(0, len(seg) - 1, length), np.arange(len(seg)), seg)
            lo, hi = seg.min(), seg.max()
            morph.append((seg - lo) / (hi - lo + 1e-9))
        nb = len(bsamp)
        for p in range(nb):
            lab = next((L for _, syms, L in groups if bsym[p] in syms), None)
            if lab is None:
                continue
            q0, q1 = p - n_before, p + n_after
            if q0 < 0 or q1 >= nb or any(morph[q] is None for q in range(q0, q1 + 1)):
                continue
            seq = [((bsamp[q] - bsamp[p]) / fs, morph[q]) for q in range(q0, q1 + 1)]
            seqs.append(seq); labels.append(lab); recs.append(rec)
            rrs.append(rr_rec[p]); targ.append(morph[p])
    labels, recs = np.array(labels), np.array(recs)
    rrs = np.array(rrs, dtype=float)
    for c in range(rrs.shape[1]):
        col = rrs[:, c]; col[np.isnan(col)] = np.nanmedian(col)
    class_labels = sorted({L for _, _, L in groups})
    idxs = [np.where(labels == c)[0] for c in class_labels]
    k = min([n_per_class] + [len(ix) for ix in idxs])
    sel = np.concatenate([rng.choice(ix, k, replace=False) for ix in idxs])
    rng.shuffle(sel)
    seqs = np.array(seqs, dtype=object)
    return (seqs[sel], labels[sel],
            {"fs": fs, "length": length, "classes": classes, "k": k,
             "records": recs[sel], "rr": rrs[sel], "rr_names": RR_NAMES,
             "target": np.array(targ, dtype=object)[sel]})


def encode_rate(beat, f_min=20.0, f_max=300.0):
    """Map a normalized beat (values in [0,1]) to a Poisson mean-rate profile (Hz)."""
    return f_min + beat * (f_max - f_min)


def delta_encode(beat, threshold=0.06):
    """Level-crossing (delta modulation) encoding, as in the DYNAP ECG work.
    Emits an UP spike each time the signal rises by `threshold` and a DOWN spike
    each time it falls by `threshold`, preserving morphology/derivative that rate
    coding discards. Returns a time-ordered list of (t_frac in [0,1], channel),
    channel 0 = UP (excitatory), 1 = DOWN (inhibitory)."""
    events = []
    ref = float(beat[0])
    n = len(beat)
    for i in range(n):
        v = float(beat[i])
        tf = i / (n - 1)
        while v - ref >= threshold:
            ref += threshold
            events.append((tf, 0))
        while ref - v >= threshold:
            ref -= threshold
            events.append((tf, 1))
    return events


def _gaussian_smooth(x, sigma):
    if sigma <= 0.1:
        return x
    r = max(1, int(round(3 * sigma)))
    t = np.arange(-r, r + 1)
    w = np.exp(-(t ** 2) / (2 * sigma ** 2)); w /= w.sum()
    return np.convolve(x, w, mode="same")


def delta_encode_proj(beat, sigma=0.0, shift=0.0, theta=0.04):
    """Per-neuron projected delta encoding: Gaussian-smooth the ECG (width sigma),
    time-shift it (fraction of the beat), renormalise, then delta-encode at theta.
    A fixed per-neuron projection decorrelates the input each neuron sees."""
    x = _gaussian_smooth(np.asarray(beat, dtype=float), sigma)
    n = len(x)
    s = int(round(shift * n))
    if s != 0:
        x = np.roll(x, s)
    lo, hi = x.min(), x.max()
    x = (x - lo) / (hi - lo + 1e-9)
    return delta_encode(x, theta)


if __name__ == "__main__":
    X, y, meta = get_beats(records=("208",), n_per_class=20)
    print("beats:", X.shape, "labels:", np.bincount(y), "meta:", meta)
    r = encode_rate(X[0])
    print("rate profile Hz: min %.0f max %.0f" % (r.min(), r.max()))
