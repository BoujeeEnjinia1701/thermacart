"""ThermaCart prototype build plan pictures (TCT-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps ...]
With no argument it draws everything. A single picture can be drawn with, for example,
`python cad/src/build_plan_media.py joints 3` or `sheets 105` (one picture per process keeps memory low).
Every picture is drawn from cad/src/model.py (build_components), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/TCT-DWG-101 to 110        making sketches for the made components
    docs/05-build-plan/cap-holes.png       hole layout on the outer face of each cap stack
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, fuse, box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
z0, z1, zm = D["z0"], D["z1"], D["zm"]
xt0, xt1, xe0, xe1 = D["xt0"], D["xt1"], D["xe0"], D["xe1"]

COL = {"tube": "#4B5563", "fins": "#0891B2", "flange": "#2563EB", "spacer": "#F59E0B", "plug": "#0D9488",
       "oring": "#DC2626", "screw": "#111827", "seal": "#7C2D12", "key": "#7C3AED", "lug": "#0369A1",
       "break": "#92400E", "arm": "#B45309", "pin": "#374151", "rod": "#64748B", "grip": "#1F2937",
       "port": "#D4A017", "fill": "#60A5FA", "label": "#93C5FD", "ind": "#38BDF8", "guard": "#475569",
       "frame": "#A8A29E", "rivet": "#57534E"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, za, zb):
    return sh & box(x0, x1, y0, y1, za, zb)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "tube": part("Shell tube", C["tube"].shape, COL["tube"]),
        "fins": part("Fins (9 bottom, 9 top)", S("fins_bot", "fins_top"), COL["fins"]),
        "cap_key": part("Key-end cap stack with its O-ring", S("flange_key", "spacer_key", "plug_key", "oring_key"), COL["flange"]),
        "key": part("Key tab and its screws", S("key", "key_screws"), COL["key"]),
        "screws": part("Radial screws with bonded seals (12)", S("screws_key", "screws_handle"), COL["screw"]),
        "cap_handle": part("Handle-end cap stack with its O-ring", S("flange_handle", "spacer_handle", "plug_handle", "oring_handle"), COL["plug"]),
        "lugs": part("Lug angles, washers and bolts", S("lugs", "thermal_break", "head_washers", "lug_bolts"), COL["lug"]),
        "bail": part("Bail: arms, pins, rod and grip", S("arms", "pins", "rod", "rod_screws", "grip"), COL["arm"]),
        "fill": part("PCM fill", C["fill"].shape, COL["fill"]),
        "port": part("Fill port plug and seal", C["port"].shape, COL["port"]),
        "ind": part("Label, melt indicator and guards", S("label", "indicator", "guards"), COL["ind"]),
        "frame": part("Adapter frame and rivets", S("frame", "rivets"), COL["frame"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"tube": (0, 0, 0), "fins": (0, 0, 0), "cap_key": (-110, 0, 0), "key": (-170, 0, 0),
           "screws": (0, -60, -250), "cap_handle": (110, 0, 0), "lugs": (165, 0, 0),
           "bail": (225, 0, 0), "fill": (0, 0, 170), "port": (150, 90, 70), "ind": (0, 0, 70),
           "frame": (0, 0, -120)}
    parts = []
    for k in off:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "ThermaCart prototype: every component, pulled apart",
                       subtitle="Numbered in build order. One C5 cartridge and its adapter frame, seen from the front right and above",
                       elev=24, azim=-55, size=(11, 7.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def _turn_cap(sh, x_face):
    """Turn a cap stack so its outer face looks at the reader in the front view (-Y)."""
    from build123d import Pos, Rot
    return Rot(0, 0, -90 if x_face > 0 else 90) * Pos(-x_face, 0, -z0) * sh


def sheets(which=None):
    from build123d import Pos, Rot
    M = made()
    base = dict(project="ThermaCart", date=DATE)
    out = []
    cart = [M["tube"], M["fins"], M["cap_key"], M["cap_handle"]]

    def sheet(n, *a, **k):
        if which is None or str(n) == str(which):
            out.append(bv.component_sheet(*a, **k, **base))

    xs = xt1 - D["x_screw"][1]
    sheet(101, Part("Shell tube", C["tube"].shape, COL["tube"]), [M["fins"], M["cap_key"], M["cap_handle"]],
          dwg_no="TCT-DWG-101", title="ThermaCart shell tube: making sketch",
          material="6063-T52 rectangular tube 6 x 2 x 1/8 in (152.4 x 50.8 x 3.175 mm)",
          view_shape=Pos(0, 0, -z0) * C["tube"].shape, inset_view=(28, -50),
          notes=["Cut 280 mm long; square both ends to the side faces and file",
                 "  them flat. The cap flanges seat on these end faces.",
                 "File a 1 mm x 45 degree lead-in chamfer round the inside of",
                 "  each end, so the O-ring slides in without being cut.",
                 "Measure the bore at both ends (about 146.05 x 44.45 mm) and",
                 "  write it down: the cap plates are cut to it.",
                 f"Radial screw holes: twelve 5.5 mm, {xs:.2f} mm in from each end,",
                 "  through the top and the bottom wall, at 34.45, 84.45 and",
                 "  134.45 mm from the front face (between the fins).",
                 "  Drill them 4.2 mm first with the caps in place (see the caps).",
                 "Deburr every edge and hole inside and out; clean, etch-prime",
                 "  the outside (not the bore) before the fins are bonded.",
                 "Check: the bore is clean and round-cornered; ends square."])
    sheet(102, Part("Fin strips", S("fins_bot", "fins_top"), COL["fins"]), [M["tube"]],
          dwg_no="TCT-DWG-102", title="ThermaCart fins (make 9 long and 9 short): making sketch",
          material="6063 flat bar 6.35 x 1.59 mm (1/4 x 1/16 in)", inset_view=(30, -50),
          view_shape=fuse([box(0, D["fin_len_bot"], 0, P["fin_t"], 0, P["fin_h"]),
                           box(0, D["fin_len_top"], 0, P["fin_t"], 20, 20 + P["fin_h"])]),
          notes=[f"Cut nine bottom fins {D['fin_len_bot']:.0f} mm and nine top fins {D['fin_len_top']:.0f} mm long",
                 "  (two 3.66 m bars also give the two 40 mm indicator guards).",
                 "Deburr; keep the long edges straight (roll them on a flat plate).",
                 f"Each fin stands on edge, 6.35 mm tall, on {D['fin_pitch']:.2f} mm centres;",
                 "  the outer fins are 10 mm in from the side faces.",
                 "Bottom fins start 8 mm in from each tube end.",
                 "Top fins start 8 mm in from the key end and stop 96 mm",
                 "  short of the handle end, leaving the label band clear.",
                 "Bond with the 120 degree C epoxy: a thin bead under the edge and",
                 "  a fillet down each side. Hold them upright in a slotted comb",
                 "  (a wooden strip sawn at the fin pitch) while the epoxy cures.",
                 "Check: every fin upright, none touching a screw hole."])
    # cap stacks: turned so the outer face is seen in the front view
    sheet(103, Part("Handle-end cap stack", S("flange_handle", "spacer_handle", "plug_handle"), COL["plug"]),
          [M["tube"], M["lugs"], M["port"]], dwg_no="TCT-DWG-103",
          title="ThermaCart handle-end cap stack (flange, spacer, plug): making sketch",
          material="6061 plate 3.175, 3 and 9.525 mm; structural epoxy",
          view_shape=_turn_cap(S("flange_handle", "spacer_handle", "plug_handle"), xe1), inset_view=(18, 20),
          notes=["Three plates, bonded face to face with the epoxy, then drilled.",
                 "Flange 3.175 mm: 152.4 x 50.8, 4.8 mm corners (the tube's outside).",
                 "Spacer 3 mm: the measured bore less 4.2 mm each way",
                 "  (about 141.85 x 40.25), 3.7 mm corners. The O-ring goes round it.",
                 "Plug 9.525 mm: the bore less 0.4 mm (about 145.65 x 44.05), 2 mm",
                 "  corners. Centre spacer and plug on the flange; bond and clamp.",
                 "Seen from outside, handle end; sizes from the centre line, heights",
                 "  from the flange's bottom edge (layout picture in the plan):",
                 "  fill port G 1/2 at 56 toward the back, 25.4 up, tapped through;",
                 "  lug bolts M4 at 27 each side, 30 and 40 up; one M4 countersunk",
                 "  stack screw at 56 toward the front, 25.4 up. All M4 holes 4.5",
                 "  through flange and spacer, tapped 7.5 deep into the plug only.",
                 "Radial holes: tap M5 7.5 deep into the plug edges (with the tube).",
                 "Check: the stack slides into the tube without the O-ring."])
    sheet(104, Part("Key-end cap stack", S("flange_key", "spacer_key", "plug_key"), COL["flange"]),
          [M["tube"], M["key"]], dwg_no="TCT-DWG-104",
          title="ThermaCart key-end cap stack (flange, spacer, plug): making sketch",
          material="6061 plate 3.175, 3 and 9.525 mm; structural epoxy",
          view_shape=_turn_cap(S("flange_key", "spacer_key", "plug_key"), xe0), inset_view=(20, -140),
          notes=["Same three plates as the handle end, cut and bonded the same way.",
                 "Seen from outside, key end; sizes from the centre line, heights",
                 "  from the flange's bottom edge:",
                 "  two M4 countersunk stack screws at 56 each side, 25.4 up;",
                 "  two M4 key tab screws 7 each side of the key centre, 14 up.",
                 "  C5 key centre: 43 toward the front (C25 0, H70 43 toward the back).",
                 "  M4 holes: 4.5 through flange and spacer, tapped 7.5 deep in",
                 "  the plug, never through it (the plug's inner face is wet).",
                 "No fill port at this end.",
                 "Radial holes: with the stack in the tube (no O-ring yet), drill",
                 "  4.2 mm through each tube hole into the plug edge, 7.5 deep; take",
                 "  the stack out, tap M5, open the tube holes to 5.5 mm.",
                 "Prime and paint the flange's outer face only.",
                 "Check: flange sits flat on the tube end all round."])
    sheet(105, Part("Key tab", C["key"].shape, COL["key"]), [M["cap_key"], M["tube"], M["frame"]],
          dwg_no="TCT-DWG-105", title="ThermaCart key tab (C5 shown): making sketch",
          material="6061 flat bar 30 x 10 mm", inset_view=(25, -140),
          notes=["Cut 16 mm off 30 x 10 mm flat bar: 30 wide, 16 tall, 10 deep.",
                 "Two 4.5 mm holes through the 10 mm depth, 8 mm in from each end",
                 "  (14 mm apart), 10 mm up from the bottom face.",
                 "Counterbore both from the front face 8 mm across, 5 mm deep, so",
                 "  the M4 x 16 socket cap screw heads sit below the face.",
                 "Break the front edges by 1 mm so it finds the slot easily.",
                 "Fit: back face flat on the key-end flange, bottom 4 mm above the",
                 "  flange's bottom edge, centre at the grade position:",
                 "  C5 43 mm toward the front, C25 on the centre line,",
                 "  H70 43 mm toward the back.",
                 "Leave it bare aluminium; stamp the grade on its top face.",
                 "Check: 3 mm clear of the frame slot all round when seated."])
    lug = C["lugs"].shape & box(xe1, xe1 + 30, 0, 50, 0, 80)
    sheet(106, Part("Lug angle", lug, COL["lug"]), [M["cap_handle"], M["bail"], M["tube"]],
          dwg_no="TCT-DWG-106", title="ThermaCart lug angle (make 2, a left and a right): making sketch",
          material="6063 equal angle 20 x 20 x 3 mm", inset_view=(18, 25),
          view_shape=Pos(-xe1, -40, -z0) * lug,
          notes=["Cut two 32 mm lengths of 20 x 20 x 3 angle; deburr.",
                 "Flat leg (goes on the cap): two 6.5 mm holes 13 mm from the outside",
                 "  of the upright leg, 8 and 18 mm up from the bottom end. The",
                 "  bolts pass with 1.25 mm air all round: the bolt must not touch.",
                 "Upright leg: one 5.2 mm pivot hole 12 mm out from the back of",
                 "  the flat leg, 24 mm up from the bottom end.",
                 "Left and right are mirror images: drill them as a pair.",
                 "Fit: flat leg on two phenolic washers (9 x 4.5 x 3 mm) per bolt,",
                 "  3 mm off the flange; bottom end 22 mm above the flange's",
                 "  bottom edge; upright legs outward, their outsides 40 mm each",
                 "  side of the centre line. M4 x 20 bolts with a 3 mm phenolic",
                 "  washer under each head, into the plug.",
                 "Check: no metal path from bolt to angle (meter: open circuit)."])
    arm = C["arms"].shape & box(0, 400, 0, 80, -50, 120)
    sheet(107, Part("Bail arm", arm, COL["arm"]), [M["lugs"], M["cap_handle"], M["tube"]],
          dwg_no="TCT-DWG-107", title="ThermaCart bail arm (make 2): making sketch",
          material="6060 flat bar 16 x 4 mm", inset_view=(18, 35),
          view_shape=Pos(-D["rod_x"], 0, -D["grip_z"]) * arm,
          notes=["Cut two 54 mm lengths of 16 x 4 mm flat bar.",
                 "Round both ends to an 8 mm radius (file to a scribed circle).",
                 "Two holes on the centre line, 8 mm from each end (38 mm apart):",
                 "  5.2 mm at the top (pivot), 6.5 mm at the bottom (rod end).",
                 "Drill the two arms clamped together so the holes match.",
                 "Fit: the arm lies flat on the outside of the angle's upright leg;",
                 "  a 5 mm stainless pin goes through both, head inside the angle,",
                 "  nyloc nut outside the arm, snug so the arm still swings.",
                 "The rod end butts on the arm's inside face; one M6 x 12",
                 "  button-head screw through the arm into the rod.",
                 "Stowed, the arm hangs straight down; raised, the grip is",
                 f"  {D['finger_gap']:.0f} mm from the end face (room for fingers).",
                 "Check: hole centres 38 mm apart, within 0.5 mm."])
    rod = C["rod"].shape
    sheet(108, Part("Bail rod", rod, COL["rod"]), [part("Arms", S("arms", "pins"), COL["arm"]), M["lugs"], M["cap_handle"]],
          dwg_no="TCT-DWG-108", title="ThermaCart bail rod: making sketch",
          material="6061 round bar 16 mm", inset_view=(18, 25),
          view_shape=Rot(0, 0, 90) * Pos(-D["rod_x"], 0, -D["grip_z"]) * rod,
          notes=["Cut 80 mm of 16 mm round bar; face both ends square.",
                 "Centre drill each end, drill 5 mm 14 deep and tap M6 12 deep",
                 "  (drill press with the bar upright in a V-block).",
                 "Break the edges 0.5 mm.",
                 "Slide the 60 mm silicone grip sleeve onto the middle (soapy",
                 "  water helps; let it dry).",
                 "Fit: between the two arms' inside faces, held by one M6 x 12",
                 "  button-head screw through each arm, with medium threadlocker.",
                 "Stowed, the rod hangs 8 mm above the tube's underside, 15 mm",
                 "  out from the end face; the grip clears the flange by 3 mm.",
                 "Leave the rod bare: the bail is not painted.",
                 "Check: 80 mm long, within 0.3 mm, so the arms are not",
                 "  pulled in or pushed out."])
    ind = S("indicator", "guards")
    sheet(109, Part("Melt indicator and guards", ind, COL["ind"]), [M["tube"], M["fins"], part("Label", C["label"].shape, COL["label"])],
          dwg_no="TCT-DWG-109", title="ThermaCart melt indicator and guards: making sketch",
          material="Clear polycarbonate tube 6 x 4 mm; fin bar 6.35 x 1.59 mm",
          view_shape=Pos(-(xt1 - 36), -P["ind_y"], -z1) * ind, inset_view=(45, -30),
          notes=["Indicator: cut 40 mm of clear polycarbonate tube, 6 mm outside,",
                 "  4 mm bore. Seal one end with a 3 mm plug of the epoxy; cure.",
                 "Warm the grade's PCM just above its melting point and fill the",
                 "  tube with a syringe, leaving a 2 mm bubble; seal the other end",
                 "  with 3 mm of epoxy. Solid PCM is white, liquid PCM is clear.",
                 "Guards: two 40 mm lengths of the fin bar.",
                 "Fit: bond the indicator to the painted top with the epoxy, along",
                 "  the cartridge, 30 mm toward the back from the centre line,",
                 "  between 16 and 56 mm from the handle end of the tube.",
                 "Bond a guard on edge 8 mm each side of it; the guards are as",
                 "  tall as the fins and take knocks.",
                 "The label is notched round them.",
                 "Check: no PCM weeps at the plugs when warmed by hand."])
    fr = S("frame", "rivets")
    sheet(110, Part("Adapter frame", fr, COL["frame"]), [M["tube"], M["fins"], M["cap_key"], M["key"]],
          dwg_no="TCT-DWG-110", title="ThermaCart adapter frame (C5 slot shown): making sketch",
          material="5052-H32 aluminium sheet 1.5 mm; 3.2 mm blind rivets",
          view_shape=Pos(-D["fx0"], 0, 0) * fr, inset_view=(30, -140),
          notes=[f"Floor {D['frame_l']:.0f} x {D['frame_w']:.1f} mm; side walls 30 mm; end stop 40 mm.",
                 "Mark one blank: floor in the middle, a wall on each long edge",
                 "  with a 12 mm tab at the stop end, and the stop on one short",
                 "  edge, 157.4 mm wide so it fits between the walls.",
                 "Cut the slot in the stop before bending: C5 36 x 22 mm, centred",
                 "  43 mm toward the front, 7.35 to 29.35 mm above the floor's top.",
                 "  (C25 on the centre line, H70 43 mm toward the back.)",
                 "Drill 3 mm relief holes where bend lines cross.",
                 "Bend the stop up 90 degrees, then the walls (inside radius 1.5),",
                 "  then fold each tab round the outside of the stop.",
                 "Drill 3.3 mm through tab and stop, 6 mm in from the wall, 8 and",
                 "  22 mm above the floor; rivet with heads inside the frame.",
                 "Check: inside width 157.4 mm; stop square to the floor."])
    return out


# ----------------------------------------------------------------- hole layout of the cap faces
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    fig = plt.figure(figsize=(12, 9.6), dpi=150)
    tw, th = P["tube_w"], P["tube_h"]
    ky = P["key_y"][P["grade"]]

    def face(ax, holes):
        ax.set_aspect("equal"); ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((-tw / 2 + 4.8, 4.8), tw - 9.6, th - 9.6, boxstyle="round,pad=4.8", fc="#F3F4F6", ec=INK, lw=1.2))
        sw, sh = D["spacer_w"], D["spacer_h"]
        ax.add_patch(FancyBboxPatch((-sw / 2 + 3.7, (th - sh) / 2 + 3.7), sw - 7.4, sh - 7.4, boxstyle="round,pad=3.7", fc="none", ec="#DC2626", lw=0.8, ls="--"))
        ax.plot([0, 0], [-3, th + 3], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
        for (x, z, d, name, dy, lx) in holes:
            ax.add_patch(plt.Circle((x, z), d / 2, fc="white", ec=INK, lw=1.0))
            ax.plot([x - d / 2 - 2, x + d / 2 + 2], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d / 2 - 2, z + d / 2 + 2], color=MUT, lw=0.4)
            if name:
                ax.text(lx if lx is not None else x, z + dy, name, ha="center", va="bottom" if dy > 0 else "top", fontsize=7.4,
                        color=INK, linespacing=1.15, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.92))
        ax.set_xlim(-tw / 2 - 4, tw / 2 + 4); ax.set_ylim(-16, th + 14)

    lr = lambda x: f"{abs(x):g} {'L' if x < 0 else 'R'}"  # noqa: E731
    # handle end, seen from outside (looking along -X): the back of the cartridge (+Y) is on the right
    hz = [(P["port_y"], 25.4, P["port_d"], f"fill port G 1/2\n{lr(P['port_y'])}, 25.4 up", -12.5, None)]
    for sx in (-1, 1):
        for bz in P["lug_bolt_z"]:
            x = sx * P["lug_bolt_y"]
            hz.append((x, bz, 4.5, f"lug bolt M4\n{lr(x)}, {bz:g} up", 5 if bz > 35 else -5, None))
    hz.append((-56.0, 25.4, 8.0, f"stack screw M4,\ncountersunk\n{lr(-56)}, 25.4 up", -6, None))
    ax1 = fig.add_axes([0.03, 0.52, 0.94, 0.36])
    face(ax1, hz)
    fig.text(0.03, 0.905, "Handle-end cap, seen from outside: front of the cartridge on the left, back on the right", fontsize=10.5, fontweight="bold", color=INK)
    # key end, seen from outside (looking along +X): the front of the cartridge (-Y) is on the right
    ks = [-(ky + s * P["key_screw_dy"]) for s in (-1, 1)]
    kz = [(-56.0, 25.4, 8.0, f"stack screw M4,\ncountersunk\n{lr(-56)}, 25.4 up", 6, None),
          (56.0, 25.4, 8.0, f"stack screw M4,\ncountersunk\n{lr(56)}, 25.4 up", 6, None),
          (ks[0], P["key_screw_z"], 4.5, "", -5, None),
          (ks[1], P["key_screw_z"], 4.5, f"key tab screws M4\n{lr(ks[0])} and {lr(ks[1])}, {P['key_screw_z']:g} up", -5, sum(ks) / 2)]
    ax2 = fig.add_axes([0.03, 0.07, 0.94, 0.36])
    face(ax2, kz)
    fig.text(0.03, 0.455, "Key-end cap (C5), seen from outside: back of the cartridge on the left, front on the right", fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.03, 0.975, "End cap stacks: hole positions on the outer face (mm)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.947, "Sideways from the centre line (L and R as you look at the face), heights from the flange's bottom edge. M4 holes are 4.5 mm through flange\n"
             "and spacer and tapped 7.5 mm deep into the plug, never through it. Dashed red: the spacer edge, where the O-ring sits; every hole stays inside it.",
             fontsize=8.5, color=MUT, va="top")
    fig.text(0.03, 0.012, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.012, "github.com/BoujeeEnjinia1701/thermacart", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "cap-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "cap-holes.png"


def joint_at(items, out, title, subtitle=None, elev=4, azim=90, size=(8, 6), dpi=160):
    """Like build_views.joint, but each part's leader ends at a given 3D point (on the cut face),
    so in a section every label lands on its own part. items: list of (Part, (x, y, z))."""
    import numpy as np
    items = [(p, a) for p, a in items if bv._has_volume(p.shape)]
    W, H = int(size[0] * dpi), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, _ = bv._raster([(p, p.color, p.alpha, (0, 0, 0)) for p, _ in items], elev, azim, W, H)
    fig, ax = bv._frame(size, dpi, title, subtitle)
    ax.imshow(img, interpolation="bilinear")
    bv._draw_labels(ax, proj, [np.asarray(a, float) for _, a in items], [p.name for p, _ in items], W, H)
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return out


# ----------------------------------------------------------------- joints
def joints(which=None):
    out = []

    def jt(n, parts, title, sub, **kw):
        if which is None or str(n) == str(which):
            out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", title, subtitle=sub, **kw))

    # 1 fin on the tube, cut across at mid length (drawn after ja is defined)
    t = P["tube_t"]
    xs = D["x_screw"][1]
    xf, xsp, xpl = xt1 + P["flange_t"] / 2, xt1 - P["spacer_t"] / 2, xt1 - P["spacer_t"] - P["plug_t"] / 2

    def ja(n, items, title, sub, **kw):
        if which is None or str(n) == str(which):
            out.append(joint_at(items, OUT / f"joint-{n:02d}.png", title, sub, **kw))
    b_ = (-4, 4, -76.5, -40, z0 - 7, z0 + 5)
    fy = -P["tube_w"] / 2 + P["fin_edge"] + D["fin_pitch"]
    ja(1, [(part("Tube wall (bottom)", win(C["tube"].shape, *b_), COL["tube"]), (4, -58, z0 + 1.6)),
           (part("Bottom fin, bonded on edge", win(C["fins_bot"].shape, *b_), COL["fins"]), (4, fy, z0 - 3.5))],
       "Joint 1: fins on the tube (cut across, front bottom corner)",
       "Each fin stands on its 1.59 mm edge; the epoxy runs under it and forms a fillet down both sides",
       elev=8, azim=-12, size=(8, 5.5))
    # 2 cap stack in the tube end, top half, cut through a radial screw
    yc = P["screw_y"][1]
    b_ = (118, 147, -30, yc, zm - 4, z1 + 6)
    ja(2, [(part("Tube wall", win(C["tube"].shape, *b_), COL["tube"]), (126, yc, z1 - 1.5)),
           (part("Radial screw on its bonded seal", win(C["screws_handle"].shape, *b_), COL["screw"]), (xs, yc, z1 + 2.5)),
           (part("O-ring in the corner gland", win(C["oring_handle"].shape, *b_), COL["oring"]), (xsp, yc, z1 - t - 1.0)),
           (part("Flange (on the tube end)", win(C["flange_handle"].shape, *b_), COL["flange"]), (xf, yc, zm + 4)),
           (part("Gland spacer", win(C["spacer_handle"].shape, *b_), COL["spacer"]), (xsp, yc, zm + 2)),
           (part("Plug", win(C["plug_handle"].shape, *b_), COL["plug"]), (xpl, yc, zm)),
           (part("PCM", win(C["fill"].shape, *b_), COL["fill"]), (123, yc, zm))],
       "Joint 2: cap stack in the tube end (handle end, top half, cut through a radial screw)",
       "Section seen from the back. The O-ring is squeezed between the spacer edge and the bore")
    # 3 radial screw close-up
    b_ = (125, 141, -2, yc, z1 - 14, z1 + 5)
    ja(3, [(part("Tube wall, 5.5 mm hole", win(C["tube"].shape, *b_), COL["tube"]), (127, yc, z1 - 1.5)),
           (part("M5 button-head screw, bonded seal", win(S("screws_handle"), *b_), COL["screw"]), (xs, yc, z1 + 2.5)),
           (part("O-ring", win(C["oring_handle"].shape, *b_), COL["oring"]), (xsp, yc, z1 - t - 1.0)),
           (part("Spacer", win(C["spacer_handle"].shape, *b_), COL["spacer"]), (xsp, yc, z1 - 10)),
           (part("Plug, tapped M5", win(C["plug_handle"].shape, *b_), COL["plug"]), (127.5, yc, z1 - 9))],
       "Joint 3: radial screw through the tube wall into the plug (cut open)",
       "The screw is on the PCM side of the O-ring, so the bonded seal under its head seals the hole")
    # 4 lug angle on its washers, cut through the lower bolt
    yb = P["lug_bolt_y"]
    zb = z0 + P["lug_bolt_z"][0]
    b_ = (130, 160, yb - 12, yb, zb - 7, zb + 6)
    ja(4, [(part("Plug, tapped M4 7.5 deep", win(C["plug_handle"].shape, *b_), COL["plug"]), (133, yb, zb - 5)),
           (part("Spacer", win(C["spacer_handle"].shape, *b_), COL["spacer"]), (xsp, yb, zb - 5)),
           (part("Flange", win(C["flange_handle"].shape, *b_), COL["flange"]), (xf, yb, zb + 4.5)),
           (part("Phenolic thermal-break washer", win(C["thermal_break"].shape, *b_), COL["break"]), (xe1 + 1.5, yb, zb + 3.4)),
           (part("Lug angle (6.5 mm hole, air gap)", win(C["lugs"].shape, *b_), COL["lug"]), (xe1 + 4.5, yb, zb + 5)),
           (part("Phenolic washer under the head", win(C["head_washers"].shape, *b_), "#B45309"), (xe1 + 7.5, yb, zb + 3.4)),
           (part("M4 x 20 bolt", win(C["lug_bolts"].shape, *b_), COL["screw"]), (xe1 + 11, yb, zb))],
       "Joint 4: lug angle on the handle-end cap (cut through the lower bolt)",
       "Section seen from the back. Only phenolic touches the angle; air round the bolt in its hole")
    # 5 pivot and rod end, seen from outside
    b_ = (xe1 - 2, xe1 + 30, 25, 56, z0 - 10, z0 + 58)
    xp, zp, zr = D["rod_x"], z0 + P["pivot_z"], D["grip_z"]
    ja(5, [(part("Flange", win(C["flange_handle"].shape, *b_), COL["flange"]), (xe1, 50, z0 + 48)),
           (part("Lug angle (upright leg)", win(C["lugs"].shape, *b_), COL["lug"]), (xe1 + 22, 39, z0 + 52)),
           (part("Pivot pin and nyloc nut", win(C["pins"].shape, *b_), COL["pin"]), (xp, 49, zp)),
           (part("Bail arm", win(C["arms"].shape, *b_), COL["arm"]), (xp + 4, 44, z0 + 27)),
           (part("Rod end and M6 screw", win(S("rod", "rod_screws"), *b_), COL["rod"]), (xp, 47.3, zr)),
           (part("Grip", win(C["grip"].shape, *b_), COL["grip"]), (xp + 9, 30, zr - 6))],
       "Joint 5: bail pivot and rod end (back side, seen from outside and behind)",
       "The arm lies flat on the angle's upright leg and swings on the pin; the rod is screwed to the arm",
       elev=12, azim=60)
    # 6 key tab, cut through one key screw
    ky = P["key_y"][P["grade"]]
    yk = ky + P["key_screw_dy"]
    zk = z0 + P["key_screw_z"]
    b_ = (xe0 - 14, xt0 + 16, ky - 22, yk, z0 - 2, z0 + 30)
    ja(6, [(part("Key tab", win(C["key"].shape, *b_), COL["key"]), (xe0 - 4, yk, z0 + 7)),
           (part("M4 x 16 screw in its counterbore", win(C["key_screws"].shape, *b_), COL["screw"]), (xe0 - 7, yk, zk)),
           (part("Flange", win(C["flange_key"].shape, *b_), COL["flange"]), (xe0 + 1.6, yk, z0 + 26)),
           (part("Spacer", win(C["spacer_key"].shape, *b_), COL["spacer"]), (xt0 + 1.5, yk, z0 + 22)),
           (part("Plug, tapped M4 7.5 deep", win(C["plug_key"].shape, *b_), COL["plug"]), (xt0 + 8, yk, z0 + 24)),
           (part("Tube wall", win(C["tube"].shape, *b_), COL["tube"]), (xt0 + 14, yk, z0 + 1.5))],
       "Joint 6: key tab on the key-end cap (cut through one screw)",
       "Section seen from the back. Screws from the front of the tab into blind holes in the plug")
    # 7 fill port, cut through its axis
    py = P["port_y"]
    b_ = (120, 152, py - 18, py, z0 - 2, z1 + 2)
    ja(7, [(part("Tube wall", win(C["tube"].shape, *b_), COL["tube"]), (126, py, z1 - 1.5)),
           (part("Flange", win(C["flange_handle"].shape, *b_), COL["flange"]), (xf, py, z0 + 44)),
           (part("Spacer", win(C["spacer_handle"].shape, *b_), COL["spacer"]), (xsp, py, z0 + 42)),
           (part("Plug", win(C["plug_handle"].shape, *b_), COL["plug"]), (xpl, py, z0 + 42)),
           (part("G 1/2 plug and bonded seal", win(C["port"].shape, *b_), COL["port"]), (xe1 + 3.5, py, zm + 11)),
           (part("PCM", win(C["fill"].shape, *b_), COL["fill"]), (124, py, zm))],
       "Joint 7: fill port in the handle-end cap (cut through its axis)",
       "Section seen from the back. Tapped through the bonded stack, 3.5 mm inside the O-ring line")
    # 8 melt indicator and guards on the top
    b_ = (xt1 - 62, xt1 - 20, 14, 50, z1 - 3, z1 + 8)
    jt(8, [part("Shell top (painted)", win(C["tube"].shape, *b_), COL["tube"]),
           part("Label, notched", win(C["label"].shape, *b_), COL["label"]),
           part("Melt indicator tube (PCM inside)", win(C["indicator"].shape, *b_), COL["ind"]),
           part("Guards (fin bar)", win(C["guards"].shape, *b_), COL["guard"])],
       "Joint 8: melt indicator and its guards on the top, handle end",
       "Indicator and guards are bonded to the paint with the epoxy; the label is notched round them",
       elev=35, azim=-60, size=(8, 5.5))
    # 9 frame corner
    fx0, ft, wi = D["fx0"], P["frame_t"], D["frame_in_w"] / 2
    b_ = (fx0 - 6, fx0 + 25, 55, 84, -1, 45)
    fr = win(C["frame"].shape, *b_)
    stop = fr & box(fx0, fx0 + ft, -wi, wi, ft, 50)
    wall = (fr & box(fx0, 200, wi, 100, ft, 50)) + (fr & box(fx0 - 5, fx0, 0, 100, ft, 50))
    floor = fr & box(-200, 200, -100, 100, -1, ft)
    rv = win(C["rivets"].shape, *b_)
    ja(9, [(part("Side wall and its folded tab", wall, "#A8A29E"), (fx0 - ft, wi + ft - 2, ft + 15)),
           (part("End stop", stop, "#78716C"), (fx0, wi - 8, ft + 34)),
           (part("Floor", floor, "#D6D3D1"), (fx0 + 22, 56, ft)),
           (part("Rivets (tails outside, heads inside)", rv, COL["rivet"]), (fx0 - ft - 2, wi + ft - P["tab_l"] / 2, ft + P["rivet_z"][1]))],
       "Joint 9: frame corner (back corner at the stop, seen from outside)",
       "The wall's 12 mm tab folds round the outside of the stop and is riveted twice",
       elev=22, azim=-160, size=(8, 5.5))
    # 10 key through the stop slot, cartridge seated
    b_ = (fx0 - 10, xt0 + 30, ky - 40, ky + 25, -1, 62)
    ja(10, [(part("Frame stop and floor", win(C["frame"].shape, *b_), COL["frame"]), (fx0, ky + 20, ft + 33)),
            (part("Rivets", win(C["rivets"].shape, *b_), COL["rivet"]), (fx0 - ft - 2, -(wi + ft - P["tab_l"] / 2), ft + P["rivet_z"][1])),
            (part("Key tab, through the slot", win(S("key", "key_screws"), *b_), COL["key"]), (xe0 - 10, ky + 8, z0 + 17)),
            (part("Key-end flange (2 mm off the stop)", win(C["flange_key"].shape, *b_), COL["flange"]), (xe0, ky + 10, z1 - 4)),
            (part("Tube", win(S("tube", "fins_bot", "fins_top"), *b_), COL["tube"]), (xt0 + 20, -P["tube_w"] / 2, z1 - 12))],
       "Joint 10: seated cartridge, key through the slot in the stop",
       "3 mm clear round the key; a wrong grade's key meets the stop and the cartridge stays 12 mm short",
       elev=28, azim=-150)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(which=None):
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        if which is None or str(n) == str(which):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    tube = M["tube"]
    st(1, [tube], [mv(part("Bottom fins (9)", C["fins_bot"].shape, COL["fins"]), (0, 0, -70))],
       "bottom fins onto the tube", "Tube upside down in the comb jig; epoxy bead and fillets; cure before turning over. Seen from below",
       elev=-30, azim=-55)
    st(2, [tube, part("Bottom fins", C["fins_bot"].shape, COL["fins"])], [mv(part("Top fins (9)", C["fins_top"].shape, COL["fins"]), (0, 0, 70))],
       "top fins onto the tube", "Key end flush with the bottom fins; 96 mm left bare at the handle end for the label. Then prime and paint",
       elev=28, azim=-55, label_done=False)
    shell = [tube, part("Fins", S("fins_bot", "fins_top"), COL["fins"])]
    capk = part("Key-end cap stack", S("flange_key", "spacer_key", "plug_key"), COL["flange"])
    st(3, [capk], [mv(part("Key tab", C["key"].shape, COL["key"]), (-60, 0, 0)),
                   mv(part("M4 x 16 screws (2)", C["key_screws"].shape, COL["screw"]), (-110, 0, 0))],
       "key tab onto the key-end cap", "Two M4 x 16 socket cap screws with thread sealant, into blind holes in the plug",
       elev=20, azim=-130)
    keytab = part("Key tab", S("key", "key_screws"), COL["key"])

    def screws(end):
        sh = C[f"screws_{end}"].shape
        top = win(sh, -200, 200, -100, 100, zm, 100)
        bot = win(sh, -200, 200, -100, 100, -50, zm)
        return [mv(part("Top radial screws and seals (3)", top, COL["screw"]), (0, 0, 45)),
                mv(part("Bottom radial screws and seals (3)", bot, COL["screw"]), (0, 0, -45))]
    capk_full = part("Key-end cap with O-ring and key tab", S("flange_key", "spacer_key", "plug_key", "oring_key", "key", "key_screws"), COL["flange"])
    st(4, shell, [mv(capk_full, (-110, 0, 0))],
       "key-end cap into the tube", "O-ring on the spacer, lightly greased; push the stack in until the flange meets the tube end",
       elev=22, azim=-125, label_done=False)
    keyend = shell + [part("Key-end cap", S("flange_key", "spacer_key", "plug_key", "oring_key"), COL["flange"]), keytab]
    st(5, keyend, screws("key"), "radial screws at the key end",
       "Six M5 x 10 button-head screws, each on a bonded seal, into the plug; tighten evenly", elev=12, azim=-125, label_done=False)
    keyend = keyend + [part("Key-end screws", C["screws_key"].shape, COL["screw"])]
    caph = part("Handle-end cap stack", S("flange_handle", "spacer_handle", "plug_handle"), COL["plug"])
    st(6, [caph], [mv(part("Thermal-break washers (4)", C["thermal_break"].shape, COL["break"]), (25, 0, 0)),
                   mv(part("Lug angles (2)", C["lugs"].shape, COL["lug"]), (55, 0, 0)),
                   mv(part("Head washers and M4 x 20 bolts", S("head_washers", "lug_bolts"), COL["screw"]), (100, 0, 0))],
       "lug angles onto the handle-end cap", "Two phenolic washers under each angle, one under each bolt head; bolts snug with thread sealant",
       elev=18, azim=35)
    st(7, keyend, [mv(part("Handle-end cap", S("flange_handle", "spacer_handle", "plug_handle", "oring_handle", "thermal_break", "lugs", "head_washers", "lug_bolts"), COL["plug"]), (80, 0, 0))],
       "handle-end cap into the tube", "With its O-ring and lug angles, as step 4; the fill port hole toward the back, the lug angles outward",
       elev=22, azim=-55, label_done=False)
    capped0 = keyend + [part("Handle-end cap", S("flange_handle", "spacer_handle", "plug_handle", "oring_handle", "thermal_break", "lugs", "head_washers", "lug_bolts"), COL["plug"])]
    st(8, capped0, screws("handle"), "radial screws at the handle end", "Six M5 x 10 button-head screws on bonded seals into the plug, as step 5", elev=14, azim=-65, label_done=False)
    capped = capped0 + [part("Handle-end screws", C["screws_handle"].shape, COL["screw"])]
    st(9, capped, [mv(part("Arms, pins and nuts", S("arms", "pins"), COL["arm"]), (40, 0, 0)),
                   mv(part("Rod with grip, M6 screws", S("rod", "grip", "rod_screws"), COL["rod"]), (90, 0, 0))],
       "bail onto the lug angles", "Pins through angle and arm, nuts snug so the arm swings; rod between the arms on two M6 screws",
       elev=18, azim=-35, label_done=False)
    bail = part("Bail", S("arms", "pins", "rod", "grip", "rod_screws"), COL["arm"])
    st(10, capped + [bail], [mv(part("G 1/2 plug and bonded seal", C["port"].shape, COL["port"]), (60, 0, 0))],
       "fill with PCM, then plug the port", "Handle end up, PCM poured in by weight at its fill temperature; new bonded seal; plug tightened. Seen from the back",
       elev=20, azim=35, label_done=False)
    full = capped + [bail, part("Fill port plug", C["port"].shape, COL["port"])]
    st(11, full, [mv(part("Grade label (notched)", C["label"].shape, COL["label"]), (0, 0, 40)),
                  mv(part("Melt indicator", C["indicator"].shape, COL["ind"]), (0, 0, 80)),
                  mv(part("Guards (2)", C["guards"].shape, COL["guard"]), (0, 0, 110))],
       "melt indicator, guards and label onto the top", "Bond the indicator and guards with the epoxy; then apply the label round them",
       elev=35, azim=-55, label_done=False)
    done = full + [part("Label and indicator", S("label", "indicator", "guards"), COL["ind"])]
    st(12, [M["frame"]], [mv(part("Finished cartridge (C5)", fuse([p.shape for p in done]), "#374151"), (40, 0, 140))],
       "cartridge into the adapter frame", "Lower it in 15 mm back from the stop, then slide it forward until the key passes through the slot",
       elev=24, azim=-50)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps}
    if not args:
        for k, f in fns.items():
            print(k, "->", f())
    else:
        w = args[0]
        r = fns[w](*args[1:2]) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, "->", r)
