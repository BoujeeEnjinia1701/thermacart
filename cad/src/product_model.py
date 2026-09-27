"""ThermaCart product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a TC-L cartridge in the cold-chain grade (C5) seated
in its adapter frame. The finned tube and end flanges carry the matte black finish (TCT-DDR-002,
O8) with filleted edges and a seam at each flange; radial cap screws with hex sockets; a grade
colour band round the nose end; a printed polyester label with the grade block, wordmark and data
lines; the sight window as a black bezel, clear lens and the white (solid, charged) PCM vial under
it; the G 3/4 fill port plug with its sealing washer; the folding bail on phenolic thermal-break
washers with pivot pins and a ribbed silicone grip; and the aluminium key tab at the grade position.
Inside: the PCM fill, the gland spacer and plug of each cap and the FKM O-rings. The adapter frame
has bend radii and a grade decal beside its key slot.
Context: a compact bench top with the other two grades (C25 green, H70 red) lying behind the C5
cartridge as a lineup, each with its key tab at its own grade position.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: X along the cartridge (handle at +X, keyed nose at -X), Y across, Z up, units mm;
the frame floor underside is at z = 0 and sits on the bench top. The bail is shown stowed, as in
model.py. The lineup cartridges are the same geometry with the grade's key position (PARAMS
"key_y") and lie directly on the bench. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Text,
                       extrude, fillet)
from model import PARAMS, derived, build_parts

FONT = str(Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

TITLE = "ThermaCart: swappable phase-change thermal storage cartridge"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); C5 cold-chain cartridge in "
             "its adapter frame, handle end at right, with the C25 and H70 grades lying behind it"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): finned shell, PCM fill, "
             "end caps with O-rings, cap screws, label and sight window, fill port plug, folding bail, key tab, "
             "adapter frame"},
    {"name": "detail", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 22, "az": -140,
     "note": "Detail from the front left and above (about 22 deg elevation): keyed nose at the adapter frame's "
             "end stop, with the grade key slot and the blue C5 band"},
]

# Colours (restrained product palette; kit accent)
C_BLACK = "#2B2F35"      # matte black high-temperature paint
C_ALU = "#C3C8CE"        # bare aluminium (bail, key, frame)
C_ALU_DK = "#A9B0B8"     # plate inside the caps
C_STEEL = "#B8BEC6"      # A2 stainless
C_PHENOLIC = "#6B4A2E"
C_RUBBER = "#33373D"     # silicone grip
C_FKM = "#1C1D20"
C_LABEL = "#F4F4F1"
C_INK = "#2B2F36"
C_ACCENT = "#0F766E"
C_BEZEL = "#1E2126"
C_LENS = "#DDEAF3"
C_VIAL = "#F3F1EA"       # solid paraffin is opaque white (charged)
C_BENCH = "#DAD7D1"
GRADE = {"C5": ("#2F6DB3", "#D6E4F2", "5 °C cold chain"),
         "C25": ("#3C8A56", "#DCEBDF", "25 °C comfort"),
         "H70": ("#B8412F", "#F1DDD7", "70 °C hot holding")}
LINEUP = [("C25", 172.0), ("H70", 338.0)]   # grade and Y offset of the lineup cartridges on the bench
BENCH = (-190.0, 205.0, -108.0, 432.0, 24.0)  # x0, x1, y0, y1, thickness (top at z = 0)


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _par(s, axis):
    return s.edges().filter_by(axis)


def _face_edges(s, axis, i):
    return s.faces().sort_by(axis)[i].edges()


def _text_top(txt, size, x, y, z, h=0.2, align=(Align.CENTER, Align.CENTER)):
    """Raised text on a face that looks up (+Z), reading along +X."""
    return Pos(x, y, z) * extrude(Text(txt, font_size=size, font_path=FONT, align=align), amount=h)


def _text_front(txt, size, x, y, z, h=0.25):
    """Raised text on a face that looks toward -Y (front), reading along +X."""
    return Pos(x, y, z) * extrude(Plane.XZ * Text(txt, font_size=size, font_path=FONT,
                                                  align=(Align.CENTER, Align.CENTER)), amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _cartridge(P, D, grade, dy=0.0, dz=0.0):
    """Appearance parts of one cartridge as tuples (key, name, shape, color, material, bom, explode)."""
    t, tw, th = P["tube_t"], P["tube_w"], P["tube_h"]
    y0, y1 = -tw / 2, tw / 2
    z0, z1 = D["z0"], D["z1"]
    zm = (z0 + z1) / 2
    xt0, xt1, xe0, xe1 = D["xt0"], D["xt1"], D["xe0"], D["xe1"]
    col, tint, gname = GRADE[grade]
    R = 4.0                                   # outer corner radius of the stock tube
    out = []

    def add(key, name, shape, color, material, bom, explode):
        out.append((key, name, Pos(0, dy, dz) * shape, color, material, bom, explode))

    # 1 shell: tube with rounded outer corners, fins with softened ends
    outer = _box(xt0, xt1, y0, y1, z0, z1)
    outer = _fillet_try(outer, _par(outer, Axis.X), [R, 3.0, 2.0])
    tube = outer - _box(xt0 - 1, xt1 + 1, y0 + t, y1 - t, z0 + t, z1 - t)
    add("tube", "Cartridge shell tube (6063, matte black)", tube, C_BLACK, "painted", 1, (0, 0, 0))
    fins = []
    for i in range(P["fin_n"]):
        y = y0 + P["fin_edge"] + i * D["fin_pitch"]
        yb, yt = y - P["fin_t"] / 2, y + P["fin_t"] / 2
        for fz0, fz1, fx1, top in ((z0 - P["fin_h"], z0, xt1 - P["fin_inset"], False),
                                   (z1, z1 + P["fin_h"], xt1 - P["label_band"] - 1.0, True)):
            f = _box(xt0 + P["fin_inset"], fx1, yb, yt, fz0, fz1)
            outer_face = _face_edges(f, Axis.Z, -1 if top else 0)
            f = _fillet_try(f, [e for e in outer_face if e.length > 5], [0.6, 0.4])
            fins.append(f)
    add("fins", "Cartridge fins (18 bars, matte black)", _union(fins), C_BLACK, "painted", 1, (0, 0, 0))

    # grade colour band round the nose end of the tube (painted), cut round the fins
    bx0, bx1 = xt0 + 22.0, xt0 + 40.0
    ring = _box(bx0, bx1, y0 - 0.3, y1 + 0.3, z0 - 0.3, z1 + 0.3)
    ring = _fillet_try(ring, _par(ring, Axis.X), [R + 0.3, 3.3, 2.3])
    core = _box(bx0 - 1, bx1 + 1, y0, y1, z0, z1)
    core = _fillet_try(core, _par(core, Axis.X), [R, 3.0, 2.0])
    band = ring - core
    for f in fins:
        band -= f
    add("band", f"Grade colour band ({grade}, painted)", band, col, "painted", 1, (0, 0, 0))

    # side marking on the front face (white paint)
    mark = _text_front("ThermaCart", 10.0, 40.0, y0, z0 + 40.5, 0.25)
    mark += _text_front(f"TC-L  {grade}", 5.5, 40.0, y0, z0 + 30.5, 0.25)
    add("mark", "Side marking (painted)", mark, "#E7E8EA", "painted", 6, (0, -40, 0))

    # 3 end caps: flange outside (shell), gland spacer and plug inside (internal), O-rings
    c, g = P["plug_clear"], P["gland_depth"]
    for sgn, xo, label in ((1, xt1, "handle end"), (-1, xt0, "keyed end")):
        lo, hi = sorted((xo, xo + sgn * P["flange_t"]))
        fl = _box(lo, hi, y0, y1, z0, z1)
        fl = _fillet_try(fl, _par(fl, Axis.X), [R, 3.0, 2.0])
        fl = _fillet_try(fl, _face_edges(fl, Axis.X, -1 if sgn > 0 else 0), [0.8, 0.5])
        a0, a1 = sorted((xo, xo - sgn * P["spacer_t"]))
        p0, p1 = sorted((xo - sgn * P["spacer_t"], xo - sgn * D["plug_depth"]))
        inner = (_box(a0, a1, y0 + t + g, y1 - t - g, z0 + t + g, z1 - t - g)
                 + _box(p0, p1, y0 + t + c, y1 - t - c, z0 + t + c, z1 - t - c))
        if sgn > 0:
            bore = _xcyl(xo, P["port_y"], zm, P["port_d"] / 2 - 1.5, 60)
            fl -= bore
            inner -= bore
        ex = sgn * 130.0
        add(f"flange_{sgn}", f"End cap flange, {label} (matte black)", fl, C_BLACK, "painted", 3, (ex, 0, 0))
        add(f"plug_{sgn}", f"End cap spacer and plug, {label} (6061)", inner, C_ALU_DK, "metal", 3,
            (sgn * 85.0, 0, 0))
        xr = xo - sgn * P["spacer_t"] / 2
        rc = P["oring_cord"] / 2
        ring = (_box(xr - rc, xr + rc, y0 + t, y1 - t, z0 + t, z1 - t)
                - _box(xr - rc - 1, xr + rc + 1, y0 + t + g, y1 - t - g, z0 + t + g, z1 - t - g))
        add(f"oring_{sgn}", f"FKM O-ring, {label}", ring, C_FKM, "rubber", 3, (sgn * 55.0, 0, 0))

    # radial cap screws (BOM 8): heads with hex sockets, top and bottom, positions as model.py
    heads_t, heads_b = [], []
    for x in (xt0 + P["spacer_t"] + P["plug_t"] / 2, xt1 - P["spacer_t"] - P["plug_t"] / 2):
        for yy in (-50.0, 0.0, 50.0):
            for zz, sg in ((z1, 1), (z0, -1)):
                h = Pos(x, yy + 8.25, zz + sg * 0.6) * Cylinder(4.5, 1.2)
                h = _fillet_try(h, _face_edges(h, Axis.Z, -1 if sg > 0 else 0), [0.5, 0.3])
                sock = Pos(x, yy + 8.25, zz + sg * 1.2) * extrude(RegularPolygon(1.75, 6), amount=1.6, both=True)
                (heads_t if sg > 0 else heads_b).append(h - sock)
    add("screws_t", "Cap screws, top (M5 A2)", _union(heads_t), C_STEEL, "metal", 8, (0, 0, 45))
    add("screws_b", "Cap screws, bottom (M5 A2)", _union(heads_b), C_STEEL, "metal", 8, (0, 0, -45))

    # 4 fill port plug: shank in the bore, sealing washer, hex head with a chamfered top
    py = P["port_y"]
    shank = _xcyl(xe1 - 6.0, py, zm, P["port_d"] / 2 - 1.6, 12.0)
    wash = _xcyl(xe1 + 0.75, py, zm, P["port_d"] / 2 + 1.0, 1.5)
    hx0, hx1 = xe1 + 1.5, xe1 + P["port_head"]
    hexa = Pos(hx0, py, zm) * extrude(Plane.YZ * RegularPolygon((P["port_d"] / 2 + 2) * 0.98, 6), amount=hx1 - hx0)
    cham = _xcyl((hx0 + hx1) / 2, py, zm, P["port_d"] / 2 + 2.4, hx1 - hx0)
    cham = _fillet_try(cham, _face_edges(cham, Axis.X, -1), [2.2, 1.5])
    head = (hexa & cham) - (Pos(hx1, py, zm) * extrude(Plane.YZ * RegularPolygon(5.5, 6), amount=-4.0))
    add("port", "Fill port plug, G 3/4 hex (stainless)", shank + head, C_STEEL, "metal", 4, (175, 0, 60))
    add("washer", "Fill port sealing washer (FKM)", wash, C_FKM, "rubber", 4, (150, 0, 60))

    # 5 folding bail on thermal-break washers (stowed), as model.py
    lw, ly = P["lug_w"], P["lug_y"]
    zp = z0 + P["pivot_z"]
    zl0, zl1 = zp - P["lug_h"] / 2, zp + P["lug_h"] / 2
    xb0 = xe1 + P["break_t"]
    brk = _union([_box(xe1, xb0, s * ly - lw / 2, s * ly + lw / 2, zl0, zl1) for s in (-1, 1)])
    add("break", "Thermal-break washers (phenolic)", brk, C_PHENOLIC, "plastic", 5, (165, 0, 0))
    lugs = []
    for s in (-1, 1):
        lg = _box(xb0, xb0 + P["lug_l"], s * ly - lw / 2, s * ly + lw / 2, zl0, zl1)
        lg = _fillet_try(lg, _par(lg, Axis.Y), [2.0, 1.2])
        lugs.append(lg)
    xa0, xa1 = xb0 + P["lug_l"], xb0 + P["lug_l"] + P["arm_t"]
    zg = D["grip_z"]
    rod_len = 2 * ly + lw
    bail = []
    for s in (-1, 1):
        arm = _box(xa0, xa1, s * ly - lw / 2, s * ly + lw / 2, zg, zp + 4)
        arm = _fillet_try(arm, _par(arm, Axis.X), [3.0, 2.0])
        bail.append(arm)
    rod = _ycyl(D["rod_x"], 0, zg, P["rod_d"] / 2, rod_len)
    rod = _fillet_try(rod, rod.edges(), [1.2, 0.8])
    bail.append(rod)
    add("lugs", "Bail pivot lugs (aluminium)", _union(lugs), C_ALU, "metal", 5, (200, 0, 0))
    add("bail", "Folding bail, arms and rod (aluminium)", _union(bail), C_ALU, "metal", 5, (235, 0, 0))
    pins = []
    for s in (-1, 1):
        pin = _xcyl(xa1 + 1.0, s * ly, zp, 3.6, 2.0)
        pins.append(_fillet_try(pin, _face_edges(pin, Axis.X, -1), [1.2, 0.8]))
    pins = _union(pins)
    add("pins", "Bail pivot pins (stainless)", pins, C_STEEL, "metal", 5, (235, 0, 0))
    grip = _ycyl(D["rod_x"], 0, zg, P["grip_od"] / 2, P["grip_l"])
    grip = _fillet_try(grip, grip.edges(), [2.5, 1.5])
    for k in range(7):
        yk = -P["grip_l"] / 2 + 9.0 + k * 7.0
        grip -= _ycyl(D["rod_x"], yk, zg, P["grip_od"] / 2 + 1, 2.2) - _ycyl(D["rod_x"], yk, zg, P["grip_od"] / 2 - 0.8, 3)
    grip -= _ycyl(D["rod_x"], 0, zg, P["rod_d"] / 2, P["grip_l"] + 2)
    add("grip", "Bail grip sleeve (silicone, ribbed)", grip, C_RUBBER, "rubber", 5, (235, 0, 0))

    # keyed nose: aluminium tab at the grade position, rounded leading edges
    ky = P["key_y"][grade]
    key = _box(D["x_min"], xe0, ky - P["key_w"] / 2, ky + P["key_w"] / 2, z0 + P["key_z"], z0 + P["key_z"] + P["key_h"])
    key = _fillet_try(key, [e for e in _face_edges(key, Axis.X, 0)], [2.0, 1.2])
    add("key", f"Keyed nose tab ({grade} position)", key, C_ALU, "metal", 5, (-190, 0, 0))

    # 6 label band and sight window (label and window footprints as model.py)
    lx1 = xt1 - 14.0
    lx0 = lx1 - P["label_l"]
    wx, wy, wr = lx1 - 18.0, 30.0, P["window_d"] / 2
    zl = z1 + P["label_t"]
    lab = _box(lx0, lx1, y0 + 16, y1 - 16, z1, zl)
    lab = _fillet_try(lab, _par(lab, Axis.Z), [3.0, 2.0])
    lab -= Pos(wx, wy, z1) * Cylinder(wr, 4)
    add("label", "Grade label (polyester)", lab, C_LABEL, "paper", 6, (0, 0, 40))
    blk = _box(lx0 + 3, wx - wr - 4, 8, y1 - 19, zl, zl + 0.15)
    blk = _fillet_try(blk, _par(blk, Axis.Z), [2.0, 1.0])
    add("gradeblk", f"Label grade block ({grade})", blk, col, "paper", 6, (0, 0, 40))
    bcx = (lx0 + 3 + wx - wr - 4) / 2
    txt = _text_top(grade, 14.0, bcx, 30.5, zl + 0.15, 0.15)
    txt += _text_top(gname.split(" ", 2)[0] + " " + gname.split(" ", 2)[1], 4.2, bcx, 14.5, zl + 0.15, 0.15)
    add("gradetxt", "Label grade lettering", txt, "#FFFFFF", "paper", 6, (0, 0, 40))
    ink = _text_top("ThermaCart", 9.0, lx0 + 4, -6.0, zl, 0.15, (Align.MIN, Align.CENTER))
    ink += _text_top(f"TC-L  {gname.split(' ', 2)[2]}", 4.0, lx0 + 4, -17.0, zl, 0.15, (Align.MIN, Align.CENTER))
    ink += _text_top("PCM sealed for life  |  carry by the bail", 3.2, lx0 + 4, -25.0, zl, 0.15, (Align.MIN, Align.CENTER))
    for k, w in enumerate((56.0, 44.0, 50.0)):
        ink += _box(lx0 + 4, lx0 + 4 + w, -33.5 - 4.2 * k, -32.5 - 4.2 * k, zl, zl + 0.15)
    ink += _text_top("solid = charged", 3.0, wx, wy - wr - 4.5, zl, 0.15)
    add("ink", "Label print", ink, C_INK, "paper", 6, (0, 0, 40))
    acc = _box(lx0 + 4, lx1 - 4, -51.0, -48.0, zl, zl + 0.15)
    add("accent", "Label accent stripe", acc, C_ACCENT, "paper", 6, (0, 0, 40))
    bez = Pos(wx, wy, z1 + P["window_h"] / 2) * (Cylinder(wr, P["window_h"]) - Cylinder(wr - 3.5, P["window_h"] + 1))
    bez = _fillet_try(bez, _face_edges(bez, Axis.Z, -1), [0.8, 0.5])
    add("bezel", "Sight window bezel", bez, C_BEZEL, "plastic", 6, (0, 0, 62))
    lens = Pos(wx, wy, z1 + 1.2) * Cylinder(wr - 3.6, 1.4)
    lens = _fillet_try(lens, _face_edges(lens, Axis.Z, -1), [0.5, 0.3])
    add("lens", "Sight window lens (polycarbonate)", lens, C_LENS, "clear", 6, (0, 0, 62))
    vial = Pos(wx, wy, z1 + 0.25) * Cylinder(wr - 3.6, 0.5)
    add("vial", "Melt indicator vial (solid PCM, charged)", vial, C_VIAL, "plastic", 6, (0, 0, 52))

    # 2 PCM fill (internal), as model.py
    fill_h = D["in_h"] * P["fill_fraction"]
    xi0, xi1 = xt0 + D["plug_depth"], xt1 - D["plug_depth"]
    fill = _box(xi0 + 0.3, xi1 - 0.3, y0 + t + 0.3, y1 - t - 0.3, z0 + t + 0.3, z0 + t + fill_h)
    fill = _fillet_try(fill, _par(fill, Axis.X), [2.0, 1.0])
    add("fill", f"PCM fill, {grade} grade (solid, charged)", fill, tint, "plastic", 2, (0, 0, 175))
    return out


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # main cartridge, C5 grade, seated in its frame (positions as model.py)
    internal = {"fill", "plug_1", "plug_-1", "oring_1", "oring_-1", "vial"}
    for key, name, shape, color, mat, bom, ex in _cartridge(P, D, P["grade"]):
        add(name, shape, color, mat, bom, "internal" if key in internal else "shell", ex)

    # 7 adapter frame (accessory): model.py frame with softened bends, grade decal by the slot
    frame = m["frame"]
    ft = P["frame_t"]
    def bends(s, z):
        return [e for e in _par(s, Axis.X) if abs(e.center().Z - z) < 0.01 and e.length > 250]
    frame = _fillet_try(frame, bends(frame, 0.0), [ft * 1.5, ft])            # outer bend radius
    frame = _fillet_try(frame, bends(frame, ft), [ft / 2, ft / 3])           # inner bend radius
    frame = _fillet_try(frame, bends(frame, ft + P["frame_wall_h"]), [0.6, 0.4])
    add("Cabinet adapter frame (5052 aluminium)", frame, C_ALU, "metal", 7, "accessory", (0, 0, -120))
    ky = P["key_y"][P["grade"]]
    fx0 = D["fx0"]
    zs = D["z0"] + P["key_z"] + P["key_h"] + P["slot_clear"] + 5.0
    decal = _box(fx0 - 0.3, fx0, ky - 18, ky + 18, zs, zs + 9)
    add("Frame grade decal (C5)", decal, GRADE[P["grade"]][0], "paper", 7, "accessory", (0, 0, -120))
    dtxt = Pos(fx0 - 0.3, ky, zs + 4.5) * Rot(0, 0, -90) * extrude(
        Plane.XZ * Text("C5 ONLY", font_size=5.0, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=0.15)
    add("Frame grade decal lettering", dtxt, "#FFFFFF", "paper", 7, "accessory", (0, 0, -120))
    feet = _union([Pos(x, y, -0.6) * Cylinder(5.0, 1.2) for x in (D["fx0"] + 20, D["fx1"] - 20)
                   for y in (-D["frame_w"] / 2 + 14, D["frame_w"] / 2 - 14)])
    add("Frame rubber feet", feet, C_FKM, "rubber", 7, "accessory", (0, 0, -125))

    # context: bench top and the other grades as a lineup (merged by colour and material)
    bx0, bx1, by0, by1, bt = BENCH
    bench = _box(bx0, bx1, by0, by1, -1.2 - bt, -1.2)
    bench = _fillet_try(bench, _face_edges(bench, Axis.Z, -1), [2.0, 1.0])
    add("Bench top (laminate)", bench, C_BENCH, "plastic", None, "context", (0, 0, 0))
    for grade, dy in LINEUP:
        groups = {}
        for key, name, shape, color, mat, bom, ex in _cartridge(P, D, grade, dy=dy, dz=-P["frame_t"] - 1.2):
            if key in internal - {"vial"}:
                continue
            groups.setdefault((color, mat), []).append((name, shape))
        for (color, mat), items in groups.items():
            nm = items[0][0] if len(items) == 1 else f"{items[0][0]} and {len(items) - 1} more"
            add(f"Lineup {grade}: {nm}", Compound(children=[s for _, s in items]), color, mat, None, "context",
                (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:48s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
