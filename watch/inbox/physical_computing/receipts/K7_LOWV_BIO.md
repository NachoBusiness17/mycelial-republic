# K7 — Low-Voltage Lattice Traces in a Living Block (receipt)

- Lane: `K7_LOWV_BIO` (wave lane, physical_computing)
- Date opened: 2026-09-16
- Question: where is the line between **stimulating** and **cooking** a living mycelial block that carries embedded lattice traces?
- Rules: receipt-first (this file), appended as researched · no git · no paid APIs · WebSearch/WebFetch only
- Status: **LANDED 2026-09-16** (sections 1–2 appended early, 3–5 closed same session)

## Sections (appended as researched)

1. Electrolysis physics — DC at 3–5 V over days (gas, pH, metal migration)
2. Mitigations — AC / pulsed bipolar drive, charge balancing (electrochem + neuro-stim practice)
3. Field thresholds — fungal galvanotropism V/cm vs damage
4. Species tolerance — chronic field exposure effects on mycelial growth
5. Verdict — safe operating envelope + red lines

---

## 1. Electrolysis physics — what 3–5 V DC does over days

**Thermodynamic line.** Water splits at **1.23 V** (25 °C, Nernst minimum); the thermoneutral voltage is **1.48 V**. Practical electrolysis needs overpotential on top of that (kinetic barriers, bubbles, ohmic drop) — real cells run **~1.7–2.2 V+** before useful current flows. Sources: [ScienceDirect — Decomposition Voltage](https://www.sciencedirect.com/topics/engineering/decomposition-voltage) · [Wikipedia — Electrolysis of water](https://en.wikipedia.org/wiki/Electrolysis_of_water) · [RSC: Low-temperature water electrolysis](https://pubs.rsc.org/ma/article/3/14/5598/771412/Low-temperature-water-electrolysis-fundamentals).

**Two different axes — do not conflate.** The *cell voltage* (3–5 V across the block) sets the **electrode-surface electrochemistry** (the ~1.5–2+ V of overpotential is burned at each electrode, guaranteeing Faradaic reactions). The *field strength* (V/cm = voltage ÷ electrode spacing) is what the hyphae actually feel. 5 V across a 10 cm block is a mild 0.5 V/cm field — but the electrodes still sit at ~3 V of drive and electrolyze hard.

**Faraday's-law arithmetic for a living block** (Q = I·t; F = 96,485 C/mol e⁻):

| DC drive | per electrode per day |
|---|---|
| 100 µA | 8.6 C ≈ 0.09 mmol e⁻ → ~1 mL H₂(g) · ~0.09 mmol strong acid/base · ~2.8 mg Cu²⁺ (if Cu anode) |
| 1 mA | 86.4 C ≈ 0.9 mmol e⁻ → ~10 mL H₂ + ~2.5 mL O₂(g) · 0.9 mmol H⁺/OH⁻ · **~28 mg Cu²⁺** |

In a ~100 mL printed block, 1 mA·day of DC = **~9 mM strong-base/strong-acid equivalent** → cathode-zone pH ≈ 12, anode-zone pH ≈ 2, and bulk drift within days. Cultivated mycelium (Pleurotus, Ganoderma, etc.) is injured below ~pH 4 and above ~pH 9 — the block dies zone by zone from the electrodes outward.

**Gas:** H₂ at the cathode, O₂/Cl₂ at the anode. Bubbles desiccate and delaminate the gel around traces. Worse, spent-oats/agar medium contains chloride → the anode makes **Cl₂ → HOCl/OCl⁻ (hypochlorite = bleach)**, lethal to hyphae at ppm — an unstated killer that plain-water intuition misses.

**Metal migration:** the anode dissolves Faradaically. Cu → Cu²⁺ (~28 mg per mA·day; dissolved-Cu growth inhibition for many fungi sits at **~1–10 ppm**, so 1 mA·day DC makes the block antifungally toxic). Stainless → Fe/Ni/Cr leachate (Ni, Cr biotoxic). Ag → Ag⁺ (oligodynamic antimicrobial — fine for sensing, poison at mA·days). Copper traces as anodes under DC visibly corrode within days.

**Bottom line for step 1:** 3–5 V DC is not a "weak" drive in a living block — it is a continuous chemical-reactor setpoint: pH fronts, chlorine chemistry, metal ion plating into the mycelium, and gas damage, all scaling with total charge passed (I × days).

## 2. Mitigations — charge-balanced pulsed/AC drive

**The canonical fix (neuro-stimulation practice, decades of in-vivo evidence):** never pass net DC. Use **biphasic charge-balanced pulses** — a stimulating phase followed by an equal-and-opposite reversal phase — so net Faradaic product per cycle ≈ 0 (pH, gas, and metal dissolution all stop accumulating).

- Practice & rationale: [16-ch biphasic charge-balanced stimulator (PMC5556675)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5556675/) · [Biphasic charge-balanced pulses (PLoS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0018738) — "charge-balanced to avoid unintended chemical reactions by charge accumulation."
- **Shannon (1992)** safety boundary: log₁₀(Q/A) = k − log₁₀(Q), k ≈ 1.5–1.85 for Pt electrodes in vivo ([Shannon, IEEE TBME 39(4):424–426](https://ui.adsabs.harvard.edu/abs/1992ITBE...39..424S/abstract)). Practical translation: keep **charge density per phase ≲ 30 µC/cm²** (smooth Pt injects ~50–150 µC/cm² before the water window; carbon/graphite lower, activated iridium oxide up to ~1–3 mC/cm²).
- Modern critique — don't push the limit on microelectrodes: [Cogan et al. 2016, "Tissue damage thresholds during therapeutic electrical stimulation" (PMC5386002)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5386002/) · [Vatsyayan et al., universal electrochemical safety limits (PMC8216108)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8216108/) · [Niederhoffer et al. 2024, charge-balanced trains in unbuffered saline (JNE)](https://iopscience.iop.org/article/10.1088/1741-2552/ad3b6a) — unbuffered media (our oat/agar gel is exactly this) shift electrode potentials further, i.e. **less margin** than in buffered culture.

**Parameter envelope from the literature:** symmetric ± phases, phase duration 50–500 µs, interphase delay 50–100 µs, 10–1000 Hz pulse trains, balance mismatch ≤ 1–5 %, residual DC leak target **< 100 nA per electrode** (implant-grade stimulators spec this).

**AC option:** sinusoidal ≥ ~1 kHz gives symmetric, tiny Faradaic transfer per half-cycle; a **series coupling capacitor** structurally guarantees zero long-term DC bias (the capacitor charges to any electrode offset and then blocks it). This is the same regime impedance-sensing electronics live in — safe for continuous operation.

**Caveat for steering:** true galvanotropism (§3) responds to *DC/low-frequency vector* fields — charge balancing and steering are in direct tension. Resolution: steering is a short-exposure mode (minutes–hours at ≤ a few V/cm, noble electrodes only); **lifetime lattice traces operate near-zero-net-DC** (AC or balanced pulses), with any DC steering windows explicitly duty-limited and logged.

---

## 3. Field thresholds — galvanotropism vs damage

**The steering regime (classic literature):** applied DC fields polarize hyphal growth — germ tubes and hyphae reorient, usually toward the **cathode**, with species/branch exceptions (e.g. *Trichoderma harzianum* hyphae and branches orient oppositely).

- **McGillivray & Gow 1986**, *J Gen Microbiol* 132:2515 — ["Applied electrical fields polarize the growth of mycelial fungi"](https://www.semanticscholar.org/paper/Applied-Electrical-Fields-Polarize-the-Growth-of-Mcgillivray-Gow/30a784b13ffe93df9c44bf69f9560a8f10084ea5) · [journal page](https://www.microbiologyresearch.org/content/journal/micro/10.1099/00221287-132-9-2515) — *Neurospora*, *Aspergillus*, *Mucor*, *Trichoderma*: germination site, branching, extension direction all polarized. Secondary summaries place the classic experiments at **~2–20 V/cm DC, exposures of minutes to hours** (primary abstract does not state numbers).
- **Brand et al. 2007**, *Curr Biol* 17:347 — [Hyphal orientation of *Candida albicans*](https://www.sciencedirect.com/science/article/pii/S0960982207008275) · [author PDF](https://www.abdn.ac.uk/staffpages/uploads/gen053/PDFs/2007-Curr-Biol-Brand-tropism.pdf): **10 V/cm** → strong cathodal orientation; mechanism is **Ca²⁺ influx at the tip** (stretch-activated Cch1/Mid1 channels); germlings stay viable and grow. Follow-up: [Brand et al. 2008, Eukaryotic Cell (PMC2292634)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2292634/) — polarity reversal → tips re-orient (fields are a live, reversible steering input). Review: [Brand & Gow 2009, "Mechanisms of hypha orientation of fungi" (PMC2728830)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2728830/) — confirms no growth-rate/viability penalty reported at these steering doses, but those are **short, buffered, electrode-separated exposures**, not lifetime immersion.
- **Modern weak-field end:** [Moratto et al. 2023, *Phys Biol*](https://iopscience.iop.org/article/10.1088/1478-3975/ace751) · [PubMed 37442125](https://pubmed.ncbi.nlm.nih.gov/37442125/): **0.7–1.0 V/cm** already accumulates *Phytophthora palmivora* zoospores, **increases germination rate**, orients germ tubes — fields "of the same magnitude as plant roots" ([2024 follow-up, *Sci Rep*](https://www.nature.com/articles/s41598-024-68730-y) diverts infection). Take: **sub-1 V/cm is behaviorally potent** — you do not need galvanotropism-grade fields to matter.
- Cellular scale: [Crombie et al. 1990, PubMed 2182770](https://pubmed.ncbi.nlm.nih.gov/2182770/) — bud-site polarization tracks the **induced membrane voltage (~12 mV per cell)**, i.e. cells sense local V, not V/cm as such.
- Context reviews: [Gow & Morris 1995, "The electric fungus"](https://www.tandfonline.com/doi/pdf/10.1080/03746609508684833) · [2025 review, "Electrical signals in fungi" (PMC11995700)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/) — hyphae run their own **endogenous tip currents at ~µA/cm² scale** (~0.05–1 µA/cm² in classic Gow-school measurements; fetch failed, treat exact value as approximate); pH- and Ca²⁺-dependence confirmed; beware Donnan potentials in agar as artifacts.
- **What damages:** the galvanotropism literature never reports a clean lethality field because exposures are short and cells are shielded from electrodes (buffered media, separated chambers — an explicit design practice worth copying). The damage data live in the *antifungal* literature: see §4. Physics also bounds it: in a wet block (σ ≈ 0.1–3 S/m), Joule heating = σE² → **1 V/cm ≈ 10–30 mW/L**, **10 V/cm ≈ 1–3 W/L** (cooking in a sealed, uncooled block).

## 4. Species tolerance — chronic exposure on mycelial growth

- **Pulsed high-voltage (lightning analog) helps fruiting, not mycelium:** [Hasan et al., *Microorganisms* 2016 (PMC5029503)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5029503/) — compact pulsed-power stimulation of cultivated mushrooms.
- **Brief shock post-colonization speeds growth:** electrical-shock + high-light treatment bags grew mycelium at **~0.94–0.96 cm/day vs 0.62 control** ([researcherslinks study](https://researcherslinks.com/current-issues/Physical-Stimulations-Electrical-Shock-High-Light/14/34/10078/html)) — again episodic, not chronic field.
- **The fungicidal dose — the key red-line number:** [Cell Reports Physical Science 2025 review, "Electrical stimulation as an emerging antifungal therapeutic strategy"](https://www.cell.com/cell-reports-physical-science/fulltext/S2666-3864(25)00581-8): **500 µA DC × 12 h** or **200 µA DC × 36 h** significantly reduces planktonic *Candida* and biofilm; corroborated by [PMC11200915](https://pmc.ncbi.nlm.nih.gov/articles/PMC11200915/) (DC killing, synergy with fluconazole/amphotericin B) and [ACS AMI 2019](https://pubs.acs.org/doi/10.1021/acsami.9b09977) (**99.7 %** planktonic kill, drug-tolerant biofilms eradicated). Mechanisms: membrane permeabilization/disruption **plus electrode electrochemistry** (ROS, pH, metal species). **Sub-milliamp DC over half a day is lethal to fungi — that is the whole verdict in one number.**
- **AC is dose-bimodal:** weak AC microcurrent can stimulate or inhibit microbes depending on dose ([J Microbiol Infect](https://e-jmi.org/archive/detail/13?is_paper=y)); classic DC-AC distinction: AC avoids electrode polarization byproducts.
- **De facto envelope of the mycelium-electronics community:** every long-term living-block practice runs small signals, never drive current — [Adamatzky, "Fungal electronics" (UWE)](https://uwe-repository.worktribe.com/OutputFile/9567166) · [moisture sensing in mycelium composites (PMC10069029)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10069029/) · [signal transfer in mycelium-bound composites (CSIC PDF, LCR/impedance)](https://digital.csic.es/bitstream/10261/394452/1/1-s2.0-S1754504824000291-main.pdf) · [Cornell biohybrid robots, *Science Robotics* 2024](https://www.science.org/doi/10.1126/scirobotics.adk8019) · [Mycoelectronics, bioprinted living fungal bioelectronics (bioRxiv → PNAS)](https://www.biorxiv.org/content/10.1101/2025.10.06.680560v3.full) · [ETH "Fungal Circuitry"](https://www.research-collection.ethz.ch/bitstreams/05ff7cdd-b842-416b-8480-885018417087/download). Mycelium is effectively an insulator whose impedance swings with moisture — sensing signals are mV–µV; **nobody runs continuous mA through a living block because it dies.**

## 5. VERDICT — safe operating envelope & red lines

**The line between stimulating and cooking is not volts — it is *net charge passed*.** A 3–5 V DC trace across a block is a slow chemical reactor (§1); the same 3–5 V delivered as symmetric kHz AC or charge-balanced µs-pulses is nearly inert. Sub-milliamp DC kills fungi within hours-to-days (§4); sub-1 V/cm AC/pulsed fields measurably interact with growth without published harm (§3).

### Safe operating envelope (LIFETIME lattice traces in a living block)

| Parameter | Envelope | Basis |
|---|---|---|
| **Waveform** | Bipolar AC sine ≥ ~1 kHz **or** symmetric biphasic pulses (50–500 µs/phase, 50–100 µs interphase gap, 10–1000 Hz); **series coupling capacitor on every driven trace**; balance mismatch ≤ 1 % | charge-balanced practice (§2, Shannon/Cogan); cap structurally enforces zero DC |
| **Residual DC** | **< 100 nA per electrode** (audit with a DMM on mV across a sense resistor, monthly) | implant-grade stimulator spec (§2) |
| **Electrode potential** | Stay inside the water window: **≤ ±0.8–1.2 V vs medium** → ≤ ~2 V pk-pk between adjacent driven electrodes | Pt water window; Shannon k ≈ 1.5–1.85 (§2) |
| **Charge per phase** | **≤ 10–30 µC/cm²** (carbon) — 5–10× margin under Pt capacity 50–150 µC/cm², extra margin for unbuffered oat/agar medium | Shannon/Cogan, unbuffered-saline caveat (§2) |
| **Field in medium** | Lifetime continuous: **≤ 0.1–0.3 V/cm**. Optional steering mode: 1–5 V/cm, minutes–hours max, logged, then rest ≥ exposure | 0.7–1 V/cm already behaviorally active (Moratto); 2–20 V/cm classic steering is short-exposure only (§3) |
| **Drive current** | ≤ ~10 µA per electrode continuous, duty ≤ 10 % at the top of that; sensing electrodes: mV–µV signals, ≥ 10 MΩ input impedance, nA-class bias | 100–500× under fungicidal DC doses; community practice (§4) |
| **Joule heat** | Dissipation ≤ ~1 mW per cm³ of block; target ΔT < 1–2 °C (P = σE², σ ≈ 0.1–3 S/m wet) | §1/§3 heating arithmetic |
| **Electrodes** | **Graphite/carbon or Pt** for anything that injects charge; Ag/AgCl only for high-Z sensing/reference; encapsulate driven metal so only inert surface faces the medium | Cu²⁺ antifungal (§1); community practice (§4) |
| **Steering exception** | If galvanotropism is wanted (see K2): brief DC windows ≤ 5 V/cm ≤ hours, noble electrodes, separated/flushed electrode zones, then balanced-rest — and expect electrolysis budget spent per §1 Faraday table | §3 + §1 |

### RED LINES (must not cross in a living block)

1. **Any sustained DC above ~100 nA residual.** Published fungicidal dose is 200–500 µA DC × 12–36 h; lower DC still runs §1 chemistry (pH fronts, Cl₂/hypochlorite, metal plating). DC = cooking, full stop.
2. **Electrode potentials beyond the water window (~±1 V vs medium)** → water splitting, chlorine chemistry in chloride media, gas delamination, pH 2 / pH 12 zones.
3. **Copper or bare stainless as charge-injecting electrodes** — Cu anode dissolves ~28 mg per mA·day straight into the mycelium (antifungal at ~1–10 ppm dissolved).
4. **Continuous fields ≥ 1 V/cm in a sealed, uncooled block** (≈ 10–30 mW/L wet, rises with moisture) and anything ≥ ~10 V/cm continuous (≥ W/L — thermal death).
5. **Charge-unbalanced pulses, or a drift/failure that silently makes them DC** — the balance budget needs a standing audit, not a one-time design claim.
6. **Low-frequency high-amplitude drive (e.g. 50 Hz at volts)** — behaves near-DC per half cycle; worst case for Faradaic transfer.

### Cross-refs
- K2_GALVANOTROPISM.md (sister lane: steering-side physics; its "3–10 V/cm" operating idea must adopt this receipt's short-exposure duty limits)
- K12_CONDUCTED_BLOCK.md (lists K7 as NOT LANDED at 18:45 — now landed; its Cu/Ag lattice spec must route lifetime drive through the envelope above, Cu sensing-only or carboned)
- K9_PRIOR_ART.md (community practice evidence, §4)

### Method note
WebSearch/WebFetch only; no git; no paid APIs. Several primary fetches were blocked (403: microbiologyresearch.org, colab.ws, europepmc; timeouts: eutils, PMC2292634, PMC2728830 retry OK on second fetch). Numbers taken from primary sources where fetched (Brand & Gow 2009 review via PMC; Moratto via search summary of PubMed/IOP; antifungal doses via Cell Rep Phys Sci search snippet + PMC11200915); classic 2–20 V/cm range is from secondary summaries — flagged, consistent with Brand 2007's confirmed 10 V/cm. Endogenous tip-current magnitude is approximate (review fetch failed).
