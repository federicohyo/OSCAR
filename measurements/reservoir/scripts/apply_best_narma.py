#!/usr/bin/env python3
"""Take the best operating point found by tune_narma.py and (optionally) re-collect + score it.

Reads a tuner log (data/narma/tune_sess2.json), picks the best FEASIBLE point by J (falls back to
best overall if none feasible), overlays its tuned channels onto the base narma biases, and writes a
ready-to-load `.biases` file (preserving narma_dens/narma_rec_w). With --run it then drives the chip:
a long ff-vs-rec NARMACOLLECT at that point (narma_collect.py) and NRMSE scoring (score_narma.py).

    # just write the tuned bias file + print the next commands:
    ./.venv-meas/bin/python3 apply_best_narma.py --log data/narma/tune_sess2.json

    # write it AND re-collect (L=800) + score on the chip (tuner must have finished -> FTDI free):
    CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 apply_best_narma.py --log data/narma/tune_sess2.json --run
"""
import argparse, json, os, subprocess, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="data/narma/tune_sess2.json")
    ap.add_argument("--base", default="ofxNARMATuning/bin/bias_synapse_characterization_narma.biases")
    ap.add_argument("--out-bias", default="data/narma/best_tuned.biases")
    ap.add_argument("--out-npz", default="data/narma/narma_collect_tuned.npz")
    ap.add_argument("--L", type=int, default=800, help="final collection stream length")
    ap.add_argument("--run", action="store_true", help="also collect + score on the chip")
    ap.add_argument("--topk", type=int, default=5, help="print this many best points")
    args = ap.parse_args()

    log = json.load(open(args.log))
    if not log:
        sys.exit("empty log")
    feas = [e for e in log if e.get("feasible")]
    pool = feas if feas else log
    ranked = sorted(pool, key=lambda e: e["J"], reverse=True)
    best = ranked[0]

    print(f"{len(log)} iterations, {len(feas)} feasible. Top {min(args.topk,len(ranked))} by J"
          f"{' (feasible)' if feas else ' (NONE feasible -> best overall)'}:")
    print(f"{'it':>4} {'J':>7} {'mc0':>5} {'mc1':>5} {'mc2':>5} {'rate':>5} {'nlive':>5}")
    for e in ranked[:args.topk]:
        mc = e["mc"]
        print(f"{e['it']:4d} {e['J']:7.3f} {mc[0]:5.2f} {mc[1]:5.2f} {mc[2]:5.2f} "
              f"{e['rate']:5.2f} {e['n_live']:5d}")

    base = json.load(open(args.base))
    merged = dict(base)
    merged.update({k: float(v) for k, v in best["theta"].items()})   # overlay tuned channels
    # keep the reservoir wiring meta the collector reads
    for k in ("narma_dens", "narma_rec_w"):
        if k in base:
            merged[k] = base[k]
    os.makedirs(os.path.dirname(args.out_bias), exist_ok=True)
    with open(args.out_bias, "w") as f:
        json.dump(merged, f, indent=1)
    print(f"\nBest point (it {best['it']}, J={best['J']:.3f}, {best['n_live']} live, "
          f"mc={[round(x,3) for x in best['mc']]}):")
    print("  " + ", ".join(f"{k}={v:.4f}" for k, v in best["theta"].items()))
    print(f"wrote tuned biases -> {args.out_bias}")

    collect = ["./.venv-meas/bin/python3", "narma_collect.py", "--bias", args.out_bias,
               "--L", str(args.L), "--out", args.out_npz]
    score = ["./.venv-meas/bin/python3", "data/plots/score_narma.py", args.out_npz]
    if not args.run:
        print("\nNext (chip must be free of the tuner):")
        print("  CARAVAN_CLK_MHZ=50 " + " ".join(collect))
        print("  " + " ".join(score))
        return 0

    print("\n>> collecting on chip ...", flush=True)
    env = dict(os.environ); env.setdefault("CARAVAN_CLK_MHZ", "50")
    r = subprocess.run(collect, env=env)
    if r.returncode != 0:
        sys.exit(f"collection stopped before completion (rc={r.returncode})")
    print("\n>> scoring ff vs rec ...", flush=True)
    subprocess.run(score)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
