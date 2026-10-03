#!/usr/bin/env python3
"""Odor -> LNA -> neuron, with BOTH scope channels recorded.

    CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 LNA/odor_neuron_loop_dual.py

Same host-in-the-loop experiment as odor_neuron_loop.py -- that script is left
untouched because it produced the 2026-08-26 data -- but the scope server now
streams two channels, so this version records the analog evidence on both sides
of the loop instead of only the input side:

    ch1 = LNA output      (what the detector thresholds; drives the injections)
    ch2 = membrane monitor pin of the neuron (`M 9`), i.e. the chip's own answer

With ch2 the raster is confirmed against the scope rather than taken on faith from the AER stream: the
membrane trace shows the integration and the reset next to the stimulus that
caused it, on one time base.

WHAT CLOSES THE LOOP is unchanged. The amplifier reaches the core only through the
host, so the host does the detection: it reads ch1, and when the output rises
above a baseline-relative threshold it injects spikes into neuron 9. The decision
between amplification and spiking is made off-die -- a host-in-the-loop
demonstration, and it must be described as one.

THRESHOLD IS BASELINE-RELATIVE rather than absolute: the output DC wanders by tens of
mV over minutes (it has moved ~0.6 V since the 2026-08-26 runs). The baseline is
a trailing median over a window longer than the event.

THE RAW STREAM IS SAVED at the full 1 kHz in addition to the 250 Hz control trace: a
membrane sawtooth aliases badly at the control rate. `raw` = (t_board, t_host,
ch1, ch2); `trace`/`fires`/`counts` keep the same meaning as in the 1-channel
script so the two runs stay comparable.

MONITOR SELECT RESETS. The firmware selects neuron 14 at boot
(`select_monitor_neuron(14, ...)`), so ch2 watches a silent neuron until `M 9` is
sent -- and it reverts on every CPU reset, i.e. after every reflash and after
every DLL engage. Hence the gate below: ch2 must actually come alive when the
monitor is switched, or the run aborts before any audio is played.
"""
import argparse, json, os, subprocess, sys, time
import numpy as np

os.environ.setdefault("CARAVAN_CLK_MHZ", "25")   # the flashed image is a 25 MHz
                                                 # build; the bridge defaults to
                                                 # 50 and engages the DLL on
                                                 # startup -- a mismatch is a
                                                 # SILENT comms mismatch.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))
sys.path.insert(0, HERE)
from meas_common import BridgeSession
from lna_audio_sweep import Scope

NEURON, WEIGHT = 9, 15
SYN_DEFAULT = 15    # 2026-08-26 late: the preflight found synapse 0 dead and 15
                    # live -- the reverse of earlier tonight. Always take the
                    # synapse from a fresh preflight; treat this default with care.
SMOOTH_S   = 0.025
BASELINE_S = 1.20
THRESH_MV  = 40.0      # picked offline on the 2026-08-26 trace; re-check the
                       # printed excess range if the operating point has moved
FULL_MV    = 60.0
MAX_HZ     = 120.0
TICK_S     = 0.004
GATE_S     = 2.0       # how long to watch ch2 before trusting the monitor path
GATE_MV    = 60.0      # ch2 must swing at least this much, and 5x its own
                       # pre-`M 9` noise, once the monitor is switched to 9


class Scope2(Scope):
    """Three-field variant of the stream: 't,ch1,ch2' instead of 't,v'.

    Subclassed rather than changed in place: lna_audio_sweep.Scope is imported by
    every other measurement script, and its `len(q) >= 2` test already tolerates
    the wider line (it silently keeps ch1), so nothing else moves.
    """

    def _read(self):
        rec = []
        try:
            chunk = self.sk.recv(65536)
        except Exception:
            return rec
        if not chunk:
            raise RuntimeError("scope server closed the connection")
        self.buf += chunk
        *done, self.buf = self.buf.split(b"\n")
        for ln in done:
            if self._first:            # truncated fragment -- discard
                self._first = False
                continue
            q = ln.decode(errors="replace").strip().split(",")
            if len(q) >= 3:
                try:
                    rec.append((float(q[0]), float(q[1]), float(q[2])))
                except ValueError:
                    pass
        return rec

    def grab(self, seconds):
        rec = []
        t0 = time.time()
        while time.time() - t0 < seconds:
            rec.extend(self._read())
        return np.asarray(rec, dtype=float).reshape(-1, 3)


def drain_all(br, counts=None, stats=None):
    """Like BridgeSession.drain(), but also keeps the DROPS/STALLS lines it
    discards. The bench rule is drops == stalls == 0, so they have to be read
    somewhere."""
    if counts is None:
        counts = [0] * 16
    if stats is None:
        stats = {}
    while True:
        try:
            line = br.out_q.get_nowait()
        except Exception:
            break
        if line.startswith("S "):
            q = line.split()
            if len(q) >= 3:
                try:
                    nid = int(q[1])
                except ValueError:
                    continue
                if 0 <= nid <= 15:
                    counts[nid] += 1
        elif line.startswith(("DROPS", "STALLS", "RATE")):
            q = line.split()
            if len(q) == 2:
                try:
                    stats[q[0].lower()] = float(q[1])
                except ValueError:
                    pass
    return counts, stats


def ch2_activity(a):
    """(peak-to-peak mV, rough crossing rate Hz) of the membrane channel."""
    if len(a) < 50:
        return 0.0, 0.0
    v = a[:, 2]
    p2p = float(np.ptp(v)) * 1e3
    mid = (v.max() + v.min()) / 2.0
    up = np.flatnonzero((v[:-1] < mid) & (v[1:] >= mid))
    span = max(a[-1, 0] - a[0, 0], 1e-6)
    return p2p, len(up) / span


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav", default=os.path.join(HERE, "odor_stimulus.wav"))
    ap.add_argument("--timing", default=os.path.join(HERE, "odor_timing.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "odor_neuron_loop_dual.npz"))
    ap.add_argument("--settle", type=float, default=4.0)
    ap.add_argument("--bias", default=os.path.join(
        HERE, "biases", "bias_LNA_50dB-neuron9-16Hz.biases"),
        help="bias file applied at startup; '' to use whatever the DACs hold")
    ap.add_argument("--thresh", type=float, default=THRESH_MV,
                    help="detection threshold above the trailing baseline, mV")
    ap.add_argument("--full", type=float, default=FULL_MV,
                    help="excess mapping to the maximum injection rate, mV")
    ap.add_argument("--syn", type=int, default=SYN_DEFAULT,
                    help="input synapse index, as confirmed by odor_neuron_preflight.py")
    ap.add_argument("--dry", action="store_true", help="detect but inject nothing")
    ap.add_argument("--no-gate", action="store_true",
                    help="run even if ch2 shows no membrane activity")
    a = ap.parse_args()
    tm = json.load(open(a.timing))
    dur = tm["wav_s"] + 3.0

    rec_path = os.path.join(HERE, "odor_neuron_spikes_dual.txt")
    subprocess.run(["pkill", "-x", "pw-play"], capture_output=True)

    with BridgeSession() as br:
        # APPLY THE BIASES. Earlier versions of this script relied on the DACs
        # still holding whatever the GUI had left, which is how a run that
        # measured 8 Hz at 00:05 measured 0 Hz at 00:20 from an unchanged script:
        # the operating point had moved and nothing in the data said so. The file
        # is the operating point; a run names one to be reproducible.
        if a.bias:
            import json as _json
            _p = a.bias
            if not os.path.exists(_p) and os.path.exists(
                    os.path.join(HERE, _p)):
                _p = os.path.join(HERE, _p)   # bare name given from the repo root
            _d = _json.load(open(_p))
            _n = 0
            for _k, _v in _d.items():
                if isinstance(_v, (int, float)):
                    br.bias(_k, float(_v)); _n += 1
            print(f"biases: {_n} channels from {os.path.basename(a.bias)}")
            time.sleep(2.0); br.drain()

        br.send(f"MASK {1 << NEURON}"); time.sleep(0.3)
        br.program_weight(a.syn, WEIGHT, True); time.sleep(0.05)
        br.route(a.syn, NEURON, True); time.sleep(0.05)

        sc = Scope2(); sc.drain(a.settle)

        # --- monitor path gate ------------------------------------------------
        # ch2 sees neuron 14 until `M 9` is sent (the firmware selects 14 at boot
        # and reverts on every CPU reset). A flat ch2 leaves the monitor's state open
        # is dead -- neuron 9 is quiescent at this operating point -- so the gate
        # kicks the neuron and requires the membrane to answer. The burst is fired
        # even under --dry: it tests the path and stays outside the experiment,
        # and its spikes are drained before RECORD starts.
        pre = sc.grab(GATE_S)
        p2p_pre, _ = ch2_activity(pre)
        drain_all(br)
        br.send(f"M {NEURON}"); time.sleep(0.3)
        quiet = sc.grab(GATE_S)
        p2p_quiet, _ = ch2_activity(quiet)
        free, _ = drain_all(br)
        aer_free = sum(free)

        br.send("BURST 4")
        post = sc.grab(GATE_S)
        p2p_post, rate_post = ch2_activity(post)
        kick, _ = drain_all(br)

        print(f"ch2 monitor gate: neuron 14 (boot default) {p2p_pre:6.1f} mVpp"
              f"  ->  neuron {NEURON} idle {p2p_quiet:6.1f} mVpp"
              f"  ->  after BURST 4 {p2p_post:6.1f} mVpp ({rate_post:.0f} Hz)")
        print(f"                  AER: {aer_free} spikes idle, {sum(kick)} after the kick"
              f"  (neuron {NEURON}: {kick[NEURON]})")
        alive = p2p_post > max(GATE_MV, 5.0 * p2p_pre)
        if not alive:
            print("  ch2 did not answer a burst that the AER stream did see. The monitor")
            print("  pin, its buffer bias (buffermonp) or the probe is the problem -- no")
            print("  script change fixes it. Aborting before playing audio.")
            print("  Re-run with --no-gate to record anyway.")
            if not a.no_gate:
                sc.close()
                return 2
        if aer_free:
            print(f"  NOTE: neuron {NEURON} free-runs at ~{aer_free / GATE_S:.0f} Hz with no")
            print("        stimulus. Injected spikes sit on top of that background.")
        if kick[NEURON] > 8:
            print(f"  NOTE: BURST 4 drew {kick[NEURON]} spikes -- the neuron rings on well past")
            print("        its input. Expect the odor response to be smeared in time.")

        br.send(f"RECORD {rec_path}"); time.sleep(0.3); br.drain()

        buf_v, raw = [], []
        nsm = max(1, int(SMOOTH_S * 1000))
        nbl = max(1, int(BASELINE_S * 1000))

        print(f"threshold = baseline + {a.thresh:.0f} mV, "
              f"rate 0..{MAX_HZ:.0f} Hz over {a.full:.0f} mV"
              + ("   [DRY RUN -- no injection]" if a.dry else ""))
        # prime the baseline before the tone starts
        t0 = time.time()
        while time.time() - t0 < BASELINE_S + 0.3:
            for r in sc._read():
                buf_v.append(r[1])
        player = subprocess.Popen(["pw-play", "--", a.wav],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  start_new_session=True)
        t_start = time.time()
        fires, trace, nfire = [], [], 0
        next_fire = 0.0
        # WARM-UP: the trailing-median baseline is still full of pre-tone quiet
        # when the tone starts, so early stimulus content reads as a large excess.
        WARMUP = BASELINE_S + tm["period_s"]
        try:
            while time.time() - t_start < dur:
                now_host = time.time()
                for r in sc._read():
                    buf_v.append(r[1])
                    raw.append((r[0], now_host - t_start, r[1], r[2]))
                if len(buf_v) < nbl + nsm:
                    time.sleep(TICK_S); continue
                now = time.time() - t_start
                cur = float(np.mean(buf_v[-nsm:]))
                base = float(np.median(buf_v[-nbl:]))
                exc_mv = (cur - base) * 1e3
                trace.append((now, cur, base))
                if now < WARMUP:
                    next_fire = 0.0
                    time.sleep(TICK_S); continue
                if exc_mv > a.thresh:
                    frac = min(1.0, (exc_mv - a.thresh) / max(a.full - a.thresh, 1e-6))
                    hz = frac * MAX_HZ
                    if hz > 0 and now >= next_fire:
                        if not a.dry:
                            br.send("BURST 1")
                        fires.append((now, exc_mv, hz)); nfire += 1
                        next_fire = now + 1.0 / hz
                else:
                    next_fire = 0.0
                time.sleep(TICK_S)
        finally:
            try: player.wait(timeout=2)
            except Exception: player.kill()
            subprocess.run(["pkill", "-x", "pw-play"], capture_output=True)
            time.sleep(0.5)
            counts, stats = drain_all(br)
            br.send("RECORDSTOP"); time.sleep(0.4)
            sc.close()

    tr = np.array(trace)
    fr = np.array(fires) if fires else np.zeros((0, 3))
    rw = np.array(raw) if raw else np.zeros((0, 4))
    print(f"\n{len(tr)} control ticks over {dur:.1f} s; {len(rw)} raw 2-channel samples")
    if len(rw):
        print(f"ch1 (LNA)      : dc {rw[:,2].mean():.4f} V, {np.ptp(rw[:,2])*1e3:.1f} mVpp")
        print(f"ch2 (membrane) : dc {rw[:,3].mean():.4f} V, {np.ptp(rw[:,3])*1e3:.1f} mVpp")
    print(f"injections : {nfire}   (warm-up {WARMUP:.1f} s excluded)")
    print(f"spikes from neuron {NEURON}: {counts[NEURON]}   (all others: {sum(counts)-counts[NEURON]})")
    drops, stalls = stats.get("drops", 0.0), stats.get("stalls", 0.0)
    print(f"stream health: drops {drops:.0f}, stalls {stalls:.0f}"
          + ("   OK" if drops == 0 and stalls == 0 else "   <-- the bench rule is drops == stalls == 0"))
    if nfire:
        print(f"excess at injection: {fr[:,1].min():.0f} .. {fr[:,1].max():.0f} mV")
        print(f"instantaneous rate : {fr[:,2].min():.0f} .. {fr[:,2].max():.0f} Hz")
        # NOTE ON THE EVENT WINDOW: odor_timing.json's event_on/event_off
        # (0.330-0.565 s) describe the SPICE/reference stimulus rather than the WAV that is
        # played. Measured on odor_stimulus.wav itself, the odor content of each
        # period runs 0.501-1.260 s and peaks at 1.047 s; the 137 Hz mark at
        # 0.124 s matches t_mark and is what any offline alignment should use
        # (pw-play start latency was 0.336 s in this run and jitters by ~1 s).
        # Phase is CIRCULAR: a linear sd reports an event near the period boundary
        # as maximally scattered, which is how a locked run first looked unlocked.
        P = tm["period_s"]
        ang = 2*np.pi*(fr[:, 0] % P)/P
        R = float(np.abs(np.mean(np.exp(1j*ang))))
        mu = (float(np.angle(np.mean(np.exp(1j*ang)))) % (2*np.pi))*P/(2*np.pi)
        csd = np.sqrt(max(-2*np.log(max(R, 1e-12)), 0.0))*P/(2*np.pi)
        Z = len(ang)*R*R
        dev = ((fr[:, 0] % P) - mu + P/2) % P - P/2
        print(f"phase lock: R = {R:.3f}  (1 = perfect), circular sd {csd*1e3:.0f} ms, "
              f"mean phase {mu:.3f} s")
        print(f"            Rayleigh Z = {Z:.1f} vs uniform; "
              f"80% of injections within +-{np.percentile(np.abs(dev),80)*1e3:.0f} ms")
        print(f"            event is 235 ms long in a {P*1e3:.0f} ms period")
    np.savez_compressed(a.out, trace=tr, fires=fr, raw=rw, counts=np.array(counts),
                        period_s=tm["period_s"], reps=tm["repeats"],
                        chip_vpp=tm["chip_vpp"], thresh_mv=a.thresh,
                        full_mv=a.full, max_hz=MAX_HZ, spikes_file=rec_path,
                        monitor_neuron=NEURON, syn=a.syn, weight=WEIGHT,
                        gate_pre_mvpp=p2p_pre, gate_quiet_mvpp=p2p_quiet,
                        gate_post_mvpp=p2p_post, free_run_hz=aer_free / GATE_S,
                        drops=drops, stalls=stalls, bias_file=a.bias,
                        note="differs from the 2026-08-26 20:xx runs: different "
                             "synapse, different excitability, LNA output DC moved "
                             "~1.67 V -> ~1.26 V")
    print(f"\ndata: {os.path.basename(a.out)} + {os.path.basename(rec_path)}")


if __name__ == "__main__":
    sys.exit(main())
