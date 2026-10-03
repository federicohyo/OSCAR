#!/usr/bin/env python3
"""Autonomous 2-D hunt for a graded spike-COUNT comparator on n14.

The knob that matters is the on-chip pulse EXTENDER (vepulseextp), which sets the real
spike length at the synapse -- the LA pulse only triggers it. Charge per event is
I_w x extender_length, so shortening the extender puts one event below saturation and
lets events sum. First evidence on n5: 14 / 23 / 50 mV at N = 1 / 4 / 16 with
vepulseextp -100 mV.

vtaup comes first because it sets the working amplitude: coincidence_1_n14 sits 89 mV
below reference, a fast synapse whose response lands in the ~5 mV noise floor,
where the extender effect is buried. Raise it for signal, then sweep the extender for grading.

Objective (scope, standing rule -- AER is blind below threshold):
    span = dV(N=16) / dV(N=1),  subject to
      dV(1)  >= 15 mV   (above the noise floor, or the span is meaningless)
      dV(16) <= 300 mV  (still subthreshold; a spike reads ~1000 mV and its amplitude is
                         fixed, which would fake a flat response)

    PYTHONPATH=. CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 olfaction_graded_hunt.py
"""
import argparse, itertools, json, socket, sys, threading, time
import numpy as np
import serial

from meas_common import BridgeSession, load_biases

PORT = "/dev/ttyACM0"
NOISE_MV, FIRE_MV = 15.0, 300.0


SERVER = ("127.0.0.1", 5555)


class Scope:
    """Membrane reader. Prefers the broadcast server, falls back to the raw serial port.

    The port admits one owner, which used to mean a measurement and a live view were
    mutually exclusive -- precisely the wrong trade-off while tuning. With
    `ofxLPM/scope-pixhawk/tools/server.py` running, this connects as one of many readers
    and the GUI can watch the same stream. With no server, it opens the device directly
    and behaves exactly as before, so nothing that used to work stops working."""

    def __init__(self, port=PORT, server=SERVER):
        self.s = []
        self.source = None
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, args=(port, server), daemon=True)
        self._t.start()
        time.sleep(1.5)
        if not self.s:
            raise SystemExit(
                f"no scope stream (tried server {server[0]}:{server[1]} then {port}). "
                "Is the GUI holding the port, or the server not running?")

    def _connect(self, server):
        try:
            sk = socket.create_connection(server, timeout=2.0)
            sk.settimeout(0.5)
            return sk
        except OSError:
            return None

    def _run(self, port, server):
        sk = self._connect(server)
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
            return
        self.source = f"serial {port}"
        sp = serial.Serial(port, 115200, timeout=0.2)
        sp.dtr, sp.rts = True, False
        time.sleep(0.3); sp.reset_input_buffer()
        while not self._stop.is_set():
            try:
                ln = sp.readline().decode(errors="replace").strip()
            except Exception:
                continue
            self._parse(ln)
        sp.close()

    def _parse(self, ln):
        """Store (host_arrival, volts, board_time).

        The BOARD time is field 0 and it matters. Host arrival is fine for windowing a
        burst -- "which samples came after I sent it" -- but it cannot measure intervals
        once samples arrive in batches: over the broadcast server a whole recv() worth of
        lines is stamped with almost the same time.time(), which collapsed a membrane
        decay to tau = 0.0 ms. The board's own clock is immune to that and is what any
        duration must be computed from. Third column, so existing [:,0]/[:,1] users are
        unaffected."""
        q = ln.strip().split(",")        # device streams "<time>,<volts>" -- TWO fields
        if len(q) >= 2:
            try:
                self.s.append((time.time(), float(q[1]), float(q[0])))
            except ValueError:
                pass

    def dv(self, t0):
        a = np.array(self.s)
        pre = a[(a[:, 0] > t0 - 0.18) & (a[:, 0] < t0 - 0.02), 1]
        post = a[(a[:, 0] >= t0) & (a[:, 0] < t0 + 0.24), 1]
        if len(pre) < 4 or len(post) < 4:
            return float("nan")
        return (float(np.max(post)) - float(np.median(pre))) * 1000.0

    def stop(self):
        self._stop.set()


def measure(b, sc, k, n, reps):
    v = []
    for _ in range(reps):
        b.drain(max_lines=100000); time.sleep(0.20)
        t0 = time.time(); b.send(f"BURST {n}"); time.sleep(0.25)
        x = sc.dv(t0)
        if x == x:
            v.append(x)
    return float(np.median(v)) if v else float("nan")


def apply(base, dtau, dext):
    b = dict(base)
    if "vtaup" in b:
        b["vtaup"] = b["vtaup"] + dtau
    if "vepulseextp" in b:
        b["vepulseextp"] = b["vepulseextp"] + dext
    return b


def score(ds):
    """ds = [dV(1), dV(4), dV(16)] -> (objective, verdict)."""
    g = [x for x in ds if x == x]
    if len(g) < 3:
        return -1.0, "no data"
    if max(g) > FIRE_MV:
        return -1.0, "fires"
    if ds[0] < NOISE_MV:
        return -1.0, "noise floor"
    return ds[2] / max(ds[0], 1e-9), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neuron", type=int, default=14)
    ap.add_argument("--base",
                    default="ofxCaravanViewer/bin/"
                            "bias_synapse_characterization_coincidence_1_n14.biases")
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--out", default="data/olfaction_graded_hunt.json")
    args = ap.parse_args()
    k = args.neuron
    base = load_biases(args.base)
    sc = Scope()
    print(f"neuron {k}, base {args.base.split('/')[-1]}")
    print(f"  vtaup {base.get('vtaup'):.4f}  vepulseextp {base.get('vepulseextp'):.4f}")
    print(f"objective: dV(16)/dV(1), needs dV(1)>={NOISE_MV:.0f} mV and "
          f"dV(16)<={FIRE_MV:.0f} mV\n")

    grid_tau = (0.030, 0.060, 0.090, 0.120)
    grid_ext = (-0.060, -0.030, 0.0, 0.030, 0.060)
    hist, best = [], None
    print(f"{'dvtaup':>8} {'dvepext':>8} | {'N=1':>7} {'N=4':>7} {'N=16':>7} | "
          f"{'span':>5}  verdict")
    with BridgeSession() as b:
        b.send(f"MASK {1 << k}"); b.send("PULSEFINE 1"); time.sleep(0.1)
        for dt, de in itertools.product(grid_tau, grid_ext):
            b.apply_biases(apply(base, dt, de)); b.monitor(k); time.sleep(0.85)
            b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)
            ds = [measure(b, sc, k, n, args.reps) for n in (1, 4, 16)]
            s, why = score(ds)
            hist.append(dict(dtau=dt, dext=de, ds=ds, span=s))
            star = ""
            if s > 0 and (best is None or s > best["span"]):
                best = hist[-1]; star = "  <-- best"
            print(f"{dt*1000:+7.0f}m {de*1000:+7.0f}m | "
                  + " ".join(f"{x:7.0f}" for x in ds)
                  + f" | {s:5.2f}  {why}{star}")
            json.dump({"grid": hist, "best": best}, open(args.out, "w"), indent=2)

        if best is None:
            print("\nno point cleared both constraints -- widen the grid")
            sc.stop(); return 1

        # fine ladder at the winner
        print(f"\nrefining at dvtaup {best['dtau']*1000:+.0f} mV, "
              f"dvepext {best['dext']*1000:+.0f} mV")
        b.apply_biases(apply(base, best["dtau"], best["dext"]))
        b.monitor(k); time.sleep(0.9)
        b.program_weight(0, 15, exc=True); b.route(0, k, exc=True); time.sleep(0.05)
        LEV = (1, 2, 3, 4, 6, 8, 12, 16, 24, 32)
        fine = [measure(b, sc, k, n, 6) for n in LEV]
        print("  N     " + " ".join(f"{n:>5}" for n in LEV))
        print("  dV mV " + " ".join(f"{x:5.0f}" for x in fine))
        mono = sum(1 for i in range(len(fine) - 1) if fine[i + 1] >= fine[i] - 3)
        print(f"  span {max(fine)/max(min(fine),1e-9):.1f}x, "
              f"monotone on {mono}/{len(fine)-1} steps")
        json.dump({"grid": hist, "best": best, "fine_levels": list(LEV),
                   "fine_dv": fine}, open(args.out, "w"), indent=2)
        b.send("PULSEFINE 0")
    sc.stop()
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
