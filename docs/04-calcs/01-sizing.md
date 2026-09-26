---
doc_id: TCT-CAL-001
title: ThermaCart sizing calculations
project: ThermaCart
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (geometry and mass, storage per grade, pressure and wall stress, 2 mm wall option, hold times, recharge, handle temperature, keying, cost)
---

# ThermaCart sizing calculations

On paper the TC-L cartridge meets nine of its eighteen requirements, has three at risk, misses three and leaves three that only tests can settle. The three misses are the PCM mass fraction (R5: 38 to 40 % against 50 %), the cold-chain hold time (R10: about 2 h against 8 h, because the cartridge cannot pull heat out of the cooler air fast enough, although it stores enough energy for 9.7 h) and the parts cost (R16: $71 per cartridge against $50, which also puts one cartridge and one frame $7 over the $80 budget). The three at risk are recharge on a 60 W pad (R12), the handle of an H70 cartridge straight from the oven (R14) and the C25 melt range, which starts 2 K below its target band (R1). With the verified Rubitherm datasheet values, the C5 grade now meets R3 (65 Wh), which the TRL 2 estimate did not; C25 meets it by a thin margin. The 2 mm wall evaluated under decision D5 is rejected: it adds only 3.5 % volume and its walls would yield under the vacuum that forms when a cartridge is frozen. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C3], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that a cartridge is leak-tight, drop-safe or fit for food contact, and they are not a substitute for tests. ThermaCart is not qualified for vaccines or medicines. See TCT-PRC-001, Safety.

## Scope and method

The note checks every requirement in TCT-REQ-001 v0.3 against the design in TCT-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, its derived dimensions and its build123d solids, so the inner volume, part volumes, areas and key positions used here are those in the STEP files and in drawing TCT-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| PCM data | RT 5 HC: 250 kJ/kg from -2 to 13 °C, melt 5 to 6 °C, 0.85 kg/L solid, 0.76 kg/L liquid at 20 °C, maximum operating temperature 45 °C. RT 25 HC: 230 kJ/kg from 16 to 31 °C, melt 22 to 26 °C, 0.88 and 0.77 kg/L (liquid at 40 °C), maximum 65 °C. RT 70 HC: 260 kJ/kg from 62 to 77 °C, melt 69 to 71 °C, about 0.9 and 0.8 kg/L (liquid at 80 °C), maximum 90 °C. All: cp 2 kJ/(kg·K), k 0.2 W/(m·K), capacity ±7.5 % | Rubitherm datasheets for [RT 5 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT5HC_EN_23072026.PDF), [RT 25 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT25HC_EN_21012026.PDF) and [RT 70 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT70HC_EN_21012026.PDF), read 2026-09-25 |
| Usable storage | Latent heat = capacity at the low side of the tolerance minus 2 kJ/(kg·K) x 15 K sensible; usable = latent plus sensible over the ±3 K band of R3; latent spread evenly over the melt range | Conservative reading of the datasheets |
| Fill | 90 % of the inner volume, filled as liquid at the grade's maximum operating temperature (45, 65 and 90 °C), then sealed with air at 1 atm; liquid expansion 0.001 /K, solid 0.0003 /K | Expansion coefficients are typical paraffin values, to confirm |
| Aluminium | 6063-T52 tube, minimum yield 110 MPa, design factor 1.5 (allowable 73 MPa); E 69 GPa; 2.70 kg/L, 0.9 kJ/(kg·K) | ASTM B221 minimum |
| Air side | Natural convection h = 1.32 (ΔT/0.15 m)^0.25 W/(m²·K) plus radiation; emissivity 0.10 for mill-finish aluminium, 0.90 if painted or anodized dark; 85 % of the outer area exposed | Handbook correlations |
| Cold box (R10) | 25 L cooler, 0.5 W/K, 32 °C ambient; 5 kg of produce precooled to 5 °C (3.9 kJ/(kg·K)) plus 2 kJ/K of air and liner; cartridges conditioned to 2 °C; contents and cooler air lumped, no direct contact between produce and cartridge | As in TCT-REQ-001; contact would help and is not credited |
| Hot box (R11) | GN carrier, 0.25 W/K, 25 °C ambient; 4 kg of food at 75 °C (3.5 kJ/(kg·K)) plus 2 kJ/K of liner; H70 charged to 85 °C | As in TCT-REQ-001 |
| Charging (R12) | Still-air freezer at -18 °C, refrigerator at 2 or 4 °C, fan oven at 85 °C (h 15 W/(m²·K) plus radiation), 60 W pad with 80 % of its output entering the cartridge | Screening values |
| Burn thresholds (R14) | 10 s contact: about 55 °C for bare metal and about 70 °C for plastics and rubber | Commonly quoted from ISO 13732-1; not checked against the standard (paywalled) |
| Cost | Indicative one-off USD prices in `bom/bom.csv`, not quotes; PCM at $10/kg | To be replaced with quotes before any build |

## A. Geometry and mass (R2, R4, R5)

- **Envelope.** With the bail stowed the cartridge is 323.4 x 152.4 x 63.5 mm, inside the GN 1/3 slot (325 x 176 mm, 65 mm deep) with margins of 1.6, 23.6 and 1.5 mm [A1]. The TRL 2 fixed handle left only about 14 mm between grip and end cap, too little for fingers; the folding bail stows inside the envelope and gives a 39 mm finger gap when raised [A3].
- **Inner volume.** 146.05 x 44.45 x 254.9 mm, or 1.655 L [A2], slightly more than the 1.62 L of TRL 2, because a thinner 3.175 mm (1/8 in) flange let the tube grow from 270 to 280 mm.
- **Mass.** The model's aluminium parts come to 1.665 kg, and seals, screws, plug, grip, label and adhesive add 0.115 kg, so the empty cartridge is 1.78 kg [A4, A5] against about 1.5 kg at TRL 2. The caps are the reason: a garage-built cap is a solid stack of flange, gland spacer and plug (about 100 cm³ each) rather than the milled, pocketed cap assumed at TRL 2.
- **Filled.** C5 2.89 kg, C25 2.90 kg and H70 2.96 kg, with 1.104, 1.119 and 1.180 kg of PCM [A6]. R4 (3.0 kg) is met with a thin margin; R5 is not met, at 38.3 to 39.9 % PCM.

## B. Usable storage per grade (R1, R3)

R1 is met for C5 and H70. RT 25 HC melts over 22 to 26 °C, so its melt starts 2 K below the 24 to 27 °C band set for C25; either the band or the product needs a second look (at risk).

*Table 2. Storage within ±3 K of the melt point [B1].*

| Grade | PCM | Latent (low side) | Usable in band | Per cartridge | At nominal datasheet value |
| --- | --- | --- | --- | --- | --- |
| C5 | 1.104 kg | 201.2 kJ/kg | 213.2 kJ/kg | **65.4 Wh** | 71.2 Wh |
| C25 | 1.119 kg | 182.8 kJ/kg | 194.8 kJ/kg | **60.5 Wh** | 65.9 Wh |
| H70 | 1.180 kg | 210.5 kJ/kg | 222.5 kJ/kg | **72.9 Wh** | 79.3 Wh |

- All three grades meet R3 (60 Wh). The TRL 2 figures (55, 61 and 67 Wh) used assumed usable heats of 180, 200 and 220 kJ/kg; the datasheets support more for C5 and H70 and less for C25.
- Energy density on filled mass is 22.7, 20.9 and 24.6 Wh/kg [B2].
- **2 mm wall (D5).** A metric 150 x 50 x 2 mm tube of the same length holds 1.712 L, only 3.5 % more, and would raise C5 to 67.7 Wh [B3]. Section C shows its walls would yield. It is not needed for R3 and is not adopted.

## C. Pressure and wall stress (R8, D5)

Filling as liquid at the grade's maximum operating temperature fixes the gauge pressure at zero at that temperature. Everything colder makes a partial vacuum, because the PCM shrinks by about 12 % on freezing and the trapped air cools.

*Table 3. Gauge pressure with 10 % ullage [C1].*

| Grade | Sealed at | Solid at -25 °C | 20 K above the limit |
| --- | --- | --- | --- |
| C5 | 45 °C | -0.63 bar (ullage 20.8 %) | +0.29 bar at 65 °C |
| C25 | 65 °C | -0.68 bar (ullage 22.1 %) | +0.29 bar at 85 °C |
| H70 | 90 °C | -0.64 bar (ullage 18.5 %) | +0.29 bar at 110 °C |

- **R8 is met**: 0.00 bar at the fill temperature by construction and +0.29 bar even 20 K beyond the datasheet limit, against 0.5 bar [C2].
- **Walls.** Treating the tube as a closed frame loaded on all four walls, the corner bending stress is 56 MPa at -0.68 bar, 83 MPa at full vacuum and 24 MPa at +0.29 bar, against an allowable of 73 MPa [C3]. The 3.175 mm wall carries the worst service vacuum with margin. Full vacuum could only arise in a cartridge sealed with no air; it would exceed the allowable stress but not the yield. The broad faces deflect about 0.8 mm inward at -0.68 bar [C5].
- **2 mm wall (D5).** The same vacuum gives 141 MPa, 1.28 times the minimum yield; its allowable pressure is only 0.35 bar [C4]. Rejected.
- **Caps.** At +0.29 bar each cap carries 190 N, 32 N per radial M5 screw [C6]. Under vacuum the flange bears on the tube end.
- **Drop (R6, indicative).** A molten cartridge dropped 1 m end-on and stopping in 4 mm decelerates at about 250 g; if the gas ullage did not cushion the liquid, the surge could reach 5.0 bar on the lower cap, 541 N per screw [C7]. The screws have ample capacity (M5 A2-70 proof load about 6,400 N), but that surge is ten times the service pressure on the walls and the O-ring. R6 needs a drop test at TRL 4.

## D. Hold times (R10, R11)

The outer area is 0.1138 m² of tube, 0.0503 m² of fins and 0.0155 m² of end faces, 0.1526 m² effective [D1].

**R10 is not met.** Two C5 cartridges store 131 Wh within the band, enough for 9.7 h at the 13.5 W leak [D2], so energy is not the limit. The limit is heat transfer from the cooler air into the cartridges. With mill-finish aluminium, still air gives only about 3.3 W/(m²·K), 0.50 W/K per cartridge, so the contents settle near 14 °C while the PCM melts and leave the 2 to 8 °C band after 1.9 h at 32 °C [D3] (2.8 h at 25 °C [D4]). A dark painted or anodized finish (emissivity 0.9) raises the coupling to 1.11 W/K and the hold to 2.4 h; the band then holds indefinitely while the PCM melts only below about 19 °C ambient [D3]. A third cartridge gives 3.4 h [D5]. The model does not credit produce lying directly on the cartridges, which is how ice packs are used and which would help, so this is a pessimistic bound; but the 8 h target cannot be shown on paper.

**R11 is met.** One H70 cartridge charged to 85 °C keeps 4 kg of food from 75 °C at 63 °C or more for 7.2 h with a bare finish and 13.6 h with a dark finish [D6]. The food alone would last 4.9 h [D7], so the cartridge adds at least 2.3 h. The hot case works because the H70 cartridge runs about 7 K above the food and radiation is stronger at 70 °C.

## E. Recharge (R12)

A quasi-steady Stefan model adds the resistance of the growing layer of changed PCM (k 0.2 W/(m·K), up to 22 mm from each broad face) to the air-side film.

*Table 4. Recharge time [E1, E2, E3].*

| Case | Bare finish | Dark finish | R12 (8 h) |
| --- | --- | --- | --- |
| C5 from 8 °C in a -18 °C freezer | 5.6 h | 4.2 h | Met |
| C5 in a 2 °C refrigerator | 51.1 h | 31.4 h | Not practical |
| C25 from 28 °C in a -18 °C freezer | 2.8 h | 2.1 h | Met |
| C25 in a 4 °C refrigerator | 6.6 h | 4.6 h | Met |
| H70 from 25 °C in a fan oven at 85 °C | 6.1 h | 5.3 h | Met |
| H70 on a 60 W pad | 2.7 h if the heat reaches the PCM; up to 10.3 h if the melt must conduct upward from a 90 °C base | | At risk |

- Charging C5 in a refrigerator, one option in the TRL 2 open questions, would take one to two days, so freezer charging with a conditioning step is the practical route (open item O3).
- The TRL 2 figure of about 2.5 h on a 60 W pad assumed the heat is absorbed as fast as it is supplied. It needs 130 Wh [E3]; paraffin conducts poorly, and the pad must never push the base above the RT 70 HC limit of 90 °C, so the true time lies between 2.7 and 10.3 h and depends on convection in the melt. This is a question for a TRL 4 test.
- **R12 target correction.** The TRL 2 target allowed an oven "at 100 °C or less", which is above the 90 °C maximum operating temperature of RT 70 HC. TCT-REQ-001 v0.3 now says 85 °C, never above 90 °C.
- The energy flow of one pad charge is 162 Wh in, 130 Wh stored between 25 and 80 °C, 88 Wh released above 63 °C and 42 Wh below it, with 32 Wh lost at the pad [E4] (Figure 2 of TCT-PRC-001).

## F. Handle temperature (R14)

- **Thermal break.** Each bail lug sits on a 3 mm phenolic washer. The two washers conduct 0.032 W/K and the bail loses 0.069 W/K to the air, so a bail on a cartridge at 71 or 80 °C settles at 39.6 or 42.5 °C [F1], below the assumed 55 °C bare-metal threshold [F3].
- **Straight from the oven** the bail is at oven temperature, 85 °C. With a 10 min time constant it falls below 55 °C after about 12 min [F2]. The silicone grip is also at 85 °C at first, above the assumed 70 °C threshold for rubber.
- R14 is **at risk**: met for pad charging and after a 12 min wait, not met for a cartridge lifted straight out of an oven. A handling rule (oven gloves, or wait) is proposed in `docs/REVIEW.md`, awaiting Amish. C5 and C25 never exceed 65 °C and meet R14.

## G. Grade keying (R9)

Key tabs 30 mm wide sit at -43, 0, +43 and -61 mm (C5, C25, H70, W0), and each frame slot is 3 mm wider than its key on each side. Every pairing was checked: each frame accepts only its own grade [G1]. The W0 key overlaps the C5 slot but cannot pass it.

## H. Cost and budget (R16)

- One cartridge costs $71.00 against the $50 target and one frame $16.00 against $20 [H1]. The TRL 2 estimate of $49 left out the fin bar, priced the caps as simple plates and used a lower tube price; all figures remain indicative, not quoted.
- Decision D6 keeps the $80 budget for one C5 cartridge and one frame. That build is $87.00, $7.00 over [H1]. A set of one cartridge per grade and one frame would be about $230 [H2]. PCM at $20/kg instead of $10/kg would add $11 per cartridge [H3].
- The build uses plates cut and filed and bars bonded with epoxy, with no milling; the frame needs a hand brake, available at a makerspace.

## I. Results against every requirement

*Table 5. Requirement status from this note [S1 and sections A to H].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R5 | Efficient use of mass | 38.3 to 39.9 % PCM [A6] | 50 % or more | **Not met** |
| R10 | Cold-chain hold time | 1.9 h bare, 2.4 h dark finish, at 32 °C; energy alone 9.7 h [D2, D3] | 8 h at 2 to 8 °C | **Not met** |
| R16 | Low cost, garage-buildable | $71 per cartridge, $16 per frame; no milling [H1] | $50 and $20 | **Not met** (cartridge) |
| R12 | Recharge with common equipment | C5 freezer 5.6 h, C25 refrigerator 6.6 h, H70 oven 6.1 h; H70 pad 2.7 to 10.3 h [E1 to E3] | 8 h or less | **At risk** (pad) |
| R14 | Safe to handle when charged | Bail 42.5 °C on pad charge; 85 °C for about 12 min after an oven [F1, F2] | Below the 10 s burn threshold | **At risk** (H70 from oven) |
| R1 | Standard grades | RT 5 HC 5 to 6 °C, RT 70 HC 69 to 71 °C; RT 25 HC 22 to 26 °C (datasheets) | C5 4 to 6, C25 24 to 27, H70 68 to 72 °C | **At risk** (C25) |
| R6 | Sealed for life | Seal design reviewed; drop surge up to 5.0 bar flagged [C7] | No leak over 1,000 cycles and a 1 m drop | Not verifiable at TRL 3 |
| R7 | Long life | Paraffins plausible; supplier cycling data not yet checked | 1,000 cycles, under 10 % loss | Not verifiable at TRL 3 |
| R17 | Open and documented | Envelope, key and grade tables published (TCT-DWG-001, this note); fill recipe waits for TRL 4 | Published under CERN-OHL-S-2.0 | Not verifiable at TRL 3 (partly met) |
| R3 | Stored energy | C5 65.4, C25 60.5, H70 72.9 Wh [B1] | 60 Wh or more | Met (C25 thin) |
| R4 | One-hand carry | 2.89 to 2.96 kg [A6] | 3.0 kg or less | Met (thin) |
| R8 | No pressure hazard | 0.00 bar at fill temperature; +0.29 bar 20 K over the limit; walls 56 MPa under vacuum [C1 to C3] | 0.5 bar or less, 10 % ullage | Met |
| R11 | Hot-holding time | 7.2 h [D6] | 4 h at 63 °C or more | Met |
| R2 | Common envelope | 323.4 x 152.4 x 63.5 mm [A1] | GN 1/3, 65 mm | Met |
| R9 | Wrong grade cannot fit | All pairings rejected [G1] | Keyed | Met by design |
| R13 | State visible | Sight window over a PCM vial | Readable at a glance | Met by design |
| R15 | Compatible materials | Aluminium, FKM, epoxy rated 120 °C or more, paraffin only | No corrosion or swelling | Met by design (paraffins) |
| R18 | Recoverable | G 3/4 port drains the melt; fill named on label | Drain and reuse | Met by design |

Counts: 3 not met, 3 at risk, 3 not verifiable at TRL 3, 9 met (5 by calculation, 4 by design).

## Checks against the TRL 2 figures

*Table 6. TRL 2 claims checked.*

| TRL 2 claim (TCT-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| 322 x 152 x 61 mm | 323.4 x 152.4 x 63.5 mm with the folding bail and stock 6.35 mm fin bar | Precis and README updated |
| 1.62 L, about 1.1 kg PCM | 1.655 L; 1.10 to 1.18 kg | Updated |
| C5 55, C25 61, H70 67 Wh | 65.4, 60.5, 72.9 Wh | Updated; R3 now met for C5 |
| About 2.6 kg filled, 42 % PCM | 2.89 to 2.96 kg, 38 to 40 % | Updated; R4 thin, R5 further from target |
| Two C5 hold a 25 L cooler for about 8.1 h | Energy lasts 9.7 h, but air-side coupling limits the hold to 1.9 to 2.4 h | R10 changed from at risk to not met |
| One H70 holds a GN carrier for about 6 h | 7.2 h | Updated |
| C5 recharge 4 to 8 h in a freezer; H70 2.5 h on a pad | 5.6 h; 2.7 to 10.3 h | Updated; pad at risk |
| Charge H70 at 100 °C or less | RT 70 HC limit is 90 °C | R12 target and safety text corrected |
| About $49 per cartridge, $15 per frame | $71 and $16 | R16 changed from met to not met |
