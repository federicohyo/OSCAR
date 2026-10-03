#!/usr/bin/env python3
"""Phase-2 de-risk + tuning: does the chip's firmware SETRECUR (on-die recurrence) create
SUSTAINED FADING MEMORY? Give a neuron a brief input impulse, STOP the input, then measure how
long its activity REVERBERATES via a self-loop (neuron k spike -> REC_SYN inject c spikes back to
k). Recurrence ON should keep k firing after the input stops (memory); OFF should decay at once.

Sweeps the self-loop count c to find the fading-memory regime (reverberation lasts several times
the input, but decays -- not dead, not runaway). This is the operating point T-XOR / NARMA need.
Captures a scope membrane trace at a representative setting.

    ./.venv-meas/bin/python3 txor_recurrence_probe.py --neuron 5 --counts 0,1,2,3,4
"""
import argparse, time, os, fcntl
import numpy as np
from meas_common import BridgeSession, load_biases

MERGED = "data/xor_dim/biases_merged/n{k}.biases"
JUL10 = "ofxCaravanViewer/bin/bias_synapse_characterization_super_n{k}_jul10.biases"
REC_SYN = 1
SCOPEDIR = "data/scope"


def bias_path(k):
    p = MERGED.format(k=k)
    return p if os.path.exists(p) else JUL10.format(k=k)


def collect_k(b, k, window_s):
    """Collect chip-timestamped output spikes of neuron k for window_s seconds. Returns times(s)."""
    import queue
    times = []
    t_end = time.time() + window_s
    while time.time() < t_end:
        try:
            line = b.out_q.get(timeout=0.01)
        except queue.Empty:
            continue
        if line.startswith("S "):
            p = line.split()
            if len(p) >= 3 and p[1].isdigit() and int(p[1]) == k:
                try:
                    times.append(float(p[2]) / 1e6)   # abs_us -> s
                except ValueError:
                    pass
    return np.array(times)


def scope_grab(path, vdiv=0.3, tdiv=2e-2, offset=0.9):   # center=+0.9V -> 0V ground low, full swing visible
    try:
        fd = os.open("/dev/usbtmc0", os.O_RDWR)
        try: fcntl.ioctl(fd, (91 << 8) | 2)
        except OSError: pass
        os.close(fd)
        import sys; sys.path.insert(0, ".")
        from scope_usb import Scope
        with Scope() as sc:
            sc.connect() if not getattr(sc, "_connected", False) else None
            sc.channel(1, scale=vdiv, offset=offset, coupling="DC")
            sc.timebase(scale=tdiv, position=0.0)
            sc.trigger_edge(source=1, level=offset + vdiv, slope="POS", sweep="AUTO")
            sc.run(); time.sleep(0.2)
            sc.screenshot(path)
        return True
    except Exception as e:
        print("  [scope grab failed:", e, "]")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--counts", default="0,1,2,3,4", help="self-loop reinjection counts to sweep")
    ap.add_argument("--impulse", type=int, default=8, help="input spikes in the driving impulse")
    ap.add_argument("--impulse-rate", type=float, default=400.0)
    ap.add_argument("--observe", type=float, default=0.6, help="reverberation window after impulse (s)")
    ap.add_argument("--weight", type=int, default=15, help="INPUT synapse weight (seeding)")
    ap.add_argument("--rec-weight", type=int, default=15, help="REC_SYN weight (recurrence gain)")
    ap.add_argument("--scope", action="store_true")
    args = ap.parse_args()
    k = args.neuron
    counts = [int(x) for x in args.counts.split(",")]

    print(f"recurrence memory probe on n{k}: impulse={args.impulse} spikes then observe "
          f"{args.observe}s reverberation. self-loop counts {counts}\n")
    print(f"{'count':>5} {'recur':>5} | {'revspk':>6} {'last_s':>7} {'meanHz':>7}")
    with BridgeSession() as b:
        b.apply_biases(load_biases(bias_path(k))); b.monitor(k); time.sleep(0.6)
        b.program_weight(0, args.weight, exc=True)                # input synapse (seeding)
        b.program_weight(REC_SYN, args.rec_weight, exc=True)      # recurrent synapse (gain)
        results = []
        for c in counts:
            recur = c > 0
            # (re)configure recurrence: self-loop k->k with reinjection count c
            b.send(f"SETRECUR {k} {k} {max(c,1)} 1")
            b.send(f"RECURCTRL {1 if recur else 0}")
            time.sleep(0.2)
            b.route(0, k, exc=True); time.sleep(0.02)
            b.drain(max_lines=200000)                             # clear
            # fire the input impulse fast
            per = 1.0 / args.impulse_rate
            t0 = time.time()
            for _ in range(args.impulse):
                b.fire(1); time.sleep(per)
            t_impulse_end = time.time() - t0
            # observe reverberation AFTER input stops
            rev = collect_k(b, k, args.observe)
            rev_after = rev[rev > t_impulse_end] if rev.size else rev
            last = float(rev_after.max() - t_impulse_end) if rev_after.size else 0.0
            hz = rev_after.size / args.observe
            results.append((c, recur, rev_after.size, last, hz))
            print(f"{c:5d} {int(recur):5d} | {rev_after.size:6d} {last:7.3f} {hz:7.1f}")
            if args.scope and c == counts[-1]:
                scope_grab(f"{SCOPEDIR}/recur_probe_n{k}_c{c}.png")
        b.send("RECURCTRL 0")
    print("\nMemory works if reverberation spikes / last-spike-time GROW with count (rec) vs "
          "~0 at count=0 (ff). Pick the count with sustained-but-decaying reverberation.")


if __name__ == "__main__":
    raise SystemExit(main())
