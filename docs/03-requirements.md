---
doc_id: TCT-REQ-001
title: ThermaCart requirements
project: ThermaCart
doc_type: Requirements
version: "0.2"
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
  change: First measurable requirements for TRL 2, with status against the concept estimates
---

# ThermaCart requirements

These are first-pass requirements for the TC-L cartridge and its adapter frame. Targets are proposals for review, awaiting Amish. The status column compares them with the first-order estimates in the design precis (TCT-PRC-001); every estimate will be checked by calculation at TRL 3. Four requirements are **not met** or **at risk** on paper: R3 (C5 grade), R5, R10 and R14.

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Offer a small set of standard temperature grades | At least three: C5 (melt 4 to 6 °C, cold chain), C25 (24 to 27 °C, comfort), H70 (68 to 72 °C, hot holding) | Material datasheets; later DSC test of each fill batch | Met on paper (commercial PCMs exist for each grade) |
| R2 | Common envelope that fits kitchen and cooler formats | Fits a GN 1/3 slot: at most 325 x 176 mm footprint and 65 mm high, handle included | Model and drawing | Met: 322 x 152 x 61 mm |
| R3 | Enough stored energy per cartridge | 60 Wh (216 kJ) or more of usable storage within ±3 K of the melt point | Calculation per grade | **Not met for C5** (about 55 Wh); C25 about 61 Wh (thin margin); H70 about 67 Wh |
| R4 | Carry with one hand | Filled mass 3.0 kg or less | Mass estimate, then weighing | Met: about 2.6 kg |
| R5 | Efficient use of mass | PCM at least 50 % of filled mass | Mass estimate | **Not met**: about 42 % with the stock 3.18 mm tube |
| R6 | Sealed for life | No leak through 1,000 thermal cycles and a 1 m drop onto concrete in any state | Seal design review at TRL 3; cycle and drop tests belong to TRL 4 | Not yet assessed |
| R7 | Long life | 1,000 cycles or more with less than 10 % loss of latent capacity | Literature and supplier data at TRL 3 | Plausible for paraffins; unassessed for salt hydrates |
| R8 | No pressure hazard | Internal gauge pressure 0.5 bar or less at the highest charge temperature; ullage of at least 10 % of the inner volume at that temperature | Calculation | Plausible (filled hot, estimate); to be calculated |
| R9 | Wrong grade cannot be fitted | Each grade has its own nose key; a frame for one grade rejects the others | Design review of key geometry | Met in concept |
| R10 | Cold-chain hold time | Two C5 cartridges keep a 25 L cooler (heat leak about 0.5 W/K, estimate) at 2 to 8 °C for 8 h or more at 32 °C ambient | Heat balance calculation | **At risk**: about 8.1 h, no margin |
| R11 | Hot-holding time | One H70 cartridge keeps food in an insulated GN carrier (about 0.25 W/K, estimate) at 63 °C or more for 4 h or more at 25 °C ambient | Heat balance calculation | Met: about 6 h |
| R12 | Recharge with common equipment | Full recharge in 8 h or less: C5 and C25 in a domestic freezer or refrigerator, H70 in an oven at 100 °C or less or on a 60 W heating pad | Calculation (Stefan problem plus fin convection) | At risk for C5 (4 to 8 h, estimate); H70 about 2.5 h |
| R13 | State of charge visible | Charged or melted state readable at a glance without tools | Design review | Met in concept (sight window on a PCM vial) |
| R14 | Safe to handle when charged | Handle touch temperature below the ISO 13732-1 burn threshold for 10 s contact on every grade | Calculation of handle temperature | **Not met for H70** with a bare aluminium handle; insulated grip proposed |
| R15 | Materials compatible with each fill | No corrosion, swelling or permeation: aluminium shell with FKM or NBR seals for paraffins; coated shell or polymer liner for salt hydrates | Compatibility review against supplier data | Met for paraffin grades; open for salt hydrates |
| R16 | Low cost and garage-buildable | $50 or less in parts per cartridge and $20 or less per frame; stock sections, drill press and taps only | Priced BOM | Met, thin margin: about $49 per cartridge, about $15 per frame (indicative) |
| R17 | Open and documented | Envelope, key geometry, grade table and fill recipe published under CERN-OHL-S-2.0 | Repository review | In progress |
| R18 | Recoverable at end of life | Fill can be drained or melted out through the fill port and the shell reused; fill named on the label | Design review | Met in concept |

## Assumptions

- Usable latent storage within the working band: 180 kJ/kg for C5, 200 kJ/kg for C25 and 220 kJ/kg for H70, below the 250, 230 and 260 kJ/kg that Rubitherm quotes for its RT 5 HC, RT 25 HC and RT 70 HC grades, which include sensible heat over a wider band ([Rubitherm](https://www.rubitherm.eu/en/productcategory/organische-pcm-rt)).
- Fill of about 1.1 kg: 90 % of a 1.62 L inner volume, filled as liquid at the top of the grade's service temperature, at a liquid density of about 0.77 kg/L (estimate for paraffins).
- Hot-holding threshold of 63 °C follows common food-safety practice (the US FDA Food Code uses 57 °C, 135 °F); the lower value would lengthen the hold time.
- Cooler and carrier heat leaks are estimates for typical polyurethane and EPP boxes and must be replaced with measured values from a partner's real boxes.
