# Plotting the paper results

This is the operation a user actually runs. Each row names a **paper result**
(figure/table id), the **data file(s)** it needs, the **plotting script** in this
repository, and the **output file** the script writes — so the plots can be
produced **without the paper source**.

**Nothing here needs a manuscript.** OSCAR ships no `.tex`, `.bib`, `.cls`,
`.sty`, or paper `.pdf`. The published articles are cited (see `CITATION.cff` /
`NOTICE`); figure/table ids below are labels from those articles.

Rows whose producer or data is genuinely missing are marked **[GAP]** rather
than invented. Non-data-driven floats are **[ASSET]** and ship as exported
images under `docs/figures/`.

## Environment

The bench/measurement virtual environment is not committed. Recreate it and run
every script with it (absolute path shown; adjust to your checkout):

```bash
PY=/path/to/avlsi2024-sw/.venv-meas/bin/python3
# plotting scripts expect the repo root as CWD and imports resolved via PYTHONPATH
cd /path/to/OSCAR
PYTHONPATH=. "$PY" <script>
```

Most scripts only need `numpy`, `matplotlib`, `scipy`, `pandas`, `scikit-learn`.

## Path rewrite (applied to the shipped scripts)

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
| `LNA/ISCAS27/IEEE_PAD_SkyWater_2026/figures/` | `measurements/lna/figures/` or `measurements/wet_pad/figures/` |
| `LNA/ISCAS27/IEEE_RISC-V/figures/` | `measurements/olfaction/figures/` |
| `paper/RISCV_NeuronArray_2026/data/` | `data/array/` |
| `paper/RISCV_NeuronArray_2026/figures/` | `measurements/array/figures/` |
| `paper/micro/figures/` | `measurements/paper_figures/` |

Two scripts defined their repo root by counting directory levels and needed the
depth corrected in addition to the fragment rewrite:
`measurements/paper_figures/make_synapse_weight.py` and
`measurements/olfaction/scripts/make_fig_olfaction_iscas.py`. The LNA
`make_paper_figures.py` now writes to `measurements/lna/figures/` and reads
`measurements/lna/data/`.

## ISCAS 2026 — "An Open-Silicon Neuromorphic Chemosensing Front-End with Electrode-Pad Wet Transduction"

| Paper result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| Fig. 1 architecture | — (design asset) | — (asset export) | `docs/figures/arch_overview.pdf` / `.png` | **[ASSET]** exported from the paper's system-overview float; no data. |
| **Fig. 2 hardware layout** | — (design assets) | — (one-time compose/export) | `docs/figures/fig_hardware_layout.{pdf,png}` | **[ASSET]** composed from `ISLPED2025-layout.png`, `skywater_2024_avlsi_chip_SNN_RISCV.jpg`, `19701130_045846_826317_daugther_chip.jpg`. Also the README figure. |
| Fig. 3 LNA schematic | `design/xschem/` (LNA cell) | — | `docs/figures/lna_schematic.pdf` | **[GAP]** the paper used TikZ; no clean xschem batch export is shipped. Export manually (xschem GUI → SVG/PDF) or request it. |
| Fig. 4 transfer, gain + noise (`fig12_lna_gain_noise.pdf`) | `measurements/lna/data/lna_transfer_final.csv`, `lna_transfer_ref.csv`, `lna_noise.csv` | `measurements/lna/clean_2026-08-26/scripts/make_paper_figures.py` | `measurements/lna/figures/fig12_lna_transfer.pdf` (gain) **and** `fig14_lna_noise.pdf` (noise) | Script emits the two panels separately. The combined two-panel `fig12_lna_gain_noise.pdf` is a manual overlay → **[GAP: no composer script]**; recommend `make_fig12_gain_noise.py`. A reference copy of the combined asset is shipped at `measurements/lna/figures/fig12_lna_gain_noise.pdf`. |
| Fig. 5 wet transduction | `measurements/wet_pad/data/scope_20260829_094236.csv`, `scope_20260829_103015.csv` | `measurements/wet_pad/scripts/tio2_combi_ISCAS.py` | `measurements/wet_pad/figures/fig16_tio2_wetting_paper.pdf`, `fig17_tio2_dilute3x_paper.pdf` | Shadows: `tio2_three_panel.py`, `tio2_dilute3x_panel.py`, `tio2_injection_recovery.py`, `make_fig_saline_chain.py`. |
| Fig. 6 pad-evoked spiking | `measurements/wet_pad/data/scope_20260831_123139_single_payed_back_chip1_v1.csv` | `measurements/wet_pad/scripts/make_fig_pad_evoked.py` | `measurements/wet_pad/figures/fig18_pad_evoked_chip1.pdf` | |
| Table I SOTA | — | — | `docs/` Markdown/CSV (hand-entered) | Compiled from literature; not LaTeX. |

## ISCAS 2027 — "A RISC-V-Managed Analog Spiking Neural Network Array for On-Sensor Olfactory Processing"

| Paper result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| Fig. 1 domain map | — (design asset) | — (asset export) | `docs/figures/domain_map.{pdf,png}` | **[ASSET]** composed from the layout + die micrograph. |
| Fig. 2a weight code | `data/synapse/onset_n5.json`, `onset_n5_ladder.json` | `measurements/paper_figures/make_synapse_weight.py --panels b --out …` | `measurements/paper_figures/weight_code_words.pdf` | Default invocation emits the two-panel `weight_code.pdf`; `--panels b` emits the published all-words panel. Inputs produced by `measurements/array/scripts/synapse_onset.py`. |
| Fig. 2b neuron FI | `data/array/neuron_fi_allneurons.csv`, `data/array/scope_{14,17,20}_neu14_if.csv` | `measurements/array/scripts/plot_fi_insets_all16.py --style iscas --out …` | `measurements/array/figures/neuron_fi_iscas.pdf` | Default output is `neuron_fi_all16_insets.pdf`; `--style iscas` is the paper figure. The three scope CSVs are required. |
| Fig. 3 pipeline row | `data/olfaction/olf_validate/*.npz` (one held-out chunk) | `measurements/olfaction/scripts/make_fig_pipeline1row.py` | `measurements/olfaction/figures/fig_pipeline_row.pdf` | Cross-imports `olfaction_bias_bo.py` and `make_fig_odorclass.py` (same `scripts/` dir; the script adds its dir to `sys.path`). |
| Table II command set | `firmware/neuron_handshake/neuron_handshake.c` | — (derived) | `firmware/README.md` (Markdown table) | Derived from opcodes; printed, not LaTeX. |
| Table III odor capacity | `data/olfaction/olfaction_class_curve.json` ← `data/olfaction/olf_validate/*.npz` (9 acquisitions) | `measurements/olfaction/scripts/olfaction_class_curve.py`; figure `make_fig_olfaction_iscas.py` | `measurements/olfaction/figures/olfaction_capacity.pdf` + CSV/JSON | `make_fig_olfaction_iscas.py` re-verifies against the JSON and caches `data/olfaction/olfaction_iscas_k3.json`. |
| Table IV energy/decision | `data/olfaction/olfaction_hybrid_score.json`, `olfaction_hybrid_slot.json`, `olfaction_mismatch_payoff.json` | `measurements/paper_figures/constants.py` | `measurements/paper_figures/energy_table.csv` | **Changed from R2:** `constants.py` now emits **CSV** (and prints the values); it no longer writes `generated_constants.tex`. |
| Table V SOTA | — | — | `docs/` Markdown/CSV (hand-entered) | Compiled from literature. |

## TBioCAS journal companion (source not in repo; shared result panels)

The journal's source and PDF are **not shipped**; these rows share the same
scripts/data as above, so the panels can be regenerated if wanted.

| Paper result | Data file(s) | Plotting script | Output file | Notes |
|---|---|---|---|---|
| LNA transfer | `measurements/lna/data/lna_transfer_final.csv`, `lna_transfer_ref.csv` | `measurements/lna/clean_2026-08-26/scripts/make_paper_figures.py` | `measurements/lna/figures/fig12_lna_transfer.pdf` | High-gain point `V_iref = 1.08 V`. |
| LNA linearity | `measurements/lna/data/lna_gain_vs_level_ALL.csv` | `measurements/lna/clean_2026-08-26/scripts/make_paper_figures.py` (or `run_gain_vs_level.py`) | `measurements/lna/figures/gain_vs_level_highgain.pdf` | |
| LNA noise | `measurements/lna/data/lna_noise.csv` | `measurements/lna/clean_2026-08-26/scripts/make_paper_figures.py` | `measurements/lna/figures/fig14_lna_noise.pdf` | |
| Array characterization | `data/synapse/`, `data/array/` | `measurements/paper_figures/make_synapse_weight.py`, `measurements/array/scripts/plot_fi_insets_all16.py` | as ISCAS 2027 Fig. 2a/2b | Shared. |
| Odor pipeline | `data/olfaction/olf_validate/*.npz` | `measurements/olfaction/scripts/make_fig_pipeline1row.py` | `measurements/olfaction/figures/fig_pipeline_row.pdf` | Shared. |
| Odor capacity | `data/olfaction/olfaction_class_curve.json`, `olfaction_class_curve_emul.json` | `measurements/paper_figures/make_olfaction_capacity.py` | `measurements/paper_figures/figures/olfaction_capacity.pdf` | Analog + emulated on RISC-V. |
| Energy by substrate | `data/olfaction/olfaction_hybrid_score.json`, `olfaction_hybrid_slot.json` | `measurements/paper_figures/constants.py`, `make_olfaction.py` | `measurements/paper_figures/energy_table.csv` | Shared. |
| Wet transduction / saline | `measurements/wet_pad/data/scope_20260829_*.csv` | `measurements/wet_pad/scripts/tio2_combi_ISCAS.py` | `measurements/wet_pad/figures/fig16_*`, `fig17_*` | Shared. |
| MICPRO-only set (comparator / drift / frontier / coincidence / DEFF panels) | `data/olfaction/*.json`, `data/olfaction/*.npz` | `measurements/paper_figures/make_comparator*.py`, `make_drift*.py`, `make_frontier.py`, `make_coincidence_membrane.py`, `make_deff*.py`, `make_olfaction_scaling.py` | `measurements/paper_figures/figures/*.pdf` | Optional extra panels; their source manuscript is not shipped. |

## Commands verified to run

These were executed from the repository root during the release build (paths and
data resolve; outputs regenerated):

```bash
PY=/path/to/avlsi2024-sw/.venv-meas/bin/python3

# LNA transfer + noise + linearity (ISCAS 2026 Fig. 4; TBioCAS)
"$PY" measurements/lna/clean_2026-08-26/scripts/make_paper_figures.py

# Wet-pad TiO2 panels (ISCAS 2026 Fig. 5)
"$PY" measurements/wet_pad/scripts/tio2_combi_ISCAS.py

# Neuron FI insets (ISCAS 2027 Fig. 2b)
PYTHONPATH=. "$PY" measurements/array/scripts/plot_fi_insets_all16.py --style iscas \
    --out measurements/array/figures/neuron_fi_iscas.pdf

# Weight-code words (ISCAS 2027 Fig. 2a)
PYTHONPATH=. "$PY" measurements/paper_figures/make_synapse_weight.py --panels b \
    --out measurements/paper_figures/weight_code_words.pdf

# Energy/decision table (ISCAS 2027 Table IV) -> CSV
"$PY" measurements/paper_figures/constants.py
```

## [GAP]s and open decisions

1. **Combined `fig12_lna_gain_noise.pdf` — no composer.** The two panels are
   produced separately; the combined figure was assembled in the manuscript
   build. Recommend writing
   `measurements/lna/clean_2026-08-26/scripts/make_fig12_gain_noise.py`.
2. **`docs/figures/lna_schematic.pdf` — not exported.** The paper's schematic
   was TikZ; export the `design/xschem/` LNA cell manually if needed.
3. **Table I / Table V — hand-entered.** Compiled from literature into
   Markdown/CSV under `docs/`; no data-driven producer exists.
4. **Operating point.** Many results are operating-point and clock dependent.
   Where a row says `_25mhz` or a named bias file, reproduce that clock and bias
   file, not just "a" bias file. See `docs/HARDWARE_TRAPS.md`.
5. **Excluded companion datasets.** The XOR / T-XOR / NARMA and ECG
   acquisitions are not shipped in this release (not part of the two cited
   papers). Their scripts remain under `measurements/reservoir/` and
   `measurements/analysis/`, and will point at `data/…` paths that are absent —
   supply your own acquisition to use them.
