"""ThermaCart concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Shown: one large cartridge (TC-L) in the cold-chain grade (C5), lying flat in its
cabinet adapter frame. Axes: X along the cartridge (handle at +X, keyed nose at -X),
Y across, Z up. Units mm.

The body is a 152.4 x 50.8 x 3.18 mm (6 x 2 x 1/8 in) aluminium rectangular tube, 270 mm
long, closed by two O-ring-sealed end caps. The finished cartridge, handle included, fits
the 325 x 176 mm footprint of a GN 1/3 gastronorm slot. Proposed, awaiting Amish.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# Body tube
TL, TW, TH, T = 270.0, 152.4, 50.8, 3.18
X0, X1 = -TL / 2, TL / 2
Y0, Y1 = -TW / 2, TW / 2
Z0 = 6.0                       # bottom fins (5 mm) rest on the frame floor at z = 1
Z1 = Z0 + TH
FIN_H, FIN_T, FIN_N = 5.0, 1.5, 9
CAP = 12.0                     # end cap thickness

# 1 Shell: tube with bonded fin strips on the bottom face and on the top face
#   (top fins leave a band free at the +X end for the label and indicator)
shell = box(X0, X1, Y0, Y1, Z0, Z1) - box(X0 - 1, X1 + 1, Y0 + T, Y1 - T, Z0 + T, Z1 - T)
pitch = (TW - 20) / (FIN_N - 1)
for i in range(FIN_N):
    y = Y0 + 10 + i * pitch
    shell = shell + box(X0 + 8, X1 - 8, y - FIN_T / 2, y + FIN_T / 2, Z1, Z1 + FIN_H)       # top
    shell = shell + box(X0 + 8, X1 - 8, y - FIN_T / 2, y + FIN_T / 2, Z0 - FIN_H, Z0)  # bottom, rests on the frame floor
# free band for the label on the top face: cut the top fins back
shell = shell - box(X1 - 95, X1 - 7, Y0 - 1, Y1 + 1, Z1 + 0.01, Z1 + FIN_H + 1)

# 2 PCM fill: about 90 % of the inner volume, ullage at the top
inner_h = TH - 2 * T
fill = box(X0 + 10.5, X1 - 10.5, Y0 + T + 0.5, Y1 - T - 0.5, Z0 + T + 0.5, Z0 + T + 0.9 * inner_h)

# 3 End caps with O-ring seals (plug into the tube, flange outside)
def end_cap(sign):
    xo = X1 if sign > 0 else X0
    flange = box(xo if sign > 0 else xo - CAP / 2, xo + CAP / 2 if sign > 0 else xo, Y0, Y1, Z0, Z1)
    plug = box(xo - 10 if sign > 0 else xo, xo if sign > 0 else xo + 10,
               Y0 + T + 0.2, Y1 - T - 0.2, Z0 + T + 0.2, Z1 - T - 0.2)
    return flange + plug
XE1, XE0 = X1 + CAP / 2, X0 - CAP / 2          # outer faces of the caps

# 4 Fill port plug and seal (G 3/4 class), in the +X cap between the handle posts
port = Pos(XE1 + 5, 20, Z0 + TH / 2) * Rot(0, 90, 0) * Cylinder(12, 10)

# 5 Handle (+X) and keyed nose (-X): the nose tab position codes the grade
handle = (box(XE1, XE1 + 22, -58, -46, Z0 + 14, Z0 + 32) + box(XE1, XE1 + 22, 46, 58, Z0 + 14, Z0 + 32)
          + Pos(XE1 + 22, 0, Z0 + 23) * Rot(90, 0, 0) * Cylinder(8, 116))
key = box(XE0 - 10, XE0, -58, -28, Z0 + 4, Z0 + 20)       # C5 key position: left of centre

# 6 Grade label and melt indicator (sight window onto a PCM vial)
label = box(X1 - 88, X1 - 14, -60, 60, Z1, Z1 + 1.2)
window = Pos(X1 - 32, 30, Z1 + 1.2) * Cylinder(11, 1.6)
indicator = label + window

# 7 Cabinet adapter frame: floor plate, two side rails, keyed stop at -X
FX0, FX1 = XE0 - 24, XE1 + 4
frame = (box(FX0, FX1, Y0 - 10, Y1 + 10, -4, 1)
         + box(FX0, FX1, Y0 - 10, Y0 - 4, 1, Z0 + 24) + box(FX0, FX1, Y1 + 4, Y1 + 10, 1, Z0 + 24)
         + box(FX0, XE0 - 12, Y0 - 10, Y1 + 10, 1, Z0 + 30) - box(FX0 + 6, XE0 - 11, -60, -26, Z0 + 2, Z0 + 22))
frame = frame + box(X0 + 4, X1 - 4, Y0 - 4, Y0, 1, Z0) + box(X0 + 4, X1 - 4, Y1, Y1 + 4, 1, Z0)

cap_p, cap_n = end_cap(+1), end_cap(-1)
parts = [
    Part("Cartridge shell, finned aluminium tube", shell, "#A8B0B8", 1, (0, 0, 0)),
    Part("PCM fill, C5 grade (5 °C)", fill, "#60A5FA", 2, (0, 0, 120)),
    Part("End caps with O-ring seals (2)", cap_p, "#6B7280", 3, (130, 0, 0)),
    Part("End cap, keyed end", cap_n, "#6B7280", None, (-130, 0, 0)),
    Part("Fill port plug and seal", port, "#D4A017", 4, (110, 0, 150)),
    Part("Handle and keyed nose", handle, "#374151", 5, (240, 0, 0)),
    Part("Keyed nose", key, "#374151", None, (-150, 0, 0)),
    Part("Grade label and melt indicator", indicator, "#0F766E", 6, (0, 0, 210)),
    Part("Cabinet adapter frame", frame, "#D1D5DB", 7, (0, 0, -120)),
]

# Context for scale: a table top and a 25 L picnic cooler behind the cartridge
table = box(-260, 330, -170, 330, -34, -4)
cooler = box(-120, 240, 110, 320, -4, 330) + box(-116, 236, 114, 316, 330, 346)
context = [Part("Table top", table, "#C8CDD3"), Part("25 L cooler", cooler, "#9CA3AF")]

render_all(
    parts, project="ThermaCart", title="TC-L cartridge concept", dwg_no="TCT-DWG-010",
    key_figures=["TC-L: 322 x 152 x 61 mm, fits a GN 1/3 slot",
                 "About 1.1 kg of PCM in 1.6 L (estimate)",
                 "Usable: C5 55 Wh, C25 61 Wh, H70 67 Wh (est.)",
                 "About 2.6 kg filled (estimate)",
                 "Keyed nose: frames accept only their grade",
                 "About $49 per cartridge, $15 per frame (indicative)"],
    scale_figure=False, context=context,
    flow={"title": "energy per charge cycle, one TC-L H70 cartridge for hot holding (all values are estimates)",
          "unit": "Wh",
          "stages": [("Charge input", 150), ("Stored, 25 to 75 °C", 120),
                     ("Released above 63 °C", 70), ("Insulated food box", "63 °C+ for about 6 h")],
          "losses": [(0, "Charger loss (est.)", 30),
                     (1, "Below 63 °C (est.)", 50)]},
)
