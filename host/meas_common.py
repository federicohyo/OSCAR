#!/usr/bin/env python3
"""Shared helpers for driving the chip through neuron_bridge.py.

All new characterization scripts (epsp_measure.py, neuron_fi.py, routing_demo.py,
synapse_rate_transfer.py, throughput_measure.py) reuse this so they share one
proven way to spawn the bridge, set biases, inject spikes, and sample rates.

The bridge (neuron_bridge.py) is the *only* process allowed to own the FT4232H,
so everything here talks to it over stdin/stdout instead of reopening FTDI.

Bridge command primitives (see neuron_bridge.py docstring):
    B <name> <volt>            set analog bias (DAC bit-bang)
    P <syn> <weight> exc|nexc  program 4-bit synapse weight word (UART 0xF0)
    S <syn> <neu> exc|nexc     stage AER route synapse->neuron (UART 0xE0)
    T [count]                  fire count spikes on staged route (UART 0xE1)
    M <neuron>                 monitor-mux select (UART 0xD0)
Return stream: "S <neuron> <abs_us>" per spike, "RATE <spk/s>" once/sec.

Caveat: the bridge emits BOK only for PMOS biases, not NMOS ones
(vleakn/vtaun/vrefn/JExcWn*), so never block waiting for a bias ack.
"""

import json
import os
import queue
import subprocess
import sys
import threading
import time
from typing import Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BRIDGE_PATH = os.path.join(REPO_ROOT, "neuron_bridge.py")

# Bias names the bridge understands (from neuron_bridge.py BIAS_TABLE).
BRIDGE_BIASES = {
    "vtaup", "vthrdp", "vepulseextp", "vipulseextp", "vleakn", "vtaun", "vrefn",
    "free", "lna_iref", "JInhWp1", "JInhWp2", "JInhWp3", "JExcWn0", "JExcWn1",
    "JExcWn2", "JExcWn3", "VREF", "VB1", "VB2", "TUNEp", "buffermonp", "JInhWp0",
    "vthrdn", "ifdcp",
}

# NMOS-referenced biases are clamped to VREFN=0.89 by the bridge; others to 1.79.
NMOS_BIASES = {"vleakn", "vtaun", "vrefn", "JExcWn0", "JExcWn1", "JExcWn2", "JExcWn3"}


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def load_biases(path: str) -> Dict[str, float]:
    """Load a bias preset JSON (e.g. ofxCaravanViewer/efficacysearch.json)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    biases: Dict[str, float] = {}
    for key, value in data.items():
        if key in BRIDGE_BIASES and isinstance(value, (int, float)):
            biases[key] = clamp(float(value), 0.0, 1.79)
    if not biases:
        raise RuntimeError(f"No valid bridge bias keys in {path}")
    return biases


class BridgeSession:
    """Spawn neuron_bridge.py and expose a small, synchronous API to it."""

    def __init__(self, python: Optional[str] = None, verbose: bool = False):
        self.python = python or sys.executable
        self.verbose = verbose
        self.proc: Optional[subprocess.Popen] = None
        self.out_q: "queue.Queue[str]" = queue.Queue()
        self._reader: Optional[threading.Thread] = None
        log_path = os.environ.get("CARAVAN_DAC_LOG")
        if log_path:
            os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        self._dac_log = open(log_path, "a", buffering=1) if log_path else None
        if self._dac_log is not None:
            self._dac_log.write(f"# session open {time.time():.6f}  "
                                f"CARAVAN_CLK_MHZ={os.environ.get('CARAVAN_CLK_MHZ', '50')}\n")

    # -- lifecycle -------------------------------------------------------
    def __enter__(self) -> "BridgeSession":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.stop()

    def start(self, ready_timeout_s: float = 15.0) -> None:
        self.proc = subprocess.Popen(
            [self.python, BRIDGE_PATH],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=(None if self.verbose else subprocess.DEVNULL),
            cwd=REPO_ROOT, text=True, bufsize=1,
        )
        self._reader = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader.start()
        self._wait_for("READY", ready_timeout_s)

    def stop(self) -> None:
        if self.proc is None:
            return
        try:
            self.send("QUIT")
        except Exception:
            pass
        try:
            self.proc.wait(timeout=3)
        except Exception:
            self.proc.kill()
        self.proc = None

    # -- io --------------------------------------------------------------
    def _read_stdout(self) -> None:
        assert self.proc is not None and self.proc.stdout is not None
        for raw in self.proc.stdout:
            line = raw.strip()
            if line:
                self.out_q.put(line)

    def send(self, command: str) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise RuntimeError("Bridge not started")
        self.proc.stdin.write(command + "\n")
        self.proc.stdin.flush()

    def _wait_for(self, token: str, timeout_s: float) -> None:
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            try:
                line = self.out_q.get(timeout=0.2)
            except queue.Empty:
                continue
            if line == token:
                return
        raise TimeoutError(f"Timed out waiting for {token!r} from bridge")

    def drain(self, counts: Optional[List[int]] = None, max_lines: int = 100000) -> List[int]:
        """Drain pending output; tally per-neuron 'S' lines into counts."""
        if counts is None:
            counts = [0] * 16
        for _ in range(max_lines):
            try:
                line = self.out_q.get_nowait()
            except queue.Empty:
                break
            if line.startswith("S "):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        nid = int(parts[1])
                    except ValueError:
                        continue
                    if 0 <= nid <= 15:
                        counts[nid] += 1
        return counts

    # -- high-level primitives ------------------------------------------
    def bias(self, name: str, value: float, settle_s: float = 0.0) -> None:
        # The DACs are write-only: there is no readback, and during a bisection the host
        # writes computed values that correspond to no .biases file. Recording a filename is
        # therefore not enough to reconstruct the chip's state -- log every write instead.
        # Enable with CARAVAN_DAC_LOG=<path>; the log is append-only and never rotated.
        if self._dac_log is not None:
            self._dac_log.write(f"{time.time():.6f}\t{name}\t{value:.6f}\n")
            self._dac_log.flush()
        self.send(f"B {name} {value:.6f}")
        if settle_s:
            time.sleep(settle_s)

    def apply_biases(self, biases: Dict[str, float]) -> None:
        for name, value in biases.items():
            self.bias(name, value)

    def monitor(self, neuron: int) -> None:
        self.send(f"M {int(neuron)}")

    def program_weight(self, syn: int, weight: int, exc: bool = True) -> None:
        self.send(f"P {int(syn)} {int(weight)} {'exc' if exc else 'nexc'}")

    def route(self, syn: int, neuron: int, exc: bool = True) -> None:
        # NOTE: always call program_weight() BEFORE route(): weight programming
        # clobbers shared LA0 bits and the firmware re-runs spikesetup after it.
        self.send(f"S {int(syn)} {int(neuron)} {'exc' if exc else 'nexc'}")

    def fire(self, count: int = 1) -> None:
        self.send(f"T {int(count)}")

    def poisson(self, hz: float) -> None:
        """Start on-chip RISC-V Poisson generation at mean rate `hz` on the staged route."""
        self.send(f"POISSON {hz:.3f}")

    def poisson_stop(self) -> None:
        self.send("POISSONSTOP")

    def synfire(self, laps: int = 5) -> None:
        """Start RISC-V synfire chain: 0→1→2→...→15→0 for `laps` rounds."""
        self.send(f"SYNFIRE {int(laps)}")

    def synfire_stop(self) -> None:
        self.send("SYNFIRESTOP")

    def coincidence(self, syn_a: int, syn_b: int, neuron: int, dt_us: float) -> None:
        """One on-chip coincidence trial: fire input on `syn_a` then `syn_b` (both
        routed to `neuron`), separated by `dt_us` microseconds, all timed by the RISC-V."""
        self.send(f"COINC {int(syn_a)} {int(syn_b)} {int(neuron)} {dt_us:.1f}")

    def sample_spikes(self, sample_s: float) -> Dict[str, object]:
        """Count per-neuron 'S' lines over a window; also average RATE lines.

        Also totals the chip's own integrity flags for the window:
          drops  -- the on-chip ring overflowed: spikes were LOST.
          stalls -- the flush waited on the UART FIFO: the link is back-pressuring
                    the array, so these counts are not free-running.
        A window with either nonzero is NOT a measurement of the array. This matters:
        dropped spikes from a contended AER bus are what collapsed the recurrent
        reservoir (0.987 -> 0.58/0.77), and the old readout reported no error at all.
        Callers should assert both are zero, or mask neurons to buy bandwidth.
        """
        counts = [0] * 16
        rates: List[float] = []
        drops = 0
        stalls = 0
        deadline = time.time() + sample_s
        while time.time() < deadline:
            timeout = max(0.05, min(0.2, deadline - time.time()))
            try:
                line = self.out_q.get(timeout=timeout)
            except queue.Empty:
                continue
            if line.startswith("S "):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        nid = int(parts[1])
                    except ValueError:
                        continue
                    if 0 <= nid <= 15:
                        counts[nid] += 1
            elif line.startswith("RATE "):
                parts = line.split()
                if len(parts) == 2:
                    try:
                        rates.append(float(parts[1]))
                    except ValueError:
                        pass
            elif line.startswith("DROPS ") or line.startswith("STALLS "):
                parts = line.split()
                if len(parts) == 2:
                    try:
                        n = int(parts[1])
                    except ValueError:
                        continue
                    if line[0] == "D":
                        drops += n
                    else:
                        stalls += n
        per_neuron_hz = {i: counts[i] / sample_s for i in range(16)}
        return {
            "per_neuron_hz": per_neuron_hz,
            "total_hz": sum(per_neuron_hz.values()),
            "bridge_rate_hz": (sum(rates) / len(rates)) if rates else None,
            "counts": counts,
            "drops": drops,
            "stalls": stalls,
            "clean": (drops == 0 and stalls == 0),
        }

    def inject_spikes(self, rate_hz: float, count: int) -> List[int]:
        """Host-paced stimulation: fire `count` spikes at `rate_hz`, tally outputs.

        One 'T' (=one 0xE1 byte) per spike, paced with perf_counter. Returns the
        per-neuron output-spike counts observed during and just after injection.
        """
        counts = [0] * 16
        self.drain(max_lines=100000)  # clear stale
        period = 1.0 / rate_hz
        t0 = time.perf_counter()
        next_t = t0
        for _ in range(count):
            now = time.perf_counter()
            if next_t > now:
                time.sleep(next_t - now)
            self.fire(1)
            next_t += period
            self.drain(counts)
        # tail to catch trailing UART packets
        tail = time.perf_counter() + max(0.05, 2.0 * period)
        while time.perf_counter() < tail:
            self.drain(counts)
            time.sleep(0.005)
        return counts


if __name__ == "__main__":
    # Smoke test: start the bridge, print any streamed lines for a few seconds.
    with BridgeSession(verbose=True) as b:
        print("bridge up; listening 3s...", file=sys.stderr)
        t0 = time.time()
        while time.time() - t0 < 3.0:
            try:
                print("<<", b.out_q.get(timeout=0.3))
            except queue.Empty:
                pass
