# Plotting the results

This is the operation a user actually runs. Each row names a **result**
(what it plots), the **data file(s)** it needs, the **plotting script** in this
repository, and the **output file** the script writes — so the plots can be
produced from the archived data alone.

**Every figure below is produced from the data and scripts in this
repository.** The rows describe what each result plots, the data it reads and
the script that produces it.

Rows without a dedicated producer script are marked **[GAP]** and note how the
figure is produced. Non-data-driven floats are **[ASSET]** and are provided as
exported images under `docs/figures/`.

## Environment

Recreate the bench/measurement virtual environment and run every script with it
(absolute path shown; adjust to your checkout):

```bash
PY=/path/to/avlsi2024-sw/.venv-meas/bin/python3
# plotting scripts expect the repo root as CWD and imports resolved via PYTHONPATH
cd /path/to/OSCAR
PYTHONPATH=. "$PY" <script>
```

Most scripts only need `numpy`, `matplotlib`, `scipy`, `pandas`, `scikit-learn`.

## Path rewrite (applied to the scripts in this repository)

The reorganisation `results/`→`data/`, `LNA/`→`measurements/` invalidated
hardcoded paths in the original working tree. The scripts in this repository
have already been rewritten; the map below is what was applied, so you can
re-point any script that still references the old layout:

| Old path fragment (source tree) | New OSCAR path |
|---|---|
| `results/` | `data/` |
| `results/olf_validate/` | `data/olfaction/olf_validate/` |
| `results/synapse/` | `data/synapse/` |
| `LNA/` | `measurements/lna/` |
| `ofxLPM/scope-pixhawk-client/bin/data/` | `measurements/wet_pad/data/` |
| `LNA/<front-end-build>/figures/` | `measurements/lna/figures/` or `measurements/wet_pad/figures/` |
| `LNA/<riscv-build>/figures/` | `measurements/olfaction/figures/` |
| `<original-source>/RISCV_NeuronArray_2026/data/` | `data/array/` |
| `<original-source>/RISCV_NeuronArray_2026/figures/` | `measurements/array/figures/` |
| `<original-source>/micro/figures/` | `measurements/plotting/` |

Two scripts defined their repo root by counting directory levels and needed the
depth corrected in addition to the fragment rewrite:
`measurements/plotting/make_synapse_weight.py` and
`measurements/olfaction/scripts/make_fig_olfaction.py`. The LNA
`make_figures.py` now writes to `measurements/lna/figures/` and reads
`measurements/lna/data/`.

## Front-end / pad results

| Result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| System architecture | — (design asset) | — (asset export) | `docs/figures/arch_overview.pdf` / `.png` | **[ASSET]** exported system-overview float; no data. |
| **Hardware layout** | — (design assets) | — (one-time compose/export) | `docs/figures/fig_hardware_layout.{pdf,png}` | **[ASSET]** composed from `ISLPED2025-layout.png`, `skywater_2024_avlsi_chip_SNN_RISCV.jpg`, `19701130_045846_826317_daugther_chip.jpg`. Also the README figure. |
| LNA schematic | `design/xschem/` (LNA cell) | — | `docs/figures/lna_schematic.pdf` | **[GAP: no dedicated script]** produced manually from the LNA cell (xschem GUI → SVG/PDF). |
| LNA transfer, gain + noise (`fig12_lna_gain_noise.pdf`) | `measurements/lna/data/lna_transfer_final.csv`, `lna_transfer_ref.csv`, `lna_noise.csv` | `measurements/lna/clean_2026-08-26/scripts/make_figures.py` | `measurements/lna/figures/fig12_lna_transfer.pdf` (gain) **and** `fig14_lna_noise.pdf` (noise) | Script emits the two panels separately. The combined two-panel `fig12_lna_gain_noise.pdf` is produced manually → **[GAP: no dedicated script]**; recommend `make_fig12_gain_noise.py`. A reference copy of the combined asset is provided at `measurements/lna/figures/fig12_lna_gain_noise.pdf`. |
| TiO2 wet-transduction panels | `measurements/wet_pad/data/scope_20260829_094236.csv`, `scope_20260829_103015.csv` | `measurements/wet_pad/scripts/tio2_combi.py` | `measurements/wet_pad/figures/fig16_tio2_wetting.pdf`, `fig17_tio2_dilute3x.pdf` | Shadows: `tio2_three_panel.py`, `tio2_dilute3x_panel.py`, `tio2_injection_recovery.py`, `make_fig_saline_chain.py`. |
| Pad-evoked spiking | `measurements/wet_pad/data/scope_20260831_123139_single_payed_back_chip1_v1.csv` | `measurements/wet_pad/scripts/make_fig_pad_evoked.py` | `measurements/wet_pad/figures/fig18_pad_evoked_chip1.pdf` | |
| SOTA comparison | — | — | `docs/` Markdown/CSV (hand-entered) | Compiled from literature. |

## Array, calibration and olfaction results

| Result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| Domain map | — (design asset) | — (asset export) | `docs/figures/domain_map.{pdf,png}` | **[ASSET]** composed from the layout + die micrograph. |
| Weight-code words | `data/synapse/onset_n5.json`, `onset_n5_ladder.json` | `measurements/plotting/make_synapse_weight.py --panels b --out …` | `measurements/plotting/weight_code_words.pdf` | Default invocation emits the two-panel `weight_code.pdf`; `--panels b` emits the all-words panel. Inputs produced by `measurements/array/scripts/synapse_onset.py`. |
| Neuron FI insets | `data/array/neuron_fi_allneurons.csv`, `data/array/scope_{14,17,20}_neu14_if.csv` | `measurements/array/scripts/plot_fi_insets_all16.py --style compact --out …` | `measurements/array/figures/neuron_fi_reference.pdf` | Default output is `neuron_fi_all16_insets.pdf`; `--style compact` is the reference rendering. The three scope CSVs are required. |
| Classification pipeline row | `data/olfaction/olf_validate/*.npz` (one held-out chunk) | `measurements/olfaction/scripts/make_fig_pipeline1row.py` | `measurements/olfaction/figures/fig_pipeline_row.pdf` | Cross-imports `olfaction_bias_bo.py` and `make_fig_odorclass.py` (same `scripts/` dir; the script adds its dir to `sys.path`). |
| UART command set | `firmware/neuron_handshake/neuron_handshake.c` | — (derived) | `firmware/README.md` (Markdown table) | Derived from opcodes. |
| Odor capacity | `data/olfaction/olfaction_class_curve.json` ← `data/olfaction/olf_validate/*.npz` (9 acquisitions) | `measurements/olfaction/scripts/olfaction_class_curve.py`; figure `make_fig_olfaction.py` | `measurements/olfaction/figures/olfaction_capacity.pdf` + CSV/JSON | `make_fig_olfaction.py` re-verifies against the JSON and caches `data/olfaction/olfaction_k3.json`. |
| Energy per decision | `data/olfaction/olfaction_hybrid_score.json`, `olfaction_hybrid_slot.json`, `olfaction_mismatch_payoff.json` | `measurements/plotting/constants.py` | `measurements/plotting/energy_table.csv` | `constants.py` emits **CSV** (and prints the values). |
| SOTA comparison | — | — | `docs/` Markdown/CSV (hand-entered) | Compiled from literature. |

## Additional / shared result panels

These rows share the same scripts/data as above, so the panels can be
regenerated if wanted.

| Result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| LNA transfer | `measurements/lna/data/lna_transfer_final.csv`, `lna_transfer_ref.csv` | `measurements/lna/clean_2026-08-26/scripts/make_figures.py` | `measurements/lna/figures/fig12_lna_transfer.pdf` | High-gain point `V_iref = 1.08 V`. |
| LNA linearity | `measurements/lna/data/lna_gain_vs_level_ALL.csv` | `measurements/lna/clean_2026-08-26/scripts/make_figures.py` (or `run_gain_vs_level.py`) | `measurements/lna/figures/gain_vs_level_highgain.pdf` | |
| LNA noise | `measurements/lna/data/lna_noise.csv` | `measurements/lna/clean_2026-08-26/scripts/make_figures.py` | `measurements/lna/figures/fig14_lna_noise.pdf` | |
| Array characterization | `data/synapse/`, `data/array/` | `measurements/plotting/make_synapse_weight.py`, `measurements/array/scripts/plot_fi_insets_all16.py` | `measurements/plotting/weight_code_words.pdf`, `measurements/array/figures/neuron_fi_reference.pdf` | Shared. |
| Odor pipeline | `data/olfaction/olf_validate/*.npz` | `measurements/olfaction/scripts/make_fig_pipeline1row.py` | `measurements/olfaction/figures/fig_pipeline_row.pdf` | Shared. |
| Odor capacity | `data/olfaction/olfaction_class_curve.json`, `olfaction_class_curve_emul.json` | `measurements/plotting/make_olfaction_capacity.py` | `measurements/plotting/figures/olfaction_capacity.pdf` | Analog + emulated on RISC-V. |
| Energy by substrate | `data/olfaction/olfaction_hybrid_score.json`, `olfaction_hybrid_slot.json` | `measurements/plotting/constants.py`, `make_olfaction.py` | `measurements/plotting/energy_table.csv` | Shared. |
| Wet transduction / saline | `measurements/wet_pad/data/scope_20260829_*.csv` | `measurements/wet_pad/scripts/tio2_combi.py` | `measurements/wet_pad/figures/fig16_*`, `fig17_*` | Shared. |
| Extra panels (comparator / drift / frontier / coincidence / DEFF) | `data/olfaction/*.json`, `data/olfaction/*.npz` | `measurements/plotting/make_comparator*.py`, `make_drift*.py`, `make_frontier.py`, `make_coincidence_membrane.py`, `make_deff*.py`, `make_olfaction_scaling.py` | `measurements/plotting/figures/*.pdf` | Optional extra panels. |

## Commands verified to run

These were executed from the repository root during the release build (paths and
data resolve; outputs regenerated):

```bash
PY=/path/to/avlsi2024-sw/.venv-meas/bin/python3

# LNA transfer + noise + linearity
"$PY" measurements/lna/clean_2026-08-26/scripts/make_figures.py

# Wet-pad TiO2 panels
"$PY" measurements/wet_pad/scripts/tio2_combi.py

# Neuron FI insets
PYTHONPATH=. "$PY" measurements/array/scripts/plot_fi_insets_all16.py --style compact \
    --out measurements/array/figures/neuron_fi_reference.pdf

# Weight-code words (--out resolves next to the script)
PYTHONPATH=. "$PY" measurements/plotting/make_synapse_weight.py --panels b \
    --out weight_code_words.pdf

# Energy/decision table -> CSV
"$PY" measurements/plotting/constants.py
```

## [GAP]s and open decisions

1. **Combined `fig12_lna_gain_noise.pdf` — no dedicated script.** The two panels
   are produced separately; the combined figure is produced manually. Recommend
   writing
   `measurements/lna/clean_2026-08-26/scripts/make_fig12_gain_noise.py`.
2. **`docs/figures/lna_schematic.pdf` — no dedicated script.** The schematic is
   produced manually from the `design/xschem/` LNA cell.
3. **SOTA tables — hand-entered.** Compiled from literature into Markdown/CSV
   under `docs/`.
4. **Operating point.** Many results are operating-point and clock dependent.
   Where a row says `_25mhz` or a named bias file, reproduce that clock and bias
   file, not just "a" bias file. See `docs/HARDWARE_TRAPS.md`.
