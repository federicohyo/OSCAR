#!/usr/bin/env python3
"""Software-LIF control for the per-neuron input-projection experiment.

Replaces the analog chip with a bank of IDENTICAL (non-mismatched) leaky integrate-
and-fire neurons -- same membrane tau, threshold, reset, refractory, synaptic weight
for all units -- driven by exactly the same per-neuron projected delta streams the
hardware received (reservoir_input_proj.json + delta_encode_proj). This isolates the
question: is the effective-dimensionality expansion a property of the INPUT PROJECTION
(would appear even with identical neurons) or of the analog DEVICE MISMATCH?

--shared drives every neuron with the SAME (unprojected) delta stream, the identical-
neurons + shared-input control (expected eff-dim ~1, fully redundant).
--mismatch F adds F relative Gaussian jitter to per-neuron tau/threshold/weight, an
optional software analogue of device mismatch.

Saves an npz in the same format as reservoir_run.py so reservoir_analysis.py /
reservoir_kernel.py consume it unchanged.
"""

import argparse
import json
import numpy as np

from reservoir_data import get_beats, delta_encode, delta_encode_proj


def sim_lif(events, T, tau_m, vth, vreset, tref, w_exc, w_inh, dt=0.001):
    """Event-driven LIF over [0,T]. events = [(t_frac, channel)], channel 0=UP(exc),
    1=DOWN(inh). Returns output spike times (s)."""
    v = 0.0
    last_spike = -1e9
    decay = np.exp(-dt / tau_m)
    nsteps = int(round(T / dt))
    # bin input jumps onto the time grid
    jump = np.zeros(nsteps + 1)
    for tf, ch in events:
        i = min(nsteps, int(round(tf * T / dt)))
        jump[i] += w_exc if ch == 0 else -w_inh
    out = []
    for i in range(nsteps):
        v = v * decay + jump[i]
        t = i * dt
        if v < 0:
            v = 0.0                      # rectify (hyperpolarised runaway blocked)
        if t - last_spike < tref:
            v = vreset
            continue
        if v >= vth:
            out.append(t)
            v = vreset
            last_spike = t
    return np.array(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", default="208,233,119,106,221")
    ap.add_argument("--n-per-class", type=int, default=30)
    ap.add_argument("--classes", default="NV")
    ap.add_argument("--beats", default=None,
                    help="frozen beat set from make_beatset.py; overrides "
                         "--records/--n-per-class/--classes so the SW baseline is "
                         "beat-matched to the hardware runs.")
    ap.add_argument("--config", default="reservoir_input_proj.json")
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--T", type=float, default=2.0)
    ap.add_argument("--tau-m", type=float, default=0.02, help="membrane tau (s)")
    ap.add_argument("--vth", type=float, default=1.0)
    ap.add_argument("--tref", type=float, default=0.005, help="refractory (s)")
    ap.add_argument("--w-exc", type=float, default=0.34)
    ap.add_argument("--w-inh", type=float, default=0.34)
    ap.add_argument("--thr", type=float, default=0.04, help="delta thr for --shared")
    ap.add_argument("--shared", action="store_true", help="same delta stream for all neurons")
    ap.add_argument("--mismatch", type=float, default=0.0, help="rel. per-neuron param jitter")
    ap.add_argument("--mismatch-taus-only", action="store_true",
                    help="apply --mismatch to the membrane time constants ONLY, leaving "
                         "threshold and weight identical across neurons. This is the tight "
                         "control for the D_eff claim (Task 2): it isolates heterogeneous "
                         "tau from every other way silicon differs from the SW model.")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    with open(args.config) as f:
        proj = {int(c["neuron"]): c for c in json.load(f)["proj"]}
    if args.beats:
        from make_beatset import load_beatset
        X, y, meta = load_beatset(args.beats)
        print(f"beats: loaded {len(X)} from {args.beats}")
    else:
        X, y, meta = get_beats(records=tuple(args.records.split(",")),
                               n_per_class=args.n_per_class, classes=args.classes)
    neurons = list(range(args.n))

    rng = np.random.default_rng(args.seed)
    # per-neuron LIF params: identical unless --mismatch>0
    def jit(base):
        return base * (1.0 + args.mismatch * rng.standard_normal(args.n))
    taus = np.clip(jit(args.tau_m), 0.003, None)
    if args.mismatch_taus_only:
        vths = np.full(args.n, args.vth)
        wes = np.full(args.n, args.w_exc)
    else:
        vths = np.clip(jit(args.vth), 0.2, None)
        wes = np.clip(jit(args.w_exc), 0.02, None)

    mode = "shared" if args.shared else "proj"
    out = args.out or f"reservoir_spikes_nv_swlif_{mode}" + \
        (f"_mm{args.mismatch:g}" if args.mismatch else "") + ".npz"
    print(f"SW-LIF ({mode}, mismatch={args.mismatch}): {args.n} identical LIF "
          f"tau_m={args.tau_m*1e3:.0f}ms vth={args.vth} tref={args.tref*1e3:.0f}ms "
          f"w={args.w_exc}  beats={len(X)}  -> {out}")

    spikes = np.empty((args.n, len(X)), dtype=object)
    for k in neurons:
        tot = 0
        for bi in range(len(X)):
            if args.shared:
                ev = delta_encode(X[bi], args.thr)
            else:
                p = proj[k]
                ev = delta_encode_proj(X[bi], sigma=p["sigma"], shift=p["shift"], theta=p["theta"])
            st = sim_lif(ev, args.T, taus[k], vths[k], 0.0, args.tref, wes[k], args.w_inh)
            spikes[k, bi] = st
            tot += len(st)
        print(f"  neuron {k:2d}: {tot} spikes over {len(X)} beats" + ("  [DEAD]" if tot == 0 else ""))

    np.savez(out, spikes=spikes, labels=y, records=meta["records"],
             neurons=np.array(neurons), T=args.T, coding=f"swlif_{mode}", classes=args.classes)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
