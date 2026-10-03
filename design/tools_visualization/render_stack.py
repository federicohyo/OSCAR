#!/usr/bin/env python3
"""Render sky130 cells as stacked 3D layer geometry -> PNG frames.

Reads the JSON written by dump_layers.rb, extrudes every layer to its real
height in the sky130 process, and orbits a camera around the result. The camera
path is periodic over the frame count, so the frames loop seamlessly.

  ./render_stack.py BUILD_DIR OUT_DIR N_FRAMES

OUT_DIR of "-" streams raw RGBA frames to stdout instead of writing one PNG per
frame, so they can be piped straight into ffmpeg without ever hitting disk (900
frames of PNG is ~400 MB of clutter). Progress then goes to stderr, to keep
stdout a clean video stream.

Panels are given as CELL:LABEL:ZOOM, repeated, via --panel. Zoom > 1 pulls the
camera back for that panel; it exists because cells of different sizes otherwise
render at wildly different apparent scales.
"""
import json, sys, os, math, time, argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# GDS layer -> (name, z bottom um, thickness um, colour, alpha).
# Heights are the real sky130 stack. Colours come from the PDK's own
# sky130A.lyp, except the via/contact layers, which are dimmed: at this scale
# there are hundreds of them and at full brightness they read as noise.
# Upper metals are translucent so the devices underneath stay visible.
STACK = [
    ("64/20", "nwell",  -0.30, 0.30, "#00cc66", 0.30),
    ("65/20", "diff",    0.00, 0.12, "#00ff00", 1.00),
    ("65/44", "tap",     0.00, 0.12, "#d9cc00", 1.00),
    ("66/20", "poly",    0.18, 0.18, "#ff2020", 1.00),
    ("66/44", "licon1",  0.36, 0.58, "#9a9478", 0.45),
    ("67/20", "li1",     0.94, 0.10, "#ffe6bf", 0.85),
    ("67/44", "mcon",    1.04, 0.34, "#7a7a88", 0.50),
    ("68/20", "met1",    1.38, 0.36, "#4060ff", 0.80),
    ("68/44", "via",     1.74, 0.27, "#7e30ff", 0.85),
    ("69/20", "met2",    2.01, 0.36, "#ff00ff", 0.55),
    ("69/44", "via2",    2.37, 0.42, "#ff8000", 0.85),
    ("70/20", "met3",    2.79, 0.82, "#00ffff", 0.42),
    ("70/44", "via3",    3.61, 0.41, "#38d69b", 0.85),
    ("71/20", "met4",    4.02, 0.82, "#8b3cff", 0.30),
    ("71/44", "via4",    4.84, 0.53, "#ffff00", 0.85),
    ("72/20", "met5",    5.37, 1.26, "#d9cc00", 0.30),
]

# name -> index in STACK, so a rung can be named "met2" rather than "69/20"
INDEX = {name: si for si, (_, name, *_) in enumerate(STACK)}

BG = "#05070c"


def rgba(h, a):
    c = h.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, a)


def shade(h, k):
    c = h.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda v: max(0, min(255, int(v * k)))
    return "#%02x%02x%02x" % (f(r), f(g), f(b))


def build(data, zex, dim):
    """Extrude every quad into a prism.

    Returns (verts, facecolours, edgecolours) as numpy arrays: verts is
    (N, 4, 3) float32, the colours (N, 4).

    Nested Python lists cost about 1.1 kB per face, which put a 7 M-face cell
    at 12 GB and forced matplotlib to re-convert the whole list on every frame.
    The same geometry as one float32 array is ~20x smaller and can be handed to
    a Poly3DCollection built once, so the per-frame conversion disappears.
    """
    Vs, FCs, ECs, spans = [], [], [], []
    nf = 0
    for si, (key, _name, z0, th, col, alpha) in enumerate(STACK):
        quads = data["layers"].get(key)
        if not quads:
            continue
        zb, zt = z0 * zex, (z0 + th) * zex

        # One uniform (Q, 4, 2) array. dump_layers.rb emits trapezoids but keeps
        # anything with >= 3 points, so pad triangles by repeating the last
        # vertex: the extra edge is degenerate and rasterises to nothing.
        Q = len(quads)
        P = np.empty((Q, 4, 2), dtype=np.float32)
        for i, q in enumerate(quads):
            m = len(q)
            if m >= 4:
                P[i] = q[:4]
            else:
                P[i, :m] = q
                P[i, m:] = q[-1]

        top = np.empty((Q, 4, 3), dtype=np.float32)
        top[:, :, :2] = P
        top[:, :, 2] = zt

        a = P                        # edge starts
        b = np.roll(P, -1, axis=1)   # edge ends
        w = np.empty((Q, 4, 4, 3), dtype=np.float32)
        w[:, :, 0, :2], w[:, :, 0, 2] = a, zb
        w[:, :, 1, :2], w[:, :, 1, 2] = b, zb
        w[:, :, 2, :2], w[:, :, 2, 2] = b, zt
        w[:, :, 3, :2], w[:, :, 3, 2] = a, zt
        walls = w.reshape(Q * 4, 4, 3)

        f_top = np.array(rgba(col, alpha * dim), dtype=np.float32)
        f_side = np.array(rgba(shade(col, 0.62), alpha * dim), dtype=np.float32)
        e_col = np.array(rgba(shade(col, 1.3), min(1.0, alpha + 0.25) * dim),
                         dtype=np.float32)

        Vs += [top, walls]
        FCs += [np.tile(f_top, (Q, 1)), np.tile(f_side, (Q * 4, 1))]
        ECs += [np.tile(e_col, (Q, 1)), np.tile(e_col, (Q * 4, 1))]
        spans.append((si, nf, nf + Q * 5))     # this layer's slice of the array
        nf += Q * 5

    if not Vs:
        z = np.zeros((0, 4, 3), dtype=np.float32)
        e = np.zeros((0, 4), dtype=np.float32)
        return z, e, e, []
    return (np.concatenate(Vs), np.concatenate(FCs), np.concatenate(ECs), spans)


def px_per_um(ax, cx, cy):
    """Screen pixels per data micron, measured horizontally.

    The scale bar is a flat 2D overlay, so it is only strictly true at one
    camera pose; we calibrate at the centre of the rock. Of all the directions
    lying on the substrate, we measure along the one that comes out horizontal
    on screen, since that is the direction the bar is drawn in.
    """
    M = ax.get_proj()

    def scr(x, y, z=0.0):
        xs, ys, _ = proj3d.proj_transform(x, y, z, M)
        return np.array(ax.transData.transform((xs, ys)))

    o = scr(cx, cy)
    vx, vy = scr(cx + 1.0, cy) - o, scr(cx, cy + 1.0) - o
    # unit in-plane direction a*ex + b*ey whose projection has no vertical part
    a, b = vy[1], -vx[1]
    n = math.hypot(a, b)
    if n < 1e-12:                       # dead-on top view; nothing is horizontal
        return math.hypot(*vx)
    v = (a / n) * vx + (b / n) * vy
    return math.hypot(*v)


def add_scale_bar(fig, i, n, bar_px, um, dim, colour="#7fe3d0"):
    """Draw a capped scale bar at the bottom-right of panel i, in figure coords."""
    fw, fh = fig.get_figwidth() * fig.dpi, fig.get_figheight() * fig.dpi
    x1 = 0.945
    x0 = x1 - bar_px / fw
    y = (0.5 * (n - 1 - i) if n == 2 else 0.0) + 0.042
    a = 0.85 * dim
    cap = 4.5 / fh
    segs = [([x0, x1], [y, y]), ([x0, x0], [y - cap, y + cap]),
            ([x1, x1], [y - cap, y + cap])]
    lines = []
    for xs, ys in segs:
        ln = Line2D(xs, ys, transform=fig.transFigure, color=colour, lw=1.3,
                    alpha=a, solid_capstyle="butt")
        fig.add_artist(ln)
        lines.append(ln)
    txt = fig.text((x0 + x1) / 2, y + 0.013, f"{um:g} \u00b5m", color=colour,
                   fontsize=9, family="monospace", alpha=a, ha="center")
    return lines, txt


NICE_UM = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]


def nice_bar(ppu, target_px=140.0):
    """Round micron length whose on-screen bar lands nearest target_px."""
    return min(NICE_UM, key=lambda u: abs(u * ppu - target_px))


def move_scale_bar(fig, handles, i, n, bar_px, um):
    """Re-point an existing bar; used when the camera zooms during the loop."""
    lines, txt = handles
    fw, fh = fig.get_figwidth() * fig.dpi, fig.get_figheight() * fig.dpi
    x1 = 0.945
    x0 = x1 - bar_px / fw
    y = (0.5 * (n - 1 - i) if n == 2 else 0.0) + 0.042
    cap = 4.5 / fh
    lines[0].set_data([x0, x1], [y, y])
    lines[1].set_data([x0, x0], [y - cap, y + cap])
    lines[2].set_data([x1, x1], [y - cap, y + cap])
    txt.set_position(((x0 + x1) / 2, y + 0.013))
    txt.set_text(f"{um:g} \u00b5m")


def peel_amount(frac, keys):
    """How many top layers are lifted off at this point in the loop.

    Driving the peel from a single scalar rather than a one-way schedule is
    what lets it run backwards: bring the amount back to 0 before t=1 and the
    stack reassembles, so a flythrough can return to its opening frame.
    """
    if frac <= keys[0][0]:
        return keys[0][1]
    if frac >= keys[-1][0]:
        return keys[-1][1]
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t0 <= frac <= t1:
            r = 0.0 if t1 == t0 else (frac - t0) / (t1 - t0)
            e = r * r * (3 - 2 * r)
            return p0 + (p1 - p0) * e
    return keys[-1][1]


def peel_alpha(amount):
    """{stack index: alpha multiplier} for a fractional number of peeled layers.

    Layer j down from the top is fully gone once amount passes j+1 and fully
    present below j, so a fractional amount fades exactly one layer at a time.
    """
    out = {}
    for j in range(len(STACK)):
        out[len(STACK) - 1 - j] = 1.0 - min(1.0, max(0.0, amount - j))
    return out


def rungs_to_keys(rungs, loop_fade):
    """Peel keys that put one more rung of the stack on screen per loop.

    A rung names the topmost layer standing at the end of that loop, so the
    peel amount it wants is however many layers sit above it. Each loop opens
    by easing from the previous rung's amount to its own: the smoothstep
    peel_amount already runs between keys is the fade, and a rung that adds a
    via and the metal on it fades them in one after the other for free.

    Slow-in matters here. Dense geometry stacks many translucent faces, so a
    linear fade reads as finished about a quarter of the way through; the
    smoothstep spends its first frames barely moving, which is what makes the
    layer look like it lands rather than blinks.
    """
    amounts = [len(STACK) - 1 - INDEX[r] for r in rungs]
    n = len(rungs)
    keys = [(0.0, float(amounts[0]))]
    for k in range(1, n):
        t = k / n
        keys.append((t, float(amounts[k - 1])))
        keys.append((t + loop_fade / n, float(amounts[k])))
    return keys


def rung_notes(rungs):
    """Caption for each loop: which layers it puts on."""
    out, low = [], 0
    for k, r in enumerate(rungs):
        top = INDEX[r]
        added = " + ".join(STACK[i][1] for i in range(low, top + 1))
        out.append(f"loop {k + 1}/{len(rungs)}   + {added}")
        low = top + 1
    return out


def rock_at(frac, keys, az_amp, el_amp):
    """Rock amplitudes at this point in the loop.

    A straight traverse wants the camera angle held still: with the rock
    running, azimuth and elevation swing underneath the pan and the apparent
    height and level of detail drift even though span and elevation are fixed.
    Taking the amplitudes to zero freezes the angle without a discontinuity,
    since the rock is amplitude * sin(u) and only the amplitude changes.
    """
    if not keys:
        return az_amp, el_amp
    if frac <= keys[0][0]:
        return keys[0][1], keys[0][2]
    if frac >= keys[-1][0]:
        return keys[-1][1], keys[-1][2]
    for (t0, a0, e0), (t1, a1, e1) in zip(keys, keys[1:]):
        if t0 <= frac <= t1:
            r = 0.0 if t1 == t0 else (frac - t0) / (t1 - t0)
            w = r * r * (3 - 2 * r)
            return a0 + (a1 - a0) * w, e0 + (e1 - e0) * w
    return keys[-1][1], keys[-1][2]


def parse_waypoint(spec):
    """T:CX:CY:SPAN[:ELEV] -- loop fraction, centre um, half-width um, degrees.

    ELEV is optional and defaults to --el-centre. It matters because the angle
    that flatters a whole array (low, looking across the stack) buries the
    camera in metal up close, where a steeper view reads like a layout.
    """
    v = [float(x) for x in spec.split(":")]
    if len(v) == 4:
        v.append(float("nan"))
    t, cx, cy, span, el = v
    return t, cx, cy, span, el


def camera_at(frac, wps):
    """Interpolate (cx, cy, span, elev) along the waypoint path.

    Centre moves linearly, span geometrically: a zoom that is linear in span
    spends most of its time already close in, whereas linear-in-log reads as a
    steady dive. Smoothstep on both so the move eases in and out.
    """
    if frac <= wps[0][0]:
        return wps[0][1:]
    if frac >= wps[-1][0]:
        return wps[-1][1:]
    for (t0, x0, y0, s0, e0), (t1, x1, y1, s1, e1) in zip(wps, wps[1:]):
        if t0 <= frac <= t1:
            r = 0.0 if t1 == t0 else (frac - t0) / (t1 - t0)
            e = r * r * (3 - 2 * r)
            return (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e,
                    s0 * (s1 / s0) ** e, e0 + (e1 - e0) * e)
    return wps[-1][1:]


def parse_panel(spec):
    parts = spec.split(":")
    cell = parts[0]
    label = parts[1] if len(parts) > 1 else cell
    zoom = float(parts[2]) if len(parts) > 2 else 1.0
    return cell, label, zoom


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build_dir")
    ap.add_argument("out_dir")
    ap.add_argument("frames", type=int)
    ap.add_argument("--panel", action="append", default=None,
                    help="CELL:LABEL:ZOOM (repeatable)")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--zex", type=float, default=22.0,
                    help="z exaggeration; the true stack is a pancake at cell scale")
    ap.add_argument("--span", type=float, default=0.27,
                    help="camera distance as a fraction of the cell diagonal")
    ap.add_argument("--dim", type=float, default=1.0,
                    help="global alpha multiplier; <1 pushes it into the background")
    ap.add_argument("--spin", action="store_true",
                    help="full 360 orbit instead of the default rock")
    ap.add_argument("--az-centre", type=float, default=95.0)
    ap.add_argument("--az-amp", type=float, default=45.0)
    ap.add_argument("--el-centre", type=float, default=20.0)
    ap.add_argument("--el-amp", type=float, default=8.0)
    ap.add_argument("--scale-um", type=float, default=5.0,
                    help="scale-bar length in microns; 0 disables it. "
                         "A true-to-scale 130 nm bar would be ~3 px, hence the "
                         "round micron default")
    ap.add_argument("--waypoint", action="append", default=None,
                    help="T:CX:CY:SPAN (repeatable) -- fly the camera along "
                         "these points instead of holding the cell centred. T "
                         "is a fraction of the loop, SPAN a half-width in um. "
                         "A one-way path does not loop seamlessly.")
    ap.add_argument("--rock-key", action="append", default=None,
                    help="T:AZ_AMP:EL_AMP (repeatable) -- vary the rock over "
                         "the loop. Take both to 0 to hold the camera angle "
                         "still, e.g. during a straight pan.")
    ap.add_argument("--peel-key", action="append", default=None,
                    help="T:P (repeatable) -- P top layers peeled at loop "
                         "fraction T, interpolated between keys. Return P to "
                         "its starting value before t=1 for a loopable path.")
    ap.add_argument("--peel", default=None,
                    help="T0:T1:N -- fade the top N layers of the stack away "
                         "between loop fractions T0 and T1, topmost first. "
                         "Lets a zoom reach device level instead of burying "
                         "the camera in upper metal.")
    ap.add_argument("--loop-frames", type=int, default=None,
                    help="frames in one loop (default: all of them). Set it "
                         "below FRAMES to repeat the same flight several times "
                         "in one render, which is what --rung builds on: the "
                         "camera repeats while the stack keeps growing.")
    ap.add_argument("--rung", action="append", default=None,
                    help="LAYER (repeatable, bottom-up) -- add one rung of the "
                         "stack per loop, LAYER being the topmost layer left "
                         "standing at the end of that loop, e.g. --rung poly "
                         "--rung li1 --rung met1. Implies a peel schedule, so "
                         "it cannot be combined with --peel/--peel-key.")
    ap.add_argument("--rung-fade", type=float, default=0.12,
                    help="fraction of a loop spent fading the new rung in")
    ap.add_argument("--frame-start", type=int, default=0,
                    help="first frame of a contiguous slice; camera angles are "
                         "still derived from the total frame count so parallel "
                         "chunks line up seamlessly")
    ap.add_argument("--frame-count", type=int, default=None,
                    help="how many frames of the slice to render (default: all "
                         "the way to the end)")
    ap.add_argument("--node-note", default="sky130  \u00b7  130 nm process",
                    help="small caption bottom-left; empty string disables")
    args = ap.parse_args()

    specs = args.panel or [
        "neuron_analog_fc_v2:SOMA  ·  analog LIF neuron:1.62",
        "dpi_syn_exc_4bit_fc_v2:SYNAPSE  ·  DPI, 4-bit weight (exc):1.72",
    ]

    built = []
    for spec in specs:
        cell, label, zoom = parse_panel(spec)
        d = json.load(open(f"{args.build_dir}/{cell}.json"))
        verts, fc, ec, spans = build(d, args.zex, args.dim)
        x0, y0, x1, y1 = d["bbox"]
        # The parsed JSON is several GB of Python lists for a big cell and is
        # dead once the geometry is in numpy. Drop it before the next panel so
        # parallel workers each hold the arrays, not the parse tree.
        d = None
        built.append(dict(verts=verts, fc=fc, ec=ec, label=label, spans=spans,
                          fa0=fc[:, 3].copy(), ea0=ec[:, 3].copy(),
                          cx=(x0 + x1) / 2, cy=(y0 + y1) / 2,
                          span=math.hypot(x1 - x0, y1 - y0) * args.span * zoom))
        print(f"{cell}: {len(verts)} faces", file=sys.stderr, flush=True)

    n = len(built)
    # The span default is calibrated for the two-panel layout, where each panel
    # gets half the frame. A lone panel needs the camera further back.
    if n == 1:
        built[0]["span"] *= 1.85

    stream = args.out_dir == "-"
    if not stream:
        os.makedirs(args.out_dir, exist_ok=True)
    dpi = 100
    fig = plt.figure(figsize=(args.width / dpi, args.height / dpi),
                     dpi=dpi, facecolor=BG)

    # Axes are transparent and deliberately oversized: matplotlib leaves a wide
    # dead margin around a 3D axes, and overfilling crops it back off.
    axes = []
    for i in range(n):
        ax = fig.add_subplot(n, 1, i + 1, projection="3d", facecolor="none")
        if n == 2:
            ax.set_position([-0.26, 0.36 - 0.475 * i, 1.52, 0.80])
        else:
            ax.set_position([-0.20, -0.10, 1.40, 1.20])
        axes.append(ax)

    for i, b in enumerate(built):
        fig.text(0.06, 0.945 - (0.50 * i if n == 2 else 0), b["label"],
                 color="#7fe3d0", fontsize=11, family="monospace",
                 alpha=0.85 * args.dim)

    # The rung caption is the only text that changes during a render, so it
    # gets its own artist rather than being rebuilt into the panel label.
    rung_txt = None
    if args.rung:
        rung_txt = fig.text(0.06, 0.911, "", color="#ffd166", fontsize=10,
                            family="monospace", alpha=0.9 * args.dim)

    if args.node_note:
        fig.text(0.055, 0.018, args.node_note, color="#5f7f8c", fontsize=8,
                 family="monospace", alpha=0.8 * args.dim)

    # Pose the axes once. Nothing below changes them again, so the camera can
    # be moved per frame with view_init alone.
    for ax, b in zip(axes, built):
        ax.set_facecolor("none")
        ax.patch.set_alpha(0.0)
        ax.set_xlim(b["cx"] - b["span"], b["cx"] + b["span"])
        ax.set_ylim(b["cy"] - b["span"], b["cy"] + b["span"])
        ax.set_zlim(-1 * args.zex, 7.0 * args.zex)
        ax.set_box_aspect((1, 1, 1.05))
        ax.set_axis_off()
        ax.view_init(elev=args.el_centre, azim=args.az_centre)

    wps = sorted(parse_waypoint(w) for w in (args.waypoint or []))
    wps = [(t, cx, cy, sp, args.el_centre if el != el else el)
           for t, cx, cy, sp, el in wps]          # el != el catches the NaN
    bars = {}
    rock_keys = sorted(tuple(float(v) for v in k.split(":"))
                       for k in (args.rock_key or [])) or None
    peel_keys = None
    if args.peel_key:
        peel_keys = sorted(tuple(float(v) for v in k.split(":"))
                           for k in args.peel_key)
    elif args.peel:
        pt0, pt1, pn = (float(v) for v in args.peel.split(":"))
        # the one-shot form never comes back, so it does not loop
        peel_keys = [(0.0, 0.0), (pt0, 0.0), (pt1, pn), (1.0, pn)]
    notes = None
    if args.rung:
        if peel_keys:
            sys.exit("--rung sets the peel itself; drop --peel/--peel-key")
        bad = [r for r in args.rung if r not in INDEX]
        if bad:
            sys.exit(f"unknown layer(s) {bad}; known: {', '.join(INDEX)}")
        idx = [INDEX[r] for r in args.rung]
        if idx != sorted(idx) or len(set(idx)) != len(idx):
            sys.exit(f"rungs must climb the stack: {args.rung}")
        peel_keys = rungs_to_keys(args.rung, args.rung_fade)
        notes = rung_notes(args.rung)
        for note in notes:
            print(f"  {note}", file=sys.stderr, flush=True)
    if peel_keys:
        top = max(p for _, p in peel_keys)
        names = ", ".join(STACK[len(STACK) - 1 - j][1]
                          for j in range(int(math.ceil(top))))
        print(f"  peel keys {peel_keys} -> up to {top:g} layers: {names}",
              file=sys.stderr, flush=True)
    last_vis = None
    last_cut = None
    last_note = None

    # Calibrate the overlay bar against the real projection while the axes are
    # still empty: the projection depends only on the limits, box aspect and
    # view, so this draw costs nothing even for a 7 M-face cell.
    if args.scale_um > 0:
        fig.canvas.draw()
        for i, (ax, b) in enumerate(zip(axes, built)):
            ppu = px_per_um(ax, b["cx"], b["cy"])
            print(f"  panel {i}: {ppu:.2f} px/um -> {args.scale_um:g} um bar = "
                  f"{ppu * args.scale_um:.1f} px", file=sys.stderr, flush=True)
            bars[i] = add_scale_bar(fig, i, n, ppu * args.scale_um,
                                    args.scale_um, args.dim)

    # Attach the geometry once. Poly3DCollection re-projects from the axes
    # matrix on every draw, so the camera can move without rebuilding it --
    # which is the whole point of keeping the verts in one numpy array.
    for ax, b in zip(axes, built):
        b["ax"] = ax
        b["cut"] = len(b["verts"])
        b["coll"] = Poly3DCollection(
            b["verts"], facecolors=b["fc"], edgecolors=b["ec"],
            linewidths=0.14, shade=False)
        ax.add_collection3d(b["coll"])

    start = args.frame_start
    count = (args.frames - start if args.frame_count is None
             else min(args.frame_count, args.frames - start))
    if count <= 0:
        sys.exit(f"nothing to render: frames={args.frames} start={start} "
                 f"count={args.frame_count}")

    # The camera runs on the loop clock, the peel on the whole render's clock.
    # Splitting the two is the whole trick: the same flight repeats while the
    # stack keeps growing underneath it.
    loop_n = args.loop_frames or args.frames
    if args.frames % loop_n:
        print(f"  warning: {args.frames} frames is not a whole number of "
              f"{loop_n}-frame loops; the last loop is cut short",
              file=sys.stderr, flush=True)

    t0 = time.time()
    for i in range(count):
        fr = start + i
        lf = (fr % loop_n) / loop_n              # position within this loop
        u = 2 * math.pi * lf                     # one full period => seamless
        az_amp, el_amp = rock_at(lf, rock_keys, args.az_amp, args.el_amp)
        if args.spin:
            az = 360.0 * lf
            el = args.el_centre + el_amp * math.sin(u)
        else:
            az = args.az_centre + az_amp * math.sin(u)
            el = args.el_centre + el_amp * math.cos(u)

        if wps:
            _, _, _, el_base = camera_at(lf, wps)
            el = el_base + el_amp * math.cos(u)

        for ax in axes:
            ax.view_init(elev=el, azim=az)

        if peel_keys:
            vis = peel_alpha(peel_amount(fr / args.frames, peel_keys))
            # ^ global: the peel is the one thing that does not repeat
            # only rewrite the layers whose alpha actually moved; at 7 M faces
            # touching every layer each frame is real work
            moved = {si for si, m in vis.items()
                     if last_vis is None or last_vis.get(si) != m}
            if moved:
                for b in built:
                    for si, i0, i1 in b["spans"]:
                        if si in moved:
                            m = vis[si]
                            b["fc"][i0:i1, 3] = b["fa0"][i0:i1] * m
                            b["ec"][i0:i1, 3] = b["ea0"][i0:i1] * m
                last_vis = vis

                # Layers are stacked bottom-to-top in the arrays, and the peel
                # always takes the top ones, so whatever is still visible is a
                # contiguous prefix. Slicing the fully transparent tail off
                # keeps matplotlib from depth-sorting and rasterising faces
                # that cannot contribute a pixel -- worth ~37% of the geometry
                # on this cell while the stack is peeled back.
                for b in built:
                    cut = 0
                    for si, i0, i1 in b["spans"]:
                        if vis.get(si, 1.0) > 0.0:
                            cut = max(cut, i1)
                    if cut != b.get("cut"):
                        b["cut"] = cut
                        b["coll"].remove()
                        b["coll"] = Poly3DCollection(
                            b["verts"][:cut], facecolors=b["fc"][:cut],
                            edgecolors=b["ec"][:cut], linewidths=0.14,
                            shade=False)
                        b["ax"].add_collection3d(b["coll"])
                    else:
                        b["coll"].set_facecolor(b["fc"][:cut])
                        b["coll"].set_edgecolor(b["ec"][:cut])

        if wps:
            # Re-window the axes; the geometry is untouched, so this stays
            # cheap -- the collection re-projects on every draw regardless.
            cx, cy, span, _ = camera_at(lf, wps)
            for j, ax in enumerate(axes):
                ax.set_xlim(cx - span, cx + span)
                ax.set_ylim(cy - span, cy + span)
                if j in bars:
                    # A bar calibrated once would be wrong by the zoom factor,
                    # so re-measure and relabel it as the window changes.
                    ppu = px_per_um(ax, cx, cy)
                    um = nice_bar(ppu)
                    move_scale_bar(fig, bars[j], j, n, um * ppu, um)

        if notes:
            k = min(fr // loop_n, len(notes) - 1)
            if k != last_note:
                rung_txt.set_text(notes[k])
                last_note = k

        if stream:
            fig.canvas.draw()
            if i == 0:
                got = fig.canvas.get_width_height()
                if got != (args.width, args.height):
                    # rawvideo has no header: ffmpeg is told the size up front,
                    # so a mismatch would silently shear the whole video.
                    sys.exit(f"canvas is {got[0]}x{got[1]}, expected "
                             f"{args.width}x{args.height} -- refusing to write "
                             f"a rawvideo stream that ffmpeg would misread")
            sys.stdout.buffer.write(fig.canvas.buffer_rgba())
        else:
            fig.savefig(f"{args.out_dir}/f{fr:04d}.png",
                        facecolor=BG, pad_inches=0)
        if i % 20 == 0 or i == count - 1:
            e = time.time() - t0
            print(f"  {i + 1}/{count}  {e:.1f}s  ({e/(i+1):.2f}s/frame)",
                  file=sys.stderr, flush=True)

    if stream:
        sys.stdout.buffer.flush()
    print(f"done in {time.time() - t0:.1f}s", file=sys.stderr, flush=True)


main()
