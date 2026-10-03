# Synaptic weight-code characterization (2026-07-28, re-measured at 25 MHz 2026-08-02)

Data behind the synaptic weight-code figure (`../../measurements/plotting/make_synapse_weight.py`,
output `../../measurements/plotting/figures/weight_code.pdf`),
measured on neuron 5 / synapse 0, chip biased from
`ofxCaravanViewer/bin/bias_synapse_characterization_super_n5_jul10.biases`.

The weight-code figure now shows the 25 MHz measurement (`onset_n5_25mhz*`), with
25 MHz as the nominal shipping clock. The original 50 MHz run (`onset_n5*`) is kept: the two
together are the evidence that the calibration transfers across clock. See
"Does the calibration transfer across clock?" at the end of this file, and
`../../measurements/plotting/figures/weight_code_50mhz.pdf` for the superseded render.

## What the measurement is, and why it uses onset bias

The obvious experiment — sweep the programmed weight word, read the neuron's output rate —
gives a sharp threshold response on this die, which is itself a result:

- At every soma operating point reachable here the rate response is a **cliff**: below
  threshold the neuron is silent, and the moment delivered charge crosses threshold it
  fires at close to the input rate (~900 Hz for 800 Hz in). The transition is sharp.
- Lowering the leak to buy temporal summation makes the neuron **free-run**: at `w=0`, i.e.
  the synapse weight programmed to zero, it fires at 350–626 Hz (`vleakn <= 0.225`). Any
  "graded" curve measured there is spontaneous activity. **Always include `w=0` as
  the baseline** — it is what caught this.

So the rate carries one usable bit (fired / silent). Instead we use that sharp
threshold as a **null detector**: for each weight word, bisect the excitatory branch bias
until the word just brings the neuron to threshold. In weak inversion current is exponential
in gate voltage, so

    V_onset(w) = V0 - nUT * ln(A(w))

with `A(w)` the delivered charge in units of one branch. The onset bias is a **logarithmic
readout of synaptic efficacy** — graded and repeatable to ~1 mV, at a resolution beyond
what the firing rate alone gives.

## Results

Both clocks are stated, so this table describes two clocks explicitly. **The 25 MHz column
is what the reference figure now shows**; the two agree within the ±1 mV bisection
resolution, which is the point.

| quantity | 50 MHz (2026-07-28) | 25 MHz (2026-08-02) |
|---|---|---|
| `nUT` (weak-inversion slope) | **31.8 mV** → n ≈ 1.2 | **31.1 mV** → n ≈ 1.2 |
| one doubling of branch current | **22.1 mV** | **21.6 mV** |
| bit↔bias mapping | `JExcWn_j` drives weight bit `j`, 1:1, **independent** | same |
| branch mismatch, bits 0–2 | within **2 mV** of each other | within **4.1 mV** |
| bit 3 | **36 mV weaker** than bit 0 | **36.6 mV weaker** |
| binary code would need | 66 mV between bit 0 and bit 3 | 64.6 mV |

**Equal branch biases (as normally used):** delivered charge tracks `popcount(w)` rather than
`w`, giving 7 resolvable levels (3.0 effective bits) with order inversions exactly at the
binary carries `3→4`, `7→8`, `11→12`, where one equal branch replaces several. (At 25 MHz the
same data resolves 8 levels and a fourth inversion at `1→2`, because the bit-0/bit-1 mismatch
crosses the resolution test there; see the clock section below before quoting either count.)

**Calibrated bias ladder:** applying

    V_j = V + (V_onset,j - V_onset,0) + j * nUT * ln 2

(first term cancels each branch's mismatch, second builds the 1:2:4:8 ratio) makes the onset
fall **monotonically across all 15 non-zero words**, following `V0 - nUT*ln(w)` to within a
few mV: **14 resolvable levels, 3.9 of the nominal 4 bits.**

> The 4-bit code is real, and it is a property of the **biasing**; it must be calibrated per
> die. Once the branch biases are calibrated, the branches behave as binary-weighted.

## Files

| file | contents |
|---|---|
| `onset_n5.csv` / `.json` | equal branch biases: per-branch onsets, nUT fit, all 15 words |
| `onset_n5_ladder.csv` / `.json` | same 15 words re-measured under the calibrated ladder |
| `ladder_n5.json` | the computed per-branch offsets |

## Reproducing

```bash
./bringup_50.sh                                   # chip powers up on the 10 MHz crystal
CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 bench_bringup_check.py      # gate: confirms clean AER addressing

CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 synapse_onset.py \
    --neuron 5 --stages branches,slope,code --repeats 3 --spikes 150 \
    --rate 800 --lo 0.350 --hi 0.470 --tag n5

./.venv-meas/bin/python3 synapse_make_ladder.py --tag n5

CARAVAN_CLK_MHZ=50 ./.venv-meas/bin/python3 synapse_onset.py \
    --neuron 5 --stages code --repeats 3 --spikes 150 --rate 800 \
    --lo 0.295 --hi 0.455 --ladder results/synapse/ladder_n5.json --tag n5_ladder

./.venv-meas/bin/python3 measurements/plotting/make_synapse_weight.py --tag n5 --ladder-tag n5_ladder
```

The bracket `--lo/--hi` must contain the onsets: the ladder shifts them ~85 mV lower, which
is why run 2 uses a lower bracket. A word whose onset lies outside the bracket gets the
out-of-range status rather than being clipped silently.

## Traps hit along the way (all fixed in the scripts)

1. **Host queue backlog, rather than chip behaviour.** The bridge delivers spikes over USB
   in ~16 ms batches. The original fixed ~80 ms tail drain truncated each point and spilled
   its remainder into the *next* one, so every reading reported the *previous* weight word.
   This produced order-dependent readings that looked like a bistable neuron latching for
   ~1 s after strong drive. `inject()` now **drains until the link has been quiet for
   250 ms**; with that fix the neuron goes silent immediately after drive. Same family of
   bug as `narma-collection-inputpath-bug`.
2. **Mask to the neuron you are recording** (`MASK 1<<neuron`). Every point reports
   `drop=0 stall=0`; masking to the recorded neuron keeps the UART below its ceiling, while
   at all-16 the UART saturates near the 1200 spk/s ceiling at 50 MHz and counts stop
   meaning anything.
3. **Re-programming the weight inside a bisection is repeated overhead.** The biases move
   within one word's search, so `P`/`S`/`M` and their settling are hoisted out — 120 s per
   onset became 8–10 s.
4. The old `Jexc_spikerate_w1_lab20260422.csv` behind the *previous* weight-code figure has
   `weight == 1` for every row: it swept the analog bias `JexcWn0_v` across all rows, so it
   supports the analog-bias contribution. The current figure uses the programmed weight word.

Chip state on exit: mask restored to all-16; neuron 5's `JExcWn*` left at the ladder values.
Every bench script loads its own biases, so a fresh run reloads its own settings.

---

## Does the calibration transfer across clock? (re-measurement, 2026-08-02)

Delivered synaptic charge falls as the core clock rises, mechanism under study. That raised a
fair question about the weight-code figure: if efficacy is
clock-dependent, is the calibration a 50 MHz artefact?

It transfers, and the argument for why is worth stating because it predicted the result. The
calibration is a **ratio between branches**, so a common-mode gain shift should cancel and
the ladder should transfer. We confirmed this by measurement: the
identical protocol was re-run at **25 MHz** on the shipping firmware
(`neuron_handshake_25MHz.hex`, byte-identical to a fresh `make hex F_CPU_MHZ=25
STREAM_SPIKES=1`), same neuron, same synapse, same 800 Hz drive, same soma bias file.

Keeping the soma bias fixed and letting the branch bias absorb the clock is what makes the
comparison clean: the null detector is held constant and only the quantity under test moves.

| quantity | 50 MHz | 25 MHz | difference |
|---|---|---|---|
| `nUT` | 31.84 ± 0.96 mV | **31.08 ± 0.96 mV** | −0.75 ± 1.36 mV (0.6 σ) |
| one doubling of branch current | 22.07 ± 0.67 mV | **21.55 ± 0.67 mV** | −0.52 ± 0.47 mV |
| slope factor `n` | 1.23 | **1.20** | — |
| bit-3 offset vs bit 0 | 35.6 mV | **36.6 mV** | +1.0 mV |
| equal biases | 7 levels / 3.0 bits | **8 levels / 3.17 bits** | resolution artefact, below |
| calibrated ladder | 14 levels / 3.9 bits | **14 levels / 3.91 bits** | identical |

**The constants agree within their uncertainty** — 0.6 σ, 2.4 % of `nUT`. The uncertainty is
the ±1 mV bisection floor: three repeats returned `sd = 0.000 V` on every single
onset at both clocks, so the error bars state the bisection resolution.

Per-branch onsets at 25 MHz (equal biases): bit 0 `0.4104`, bit 1 `0.4145`, bit 2 `0.4135`,
bit 3 `0.4470` V. Bits 0–2 span **4.1 mV** where a binary code needs 64.6 mV across the word;
bit 3 is **36.6 mV weaker**. Same picture as at 50 MHz.

**The one number that moved, and why it is a resolution artefact.** The equal-bias code
resolves 8 levels at 25 MHz against 7 at 50 MHz. The extra level is the bit-0/bit-1 pair:
they differ by 1.8 mV at 50 MHz (inside the 2 mV resolution test, so counted as one level)
and by 4.1 mV at 25 MHz (outside it, so counted as two). It is the same physical branch
mismatch crossing a threshold; the code is unchanged, and the inversion list grows from
{3→4, 7→8, 11→12} to {1→2, 3→4, 7→8, 11→12} for the same reason. **Quote 7 levels /
3.0 bits** unless the text explicitly says which clock and which resolution test produced
the count.

### Controls that were run

- **w = 0 at every stage, every bracket**: silent throughout `[0.350, 0.480]` V and
  `[0.290, 0.460]` V, so spontaneous activity stays separate from synaptic response.
- **Excitatory positive control before collection**: `bench_bringup_check.py` at 25 MHz,
  15/16 neurons decoding as themselves, neuron 5 returning 41 spikes from a 30-spike burst.
  Every conclusion here rests on this control, which licenses reading the onsets as
  synaptic response rather than as a mistuned array.
- **Telemetry headroom**: the 25 MHz ceiling is ≈600 spk/s, half the 50 MHz figure. Output
  rates at the fire/silent boundary are tens of Hz, the top of the bracket approaches the
  input rate, and every point ran with `MASK 1<<5` so neuron 5 streamed alone, with
  `inject()` draining until the link is quiet. The counts stay well below the ceiling.
- **Every DAC write logged** with value and timestamp to `logs/dac_writes_25mhz.log`
  (4752 writes). The DACs are write-only, so a bisection produces a fresh value sequence;
  the per-write log is what reconstructs the run.

### Files

| file | contents |
|---|---|
| `onset_n5_25mhz.csv` / `.json` | 25 MHz, equal branch biases: per-branch onsets, `nUT` fit, all 15 words, w=0 controls |
| `onset_n5_25mhz_ladder.csv` / `.json` | 25 MHz, same 15 words under the calibrated ladder |
| `ladder_n5_25mhz.json` | the computed per-branch offsets at 25 MHz |
| `logs/onset_n5_25mhz*.log` | run logs |
| `logs/dac_writes_25mhz.log` | every DAC write, value + timestamp |

### Reproducing

```bash
# flash the shipping 25 MHz image on the crystal (flash SCK scales with the core clock)
./.venv-meas/bin/python3 -c "import run_neuron_test as r; r.set_core_clock(10)"
cp firmware/neuron_handshake/binaries/neuron_handshake_25MHz.hex \
   firmware/neuron_handshake/neuron_handshake.hex
./.venv-meas/bin/python3 run_neuron_test.py --clock 10 --skip-dac

CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 bench_bringup_check.py    # gate + positive control

export CARAVAN_DAC_LOG=results/synapse/logs/dac_writes_25mhz.log
CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 synapse_onset.py \
    --neuron 5 --stages branches,slope,code --repeats 3 --spikes 150 \
    --rate 800 --lo 0.350 --hi 0.480 --tag n5_25mhz

./.venv-meas/bin/python3 synapse_make_ladder.py --tag n5_25mhz

CARAVAN_CLK_MHZ=25 ./.venv-meas/bin/python3 synapse_onset.py \
    --neuron 5 --stages code --repeats 3 --spikes 150 --rate 800 \
    --lo 0.290 --hi 0.460 --ladder results/synapse/ladder_n5_25mhz.json \
    --tag n5_25mhz_ladder

./.venv-meas/bin/python3 measurements/plotting/make_synapse_weight.py \
    --tag n5_25mhz --ladder-tag n5_25mhz_ladder --out weight_code.pdf
```

The ladder shifts the onsets ~85 mV lower at 25 MHz too, which is why the second run uses a
lower bracket. A word whose onset falls outside the bracket gets the out-of-range status
rather than being clipped silently.

**Chip state on exit:** 25 MHz image flashed, core left at 25 MHz. The DACs hold whatever the
last bias write left — `synapse_onset.py` restores `MASK 65535` while the bias point stays as
last written, and a subsequent positive-control scan wrote neuron 15's `_jul10` values.
Every bench script loads its own biases, so a fresh run reloads its own settings; the DACs
reflect the last write.
