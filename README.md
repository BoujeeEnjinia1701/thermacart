# ThermaCart

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Shared Components · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $80 USD · **Difficulty:** 2 of 5

A sealed, swappable phase-change thermal cartridge in a few standard temperature ranges (cold chain, comfort and cooking) that stores heat or cold and drops into coolers, cabinets and heat exchangers.

![ThermaCart concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

A common cartridge format turns thermal storage into a part you choose instead of a subsystem you design, and lets cartridges move between cold boxes, ovens and heat stores. Phase-change material (PCM) holds heat or cold at a nearly constant temperature, so the grade of the fill, not a thermostat, sets the temperature of the box it sits in. Sealing the PCM in a keyed cartridge keeps a messy or combustible material out of users' hands and stops the wrong temperature going into the wrong box.

The design is open and garage-buildable on purpose. The shell is a stock 6 x 2 in aluminium tube with bolted, O-ring-sealed end caps, so anyone with a drill press and a tap set can make one, and the envelope fits a GN 1/3 gastronorm slot that commercial kitchens already use. Publishing the envelope, key table and fill recipes lets other open projects, including ColdPod and ZeerBox in this portfolio, design around the same cartridge.

## Burning platform

Around 14 % of the world's food, worth about $400 billion a year, is lost between harvest and retail ([FAO and UNEP, 2022](https://www.fao.org/newsroom/detail/FAO-UNEP-agriculture-environment-food-loss-waste-day-2022/en)), much of it spoilage where cooling is missing or unreliable. Cold chains also fail by overcooling: freezing exposure is common in vaccine storage and transport studies, largely because water ice sits at 0 °C or below ([Hanson et al., 2017](https://www.sciencedirect.com/science/article/pii/S0264410X16309471)).

On the hot side, about 2.1 billion people still cook with polluting fuels, and household air pollution caused an estimated 2.9 million deaths in 2021 ([WHO, 2025](https://www.who.int/news-room/fact-sheets/detail/household-air-pollution-and-health)). Demand for cooling is rising fast: UNEP expects installed cooling capacity to triple by 2050, with cooling emissions above 10 % of the global total unless efficiency improves ([UNEP](https://www.unep.org/topics/energy/cooling/about-cooling)). Cheap, portable thermal storage lets heat and cold be made where energy is available and used where it is not.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Food service and catering | H70 cartridges in insulated GN carriers keep delivered meals hot without gas or mains |
| Fresh produce and dairy logistics | C5 cartridges in coolers on motorbikes, vans and market stalls, recharged overnight in a shared freezer |
| Off-grid refrigeration | A swappable cold store for solar direct-drive fridges and cool boxes instead of built-in ice banks |
| Telecom and electronics enclosures | C25 cartridges buffer daily temperature swings in outdoor cabinets and battery boxes |
| Open hardware and product design | A documented storage block for new cold boxes, warmers and heat stores, so designers size the box, not the storage |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| India | A 2022 national study put post-harvest losses at 6 to 15 % for fruits and 5 to 12 % for vegetables ([MoFPI, citing NABCONS](https://www.mofpi.gov.in/sites/default/files/_annex_265_au2145_qhinz4.pdf)) |
| Nigeria | About 45 % of food spoils for lack of cold storage, and solar cold rooms such as ColdHubs show the demand for shared cooling ([IFPRI, 2018](https://www.ifpri.org/blog/coldhubs-addressing-crucial-problem-food-loss-nigeria-solar-powered-refrigeration/)) |
| Sub-Saharan Africa (for example Kenya and Tanzania) | About four in five households lack clean cooking ([IEA](https://www.iea.org/reports/universal-access-to-clean-cooking-in-africa/executive-summary)); keeping cooked food hot saves fuel and smoke |
| European Union | About 132 kg of food per person was wasted in 2022, 54 % of it in households ([Eurostat](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20240927-2)); kitchens already use GN formats |
| United States | State food codes based on the FDA Food Code require hot food to be held at 57 °C (135 °F) or above ([for example Delaware, § 3-501.16](https://www.law.cornell.edu/regulations/delaware/16-Del-Admin-Code-SS-3-501.16)); caterers and school meal programs need hot holding away from mains |
| United Kingdom | Salt-hydrate heat batteries are already used in homes for hot water ([University of Edinburgh](https://chem.ed.ac.uk/research/research-impact/heat-storage-technology)), showing that sealed PCM storage already sells in high-income markets |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. ThermaBrick, ZeerBox, ColdPod and HelioLite each store heat or cold in their own way. The real-world trigger was that WHO standardised vaccine coolant packs by size ([WHO PQS E005](https://extranet.who.int/prequal/key-resources/documents/pqs-performance-specification-e005ip012-water-packs-use-icepacks-cool-packs)), but only for water, so there is no open equivalent for other temperatures.

## Problem

Thermal storage is designed from scratch in every cold box, cooker and heat store, and phase-change materials are messy, corrosive or unsafe when handled loose. Water ice is too cold for vaccines and some produce, salt hydrates corrode aluminium, and paraffins burn and can permeate plastics.

Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

A sealed aluminium cartridge, 322 x 152 x 61 mm, holds about 1.1 kg of PCM in one of three proposed grades: C5 (5 °C, cold chain), C25 (25 °C, comfort) and H70 (70 °C, hot holding of cooked food). It fits a GN 1/3 slot, shows its state through a sight window and locks into an adapter frame whose key accepts only its grade. First-order estimates: 55 to 67 Wh of usable storage per cartridge, 2.6 kg filled and about $49 in parts. Two C5 cartridges hold a 25 L cooler at 2 to 8 °C for about 8 h at 32 °C, and one H70 cartridge keeps a GN carrier at 63 °C or more for about 6 h. The C5 storage target, the PCM mass fraction and the H70 handle temperature are not met on paper yet (see the [review note](docs/REVIEW.md)). All values are estimates, and all choices are proposed, awaiting Amish.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Requirements: [docs/03-requirements.md](docs/03-requirements.md)

![Exploded view](media/exploded.png)

## Key components

1. Cartridge shell: finned 6063 aluminium rectangular tube
2. PCM fill: C5, C25 or H70 paraffin grade (water W0 as an option for produce only)
3. End caps with FKM O-ring seals
4. Fill port plug and seal
5. Handle with insulating grip, and keyed nose
6. Grade label and melt indicator (sight window)
7. Cabinet adapter frame with keyed stop

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Paraffin fills are combustible: never charge a cartridge on an open flame or above 100 °C, and keep cartridges away from fire. H70 cartridges reach about 75 °C and can burn skin, so carry them only by the insulated handle. Fill hot to the specified level and never seal a partly filled cartridge, so it cannot pressurise. C5 cartridges come out of a freezer below 0 °C; ThermaCart is not qualified for vaccines or medicines. Deburr all cut aluminium.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (TCT-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `TCT-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Shared components set.
