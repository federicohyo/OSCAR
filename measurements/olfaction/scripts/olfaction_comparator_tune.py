#!/usr/bin/env python3
"""Calibrate the spike-count comparator ladder on n14, scope-in-the-loop.

WHY THE SEARCH AXIS IS JExc AND NOT vleakn (2026-08-16). Both knobs move the switching
count, in a different way: vleakn sets where the membrane rests relative to threshold,
JExc sets how much each input spike climbs, i.e. the RAMP STEEPNESS. Bisecting vleakn
alone -- the first thing I did -- makes one knob cover the whole ladder, and the low
levels then land within half a millivolt of the free-run edge, where they overlap
(0.2563 read N>=3 and then N>=4 on a repeat). The measured map says it plainly:
at vleakn 0.2587, dJExc 0 -> N>=24, +5 mV -> N>=3, +10 mV -> N>=1. The same five levels
that vleakn crushed into 0.5 mV are spread over 5 mV of JExc, and p(fire | N=0) stayed
0.00 at every one of them -- the free-run edge is set by vleakn alone. So: park vleakn a
safe 2 mV above the edge and place the levels along JExc, using vleakn only for the top
of the ladder, where dJExc has run out of room at zero.

A free-running neuron fires at N=1 and so scores as a perfect comparator. That is why
the edge is measured first, and why a SAVED level demands p(N=0) == 0.00 exactly and
p(target) == 1.00; the loose p0 <= 0.3 classifier is for the sweep only, and it has
already let a free-running point through once.

OPERATING CONDITION. A .biases file alone does NOT reproduce the comparator: it is
calibrated against synapse 0 at weight 15, excitatory, routed to the neuron, driven by
BURST (firmware-paced, spikes back to back roughly a microsecond apart) at the firmware's
default input-pulse width. The leak means N spikes spread over a longer window integrate
less, so N* is a count AT THIS PACING rather than a pacing-independent counter. Reload the file
and set the same route, or the switching count departs from the label. It is
recorded in the results JSON alongside the levels.

SCOPE. Federico's standing rule, and here it is also the mechanism panel: AER says only
that threshold was crossed, the membrane shows the staircase climbing to it. Both are
recorded at every (point, N).

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_comparator_tune.py
"""
import argparse, json, os, random, time
import numpy as np

from meas_common import BridgeSession, load_biases
from olfaction_bias_bo import AERLatch, aer_scan
from olfaction_graded_hunt import Scope

LEV = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]
JK = [f"JExcWn{j}" for j in range(4)]


def biasfor(base, vleakn, djexc):
    bi = dict(base)
    bi["vleakn"] = round(vleakn, 5)
    for k in JK:
        if k in bi:
            bi[k] = round(bi[k] + djexc, 5)
    return bi


def setup(b, k, bi):
    b.apply_biases(bi); b.monitor(k); time.sleep(0.85)
    b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)


def sparkline(sc, t0, n=28):
    """The membrane over the burst window, as one line of text.

    A scalar peak says how high it got; the shape says WHY -- whether the ramp is a
    staircase climbing to threshold, a single saturating jump, or a flat line. That is
    the difference between a knob that is working and one that is off, and it stays
    invisible in p(fire) at all."""
    a = np.array(sc.s)
    if len(a) < 8:
        return "", float("nan")
    w = a[(a[:, 0] >= t0 - 0.05) & (a[:, 0] < t0 + 0.30)]
    if len(w) < 8:
        return "", float("nan")
    y = w[:, 1] * 1000.0
    base = float(np.median(y[:max(3, len(y) // 8)]))
    y = y - base
    hi = max(float(np.max(y)), 1.0)
    b = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"
    idx = np.linspace(0, len(y), n + 1).astype(int)
    out = "".join(b[min(7, max(0, int(np.max(y[i:j]) / hi * 7)))] if j > i else " "
                  for i, j in zip(idx[:-1], idx[1:]))
    return out, float(np.max(y))


def pf(b, sc, k, n, reps, wait, echo=False, keep=None):
    """p(fire) plus the membrane excursion, for one burst size.

    `keep`: a list to append the RAW record of every repetition to -- burst size, the AER
    counts across all 16 neurons, and the membrane window itself. The decision path is
    unchanged; this only exposes what it already measured, so a reference result can be
    re-derived from the traces rather than from this function's summary of them."""
    g, mv, spark = 0, [], ""
    for _ in range(reps):
        b.drain(max_lines=100000)
        t0 = time.time()
        if n > 0:
            b.send(f"BURST {n}")
        time.sleep(wait)
        c = [0] * 16
        for _ in range(3):
            b.drain(c); time.sleep(0.02)
        fired = c[k] > 0
        g += 1 if fired else 0
        if sc is not None:
            sp, pk = sparkline(sc, t0)
            mv.append(pk)
            if keep is not None:
                a = np.array(sc.s)
                w = a[(a[:, 0] >= t0 - 0.05) & (a[:, 0] < t0 + 0.30)] if len(a) else a
                keep.append(dict(n=n, fired=int(fired), counts=list(c), peak_mv=pk,
                                 t0=t0,
                                 t=(w[:, 0] - t0).astype(np.float32) if len(w) else
                                 np.zeros(0, np.float32),
                                 v=(w[:, 1] * 1000.0).astype(np.float32) if len(w) else
                                 np.zeros(0, np.float32)))
            if echo and not spark:
                spark = f"  N={n:<3d}|{sp}| {pk:5.0f} mV {'FIRE' if fired else '    '}"
            del sc.s[:-40000]
    if echo and spark:
        print(spark)
    v = [x for x in mv if x == x]
    return g / reps, (float(np.median(v)) if v else float("nan"))


def probe(b, sc, k, reps, wait, seed=0, echo=False):
    p0, v0 = pf(b, sc, k, 0, reps, wait, echo)
    order = random.Random(seed).sample(LEV, len(LEV))   # reshuffled: order was fixed
    r = {n: pf(b, sc, k, n, reps, wait, echo) for n in order}
    return p0, v0, [r[n][0] for n in LEV], [r[n][1] for n in LEV]


def show(tag, p0, ps, vs):
    sw = next((n for n, q in zip(LEV, ps) if q >= 0.5), None)
    lab = "free-runs" if p0 > 0.3 else (f"N>={sw}" if sw else "never")
    print(f"{tag} | {p0:5.2f} " + " ".join(f"{q:4.2f}" for q in ps) + f" | {lab}")
    print(f"{' '*len(tag)} | {'mV':>5} " + " ".join(f"{v:4.0f}" for v in vs))
    return sw


def center(trace, n):
    """Deepest point inside level n's plateau: p(n)=1, p(prev)=0, p0=0, widest margin.

    The greedy first-crossing pick lands on the plateau EDGE (level 12 was saved at
    p=0.88). Sweeping first and choosing offline costs no extra bench time."""
    i = LEV.index(n)
    ok = [t for t in trace
          if t["p0"] == 0.0 and t["p"][i] == 1.0
          and (i == 0 or t["p"][i - 1] == 0.0)]
    if not ok:
        return None
    return max(ok, key=lambda t: sum(t["p"][i:]) - sum(t["p"][:i]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--base", default="ofxCaravanViewer/bin/ramp_comparator_fed.biases")
    ap.add_argument("--vleakn", type=float, default=0.2582, help="parked, 2 mV above edge")
    ap.add_argument("--reps", type=int, default=6)
    ap.add_argument("--djexc-lo", type=float, default=-4.0,
                    help="mV. Floor of the JExc sweep. Was -1.0, which assumed n14's "
                         "excitability on 2026-08-16; after the bench move the same "
                         "neuron fires 2 counts earlier, and a floor that is too high "
                         "puts the whole ladder at N>=1 with nowhere to go. The same "
                         "hard-coded floor is why n5/n11/n2 each yielded one level.")
    ap.add_argument("--djexc-hi", type=float, default=10.0)
    ap.add_argument("--coarse-lo", type=float, default=-16.0,
                    help="mV. Floor of the COARSE bracketing scan. Wide on purpose: "
                         "mismatch moves a neuron's usable JExc window by many mV, and "
                         "the window is found rather than assumed.")
    ap.add_argument("--vreps", type=int, default=10, help="reps in the verify pass")
    ap.add_argument("--wait", type=float, default=0.25,
                    help="post-burst settle; 0.12 gave a systematic 0.88 at N=24")
    ap.add_argument("--outdir", default="ofxCaravanViewer/bin")
    ap.add_argument("--out", default="data/olfaction_comparator_tune.json")
    ap.add_argument("--verify-only", action="store_true",
                    help="reload the placed .biases files and re-probe the ladder "
                         "(~4 min). The levels sit 0.5-1 mV apart in weak inversion, so "
                         "whether the calibration survives a power cycle or a day of "
                         "drift is unmeasured -- run this before trusting the files.")
    args = ap.parse_args()
    k, base = args.neuron, load_biases(args.base)
    rec = {"neuron": k, "base": args.base, "vleakn_park": args.vleakn,
           "wait": args.wait, "levels": LEV,
           # what the .biases files leave out, needed for the comparator to work
           "operating_point": {"synapse": 0, "weight": 15, "exc": True, "route_to": k,
                               "drive": "BURST (firmware-paced, ~1 us inter-spike)",
                               "pulse_width": "firmware default pulse_mult",
                               "clk_mhz": int(os.environ.get("CARAVAN_CLK_MHZ", 25)),
                               "mask": f"MASK {1 << k}"}}
    sc = Scope()
    print(f"scope live on /dev/ttyACM0 ({len(sc.s)} samples buffered)")

    if args.verify_only:
        old = json.load(open(args.out))
        with BridgeSession() as b:
            b.send(f"MASK {1 << k}")
            print(f"{'  level':>16} | {'N=0':>5} " + " ".join(f"{n:>4}" for n in LEV)
                  + " | level")
            bad = []
            for n in sorted(map(int, old["placed"])):
                setup(b, k, load_biases(old["placed"][str(n)]["path"]))
                p0, v0, ps, vs = probe(b, sc, k, args.vreps, args.wait, seed=200 + n)
                if show(f"{('N>='+str(n)):>16}", p0, ps, vs) != n or p0 != 0.0:
                    bad.append(n)
        sc.stop()
        print(f"\n{'all levels hold' if not bad else 'DRIFTED: ' + str(bad)}")
        return 1 if bad else 0

    with BridgeSession() as b:
        ok, det, _ = aer_scan(b, list(range(16)), {j: base for j in range(16)}, "before")
        rec["aer_before"] = det
        if not ok:
            raise AERLatch(det)
        b.send(f"MASK {1 << k}")

        # ---- step 1: the free-run edge (vleakn only) ------------------------
        print("\nstep 1: free-run edge")
        lo, hi = 0.2500, 0.2650
        for _ in range(6):
            v = 0.5 * (lo + hi)
            setup(b, k, biasfor(base, v, 0.0))
            p0, mv = pf(b, sc, k, 0, args.reps, args.wait, echo=True)
            print(f"  vleakn {v:.4f}  N=0 {p0:.2f}  vmem {mv:5.0f} mV"
                  + ("  free-runs" if p0 > 0.3 else ""))
            lo, hi = (v, hi) if p0 > 0.3 else (lo, v)
        rec["free_run_edge"] = hi
        park = max(args.vleakn, hi + 0.002)
        print(f"  edge {hi:.4f}; parking vleakn at {park:.4f}")

        trace = []

        def sweep(pts, tag):
            print(f"\n{tag}\n{'  point':>16} | {'N=0':>5} "
                  + " ".join(f"{n:>4}" for n in LEV) + " | level")
            for i, (v, dj) in enumerate(pts):
                setup(b, k, biasfor(base, v, dj))
                print(f"  --- vleakn {v:.4f}  dJExc {dj*1000:+.1f} mV "
                      "(membrane over the burst window) ---")
                p0, v0, ps, vs = probe(b, sc, k, args.reps, args.wait, seed=i, echo=True)
                lbl = f"{v:.4f} {dj*1000:+5.1f}"
                show(f"{lbl:>16}", p0, ps, vs)
                trace.append(dict(vleakn=v, djexc=dj, p0=p0, vmem0=v0, p=ps, vmem=vs))
                rec["trace"] = trace
                json.dump(rec, open(args.out, "w"), indent=2)

        # ---- step 2a: find the JExc window this neuron needs ----------------
        # Mismatch moves the usable window by many millivolts between neurons, and a
        # hard-coded range is why n5/n11/n2 each yielded a single level: at every setting
        # in n14's window they already fired at N=1, so the fine sweep had nothing to
        # resolve. Bracket coarsely first, then sweep finely only where levels exist.
        print(f"\nstep 2a: coarse scan for this neuron's JExc window "
              f"({args.coarse_lo:+.0f} to {args.djexc_hi:+.0f} mV)")
        print(f"{'  dJExc':>16} | {'N=0':>5} " + " ".join(f"{n:>4}" for n in LEV)
              + " | level")
        coarse = []
        for d in np.arange(args.coarse_lo, args.djexc_hi + 0.01, 2.0):
            setup(b, k, biasfor(base, park, d / 1000.0))
            p0, v0, ps, vs = probe(b, sc, k, 4, args.wait, seed=int(d))
            swc = show(f"{d:>16.1f}", p0, ps, vs)
            coarse.append((d, p0, swc))
        usable = [d for d, p0, swc in coarse if p0 <= 0.3 and swc is not None]
        if usable:
            lo_d = max(args.coarse_lo, min(usable) - 2.0)
            hi_d = min(args.djexc_hi, max(usable) + 2.0)
        else:
            lo_d, hi_d = args.coarse_lo, args.djexc_hi
            print("  no setting produced a placeable level; sweeping the whole range")
        rec["coarse"] = [dict(djexc=d, p0=p0, switch=swc) for d, p0, swc in coarse]
        print(f"  -> fine sweep {lo_d:+.1f} to {hi_d:+.1f} mV")

        # ---- step 2b: place the ladder along JExc ---------------------------
        sweep([(park, d / 1000.0) for d in np.arange(lo_d, hi_d + 0.01, 0.5)],
              "step 2b: JExc axis at parked vleakn (low/mid levels)")

        # ---- step 3: top of the ladder needs vleakn (dJExc is already 0) ----
        sweep([(v, 0.0) for v in np.arange(park, park + 0.0026, 0.0005)],
              "step 3: vleakn axis at dJExc=0 (top levels)")

        # ---- write the files from plateau centres ---------------------------
        print("\nplacing levels (plateau centres, p0 == 0.00 and p(N) == 1.00):")
        placed = {}
        for n in LEV:
            c = center(trace, n)
            if c is None:
                print(f"  N>={n:2d}: not placed")
                continue
            bi = biasfor(base, c["vleakn"], c["djexc"])
            path = os.path.join(args.outdir, f"comparator_n{k}_lvl{n}.biases")
            with open(path, "w") as f:
                f.write("{\n" + ",\n".join(f'  "{a}": {q}' for a, q in bi.items()) + "\n}\n")
            placed[n] = dict(vleakn=c["vleakn"], djexc=c["djexc"], path=path)
            print(f"  N>={n:2d}: vleakn {c['vleakn']:.4f} dJExc {c['djexc']*1000:+.1f} mV"
                  f"  -> {os.path.basename(path)}")
        rec["placed"] = {str(a): q for a, q in placed.items()}

        # ---- verify: reload each file from disk, as the tree will ------------
        print("\nverify (files reloaded from disk):")
        print(f"{'  level':>16} | {'N=0':>5} " + " ".join(f"{n:>4}" for n in LEV) + " | level")
        ver = {}
        for n, q in placed.items():
            setup(b, k, load_biases(q["path"]))
            print(f"  --- verify N>={n} ---")
            p0, v0, ps, vs = probe(b, sc, k, args.vreps, args.wait,
                                   seed=100 + n, echo=True)
            sw = show(f"{('N>='+str(n)):>16}", p0, ps, vs)
            ver[str(n)] = dict(p0=p0, p=ps, vmem=vs, switch=sw, ok=(sw == n and p0 == 0.0))
        rec["verify"] = ver

        ok, det, _ = aer_scan(b, list(range(16)), {j: base for j in range(16)}, "after")
        rec["aer_after"] = det
    sc.stop()
    json.dump(rec, open(args.out, "w"), indent=2)
    good = [n for n in placed if ver[str(n)]["ok"]]
    print(f"\nplaced {sorted(placed)}; verified {sorted(good)}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
