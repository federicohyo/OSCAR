#!/usr/bin/env python3
"""Task N: does refractory saturation carry the unexplained D_eff residual?

PREMISE TEST FIRST -- and the premise as briefed is FALSE.

The brief: "73% of measured ISIs imply >26 Hz instantaneous, against mean rates of
1.8-15.4 Hz. The array bursts at its refractory ceiling." The two rate figures are
right (`reservoir_spikes_nv_randproj.npz`: per-neuron means 1.81-15.43 Hz, 72.6% of
ISIs below 1/26 s). The inference from them is not, and this script measures why.

Every inter-event interval in ALL THREE ECG recordings is an integer multiple of a
single period of 11.986 ms, to a mean residual of 0.9% of a period, with

  * NO interval at one period -- the shortest is always two, i.e. 23.97 ms;
  * the same period in all three datasets, which were taken on different days with
    different encoders;
  * a per-trial phase concentration R = 0.998, i.e. every spike in a trial lies on
    ONE lattice whose phase is set at trial onset;
  * a per-neuron minimum ISI of 23.20-23.77 ms, identical across all 16 neurons to
    2.5%, in an array whose per-neuron RATES span 8.5x through mismatch.

An analog refractory period cannot do that. An acquisition clock started at trial
onset can, and these three files are all from 2026-07-05, before the 2026-07-10
change to chip Timer0 timestamps (reservoir_run.py:905c46c) -- so they carry HOST
ARRIVAL times, exactly as the reference analysis already says. The recorded
ISI distribution is therefore a measurement of the host read cadence, not of the
neurons. "73% above 26 Hz" is the fraction of intervals at lattice steps 2 and 3.

That does NOT make the mechanism uninteresting -- it makes it a different
mechanism, and one round 2 did not test. Round 2 ruled out a 250 ms blanking dead
time (it would cap the array at 128 events/window against 282 observed) and
modelled 16 ms uniform timestamp quantisation (-1% on D_eff). A 24 ms per-neuron
dead time caps a neuron at 83 events/window, 16 neurons at 1335 -- far above the
282 observed, so it was never excluded by that argument, and its signature is in
the data: 15954 intervals, not one below 23.2 ms.

So this script runs both readings of "refractory", on top of the
operating-point-matched condition (D_eff 12.2, <|rho|> 0.30 at tau = 20 ms):

  R  a genuine NEURON refractory in sim_lif, swept over the values the reference campaign can
     point at: 5 ms (the sim_lif default), 24 ms (this recording's own ISI floor)
     and 38.5 ms (the 26 Hz f-I saturation of the reference figure, a different bias point);
  A  the ACQUISITION LATTICE measured above, applied to the software neuron's
     output exactly as the recording path applied it to silicon's: quantise to the
     11.986 ms grid at a per-trial phase, merge spikes landing in one slot, and
     enforce the two-slot minimum the data show;
  C  comparator coarseness (membrane quantisation + hysteresis);
  F  short-term facilitation.

PROVENANCE
  MEASURED   the lattice period, its residual, the per-neuron ISI floor, and the
             per-neuron rate distribution -- all read off the silicon recording
  DERIVED    per-neuron thresholds, bisected to reproduce the measured rates
             (unchanged from deff_operating_point.py)
  SIMULATED  every ablation condition; C and F in particular have NO measured
             parameter on this die, so they are swept, not calibrated

Run:  ./.venv-meas/bin/python3 deff_refractory_ablation.py
"""
import json

import numpy as np

from reservoir_data import delta_encode_proj
from reservoir_datasets import ACC, DIM, NSV
from reservoir_demo_proj import corr_effdim, load

HW = DIM.path                      # the D_eff recording; every number below is ITS
ALL_HW = [DIM.path, ACC.path, NSV.path]
K = 8
TAUS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
T_BEAT = 2.0
TAU_M, W_EXC, W_INH = 0.02, 0.34, 0.34
TREF_DEFAULT = 0.005
DT = 0.001
SUBMS = 0.001            # the <1 ms cluster is a known packet artefact, excluded


# ---------------------------------------------------------------------------
# premise test
# ---------------------------------------------------------------------------
def isis(sp, drop_subms=True):
    out = []
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            t = np.sort(np.asarray(sp[j, b], dtype=float))
            if len(t) > 1:
                d = np.diff(t)
                out.append(d[d >= SUBMS] if drop_subms else d)
    return np.concatenate([o for o in out if len(o)])


def fit_lattice(d, lo=0.008, hi=0.020, step=2e-6):
    """Period minimising the mean distance of d/period from an integer."""
    best = None
    for g in np.arange(lo, hi, step):
        r = d / g
        s = float(np.abs(r - np.round(r)).mean())
        if best is None or s < best[1]:
            best = (float(g), s)
    return best


def trial_phase_concentration(sp, g):
    r = []
    for j in range(sp.shape[0]):
        for b in range(sp.shape[1]):
            t = np.asarray(sp[j, b], dtype=float)
            if len(t) < 2:
                continue
            ph = (t / g) % 1.0
            r.append(abs(np.mean(np.exp(2j * np.pi * ph))))
    return float(np.mean(r))


def premise_test():
    print("=" * 78)
    print("PREMISE TEST: is the ISI floor a neuron refractory or an acquisition clock?")
    print("=" * 78)
    sp, _, _ = load(HW)
    d = isis(sp)
    rates = np.array([sum(len(np.asarray(sp[j, b])) for b in range(sp.shape[1]))
                      / sp.shape[1] / T_BEAT for j in range(sp.shape[0])])
    print(f"{HW}: per-neuron mean rate {rates.min():.2f}-{rates.max():.2f} Hz "
          f"(CV {rates.std()/rates.mean():.3f}); {len(d)} intervals")
    print(f"  fraction implying >26 Hz (ISI < 38.5 ms): {(d < 1/26.).mean():.3f}"
          "   <- the brief's 73%, reproduced")
    g, res = fit_lattice(d)
    k = np.round(d / g).astype(int)
    print(f"\n  best-fit lattice period      {g*1e3:.3f} ms  (mean |residual| "
          f"{res:.4f} of a period)")
    print(f"  intervals within 0.1 period  {np.mean(np.abs(d/g - k) < 0.1):.4f}")
    hist = {int(v): int(c) for v, c in zip(*np.unique(k[k <= 5], return_counts=True))}
    print(f"  lattice-step histogram k<=5  {hist}   <- no k=1 anywhere")
    print(f"  steps 2+3 as a fraction      {np.mean((k == 2) | (k == 3)):.3f}"
          "   <- this IS the '73%'")
    print(f"  per-trial phase concentration R = {trial_phase_concentration(sp, g):.3f}"
          "   (1 = one lattice per trial)")
    print("\n  per-neuron minimum ISI (ms), against an 8.5x spread in mean rate:")
    mins = []
    for j in range(sp.shape[0]):
        dj = []
        for b in range(sp.shape[1]):
            t = np.sort(np.asarray(sp[j, b], dtype=float))
            if len(t) > 1:
                dd = np.diff(t)
                dj.append(dd[dd >= SUBMS])
        dj = np.concatenate([x for x in dj if len(x)])
        mins.append(dj.min())
    mins = np.array(mins)
    print("    " + " ".join(f"{v*1e3:.1f}" for v in mins))
    print(f"    spread {mins.max()/mins.min():.3f}x  vs  rate spread "
          f"{rates.max()/rates.min():.1f}x")
    print("\n  the same lattice in the other two recordings:")
    for f in ALL_HW[1:]:
        s2, _, _ = load(f)
        d2 = isis(s2)
        g2, r2 = fit_lattice(d2)
        print(f"    {f:44s} {g2*1e3:.3f} ms (resid {r2:.4f}, "
              f"R {trial_phase_concentration(s2, g2):.3f})")
    print("\n  VERDICT: one acquisition lattice, common to three recordings taken on")
    print("  different days with different encoders, phase-locked per trial, with a")
    print("  two-slot minimum. Not 16 mismatched analog refractory periods.")
    return g, float(mins.min())


# ---------------------------------------------------------------------------
# the software neuron, with each mechanism switchable
# ---------------------------------------------------------------------------
def sim_lif_x(events, T, tau_m, vth, vreset, tref, w_exc, w_inh, dt=DT,
              v_quant=0.0, hyst=0.0, fac_tau=0.0, fac_inc=0.0):
    """reservoir_sw_lif.sim_lif with three optional non-idealities.

    v_quant  comparator resolution: the membrane is compared on a grid of this size
    hyst     comparator hysteresis: threshold raised by this fraction for one step
             after a spike (positive-feedback reset)
    fac_tau  short-term facilitation time constant (s); 0 disables
    fac_inc  facilitation increment per input event

    With all four at their defaults this is bit-identical to sim_lif.
    """
    v = 0.0
    last_spike = -1e9
    decay = np.exp(-dt / tau_m)
    nsteps = int(round(T / dt))
    jump = np.zeros(nsteps + 1)
    if fac_tau > 0.0:
        u, fdecay, tprev = 1.0, np.exp(-dt / fac_tau), None
        # facilitation is a state of the SYNAPSE, so it advances on the event
        # timeline, not the membrane grid
        ev = sorted(((tf * T, ch) for tf, ch in events))
        for t, ch in ev:
            if tprev is not None:
                u = 1.0 + (u - 1.0) * np.exp(-(t - tprev) / fac_tau)
            u += fac_inc
            tprev = t
            i = min(nsteps, int(round(t / dt)))
            jump[i] += u * (w_exc if ch == 0 else -w_inh)
        del fdecay
    else:
        for tf, ch in events:
            i = min(nsteps, int(round(tf * T / dt)))
            jump[i] += w_exc if ch == 0 else -w_inh
    out = []
    for i in range(nsteps):
        v = v * decay + jump[i]
        t = i * dt
        if v < 0:
            v = 0.0
        if t - last_spike < tref:
            v = vreset
            continue
        vc = v if v_quant <= 0 else np.floor(v / v_quant) * v_quant
        thr = vth * (1.0 + hyst) if (t - last_spike) < 2 * dt else vth
        if vc >= thr:
            out.append(t)
            v = vreset
            last_spike = t
    return np.array(out)


def apply_lattice(times, grid, phase, min_steps=2):
    """The acquisition path, as measured: snap to the trial's lattice, merge spikes
    that land in one slot, and drop any spike closer than `min_steps` slots to the
    previous surviving one."""
    if len(times) == 0:
        return times
    k = np.round((np.asarray(times) - phase) / grid).astype(int)
    k = np.unique(k)                        # one report per slot
    keep = [k[0]]
    for kk in k[1:]:
        if kk - keep[-1] >= min_steps:
            keep.append(kk)
    return phase + np.array(keep) * grid


# ---------------------------------------------------------------------------
def build_condition(evs, vths, tref=TREF_DEFAULT, lattice=None, rng=None,
                    min_steps=2, **kw):
    """One (neuron, beat) pair is one presentation in reservoir_run.py, so the
    lattice phase is drawn per pair -- which is what the silicon recording shows
    (per-trial phase concentration 0.998, no phase shared across neurons)."""
    n, nb = len(vths), len(evs[0])
    sp = np.empty((n, nb), dtype=object)
    for j in range(n):
        for b in range(nb):
            st = sim_lif_x(evs[j][b], T_BEAT, TAU_M, vths[j], 0.0, tref,
                           W_EXC, W_INH, **kw)
            if lattice is not None:
                st = apply_lattice(st, lattice, rng.uniform(0, lattice), min_steps)
            sp[j, b] = st
    return sp


def score(sp):
    return (float(corr_effdim(sp, T_BEAT, K, "exp", 0.02)[1]),
            [float(corr_effdim(sp, T_BEAT, K, "exp", t)[2]) for t in TAUS])


def rate_of(sp):
    return float(np.mean([sum(len(sp[j, b]) for b in range(sp.shape[1]))
                          / sp.shape[1] / T_BEAT for j in range(sp.shape[0])]))


def main():
    grid, isi_floor = premise_test()

    # --- the operating-point-matched starting condition, reused verbatim -------
    op = np.load("sw_proj_opdispersion.npz", allow_pickle=True)
    vths = op["vths"]
    proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
    b = np.load("beats_nv60_orig.npz", allow_pickle=True)
    X = b["X"]
    evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                                 theta=proj[k]["theta"]) for i in range(len(X))]
           for k in range(16)}

    print("\n" + "=" * 78)
    print("ABLATION: each mechanism ON TOP OF the operating-point-matched condition")
    print("=" * 78)
    rng = np.random.default_rng(0)

    conds = []
    conds.append(("op-matched (baseline)", dict()))
    # R -- a genuine neuron refractory
    conds.append(("+ refractory 10 ms", dict(tref=0.010)))
    conds.append((f"+ refractory {isi_floor*1e3:.0f} ms (recording ISI floor)",
                  dict(tref=float(np.round(isi_floor, 5)))))
    conds.append(("+ refractory 38.5 ms (26 Hz f-I sat.)", dict(tref=1 / 26.)))
    # A -- the acquisition lattice actually present in the recording, in two halves:
    #      the timing quantisation on its own (which does not change the rate at
    #      all) and the two-slot floor that deletes events
    conds.append((f"+ lattice timing only {grid*1e3:.1f} ms",
                  dict(lattice=grid, rng=np.random.default_rng(1), min_steps=1)))
    conds.append((f"+ acquisition lattice {grid*1e3:.1f} ms (full)",
                  dict(lattice=grid, rng=np.random.default_rng(1))))
    conds.append(("+ lattice + refractory 24 ms",
                  dict(lattice=grid, rng=np.random.default_rng(2),
                       tref=float(np.round(isi_floor, 5)))))
    # C -- comparator coarseness
    for q in (0.05, 0.20):
        conds.append((f"+ comparator quantisation {q:.2f} V_th", dict(v_quant=q)))
    conds.append(("+ comparator hysteresis 0.20", dict(hyst=0.20)))
    # F -- short-term facilitation
    for tf_ in (0.010, 0.050, 0.200):
        conds.append((f"+ facilitation tau_f {tf_*1e3:.0f} ms", dict(fac_tau=tf_, fac_inc=0.15)))

    hdr = "  ".join(f"{t*1e3:5.0f}" for t in TAUS)
    print(f"{'condition':42s} {'rate':>6s} {'<|rho|>':>8s}  {hdr}")
    res = {}
    for name, kw in conds:
        sp = build_condition(evs, vths, **kw)
        rho, deff = score(sp)
        res[name] = {"rho": rho, "deff": deff, "rate_hz": rate_of(sp)}
        print(f"{name:42s} {rate_of(sp):6.2f} {rho:8.2f}  "
              + "  ".join(f"{v:5.1f}" for v in deff))

    for nm, f in [("SILICON", HW)]:
        sp, _, TT = load(f)
        rho, deff = score(sp)
        res[nm] = {"rho": rho, "deff": deff, "rate_hz": rate_of(sp)}
        print(f"{nm:42s} {rate_of(sp):6.2f} {rho:8.2f}  "
              + "  ".join(f"{v:5.1f}" for v in deff))

    i20 = TAUS.index(0.02)
    base = res["op-matched (baseline)"]["deff"][i20]
    si = res["SILICON"]["deff"][i20]

    # -----------------------------------------------------------------------
    # THE CONTROL THAT DECIDES THE ABLATION.
    #
    # Every mechanism above that raises D_eff also LOWERS the output rate, and the
    # op-matched baseline overshoots silicon's mean rate (11.4 Hz against 8.8). So
    # a mechanism could look explanatory purely by making the neuron quieter. We
    # therefore build a family that changes NOTHING but the rate -- a common scale
    # on all 16 thresholds -- and read each mechanism's D_eff against the D_eff
    # that family reaches at the SAME output rate. The excess over that curve is
    # the part of the effect that is not simply a rate change.
    # -----------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("RATE CONTROL: threshold-only family (no mechanism, rate alone)")
    print("=" * 78)
    fam_r, fam_d = [], []
    print(f"{'threshold scale':42s} {'rate':>6s} {'<|rho|>':>8s} {'Deff@20ms':>10s}")
    for s in (0.85, 1.0, 1.03, 1.06, 1.09, 1.12, 1.15, 1.20, 1.30, 1.50, 1.75, 2.0, 2.5):
        sp = build_condition(evs, vths * s)
        rho, deff = score(sp)
        fam_r.append(rate_of(sp))
        fam_d.append(deff[i20])
        print(f"  x{s:<40.2f} {fam_r[-1]:6.2f} {rho:8.2f} {fam_d[-1]:10.1f}")
    order = np.argsort(fam_r)
    fam_r = np.array(fam_r)[order]
    fam_d = np.array(fam_d)[order]
    res["_rate_control"] = {"rate_hz": fam_r.tolist(), "deff20": fam_d.tolist()}

    def expected(r):
        return float(np.interp(r, fam_r, fam_d))

    print(f"\nAt tau = 20 ms: op-matched {base:.1f}, silicon {si:.1f}, "
          f"raw residual {si-base:.1f} D_eff units.")
    print(f"Silicon's own rate is {res['SILICON']['rate_hz']:.2f} Hz, where the "
          f"threshold-only family reaches {expected(res['SILICON']['rate_hz']):.1f};")
    print(f"the RATE-MATCHED residual is therefore "
          f"{si - expected(res['SILICON']['rate_hz']):.1f} D_eff units.\n")
    print(f"{'mechanism':42s} {'rate':>6s} {'Deff':>6s} {'rate-only':>10s} "
          f"{'excess':>7s} {'share':>7s}")
    si_excess = si - expected(res["SILICON"]["rate_hz"])
    for name in list(res):
        if name.startswith("_") or name == "op-matched (baseline)":
            continue
        r = res[name]["rate_hz"]
        d = res[name]["deff"][i20]
        ex = d - expected(r)
        res[name]["excess_over_rate_control"] = ex
        tag = "" if name == "SILICON" else f"{100*ex/si_excess:+6.0f}%"
        print(f"  {name:40s} {r:6.2f} {d:6.1f} {expected(r):10.1f} {ex:+7.2f} {tag:>7s}")

    res["_meta"] = {
        "lattice_period_s": grid,
        "isi_floor_s": isi_floor,
        "taus_s": TAUS,
        "provenance": {
            "lattice_period_s": "MEASURED on reservoir_spikes_nv_randproj.npz",
            "isi_floor_s": "MEASURED, smallest per-neuron ISI over the recording",
            "thresholds": "DERIVED, bisected in deff_operating_point.py",
            "comparator and facilitation parameters": "SIMULATED -- no measured "
                                                      "value exists on this die",
        },
    }
    json.dump(res, open("data/deff_refractory_ablation.json", "w"), indent=2)
    print("\nwrote data/deff_refractory_ablation.json")


if __name__ == "__main__":
    raise SystemExit(main())
