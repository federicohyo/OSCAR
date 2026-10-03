"""Positive control for the mechanism search: can it detect a KNOWN large effect?

A search that returns "nothing" is only informative if it would have said something
had there been something. The per-neuron input projection is the one manipulation
whose effect on D_eff is established (3.6 -> 9.6 in the published decomposition), so
run the identical harness with the projection REMOVED -- every neuron driven by the
same shared delta stream -- and check the harness sees it collapse.
"""
import json, sys
import numpy as np
sys.path.insert(0, "/storage/tue/avlsi2024-sw")
import deff_physical_mechanisms as M
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

IT = M.TAUS.index(M.TAU_TABLE)
sp_si, _, _ = load("reservoir_spikes_ref25_expanded_2026-08-12.npz")
nb = sp_si.shape[1]; M.NB = nb
targets = M.silicon_rates(sp_si)
proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
X = np.load("beats_nv160_16rec.npz", allow_pickle=True)["X"]

for lab, per_neuron in (("per-neuron projection (as searched)", True),
                        ("SHARED input (projection removed)", False)):
    evs = {k: [delta_encode_proj(
        X[i], sigma=proj[k if per_neuron else 0]["sigma"],
        shift=proj[k if per_neuron else 0]["shift"],
        theta=proj[k if per_neuron else 0]["theta"]) for i in range(nb)]
        for k in range(M.NN)}
    up, dn = build_jump(M.flatten_events(evs), T_BEAT, DT_DEFAULT,
                        int(round(T_BEAT / DT_DEFAULT)))
    kw = dict(tau_syn=0.020)
    vth, _ = M.bisect_to_rates(up, dn, targets, kw, hi=200.0)
    sp = M.unflatten(simulate(up, dn, np.repeat(vth, nb), **kw))
    d = corr_effdim(sp, T_BEAT, 8, "exp", M.TAU_TABLE)[2]
    print(f"  {lab:38s} D_eff(20ms) {d:6.2f}")
