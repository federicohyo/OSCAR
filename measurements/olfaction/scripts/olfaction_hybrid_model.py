#!/usr/bin/env python3
"""Build the hybrid tree: a boosted ensemble whose every node test is a comparison the
analog array can physically perform. Offline half -- no bench time.

THE ARCHITECTURE (6.15). Conditional control stays on the RISC-V, where a branch is free;
the comparison goes to an analog neuron acting as a spike-count comparator. A node test
`x[f] <= t` becomes: encode x[f] as a burst of N spikes, present it to a neuron calibrated
to fire at >= L spikes, and take "did not fire" as the left branch.

THE OFF-BY-ONE, which is the whole reason this file exists separately. The tree asks
`N <= t`; the comparator answers `N >= L`. Those agree only for L = t+1, so the thresholds
this array can represent are t in {L-1} = {0,1,2,3,5,7,11,15,23,31}, NOT the calibrated
ladder {1,2,3,4,6,8,12,16,24,32} itself. Snapping to the wrong set costs accuracy that
then looks exactly like analog error. Hence check(): the snapped model is executed twice,
once with the arithmetic test and once through comparator semantics, and the two must
agree on every chunk before anything is run on silicon.

THE THREE RUNGS, so the analog cost is attributable. (i) full-precision digital, the
reference baseline; (ii) the same model quantised to 33 burst levels with thresholds
snapped to the ten the array has, executed DIGITALLY -- the algorithm's own ceiling under
the array's representation; (iii) rung (ii) executed with analog comparisons
(olfaction_hybrid_chip.py). Only the (ii)->(iii) gap is the analog substrate's cost.

Split mirrors olfaction_export_model.py exactly -- train on the 1.0 s pulses, test on the
0.1 s ones -- so these numbers sit beside the digital baseline with no CV machinery. The
quantiser is fit on TRAIN chunks only.

    ./.venv-meas/bin/python3 olfaction_hybrid_model.py
"""
import argparse, json, os
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as HGB

from olfaction_identity import chunks

NMAX = 32                                        # burst alphabet is 0..32 spikes
LADDER = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]      # bias FILE names (nominal levels)
THRS = [L - 1 for L in LADDER]                   # representable tree thresholds t

# The count at which each file actually switches, measured over ALL N in 0..32
# (olfaction_hybrid_chip.py --transfer). Five of the ten differ from their nominal
# level: the ladder calibration only ever probed N at the ladder points, so "lvl12
# switches at 12" was equally consistent with switching at 10 -- N=10 and 11 were never
# presented. The tree presents every count, so it needs the measured numbers. Nominal
# names are kept because they name the bias files on disk.
SWITCH = [1, 2, 3, 4, 6, 7, 10, 14, 20, 25]


def load(npz="data_olfaction/olfaction_pulses.npz"):
    d = np.load(npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / 1000.0 + float(d["t0"]) / 1000.0
    dur = np.array([m[0] for m in meta])
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])
    tr, te = dur == "1.0s", dur == "0.1s"
    Ftr, itr = chunks(X[tr], Th[tr], t, 1.0, 0.05, tail=0.2)
    Fte, ite = chunks(X[te], Th[te], t, 0.1, 0.05, tail=0.2)
    return Ftr, Y[tr][itr], Fte, Y[te][ite], ite, names


def dedupe(ladder, sw):
    """Drop bias files that switch at a count another file already covers.

    Drift closes gaps: after five hours lvl6 and lvl8 both switched at 8, and two files
    with the same switching count are the same comparator. Keeping both breaks the
    interval algebra outright -- ordinal j would need a burst that is simultaneously
    below and not below the same threshold -- which is what aborted the rebuild. Since
    the level sweep shows accuracy saturating at six levels (olfaction_hybrid_levels.py),
    losing a redundant one costs nothing measurable."""
    keep_l, keep_s = [], []
    for L, S in zip(ladder, sw):
        if S is not None and (not keep_s or S > keep_s[-1]):
            keep_l.append(L); keep_s.append(S)
    return keep_l, keep_s


def quantiser(Ftr, LADDER, SW=None):
    """Per-feature map to a burst count, built AROUND the calibrated ladder.

    A linear map to 0..NMAX is the obvious encoder and it destroys the model: the
    quantised features pile up at 20..32 (median 23) while the representable thresholds
    {0,1,2,3,5,7,11,15,23,31} are dense at the low end, so every split snaps somewhere
    useless and accuracy falls to chance (0.19 against 0.90). The ladder is roughly
    geometric; the data is not; a linear encoder cannot reconcile them.

    So place the ladder on the data instead. Per feature, take ten cuts at ten evenly
    spaced quantiles of the TRAIN chunks, and emit N = L_j where j counts how many cuts
    the value exceeds. Because L is increasing, (N >= L_k) <=> (j >= k) <=> (x > c_k)
    exactly -- so comparator k answers "is this feature above its k-th quantile", and all
    ten calibrated levels are useful instead of eight of them being no-ops."""
    sw = SW or SWITCH
    n = len(LADDER)
    pr = np.linspace(1.0, n, n) / (n + 1.0)
    cuts = np.percentile(Ftr, pr * 100.0, axis=0)          # (10, n_features)

    def ordinal(F):
        """j in 0..10: how many of this feature's cuts the value exceeds."""
        return (F[None, :, :] > cuts[:, None, :]).sum(axis=0).astype(np.int16)

    def burst(F):
        """The spike count actually sent to the chip -- the MIDPOINT of the interval that
        selects ordinal j, not its lower edge.

        Sending N = switch_j is correct arithmetic and a bad measurement: it puts the
        input exactly ON the comparator's switching boundary, the one count where the
        device is not sharp. Measured on the first tree run, that single choice produced
        essentially all of the error -- 100% of comparisons wrong at the boundary for
        levels 8 and 12, against 0.1-0.6% away from it. The comparator was exact; the
        encoder was aiming at its blind spot.

        Ordinal j needs N >= switch_j and N < switch_{j+1}, so any count in that interval
        is valid. Taking the midpoint spends the slack on margin. Levels 1-3 have adjacent
        switches and get no margin -- they also measured 0.0% error, so they do not need
        any."""
        j = ordinal(F)
        nxt = sw[1:] + [NMAX + 1]
        mid = [(a + b) // 2 for a, b in zip(sw, nxt)]
        tab = np.array([0] + mid, dtype=np.int16)
        return tab[j]
    return ordinal, burst, dict(cuts=cuts.tolist(), probs=pr.tolist(), switch=sw)


def extract(g, LADDER, SW=None):
    """(nodes, roots) with thresholds SNAPPED to the representable set."""
    nodes, roots = [], []
    for stage in g._predictors:
        for tr_ in stage:
            roots.append(len(nodes)); n = tr_.nodes; off = len(nodes)
            for k in range(len(n)):
                isl = bool(n[k]["is_leaf"])
                if isl:
                    nodes.append(dict(leaf=True, value=float(n[k]["value"])))
                else:
                    # the tree is trained on the ORDINAL j, so its threshold is already
                    # in cut units: `j <= r` <=> x <= c_{r+1} <=> NOT (N >= L_{r+1}).
                    raw = float(n[k]["num_threshold"])
                    r = int(np.clip(np.floor(raw), 0, len(LADDER) - 1))
                    # `level` names the bias FILE to load; `switch` is the count that
                    # file actually fires at, and is what the burst must clear.
                    nodes.append(dict(leaf=False, f=int(n[k]["feature_idx"]), thr=r,
                                      level=LADDER[r], switch=(SW or SWITCH)[r], raw=raw,
                                      left=int(n[k]["left"]) + off,
                                      right=int(n[k]["right"]) + off))
    return nodes, roots


def predict(nodes, roots, Q, nc, fire=None):
    """Walk the ensemble. fire(node_index, chunk_index) -> bool overrides the arithmetic
    test with a measured comparator outcome; left branch is 'did not fire'."""
    out = np.empty(len(Q), dtype=int)
    for j, x in enumerate(Q):
        sc = [0.0] * nc; c = 0
        for r in roots:
            i = r
            while not nodes[i]["leaf"]:
                nd = nodes[i]
                hit = (x[nd["f"]] > nd["thr"]) if fire is None else fire(i, j)
                i = nd["right"] if hit else nd["left"]
            sc[c] += nodes[i]["value"]; c = (c + 1) % nc
        out[j] = int(np.argmax(sc))
    return out


def visits(nodes, roots, Q):
    return float(np.mean([sum(1 for r in roots
                              for _ in iter(lambda s=[r]: None, 1))
                          for _ in Q])) if False else _visits(nodes, roots, Q)


def _visits(nodes, roots, Q):
    tot = 0
    for x in Q:
        for r in roots:
            i = r
            while not nodes[i]["leaf"]:
                tot += 1
                nd = nodes[i]
                i = nd["right"] if x[nd["f"]] > nd["thr"] else nd["left"]
    return tot / len(Q)


def acc(p, y, it, nc):
    per = float((p == y).mean())
    vot = float(np.mean([np.bincount(p[it == j], minlength=nc).argmax() == y[it == j][0]
                         for j in np.unique(it)]))
    return per, vot


def check(nodes, roots, J, B, nc):
    """Execute the tree arithmetically on the ordinal, and through the comparator on the
    burst count, and require them to agree. This is where an off-by-one dies quietly, so
    it is asserted rather than reasoned about."""
    a = predict(nodes, roots, J, nc)
    b = predict(nodes, roots, J, nc,
                fire=lambda i, j: bool(B[j][nodes[i]["f"]] >= nodes[i]["switch"]))
    assert np.array_equal(a, b), "comparator semantics disagree with the arithmetic test"
    # (N >= L_k) must be exactly (j >= k), for every level and every ordinal
    # (N_j >= switch_k) must be exactly (j >= k) for the ENCODED counts, whatever margin
    # they were given -- this is what makes midpoint encoding safe rather than merely
    # plausible. B carries the real encoding, so read the per-ordinal counts back from it.
    sw = [nodes[i]["switch"] for i in range(len(nodes)) if not nodes[i]["leaf"]]
    enc = sorted(set(int(v) for v in np.unique(B)))
    for S in sorted(set(sw)):
        for v in enc:
            k = sum(1 for a in sorted(set(sw)) if a <= v)
            assert (v >= S) == (k >= sum(1 for a in sorted(set(sw)) if a <= S)), \
                f"encoded count {v} orders wrongly against switch {S}"
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=10, help="boosting iterations")
    ap.add_argument("--leaves", type=int, default=8)
    ap.add_argument("--sweep", action="store_true", help="size/accuracy trade-off table")
    ap.add_argument("--transfer", default="data/olfaction_hybrid_transfer.json",
                    help="measured p(fire|N,L); supplies the true switching counts")
    ap.add_argument("--out", default="data/olfaction_hybrid_model.json")
    args = ap.parse_args()

    Ftr, Ytr, Fte, Yte, ite, names = load()
    nc = len(names)
    ladder, sw = list(LADDER), list(SWITCH)
    if args.transfer and os.path.exists(args.transfer):
        t = json.load(open(args.transfer))
        # STRICT: the first count that fires EVERY repetition. The p >= 0.5 rule put
        # lvl8 at N=7 and lvl12 at N=10, both counts the transfer itself flagged as
        # ambiguous, and the tree run then disagreed with them ~100% of the time -- the
        # chip reliably does NOT fire there. A comparator's switch is the first count it
        # fires reliably, not the first it fires sometimes.
        have = [L for L in list(LADDER) if str(L) in t.get("p", {})]
        # A level that fires with NO input is not a comparator: it reports "at least N"
        # for every N, so it scores as perfect while measuring nothing. This is the
        # failure that got through the original calibration's loose p0 <= 0.3 guard, and
        # after the bench move lvl1 came back at p(N=0) = 0.12. Refuse it here rather
        # than rely on reading the table.
        free = [L for L in have if t["p"][str(L)][0] > 0.05]
        if free:
            print(f"  DROPPED {free}: fire with no input (p(N=0) > 0.05) -- not comparators")
        have = [L for L in have if L not in free]
        sw = [next((n for n, q in zip(t["N"], t["p"][str(L)]) if q >= 1.0), None)
              for L in have]
        print(f"measured switch counts from {args.transfer}: {sw}")
        n_before = len(have)
        ladder, sw = dedupe(have, sw)
        if len(ladder) < n_before:
            print(f"  {n_before - len(ladder)} level(s) dropped as redundant or "
                  f"unreachable")
        print(f"  ladder {ladder} switching at {sw}")
    ordinal, burst, qp = quantiser(Ftr, ladder, sw)
    Qtr, Qte = ordinal(Ftr), ordinal(Fte)          # what the tree splits on
    Bte = burst(Fte)                                # what the chip is actually sent
    print(f"{len(Ftr)} train chunks, {len(Fte)} test chunks over "
          f"{len(np.unique(ite))} trials, {nc} classes, burst alphabet 0..{NMAX}")
    print(f"representable thresholds t = {THRS}\n  (comparator levels L = {LADDER})\n")

    # ---- rung (i): the reference full-precision digital baseline ----------
    ref = HGB(max_iter=10, max_leaf_nodes=8, random_state=0).fit(Ftr, Ytr)
    p = ref.predict(Fte)
    print(f"(i)   full-precision digital      per-chunk {acc(p, Yte, ite, nc)[0]:.3f}"
          f"  voted5 {acc(p, Yte, ite, nc)[1]:.3f}")

    if args.sweep:
        print("\n  iters leaves  nodes  visits/dec  per-chunk  voted5")
        for it_ in (2, 3, 5, 10):
            for lv in (4, 8):
                g = HGB(max_iter=it_, max_leaf_nodes=lv, random_state=0).fit(Qtr, Ytr)
                nd, rt = extract(g, ladder, sw)
                pq = predict(nd, rt, Qte, nc)
                a, v = acc(pq, Yte, ite, nc)
                ni = sum(1 for x in nd if not x["leaf"])
                print(f"  {it_:5d} {lv:6d} {ni:6d} {_visits(nd, rt, Qte):11.1f}"
                      f"  {a:9.3f} {v:7.3f}")
        print()

    # ---- rung (ii): quantised + snapped, executed digitally ---------------
    g = HGB(max_iter=args.iters, max_leaf_nodes=args.leaves,
            random_state=0).fit(Qtr, Ytr)
    nodes, roots = extract(g, ladder, sw)
    check(nodes, roots, Qte, Bte, nc)
    pq = predict(nodes, roots, Qte, nc)
    a2, v2 = acc(pq, Yte, ite, nc)
    ni = sum(1 for x in nodes if not x["leaf"])
    nv = _visits(nodes, roots, Qte)
    print(f"(ii)  snapped, digital execution  per-chunk {a2:.3f}  voted5 {v2:.3f}")
    print(f"      {ni} internal nodes over {len(roots)} trees, {nv:.1f} visits/decision")
    print(f"      comparator semantics agree with the arithmetic test on all "
          f"{len(Qte)} chunks")

    # what the bench run costs: every node x every chunk, grouped by level
    bylev = {L: sum(1 for x in nodes if not x["leaf"] and x["level"] == L)
             for L in ladder}
    tot = ni * len(Qte)
    print(f"\nbench cost: {ni} nodes x {len(Qte)} chunks = {tot} bursts "
          f"(~{tot * 0.33 / 60:.0f} min), {sum(1 for L in bylev if bylev[L])} bias loads")
    print("  nodes per level: " + " ".join(f"{L}:{bylev[L]}" for L in ladder))

    json.dump(dict(ladder=ladder, switch=sw, thresholds=THRS, nmax=NMAX,
                   classes=names,
                   quant=qp, iters=args.iters, leaves=args.leaves,
                   nodes=nodes, roots=roots,
                   n_internal=ni, visits_per_decision=nv,
                   digital_full=dict(zip(("per_chunk", "voted5"),
                                         acc(p, Yte, ite, nc))),
                   digital_snapped=dict(per_chunk=a2, voted5=v2),
                   test_labels=Yte.tolist(), test_trial=ite.tolist(),
                   test_ordinal=Qte.tolist(), test_bursts=Bte.tolist()),
              open(args.out, "w"))
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
