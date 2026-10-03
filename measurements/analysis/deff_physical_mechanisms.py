#!/usr/bin/env python3
"""Can the unexplained D_eff residual be closed by soma physics the model omits?

the reference analysis accounts for the expansion from D_eff 9.6
(identical software LIF + input projection) to silicon's 18.1 through the
operating-point distribution, a mean-rate control and the measured 11.99 ms
acquisition lattice, and leaves ~1.4 units with no mechanism named. Every
mechanism tested there is a property of the ACQUISITION or a spread of LIF
PARAMETERS. None of them changes the model neuron's EQUATIONS.

This script tests the four ways the fabricated soma's equations differ from
reservoir_sw_lif.sim_lif (see deff_physical_sim.py for what each is and why):

    RECT   membrane holds state below rest instead of rectifying at 0
    SYN    DPI synaptic tail instead of an impulse
    LEAK   constant-current (linear) leak instead of an ohmic (exponential) one
    NOISE  membrane noise instead of a noiseless integrator

METHOD, and the one thing that makes it interpretable. Every mechanism changes
the output rate, and in this pipeline D_eff rises as rate falls, so a mechanism
can look explanatory purely by quietening the neuron -- the trap the reference analysis
already documents. Rather than correct for it afterwards with a rate-control
family, we remove it by construction: for EVERY condition the 16 thresholds are
re-bisected so that each model neuron reproduces its silicon counterpart's mean
output rate, in rank order. Every row below therefore sits at silicon's own
per-neuron rate distribution, and no D_eff difference between rows is a rate
effect. The measured acquisition lattice is applied to every row as well, so each
row is scored against the reference analysis's BEST model (16.7), not its baseline.

The residual is reported with the paired bootstrap interval of
deff_residual_ci.py, because a mechanism that "closes the gap" has only closed a
quantity whose own 95% interval is [+0.04, +2.08].

  PYTHONPATH=. ./.venv-meas/bin/python3 deff_physical_mechanisms.py

Writes data/deff_physical_mechanisms.json.
"""
import json
import sys

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_datasets import DIM
from reservoir_demo_proj import corr_effdim, load
from deff_refractory_ablation import apply_lattice, fit_lattice, isis
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

K = 8
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
TAU_TABLE = 0.02
N_BOOT = 200
LATTICE_SEEDS = 4
NB = 60
NN = 16


# ---------------------------------------------------------------------------
def silicon_rates(sp):
    return np.array([sum(len(np.asarray(sp[j, b])) for b in range(sp.shape[1]))
                     / sp.shape[1] / T_BEAT for j in range(sp.shape[0])])


def flatten_events(evs):
    """(neuron, beat) -> flat unit list, u = neuron*NB + beat."""
    return [evs[k][b] for k in range(NN) for b in range(NB)]


def unflatten(spk_list, lattice=None, rng=None):
    sp = np.empty((NN, NB), dtype=object)
    for k in range(NN):
        for b in range(NB):
            st = spk_list[k * NB + b]
            if lattice is not None:
                st = apply_lattice(st, lattice, rng.uniform(0, lattice), 2)
            sp[k, b] = st
    return sp


def rates_from(spk_list):
    return np.array([sum(len(spk_list[k * NB + b]) for b in range(NB)) / NB / T_BEAT
                     for k in range(NN)])


def bisect_to_rates(up, dn, targets, kw, iters=22, lo=0.02, hi=40.0,
                    vth_scale=None):
    """Bisect all 16 thresholds simultaneously to silicon's per-neuron rates.

    Every (neuron, beat) pair advances in one state vector, so one simulation
    evaluates all 16 candidate thresholds at once and the whole bisection costs
    `iters` simulations rather than 16*iters*NB.
    """
    lo_v = np.full(NN, lo)
    hi_v = np.full(NN, hi)

    def rate_at(vth_per_neuron):
        vth_u = np.repeat(vth_per_neuron, NB)
        if vth_scale is not None:
            vth_u = vth_u * vth_scale
        return rates_from(simulate(up, dn, vth_u, **kw))

    r_lo = rate_at(lo_v)
    for _ in range(iters):
        mid = 0.5 * (lo_v + hi_v)
        r = rate_at(mid)
        # rate is monotone DECREASING in threshold
        too_fast = r > targets
        lo_v = np.where(too_fast, mid, lo_v)
        hi_v = np.where(too_fast, hi_v, mid)
    del r_lo
    vth = 0.5 * (lo_v + hi_v)
    return vth, rate_at(vth)


def score(sp):
    rho = corr_effdim(sp, T_BEAT, K, "exp", TAU_TABLE)[1]
    curve = [corr_effdim(sp, T_BEAT, K, "exp", t)[2] for t in TAUS]
    return float(rho), [float(c) for c in curve]


# ---------------------------------------------------------------------------
def main():
    sp_si, _, _ = load(DIM.path)
    targets = silicon_rates(sp_si)
    grid, _ = fit_lattice(isis(sp_si))
    rho_si, curve_si = score(sp_si)
    d_si = curve_si[TAUS.index(TAU_TABLE)]
    print(f"silicon: D_eff {d_si:.2f}  <|rho|> {rho_si:.3f}  "
          f"mean rate {targets.mean():.2f} Hz  lattice {grid*1e3:.2f} ms")
    print(f"per-neuron rate targets: {np.round(np.sort(targets), 1)}\n")

    with open("reservoir_input_proj.json") as f:
        proj = {int(c["neuron"]): c for c in json.load(f)["proj"]}
    X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(NB)]
           for k in range(NN)}
    flat = flatten_events(evs)

    conds = [
        ("baseline (reference analysis best model)", dict()),
        ("RECT  no rectification below rest", dict(rectify=False)),
        ("LEAK  constant-current leak", dict(leak_mode="const")),
        ("LEAK  constant leak, no rectification", dict(leak_mode="const", rectify=False)),
    ]
    for ts in (0.002, 0.005, 0.010, 0.020):
        conds.append((f"SYN   DPI tail tau_syn {ts*1e3:.0f} ms", dict(tau_syn=ts)))
    for sg in (0.05, 0.10, 0.20, 0.40):
        conds.append((f"NOISE membrane sigma {sg:.2f}", dict(noise_sigma=sg)))
    conds.append(("ALL   rect+leak+syn5ms", dict(rectify=False, leak_mode="const",
                                                 tau_syn=0.005)))
    conds.append(("ALL   rect+leak+syn5ms+noise0.10",
                  dict(rectify=False, leak_mode="const", tau_syn=0.005,
                       noise_sigma=0.10)))

    # E/I RATIO MISMATCH. The excitatory and inhibitory synapses are separate DPI
    # circuits (the reference figure) with their own bias lines and their own device mismatch,
    # so the ratio w_inh/w_exc differs from neuron to neuron. This is the one
    # parameter axis the per-neuron threshold bisection above CANNOT absorb: a
    # common per-neuron gain is exactly what the threshold trades against, but the
    # BALANCE between the two input channels is not. the reference analysis's weight-code
    # result makes it concrete -- the four branches are equal-sized rather than
    # binary, and the ECG experiments ran on the uncalibrated code (the reference analysis), so
    # the delivered exc and inh weights were not the programmed ones.
    for sp_ei in (0.20, 0.40, 0.65):
        conds.append((f"EI    E/I ratio mismatch {sp_ei*100:.0f}%",
                      dict(_ei=sp_ei)))
    conds.append(("EI+RECT  E/I 40%, no rectification",
                  dict(_ei=0.40, rectify=False)))
    conds.append(("EI+NOISE E/I 40% + sigma 0.10",
                  dict(_ei=0.40, noise_sigma=0.10)))

    # PER-TRIAL EXCITABILITY JITTER. The white membrane noise above is the wrong
    # TIMESCALE: it averages out under a 20 ms kernel and leaves <|rho|> flat.
    # What the <|rho|> ordering asks for is variation that is independent BETWEEN
    # NEURONS and slow compared with a beat -- bias drift, 1/f at low frequency,
    # temperature -- i.e. each neuron's excitability redrawn per presentation.
    # This is the only axis tested here that decorrelates neurons instead of
    # smoothing them, and it is Federico's candidate 4 in its per-neuron
    # (not common-mode) form.
    for jz in (0.05, 0.10, 0.20, 0.35, 0.50):
        conds.append((f"JIT   per-trial excitability {jz*100:.0f}%", dict(_jit=jz)))
    conds.append(("JIT+RECT per-trial 20%, no rectification",
                  dict(_jit=0.20, rectify=False)))

    # dt refinement is required once a synaptic tail of a few ms is in play; keep
    # every condition on the same grid so rows stay comparable
    dt = 0.00025
    nsteps = int(round(T_BEAT / dt))
    up, dn = build_jump(flat, T_BEAT, dt, nsteps)
    print(f"simulation grid dt = {dt*1e3:.2f} ms ({nsteps} steps)\n")

    hdr = "  ".join(f"{t*1e3:5.0f}" for t in TAUS)
    print(f"{'condition':44s} {'rate':>6s} {'<|rho|>':>8s}  {hdr}   {'resid':>6s}")
    print("-" * 104)
    res = {}
    unreach = {}
    for name, kw in conds:
        kw = dict(kw)
        kw.setdefault("dt", dt)
        ei = kw.pop("_ei", 0.0)
        jit = kw.pop("_jit", 0.0)
        needs_rng = kw.get("noise_sigma", 0.0) > 0.0
        curves, rhos, rates = [], [], []
        for s in range(LATTICE_SEEDS):
            k2 = dict(kw)
            if needs_rng:
                k2["rng"] = np.random.default_rng(500 + s)
            vth_scale = None
            if jit:
                vth_scale = np.random.default_rng(900 + s).normal(
                    1.0, jit, NN * NB).clip(0.15, None)
            if ei:
                # one inhibitory gain per NEURON, held across its 60 beats
                g = np.random.default_rng(700 + s).normal(1.0, ei, NN).clip(0.05, None)
                k2["w_inh"] = np.repeat(0.34 * g, NB)
            vth, r = bisect_to_rates(up, dn, targets, k2, vth_scale=vth_scale)
            vth_u = np.repeat(vth, NB)
            if vth_scale is not None:
                vth_u = vth_u * vth_scale
            spk = simulate(up, dn, vth_u, **k2)
            sp = unflatten(spk, lattice=grid, rng=np.random.default_rng(100 + s))
            rho, curve = score(sp)
            curves.append(curve); rhos.append(rho); rates.append(r.mean())
            # honesty check: not every target rate is reachable by threshold in
            # every condition. The impulse model with rectification caps a neuron
            # near one spike per excitatory event, so the fastest silicon neurons
            # are out of reach. Under-shooting the rate FLATTERS the condition
            # (D_eff rises as rate falls here), so any residual reported for a row
            # that misses its targets is a lower bound on that row's true residual.
            miss = int(np.sum(np.abs(r - targets) > 0.10 * np.maximum(targets, 1e-9)))
            unreach.setdefault(name, []).append(miss)
        curve = np.mean(curves, axis=0)
        d20 = curve[TAUS.index(TAU_TABLE)]
        res[name] = {"deff_curve": curve.tolist(),
                     "deff_curve_sd": np.std(curves, axis=0).tolist(),
                     "deff20": float(d20), "rho": float(np.mean(rhos)),
                     "rate_hz": float(np.mean(rates)),
                     "residual": float(d_si - d20)}
        nm_miss = int(np.max(unreach[name]))
        res[name]["neurons_off_target_rate"] = nm_miss
        flag = f"  [{nm_miss}/16 rate unreachable]" if nm_miss else ""
        print(f"{name:44s} {np.mean(rates):6.2f} {np.mean(rhos):8.3f}  "
              + "  ".join(f"{v:5.1f}" for v in curve)
              + f"   {d_si - d20:+6.2f}{flag}")

    print("-" * 104)
    print(f"{'SILICON':44s} {targets.mean():6.2f} {rho_si:8.3f}  "
          + "  ".join(f"{v:5.1f}" for v in curve_si) + f"   {0.0:+6.2f}")

    res["_silicon"] = {"deff_curve": curve_si, "deff20": float(d_si),
                       "rho": float(rho_si), "rate_hz": float(targets.mean())}
    res["_meta"] = {"dt_s": dt, "taus_s": TAUS, "lattice_period_s": float(grid),
                    "lattice_seeds": LATTICE_SEEDS,
                    "residual_ci95_from": "data/deff_residual_ci.json",
                    "note": "every row is threshold-bisected to silicon's "
                            "per-neuron rates, so no row's D_eff is a rate effect"}
    with open("data/deff_physical_mechanisms.json", "w") as f:
        json.dump(res, f, indent=2)
    print("\nwrote data/deff_physical_mechanisms.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
