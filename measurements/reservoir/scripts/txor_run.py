#!/usr/bin/env python3
"""Temporal-XOR ON-CHIP via firmware SETRECUR recurrence (Phase 2). Two bits are presented at
DIFFERENT times to a bank of input neurons; the label is a XOR b. The readout uses a LATE window
(after both bits) so a FEEDFORWARD network -- which has forgotten bit a by then -- scores chance
on the a*b interaction, while ON-DIE RECURRENCE (self-loops, tuned REC_SYN weight ~7,
count 2) sustains bit a's trace into the late window so a LINEAR readout separates XOR.

Recurrence is a NETWORK property -> all input neurons run simultaneously under ONE global bias
(unlike the one-neuron-at-a-time XOR dim run). Bit a -> exc/inh per neuron sign pattern in window
A; bit b in window B; membranes carry state across the gap; read ALL 16 over the whole trial
(late-window readout chosen offline). Runs feedforward (RECURCTRL 0) and recurrent (RECURCTRL 1)
back-to-back on the same trials. Raw spikes saved -> offline scoring (score_txor.py).

    ./.venv-meas/bin/python3 txor_run.py --bias ofxCaravanViewer/bin/bias_reservoir.biases \
        --rec-weight 7 --rec-count 2 --per-cell 10 --out data/txor/txor_run.npz
"""
import argparse, os, time, queue
import numpy as np
from meas_common import BridgeSession, load_biases

REC_SYN = 1
# per-neuron (chan_a, chan_b): 0=exc, 1=inh. a-exc/b-inh detects (1,0); a-inh/b-exc detects (0,1);
# a-exc/b-exc is a summation unit. Recurrence sustains the early bit into the late readout window.
SIGN_PATTERNS = [(0, 1), (1, 0), (0, 0)]


def make_trials(per_cell, rng):
    ab, grp = [], []
    for a in (0, 1):
        for b in (0, 1):
            for r in range(per_cell):
                ab.append((a, b)); grp.append(r)
    ab = np.array(ab)
    order = rng.permutation(len(ab))
    return ab[order], np.array(grp)[order]


def present(b, a, bit_b, in_neurons, patt, T, winA, winB, burst, jitter, rng):
    """Present bit a in winA and bit b in winB to the input neurons (exc/inh per pattern),
    reading ALL 16 neurons over [0,T]. Returns dict neuron->spike times (s, host-relative)."""
    b.drain(max_lines=200000)
    times = {k: [] for k in range(16)}
    t0 = time.time()

    def collect(until):
        while time.time() < until:
            try:
                line = b.out_q.get(timeout=0.002)
            except queue.Empty:
                continue
            if line.startswith("S "):
                p = line.split()
                if len(p) >= 3 and p[1].isdigit():
                    nid = int(p[1])
                    if 0 <= nid <= 15:
                        times[nid].append(time.time() - t0)

    # build (t_frac, neuron, exc) events for both bits
    events = []
    for bit, win, chsel in ((a, winA, 0), (bit_b, winB, 1)):
        if not bit:
            continue
        lo, hi = win
        for idx, k in enumerate(in_neurons):
            ch = patt[idx][chsel]                      # 0 exc / 1 inh for this neuron & bit
            for _ in range(burst):
                t = float(np.clip(rng.uniform(lo, hi) + jitter * rng.standard_normal(), 0, T))
                events.append((t, k, ch == 0))
    events.sort(key=lambda e: e[0])
    for tf, k, exc in events:
        collect(t0 + tf)
        b.route(0, k, exc=exc)                          # syn0 exc or inh -> neuron k
        b.fire()
    collect(t0 + T)                                     # includes the late readout window
    return {k: np.array(times[k]) for k in range(16)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias", default="ofxCaravanViewer/bin/bias_reservoir.biases")
    ap.add_argument("--in-neurons", default="0,1,2,3,4,5,6,7")
    ap.add_argument("--per-cell", type=int, default=10)
    ap.add_argument("--T", type=float, default=1.5)
    ap.add_argument("--winA", default="0.1,0.25")       # bit a (early)
    ap.add_argument("--winB", default="0.6,0.75")       # bit b (late); gap ~0.35 s
    ap.add_argument("--burst", type=int, default=6)
    ap.add_argument("--jitter", type=float, default=0.02)
    ap.add_argument("--weight", type=int, default=15)   # input synapse
    ap.add_argument("--rec-weight", type=int, default=7)
    ap.add_argument("--rec-count", type=int, default=2)
    ap.add_argument("--reset-vleakn", type=float, default=0.35)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="data/txor/txor_run.npz")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    in_neurons = [int(x) for x in args.in_neurons.split(",")]
    patt = [SIGN_PATTERNS[i % len(SIGN_PATTERNS)] for i in range(len(in_neurons))]
    winA = tuple(float(x) for x in args.winA.split(","))
    winB = tuple(float(x) for x in args.winB.split(","))
    rng = np.random.default_rng(args.seed)
    ab, grp = make_trials(args.per_cell, rng)
    if args.smoke:
        ab, grp = ab[:8], grp[:8]
    y = (ab[:, 0] ^ ab[:, 1]).astype(int)
    biases = load_biases(args.bias); op_vl = biases.get("vleakn", 0.26)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    print(f"T-XOR on-chip: {len(ab)} trials, in={in_neurons}, winA={winA} winB={winB} "
          f"gap={winB[0]-winA[1]:.2f}s, rec_w={args.rec_weight} cnt={args.rec_count}, bias={args.bias}")

    spikes = {"ff": np.empty((16, len(ab)), object), "rec": np.empty((16, len(ab)), object)}
    with BridgeSession() as b:
        b.apply_biases(biases); time.sleep(1.0)
        b.program_weight(0, args.weight, exc=True)
        b.program_weight(0, args.weight, exc=False)
        b.program_weight(REC_SYN, args.rec_weight, exc=True)
        b.program_weight(REC_SYN, args.rec_weight, exc=False)
        for k in in_neurons:                            # self-loop memory on each input neuron
            b.send(f"SETRECUR {k} {k} {args.rec_count} 1")
        for cond in ("ff", "rec"):
            b.send(f"RECURCTRL {1 if cond=='rec' else 0}"); time.sleep(0.2)
            print(f"  --- condition {cond} ---")
            for bi in range(len(ab)):
                st = present(b, int(ab[bi, 0]), int(ab[bi, 1]), in_neurons, patt,
                             args.T, winA, winB, args.burst, args.jitter, rng)
                for k in range(16):
                    spikes[cond][k, bi] = st[k]
                # reset: raise vleakn to discharge membranes + kill reverberation between trials
                b.bias("vleakn", args.reset_vleakn); time.sleep(0.08)
                b.bias("vleakn", op_vl); time.sleep(0.05)
                if bi % 8 == 0:
                    tot = sum(len(st[k]) for k in range(16))
                    print(f"    trial {bi} (a={ab[bi,0]} b={ab[bi,1]} y={y[bi]}): {tot} spikes")
                if not args.smoke and bi % 8 == 0:
                    _save(args, spikes, ab, y, grp, in_neurons, patt, winA, winB)
        b.send("RECURCTRL 0")
    if not args.smoke:
        _save(args, spikes, ab, y, grp, in_neurons, patt, winA, winB)
        print("wrote", args.out)
    return 0


def _save(args, spikes, ab, y, grp, in_neurons, patt, winA, winB):
    tmp = args.out + ".tmp.npz"
    np.savez(tmp, spikes_ff=spikes["ff"], spikes_rec=spikes["rec"], labels=y, bits_ab=ab,
             groups=grp, in_neurons=np.array(in_neurons), patterns=np.array(patt),
             T=args.T, winA=np.array(winA), winB=np.array(winB), coding="txor_setrecur")
    os.replace(tmp, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
