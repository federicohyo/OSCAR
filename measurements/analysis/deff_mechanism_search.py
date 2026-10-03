#!/usr/bin/env python3
"""Search for a mechanism that closes the D_eff gap. Criteria: bench/deff_mechanism_search.md.

Read the criteria before the numbers. In particular every mechanism is scored as its
EXCESS over a rate-matched baseline with thresholds RE-BISECTED under the mechanism,
never as a raw D_eff -- D_eff rises as rate falls, so anything that merely quietens
the array would otherwise look like an explanation.

Two-stage, to keep the compute honest and affordable at 160 beats: screen every
candidate at tau_syn = 20 ms, then re-run whatever clears 30% of the gap at 10 ms for
the envelope-stability check the criteria require (criterion 2).

    PYTHONPATH=. ./.venv-meas/bin/python3 deff_mechanism_search.py
"""
import json
import numpy as np

import deff_physical_mechanisms as M
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

SILICON = "reservoir_spikes_ref25_expanded_2026-08-12.npz"
BEATS = "beats_nv160_16rec.npz"
IT = M.TAUS.index(M.TAU_TABLE)
SEEDS = 2                    # stochastic mechanisms are averaged over this many draws
CONTRIB = 0.30               # criterion 1: excess >= 30% of the gap to count


def live_rho(sp):
    live = [j for j in range(sp.shape[0])
            if sum(len(np.asarray(sp[j, b])) for b in range(sp.shape[1])) > 0]
    if len(live) < 2:
        return float("nan")
    return float(corr_effdim(sp[live, :], T_BEAT, 8, "exp", M.TAU_TABLE)[1])


def evaluate(up, dn, targets, nb, ts, ei=0.0, tsp=0.0, **extra):
    """Bisect to the target rates under the mechanism, then score. Stochastic
    mechanisms (ei, tau_syn spread) are averaged over SEEDS draws."""
    curves, rhos, rates, offs = [], [], [], []
    for s in range(SEEDS if (ei or tsp) else 1):
        kw = dict(extra)
        kw["tau_syn"] = (np.repeat(
            np.random.default_rng(800 + s).normal(ts, tsp * ts, M.NN).clip(1e-4, None), nb)
            if tsp else ts)
        if ei:
            g = np.random.default_rng(700 + s).normal(1.0, ei, M.NN).clip(0.05, None)
            kw["w_inh"] = np.repeat(0.34 * g, nb)
        vth, ach = M.bisect_to_rates(up, dn, targets, kw, hi=200.0)
        sp = M.unflatten(simulate(up, dn, np.repeat(vth, nb), **kw))
        curves.append([corr_effdim(sp, T_BEAT, 8, "exp", t)[2] for t in M.TAUS])
        rhos.append(live_rho(sp))
        rates.append(np.mean([sum(len(np.asarray(sp[j, b])) for b in range(nb)) / nb / T_BEAT
                              for j in range(M.NN)]))
        offs.append(int((np.abs(ach - targets) / np.maximum(targets, 1e-9) > 0.2).sum()))
    c = np.array(curves).mean(axis=0)
    return dict(deff=list(c), deff20=float(c[IT]), rho=float(np.nanmean(rhos)),
                rate=float(np.mean(rates)), n_off=int(np.mean(offs)))


CANDIDATES = [
    ("baseline (tail only)",              dict()),
    ("E/I ratio mismatch 20%",            dict(ei=0.20)),
    ("E/I ratio mismatch 40%",            dict(ei=0.40)),
    ("E/I ratio mismatch 65%",            dict(ei=0.65)),
    ("per-neuron tau_syn spread 40%",     dict(tsp=0.40)),
    ("per-neuron tau_syn spread 80%",     dict(tsp=0.80)),
    ("no rectification below rest",       dict(rectify=False)),
    ("constant-current leak",             dict(leak_mode="const")),
    ("E/I 40% + tau_syn spread 40%",      dict(ei=0.40, tsp=0.40)),
    ("E/I 40% + no rectification",        dict(ei=0.40, rectify=False)),
]


def main():
    sp_si, _, _ = load(SILICON)
    nb = sp_si.shape[1]
    M.NB = nb
    targets = M.silicon_rates(sp_si)
    si = [corr_effdim(sp_si, T_BEAT, 8, "exp", t)[2] for t in M.TAUS]
    si_rho = live_rho(sp_si)
    print(f"silicon: {nb} beats, D_eff(20ms) {si[IT]:.2f}, <|rho|> {si_rho:.3f}, "
          f"mean rate {targets.mean():.1f} Hz\n")

    proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
    X = np.load(BEATS, allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(nb)]
           for k in range(M.NN)}
    up, dn = build_jump(M.flatten_events(evs), T_BEAT, DT_DEFAULT,
                        int(round(T_BEAT / DT_DEFAULT)))

    out = {"silicon": {"deff20": si[IT], "rho": si_rho, "n_beats": nb}, "stages": {}}
    survivors = []
    for stage, ts in (("screen", 0.020), ("confirm", 0.010)):
        pool = CANDIDATES if stage == "screen" else \
            [c for c in CANDIDATES if c[0] == "baseline (tail only)" or c[0] in survivors]
        if stage == "confirm" and not survivors:
            print("\nno candidate cleared 30% at the screen -- nothing to confirm")
            break
        print(f"\n{'='*84}\n{stage.upper()}  tau_syn = {ts*1e3:.0f} ms\n{'='*84}")
        print(f"{'condition':34s} {'D_eff20':>8} {'excess':>8} {'% gap':>7} "
              f"{'<|rho|>':>8} {'d_rho':>7} {'off':>4}")
        base = gap = None
        for name, kw in pool:
            r = evaluate(up, dn, targets, nb, ts, **kw)
            if base is None:
                base, gap = r["deff20"], si[IT] - r["deff20"]
                base_rho = r["rho"]
            exc = r["deff20"] - base
            pct = 100 * exc / gap
            drho = abs(r["rho"] - si_rho) - abs(base_rho - si_rho)   # negative = closer
            print(f"{name:34s} {r['deff20']:8.2f} {exc:8.2f} {pct:6.0f}% "
                  f"{r['rho']:8.3f} {drho:+7.3f} {r['n_off']:4d}")
            out["stages"].setdefault(stage, {})[name] = dict(r, excess=float(exc),
                                                             pct_of_gap=float(pct),
                                                             d_rho=float(drho))
            if stage == "screen" and name != "baseline (tail only)" and pct >= CONTRIB * 100:
                survivors.append(name)
        if stage == "screen":
            print(f"\ngap to close: {gap:.2f} units")
            print(f"clearing {CONTRIB*100:.0f}%: {survivors or 'NONE'}")
    json.dump(out, open("data/deff_mechanism_search.json", "w"), indent=2)
    print("\nwrote data/deff_mechanism_search.json")


if __name__ == "__main__":
    raise SystemExit(main())
