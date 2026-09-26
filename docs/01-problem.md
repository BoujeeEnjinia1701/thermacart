---
doc_id: TCT-PRB-001
title: ThermaCart problem statement
project: ThermaCart
doc_type: Problem statement
version: "0.4"
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
  change: Populate to TRL 2 (users, context, constraints, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (paraffin expansion from datasheets, budget scope per TCT-DDR-001 D6, first host type, temperature limits)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# ThermaCart problem statement

Every cold box, food carrier and small heat store that uses phase-change material (PCM) designs its own container, fill and interface from scratch, and loose or improvised PCM is messy, can corrode metal, can burn, and can freeze or overheat what it is meant to protect. There is no open, standard, sealed cartridge that a builder can pick by temperature grade and drop into a cooler, cabinet or heat exchanger.

## Why it matters

Storing heat or cold cheaply is the missing piece wherever power is intermittent or absent:

- Around 14 % of the world's food, worth about $400 billion a year, is lost between harvest and retail, and a further 17 % is wasted in retail and homes ([FAO and UNEP, 2022](https://www.fao.org/newsroom/detail/FAO-UNEP-agriculture-environment-food-loss-waste-day-2022/en)). Much of the loss in hot climates is spoilage for want of cooling.
- Cold chains fail in both directions. Water ice packs sit at 0 °C or below, and freezing exposure is common in vaccine storage and transport studies ([Hanson et al., 2017](https://www.sciencedirect.com/science/article/pii/S0264410X16309471)). A PCM that melts at 5 °C avoids this, which is why ColdPod in this portfolio uses one.
- About 2.1 billion people still cook on open fires or inefficient stoves using polluting fuels, and household air pollution caused an estimated 2.9 million deaths in 2021 ([WHO fact sheet, 2025](https://www.who.int/news-room/fact-sheets/detail/household-air-pollution-and-health)). Keeping cooked food hot without relighting a stove saves fuel and smoke.
- UNEP expects the world's installed cooling capacity to triple by 2050, with cooling emissions reaching more than 10 % of global emissions unless efficiency improves ([UNEP, About cooling](https://www.unep.org/topics/energy/cooling/about-cooling)). Thermal storage lets cooling run when power is cheap or clean.

## Users and context

| User | Context | What they need from a cartridge |
| --- | --- | --- |
| Builders of thermal devices, including this portfolio (ColdPod, ZeerBox, ThermaBrick, HelioLite) and other open hardware makers | Workshops and makerspaces | A known, documented storage block with published capacity, so they design the box, not the storage |
| Small food vendors, caterers and school or community kitchens | Carrying cooked food to a site, or holding it on a stall | Keep food at or above hot-holding temperature for a service period without gas or mains |
| Traders and smallholders moving produce or dairy | Coolers on motorbikes, in vans and on market stalls, often in 30 to 40 °C heat | Cold that lasts a working day and recharges overnight in a shared freezer |
| Off-grid households and clinics | Solar direct-drive refrigerators, cool boxes, comfort cooling | Swappable cold or heat that can be charged where power exists and carried to where it does not |
| Equipment integrators | Outdoor electronics and battery cabinets | A comfort-grade (25 °C) buffer that smooths daily temperature swings |

## Prior work

- **Commercial PCM products.** Rubitherm publishes organic PCMs from about −9 to 90 °C with storage capacities of 190 to 260 kJ/kg ([Rubitherm RT range](https://www.rubitherm.eu/en/productcategory/organische-pcm-rt)); Pluss sells savE PCMs and packs for cold chain ([Pluss](https://www.pluss.co.in/knowledge-center/technology/phase-change-materials/)). These are materials and proprietary packs, not an open, interchangeable format.
- **Standard coolant packs.** WHO PQS E005 fixes the sizes of water packs for vaccine carriers (0.3, 0.4 and 0.6 L; the 0.6 L pack is 190 x 120 x 34 mm) ([WHO PQS E005](https://extranet.who.int/prequal/key-resources/documents/pqs-performance-specification-e005ip012-water-packs-use-icepacks-cool-packs)). This shows the value of a common envelope, but it covers water only, at 0 °C.
- **Ice banks in solar refrigerators.** Solar direct-drive vaccine refrigerators freeze water or another PCM by day and run from that ice bank at night, giving about 83 to 170 h of autonomy in the prequalified models PATH lists ([PATH](https://media.path.org/documents/TS_opt_ebs_dd_solar_fridge.pdf)). The storage is built into each appliance.
- **Heat batteries.** Sunamp's salt-hydrate heat batteries, developed with the University of Edinburgh, store heat for hot water in homes and hold RAL quality certification for stability over tens of thousands of cycles ([University of Edinburgh](https://chem.ed.ac.uk/research/research-impact/heat-storage-technology)). The RAL-GZ 896 scheme sets quality and test rules for PCMs ([Quality Association PCM](https://pcm-ral.org/quality-testing-specifications-pcm/)).
- **Food service containers.** Gastronorm (EN 631) sizes are the shared format of commercial kitchens; a GN 1/3 slot is 325 x 176 mm ([Gastronorm](https://en.wikipedia.org/wiki/Gastronorm)).

The gap is an open cartridge: a published envelope, a small set of temperature grades, a fill and seal recipe, and a keyed interface, all under an open hardware license.

## Known material problems

- **Salt hydrates** are dense and cheap but supercool, separate into phases over cycling and corrode aluminium and copper ([corrosion study](https://www.researchgate.net/publication/229021530_Corrosive_effects_of_salt_hydrate_phase_change_materials_used_with_aluminium_and_copper); [cycling study](https://www.sciencedirect.com/science/article/abs/pii/S2352152X19315464)).
- **Paraffins** are stable and non-corrosive but combustible, expand by 12.5 to 13 % on melting ([Rubitherm RT 5 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT5HC_EN_23072026.PDF) and [RT 25 HC](https://www.rubitherm.eu/media/products/datasheets/Techdata_-RT25HC_EN_21012026.PDF) datasheets), and soften or permeate some plastics, including polyethylene ([compatibility of plastics with PCM](https://www.researchgate.net/publication/227717836_Compatibility_of_plastic_with_phase_change_materials_PCM)).
- **Water** is the cheapest store but expands on freezing and sits at 0 °C, which is too cold for vaccines and some produce.

## Constraints

- Garage-buildable prototype for about $80 USD, using stock aluminium sections, hand tools, a drill press and a tap set. No custom extrusion, casting, milling or welding for the first build. The $80 covers one C5 cartridge and one adapter frame; a set in all three grades is outside it (TCT-DDR-001, D6, decided by Amish on 2026-09-25). Supplier quotes come before any budget change (TCT-DDR-002, O6).
- First host type: a produce cooler used by a trader or smallholder, reached through a local partner (TCT-DDR-001, D7); no partner is named yet.
- Each paraffin grade has a datasheet maximum operating temperature (C5 45 °C, C25 65 °C, H70 90 °C) that charging and storage must respect.
- Sealed for life in normal use; refillable only by a builder with the fill recipe.
- Safe to carry by hand at any state of charge; no pressure vessel.
- Open design under CERN-OHL-S-2.0, with published fill recipes and grade data.

## Out of scope

- Qualification for vaccines or medicines. A C5 cartridge could support a cold box such as ColdPod, but any medical use needs WHO PQS or equivalent qualification, which is beyond this project.
- High-temperature storage above 90 °C, the limit of the H70 paraffin, for example solar cooking at 200 °C or more. That needs different materials and belongs with ThermaBrick-type designs.
- Active parts: the cartridge has no electronics, heaters or fans. Charging uses existing freezers, ovens, heat stores or host appliances.
