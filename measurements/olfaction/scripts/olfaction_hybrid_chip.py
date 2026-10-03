#!/usr/bin/env python3
"""Execute the hybrid tree on silicon: every node comparison is a real burst into one
time-multiplexed analog neuron.

WHAT IS ANALOG AND WHAT IS DIGITAL. Each node test is performed by neuron 14 acting as a
spike-count comparator: the feature's burst is presented, and the neuron's own membrane
decides the branch. The routing between visits -- which node next, which leaf value to
accumulate -- is digital, exactly as the architecture intends (6.15: conditionality is
free in software, integration is what the array is for). The routing runs on the HOST
rather than the core for one hard reason: the RISC-V cannot program the bias DACs
([[host-owns-the-bias-dacs-not-the-core]]), and a comparator's threshold IS a bias, so
threshold switching runs off-core on this die. That is an architectural finding
about this chip rather than a shortcut -- the per-visit routing cost is separately measured
(532 cycles) so the energy accounting is unaffected.

ONE NEURON, TIME-MULTIPLEXED. n14 is the calibrated one, so it serves every node in turn.
The accuracy claim is unaffected (each comparison is physically performed); the energy
projection assumes 16 neurons working in parallel and is stated as such.

EXECUTION ORDER. Grouped by threshold level rather than by chunk: a bias load costs ~0.9 s and a
burst ~0.3 s, so walking chunk-major would spend the entire run switching biases. Every
node is evaluated on every chunk and the tree is walked afterwards from the measured
outcomes -- the same comparisons, in a cache-friendly order.

    # transfer matrix first: the tree presents counts outside what the ladder calibration probed
    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_hybrid_chip.py --transfer
    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_hybrid_chip.py --tree
"""
import argparse, json, os, time
import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from olfaction_bias_bo import AERLatch, aer_scan
from olfaction_comparator_tune import LEV, pf, probe, setup, show
from olfaction_hybrid_model import LADDER as FULL_LADDER
from olfaction_graded_hunt import Scope

BIAS = "ofxCaravanViewer/bin/comparator_n14_lvl{L}.biases"


def archive(path, keep, levels, **extra):
    """Everything a reader needs to redo the analysis without the chip: every burst's AER
    counts across all 16 neurons, the sub-threshold membrane window that produced each
    decision, the bias files by content hash, the firmware image hash and the clock.

    Traces are ragged (the scope free-runs at ~1 kHz and a window catches whatever landed
    in it), so they are stored flat with an index rather than padded into a rectangle."""
    tl = [r["t"] for r in keep]
    off = np.cumsum([0] + [len(x) for x in tl])
    np.savez_compressed(
        path,
        burst_n=np.array([r["n"] for r in keep], np.int16),
        fired=np.array([r["fired"] for r in keep], np.int8),
        counts=np.array([r["counts"] for r in keep], np.int32),
        peak_mv=np.array([r["peak_mv"] for r in keep], np.float32),
        t0=np.array([r["t0"] for r in keep], np.float64),
        trace_t=np.concatenate(tl) if tl else np.zeros(0, np.float32),
        trace_v=np.concatenate([r["v"] for r in keep]) if keep else np.zeros(0, np.float32),
        trace_off=off.astype(np.int64),
        bias_levels=np.array(levels),
        **provenance(bias_files=[BIAS.format(L=L) for L in levels],
                     task="olfaction_hybrid", **extra))
    print(f"  archived {len(keep)} bursts + traces -> {path}")


def switch_now(b, sc, k, hint, reps, wait):
    """The count this level ACTUALLY switches at, right now.

    A single before/after ladder check tells you drift happened, leaving its timing open, and run 1
    drifted on three of ten levels over five hours. Bracketing each level's node group
    turns that into a measured, attributable quantity for ~9 s per call: if a level moved
    while its own nodes were being evaluated, its comparisons are the suspect ones and
    the rest of the run is untouched."""
    ns = list(range(max(0, hint - 3), min(32, hint + 4) + 1))
    ps = [pf(b, sc, k, n, reps, wait)[0] for n in ns]
    sw = next((n for n, q in zip(ns, ps) if q >= 1.0), None)
    return sw, {str(n): q for n, q in zip(ns, ps)}


def verify(b, sc, k, levels, reps, wait, tag):
    """Re-probe the placed files. The levels sit 0.5-1 mV apart in weak inversion, so
    'did the ladder still hold' is a question with a real answer on each side of a run."""
    print(f"\nladder check ({tag}):")
    print(f"{'  level':>16} | {'N=0':>5} " + " ".join(f"{n:>4}" for n in LEV) + " | level")
    bad = []
    for L in levels:
        setup(b, k, load_biases(BIAS.format(L=L)))
        p0, v0, ps, vs = probe(b, sc, k, reps, wait, seed=300 + L)
        if show(f"{('N>='+str(L)):>16}", p0, ps, vs) != L or p0 != 0.0:
            bad.append(L)
    print(f"  {'all levels hold' if not bad else 'DRIFTED: ' + str(bad)}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="data/olfaction_hybrid_model.json")
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--wait", type=float, default=0.25, help="the calibrated pacing")
    ap.add_argument("--transfer", action="store_true",
                    help="measure p(fire | N, L) over ALL N in 0..32, beyond the ladder")
    ap.add_argument("--treps", type=int, default=4)
    ap.add_argument("--tree", action="store_true", help="execute the tree on chip")
    ap.add_argument("--nodes", type=int, default=0, help="cap nodes (0 = all)")
    ap.add_argument("--trace-every", type=int, default=10,
                    help="keep the full membrane window every Nth burst. Per-burst AER "
                         "counts, fired flag and peak are kept for ALL bursts; the raw "
                         "windows are ~2 kB each and 52k of them is a 60 MB artefact, so "
                         "the waveforms are sampled and the decisions are not.")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    k = args.neuron
    m = json.load(open(args.model))
    # The transfer always probes EVERY bias file on disk rather than the model's ladder. The
    # model's ladder may already have levels pruned as redundant, and that prune came
    # from an OLDER transfer -- inheriting it makes pruning a RATCHET, so a level that
    # drifted into a duplicate yesterday would be measured just once even after it
    # drifted back apart. Run 3's first attempt silently probed nine levels for exactly
    # this reason. The tree mode is different and must use the model's ladder, because
    # that is what the encoding was built from.
    LADDER = FULL_LADDER if args.transfer else m["ladder"]
    sc = Scope()
    print(f"scope live on /dev/ttyACM0 ({len(sc.s)} samples buffered)")

    if args.transfer:
        out = args.out or "data/olfaction_hybrid_transfer.json"
        NS = list(range(0, m["nmax"] + 1))
        rec = {"neuron": k, "levels": LADDER, "N": NS, "reps": args.treps}
        with BridgeSession() as b:
            b.send(f"MASK {1 << k}")
            P, keep = {}, []
            print(f"\ntransfer matrix: {len(LADDER)} levels x {len(NS)} counts "
                  f"x {args.treps} reps")
            # A level whose bias file was pruned off disk was placed but stopped at
            # verification, so it stays off the ladder. Skip it and move on:
            # after the bench move only 6 of 10 verified, and six is the count at which
            # accuracy saturates anyway (olfaction_hybrid_levels.py).
            LADDER = [L for L in LADDER if os.path.exists(BIAS.format(L=L))]
            rec["levels"] = LADDER
            print(f"  ladder present on disk: {LADDER}")
            for L in LADDER:
                setup(b, k, load_biases(BIAS.format(L=L)))
                row = [pf(b, sc, k, n, args.treps, args.wait, keep=keep)[0]
                       for n in NS]
                P[str(L)] = row
                print(f"  L={L:<3d} " + "".join("#" if q >= 0.5 else "." for q in row)
                      + f"  switches at N={next((n for n, q in zip(NS, row) if q >= 0.5), None)}")
                rec["p"] = P
                json.dump(rec, open(out, "w"), indent=2)
            rec["switch_measured"] = {
                str(L): next((n for n, q in zip(NS, P[str(L)]) if q >= 0.5), None)
                for L in LADDER}
            json.dump(rec, open(out, "w"), indent=2)
            archive(out.replace(".json", "_raw.npz"), keep, LADDER, mode="transfer")
        sc.stop()
        print(f"\nwrote {out}")
        return 0

    if not args.tree:
        print("nothing to do: pass --transfer or --tree"); return 2

    out = args.out or "data/olfaction_hybrid_chip.json"
    nodes, B = m["nodes"], np.array(m["test_bursts"], dtype=int)
    inter = [i for i, n in enumerate(nodes) if not n["leaf"]]
    if args.nodes:
        inter = inter[:args.nodes]
    # HIGHEST level first. The drift measured between two transfer matrices five hours
    # apart is confined to the upper ladder -- levels 1-4 held steady, while 16,
    # 24 and 32 moved by 3, 5 and 2 counts. Whatever the cause, the encoding is built
    # from a transfer taken just before the run, so it is most accurate at the start.
    # Spending that accuracy on the levels that actually move, rather than on the four
    # that are stable either way, costs nothing and is strictly better than ascending.
    used = sorted({nodes[i]["level"] for i in inter}, reverse=True)
    nch = len(B)
    print(f"\n{len(inter)} internal nodes x {nch} chunks = {len(inter)*nch} bursts "
          f"over {len(used)} levels {used}")
    print(f"estimated {len(inter)*nch*(args.wait+0.08)/3600:.1f} h")

    fire = np.full((len(nodes), nch), -1, dtype=np.int8)
    keep = []
    rec = {"neuron": k, "model": args.model, "wait": args.wait, "levels_used": used}
    t0 = time.time()
    with BridgeSession() as b:
        ok, det, _ = aer_scan(b, list(range(16)),
                              {j: load_biases(BIAS.format(L=min(used)))
                               for j in range(16)}, "before")
        rec["aer_before"] = det
        if not ok:
            raise AERLatch(det)
        b.send(f"MASK {1 << k}")
        rec["ladder_before"] = verify(b, sc, k, used, 6, args.wait, "before")

        track = {}
        rec["switch_track"] = track
        for L in used:
            setup(b, k, load_biases(BIAS.format(L=L)))
            grp = [i for i in inter if nodes[i]["level"] == L]
            hint = next(nodes[i]["switch"] for i in grp)
            s0, p0v = switch_now(b, sc, k, hint, 4, args.wait)
            track[str(L)] = dict(expected=hint, before=s0, p_before=p0v)
            print(f"  L={L:<3d} switch before group: {s0} (model assumes {hint})"
                  + ("" if s0 == hint else "   <-- ALREADY OFF"))
            for c, i in enumerate(grp):
                f = nodes[i]["f"]
                for j in range(nch):
                    p, _ = pf(b, sc, k, int(B[j][f]), 1, args.wait, keep=keep)
                    if len(keep) % args.trace_every:
                        keep[-1]["t"] = keep[-1]["t"][:0]
                        keep[-1]["v"] = keep[-1]["v"][:0]
                    fire[i, j] = int(p >= 0.5)
                el = time.time() - t0
                done = int((fire >= 0).sum())
                print(f"  L={L:<3d} node {i:4d} ({c+1}/{len(grp)})  feat {f:3d}  "
                      f"fired {int(fire[i].sum()):3d}/{nch}   "
                      f"{done}/{len(inter)*nch} bursts, {el/60:.0f} min elapsed",
                      flush=True)
                np.savez(out.replace(".json", ".npz"), fire=fire,
                         nodes_done=np.array(sorted(set(inter[:inter.index(i)+1]))))
                json.dump(rec, open(out, "w"), indent=2)
            s1, p1v = switch_now(b, sc, k, hint, 4, args.wait)
            track[str(L)].update(after=s1, p_after=p1v)
            print(f"  L={L:<3d} switch after  group: {s1}"
                  + ("" if s1 == track[str(L)]["before"] else
                     f"   <-- DRIFTED during this group ({track[str(L)]['before']} -> {s1})"))
            json.dump(rec, open(out, "w"), indent=2)

        rec["ladder_after"] = verify(b, sc, k, used, 6, args.wait, "after")
        ok, det, _ = aer_scan(b, list(range(16)),
                              {j: load_biases(BIAS.format(L=min(used)))
                               for j in range(16)}, "after")
        rec["aer_after"] = det
    sc.stop()
    np.savez(out.replace(".json", ".npz"), fire=fire, nodes_done=np.array(inter),
             node_level=np.array([nodes[i]["level"] for i in inter]),
             node_feature=np.array([nodes[i]["f"] for i in inter]),
             labels=np.array(m["test_labels"]), trial=np.array(m["test_trial"]),
             **provenance(bias_files=[BIAS.format(L=L) for L in used],
                          task="olfaction_hybrid_tree", model=args.model))
    archive(out.replace(".json", "_raw.npz"), keep, used, mode="tree")
    json.dump(rec, open(out, "w"), indent=2)
    print(f"\nwrote {out} and {out.replace('.json', '.npz')} "
          f"({(time.time()-t0)/60:.0f} min)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
