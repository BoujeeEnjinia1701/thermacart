---
doc_id: TCT-DDR-001
title: ThermaCart TRL 2 review decisions
project: ThermaCart
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, the items that remain open, and the TRL 3 refinements that follow from TCT-CAL-001
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "O1 to O3 decided by Amish on 2026-10-02 (TCT-DEC-001, items 4 to 6)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish accepted all recommendations ("i accept all your recommendations, go with them across all repos"). Items D1 to D8, T1 to T4 and O4 to O9 are decided by Amish, going with the recommendation; items O1 to O3 had no recommendation at this record and were decided by Amish on 2026-10-02 (TCT-DEC-001, items 4 to 6): "i approve your recommendations for all 555 open decisions." See TCT-DDR-002.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", and the design precis TCT-PRC-001 v0.2 listed six key design choices, each with options and, for most, a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". At first every item that carried a recommendation was adopted as recommended for TRL 3 under that instruction and left open for his review. Later on 2026-09-25 Amish accepted all recommendations across all repos, so those items are now decided (TCT-DDR-002). Items without a recommendation stay "Proposed, awaiting Amish".

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in TCT-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided by Amish, 2026-09-25.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| D1 | Envelope | Option (a): a stock 6 x 2 x 1/8 in aluminium tube sized to a GN 1/3 slot; the WHO PQS 0.6 L envelope (b) kept as a later small size, a custom finned extrusion (c) only at volume | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Grades | C5, C25 and H70 in organic paraffin; water (W0) as a produce-only option; salt hydrates deferred to a lined variant; C5 is the first build | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Pitch wording | Option (b): "cold chain, comfort and hot holding" instead of "cold chain, comfort and cooking", because the H70 grade holds cooked food hot and does not cook. Applied to `project.yaml` and `README.md` | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Grade keying and indicator | Mechanical nose key per grade, key table published as part of the open standard; passive sight window over a vial of the same PCM rather than a thermochromic strip | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Closing the C5 gaps | Evaluate a 2 mm wall at TRL 3. Done in TCT-CAL-001: the 2 mm wall adds 3.5 % volume and would reach 1.28 times the minimum yield under the vacuum of a frozen cartridge, so it is not adopted; with verified datasheet values C5 meets R3 (65.4 Wh) on the 3.175 mm tube | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Budget | Option (a): keep `budget_usd` at $80 for one C5 cartridge and one frame; the three-grade set is outside the budget. No new budget figure was recommended, so `budget_usd` is unchanged. TCT-CAL-001 prices that build at $87, $7 over (see O6) | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | First host type | A produce cooler user, reached through a local partner, because R10 is the tightest requirement. Only the host type is adopted; no partner is named | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Fill and shell | Fill hot and seal for life (now: fill as liquid at each grade's maximum operating temperature); aluminium shell for paraffins, no HDPE | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. TRL 3 refinements made within D1, D4, D6 and D8 because of TCT-CAL-001; decided by Amish, 2026-09-25: go with recommendation.*

| # | Refinement | Reason |
| --- | --- | --- |
| T1 | Folding bail handle on phenolic thermal-break washers, stowed within the GN 1/3 length, in place of the fixed handle | The fixed handle left about 14 mm of finger room; the bail gives 39 mm and keeps R2 (323.4 mm) |
| T2 | Caps built as a stack of 3.175 mm flange, 3 mm gland spacer and 9.525 mm plug, with a spliced FKM cord O-ring in the corner gland and six radial M5 screws; tube lengthened from 270 to 280 mm | Garage-buildable without milling (R16); the thinner flange frees length for PCM |
| T3 | Fins from stock 6.35 x 1.59 mm (1/4 x 1/16 in) 6063 flat bar | Stock section; overall height 63.5 mm, within 65 mm |
| T4 | R12 target corrected from an oven "at 100 °C or less" to "at 85 °C, never above 90 °C"; storage limits of 45 °C (C5) and 65 °C (C25) added to the safety text | Rubitherm datasheet maximum operating temperatures |

*Table 3. Items listed as open at v0.1, with their status after Amish's 2026-09-25 decision (TCT-DDR-002).*

| # | Item | Status |
| --- | --- | --- |
| O1 | The named co-design partner and region for the first produce cooler host. No recommendation was made beyond the host type in D7 | Decided by Amish, 2026-10-02 (TCT-DEC-001, item 4): a produce cooler user through a postharvest extension partner; first candidate to approach, the UC Davis Postharvest Technology Center. Nothing is agreed. |
| O2 | Whether ColdPod or ZeerBox should declare ThermaCart as a dependency. No recommendation was made; neither repo is in this batch and neither was changed | Decided by Amish, 2026-10-02 (TCT-DEC-001, item 5): neither declares ThermaCart as a dependency now. |
| O3 | C5 charging: freezer with a conditioning step, or a refrigerator at 0 to 2 °C. No recommendation was made at TRL 2; TCT-CAL-001 shows refrigerator charging takes 31 to 51 h | Decided by Amish, 2026-10-02 (TCT-DEC-001, item 6): domestic freezer followed by the conditioning step, with the conditioning time printed on the C5 label as a required step. |
| O4 | R5 (PCM fraction 38 to 40 % against 50 %): relax the target for the stock-tube build, or keep it for a later extrusion | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |
| O5 | R10 (cold hold about 2 h against 8 h): dark finish, contact with the load, more cartridges, or a revised requirement | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |
| O6 | R16 and budget: $71 per cartridge against $50, and $87 for the D6 build against $80 | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |
| O7 | R14: handling rule for an H70 cartridge taken straight from an oven | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |
| O8 | Surface finish of the shell (mill finish or dark paint or anodizing), which affects R10, R11 and R12 | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |
| O9 | R1 for C25: widen the C25 melt band to 22 to 27 °C, or look for a paraffin that melts within 24 to 27 °C | Decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002) |

## Consequences

- `project.yaml`: pitch reworded under D3; TRL fields set to 3. `budget_usd` stays at $80 and `problem` is unchanged.
- TCT-PRB-001, TCT-PRC-001 and TCT-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed"; they carry the D1 to D8 wording. Requirement changes: R12's oven temperature (T4) and a note under R16 that the $80 budget covers one C5 cartridge and one frame (D6). No other target is relaxed.
- TCT-CAL-001 v0.1 found R5, R10 and R16 not met and R1 (C25 melt band), R12 and R14 at risk. The options for each were decided by Amish on 2026-09-25 (TCT-DDR-002); TCT-CAL-001 v0.2 gives the status after those decisions.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
