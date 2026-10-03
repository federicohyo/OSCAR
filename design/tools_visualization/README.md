# tools_visualization

Turns the cells in `mag/` into a 3D movie of the silicon: every layer extruded
to its real height in the sky130 stack, in the PDK's own colours, orbiting.
Built for the `ofxLPM-1959` installation, where it plays behind the spikes
coming off the die. Copied here from the `avlsi-skywater130` teaching repo so it
can run against the real tapeout cells.

## Run it

```bash
./tools_visualization/make_video.sh
```

That produces `tools_visualization/build/soma_synapse.mp4` — a 60 s seamless
loop at 960x1080, which is the left half of a 1080p window (`splitFraction`
is 0.5 in the app).

The camera rocks through one full period per loop, so **`SECONDS_LOOP` sets the
speed as well as the length**: a longer loop is a slower rock, same motion.

Useful variables:

| variable       | default                            | what it does                          |
|----------------|------------------------------------|---------------------------------------|
| `VIZ_CELLS`    | `neuron_analog_fc_v2 dpi_syn_exc_4bit_fc_v2` | which cells from `mag/` to render |
| `SECONDS_LOOP` | `60`                               | loop length, and therefore rock speed  |
| `AZ_AMP`       | `45`                               | rock amplitude in degrees              |
| `EL_AMP`       | `8`                                | vertical drift in degrees              |
| `FPS`          | `30`                               | frame rate                             |
| `W` / `H`      | `960` / `1080`                     | output size                            |
| `SPIN=1`       | off                                | full 360 orbit instead of a slow rock  |
| `DIM`          | `1.0`                              | global alpha; `0.6` for a backdrop     |
| `ZEX`          | `22`                               | vertical exaggeration                  |
| `JOBS`         | `min(nproc, 8)`                    | parallel render workers; `1` disables  |
| `CHUNKS`       | `JOBS * 6`                         | pieces the render is cut into, queued  |
| `STAGGER`      | `4`                                | seconds between the first wave's starts|
| `RUNGS`        | off                                | `layer layer ...` — one loop per rung  |
| `RUNG_FADE`    | `0.12`                             | how much of a loop the new rung fades in|
| `PANELS`       | renderer's own defaults            | `CELL:LABEL:ZOOM;...` — set with `VIZ_CELLS` |
| `WAYPOINTS`    | off                                | `T:CX:CY:SPAN[:ELEV];...` camera path  |
| `PEEL`         | off                                | `T0:T1:N` fade the top N layers away   |
| `PEEL_KEYS`    | off                                | `T:P;...` peel as a curve, can reverse |
| `SCALE_UM`     | `5`                                | scale-bar length in um; `0` hides it   |
| `NODE_NOTE`    | `sky130 · 130 nm process`          | bottom-left caption; `""` hides it      |
| `OUT`          | `build/soma_synapse.mp4`           | output path                            |

Render cost is ~0.12 s/frame per worker for the default cells at 960x1080, so
the 60 s loop takes about a minute across the default 8 workers.
Cost scales with polygon count, not with cell area.

## What this can and cannot render

Cost scales with **polygon count**, not cell area, and matplotlib is the limit.
Measured on this repo's cells at 960x1080:

Per-frame times are one worker; the 60 s column assumes the default 8.

| cell                                 | quads     | size (um)  | s/frame | 60 s loop |
|--------------------------------------|-----------|------------|---------|-----------|
| `neuron_analog_fc_v2`                | 669       | 12 x 14    | 0.06    | ~1 min    |
| `dpi_syn_exc_4bit_fc_v2`             | 930       | 19 x 14    | 0.08    | ~1 min    |
| `neuron_32syn_v1`                    | 104,650   | 630 x 25   | ~2.3    | ~10 min   |
| `neuro_synaptic_core_16neu_32syn_v3` | 1,556,679 | 649 x 328  | ~34     | ~2.2 h    |
| `neuron_synapse_array_..._v2`        | 1,592,529 | 692 x 329  | ~34     | ~2.2 h    |

So: single devices are near-instant, `neuron_32syn_v1` is a coffee break, and
the big arrays are a long lunch rather than the multi-day job they used to be.
Each worker holds its own copy of the geometry (~4 GB for the 1.6 M-quad
cells), so on a 64 GB machine keep `JOBS` at or below about 12 for those.
**`Niet_Top` (9 M lines) is still out of scope** — do not point this at it. A whole-chip view needs a rasterising
renderer, not a per-polygon one; KLayout's own image export is the right tool
for that.

## Building the chip layer by layer

`RUNGS` renders the same flight several times over, with one more slice of the
stack standing each time, so the chip builds itself from the wells up. Each
name is the topmost layer left at the end of that loop:

```bash
JOBS=24 FPS=30 SECONDS_LOOP=16 AZ_AMP=25 \
VIZ_CELLS="neuron_synapse_array_with_input_output_logic_v2" \
PANELS="neuron_synapse_array_with_input_output_logic_v2:16 NEURONS x 32 SYNAPSES  ·  sky130:1.0" \
RUNGS="li1 met1 met2 met3 met4" \
SCALE_UM=100 ./tools_visualization/make_video.sh
```

**`SECONDS_LOOP` is one loop, not the whole video** — five rungs at 24 s is a
two-minute film. A caption under the panel label names what each loop puts on.

Five rungs is the version built for the installation: the first loop brings the
whole device level up at once (wells, diff, tap, poly, licon1, li1) because the
layers below the metals are not worth a loop each at array scale, and then one
metal comes on per loop. Split them out again — `RUNGS="tap poly licon1 li1
met1 met2 met3 met4"` — to watch the transistors themselves being made.

Naming a metal without its via brings both on together (`met1` after `li1`
adds mcon and met1), because the peel only ever takes whole layers off the top.
That is usually what you want: a via layer alone is a field of small posts.

The fade is a smoothstep, and slow-in is the point. Dense geometry stacks many
translucent faces, so a linear fade reads as finished about a quarter of the
way through; easing in makes the layer look like it lands rather than blinks.

Cost follows the rungs you pick, not the layer count: a loop spends its frames
at its own rung's state, so the total is `frames-per-loop x (sum of the
per-frame cost at each rung)`. Measured on the array at 960x1080, a frame costs
0.4 s at bare nwell and 43.7 s at full stack; the five rungs above add up to
196 s, the eight-rung split is 243 s, and all fourteen layers would be 422 s.
Merging cheap rungs away barely helps — it is the loops carrying full metal
that cost.

Five rungs:

| per loop | video | CPU-hours | on 24 workers |
|----------|-------|-----------|---------------|
| 16 s     | 1:20  | 26        | ~1.1 h        |
| 24 s     | 2:00  | 39        | ~1.6 h        |
| 30 s     | 2:30  | 49        | ~2.0 h        |

Add ~90 s per chunk for re-reading the JSON and rebuilding the geometry: at the
default `CHUNKS` that is about 11% on top, worth trading for a full queue. Lower
`CHUNKS` if a cell is slow to build and the frames are cheap.

## Flying the camera

By default the camera holds the cell centred and rocks. `WAYPOINTS` replaces
that with a path: each point is `T:CX:CY:SPAN[:ELEV]` — loop fraction, centre
in microns, half-width in microns, and an optional elevation. Centres and
elevation interpolate linearly, **span geometrically**, both eased with a
smoothstep, because a zoom that is linear in span spends nearly all its time
already close in.

Two things stop a deep zoom from turning to mush:

- **`PEEL`.** Diving into a large array without it buries the camera in upper
  metal — you end up inside a solid wall of met1. `PEEL="T0:T1:N"` fades the
  top `N` layers away across that window, topmost first, each with its own
  slice of it, so the stack comes off a layer at a time. `N=10` leaves li1,
  poly, diff, tap and nwell: recognisably the same device level the standalone
  cells render at.
- **Elevation in the waypoint.** The low angle that flatters a whole array is
  exactly the one that looks into the side of the stack up close. Ramping to
  ~55 degrees on the way in reads like a layout view.

The scale bar follows: it re-measures the projection every frame and relabels
itself from a round ladder, so it steps 100 -> 50 -> 20 -> 10 um on the way
down instead of staying wrong at its calibrated value.

A worked example — 3 s, hold on the full array then dive to one neuron:

```bash
JOBS=8 FPS=30 SECONDS_LOOP=3 \
VIZ_CELLS="neuron_synapse_array_with_input_output_logic_v2" \
PANELS="neuron_synapse_array_with_input_output_logic_v2:SOMA:1.0" \
WAYPOINTS="0:345.9:164.6:383:20;0.1667:345.9:164.6:383:20;1:619:159:15:55" \
PEEL="0.25:0.80:10" SCALE_UM=100 \
./tools_visualization/make_video.sh
```

### Making a path loop

A path loops when it is **periodic**, not when its last frame is a copy of its
first — duplicating a frame just adds a stutter. Give the path the same centre,
span and elevation at `T=0` and `T=1`, bring `PEEL_KEYS` back to its opening
value, and the azimuth rock takes care of itself since it runs one full sine
period. Frame `N-1` then sits one step before frame 0 and the wrap is invisible.

`PEEL_KEYS="T:P;..."` is the peel as a curve — `P` top layers removed at
fraction `T` — which is what lets it run backwards and reassemble the stack.
The older one-shot `PEEL` never comes back, so it cannot loop.

A worked 24 s loop: open on the array, dive to a neuron, retreat, sweep one row
left to right, and pull back to the opening frame.

```bash
JOBS=8 FPS=30 SECONDS_LOOP=24 AZ_AMP=25 \
VIZ_CELLS="neuron_synapse_array_with_input_output_logic_v2" \
PANELS="neuron_synapse_array_with_input_output_logic_v2:16 NEURONS x 32 SYNAPSES:1.0" \
WAYPOINTS="0:345.9:164.6:383:20;0.06:345.9:164.6:383:20;0.30:619:159:15:55;\
0.37:619:159:15:55;0.45:345.9:164.6:383:30;0.52:80:159:45:40;\
0.76:600:159:45:40;0.90:345.9:164.6:383:20;1:345.9:164.6:383:20" \
PEEL_KEYS="0:0;0.08:0;0.28:10;0.86:10;0.98:0;1:0" \
SCALE_UM=100 ./tools_visualization/make_video.sh
```

Check a loop by comparing the last-to-first frame difference against a normal
adjacent-frame difference; a clean seam is about the same size.

Target coordinates come from the layout itself rather than guesswork: walk the
GDS hierarchy with KLayout and read off the absolute bbox of the instance you
want to land on.

## Why it is fast enough

Two things carry the load, and the first is what makes the second possible.

**Geometry lives in numpy.** `build()` returns one `(N, 4, 3)` float32 array
rather than nested Python lists, which cost ~1.1 kB per face and put a 7 M-face
cell at 12 GB. The `Poly3DCollection` is then built **once** and the frame loop
only moves the camera, so matplotlib stops re-converting the whole scene every
frame. Measured on a 1.6 M-quad cell: 56.4 -> 34.4 s/frame, 12.4 -> ~4 GB.

**Frames render in parallel.** A single render is single-threaded, so the loop
is cut into contiguous chunks that workers take from a queue, each encoding its
own part file, and the parts are joined with `ffmpeg -f concat -c copy` — no
re-encode. Slices must be contiguous because each part is a time range; camera
angles are still derived from the frame number, so the joined loop stays
seamless.

Together, on that same cell: **846.7 s -> 140.3 s for 15 frames, a 6x speedup**,
with output verified frame-for-frame against the serial render.

There are deliberately more chunks than workers (`CHUNKS`, default `JOBS * 6`).
Frames are nowhere near equal cost: in a `RUNGS` render the first loop draws a
few thousand quads and the last draws 1.4 M, about **100:1**. One chunk per
worker would leave the unlucky worker running for hours after the others had
finished; small chunks handed out on demand even that out.

Memory, not cores, sets `JOBS`. Each worker holds its own copy of the geometry
(~4 GB for the 1.6 M-quad cells), so 100 GB is about 24 workers however many
cores there are. The high-water mark is the first wave, where each worker still
holds the parsed JSON on top of its arrays — hence `STAGGER`, which spaces
those starts out. Forking workers *after* the geometry is built would let them
share it and use every core; not done yet.

## How it works

```
mag/*.mag  --magic-->  GDS  --klayout-->  per-layer polygons (JSON)
           --python-->  extruded prisms  --pipe-->  ffmpeg  -->  mp4
```

Frames are never written to disk. `render_stack.py` streams raw RGBA straight
into ffmpeg, because 900 PNGs is ~350 MB of clutter that ffmpeg would only read
back again. Passing a real directory instead of `-` still writes PNGs, which is
handy when you want to inspect a single frame.

- `export_gds.tcl` — magic writes each named cell out as GDS.
- `dump_layers.rb` — KLayout flattens the hierarchy, merges each layer, and
  decomposes the polygons into trapezoids. Trapezoids are convex quads, so the
  renderer can extrude them without handling holes.
- `render_stack.py` — extrudes each quad into a prism at its layer's real z, and
  orbits a camera. The camera path is periodic over the frame count, which is
  what makes the loop seamless.
- `make_video.sh` — runs all of it and pipes the frames into ffmpeg.

rawvideo carries no header, so ffmpeg is told the frame size up front and
`render_stack.py` aborts on frame 0 if its canvas disagrees, rather than
emitting a stream ffmpeg would silently misread.

KLayout's own 2.5D viewer is a GUI feature and cannot be driven headless, so
KLayout is used here for geometry only; the 3D is drawn with matplotlib.

## The scale bar

A bar sits bottom-right of each panel. It is a flat 2D overlay whose length is
calibrated against the real projection at the centre of the rock (`--az-centre`
/ `--el-centre`), so it is exact at that pose and drifts as the camera turns.

It reads `5 um` rather than the process node, because at this framing 130 nm
projects to about 3 pixels — smaller than the text stroke that would label it.
The node is stated separately in the bottom-left caption instead.

## Two deliberate distortions

The stack is about 6 um tall on a cell 12 um wide. At true scale it renders as a
pancake, so **z is exaggerated ~22x** (`ZEX`). And the upper metals are drawn
**semi-transparent**, otherwise met4 is an opaque lid over everything
interesting. Layer heights and colours are otherwise the real ones — heights
from the sky130 process, colours from `$PDK_ROOT/$PDK/libs.tech/klayout/tech/sky130A.lyp`.

## Adding a cell

Any cell in `mag/` works:

```bash
VIZ_CELLS="dpi_syn_inh_4bit_fc_v2_fed neuron_analog_fc_v2" ./tools_visualization/make_video.sh
```

To control the labels and per-panel framing, call the renderer directly:

```bash
python3 tools_visualization/render_stack.py build out_frames 600 \
    --panel "dpi_syn_inh_4bit_fc_v2_fed:SYNAPSE  ·  DPI, inhibitory:1.7" \
    --panel "neuron_analog_fc_v2:SOMA  ·  analog LIF neuron:1.6"
```

`ZOOM` (the third field) pulls the camera back for that panel — cells of
different sizes otherwise render at very different apparent scales.

## Requires

magic, klayout, ffmpeg, python3 with numpy + matplotlib, and `PDK_ROOT`/`PDK`
pointing at sky130A. All present on this machine.
