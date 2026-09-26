"""ThermaCart parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    thermacart-assembly.step / .stl   one TC-L cartridge (C5 key) seated in its adapter frame
    tc-l-cartridge.step / .stl        the cartridge alone: shell, fins, caps, handle, key, label
    end-cap.step / .stl               one end cap (flange, O-ring gland spacer and plug)
    adapter-frame.step / .stl         the adapter frame with the C5 key slot

Axes: X along the cartridge (handle at +X, keyed nose at -X), Y across, Z up, units mm.
The frame floor top is at z = FLOOR_T and the bottom fins rest on it. Main dimensions and
interfaces only: stock tube and fin sections, cap stack, handle with thermal break, grade key
positions, sight window, frame and key slot. Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (TCT-CAL-001) and the drawing TCT-DWG-001
(cad/src/sheets.py).
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 shell: 6063-T52 rectangular tube 6 x 2 x 1/8 in, cut length
    "tube_w": 152.4, "tube_h": 50.8, "tube_t": 3.175, "tube_l": 280.0,
    # 1 fins: 6063 flat bar 1/4 x 1/16 in bonded on edge, top and bottom faces
    "fin_n": 9, "fin_h": 6.35, "fin_t": 1.59, "fin_edge": 10.0, "fin_inset": 8.0,
    "label_band": 95.0,                 # top fins cut back over this length at the handle end
    # 1 finish (TCT-DDR-002, O8): outer shell, fins and caps painted matte black with a
    #   high-temperature paint over etch primer, emissivity about 0.9; no geometry change
    "finish": "matte black high-temperature paint, emissivity about 0.9",
    # 3 end caps: flange outside the tube, O-ring gland spacer and plug inside it
    "flange_t": 3.175, "spacer_t": 3.0, "gland_depth": 2.5, "plug_t": 9.525, "plug_clear": 0.2,
    "oring_cord": 3.0, "cap_screws": 6, "screw": "M5 x 12 A2 countersunk",
    # 2 fill: fraction of the inner volume filled as liquid at the grade's fill temperature
    "fill_fraction": 0.90,
    # 4 fill port: G 3/4 hex plug in the handle-end cap, outboard of the bail
    "port_d": 26.4, "port_head": 10.0, "port_y": 60.0,
    # 5 handle: folding bail on two pivot lugs, lugs on phenolic thermal-break washers,
    #   16 mm rod with a silicone grip sleeve; shown stowed (hanging against the end face)
    "lug_w": 12.0, "lug_l": 10.0, "lug_h": 16.0, "lug_y": 36.0, "pivot_z": 46.0,
    "bail_arm": 38.0, "arm_t": 4.0, "break_t": 3.0, "rod_d": 16.0, "grip_od": 24.0, "grip_l": 60.0,
    # 5 keyed nose: tab position across the nose codes the grade (Y of the tab center)
    "key_l": 10.0, "key_w": 30.0, "key_h": 16.0, "key_z": 4.0,
    "key_y": {"C5": -43.0, "C25": 0.0, "H70": 43.0, "W0": -61.0},
    "grade": "C5",
    # 6 label band and sight window over a PCM vial
    "label_l": 74.0, "label_t": 0.6, "window_d": 22.0, "window_h": 2.0,
    # 7 adapter frame: bent 1.5 mm aluminium sheet, floor, two side walls, keyed end stop
    "frame_t": 1.5, "frame_clear": 2.5, "frame_wall_h": 30.0, "stop_h": 40.0,
    "stop_gap": 2.0, "slot_clear": 3.0, "frame_lead": 4.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    t = p["tube_t"]
    in_w, in_h = p["tube_w"] - 2 * t, p["tube_h"] - 2 * t
    plug_depth = p["spacer_t"] + p["plug_t"]
    in_l = p["tube_l"] - 2 * plug_depth
    floor_top = p["frame_t"]
    z0 = floor_top + p["fin_h"]                      # tube underside
    z1 = z0 + p["tube_h"]
    xt0, xt1 = -p["tube_l"] / 2, p["tube_l"] / 2
    xe0, xe1 = xt0 - p["flange_t"], xt1 + p["flange_t"]
    rod_x = xe1 + p["break_t"] + p["lug_l"] + p["arm_t"] / 2   # bail plane when stowed
    x_min = xe0 - p["key_l"]
    x_max = max(rod_x + p["grip_od"] / 2, xe1 + p["port_head"])
    fin_pitch = (p["tube_w"] - 2 * p["fin_edge"]) / (p["fin_n"] - 1)
    fin_len_bot = p["tube_l"] - 2 * p["fin_inset"]
    fin_len_top = fin_len_bot - (p["label_band"] - p["fin_inset"] + 1.0)
    frame_in_w = p["tube_w"] + 2 * p["frame_clear"]
    fx0 = x_min - p["stop_gap"] - p["frame_t"]
    fx1 = xe1 + p["frame_lead"]
    return {
        "in_w": in_w, "in_h": in_h, "in_l": in_l, "plug_depth": plug_depth,
        "v_inner_l": in_w * in_h * in_l / 1e6,
        "z0": z0, "z1": z1, "floor_top": floor_top,
        "xt0": xt0, "xt1": xt1, "xe0": xe0, "xe1": xe1, "rod_x": rod_x,
        "x_min": x_min, "x_max": x_max,
        "grip_z": z0 + p["pivot_z"] - p["bail_arm"],
        # finger gap between the end flange and the grip with the bail swung out level
        "finger_gap": p["break_t"] + p["lug_l"] + p["bail_arm"] - p["grip_od"] / 2,
        "overall_l": x_max - x_min, "overall_w": p["tube_w"],
        "overall_h": p["tube_h"] + 2 * p["fin_h"],
        "fin_pitch": fin_pitch, "fin_len_bot": fin_len_bot, "fin_len_top": fin_len_top,
        "frame_w": frame_in_w + 2 * p["frame_t"], "frame_in_w": frame_in_w,
        "fx0": fx0, "fx1": fx1, "frame_l": fx1 - fx0,
        # outer area of the tube (4 faces), both flange faces and all fin faces, m2
        "area_tube_m2": 2 * (p["tube_w"] + p["tube_h"]) * p["tube_l"] / 1e6,
        "area_fins_m2": p["fin_n"] * (fin_len_bot + fin_len_top) * 2 * p["fin_h"] / 1e6,
        "area_ends_m2": 2 * p["tube_w"] * p["tube_h"] / 1e6,
    }


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def build_parts(p=PARAMS):
    """Return the named solids of one cartridge in its frame."""
    from build123d import Cylinder, Pos, Rot
    D = derived(p)
    t, tw, th = p["tube_t"], p["tube_w"], p["tube_h"]
    y0, y1 = -tw / 2, tw / 2
    z0, z1 = D["z0"], D["z1"]
    xt0, xt1, xe0, xe1 = D["xt0"], D["xt1"], D["xe0"], D["xe1"]

    # 1 shell tube and fins
    tube = box(xt0, xt1, y0, y1, z0, z1) - box(xt0 - 1, xt1 + 1, y0 + t, y1 - t, z0 + t, z1 - t)
    fins = None
    for i in range(p["fin_n"]):
        y = y0 + p["fin_edge"] + i * D["fin_pitch"]
        yb, yt = y - p["fin_t"] / 2, y + p["fin_t"] / 2
        bot = box(xt0 + p["fin_inset"], xt1 - p["fin_inset"], yb, yt, z0 - p["fin_h"], z0)
        top = box(xt0 + p["fin_inset"], xt1 - p["label_band"] - 1.0, yb, yt, z1, z1 + p["fin_h"])
        fins = bot + top if fins is None else fins + bot + top
    shell = tube + fins

    # 2 PCM fill (level at the fill temperature, ullage at the top when lying flat)
    fill_h = D["in_h"] * p["fill_fraction"]
    xi0, xi1 = xt0 + D["plug_depth"], xt1 - D["plug_depth"]
    fill = box(xi0 + 0.3, xi1 - 0.3, y0 + t + 0.3, y1 - t - 0.3, z0 + t + 0.3, z0 + t + fill_h)

    # 3 end caps: flange (outside), gland spacer (O-ring sits round it), plug (inside)
    c = p["plug_clear"]
    g = p["gland_depth"]

    def end_cap(sign):
        xo = xt1 if sign > 0 else xt0
        s = 1 if sign > 0 else -1
        def span(a, b):
            lo, hi = sorted((xo + s * a, xo + s * b))
            return lo, hi
        fl = box(*span(0, p["flange_t"]), y0, y1, z0, z1)
        sp = box(*span(0, -p["spacer_t"]), y0 + t + g, y1 - t - g, z0 + t + g, z1 - t - g)
        pl = box(*span(-p["spacer_t"], -D["plug_depth"]), y0 + t + c, y1 - t - c, z0 + t + c, z1 - t - c)
        cap = fl + sp + pl
        if sign > 0:   # fill port bore through the handle-end cap
            cap = cap - Pos(xo, p["port_y"], (z0 + z1) / 2) * Rot(0, 90, 0) * Cylinder(p["port_d"] / 2 - 1.5, 60)
        return cap
    cap_h, cap_k = end_cap(+1), end_cap(-1)
    xa, xb = xt0 + p["spacer_t"] / 2, xt1 - p["spacer_t"] / 2
    rc = p["oring_cord"] / 2
    oring = None
    for x in (xa, xb):
        ring = (box(x - rc, x + rc, y0 + t, y1 - t, z0 + t, z1 - t)
                - box(x - rc - 1, x + rc + 1, y0 + t + g, y1 - t - g, z0 + t + g, z1 - t - g))
        oring = ring if oring is None else oring + ring
    # radial cap screws through the tube wall into the plugs, 3 top and 3 bottom per cap
    screws = None
    for x in (xt0 + p["spacer_t"] + p["plug_t"] / 2, xt1 - p["spacer_t"] - p["plug_t"] / 2):
        for yy in (-50.0, 0.0, 50.0):
            for zz, sg in ((z1, 1), (z0, -1)):
                h = Pos(x, yy + 8.25, zz + sg * 0.6) * Cylinder(4.5, 1.2)
                screws = h if screws is None else screws + h

    # 4 fill port plug (hex head outside the handle-end flange)
    port = Pos(xe1 + p["port_head"] / 2, p["port_y"], (z0 + z1) / 2) * Rot(0, 90, 0) * Cylinder(p["port_d"] / 2 + 2, p["port_head"])

    # 5 folding bail handle on thermal-break washers (stowed), keyed nose
    lw, ly = p["lug_w"], p["lug_y"]
    zp = z0 + p["pivot_z"]
    zl0, zl1 = zp - p["lug_h"] / 2, zp + p["lug_h"] / 2
    xb0 = xe1 + p["break_t"]
    brk = (box(xe1, xb0, -ly - lw / 2, -ly + lw / 2, zl0, zl1)
           + box(xe1, xb0, ly - lw / 2, ly + lw / 2, zl0, zl1))
    lugs = (box(xb0, xb0 + p["lug_l"], -ly - lw / 2, -ly + lw / 2, zl0, zl1)
            + box(xb0, xb0 + p["lug_l"], ly - lw / 2, ly + lw / 2, zl0, zl1))
    xa0, xa1 = xb0 + p["lug_l"], xb0 + p["lug_l"] + p["arm_t"]
    zg = D["grip_z"]
    arms = (box(xa0, xa1, -ly - lw / 2, -ly + lw / 2, zg, zp + 4)
            + box(xa0, xa1, ly - lw / 2, ly + lw / 2, zg, zp + 4))
    rod_len = 2 * ly + lw
    handle = lugs + arms + Pos(D["rod_x"], 0, zg) * Rot(90, 0, 0) * Cylinder(p["rod_d"] / 2, rod_len)
    grip = (Pos(D["rod_x"], 0, zg) * Rot(90, 0, 0) * Cylinder(p["grip_od"] / 2, p["grip_l"])
            - Pos(D["rod_x"], 0, zg) * Rot(90, 0, 0) * Cylinder(p["rod_d"] / 2, p["grip_l"] + 2))
    ky = p["key_y"][p["grade"]]
    key = box(D["x_min"], xe0, ky - p["key_w"] / 2, ky + p["key_w"] / 2, z0 + p["key_z"], z0 + p["key_z"] + p["key_h"])

    # 6 label band and sight window
    lx1 = xt1 - 14.0
    label = box(lx1 - p["label_l"], lx1, y0 + 16, y1 - 16, z1, z1 + p["label_t"])
    window = Pos(lx1 - 18.0, 30.0, z1 + p["window_h"] / 2) * Cylinder(p["window_d"] / 2, p["window_h"])
    indicator = label + window

    # 7 adapter frame: floor, side walls, end stop with the grade key slot
    ft = p["frame_t"]
    fx0, fx1 = D["fx0"], D["fx1"]
    wi = D["frame_in_w"] / 2
    floor = box(fx0, fx1, -wi - ft, wi + ft, 0, ft)
    walls = (box(fx0, fx1, -wi - ft, -wi, ft, ft + p["frame_wall_h"])
             + box(fx0, fx1, wi, wi + ft, ft, ft + p["frame_wall_h"]))
    stop = box(fx0, fx0 + ft, -wi - ft, wi + ft, ft, ft + p["stop_h"])
    sc = p["slot_clear"]
    slot = box(fx0 - 1, fx0 + ft + 1, ky - p["key_w"] / 2 - sc, ky + p["key_w"] / 2 + sc,
               z0 + p["key_z"] - sc, z0 + p["key_z"] + p["key_h"] + sc)
    frame = floor + walls + stop - slot

    return {"shell": shell, "tube": tube, "fins": fins, "fill": fill, "cap_handle_end": cap_h,
            "cap_key_end": cap_k, "orings": oring, "screws": screws, "port": port,
            "thermal_break": brk, "handle": handle, "grip": grip, "key": key,
            "indicator": indicator, "frame": frame}


def cartridge(p=PARAMS):
    from build123d import Compound
    m = build_parts(p)
    names = ["shell", "fill", "cap_handle_end", "cap_key_end", "orings", "screws", "port",
             "thermal_break", "handle", "grip", "key", "indicator"]
    return Compound(children=[m[n] for n in names])


def assembly(p=PARAMS):
    from build123d import Compound
    m = build_parts(p)
    return Compound(children=[cartridge(p), m["frame"]])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    m = build_parts()
    D = derived()
    items = {
        "thermacart-assembly": assembly(),
        "tc-l-cartridge": cartridge(),
        "end-cap": Compound(children=[m["cap_handle_end"]]),
        "adapter-frame": Compound(children=[m["frame"]]),
    }
    for name, c in items.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    print(f"cartridge overall {D['overall_l']:.1f} x {D['overall_w']:.1f} x {D['overall_h']:.1f} mm; "
          f"inner {D['in_w']:.2f} x {D['in_h']:.2f} x {D['in_l']:.1f} mm = {D['v_inner_l']:.3f} L; "
          f"frame {D['frame_l']:.1f} x {D['frame_w']:.1f} mm")
