# LNA re-measurement — clean setup, 2026-08-26 (chip0)

Re-measurement of the LNA after the bench was moved and a **ground loop was
found and removed**. The setup is now at its quietest and highest-gain state of
the day.

**This is a NEW operating point, not a correction of the earlier campaign.** The bias file
in force differs from the one used earlier, and the gain is
~3× higher. The two sets of numbers describe different bias points and must not
be mixed. See "Relationship to the earlier measurement" below.

| | this campaign | earlier campaign (`../../README_MEASUREMENTS.md`) |
|---|---|---|
| `lna_iref` (the one bias that differs) | **1.079 V** | 1.5 V |
| midband gain | ~272–293× (48.5–49.3 dB) | 97.7× (39.8 dB) |
| usable input | ≤ ~900 µVpp | 400 µV – 7 mVpp |
| raw traces kept | **yes** | no (listed as an open item there) |

---

## What is here

```
setup/      exact bias file in force + the bench state it was measured in
raw/        ONE .npz PER MEASURED POINT: the full scope trace + its metadata
derived/    one CSV per block, checkpointed after every point
figures/    the three figures, .png and .pdf
scripts/    the code that produced all of it
debug/      evidence for the ground-loop diagnosis (03 is the write-up)
```

Every number in `derived/` is reproducible from `raw/`, and every figure is
rebuildable with no bench:

```bash
/storage/tue/avlsi2024-sw/.venv-meas/bin/python3 scripts/analyze.py
```

Each `raw/<block>/<tag>.npz` holds `t` (seconds, 1 ms grid), `v` (volts at the
LNA output) and the metadata needed to interpret it: `freq_hz`, `jack_vpp`,
`divider`, `vin_pp`, `settle_s`, `window_s`, `utc`.

---

## Method

- **Chip read-only.** No FTDI opened, no DAC written; the GUI and
  `neuron_bridge.py` held the device throughout. Only audio out and the scope
  server were used.
- **60 s settling after every drive change.** The amplifier needs ~40 s and the
  runs that used 38 s were the marginal ones all afternoon.
- **Decommensurate drive frequencies.** A round frequency lands a whole number of
  samples per cycle on the 1 kS/s grid and freezes the sampling phase.
- **One continuous WAV per point**, outlasting settle + window, so no `pw-play`
  relaunch gap falls inside a measurement window.
- **Coherent least-squares sine fit** at the known drive frequency, with 2f/3f and
  a linear trend fitted alongside. Never a peak-to-peak or percentile spread.
- **First point repeated last** as a repeat guard. >10% spread invalidates a block.
- Input amplitude is `jack_vpp × 0.028`, the original resistive divider.

---

## Results

Five blocks, all at 88.57 Hz unless stated. Every block carries its own repeat
guard; all passed.

| block | what | guard |
|---|---|---|
| `gain_vs_level` | main ladder, 150–900 µVpp | **0.06%** |
| `gain_vs_level` (S) | low-end extension, 40–100 µVpp | 2.8% |
| `gain_crosscheck` | 100/150/200 µVpp back to back | 0.7% |
| `transfer` | 21 frequencies, 0.21–400 Hz | 3.7% |
| `noise` | 8 × 30 s quiet blocks | — |

**All gains below are quantisation-corrected.** `make_wav` writes 16-bit PCM, and
at these levels a tone is only tens of counts tall — the 40 µVpp drive is 16
counts. The delivered fundamental is therefore systematically *low*: −3.8% at
40 µVpp, −0.16% at 900 µVpp. Dividing by the nominal input under-states gain,
worst exactly where the signal is smallest. `analyze.py:true_drive()` fits the
real amplitude out of each WAV and uses that as the x-axis.

### Gain vs frequency — `figures/gain_vs_frequency.png`

**48.55 dB (267.7×) midband**, flat to within 1% from 28 Hz to 188 Hz
(265.6 / 268.0 / 270.3 / 270.2 / 267.4 / 266.3 ×). Roll-off above ~200 Hz is
real: 253.7× at 274 Hz, 223.3× at 400 Hz.

**−3 dB at 1.53 Hz** after the drive path is divided out; the raw chain reads
1.91 Hz. Both curves are plotted — the gap between them is the sound card's own
AC coupling, not the amplifier.

Against the earlier campaign (39.8 dB, corner 0.49 Hz) gain and corner moved **up together**.
That is what a higher-gain bias point does: the same DC-restoration element now
works against more loop gain.

### Gain vs input amplitude — `figures/gain_vs_level.png`

14 points over a 23× span of input (39–898 µVpp), from three blocks plotted
separately — merging them would invent structure that is partly elapsed time.

| input | gain | h2 |
|---|---|---|
| 38.5 µVpp | 285.4× | 1.5% |
| 68.3 µVpp | 280.7× | 0.8% |
| 98.5 µVpp | 280.3× | 1.8% |
| 148.5 µVpp | 296.3× | 1.4% |
| 298.5 µVpp | 277.4× | 2.2% |
| 498.4 µVpp | 266.8× | 3.2% |
| 698.5 µVpp | 272.0× | 5.3% |
| 898.5 µVpp | 273.4× | 5.4% |

**Gain falls with drive**: `gain = a − 7.1·ln(vin)`, r = −0.64 against log input.
Roughly 7.6% of compression across the full 23×. h2 rises with level as expected,
0.8% → 5.4%.

**Two negative results worth recording, because both look plausible and both are
wrong:**

- *The 150 µVpp "bump" is not real.* The main ladder read 296.3× there, twice,
  0.07% apart — 6% above both neighbours. But those neighbours came from other
  blocks. Measuring 100/150/200 µVpp **back to back in one block** gives
  279.9 / 287.0 / 285.9×: a step of ~2.5%, not 6%. The rest was block-to-block
  drift. At ~2.5% it is comparable to the scatter and should not be called a
  feature.
- *Output DC does not set the gain.* Within the cross-check block gain appeared
  to track DC neatly. Across all 20 gain points the correlation is **+0.012** —
  nothing. Adding DC to a fit that already has input level moves the residual
  only 2.54% → 2.40%. The apparent link was a four-point coincidence.

**Reproducibility, stated honestly:** within a block, 0.06–2.8%. Across blocks
separated by tens of minutes, ~2.5–3%. Quote absolute gain as **~270–290×
(48.6–49.2 dB) ± 3%**, not to three digits.

The ladder stops at ~900 µVpp because at ~270× that is where the 1.78 V rail
arrives. Nothing in any block touched the rail; the output DC sags from 1.673 to
1.630 V as drive rises, opening headroom about as fast as the signal needs it.

### Noise — `figures/noise.png`

8 × 30 s quiet blocks, sound card **idle** (not merely silent — activating its
output stage was itself the fault this campaign exists to escape). 48 Welch
averages, 8192-point segments.

| | this campaign | earlier campaign |
|---|---|---|
| input-referred at 1 Hz | **6.8 µV/√Hz** | 12.4 µV/√Hz |
| at 10 Hz | 2.24 µV/√Hz | — |
| floor, 20–300 Hz | **1.85 µV/√Hz** | — |
| integrated | 34 µV rms (1–300 Hz) | 137 µV rms (0.2–300 Hz) |

The integrated figures are over **different bands** and are not comparable
directly. The improvement at 1 Hz is largely because we divide by ~3× more gain,
not because the amplifier itself got quieter.

Input-referring uses the **corrected amplifier gain**, not the raw chain — below
~20 Hz the raw curve is mostly the sound card, and dividing by it would inflate
the input-referred noise by the sound card's own roll-off.

Narrowband lines are found **generically**, as bins standing >3× above a running
median of their neighbourhood, not by assuming mains. On this bench they are not
mains: the strongest sit at **87.4, 184.5 and 271.9 Hz**. The 271.9 Hz line was
present in every quiet measurement taken this evening, including before this
campaign began — it is a fixed interferer in the bench and is worth finding
before the odor run, where the signal of interest is a few mV at the chip.

The output DC held at 1.634–1.645 V across the whole 4-minute noise record, with
0.00% of samples at the rail in every block.

## Assumptions and caveats

- **The bias record is not a readback.** `setup/biases_in_force.biases` is the
  file that was written. The DACs are write-only and the GUI's sliders do not
  reflect the chip, so nothing here can confirm the chip's actual bias state. If
  the GUI was touched after 16:57, this record is stale.
- **No reference pass was taken.** Correcting the sound card's own AC-coupled
  roll-off below ~20 Hz needs a probe on the divider output — and that probe is
  the instrument whose earth caused the ground loop this campaign exists to
  escape. So the transfer block reports the **raw chain**, and any low-frequency
  correction reuses the previous campaign's `../../lna_transfer_ref.csv` shape.
  That reuse assumes the sound card's response is unchanged: same laptop, same
  jack, same mixer setting, and only the *shape* is used. It is an assumption,
  not a measurement.
- **Absolute level rides on the mixer setting**, unchanged since the original
  0.25 Vpp → 7 mVpp anchor. Nothing in this campaign re-verifies that anchor.
- The gain ladder spans 23× in input (39–898 µVpp), against the earlier campaign's 17.5×,
  but sits an order of magnitude lower: 39–898 µVpp against 400 µV–7 mVpp. The
  top is a hard headroom limit — at ~270× the rail arrives near 900 µVpp — and
  the bottom is set by the fit's own error bar (~1.7% at 40 µVpp), not by taste.
- **The drive-quantisation correction is essential at the low end, and it is
  snapshotted, not recomputed.** `setup/drive_calibration.csv` holds the fitted
  true amplitude of every WAV used. `analyze.py` reads that first, the WAV
  second, and falls back to nominal only with a loud warning — the WAVs live
  outside this archive (~270 MB), and a silent fallback would quietly un-correct
  the low-end gains by up to 4%. Verified: with the WAV directory removed
  entirely, every figure rebuilds to identical numbers.

---

## Relationship to the earlier measurement, and one open reconciliation

The earlier campaign (`../../README_MEASUREMENTS.md`) is unaffected by anything here.
Its data was taken before the bench was moved, and it carries its own evidence
of a quiet bench: fit error bars of 0.41–1.49 mV against 2.71–2.79 mV for the
afternoon's contaminated runs, h2 of 0.6–3.9%, and no samples at the rail.

**RESOLVED — the write-up has been updated.** It attributed a 10.2 dB gap
between simulated (50.05 dB) and measured (39.8 dB) gain to parasitic capacitance
across C₂. With `lna_iref` at 1.079 V the measured gain is 48.6 dB, within 1.5 dB
of simulation, so the capacitor ratio is close to drawn and the deficit at the
1.5 V setting was **insufficient OTA loop gain**, not parasitic C₂.

Two independent observations support loop gain over the capacitor ratio:
`lna_iref` was the only bias changed, and gain and corner moved **together**
(×2.7 and ×3.1). A change in C₂ alone would move them in *opposite* directions —
more C₂ means less gain but a *longer* feedback time constant, hence a lower
corner. Only the feedback factor scales both the same way.

The gain and noise figures were replaced accordingly and the parasitic-C₂
paragraph rewritten. Untested: whether the residual 1.5 dB closes with still
more bias current.
