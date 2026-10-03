# data

Archived result datasets — the inputs the plotting scripts in
`../measurements/` read. The shipped results cover LNA, wet-pad, array
characterisation, synaptic calibration, olfaction classification, and the
curated bias operating points.

| Directory | Contents |
|---|---|
| `olfaction/` | Olfaction classification: `olf_validate/*.npz` (nine held-out acquisitions), `olfaction_class_curve.json` / `_emul.json`, `olfaction_k3.json`, the hybrid score/slot/payoff JSONs, comparator JSONs. |
| `synapse/` | Synaptic calibration: `onset_n5*.json` / `.csv` (weight-code ladder) and the rate-transfer CSVs. |
| `array/` | Array characterisation: `neuron_fi_allneurons.csv` (16-neuron FI sweep) and `scope_{14,17,20}_neu14_if.csv` (neuron-14 membrane traces used as FI insets). |
| `biases/` | Curated `*.biases` operating points referenced by the plotting table (25 MHz reference points, synapse-characterisation patterns, comparator levels, LNA biases). |

## Not shipped (deliberately)

The autonomous-exploration datasets — `xor_dim` (dimensionality → XOR), `txor`
(recurrence → temporal-XOR), `narma` (cross-coupled reservoir, in progress),
and the ECG reservoir sessions — are excluded from this release. The scripts
that produced/consumed them remain in `../measurements/reservoir/` and
`../measurements/analysis/`; supply your own acquisition if you want to rerun
those experiments.

Third-party raw data (the metal-oxide odor dataset) is not redistributed beyond
the derived result files here.

See `../docs/PLOTTING.md` for which figure reads which file.
