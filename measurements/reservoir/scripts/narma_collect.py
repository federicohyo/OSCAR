#!/usr/bin/env python3
"""NARMA on-chip collection (cross-coupled reservoir) -- PROBE-IDENTICAL readout.

Rewritten 2026-07-25. The previous version read state by parsing host-side out_q "S " lines over a
0.1s window; under MASK-all-16 + recurrence that queue backlogs and smears per-step spike
attribution, so the per-timestep u(t) correlation was destroyed (collected MC0~=0 even though the
live NARMAPROBE reached MC0~=0.47). This version delegates the whole per-step loop to the bridge's
`NARMACOLLECT` command, which reuses the EXACT NARMAPROBE drive + `_live_counts` snapshot readout
(robust, bridge-side), so the collection input/readout path is identical to the tuning probe by
construction. ff and rec use the same fixed-seed u stream.

The bridge streams one `NARMAROW t u c0..c15` per step and a final
`NARMACOLLECTDONE M mc0 mc1 mc2 rate` -- the MC is measured on the 2nd half of the FULL long stream,
so long-stream saturation (which the 90-step probe cannot see) is reported directly. Watch that
mc0/mc1 stay up and rate stays bounded; if rate climbs and mc0 collapses the reservoir is
saturating -> lower rec_w / raise membrane tau at the bench (tune live with NARMAPROBE first).

    ./.venv-meas/bin/python3 narma_collect.py \
        --bias ofxNARMATuning/bin/bias_synapse_characterization_narma.biases \
        --L 800 --tstep 0.1 --out data/narma/narma_collect.npz
"""
import argparse, os, json, time
import numpy as np
from meas_common import BridgeSession, load_biases

IN_NEURONS = list(range(8))


def collect_cond(b, recur, M, tstep_ms, kmax, dens, rec_w, in_w, timeout_s, stall_s=25.0):
    """Send NARMACOLLECT and read the streamed rows until NARMACOLLECTDONE. Returns (state, u, done).
    A slow-but-progressing stream (AER stalls -> ~4x slower) is tolerated up to timeout_s; a TRUE
    jam (no new row for stall_s) aborts fast instead of hanging on the full timeout."""
    b.send(f"NARMACOLLECT {1 if recur else 0} {M} {tstep_ms} {kmax} {dens} {rec_w} {in_w}")
    state = np.zeros((M, 16), int)
    u = np.zeros(M)
    seen = np.zeros(M, bool)
    done = None
    deadline = time.time() + timeout_s
    last_progress = time.time()
    while time.time() < deadline:
        try:
            line = b.out_q.get(timeout=1.0)
        except Exception:
            if time.time() - last_progress > stall_s:
                break                                      # no rows for stall_s -> jammed, give up
            continue
        if line.startswith("NARMAROW "):
            p = line.split()
            t = int(p[1])
            if 0 <= t < M:
                u[t] = float(p[2])
                state[t] = [int(x) for x in p[3:19]]
                seen[t] = True
                last_progress = time.time()
        elif line.startswith("NARMACOLLECTDONE"):
            done = line
            break
        elif line.startswith("ERROR"):
            raise RuntimeError(f"bridge: {line}")
    if done is None:
        raise TimeoutError(f"NARMACOLLECT (recur={recur}) stalled; got {int(seen.sum())}/{M} rows")
    if not seen.all():
        print(f"  WARNING: {int((~seen).sum())}/{M} rows missing (filled 0)")
    return state, u, done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias", default="ofxNARMATuning/bin/bias_synapse_characterization_narma.biases")
    ap.add_argument("--L", type=int, default=800, help="stream length (timesteps)")
    ap.add_argument("--washout", type=int, default=100, help="discard first N timesteps (offline)")
    ap.add_argument("--tstep", type=float, default=0.1, help="timestep duration (s)")
    ap.add_argument("--kmax", type=int, default=8, help="input spikes at u=0.5")
    ap.add_argument("--in-weight", type=int, default=15)
    ap.add_argument("--out", default="data/narma/narma_collect.npz")
    args = ap.parse_args()

    meta = json.load(open(args.bias))
    dens = int(meta.get("narma_dens", 15)); rec_w = int(meta.get("narma_rec_w", 10))
    tstep_ms = int(round(args.tstep * 1000))
    timeout_s = args.L * args.tstep * 4 + 60       # tolerate up to ~4x AER slowdown before giving up
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    print(f"NARMA collect (probe-identical): L={args.L}, tstep={args.tstep}s, dens={dens}, "
          f"rec_w={rec_w}, bias={args.bias}")

    states = {}; us = {}
    with BridgeSession() as b:
        b.apply_biases(load_biases(args.bias)); time.sleep(1.0)
        for cond, recur in (("ff", 0), ("rec", 1)):
            t0 = time.time()
            st, u, done = collect_cond(b, recur, args.L, tstep_ms, args.kmax, dens, rec_w,
                                       args.in_weight, timeout_s)
            states[cond] = st; us[cond] = u
            print(f"  {cond}: {done.strip()}  ({time.time()-t0:.0f}s)")

    if not np.allclose(us["ff"], us["rec"]):
        print("  NOTE: ff/rec u streams differ (unexpected) -- saving rec's u")
    u = us["rec"]
    np.savez(args.out, state_ff=states["ff"], state_rec=states["rec"], u=u,
             tstep=args.tstep, washout=args.washout, dens=dens, rec_w=rec_w,
             in_neurons=np.array(IN_NEURONS), coding="narma_reservoir")
    print("wrote", args.out)
    print("score offline: ./.venv-meas/bin/python3 data/plots/score_narma.py", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
