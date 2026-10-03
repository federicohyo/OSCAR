# Archived figure inputs

`olfaction_hybrid_transfer_calsession.json` is the transfer matrix of the **calibration
session** the comparator figure documents (ladder `[6, 8, 12, 16, 24, 32]` switching at
`[6, 8, 11, 18, 21, 29]`), taken from commit `287f0b7`.

`results/olfaction_hybrid_transfer.json` in the working tree is a **later, re-measured**
matrix (commit `4154299`) taken after the thresholds had drifted, so regenerating the
figure against it silently changes the published ladder. Pass this file explicitly:

    ./.venv-meas/bin/python3 paper/micro/figures/make_comparator.py \
        --panels ac --out comparator_cal_ac \
        --transfer paper/micro/figures/data/olfaction_hybrid_transfer_calsession.json

Verified: `--panels abc` against this file reproduces the committed `comparator_cal.pdf`
byte-for-byte.
