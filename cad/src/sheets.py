"""ThermaCart general arrangement sheet TCT-DWG-001, Rev P4 (TRL 3, constructable design TCT-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/TCT-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is TCT-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DATE_P4 = "2026-10-01"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x9CA3AF, line_type=LineType.ISO_DASH, line_weight=line_weight / 3)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="ThermaCart", title="General arrangement, TC-L in frame", dwg_no="TCT-DWG-001", rev="P4",
              author="Amish Chadha", date=DATE_P4, scale=0.4, theme="technical",
              material="6063-T52 tube, 6061 caps, 5052 frame; FKM seals; matte black finish. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Dark finish and H70 handling rule added (TCT-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Constructable design (TCT-DDR-003)", DATE_P4, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zt = bb.max.Z
    yd = Z(zt) - 4
    L += [ext(X(D["x_min"]), Z(zt) - 1, X(D["x_min"]), yd - 1), ext(X(D["x_max"]), Z(zt) - 1, X(D["x_max"]), yd - 1)]
    L += dim_h(X(D["x_min"]), X(D["x_max"]), yd, f"{D['overall_l']:.1f} overall (GN 1/3: 325)")
    z_bot, z_top = D["floor_top"], D["floor_top"] + D["overall_h"]
    xv = X(bb.max.X) + 6
    L += [ext(X(D["xe1"]), Z(z_top), xv + 1, Z(z_top)), ext(X(D["xe1"]), Z(z_bot), xv + 1, Z(z_bot))]
    L += dim_v(xv, Z(z_top), Z(z_bot), f"{D['overall_h']:.1f}", side=3)
    L += leader(X(D["rod_x"]), Z(D["grip_z"]), X(bb.max.X) - 30, Z(-45), "FOLDING BAIL, STOWED")
    L += leader(X(D["x_min"] + 3), Z(D["z0"] + P["key_z"] + 8), X(bb.min.X) - 6, Z(D["z0"]) + 14, "GRADE KEY", "end")
    L += leader(X(D["fx0"] + 20), Z(0.7), X(D["fx0"] + 40), Z(-45), "ADAPTER FRAME, KEYED STOP")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    yt1 = Yt(bb.max.Y) - 13
    L += [ext(Xt(D["xt0"]), Yt(P["tube_w"] / 2) - 1, Xt(D["xt0"]), yt1 - 1), ext(Xt(D["xt1"]), Yt(P["tube_w"] / 2) - 1, Xt(D["xt1"]), yt1 - 1)]
    L += dim_h(Xt(D["xt0"]), Xt(D["xt1"]), yt1, f"{P['tube_l']:.0f} tube")
    yt2 = yt1 - 7
    L += [ext(Xt(D["fx0"]), Yt(bb.max.Y) - 1, Xt(D["fx0"]), yt2 - 1), ext(Xt(D["fx1"]), Yt(bb.max.Y) - 1, Xt(D["fx1"]), yt2 - 1)]
    L += dim_h(Xt(D["fx0"]), Xt(D["fx1"]), yt2, f"{D['frame_l']:.1f} frame")
    xl = Xt(bb.min.X) - 13
    L += [ext(Xt(D["xt0"]), Yt(P["tube_w"] / 2), xl - 1, Yt(P["tube_w"] / 2)),
          ext(Xt(D["xt0"]), Yt(-P["tube_w"] / 2), xl - 1, Yt(-P["tube_w"] / 2))]
    L += dim_v(xl, Yt(P["tube_w"] / 2), Yt(-P["tube_w"] / 2), f"{P['tube_w']:.1f}")
    xl2 = xl - 10
    L += dim_v(xl2, Yt(D["frame_w"] / 2), Yt(-D["frame_w"] / 2), f"{D['frame_w']:.1f} frame")
    L += leader(Xt(D["xt1"] - 32), Yt(30), Xt(bb.max.X) + 6, Yt(10), "MELT INDICATOR")
    L += leader(Xt(D["xe1"] + 4), Yt(P["port_y"]), Xt(bb.max.X) + 6, Yt(P["port_y"]), "G 1/2 FILL PORT")
    L += leader(Xt(0), Yt(-P["tube_w"] / 2 + 10), Xt(bb.max.X) + 6, Yt(-40), "FINS, 9 TOP AND 9 BOTTOM")

    # right view (from +X): looking along -X, +Y to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L.append(_t(Yr(0), Zr(bb.max.Z) - 4, "HANDLE END", 2.0, 600, MUTED, "middle"))

    s._layers += L
    s.add_svg(views["iso"], 276, 36, 140, 66, label="Isometric view", sublabel="Not to scale")
    ky = P["key_y"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Shell 6 x 2 x 1/8 in tube, {P['tube_l']:.0f} long; inner {D['in_w']:.1f} x {D['in_h']:.1f} x {D['in_l']:.1f}",
        f"Inner volume {D['v_inner_l']:.3f} L; filled to {P['fill_fraction'] * 100:.0f} % as liquid at the grade limit",
        f"Fins 9 top, 9 bottom, {P['fin_h']:.2f} x {P['fin_t']:.2f} on {D['fin_pitch']:.1f} pitch",
        f"Caps: {P['flange_t']:.3f} flange, {P['spacer_t']:.0f} spacer, {P['plug_t']:.3f} plug, bonded; FKM {P['oring_cord']:g} cord",
        "Six radial M5 button-head screws per cap on bonded seals; G 1/2 fill port",
        f"Bail: 20 x 20 x 3 angles on {P['break_t']:.0f} phenolic washers; finger gap {D['finger_gap']:.0f} raised",
        "Key tab 30 wide, 16 high, 2 x M4; centre Y: " + ", ".join(f"{g} {v:+.0f}" for g, v in ky.items()),
        f"Frame 1.5 sheet, {D['frame_l']:.0f} x {D['frame_w']:.0f}; key passes the stop slot (key + {P['slot_clear']:.0f})",
        "Finish: shell, fins and caps etch-primed, matte black high-temp paint (e about 0.9)",
        "H70 label rule: from an oven use oven gloves or wait 12 min; pad charging preferred",
        "Sized in TCT-CAL-001; shown: C5 key and C5 frame",
        "Third-angle; front view from -Y; handle end at +X",
    ], x=276, y=120, width=140)
    out = s.save(ROOT / "cad" / "drawings" / "TCT-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}" if k < 1 else f"wrote {out} at scale {k:g}:1")


if __name__ == "__main__":
    main()
