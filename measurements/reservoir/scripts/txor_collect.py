#!/usr/bin/env python3
"""T-XOR on-chip collection (approach a: recurrent reservoir, time-multiplexed).

Each neuron is recorded ONE AT A TIME with its own tuned `_rec.biases` (which embed rec_w/rec_cnt
from the GUI) and a self-loop (SETRECUR k->k) -> a self-recurrent unit. The per-neuron late-window
responses are concatenated offline into one linear readout. Recurrence (RECURCTRL 1) provides the
MEMORY that carries bit a (early) to the late window; feedforward (RECURCTRL 0) forgets it.

Stimulus (temporal XOR): bit a in an early window (EXC, so it seeds firing the self-loop can hold),
bit b in a late window with a per-neuron RANDOM exc/inh sign (fixed seeded projection = reservoir
diversity). Readout window is AFTER bit b, so feedforward (no memory of a) is at chance while
recurrence solves it. Label = a XOR b.

MASKING: only the recorded neuron is streamed (MASK = 1<<k); all others masked (they still run in
the array, they just cost no AER bandwidth) -> no drops/stalls from jamming neurons.

    ./.venv-meas/bin/python3 txor_collect.py --neurons 0-15 --per-cell 12 --out data/txor/txor_collect.npz
"""
import argparse, os, time, json, queue
import numpy as np
from meas_common import BridgeSession, load_biases
from reservoir_synthtask import make_trials

REC_SYN = 1
BIAS_PAT = "ofxXORtuning/bin/bias_synapse_characterization_super_n{k}_jul10_rec.biases"


def parse_neurons(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def read_rec_params(path):
    """rec_w, rec_cnt embedded in the _rec.biases JSON by the GUI (default 8/2 if absent)."""
    try:
        d = json.load(open(path))
        return int(d.get("rec_w", 8)), int(d.get("rec_cnt", 2))
    except Exception:
        return 8, 2


def present(b, k, a, bit_b, b_exc, T, winA, winB, burst):
    """Temporal stimulus on neuron k: bit a EXC in winA, bit b (exc/inh per b_exc) in winB.
    Record k's spike times over [0,T] (readout window is chosen offline, after winB)."""
    b.drain(max_lines=200000)
    times = []
    t0 = time.time()

    def collect(until):
        while time.time() < until:
            try:
                line = b.out_q.get(timeout=0.002)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3 and p[1].isdigit() and int(p[1]) == k:
                    times.append(time.time() - t0)

    collect(t0 + winA[0])
    if a:
        b.route(0, k, exc=True); b.fire(burst)        # bit a: EXC seed (early)
    collect(t0 + winB[0])
    if bit_b:
        b.route(0, k, exc=b_exc); b.fire(burst)        # bit b: per-neuron sign (late)
    collect(t0 + T)
    return np.array(times)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neurons", default="0-15")
    ap.add_argument("--per-cell", type=int, default=12)
    ap.add_argument("--T", type=float, default=1.5)
    ap.add_argument("--winA", default="0.1,0.25")     # bit a (early)
    ap.add_argument("--winB", default="0.6,0.75")     # bit b (late); gap ~0.35 s
    ap.add_argument("--burst", type=int, default=12)
    ap.add_argument("--in-weight", type=int, default=15)
    ap.add_argument("--proj-seed", type=int, default=42, help="fixed random b-sign projection")
    ap.add_argument("--out", default="data/txor/txor_collect.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    neurons = parse_neurons(args.neurons)
    winA = tuple(float(x) for x in args.winA.split(","))
    winB = tuple(float(x) for x in args.winB.split(","))
    rng = np.random.default_rng(0)
    _, ab, labels, groups = make_trials(args.per_cell, args.T, args.burst, 0.0, rng)
    y = labels["XOR"].astype(int)
    ntr = len(ab)
    if args.smoke:
        idx = np.concatenate([np.where((ab[:, 0]*2+ab[:, 1]) == c)[0][:2] for c in range(4)])
        ab, y, groups = ab[idx], y[idx], groups[idx]; ntr = len(ab); neurons = neurons[:2]
    # fixed per-neuron b-sign projection (0=exc,1=inh); bit a is always exc
    prng = np.random.default_rng(args.proj_seed)
    b_sign = {k: int(prng.integers(0, 2)) for k in neurons}
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    ff = np.empty((16, ntr), object); rec = np.empty((16, ntr), object)
    for arr in (ff, rec):
        for k in range(16):
            for t in range(ntr):
                arr[k, t] = np.array([])
    done, recparams = [], {}

    def save():
        tmp = args.out + ".tmp.npz"
        np.savez(tmp, spikes_ff=ff, spikes_rec=rec, labels=y, bits_ab=ab, groups=groups,
                 neurons=np.array(neurons), b_sign=np.array([b_sign[k] for k in neurons]),
                 T=args.T, winA=np.array(winA), winB=np.array(winB), done=np.array(done, int),
                 coding="txor_recurrent_reservoir")
        os.replace(tmp, args.out)

    print(f"T-XOR collect: {len(neurons)} neurons, {ntr} trials, winA={winA} winB={winB} "
          f"gap={winB[0]-winA[1]:.2f}s, proj_seed={args.proj_seed}")
    with BridgeSession() as b:
        for k in neurons:
            b.send(f"MASK 0x{(1 << k):04X}")               # stream ONLY neuron k
            bp = BIAS_PAT.format(k=k)
            rec_w, rec_cnt = read_rec_params(bp)
            recparams[k] = (rec_w, rec_cnt)
            b.apply_biases(load_biases(bp)); b.monitor(k); time.sleep(0.8)
            b.program_weight(0, args.in_weight, exc=True)
            b.program_weight(0, args.in_weight, exc=False)
            b.program_weight(REC_SYN, rec_w, exc=True)
            b.send(f"SETRECUR {k} {k} {rec_cnt} 1")
            be = (b_sign[k] == 0)                            # bit-b sign for this neuron
            # warm-up (discard) to clear the post-routing settling transient
            b.send("RECURCTRL 1"); time.sleep(0.15)
            present(b, k, 1, 1, be, args.T, winA, winB, args.burst)
            for cond, arr in (("ff", ff), ("rec", rec)):
                rc = 1 if cond == "rec" else 0

                def reset_present(a, bb):
                    # clear reverberation (toggle recurrence off->on), then present
                    b.send("RECURCTRL 0"); time.sleep(0.12)
                    b.send(f"RECURCTRL {rc}"); time.sleep(0.04)
                    return present(b, k, a, bb, be, args.T, winA, winB, args.burst)

                b.send(f"RECURCTRL {rc}"); time.sleep(0.15)
                prev = None
                for t in range(ntr):
                    corner = (int(ab[t, 0]), int(ab[t, 1]))
                    if corner != prev:            # warm-up trials after each routing change
                        reset_present(*corner); reset_present(*corner)   # 2 discarded settles
                        prev = corner
                    arr[k, t] = reset_present(*corner)
            b.send("RECURCTRL 0")
            done.append(int(k))
            tot_ff = sum(len(ff[k, t]) for t in range(ntr))
            tot_rec = sum(len(rec[k, t]) for t in range(ntr))
            print(f"  n{k:2d} (b->{'exc' if be else 'inh'}, rW={rec_w} c={rec_cnt}): "
                  f"ff {tot_ff} spk, rec {tot_rec} spk")
            if not args.smoke:
                save()
        b.send("MASK 0xFFFF")                               # restore: stream all
    if not args.smoke:
        save(); print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
