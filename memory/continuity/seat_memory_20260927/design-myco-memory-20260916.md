---
name: design-myco-memory-20260916
description: Operator's "VRAM in mycelial networks" question reframed as a
  living memory hierarchy — controller+bus is the missing layer; six dogfooded
  baby steps from the $31 ear to mounting myco-bit-0 as a fleet file
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16 night — operator asked "How can we create VRAM in mycelial networks... babysteps
dogfood... like we built our system." Design filed at
watch/inbox/physical_computing/DESIGN_MYCO_MEMORY_20260916.md.

Core reframe: not building VRAM (billions of bits at ns) but owning a **living memory
hierarchy** end to end. Mycelium already has every layer; what exists nowhere is the
controller and the bus. Pyramid: registers = membrane voltage (ms, measured); RAM =
reservoir fading memory (seconds-minutes, measured tiny 0.048–0.209, Telhan 2026); disk =
hyphal tube remodeling (hours-days; Physarum habituation is the published precedent);
archive = sclerotia/spores.

Six dogfooded baby steps (fleet law: every step must be CONSUMED by the fleet — observation
alone is theater):
0. the ear — C17 $31 rig, noise floor → dashboard heartbeat tile
1. the read — capacity meter (PRBS drive, delayed-input readout), nightly MC number in trails
2. the first write — conditioning, before/after receipt pair (did anything persist past the
   electrical ghost)
3. addressing — write at electrode A, read at B; the distance-decay curve is the embryonic
   address decoder
4. the filesystem — pattern→response lookup counted in honest bits (one bit held an hour =
   world-class at this table)
5. the mount — myco-bit-0 as a literal file the fleet reads; MUD room; estate-walk lantern

Walls pre-armed: separating volatile electrical traces from persistent structural memory is
the hard science (dead twin + shuffled surrogates do it); retreat to "best-instrumented
mycelium sensor in the hobbyist world" pre-written. Same $31 rig as [[mycelium-multispecies-lattice-20260916]]
(CUBE1_SHOPPING_LIST.md); corpus/venue/skeptic survey lanes S1–S5 feed the species-pairing
and protocol choices.

**WRITE-MECHANISM CORRECTION (G-D lane, 2026-09-16 late):** the R1 swarm lead "±0.55 V
electrical write, hours retention, ion redistribution" is FALSIFIED-AS-STATED — no source
contains 0.55 V; living-mycelium electrical write does not exist in publication (Beasley
2022: fruit bodies, loops fail to pinch, no retention; LaRocco 2025: sun-dried substrate,
explicitly volatile; Schmidt 2025: independent replication of the Physarum bio-memristor
FAILED — 94.4% of traces plain RC). VERIFIED write path instead: **tube remodeling** —
nutrient forcing redistributes tube diameter in ~15 min, imprint persists ≥310 min (Kramar
& Alim 2021 PNAS); chemical habituation ~4 days, network cut = memory deletion (Yoneoka
2023); survives month-scale dormancy as sclerotia (Boussard 2019). Stage 2 therefore
targets **nutrient write / electrical-impedance read FIRST** (fits the nightly cadence);
electrical hysteresis demoted to one bounded control night that still files the
falsification datapoint. Step 2's "first write" is now the nutrient pulse.
