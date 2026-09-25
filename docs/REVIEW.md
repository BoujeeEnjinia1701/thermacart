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

### Proposed, awaiting Amish

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
