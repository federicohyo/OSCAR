# measurements

Bench campaigns, their generating scripts, and the figure plotting code.
This directory separates *how the data was taken and plotted* from the
archived datasets in `../data/`.

| Directory | Contents |
|---|---|
| `lna/` | LNA front-end measurements: `scripts/` (flat LNA scripts: freq sweep, noise, figures, tio2 shadow variants), `data/` (LNA CSVs/JSON), `figures/`, and the archived self-contained campaign `clean_2026-08-26/` (`raw/ derived/ figures/ setup/ debug/ scripts/`). |
| `wet_pad/` | TiO₂ wetting, saline and pad-evoked panels: `scripts/` (`tio2_combi.py`, `make_fig_pad_evoked.py`, `make_fig_saline_chain.py`, `tio2_*_panel.py`), `data/` (scope CSVs), `figures/`. |
| `array/` | Synapse / neuron calibration and coincidence: `scripts/` (`neuron_fi.py`, `neuron_fi_poisson.py`, `plot_fi_insets*.py`, `synapse_*.py`, `coincidence_*.py`, `epsp_measure.py`), `figures/`. |
| `olfaction/` | Electronic-nose pipeline: `scripts/` (`olfaction_*.py`, `make_fig_odorclass.py`, `make_fig_olfaction.py`, `make_fig_pipeline1row.py`, `olfaction_bias_bo.py`, `odor_*.py`), `figures/`. Note: `make_fig_pipeline1row.py` cross-imports `olfaction_bias_bo.py` and `make_fig_odorclass.py` from the same directory. |
| `reservoir/` | On-chip reservoir tasks: `scripts/` (`reservoir_*.py`, `txor_*.py`, `narma_*.py`, `make_beatset.py`, `repeatability*.py`, `esn_*.py`, `shd_*.py`), `figures/`. |
| `plotting/` | Independent composers: `make_synapse_weight.py`, `make_olfaction*.py`, `make_deff*.py`, `make_comparator*.py`, `make_frontier.py`, `make_coincidence_membrane.py`, `make_drift*.py`, `constants.py`, and `figures/`. |
| `analysis/` | Cross-cutting scoring shared by the reservoir rows: `reservoir_a2.py`, `reservoir_kernel.py`, `reservoir_data.py`, `deff_*.py`, `score_multibias.py`, `sweep_kernel_grid.py`, … |

See `../docs/PLOTTING.md` for the result → data → script → output map and
the path-rewrite that was applied. Plotting scripts expect the **repository
root** as the current working directory; cross-directory imports are documented
in `PLOTTING.md`.
