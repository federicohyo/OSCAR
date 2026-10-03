#!/usr/bin/env bash
# Bring the chip up at 50 MHz after a power cycle.
#
# Physical reality: the chip ALWAYS powers up on the 10 MHz crystal (the DLL is a
# volatile register and does not survive a power cycle). Flash IS non-volatile, so the
# 50 MHz firmware image persists across power cycles -- only the DLL has to be re-engaged.
#
#   ./bringup_50.sh          fast: engage the DLL to 50 MHz (firmware already in flash)
#   ./bringup_50.sh flash    full: re-flash the 50 MHz image on the crystal, then engage
#
# Note: neuron_bridge.py / the GUI / bench scripts also auto-engage the DLL on startup
# (CARAVAN_CLK_MHZ default is 50), so for normal use you can just start them -- this
# script is the explicit helper. Biases are NOT programmed here (bench scripts load
# per-neuron biases; run_neuron_test's generic DAC path hits the VREF trap).
set -e
cd "$(dirname "$0")"
PY=./.venv-meas/bin/python3
if [ "$1" = "flash" ]; then
    echo ">> Full bring-up: flash 50 MHz firmware on the crystal, then engage the DLL"
    "$PY" run_neuron_test.py --clock 50 --skip-dac
else
    echo ">> Fast bring-up: engage the DLL to 50 MHz (firmware persists in flash)"
    "$PY" run_neuron_test.py --clock 50 --skip-flash --skip-dac
fi
echo ">> Chip at 50 MHz. (A power cycle drops it back to the 10 MHz crystal -- rerun this.)"
