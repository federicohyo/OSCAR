# Bench state for this campaign — 2026-08-26, from ~17:30

## Why this campaign exists

The setup was physically moved earlier today. Everything measured between the
move and ~17:20 is unreliable, and the reason is documented in `../debug/`:
a **ground loop through a second bench scope** that was monitoring the LNA input.
It injected a 60 Hz harmonic ladder that appeared **while the sound card was
active**, i.e. during a gain measurement, while baseline checks stayed clean.

The earlier campaign's data predates the move and is unaffected — see `../README.md`.

## The chain

```
audio jack -> two-resistor divider (purely resistive, flat) -> LNA input
LNA output -> pixhawk ADC -> server.py -> TCP 127.0.0.1:5555
```

- **Divider: the ORIGINAL one, 2.8%.** 0.25 Vpp at the jack gives 7 mVpp at the
  chip. A 6.67% divider was tried this afternoon and removed again; measured, it
  delivered ~1.67%. All `vin_pp` columns use 0.028.
- **Readout: 1000 S/s, unipolar (0 .. ~1.78 V), 0.805 mV/step.**
- **Leave the mixer volume untouched** — the absolute input calibration rides on
  its current setting, exactly as in the previous campaign.

## What is unplugged, and must stay unplugged

| item | why |
|---|---|
| **the second bench scope on the LNA input** | its earth closed the ground loop. Re-plugging it brings the 60 Hz ladder back and invalidates everything. |
| **the DisplayLink ThinkPad dock** | contributed roughly half the pickup (126.9 -> 57.7 mV rms when removed). |

Consequence: with the second scope gone, **the drive-path correction reuses the
earlier `lna_transfer_ref.csv` shape** rather than a fresh probe, since a new
`--ref` pass would reintroduce the fault — see the assumption stated in
`../README.md`.

## Bias state

**Treat the GUI as the authority on the chip's bias state; the `.biases` files on
disk are occasional snapshots.** Federico adjusts biases live in the GUI, and the
GUI's state is the authority; files are written from it occasionally, and a save
can capture GUI defaults rather than the latched point (`[[gui-chip-bias-desync]]`).
`biases_in_force.biases` is a copy taken at 18:00:37, two minutes before the
campaign began, and is the best available record. The bias DACs are write-only,
so the chip's actual state is what the GUI holds.

**What actually changed between the earlier dataset and this one**, per Federico:
a single bias, `lna_iref` — the gate of the PMOS current source setting the input
pair's tail current.

| | earlier dataset | this campaign |
|---|---|---|
| `lna_iref` | 1.5 V | **1.079 V** |
| midband gain | 39.8 dB (97.7x) | **48.6 dB (268x)** |
| −3 dB corner | 0.49 Hz | **1.53 Hz** |

PMOS, so *lower* gate voltage means *more* current, more input-pair $g_m$, more
OTA open-loop gain, and a closed-loop gain nearer the ideal $C_1/C_2 = 369\times$:
26% of ideal at 1.5 V, 73% at 1.079 V.

**Correction to an earlier version of this file.** It previously claimed three
channels differed (`lna_iref` 1.0790→1.1217, `VB1` 0.8617→0.5340, `VB2`
0.8740→1.0087), inferred by diffing the files. That inference has been superseded
twice over: those values belonged to a version of `..._1.5v2.biases` saved at
16:57 and replaced at 17:54, before any measurement here; and the files capture
the GUI at save time. Consider the three-channel claim superseded.

## Discipline applied to every point

- **60 s settling** after every drive change. The morning's trustworthy runs are
  labelled `levels_60s_settle`; 38 s runs were the marginal ones all afternoon.
- **Decommensurate drive frequencies.** A round frequency freezes the sampling
  phase on the 1 kS/s grid.
- **One continuous WAV per point**, long enough to outlast settle + window, so a
  `pw-play` relaunch gap stays outside the measurement.
- **First point repeated last** as a repeat guard; >10% spread marks a block for re-run.
- **Raw traces saved for every point** under `../raw/`, alongside the fitted results.
- **Chip read-only**: the FTDI is left closed and DACs are left as set. The GUI
  and `neuron_bridge.py` keep the device throughout.
