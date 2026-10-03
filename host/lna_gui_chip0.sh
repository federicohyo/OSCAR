#!/usr/bin/env bash
# Launch the GUI for chip0 -- the chip whose on-die flash passthrough is
# dead (2026-08-30). Its flash is frozen with the pinned 25 MHz odor image
# (LNA/firmware/neuron_handshake_25MHz_odor_20260825.hex), so the chip must
# ALWAYS be talked to at 25 MHz. neuron_bridge.py defaults to 50 MHz; a
# bare GUI launch gives the documented silent comms failure on this chip.
#
# chip0 cannot be reflashed over USB anymore. Reflash path: Raspberry Pi
# hyo@192.168.1.48:/home/hyo/firmware-write/flash.sh via the J15 header
# (daughterboard removed from J24).
set -e
cd "$(dirname "$0")"
export CARAVAN_CLK_MHZ=25
if [ ! -x ofxCaravanViewer/bin/ofxCaravanViewer ]; then
    echo "GUI not built yet: (cd ofxCaravanViewer && make -j\$(nproc))" >&2
    exit 1
fi
echo "chip0 GUI: CARAVAN_CLK_MHZ=25 (pinned 25 MHz image in flash)"
exec ofxCaravanViewer/bin/ofxCaravanViewer "$@"
