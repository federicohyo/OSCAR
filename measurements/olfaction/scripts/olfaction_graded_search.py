#!/usr/bin/env python3
"""Search the bias space for a GRADED spike-count comparator.

A previous pass concluded such an operating point lies beyond this die. That claim came
from sweeping three channels out of twenty-four, mostly one at a time along lines, and it
was overstated (F. Corradi: "there are so many bias settings available and
you have just explored one or two"). The membrane saturating at a fixed plateau is what a
FAST synapse does; whether it accumulates is governed by the synaptic time constant, which
stayed untouched.

Channels searched, and why each is in:
  d_JExc   all four weight branches together -- charge per input event (NMOS: higher=more)
  d_vthrdn threshold                                        (NMOS: higher = harder to fire)
  d_vtaup  SYNAPTIC time constant. PMOS, so HIGHER voltage = LESS current = SLOWER decay
           = charge persists between spikes. The knob the earlier pass missed entirely.
  d_vtaun  the NMOS tau                                     (higher = more current = faster)
  d_vepext excitatory pulse extension, charge per spike     (PMOS: lower = wider = more)

Objective, measured over a burst-count ladder: P(fire | N=16) - P(fire | N=1), penalised
if the low end already fires. A graded comparator has P(1) near zero and P(16) near one;
the cliff we kept finding has both at one, scoring zero.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_graded_search.py
"""
import argparse, json, time
import numpy as np

from meas_common import BridgeSession, load_biases
from narma_tuner import Channel, ConstrainedBO, channels_to_dict

LEVELS = (1, 2, 3, 4, 6, 8, 12, 16)


def apply(base, off):
    b = dict(base)
    for j in range(4):
        k = f"JExcWn{j}"
        if k in b:
            b[k] = b[k] + off["d_JExc"]
    for name, key in (("vthrdn", "d_vthrdn"), ("vtaup", "d_vtaup"),
                      ("vtaun", "d_vtaun"), ("vepulseextp", "d_vepext")):
        if name in b:
            b[name] = b[name] + off[key]
    return b


def ladder(b, k, reps, mult):
    ps = []
    for n in LEVELS:
        g = 0
        for _ in range(reps):
            b.drain(max_lines=100000)
            b.send(f"BURST {n}")
            time.sleep(0.045)
            c = [0] * 16
            b.drain(c)
            g += 1 if c[k] > 0 else 0
        ps.append(g / reps)
    return ps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--iters", type=int, default=45)
    ap.add_argument("--reps", type=int, default=8)
    ap.add_argument("--mult", type=int, default=12)
    ap.add_argument("--span", type=float, default=0.060)
    ap.add_argument("--out", default="data/olfaction_graded_search.json")
    args = ap.parse_args()
    k = args.neuron

    ch = [Channel("d_JExc", 0.0, args.span), Channel("d_vthrdn", 0.0, args.span),
          Channel("d_vtaup", 0.0, 0.120), Channel("d_vtaun", 0.0, args.span),
          Channel("d_vepext", 0.0, args.span)]
    bo = ConstrainedBO(ch, seed=0)
    base = load_biases(f"ofxCaravanViewer/bin/bias_ref2_25mhz_n{k}.biases")
    hist, best = [], None
    print(f"neuron {k}, burst ladder {LEVELS}, pulse_mult {args.mult}, {args.reps} reps")
    print("objective = P(fire|16) - P(fire|1), penalised if the low end already fires\n")
    print(f"{'it':>3} {'dJExc':>7} {'dvthr':>7} {'dvtaup':>7} {'dvtaun':>7} {'dvpx':>7} "
          f"{'P(1)':>6} {'P(16)':>6} {'obj':>7}")
    with BridgeSession() as b:
        b.send(f"MASK {1 << k}")
        b.send(f"PULSEMULT {args.mult}")
        for i in range(args.iters):
            x = np.zeros(len(ch)) if i == 0 else bo.ask()
            off = channels_to_dict(ch, x)
            b.apply_biases(apply(base, off)); b.monitor(k); time.sleep(0.55)
            b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.04)
            ps = ladder(b, k, args.reps, args.mult)
            spread = ps[-1] - ps[0]
            obj = spread - (0.6 * max(0.0, ps[0] - 0.2))
            bo.tell(x, obj)
            rec = dict(x=off, ps=ps, spread=float(spread), obj=float(obj))
            hist.append(rec)
            star = ""
            if best is None or obj > best["obj"]:
                best = rec; star = "  <-- best"
            print(f"{i:3d} {off['d_JExc']*1000:+6.0f}m {off['d_vthrdn']*1000:+6.0f}m "
                  f"{off['d_vtaup']*1000:+6.0f}m {off['d_vtaun']*1000:+6.0f}m "
                  f"{off['d_vepext']*1000:+6.0f}m {ps[0]:6.2f} {ps[-1]:6.2f} {obj:7.3f}{star}")
            json.dump({"history": hist, "best": best, "levels": list(LEVELS)},
                      open(args.out, "w"), indent=2)
        b.send("PULSEMULT 1")
    print(f"\nBEST spread {best['spread']:.2f}: P(fire|N) = "
          + " ".join(f"{p:.2f}" for p in best["ps"]))
    print("  at " + ", ".join(f"{n[2:]} {v*1000:+.0f}mV" for n, v in best["x"].items()))
    amb = sum(1 for p in best["ps"] if 0.1 < p < 0.9)
    print(f"  intermediate levels: {amb} of {len(LEVELS)}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    raise SystemExit(main())
