#!/usr/bin/env python3
"""Rate-matched software baseline against a silicon recording, at ITS beat count.

D_eff depends on the number of beats the covariance is estimated from -- measured at
+2.2 units going from 60 to 160 on one recording (deff_drift_test.py) -- so silicon
and model must be scored on the SAME beat set, not merely at the same firing rate.
This script takes both from the recording it is pointed at.

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_match_baseline.py \
        --silicon reservoir_spikes_ref25_expanded_2026-08-12.npz \
        --beats beats_nv160_16rec.npz

The tail time constant is not identifiable from spike data (we record spikes, not
membrane current), so the comparison is quoted across every value that reaches the
array's rates rather than at one fitted value.
"""
import argparse, json
import numpy as np

import deff_physical_mechanisms as M
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

TAUS = M.TAUS
IT = TAUS.index(M.TAU_TABLE)


def live_rho(sp):
    live = [j for j in range(sp.shape[0])
            if sum(len(np.asarray(sp[j, b])) for b in range(sp.shape[1])) > 0]
    return float(corr_effdim(sp[live, :], T_BEAT, 8, "exp", M.TAU_TABLE)[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--silicon", default="reservoir_spikes_ref25_expanded_2026-08-12.npz")
    ap.add_argument("--beats", default="beats_nv160_16rec.npz")
    ap.add_argument("--config", default="reservoir_input_proj.json")
    ap.add_argument("--tau-syn", default="0.010,0.020,0.030")
    ap.add_argument("--out", default="data/deff_match_baseline.json")
    args = ap.parse_args()

    sp_si, _, _ = load(args.silicon)
    nb = sp_si.shape[1]
    M.NB = nb                      # the module's helpers read this at call time
    targets = M.silicon_rates(sp_si)
    si_curve = [corr_effdim(sp_si, T_BEAT, 8, "exp", t)[2] for t in TAUS]
    si_rho = live_rho(sp_si)
    print(f"silicon {args.silicon}")
    print(f"  {nb} beats, mean rate {targets.mean():.1f} Hz, max {targets.max():.1f}")
    print(f"  D_eff(20ms) {si_curve[IT]:.2f}   <|rho|> {si_rho:.3f}")

    proj = {int(c["neuron"]): c for c in json.load(open(args.config))["proj"]}
    X = np.load(args.beats, allow_pickle=True)["X"]
    assert len(X) == nb, f"beat set has {len(X)} beats, recording has {nb}"
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(nb)]
           for k in range(M.NN)}
    nsteps = int(round(T_BEAT / DT_DEFAULT))
    up, dn = build_jump(M.flatten_events(evs), T_BEAT, DT_DEFAULT, nsteps)

    out = {"silicon": {"path": args.silicon, "n_beats": nb,
                       "deff": si_curve, "deff20": si_curve[IT], "rho": si_rho,
                       "mean_rate": float(targets.mean())}, "model": {}}
    print(f"\n{'tau_syn':>8} {'rate':>7} {'off>20%':>8} {'D_eff20':>8} {'<|rho|>':>8} {'gap':>7}")
    for ts in [float(x) for x in args.tau_syn.split(",")]:
        kw = dict(tau_syn=ts)
        vth, ach = M.bisect_to_rates(up, dn, targets, kw, hi=200.0)
        sp = M.unflatten(simulate(up, dn, np.repeat(vth, nb), **kw))
        curve = [corr_effdim(sp, T_BEAT, 8, "exp", t)[2] for t in TAUS]
        rate = float(np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T_BEAT
                              for j in range(M.NN)]))
        off = int((np.abs(ach - targets) / np.maximum(targets, 1e-9) > 0.2).sum())
        gap = si_curve[IT] - curve[IT]
        print(f"{ts*1e3:7.0f}m {rate:7.1f} {off:8d} {curve[IT]:8.2f} {live_rho(sp):8.3f} {gap:7.2f}")
        out["model"][f"tau_syn_{ts}"] = {"deff": curve, "deff20": curve[IT],
                                         "rho": live_rho(sp), "rate": rate,
                                         "n_off": off, "gap": float(gap)}
    g = [v["gap"] for v in out["model"].values()]
    out["gap_range"] = [float(min(g)), float(max(g))]
    print(f"\nGAP at tau=20 ms, across every tail that reaches the rates: "
          f"{min(g):.1f}-{max(g):.1f} units  (n={nb} beats, both sides)")
    json.dump(out, open(args.out, "w"), indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
