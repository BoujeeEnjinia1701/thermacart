---
doc_id: TCT-DDR-002
title: ThermaCart recommendations accepted
project: ThermaCart
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. The front matter status stays Draft because the documentation standard allows only Draft, In review, Released or Superseded.

## Context

The TRL 3 session recorded items D1 to D8 and T1 to T4 in TCT-DDR-001 as "adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review", and items O1 to O9 as "Proposed, awaiting Amish" (`docs/REVIEW.md`, session 2026-09-25, TRL 3). On 2026-09-25 Amish wrote in chat: "i accept all your recommendations, go with them across all repos." Every item that carries a recommendation is therefore decided, and where a recommendation named one of several options, that option is the decision. Items without a recommendation stay open.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Envelope | Stock 6 x 2 x 1/8 in tube in a GN 1/3 envelope; WHO PQS 0.6 L size later; extrusion only at volume | Status wording only; the design already followed it |
| D2 | Grades | C5, C25 and H70 paraffins, W0 produce-only option, C5 first | Status wording only |
| D3 | Pitch | "Cold chain, comfort and hot holding" | Already applied to `project.yaml` and `README.md`; no further change |
| D4 | Keying and indicator | Grade nose key, published key table, sight window | Status wording only |
| D5 | 2 mm wall | Evaluated and not adopted | Status wording only |
| D6 | Budget | Keep `budget_usd` at $80 for one C5 cartridge and one frame | `budget_usd` unchanged at $80 |
| D7 | First host type | A produce cooler user through a local partner | Status wording only; no partner named (O1) |
| D8 | Fill and shell | Fill as liquid at the grade limit, seal for life, aluminium shell, no HDPE | Status wording only |
| T1 to T4 | TRL 3 refinements | Folding bail on a thermal break, cap stack from plate, stock fin bar, 85 °C oven limit | Status wording only |
| O4 | R5, PCM fraction | Option (a): relax R5 to 38 % for the stock-tube build, with (c) 50 % kept as the target for a later extrusion | R5 in TCT-REQ-001 v0.4 restated; status from not met (38.3 to 39.9 % against 50 %) to met, thin (38.1 to 39.7 % against 38 %) |
| O5 | R10, cold hold | Option (a): dark finish plus user guidance to lay produce on the cartridges; R10 kept at 8 h until a test shows the contact effect | Guidance added to TCT-PRC-001 v0.4 (How it works); R10 target unchanged; hold 1.9 h (bare, v0.1 basis) to 2.4 h (dark, now the design case), still not met. The measurement is TRL 4 work: decided but on hold |
| O6 | R16 and budget | Option (b): get supplier quotes first; do not raise the budget until quotes are in | `budget_usd` stays $80. Getting quotes is a purchasing step: decided but on hold with TRL 4. R16 stays not met |
| O7 | R14, H70 from an oven | Adopt a handling rule on the label (oven gloves or a 12 min wait) and prefer pad charging | R14 restated with the rule; status from at risk to met with the handling rule; H70 label text, precis, safety text and drawing note updated |
| O8 | Surface finish | Dark finish | Row 1 of `bom/bom.csv` adds etch primer and matte black high-temperature paint ($24 to $29); `finish` parameter in `cad/src/model.py`; TCT-DWG-001 Rev P1 to P2 with a finish note; media re-rendered with a black shell; TCT-CAL-001 v0.2 uses emissivity 0.9 as the design case and adds 15 g of paint |
| O9 | R1, C25 band | Widen the C25 band to 22 to 27 °C | R1 restated; status from at risk to met |

## Effect on the numbers

*Table 2. Numbers before and after (TCT-CAL-001 v0.1 to v0.2).*

| Quantity | Before | After |
| --- | --- | --- |
| Cartridge parts cost | $71.00 | $76.00 |
| One C5 cartridge and one frame, against the $80 budget | $87.00 ($7 over) | $92.00 ($12 over) |
| Three-grade set plus one frame | about $230 | about $245 |
| Empty cartridge | 1.78 kg | 1.80 kg |
| Filled mass | 2.89 to 2.96 kg | 2.90 to 2.98 kg (R4 still met, thin) |
| PCM fraction | 38.3 to 39.9 % | 38.1 to 39.7 % |
| R10 hold, two C5 at 32 °C (design case) | 1.9 h bare | 2.4 h dark |
| R11 hold, one H70 (design case) | 7.2 h bare | 13.6 h dark |
| R12 C5 freezer, C25 refrigerator, H70 oven (design case) | 5.6, 6.6 and 6.1 h | 4.2, 4.6 and 5.3 h |
| Requirement counts | 3 not met, 3 at risk, 3 not verifiable, 9 met | 2 not met (R10, R16), 1 at risk (R12), 3 not verifiable (R6, R7, R17), 12 met |

## Items still open

*Table 3. Items with no recommendation, still "Proposed, awaiting Amish".*

| # | Item |
| --- | --- |
| O1 | The named co-design partner and region for the first produce cooler host |
| O2 | Whether ColdPod or ZeerBox should declare ThermaCart as a dependency |
| O3 | C5 charging: freezer with a conditioning step, or a refrigerator (TCT-CAL-001 shows 31 to 51 h in a refrigerator, which favours the freezer, but no recommendation was made) |

## Consequences

- Controlled documents bumped: TCT-PRB-001 v0.4, TCT-PRC-001 v0.4, TCT-REQ-001 v0.4, TCT-CAL-001 v0.2, TCT-DDR-001 v0.2. Drawing TCT-DWG-001 is at Rev P2.
- `project.yaml`: `budget_usd` stays at $80, `trl: 3` and `trl_target: 3`.
- No cross-repo action follows from these decisions; O2 has no recommendation and no other repo was changed.
- The R10 contact measurement and supplier quotes are TRL 4 work, on hold by Amish's instruction. Nothing in this record authorizes building, testing or purchasing.
