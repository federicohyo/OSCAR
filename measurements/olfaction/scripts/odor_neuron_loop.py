#!/usr/bin/env python3
"""Host-in-the-loop odor detection: LNA -> host -> neuron 9.

    ../.venv-meas/bin/python3 LNA/odor_neuron_loop.py

WHAT CLOSES THE LOOP. The RISC-V core sees spikes rather than the amplifier -- the LNA output
reaches the core only through the host -- so the host does the detection:
it reads the LNA output from the scope stream, and when the output rises above a
baseline-relative threshold it injects spikes into neuron 9 through the bridge.
The chip amplifies and the chip spikes; the decision between them is made off-die.
This is a host-in-the-loop demonstration and must be described as one.

THRESHOLD IS BASELINE-RELATIVE rather than an absolute voltage: the amplifier's output
DC wanders by tens of millivolts over minutes, so a fixed level would drift into
either permanent firing or permanent silence. The baseline is a trailing median
over a window longer than the event, so the event itself leaves it steady.

RATE CODING. Excess over threshold is mapped to an input spike rate. Measured
transfer at vleakn = 0.34: 6 Hz in -> 18 spikes, 30 -> 66, 60 -> 73, 119 -> 89;
monotonic and compressive, so output rate encodes amplitude.

The live signal is smoothed over 25 ms before thresholding. That rejects the
272 Hz bench interferer, which would otherwise cross the threshold on its own,
and costs ~12 ms of latency against a 235 ms event.

Everything is saved: the scope trace, every injection time, and the chip's own
spike timestamps, so the alignment can be checked afterwards rather than assumed.
"""
import argparse, json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))
sys.path.insert(0, HERE)
from meas_common import BridgeSession
from lna_audio_sweep import Scope

NEURON, SYN, WEIGHT = 9, 0, 15
SMOOTH_S   = 0.025
BASELINE_S = 1.20
THRESH_MV  = 40.0      # chosen offline on the recorded raw trace: at 25 ms
                       # smoothing every crossing at 40 mV falls inside the event,
                       # while 30 mV admits a ~20% false-positive tail
FULL_MV    = 60.0      # excess mapping to the maximum input rate; the event
                       # peaks near 88 mV, so this ramps over its usable span
MAX_HZ     = 120.0
TICK_S     = 0.004


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav", default=os.path.join(HERE, "odor_stimulus.wav"))
    ap.add_argument("--timing", default=os.path.join(HERE, "odor_timing.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "odor_neuron_loop.npz"))
    ap.add_argument("--settle", type=float, default=4.0)
    ap.add_argument("--dry", action="store_true", help="detect but inject nothing")
    a = ap.parse_args()
    tm = json.load(open(a.timing))
    dur = tm["wav_s"] + 3.0

    rec = os.path.join(HERE, "odor_neuron_spikes.txt")
    subprocess.run(["pkill", "-x", "pw-play"], capture_output=True)

    with BridgeSession() as br:
        br.send(f"MASK {1 << NEURON}"); time.sleep(0.3)
        br.program_weight(SYN, WEIGHT, True); time.sleep(0.05)
        br.route(SYN, NEURON, True); time.sleep(0.05)
        br.send(f"RECORD {rec}"); time.sleep(0.3); br.drain()

        sc = Scope(); sc.drain(a.settle)
        buf_t, buf_v = [], []
        nsm = max(1, int(SMOOTH_S * 1000))
        nbl = max(1, int(BASELINE_S * 1000))

        print(f"settling done. threshold = baseline + {THRESH_MV:.0f} mV, "
              f"rate 0..{MAX_HZ:.0f} Hz over {FULL_MV:.0f} mV"
              + ("   [DRY RUN -- no injection]" if a.dry else ""))
        # prime the baseline before the tone starts
        t0 = time.time()
        while time.time() - t0 < BASELINE_S + 0.3:
            for _, vv in sc._read(): buf_v.append(vv)
        player = subprocess.Popen(["pw-play", "--", a.wav],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  start_new_session=True)
        t_start = time.time()
        fires, trace, nfire = [], [], 0
        next_fire = 0.0
        # WARM-UP. The baseline is a trailing median, and when the tone starts that
        # window is still full of pre-tone quiet, so early stimulus content reads as
        # a large excess and fires spuriously. Measured: the first repeat drew 11 of
        # 30 injections and every one of the far-off-phase outliers. Inject nothing
        # until one full period of tone has passed through the baseline window.
        WARMUP = BASELINE_S + tm["period_s"]
        try:
            while time.time() - t_start < dur:
                for _, vv in sc._read():
                    buf_v.append(vv)
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
                if exc_mv > THRESH_MV:
                    frac = min(1.0, (exc_mv - THRESH_MV) / max(FULL_MV - THRESH_MV, 1e-6))
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
            counts = br.drain()
            br.send("RECORDSTOP"); time.sleep(0.4)
            sc.close()

    tr = np.array(trace)
    fr = np.array(fires) if fires else np.zeros((0, 3))
    print(f"\n{len(tr)} control ticks over {dur:.1f} s")
    print(f"injections : {nfire}   (warm-up {BASELINE_S + tm['period_s']:.1f} s excluded)")
    print(f"spikes from neuron {NEURON}: {counts[NEURON]}   (all others: {sum(counts)-counts[NEURON]})")
    if nfire:
        print(f"excess at injection: {fr[:,1].min():.0f} .. {fr[:,1].max():.0f} mV")
        print(f"instantaneous rate : {fr[:,2].min():.0f} .. {fr[:,2].max():.0f} Hz")
        # Phase is CIRCULAR. A linear standard deviation on it reports an event
        # sitting near the period boundary as maximally scattered, which is how a
        # perfectly locked run first looked unlocked here.
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
    np.savez_compressed(a.out, trace=tr, fires=fr, counts=np.array(counts),
                        period_s=tm["period_s"], reps=tm["repeats"],
                        chip_vpp=tm["chip_vpp"], thresh_mv=THRESH_MV,
                        full_mv=FULL_MV, max_hz=MAX_HZ, spikes_file=rec)
    print(f"\ndata: {os.path.basename(a.out)} + {os.path.basename(rec)}")


if __name__ == "__main__":
    sys.exit(main())
