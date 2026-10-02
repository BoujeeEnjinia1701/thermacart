# Review note: ThermaCart

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (TCT-PRB-001 v0.2): problem, why it matters (cited), users and context, prior work with links (Rubitherm, Pluss, WHO PQS E005 packs, solar direct-drive ice banks, Sunamp, RAL-GZ 896, Gastronorm), known material problems, constraints and out of scope. The file had no co-design checklist to keep.
- `docs/03-requirements.md` (TCT-REQ-001 v0.2): 18 measurable requirements (R1 to R18) with targets, planned verification and a status column against the concept estimates.
- `docs/02-concept.md` (TCT-PRC-001 v0.2): how it works, proposed grades, numbered components, first-order numbers with assumptions, design choices with options, safety section and open questions.
- `cad/src/concept_media.py`: massing model of one TC-L cartridge (C5 grade) in its adapter frame, seven BOM-numbered parts, with a table top and a 25 L cooler as the scale context (the cartridge is a small object, so no 1.75 m figure).
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts, `cutaway.png`, `flow.png` (energy per H70 charge cycle, all values labeled as estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: eight lines with indicative USD prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line, expanded Concept rationale, Burning platform (four cited figures), Where it could be used (5 industries, 6 countries or regions with cited facts), What sparked the idea (origin kept, WHO PQS trigger added), and updated Problem, Concept, Key components and Safety.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Overall size | 322 x 152 x 61 mm, fits a GN 1/3 slot | R2 met |
| PCM per cartridge | about 1.1 kg in 1.62 L | |
| Usable storage | C5 55 Wh, C25 61 Wh, H70 67 Wh | R3 **not met for C5**; C25 thin margin |
| Filled mass | about 2.6 kg | R4 met |
| PCM mass fraction | about 42 % | R5 **not met** (target 50 %) |
| Cold hold, two C5 in a 25 L cooler at 32 °C | about 8.1 h | R10 **at risk**, no margin |
| Hot hold, one H70 in a GN carrier at 25 °C | about 6 h at 63 °C or more | R11 met |
| Recharge | C5 about 4 to 8 h in a freezer; H70 about 2.5 h on a 60 W pad | R12 at risk for C5 |
| Handle temperature, H70 | bare aluminium handle near 75 °C | R14 **not met**; insulated grip proposed |
| Parts cost | about $49 per cartridge, $15 per frame, $64 for one of each | R16 met, thin margin; within the $80 budget |

Requirements not met or at risk: R3 (C5), R5, R10, R12 (C5) and R14 (H70). R6 (seal and drop) and R7 (cycle life for salt hydrates) are not yet assessed.

### Proposed, awaiting Amish (status updated 2026-09-25)

Items 1 to 7 are decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-001 D1 to D7, TCT-DDR-002). Item 8 had no recommendation and stays proposed, awaiting Amish (O2).

1. **Envelope.** (a) Stock 6 x 2 in aluminium tube sized to a GN 1/3 slot; (b) the WHO PQS 0.6 L pack envelope; (c) a custom finned extrusion. Recommendation: (a) now, (b) later as a small size, (c) only at volume.
2. **Grades.** C5, C25 and H70 in organic paraffin, with water (W0) as a produce-only option and salt hydrates deferred to a lined variant. Recommendation: adopt, and build C5 first (lowest hazard, links to ColdPod).
3. **Reading of "cooking" in the pitch.** The concept treats the cooking range as hot holding of cooked food at 70 °C; true cooking storage above 100 °C is out of scope. Options: (a) keep the pitch wording; (b) reword to "cold chain, comfort and hot holding". Recommendation: (b), a small pitch change that is Amish's to make. `project.yaml` was not changed.
4. **Grade keying and passive sight-window indicator.** Recommendation: adopt both and publish the key table as part of the open standard.
5. **Closing the C5 gaps (R3, R10, R5).** Options: thinner tube wall (3.18 to 2 mm), a taller tube within the 65 mm GN depth, or accept about 55 Wh for C5. Recommendation: evaluate a 2 mm wall at TRL 3.
6. **Budget.** The $80 covers one cartridge and one frame (about $64). A three-grade set with one frame is about $162. Options: (a) keep $80 and build one C5 cartridge; (b) raise to about $165 for all three grades. Recommendation: (a) for now; revisit before any build.
7. **Host and partner for co-design.** A produce trader or market cooler user, a caterer using GN carriers, or ColdPod as the first host. Recommendation: a produce cooler user through a local partner, because R10 is the tightest requirement.
8. **Dependencies.** Whether ColdPod or ZeerBox should adopt ThermaCart. No sibling README in this batch references ThermaCart, and no other repo was changed.

`project.yaml` is unchanged: `pitch` and `problem` are still correct, and budget, TRL, name, slug, area and licenses were not touched. No SwapCell pack is used or proposed.

### Safety concerns

- Paraffin fills are combustible: no charging on flame or above 100 °C; clear labels.
- H70 surfaces at about 75 °C: burn risk; R14 needs an insulated grip.
- Pressure: fill hot with 10 % ullage and never seal a partly molten H70 cartridge; R8 must be confirmed by calculation.
- C5 from a freezer is below 0 °C; not qualified for vaccines or medicines, and W0 must never be used with them.
- Salt hydrates corrode aluminium: not to be used in this shell.
- Sharp cut aluminium edges and a 2.6 kg mass.

### Recommended next step

Review this note and the media, and decide items 1 to 6. If approved, run `/advance-trl3` to calculate storage, hold times, charge times, handle temperature and internal pressure per grade (CAL), build the parametric model with STEP export and the drawing sheet, and price every BOM line.

## Session 2026-09-25: TRL 3

Amish asked for this batch to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item with a recommendation is adopted as recommended for TRL 3 under that instruction, open for his review, and items without one stay open. TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (TCT-DDR-001 v0.1): items D1 to D8 adopted as recommended for TRL 3, open for review; TRL 3 refinements T1 to T4; open items O1 to O9.
- `docs/04-calcs/01-sizing.md` (TCT-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: geometry and mass, storage per grade from the Rubitherm datasheets, pressure and wall stress (including the 2 mm wall of D5), hold times with a two-node heat model, recharge (Stefan model), handle temperature, keying and cost, with a results table for R1 to R18. The script imports the model and reads the BOM and `project.yaml`.
- `cad/src/model.py`: parametric build123d model (tube, fins, cap stacks, O-rings, screws, fill port, folding bail on a thermal break, grade key, label and window, adapter frame). Exports `cad/step/` and `cad/stl/`: `thermacart-assembly`, `tc-l-cartridge`, `end-cap`, `adapter-frame`.
- `cad/src/sheets.py` and `cad/drawings/TCT-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:2.5, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept blueprint keeps TCT-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced (indicative, not quoted) with a supplier type.
- `cad/src/concept_media.py` now builds from the model; all media refreshed (`hero`, `concept-blueprint` `.png`, `.pdf`, `.svg`, `exploded`, `cutaway`, `flow`, `model.glb`, `viewer.html`) and checked by eye. Temporary `media/_views*` folders removed. The kit's cutaway cuts at the mean Y of the parts; the cartridge is centred on the origin, so no shift was needed.
- TCT-PRB-001, TCT-PRC-001 and TCT-REQ-001 revised to v0.3; `README.md` and `project.yaml` updated (pitch reworded under D3; `trl: 3`, `trl_target: 3`, evidence listed). PDFs rebuilt in `docs/pdf/`.

### Requirements (TCT-CAL-001, Table 5)

Counts: 3 not met, 3 at risk, 3 not verifiable at TRL 3, 9 met.

| ID | Status | Value against target |
| --- | --- | --- |
| R5 | **Not met** | PCM 38.3 to 39.9 % of filled mass against 50 %; the solid cap stacks weigh about 0.27 kg each |
| R10 | **Not met** | Two C5 hold a 25 L cooler at 2 to 8 °C for 1.9 h (bare) or 2.4 h (dark finish) at 32 °C against 8 h. The stored energy (131 Wh) would last 9.7 h; the limit is heat transfer from the cooler air (about 0.5 to 1.1 W/K per cartridge). Direct contact with the load is not credited |
| R16 | **Not met** | $71 per cartridge against $50 (frame $16, met); the first C5 build is $87 against the $80 budget |
| R1 | At risk | RT 25 HC melts from 22 °C, below the 24 to 27 °C C25 band; C5 and H70 met |
| R12 | At risk | Freezer, refrigerator (C25) and 85 °C oven all within 8 h; a 60 W pad takes 2.7 to 10.3 h depending on convection in the melt |
| R14 | At risk | H70 bail 42.5 °C on its thermal break, but at 85 °C for about 12 min after an oven |
| R6, R7, R17 | Not verifiable at TRL 3 | Seal, drop (surge up to 5 bar flagged), cycle life and fill recipe need TRL 4 work |
| R2, R3, R4, R8, R11 | Met by calculation | 323.4 x 152.4 x 63.5 mm; C5 65.4, C25 60.5, H70 72.9 Wh; 2.89 to 2.96 kg (thin); 0 bar at fill, +0.29 bar over limit, 56 MPa wall stress; 7.2 h hot hold |
| R9, R13, R15, R18 | Met by design | Keying checked for every pairing; sight window; aluminium, FKM and 120 °C epoxy with paraffins; drain through the fill port |

Changes against TRL 2: C5 now meets R3 (verified datasheet values); R10 moved from at risk to not met; R16 from met to not met; mass rose from about 2.6 to 2.9 kg. The H70 charge limit was 100 °C in the TRL 2 documents; the RT 70 HC datasheet limit is 90 °C, and R12 and the safety text are corrected.

### Decisions recorded (TCT-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Now decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002):

- D1 stock 6 x 2 x 1/8 in tube in a GN 1/3 envelope; D2 C5, C25, H70 paraffins, W0 produce-only option, C5 first; D3 pitch reworded to "cold chain, comfort and hot holding" (applied to `project.yaml` and `README.md`); D4 grade keying with a published key table and a sight-window indicator; D5 2 mm wall evaluated and not adopted (it would yield under the cold vacuum and adds only 3.5 % volume); D6 `budget_usd` kept at $80 for one C5 cartridge and one frame (unchanged in `project.yaml`); D7 first host type a produce cooler user through a local partner; D8 fill as liquid at the grade limit and seal for life, aluminium shell, no HDPE.
- TRL 3 refinements within those decisions, now also decided by Amish, 2026-09-25: go with recommendation: T1 folding bail on a thermal break (the fixed handle left about 14 mm for fingers); T2 cap stack from flat plate and a 280 mm tube (no milling); T3 stock 1/4 x 1/16 in fin bar; T4 R12 oven 85 °C, never above 90 °C, and storage limits of 45 °C (C5) and 65 °C (C25).

### Still awaiting Amish (status updated 2026-09-25)

O4 to O9 are now decided by Amish, 2026-09-25: go with recommendation (TCT-DDR-002). O1 to O3 had no recommendation and stay proposed, awaiting Amish.

1. **O1 Named co-design partner and region** for the first produce cooler. No recommendation.
2. **O2 ColdPod or ZeerBox dependency.** No recommendation; neither repo is in this batch.
3. **O3 C5 charging.** Freezer plus conditioning, or refrigerator. No recommendation at TRL 2; CAL shows a refrigerator takes 31 to 51 h, which favours the freezer.
4. **O4 R5.** Options: (a) relax R5 to 38 % for the stock-tube build; (b) lighten the caps (a pocketed plug needs a machine shop and adds cost); (c) keep 50 % for a later extrusion. Recommendation: (a) with (c) as the long-term target.
5. **O5 R10.** Options: (a) dark finish plus guidance to lay produce on the cartridges, then measure at TRL 4; (b) three or four cartridges per cooler; (c) restate R10 for a lower ambient or a shorter day. Recommendation: (a), with R10 kept as the target until a test shows the contact effect.
6. **O6 R16 and budget.** One C5 cartridge and one frame cost $87 against $80 (indicative). Options: (a) drop the fins for the first build (saves about $8, costs coupling in R10 and R12); (b) get quotes first and revisit; (c) raise the budget to about $90. Recommendation: (b); do not raise the budget until quotes are in.
7. **O7 R14.** A handling rule for H70 out of an oven (oven gloves or a 12 min wait) on the label. Recommendation: adopt the rule and prefer pad charging.
8. **O8 Surface finish.** Mill finish or dark paint or anodizing. Recommendation: dark finish; it helps R10, R11 and R12 at small cost.
9. **O9 R1 for C25.** Widen the C25 band to 22 to 27 °C, or seek a paraffin melting within 24 to 27 °C. Recommendation: widen the band; comfort uses do not need a tighter one.

### Consistency with shared components

ThermaCart uses none of the other shared components in this batch (FieldNode, CellGuard, MotionCore, TwinKit, CalRig) and none of them references it; GridBench's review lists it as not applicable. No sibling repo was changed and no conflict was found. No SwapCell pack is used.

### Citations

The Rubitherm product page and the RT 5 HC, RT 25 HC and RT 70 HC datasheets were fetched on 2026-09-25 and their figures are used in TCT-CAL-001; the datasheet links are added to TCT-PRC-001 and TCT-PRB-001. The TRL 2 note listed no unchecked citations. The ISO 13732-1 burn thresholds used for R14 could not be checked (the standard is paywalled and WebSearch is exhausted); they are flagged as assumptions in TCT-CAL-001 and TCT-REQ-001.

### Safety concerns

- H70 charging: the RT 70 HC limit is 90 °C, not 100 °C as the TRL 2 documents said; domestic oven thermostats can overshoot, so an oven thermometer is needed.
- C5 and C25 have datasheet limits of 45 and 65 °C; a cartridge left in a hot car may exceed them.
- Frozen cartridges hold a partial vacuum of about 0.7 bar; walls are within the allowable stress at 3.175 mm but a thinner wall would yield.
- A dropped molten cartridge may see a pressure surge of up to 5 bar at the cap (unverified; R6 test at TRL 4).
- Hot bail and grip for about 12 min after an oven (R14).
- Paraffin is combustible; C5 is below 0 °C out of a freezer; not for vaccines or medicines; W0 never with them; sharp edges; 3 kg mass.

### TRL 4 material

None found in the repo; nothing was added. `build-log/README.md` is the scaffold file and was not touched.

### Recommended next step

Review TCT-DDR-001 and items O1 to O9 above, starting with O5 (R10) and O6 (cost), since they decide whether the C5 cold-chain case is worth building. Before any build, replace the indicative BOM prices with supplier quotes. TRL 4 is on hold by Amish's instruction. For the record only, TRL 4 would need: a built C5 cartridge and frame, a lab test report (TST, `environment: lab`) covering leak-tightness through thermal cycles, the 1 m drop (R6), the cooler hold with a real 25 L box and load (R10), freezer and pad charge times (R12) and bail temperature (R14), a written fill recipe (R17), and dated build-log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (TCT-DDR-002 v0.1). TCT-DDR-001 is at v0.2 with the new status wording.

### Decisions applied and what changed

- **D1 to D8 and T1 to T4:** status wording only; the design already followed them. D6 keeps `budget_usd` at $80 (unchanged). D3's pitch was already applied.
- **O4, R5:** relaxed to 38 % PCM for the stock-tube build, 50 % kept for a later extrusion. Before: not met, 38.3 to 39.9 % against 50 %. After: met (thin), 38.1 to 39.7 % against 38 %.
- **O5, R10:** dark finish plus guidance to lay produce on the cartridges (added to TCT-PRC-001, How it works); R10 kept at 8 h. Design-case hold 1.9 h (bare) before, 2.4 h (dark) after; still not met. The contact measurement is TRL 4: decided, on hold.
- **O6, R16 and budget:** quotes first, budget not raised; `budget_usd` stays $80. Getting quotes is a purchasing step: decided, on hold with TRL 4.
- **O7, R14:** H70 label rule (oven gloves or a 12 min wait) and pad charging preferred. R14 restated; at risk before, met with the handling rule after. Rule added to the precis, safety text, README and the drawing notes.
- **O8, finish:** matte black high-temperature paint over etch primer on shell, fins and caps. BOM row 1 $24 to $29; cartridge $71 to $76; first build $87 to $92 against $80; three-grade set about $230 to $245; empty mass 1.78 to 1.80 kg; filled 2.89 to 2.96 kg to 2.90 to 2.98 kg. Design-case R11 hold 7.2 to 13.6 h; R12 C5 freezer 5.6 to 4.2 h, C25 refrigerator 6.6 to 4.6 h, H70 oven 6.1 to 5.3 h. `finish` parameter added to `cad/src/model.py` (no geometry change; STEP and STL re-exported); TCT-DWG-001 Rev P1 to P2 with finish and handling notes; media re-rendered with a black shell and checked by eye.
- **O9, R1:** C25 band widened from 24 to 27 °C to 22 to 27 °C; at risk before, met after.
- Documents bumped: TCT-PRB-001 v0.4, TCT-PRC-001 v0.4, TCT-REQ-001 v0.4, TCT-CAL-001 v0.2 (results table regenerated from `docs/04-calcs/sizing.py`), TCT-DDR-001 v0.2, TCT-DDR-002 v0.1 new. PDFs rebuilt.
- `README.md`: Concept, Key components and Safety updated; "What sparked the idea" rewritten around the 1964 gastronorm standard (EN 631, 1993) in place of the earlier origin text.
- Generated files (drawing, media, PDFs) re-rendered so they carry the designmolecule.com footer.

### Requirement status (TCT-CAL-001 v0.2, Table 5)

Counts: 2 not met, 1 at risk, 3 not verifiable at TRL 3, 12 met.

| ID | Status | Value against target |
| --- | --- | --- |
| R10 | **Not met** | 2.4 h (dark finish) against 8 h at 32 °C; energy alone would last 9.7 h; produce contact not credited |
| R16 | **Not met** | $76 per cartridge against $50; first build $92 against the $80 budget (indicative) |
| R12 | At risk | Freezer, refrigerator and oven within 8 h; 60 W pad 2.7 to 10.3 h |
| R6, R7, R17 | Not verifiable at TRL 3 | Need TRL 4 tests and the fill recipe |
| R1, R2, R3, R4, R5, R8, R11, R14 | Met | R4 (2.98 kg against 3.0) and R5 (38.1 % against 38 %) are thin; R14 with the handling rule |
| R9, R13, R15, R18 | Met by design | |

### Still awaiting Amish

1. **O1** Named co-design partner and region for the first produce cooler. No recommendation.
2. **O2** Whether ColdPod or ZeerBox should declare ThermaCart as a dependency. No recommendation.
3. **O3** C5 charging: freezer with conditioning, or refrigerator. No recommendation (CAL favours the freezer).

### Cross-repo actions

None. No decision requires a change in another repo; O2, the only cross-repo question, has no recommendation. No other repo was edited.

### Safety concerns

Unchanged from the TRL 3 session, plus: the dark finish must be a high-temperature paint rated well above 90 °C and must not be applied over the fill port thread, O-ring gland or sight window. The H70 label now carries the oven handling rule.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Decided but on hold: the R10 contact measurement (O5) and supplier quotes (O6).

## Session 2026-09-26: sources strengthened

- `README.md`, "What sparked the idea": the Wikipedia article "Gastronorm" was replaced by the primary sources for the same event: the SVG (Swiss association for hospital, care-home and institutional catering) Gastro-Norm fact sheet, which records that SVG, the Swiss Hotel Association and Swiss kitchen equipment makers created the norm on a 530 x 325 mm grid in November 1964, and the BSI record for BS EN 631-1:1993. The unsupported day ("17 November") was dropped. The inspiration event is unchanged; its line in `INSPIRATIONS.md` now names the sources.
- `docs/01-problem.md` (TCT-PRB-001 v0.5): the Gastronorm prior-work line now cites BSI (EN 631-1) and SVG (530 x 325 mm grid); Wikipedia is kept only alongside them for the GN 1/3 size.
- All other links in the four README source sections were re-fetched and confirmed (FAO, Hanson et al. 2017, WHO, UNEP, MoFPI, IFPRI, IEA, Eurostat, Delaware food code, University of Edinburgh). No country rows were replaced.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal product renders; the massing model, BOM, documents and drawing are unchanged.

### What was added

- `cad/src/product_model.py`: `product_parts()` (66 parts: 23 shell, 6 internal, 4 accessory, 33 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view of the keyed nose at the frame's end stop without the bench). It imports `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py`, so every main dimension and interface is unchanged. It adds:
  - rounded outer corners (R4) on the tube and end flanges, softened fin edges, and a seam at each flange;
  - cap screw heads with hex sockets at the model.py positions; a hex G 3/4 fill port plug with its FKM sealing washer and a shank in the bore;
  - the folding bail with phenolic thermal-break washers, pivot pin heads and a ribbed silicone grip; the key tab with rounded leading edges;
  - the printed label (grade block, wordmark, data lines, kit-accent stripe), a painted grade colour band round the nose end and a painted side marking;
  - the sight window as a black bezel, a clear polycarbonate lens and the white (solid, charged) PCM vial under it;
  - inside: the PCM fill, gland spacers and plugs, and FKM O-rings;
  - the adapter frame with bend radii, a "C5 ONLY" grade decal beside the key slot and small rubber feet;
  - context: a compact bench top, with the C25 (green) and H70 (red) grades lying behind the C5 cartridge as a lineup, each with its key tab at its own grade position.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced later by the orchestrator.

### Where the appearance model differs from model.py (Proposed, awaiting Amish)

1. **Grade colour band on the shell.** model.py and the BOM code the grade only by the label colour and the key position. The renders add an 18 mm painted band round the nose end in the grade colour (blue, green, red), visible from the side and when a cartridge sits in a frame. Recommendation: adopt it as a paint-masking step in BOM line 1 (no cost change within the indicative figure); the alternative is a colour-coded wrap label.
2. **Side marking.** A painted "ThermaCart, TC-L C5" marking on the front face. Recommendation: adopt as part of the label set (BOM line 6).
3. **Frame grade decal and feet.** A "C5 ONLY" decal beside the frame's key slot and four 1.2 mm rubber feet under the frame; neither is in model.py or BOM line 7. Recommendation: adopt the decal (it makes the keying legible to users); treat the feet as host-specific and leave them out of the BOM.
4. **Sight window build-up.** model.py shows the window as a 22 mm solid disc on the label; the render shows the same 22 mm outline as a bezel ring with a 15 mm clear lens and the PCM vial as a thin disc under it, above the tube wall. Recommendation: keep the model.py envelope; the vial arrangement is a TRL 4 detail and is on hold.
5. **Rounded tube corners.** model.py uses a sharp-cornered tube; stock 6 x 2 x 1/8 in tube has rounded outer corners, drawn here at R4. Recommendation: no change to model.py at TRL 3; confirm the supplier's corner radius with the quotes (O6).
6. **Pivot pins and fill port hex.** Pin heads are drawn on the outer faces of the bail arms (model.py has no pins; BOM line 5 lists stainless pins). The fill port hex (about 26 mm across flats) and its 1.5 mm washer stay inside the model.py port envelope. Recommendation: no change.
7. **Cap screws.** Shown as 1.2 mm proud heads at the model.py positions, as model.py draws them; BOM line 8 lists countersunk screws, which would sit flush. Recommendation: keep countersunk in the BOM and let the renders follow model.py for now.

### Status

This is an appearance model only: no tolerances, no fabrication detail, concept, not for fabrication. `trl` stays 3 and `trl_target` stays 3. TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: constructable design and illustrated build plan (/build-plan, kit 1.7.0)

Authority: the `/build-plan` command, Amish's instruction of 2026-09-30 ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations"), his 2026-09-30 rule that outstanding decisions go in a separate register, and his 2026-10-01 note that budgets are value-engineering targets.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced with `.kit/CLAUDE.md`.
- `cad/src/model.py`: rebuilt as separate components with BOM lines (`build_components()`), the constructable design P1 to P11 below, and 68 build123d constructability checks (`python cad/src/model.py --check`: overlaps, contacts and clearances for every pair of parts that meet, and the bail swung to 90 and 180 degrees). All 68 pass. `build_parts()` keeps the old grouped names for `sizing.py`, `concept_media.py` and `product_model.py`. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (TCT-DDR-003 v0.1, Draft): every change with its reason; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (TCT-CAL-001 v0.3): masses from the new components, the bail thermal break with insulated bolts, cost and the value-engineering wording.
- `bom/bom.csv` lines 1 and 3 to 8 rewritten for the parts the build needs; `bom/bom-notes.md` updated.
- `cad/src/sheets.py`: general arrangement TCT-DWG-001 at Rev P4.
- `cad/src/build_plan_media.py` (new): overview, 10 making sketches `cad/drawings/TCT-DWG-101` to `110`, a cap hole layout, 10 joint close-ups (section views label each part on its cut face) and 12 assembly steps, in `docs/05-build-plan/`. Every picture was looked at and fixed where labels landed on the wrong part or covered it.
- `docs/05-build-plan.md` (TCT-BLD-001 v0.1) and `docs/06-design-decisions.md` (TCT-DEC-001 v0.1) written from the kit templates.
- `cad/src/concept_media.py` re-run: `media/hero.png`, `exploded.png`, `cutaway.png`, `flow.png`, `concept-blueprint.*`, `model.glb` and `viewer.html` now show the constructable model.
- TCT-PRB-001 v0.6, TCT-PRC-001 v0.5, TCT-REQ-001 v0.5: budget wording, numbers and component descriptions. `project.yaml`: `design_state: constructable`, TCT-DDR-003, BLD and DEC added to `trl_evidence`; `budget_usd` unchanged. `README.md`: links line, "Building the prototype" section with the overview picture, value-engineering wording.

### Design changes made for construction (TCT-DDR-003)

1. **P1 fill port:** the G 3/4 bore cut through the O-ring; now a G 1/2 anodised aluminium plug on a bonded seal, 56 mm toward the back, 3.5 mm inside the O-ring line.
2. **P2 O-ring gland:** 94 % full; now 2.5 mm FKM cord in a 2.1 mm deep gland (78 % fill, 16 % squeeze), plates cut to the measured bore, corners rounded, 1 mm lead-in chamfer on the tube ends.
3. **P3 radial screws:** on the wet side of the O-ring with no seal, countersunk in a 3.175 mm wall; now M5 x 10 button-head screws on FKM bonded seals into tapped plug edges.
4. **P4 cap stack:** no fixing between the three plates; now bonded face to face and screwed into blind holes in the plug.
5. **P5 bail:** the arms could not swing and the lugs sat over the seal with no fixing; now bolted 20 x 20 x 3 mm lug angles on phenolic washers, insulated bolts, 16 x 4 mm arms on 5 mm pins, rod screwed between the arms. Finger gap 41 mm; bail 39.1 °C (was 42.5 °C).
6. **P6 key tab:** no fixing; now two M4 screws into the plug.
7. **P7 frame stop:** stood 2 mm in front of the key, so no grade could seat; now the key passes through the slot and the frame floor is 294 mm (was 304 mm).
8. **P8 frame corners:** walls and stop overlapped; now the walls' tabs fold round the stop and are riveted.
9. **P9 melt indicator:** a 22 mm disc 2 mm thick; now a clear polycarbonate tube of the same paraffin between two fin-bar guards.
10. **P10 fins:** epoxy fillet each side and a comb jig (no geometry change).
11. **P11 tube corner radii** added to the model.

### Key results

- Envelope 323.4 x 152.4 x 63.5 mm (unchanged); inner volume 1.655 L (unchanged); empty 1.80 kg; filled 2.90 to 2.98 kg (R4 met, thin); PCM fraction 38.1 to 39.6 % (R5 met, thin).
- Value-engineering target: USD 80 for one C5 cartridge and one frame. Estimated cost of the constructable design: USD 97 (USD 17 over the target). R16: $80 per cartridge, over its $50 value-engineering target by $30; frame $17, $3 under.
- Requirement status: 1 not met (R10, cold-chain hold 2.4 h against 8 h), 1 over the value-engineering target (R16), 1 at risk (R12, pad charging), 3 not verifiable at TRL 3 (R6, R7, R17), 12 met.

### Proposed, awaiting Amish

All open decisions are in the design decisions register (`docs/06-design-decisions.md`): A1 how a wrong grade is shown to be rejected by the frame (touches the safety case), A2 W0 key fixing, A3 the R5 margin, O1 to O3 from TCT-DDR-001, and the appearance-model items 1 to 3 of 2026-09-26. Nine items are listed to confirm when parts are bought.

### Stale media (made on Amish's Mac, not regenerated here)

`media/render-*.png`, `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept bail and lugs, the round sight window, the G 3/4 plug and the concept frame stop. The design changed visibly; they need updating on the Mac. `media/render-hero.png`, which the README leads with, is not in this copy of the repo.

### Safety concerns

- Paraffin is melted for filling: water bath on a thermostat only, never a flame; C5 never above 45 °C (build plan S2, S3).
- The thermal break works only if no lug bolt touches its angle; the build plan has a meter check.
- The wrong-grade rejection (A1) relies on a 12 mm stand-off; a frozen W0 or hot H70 cartridge could still be left partly seated in a cold-chain host until A1 is decided.

### Recommended next step

Review TCT-DDR-003 and decide A1 in the register. TRL 4 (building and testing to TCT-BLD-001) remains on hold.
