#!/usr/bin/env python3
"""Deterding Vowel on the chip: test whether spike-count noise limits a nonlinear reservoir.

Vowel is the real XOR-analogue (linear ~0.65/0.77, RBF ~0.94/0.95 -- nonlinearity REQUIRED).
The software de-risk says a LIF reservoir CAN lift it, but the chip's spike-COUNT readout
adds Poisson noise (~1/sqrt(count)) that may cap it. This physically tests that.

Method (chip as the nonlinear activation, one neuron at a time -- as chosen):
  - host random projections give each reservoir feature j a drive  d_js = P[j] . x_s.
  - present d_js to a chip neuron as a BASELINE exc bias burst + a SIGNED burst
    (exc if d>0, inh if d<0), read the neuron's OUTPUT SPIKE COUNT = the nonlinear feature.
  - N_features features (spread across the 16 physical neurons for mismatch diversity),
    optionally averaged over `reps` presentations to trade bench time for less count noise.
  - offline: StandardScaler + LogisticRegression, StratifiedKFold. Compare to the 0.77
    linear baseline and the 0.95 RBF ceiling.

    CARAVAN_CLK_MHZ=10 ./.venv-meas/bin/python3 reservoir_run_vowel.py --smoke   # calibrate
    CARAVAN_CLK_MHZ=10 ./.venv-meas/bin/python3 reservoir_run_vowel.py --features 64 --reps 1
"""
import argparse
import os
import time
import numpy as np

from meas_common import BridgeSession, load_biases
from reservoir_run import present_delta

# PER-NEURON tuned biases, exactly as the ECG runs (reservoir_run.py) use them: each neuron k
# is stimulated under its OWN operating point where it fires well.
BIAS_PATTERN = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases"
WIN = (0.30, 0.55)     # coincident burst window (fraction of T); bias + drive compete here


def load_vowel(pair):
    from sklearn import datasets as skd
    from sklearn.preprocessing import StandardScaler
    d = skd.fetch_openml("vowel", version=2, as_frame=True, parser="liac-arff")
    X = d.frame[[f"Feature_{i}" for i in range(10)]].to_numpy(float)
    y = d.frame["Class"].to_numpy()
    if pair:
        a, b = pair.split(",")
        m = np.isin(y, [a, b]); X, y = X[m], (y[m] == b).astype(int)
    Xs = StandardScaler().fit_transform(X)
    return Xs, y


def burst(nspk, chan, T, rng):
    lo, hi = WIN
    if nspk <= 0:
        return []
    ts = rng.uniform(lo, hi, int(nspk))
    return [(float(t), chan) for t in ts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", default="hYd,had", help="binary vowel pair (empty=all 11 classes)")
    ap.add_argument("--features", type=int, default=64, help="number of reservoir features")
    ap.add_argument("--reps", type=int, default=1, help="average over reps presentations (less noise)")
    ap.add_argument("--bias-burst", type=int, default=20, help="baseline exc spikes (sets the f-I midpoint)")
    ap.add_argument("--drive-scale", type=float, default=6.0, help="spikes per unit |drive|")
    ap.add_argument("--weight", type=int, default=15)
    ap.add_argument("--jexc-boost", type=float, default=0.06,
                    help="add to JExcWn0..3 ONLY for neurons NOT in --live-neurons (wakes the "
                         "ones dead at 10 MHz; live ones stay at their tuned _jul10 point)")
    ap.add_argument("--live-neurons", default="1,2,5,6,7,13",
                    help="neurons already responsive at baseline (get NO boost)")
    ap.add_argument("--T", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-samples", type=int, default=0, help="balanced subset of samples (0=all)")
    ap.add_argument("--save-shots", action="store_true",
                    help="save each rep's count separately -> offline accuracy-vs-reps curve")
    ap.add_argument("--out", default="vowel_chip.npz")
    ap.add_argument("--skip-bias", action="store_true",
                    help="use the DACs already programmed (run_neuron_test) instead of loading BIAS")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    Xs, y = load_vowel(args.pair)
    if args.max_samples and args.max_samples < len(y):     # balanced subset (reproducible)
        srng = np.random.default_rng(12345)
        per = args.max_samples // len(set(y.tolist()))
        sel = np.concatenate([srng.choice(np.where(y == c)[0], per, replace=False)
                              for c in sorted(set(y.tolist()))])
        srng.shuffle(sel); Xs, y = Xs[sel], y[sel]
    rng = np.random.default_rng(args.seed)
    NF = args.features
    P = rng.standard_normal((NF, Xs.shape[1]))
    P /= np.linalg.norm(P, axis=1, keepdims=True)          # unit-norm projections
    drives = Xs @ P.T                                       # (n_samples, NF)
    neuron_of = [j % 16 for j in range(NF)]                 # spread features over 16 neurons

    if args.smoke:
        # a few features x a few samples, report counts + timing + does count track drive
        Xs, y = Xs[:6], y[:6]; drives = drives[:6]; NF = 4; neuron_of = [0, 5, 9, 14]

    live = set(int(x) for x in args.live_neurons.split(",") if x != "")
    n = len(y)
    feats = np.zeros((n, NF))
    shots = np.zeros((args.reps, NF, n)) if args.save_shots else None   # per-rep counts
    traces = np.empty((NF, n), dtype=object)          # full HW spike-time trace per presentation
    for j in range(NF):
        for s in range(n):
            traces[j, s] = np.array([])
    done_set = set()
    if not args.smoke and os.path.exists(args.out):   # RESUME: reuse already-captured features
        try:
            d = np.load(args.out, allow_pickle=True)
            if d["feats"].shape == feats.shape:
                feats = d["feats"]; done_set = set(int(x) for x in d["done"])
                if "traces" in d.files and d["traces"].shape == traces.shape:
                    traces = d["traces"]
                print(f"RESUME: {len(done_set)}/{NF} features already captured, skipping them")
        except Exception as e:
            print(f"(could not resume from {args.out}: {e})")
    print(f"vowel chip: pair={args.pair} n={n} features={NF} reps={args.reps} "
          f"T={args.T} bias_burst={args.bias_burst} drive_scale={args.drive_scale}")
    print(f"drive range [{drives.min():.2f},{drives.max():.2f}] std {drives.std():.2f} "
          f"-> burst up to ~{int(args.drive_scale*abs(drives).max())} spikes")
    t0 = time.time()
    done = list(done_set)
    with BridgeSession() as b:
        cur_n = None
        for j in range(NF):
            if j in done_set:                          # already captured (resume)
                continue
            k = neuron_of[j]
            if k != cur_n:
                if not args.skip_bias:                       # per-neuron tuned bias, as ECG
                    bd = load_biases(BIAS_PATTERN.format(k=k))
                    boost = 0.0 if k in live else args.jexc_boost   # ONLY boost unresponsive ones
                    for i in range(4):
                        bd[f"JExcWn{i}"] = min(0.85, bd.get(f"JExcWn{i}", 0.30) + boost)
                    b.apply_biases(bd)
                b.monitor(k); time.sleep(0.6)
                b.program_weight(0, args.weight, exc=True)
                b.program_weight(0, args.weight, exc=False)
                cur_n = k
            proj = j // 16                                    # which projection block (0..3)
            # DIVERSITY: exc and inh have different dynamics. Odd projections use a HIGH
            # exc baseline (neuron spikes spontaneously) that inhibition CARVES DOWN, so the
            # feature responds via inhibitory dynamics -- complementary to the low-baseline,
            # excitation-driven even projections. Two dynamical regimes -> higher-D expansion.
            inh_driven = (proj % 2 == 1)
            base = args.bias_burst * (3 if inh_driven else 1)
            for s in range(n):
                d = drives[s, j]
                acc = 0
                last_st = np.array([])
                for rp in range(args.reps):
                    ev = burst(base, 0, args.T, rng)
                    if inh_driven:                            # high baseline, drive via inh (down) / exc (up)
                        if d >= 0:
                            ev += burst(round(args.drive_scale * d), 1, args.T, rng)   # inh: carve down
                        else:
                            ev += burst(round(args.drive_scale * -d), 0, args.T, rng)  # exc: push up
                    else:                                     # low baseline, excitation-driven
                        if d >= 0:
                            ev += burst(round(args.drive_scale * d), 0, args.T, rng)   # exc
                        else:
                            ev += burst(round(args.drive_scale * -d), 1, args.T, rng)  # inh
                    ev.sort(key=lambda x: x[0])
                    st = present_delta(b, k, ev, args.T, 0, 0)
                    acc += len(st); last_st = st
                    if shots is not None:
                        shots[rp, j, s] = len(st)
                feats[s, j] = acc / args.reps
                traces[j, s] = last_st                        # save the raw HW spike trace
            done.append(j)
            if args.smoke:
                col = feats[:, j]
                print(f"  feat {j} (neuron {k}): drives {np.round(drives[:n,j],2)} -> "
                      f"counts {np.round(col,1)}  (mean {col.mean():.1f})")
            else:
                el = time.time() - t0
                eta = el / len(done) * (NF - len(done))
                print(f"  feature {j+1}/{NF} (neuron {k}) done, {el/60:.1f} min elapsed, "
                      f"~{eta/60:.0f} min left", flush=True)
                extra = {"shots": shots} if shots is not None else {}
                np.savez(args.out + ".tmp.npz", feats=feats, traces=traces, y=y,
                         done=np.array(done), drives=drives, neuron_of=np.array(neuron_of),
                         T=args.T, pair=args.pair, **extra)
                os.replace(args.out + ".tmp.npz", args.out)

    if args.smoke:
        # does the output count track the drive? (monotonic f-I => usable feature)
        allc = feats.flatten(); alld = drives[:n, :NF].flatten()
        r = np.corrcoef(alld, allc)[0, 1]
        print(f"\ncount-vs-drive correlation (want strongly +, monotonic f-I): {r:+.2f}")
        print(f"per-presentation time: {(time.time()-t0)/(NF*n):.2f} s")
        print(f"=> full run {args.features} feat x {len(load_vowel(args.pair)[1])} samp x {args.reps} reps"
              f" ~ {(time.time()-t0)/(NF*n)*args.features*len(load_vowel(args.pair)[1])*args.reps/3600:.1f} h")
    else:
        print(f"wrote {args.out} ({NF} features x {n} samples), {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    raise SystemExit(main())
