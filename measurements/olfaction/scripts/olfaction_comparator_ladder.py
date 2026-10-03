#!/usr/bin/env python3
"""Calibrate the spike-count comparator ladder: one vleakn per switching level.

The array can act as a bank of threshold comparators on spike COUNT. Three things had to
be right, and all three came from F. Corradi:

  * the on-chip pulse EXTENDER (vepulseextp) sets the real spike length at the synapse --
    the LA pulse only triggers it. Shortening it puts one event below saturation so
    events sum instead of one spike saturating the membrane.
  * coincidence_1_n14 as the starting point, and a raised excitatory weight, which lifts
    the ramp clear of the noise floor: 20 -> 299 mV over N = 0..32, monotone.
  * vleakn moves the RESTING potential, not just the leak rate, so it slides the whole
    ramp against a fixed threshold. vthrdn is inert on this path (ten e-folds, no effect).

So the switching count is set by vleakn at about a millivolt per level. This bisects
vleakn per target level and writes one bias file each.

Every point carries an N=0 control: as rest approaches threshold the neuron eventually
free-runs, and a free-running neuron reads as a perfect comparator if you do not check.

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_comparator_ladder.py
"""
import argparse, json, os, random, time

from meas_common import BridgeSession, load_biases

LEV = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32]


def pf(b, k, n, reps):
    g = 0
    for _ in range(reps):
        b.drain(max_lines=100000)
        if n > 0:
            b.send(f"BURST {n}")
        time.sleep(0.12)                      # 45 ms undercounts; P ceilings near 0.8
        c = [0] * 16
        for _ in range(3):
            b.drain(c); time.sleep(0.02)
        g += 1 if c[k] > 0 else 0
    return g / reps


def ladder(b, k, reps):
    """P(fire) over the count ladder, shuffled, plus the N=0 control."""
    p0 = pf(b, k, 0, reps)
    order = random.Random(9).sample(LEV, len(LEV))
    r = {n: pf(b, k, n, reps) for n in order}
    ps = [r[n] for n in LEV]
    sw = next((n for n, q in zip(LEV, ps) if q >= 0.5), None)
    return p0, ps, sw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--base", default="ofxCaravanViewer/bin/ramp_comparator_fed.biases")
    ap.add_argument("--targets", default="1,2,4,8,16,32")
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--lo", type=float, default=0.2530, help="vleakn low bound (V)")
    ap.add_argument("--hi", type=float, default=0.2621, help="vleakn high bound (V)")
    ap.add_argument("--iters", type=int, default=7)
    ap.add_argument("--outdir", default="ofxCaravanViewer/bin")
    ap.add_argument("--out", default="data/olfaction_comparator_ladder.json")
    args = ap.parse_args()
    k = args.neuron
    base = load_biases(args.base)
    targets = [int(x) for x in args.targets.split(",")]
    print(f"neuron {k}, base {os.path.basename(args.base)}, "
          f"vleakn {base['vleakn']:.4f}")
    print(f"bisecting vleakn in [{args.lo:.4f}, {args.hi:.4f}] for levels {targets}\n")

    found, trace = {}, []
    with BridgeSession() as b:
        b.send(f"MASK {1 << k}")
        for tgt in targets:
            lo, hi = args.lo, args.hi
            best = None
            print(f"--- target N>={tgt} ---")
            for _ in range(args.iters):
                v = 0.5 * (lo + hi)
                bi = dict(base); bi["vleakn"] = v
                b.apply_biases(bi); b.monitor(k); time.sleep(0.85)
                b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)
                b.send("PULSEFINE 1"); time.sleep(0.06)
                p0, ps, sw = ladder(b, k, args.reps)
                b.send("PULSEFINE 0")
                trace.append(dict(target=tgt, vleakn=v, p0=p0, p=ps, switch=sw))
                lab = "free-runs" if p0 > 0.3 else (f"N>={sw}" if sw else "never")
                print(f"  vleakn {v:.4f} -> {lab:<10} (N=0 {p0:.2f})")
                if p0 > 0.3:            # rest too high: back off
                    lo = v
                elif sw is None:        # never fires: rest too low
                    hi = v
                elif sw > tgt:          # switches too late
                    hi = v
                elif sw < tgt:          # switches too early
                    lo = v
                else:
                    best = dict(vleakn=v, p0=p0, p=ps, switch=sw); break
                # p0 <= 0.3 is REQUIRED here, not only in the branch above: a
                # free-running neuron fires at N=1, so switch==1 matches a target of 1
                # and this fallback would record it as a perfect comparator. That is
                # exactly what the N=0 control exists to prevent, and it slipped past
                # once already.
                if (sw is not None and p0 <= 0.3
                        and (best is None or abs(sw - tgt) < abs(best["switch"] - tgt))):
                    best = dict(vleakn=v, p0=p0, p=ps, switch=sw)
            if best:
                found[tgt] = best
                exact = "exact" if best["switch"] == tgt else f"closest N>={best['switch']}"
                print(f"  -> vleakn {best['vleakn']:.4f}  {exact}")
                bi = dict(base); bi["vleakn"] = best["vleakn"]
                path = os.path.join(args.outdir, f"comparator_n{k}_lvl{tgt}.biases")
                with open(path, "w") as f:
                    f.write("{\n" + ",\n".join(f'  "{a}": {c}' for a, c in bi.items())
                            + "\n}\n")
                print(f"  -> wrote {os.path.basename(path)}")
            else:
                print(f"  -> no vleakn found for N>={tgt}")
            json.dump({"neuron": k, "base": args.base, "levels": LEV,
                       "found": {str(t): v for t, v in found.items()}, "trace": trace},
                      open(args.out, "w"), indent=2)
    print(f"\n{len(found)}/{len(targets)} levels placed; wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
