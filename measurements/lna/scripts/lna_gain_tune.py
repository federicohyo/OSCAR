#!/usr/bin/env python3
"""LNA gain maximizer: sweeps the five LNA bias DACs and keeps what
maximizes the output amplitude seen on the membrane scope stream.

Self-contained: bit-bangs the AD5664R DACs over the FT4232H (channels B/C)
and reads Vout as a client of the scope broadcast server. No repo imports.

Vout path: the LNA output node is what the pixhawk scope streams as
"<time>,<volts>" lines. Connect via ofxLPM/scope-pixhawk/tools/server.py
(127.0.0.1:5555); if no server answers, falls back to opening
/dev/ttyACM0 directly. VPP is the 5th-95th percentile spread of volts in
a window -- raw max-min is too easily inflated by single ADC spikes.

Vin stays fixed for the whole run, so maximizing Vout(VPP) maximizes gain;
pass --vin-pp to also log the gain ratio and dB.

Prereqs before running:
  - kill anything owning the FTDI:  pkill -f '[n]euron_bridge.py' ; close the GUI
  - start the scope server once:    ./.venv-meas/bin/python3 ofxLPM/scope-pixhawk/tools/server.py
    (or leave it off and make sure nothing else holds /dev/ttyACM0)

Usage:
  ../../.venv-meas/bin/python3 lna_gain_tune.py                  # from LNA/
  ../../.venv-meas/bin/python3 lna_gain_tune.py --vin-pp 0.02    # also log gain
  ../../.venv-meas/bin/python3 lna_gain_tune.py --start lna_gain_best.json  # resume from best

Logs:  lna_gain_log.csv   every measurement
       lna_gain_best.json best bias set so far + its VPP (safe to re-feed via --start)

Bias <-> schematic mapping and sweep windows live in the BIASES table below.
Edit that one table if the pin mapping differs. All writes are
clipped to [each bias's lo..hi]. lna_iref (DAC3 ch A) is powered down to
high-Z at chip startup (pin shared with monout_single), so a power-up frame
(mode=0b00) is sent before each write to it.

Ctrl-C: restores the biases the run started with and closes everything.
"""

import argparse
import csv
import json
import math
import os
import socket
import statistics
import sys
import threading
import time

import serial
from pyftdi.gpio import GpioAsyncController

VDD = 1.78

FTDI_B = 'ftdi://ftdi:4232h/2'
FTDI_C = 'ftdi://ftdi:4232h/3'

BIASES = {
    "vref":     {"dac": 5, "addr": 0b000, "design": 0.80,  "lo": 0.40, "hi": 1.20, "schematic": "vref (input-pair reference)"},
    "vb1":      {"dac": 5, "addr": 0b001, "design": 0.793, "lo": 0.39, "hi": 1.19, "schematic": "vb1 (cascode bias)"},
    "vb2":      {"dac": 5, "addr": 0b010, "design": 0.647, "lo": 0.245, "hi": 1.045, "schematic": "vb2 (cascode bias)"},
    "tunep":    {"dac": 5, "addr": 0b011, "design": 0.709, "lo": 0.31, "hi": 1.11, "schematic": "tunep (active-cascode bias)"},
    "lna_iref": {"dac": 3, "addr": 0b000, "design": 1.105, "lo": 0.70, "hi": 1.50, "schematic": "iref (input-pair mirror)", "needs_wake": True},
}

SCOPE_SERVER = ("127.0.0.1", 5555)
SCOPE_PORT = "/dev/ttyACM0"
SCOPE_BAUD = 115200

PIN_CLK = 0
PIN_DATA = 1
PIN_FORCE_OUT = 5
DAC_TO_CDBUS = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
HALF_PERIOD_S = 2e-6

CMD_WRITE_UPDATE = 0b011
CMD_POWER = 0b100
POWER_NORMAL = 0b00


class DACs:
    """AD5664R bit-bang, minimal copy of firmware/riscvprog.py logic."""

    def __init__(self, url_b=FTDI_B, url_c=FTDI_C, frequency=200_000):
        self._b = GpioAsyncController()
        self._c = GpioAsyncController()
        self._cs_mask = sum(1 << p for p in DAC_TO_CDBUS.values())
        b_dir = (1 << PIN_CLK) | (1 << PIN_DATA) | (1 << PIN_FORCE_OUT)
        self._b.configure(url_b, direction=b_dir, frequency=frequency)
        self._c.configure(url_c, direction=self._cs_mask, frequency=frequency)
        self._b_state = 0
        self._c_state = self._cs_mask
        self._b.write(self._b_state)
        self._c.write(self._c_state)

    def close(self):
        try:
            self._c.write(self._cs_mask)
            self._b.write(0)
        finally:
            self._b.close()
            self._c.close()

    def _clk_data(self, clk, data):
        self._b_state = ((self._b_state | (1 << PIN_CLK)) if clk
                         else (self._b_state & ~(1 << PIN_CLK)))
        if data:
            self._b_state |= (1 << PIN_DATA) | (1 << PIN_FORCE_OUT)
        else:
            self._b_state &= ~((1 << PIN_DATA) | (1 << PIN_FORCE_OUT))
        self._b.write(self._b_state)

    def _select(self, dac_id):
        self._c_state = self._cs_mask & ~(1 << DAC_TO_CDBUS[dac_id])
        self._c.write(self._c_state)

    def write(self, dac_id, command, address, data16):
        frame = ((command & 7) << 19) | ((address & 7) << 16) | (data16 & 0xFFFF)
        self._select(dac_id)
        time.sleep(HALF_PERIOD_S)
        for i in range(23, -1, -1):
            bit = (frame >> i) & 1
            self._clk_data(0, bit)
            self._clk_data(1, bit)
            self._clk_data(0, bit)
        time.sleep(HALF_PERIOD_S)
        self._c.write(self._cs_mask)

    def set_voltage(self, dac_id, address, volts, vref=VDD):
        volts = min(max(volts, 0.0), vref)
        self.write(dac_id, CMD_WRITE_UPDATE, address, round(volts / vref * 65535))

    def power_up(self, dac_id, address):
        data16 = (POWER_NORMAL << 4) | (1 << address)
        self.write(dac_id, CMD_POWER, 0b000, data16)


def set_bias(dacs, name, volts):
    cfg = BIASES[name]
    v = min(max(volts, cfg["lo"]), cfg["hi"])
    if cfg.get("needs_wake"):
        dacs.power_up(cfg["dac"], cfg["addr"])
    dacs.set_voltage(cfg["dac"], cfg["addr"], v)
    return v


class ScopeClient:
    """Reader for the pixhawk scope stream: server first, raw port as fallback.

    Same contract as ofxLPM/scope-pixhawk/tools/server.py: lines of
    "<board_time>,<volts>". Windowed stats use host arrival time; durations
    inside a window use the board clock (batches arrive together over TCP)."""

    def __init__(self, server=SCOPE_SERVER, port=SCOPE_PORT, baud=SCOPE_BAUD):
        self.samples = []
        self.source = None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, args=(server, port, baud), daemon=True)
        self._t.start()
        t0 = time.time()
        while time.time() - t0 < 6.0:
            with self._lock:
                if self.samples:
                    return
            time.sleep(0.1)
        raise SystemExit(
            f"no scope samples after 6 s (tried server {server[0]}:{server[1]} then {port}). "
            "Start server.py or free the port.")

    def _run(self, server, port, baud):
        while not self._stop.is_set():
            try:
                sk = socket.create_connection(server, timeout=1.0)
                sk.settimeout(0.5)
            except OSError:
                sk = None
            if sk is not None:
                self.source = f"server {server[0]}:{server[1]}"
                buf = b""
                with sk:
                    while not self._stop.is_set():
                        try:
                            chunk = sk.recv(4096)
                        except socket.timeout:
                            continue
                        except OSError:
                            break
                        if not chunk:
                            break
                        buf += chunk
                        *done, buf = buf.split(b"\n")
                        for raw in done:
                            self._parse(raw.decode(errors="replace"))
                continue
            try:
                sp = serial.Serial(port, baud, timeout=0.2)
            except serial.SerialException:
                time.sleep(1.0)
                continue
            self.source = f"serial {port}"
            sp.dtr, sp.rts = True, False
            time.sleep(0.3)
            sp.reset_input_buffer()
            while not self._stop.is_set():
                try:
                    ln = sp.readline().decode(errors="replace")
                except Exception:
                    break
                self._parse(ln)
            sp.close()
            time.sleep(1.0)

    def _parse(self, ln):
        q = ln.strip().split(",")
        if len(q) >= 2:
            try:
                rec = (time.time(), float(q[1]), float(q[0]))
            except ValueError:
                return
            with self._lock:
                self.samples.append(rec)
                if len(self.samples) > 5_000_000:
                    del self.samples[:1_000_000]

    def close(self):
        self._stop.set()

    def vpp(self, window_s):
        """Collect for window_s seconds, return (Vpp, n_samples, est_freq_hz).

        Vpp = 95th - 5th percentile of volts. Frequency from rising
        zero-crossings of the window median against the board clock."""
        with self._lock:
            n0 = len(self.samples)
        time.sleep(window_s)
        with self._lock:
            seg = self.samples[n0:]
        if len(seg) < 10:
            raise RuntimeError(f"scope stream stalled ({len(seg)} samples in {window_s} s)")
        vs = sorted(v for _, v, _ in seg)
        lo = vs[int(0.05 * (len(vs) - 1))]
        hi = vs[int(0.95 * (len(vs) - 1))]
        vpp = hi - lo
        med = vs[len(vs) // 2]
        crossings = 0
        prev = seg[0][1]
        span = seg[-1][2] - seg[0][2]
        for _, v, _ in seg:
            if prev < med <= v:
                crossings += 1
            prev = v
        freq = crossings / span if span > 0 else 0.0
        return vpp, len(seg), freq


def gain_db(vout_pp, vin_pp):
    if not vin_pp or vout_pp <= 0:
        return float("nan")
    return 20.0 * math.log10(vout_pp / vin_pp)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--window", type=float, default=1.0, help="scope seconds per VPP estimate")
    ap.add_argument("--reps", type=int, default=2, help="windows per point (median)")
    ap.add_argument("--grid", type=int, default=7, help="points per bias sweep")
    ap.add_argument("--passes", type=int, default=4, help="coordinate-descent passes")
    ap.add_argument("--vin-pp", type=float, default=0.0, help="input Vpp for gain readout")
    ap.add_argument("--fin", type=float, default=580e3, help="expected input frequency (sanity check)")
    ap.add_argument("--settle", type=float, default=0.3, help="seconds to wait after a bias write")
    ap.add_argument("--start", default="", help="JSON file with starting biases (name: volts)")
    ap.add_argument("--log", default="lna_gain_log.csv")
    ap.add_argument("--best", default="lna_gain_best.json")
    args = ap.parse_args()

    start = {name: cfg["design"] for name, cfg in BIASES.items()}
    if args.start:
        with open(args.start) as f:
            loaded = json.load(f)
        biases_in = loaded.get("biases", loaded)
        for name in start:
            if name in biases_in:
                start[name] = float(biases_in[name])

    print("LNA gain tuner -- close the GUI / neuron_bridge.py first (exclusive FTDI).")
    scope = ScopeClient()
    print(f"scope: streaming from {scope.source}")
    dacs = DACs()
    best_biases = dict(start)
    best_vpp = -1.0
    try:
        for name, v in start.items():
            set_bias(dacs, name, v)
        time.sleep(args.settle)

        log_exists = os.path.exists(args.log)
        logf = open(args.log, "a", newline="")
        log = csv.writer(logf)
        if not log_exists:
            log.writerow(["t", "pass", "bias", "volts"] +
                         [f"hold_{n}" for n in BIASES] +
                         ["vpp_out", "gain", "gain_db", "n_samp", "f_est_hz"])

        cur_pass = 0
        current = dict(start)

        def measure(name, volts):
            vpp_w, ns, f = [], [], []
            for _ in range(args.reps):
                v, n, fr = scope.vpp(args.window)
                vpp_w.append(v)
                ns.append(n)
                f.append(fr)
            vpp = statistics.median(vpp_w)
            g = (vpp / args.vin_pp) if args.vin_pp else float("nan")
            log.writerow([f"{time.time():.3f}", cur_pass, name, f"{volts:.4f}" if volts is not None else ""] +
                         [f"{current[n]:.4f}" for n in BIASES] +
                         [f"{vpp:.5f}",
                          f"{g:.3f}" if args.vin_pp else "",
                          f"{gain_db(vpp, args.vin_pp):.2f}" if args.vin_pp else "",
                          sum(ns) // len(ns), f"{statistics.median(f):.0f}"])
            logf.flush()
            return vpp, statistics.median(f)

        best_vpp, f0 = measure("start", None)
        if f0 and abs(f0 - args.fin) / args.fin > 0.2:
            print(f"WARNING: stream crosses at ~{f0/1e3:.1f} kHz, expected ~{args.fin/1e3:.1f} kHz")
        print(f"start: VPP={best_vpp*1e3:.1f} mV" +
              (f"  gain={best_vpp/args.vin_pp:.1f} ({gain_db(best_vpp, args.vin_pp):.1f} dB)" if args.vin_pp else ""))

        total = args.passes * len(BIASES) * args.grid * args.reps
        print(f"plan: {args.passes} passes x {len(BIASES)} biases x {args.grid} pts "
              f"(~{total * args.window:.0f} s of scope time)")

        r_lo, r_hi = 0.15, 0.85
        for cur_pass in range(1, args.passes + 1):
            span_frac = 0.5 * (0.45 ** (cur_pass - 1))
            improved = False
            for name, cfg in BIASES.items():
                span = (cfg["hi"] - cfg["lo"]) * span_frac
                lo = max(cfg["lo"], current[name] - span)
                hi = min(cfg["hi"], current[name] + span)
                pts = sorted({round(lo + (hi - lo) * (r_lo + (r_hi - r_lo) * i / (args.grid - 1)), 4)
                              for i in range(args.grid)} | {round(current[name], 4)})
                local_best_v, local_best_vpp = current[name], best_vpp
                for v in pts:
                    current[name] = set_bias(dacs, name, v)
                    time.sleep(args.settle)
                    vpp, _ = measure(name, current[name])
                    print(f"  pass{cur_pass} {name:9s} {current[name]:.3f} V -> {vpp*1e3:8.1f} mV"
                          + (f"  ({gain_db(vpp, args.vin_pp):5.1f} dB)" if args.vin_pp else ""))
                    if vpp > local_best_vpp:
                        local_best_v, local_best_vpp = current[name], vpp
                if local_best_vpp > best_vpp:
                    improved = True
                current[name] = local_best_v
                best_vpp = max(best_vpp, local_best_vpp)
                set_bias(dacs, name, current[name])
                best_biases = dict(current)
                with open(args.best, "w") as bf:
                    json.dump({"biases": best_biases, "vpp_out": best_vpp,
                               "vin_pp": args.vin_pp or None,
                               "gain_db": gain_db(best_vpp, args.vin_pp) if args.vin_pp else None,
                               "t": time.time()}, bf, indent=2)
            print(f"pass {cur_pass}: best VPP={best_vpp*1e3:.1f} mV  "
                  f"best={ {k: round(v, 3) for k, v in best_biases.items()} }")
            if not improved and cur_pass > 1:
                print("no improvement this pass; converged")
                break

        print(f"\nDONE. best VPP={best_vpp*1e3:.1f} mV"
              + (f"  gain={best_vpp/args.vin_pp:.1f} ({gain_db(best_vpp, args.vin_pp):.1f} dB)" if args.vin_pp else ""))
        print(f"best biases left applied; saved to {args.best}")
        logf.close()

    except KeyboardInterrupt:
        print("\nCtrl-C: restoring start biases...")
        for name, v in start.items():
            set_bias(dacs, name, v)
        print("restored.")
    finally:
        scope.close()
        dacs.close()


if __name__ == "__main__":
    sys.exit(main())
