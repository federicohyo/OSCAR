# The ground loop: what was measured, in the order it was measured

All figures below are the **LNA output node**, read through the pixhawk ADC at
1000 S/s. "hum" is the rms of the whole record; "at rail" is the fraction of
samples at or above 1.775 V. Reference point: this morning, before the bench was
moved, the quiet node read **22.6 mV rms, 0% at rail**.

## 1. The symptom, and why it hid for hours

Every gain measurement taken after the move was unstable (46× … 258× for the
same drive) while every quiet baseline looked fine. That combination is the whole
story: **the noise was present only while the sound card was active** — i.e. only
during a gain measurement, and never during a baseline.

It also explains the symptom Federico reported independently: drive the amplifier,
stop, and "noise appears after 2–3 s and gets amplified." Nothing switches on.
Under drive the output is compressed against the rail, which squashes everything
else; when the drive stops the operating point walks back out of compression over
a couple of seconds and the full gain lands on pickup that was there all along.

## 2. Removing the sources, one at a time

Quiet node, no tone playing, 60 s record each time:

| state | hum (rms) | 60 Hz | 120 Hz | 180 Hz | DC |
|---|---|---|---|---|---|
| dock + 2nd scope connected | **126.9 mV** | 77.5 mV | 117.4 mV | 88.5 mV | 1.461 V |
| DisplayLink dock unplugged | **57.7 mV** | 47.1 mV | 66.5 mV | 59.0 mV | 1.569 V |
| 2nd bench scope unplugged | **17.9 mV** | — gone — | — gone — | — gone — | 1.667 V |

The interferer was a **60 Hz fundamental with a full harmonic ladder** (60, 120,
180, 240, 300, 360 Hz). Two things follow:

- **It was not mains.** This bench is on 50 Hz and there was essentially nothing
  at 50 Hz.
- **It was not sinusoidal.** A pure tone gives one line; a full ladder means a
  sharp, pulsed source. 60 Hz is the display refresh rate.

Removing the second bench scope — which was monitoring the **LNA input**, and
whose earth closed the loop — took the ladder out entirely and returned the
output DC to its 1.667 V working point.

## 3. The decisive test: playing silence

The clinching measurement. A WAV of **zero amplitude** was played through the
same path — same `pw-play`, same jack, no tone at all:

| state | DC | hum (rms) | at rail | strongest lines |
|---|---|---|---|---|
| nothing playing | 1.6675 V | **24.4 mV** | 0.0% | 120 Hz @ 30 mV, 60 Hz @ 24 mV |
| **silent WAV playing** | 1.5763 V | **178.8 mV** | **10.4%** | 120 Hz @ 269 mV, 60 Hz @ 228 mV |
| stopped again | 1.6660 V | **24.4 mV** | 0.0% | 120 Hz @ 31 mV, 60 Hz @ 24 mV |

Merely opening the audio output raised the noise 7×, brought back the ladder,
dragged the DC down 90 mV and pushed a tenth of all samples into the rail —
with no signal present. Reversible, in both directions, returning to 24.4 mV
exactly.

**Conclusion:** activating the sound card's output stage coupled the 60 Hz ladder
in through the audio cable's ground. That is why gain measurements were poisoned
and baselines were not.

## 4. Why the contaminated numbers were wrong, not just noisy

The pickup saturated the amplifier against the 1.78 V rail (9–37% of samples in
the affected runs). A coherent sine fit through a clipped waveform reports an
**inflated** amplitude, so the readings did not merely scatter — they were biased
upward. The 156×, 220× and 258× figures came from there.

Diagnostic separation between contaminated and clean runs:

| | contaminated (afternoon) | clean (this campaign) |
|---|---|---|
| fit error bar | 2.71–2.79 mV | 0.18–0.51 mV |
| h2 | 7.0–7.2% | 0.5–5.4% |
| samples at rail | 9–37% | 0.0% |
| repeat guard | 6.8–53.6% | 0.06–3.7% |

## 5. The earlier campaign's data is unaffected

The earlier data was measured before the bench was moved, and carries its own evidence
of a quiet bench: fit error bars of 0.41–1.49 mV, h2 of 0.6–3.9%, no samples at
the rail, and `lna_noise.csv` giving an output ASD near 55 Hz of
7.4 × 10⁻⁴ V/√Hz. The 60 Hz line seen this afternoon was ~228 mV; had it been
present that morning it would have stood roughly a thousand times above that
floor and been impossible to miss.

## 6. What must stay unplugged

The **second bench scope on the LNA input**. Re-plugging it restores the ground
loop. The practical cost is that the LNA input can no longer be probed directly,
so no drive-path reference pass is possible — see the assumption recorded in
`../README.md`.

## 7. Still open

A fixed narrowband line at **271.9 Hz** (with others at 87.4 and 184.5 Hz)
survived every step above and is present in the final noise record. It is small
compared to what was removed, but it is a real, repeatable interferer and worth
finding before the odor measurement, where the signal of interest is only a few
mV at the chip.
