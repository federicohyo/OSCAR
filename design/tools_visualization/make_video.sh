#!/usr/bin/env bash
# End-to-end: magic layout -> GDS -> layer JSON -> 3D frames -> mp4.
#
# Frames are piped, kept off disk.
#
#   ./tools_visualization/make_video.sh                    # default soma + synapse loop
#   SECONDS_LOOP=25 ./tools_visualization/make_video.sh     # longer loop
#   SPIN=1 DIM=0.6 ./tools_visualization/make_video.sh      # full orbit, dimmed for background
#
# Run it from anywhere; paths are resolved from the repo root.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
MAGDIR="$ROOT/mag"

: "${PDK_ROOT:=/storage/pdks}"
: "${PDK:=sky130A}"
export PDK_ROOT PDK

VIZ_CELLS="${VIZ_CELLS:-neuron_analog_fc_v2 dpi_syn_exc_4bit_fc_v2}"
BUILD="${BUILD:-$HERE/build}"
FPS="${FPS:-30}"
SECONDS_LOOP="${SECONDS_LOOP:-60}"
NFRAMES=$(( FPS * SECONDS_LOOP ))
# RUNGS="tap poly licon1 ..." renders one loop per rung: the same flight over
# and over, with one more slice of the stack standing each time, so the chip
# builds itself from the wells up. Each name is the topmost layer left at the
# end of that loop, so "met1" after "li1" brings mcon and met1 on together.
# SECONDS_LOOP is then the length of ONE loop, while the video spans all rungs.
RUNG_LIST=()
if [ -n "${RUNGS:-}" ]; then
    read -ra RUNG_LIST <<< "$RUNGS"
    LOOP_FRAMES=$(( FPS * SECONDS_LOOP ))
    NFRAMES=$(( LOOP_FRAMES * ${#RUNG_LIST[@]} ))
fi
JOBS="${JOBS:-$(( $(nproc) < 8 ? $(nproc) : 8 ))}"
W="${W:-960}"
H="${H:-1080}"
OUT="${OUT:-$BUILD/soma_synapse.mp4}"

mkdir -p "$BUILD"

echo "==> 1/3  magic: exporting GDS for: $VIZ_CELLS"
( cd "$MAGDIR" && VIZ_CELLS="$VIZ_CELLS" VIZ_OUT="$BUILD" \
    magic -dnull -noconsole "$HERE/export_gds.tcl" 2>&1 | grep -E "WROTE|SKIP" )

echo "==> 2/3  klayout: dumping layer geometry"
for c in $VIZ_CELLS; do
    VIZ_CELL="$c" VIZ_OUT="$BUILD" klayout -b -r "$HERE/dump_layers.rb" 2>&1 | grep WROTE
done

echo "==> 3/3  rendering $NFRAMES frames at ${W}x${H} -> $OUT"
EXTRA=()
[ "${SPIN:-0}" = "1" ] && EXTRA+=(--spin)
[ -n "${DIM:-}" ] && EXTRA+=(--dim "$DIM")
[ -n "${ZEX:-}" ] && EXTRA+=(--zex "$ZEX")
[ -n "${AZ_AMP:-}" ] && EXTRA+=(--az-amp "$AZ_AMP")
[ -n "${EL_AMP:-}" ] && EXTRA+=(--el-amp "$EL_AMP")
[ -n "${SCALE_UM:-}" ] && EXTRA+=(--scale-um "$SCALE_UM")
[ -n "${PEEL:-}" ] && EXTRA+=(--peel "$PEEL")
# PEEL_KEYS="t:p;t:p;..." drives the peel as a curve, so it can come back down
# and the flythrough can return to its opening frame.
# ROCK_KEYS="t:az:el;..." varies the rock; zero amplitudes hold the angle
# still, which is what a straight left-to-right pan wants.
if [ -n "${ROCK_KEYS:-}" ]; then
    IFS=';' read -ra _RS <<< "$ROCK_KEYS"
    for _r in "${_RS[@]}"; do EXTRA+=(--rock-key "$_r"); done
fi
if [ -n "${PEEL_KEYS:-}" ]; then
    IFS=';' read -ra _KS <<< "$PEEL_KEYS"
    for _k in "${_KS[@]}"; do EXTRA+=(--peel-key "$_k"); done
fi
# VIZ_CELLS only drives the magic/klayout export; the renderer keeps its own
# panel defaults. Set PANELS="CELL:LABEL:ZOOM;CELL:LABEL:ZOOM" whenever you
# change VIZ_CELLS, or the video will show the default cells instead.
if [ -n "${PANELS:-}" ]; then
    IFS=';' read -ra _PS <<< "$PANELS"
    for _p in "${_PS[@]}"; do EXTRA+=(--panel "$_p"); done
fi
# WAYPOINTS="t:cx:cy:span;t:cx:cy:span;..." flies the camera instead of holding
# the cell centred. Such a path is one-way, so the result serves one-shot flights.
if [ -n "${WAYPOINTS:-}" ]; then
    IFS=';' read -ra _WPS <<< "$WAYPOINTS"
    for _w in "${_WPS[@]}"; do EXTRA+=(--waypoint "$_w"); done
fi
if [ ${#RUNG_LIST[@]} -gt 0 ]; then
    for _g in "${RUNG_LIST[@]}"; do EXTRA+=(--rung "$_g"); done
    EXTRA+=(--loop-frames "$LOOP_FRAMES")
    [ -n "${RUNG_FADE:-}" ] && EXTRA+=(--rung-fade "$RUNG_FADE")
fi
[ -n "${NODE_NOTE+x}" ] && EXTRA+=(--node-note "$NODE_NOTE")
# Frames stream straight into ffmpeg as raw RGBA instead of landing as ~900
# PNGs (~400 MB) that ffmpeg would read back again. rawvideo streams headerless
# frames, so ffmpeg is told the frame size here and render_stack.py aborts on
# frame 0 if its canvas disagrees.
#
# Rendering is single-threaded per process, so the loop is cut into contiguous
# chunks that workers take from a queue. Slices must be contiguous: each part
# is a time range, and the camera angle still derives from the frame number,
# so the joined video stays seamless.
#
# There are deliberately more chunks than workers. Frames are nowhere near
# equal cost -- in a rung render the first loop draws a few thousand quads and
# the last draws 1.4 M, about 100:1 -- so one chunk per worker leaves the
# unlucky worker running for hours alone. Small chunks handed out as workers
# free up even that out.
render_one () {          # $1 = first frame, $2 = how many, $3 = output file
    python3 "$HERE/render_stack.py" "$BUILD" - "$NFRAMES" \
        --frame-start "$1" --frame-count "$2" \
        --width "$W" --height "$H" "${EXTRA[@]}" \
      | ffmpeg -y -loglevel error \
          -f rawvideo -pix_fmt rgba -s "${W}x${H}" -framerate "$FPS" -i - \
          -c:v libx264 -pix_fmt yuv420p -crf 18 "$3"
}

run_chunk () {           # $1 = first frame, $2 = how many, $3 = part, $4 = index
    if render_one "$1" "$2" "$3" 2>"$BUILD/chunk_$4.log"; then
        echo "    chunk $4 done: $2 frames from $1"
    else
        touch "$BUILD/FAILED"
        echo "    chunk $4 FAILED, see $BUILD/chunk_$4.log" >&2
    fi
}

if [ "$JOBS" -le 1 ]; then
    render_one 0 "$NFRAMES" "$OUT"
else
    CHUNKS="${CHUNKS:-$(( JOBS * 6 ))}"
    [ "$CHUNKS" -gt "$NFRAMES" ] && CHUNKS="$NFRAMES"
    # Each worker briefly holds the parsed JSON on top of its numpy arrays, so
    # a whole wave starting at once is the high-water mark for memory. Spacing
    # the first wave out keeps a big cell on many workers off the ceiling;
    # after that the queue staggers itself.
    STAGGER="${STAGGER:-4}"
    echo "    $JOBS workers over $CHUNKS chunks of ~$(( NFRAMES / CHUNKS )) frames"
    echo "    per-frame progress: tail -f $BUILD/chunk_0.log"
    rm -f "$BUILD/FAILED"
    PARTS=(); START=0; RUNNING=0
    for k in $(seq 0 $((CHUNKS - 1))); do
        CNT=$(( NFRAMES / CHUNKS + (k < NFRAMES % CHUNKS ? 1 : 0) ))
        [ "$CNT" -eq 0 ] && continue
        PART="$BUILD/part_$(printf %04d "$k").mp4"
        run_chunk "$START" "$CNT" "$PART" "$k" &
        PARTS+=("$PART"); START=$((START + CNT)); RUNNING=$((RUNNING + 1))
        [ "$k" -lt "$JOBS" ] && sleep "$STAGGER"
        if [ "$RUNNING" -ge "$JOBS" ]; then
            wait -n || true
            RUNNING=$((RUNNING - 1))
        fi
    done
    wait
    if [ -f "$BUILD/FAILED" ]; then
        echo "a render worker failed; see $BUILD/chunk_*.log" >&2
        exit 1
    fi
    LIST="$BUILD/parts.txt"; : > "$LIST"
    for pp in "${PARTS[@]}"; do echo "file '$pp'" >> "$LIST"; done
    ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" \
        -c copy -movflags +faststart "$OUT"
    rm -f "${PARTS[@]}" "$LIST" "$BUILD"/chunk_*.log
fi

echo
echo "done: $OUT"
ls -lh "$OUT"
