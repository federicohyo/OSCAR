"""An impulse-driven LIF cannot exceed 1 spike per input event, whatever the
threshold: each instantaneous jump crosses threshold at most once before reset.
Silicon reaches 2.08x because the DPI synapse has a TAIL -- charge delivered over
time, so one event can drive several crossings. simulate() models that with
tau_syn>0, which is the condition deff_physical_mechanisms already calls
"SYN DPI tail". Test whether it unlocks REF25's rates."""
import json, sys
import numpy as np
sys.path.insert(0, "/storage/tue/avlsi2024-sw")
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_mechanisms import silicon_rates, flatten_events, unflatten, NN, NB, TAUS
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

sp_si, _, _ = load("reservoir_spikes_ref25_2026-08-12.npz")
targets = silicon_rates(sp_si)
proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                             theta=proj[k]["theta"]) for i in range(NB)] for k in range(NN)}
nsteps = int(round(T_BEAT / DT_DEFAULT))
up, dn = build_jump(flatten_events(evs), T_BEAT, DT_DEFAULT, nsteps)

def rates(kw, vth):
    out = simulate(up, dn, np.repeat(np.full(NN, vth), NB), **kw)
    return np.array([sum(len(out[k*NB+b]) for b in range(NB))/NB/T_BEAT for k in range(NN)])

print(f"silicon REF25 target: mean {targets.mean():.1f} Hz, max {targets.max():.1f} Hz")
print(f"{'condition':34s} {'max achievable Hz':>18}   (thresholds driven to floor)")
for lab, kw in [("impulse (as published)", dict()),
                ("DPI tail tau_syn 5 ms",  dict(tau_syn=0.005)),
                ("DPI tail tau_syn 10 ms", dict(tau_syn=0.010)),
                ("DPI tail tau_syn 20 ms", dict(tau_syn=0.020))]:
    r = rates(kw, 0.02)
    print(f"{lab:34s} {r.mean():8.1f} mean {r.max():7.1f} max")
