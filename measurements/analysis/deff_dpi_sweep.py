#!/usr/bin/env python3
"""How nonlinear would the DPI synapse have to be to matter for D_eff?

The DPI is a LINEAR first-order low-pass in its linear regime (I_w >> I_tau,
I_syn >> I_gain) -- that is exactly the tau_syn filter the baseline already uses. Its
nonlinearity is a quadratic self-limiting term, i.e. saturation, and the measured
saturation signature on silicon is weak (corr(input rate, gain) = -0.082 +/- 0.131).

So rather than pick one operating point, sweep the nonlinearity from linear to strong
and ask how far from linear the synapse would have to be for the gap to move. That is
informative whichever way it comes out. Rates are re-bisected at every point, so this
measures the nonlinearity's effect on TEMPORAL structure, not on rate.

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_dpi_sweep.py
"""
import json
import numpy as np
import deff_physical_mechanisms as M
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

SIL, BEATS = "reservoir_spikes_ref25_expanded_2026-08-12.npz", "beats_nv160_16rec.npz"


def main():
    sp_si, _, _ = load(SIL)
    nb = sp_si.shape[1]; M.NB = nb
    targets = M.silicon_rates(sp_si)
    si = corr_effdim(sp_si, T_BEAT, 8, "exp", M.TAU_TABLE)[2]

    def rho(sp):
        live = [j for j in range(16)
                if sum(len(np.asarray(sp[j, b])) for b in range(nb)) > 0]
        return float(corr_effdim(sp[live, :], T_BEAT, 8, "exp", M.TAU_TABLE)[1]) \
            if len(live) > 1 else float("nan")

    si_rho = rho(sp_si)
    proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
    X = np.load(BEATS, allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(nb)]
           for k in range(16)}
    up, dn = build_jump(M.flatten_events(evs), T_BEAT, DT_DEFAULT,
                        int(round(T_BEAT / DT_DEFAULT)))

    print(f"silicon D_eff {si:.2f}, <|rho|> {si_rho:.3f}, {nb} beats\n")
    print(f"{'syn_sat':>10} {'regime':>12} {'rate':>7} {'D_eff20':>8} {'excess':>8} "
          f"{'% gap':>7} {'<|rho|>':>8}")
    base = None; out = {}
    for sat in (0.0, 10.0, 3.0, 1.0, 0.3, 0.1):
        kw = dict(tau_syn=0.020, syn_sat=sat)
        vth, _ = M.bisect_to_rates(up, dn, targets, kw, hi=200.0)
        sp = M.unflatten(simulate(up, dn, np.repeat(vth, nb), **kw))
        d = corr_effdim(sp, T_BEAT, 8, "exp", M.TAU_TABLE)[2]
        r = float(np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T_BEAT
                           for j in range(16)]))
        if base is None:
            base, gap = d, si - d
        lab = "linear (DPI)" if sat == 0 else ("weak" if sat >= 3 else "strong")
        print(f"{sat:10.1f} {lab:>12} {r:7.1f} {d:8.2f} {d-base:8.2f} "
              f"{100*(d-base)/gap:6.0f}% {rho(sp):8.3f}")
        out[str(sat)] = {"deff20": float(d), "excess": float(d - base),
                         "pct_of_gap": float(100 * (d - base) / gap),
                         "rho": rho(sp), "rate": r}
    out["silicon"] = {"deff20": float(si), "rho": si_rho, "gap": float(gap)}
    json.dump(out, open("data/deff_dpi_sweep.json", "w"), indent=2)
    print(f"\ngap to close: {gap:.2f} units")
    print("wrote data/deff_dpi_sweep.json")


if __name__ == "__main__":
    raise SystemExit(main())
