# K8: Lattice-as-Faraday — can the embedded grid BE the shield? (receipt, wave-lane)

- **Gap:** G-J prescribed a foil Faraday box as the #1 confound defense. The operator's
  metal lattice (copper/silver electrode grid embedded in the printed substrate block)
  could double as a partial Faraday shield. Question: which roles compose, which conflict,
  and what does that do to the foil-box requirement?
- **Opened:** 2026-09-16 · agent wave lane · no git, no paid APIs (WebSearch/WebFetch only)
- **Load-bearing context:** `G-J_INSTRUMENT_TIER.md` (foil-box spec, single-point bond law,
  battery-only law, "the leads are where the war is won") · `C19_XMINE_ROUND2.md` P1.1
  (Adamatzky 2026 star array: **16 electrodes → 8 differential compass channels**, 1 Hz ×
  5 days, Pleurotus on wood shavings) · `C17_CUBE_INSTRUMENT_PLAN.md` (ADS1115 rig,
  S0.1 gate < 1 mV RMS dead-substrate) · `DESIGN_MULTISPECIES_LATTICE_20260916.md` (cube 2
  = printed two-species block, electrodes AT zone lines).
- **Sources budget:** free web only; every load-bearing number gets a URL in this receipt.
  [V] = byte-verified this session · [F] = flagged, canon-consistent, not byte-verified.

## Appended log (chronological)

- [~19:00] Receipt opened (BEFORE research, per receipt-FIRST law). Context loaded from
  G-J/C19/C17/design files. Research queue: (1) shielding physics at 50/60 Hz + kHz —
  E vs H field, skin depth, mesh/aperture rules at sub-RF; (2) guard-ring / driven-shield
  instrumentation technique; (3) grounding scheme + role-conflict analysis; (4) verdict on
  the foil-box requirement.
- [x] GATHER round 1 (WebFetch, live bytes — WebSearch degraded-then-recovered):
  - **Skin depth [V]** (Wikipedia "Skin effect"): δ = √(2ρ/ωμ); **copper @ 60 Hz = 8.5 mm
    (8420 µm), @ 50 Hz = 9.22 mm, @ 10 kHz = 652 µm, @ 1 MHz = 65.2 µm**. Our lattice wire
    (0.2–0.5 mm) is ~20–40× UNDER one skin depth at mains frequency.
  - **What a Faraday shield actually does at low frequency [V]** (Wikipedia "Faraday cage"):
    shielding of E-fields is **electrostatic charge redistribution** — mobile charges cancel
    the interior field; skin depth is NOT the mechanism. "Faraday cages cannot block stable
    or slowly varying magnetic fields" — a compass still works inside. Mesh rule: holes
    "significantly smaller than the wavelength."
  - **The 100 kHz crossover [V]** (Wikipedia "Electromagnetic shielding"): "For static or
    slowly varying magnetic fields (below about 100 kHz) the Faraday shielding described
    above is ineffective" — high-µ materials (mu-metal/permalloy) are the magnetic answer
    (they *draw in* the field; closed container shape); eddy-current cancellation only
    works for varying fields; electric-field shielding works at ANY frequency down to DC
    via induced charge.
  - **Driven shield / guard technique [V]** (BioSemi, MettingVanRijn et al.,
    biosemi.com/publications/artikel3.htm): shielded input cable capacitance *reduces
    amplifier input impedance* and worsens interference (divider effect); per-channel
    guarding — "when a shield is driven with the signal at the inner wire, there is
    virtually no cable capacitance" (quoting Morrison 1977) — needs one buffer per input;
    **averaged guarding** drives all shields with the buffered **common-mode** (average of
    inputs), driver gain **0.99** for stability margin → effective cable capacitance cut
    by **factor ~100**; stability needs unity gain DC–MHz and small compensation caps.
    Body/mains numbers: C_body ≈ 300 pF, C_pow ≈ 3 pF, 220 V @ 50 Hz drives ≈ 0.5 µA p-p
    interference current through the subject (10× variations common).
  - **Interference pathway taxonomy for our band [V]** (Usakli 2010, PMC2817545, "Improvement
    of EEG Signal Acquisition"): mains hum = most important external noise; four pathways —
    (I) **magnetic-field-induced voltage in cable loops**, (II) displacement current onto
    subject dropping across electrode impedance, (III) displacement current on body,
    (IV) potential between measurement electrode and amplifier common. Countermeasure list
    includes "guarding (driven or not)", battery operation, metal enclosure for
    electronics/cables, twisted cabling. Half-cell offsets up to ±300 mV; >1 GΩ input
    impedance recommended.
  - ADI "Shielding and Guarding" (AN-347 class) fetch TIMED OUT 3× — the technique is
    byte-covered by the BioSemi/Usakli sources instead; ADI left as [F] corroboration.
- [x] GATHER round 2 (WebSearch recovered, then arXiv API):
  - **Mesh-as-Faraday math [V]** (Delourme & Hewett, arXiv:1806.10433, "Electromagnetic
    shielding by thin periodic structures and the Faraday cage effect"): rigorous
    homogenization result — a thin periodic layer of perfectly conducting obstacles gives
    "full shielding (the so-called 'Faraday cage effect') occurring only in the case of a
    wire mesh." A grounded periodic mesh behaves like a solid wall for fields varying
    slowly across the pitch. Supports: lattice shell ≈ foil box for the electrostatic
    role, provided the mesh is grounded/driven and closed.
  - **Mesh decay law [F]:** field penetration behind a periodic grid is conventionally
    given as |E| ∝ exp(−2π·d/pitch) (evanescent spatial harmonics; decay length =
    pitch/2π; wire radius a subleading correction). VERIFICATION FAILED this session — the
    two IDs the search summary supplied were wrong on byte-check (arXiv:1612.07743 = an
    axion-production paper; PMC7414290 = a COVID health-disparities commentary) and arXiv
    API queries for the static case came back empty. The design below does NOT depend on
    the exact constant: it keeps every measured point ≥ 1 full pitch behind grounded mesh,
    where ANY of the candidate attenuation curves is ≥ 20–50 dB.
  - **Wavelength arithmetic (c/f, no source needed):** λ @ 50 Hz = 6000 km, @ 60 Hz =
    5000 km → aperture rule trivially satisfied at mains; λ @ 2.4 GHz WiFi = 12.5 cm →
    pitch ≤ 12 mm satisfies λ/10, pitch ≤ 6 mm satisfies λ/20. A 5 mm lattice pitch is
    therefore BOTH an electrostatic shield and a workable RF shield.
- [x] SYNTHESIS: role-conflict analysis + guard spec + grounding scheme written below.
  Leakage arithmetic (EE basics, capacitance value [F]): guard mesh 2–3 mm from signal
  runs ≈ 0.3–1 pF/cm → ~5–10 pF per channel; passive guard (at battery −) with inputs
  biased at mid-rail 1.65 V drives i = 2πfCV ≈ 5 nA @ 50 Hz per channel → ~100 µV
  common-mode across 20 kΩ wet-electrode impedance, killed by ADS1115 CMRR 105 dB [V, G-J
  receipt]; residual differential term from ±10–20% C mismatch ≈ 10–20 µV — invisible vs
  mV Pleurotus spikes, marginal vs the ~30 µV smallest published species average → driven
  guard earns its op-amp for cube 2 zone-line work, optional at stage 0.

---

## FINAL REPORT — K8 lattice-as-Faraday (receipt closure 2026-09-16)

### Answer 1 — the physics at our band (50/60 Hz…kHz), in one table

| Interference | Mechanism (Usakli pathway [V]) | Does copper lattice shield it? |
|---|---|---|
| Mains E-field (capacitive hum) | Displacement current onto substrate/leads (II, III, IV) | **YES — excellent.** Electrostatic charge redistribution, thickness-independent, works down to DC [V]. Mesh = solid wall when grounded and closed [V: arXiv:1806.10433]. |
| Mains/transformer B-field (inductive) | Loop induction in lead pairs (I) | **NO.** "Faraday cages cannot block stable or slowly varying magnetic fields" [V]; Faraday-type shielding ineffective below ~100 kHz for H-field [V]; copper delta = 9.22 mm @ 50 Hz [V] vs 0.2–0.5 mm wire. Answer is geometry: twisted pairs, short runs, distance from bricks/motors (G-J lead discipline — unchanged, still required). |
| RF (WiFi 2.4 GHz, switching supplies) | Radiated | **YES if pitch <= ~6–12 mm** (lambda/20–lambda/10 of 12.5 cm) [V: aperture rule]. The lattice pitch is far under. |

The founding insight: at 50 Hz the lambda/10 aperture rule is trivially satisfied (lambda is
5–6000 km) — the foil box was never doing anything magnetic. It was ALWAYS an electrostatic
shield, and **electrostatics does not care whether the conductor is solid, foil, or mesh** —
it cares that the conductor is (a) continuous-ish, (b) closed, (c) referenced to a low
impedance (ground or guard drive). A printed copper/silver lattice meeting those three
conditions IS the cage for the dominant confound.

### Answer 2 — three roles, two nets: what composes and what conflicts

| Role pair | Verdict | Why |
|---|---|---|
| (a) electrode grid + (c) hum shield | **COMPOSE — as two separate metals/zones** | Sensing pads INSIDE the substrate; shield shell = the block's printed wall itself. The substrate is born inside the cage — no assembly step, no lid-lift; the defense is load-bearing structure. |
| (b) guard ring + (c) hum shield | **COMPOSE — a driven guard IS a shield, a better one** | Driven at the input common-mode, the guard's interception capacitance sees dV ~ 0 → no leakage term at all (BioSemi: factor ~100 cable-C reduction, gain-0.99 recipe [V]). Strictly better than passive ground for high-impedance nodes. |
| (a) electrode grid + (b) guard ON THE SAME METAL | **CONFLICT — forbidden** | One wire cannot touch the ionic medium AND carry drive: guard current into the substrate = electrolysis (DC), polarization drift, half-cell pollution, and a shield-current path straight through the measurement medium. Resolution is insulation + geometric partition, not material choice. |
| driven-guard + single-point ground bond | **CONFLICT — pick one net** | If the guard mesh touches the shield/ground net anywhere, the drive buffer is shorted. Two nets (GUARD driven, SHIELD grounded) or one net (both passive). Never both. |
| shield + substrate contact | **CONFLICT — encapsulate** | The substrate is an exposed ionic conductor: any un-insulated shield metal facing it becomes a giant uncontrolled electrode, and mains displacement current couples INTO the medium (Usakli pathway II [V]). Every non-electrode lattice metal gets a printed/conformal barrier; >10 Mohm wet is the pre-flight gate. |

**Compose-vs-conflict VERDICT: the roles compose at the SYSTEM level and conflict only at
the METAL level.** Three roles resolve into two shield nets + the electrode nets:
**SHIELD** (outer shell + lid + port collars — one net, one ground bond) and **GUARD**
(inner ring + inter-pair ribs + lead sleeves — one net, buffer-driven at mid-rail). The
electrode grid stays its own 16 nets, Ag/AgCl-padded, and is the ONLY metal that touches
the biology. G-J's single-point bond law is preserved and extended: the guard buffer's
reference is the same battery-minus star.

### Answer 3 — guard-ring spec for the 16-electrode star mux (the deliverable)

**Geometry (star array, Adamatzky compass layout, 16 electrodes -> 8 differential pairs):**
1. **GUARD ring:** annular mesh band in the print, radius >= 5 mm beyond the outermost
   electrode, full circle, one electrically common net.
2. **GUARD ribs:** fingers extending inward BETWEEN adjacent electrode pairs (in the
   compass gaps), terminating >= 5 mm from any electrode pad and >= 2 mm from any signal
   trace — this guards the radial lead runs, where pickup actually happens.
3. **Lead sleeves:** the 8 twisted pairs exit through the GUARD mesh; the guard overlaps
   the first >= 5 cm of each cable run (or braid the exit cables' shield INTO the guard
   net at the ADC end only — G-J's end-law, now applied to the guard).
4. **Spacing law:** >= 2 mm guard-to-signal everywhere (keeps C_guard-signal ~0.3–1 pF/cm
   [F]; passive residual ~10–20 uV differential, ~0 driven).
5. **SHIELD shell:** separate mesh/foil layer over the block's outer wall + lid + port
   collars, >= 3 mm OUTSIDE the guard ring, electrically separate from it (driven-guard
   config) or bonded to it (passive config). Fruit-body exit ports get a metal collar
   bonded to SHIELD — the mushroom is a probe through the cage; collar it.

**Drive (the "ADC reference" translation):** the ADS1115 breakout exposes no reference
pin; on a 3.3 V single-supply rig the input common-mode is the mid-rail divider
(2 x 100 kOhm, 100 nF decoupled) that biases the electrode pairs — so:
- **Stage 0 (passive):** GUARD and SHIELD both bonded to battery-minus at the ONE star
  point. $0, zero new parts, zero stability risk. Residual ~10–20 uV differential
  (C-mismatch term) — 30–100x under the S0.1 gate and under the smallest published
  species-average spike.
- **Stage 1 (driven, cube-2 upgrade):** one RRIO CMOS op-amp (MCP6001 class), non-inverting
  input = the mid-rail divider, output -> GUARD net through 1 kOhm isolation R. Because our
  common-mode is a design constant (bias resistors), the guard is a STATIC reference drive —
  no signal bootstrapping, so BioSemi's 0.99-gain stability dance is unnecessary; the
  isolation R handles the mesh's few-hundred-pF load. Residual dV across guard capacitance
  ~ buffer error x C-ratio -> uV-nV class at 50 Hz. Add only if zone-line uV ambitions
  survive stage-1 magnitude data (same gate logic as the ADS1220 trigger in G-J).

**Grounding scheme (ties lattice-as-shield to the battery rig safely):**
- Battery-only law unchanged (G-J). All loop voltages are <= 3.3 V + electrode half-cells
  (+/-300 mV class [V]) — no shock path; the single bond doubles as the ESD bleed.
- ONE star point at the first ADS1115's GND. SHIELD -> star (one clip). GUARD buffer
  reference -> same star. No other connection between any shield metal and anything else
  exists; charging the power bank while measuring = forbidden (it reintroduces mains).
- Pre-flight adds three DMM checks to the G-J continuity ritual: SHIELD any-point < few
  ohm; GUARD-vs-any-electrode > 10 Mohm; SHIELD-vs-any-electrode > 10 Mohm (wet-substrate
  readings logged per session — drift in this number is itself shield-integrity evidence).

### Closing verdict — the three mandated answers

1. **Compose vs conflict:** roles compose at system level, conflict at metal level.
   Two-net architecture (SHIELD grounded + GUARD passive/driven) + insulation partition
   captures all three roles. The one hard prohibition: no single piece of metal may be
   both electrode and guard/shield.
2. **Guard-ring spec:** annular ring + inter-pair ribs + 5 cm lead-sleeve overlap,
   >= 2 mm from all signal metal, driven at mid-rail by one follower (stage 1) or bonded
   to battery-minus (stage 0) — full spec in Answer 3.
3. **Does a shielded lid + shielded traces materially reduce the foil-box requirement?**
   **YES — materially, not totally.** For the SUBSTRATE VOLUME, lattice shell + lid +
   guarded leads replaces the foil box's function for the dominant confound (capacitive
   mains hum), and in one respect does it better: the block is enclosed at birth, with the
   substrate >= 1 full pitch behind grounded mesh everywhere (>= 20–50 dB by any candidate
   attenuation curve). The foil box retains TWO jobs: (i) enclosing the LOGGER side —
   ESP32 + ADCs + their wiring is itself a switching-noise radiator that needs containment
   (the $12 foil tub or a metal project box); (ii) calibration reference for the A/B
   experiment below. **The B-field gap is identical for both** (copper and foil are
   equally transparent at 50 Hz [V]) — twisted pairs + distance remain the only defense,
   exactly as G-J wrote. **Falsifiable demotion gate (house style):** dead-substrate A/B,
   1 h per arm, foil box ON vs lattice-shield-only, log RMS in the 50 Hz band + broadband:
   if lattice-only meets S0.1 (< 1 mV RMS; stretch < 100 uV), the foil box demotes to
   electronics-enclosure duty and the lattice carries the defense; if not, it stays
   primary and the lattice shield is a bonus layer. Either way the A/B run turns the
   defense into DATA — the shielding factor of the operator's own lattice, measured, not
   assumed. "Turn the defense into the substrate," executed twice over.

### Sources (all free-tier; [V] = byte-verified this session, [F] = flagged)

1. [V] Wikipedia, "Skin effect" — copper delta: 8.5 mm @ 60 Hz, 9.22 mm @ 50 Hz, 652 um
   @ 10 kHz: en.wikipedia.org/wiki/Skin_effect
2. [V] Wikipedia, "Faraday cage" — charge-redistribution mechanism; "cannot block stable
   or slowly varying magnetic fields"; aperture-wavelength rule: en.wikipedia.org/wiki/Faraday_cage
3. [V] Wikipedia, "Electromagnetic shielding" — Faraday shielding ineffective for H below
   ~100 kHz; mu-metal class for magnetic; aperture rules: en.wikipedia.org/wiki/Electromagnetic_shielding
4. [V] BioSemi / Metting van Rijn et al., "Active electrode technology" — driven shield at
   common-mode, gain 0.99, factor-100 cable-C reduction, per-channel vs averaged guarding:
   biosemi.com/publications/artikel3.htm
5. [V] Usakli 2010, "Improvement of EEG Signal Acquisition: An Electrical Aspect,"
   Comput Intell Neurosci (PMC2817545) — interference pathway taxonomy (I–IV), guarding
   "driven or not", battery operation, +/-300 mV half-cell, >1 Gohm inputs:
   pmc.ncbi.nlm.nih.gov/articles/PMC2817545/
6. [V] Delourme & Hewett, "Electromagnetic shielding by thin periodic structures and the
   Faraday cage effect," arXiv:1806.10433 — homogenized wire-mesh layer gives full
   Faraday-cage shielding: arxiv.org/abs/1806.10433
7. [F] Mesh decay constant exp(-2*pi*d/pitch): physics-standard (evanescent spatial
   harmonics) but the specific citations surfaced this session failed byte-check
   (arXiv:1612.07743 = axion paper; PMC7414290 = COVID paper) — DO NOT CITE those IDs.
   Design de-risked so the verdict does not depend on the constant.
8. [F] ADI AN-347 "Shielding and Guarding" — fetch timed out 3x; technique independently
   covered by sources 4–5.
9. [F] C_guard ~ 0.3–1 pF/cm at 2–3 mm spacing — engineering estimate; measure it in the
   A/B run if the driven guard is ever built.
10. [V-inherited] G-J receipt numbers reused: ADS1115 CMRR 105 dB, noise tables, foil-box
    spec, single-point bond law, lead discipline (receipts/G-J_INSTRUMENT_TIER.md).

**Status: FILED 2026-09-16.** No git, no paid APIs. Two search-supplied citations were
byte-checked and rejected (logged in [7]) — the receipt's numbers are only those verified
above or flagged [F]. Nothing purchased; the demotion gate (Closing verdict 3) is
operator-gated like all stage-0 spend.
- [x] Final: compose-vs-conflict verdict + guard-ring spec + foil-box demotion verdict.
