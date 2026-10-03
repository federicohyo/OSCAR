#!/usr/bin/env bash
# Flash the firmware binary built for a given core clock, engage that clock, and
# launch the GUI matched to it -- so you can test the synapse at each speed by eye.
#
#   ./test_at_clock.sh 25          # flash 25 MHz image, GUI at 25 MHz
#   ./test_at_clock.sh 10          # crystal (10 MHz)  -- inhibition known-good here
#   ./test_at_clock.sh 25 noflash  # skip flashing (image already loaded), just GUI
#
# Reachable clocks: 10 (crystal), 20, 25, 33, 50 MHz.
# NOTE: 50 MHz (and, per today's inconclusive test, possibly 25/33) delivers reduced
# synaptic charge -- that's exactly what this lets you check.
set -e
cd "$(dirname "$0")"
REPO="$(pwd)"
PY="$REPO/.venv-meas/bin/python3"
MHZ="${1:-}"
MODE="${2:-flash}"
BIN="$REPO/firmware/neuron_handshake/binaries/neuron_handshake_${MHZ}MHz.hex"
GUI="$REPO/ofxCaravanViewer/bin/ofxCaravanViewer"

case "$MHZ" in
  10|20|25|33|50) ;;
  *) echo "usage: $0 <10|20|25|33|50> [noflash]"; exit 1 ;;
esac
if [ ! -f "$BIN" ]; then echo "missing binary: $BIN (run 'make hex F_CPU_MHZ=$MHZ' in firmware/neuron_handshake)"; exit 1; fi

# free the FTDI (one process owns it at a time)
pkill -f neuron_bridge.py 2>/dev/null || true
pkill -f inh_scope.py 2>/dev/null || true
sleep 1

if [ "$MODE" != "noflash" ]; then
  echo ">> forcing crystal before flash (flash SCK scales with the core clock)"
  "$PY" -c "import run_neuron_test as r; r.set_core_clock(10)" >/dev/null 2>&1
  echo ">> flashing ${MHZ} MHz image"
  cp "$BIN" "$REPO/firmware/neuron_handshake/neuron_handshake.hex"
  # --clock 10 keeps the chip on the crystal after flashing; the GUI engages the
  # real clock itself, so the DLL is engaged exactly once (by the GUI's bridge).
  "$PY" run_neuron_test.py --clock 10 --skip-dac 2>&1 | grep -iE "flash|done|error|MHz" | tail -6
fi

echo ">> launching GUI at ${MHZ} MHz (CARAVAN_CLK_MHZ=${MHZ}); its bridge engages the DLL + sets baud"
cd "$REPO/ofxCaravanViewer"
exec env CARAVAN_CLK_MHZ="$MHZ" "$GUI"
