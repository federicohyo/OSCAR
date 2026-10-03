#!/usr/bin/env python3
"""Single-synapse EPSP/IPSP on the membrane potential, captured on the DSO-X 2002A.

Programs ONE synapse, routes it to one neuron, holds that neuron subthreshold,
routes its Vmem to the analog monitor pin, then repeatedly injects single spikes
while the scope edge-triggers on the membrane response and averages. The result
is a clean averaged EPSP (excitatory) or IPSP (inhibitory) transient.

Modes:
  --mode epsp          one averaged excitatory EPSP  -> CSV(t,V) + PNG
  --mode ipsp          one averaged inhibitory IPSP  -> CSV(t,V) + PNG
  --mode weight-sweep  loop 4-bit weight 1..15, capture each EPSP, extract dVmem

Everything (bias, program, route, monitor, stimulate) is driven by the on-die
RISC-V via neuron_bridge.py; the scope is controlled over USBTMC (scope_usb).

Example:
  python epsp_measure.py --mode epsp --neuron 5 --syn 0 --weight 12 \
      --rate 30 --avg 128 --vdiv 0.05 --tdiv 1e-3 --trig-level 0.02 \
      --out epsp_exc.csv --png epsp_exc.png
"""

import argparse
import csv
import os
import threading
import time

import numpy as np

from meas_common import BridgeSession, load_biases, REPO_ROOT

PRESET = os.path.join(REPO_ROOT, "ofxCaravanViewer", "efficacysearch.json")


def setup_biases(b: BridgeSession, args, inhibitory: bool) -> None:
    """Apply the stimulation preset, then set the neuron just below threshold and
    enable the correct (exc/inh) synaptic pulse path."""
    biases = load_biases(PRESET)
    # Keep the neuron quiet so only stimulated PSPs move Vmem.
    if args.ifdcp is not None:
        biases["ifdcp"] = args.ifdcp
    if args.vleakn is not None:
        biases["vleakn"] = args.vleakn
    biases["buffermonp"] = args.buffermonp  # LOW -> monitor buffer drives the pin
    # Enable the pulse-extender for the path under test, disable the other.
    if inhibitory:
        biases["vipulseextp"] = args.vpulse   # ON (lower = wider inhibitory pulse)
        biases["vepulseextp"] = 1.78          # OFF
    else:
        biases["vepulseextp"] = args.vpulse   # ON
        biases["vipulseextp"] = 1.78          # OFF
    b.apply_biases(biases)
    time.sleep(args.settle)


def program_route(b: BridgeSession, syn: int, neuron: int, weight: int, inhibitory: bool) -> None:
    exc = not inhibitory
    b.program_weight(syn, weight, exc=exc)  # P must precede S
    b.route(syn, neuron, exc=exc)
    b.monitor(neuron)
    time.sleep(0.2)


def fire_loop(b: BridgeSession, rate_hz: float, stop: threading.Event) -> None:
    period = 1.0 / rate_hz
    nxt = time.perf_counter()
    while not stop.is_set():
        now = time.perf_counter()
        if nxt > now:
            time.sleep(min(period, nxt - now))
        b.fire(1)
        nxt += period


def capture(sc, b: BridgeSession, args, inhibitory: bool):
    """Fire spikes continuously while the scope averages; return (t, v)."""
    from scope_usb import Scope  # local import so the scope libs are optional for --no-scope
    assert isinstance(sc, Scope)
    slope = "NEG" if inhibitory else "POS"
    sc.channel(args.channel, scale=args.vdiv, offset=args.voffset)
    sc.timebase(scale=args.tdiv, position=args.tpos)
    sc.trigger_edge(source=args.channel, level=args.trig_level, slope=slope)
    sc.average(args.avg)
    stop = threading.Event()
    th = threading.Thread(target=fire_loop, args=(b, args.rate, stop), daemon=True)
    th.start()
    try:
        sc.digitize(args.channel)   # blocks until `avg` triggers averaged
    finally:
        stop.set()
        th.join(timeout=2)
    return sc.read_waveform(args.channel, points=args.points)


def amplitude(t: np.ndarray, v: np.ndarray, inhibitory: bool) -> float:
    """dVmem: signed deflection from the pre-trigger baseline."""
    base = v[t < 0]
    baseline = float(np.median(base)) if base.size else float(np.median(v[:len(v) // 5]))
    return (float(np.min(v)) - baseline) if inhibitory else (float(np.max(v)) - baseline)


def save_trace(path: str, t: np.ndarray, v: np.ndarray) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "v_volt"])
        for ti, vi in zip(t, v):
            w.writerow([f"{ti:.9e}", f"{vi:.6e}"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["epsp", "ipsp", "weight-sweep"], default="epsp")
    ap.add_argument("--neuron", type=int, default=5)
    ap.add_argument("--syn", type=int, default=0)
    ap.add_argument("--weight", type=int, default=12)
    ap.add_argument("--rate", type=float, default=30.0, help="stimulation rate (Hz)")
    ap.add_argument("--avg", type=int, default=128, help="scope averages")
    ap.add_argument("--vpulse", type=float, default=0.69, help="pulse-extender bias ON value")
    ap.add_argument("--ifdcp", type=float, default=None, help="override neuron charging bias")
    ap.add_argument("--vleakn", type=float, default=None, help="override leak bias")
    ap.add_argument("--buffermonp", type=float, default=0.2)
    ap.add_argument("--settle", type=float, default=1.0)
    # scope
    ap.add_argument("--channel", type=int, default=1)
    ap.add_argument("--vdiv", type=float, default=0.05)
    ap.add_argument("--voffset", type=float, default=0.0)
    ap.add_argument("--tdiv", type=float, default=1e-3)
    ap.add_argument("--tpos", type=float, default=0.0)
    ap.add_argument("--trig-level", type=float, default=0.02)
    ap.add_argument("--points", type=int, default=2000)
    # output
    ap.add_argument("--out", default=None, help="CSV path (single mode)")
    ap.add_argument("--png", default=None, help="screenshot path (single mode)")
    ap.add_argument("--out-prefix", default="epsp_w", help="weight-sweep file prefix")
    ap.add_argument("--wmin", type=int, default=1)
    ap.add_argument("--wmax", type=int, default=15)
    ap.add_argument("--no-scope", action="store_true", help="drive chip only (no capture)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    inhibitory = (args.mode == "ipsp")

    sc = None
    if not args.no_scope:
        from scope_usb import Scope
        sc = Scope()
        print("Scope:", sc.connect())

    with BridgeSession(verbose=args.verbose) as b:
        setup_biases(b, args, inhibitory)

        if args.mode in ("epsp", "ipsp"):
            program_route(b, args.syn, args.neuron, args.weight, inhibitory)
            if args.no_scope:
                print("Bridge configured (no scope). Firing 100 spikes for a scope check...")
                b.inject_spikes(args.rate, 100)
                return 0
            t, v = capture(sc, b, args, inhibitory)
            amp = amplitude(t, v, inhibitory)
            out = args.out or f"{args.mode}_n{args.neuron}_s{args.syn}_w{args.weight}.csv"
            save_trace(out, t, v)
            if args.png:
                sc.screenshot(args.png)
            print(f"{args.mode}: dVmem = {amp*1e3:.2f} mV  ->  {out}")

        else:  # weight-sweep
            rows = []
            for w in range(args.wmin, args.wmax + 1):
                program_route(b, args.syn, args.neuron, w, inhibitory=False)
                t, v = capture(sc, b, args, inhibitory=False)
                amp = amplitude(t, v, inhibitory=False)
                trace_path = f"{args.out_prefix}{w:02d}.csv"
                save_trace(trace_path, t, v)
                rows.append((w, amp))
                print(f"weight {w:2d}: dVmem = {amp*1e3:.2f} mV -> {trace_path}")
            summ = args.out or "epsp_vs_weight.csv"
            with open(summ, "w", newline="") as f:
                wr = csv.writer(f)
                wr.writerow(["weight", "dVmem_volt"])
                wr.writerows(rows)
            print(f"summary -> {summ}")

    if sc is not None:
        sc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
