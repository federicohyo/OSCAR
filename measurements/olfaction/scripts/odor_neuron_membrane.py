#!/usr/bin/env python3
"""Capture the membrane of neuron 9 while replaying the odor-evoked injection train.

    ../.venv-meas/bin/python3 LNA/odor_neuron_membrane.py

The readout ADC is single-channel, so the amplifier and the membrane are captured one at a
watched at once and the closed loop needs the amplifier. This pass therefore
replays, verbatim, the injection train that the closed-loop run produced, and
records the membrane instead. The neuron's output leaves the input origin unreported, so
from, and the replayed times are ones we command exactly rather than detect, so
the input timing here is better defined than a live pass would be.

Saves the whole membrane trace, the injection times and the chip's spike stamps.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meas_common import BridgeSession
from lna_audio_sweep import Scope

HERE = os.path.dirname(os.path.abspath(__file__))
SCHED = "/tmp/claude-1000/-storage-tue-avlsi2024-sw/44279eef-612f-4a6a-a16c-abc5bb0ff302/scratchpad/inj_schedule.npy"
NEURON, SYN, WEIGHT = 9, 0, 15

sched = np.load(SCHED)
rec = os.path.join(HERE, "odor_neuron_membrane_spikes.txt")
with BridgeSession() as br:
    br.send(f"MASK {1 << NEURON}"); time.sleep(0.2)
    br.monitor(NEURON); time.sleep(0.4)
    br.program_weight(SYN, WEIGHT, True); time.sleep(0.05)
    br.route(SYN, NEURON, True); time.sleep(0.05)
    br.send(f"RECORD {rec}"); time.sleep(0.3); br.drain()
    sc = Scope(); sc.drain(2.0)

    tv, vv, fired = [], [], []
    t0 = time.time() + 1.0
    # one consistent time base throughout: seconds relative to t0. The pre-roll
    # previously logged the scope's own board clock here while the main loop logged
    # relative time, producing an array that mixed the two.
    while time.time() < t0:
        for _a, b in sc._read(): tv.append(time.time()-t0); vv.append(b)
    i = 0
    end = t0 + sched[-1] + 1.5
    while time.time() < end:
        now = time.time() - t0
        for _a, b in sc._read(): tv.append(time.time()-t0); vv.append(b)
        if i < len(sched) and now >= sched[i]:
            br.send("BURST 1"); fired.append(now); i += 1
        time.sleep(0.001)
    time.sleep(0.5)
    counts = br.drain(); br.send("RECORDSTOP"); time.sleep(0.4)
    sc.close()

v = np.asarray(vv, float); t = np.asarray(tv, float)
print(f"membrane trace: {len(v)} samples over {t[-1]:.1f} s")
print(f"  rest {np.median(v):.4f} V   min {v.min():.4f}   max {v.max():.4f}")
print(f"  injections replayed: {len(fired)}/{len(sched)}")
print(f"  spikes from neuron {NEURON}: {counts[NEURON]}")
thr = np.median(v) + 0.25*(v.max()-np.median(v))
above = v > thr
nsp = int(np.sum(above[1:] & ~above[:-1]))
print(f"  membrane excursions above {thr:.3f} V: {nsp}")
np.savez_compressed(os.path.join(HERE, "odor_neuron_membrane.npz"),
                    t=t, v=v, fired=np.array(fired), sched=sched,
                    counts=np.array(counts), spikes_file=rec)
print(f"\ndata: odor_neuron_membrane.npz + {os.path.basename(rec)}")
