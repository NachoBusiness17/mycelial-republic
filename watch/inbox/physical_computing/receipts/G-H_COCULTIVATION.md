# G-H COCULTIVATION — research receipt (wave lane)

- **Gap:** G-H — multispecies lattice assumes two species can share a printed block with a stable zone line. Verify the ecology.
- **Method:** WebSearch/WebFetch only (free). Receipt-first; appended as gathered. No git. No paid APIs.
- **Date:** 2026-09-16
- **Questions:** (1) paired-species co-cultivation outcomes + timescales; (2) what pins the zone line; (3) multi-species contamination risk + mitigation.
- **Status:** FILED 2026-09-16 — complete. Answers + verdict at bottom (receipt ends with pairing recommendation, zone-pinning method, contamination delta).

## Findings (appended as gathered)

### Batch 1 — the combat framework (mycology journals)

Note: WebSearch rate-limited (429) throughout; worked around via PubMed E-utilities + Europe PMC REST (both free, no key).

1. **Boddy L (2000), "Interspecific combative interactions between wood-decaying basidiomycetes", *FEMS Microbiology Ecology* 31(3):185–194** (PMID 10719199)
   - The canonical framework: outcomes are **deadlock** (neither captures territory) or **replacement** (one displaces the other), with a spectrum between (partial/mutual replacement per 2018 review).
   - Outcomes follow a **combative-ability hierarchy** that is complicated by **intransitivity** (A beats B, B beats C, C beats A) and **modified by abiotic variables** (water potential, pH, gas regime).
   - Mechanisms: antagonism at a distance (volatile/diffusible metabolites), hyphal interference, mycoparasitism, gross mycelial contact.
   - Implication for the lattice: the zone line is NOT a designed interface; it is the visible record of a fight whose winner depends on species pair AND substrate conditions.

2. **Hiscox J, O'Leary J, Boddy L (2018), "Fungus wars: basidiomycete battles in wood decay", *Studies in Mycology* 89:117–124** (PMID 29910518)
   - Confirms deadlock/replacement/intermediates; notes research is moving from 2D plate assays to **3D spatial orientation** — exactly the lattice's regime, and the review says 3D outcomes are not fully predictable from 2D ones.
   - Key caveat for cube 2: a printed 3D block is a regime where the literature itself says extrapolation is weak.

3. **Wald P, Pitkänen S, Boddy L (2004), "Interspecific interactions between the rare tooth fungi Creolophus cirrhatus, Hericium erinaceus, H. coralloides and other wood decay species in agar and wood", *Mycological Research* 108(12):1447–1457** (PMID 15757181)
   - Directly relevant methodology: 20+ species pairings, in agar AND in wood.
   - **Timescale datum: wood pairings incubated 36–38 weeks** — zone boundaries in wood are a many-weeks-to-months phenomenon, not days.
   - **Abiotic conditions (water potential, pH, CO2/O2) altered outcomes** — supports substrate-level control of who wins.
   - "Outcomes in wood were representative of those in agar" — plate pre-screens have some predictive value.

### Batch 2 — zone lines as an inducible, condition-gated structure (spalting literature)

4. **Tudor D, Robinson SC, Cooper PA (2012), "The influence of moisture content variation on fungal pigment formation in spalted wood", *AMB Express* 2:69** (DOI 10.1186/2191-0855-2-69)
   - Wood science's zone lines (pseudosclerotic plates, dark demarcation lines in spalted wood) form under controlled moisture; pigment and zone-line production is **gated by substrate moisture content** — too dry = no activity, too wet = bacterial washout.
   - Found via Europe PMC; spalting lit lives in wood-science journals, not PubMed proper.
   - **Concrete numbers:** species-specific moisture windows — *Inonotus hispidus* >22–28% MC (beech); *Fomes fomentarius* max 26–41% MC; *Scytalidium cuboideum* >35% MC; *Polyporus brumalis* 59–96% MC. Conclusion of the authors: **controlling substrate moisture steers which fungus does what, where** — the strongest published analog of "pinning" a printed structure.

### Batch 3 — timescales of the standoff, and what a zone line IS

5. **Barrage-zone timing (paired basidiomycete cultures):**
   - Mycological Progress (2015) study of 80 basidiomycete isolates (disturbed pine forests): incompatibility reactions visible **4–13 days after contact, most barrage lines ~day 6** (agar).
   - *Schizophyllum commune* (Frontiers in Microbiology, 2021): fruiting-inducing barrage at the confrontation zone **7–8 days after pairing**.
   - Contrast with wood blocks (Wald 2004): weeks–months. **Plate standoff appears in days; block standoff takes weeks; and plate timing does not predict block timing.**

6. **What the zone line is, structurally:**
   - "Delimited barrage zone (DBZ)" (Chase & Uscuplic 1986, via Boddy & Rayner's *Heterobasidion* work; Frontiers 2013 review): a delimited zone between paired isolates where (1) secondary metabolites accumulate, (2) one isolate's mycelium excludes the other's, (3) growth beyond is suppressed.
   - Morphology (Studies in Mycology 79:95; Life 9:23; Springer 10.1007/s10201-015-0462-1): the dark line = **melanin deposition**, aggregated brown hyphae with swollen thick-walled cells; related forms: compression zones, inhibition zones ("clean zone free of hyphae").
   - Mechanisms (Rayner & Todd 1977 lineage): hyphal interference (rapid localized growth arrest on contact), diffusible inhibitors (e.g., 3-phenylpropanol), territorial strategy.
   - Note for the electrode hypothesis: the zone line is a chemically active, melanin-rich, metabolite-charged boundary — plausible electrophysiology target, and the metabolites are exactly what Boddy 2000 says "antagonism at a distance" is made of.

### Batch 4 — pairing outcomes on the same substrate (oyster vs shiitake vs reishi vs enoki)

7. **Practical cultivation consensus (Shroomery / FB grow groups / Reddit, via WebSearch):**
   - **Oyster (Pleurotus ostreatus) reliably overruns shiitake** in shared bags/blocks: shiitake is a slow, methodical colonizer; oyster is famously fast ("Shiitake take much longer to colonize" — FB Oyster Mushroom Cultivation group). Counter-nuance from Shroomery: shiitake's metabolite excretions resist competitors well **once established** — first-colonizer-wins dynamics.
   - Community standard advice: **keep species in separate blocks**; mixed spawn in one bag = "the conflict of two strains in one bag," unpredictable dominance, one species wins rather than co-fruits.
   - **Sequential** cultivation (oyster then shiitake on willow; Biomass Conversion and Biorefinery 2025) improves outcomes vs simultaneous mixing — timing-staggered co-culture works better than side-by-side from day 0. Directly relevant to an inoculation-order control knob.
   - Reishi contamination datum: green mold (*Trichoderma longibrachiatum*) is a recognized disease of cultivated *Ganoderma lingzhi* with a dedicated rapid-detection paper (Life, 2026) — i.e., Ganoderma blocks are known Trichoderma targets.

### Batch 5 — what sets the zone-line POSITION, and the Adamatzky grounding

8. **Position of the confrontation line = relative colonization speed × inoculation timing.**
   - Dual-culture methodology (PIRG assays; e.g., Rahman 2009 lineage, Živković 2012, ScienceDirect S1049964418305334, PMC8052857): the meeting/inhibition zone sits where the two fronts collide — biased toward the slower grower's side. No single paper states "you can pin the line" in those words; it is implicit in every dual-culture measurement. **Design consequence: line position is steerable via growth-rate matching and staggered inoculation, not fixed by geometry alone.**
   - Sequential-cultivation result (Biomass Conversion and Biorefinery 2025, oyster/shiitake on willow): staggered inoculation beats simultaneous — timing is a real control knob on shared substrate, not just on plates.

9. **Abiotic steering, with numbers:**
   - Moisture: species-specific activity windows (item 4: 22–96% MC depending on species) — moisture variance moves where each species is active.
   - Water potential and pH: Wald 2004 (pH 4, −1.25 MPa treatments flipped some pairings' outcomes); Boddy 2000 lists pH/gas/water potential as outcome modifiers.
   - **pH trace: no literature found demonstrating pH patterning pins a line's POSITION.** pH modulates who wins; pinning-by-pH is an unproven cube-2 experiment, not a citation-backed method.

10. **Adamatzky grounding (the "species tables" the lattice design defers to):**
   - "Towards fungal computer", *Interface Focus* 2018 (PMC6227805): **single species only** (*P. ostreatus*), chosen for availability; no mixed-species cultures anywhere in the fungal-computing literature found. The multispecies lattice is genuinely novel — and therefore has no precedent to copy, good or bad.
   - The multi-species spiking comparisons live in later papers ("Language of fungi derived from their electrical spiking activity", *Royal Society Open Science* 9:211926, 2022 — ghost *Omphalotus nidiformis*, enoki *Flammulina velutipes*, splitgill *Schizophyllum commune*; other work used pink oyster *P. djamor* and *Ganoderma resinaceum*).
   - Fun precedent for "grown boundaries": Adamatzky cites Shantz & Piemeisel (1916) — interacting wild fairy-ring wavefronts of two species approximating a Voronoi diagram. Wavefront boundaries between species are a real, old observation; instrumenting one at cm-scale in a block is the new part.

### Batch 6 — contamination: multi-species vs single, and mitigation

11. **The contamination model is a race condition** (Mushroom Spawn Store framing; Groenewald et al. 2013, *Applied Microbiology and Biotechnology* review; Cornell Extension / PSU spawn-run protocols):
    - *Trichoderma* (esp. T. harzianum, T. aggressivum on Agaricus; **T. pleuroticola / T. pleurotum specialized on Pleurotus**; T. longibrachiatum on Ganoderma) wins via mycoparasitism + antibiosis + speed. Every prevention measure either reduces spore introduction or accelerates mushroom mycelium to full colonization. **A block is only "safe" once FULLY colonized by the crop fungus.**
    - Standard protocol: sterilize/pasteurize substrate; SAB or laminar hood; vigorous fresh spawn at ≥1–2% wet weight (5–10% sawdust spawn safer); tight pack, no air pockets; filter-patch bags; whole prep→spawn→seal in one day; spawn-run below ~75–80°F (T. harzianum optimum is 30°C); bleach/alcohol dips on spawn containers; quarantine on first green; cut-out salvage only for late-stage single-species blocks.
12. **Multi-species deltas (this is what changes vs cube 1):**
    - **Vulnerable window = the SLOWER species' window.** Oyster side may be done in 1–3 weeks; shiitake needs 3–4+ weeks (weeks more on dense/oats-wood mixes). The whole block stays at risk the entire time.
    - **The zone line is a necromass hotspot:** barrage zones are built of lysed/aggregated hyphae and metabolite-rich melanin (item 6) — a nutrient patch for bacteria and Trichoderma at exactly the interface the design cares about. This attack surface does not exist in single-species cube 1.
    - **Two spawn lots = two exposure events**; two species' temperature optima conflict (cool shiitake run extends the window; hot run favors Trichoderma).
    - Salvage rule changes: cut-out salvage assumes you can sacrifice infected area; in a mixed block, cutting breaches the zone and smears interface material — **first green = retire the whole block, outside the grow space, never open it indoors.**

## Answers to the Socratic questions

**(1) Stable standoff, overrun, or mutual inhibition?** Pair-specific, and NOT the default in either direction. The outcome taxonomy is replacement / deadlock / partial replacement (Boddy 2000; Hiscox 2018), chosen by combat rank, colonization speed, and abiotic conditions. Among the four candidates: **oyster overruns shiitake** in shared blocks (speed mismatch; grower consensus + first-colonizer-wins), enoki is also a fast grower (same fate likely), reishi is slow AND a known Trichoderma target. Deadlock-with-a-line is what similar-rank combatants do (documented barrage zones even between isolates of the same species — Ganoderma pairings are literally used as a genotyping tool). **Timescales:** agar standoff appears 4–13 days after contact (~day 6 typical); wood/substrate standoffs take weeks to months (Wald 2004: 36–38 wk pairings); plate outcomes only weakly predict block outcomes, and 3D geometry is exactly where the literature says extrapolation fails.

**(2) What controls zone-line POSITION?** The line forms where the two colonization fronts first meet: **relative growth rate × inoculation timing** (dual-culture PIRG methodology), modulated by **moisture content** (species-specific windows, spalting data), **water potential/pH/gas regime** (Wald 2004, Boddy 2000), and **nutrient gradients** (space = nutrient capture). A printed groove only delays contact — mycelium bridges empty space; to anchor a line at a groove, the groove must carry a LOW-nutrient charge (inert/unsupplemented) so the fronts stall there. A pH trace is plausible for steering but **no literature shows pH pins position** — treat as experiment. The strongest literature-backed pins, in order: staggered inoculation (sequential > simultaneous, BCB 2025), growth-rate matching, moisture banding.

**(3) Contamination risk multi vs single?** Strictly worse, in three compounding ways: the slower species stretches the at-risk window for the WHOLE block; the zone line itself is a metabolite-rich necromass patch (new attack surface); and there are two spawn exposures plus a temperature-optimum conflict. Mitigation is the same race-condition playbook with additions (see verdict).

## VERDICT

**Recommended cube-2 pairing: *Pleurotus ostreatus* (oyster) vs *Lentinula edodes* (shiitake), with SHIITAKE-SEEDED-FIRST staggered inoculation (7–14 days ahead), not a same-day mix.** Reason: oyster-vs-anything else risks replacement; shiitake's documented metabolite resistance once established + a head start converts oyster's speed advantage into a contained collision instead of a takeover, and sequential-cultivation data show staggering beats simultaneous on shared substrate. Add a printed low-nutrient channel at the planned line. Electrodes go in a BAND spanning ±2–3 cm around the geometric interface — the line WILL jitter; position is steered, not printed. **Fallback hedge (carry this in the design doc): if the interspecies line proves unstable in the pilot, run two oyster strains instead** — same-species barrage zones are the literature's most reliable "stable standoff at a line," still give grown junctions at electrodes, and drop the contamination delta back toward cube 1. Do not pair with reishi (slow + green-mold-documented) or enoki (fast enough to be the next overrun victim, cold fruiting conflicts with oyster).

**Zone-pinning method (literature-backed):** (a) shiitake seed face inoculated 7–14 days before oyster face (timing pin); (b) low-nutrient printed channel at the planned line (stall pin — engineering inference from space=nutrients, flag as such); (c) hold substrate moisture in the low band of the workable range to slow the fast species and keep the line sharp (moisture pin — spalting MC windows 22–96% species-specific); (d) pH trace = optional experiment, modulates who wins, unproven for position.

**Contamination protocol delta vs cube 1:** keep the entire cube-1 sterile baseline (sterilized substrate, SAB/hood, filter-patch shell, 5–10% sawdust spawn rate, one-day workflow, spawn-run ≤75°F); ADD: (1) both spawn lots enter in the SAME sterile session, never re-open a seeded face; (2) colonize-completion checklist per face before fruiting conditions — block isn't safe until the SLOW face finishes; (3) keep the planned line ≥2 cm from the shell/filter boundary so the hotspot isn't at a seam; (4) probe green mold discipline: T. pleuroticola/pleurotum specifically hunt Pleurotus — first green = retire the WHOLE block outside, no cut-out salvage on mixed blocks; (5) log line position + any contaminant onset date per block (the slow-species window is the experiment's true clock).

## Sources

- Boddy L (2000), FEMS Microbiol Ecol 31:185–194 — PMID 10719199
- Hiscox J, O'Leary J, Boddy L (2018), Stud Mycol 89:117–124 — PMID 29910518
- Wald P, Pitkänen S, Boddy L (2004), Mycol Res 108:1447–1457 — PMID 15757181
- Tudor D, Robinson SC, Cooper PA (2012), AMB Express 2:69 — DOI 10.1186/2191-0855-2-69
- Mycological Progress (2015) 80-isolate pairing study (barrage 4–13 d) — via WebSearch
- Frontiers Microbiol (2021) Schizophyllum pairing barrages (7–8 d) — via WebSearch
- Chase & Uscuplic 1986 DBZ definition via Frontiers Microbiol 2013 (10.3389/fmicb.2013.00326); Studies in Mycology 79:95; Life 9:23; Springer 10.1007/s10201-015-0462-1
- Adamatzky A (2018), "Towards fungal computer", Interface Focus — PMC6227805
- "Language of fungi derived from their electrical spiking activity", R Soc Open Sci 9:211926 (2022)
- Sequential oyster/shiitake cultivation on willow, Biomass Conversion and Biorefinery (2025) — via WebSearch
- Groenewald M et al. (2013), Appl Microbiol Biotechnol (Trichoderma review) + Cornell Extension/PSU spawn-run protocols + grower consensus (Shroomery, FB groups, Reddit) — via WebSearch
- Banerjee A et al. (2026), Front Microbiol 10.3389/fmicb.2026.1757755 (contamination review, PMC13111447)
- Green mold of Ganoderma lingzhi rapid detection, Life (2026) — via Europe PMC
- Access notes: WebSearch rate-limited much of the run; PubMed E-utilities, Europe PMC REST and direct PMC fetches used as workarounds; arXiv API and DuckDuckGo/Bing HTML fetches blocked (429/CAPTCHA).
