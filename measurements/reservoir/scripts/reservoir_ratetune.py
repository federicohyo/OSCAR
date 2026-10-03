#!/usr/bin/env python3
"""Closed-loop bias tuner for the array's EVOKED firing rate.

Fills the tooling needs behind the `\\todo{MEASURE:}` in Section 4.3.1: re-acquire the
reservoir at the DIM recording's operating point so the D_eff decomposition and the
accuracy can be compared like for like.

`reservoir_biastune.py` cannot do this. It sweeps vleakn and measures the RESTING
rate with zero stimulus, which is a different quantity: the recordings' 8.8 Hz is the
rate the array emits WHILE BEATS ARE BEING PRESENTED, through the projected delta
encoder. This script measures that quantity, through the same `present_delta` path
the acquisition uses, and bisects a bias offset until it hits a target.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 reservoir_ratetune.py \\
        --bias-pattern 'ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_feedproj.biases' \\
        --beats beats_nv60_orig.npz

Run it in `screen`. Budget ~4 min per probe (16 neurons x 6 beats x 2 s) and 6-10
probes, so 25-40 minutes.


WHAT IT TARGETS, AND WHY IT AIMS ELSEWHERE THAN 8.8 Hz
-----------------------------------------
The reference analysis's 8.8 Hz is DIM's rate as REPORTED by the flash-resident read-out
with host-arrival timestamps, whose 11.986 ms lattice with a two-slot floor drops
42% of the events of a recording at today's drive (`lattice_rate_check.py`, which
also carries the control showing the lattice is near-idempotent on data already on
it). The fixed read-out drops zero. Tuning today's array to 8.8 Hz *as measured*
would therefore leave it about 29% quieter than DIM actually was.

So the objective is the LATTICE-PROJECTED rate: at each probe the measured spike
trains are pushed through the old, measured lattice parameters, and THAT is
compared to 8.81 Hz. It needs zero inversion and it is exactly the comparison
`deff_lattice_on_new.py` makes for D_eff. `--target-domain raw` restores the
literal reading of the todo; the deviation is a visible choice rather than a silent one.


THE KNOB, AND WHY A COMMON OFFSET
----------------------------------
The per-neuron bias files carry the diversity the reservoir runs on -- `_feedproj`
spreads vleakn over 28 mV across the 16 neurons. Retuning each neuron to a common
rate would destroy exactly what is being measured (and has before: see the
all-neurons-alike result that killed the count cue). So the knob is a COMMON
ADDITIVE OFFSET applied on top of each neuron's own value. In weak inversion a
common dV multiplies every neuron's current by the same exp(dV/nUT), so the
log-domain spacing between neurons -- the mismatch -- is preserved exactly.


DIRECTION IS MEASURED RATHER THAN ASSUMED
-----------------------------------
The repo's two records of vleakn polarity disagree, and both are load-bearing:
scope observation on 2026-07-12 found that LOWERING vleakn de-saturated neurons
that were railed high (so higher vleakn = more excitable), while the reference analysis's
Limitations say the neuron free-runs BELOW vleakn = 0.225 V. Both can hold if rate
versus vleakn is non-monotonic -- free-run at the bottom, saturation-silence at the
top, a usable band between. This script therefore measures the sign of the response
from its first step and flips if it guessed wrong, and it treats a rate that fell
because neurons went SILENT as a probe shortfall rather than as progress: a saturated
membrane satisfies a naive rate objective while destroying the reservoir.

Headroom is genuinely tight. `_feedproj` sits at 0.257-0.285 V, so a -30 mV offset
already puts the lowest neuron at the free-run edge. If every feasible offset misses
the target, that is a real outcome and the script says so -- see the pre-committed
fallback in `bench/README.md` (MEASURE 1 demotes to the Limitations text).
"""
import argparse
import json
import os
import time

import numpy as np

from meas_common import BridgeSession, load_biases
from run_provenance import provenance
from reservoir_data import delta_encode_proj
from reservoir_run import INTEGRITY, present_delta
from reservoir_run_randproj import load_proj, bias_path
from deff_refractory_ablation import apply_lattice

T_BEAT = 2.0
GRID_OLD = 0.011986        # MEASURED on the 2026-07 recordings rather than refitted
MIN_STEPS = 2              # the two-slot floor, also measured
LATTICE_SEEDS = 8

# Hard rails per knob, and the value below/above which the reference analysis or the bench
# notes say the array stops behaving. Staying inside these is the solution.
RAILS = {
    "vleakn": (0.150, 0.400),   # NMOS leak
    "ifdcp":  (0.600, 1.780),   # PMOS; 1.78 V is OFF
}
FREERUN_VLEAKN = 0.225          # Limitations: below this the neuron free-runs

# Reference-point selection criterion. COMMITTED 2026-08-12 in
# bench/reference_acquisition.md BEFORE the sweep that applies it. Tune within these
# to produce a winner: a reference point that only exists under a widened criterion
# falls short of the standard.
MIN_LIVE_HZ = 2.0     # slowest live neuron; below this it is one drift from dark
DRIFT_MV    = 5.0     # the drift the point must tolerate
DRIFT_TOL   = 0.25    # ... keeping the array mean within this
MIN_CV      = 0.30    # per-neuron rate diversity floor


# ---------------------------------------------------------------------------
def objective(sp, domain):
    """(objective_hz, raw_hz, latticed_hz, cv, per_neuron_hz) for one probe.

    `sp[j][b]` is neuron j's spike times on beat b. The rate definition is the
    reference analysis's, as used by reservoir_acq_compare.describe: total spikes over all
    beats / beats / window."""
    n, nb = len(sp), len(sp[0])
    per = np.array([sum(len(sp[j][b]) for b in range(nb)) / nb / T_BEAT
                    for j in range(n)])
    raw = float(per.mean())
    cv = float(per.std() / per.mean()) if per.mean() > 0 else 0.0

    lats = []
    for seed in range(LATTICE_SEEDS):
        rng = np.random.default_rng(seed)
        pl = np.array([sum(len(apply_lattice(np.asarray(sp[j][b], dtype=float),
                                             GRID_OLD, rng.uniform(0, GRID_OLD),
                                             MIN_STEPS))
                           for b in range(nb)) / nb / T_BEAT for j in range(n)])
        lats.append(pl.mean())
    lat = float(np.mean(lats))

    return (raw if domain == "raw" else lat), raw, lat, cv, per


def probe(b, delta, ctx):
    """Present the fixed beat subset to every neuron with `delta` added to the knob.

    Returns a record for the log. Every gate that could invalidate the reading is
    evaluated here and recorded, so a rejected probe is visible in the JSON rather
    than merely left blank."""
    knob, base, neurons, enc, beats = (ctx["knob"], ctx["base"], ctx["neurons"],
                                       ctx["enc"], ctx["beats"])
    lo, hi = RAILS[knob]
    vals = {k: base[k][knob] + delta for k in neurons}
    railed = [k for k, v in vals.items() if not (lo <= v <= hi)]
    if railed:
        return {"delta": delta, "rejected": "rail",
                "detail": f"{knob} out of [{lo}, {hi}] for neurons {railed}"}

    freerun = ([k for k, v in vals.items() if v < FREERUN_VLEAKN]
               if knob == "vleakn" else [])

    d0, s0 = INTEGRITY["drops"], INTEGRITY["stalls"]
    sp = [[None] * len(beats) for _ in neurons]
    for i, k in enumerate(neurons):
        b.send(f"MASK {1 << k}")            # stream only the recorded neuron
        bi = dict(base[k])
        bi[knob] = vals[k]
        b.apply_biases(bi)
        b.monitor(k)
        time.sleep(0.8)
        b.program_weight(ctx["syn"], ctx["weight"], exc=True)
        b.program_weight(ctx["inh_syn"], ctx["weight"], exc=False)
        for j, bx in enumerate(beats):
            sp[i][j] = present_delta(b, k, enc[k][bx], T_BEAT,
                                     ctx["syn"], ctx["inh_syn"])

    obj, raw, lat, cv, per = objective(sp, ctx["domain"])
    silent = [int(neurons[i]) for i in range(len(neurons)) if per[i] == 0.0]
    rec = {
        "delta": round(delta, 6),
        f"{knob}_range": [round(min(vals.values()), 4), round(max(vals.values()), 4)],
        "objective_hz": round(obj, 3), "raw_hz": round(raw, 3),
        "latticed_hz": round(lat, 3), "cv": round(cv, 3),
        "per_neuron_hz": [round(float(x), 2) for x in per],
        "silent": silent,
        "drops": INTEGRITY["drops"] - d0, "stalls": INTEGRITY["stalls"] - s0,
        "freerun_neurons": freerun,
    }
    if len(silent) > ctx["allow_silent"]:
        rec["rejected"] = "silent"
        rec["detail"] = (
            f"{len(silent)} neurons emitted nothing ({silent}), above the "
            f"--allow-silent budget of {ctx['allow_silent']}. Silence here stays "
            "unexplained: it can be an under-driven neuron or a membrane "
            "railed high, and only a scope tells them apart "
            "(scope_diag_neuron.py, silent_neuron_revive.py). Either way a mean "
            "rate computed over dead channels is not the quantity being tuned.")
    elif rec["drops"] or rec["stalls"]:
        rec["rejected"] = "integrity"
        rec["detail"] = f"drops={rec['drops']} stalls={rec['stalls']}"
    return rec


def show(rec, knob):
    if rec.get("rejected") == "rail":
        print(f"  delta {rec['delta']:+.4f} V  REJECTED (rail): {rec['detail']}")
        return
    tag = f"  REJECTED ({rec['rejected']}): {rec['detail']}" if "rejected" in rec else ""
    fr = f"  freerun{rec['freerun_neurons']}" if rec["freerun_neurons"] else ""
    print(f"  delta {rec['delta']:+.4f} V  {knob} {rec[knob+'_range'][0]:.4f}"
          f"-{rec[knob+'_range'][1]:.4f}  raw {rec['raw_hz']:6.2f}  "
          f"latticed {rec['latticed_hz']:6.2f}  CV {rec['cv']:.3f}  "
          f"silent {len(rec['silent'])}{fr}{tag}")
    print(f"      per-neuron {rec['per_neuron_hz']}")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias-pattern", default=None,
                    help="per-neuron bias files with {k}; default is the "
                         "_feedproj/_super preference of reservoir_run_randproj")
    ap.add_argument("--beats", default="beats_nv60_orig.npz",
                    help="frozen beat set; the probe subset is drawn from it")
    ap.add_argument("--config", default="reservoir_input_proj.json",
                    help="per-neuron input projection (must be the SAME one the "
                         "acquisition will use, or the tuned point does not transfer)")
    ap.add_argument("--neurons", default=",".join(map(str, range(16))))
    ap.add_argument("--knob", default="vleakn", choices=sorted(RAILS),
                    help="which bias to offset (Section 4.3.1 names vleakn/ifdcp)")
    ap.add_argument("--target", type=float, default=8.81,
                    help="target rate in Hz (default: DIM's reported 8.81)")
    ap.add_argument("--target-domain", default="latticed", choices=["latticed", "raw"],
                    help="'latticed' (default) compares through the OLD read-out, "
                         "which is what makes the target comparable to DIM; 'raw' "
                         "takes the todo's 8.8 Hz literally")
    ap.add_argument("--tol", type=float, default=0.08,
                    help="relative tolerance (default 8%%; the lattice's own "
                         "re-quantisation noise floor is 5%%, so do not go below it)")
    ap.add_argument("--n-probe-beats", type=int, default=6)
    ap.add_argument("--allow-silent", type=int, default=0,
                    help="how many neurons may be silent before a probe is rejected. "
                         "This array has neurons that are silent under EVERY bias set "
                         "on disk (n14 under jul10 and struct, n3 under jul10), so a "
                         "budget of 0 refuses every probe. Set it to the count the "
                         "positive control shows are already dark, and record which.")
    ap.add_argument("--step", type=float, default=0.010, help="initial offset step (V)")
    ap.add_argument("--sweep", default=None,
                    help="comma-separated list of offsets (V) to CHARACTERISE rather "
                         "than bisect, e.g. '-0.010,0,0.010,0.020,0.030'. Selects a "
                         "reference operating point by the criterion pre-committed in "
                         "bench/reference_acquisition.md, which is about MARGIN, not "
                         "about hitting a rate. Ignores --target.")
    ap.add_argument("--max-probes", type=int, default=12,
                    help="an off first guess costs a flip probe and a wider "
                         "bracket; 12 x 4 min is still under an hour, and the "
                         "expensive failure is ending one probe short")
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--inh-syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--out", default="data/reservoir_ratetune.json")
    ap.add_argument("--write-biases", default=None,
                    help="pattern with {k} to write the tuned per-neuron bias files. "
                         "MUST carry the clock stamp '_<clk>mhz' or the acquisition "
                         "scripts will refuse it (reservoir_run.check_bias_clock_pairing); "
                         "pass 'auto' for a correctly-stamped default.")
    args = ap.parse_args()

    clk = int(os.environ.get("CARAVAN_CLK_MHZ", "50"))
    if args.write_biases == "auto":
        args.write_biases = (f"ofxCaravanViewer/bin/bias_ratetune_{clk}mhz_"
                             f"{args.knob}_n{{k}}.biases")
    if args.write_biases:
        # Detect it in the first second rather than after an hour of tuning: a bias file the
        # acquisition would refuse makes for an unusable result. The Section 4.6 guard
        # keys on the filename, so the filename has to carry the clock.
        from reservoir_run import check_bias_clock_pairing, BiasClockMismatch
        try:
            check_bias_clock_pairing(args.write_biases)
        except BiasClockMismatch:
            print(f"ABORT: --write-biases '{args.write_biases}' carries no '_{clk}mhz' "
                  f"stamp, so reservoir_run would refuse these files at "
                  f"CARAVAN_CLK_MHZ={clk} (Section 4.6 guard). Use --write-biases auto.")
            return 2

    if args.tol < 0.05:
        print(f"WARNING: tol={args.tol:.3f} is below the lattice's 5% re-quantisation "
              "noise floor; the bisection cannot resolve it (lattice_rate_check.py)")

    neurons = [int(x) for x in args.neurons.split(",")]
    proj = load_proj(args.config)
    from make_beatset import load_beatset
    X, y, meta = load_beatset(args.beats)

    # A FIXED, class-stratified subset, so every probe sees identical input and the
    # bisection is comparing bias points rather than beat draws.
    beats = []
    for cls in sorted(set(y)):
        idx = [i for i in range(len(y)) if y[i] == cls]
        take = max(1, round(args.n_probe_beats * len(idx) / len(y)))
        beats += [idx[i] for i in np.linspace(0, len(idx) - 1, take).astype(int)]
    beats = sorted(set(beats))

    enc = {k: {bx: delta_encode_proj(X[bx], sigma=proj[k]["sigma"],
                                     shift=proj[k]["shift"], theta=proj[k]["theta"])
               for bx in beats} for k in neurons}
    paths = {k: (args.bias_pattern.format(k=k) if args.bias_pattern else bias_path(k))
             for k in neurons}
    base = {k: load_biases(paths[k]) for k in neurons}
    spread = max(base[k][args.knob] for k in neurons) - min(base[k][args.knob]
                                                            for k in neurons)

    print(f"knob={args.knob}  target={args.target:.2f} Hz ({args.target_domain})  "
          f"tol={args.tol*100:.0f}%")
    print(f"beats: {len(beats)} of {len(X)} from {args.beats} (indices {beats})")
    print(f"base {args.knob}: "
          f"{min(base[k][args.knob] for k in neurons):.4f}-"
          f"{max(base[k][args.knob] for k in neurons):.4f} V "
          f"(per-neuron spread {spread*1e3:.1f} mV, preserved by a common offset)")
    print(f"estimated {len(neurons)*len(beats)*(T_BEAT+0.2)/60:.1f} min per probe\n")

    ctx = dict(knob=args.knob, base=base, neurons=neurons, enc=enc, beats=beats,
               syn=args.syn, inh_syn=args.inh_syn, weight=args.weight,
               domain=args.target_domain, allow_silent=args.allow_silent)
    log, solution = [], None

    with BridgeSession() as b:
        def f(delta):
            rec = probe(b, delta, ctx)
            log.append(rec)
            show(rec, args.knob)
            return rec

        def usable(rec):
            return "rejected" not in rec

        if args.sweep:
            deltas = [float(x) for x in args.sweep.split(",")]
            print(f"SWEEP of {len(deltas)} points -- characterising, not bisecting.\n"
                  f"Criterion is pre-committed in bench/reference_acquisition.md: "
                  f"liveness held, slowest live neuron >= {MIN_LIVE_HZ} Hz, "
                  f"+/-{DRIFT_MV} mV moves the mean by <= {DRIFT_TOL*100:.0f}%, "
                  f"CV >= {MIN_CV}; tie-break quietest.\n")
            for d in deltas:
                f(d)
            return _finish_sweep(args, log, ctx, paths)

        print("PROBE 0 -- where the array sits today")
        r0 = f(0.0)
        if not usable(r0):
            print("\nABORT: the starting point itself is not a clean measurement.")
            return _finish(args, log, None, ctx, paths, 1)
        if abs(r0["objective_hz"] - args.target) / args.target <= args.tol:
            print("\nAlready within tolerance at delta = 0.")
            solution = r0
        else:
            need_less = r0["objective_hz"] > args.target
            print(f"\nPROBE 1 -- measuring the SIGN of d(rate)/d({args.knob})")
            print(f"  need {'less' if need_less else 'more'} activity; trying "
                  f"{'-' if need_less else '+'}{args.step:.3f} V first "
                  "(the 2026-07-12 scope result says higher vleakn = more excitable)")
            direction = -1.0 if need_less else +1.0
            r1 = f(direction * args.step)
            DEAD = 0.02          # relative move below which the probe told us nothing
            if usable(r1):
                moved = r1["objective_hz"] - r0["objective_hz"]
                if abs(moved) <= DEAD * r0["objective_hz"]:
                    # Zero movement gives zero evidence of the right direction. Measure the other side
                    # before committing the
                    # remaining probes to a guess.
                    print(f"  -> NO RESPONSE ({moved:+.2f} Hz). Trying the other "
                          "direction before committing.")
                    direction = -direction
                    r1 = f(direction * args.step)
                    if usable(r1):
                        moved = r1["objective_hz"] - r0["objective_hz"]
                        if abs(moved) <= DEAD * r0["objective_hz"]:
                            print(f"\nABORT: {args.knob} moves the evoked rate by "
                                  f"less than {DEAD*100:.0f}% in either direction at "
                                  f"+/-{args.step:.3f} V. This knob leaves the operating point unchanged "
                                  "here; try --knob ifdcp or a "
                                  "larger --step before concluding anything.")
                            return _finish(args, log, None, ctx, paths, 1)
                if usable(r1) and (moved < 0) != need_less:
                    direction = -direction
                    print(f"  -> WRONG WAY: rate moved {moved:+.2f} Hz. Flipping. "
                          f"Measured polarity: higher {args.knob} = "
                          f"{'LESS' if moved > 0 else 'MORE'} active.")
                    r1 = f(direction * args.step)
                elif usable(r1):
                    print(f"  -> correct direction (rate moved {moved:+.2f} Hz). "
                          f"Measured polarity: higher {args.knob} = "
                          f"{'MORE' if (moved > 0) == (direction > 0) else 'LESS'} active.")

            # Expand geometrically until the target is bracketed, a gate fires, or
            # we run out of probes. A gate firing IS the answer when it means the
            # array is best driven elsewhere to keep all neurons. The first step is
            # already measured (r1) -- a second probe adds nothing.
            lo_rec, hi_rec, step, cand = r0, None, args.step, r1
            while len(log) < args.max_probes:
                if not usable(cand):
                    print(f"\n  expansion stopped: {cand.get('rejected')}. "
                          "No feasible offset beyond this point in this direction.")
                    break
                straddles = ((lo_rec["objective_hz"] - args.target) *
                             (cand["objective_hz"] - args.target)) <= 0
                if straddles:
                    hi_rec = cand
                    break
                lo_rec, step = cand, step * 1.8
                cand = f(direction * step)

            if hi_rec is None:
                print("\nNo bracket found. The target is not reachable with this knob "
                      "inside its rails without silencing neurons.")
            else:
                print(f"\nBRACKETED: {lo_rec['delta']:+.4f} V "
                      f"({lo_rec['objective_hz']:.2f} Hz) .. {hi_rec['delta']:+.4f} V "
                      f"({hi_rec['objective_hz']:.2f} Hz). Bisecting.")
                a, c = lo_rec, hi_rec
                while len(log) < args.max_probes:
                    best = min((a, c), key=lambda r: abs(r["objective_hz"] - args.target))
                    if abs(best["objective_hz"] - args.target) / args.target <= args.tol:
                        solution = best
                        break
                    mid = f(0.5 * (a["delta"] + c["delta"]))
                    if not usable(mid):
                        print("  bisection hit a rejected probe; stopping.")
                        break
                    if ((a["objective_hz"] - args.target) *
                            (mid["objective_hz"] - args.target)) <= 0:
                        c = mid
                    else:
                        a = mid
                else:
                    # Ran out of probes mid-bisection. The closest endpoint counts as an approximation rather than a
                    # converged result and is kept out of the reported set.
                    solution = min((a, c),
                                   key=lambda r: abs(r["objective_hz"] - args.target))
                    solution["budget_exhausted"] = True
                    print(f"\n  BUDGET EXHAUSTED after {args.max_probes} probes without "
                          f"reaching {args.tol*100:.0f}%. Re-run with a larger "
                          "--max-probes, seeded with --step near the bracket.")

    return _finish(args, log, solution, ctx, paths, 0)


def _finish_sweep(args, log, ctx, paths):
    """Apply the pre-committed reference criterion to a characterisation sweep.

    Reports every point against every condition, so a rejected point is visible with
    the reason, and so the winner can be checked by hand."""
    knob = args.knob
    pts = sorted([r for r in log if "rejected" not in r or r["rejected"] == "silent"],
                 key=lambda r: r["delta"])
    print("\n" + "=" * 72)
    print("SWEEP RESULT -- criterion from bench/reference_acquisition.md")
    print("=" * 72)

    live0 = None
    for r in sorted(log, key=lambda r: abs(r["delta"])):
        if "per_neuron_hz" in r:
            live0 = {ctx["neurons"][i] for i, v in enumerate(r["per_neuron_hz"]) if v > 0}
            break

    rows = []
    for i, r in enumerate(pts):
        if "per_neuron_hz" not in r:
            continue
        per = r["per_neuron_hz"]
        live = {ctx["neurons"][j] for j, v in enumerate(per) if v > 0}
        live_rates = [v for v in per if v > 0]
        slowest = min(live_rates) if live_rates else 0.0

        # local sensitivity from the neighbouring points: d ln(rate) / dV
        nb = [q for q in (pts[i - 1] if i else None, pts[i + 1] if i + 1 < len(pts) else None)
              if q is not None and q.get("raw_hz", 0) > 0 and r.get("raw_hz", 0) > 0]
        sens = None
        if nb:
            slopes = [abs(np.log(q["raw_hz"] / r["raw_hz"]) / (q["delta"] - r["delta"]))
                      for q in nb if q["delta"] != r["delta"]]
            sens = float(np.mean(slopes)) if slopes else None
        drift = (np.exp(sens * DRIFT_MV * 1e-3) - 1) if sens is not None else None

        c1 = live >= live0 if live0 else False
        c2 = slowest >= MIN_LIVE_HZ
        c3 = drift is not None and drift <= DRIFT_TOL
        c4 = r["cv"] >= MIN_CV
        rows.append(dict(rec=r, live=live, slowest=slowest, drift=drift,
                         ok=(c1 and c2 and c3 and c4), c=(c1, c2, c3, c4)))

    print(f"{'delta(V)':>9} {'mean':>7} {'CV':>6} {'slowest':>8} {'live':>5} "
          f"{'+/-5mV':>8}   liveness silence drift diversity")
    for row in rows:
        r, d = row["rec"], row["drift"]
        mark = lambda b: " ok " if b else "FAIL"
        print(f"{r['delta']:+9.4f} {r['raw_hz']:7.2f} {r['cv']:6.3f} "
              f"{row['slowest']:8.2f} {len(row['live']):5d} "
              f"{(f'{d*100:6.1f}%' if d is not None else '     --'):>8}   "
              + "     ".join(mark(x) for x in row["c"]))

    winners = [row for row in rows if row["ok"]]
    chosen = min(winners, key=lambda row: row["rec"]["raw_hz"]) if winners else None

    if chosen is None:
        print("\nNO POINT SATISFIES THE CRITERION. Reporting that and stopping, per the "
              "plan: do not relax a threshold to produce a winner. Widen the sweep "
              "range, or try --knob ifdcp, and re-run.")
    else:
        r = chosen["rec"]
        print(f"\nREFERENCE POINT: delta = {r['delta']:+.4f} V on {knob}")
        print(f"  {knob} {r[knob+'_range'][0]:.4f}-{r[knob+'_range'][1]:.4f} V, "
              f"mean {r['raw_hz']:.2f} Hz, CV {r['cv']:.3f}, "
              f"{len(chosen['live'])} live, slowest {chosen['slowest']:.2f} Hz")
        print(f"  tolerates +/-{DRIFT_MV:.0f} mV for "
              f"{chosen['drift']*100:.1f}% of mean rate")
        print(f"  quietest of {len(winners)} qualifying point(s) -- the pre-committed "
              "tie-break, because D_eff rises as rate falls")
        if args.write_biases:
            for k in ctx["neurons"]:
                bi = dict(ctx["base"][k])
                bi[knob] = bi[knob] + r["delta"]
                pth = args.write_biases.format(k=k)
                os.makedirs(os.path.dirname(pth) or ".", exist_ok=True)
                with open(pth, "w") as fh:
                    json.dump(bi, fh, indent=2)
            print(f"\n  wrote reference bias files: {args.write_biases}")
            print("  next: bench_reference_check.py --write-fingerprint, then acquire")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump({
            "mode": "sweep", "knob": knob,
            "criterion": {"min_live_hz": MIN_LIVE_HZ, "drift_mv": DRIFT_MV,
                          "drift_tol": DRIFT_TOL, "min_cv": MIN_CV,
                          "tie_break": "quietest",
                          "source": "bench/reference_acquisition.md, committed "
                                    "before this sweep ran"},
            "beats": [int(x) for x in ctx["beats"]], "neurons": ctx["neurons"],
            "allow_silent": ctx["allow_silent"],
            "base_bias_files": {str(k): v for k, v in paths.items()},
            "probes": log,
            "evaluated": [{"delta": row["rec"]["delta"], "ok": row["ok"],
                           "live": sorted(row["live"]), "slowest_hz": row["slowest"],
                           "drift_frac": row["drift"],
                           "conditions": dict(zip(
                               ("liveness", "silence_margin", "drift_margin",
                                "diversity"), row["c"]))} for row in rows],
            "reference": chosen["rec"] if chosen else None,
            **provenance(bias_files=list(paths.values()), knob=knob, mode="sweep"),
        }, fh, indent=2, default=str)
    print(f"\nwrote {args.out}  ({len(log)} probes)")
    return 0 if chosen else 1


def _finish(args, log, solution, ctx, paths, rc):
    print("\n" + "=" * 72)
    if solution is None:
        print("RESULT: no feasible operating point reached the target.")
        print("This is a documented outcome, not a failure of the run. The "
              "pre-committed fallback in bench/README.md applies: MEASURE 1 demotes "
              "to the Limitations text already in the reference analysis, which is correct "
              "as written. Report the probes below; do not widen the rails to "
              "manufacture a solution.")
        usable = [r for r in log if "rejected" not in r]
        if usable:
            best = min(usable, key=lambda r: abs(r["objective_hz"] - args.target))
            print(f"\nClosest clean probe: delta {best['delta']:+.4f} V -> "
                  f"{best['objective_hz']:.2f} Hz against a target of {args.target:.2f}.")
    elif solution.get("budget_exhausted"):
        print(f"RESULT: NOT CONVERGED -- closest probe was delta "
              f"{solution['delta']:+.4f} V -> {solution['objective_hz']:.2f} Hz "
              f"against a target of {args.target:.2f} "
              f"({100*abs(solution['objective_hz']-args.target)/args.target:.1f}% off, "
              f"tolerance {args.tol*100:.0f}%). Record this point clearly when acquiring; "
              "re-run with a larger --max-probes.")
    else:
        print(f"RESULT: delta = {solution['delta']:+.4f} V on {args.knob}")
        print(f"  raw {solution['raw_hz']:.2f} Hz, latticed {solution['latticed_hz']:.2f} Hz, "
              f"CV {solution['cv']:.3f}, {len(solution['silent'])} silent")
        print(f"  target was {args.target:.2f} Hz ({args.target_domain}); "
              f"error {100*abs(solution['objective_hz']-args.target)/args.target:.1f}%")
        print("\n  CHECK THE CV before acquiring. Matching the mean rate does not "
              "match the diversity: DIM sits at 0.495, and the aug-11 recording "
              "pushed through the old lattice reads 0.210 "
              "(lattice_rate_check.py). A matched mean at a different CV is a "
              "different operating point and should be reported as one.")
        if args.write_biases:
            for k in ctx["neurons"]:
                bi = dict(ctx["base"][k])
                bi[args.knob] = bi[args.knob] + solution["delta"]
                p = args.write_biases.format(k=k)
                os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
                with open(p, "w") as fh:
                    json.dump(bi, fh, indent=2)
            print(f"\n  wrote tuned bias files: {args.write_biases}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump({
            "target_hz": args.target, "target_domain": args.target_domain,
            "tol": args.tol, "knob": args.knob,
            "lattice": {"grid_s": GRID_OLD, "min_steps": MIN_STEPS},
            "beats": [int(x) for x in ctx["beats"]],
            "neurons": ctx["neurons"],
            "base_bias_files": {str(k): v for k, v in paths.items()},
            "probes": log,
            "solution": solution,
            **provenance(bias_files=list(paths.values()),
                         knob=args.knob, target_hz=args.target,
                         target_domain=args.target_domain),
        }, fh, indent=2, default=str)
    print(f"\nwrote {args.out}  ({len(log)} probes)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
