"""Vowel reservoir with DELIBERATE bias-set diversity, all in ONE session (no drift).

Record 16 neurons x R input-projections under M bias operating modes, back-to-back in one
BridgeSession. Concatenating the modes should add ORTHOGONAL nonlinear features (unlike
accidental session drift) -> higher D_eff -> linear readout climbs toward RBF. Saves
per-(mode,feature,sample) counts; scored offline.

    CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 reservoir_vowel_multibias.py --out vowel_multibias.npz
"""
import argparse, os, time
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_run import present_delta

BP = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases"
WIN = (0.30, 0.55)
# diverse operating modes (chosen from bias_fi_scan.py: base moderate, lo-leak high-baseline,
# hi-leak sharp-threshold, hi-gain strong). NMOS higher V = more current.
MODES = {
    "base":    {},
    "lo-leak": {"vleakn": -0.05},
    "hi-leak": {"vleakn": +0.06},
    "hi-gain": {"JExcWn0": +0.05, "JExcWn1": +0.05, "JExcWn2": +0.05, "JExcWn3": +0.05},
}


def load_vowel(pair, max_samples):
    from sklearn import datasets as skd
    from sklearn.preprocessing import StandardScaler
    d = skd.fetch_openml("vowel", version=2, as_frame=True, parser="liac-arff")
    X = d.frame[[f"Feature_{i}" for i in range(10)]].to_numpy(float)
    y = d.frame["Class"].to_numpy()
    a, b = pair.split(","); m = np.isin(y, [a, b]); X, y = X[m], (y[m] == b).astype(int)
    Xs = StandardScaler().fit_transform(X)
    if max_samples and max_samples < len(y):
        r = np.random.default_rng(12345); per = max_samples // 2
        sel = np.concatenate([r.choice(np.where(y == c)[0], per, replace=False) for c in (0, 1)])
        r.shuffle(sel); Xs, y = Xs[sel], y[sel]
    return Xs, y


def burst(nb, ch, rng):
    return [(float(t), ch) for t in rng.uniform(*WIN, int(nb))] if nb > 0 else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", default="hYd,had")
    ap.add_argument("--projections", type=int, default=2, help="input projections per mode (x16 neurons)")
    ap.add_argument("--max-samples", type=int, default=90)
    ap.add_argument("--modes", default="base,lo-leak,hi-leak,hi-gain")
    ap.add_argument("--bias-burst", type=int, default=45)
    ap.add_argument("--drive-scale", type=float, default=22.0)
    ap.add_argument("--T", type=float, default=0.8)
    ap.add_argument("--out", default="vowel_multibias.npz")
    args = ap.parse_args()

    Xs, y = load_vowel(args.pair, args.max_samples)
    n = len(y)
    modes = [m for m in args.modes.split(",") if m in MODES]
    R = args.projections
    rng = np.random.default_rng(0)
    P = rng.standard_normal((16 * R, Xs.shape[1])); P /= np.linalg.norm(P, axis=1, keepdims=True)
    drives = Xs @ P.T                                  # (n, 16*R)
    neuron_of = [j % 16 for j in range(16 * R)]
    NF = 16 * R * len(modes)
    feats = np.zeros((n, NF)); done = []
    print(f"multibias: {n} samples, {R} proj x 16 neurons x {len(modes)} modes = {NF} features "
          f"({modes})", flush=True)
    t0 = time.time()
    with BridgeSession() as b:
        col = 0
        for mi, mode in enumerate(modes):
            delta = MODES[mode]
            for j in range(16 * R):                    # feature within a mode
                k = neuron_of[j]
                bd = load_biases(BP.format(k=k))
                for kk, dv in delta.items():
                    bd[kk] = float(np.clip(bd.get(kk, 0.3) + dv, 0.0, 1.78))
                b.apply_biases(bd); b.monitor(k); time.sleep(0.5)
                b.program_weight(0, 15, exc=True); b.program_weight(0, 15, exc=False)
                proj = j // 16
                inh = (proj % 2 == 1)
                base = args.bias_burst * (3 if inh else 1)
                for s in range(n):
                    d = drives[s, j]
                    ev = burst(base, 0, rng)
                    if inh:
                        ev += burst(round(args.drive_scale * d), 1, rng) if d >= 0 else burst(round(args.drive_scale * -d), 0, rng)
                    else:
                        ev += burst(round(args.drive_scale * d), 0, rng) if d >= 0 else burst(round(args.drive_scale * -d), 1, rng)
                    feats[s, col] = len(present_delta(b, k, sorted(ev, key=lambda x: x[0]), args.T, 0, 0))
                done.append(col); col += 1
                el = time.time() - t0
                print(f"  mode {mode} feat {j+1}/{16*R} (col {col}/{NF}) done, "
                      f"{el/60:.1f} min, ~{el/len(done)*(NF-len(done))/60:.0f} left", flush=True)
                np.savez(args.out + ".tmp.npz", feats=feats, y=y, done=np.array(done),
                         modes=np.array(modes), R=R, drives=drives)
                os.replace(args.out + ".tmp.npz", args.out)
    print(f"wrote {args.out} ({NF} feat x {n} samples), {(time.time()-t0)/60:.1f} min", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
