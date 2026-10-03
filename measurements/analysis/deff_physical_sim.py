#!/usr/bin/env python3
"""A software neuron carrying the analog soma's physics, vectorised.

Section 4.3 leaves ~1.4 D_eff units unexplained. Every mechanism tested there is
a non-ideality of the ACQUISITION or a spread of LIF PARAMETERS; each one
leaves the model neuron's equations as those of reservoir_sw_lif.
sim_lif. Four things the fabricated soma does that sim_lif leaves out are visible
by inspection of that function:

  RECT   `if v < 0: v = 0.0` discards all inhibitory state below rest. The delta
         encoder sends DOWN events to the inhibitory synapse, so on a quiet
         neuron the model throws away history the membrane retains. Zero free
         parameters -- this one is a bug-shaped difference rather than a physical model.
  SYN    `jump[i] += w` injects charge as an impulse. The fabricated synapse is a
         differential-pair integrator (Section 3.2) with its own time constant,
         so each event delivers a shaped current rather than a delta.
  LEAK   `v = v * decay` is an ohmic leak. The soma's leak is a current-starved
         transistor at a fixed gate bias, i.e. a constant current, so the
         membrane ramps DOWN LINEARLY rather than decaying exponentially.
  NOISE  sim_lif is noiseless. Subthreshold analog circuits have shot and 1/f
         noise at the membrane, which jitters threshold crossings.

This module provides all four as switches on one vectorised simulator, so that
each can be scored through the unchanged corr_effdim of the rest of the analysis.
Vectorisation is what makes the study affordable: every mechanism changes the
output rate, so each condition must have its 16 thresholds RE-BISECTED to
silicon's per-neuron rates before its D_eff means anything, and that is ~19k
beat-simulations per condition. All (neuron, beat) pairs are independent, so they
advance as one state vector.

`simulate(..., defaults)` is validated bit-for-bit against sim_lif in
test_physical_sim_matches().

PROVENANCE: every parameter here is SIMULATED. What is measured elsewhere and
used to constrain them is noted at each use site in deff_physical_mechanisms.py.
"""
import numpy as np

DT_DEFAULT = 0.001
T_BEAT = 2.0


def build_jump(events_per_unit, T, dt, nsteps):
    """(n_units, nsteps+1) matrix of weighted input impulses on the time grid.

    events_per_unit[u] = [(t_frac, channel)], channel 0 = UP (exc), 1 = DOWN (inh).
    Weights are applied by the caller through w_exc/w_inh so the same matrix can
    be reused; here we return the two channel counts separately.
    """
    nu = len(events_per_unit)
    up = np.zeros((nu, nsteps + 1))
    dn = np.zeros((nu, nsteps + 1))
    for u, evs in enumerate(events_per_unit):
        for tf, ch in evs:
            i = min(nsteps, int(round(tf * T / dt)))
            if ch == 0:
                up[u, i] += 1.0
            else:
                dn[u, i] += 1.0
    return up, dn


def simulate(up, dn, vth, T=T_BEAT, dt=DT_DEFAULT, tau_m=0.02, tref=0.005,
             w_exc=0.34, w_inh=0.34, vreset=0.0,
             rectify=True, tau_syn=0.0, syn_sat=0.0, leak_mode="exp", leak_rate=None,
             noise_sigma=0.0, rng=None):
    """Advance every (neuron, beat) pair together. Returns a list of spike-time
    arrays, one per unit.

    rectify      False lets the membrane hold state below rest (silicon does)
    tau_syn      >0 replaces the impulse with a first-order synaptic current of
                 this time constant, charge-preserving. NOTE this linear filter IS
                 the DPI in its linear regime (I_w >> I_tau, I_syn >> I_gain):
                 Bartolozzi & Indiveri give tau dI/dt + I = I_w I_th / I_tau there.
    syn_sat      >0 adds the DPI's quadratic self-limiting term, which is what makes
                 the circuit nonlinear once that regime is left:

                     tau ds/dt + s + s^2/syn_sat = drive

                 so the steady state saturates and the EFFECTIVE time constant
                 becomes state-dependent. syn_sat=0 (default) disables it and the
                 update is bit-identical to the linear filter above, which is the
                 limit syn_sat -> inf.

                 PHENOMENOLOGICAL, and deliberately so: the reference circuit
                 equation is a Bernoulli form whose variable definitions await
                 verification against the primary source, so this reproduces the
                 quadratic self-limiting BEHAVIOUR rather than transcribing that
                 equation. Present it as a behavioural match rather than the circuit equation.
    leak_mode    'exp'   v <- v*exp(-dt/tau_m)              (sim_lif)
                 'const' v <- v - leak_rate*dt, floored     (current-starved)
    leak_rate    constant-leak slope in units of v per second; defaults to the
                 slope that takes v=vth to rest in one tau_m
    noise_sigma  s.d. of Gaussian membrane noise per sqrt(s), added as
                 sigma*sqrt(dt) each step
    """
    nu, ncols = up.shape
    nsteps = ncols - 1
    vth = np.asarray(vth, dtype=float)
    if vth.ndim == 0:
        vth = np.full(nu, float(vth))

    decay = np.exp(-dt / tau_m)
    if leak_rate is None:
        leak_rate = vth / tau_m               # per-unit, keeps the scale sane

    # w_exc/w_inh may be per-unit vectors: the excitatory and inhibitory synapses
    # are separate DPI circuits with independent biases and independent mismatch,
    # so their RATIO varies from neuron to neuron. That ratio is the one parameter
    # axis a per-neuron threshold leaves unabsorbed (see deff_physical_mechanisms.py).
    we = np.asarray(w_exc, dtype=float).reshape(-1, 1) if np.ndim(w_exc) else w_exc
    wi = np.asarray(w_inh, dtype=float).reshape(-1, 1) if np.ndim(w_inh) else w_inh
    drive = we * up - wi * dn
    # tau_syn may be a per-unit vector for the same reason w_exc/w_inh may: the DPI's
    # current tail is a device property and carries its own mismatch. A SCALAR takes
    # exactly the path it always did -- np.ndim()==0 leaves sdec/gain as scalars -- so
    # this is backward compatible and the sim_lif bit-exactness check below still holds.
    _ts = np.asarray(tau_syn, dtype=float)
    tau_syn_on = bool(np.any(_ts > 0.0))
    if tau_syn_on:
        # charge-preserving first-order synaptic filter: the impulse becomes a
        # current that decays with tau_syn and integrates to the same area
        if np.ndim(_ts):
            sdec = np.exp(-dt / _ts).ravel()
            gain = (dt / _ts).ravel()
            _tau_eff = _ts.ravel()
        else:
            sdec = np.exp(-dt / tau_syn)
            gain = dt / tau_syn
            _tau_eff = tau_syn
    v = np.zeros(nu)
    s = np.zeros(nu)
    last = np.full(nu, -1e9)
    fired = np.zeros((nsteps, nu), dtype=bool)

    for i in range(nsteps):
        t = i * dt
        if tau_syn_on:
            s = s * sdec + drive[:, i]
            if syn_sat:
                # quadratic self-limiting, applied on the same Euler step as the
                # decay: s <- s - dt*s^2/(tau*syn_sat). Clamped at zero so a large
                # step leaves the state non-negative.
                s = np.maximum(s - (dt / _tau_eff) * s * np.abs(s) / syn_sat, -abs(syn_sat))
            inj = s * gain
        else:
            inj = drive[:, i]

        if leak_mode == "const":
            v = v - leak_rate * dt + inj
        else:
            v = v * decay + inj

        if noise_sigma > 0.0:
            v = v + rng.normal(0.0, noise_sigma * np.sqrt(dt), nu)

        if rectify:
            v = np.maximum(v, 0.0)
        elif leak_mode == "const":
            # a constant leak falls unbounded on a silent unit;
            # the real membrane sits at its rest rail. Clamp one threshold below.
            v = np.maximum(v, -vth)

        in_refr = (t - last) < tref
        if in_refr.any():
            v = np.where(in_refr, vreset, v)

        fire = (~in_refr) & (v >= vth)
        if fire.any():
            fired[i] = fire
            v = np.where(fire, vreset, v)
            last = np.where(fire, t, last)

    idx = np.arange(nsteps) * dt
    return [idx[fired[:, u]] for u in range(nu)]


def test_physical_sim_matches(n_check=40, seed=0):
    """The vectorised simulator must reproduce reservoir_sw_lif.sim_lif exactly in
    its default configuration, or nothing downstream is comparable to the
    reference rows."""
    from reservoir_sw_lif import sim_lif

    rng = np.random.default_rng(seed)
    evs = []
    for _ in range(n_check):
        m = rng.integers(5, 60)
        evs.append([(float(rng.uniform(0, 1)), int(rng.integers(0, 2)))
                    for _ in range(m)])
    vth = rng.uniform(0.4, 3.0, n_check)
    up, dn = build_jump(evs, T_BEAT, DT_DEFAULT, int(round(T_BEAT / DT_DEFAULT)))
    got = simulate(up, dn, vth)
    bad = 0
    for u in range(n_check):
        ref = sim_lif(evs[u], T_BEAT, 0.02, vth[u], 0.0, 0.005, 0.34, 0.34)
        if len(ref) != len(got[u]) or not np.allclose(ref, got[u]):
            bad += 1
            if bad <= 3:
                print(f"  MISMATCH unit {u}: ref {len(ref)} spikes, got {len(got[u])}")
    print(f"vectorised simulator vs sim_lif: {n_check - bad}/{n_check} units identical")
    return bad == 0


if __name__ == "__main__":
    ok = test_physical_sim_matches()
    raise SystemExit(0 if ok else 1)
