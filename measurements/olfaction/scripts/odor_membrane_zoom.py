#!/usr/bin/env python3
"""One odor-evoked burst, captured fast enough to be a measurement of it.

    CARAVAN_CLK_MHZ=25 ../.venv-meas/bin/python3 odor_membrane_zoom.py

The pixhack streams both channels for the whole 16 s stimulus at 1 kHz -- right
for the event, the envelope and the alignment, wrong for the burst inside it.
The chip's own timestamps put the within-burst interspike interval at 1.368 ms,
so 1 kHz takes 1.4 samples per spike and returns an alias: 1000-731 = 269 Hz,
an apparent spike every 3.7 ms, which is exactly what the first attempt at a
zoomed inset drew.

This runs the closed loop unchanged and, while it runs, arms the Agilent
DSO-X 2002A on the same membrane node for ONE single-shot acquisition of one
real odor-evoked burst -- 50 kpts over 100 ms, 500 kSa/s, ~680 samples per
interspike interval instead of 0.7.

The scope is armed only after the loop's monitor gate has fired its test burst
(that burst would trigger it, and it is not part of the experiment) and after
the detector's warm-up period, so what triggers is an injection the amplifier
actually asked for.
"""
import argparse, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("CARAVAN_CLK_MHZ", "25")
from agilent_scope import Agilent

PY = sys.executable


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm-after", type=float, default=12.0,
                    help="seconds after the loop starts before arming (must clear "
                         "the monitor gate's own burst and the detector warm-up)")
    ap.add_argument("--span", type=float, default=0.100, help="capture window, s")
    ap.add_argument("--level", type=float, default=0.95, help="trigger level, V")
    ap.add_argument("--points", type=int, default=50000)
    ap.add_argument("--out", default=os.path.join(HERE, "odor_membrane_zoom.npz"))
    ap.add_argument("--chan", type=int, default=2)
    # Passed through to the loop. At the 2026-08-27 operating point the neuron
    # needs > ~20 Hz of input to fire at all and ceilings at ~8 Hz out, so the
    # detector's rate mapping has to span its range instead of grazing 27 Hz.
    ap.add_argument("--thresh", type=float, default=25.0)
    ap.add_argument("--full", type=float, default=45.0)
    ap.add_argument("--bias", default=os.path.join(
        HERE, "biases", "bias_LNA_50dB-meas-neuron9spikes-10Hz.biases"))
    a = ap.parse_args()

    loop = subprocess.Popen(
        [PY, os.path.join(HERE, "odor_neuron_loop_dual.py"), "--syn", "15",
         "--thresh", str(a.thresh), "--full", str(a.full),
         "--out", os.path.join(HERE, "odor_neuron_loop_dual_zoom.npz")],
        cwd=os.path.dirname(HERE), env=dict(os.environ, CARAVAN_CLK_MHZ="25"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    with Agilent() as sc:
        print(sc.idn())
        t0 = time.time()
        # Drain the child's output while waiting, keeping the pipe flowing.
        while time.time() - t0 < a.arm_after:
            ln = loop.stdout.readline()
            if ln:
                print("  loop |", ln.rstrip())
            if loop.poll() is not None:
                break
        print(f"\n>> arming: CH{a.chan}, {a.span*1e3:.0f} ms window, {a.points} pts "
              f"({a.points/a.span/1e6:.2f} MSa/s), rising through {a.level:.2f} V")
        sc.setup_single(chan=a.chan, span_s=a.span, level=a.level,
                        points=a.points, delay_frac=0.30)

        t_arm = time.time()
        triggered = False
        while time.time() - t_arm < 40.0:
            if sc.triggered():
                triggered = True
                break
            ln = loop.stdout.readline()
            if ln:
                print("  loop |", ln.rstrip())
            if loop.poll() is not None and time.time() - t_arm > 25:
                break
        if not triggered:
            print("!! scope armed but untriggered -- the injection stayed below "
                  f"{a.level:.2f} V on CH{a.chan} while armed")
        else:
            t, v = sc.read_waveform(a.chan)
            print(f">> captured {len(v)} pts, "
                  f"{1.0/np.median(np.diff(t))/1e6:.3f} MSa/s, "
                  f"span {(t[-1]-t[0])*1e3:.1f} ms, {v.min():.3f}..{v.max():.3f} V")
            np.savez_compressed(a.out, t=t, v=v, chan=a.chan, level=a.level,
                                span_s=a.span, note="Agilent DSO-X 2002A, single "
                                "shot on one odor-evoked burst; pixhack streams the "
                                "same node at 1 kHz for the event-scale panels")
            print(f">> {os.path.basename(a.out)}")
        sc.w(":RUN")

    for ln in loop.stdout:
        print("  loop |", ln.rstrip())
    loop.wait()
    return 0


if __name__ == "__main__":
    sys.exit(main())
