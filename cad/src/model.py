"""ThermaCart parametric model (build123d), TRL 3, constructable design (TCT-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL and prints the constructability checks
    python cad/src/model.py --check    prints the constructability checks only
Exports into cad/step and cad/stl:
    thermacart-assembly.step / .stl   one TC-L cartridge (C5 key) seated in its adapter frame
    tc-l-cartridge.step / .stl        the cartridge alone
    end-cap.step / .stl               the handle-end cap stack (flange, gland spacer, plug)
    adapter-frame.step / .stl         the adapter frame with the C5 key slot, tabs and rivets

Axes: X along the cartridge (handle at +X, keyed nose at -X), Y across, Z up, units mm.
The frame floor underside is at z = 0; the bottom fins rest on the floor top at z = FLOOR_T.

The concept model (TCT-DDR-001, TCT-DDR-002) showed what ThermaCart does. This version is the
constructable design: every part can be cut, drilled, bent or bought, and every part is fixed
to the next (TCT-DDR-003). build_components() returns each component with its BOM line and
whether it is made or bought; build_parts() keeps the grouped names that docs/04-calcs/sizing.py,
cad/src/concept_media.py and cad/src/product_model.py use. checks() runs the build123d
constructability checks (overlaps, contacts and clearances).
Main dimensions and interfaces only; no tolerances before TRL 4. Not for fabrication.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 shell: 6063-T52 rectangular tube 6 x 2 x 1/8 in, cut length, stock corner radii (to confirm
    #   with the supplier: outside 3/16 in, inside 1/16 in)
    "tube_w": 152.4, "tube_h": 50.8, "tube_t": 3.175, "tube_l": 280.0,
    "tube_ro": 4.8, "tube_ri": 1.6, "lead_chamfer": 1.0,
    # 1 fins: 6063 flat bar 1/4 x 1/16 in bonded on edge, top and bottom faces
    "fin_n": 9, "fin_h": 6.35, "fin_t": 1.59, "fin_edge": 10.0, "fin_inset": 8.0,
    "label_band": 95.0,                 # top fins cut back over this length at the handle end
    # 1 finish (TCT-DDR-002, O8): outer shell, fins and caps painted matte black with a
    #   high-temperature paint over etch primer, emissivity about 0.9; no geometry change
    "finish": "matte black high-temperature paint, emissivity about 0.9",
    # 3 end caps: flange outside the tube, O-ring gland spacer and plug inside it, bonded face to
    #   face. The gland is the corner between tube bore, flange, spacer edge and plug (DDR-003, P2)
    "flange_t": 3.175, "spacer_t": 3.0, "gland_depth": 2.1, "plug_t": 9.525, "plug_clear": 0.2,
    "plug_r": 2.0, "oring_cord": 2.5, "cap_screws": 6,
    # radial cap screws: M5 x 10 A2 button head (ISO 7380) on an FKM bonded sealing washer,
    #   through the tube wall into a tapped hole in the plug edge, between the fins (DDR-003, P3)
    "screw": "M5 x 10 A2 button head with FKM bonded seal", "screw_y": (-41.75, 8.25, 58.25),
    "screw_l": 10.0, "screw_head": (9.5, 2.75), "seal_m5": (10.0, 5.7, 1.0), "tap_depth": 7.5,
    # cap stack screws: M4 x 12 A2 countersunk through flange and spacer into a blind tapped hole
    "stack_screw_y": {"handle": (-56.0,), "key": (-56.0, 56.0)},
    # 2 fill: fraction of the inner volume filled as liquid at the grade's fill temperature
    "fill_fraction": 0.90,
    # 4 fill port: G 1/2 plug with collar and hex socket (DIN 908 class) on a bonded FKM seal,
    #   in the handle-end cap, clear of the O-ring gland (DDR-003, P1)
    "port_d": 20.955, "port_thread_l": 12.0, "port_collar": (26.0, 3.0), "port_seal": (28.7, 21.5, 2.0),
    "port_y": 56.0, "port_head": 5.0,
    # 5 handle: folding bail. Two lug angles (20 x 20 x 3 mm aluminium angle, 32 long) stand on
    #   phenolic thermal-break washers and are held by two M4 bolts each into the plug; a 16 x 4 mm
    #   arm pivots on a 5 mm stainless pin on the outside of each angle; a 16 mm rod with a silicone
    #   grip is screwed between the arms (DDR-003, P5). Shown stowed (hanging against the end face).
    #   Pivot 47.5 mm up and arms 36 mm between holes (TCT-DEC-001 item 1, 2026-10-02): the stowed
    #   grip is 3.5 mm higher than before, its underside 1.85 mm above the frame lip's top.
    "angle": (20.0, 3.0), "lug_len": 32.0, "lug_z0": 22.0, "lug_yout": 40.0, "break_t": 3.0,
    "break_washer": (9.0, 4.5), "lug_bolt_y": 27.0, "lug_bolt_z": (30.0, 40.0), "lug_bolt_hole": 6.5,
    "head_washer": (9.0, 4.3, 3.0), "pivot_dx": 15.0, "pivot_z": 47.5, "pin_d": 5.0,
    "arm_w": 16.0, "arm_t": 4.0, "bail_arm": 36.0, "rod_d": 16.0, "grip_od": 24.0, "grip_l": 60.0,
    # 5 keyed nose: tab position across the nose codes the grade (Y of the tab centre); two
    #   M4 x 16 socket cap screws in 5 mm counterbores, 7 mm each side of the tab centre (DDR-003, P6)
    "key_l": 10.0, "key_w": 30.0, "key_h": 16.0, "key_z": 4.0, "key_screw_dy": 7.0, "key_screw_z": 14.0,
    "key_y": {"C5": -43.0, "C25": 0.0, "H70": 43.0, "W0": -61.0},
    "grade": "C5",
    # 1 grade colour band (TCT-DEC-001 item 7): 18 mm painted band round the nose end of the shell,
    #   masked, starting 22 mm from the key-end face; paint only, no solid in the assembly
    "band_x0": 22.0, "band_w": 18.0,
    # 6 label band and melt indicator: a clear polycarbonate tube 6 x 4 mm, 40 long, holding the
    #   grade's PCM, bonded to the shell between two guards of fin bar, in a notch in the label
    #   (DDR-003, P9)
    "label_l": 74.0, "label_t": 0.6, "ind_od": 6.0, "ind_id": 4.0, "ind_l": 40.0, "ind_y": 30.0,
    "ind_x1": 16.0, "guard_dy": 8.0,
    # 7 adapter frame: bent 1.5 mm aluminium sheet; floor, two side walls, keyed end stop; the side
    #   walls end in 12 mm tabs folded round the outside of the stop, two 3.2 mm rivets each (P7, P8)
    "frame_t": 1.5, "frame_clear": 2.5, "frame_wall_h": 30.0, "stop_h": 40.0,
    "stop_gap": 2.0, "slot_clear": 3.0, "tab_l": 12.0, "rivet_z": (8.0, 22.0),
    #   low lip folded up at the open end (TCT-DEC-001 item 1, option (b)): its inside face is
    #   lip_gap beyond the seated bottom fins' ends, so the fins drop behind it only when the key is
    #   through the slot; a wrong grade's key meets the stop 8 mm short of seated and its fins land
    #   on top of the lip. Three notches let the bottom radial screw heads drop past the lip.
    "lip_h": 4.0, "lip_gap": 3.0, "lip_notch": 14.0,
}

Comp = namedtuple("Comp", "name shape bom kind group")


def derived(p=PARAMS):
    """Dimensions the calc note, drawings and build plan quote, computed from PARAMS."""
    t = p["tube_t"]
    in_w, in_h = p["tube_w"] - 2 * t, p["tube_h"] - 2 * t
    plug_depth = p["spacer_t"] + p["plug_t"]
    in_l = p["tube_l"] - 2 * plug_depth
    floor_top = p["frame_t"]
    z0 = floor_top + p["fin_h"]                      # tube underside
    z1 = z0 + p["tube_h"]
    xt0, xt1 = -p["tube_l"] / 2, p["tube_l"] / 2
    xe0, xe1 = xt0 - p["flange_t"], xt1 + p["flange_t"]
    rod_x = xe1 + p["pivot_dx"]                      # bail rod (and pivot) plane when stowed
    fin_end = xt1 - p["fin_inset"]                   # handle-end ends of the bottom fins
    x_min = xe0 - p["key_l"]
    x_max = max(rod_x + p["grip_od"] / 2, xe1 + p["break_t"] + p["angle"][0])
    fin_pitch = (p["tube_w"] - 2 * p["fin_edge"]) / (p["fin_n"] - 1)
    fin_len_bot = p["tube_l"] - 2 * p["fin_inset"]
    fin_len_top = fin_len_bot - (p["label_band"] - p["fin_inset"] + 1.0)
    frame_in_w = p["tube_w"] + 2 * p["frame_clear"]
    fx0 = xe0 - p["stop_gap"] - p["frame_t"]          # outer face of the end stop
    lip_x = fin_end + p["lip_gap"]                   # inside face of the lip
    fx1 = lip_x + p["frame_t"]                       # outside face of the lip (frame open end)
    short = p["key_l"] - p["stop_gap"]               # how far short a wrong grade stops (key tip on the stop)
    g = p["gland_depth"]
    sp_w, sp_h = in_w - 2 * g, in_h - 2 * g
    cord_a = math.pi * p["oring_cord"] ** 2 / 4
    return {
        "in_w": in_w, "in_h": in_h, "in_l": in_l, "plug_depth": plug_depth,
        "v_inner_l": in_w * in_h * in_l / 1e6,
        "z0": z0, "z1": z1, "zm": (z0 + z1) / 2, "floor_top": floor_top,
        "xt0": xt0, "xt1": xt1, "xe0": xe0, "xe1": xe1, "rod_x": rod_x,
        "x_min": x_min, "x_max": x_max,
        "grip_z": z0 + p["pivot_z"] - p["bail_arm"],
        # finger gap between the end flange and the grip with the bail swung out level
        "finger_gap": p["pivot_dx"] + p["bail_arm"] - p["grip_od"] / 2,
        "overall_l": x_max - x_min, "overall_w": p["tube_w"],
        "overall_h": p["tube_h"] + 2 * p["fin_h"],
        "fin_pitch": fin_pitch, "fin_len_bot": fin_len_bot, "fin_len_top": fin_len_top,
        "frame_w": frame_in_w + 2 * p["frame_t"], "frame_in_w": frame_in_w,
        "fx0": fx0, "fx1": fx1, "frame_l": fx1 - fx0, "lip_x": lip_x, "fin_end": fin_end,
        "lip_top": floor_top + p["lip_h"], "short": short,
        # a wrong grade's bottom fins overlap the lip top by this much (they rest on it)
        "lip_bearing": fin_end + short - lip_x,
        "seated_lip_gap": lip_x - fin_end,
        "spacer_w": sp_w, "spacer_h": sp_h, "spacer_r": p["tube_ri"] + g,
        "plug_w": in_w - 2 * p["plug_clear"], "plug_h": in_h - 2 * p["plug_clear"],
        "gland_fill": cord_a / (p["spacer_t"] * g), "squeeze": 1 - g / p["oring_cord"],
        "x_screw": (xt0 + p["spacer_t"] + p["plug_t"] / 2, xt1 - p["spacer_t"] - p["plug_t"] / 2),
        # outer area of the tube (4 faces), both flange faces and all fin faces, m2
        "area_tube_m2": 2 * (p["tube_w"] + p["tube_h"]) * p["tube_l"] / 1e6,
        "area_fins_m2": p["fin_n"] * (fin_len_bot + fin_len_top) * 2 * p["fin_h"] / 1e6,
        "area_ends_m2": 2 * p["tube_w"] * p["tube_h"] / 1e6,
    }


# ------------------------------------------------------------------ geometry helpers
def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rrect_x(x0, x1, w, h, r, zc, yc=0.0):
    """Rounded rectangle w (Y) x h (Z), corner radius r, extruded along X from x0 to x1."""
    from build123d import Plane, Pos, RectangleRounded, extrude
    return Pos(x0, yc, zc) * extrude(Plane.YZ * RectangleRounded(w, h, r), amount=x1 - x0)


def xcyl(x0, x1, y, z, d):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, x1 - x0)


def ycyl(y0, y1, x, z, d):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(d / 2, y1 - y0)


def zcyl(z0, z1, x, y, d):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(d / 2, z1 - z0)


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ components
def build_components(p=PARAMS, grade=None):
    """Every component as a Comp(name, shape, bom, kind, group), keyed by a short name, in build
    order. kind is 'made', 'bought' or 'fixing'."""
    D = derived(p)
    grade = grade or p["grade"]
    t, tw, th = p["tube_t"], p["tube_w"], p["tube_h"]
    y0, y1 = -tw / 2, tw / 2
    z0, z1, zm = D["z0"], D["z1"], D["zm"]
    xt0, xt1, xe0, xe1 = D["xt0"], D["xt1"], D["xe0"], D["xe1"]
    C = {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    # 1 shell tube, with the twelve radial screw holes (5.5 mm) through its top and bottom walls
    tube = rrect_x(xt0, xt1, tw, th, p["tube_ro"], zm) - rrect_x(xt0 - 1, xt1 + 1, D["in_w"], D["in_h"], p["tube_ri"], zm)
    for xs in D["x_screw"]:
        for yy in p["screw_y"]:
            tube -= zcyl(z0 - 1, z0 + t + 1, xs, yy, 5.5) + zcyl(z1 - t - 1, z1 + 1, xs, yy, 5.5)
    add("tube", "Shell tube", tube, 1, "made", "shell")

    # 1 fins, bonded on edge
    bot, top = [], []
    for i in range(p["fin_n"]):
        y = y0 + p["fin_edge"] + i * D["fin_pitch"]
        yb, yt = y - p["fin_t"] / 2, y + p["fin_t"] / 2
        bot.append(box(xt0 + p["fin_inset"], xt1 - p["fin_inset"], yb, yt, z0 - p["fin_h"], z0))
        top.append(box(xt0 + p["fin_inset"], xt1 - p["label_band"] - 1.0, yb, yt, z1, z1 + p["fin_h"]))
    add("fins_bot", "Bottom fins (9)", fuse(bot), 1, "made", "shell")
    add("fins_top", "Top fins (9)", fuse(top), 1, "made", "shell")

    # 3 end cap stacks: flange (outside), gland spacer and plug (inside), bonded face to face
    g, c = p["gland_depth"], p["plug_clear"]
    ky = p["key_y"][grade]

    def holes_x(xa, xb, pts, d):
        return fuse([xcyl(xa, xb, yy, zz, d) for yy, zz in pts])

    def cap(end):
        s = 1 if end == "handle" else -1
        xo = xt1 if s > 0 else xt0                    # tube end face
        span = lambda a, b: tuple(sorted((xo + s * a, xo + s * b)))  # noqa: E731
        fl = rrect_x(*span(0, p["flange_t"]), tw, th, p["tube_ro"], zm)
        sp = rrect_x(*span(0, -p["spacer_t"]), D["spacer_w"], D["spacer_h"], D["spacer_r"], zm)
        pl = rrect_x(*span(-p["spacer_t"], -D["plug_depth"]), D["plug_w"], D["plug_h"], p["plug_r"], zm)
        xs = xo - s * (p["spacer_t"] + p["plug_t"] / 2)
        # tapped holes for the radial screws in the plug's top and bottom edges
        zt, zb = z1 - t - c, z0 + t + c
        for yy in p["screw_y"]:
            pl -= zcyl(zt - p["tap_depth"], zt + 0.1, xs, yy, 5.0) + zcyl(zb - 0.1, zb + p["tap_depth"], xs, yy, 5.0)
        xf_out = xo + s * p["flange_t"]               # flange outer face
        xp_in = xo - s * D["plug_depth"]              # plug inner face (wet)
        blind = xp_in + s * 2.0                        # tapped holes stop 2 mm short of the wet face
        if end == "handle":
            bolts = [(sy * p["lug_bolt_y"], z0 + bz) for sy in (-1, 1) for bz in p["lug_bolt_z"]]
            stack = [(yy, zm) for yy in p["stack_screw_y"]["handle"]]
            # G 1/2 tapped port through the whole stack
            port = xcyl(min(xf_out, xp_in) - 0.1, max(xf_out, xp_in) + 0.1, p["port_y"], zm, p["port_d"])
            fl, sp, pl = fl - port, sp - port, pl - port
        else:
            bolts = [(ky + sd * p["key_screw_dy"], z0 + p["key_screw_z"]) for sd in (-1, 1)]
            stack = [(yy, zm) for yy in p["stack_screw_y"]["key"]]
        for pts, d in ((bolts, 4.0), (stack, 4.0)):
            hx = holes_x(min(xf_out, blind), max(xf_out, blind), pts, d)
            fl, sp, pl = fl - hx, sp - hx, pl - hx
        # countersinks for the stack screws in the flange
        fl -= holes_x(min(xf_out, xf_out - s * 2.2), max(xf_out, xf_out - s * 2.2), stack, 8.0)
        return fl, sp, pl

    for end in ("key", "handle"):
        fl, sp, pl = cap(end)
        nm = "Key-end" if end == "key" else "Handle-end"
        add(f"flange_{end}", f"{nm} flange", fl, 3, "made", f"cap_{end}")
        add(f"spacer_{end}", f"{nm} gland spacer", sp, 3, "made", f"cap_{end}")
        add(f"plug_{end}", f"{nm} plug", pl, 3, "made", f"cap_{end}")
        # O-ring: spliced FKM cord in the gland, squeezed between spacer edge and tube bore
        xo = xt1 if end == "handle" else xt0
        s = 1 if end == "handle" else -1
        xc = xo - s * p["spacer_t"] / 2
        ring = (rrect_x(xc - p["oring_cord"] / 2, xc + p["oring_cord"] / 2, D["in_w"], D["in_h"], p["tube_ri"], zm)
                - rrect_x(xc - 2, xc + 2, D["spacer_w"], D["spacer_h"], D["spacer_r"], zm))
        add(f"oring_{end}", f"{nm} O-ring (FKM cord 2.5 mm, spliced)", ring, 3, "bought", f"cap_{end}")
        # stack screws: countersunk M4 x 12
        xf_out = xo + s * p["flange_t"]
        shs = []
        for yy in p["stack_screw_y"][end]:
            x_a, x_b = sorted((xf_out, xf_out - s * 12.0))
            shs.append(xcyl(x_a, x_b, yy, zm, 4.0))
            x_a, x_b = sorted((xf_out, xf_out - s * 2.2))
            shs.append(xcyl(x_a, x_b, yy, zm, 8.0))
        add(f"stack_screws_{end}", f"{nm} stack screws, M4 countersunk", fuse(shs), 8, "fixing", f"cap_{end}")

    # radial cap screws: shank through the tube wall into the plug edge, button head on a bonded seal
    sd, sk = p["screw_head"]
    od, idd, st = p["seal_m5"]
    for end, xs in (("key", D["x_screw"][0]), ("handle", D["x_screw"][1])):
        parts = []
        for yy in p["screw_y"]:
            for zf, sg in ((z1, 1), (z0, -1)):
                seal = zcyl(*sorted((zf, zf + sg * st)), xs, yy, od) - zcyl(zf - 2, zf + 2, xs, yy, idd)
                head = zcyl(*sorted((zf + sg * st, zf + sg * (st + sk))), xs, yy, sd)
                shank = zcyl(*sorted((zf + sg * st, zf + sg * (st - p["screw_l"]))), xs, yy, 5.0)
                parts += [seal, head, shank]
        nm = "Key-end" if end == "key" else "Handle-end"
        add(f"screws_{end}", f"{nm} radial screws (6) with bonded seals", fuse(parts), 8, "fixing", f"cap_{end}")

    # 5 key tab on the nose, two M4 x 16 socket cap screws in 5 mm counterbores
    kx0, kx1 = D["x_min"], xe0
    kz0, kz1 = z0 + p["key_z"], z0 + p["key_z"] + p["key_h"]
    key = box(kx0, kx1, ky - p["key_w"] / 2, ky + p["key_w"] / 2, kz0, kz1)
    kpts = [(ky + sd_ * p["key_screw_dy"], z0 + p["key_screw_z"]) for sd_ in (-1, 1)]
    key -= holes_x(kx0 - 1, kx1 + 1, kpts, 4.5) + holes_x(kx0 - 1, kx0 + 5, kpts, 8.0)
    add("key", f"Key tab ({grade})", key, 5, "made", "key")
    ks = fuse([xcyl(kx0 + 5, kx0 + 5 + 16, yy, zz, 4.0) for yy, zz in kpts]
              + [xcyl(kx0 + 1, kx0 + 5, yy, zz, 7.0) for yy, zz in kpts])
    add("key_screws", "Key tab screws, M4 x 16 socket cap (2)", ks, 8, "fixing", "key")

    # 5 handle: lug angles on thermal-break washers, arms, pins, rod, grip
    a_leg, a_t = p["angle"]
    zl0, zl1 = z0 + p["lug_z0"], z0 + p["lug_z0"] + p["lug_len"]
    xb0 = xe1 + p["break_t"]
    xp, zp = xe1 + p["pivot_dx"], z0 + p["pivot_z"]
    yo = p["lug_yout"]
    lugs, washers, bolts, heads = [], [], [], []
    arms, pins, rod_screws = [], [], []
    for sy in (-1, 1):
        ys = sorted((sy * (yo - a_leg), sy * yo))
        base = box(xb0, xb0 + a_t, *ys, zl0, zl1)
        yl = sorted((sy * (yo - a_t), sy * yo))
        leg = box(xb0, xb0 + a_leg, *yl, zl0, zl1)
        lug = base + leg
        for bz in p["lug_bolt_z"]:
            lug -= xcyl(xb0 - 1, xb0 + a_t + 1, sy * p["lug_bolt_y"], z0 + bz, p["lug_bolt_hole"])
            wo, wi = p["break_washer"]
            washers.append(xcyl(xe1, xb0, sy * p["lug_bolt_y"], z0 + bz, wo) - xcyl(xe1 - 1, xb0 + 1, sy * p["lug_bolt_y"], z0 + bz, wi))
            ho, hi, ht = p["head_washer"]
            xh = xb0 + a_t
            heads.append(xcyl(xh, xh + ht, sy * p["lug_bolt_y"], z0 + bz, ho) - xcyl(xh - 1, xh + ht + 1, sy * p["lug_bolt_y"], z0 + bz, hi))
            # M4 x 20 socket cap bolt: head on the head washer, shank into the plug
            bolts.append(xcyl(xh + ht, xh + ht + 4.0, sy * p["lug_bolt_y"], z0 + bz, 7.0))
            bolts.append(xcyl(xh + ht - 20.0, xh + ht, sy * p["lug_bolt_y"], z0 + bz, 4.0))
        lug -= ycyl(min(yl) - 1, max(yl) + 1, xp, zp, p["pin_d"] + 0.2)
        lugs.append(lug)
        # arm: 16 x 4 flat bar, round ends, outside the angle's upright leg
        ya = sorted((sy * yo, sy * (yo + p["arm_t"])))
        zr = D["grip_z"]
        arm = (box(xp - p["arm_w"] / 2, xp + p["arm_w"] / 2, *ya, zr, zp)
               + ycyl(*ya, xp, zp, p["arm_w"]) + ycyl(*ya, xp, zr, p["arm_w"]))
        arm -= ycyl(ya[0] - 1, ya[1] + 1, xp, zp, p["pin_d"] + 0.2) + ycyl(ya[0] - 1, ya[1] + 1, xp, zr, 6.5)
        arms.append(arm)
        # pivot pin: head inside the angle leg, nyloc nut outside the arm
        yin = sy * (yo - a_t)
        pins.append(ycyl(*sorted((yin, sy * (yo + p["arm_t"] + 5.0))), xp, zp, p["pin_d"]))
        pins.append(ycyl(*sorted((yin, yin - sy * 3.0)), xp, zp, 8.0))
        pins.append(ycyl(*sorted((sy * (yo + p["arm_t"]), sy * (yo + p["arm_t"] + 5.0))), xp, zp, 8.0))
        # rod-end screw: M6 x 12 button head through the arm into the rod end
        rod_screws.append(ycyl(*sorted((sy * (yo + p["arm_t"]), sy * (yo + p["arm_t"] + 3.3))), xp, zr, 10.5))
        rod_screws.append(ycyl(*sorted((sy * (yo + p["arm_t"]), sy * (yo - 8.0))), xp, zr, 6.0))
    add("thermal_break", "Thermal-break washers, phenolic (4)", fuse(washers), 5, "bought", "handle")
    add("lugs", "Lug angles (2)", fuse(lugs), 5, "made", "handle")
    add("head_washers", "Phenolic washers under the lug bolt heads (4)", fuse(heads), 5, "bought", "handle")
    add("lug_bolts", "Lug bolts, M4 x 20 socket cap (4)", fuse(bolts), 8, "fixing", "handle")
    add("arms", "Bail arms (2)", fuse(arms), 5, "made", "handle")
    add("pins", "Pivot pins, 5 mm stainless, with nyloc nuts (2)", fuse(pins), 5, "fixing", "handle")
    rod = ycyl(-yo, yo, xp, D["grip_z"], p["rod_d"])
    rod -= ycyl(-yo - 1, -yo + 12, xp, D["grip_z"], 6.0) + ycyl(yo - 12, yo + 1, xp, D["grip_z"], 6.0)
    add("rod", "Bail rod", rod, 5, "made", "handle")
    add("rod_screws", "Rod-end screws, M6 x 12 button head (2)", fuse(rod_screws), 8, "fixing", "handle")
    grip = ycyl(-p["grip_l"] / 2, p["grip_l"] / 2, xp, D["grip_z"], p["grip_od"]) - ycyl(-p["grip_l"], p["grip_l"], xp, D["grip_z"], p["rod_d"])
    add("grip", "Silicone grip sleeve", grip, 5, "bought", "handle")

    # 4 fill port plug: thread in the stack, bonded seal and collar on the flange face
    so, si, sth = p["port_seal"]
    cd, ch = p["port_collar"]
    py = p["port_y"]
    port = (xcyl(xe1 - p["port_thread_l"], xe1, py, zm, p["port_d"])
            + xcyl(xe1 + sth, xe1 + sth + ch, py, zm, cd)
            + (xcyl(xe1, xe1 + sth, py, zm, so) - xcyl(xe1 - 1, xe1 + sth + 1, py, zm, si)))
    from build123d import Plane, Pos, RegularPolygon, extrude
    port -= Pos(xe1 + sth + ch - 2.5, py, zm) * extrude(Plane.YZ * RegularPolygon(5.0, 6), amount=3.0)
    add("port", "Fill port plug G 1/2 with bonded seal", port, 4, "bought", "port")

    # 2 PCM fill (level at the fill temperature, ullage at the top when lying flat)
    fill_h = D["in_h"] * p["fill_fraction"]
    xi0, xi1 = xt0 + D["plug_depth"], xt1 - D["plug_depth"]
    fill = rrect_x(xi0 + 0.3, xi1 - 0.3, D["in_w"] - 0.6, D["in_h"] - 0.6, p["tube_ri"] - 0.3, zm)
    fill &= box(xi0, xi1, y0, y1, z0 + t, z0 + t + fill_h)
    add("fill", f"PCM fill ({grade})", fill, 2, "bought", "fill")

    # 6 label band (notched for the indicator), indicator tube and its guards
    lx1 = xt1 - 15.0
    iy, ix1 = p["ind_y"], xt1 - p["ind_x1"]
    ix0 = ix1 - p["ind_l"]
    label = box(lx1 - p["label_l"], lx1, y0 + 16, y1 - 16, z1, z1 + p["label_t"])
    label -= box(ix0 - 4, lx1 + 1, iy - p["guard_dy"] - 4, iy + p["guard_dy"] + 4, z1 - 1, z1 + 2)
    add("label", "Grade label (polyester)", label, 6, "bought", "indicator")
    zc = z1 + p["ind_od"] / 2
    ind = xcyl(ix0, ix1, iy, zc, p["ind_od"]) - xcyl(ix0 + 3, ix1 - 3, iy, zc, p["ind_id"])
    pcm = xcyl(ix0 + 3, ix1 - 3, iy, zc, p["ind_id"])
    add("indicator", "Melt indicator tube (polycarbonate, PCM filled)", ind + pcm, 6, "made", "indicator")
    guards = fuse([box(ix0, ix1, iy + sd_ * p["guard_dy"] - p["fin_t"] / 2, iy + sd_ * p["guard_dy"] + p["fin_t"] / 2, z1, z1 + p["fin_h"])
                   for sd_ in (-1, 1)])
    add("guards", "Indicator guards (2, fin bar)", guards, 6, "made", "indicator")

    # 7 adapter frame: floor, side walls with corner tabs, end stop with the key slot, rivets
    ft = p["frame_t"]
    fx0, fx1 = D["fx0"], D["fx1"]
    wi = D["frame_in_w"] / 2
    floor = box(fx0, fx1, -wi - ft, wi + ft, 0, ft)
    walls = box(fx0, fx1, -wi - ft, -wi, ft, ft + p["frame_wall_h"]) + box(fx0, fx1, wi, wi + ft, ft, ft + p["frame_wall_h"])
    stop = box(fx0, fx0 + ft, -wi, wi, ft, ft + p["stop_h"])
    sc = p["slot_clear"]
    stop -= box(fx0 - 1, fx0 + ft + 1, ky - p["key_w"] / 2 - sc, ky + p["key_w"] / 2 + sc,
                z0 + p["key_z"] - sc, z0 + p["key_z"] + p["key_h"] + sc)
    tabs = (box(fx0 - ft, fx0, -wi - ft, -wi - ft + p["tab_l"], ft, ft + p["frame_wall_h"])
            + box(fx0 - ft, fx0, wi + ft - p["tab_l"], wi + ft, ft, ft + p["frame_wall_h"]))
    rv, rpts = [], [(sy * (wi + ft - p["tab_l"] / 2), ft + rz) for sy in (-1, 1) for rz in p["rivet_z"]]
    for yy, zz in rpts:
        hole = xcyl(fx0 - ft - 1, fx0 + ft + 1, yy, zz, 3.3)
        stop -= hole
        tabs -= hole
        rv += [xcyl(fx0 - ft, fx0 + ft, yy, zz, 3.2), xcyl(fx0 + ft, fx0 + ft + 1.0, yy, zz, 6.0),
               xcyl(fx0 - ft - 2.0, fx0 - ft, yy, zz, 4.5)]
    lip = box(D["lip_x"], fx1, -wi - ft, wi + ft, ft, D["lip_top"])
    for yy in p["screw_y"]:
        lip -= box(D["lip_x"] - 1, fx1 + 1, yy - p["lip_notch"] / 2, yy + p["lip_notch"] / 2, ft, D["lip_top"] + 1)
    frame = floor + walls + stop + tabs + lip
    add("frame", "Adapter frame", frame, 7, "made", "frame")
    add("rivets", "Frame rivets, 3.2 mm blind (4)", fuse(rv), 7, "fixing", "frame")
    return C


def build_parts(p=PARAMS):
    """Grouped solids used by sizing.py, concept_media.py and product_model.py."""
    C = build_components(p)
    S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
    return {
        "tube": C["tube"].shape, "fins": S("fins_bot", "fins_top"), "shell": S("tube", "fins_bot", "fins_top"),
        "fill": C["fill"].shape,
        "cap_handle_end": S("flange_handle", "spacer_handle", "plug_handle"),
        "cap_key_end": S("flange_key", "spacer_key", "plug_key"),
        "orings": S("oring_handle", "oring_key"),
        "screws": S("screws_handle", "screws_key", "stack_screws_handle", "stack_screws_key", "key_screws",
                    "lug_bolts", "rod_screws"),
        "port": C["port"].shape,
        "thermal_break": S("thermal_break", "head_washers"),
        "handle": S("lugs", "arms", "rod", "pins"),
        "grip": C["grip"].shape, "key": C["key"].shape,
        "indicator": S("label", "indicator", "guards"),
        "frame": S("frame", "rivets"),
    }


def cartridge(p=PARAMS):
    from build123d import Compound
    C = build_components(p)
    return Compound(children=[c.shape for k, c in C.items() if c.group != "frame"])


def assembly(p=PARAMS):
    from build123d import Compound
    C = build_components(p)
    return Compound(children=[c.shape for c in C.values()])


def grade_band(p=PARAMS, grade=None, thick=0.3):
    """The painted grade band as a thin skin round the tube (appearance only, not a component)."""
    D = derived(p)
    tw, th = p["tube_w"], p["tube_h"]
    x0 = D["xt0"] + p["band_x0"]
    ring = (rrect_x(x0, x0 + p["band_w"], tw + 2 * thick, th + 2 * thick, p["tube_ro"] + thick, D["zm"])
            - rrect_x(x0 - 1, x0 + p["band_w"] + 1, tw, th, p["tube_ro"], D["zm"]))
    C = build_components(p, grade)
    return ring - C["fins_bot"].shape - C["fins_top"].shape


def wrong_grade(C, grade, p=PARAMS, on_lip=True):
    """Cartridge components of another grade pushed into a C5 frame until its key meets the stop:
    moved 12 mm back toward the handle end, and either resting on the lip (on_lip) or, to show it
    cannot drop in, at the seated height."""
    from build123d import Pos
    D = derived(p)
    W = build_components(p, grade)
    dz = p["lip_h"] if on_lip else 0.0
    return {k: Pos(D["short"], 0, dz) * c.shape for k, c in W.items() if c.group != "frame"}


def bail_swung(C, angle, p=PARAMS):
    """The bail (arms, pins, rod, grip, rod screws) turned about the pivot by angle degrees
    (0 stowed, 90 level, 180 straight up)."""
    from build123d import Axis, Pos
    D = derived(p)
    xp, zp = D["xe1"] + p["pivot_dx"], D["z0"] + p["pivot_z"]
    ax = Axis((xp, 0, zp), (0, -1, 0))
    return fuse([C[k].shape.rotate(ax, angle) for k in ("arms", "rod", "grip", "rod_screws")])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, and pairs that must stay apart by a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    D = derived(p)
    S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        """expect: 'touch' (no overlap, gap 0) or a minimum clearance in mm."""
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Bottom fins on the tube", S("fins_bot"), S("tube"), "touch")
    chk("Top fins on the tube", S("fins_top"), S("tube"), "touch")
    for end in ("key", "handle"):
        nm = "Key-end" if end == "key" else "Handle-end"
        chk(f"{nm} flange on the tube end", S(f"flange_{end}"), S("tube"), "touch")
        chk(f"{nm} spacer on the flange (bonded)", S(f"spacer_{end}"), S(f"flange_{end}"), "touch")
        chk(f"{nm} plug on the spacer (bonded)", S(f"plug_{end}"), S(f"spacer_{end}"), "touch")
        chk(f"{nm} plug clear of the tube bore", S(f"plug_{end}"), S("tube"), 0.15)
        chk(f"{nm} spacer clear of the tube bore (gland depth)", S(f"spacer_{end}"), S("tube"), p["gland_depth"] - 0.05)
        chk(f"{nm} O-ring on the tube bore", S(f"oring_{end}"), S("tube"), "touch")
        chk(f"{nm} O-ring on the spacer edge", S(f"oring_{end}"), S(f"spacer_{end}"), "touch")
        chk(f"{nm} radial screws in the plug", S(f"screws_{end}"), S(f"plug_{end}"), "touch")
        chk(f"{nm} radial screws clear of the fins", S(f"screws_{end}"), S("fins_bot", "fins_top"), 1.0)
        chk(f"{nm} radial screws clear of the O-ring", S(f"screws_{end}"), S(f"oring_{end}"), 2.0)
        chk(f"{nm} stack screws in the plug", S(f"stack_screws_{end}"), S(f"plug_{end}"), "touch")
        chk(f"{nm} stack screws clear of the radial screws", S(f"stack_screws_{end}"), S(f"screws_{end}"), 1.5)
        chk(f"{nm} stack screws clear of the O-ring", S(f"stack_screws_{end}"), S(f"oring_{end}"), 2.0)
        chk(f"{nm} plug clear of the PCM", S(f"plug_{end}"), S("fill"), 0.2)
    chk("Fill port plug in the handle-end cap", S("port"), S("flange_handle"), "touch")
    chk("Fill port clear of the O-ring", S("port"), S("oring_handle"), 3.0)
    chk("Fill port clear of the radial screws", S("port"), S("screws_handle"), 1.5)
    chk("Fill port clear of the lug bolts and stack screw", S("port"), S("lug_bolts", "stack_screws_handle"), 1.5)
    chk("Key tab on the key-end flange", S("key"), S("flange_key"), "touch")
    chk("Key screws in the plug", S("key_screws"), S("plug_key"), "touch")
    chk("Key screws clear of the radial screws", S("key_screws"), S("screws_key"), 1.5)
    chk("Key screws clear of the O-ring", S("key_screws"), S("oring_key"), 2.0)
    chk("Thermal-break washers on the flange", S("thermal_break"), S("flange_handle"), "touch")
    chk("Lug angles on the thermal-break washers", S("lugs"), S("thermal_break"), "touch")
    chk("Lug angles clear of the flange (3 mm break)", S("lugs"), S("flange_handle"), p["break_t"] - 0.05)
    chk("Lug bolts in the plug", S("lug_bolts"), S("plug_handle"), "touch")
    chk("Lug bolts clear of the angles (air gap in the hole)", S("lug_bolts"), S("lugs"), 1.0)
    chk("Lug bolts clear of the radial screws", S("lug_bolts"), S("screws_handle"), 1.5)
    chk("Lug bolts clear of the O-ring", S("lug_bolts"), S("oring_handle"), 2.0)
    chk("Bail arms on the angles' upright legs", S("arms"), S("lugs"), "touch")
    chk("Pivot pins through the angles and arms", S("pins"), S("arms"), "touch")
    chk("Rod between the arms", S("rod"), S("arms"), "touch")
    chk("Grip on the rod", S("grip"), S("rod"), "touch")
    chk("Grip clear of the handle-end flange", S("grip"), S("flange_handle"), 2.0)
    chk("Grip clear of the lug angles and bolt heads", S("grip"), S("lugs", "lug_bolts", "head_washers"), 1.5)
    chk("Bail clear of the fill port plug", S("arms", "rod", "rod_screws", "grip"), S("port"), 1.5)
    chk("Pivot pins clear of the lug bolts", S("pins"), S("lug_bolts", "head_washers"), 1.0)
    chk("Label on the shell", S("label"), S("tube"), "touch")
    chk("Indicator tube on the shell", S("indicator"), S("tube"), "touch")
    chk("Indicator guards on the shell", S("guards"), S("tube"), "touch")
    chk("Indicator clear of its guards", S("indicator"), S("guards"), 3.0)
    chk("Indicator and guards clear of the top fins", S("indicator", "guards"), S("fins_top"), 20.0)
    chk("Indicator and guards clear of the radial screws", S("indicator", "guards", "label"), S("screws_handle"), 2.0)
    frame = S("frame", "rivets")
    chk("Bottom fins on the frame floor", S("fins_bot"), S("frame"), "touch")
    chk("Key tab through the stop slot", S("key"), S("frame"), 2.5)
    chk("Nose flange clear of the stop and rivet heads", S("flange_key", "stack_screws_key", "key_screws"), frame, 0.9)
    chk("Radial screw heads clear of the frame floor", S("screws_key", "screws_handle"), frame, 2.0)
    chk("Grip clear of the frame floor", S("grip"), frame, 2.0)
    chk("Shell clear of the frame walls", S("tube", "flange_key", "flange_handle"), S("frame"), 2.0)
    chk("Frame tabs on the stop (riveted)", S("rivets"), S("frame"), "touch")
    for ang in (90, 180):
        sw = bail_swung(C, ang, p)
        chk(f"Bail swung to {ang} degrees clear of the cartridge", sw,
            S("tube", "fins_top", "flange_handle", "port", "lug_bolts", "head_washers", "label", "indicator", "guards"), 2.0)
    # Frame lip (TCT-DEC-001 item 1): the right grade seats behind it, a wrong grade is held out,
    # with the bail stowed (0 degrees) and raised (180 degrees)
    chk("C5 seated: bottom fins behind the lip", S("fins_bot"), S("frame"), "touch")
    chk("C5 seated: fin ends clear of the lip's inside face", S("fins_bot"),
        box(D["lip_x"], D["fx1"], -100, 100, 0, D["lip_top"]), p["lip_gap"] - 0.05)
    chk("C5 seated: radial screw heads clear of the lip notches", S("screws_handle"),
        S("frame") & box(D["lip_x"] - 0.1, D["fx1"] + 0.1, -100, 100, p["frame_t"], D["lip_top"]), 2.0)
    for ang in (0, 180):
        bl = S("arms", "rod", "grip", "rod_screws") if ang == 0 else bail_swung(C, ang, p)
        chk(f"C5 seated, bail at {ang} degrees: bail clear of the frame and lip", bl, frame, 2.0)
    from build123d import Axis, Pos
    for g in [k for k in p["key_y"] if k not in (p["grade"], "W0")]:
        W = wrong_grade(C, g, p, on_lip=True)
        chk(f"{g} in the C5 frame: key on the stop face", W["key"], S("frame"), "touch")
        chk(f"{g} in the C5 frame: bottom fins resting on the lip", W["fins_bot"], S("frame"), "touch")
        chk(f"{g} in the C5 frame: no other contact with the frame", fuse([W[k] for k in W if k not in ("key", "fins_bot")]), frame, 0.5)
        v = _vol(wrong_grade(C, g, p, on_lip=False)["fins_bot"], S("frame"))
        rows.append((f"{g} in the C5 frame: cannot drop to the floor (fins would cut into the lip)", v, 0.0, "blocked", v > 1.0))
        ax = Axis((D["rod_x"] + D["short"], 0, D["z0"] + p["pivot_z"] + p["lip_h"]), (0, -1, 0))
        for ang in (0, 180):
            bl = fuse([W[k].rotate(ax, ang) if ang else W[k] for k in ("arms", "rod", "grip", "rod_screws")])
            chk(f"{g} in the C5 frame, bail at {ang} degrees: bail clear of the frame", bl, frame, 2.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:60s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    D = derived()
    import copy
    items = {
        "thermacart-assembly": list(C),
        "tc-l-cartridge": [k for k, c in C.items() if c.group != "frame"],
        "end-cap": ["flange_handle", "spacer_handle", "plug_handle"],
        "adapter-frame": ["frame", "rivets"],
    }
    for name, keys in items.items():
        c = Compound(children=[copy.copy(C[k].shape) for k in keys])   # copies: a shape has one parent
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    print(f"cartridge overall {D['overall_l']:.1f} x {D['overall_w']:.1f} x {D['overall_h']:.1f} mm; "
          f"inner {D['in_w']:.2f} x {D['in_h']:.2f} x {D['in_l']:.1f} mm = {D['v_inner_l']:.3f} L; "
          f"frame {D['frame_l']:.1f} x {D['frame_w']:.1f} mm")
    print(f"O-ring gland fill {D['gland_fill'] * 100:.0f} %, squeeze {D['squeeze'] * 100:.0f} %; finger gap {D['finger_gap']:.0f} mm")
    print_checks()
