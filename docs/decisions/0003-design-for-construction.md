---
doc_id: TCT-DDR-003
title: ThermaCart design for construction
project: ThermaCart
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Table 3 decided by Amish on 2026-10-02 (A1 option (b), A2 and A3 as recommended); Tables 1 and 2 still open for review; record stays Draft"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Tables 1 and 2 accepted by Amish on 2026-10-02; record stays Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This covers the changes P1 to P11 in Table 1 and the knock-on changes in Table 2, made under Amish's 2026-09-30 instruction to make the design physically buildable, and is recorded in the design decisions register (TCT-DEC-001). Items that would change what the cartridge does, its pitch or its safety case are not made here: they were listed in Table 3 as "Proposed, awaiting Amish", and Amish accepted the recommendations for all three earlier the same day: "i approve your recommendations for all 555 open decisions." For A1 the accepted recommendation is option (b), the low lip, which differs from the (a) first proposed here; it is to be designed and is not yet in the model. Recorded in the design decisions register (TCT-DEC-001, items 1 to 3). The record stays Draft.

## Context

On 2026-09-30 Amish asked for every repo to have a prototype build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model behind TCT-DDR-001 and TCT-DDR-002 showed what ThermaCart does and was sized in TCT-CAL-001, but a constructability review of `cad/src/model.py` with build123d (overlap volumes, contacts and clearances between every pair of parts that meet) found parts that could not be made, assembled or sealed as drawn.

The changes keep what ThermaCart does: the same stock tube, inner volume (1.655 L), fill, grades, fins, finish, GN 1/3 envelope (323.4 x 152.4 x 63.5 mm with the bail stowed), folding bail, key positions and frame. Every change is in `cad/src/model.py`, which now builds each component separately and runs 68 constructability checks (`python cad/src/model.py --check`), including the bail swung to 90 and 180 degrees. All 68 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The G 3/4 fill port bore, 60 mm from the centre line, reached 71.7 mm from the centre; the spacer edge (the O-ring line) is at 70.5 mm, so the bore cut through the O-ring (24 mm³ of overlap in the model). | A G 1/2 plug with a collar and hex socket (DIN 908 class) in anodised aluminium, on a bonded FKM sealing washer, tapped through the bonded cap stack 56 mm toward the back from the centre line at mid-height. Its thread stays 3.5 mm inside the O-ring line and its collar 2 mm clear of the bail. | Smallest change that seals: the port moves inside the gland, and G 1/2 still pours and drains paraffin. An aluminium plug avoids a stainless and aluminium couple and is 20 g lighter, which keeps R5. |
| P2 | A 3 mm O-ring cord in a corner gland 3 mm long and 2.5 mm deep fills 94 % of the gland, with no room for the cord to swell at 90 °C; the square spacer and plug corners would also hit the stock tube's inside corner fillets. | FKM cord 2.5 mm, gland 2.1 mm deep (the spacer is cut to the measured bore less 4.2 mm each way): 78 % fill, 16 % squeeze. Spacer corners 3.7 mm radius, plug corners 2 mm, flange corners 4.8 mm to match the tube; a 1 mm lead-in chamfer inside each tube end. | A static radial seal wants about 15 to 25 % squeeze and under about 85 % fill. Cutting to the measured bore takes up the extrusion's tolerance on a one-off build. |
| P3 | The six radial screws per cap sit inboard of the O-ring, so their holes in the tube wall are on the PCM side of the seal (a leak path); they were drawn as heads only; and an M5 countersink in a 3.175 mm wall leaves a knife edge. | M5 x 10 A2 button-head screws (ISO 7380) on M5 FKM bonded sealing washers, through 5.5 mm holes into M5 holes tapped 7.5 mm deep in the plug edge. Heads sit between the fins (2.1 mm clear) and 2.6 mm above the frame floor. Holes are transfer-drilled with the cap in place. | The bonded washer seals each hole where the screw head clamps it; moving the O-ring outboard of the screws would need a fourth plate and more length the envelope does not have. |
| P4 | The flange, gland spacer and plug had no fixing to each other. | Bonded face to face over their whole faces with the 120 °C structural epoxy, which also seals the joint lines, and held by M4 screws into blind holes tapped 7.5 mm deep in the plug, never through its wet face: at the handle end the four lug bolts and one M4 countersunk screw; at the key end the two key tab screws and two M4 countersunk screws. | The stack is one rigid block before it is tapped and fitted; no screw hole reaches the PCM. |
| P5 | The bail could not fold: each arm sat in front of its lug, so its pin would have run along the cartridge. The lugs stood 3.2 mm above the flange, over the O-ring gland, with no fixing; a steel bolt through the thermal-break washer would have bypassed the break; and the 16 mm rod was wider than the 12 mm arms. | Two lug angles (20 x 20 x 3 mm aluminium angle, 32 mm long) each held by two M4 x 20 bolts into the plug, standing on two phenolic washers (9 mm across, 3 mm thick) per bolt, with a 3 mm phenolic washer under each bolt head and 1.25 mm of air round each bolt in a 6.5 mm hole. Two 16 x 4 mm arms, 38 mm between holes, lie on the outside of the angles' upright legs on 5 mm stainless pins with nyloc nuts. The 16 mm rod, 80 mm long and tapped M6 at both ends, sits between the arms on two M6 x 12 button-head screws. | Every joint is face to face and fixed, the pivot runs across the cartridge as a bail must, and only phenolic touches the bail, so the thermal break works. The stowed envelope is unchanged; the raised finger gap is 41 mm (was 39 mm). |
| P6 | The key tab had no fixing. | Two M4 x 16 socket cap screws in 5 mm counterbores from the front of the tab, through flange and spacer into blind holes in the plug, 7 mm each side of the key centre and 14 mm above the flange's bottom edge. | The screw heads sit below the tab's front face and clear of the frame slot. |
| P7 | The frame's end stop stood 2 mm in front of the key tip, so the key never entered its slot and the frame had no seated position for any grade. | The stop moved so that a seated cartridge's nose flange is 2 mm from the stop and the key passes through the slot with 3 mm clearance all round. The frame floor is 294 mm long (was 304 mm). A wrong grade's key meets the stop and that cartridge stays 12 mm short of seated. | This is what the keying in R9 and TCT-CAL-001 (G1) assumed. |
| P8 | The stop and the side walls overlapped in the corners, which a sheet bent from one blank cannot do. | The stop is 157.4 mm wide and bends up between the walls; each wall ends in a 12 mm tab folded round the outside of the stop and fixed with two 3.2 mm blind rivets, heads inside, 1 mm clear of the nose flange; 3 mm relief holes where bend lines cross. | A standard box corner for a hand brake. |
| P9 | The "sight window" was a 22 mm disc 2 mm thick on the label: too thin to hold a vial, and with no fixing. | A clear polycarbonate tube, 6 mm outside and 4 mm bore, 40 mm long, filled with the grade's PCM and closed with epoxy plugs, bonded along the top 30 mm toward the back from the centre line, between two 40 mm guards of the fin bar bonded on edge 8 mm either side. The label is notched round them. | It shows solid (white) or liquid (clear) as before, is made with a saw, a syringe and the same epoxy, and the guards (as tall as the fins) take knocks. Polycarbonate is rated well above 90 °C and paraffins do not attack it. |
| P10 | The fins were bonded on their 1.59 mm edge with no bond detail. | A bead of the epoxy under each fin and a fillet down both sides, with the fins held upright at pitch in a slotted wooden comb while it cures. No geometry change. | A fillet spreads the load from a knock along the fin. |
| P11 | The stock tube's corner radii were not in the model. | The tube is drawn with 4.8 mm outside and 1.6 mm inside corner radii (3/16 and 1/16 in, typical for 6 x 2 x 1/8 in tube); the cap plates follow them (P2). | The real radii are to be confirmed with the supplier (TCT-DEC-001). |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Empty cartridge 1.80 kg, unchanged [A5]; filled 2.90 to 2.98 kg (R4 met, thin); PCM fraction 38.1 to 39.6 % (was 38.1 to 39.7 %, R5 met, thin). | The added screws, bolts, washers, pins and guards are balanced by the lighter aluminium fill plug (9 g against 30 g for the G 3/4 plug) and slightly less aluminium in the bail and cap plates. |
| Handle temperature | Bail 36.8 and 39.1 °C on cartridges at 71 and 80 °C (was 39.6 and 42.5 °C); below 55 °C 10 min after an 85 °C oven (was 12 min) [F1, F2]. | The new bail has more area to the air and the bolts are insulated (P5). The 12 min label rule is kept. |
| Cost | Cartridge $80 (was $76), frame $17 (was $16); one C5 cartridge and one frame $97 against the $80 value-engineering target, $17 over [H1]. | Bonded seals, bolts, phenolic washers, rivets; the G 1/2 plug is $1 cheaper. `budget_usd` is unchanged. |
| Thermal and pressure | Unchanged: inner volume, fill, fins, finish and wall are unchanged, so B to E of TCT-CAL-001 are unchanged. | |
| Drawing | TCT-DWG-001 Rev P4; making sketches TCT-DWG-101 to 110 added. | Follows the model. |
| Documents | TCT-CAL-001 v0.3, TCT-REQ-001 v0.5, TCT-PRC-001 v0.5; BOM lines 1 and 3 to 8 rewritten. No requirement target changed. | Follows the model. |

*Table 3. Proposed, then decided by Amish on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | How a wrong grade is shown to be rejected (R9). With P7, a wrong grade's key meets the stop and the cartridge stays 12 mm short, its handle end standing proud of the frame, but nothing stops it being left in the host like that. This touches the safety case: a frozen W0 or hot H70 cartridge in a cold-chain box. | (a) accept the 12 mm stand-off and check at TRL 4 that the host's lid or door will not close on it; (b) a low lip at the frame's open end that the bottom fins drop behind only when the key is through the slot (needs the stowed grip moved up, a change to the bail); (c) a sprung detent in the stop. | (a) for the prototype, with the check written into the TRL 4 plan; (b) if the check fails. Decided 2026-10-02: (b). Design the low lip on paper now, with the stowed grip moved up, so the frame rejects a wrong grade; fall back to (a) only if the TRL 4 check shows no target host's lid can close on a proud cartridge. |
| A2 | The W0 option (key at 61 mm toward the front) does not fit the constructable cap and frame: its outer key screw would be 0.9 mm from the O-ring line, and its slot would cut through the frame's corner tab. | (a) when W0 is sized, fix its tab with screws 4 mm each side of its centre and shorten that frame's tab; (b) move the W0 key position, which changes the published key table. | (a); W0 is an option not yet sized, and the key table is part of the open standard. Accepted 2026-10-02: (a), when W0 is sized; the key table is unchanged. |
| A3 | R5 now has 0.1 percentage point of margin (38.1 % against 38 %) on catalogue masses. | (a) accept and weigh the prototype at TRL 4; (b) look for mass now (a tubular bail rod, thinner plugs with M4 radial screws). | (a). Accepted 2026-10-02: (a); if the weighed prototype misses, the tubular bail rod first. |

## Consequences

- `design_state: constructable` in `project.yaml`. The prototype build plan TCT-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 1 not met (R10), 1 over its value-engineering target (R16), 1 at risk (R12), 3 not verifiable at TRL 3 (R6, R7, R17), 12 met (TCT-CAL-001 v0.3). R16 was counted as not met before 2026-10-01; the budget is now a value-engineering target (STANDARDS section 18).
- The photoreal renders (`media/render-*.png`, made on Amish's Mac), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept bail, the round sight window, the G 3/4 plug and the concept frame stop. They need updating on Amish's Mac. The concept media from `cad/src/concept_media.py` have been regenerated from the constructable model.
- The tube's corner radii, its bore and the bought parts in TCT-DEC-001 ("To confirm when parts are bought") are checked when parts are bought, which waits with TRL 4.
