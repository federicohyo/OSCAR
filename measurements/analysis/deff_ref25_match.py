import json, sys
import numpy as np
sys.path.insert(0, "/storage/tue/avlsi2024-sw")
from reservoir_data import delta_encode_proj
from reservoir_demo_proj import corr_effdim, load
from deff_physical_mechanisms import (silicon_rates, flatten_events, unflatten,
                                      bisect_to_rates, NN, NB, TAUS)
from deff_physical_sim import build_jump, simulate, T_BEAT, DT_DEFAULT

sp_si, _, _ = load("reservoir_spikes_ref25_2026-08-12.npz")
targets = silicon_rates(sp_si)
proj = {int(c["neuron"]): c for c in json.load(open("reservoir_input_proj.json"))["proj"]}
X = np.load("beats_nv60_orig.npz", allow_pickle=True)["X"]
evs = {k: [delta_encode_proj(X[i], sigma=proj[k]["sigma"], shift=proj[k]["shift"],
                             theta=proj[k]["theta"]) for i in range(NB)] for k in range(NN)}
nsteps = int(round(T_BEAT / DT_DEFAULT))
up, dn = build_jump(flatten_events(evs), T_BEAT, DT_DEFAULT, nsteps)

out = {}
for ts in (0.010, 0.015, 0.020, 0.030):
    kw = dict(tau_syn=ts)
    vth, ach = bisect_to_rates(up, dn, targets, kw, hi=200.0)
    miss = np.abs(ach - targets) / np.maximum(targets, 1e-9)
    sp_sw = unflatten(simulate(up, dn, np.repeat(vth, NB), **kw))
    curve = [corr_effdim(sp_sw, T_BEAT, 8, "exp", t)[2] for t in TAUS]
    r = np.mean([sum(len(np.asarray(sp_sw[j,b])) for b in range(NB))/NB/T_BEAT for j in range(NN)])
    print(f"tau_syn {ts*1e3:4.0f} ms: matched rate {r:5.1f} Hz (target {targets.mean():.1f}), "
          f"{int((miss>0.2).sum())}/16 off by >20%,  D_eff(20ms) {curve[1]:5.1f}")
    out[f"tau_syn_{ts}"] = {"deff": curve, "rate": float(r),
                            "n_off": int((miss>0.2).sum())}
si = [corr_effdim(sp_si, T_BEAT, 8, "exp", t)[2] for t in TAUS]
print(f"SILICON REF25                                                        "
      f"       D_eff(20ms) {si[1]:5.1f}")
out["silicon"] = {"deff": si, "rate": float(targets.mean())}
json.dump(out, open("data/deff_ref25_match.json", "w"), indent=2)
print("\nwrote data/deff_ref25_match.json")
