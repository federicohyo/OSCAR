#!/usr/bin/env python3
"""Autonomous NARMA-reservoir bias tuner -- driver / CLI.

Closed loop: constrained Bayesian optimisation over a SMALL, BOUNDED window (weak inversion!) in
VOLT space, evaluating each candidate bias vector on a pluggable backend that returns AER stream
counts + scope membrane traces; the shared objective rewards fading memory (MC1/MC2) subject to
bounded rate, saturation-free (drift), railing-free, a diversity floor, and a tau_eff band.

    # validate the whole loop against the software chip-sim (chip and scope untouched):
    ./.venv-meas/bin/python3 tune_narma.py --backend sim --iters 40

    # bench (chip up at 50 MHz, base biases loaded, scope on /dev/usbtmc0):
    CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 tune_narma.py --backend chip \
        --base ofxNARMATuning/bin/bias_synapse_characterization_narma.biases --iters 30

Checkpoints every evaluation to <out> so a bench run can be stopped/resumed and audited.
"""
import argparse, json, os, time
import numpy as np
from narma_tuner import (Channel, ConstrainedBO, ObjectiveCfg, analyze, objective,
                         channels_to_dict)

# Tuned channels: the 5-6 that set the edge-of-chaos point, each a SMALL window (V) around a
# known-good centre. half_span kept to <= ~2 weak-inversion e-folds (~0.06 V) so steps stay bounded.
DEFAULT_CHANNELS = [
    Channel("vleakn", 0.268, 0.045),     # membrane leak -> tau_m / excitability
    Channel("JExcWn0", 0.620, 0.050),    # excitatory / recurrent gain (toward chaos)
    Channel("vtaun", 0.600, 0.050),      # synapse tau -> integration / memory horizon
    Channel("JInhWp0", 0.900, 0.050),    # inhibition (tempers runaway)
    Channel("vthrdn", 0.700, 0.030),     # threshold (spike rate)
]


def make_backend(args):
    M = args.M if args.M > 0 else (800 if args.backend == "sim" else 300)
    if args.backend == "sim":
        from narma_tuner_backends import SimBackend
        return SimBackend(M=M, seed=args.seed), None
    from narma_tuner_backends import ChipBackend
    from meas_common import BridgeSession, load_biases
    base = load_biases(args.base)
    meta = json.load(open(args.base))
    dens = int(meta.get("narma_dens", 15)); rec_w = int(meta.get("narma_rec_w", 10))
    b = BridgeSession(); b.__enter__()
    b.apply_biases(base); time.sleep(1.0)
    return ChipBackend(b, base, dens, rec_w, M=M, use_scope=args.scope,
                       monitor_neuron=args.monitor, verbose=True), b


def preflight(backend, bridge):
    """Chip sanity check before spending BO iterations: excitatory positive control on a few neurons
    + one short recurrent NARMACOLLECT. Aborts if the array is completely dead (mis-bring-up)."""
    import numpy as np
    print(">> preflight: positive control + short NARMACOLLECT ...", flush=True)
    tot = 0
    for k in (5, 7, 13, 14):
        bridge.program_weight(0, 15, exc=True); bridge.route(0, k, exc=True); time.sleep(0.03)
        bridge.drain(max_lines=200000)
        c = [0] * 16; bridge.fire(15); time.sleep(0.2); bridge.drain(c)
        tot += sum(c); print(f"   posctrl n{k}: counts[{k}]={c[k]} total={sum(c)}", flush=True)
    state, u = backend._collect_stream(recur=1)
    spikes = int(state.sum())
    print(f"   NARMACOLLECT recur: {spikes} spikes, per-neuron={state.sum(0).tolist()}", flush=True)
    if tot == 0 and spikes < 5:
        raise SystemExit("preflight flagged the array as silent. Re-bring-up "
                         "(./bringup_50.sh) and load biases before tuning.")
    print(">> preflight OK\n", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["sim", "chip"], default="sim")
    ap.add_argument("--iters", type=int, default=40)
    ap.add_argument("--reps", type=int, default=1, help="evaluations averaged per candidate (noise)")
    ap.add_argument("--M", type=int, default=0, help="stream frames (0=auto: chip 120, sim 800)")
    ap.add_argument("--scope", action="store_true", help="use scope membrane (tau_eff/railing); "
                    "default OFF -- tune on AER memory first, add scope once validated")
    ap.add_argument("--monitor", type=int, default=None, metavar="N",
                    help="route neuron N's membrane to the scope monitor pin during tuning "
                         "(live human view; e.g. --monitor 1 for an active reservoir neuron)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--base", default="ofxNARMATuning/bin/bias_synapse_characterization_narma.biases")
    ap.add_argument("--out", default="data/narma/tune_log.json")
    args = ap.parse_args()

    channels = DEFAULT_CHANNELS
    cfg = ObjectiveCfg()
    bo = ConstrainedBO(channels, seed=args.seed)
    backend, bridge = make_backend(args)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    log = []
    scope_note = "scope ON (tau_eff/railing)" if args.scope else "AER-only (no scope)"
    if args.monitor is not None:
        scope_note += f", monitor->n{args.monitor} on scope pin"
    print(f"NARMA tuner: backend={args.backend}, {scope_note}, {len(channels)} channels, "
          f"{args.iters} iters, reps={args.reps}\nchannels (V, +/-span): " +
          ", ".join(f"{c.name}[{c.center:.3f}+/-{c.half_span:.3f}]" for c in channels))
    if bridge is not None:
        preflight(backend, bridge)
    print(f"\n{'it':>3} {'J':>7} {'feas':>4} {'mc0':>5} {'mc1':>5} {'mc2':>5} "
          f"{'mc1ff':>5} {'gap1':>5} {'rate':>5} {'drift':>6} {'nlive':>5}   (mc1/gap1 = recurrent / rec-ff)")

    best_J = -1e9; best = None
    try:
        for it in range(args.iters):
            x = bo.ask(); theta = channels_to_dict(channels, x)
            diags = []
            for _ in range(args.reps):
                diags.append(analyze(backend.measure(theta)))
            # average diagnostics over reps (noise)
            d = diags[0]
            if args.reps > 1:
                from narma_tuner import Diagnostics
                d = Diagnostics(
                    *(float(np.mean([getattr(x_, f) for x_ in diags]))
                      for f in ("mc0", "mc1", "mc2", "rate", "drift")),
                    int(np.median([x_.n_live for x_ in diags])),
                    float(np.nanmedian([x_.tau_eff for x_ in diags])),
                    float(np.mean([x_.railed_frac for x_ in diags])),
                    float(np.nanmean([x_.mc1_ff for x_ in diags])),
                    float(np.nanmean([x_.mc2_ff for x_ in diags])))
            gap1 = (d.mc1 - d.mc1_ff) if np.isfinite(d.mc1_ff) else float("nan")
            J, feas, info = objective(d, cfg)
            bo.tell(x, J)
            log.append({"it": it, "theta": theta, "J": J, "feasible": feas,
                        "mc": [d.mc0, d.mc1, d.mc2], "mc_ff": [d.mc1_ff, d.mc2_ff],
                        "gap1": gap1, "rate": d.rate, "drift": d.drift,
                        "tau_eff": d.tau_eff, "railed_frac": d.railed_frac, "n_live": d.n_live,
                        "viol": info["viol"]})
            with open(args.out, "w") as f:
                json.dump(log, f, indent=1)
            g_s = f"{gap1:+5.2f}" if np.isfinite(gap1) else "  n/a"
            print(f"{it:3d} {J:7.3f} {str(feas)[0]:>4} {d.mc0:5.2f} {d.mc1:5.2f} {d.mc2:5.2f} "
                  f"{d.mc1_ff:5.2f} {g_s} {d.rate:5.2f} {d.drift:+6.2f} {d.n_live:5d}")
            if J > best_J:
                best_J = J; best = {"it": it, "theta": theta, "diag": log[-1]}
    finally:
        if bridge is not None:
            try: backend.close()
            except Exception: pass
            bridge.__exit__(None, None, None)

    print("\n=== BEST ===")
    if best:
        print(f"iter {best['it']}  J={best_J:.3f}  feasible={best['diag']['feasible']}")
        print("theta (V): " + ", ".join(f"{k}={v:.4f}" for k, v in best["theta"].items()))
        bd = best['diag']
        print(f"mc(rec)={bd['mc']}  mc_ff={bd.get('mc_ff')}  gap1={bd.get('gap1')}  "
              f"rate={bd['rate']:.2f}  drift={bd['drift']:+.2f}  n_live={bd['n_live']}")
        print("  gap1 = recurrent MC1 - feedforward MC1: recurrence helps only if this is clearly > 0")
    print(f"\nfull log: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
