"""ThermaCart product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders: a TC-L cartridge in the cold-chain grade (C5) seated
in its adapter frame. Every solid comes from model.build_components() (the constructable design,
TCT-DDR-003, with the frame lip and raised grip of TCT-DEC-001 item 1), coloured by finish: the
finned tube, flanges and indicator guards carry the matte black finish (TCT-DDR-002, O8); the 18 mm
grade colour band is masked and painted round the nose end (TCT-DEC-001 item 7); the side marking
"ThermaCart, TC-L C5" is painted on the front face (item 8); the notched polyester label carries the
grade block, wordmark, data lines and, for C5, the conditioning time (item 6); the clear melt
indicator tube shows the white (solid, charged) PCM between its guards; the G 1/2 fill port plug,
sealed radial and stack screws, bolted lug angles on phenolic washers, folding bail with silicone
grip, and the aluminium key tab at the grade position. Inside: the PCM fill, the gland spacer and
plug of each cap and the FKM O-rings. The adapter frame has bend radii, the 4 mm lip at its open
end and the "C5 ONLY" decal beside its key slot; it has no rubber feet (left to each host, item 9).
Context: a compact bench top with the other two grades (C25 green, H70 red) lying behind the C5
cartridge as a lineup, each with its key tab at its own grade position.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the cartridge (handle at +X, keyed nose at -X), Y across, Z up, units mm;
the frame floor underside is at z = 0 and sits on the bench top. The bail is shown stowed, as in
model.py. The lineup cartridges lie directly on the bench. See docs/REVIEW.md, 2026-10-02.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Text,
                       extrude, fillet)
from model import PARAMS, derived, build_parts, build_components, grade_band

FONT = str(Path(__file__).resolve().parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

TITLE = "ThermaCart: swappable phase-change thermal storage cartridge"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); C5 cold-chain cartridge in "
             "its adapter frame, handle end at right, with the C25 and H70 grades lying behind it"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): finned shell, PCM fill, "
             "end caps with O-rings, screws, label and melt indicator, fill port plug, folding bail, key tab, "
             "adapter frame with its lip"},
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


# component key in model.py -> (appearance name, colour, material, BOM line, explode vector, internal)
_LOOK = {
    "tube": ("Cartridge shell tube (6063, matte black)", C_BLACK, "painted", 1, (0, 0, 0), False),
    "fins_bot": ("Bottom fins (9, matte black)", C_BLACK, "painted", 1, (0, 0, -30), False),
    "fins_top": ("Top fins (9, matte black)", C_BLACK, "painted", 1, (0, 0, 30), False),
    "flange_key": ("Key-end flange (matte black)", C_BLACK, "painted", 3, (-130, 0, 0), False),
    "spacer_key": ("Key-end gland spacer (6061)", C_ALU_DK, "metal", 3, (-100, 0, 0), True),
    "plug_key": ("Key-end plug (6061)", C_ALU_DK, "metal", 3, (-85, 0, 0), True),
    "oring_key": ("Key-end O-ring (FKM)", C_FKM, "rubber", 3, (-55, 0, 0), True),
    "stack_screws_key": ("Key-end stack screws (A2)", C_STEEL, "metal", 8, (-150, 0, 0), False),
    "flange_handle": ("Handle-end flange (matte black)", C_BLACK, "painted", 3, (130, 0, 0), False),
    "spacer_handle": ("Handle-end gland spacer (6061)", C_ALU_DK, "metal", 3, (100, 0, 0), True),
    "plug_handle": ("Handle-end plug (6061)", C_ALU_DK, "metal", 3, (85, 0, 0), True),
    "oring_handle": ("Handle-end O-ring (FKM)", C_FKM, "rubber", 3, (55, 0, 0), True),
    "stack_screws_handle": ("Handle-end stack screw (A2)", C_STEEL, "metal", 8, (150, 0, 0), False),
    "screws_key": ("Key-end radial screws on bonded seals (A2)", C_STEEL, "metal", 8, (0, 0, 45), False),
    "screws_handle": ("Handle-end radial screws on bonded seals (A2)", C_STEEL, "metal", 8, (0, 0, 45), False),
    "key": ("Key tab (aluminium)", C_ALU, "metal", 5, (-190, 0, 0), False),
    "key_screws": ("Key tab screws (A2)", C_STEEL, "metal", 8, (-215, 0, 0), False),
    "thermal_break": ("Thermal-break washers (phenolic)", C_PHENOLIC, "plastic", 5, (165, 0, 0), False),
    "lugs": ("Lug angles (aluminium)", C_ALU, "metal", 5, (190, 0, 0), False),
    "head_washers": ("Phenolic washers under the lug bolt heads", C_PHENOLIC, "plastic", 5, (205, 0, 0), False),
    "lug_bolts": ("Lug bolts (A2)", C_STEEL, "metal", 8, (220, 0, 0), False),
    "arms": ("Bail arms (aluminium)", C_ALU, "metal", 5, (240, 0, 0), False),
    "pins": ("Bail pivot pins and nuts (stainless)", C_STEEL, "metal", 5, (240, 0, 0), False),
    "rod": ("Bail rod (aluminium)", C_ALU, "metal", 5, (240, 0, 0), False),
    "rod_screws": ("Rod-end screws (A2)", C_STEEL, "metal", 8, (240, 0, 0), False),
    "grip": ("Bail grip sleeve (silicone)", C_RUBBER, "rubber", 5, (240, 0, 0), False),
    "port": ("Fill port plug G 1/2 with bonded seal (anodised aluminium)", C_ALU_DK, "metal", 4, (175, 0, 60), False),
    "fill": ("PCM fill (solid, charged)", None, "plastic", 2, (0, 0, 175), True),
    "label": ("Grade label (polyester, notched)", C_LABEL, "paper", 6, (0, 0, 40), False),
    "indicator": ("Melt indicator tube (solid PCM, charged)", C_VIAL, "plastic", 6, (0, 0, 62), False),
    "guards": ("Indicator guards (fin bar, matte black)", C_BLACK, "painted", 6, (0, 0, 62), False),
}


def _cartridge(P, D, grade, dy=0.0, dz=0.0):
    """Appearance parts of one cartridge as tuples (key, name, shape, color, material, bom, explode).
    Geometry is the constructable design from model.build_components(); the grade band, side
    marking and label print are added on top as thin skins."""
    tw = P["tube_w"]
    y0, y1 = -tw / 2, tw / 2
    z1 = D["z1"]
    xt1 = D["xt1"]
    col, tint, gname = GRADE[grade]
    C = build_components(P, grade)
    out = []

    def add(key, name, shape, color, material, bom, explode):
        out.append((key, name, Pos(0, dy, dz) * shape, color, material, bom, explode))

    for k, (name, color, mat, bom, ex, _inner) in _LOOK.items():
        nm = name if k != "fill" else f"PCM fill, {grade} grade (solid, charged)"
        add(k, nm, C[k].shape, color or tint, mat, bom, ex)

    # grade colour band (TCT-DEC-001 item 7): 18 mm, masked and painted round the nose end
    add("band", f"Grade colour band ({grade}, painted, 18 mm)", grade_band(P, grade), col, "painted", 1, (0, 0, 0))

    # painted side marking on the front face (TCT-DEC-001 item 8)
    mark = _text_front("ThermaCart", 10.0, 40.0, y0, D["z0"] + 33.0, 0.25)
    mark += _text_front(f"TC-L  {grade}", 5.5, 40.0, y0, D["z0"] + 21.0, 0.25)
    add("mark", "Side marking (painted)", mark, "#E7E8EA", "painted", 6, (0, -40, 0))

    # label print on the notched label (footprint as model.py: x lx1 - label_l to lx1)
    lx1 = xt1 - 15.0
    lx0 = lx1 - P["label_l"]
    ix0 = xt1 - P["ind_x1"] - P["ind_l"]
    zl = z1 + P["label_t"]
    bx1 = ix0 - 8.0
    blk = _box(lx0 + 3, bx1, 8, y1 - 19, zl, zl + 0.15)
    blk = _fillet_try(blk, _par(blk, Axis.Z), [2.0, 1.0])
    add("gradeblk", f"Label grade block ({grade})", blk, col, "paper", 6, (0, 0, 40))
    bcx = (lx0 + 3 + bx1) / 2
    txt = _text_top(grade, 12.0, bcx, 36.0, zl + 0.15, 0.15)
    txt += _text_top(gname.split(" ", 1)[0], 4.2, bcx, 20.0, zl + 0.15, 0.15)
    add("gradetxt", "Label grade lettering", txt, "#FFFFFF", "paper", 6, (0, 0, 40))
    ink = _text_top("ThermaCart", 9.0, lx0 + 4, -6.0, zl, 0.15, (Align.MIN, Align.CENTER))
    ink += _text_top(f"TC-L  {gname.split(' ', 2)[2]}", 4.0, lx0 + 4, -17.0, zl, 0.15, (Align.MIN, Align.CENTER))
    rule = "Freezer, then condition 4.2 h" if grade == "C5" else "PCM sealed for life"
    ink += _text_top(rule + "  |  carry by the bail", 3.2, lx0 + 4, -25.0, zl, 0.15, (Align.MIN, Align.CENTER))
    for k, w in enumerate((56.0, 44.0, 50.0)):
        ink += _box(lx0 + 4, lx0 + 4 + w, -33.5 - 4.2 * k, -32.5 - 4.2 * k, zl, zl + 0.15)
    ink += _text_top("solid = charged", 3.0, ix0 + P["ind_l"] / 2, 12.0, zl, 0.15)
    add("ink", "Label print", ink, C_INK, "paper", 6, (0, 0, 40))
    acc = _box(lx0 + 4, lx1 - 4, -51.0, -48.0, zl, zl + 0.15)
    add("accent", "Label accent stripe", acc, C_ACCENT, "paper", 6, (0, 0, 40))
    return out


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # main cartridge, C5 grade, seated in its frame (positions as model.py)
    internal = {k for k, v in _LOOK.items() if v[5]}
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
    zs = D["z0"] + P["key_z"] + P["key_h"] + P["slot_clear"] + 1.5   # between the slot and the stop's top edge
    decal = _box(fx0 - 0.3, fx0, ky - 18, ky + 18, zs, zs + 8)
    add("Frame grade decal (C5)", decal, GRADE[P["grade"]][0], "paper", 7, "accessory", (0, 0, -120))
    dtxt = Pos(fx0 - 0.3, ky, zs + 4.0) * Rot(0, 0, -90) * extrude(
        Plane.XZ * Text("C5 ONLY", font_size=4.5, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=0.15)
    add("Frame grade decal lettering", dtxt, "#FFFFFF", "paper", 7, "accessory", (0, 0, -120))
    # no rubber feet: they are left to each host (TCT-DEC-001 item 9)

    # context: bench top and the other grades as a lineup (merged by colour and material)
    bx0, bx1, by0, by1, bt = BENCH
    bench = _box(bx0, bx1, by0, by1, -bt, 0.0)
    bench = _fillet_try(bench, _face_edges(bench, Axis.Z, -1), [2.0, 1.0])
    add("Bench top (laminate)", bench, C_BENCH, "plastic", None, "context", (0, 0, 0))
    for grade, dy in LINEUP:
        groups = {}
        for key, name, shape, color, mat, bom, ex in _cartridge(P, D, grade, dy=dy, dz=-P["frame_t"]):
            if key in internal:
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
