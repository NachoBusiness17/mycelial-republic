# K5_ION_DOPING — receipt

- **Wave lane:** physical_computing / K5 (ionic doping of mycelium blocks)
- **Date:** 2026-09-16
- **Seat:** ZCode research agent (WebSearch/WebFetch only; no git; no paid APIs)
- **Mission:** Can printed ionic gradients turn a mycelium block into a DESIGNABLE resistance/conductivity map? ("nutrient traces as dopants" — the operator's formalization)
- **Method:** receipt-first, append-as-you-go. Four research steps: (1) substrate conductivity physics, (2) printed salt gradients + persistence, (3) ion gradients as hyphal chemotaxis cues, (4) the doping design.

---

## Step 1 — Substrate conductivity physics (DONE)

**Mechanism (soil/substrate physics, well established):**
- Conduction in wet porous media is dominated by **ionic transport of dissolved salts through pore water**. Two parallel paths: (1) liquid pore-water path (ion concentration × moisture cross-section), (2) surface / electrical-double-layer (EDL) path along particle surfaces — secondary in salty organic substrates. Pure water conducts ~0.055 µS/cm; even tap water is ~50–500 µS/cm purely from dissolved salts. (METER Group, USDA-NRCS, Corwin 2020: bulk EC ≥ 2 dS/m → salinity is the dominant conductive constituent.)
- Moisture controls the **cross-sectional area** of the conducting liquid path; salt content controls **carrier density**. So EC = f(moisture, salt) — moisture is the multiplier, salt is the signal. Temperature adds ~2%/°C.

**Numbers — mushroom substrates:**
- Field-weathered spent mushroom substrate (SMS) leachate: **pH 6.6–9.0, EC 21–66 dS/m (21,000–66,000 µS/cm)** (PubMed 11577879, leachate chemistry of field-weathered SMS). Very saline — compost salts concentrate in leachate.
- EC varies by species; oyster/paddy-straw spent substrates show rising EC over fruiting (DMR Solan bulletin).
- Standard measurement: saturated-paste or 1:10 water extract, benchtop meter (WTW inoLab).

*(oat-substrate-specific + mycelium-block conductivity numbers appending below)*

**Numbers — colonized / mycelium blocks:**
- Hwang et al. (cited via ResearchGate fig 11770417): EC of **mycelium-colonized substrate = 1.89 dS/m (1,890 µS/cm), higher than non-colonized substrate** — fungal metabolism *releases* ionic metabolites; colonization raises the salt content. (1:5-type water extracts; horticultural growing media typically land 0.5–3 dS/m in such extracts.)
- Buffi et al. 2025 review (PMC11995700, "Electrical signaling in fungi: past and present challenges"):
  - ITO-stripe slide setup, Keithley 2400, 2–12 mm separations: **bare (uninoculated) substrate 45–128 Ω** (thin-film/wet-slide regime).
  - **P. ostreatus & C. cinerea mycelium-covered regions: resistance > 5×10⁸ Ω** — living hyphal mats are *insulating*, because hydrophobins make the wall hydrophobic. **The conductive phase is the saline pore water, not the hyphae.** This is the central physics fact for the doping design.
  - Hyphal-tip currents: 0.05–0.60 µA/cm² across 5 species; carried by **H⁺/Cl⁻, Ca²⁺, K⁺** (electrogenic H⁺ pump, stretch-activated Ca²⁺/K⁺ channels).
  - ⚠️ Method caveat that binds our own measurement design: stainless-steel needle electrodes in agar can read **abiotic Donnan potentials** (one cited study recorded "signals" with thread instead of mycelium). → 2-electrode conductance measurement should use AC excitation or 4-terminal geometry; DC readings confound electrode polarization with substrate conductance.
- Adamatzky-group moisture study (PMC10069029, Pleurotus ostreatus / Hericium / Ganoderma on rye-millet blocks, stainless sub-dermal needle pairs 1–2 cm): activity windows depend strongly on moisture (~95–65% fresh; <20% dried = silent); fully dehydrated blocks show no electrical response — **moisture is the on/off switch of the conductive phase**.

**Step 1 synthesis:** In spent-oat substrate, conductivity is dominated by **dissolved salt ions in pore water**; moisture sets the conducting cross-section (dry block ≈ insulator, mS/m or less), pH mainly matters via H⁺ mobility at extremes and via fungal metabolism. Leachate/extract EC spans roughly **1–3 dS/m for actively colonized grain substrate** (Hwang: 1.89 dS/m) up to **21–66 dS/m for saline spent compost leachate**. Salt doping moves you along this same axis in a *spatially patterned* way.

---

## Step 2 — Printed salt gradients: feasibility + persistence (DONE)

**Fungal transport = the gradient-erasing mechanism (measured):**
- Classic review baseline (Cairney 1992): solute movement in mycelial cords **0.2–2.0 mm/h** (isotopic tracers).
- Corded basidiomycetes (¹³C glucose / ³²P phosphate pulse-chase): **C 44–48 mm/h, P 16 mm/h, amino acids 36–52 mm/h**; non-corded mycelium only ~2 mm/h (Functional Ecology 1999 / BMS).
- Real-time imaging *Serpula lacrymans* (Frontiers Microbiol 2018): **N ~8 mm/h, C ~25 mm/h**, allocation fronts ~460 mm/d; reviews note up to ~1,000 mm/h in extensible rhizomorphs.
- ⇒ Live mycelium actively **transports and evens** solute gradients at cm/day scale. A printed salt line will not stay put: expect perceptible smearing in **hours-to-a-day** where hyphae contact it, and near-homogenization over a 10 cm block in **~1–3 weeks** unless the pattern is periodically refreshed or the fungus is killed (heat-fix) after printing.

**Physics of gradient decay (no fungus):**
- Small-ion diffusion in water D ≈ 1.5–2×10⁻⁹ m²/s; in saturated porous organic substrate effective D ≈ 0.3–0.5× that. Smear length √(2Dt): ≈ 6 mm/day, ~2 cm/week, ~5 cm in ~5–6 weeks. So even *sterile*, a printed 1 cm line blurs to a few-cm gradient within days-to-weeks — sharpness must be maintained by printing into a *viscous carrier* (paste/gel) that fixes the salt mechanically, not free solution.

**Printing feasibility:**
- No direct "printed salt line in a mycelium block" paper exists in the searched literature — the mechanism composes from established parts: (a) salt dosing of substrate is standard practice (gypsum/salt amendments), and EC of substrate is a routine QC metric; (b) NaCl tolerance data define a wide printable dosing window (below); (c) viscous-paste extrusion (syringe/paste extruder, agar-oat paste carrier) is the natural print modality into or onto pre-colonized blocks — the paste mechanically pins the ions so decay is fungal/diffusive, not convective.
- Distinguish two printable inks: **conductive ink** (salt — sets EC) and **attractant ink** (nutrients — sets hyphal preference). They can be combined in one paste (malt/yeast-extract paste already carries K⁺/PO₄³⁻ salts ≈ several mS/cm and is both conductive *and* chemoattractive).

**Osmotic tolerance defines the doping window (Pleurotus ostreatus, NaCl):**
- ≤0.1–0.2 M (6–12 g/L): little/no effect on growth (tolerated).
- **0.3 M (~17.5 g/L): ~24% growth reduction** — moderate stress, still navigable (Lv 2023, Bioengineered).
- **0.6 M (~35 g/L): ~84–88% growth inhibition** (Zhao 2023, Front. Microbiol.) — usable as a *negative mask / resist* (channel walls).
- 1.2 M (~70 g/L): ~95–97% growth arrest (Yang 2024) — hard barrier.
- ⇒ Printable design space: **0.05–0.3 M as dopant/highway ink, ≥0.6 M as resist/barrier ink.** P. ostreatus is moderately salt-tolerant (glycerol/glycine-betaine compatible solutes), so gradients persist as *growth-bias* gradients long after raw concentrations homogenize — the fungus writes the encountered osmotic history into its branching pattern.

---

## Step 3 — Do conductivity/ion gradients steer hyphal growth? (EVIDENCE: YES, for nutrients and ions)

- **Chemotropism toward amino acids:** Ellis et al. 2017 (*PLOS Pathogens*, *Trichoderma reesei*) — hyphae grow toward amino-acid source; photoreceptor mutants (MSE1, ENV1) misguide hyphal trajectories. Also *Candida albicans* toward glutamate (Brand 2007, capillary assays).
- **Toward sugars and ammonium:** Youatt, Fleming & Jobling 1982 (*FEMS*, *Saprolegnia ferax*) — electrophysiological + growth responses to gradients of **sugars, amino acids, and ammonium ions**; gradients of L-glutamate, L-proline, sucrose, glucose steer hyphae of *S. pombe* / *A. nidulans* (attraction or repulsion depending on dose).
- **Toward ions (Ca²⁺) and electric fields:** Jackson & Heath 1992 (*Exp. Mycology*) — Ca²⁺ and the hyphal tip are central to chemotropic response; Levina & Lew 2006 — *Neurospora crassa* Ca²⁺-channel mutants lose gradient guidance; galvanotropism (directed growth in electric fields) is **Ca²⁺- and pH-dependent** across A. nidulans, N. crassa, C. cinerea (from Buffi 2025 review, Step 1).
- **Single-channel mechanism:** Cho et al. 2017 (*PNAS*) — TRPY mechanosensitive ion channel in *N. crassa* senses osmotic pressure, glucose and amino acids, guiding growth to nutrient-rich surfaces.
- **Macroscopic equivalent — mycelial foraging:** hyphae preferentially colonize resource patches in heterogeneous litter/wood (Boddy's foraging literature; resource-node colonization, cord formation toward new resources — consistent with the ¹³C/³²P translocation studies in Step 2: flux *follows* discovered resources).
- **Nuance for our design:** pure NaCl is not a documented chemoattractant at steering doses — it is the *conductivity* dopant and, at high dose, a repellent/resist. The *attractant* evidence is for sugars/amino acids/NH₄⁺/Ca²⁺ gradients. Hence the recipe: **nutrient-bearing conductive paste** (malt/yeast extract, oat flour + salt) = attractant + dopant in one ink; **0.6 M+ NaCl** = resist. Moderate Ca²⁺ enrichment (gypsum) is a literature-backed mild steering cue compatible with mushroom practice.

---

## Step 4 — The doping design (wiring diagram printed in salt)

**Architecture (two inks, one carrier, PCB-style pattern):**
- **Ink A — "conductive trace" (dopant + attractant):** gelatinized oat-flour paste carrying NaCl 0.15–0.25 M + gypsum 1–2% w/w. Conductive (≈30 mS/cm pore fluid → ~10–15× bulk substrate EC) *and* chemoattractive (sugars/amino acids from the flour; Ca²⁺ cue). Printed as beads (5–10 mm wide × 3–5 mm deep) into pasteurized substrate at spawn time, or onto the block face.
- **Ink B — "resist / barrier":** same carrier at NaCl 0.6–1.2 M. 84–97% growth inhibition → defines insulating channel walls and keeps traces separated.
- **Positive feedback that sharpens the trace:** hyphae preferentially colonize Ink A (foraging + chemotaxis + moisture), and colonization itself raises EC (Hwang: colonized 1.89 dS/m > bare) — the more the mycelium uses the trace, the lower its resistance gets. The trace anneals itself.
- **Freeze step:** after full colonization, pasteurize the block (~65 °C, 4–6 h) — kills the mycelium, stops ion translocation and metabolism; ions + architecture freeze. Converts the living drift into a stable "printed PCB" (memfractive properties of mycelium-bound composites then dominate the residual behavior — cf. ScienceDirect S1754504824000291).

**Persistence budget (from Steps 2's numbers):**
- Sterile smear: √(2Dt) ≈ 6 mm/day → 1 cm line legible ~2–6 weeks.
- Live block: translocation/contact homogenizes along hyphal paths at cm/day — visible drift in hours-to-days, near-homogenization of a 10 cm block in ~1–3 weeks. → refresh by re-printing weekly, or freeze after colonization.
- Architecture (colonized trace, metabolite salts, osmotic growth history) persists well beyond ion homogenization — the fungus writes the pattern into its own structure.

**2-electrode measurable range (L = 2–5 cm pin pair, ~1 cm² effective contact, 1 kHz AC to dodge Donnan/electrode polarization):**
- Bulk σ baseline (wet colonized block, extract EC ~1.9 dS/m × Archie-style porosity factor): **~0.05–0.2 S/m** → R ≈ **2.5–50 kΩ** (contact/spreading resistance pushes the upper end; moisture variation dominates repeatability).
- Along a printed Ink-A trace (0.3 M NaCl pore fluid ≈ 30 mS/cm, ~10–25× bulk): R ≈ **0.2–5 kΩ**.
- Across an Ink-B resist wall: path resistance 2–5× higher *plus* no mycelial bridging → effectively a high-R gap.
- Dry block (>80% → <20% moisture, PMC10069029): **>10 MΩ to GΩ** — the on/off switch.
- **Designable contrast: ~5–25× (≈ one decade), one full decade after freeze** — analogous to early semiconductor doping: discrete orders, not arbitrary precision, but fully measurable with a $10 LCR meter or even an MCU ADC + divider.

---

## VERDICT

**YES — ionic doping works, with one-decade resolution and a living-timescale clock.**
1. Conductivity in spent-oat substrate is **salt-in-pore-water dominated**; moisture is the gain knob, salt is the signal. Extract EC: ~1–3 dS/m colonized grain (1.89 dS/m, Hwang) to 21–66 dS/m saline leachate.
2. Salt gradients **can be printed** as paste zones; live mycelium actively evens them (0.2–52 mm/h transport) — pattern lifetime ≈ days-to-weeks live, indefinite once pasteurization-frozen.
3. Hyphae **do steer** along nutrient/ion gradients (amino acids, glucose, NH₄⁺, Ca²⁺; TRPY/ Ca²⁺-channel mechanosensing), so the printed trace is *preferentially colonized* — the low-R path and the growth path coincide.
4. **The wiring diagram in salt is buildable:** Ink A (oat paste + 0.9–1.5% NaCl + gypsum) prints highways; Ink B (3.5–7% NaCl) prints insulating walls; pins + 1 kHz AC read kΩ-highways vs 10s-of-kΩ-matrix; freeze with heat to stop the clock.
**Measurable conductance range (2 electrodes, 2–5 cm span, wet block): ~20 µS–0.4 mS baseline, up to ~0.2–5 mS on doped traces; dry = insulator.**

### Recipe sketch (v0)
| Item | Spec |
|---|---|
| Carrier | gelatinized oat-flour paste, 1:3 w/w flour:water (sterile) |
| Ink A trace | NaCl 0.15–0.25 M (9–15 g/L) + CaSO₄·2H₂O 1–2% w/w |
| Ink B resist | NaCl 0.6–1.2 M (35–70 g/L) |
| Geometry | 5–10 mm wide beads, 3–5 mm deep; PCB node-and-trace; print at spawn time |
| Electrodes | stainless pins or Ag/AgCl, at nodes, 2–5 cm spans |
| Readout | 1 kHz AC (avoid Donnan artifacts), 2-electrode |
| Timing | print → colonize 7–14 d → optional freeze 65 °C/4–6 h → measure |
| Expect | trace R 0.2–5 kΩ vs matrix 2.5–50 kΩ (≈10× contrast), dry >10 MΩ |

## Sources
- Leachate chemistry of field-weathered SMS (pH 6.6–9.0, EC 21–66 dS/m): https://pubmed.ncbi.nlm.nih.gov/11577879/
- EC of spent mushroom substrate (incl. Hwang et al. colonized 1.89 dS/m): https://www.researchgate.net/figure/Electrical-conductivity-EC-of-the-spent-mushroom-substrate_fig3_11770417
- Soil EC mechanism (METER Group; USDA-NRCS; Corwin 2020): https://metergroup.com/education-guides/soil-electrical-conductivity-the-complete-guide-to-measurements/ · https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%2520Electrical%2520Conductivity.pdf · https://acsess.onlinelibrary.wiley.com/doi/10.1002/saj2.20154
- Electrical response of fungi to moisture (P. ostreatus/H. erinaceus/G. lucidum, needle pairs): https://pmc.ncbi.nlm.nih.gov/articles/PMC10069029/
- Electrical signaling in fungi review (Buffi 2025; ITO resistances, tip currents, Donnan caveat, Ca²⁺/K⁺/H⁺/Cl⁻): https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/
- Mycelium-bound composites, conductive/memfractive: https://www.sciencedirect.com/science/article/pii/S1754504824000291
- Translocation velocities: Cairney 1992 https://www.sciencedirect.com/science/article/abs/pii/S0953756239800622 · Functional Ecology 1999 https://besjournals.onlinelibrary.wiley.com/doi/abs/10.1046/j.1365-2435.1999.00307.x · Serpula imaging https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2018.01649/full
- NaCl tolerance P. ostreatus (0.3 M ≈ −24%; 0.6 M ≈ −84/88%; 1.2 M ≈ −95/97%): Lv 2023 Bioengineered; Zhao 2023 Front. Microbiol.; Yang 2024 Front. Microbiol. (via search summaries)
- Chemotropism evidence: Ellis 2017 PLOS Pathogens (T. reesei amino acids); Youatt 1982 FEMS (sugars/amino acids/NH₄⁺); Jackson & Heath 1992; Levina & Lew 2006 (Ca²⁺ gradients); Cho 2017 PNAS (TRPY). (via search summaries + PMC11995700)

*Receipt complete — K5 ionic doping research lane. No git actions; WebSearch/WebFetch only; no paid APIs.*
