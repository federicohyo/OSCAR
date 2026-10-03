#!/usr/bin/env python3
"""Why no mechanism moved D_eff -- and what the gap actually is.

The mechanism search found nothing, and its upward control then failed: amplifying
the per-neuron projection spread 2x and 3x did not raise D_eff either. A search whose
positive control cannot move the measurement upward is not evidence of anything, so
the cause had to be found before any negative could be believed.

It is this. In the software model D_eff is very nearly a FUNCTION OF OUTPUT RATE
ALONE. Scale the thresholds and let the rate move, and D_eff traces one tight
monotone curve. Fix the rate -- which is exactly what the rate-matching bisection
does, correctly -- and D_eff is fixed too, so no mechanism can move it. The negatives
were real; they were measuring a constraint the model imposes on itself.

Silicon does not sit on that curve, and THAT is the gap:

    silicon        D_eff 16.91  at 35.6 Hz
    model needs                    ~8.0 Hz  for the same D_eff

so the array behaves like the model running ~4.5x quieter. Stated as a rate-free
quantity: the array delivers about 4.5x more dimensionality per spike than a LIF
reproducing its dynamics -- which is an efficiency claim, and the read-out is charged
per event (Section 8), so it is the same axis the cost frontier is measured on.

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_rate_tradeoff.py

CAVEATS. One recording, one model class, 160 beats. Rate is swept by scaling
thresholds only; another route to the same rate could trace a different curve. The
8.0 Hz figure is interpolation inside the swept range (4.7-45.5 Hz), not
extrapolation.
"""
import json
import numpy as np
import deff_physical_mechanisms as M
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

SIL, BEATS = "reservoir_spikes_ref25_expanded_2026-08-12.npz", "beats_nv160_16rec.npz"
SCALES = (0.5, 0.7, 1.0, 1.5, 2.5, 4.0, 6.0, 9.0)


def main():
    sp_si, _, _ = load(SIL)
    nb = sp_si.shape[1]; M.NB = nb
    targets = M.silicon_rates(sp_si)
    si = corr_effdim(sp_si, T_BEAT, 8, "exp", M.TAU_TABLE)[2]
    proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
    X = np.load(BEATS, allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(nb)] for k in range(16)}
    up, dn = build_jump(M.flatten_events(evs), T_BEAT, DT_DEFAULT,
                        int(round(T_BEAT / DT_DEFAULT)))
    kw = dict(tau_syn=0.020)
    vth0, _ = M.bisect_to_rates(up, dn, targets, kw, hi=200.0)

    R, D = [], []
    print(f"{'rate (Hz)':>10} {'D_eff(20ms)':>12}")
    for sc in SCALES:
        sp = M.unflatten(simulate(up, dn, np.repeat(vth0 * sc, nb), **kw))
        d = corr_effdim(sp, T_BEAT, 8, "exp", M.TAU_TABLE)[2]
        r = float(np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T_BEAT
                           for j in range(16)]))
        R.append(r); D.append(d)
        print(f"{r:10.1f} {d:12.2f}")
    R, D = np.array(R), np.array(D)
    o = np.argsort(D)
    need = float(np.interp(si, D[o], R[o]))
    print(f"\nsilicon: D_eff {si:.2f} at {targets.mean():.1f} Hz")
    print(f"model needs ~{need:.1f} Hz for the same D_eff")
    print(f"-> the array delivers ~{targets.mean()/need:.1f}x more dimensionality per spike")
    json.dump({"model_rate": R.tolist(), "model_deff": D.tolist(),
               "silicon_deff": float(si), "silicon_rate": float(targets.mean()),
               "model_rate_for_silicon_deff": need,
               "dimensionality_per_spike_advantage": float(targets.mean() / need)},
              open("data/deff_rate_tradeoff.json", "w"), indent=2)
    print("wrote data/deff_rate_tradeoff.json")


if __name__ == "__main__":
    raise SystemExit(main())
