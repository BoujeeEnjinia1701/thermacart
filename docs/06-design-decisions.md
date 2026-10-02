---
doc_id: TCT-DEC-001
title: ThermaCart design decisions register
project: ThermaCart
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, the decision records and the build plan work; budget treated as a value-engineering target
---

# ThermaCart design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | How a wrong grade is shown to be rejected by the frame (R9; touches the safety case for frozen W0 or hot H70 cartridges in a cold-chain box) | (a) accept the 12 mm stand-off of a wrong grade and check at TRL 4 that the host's lid will not close on it; (b) a low lip at the frame's open end, with the stowed grip moved up; (c) a sprung detent in the stop | (a) for the prototype; (b) if the TRL 4 check fails | Adapter frame (build plan 3.10) and, for (b), the bail | TCT-DDR-003, A1 |
| 2 | W0 key fixing and frame slot | (a) for W0, screws 4 mm each side of the key centre and a shorter corner tab on the W0 frame; (b) move the W0 key position in the published key table | (a), when W0 is sized | Not part of the C5 prototype | TCT-DDR-003, A2 |
| 3 | R5 margin of 0.1 percentage point (38.1 % against 38 %) | (a) accept and weigh at TRL 4; (b) save mass now (tubular bail rod, thinner plugs with M4 radial screws) | (a) | None for (a) | TCT-DDR-003, A3 |
| 4 | Named co-design partner and region for the first produce cooler | Any produce cooler user through a local partner (host type decided, D7) | None made | Not part of the TRL 3 build | TCT-DDR-001, O1 |
| 5 | Whether ColdPod or ZeerBox declares ThermaCart as a dependency | Declare in one, both or neither | None made | None | TCT-DDR-001, O2 |
| 6 | How C5 cartridges are charged | (a) domestic freezer with a conditioning step (4.2 h); (b) refrigerator at 2 °C (31 to 51 h) | None made; the calculations favour (a) | Charging in the first checks of the build plan | TCT-DDR-001, O3 |
| 7 | Grade colour band round the nose end (appearance model) | (a) a painted 18 mm band, a masking step in BOM line 1; (b) a colour-coded wrap label | (a) | Painting of the shell | REVIEW.md, 2026-09-26, item 1 |
| 8 | Painted side marking "ThermaCart, TC-L C5" | Adopt as part of the label set, or leave out | Adopt (BOM line 6) | Label set | REVIEW.md, 2026-09-26, item 2 |
| 9 | Frame grade decal and rubber feet | Decal and feet, decal only, or neither | Decal only; feet are host-specific | Adapter frame | REVIEW.md, 2026-09-26, item 3 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The tube's outside and inside corner radii (3/16 and 1/16 in assumed) and its actual bore at both ends | The spacer and plug are cut to the bore and their corners follow the inside radius; the O-ring squeeze depends on it | TCT-DDR-003, P2, P11; REVIEW.md 2026-09-26, item 5 |
| 2 | FKM O-ring cord 2.5 mm is stocked, and the splicing method (cyanoacrylate splice or a vulcanised ring) for a 361 mm loop | The gland is sized for 2.5 mm cord | TCT-DDR-003, P2 |
| 3 | M5 FKM bonded sealing washers fit the button-head screws' heads | They seal the radial screw holes | TCT-DDR-003, P3 |
| 4 | A G 1/2 anodised aluminium plug with collar and a matching FKM bonded seal | The fill port seal and the R5 mass both assume it | TCT-DDR-003, P1 |
| 5 | The structural epoxy is rated to 120 °C or more and is listed as resistant to paraffins | It bonds the fins, the cap stacks and the indicator, and seals the stack joints | TCT-PRC-001; TCT-DDR-003, P4 |
| 6 | The clear polycarbonate tube grade is rated above 90 °C and stays clear with the H70 paraffin | The H70 indicator sits on a cartridge at up to 90 °C | TCT-DDR-003, P9 |
| 7 | The high-temperature paint is rated well above 90 °C, and its curing temperature | The finish (O8); some paints need an oven cure that must not reach a filled cartridge | TCT-DDR-002, O8 |
| 8 | Phenolic (paper or cotton laminate) sheet 3 mm for the washers | The thermal break is sized on phenolic's conductivity | TCT-CAL-001, F1 |
| 9 | Supplier quotes for every BOM line | All prices are indicative | TCT-DDR-002, O6 |

## Value engineering

Value-engineering target: USD 80 for one C5 cartridge and one adapter frame (a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 97 (USD 17 over the target): the cartridge USD 80 against its USD 50 target in R16, and the frame USD 17 against its USD 20 target. Main cost drivers and savings worth trying:

- The largest lines are the shell (tube, fin bar and paint, USD 29), the two cap stacks (USD 14), the frame (USD 17), the PCM (USD 11 at USD 10/kg for the first build) and the hardware (USD 11).
- Making the design constructable added USD 5 to the cartridge (bonded seals, bolts, phenolic washers) and USD 1 to the frame (rivets), less USD 1 for the smaller fill plug.
- Savings worth trying: buy tube, plate and fin bar for a batch of cartridges (offcuts and cut-to-length charges dominate a one-off); stainless hardware from a bulk supplier rather than a hardware store; paint several cartridges from one set of aerosol cans; a frame without side walls where the host already guides the cartridge; quotes for PCM in 10 kg lots. Dropping the fins (about USD 8) would cost hold and charge time (R10, R12) and is not recommended.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D8: GN 1/3 envelope from a stock tube; C5, C25 and H70 paraffins with W0 as an option, C5 first; pitch "cold chain, comfort and hot holding"; grade keying and a passive indicator; 2 mm wall not used; one C5 cartridge and one frame for the prototype; produce cooler as first host type; fill hot and seal for life in aluminium | Amish: "i accept all your recommendations, go with them across all repos." | TCT-DDR-001, TCT-DDR-002 |
| 2026-09-25 | T1 to T4: folding bail on a thermal break, cap stack from plate, stock fin bar, 85 °C oven limit | Amish, same instruction | TCT-DDR-001, TCT-DDR-002 |
| 2026-09-25 | O4 to O9: R5 38 % for the stock tube; dark finish and produce on the cartridges for R10; quotes before any cost change; H70 oven handling rule; matte black finish; C25 band 22 to 27 °C | Amish, same instruction | TCT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan: changes P1 to P11 (fill port, O-ring gland, sealed radial screws, bonded cap stack, bolted lug angles and bail, key tab fixing, frame stop, frame corners, melt indicator, fin bond, tube radii), made under this instruction and open for review | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | TCT-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a spending limit; cost requirements are reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | TCT-CAL-001 v0.3, section H |
