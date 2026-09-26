"""ThermaCart concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the cartridge and frame parts from cad/src/model.py (PARAMS), adds a table top and a
25 L cooler (grey, no BOM number) as scale context, and renders the media set with
.kit/concept.py. Parts are colored and numbered to match bom/bom.csv. Figures on the sheet
and in the flow diagram come from docs/04-calcs/sizing.py (TCT-CAL-001). Not for fabrication.

Shown: one TC-L cartridge in the cold-chain grade (C5) in its adapter frame, bail stowed, with
the matte black finish decided in TCT-DDR-002 (O8).
Axes: X along the cartridge (handle at +X, keyed nose at -X), Y across, Z up. Units mm.
The cartridge sits near the origin, so the kit's cutaway (cut at the mean Y of the parts)
passes through the fill, the caps and the gland.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


m = build_parts()
parts = [
    Part("Cartridge shell, finned aluminium tube, matte black", m["shell"], "#2F343B", 1, (0, 0, 0)),
    Part("PCM fill, C5 grade (5 °C)", m["fill"], "#60A5FA", 2, (0, 0, 120)),
    Part("End caps with O-ring seals (2)", m["cap_handle_end"] + m["orings"], "#6B7280", 3, (150, 0, 0)),
    Part("End cap, keyed end", m["cap_key_end"], "#6B7280", None, (-150, 0, 0)),
    Part("Fill port plug and seal", m["port"], "#D4A017", 4, (230, 0, 110)),
    Part("Handle (folding bail) and keyed nose", m["handle"] + m["grip"] + m["thermal_break"], "#B8BEC6", 5, (260, 0, 0)),
    Part("Keyed nose", m["key"], "#B8BEC6", None, (-200, 0, 0)),
    Part("Grade label and melt indicator", m["indicator"], "#0F766E", 6, (0, 0, 210)),
    Part("Cabinet adapter frame", m["frame"], "#D1D5DB", 7, (0, 0, -130)),
    Part("Cap screws", m["screws"], "#1F2937", 8, (0, -230, 60)),
]

# Context for scale: a table top and a 25 L picnic cooler behind the cartridge
table = box(-260, 330, -170, 330, -30, 0)
cooler = box(-120, 240, 110, 320, 0, 334) + box(-116, 236, 114, 316, 334, 350)
context = [Part("Table top", table, "#C8CDD3"), Part("25 L cooler", cooler, "#9CA3AF")]

render_all(
    parts, project="ThermaCart", title="TC-L cartridge concept", dwg_no="TCT-DWG-010",
    date="2026-09-25",
    key_figures=["TC-L: 323 x 152 x 64 mm, fits a GN 1/3 slot",
                 "1.10 to 1.18 kg of PCM in 1.66 L (TCT-CAL-001)",
                 "Usable: C5 65 Wh, C25 61 Wh, H70 73 Wh (CAL)",
                 "2.9 to 3.0 kg filled; PCM 38 to 40 % of mass",
                 "Keyed nose: frames accept only their grade",
                 "Matte black finish; $76 per cartridge, $16 per frame"],
    scale_figure=False, context=context,
    flow={"title": "energy per charge cycle, one TC-L H70 on a 60 W pad (TCT-CAL-001 estimates)",
          "unit": "Wh",
          "stages": [("Pad input", 162), ("Stored, 25 to 80 °C", 130),
                     ("Released above 63 °C", 88), ("Insulated GN carrier", "63 °C+ for about 13.6 h")],
          "losses": [(0, "Pad loss (est.)", 32),
                     (1, "Below 63 °C (est.)", 42)]},
)
