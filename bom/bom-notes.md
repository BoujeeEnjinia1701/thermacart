# BOM notes

- Rows 1 to 8 are numbered to match the exploded view (`media/exploded.png`) and the component table in the design precis (TCT-PRC-001 v0.3). Quantities and sizes follow the parametric model `cad/src/model.py`.
- All prices are indicative USD for one-off prototype quantities, as of September 2026. They are estimates, not quotes, and must be replaced with supplier quotes before any build.
- Rows 1 to 6 and 8 make one cartridge: $71.00. Row 7 (adapter frame) is per host slot: $16.00. `docs/04-calcs/sizing.py` reads this file and prints these totals (TCT-CAL-001, section H).
- Budget: `budget_usd` in `project.yaml` is $80 and covers one C5 cartridge and one frame (TCT-DDR-001, D6, adopted for TRL 3 work and open for Amish's review). That build is $87.00, $7.00 over. No new budget figure has been recommended; the overrun and the options for it await Amish (`docs/REVIEW.md`).
- A set of one cartridge in each of the three grades plus one frame would be about $230; it is outside the $80 budget.
- Row 2 is priced for the C5 grade at $10/kg. The C25 and H70 fills are 1.12 and 1.18 kg. PCM prices vary widely with quantity; at $20/kg a cartridge costs about $11 more.
- The caps (row 3) are built from flat 6061 plate cut and filed, so no milling is needed. The frame (row 7) needs a hand brake, for example at a makerspace.
