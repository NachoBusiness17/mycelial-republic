# C16 — Etch Inventory + Design Stone One (receipt)

- **Date:** 2026-09-16
- **Wave-lane:** Tier-$0 stone, pack §3 (`../PHYSICAL_COMPUTING_PACK_20260916.md`)
- **Agent:** ZCode subagent (C16)
- **Law:** receipt first, append as you go · no git · no paid APIs · WebSearch/WebFetch free

## Status: COMPLETE

- [x] Step 1 — fabrication capability inventory (repo + operator context; EXISTS vs aspirational)
- [x] Step 2 — June-tweet path: Prusa + laser-conversion kits, 2026 street prices
- [x] Step 3 — design file: `../DESIGN_ETCH_STONE_ONE_20260916.md`
- [x] Step 4 — capability table + design path + total budget (this receipt, final section)

## Log (append as you go)

- 13:4x — receipt created. Reading pack §3 + mining watch/inbox, memory/, basecamp/ for real hardware.

## Step 1 — fabrication capability inventory (what the fleet can mark or cut TODAY)

Searches run (all $0): `3d.?print|printer|ender|prusa|bambu|creality` and `laser|cnc|engrav`
and `octoprint|klipper|anycubic|sovol|voron|flashforge|mk3s|mk4` over `watch/`, `watch/inbox/`,
`memory/`, `basecamp/`, `docs/`, `handoff/` (md/json/txt). Corpus/ractor text noise filtered.

### EXISTS (verified on file)

| Asset | Source | Fabrication relevance |
|---|---|---|
| DESKTOP: 64 GB RAM, AMD RX 5600 XT ~6 GB VRAM, no CUDA | `docs/ref/HOME_HARDWARE_ENVELOPE.md` (as-of 2026-08-06) | **Design-only.** Can run OpenSCAD/FreeCAD/Blender, emit SVG/G-code/STL. Cannot mark, cut, or print anything. |
| Water computer, MUD module "The Clear Pipes" | `memory/game_modules/water_computer.v1.json` (per pack §6) | Simulation only. No physical two-bucket XOR built (falsifier §4.5 open). |
| Paper + hands + any office printer | operator environment | The only marking tool that exists today. |

That is the entire list. **Fleet fabrication hardware: zero.**

### ASPIRATIONAL (named, priced, NOT owned)

| Item | Status | Source |
|---|---|---|
| **Microduck** (Pollen Robotics) | $399 **pre-order** — hardware touchstone, not in hand; battle-bots stones are explicitly "browser-only, no hardware" | `watch/inbox/BATTLE_BOTS_SQUID_MAZE_20260914.md` §Hardware reality check, §First stones |
| **Used Prusa + laser conversion** (June 29 tweet path) | named in tweet + pack §3 Tier-$small; not purchased | `PHYSICAL_COMPUTING_PACK_20260916.md` §0, §3 |
| **Instrumented mycelium cube** (spores, substrate, Arduino sensor kit) | Tier-$small "next" — to buy | pack §3 |
| **$15 two-bucket XOR** | spec'd as falsifier §4.5 test, not built | pack §6 |
| GPU (used RTX 3090 ~$1,200) | JIT-gated, "no speculative purchase now" — and it is compute, not fab | `watch/HARDWARE_RADAR_20260901.md` §9, §12 |
| "ghetto TNG replicator" | the dream; north star only | `watch/inbox/journal_mark_202609/DREAM_MYCELIUM_20260916.md` |

**Honest verdict:** as of 2026-09-16 the fleet can *design* artifacts (SVG/G-code from the
desktop) but can mark or cut **nothing**. Every fabrication-capable item in the repo is a
price tag, not a tool. Per falsifier §4.4, the manufacture track must say plainly:
**simulation-only so far.** Cheapest credible first-marking paths researched in Step 2.

## Step 2 — the June-tweet path, priced (2026 searches, $0)

Tweet thesis: "Prusa has a good model and other brands have conversions to laser cnc … the
start of an ghetto TNG replicator" (2026-06-29, @NachoQuixotic).

| Component | 2026 finding | Price | Tag |
|---|---|---|---|
| Printer (used) | Prusa i3 MK3S, eBay street — MK4S release pushed MK3 prices down; community fair-price $250–300 | **$250–400** (median ~$300) | QUOTED (live listings + r/prusa3d consensus) |
| Laser conversion | **No official Prusa MK4 laser kit exists** — the "Prusa laser kit" ads are third-party. The real kit is **Opt Lasers PLH3D-2W** ("Original Prusa Laserupgrade"), 2 W diode, 70 g, no external cooling — but it is **MK3-generation mount**; MK4 needs an adapter (Infinity Flow S1, $7.99) | **€239.95 ≈ $260** | QUOTED (MYBOTSHOP.DE listing) |
| Bare-metal marking | 2 W diode alone cannot mark bare metal — needs LaserBond 100-class marking compound for stainless/ceramic, or a 10 W-class diode for direct dark marks | ~$30/can | QUOTED range, not priced live — UNVERIFIED |
| Higher-power option | Opt Lasers PLH3D-15W CNC kit ~€724.79 — real metal capability, breaks tier | €725 | QUOTED, noted and parked |

**Path total (canon): used MK3S (~$300) + PLH3D-2W ($260) + shipping ($40–135) + plate ($8)
≈ $610–700.** Alternative on record: a standalone 10 W-class diode engraver at ~$300–400
etches better but buys no FDM — it fails the tweet's bootstrap-replicator argument, which
is the point of the June-tweet path. Pack Tier-$small ("used Prusa + laser diode
conversion") is consistent with this pricing; nothing is purchased without operator word.

## Step 3 — the design file

**Written:** `watch/inbox/physical_computing/DESIGN_ETCH_STONE_ONE_20260916.md`

Picked: **16-node Ising Covenant Plate** (laser-etched signed coupling lattice + provable
ground-state panel + sha256 integrity block + resolution wedge, 100×100×3 mm black
anodized aluminum). Waveguide killed honestly (needs fs laser, decoration at 2 W).
Spore-print ledger deferred until the instrumented cube exists (a ledger before logs is a
plaque). Doctrine tie: LIVING_CIPHER Isfahan law — every dial counts; readback must be
lossless or the plate is decoration. DAD honesty stated in-file: information artifact, not
a dynamic computer — falsifier §4.5 stays reserved for the two-bucket XOR.

## Step 4 — final answers (the three things owed)

**Capability table:** Step 1 above — EXISTS: one desktop (design-only), one MUD water-computer
(sim only), paper and hands. Fabrication hardware owned: **zero**. Aspirational: Microduck
($399 pre-order), Prusa+laser conversion, instrumented cube, two-bucket XOR, GPU (JIT-gated).

**Design file path:** `C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\physical_computing\DESIGN_ETCH_STONE_ONE_20260916.md`

**Total budget to produce Stone One:** **$10–40** (door C: borrowed laser access, plate
only — the $0-law fastest route) · **~$700** (door A: the full canon June-tweet path, used
MK3S + PLH3D-2W + materials). No purchase authorized by this receipt; Tier-$small needs
the operator word per pack law.

## Sources

- [Prusa i3 MK3 for sale — eBay](https://www.ebay.com/b/Prusa-i3-MK3/183063/bn_7117177267) (used MK3S $200–400 listings)
- [Original Prusa Laserupgrade PLH3D-2W — MYBOTSHOP.DE](https://www.mybotshop.de/Original-Prusa-Laser-upgrade-PLH3D-2W) (€239.95)
- [Original Prusa i3 MK3/S/+ to MK4S upgrade kit — prusa3d.com](https://www.prusa3d.com/product/original-prusa-i3-mk3-s-to-mk4s-upgrade-kit-4/) ($249; confirms Prusa's official kits are printer upgrades, not lasers)
- Community pricing consensus: r/prusa3d / Facebook maker groups ($250–300 fair for used MK3S)

*Receipt closed 2026-09-16. Trust bytes, not reports: nothing physical exists until a scan
hash lands in a receipt.*
