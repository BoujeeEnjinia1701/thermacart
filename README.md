# ThermaCart

**Area:** Shared Components · **Status:** Concept · **Prototype budget:** about $80 USD · **Difficulty:** 2 of 5

A sealed, swappable phase-change thermal cartridge in a few standard temperature ranges (cold chain, comfort and cooking) that stores heat or cold and drops into coolers, cabinets and heat exchangers.

## Concept rationale

A common cartridge format turns thermal storage into a part you choose instead of a subsystem you design, and lets cartridges move between cold boxes, ovens and heat stores.

## Burning platform

Food and vaccine losses from broken cold chains, and cooking fuel poverty, both come down to storing heat or cold cheaply where power is intermittent.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. ThermaBrick, ZeerBox, ColdPod and HelioLite each store heat or cold in their own way.

## Problem

Thermal storage is designed from scratch in every cold box, cooker and heat store, and phase-change materials are messy, corrosive or unsafe when handled loose.

## Concept

A sealed, swappable phase-change thermal cartridge in a few standard temperature ranges (cold chain, comfort and cooking) that stores heat or cold and drops into coolers, cabinets and heat exchangers.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Aluminum or HDPE cartridge shell with fins
- Phase-change material fill (water, salt hydrate or paraffin grades)
- Fill port and seal
- Handle and keyed latch
- Temperature label and indicator
- Cabinet adapter frame

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Some phase-change materials are corrosive or flammable; keep cartridges sealed, label the fill and keep paraffin grades away from open flame.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Shared components set.
