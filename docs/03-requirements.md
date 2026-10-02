---
doc_id: TCT-REQ-001
title: ThermaCart requirements
project: ThermaCart
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from TCT-CAL-001; R12 oven temperature corrected to the RT 70 HC limit; R16 budget scope per TCT-DDR-001 D6
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from TCT-CAL-001 v0.3 for the constructable design (TCT-DDR-003); R16 reported against the value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R9 status note: the low lip decided on 2026-10-02 (TCT-DDR-003 A1 (b)) is still to be designed"
---

# ThermaCart requirements

These are the requirements for the TC-L cartridge and its adapter frame. The targets were proposed at TRL 2, and the design choices behind them were decided by Amish on 2026-09-25 (TCT-DDR-001 and TCT-DDR-002). Under TCT-DDR-002 the C25 band of R1 is widened to 22 to 27 °C (O9), R5 is relaxed to 38 % for the stock-tube build with 50 % kept as the target for a later extrusion (O4), and R14 carries a labelled handling rule for H70 cartridges taken from an oven (O7). R10 keeps its 8 h target (O5). The status column comes from TCT-CAL-001 v0.3, which uses the decided dark finish (O8) and the constructable design of TCT-DDR-003. One requirement is **not met** on paper (R10), one is **over its value-engineering target** (R16; `budget_usd` is a hypothetical control target, not a limit), one is **at risk** (R12), three can only be settled by tests (R6, R7 and R17) and twelve are met. No requirement text changed in v0.5.

Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 (TCT-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Offer a small set of standard temperature grades | At least three: C5 (melt 4 to 6 °C, cold chain), C25 (22 to 27 °C, comfort; widened from 24 to 27 °C by TCT-DDR-002, O9), H70 (68 to 72 °C, hot holding) | Material datasheets; later DSC test of each fill batch | Met: RT 5 HC 5 to 6 °C, RT 25 HC 22 to 26 °C, RT 70 HC 69 to 71 °C |
| R2 | Common envelope that fits kitchen and cooler formats | Fits a GN 1/3 slot: at most 325 x 176 mm footprint and 65 mm high, handle included | Model and drawing | Met: 323.4 x 152.4 x 63.5 mm with the bail stowed (TCT-DWG-001) |
| R3 | Enough stored energy per cartridge | 60 Wh (216 kJ) or more of usable storage within ±3 K of the melt point | Calculation per grade | Met: C5 65.4 Wh, C25 60.5 Wh (thin margin), H70 72.9 Wh |
| R4 | Carry with one hand | Filled mass 3.0 kg or less | Mass estimate, then weighing | Met, thin margin: 2.90 to 2.98 kg |
| R5 | Efficient use of mass | PCM at least 38 % of filled mass for the stock-tube build; 50 % remains the target for a later custom extrusion (relaxed by TCT-DDR-002, O4) | Mass estimate | Met, thin margin: 38.1 to 39.6 % |
| R6 | Sealed for life | No leak through 1,000 thermal cycles and a 1 m drop onto concrete in any state | Seal design review at TRL 3; cycle and drop tests belong to TRL 4 | Not verifiable at TRL 3; an end-on drop of a molten cartridge could see a surge of up to 5 bar |
| R7 | Long life | 1,000 cycles or more with less than 10 % loss of latent capacity | Literature and supplier data at TRL 3 | Not verifiable at TRL 3; plausible for paraffins |
| R8 | No pressure hazard | Internal gauge pressure 0.5 bar or less at the highest charge temperature; ullage of at least 10 % of the inner volume at that temperature | Calculation | Met: 0.00 bar at the fill temperature, +0.29 bar at 20 K above the limit; wall stress 56 MPa under the cold vacuum |
| R9 | Wrong grade cannot be fitted | Each grade has its own nose key; a frame for one grade rejects the others | Design review of key geometry | Met by design for the keys: every pairing checked. In the current model a wrong grade stands 12 mm proud; the low lip that makes the frame reject it (decided by Amish, 2026-10-02, TCT-DDR-003 A1 (b)) is still to be designed |
| R10 | Cold-chain hold time | Two C5 cartridges keep a 25 L cooler (heat leak about 0.5 W/K, estimate) at 2 to 8 °C for 8 h or more at 32 °C ambient | Heat balance calculation | **Not met**: 2.4 h with the decided dark finish (1.9 h bare); the stored energy would last 9.7 h, but air-side heat transfer limits the hold. Produce laid directly on the cartridges (TCT-DDR-002, O5) is not credited and waits for a TRL 4 measurement, which is on hold |
| R11 | Hot-holding time | One H70 cartridge keeps food in an insulated GN carrier (about 0.25 W/K, estimate) at 63 °C or more for 4 h or more at 25 °C ambient | Heat balance calculation | Met: 13.6 h with the dark finish (7.2 h bare) |
| R12 | Recharge with common equipment | Full recharge in 8 h or less: C5 and C25 in a domestic freezer or refrigerator, H70 in an oven set to 85 °C (never above 90 °C) or on a 60 W heating pad | Calculation (Stefan problem plus fin convection) | **At risk**: with the dark finish, C5 freezer 4.2 h, C25 refrigerator 4.6 h, H70 oven 5.3 h; H70 pad 2.7 to 10.3 h |
| R13 | State of charge visible | Charged or melted state readable at a glance without tools | Design review | Met by design (clear melt indicator tube holding the same PCM, TCT-DDR-003) |
| R14 | Safe to handle when charged | Handle touch temperature below the ISO 13732-1 burn threshold for 10 s contact on every grade; for an H70 cartridge taken from an oven, the label states a handling rule (oven gloves, or wait 12 min) and pad charging is the preferred method (TCT-DDR-002, O7) | Calculation of handle temperature; label review | Met with the handling rule: bail on its thermal break (phenolic washers under the lug angles and the bolt heads) settles at 39.1 °C on pad charging; after an oven it is at 85 °C and falls below 55 °C in about 10 min, which the 12 min label rule covers |
| R15 | Materials compatible with each fill | No corrosion, swelling or permeation: aluminium shell with FKM or NBR seals for paraffins; coated shell or polymer liner for salt hydrates | Compatibility review against supplier data | Met by design for paraffin grades (epoxy rated 120 °C or more); open for salt hydrates |
| R16 | Low cost and garage-buildable | $50 or less in parts per cartridge and $20 or less per frame; stock sections, drill press and taps only. The $80 value-engineering target (`budget_usd`, a hypothetical control target) covers one C5 cartridge and one frame (TCT-DDR-001 D6) | Priced BOM | **Over the value-engineering target by $30** per cartridge: $80 with the dark finish and the parts added for construction; frame $17, $3 under its target; one cartridge and one frame $97, $17 over the $80 target (indicative prices; quotes wait with TRL 4, TCT-DDR-002, O6) |
| R17 | Open and documented | Envelope, key geometry, grade table and fill recipe published under CERN-OHL-S-2.0 | Repository review | Not verifiable at TRL 3; envelope, key and grade tables are published, the fill recipe waits for TRL 4 |
| R18 | Recoverable at end of life | Fill can be drained or melted out through the fill port and the shell reused; fill named on the label | Design review | Met by design |

## Assumptions

- PCM data from the Rubitherm datasheets for RT 5 HC, RT 25 HC and RT 70 HC, taken at the low side of their ±7.5 % tolerance; usable storage is the latent heat plus sensible heat within ±3 K of the melt point (TCT-CAL-001, Table 1).
- Fill of 1.10 to 1.18 kg: 90 % of a 1.655 L inner volume, filled as liquid at each grade's maximum operating temperature (45, 65 and 90 °C).
- Hot-holding threshold of 63 °C follows common food-safety practice (the US FDA Food Code uses 57 °C, 135 °F); the lower value would lengthen the hold time.
- Cooler and carrier heat leaks are estimates for typical polyurethane and EPP boxes and must be replaced with measured values from a partner's real boxes.
- The burn thresholds used for R14 (about 55 °C for bare metal and 70 °C for plastics, 10 s contact) are commonly quoted from ISO 13732-1 and have not been checked against the standard.
