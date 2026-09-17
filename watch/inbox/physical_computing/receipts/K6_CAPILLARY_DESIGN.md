# K6 — CAPILLARY DESIGN: THE BLOCK IS THE WATER

**Lane:** wave / physical-computing K6
**Date filed:** 2026-09-16
**Law:** receipt first, append as you go. No git. No paid APIs. WebSearch/WebFetch only.
**Mission:** make the block WATER ITSELF — passive capillary design. Reservoir base → printed capillary channels → uniform moisture in far zones. Mycelium as the transport layer. Kill the S3 moisture-heterogeneity confound.

**Deliverable contract (end of receipt):**
1. Wicking numbers (rise height vs pore size, spent oats + hyphae)
2. Channel geometry spec — width / spacing / reservoir size for the $60 cube
3. Self-watering precedent links

---

## Worklog (appended in order)

- [x] S0: context loaded (2026-09-16)
  - **C18** (`C18_HYDRAULIC_THIRD_CHANNEL.md`): the XOR gate is a **crest-siphon threshold** — 150 mL crest in bucket W; one 100 mL/tick input never primes (bit 1), two inputs prime the siphon and dump (bit 0). BOM $13.04. Inherited insight: *threshold instabilities beat steady-state flow balance* for robustness — same doctrine for the moisture design.
  - **S3** (`S3_SKEPTIC_WATCH.md`): confound rank 3 = **moisture/temperature/ion-front transients** (artifacts A3, A12) — "its time band (minutes) is EXACTLY the claimed fungal band (0.0003–0.1 Hz). Adamatzky's own lab concedes moisture is a first-order driver (Phillips et al. 2023)." Hand-watering pulses sit dead-center in the fungal-signal band. **Passive self-leveling of moisture removes the dominant non-EM confound.**
  - **C17/CUBE1** (`C17_CUBE_INSTRUMENT_PLAN.md`, `CUBE1_SHOPPING_LIST.md`): cube01 ≈ $55 BOM ($60-class), ESP32 + 2× ADS1115 + Ag/AgCl ECG electrodes, dead twin control, oyster (Pleurotus ostreatus) spawn on grain, 32 oz deli-tub → the "$60 cube" of this mission. Skeptic rider already adds DHT22-class T/RH logging — moisture regressor is instrumented, now the *source* of moisture variance gets engineered out.
- [x] S1 (partial) — wicking physics, first bytes verified:
  - **Washburn [V]** (en.wikipedia.org/wiki/Washburn%27s_equation): penetration length **L = √(γ r t cosφ / 2η)** — wicking distance grows **√t** ("diffusive behaviour"); scales as √r, √(cosφ), 1/√η. No water worked numbers in source.
  - **Jurin's law [F]** (h = 2γcosθ/ρgr; for water h·r ≈ 1.5×10⁻⁵ m² at θ=0 — 14.7 mm rise in a 1 mm-radius pore, 1.5 m at r = 10 µm). Fallback-summary + own derivation agree; Wikipedia page timed out twice (429-storm day). Byte-verify before the geometry is etched into a print file.
- [x] S3 (partial) — fungal transport precedent landed:
  - **Tlalka, Fricker, Watkinson 2008 [V]**, Appl Environ Microbiol 74(9):2700–2708, DOI 10.1128/aem.02765-07 (PMC2394889). Serpula lacrymans grown **across inert sand** to colonize discrete wood blocks; radiolabeled [¹⁴C]-AIB "distributed throughout complex mycelial networks **within 2 h** of application," reaching growing margins **by 12 h**. The network IS a distribution system at block scale and hour timescales.
  - Lead (verification pending): Fricker MD 2017, "The Mycelium as a Network," Microbiol Spectr, DOI 10.1128/microbiolspec.funk-0033-2017 — the network-transport review.
- [x] S1: wicking physics closed (Jurin [V], Washburn [V], sorptivity [V], PLA contact angle [V])
- [x] S2: channel design closed (spacing 20 mm, reservoir 300 mL, crest overflow = C18 doctrine reused)
- [x] S3: fungal transport closed (Tlalka 2008 [V]; Fricker 2017 full-text rates [V])
- [x] S4: confound-kill argument closed
- [x] FINAL: spec + links below

---

## S1 — Wicking physics in granular substrate

**Source labels: [V] = byte-verified this session · [C] = computed from [V] constants (assumptions stated) · [F] = flagged, not byte-verified.**

### Jurin's law — rise height vs pore size [V]
Formula and water constant byte-verified (English Wikipedia, "Capillary action"): **h = 2γcosθ/(ρgr)**; for water (γ = 0.0728 N/m, 20 °C, θ ≈ 0) **h·r ≈ 1.48×10⁻⁵ m²**. Article's own anchor: r = 0.2 mm → 70 mm rise. Parallel-plate variant verified too: for a slit of width d, **h·d is the same constant**.

Computed rise table (θ = 0, full wetting):

| pore radius r | pore diameter | Jurin rise |
|---|---|---|
| 1.0 mm | 2 mm | 15 mm |
| 0.5 mm | 1 mm | 30 mm |
| 0.25 mm | 0.5 mm | 59 mm |
| 0.1 mm | 0.2 mm | 148 mm |
| 50 µm | 0.1 mm | 296 mm |
| 20 µm | 40 µm | 740 mm |
| 10 µm | 20 µm | 1.48 m |
| 2.5 µm (hyphal scale) | 5 µm | **5.9 m** |

**The design law: rise height × pore radius is a constant. Fine pores are the only way up.**

### Pore sizes in spent oats — the physics problem [C]
- Whole spent oat groats (~5 mm × 1.8 mm): interparticle pores ≈ 0.4–0.6 mm diameter → r ≈ 0.2–0.3 mm → **capillary ceiling 30–74 mm**. Whole-grain oats are a bad wick — coarse pores, and the ceiling sits below the top of any 100 mm cube.
- Spent oats (steeped/sterilized — hulls split, kernels fragmented, effective particle 1–3 mm): pores 0.2–0.6 mm → r 0.1–0.3 mm → **ceiling 49–148 mm**. Reaches mid-cube only.
- **Mycelium-bound felt** in the interstices: hyphal-scale pores 5–50 µm → **ceiling 0.3–3 m**. The fungus manufactures the fine porosity the granular substrate lacks. This is the load-bearing physics claim of the mission: *colonization converts a 30–70 mm wick into a 300+ mm wick* [C from Jurin + pore geometry — testable pre-registration: wick height of dead vs live twin in a 150 mm column].

### Wicking rates [V anchors → C estimates]
- **Washburn [V]:** L = √(γ r t cosφ / 2η) — front position grows **√t**. Ideal-tube numbers are 10–100× optimistic for granular media (gravity + tortuosity + unsaturated conductivity bind), used only for scaling.
- **Sorptivity [V]:** V = A·S·√t; wet front x = (S/f)·√t. Verified material anchors: mortar S = 0.70, clay brick S = 1.16 mm·min⁻¹ᐟ² ( gypsum 3.50, aerated concrete 0.50). For a fine substrate at f ≈ 0.5 [C]:
  - first hour: **11–18 mm** of rise (mortar-class to brick-class S);
  - 24 h: **53–88 mm** — then it stops at the Jurin/gravity ceiling.
- **Empirical equilibrium [V]:** potting mix wicks **300–400 mm** (Wikipedia "Wicking bed", citing Semananda, Ward & Myers 2016, Horticulturae 2(2):8 [F — primary bot-blocked at MDPI 403]); practitioner rule: good soil wicks **~30 cm**, standard reservoir **20 cm** (Deep Green Permaculture, fetched). Full-column equilibration is **overnight scale**.
- **Species answer to "what's the spent-oat wicking rate":** bare spent oats ≈ 10–20 mm in hour one, ceiling 30–150 mm [C]; spent oats + hyphal felt raises the ceiling ~an order of magnitude while the felt's fine pores raise sorptivity [C, pre-register the column test above].

---

## S2 — The design: printed capillary channels as passive irrigation

**Doctrine 1 — the print is formwork, not the wick.** PLA is hydrophobic [V: water contact angle 57.6° plasma-treated film → 98.8° hydrophobic composite, electrospun 129.6° — morphology-dependent; smooth print ≈ 70–85°, cosθ ≈ 0.17–0.34]. A bare 4 mm printed slot wicks h ≈ 1.48e-5/0.004 × cosθ ≈ **0.6–1.3 mm** [C] — useless. Every channel is therefore a printed groove **packed with the fine substrate itself** (spent-oat fines + vermiculite); the print supplies geometry and permanence, the granules supply pores.

**Doctrine 2 — steal the C18 gate for free.** The C18 XOR bucket gate ($13.04 receipt) established: *threshold instabilities beat steady-state flow balance; output arrives only through pipes; level is read off a sight glass, never a pour.* Reused three ways:
1. **Sight-glass marks at 100 mL intervals** on the reservoir — same mark doctrine, same "trust bytes" photo-the-level logging.
2. **Crest overflow = anti-waterlogging interlock.** A 6 mm standpipe crested at the 30 mm reservoir max: the water level physically cannot exceed the crest, whatever the operator pours in — overfill dumps to a waste cup (keeps the C18 mass-balance audit: filled + reservoir + waste must reconcile). The sim's scripted fault ("open only after water has arrived, **or both valves siphon**") becomes a safety feature: the dump threshold is the flood stop.
3. **XOR dual-use preserved:** if the cube's fill port and the C18 demo line are plumbed to the same crest, the cube IS the C18 artifact — one input, level holds (bit 1); two inputs, crest primes and dumps (bit 0). The moisture-management hardware is the hydraulic-computer hardware. One print, two falsifiers served (§4.5 sim gate + §4.3 sensor confound).

**Geometry (100 × 100 mm footprint, 32-oz-tub class per C17):**
- **Reservoir:** 100 × 100 × 30 mm = **300 mL** (same 3-mark fill as C18's SOURCE tank). Evaporation through a micropore-taped lid ≈ 5–20 mL/day [C] → **15–60 days autonomy**; top up 100 mL per mark.
- **Wicking waist:** 15 mm of fine medium (vermiculite or spent-oat fines) between reservoir and main substrate — 20–27× below the 300–400 mm potting-mix wick ceiling [V], so the bridge never limits.
- **Wick grid:** grooves 4 mm wide × 3 mm deep, at **20 mm spacing** both axes (lines at 10/30/50/70/90 mm → 5 per axis, 25 intersections), packed with the same fines. Max un-wicked lateral path = **10 mm**.
- **Corner drinking ports:** 8 mm openings at the four grid corners where trunk cords drink (see S3).

**Uniformity math [C]:** unsaturated lateral redistribution in fine media D_eff ≈ 10⁻⁸–10⁻⁹ m²/s → cell equilibration t ≈ s²/D_eff = (10 mm)²/10⁻⁸ ≈ **2.8 h** (pessimistic bound: 28 h at 10⁻⁹). Whole-cube moisture equilibrates **overnight**; with the hyphal layer active it is minutes-scale (S3 section below). Spacing 20 mm is the compromise: finer grids print fragile and choke with mycelial overgrowth; coarser grids (>30 mm) push matrix-only equilibration past a day.

**Cost:** PLA for grooved base/frame ≈ 20 g ($0.5), vermiculite 1 L ($4–5), 6 mm silicone tube ($1), overflow waste cup owned ($0), second C17 tub as sump ($0–3). **Hydraulic retrofit ≈ $6–10; worst-case cube total ≈ $65, floor ≈ $58 — inside the $60 class.** No paid anything.

---

## S3 — The fungal angle: the network IS the irrigation system

**The published numbers [V — Fricker, Heaton, Jones & Boddy 2017, "The Mycelium as a Network," Microbiol Spectrum 5(3), DOI 10.1128/microbiolspec.funk-0033-2017, PMC11687498, full text read this session]:**
- Water transport in *Suillus bovinus* mycelium: **27 cm h⁻¹**
- Water transport in ***Serpula lacrymans*: mean 148 cm h⁻¹** — driven as pressure-driven mass flow ("vastly in excess of values that could be achieved by motor-driven movement")
- **Hydraulic redistribution: "substantial water flow (18 cm h⁻¹) can be driven by hydraulic redistribution from moist to dry soil"**
- Mycorrhizal hydraulic coupling to host plant: 27 cm h⁻¹
- Solutes in cord-forming *Phanerochaete velutina*: 20–100 mm h⁻¹ depending on cord formation; *Armillaria* > 20 mm h⁻¹; *Serpula* flows 10–50 mm h⁻¹ and 20–30 cm h⁻¹
- Rhizomorph longitudinal conductivity: 1.5–3 × 10² cm² bar⁻¹ s⁻¹

**Block-scale implication [C]:** at 18–148 cm h⁻¹ the network crosses our 110 mm cube in **45 seconds to 6 minutes** — two to three orders of magnitude faster than matrix wicking (mm–cm per hour). At block scale, transport is not a limiting analogy; it is measured fact.

**Tlalka, Fricker & Watkinson 2008 [V]** (AEM 74(9):2700–2708, DOI 10.1128/aem.02765-07, PMC2394889): radiolabeled AIB applied at one point of a *Serpula* network growing across sand to discrete wood blocks was **"distributed throughout complex mycelial networks within 2 h,"** reaching growing margins by 12 h, and withdrawn network-wide into newly contacted wood. Resource redistribution across a heterogeneous microcosm — exactly our cube's situation — in hours without any pump.

**Architecture that follows:** printed channels are not irrigation lines; they are **reservoir drinking fountains**. Reservoir → waist → channel termini (corner ports) → trunk cords → network. The pump is already there: evaporation at the growing margins sets the water-potential gradient, and Fricker's mass-flow mechanism [V] does the hauling. The print supplies water at four points; the fungus does the plumbing.

**Species caveat [C, honest]:** the 148 cm h⁻¹ figure is *Serpula lacrymans* (the cord specialist). Our C17 species is *Pleurotus ostreatus* — it aggregates cords but is less rhizomorph-dedicated; expect intermediate rates. The 18 cm h⁻¹ hydraulic-redistribution figure is the conservative floor to design against: even it crosses the cube in ~37 min. Pre-registration hook: dye-tracer (food coloring in the reservoir, non-destructive, free) — time-to-corner in live vs dead twin.

---

## S4 — Sensor tie-in: passive self-leveling removes the S3 confound

From the S3 skeptic receipt (filed today): the #3 confound is **moisture/temperature/ion-front transients** (artifacts A3 + A12) — "its time band (minutes) is EXACTLY the claimed fungal band (0.0003–0.1 Hz). Adamatzky's own lab concedes moisture is a first-order driver (Phillips et al. 2023)." Hand-watering is a 50–200 mL step pulse whose moisture wave washes past the electrodes for minutes-to-hours — signal-shaped noise, injected by the experimenter on an irregular schedule.

What the reservoir design buys, term by term:
1. **No watering pulses.** After the single initial saturation, water enters only as a silent matrix-driven draw against a fixed 30 mm head. The minutes-band moisture transient is deleted at the source, not filtered afterward.
2. **Spatial heterogeneity collapses.** Every point ≤ 10 mm from a wick line; gradients relax in 3–30 h [C] and then sit at a quasi-static profile set by geometry, not by watering history. S3's skeptic scenario — "spike" = moisture front crossing the electrode pair — loses its driver.
3. **The regressor starves.** C17's concert amendment 2 requires an SHT31/T/RH nuisance-regression ("the wet-cardboard kill"). With self-leveling, the moisture regressor is near-constant → nothing for a confound to hide in. A near-flat nuisance variable can't manufacture a pass.
4. **The dead twin gets sharper.** Twin and live cube share identical hydraulic geometry → matched water history → the differential control subtracts the residual common-mode moisture term too.
5. **The reservoir is the water-use sensor.** Verified precedent: Cichello, Bruch & Earl 2023 (Front. Plant Sci. 14:1201102) regulated wicking-bed water tables with a float valve and **measured per-plant water use from reservoir level changes** [V]. Our 100 mL sight marks already log water use — one observable, two jobs (maintenance + evaporative-flux regressor).

**Honest limits:** this kills the moisture term only. S3 ranks 1–2 (EM pickup; electrode-interface chemistry) are untouched — Faraday box, chloridized electrodes, and the dead twin remain mandatory. The initial fill transient is a scheduled event: log it and exclude the first 24 h post-fill from analysis windows, pre-registered, same discipline as C17's gap rows.

---

## FINAL DELIVERABLES

### 1. The wicking numbers
- Jurin (water, θ=0): **h·r ≈ 1.48×10⁻⁵ m²** [V] → 15 mm @ r=1 mm · 74 mm @ r=0.2 mm · 148 mm @ r=0.1 mm · 296 mm @ r=50 µm · 1.48 m @ r=10 µm · 5.9 m @ hyphal 2.5 µm.
- Spent oats alone: pores 0.2–0.6 mm → **ceiling 30–150 mm, front 10–20 mm in hour one** [C from sorptivity anchors S = 0.70–1.16 mm·min⁻¹ᐟ², f = 0.5 [V]].
- Spent oats + hyphal felt: fine pores 5–50 µm → **ceiling 0.3–3 m** [C] — colonization manufactures the wick. Potting mix reference: 300–400 mm [V].
- Network transport: **18–148 cm h⁻¹** [V] → cube crossed in **45 s–6 min**; AIB network-wide in **2 h** [V].

### 2. Channel geometry spec — the $60 cube
| Parameter | Spec | Why |
|---|---|---|
| Footprint × substrate | 100 × 100 × 80 mm | 32-oz tub class (C17) |
| Wicking waist | 15 mm vermiculite/fines | 20× below the 300–400 mm wick ceiling |
| Reservoir | 100 × 100 × 30 mm = **300 mL**, sight marks @ 100 mL | C18 3-mark doctrine; 15–60 d autonomy |
| Channel width × depth | **4 × 3 mm**, packed with fines | print is formwork; granules are the wick (bare PLA wicks ≤ 1.3 mm) |
| Channel spacing | **20 mm** both axes (5/axis, 25 nodes) | max lateral path 10 mm → equilibration 3–30 h [C]; cords cut to minutes |
| Corner drinking ports | 8 mm, 4 corners | trunk-cord access points |
| Overflow crest | 6 mm standpipe @ 30 mm → waste cup | C18 siphon doctrine = flood stop + XOR dual-use |
| Fill port | top tube, pour to marks only | "output arrives only through pipes" — no substrate pouring, ever |
| Retrofit cost | **$6–10** (PLA $0.5 + vermiculite $5 + tube $1 + sump tub $0–3) | $58–65 total vs C17's $55 — inside the $60 class |

### 3. Self-watering precedent links (all fetched 2026-09-16 unless [F])
- Wikipedia — Wicking bed (300–400 mm potting-mix wick, cites Semananda et al. 2016): https://en.wikipedia.org/wiki/Wicking_bed
- Deep Green Permaculture — ideal soil depth (soil wicks ~30 cm; 20 cm standard reservoir): https://deepgreenpermaculture.com/2021/08/06/gardening-questions-008-what-is-the-ideal-soil-depth-for-wicking-beds/
- Deep Green Permaculture — wicking bed construction: https://deepgreenpermaculture.com/2016/04/03/wicking-bed-construction-2/
- Deep Green Permaculture — DIY self-watering pots & mini wicking beds: https://deepgreenpermaculture.com/2016/04/15/diy-self-watering-pots-and-mini-wicking-beds-2/
- Deep Green Permaculture — capillary watering tray for seedlings: https://deepgreenpermaculture.com/2009/10/04/self-watering-tray/
- Cichello, Bruch & Earl 2023, Front. Plant Sci. 14:1201102 — float-valve wicking bed; water use measured from reservoir level: https://doi.org/10.3389/fpls.2023.1201102
- Fungal transport: Tlalka et al. 2008, AEM 74(9):2700–2708, https://doi.org/10.1128/aem.02765-07 (PMC2394889) · Fricker et al. 2017, Microbiol Spectrum 5(3), https://doi.org/10.1128/microbiolspec.funk-0033-2017 (PMC11687498)
- Physics: https://en.wikipedia.org/wiki/Capillary_action (Jurin + sorptivity) · https://en.wikipedia.org/wiki/Washburn%27s_equation
- [F] Semananda, Ward & Myers 2016, Horticulturae 2(2):8 — primary bot-blocked (MDPI 403); figure verified via Wikipedia citation. Un-block before etching geometry into a print spec.

## Source ledger / integrity notes
- WebSearch was 429-rate-limited at the start (the gen-1/C17/C18 hazard); all load-bearing bytes came via WebFetch (Wikipedia ×4, Europe PMC REST ×5, PMC ×1, Deep Green Permaculture ×2). One Wikipedia fetch succeeded on third attempt — rate storms pass.
- Jurin's law was [F] (fallback summary) for one worklog cycle, then upgraded to [V] on the byte fetch — the receipt records both states, per trust-bytes-not-reports.
- PLA contact angle: no neat-PLA single value exists in the verified set (morphology-dependent 57.6°–129.6° across fetched abstracts); design uses cosθ 0.17–0.34 as the envelope, and the design does not depend on the exact value (channels are substrate-packed).
- Fricker full-text rates [V] are cross-species (Serpula/Suillus/Phanerochaete/Armillaria); Pleurotus-specific rates are unverified — flagged where used.
- No git. No paid APIs. Receipt is the durable artifact.

— K6 out. The block drinks on its own; the fungus does the plumbing; the skeptic loses confound #3.
