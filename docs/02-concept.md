---
doc_id: TCT-PRC-001
title: ThermaCart design precis
project: ThermaCart
doc_type: Design precis
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, grades, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from TCT-CAL-001 and TCT-DDR-001 (choices adopted for TRL 3 work, folding bail, cap stack, stock fin bar, verified PCM data, numbers, safety limits)
---

# ThermaCart design precis

## Summary

ThermaCart is a sealed aluminium cartridge, 323 x 152 x 64 mm, that holds 1.10 to 1.18 kg of phase-change material (PCM) in one of three standard grades: C5 (melts at 5 °C, cold chain), C25 (25 °C, comfort) and H70 (70 °C, hot holding). It fits a GN 1/3 gastronorm slot, carries by a folding bail, shows its state through a sight window and locks into an adapter frame whose key accepts only the right grade. The TRL 3 calculations (TCT-CAL-001) give 65, 61 and 73 Wh of usable storage per cartridge, 2.9 to 3.0 kg filled and about $71 in parts. Three requirements are not met on paper: the PCM mass fraction (R5, 38 to 40 %), the cold-chain hold time (R10, about 2 h instead of 8 h, limited by heat transfer from the cooler air) and the cost (R16). The design choices below are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction and remain open for his review (TCT-DDR-001).

![ThermaCart hero render](../media/hero.png)

*Figure 1. A TC-L cartridge (C5 grade) in its adapter frame on a table, with a 25 L cooler for scale.*

## How it works

1. **Charge.** The cartridge is put where the right temperature already exists: a freezer for C5, a refrigerator or freezer for C25, an oven set to 85 °C (never above 90 °C) or a thermostatic heating pad for H70. The PCM freezes (C5, C25) or melts (H70) and stores latent heat at a nearly constant temperature.
2. **Carry and swap.** The sight window shows the state. The owner lifts the bail, carries the cartridge to a cooler, food carrier, cabinet or heat exchanger and slides it nose first into an adapter frame.
3. **Hold.** The host box leaks heat in (cold grades) or out (H70). The PCM absorbs or releases it while staying near its melt point, so the box contents stay near that temperature for as long as the cartridge can move heat to or from them.
4. **Return.** The discharged cartridge goes back to the charging point. Nothing is consumed; the fill is sealed for life.

![Energy flow for one H70 cartridge](../media/flow.png)

*Figure 2. Energy per charge cycle for one H70 cartridge charged on a 60 W pad and used for hot holding (TCT-CAL-001, E4; estimates): 162 Wh in, 130 Wh stored between 25 and 80 °C, 88 Wh released above 63 °C and 42 Wh below it.*

## Standard grades

Table 1. Grades (adopted for TRL 3 work, open for Amish's review)

| Grade | Melt range | Fill (class) | Filled at | Usable storage per TC-L (TCT-CAL-001) | Typical hosts | Colour and key (Y of key centre) |
| --- | --- | --- | --- | --- | --- | --- |
| C5 | 5 to 6 °C | Organic paraffin, Rubitherm RT 5 HC class | 45 °C | 65.4 Wh (1.104 kg) | Produce and dairy coolers; a ColdPod-type box after qualification | Blue, -43 mm |
| C25 | 22 to 26 °C | Organic paraffin, RT 25 HC class | 65 °C | 60.5 Wh (1.119 kg) | Electronics and battery cabinets, comfort cooling | Green, 0 mm |
| H70 | 69 to 71 °C | Organic paraffin, RT 70 HC class | 90 °C | 72.9 Wh (1.180 kg) | Insulated GN food carriers, keep-warm boxes | Red, +43 mm |
| W0 (option) | 0 °C | Water with a nucleating agent | Not yet sized | Not yet calculated | Produce only; never for vaccines or medicines | White, -61 mm |

Melt ranges, densities and maximum operating temperatures are from the Rubitherm datasheets ([RT 5 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT5HC_EN_23072026.PDF), [RT 25 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT25HC_EN_21012026.PDF), [RT 70 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT70HC_EN_21012026.PDF)). Each grade is filled at its maximum operating temperature (45, 65 and 90 °C), so the cartridge is never more pressurized in service than when it was sealed. Paraffins are used because they are chemically stable, non-corrosive to aluminium and cycle well ([PATH PCM study](https://media.path.org/documents/DT_pcm_summary_rpt1.pdf)). Salt hydrates would store more per litre but supercool, separate and corrode aluminium ([corrosion study](https://www.researchgate.net/publication/229021530_Corrosive_effects_of_salt_hydrate_phase_change_materials_used_with_aluminium_and_copper)), so they are left for a later lined variant.

## Main components

Table 2. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Choice for TRL 3 | Notes |
| --- | --- | --- | --- |
| 1 | Cartridge shell | 6063-T52 rectangular tube, 152.4 x 50.8 x 3.175 mm (6 x 2 x 1/8 in), 280 mm long, with nine 6.35 x 1.59 mm (1/4 x 1/16 in) fin bars bonded on edge on each broad face | Stock sections, no welding; fins add 44 % to the tube's outer area |
| 2 | PCM fill | 1.10 to 1.18 kg of the grade's PCM, filled as liquid to 90 % of the 1.655 L inner volume | See Table 1 and Safety |
| 3 | End caps (2) | Stack of 3.175 mm flange, 3 mm gland spacer and 9.525 mm plug in 6061 plate; spliced FKM 3 mm cord O-ring in the corner gland; six radial M5 screws through the tube wall into the plug | Cut and filed, no milling; FKM (or NBR) resists paraffin, EPDM does not |
| 4 | Fill port plug | G 3/4 plug with a bonded FKM seal in the handle-end cap, outboard of the bail | Fill, drain and recycling |
| 5 | Handle and keyed nose | Folding bail (16 mm rod, silicone grip) on two lugs with 3 mm phenolic thermal-break washers, stowed against the end face; key tab at the grade position on the nose | 39 mm finger gap when raised; key positions in Table 1 |
| 6 | Grade label and melt indicator | Colour-coded polyester label; 22 mm sight window over a small glass vial of the same PCM | Paraffin is opaque white when solid and clear when liquid |
| 7 | Cabinet adapter frame | Bent 1.5 mm 5052 aluminium sheet, 304 x 160 mm, with side walls and a keyed end stop | One per host slot; host designs copy its key slot |
| 8 | Hardware | Twelve M5 x 12 A2 countersunk screws, epoxy rated 120 °C or more, thread sealant | Per cartridge |

![Exploded view with BOM numbers](../media/exploded.png)

*Figure 3. Exploded view. 1 shell, 2 PCM fill, 3 end caps, 4 fill port plug, 5 handle and keyed nose, 6 label and indicator, 7 adapter frame, 8 cap screws.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section along the cartridge. The PCM (blue) fills 90 % of the inner height when liquid; the rest is ullage. The cap stacks, fins and label band are visible. The general arrangement is drawing TCT-DWG-001.*

## Key numbers

All values are from TCT-CAL-001 and the parametric model `cad/src/model.py`.

Table 3. Key numbers

| Quantity | Value | Requirement |
| --- | --- | --- |
| Overall size | 323.4 x 152.4 x 63.5 mm, bail stowed | R2 met (GN 1/3: 325 x 176 mm, 65 mm) |
| Inner volume | 1.655 L (146.05 x 44.45 x 254.9 mm) | |
| PCM mass | C5 1.104 kg, C25 1.119 kg, H70 1.180 kg | |
| Usable storage within ±3 K | C5 65.4 Wh, C25 60.5 Wh, H70 72.9 Wh | R3 met (C25 thin) |
| Empty cartridge | 1.78 kg | |
| Filled mass | 2.89 to 2.96 kg | R4 met (thin) |
| PCM fraction | 38.3 to 39.9 % | R5 **not met** |
| Pressure | 0.00 bar gauge at the fill temperature, -0.68 bar when frozen, +0.29 bar at 20 K over the limit; wall stress 56 MPa against 73 MPa allowable | R8 met |
| Cold hold, two C5 in a 25 L cooler at 32 °C | 1.9 h (bare) to 2.4 h (dark finish); stored energy alone would last 9.7 h | R10 **not met** |
| Hot hold, one H70 in a GN carrier at 25 °C | 7.2 h at 63 °C or more | R11 met |
| Recharge | C5 in a freezer 5.6 h; C25 in a refrigerator 6.6 h; H70 in an 85 °C oven 6.1 h, on a 60 W pad 2.7 to 10.3 h | R12 at risk (pad) |
| Bail temperature, H70 | 42.5 °C on a thermal break; 85 °C for about 12 min after an oven | R14 at risk |
| Parts cost | About $71 per cartridge, $16 per frame (indicative) | R16 **not met**; $87 against the $80 budget |

## Key design choices (adopted for TRL 3 work, open for Amish's review)

Each choice below is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (TCT-DDR-001, items D1 to D8 and T1 to T4).

1. **Envelope: GN 1/3 footprint from a stock tube (D1).** A 6 x 2 in stock aluminium tube cut to fit a GN 1/3 slot. The WHO PQS 0.6 L pack envelope, 190 x 120 x 34 mm ([WHO PQS E005](https://extranet.who.int/prequal/key-resources/documents/pqs-performance-specification-e005ip012-water-packs-use-icepacks-cool-packs)), is kept as a later small size (TC-S), and a custom finned extrusion only if volumes justify a die.
2. **Three paraffin grades, water as an option, C5 first (D2).** See Table 1.
3. **Mechanical grade keying and a passive indicator (D4).** A nose tab whose position depends on the grade and a matching slot in each frame, so a frozen water or hot H70 cartridge cannot be put into a cold-chain box; the key table is published as part of the open standard. A sight window over a vial of the same PCM shows solid or liquid without electronics.
4. **The 2 mm wall is not used (D5).** It adds 3.5 % volume and would yield under the vacuum of a frozen cartridge. C5 meets R3 on the 3.175 mm tube.
5. **Fill hot, seal for life (D8).** Filling as liquid at the grade's maximum operating temperature fixes the largest PCM volume at sealing, so the cartridge only sees vacuum below that temperature and a small positive pressure if the limit is exceeded.
6. **Aluminium shell for paraffins, no HDPE (D8).** Paraffin can swell and permeate polyethylene ([compatibility study](https://www.researchgate.net/publication/227717836_Compatibility_of_plastic_with_phase_change_materials_PCM)); aluminium is compatible and conducts heat to the fins. A lined or HDPE variant is kept for salt hydrates and water.
7. **Folding bail, cap stack and stock fin bar (T1 to T3).** Refinements that keep the cartridge inside the GN 1/3 envelope, give room for fingers and avoid milling.

## Safety

> **Safety:** Paraffin fills are combustible. Never charge an H70 cartridge on an open flame, a gas ring or a hot plate. Set an oven to 85 °C and check it with an oven thermometer; never let an H70 cartridge exceed 90 °C, the maximum operating temperature of RT 70 HC. If a cartridge leaks, stop using it; spilled liquid paraffin is slippery and burns.

> **Safety:** Keep C5 cartridges below 45 °C and C25 cartridges below 65 °C, their fill temperatures and datasheet limits; do not leave them in a closed car in the sun.

> **Safety:** H70 cartridges reach 70 to 85 °C and can burn skin. Carry them only by the bail. Straight out of an oven the bail and its grip are at oven temperature for about 12 min: use oven gloves or wait. The label must carry a hot-surface warning.

> **Safety:** Do not fill, refill or open a cartridge that is warm or under pressure. Fill only as described in the fill recipe, with 10 % ullage at the grade's fill temperature. A frozen cartridge holds a partial vacuum of about 0.7 bar; its broad faces pull in by about 0.8 mm, which is expected.

> **Safety:** A C5 cartridge charged in a freezer is below 0 °C when it comes out. Condition it until the sight window shows the first liquid before using it next to anything that must not freeze. ThermaCart is not qualified for vaccines or medicines, and the W0 water grade must never be used with them.

- Aluminium edges and fins are sharp after cutting: deburr all edges.
- A 3 kg cartridge dropped on a foot can injure: keep cartridges low in racks. A drop of a molten cartridge may stress the seals (TCT-CAL-001, C7).

## Open questions after TRL 3

- R10: can a C5 cartridge cool a cooler's contents fast enough? Options are a dark finish, placing produce in contact with the cartridge, more cartridges, or a revised requirement (awaiting Amish).
- R5 and R16: accept about 39 % PCM and about $71 per cartridge for the stock-tube build, or look for savings (awaiting Amish).
- R1: the C25 paraffin melts from 22 °C, below the 24 to 27 °C band (awaiting Amish).
- Charging C5 in a refrigerator takes 31 to 51 h; is a freezer with a conditioning step acceptable (awaiting Amish)?
- Seal performance over cycles and in a drop (R6), cycle life (R7) and the pad charge time (R12) need tests, which belong to TRL 4 and are on hold.
- Which named partner hosts the first produce cooler, and does ThermaCart become a declared dependency of ColdPod or ZeerBox? Both are Amish's decisions.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [TCT-DWG-001](../cad/drawings/TCT-DWG-001.pdf).
