---
doc_id: TCT-DEC-001
title: ThermaCart design decisions register
project: ThermaCart
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, the decision records and the build plan work; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all nine open decisions on 2026-10-02 (TCT-DDR-003 Table 3 accepted, A1 as option (b)); moved to decisions made"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Design for construction (TCT-DDR-003, Tables 1 and 2) accepted by Amish on 2026-10-02; added to decisions made"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Value engineering updated for the approved follow-ups (USD 100 against the USD 80 target)"
---

# ThermaCart design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

Value-engineering target: USD 80. Estimated cost of the constructable design: USD 100 (USD 20 over the target). The target covers one C5 cartridge and one adapter frame (a hypothetical control target, not a limit; Amish, 2026-10-01): the cartridge is USD 82.50 against its USD 50 target in R16, and the frame USD 17.50 against its USD 20 target. Main cost drivers and savings worth trying:

- The largest lines are the shell (tube, fin bar, paint and grade band, USD 30.50), the two cap stacks (USD 14), the frame (USD 17.50), the PCM (USD 11 at USD 10/kg for the first build) and the hardware (USD 11).
- Making the design constructable added USD 5 to the cartridge (bonded seals, bolts, phenolic washers) and USD 1 to the frame (rivets), less USD 1 for the smaller fill plug. The decisions of 2026-10-02 added USD 1.50 for the masked grade band, USD 1 for the painted side marking and USD 0.50 for the frame decal; the lip is folded from the same blank and adds no cost.
- Savings worth trying: buy tube, plate and fin bar for a batch of cartridges (offcuts and cut-to-length charges dominate a one-off); stainless hardware from a bulk supplier rather than a hardware store; paint several cartridges from one set of aerosol cans; a frame without side walls where the host already guides the cartridge; quotes for PCM in 10 kg lots. Dropping the fins (about USD 8) would cost hold and charge time (R10, R12) and is not recommended.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D8: GN 1/3 envelope from a stock tube; C5, C25 and H70 paraffins with W0 as an option, C5 first; pitch "cold chain, comfort and hot holding"; grade keying and a passive indicator; 2 mm wall not used; one C5 cartridge and one frame for the prototype; produce cooler as first host type; fill hot and seal for life in aluminium | Amish: "i accept all your recommendations, go with them across all repos." | TCT-DDR-001, TCT-DDR-002 |
| 2026-09-25 | T1 to T4: folding bail on a thermal break, cap stack from plate, stock fin bar, 85 °C oven limit | Amish, same instruction | TCT-DDR-001, TCT-DDR-002 |
| 2026-09-25 | O4 to O9: R5 38 % for the stock tube; dark finish and produce on the cartridges for R10; quotes before any cost change; H70 oven handling rule; matte black finish; C25 band 22 to 27 °C | Amish, same instruction | TCT-DDR-002 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan: changes P1 to P11 (fill port, O-ring gland, sealed radial screws, bonded cap stack, bolted lug angles and bail, key tab fixing, frame stop, frame corners, melt indicator, fin bond, tube radii), made under this instruction; Table 3 and then Tables 1 and 2 accepted on 2026-10-02 (below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | TCT-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a spending limit; cost requirements are reported against it | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | TCT-CAL-001 v0.3, section H |
| 2026-10-02 | Wrong grade (R9): option (b). A low lip at the frame's open end is designed on paper now, with the stowed grip moved up to suit, so the frame physically rejects a wrong grade instead of leaving it 12 mm proud; fall back to (a) only if the TRL 4 check shows that no target host's lid can close on a proud cartridge | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-003, A1 |
| 2026-10-02 | W0 key: when W0 is sized, its key tab is fixed with screws 4 mm each side of its centre and that frame's corner tab is shortened; the published key table is unchanged | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-003, A2 |
| 2026-10-02 | R5 margin of 0.1 percentage point accepted; a filled prototype is weighed at TRL 4, and if it misses, the tubular bail rod is the first saving | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-003, A3 |
| 2026-10-02 | First host: a produce cooler user reached through a postharvest extension partner. First candidate to approach: the UC Davis Postharvest Technology Center, asked to introduce a grower group or market cooler operator that already uses passive or ice-based cooling | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-001, O1 |
| 2026-10-02 | Neither ColdPod nor ZeerBox declares ThermaCart as a dependency now; neither has a GN 1/3 slot, and the first host is the produce cooler of item 4 | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-001, O2 |
| 2026-10-02 | C5 is charged in a domestic freezer followed by the conditioning step (about 4.2 h), and the conditioning time is printed on the C5 label as a required step | Amish: "i approve your recommendations for all 555 open decisions." | TCT-DDR-001, O3 |
| 2026-10-02 | Grade colour band: an 18 mm painted band round the nose end, a masking step in BOM line 1 | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 1 |
| 2026-10-02 | Painted side marking "ThermaCart, TC-L C5" adopted as part of the label set (BOM line 6) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 2 |
| 2026-10-02 | "C5 ONLY" frame decal adopted; rubber feet are left to each host | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 3 |
| 2026-10-02 | Design for construction accepted: the changes in Tables 1 and 2 (P1 to P11 and their knock-on changes), as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [TCT-DDR-003](decisions/0003-design-for-construction.md), Tables 1 and 2 |
