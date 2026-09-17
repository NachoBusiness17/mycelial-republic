# K2 GALVANOTROPISM — receipt (wave lane)

- **Lane:** K2 physical computing / "physics works WITH our system" anchor
- **Question:** does an applied low-voltage electric field STEER fungal hyphal growth (galvanotropism)? If yes, our embedded low-voltage lattice is not just sensing the mycelial network — it is printing wiring by asking the biology to grow onto it.
- **Written:** 2026-09-16 (append-as-you-go; receipt FIRST per wave-lane law)
- **Method constraints:** no git, no paid APIs. WebSearch + WebFetch + PubMed E-utilities (free).
- **Status:** RESEARCH IN PROGRESS — sections below fill in as evidence lands.

## Plan
1. Classic galvanotropism literature (fungi, hyphae, DC fields) — species, thresholds, direction (anode/cathode).
2. Mechanism: field vs current vs gradient; role of extracellular Ca2+ / ionic currents at hyphal tips.
3. Inverse effects: electrolysis at electrodes, pH/byproduct stress, harm thresholds.
4. Verdict: does 3–10 V/cm across a printed block steer hyphae onto embedded traces — yes/no/uncited, with thresholds.
5. Experiment design for OUR cube-2 geometry.

## Findings log
(appending as evidence lands)

### 2026-09-16 — Round 1: the classic literature is real, and small

- PubMed `galvanotropism AND fungi` = **5 hits total**. This is a small, classic, mostly-dormant literature — good for attribution (nobody has productized it), bad for deep replication data.
- The "McGill?" memory = **McGillivray** (first author), with **N.A.R. Gow** (Aberdeen) — the two anchor groups:
  - **McGillivray & Gow 1986**, "Applied Electrical Fields Polarize the Growth of Mycelial Fungi", *J. Gen. Microbiol.* 132(9):2515 (PMID 3960928). Many filamentous fungi polarize in fields; *Trichoderma harzianum* hyphae vs branches oriented in OPPOSITE directions; *N. crassa* germ-tube emergence highly polarized toward one electrode.
  - **Lever, McGillivray, Gow et al. 1994**, "pH and Ca²⁺ dependent galvanotropism of filamentous fungi", *Mycological Research* (cited by 39). Response depends on external pH and Ca²⁺.
  - 1990 *Z. Naturforsch. C* 45(3-4) "Directed Growth of Fungal Hyphae in an Electric Field" (DOI 10.1515/znc-1990-3-427): *N. crassa* angle-distribution study; field-induced membrane-potential change can INHIBIT growth; response of longer hyphae bidirectional (anodal AND cathodal turning).
- Mechanistic core — **Brand & Gow lineage, *Candida albicans***:
  - **Brand et al. 2007**, *Current Biology* 17, PMID 17275302 (PMCID PMC1885950): **10 V/cm, 33 ± 2 mA** → hyphae orient **toward the cathode**; germ tubes emerge almost exclusively on cathode-facing pole; response **positively correlated with extracellular Ca²⁺**; halved by Ca²⁺-depleted medium, Ca²⁺-channel mutants (CaCch1Δ), and L-type channel blockers (verapamil 250 µM, nifedipine 100 µM, diltiazem 500 µM). Crucially: 10 V/cm applied **"without affecting germ-tube formation or hyphal extension rate"** — steering WITHOUT stress at this strength. Mechanism framed as membrane DEPOLARIZATION at the cathodal face opening voltage-gated Ca²⁺ channels → localized Ca²⁺ influx at the growth site. Both numbers (field AND current) reported but field-vs-current not discriminated.
  - Brand et al. 2008 *Euk. Cell* (PMID 18281602): internal polarity landmark (Rax2) required for externally induced hyphal behaviors incl. galvanotropism.
  - Brand & Gow 2014 *PNAS* (PMID 24385582): Cdc42 GTPase dynamics control directional growth responses.
- Review tying it together: **Buffi et al. 2025**, "Electrical signaling in fungi: past and present challenges", PMC11995700 — fungi show galvanotropic behavior (change of growth direction in response to applied field).
- Species known to respond so far: *Candida albicans* (cathodal, robust), *Neurospora crassa* (polarized germ tubes; bidirectional in longer hyphae), *Aspergillus* spp. (Lever 1994; A. niger cited via Bowen 2007), *Trichoderma harzianum* (hyphae vs branches opposite directions).
- Note: PubMed's broader "electric field + fungal" search is polluted by pulsed-field gel electrophoresis — filter by hand.

### 2026-09-16 — Round 2: quantitative thresholds (Gruler & Gow 1990 is the anchor)

- **Gruler & Gow 1990**, *Z. Naturforsch. C* 45(3-4), "Directed Growth of Fungal Hyphae in an Electric Field" (DOI 10.1515/znc-1990-3-427) — the quantitative dose-response paper for *N. crassa*:
  - Germ tubes grew toward the **ANODE** (note: opposite pole from *Candida* hyphae — direction is species/stage-specific, NOT a universal rule).
  - Turning efficiency scales with tip length: a 100 µm germ tube responds to fields ~10x weaker than a 10 µm one (~1.7 vs ~20 V/cm equivalent). **Longer hyphae = more sensitive to small fields.** Good for us: mature mycelium needs less field, not more.
  - Growth coefficient K_P = −18.5 mV, attributed to **field-driven redistribution of charged membrane-bound proteins** — i.e., the cell senses the FIELD VECTOR (works in a uniform electrophoresis chamber with zero field gradient), not a gradient and not bulk current.
  - **Linearity breaks above E₀ = 3.8 V/cm**: field-induced membrane-potential change begins to INHIBIT growth in *N. crassa* (inhibition coefficient 1.11). Mild inhibition, not death — but it sets a per-species comfort ceiling.
  - Longer hyphae can go **bidirectional/perpendicular to the field** when E²·l₀ crosses ~4.4 V²·cm⁻¹ — orientation dynamics are non-monotonic; the field steers growth to its VECTOR, which is not always "toward the electrode".

### 2026-09-16 — Round 3: modern electrotaxis + the harm side

- **Moratto, Rothery, Bozkurt, Sena 2023**, *Phys. Biol.* 20:056005 (PMID 37442125): *Phytophthora palmivora* (oomycete) zoospores in **0.7–1.0 V/cm** swim anode-directed, germination rate INCREASES, germ tubes oriented by the field, encystment unaffected. Weak fields as an accelerant, not a stressor.
- **Moratto et al. 2024**, *Sci. Rep.* 14 (PMID 39198508): **250–550 µA** ionic currents in hydroponics reduce zoospore attachment and root infection in *Arabidopsis*/*Medicago* with **no harm to plant health** — proof that weak-current steering of an invasive mycelial organism works in a real growing system (steering AWAY; our use is steering TOWARD, but the biophysics is the same and it is already practical).
- **Harm/inverse literature** (low-amperage DC is a known antimicrobial — this is the stress channel to avoid):
  - Chavez-Manini et al. 2024, *Indian J. Med. Microbiol.* systematic review (PMID 37437616): **150–500 µA DC** over 1 h–4 days gives 3.5–5.5 log biofilm reduction; kill scales with current × time; **electrode material matters** (redox reactions; Pt vs Ti vs Ag vs carbon differ); 70 µA/cm² DC + tobramycin eradicates persisters.
  - Mechanism channels: electrolysis products at electrodes (anode acidification, chlorine/hypochlorite when Cl⁻ present, ROS) + electroporation-like membrane permeabilization (Sreelekshmi & Venkatasubbu 2026, *Bioelectrochemistry*, PMID 41950578).
  - Crucially these currents run at electrode surfaces for hours-days. Brand 2007 ran **33 mA** through a galvanotropism chamber with no effect on germ-tube formation or extension rate — because the chamber geometry/electrodes kept the biology out of the electrolysis zone. **Field across the colony ≈ fine; DC electrolysis AT electrodes in contact with the colony ≈ the hazard.**
- Methodological caveat from Buffi et al. 2025 (FEMS Microbiol. Rev., PMC11995700): electrode-in-gel setups build **Donnan/interfacial potentials** (Blatt et al. critiques) — "applied field" claims in gel/solid substrates need four-terminal measurement, not supply-voltage arithmetic. Also: the endogenous-transhyphal-current story (Gow 1984: all growing hyphae carry 0.05–0.60 µA/cm² transhyphal currents; non-growing ones don't) is real but its role in steering "cannot be generalized" (Potapova 2012) — the APPLIED-field galvanotropism evidence stands on its own.

## Steering verdict

**YES with a boundary, and the integrated claim is UNCITED (ours to make).**

- **Cited:** fungal hyphae reliably steer in uniform DC fields from **~0.7 V/cm** (oomycete zoospores/germ tubes) through **~1–20 V/cm** (fungal hyphae, sensitivity rising with tip length). Mechanism is field-vector sensing: cathodal-face membrane depolarization → voltage-gated Ca²⁺ channel (CaCch1) opening → localized Ca²⁺ influx at the Spitzenkörper → reoriented tip growth. Uniform fields suffice → the steering cue is E (the field), not the field gradient. A 3–10 V/cm field sits squarely inside the demonstrated steering window.
- **Boundary 1 — species/direction is not universal:** *Candida albicans* hyphae → cathode; *N. crassa* germ tubes → anode; *T. harzianum* hyphae and branches → opposite poles; oomycete zoospores → anode. Direction must be measured per species before relying on it.
- **Boundary 2 — comfort ceiling:** growth inhibition onset ~3.8 V/cm for *N. crassa*; harmless at 10 V/cm for *Candida*. 3–10 V/cm spans "definitely steered, possibly slightly inhibited" — run the dose ladder.
- **Boundary 3 — the hazard is electrolysis, not the field:** DC across a wet substrate is fine for the biology in the field volume (33 mA, no harm) but electrode-metal/substrate contact drives electrolysis (pH shifts, chlorine, ROS) that IS antimicrobial at 70 µA/cm²–500 µA scale over hours. Isolate the chemistry from the biology.
- **Uncited (the novel claim):** NO published study steers mycelium through a solid printed substrate onto embedded conductive traces. Every cited result is liquid/agar chambers with external electrodes. Also untested in ANY literature: whether hyphae follow E or J in a heterogeneous substrate (in homogeneous chambers they are proportional and indistinguishable; in a printed oat block with nutrient traces they diverge). **So: "a 3–10 V/cm field across a printed block will measurably steer hyphae" is literature-supported; "hyphae grow onto embedded traces" is a defensible hypothesis with two published legs (steering at those strengths + currents concentrate through conductors) and no direct precedent. The physics works WITH our system — with per-species direction and electrolysis management as the two things to engineer.**

## Threshold numbers

| Field/current | Effect | Species | Source |
|---|---|---|---|
| 0.7–1.0 V/cm | anodal electrotaxis, ↑germination, oriented germ tubes | *Phytophthora palmivora* | Moratto 2023 (PMID 37442125) |
| ~1.7 V/cm (100 µm tip) / ~20 V/cm (10 µm tip) | turning response, anode-directed | *Neurospora crassa* | Gruler & Gow 1990 |
| 3.8 V/cm | growth-inhibition onset (linearity break) | *N. crassa* | Gruler & Gow 1990 |
| 10 V/cm (33 mA in chamber) | cathodal orientation, **zero harm** to germ-tube formation & extension rate | *Candida albicans* | Brand 2007 (PMID 17275302) |
| 250–550 µA ionic current | reduced zoospore attachment/infection, no host harm | *P. palmivora* on roots | Moratto 2024 (PMID 39198508) |
| 70 µA/cm²–500 µA DC, 1 h–4 d | biofilm kill 3.5–5.5 log (electrolysis/redox + permeabilization) | bacteria | Chavez-Manini 2024 (PMID 37437616) |
| E²·l₀ ≈ 4.4 V²·cm⁻¹ | transition to perpendicular/bidirectional growth | *N. crassa* long hyphae | Gruler & Gow 1990 |

Endogenous baseline for scale: growing hyphae carry transhyphal currents of 0.05–0.60 µA/cm² (Gow 1984) — our injected fields are strong compared to endogenous signaling, so expect a response; that same scale gap is why dosing matters.

## Cube-2 experiment design (steering onto embedded traces, on our two-species printed oat block)

**Pre-cube gate:** run on cube 1 (single species) first — attribution discipline per the lattice design file. Suggested species per cube-2 pairing logic: fast grower vs high-spiker; validate its steering pole (anode/cathode) in a 10-minute agar dish test BEFORE embedding anything (Gruler's angle-distribution assay at 2 V/cm).

1. **Geometry.** Block as designed (spent-oat substrate, nutrient traces printed in, inoculation points per lattice). Add: two BLOCK-END electrodes (the field generators) + the embedded trace array mid-block (the steering targets). Field axis co-oriented WITH the trace direction — hyphae follow the field vector, so the field must point along the wiring you want grown onto, not across it.
2. **Field budget.** Dose ladder 0 (sham) / 0.5 / 1 / 3 / 5 / 10 V/cm, 3 replicates. Expect steering from ~1 V/cm (long tips are sensitive); treat 3.8 V/cm as the *N. crassa*-style inhibition flag; 10 V/cm ceiling (harmless in *Candida*, but verify extension rate).
3. **Electrolysis management.** Block-end electrodes: Ag/AgCl or carbon, large area (cm²-scale, current density ≪ 70 µA/cm²), polarity reversal every 12 h to cancel ion migration drift, and (cleanest) salt-bridge isolation so electrode chemistry happens outside the block. Never let bare DC-driven metal sit in contact with live mycelium for days.
4. **Measure the real field, not the supply voltage.** Donnan/interfacial potentials in gel-solid substrates confound arithmetic (Blatt critique via Buffi 2025). Four-terminal sensing: two drive, two probe electrodes measure the in-block field directly. Log current at the supply — the E/J divergence in the heterogeneous block is a finding either way.
5. **Readout.** Time-lapse (hourly webcam, dark, fixed camera) over the colonization window; extract hyphal tip angles relative to the field axis near the energized trace region; Rayleigh/circular statistics on E-on vs sham vs reversed polarity. Success = significant orientation to the field-predicted pole + extension rate within 20% of sham (no-stress criterion, per Brand 2007). Secondary readout: hyphal density ON the traces vs adjacent substrate (the actual "grew onto the wiring" metric).
6. **The E-vs-J discriminator (the genuinely novel cube-2 result).** Nutrient traces are more conductive than oat substrate, so current path and field vector diverge locally. If hyphae follow **E** (literature default), they align to the field axis; if they follow **J**, they crowd onto the traces (current prefers the conductor). Uniform-chamber literature cannot tell these apart — a printed heterogeneous block can. Either answer is publishable, and the J-answer is the one where the biology literally wires itself onto the lattice.
7. **Cube-2 zone-line interaction.** Once steering is shown single-species, energize only the trace pair AT the zone line: does a 1–3 V/cm field pull the fast grower across the zone into the high-spiker's territory, and do the (charged, dense) zone lines reinforce or override the applied field? That connects K2 directly to the cube-2 hypothesis that boundaries are the active regions.

## Sources

- McGillivray & Gow 1986, *J. Gen. Microbiol.* 132:2515 — https://www.microbiologyresearch.org/content/journal/micro/10.1099/00221287-132-9-2515
- Gow & McGillivray 1986, *Prog. Clin. Biol. Res.* 210:81-8, "Ion currents, electrical fields and the polarized growth of fungal hyphae" (PMID 3960928)
- Gruler & Gow 1990, *Z. Naturforsch. C* 45:243- — https://doi.org/10.1515/znc-1990-3-427
- Lever, Robertson, Buchan, Miller, Gooday, Gow 1994, *Mycol. Res.*, "pH and Ca2+ dependent galvanotropism of filamentous fungi: implications and mechanisms" — https://doi.org/10.1016/S0953-7562(09)80458-9
- Brand et al. 2007, *Curr. Biol.* (PMID 17275302, PMCID PMC1885950) — https://pmc.ncbi.nlm.nih.gov/articles/PMC1885950/
- Brand et al. 2008, *Eukaryot. Cell* (PMID 18281602) · Brand & Gow 2009, *Curr. Opin. Microbiol.* 12:350 (DOI 10.1016/j.mib.2009.05.007) · Brand & Gow 2014, *PNAS* (PMID 24385582)
- Moratto et al. 2023, *Phys. Biol.* 20:056005 (PMID 37442125); Moratto et al. 2024, *Sci. Rep.* 14 (PMID 39198508)
- Buffi et al. 2025, *FEMS Microbiol. Rev.*, "Electrical signaling in fungi: past and present challenges" — https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/
- Chavez-Manini et al. 2024, *Indian J. Med. Microbiol.* (PMID 37437616); Sreelekshmi & Venkatasubbu 2026, *Bioelectrochemistry* (PMID 41950578)
- All PubMed records via NCBI E-utilities (free); no paid APIs used. WebSearch rate-limits hit intermittently 2026-09-16; McGillivray & Gow 1986 exact V/cm values remain paywalled/unverified — "few V/cm" per secondary sources, treat as unverified.
