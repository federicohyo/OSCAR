#!/usr/bin/env python3
"""What accuracy is this array CAPABLE of on odour identity, as a function of operating
point -- in simulation, before spending bench time.

F. Corradi, 2026-08-13: "we just switched on the array, we did a very small calibration
and you already call accuracy is capped here. I would disagree because we
can make simulations in which the accuracy is higher and we can probably tune the bias
better." Correct, and this project already recorded the lesson: ECG accuracy moved
0.913 -> 0.700 on a 2.7x drive change alone ([[reservoir-results-are-operating-point-
dependent]]). The measured 0.647/0.833 is ONE operating point, chosen for liveness, never
tuned for this task.

STRUCTURE: anchor, then explore.
  1. ANCHOR. Find the sim parameters reproducing the measured chip point (~120 Hz mean,
     0.647 per-chunk / 0.833 voted). A simulator that cannot hit the measured point is
     not a credible guide anywhere else, so this gate comes first and is reported.
  2. EXPLORE. Sweep threshold / weight / membrane and synaptic time constants, and report
     accuracy against MEAN FIRING RATE -- because rate is the observable we can actually
     match on silicon by moving vleakn/vthrdn, so it is what makes a sim prediction
     actionable as a bias target.

Same encoder, same chunks, same grouped folds and same kernel read-out as the measured
comparison (olfaction_iso_compare.py), so numbers are directly comparable.

    PYTHONPATH=. ./.venv-meas/bin/python3 olfaction_sim_sweep.py
"""
import argparse, itertools, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from deff_physical_sim import build_jump, simulate
from olfaction_identity import chunks
from olfaction_iso_compare import kernel, vote_acc
from olfaction_run_array import encode

FS = 1000.0
MEAS = {"rate": 108.3, "per_chunk": 0.647, "voted5": 0.833}


def build(duration, theta, nneur, seed0=100, npz="data_olfaction/olfaction_pulses.npz"):
    d = np.load(npz, allow_pickle=True)
    X, Th, y, meta = d["X"], d["T"], d["y"], d["meta"]
    cls = [str(c) for c in d["classes"]]
    t = np.arange(X.shape[1]) / FS + float(d["t0"]) / 1000.0
    m = np.array([mm[0] for mm in meta]) == duration
    F, it = chunks(X[m], Th[m], t, float(duration.rstrip("s")), 0.05, tail=0.2)
    lab = np.array([{"b1": "Blank", "b2": "Blank"}.get(cls[k], cls[k]) for k in y])
    names = sorted(set(lab)); Y = np.array([names.index(v) for v in lab])[m][it]
    ev = []
    for k in range(nneur):
        w = np.random.default_rng(seed0 + k).normal(0, 1, 8)
        for j in range(len(F)):
            s = F[j].reshape(50, 8) @ w
            ev.append(encode((s - s.mean()) / (s.std() + 1e-9), theta))
    return ev, Y, it, len(F), names


def run_point(up, dn, nneur, nchunk, Y, it, T, folds, **kw):
    st = simulate(up, dn, T=T, **kw)
    sp = np.empty((nneur, nchunk), dtype=object)
    for k in range(nneur):
        for j in range(nchunk):
            sp[k, j] = np.asarray(st[k * nchunk + j])
    rate = np.mean([len(sp[k, j]) for k in range(nneur) for j in range(nchunk)]) / T
    K = np.nan_to_num(kernel(sp, T))
    pred = np.zeros(len(Y), dtype=int)
    for tr, te in folds:
        m = make_pipeline(StandardScaler(),
                          LogisticRegression(C=0.1, max_iter=5000, class_weight="balanced"))
        m.fit(K[tr], Y[tr]); pred[te] = m.predict(K[te])
    return rate, float((pred == Y).mean()), vote_acc(pred, Y, it, 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", default="0.1s")
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--neurons", type=int, default=16)
    ap.add_argument("--T", type=float, default=0.15)
    ap.add_argument("--repeats", type=int, default=1,
                    help="projection seeds; accuracy is reported mean +/- sd over them")
    ap.add_argument("--ratio", action="store_true",
                    help="sweep the inhibitory/excitatory weight ratio (fresh ground)")
    ap.add_argument("--wide", action="store_true",
                    help="bracket vth and w, which the refine grid pinned at its edges")
    ap.add_argument("--refine", action="store_true",
                    help="finer grid around the coarse optimum, tau_m past the edge")
    ap.add_argument("--out", default="data/olfaction_sim_sweep.json")
    args = ap.parse_args()

    nsteps = int(round(args.T / 0.001))
    seeds = [100 + 7919 * r for r in range(args.repeats)]
    UD = []
    for sd in seeds:
        ev, Y, it, nchunk, names = build(args.duration, args.theta, args.neurons, seed0=sd)
        UD.append(build_jump(ev, args.T, 0.001, nsteps))
    folds = list(GroupKFold(n_splits=5).split(np.zeros((len(Y), 1)), Y, it))
    print(f"{nchunk} chunks / {len(np.unique(it))} trials, {args.neurons} neurons, "
          f"{len(names)} classes, chance {1/len(names):.3f}")
    print(f"measured chip point: {MEAS['rate']:.0f} Hz, "
          f"{MEAS['per_chunk']:.3f} per-chunk, {MEAS['voted5']:.3f} voted5\n")

    if args.ratio:
        # w_exc == w_inh made UP/DOWN events cancel, capping the sim at ~42 Hz and
        # putting the chip's 108 Hz out of reach. Silicon relaxes this symmetry --
        # exc and inh efficacy differ on this die and the ratio is a real
        # bias knob (JExcWn vs JInhWp). Sweep it.
        grid = dict(vth=[0.35, 0.7], w=[0.5, 1.0], tau_m=[0.05, 0.1],
                    tau_syn=[0.0], inh=[0.0, 0.25, 0.5, 1.0])
    elif args.wide:
        # refine pinned BOTH vth (low) and w (high) at their edges -- bracket them
        grid = dict(vth=[0.2, 0.35, 0.5, 0.7], w=[0.5, 0.7, 1.0, 1.4],
                    tau_m=[0.05, 0.1, 0.2], tau_syn=[0.0])
    elif args.refine:
        # tau_m ran to the EDGE of the coarse grid, so push past it before believing it
        grid = dict(vth=[0.7, 1.0, 1.5], w=[0.2, 0.34, 0.5],
                    tau_m=[0.02, 0.05, 0.1, 0.2], tau_syn=[0.0])
    else:
        grid = dict(vth=[0.5, 1.0, 2.0, 4.0], w=[0.15, 0.34, 0.7],
                    tau_m=[0.005, 0.02, 0.05], tau_syn=[0.0, 0.005, 0.02])
    print(f"{'vth':>5} {'wexc':>5} {'inh/e':>5} {'tau_m':>6} {'rate Hz':>8} "
          f"{'per-chunk':>14} {'voted5':>14}")
    res, best = [], None
    grid.setdefault("inh", [1.0])
    for vth, w, tm, ts, ih in itertools.product(*[grid[k] for k in
                                                  ("vth", "w", "tau_m", "tau_syn", "inh")]):
        rr, pp, vv = [], [], []
        for (up, dn) in UD:
            r, pc, v5 = run_point(up, dn, args.neurons, nchunk, Y, it, args.T, folds,
                                  vth=vth, w_exc=w, w_inh=w * ih, tau_m=tm, tau_syn=ts,
                                  tref=0.005, rectify=False)
            rr.append(r); pp.append(pc); vv.append(v5)
        rec = dict(vth=vth, w=w, inh=ih, tau_m=tm, tau_syn=ts, rate=float(np.mean(rr)),
                   per_chunk=float(np.mean(pp)), per_chunk_sd=float(np.std(pp)),
                   voted5=float(np.mean(vv)), voted5_sd=float(np.std(vv)),
                   n_rep=len(UD))
        res.append(rec)
        if rec["rate"] > 1.0:
            print(f"{vth:5.1f} {w:5.2f} {ih:5.2f} {tm*1000:5.0f}m {rec['rate']:8.1f} "
                  f"{rec['per_chunk']:9.3f} +/-{rec['per_chunk_sd']:.3f} "
                  f"{rec['voted5']:9.3f} +/-{rec['voted5_sd']:.3f}")
        if best is None or rec["voted5"] > best["voted5"] or (
                rec["voted5"] == best["voted5"] and rec["per_chunk"] > best["per_chunk"]):
            best = rec
    anchor = min((x for x in res if x["rate"] > 1), key=lambda x: abs(x["rate"] - MEAS["rate"]))
    print(f"\nANCHOR (sim point nearest the measured {MEAS['rate']:.0f} Hz):")
    print(f"  {anchor['rate']:.0f} Hz -> {anchor['per_chunk']:.3f} / {anchor['voted5']:.3f}"
          f"   measured {MEAS['per_chunk']:.3f} / {MEAS['voted5']:.3f}")
    d_pc = anchor["per_chunk"] - MEAS["per_chunk"]
    print(f"  sim - measured = {d_pc:+.3f} per-chunk"
          + ("   CREDIBLE, sim tracks silicon here" if abs(d_pc) <= 0.10
             else "   NOT credible: sim does not reproduce the measured point,"
                  " treat the sweep as indicative only"))
    print(f"\nBEST simulated point: vth={best['vth']} w={best['w']} "
          f"tau_m={best['tau_m']*1000:.0f}ms tau_syn={best['tau_syn']*1000:.0f}ms")
    print(f"  {best['rate']:.0f} Hz -> {best['per_chunk']:.3f} +/- {best['per_chunk_sd']:.3f}"
          f" per-chunk, {best['voted5']:.3f} +/- {best['voted5_sd']:.3f} voted5"
          f"  (n={best['n_rep']} projection seeds)")
    edge = (best["tau_m"] == max(grid["tau_m"])
            or best["vth"] in (min(grid["vth"]), max(grid["vth"]))
            or best["w"] in (min(grid["w"]), max(grid["w"])))
    if edge:
        print("  WARNING: optimum sits on a grid edge -- widen before trusting it")
    print(f"  headroom over the measured point: {best['per_chunk']-MEAS['per_chunk']:+.3f} "
          f"per-chunk, {best['voted5']-MEAS['voted5']:+.3f} voted")
    print(f"  -> bias target on silicon: move the evoked rate toward {best['rate']:.0f} Hz")
    json.dump({"measured": MEAS, "anchor": anchor, "best": best, "grid": res},
              open(args.out, "w"), indent=2)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
