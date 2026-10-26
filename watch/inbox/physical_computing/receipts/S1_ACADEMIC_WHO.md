# S1 RECEIPT — ACADEMIC WHO: who is actually publishing on mycelium electrical sensing / fungal computing (2023–2026)

- **Date:** 2026-09-16
- **Lane:** wave S1, physical_computing
- **Operator question on file:** "is this real, steal what other people are doing"
- **Mission:** survey the ACADEMIC world 2023–2026 — labs/PIs/groups, latest result + canonical link each, replication/retraction watch, honest map (center of gravity, measured SOTA, poetry). Mark NEW vs HELD (we hold C17: Telhan Sci Rep 2026, LaRocco 2025, FEMS Buffi 2025, Adamatzky star-array 2601.08099, Adamatzky canon, retracted "Fungal sensing skin" 2021, Karst et al. wood-wide-web critique).
- **Method:** WebSearch/WebFetch only (free), no paid APIs, no git. Receipt-first, appended as evidence lands.
- **Budget law:** no paid APIs; free tools only.

## Status: FILED 2026-09-16 — census complete, sections below final (S1 lane)

---

## THE CENSUS — who is actively publishing (2023–2026), latest result + canonical link

| # | Group / PI | Where | Latest result (one line) | Canonical link | NEW/HELD |
|---|---|---|---|---|---|
| 1 | **Unconventional Computing Lab — A. Adamatzky** (UWE Bristol; Mougkogiannis, Jones) | Bristol, UK | Oyster-mycelium spike propagation measured over 15 days on 8 channels: ~0.7 cm/min, 0.2–1.4 mV spikes, n=1 specimen | doi.org/10.1038/s41598-026-47035-2 (PMC13212958) | paper NEW; lab HELD |
| 2 | **Ecovative / Telhan et al.** (Green Island, NY; DARPA AIxBIO since Dec 2024) | industry-academic, US | Grown mycelium + PEDOT:PSS chips do physical RC: MC 0.048–0.209, NARMA-10 NRMSE ≈1.0, non-living at compute time | doi.org/10.1038/s41598-026-55550-5 · code github.com/otelhan/NeuromorphicMyceliumChip | HELD (AIxBIO program name NEW) |
| 3 | **Buffi / Junier group** (Univ. Neuchâtel + iSIS HEIA-FR HES-SO Fribourg + Prototypos + Los Alamos + ETH Zürich) | Switzerland/US | "Fungal potential card" PCB (8× gold differential electrodes, ~17 Hz) records Fusarium oxysporum: +1,604% PSD on colonization, 1.5–8 Hz band, cycloheximide kill-control | doi.org/10.1016/j.isci.2025.113484 (PMC12483595) | **NEW group + NEW protocol** |
| 4 | **LaRocco / Ohio State** | US | Shiitake mycelium memristor: 5.85 kHz switching at 90±1%, dehydration-tolerant | doi.org/10.1371/journal.pone.0328965 | HELD |
| 5 | **ICCMR — E. R. Miranda** (Univ. Plymouth) | UK | Slime molds FAIL quantum-entanglement simulation as bioelectronic components (honest negative from inside the field) | doi.org/10.3389/frsfm.2025.1588404 | **NEW** |
| 6 | **Schmidt / Seyfried / Reutina (Biofaction KG) + Seskir (KIT) + Miranda (Plymouth)** | Austria/Germany/UK | Independent retest of Physarum "bio-memristor": NO memristance; elliptical I-V explained by plain capacitance (RC model) | doi.org/10.1557/s43580-025-01198-8 | **NEW — failed replication** |
| 7 | **Empa, Cellulose & Wood Materials** (St. Gallen, CH) | Switzerland | 3D-printed self-digesting fungal biobattery ~300–600 mV (Reyes 2024) + living S. commune moisture-reactive bioplastics (2025) | empa.ch/web/s604/fungal-biobattery · doi.org/10.1021/acssuschemeng.4c04813-class (ACS SusChemEng 2024, name Reyes et al. — fetch-flagged) | **NEW group** |
| 8 | **Dehshibi (SUNAI, UOC Barcelona) + Adamatzky** | Spain/UK | Spike-complexity analysis of Pleurotus djamor (2021 line; FUNGAR EU project, ended) | doi.org/10.1016/j.biosystems.2021.104373 | HELD-adjacent (pre-2023 base) |
| 9 | **INRAE / Faulon** (France) | France | Bacterial strains as RC reservoirs for regression/classification (bioRxiv 2024 → PhD program + Biotechnol Adv 2025 review) | biorxiv.org/content/10.1101/2024.09.12.612674 | **NEW (adjacent)** |
| 10 | **FinalSpark (Jordan et al.)** (Vevey, CH) | wetware industry | 16 human-brain-organoid "Neuroplatform," remotely accessible wetware computing | doi.org/10.3389/frai.2024.1376042 (PMC11097343) | **NEW (adjacent)** |
| 11 | **Plant-RC line (Pieters et al.; Cambridge homeostatic-coupling work)** | BE/UK | Living plant physiology as physical reservoir; minimal reservoir coupled to a plant for nonlinear control | doi.org/10.1038/s41598-022-16874-0 (base) | HELD-adjacent (theory row in C17) |
| 12 | **MycoSoft "Fungal Computer Interface"** | industry | Marketing-grade "living sensor array" claims, no peer-reviewed artifact found | medium.com/@mycosoft.inc/fungal-computer-interface-fci-c0c444611cc1 | NEW — **poetry tier** |
| 13 | ETH Zürich "Fungal circuitry" (structural sensing) | Switzerland | Thesis: mycelium as living sensor for smart structures (no journal paper surfaced) | research-collection.ethz.ch | NEW — thesis tier |

Census shape: roughly **4 electrophysiology groups** (UWE, Neuchâtel/HES-SO, UWE-adjacent UOC, Plymouth-Physarum), **1 engineering group with money** (Ecovative/DARPA), **1 materials group** (Empa), **1 skeptic-replication cluster** (Biofaction/KIT/Plymouth), plus adjacent wetware (FinalSpark, Cortical Labs) and bacterial/plant RC. That is the whole visible academic field — it is SMALL, which is both the opportunity and the tell.

## REPLICATION / RETRACTION WATCH (2023–2026)

**Retractions — no new ones surfaced this session.** The only retraction on file remains
Adamatzky "Fungal sensing skin" (Fungal Biol Biotechnol 2021, retraction note
10.1186/s40694-021-00114-7) — and it is STILL accruing citations ("cited by 67" live today),
so citation hygiene matters more than ever.

**Disputes / failed replications (NEW since our last receipt):**
1. **Physarum bio-memristor: FAILED independent replication** — Schmidt, Seyfried, Reutina,
   Seskir, Miranda (MRS Advances 2025): no memristive behavior, hysteresis = RC capacitance
   artifact. Contests Gale/Adamatzky 2013 line. Independent authors (no Gale, no Adamatzky).
2. **Physarum quantum-simulation claim: FAILED from inside** — Miranda et al. (Frontiers Soft
   Matter 2025): slime molds cannot reliably simulate entanglement.
3. **Fungal "language": disputed in the literature** — Blatt, M.R., Fungal Ecology 68:101326
   (2024) rebuttal of Adamatzky's RSOS 2022 "50 words"; linguists (UPenn Language Log)
   independently panned the spike-lexicon method. NOT a retraction; the framing is now contested.
4. **Wood-wide-web arc (context field, same epistemic shape):** Karst/Jones/Hoeksema 2023
   critique (HELD) → Simard rebuttal (Front FGC 2024/25) → Robinson et al. 2024 anti-hype →
   Bock et al. 2025 Communications Biology (new evidence FOR CMNs) → Lehmann et al. 2025
   Functional Ecology meta-analysis → Henriksson et al. 2023 (mother-tree re-analysis,
   inconclusive). Field split; both sides want better field experiments.
5. **Good sign to weigh honestly:** Adamatzky's own 2026 Sci Rep includes temporally-shuffled
   surrogate controls (they destroy the delay structure), and Buffi et al. include a
   cycloheximide kill-control. The better papers in the field are now running artifact controls
   unprompted — but still mostly without biological replicates (Sci Rep 2026: n=1 specimen).

## THE HONEST MAP

**Center of gravity:** Switzerland (Neuchâtel/HES-SO/Empa) is now the most methodologically
serious electrophysiology+materials locus; Bristol is the volume+protocol canon but is visibly
hedging into proteinoids (≥9 of Adamatzky's 15 papers in 2026 are proteinoid, not fungal);
Ecovative is the only group with serious money (DARPA AIxBIO) and the only one with a public
code artifact; Plymouth hosts the honest-negative cluster.

**Measured state of the art (all [V] unless noted):**

| Quantity | Measured value | Source |
|---|---|---|
| Spike amplitude (living mycelium, extracellular) | 0.2–1.4 mV (median 0.6) | Adamatzky Sci Rep 2026 |
| Spike width | ~420 s median (SD 260 s) — MINUTES | Adamatzky Sci Rep 2026 |
| Inter-spike interval | tens of minutes–hours, CV>1 | Adamatzky Sci Rep 2026 |
| Signal propagation speed | ~0.7 cm/min (~40 cm/h) over ~2 cm | Adamatzky Sci Rep 2026 |
| Sampling in the canon | 1 Hz (UWE) / ~17 Hz (Buffi FPC) / 5.85 kHz (LaRocco memristor switching — not spiking) | respective papers |
| Memory capacity, mycelium-based compute | MC(K=10) 0.048–0.209 — measured ONLY on non-living PEDOT-infused chips | Telhan Sci Rep 2026 |
| Reservoir task performance | NARMA-10 NRMSE ≈ 1.01–1.07 (≈ indistinguishable from a well-tuned trivial baseline) | Telhan Sci Rep 2026 |
| Colonization electrophysiological signature | +1,604% PSD, 1.5–8 Hz band, 4 d post-inoculation | Buffi iScience 2025 |
| Fungal battery output | ~300–600 mV | Empa/Reyes 2024 |
| Independent replications of living-mycelium reservoir claims | **ZERO** | this census |

**Where it is poetry (enjoy, do not cite as support):** fungal "language" with ~50 words
(Adamatzky 2022, now Blatt-disputed); "mushroom brains" framing in talks; MycoSoft's
"Fungal Computer Interface" marketing; quantum-entanglement slime-mold simulation (tested,
failed); mother-tree telepathy in the adjacent mycorrhizal narrative (split field, contested);
the Trends Plant Sci 2026 "eclipse cues" paper (Gagliano line — contested researcher co-authoring
with the UWE/Chiolerio cluster); "six orders of magnitude energy advantage" style wetware claims
in press. Also poetry-adjacent: n=1-specimen flagship papers without replicates.

**Bottom line for the operator's "is this real":** the *sensing* is real and measurable
(mV-scale, minutes-wide, slow signals; colonization signatures with controls). The *computing*
is real only in non-living infused chips at MC ≤ 0.2 with task performance at baseline level.
The *living-cube reservoir* claim — our stage ladder — remains unclaimed by anyone, and the
2025 replication failures next door in Physarum raise the prior that some spike "memory" will
reduce to electrode/capacitance artifacts. Our dead-substrate control + surrogate-shuffle
design is exactly what the field is only now adopting.

## FINAL REPORT

**The 5 groups worth watching (ranked):**
1. **Buffi/Junier (Neuchâtel + HES-SO Fribourg + LANL)** — the only group doing systematic,
   control-first mycelial electrophysiology with a reproducible hardware artifact (FPC PCB);
   they have LANL genomics behind them and a methods line worth copying paper-by-paper.
2. **Ecovative / Telhan (DARPA AIxBIO)** — money, code on GitHub, and the only measured
   memory-capacity numbers in the field; every stage-1 result of ours should be comparable
   to their chips.
3. **Unconventional Computing Lab (Adamatzky, UWE)** — still the protocol canon (insoles,
   biohybrid roadmap, spike propagation), but watch the proteinoid pivot; treat new fungal
   claims as canon-adjacent until they replicate.
4. **Plymouth honest-negative cluster (Miranda ICCMR + Biofaction/KIT Schmidt)** — the
   replication police of the adjacent Physarum field; whatever they publish next on fungal
   memristance is the prior we must beat with our dead-substrate control.
5. **Empa Cellulose & Wood Materials** — if fungal living materials (bioplastics, biobatteries,
   moisture sensors) reach commercial sensing, it will likely be this group; their 2025
   S. commune living-materials line is the industrial off-ramp if our cube dies honestly.

**The single most steal-worthy protocol we do not yet have on file:**
**Buffi et al.'s "fungal potential card" (iScience 2025, PMC12483595)** — a purpose-built PCB
with 8 pairs of embedded gold ENIG differential electrodes (2 mm pads, chosen by testing
1–4 mm), inoculated with ~350-spore droplets, recorded inside a humid Faraday cage on a 24-bit
Pico ADC-24 at ~17 Hz, analyzed as power spectral density against uninoculated PCB controls,
with cycloheximide-poisoning as the biological-origin kill-control (kills the >1.5 Hz band).
Why it beats everything else on file: it replaces our loose-electrode-in-substrate rig with a
reproducible fixed-geometry sensor card (kills re-seating variance, our stage-0's biggest
noise source), its control design maps 1:1 onto our stage-2 dead-substrate baseline, and at
~17 Hz it sits 17x above our registered 1 Hz sampling for near-zero extra cost (same ADS1115
class hardware covers it). Action item: fold FPC geometry + cycloheximide kill-control into
cube01 as a stage-0.5 hardware revision candidate (new registration row; no claim change).

**Cross-check ledger (NEW vs HELD):**
- HELD unchanged: Telhan Sci Rep 2026 + code; LaRocco 2025; FEMS Buffi review fuaf009;
  Adamatzky star-array 2601.08099; Biosystems 262:105739; Physarum tactile/bio-memristor
  base line; Pieters 2022 + theory row; "Fungal sensing skin" retraction; Karst 2023.
- NEW this receipt: Adamatzky Sci Rep s41598-026-47035-2 (+full protocol numbers, n=1 flag);
  Mougkogiannis & Adamatzky Trichoderma ACS ABM 2026; proteinoid pivot quantified;
  Buffi/Junier group + iScience 2025 FPC protocol; DARPA AIxBIO program attribution;
  Schmidt/KIT Physarum replication failure; Miranda quantum-test failure; Blatt 2024 language
  critique; Simard/Bock/Lehmann/Robinson/Henriksson wood-wide-web arc updates; Empa biobattery
  + living materials; INRAE bacterial RC; FinalSpark wetware platform; MycoSoft poetry tier;
  ETH thesis tier; Gagliano co-authorship red flag; retracted-skin citation-accrual note.

*Sources verified via Europe PMC API, PMC full-text fetches, PEARL (Plymouth), and live search
this session; flagged items (Empa Reyes ACS DOI exact string, RSOS 252341 record) marked
fetch-flagged/UNVERIFIED in-line. No paid APIs used; no git operations.*

### Progress log

- [step 0] Receipt created before any other work.
- [step 1] Held-set read: C17_CUBE_INSTRUMENT_PLAN.md (Telhan Sci Rep 2026 + code, LaRocco PLOS ONE 2025,
  Adamatzky canon incl. retracted "Fungal sensing skin" 2021, Biosystems 262:105739 Feb 2026,
  star-array arXiv 2601.08099 [held per mission brief], FEMS Buffi fuaf009 review [held],
  Physarum tactile/bio-memristor line, theory 2508.19145/Sugiura 2024/Pieters 2022).
- [step 2] WebSearch sweep 1 (Adamatzky status + general group census):
  - **[HELD+UPDATE] Adamatzky / UWE Unconventional Computing Lab — still active, Head of Lab confirmed.**
    NEW vs C17: "Propagation of electrical spike trains in substrates colonised by oyster fungi,"
    Sci Rep (2026), doi.org/10.1038/s41598-026-47035-2 — long-term multi-channel recording of
    Pleurotus-colonised substrate (companion to the held star-array preprint; likely the
    peer-reviewed landing). Link: nature.com/articles/s41598-026-47035-2.
    Also surfaced: Royal Society Open Science 13:7 (2026) "Multi-scale electrical activity and
    signal propagation" royalsocietypublishing.org/rsos/article/13/7/252341 — UNVERIFIED authorship,
    fetch pending. Springer book "Fungal Machines: Sensing and Computing with Fungi" (© 2026) —
    Adamatzky, canonical monograph to cite.
  - **[NEW GROUP] Buffi M. et al. 2025, "Detection of electrical signals in fungal mycelia in
    response to …" — PMC12483595 — PCB with embedded differential electrodes for extracellular
    mycelial recording.** This is a protocol-grade instrumenting group distinct from UWE;
    affiliation + latest-result fetch pending (likely Univ. Neuchâtel / Junier lab, per the
    held FEMS review authorship "… Junier P.").
  - MycoSoft "Fungal Computer Interface (FCI)" (industry/Medium, not academic peer-reviewed) — noted, tiered
    as artifact/press, not evidence.
- [step 3] Group verification fetches:
  - **[NEW — Buffi/Junier group verified via PMC12483595 full fetch]:** Matteo Buffi, Guillaume Cailleau,
    Saskia Bindschedler, Pilar Junier (Univ. Neuchâtel) + Silvia Giangaspero, Daniel Oberson,
    Lorenzo Pirrami (iSIS Institute, HEIA-FR, HES-SO Fribourg) + Valerio Foiada, Loïc Puthod
    (Prototypos Sarl) + Aaron J. Robinson, Julia M. Kelliher, Patrick S.G. Chain (Los Alamos
    National Lab) + Markus Künzler (ETH Zürich). Latest result: "Detection of electrical signals
    in fungal mycelia…", **iScience 28(10):113484 (2025-10), DOI 10.1016/j.isci.2025.113484, CC BY.**
    Rig: "fungal potential card" (FPC) — PCB with 8 pairs of embedded gold ENIG differential
    electrodes (2 mm), Faraday cage, Pico ADC-24, **~17 Hz sampling**. Organism: Fusarium oxysporum.
    Numbers: colonization → +1,604.75% PSD vs uninoculated control (p<0.001); signature
    frequencies 1.5–8 Hz at ≥4 days post-inoculation (controls <1 Hz); cycloheximide kills the
    >1.5 Hz band (biological-origin control — this is the kind of kill-control our stage ladder
    wants). Biocide responses non-significant = honest negative flagged in their own text.
  - **[HELD+NEW — Ecovative/DARPA line verified]:** Telhan, Winiski, Schaak, Siegel, Petrillo,
    Bayer — Ecovative LLC; Sci Rep 16:26421 (2026) is held in C17. NEW detail: funded by
    **DARPA BTO AIxBIO program (awarded Dec 2024)** for bioelectronic mycelial computing
    (distinct from the 2016 ELM $9.1M contract). Telhan project page:
    orkantelhan.com/myceliumcompute. PubMed 42271130.
- [step 4] Replication/dispute sweep 1 — TWO NEW disputes found (both 2025, both negative-replication class):
  - **[NEW DISPUTE] Schmidt et al. 2025, "Electrical characterization of the alleged
    bio-memristor Physarum polycephalum," MRS Advances** (DOI 10.1557/S43580-025-01198-8;
    Plymouth PEARL + Karlsruhe Institute of Technology) — reports **NO memristive behavior**;
    observed hysteresis may be a measurement artifact. Directly contests the Gale/Adamatzky
    "slime mould memristor" line (arXiv 1306.3414). Not a retraction — a failed independent
    replication. Word "alleged" in title signals the field's own skepticism.
  - **[NEW DISPUTE] Miranda et al. 2025, "From simulation to reality: experimental analysis of a
    quantum entanglement simulation with slime molds as bioelectronic components," Frontiers in
    Soft Matter (2025, DOI 10.3389/frsfm.2025.1588404)** — Eduardo R. Miranda (Plymouth, ICCMR;
    author of the original 2017 "growing bio-memristors from slime mold" method) reports slime
    molds FAIL the quantum-entanglement simulation test; honest negative from the line's own
    founder-adjacent lab.
  - **[NEW DISPUTE] Fungal "language" critique:** Fungal Ecology 2024 (bibcode 2024FunE...6801326B)
    — methodological rebuttal to Adamatzky's 2022 RSOS "fungal words" claim ("up to 50 words");
    UPS Language Log linguists separately critiqued the spike-lexicon methodology. Authorship
    verification pending (ADS fetch) — search summary attributed "M.R. Blatt et al.", UNVERIFIED.
  - Note S3 lane overlap: skeptic watch will want the Blatt/Physarum disputes; filed here as
    primary, S3 may cross-ref.
- [step 5] Blatt authorship VERIFIED + Karst follow-ups + adjacent biological RC census:
  - **[VERIFIED] Blatt, M.R. (2024), "Does electrical activity in fungi function as a language?",
    Fungal Ecology 68:101326** (sciencedirect.com/science/article/abs/pii/S1754504823001034) —
    commentary directly contesting Adamatzky 2022 RSOS "Language of fungi… up to 50 words."
    Blatt = plant electrophysiologist (Univ. Glasgow) — an outsider-from-physiology critique,
    cited ~15x. NOT a retraction of Adamatzky 2022; the RSOS paper still stands but the
    "language" framing is now officially disputed in the literature.
  - **[HELD+NEW — wood-wide-web arc]** We hold Karst/Jones/Hoeksema 2023 Nat Ecol Evol
    ("positive citation bias… misinformation on CMNs"). NEW since:
    (a) Simard, "Response to questions about common mycorrhizal networks," Frontiers in Forests
    and Global Change (2024/25, DOI 10.3389/ffgc.2024.1512518) — direct rebuttal defending CMN evidence;
    (b) Robinson et al. 2024, Trends in Plant Science — "mother trees, altruistic fungi, perils
    of plant intelligence" (anti-hype side);
    (c) Bock et al. 2025, Communications Biology (nature.com/articles/s42003-025-08432-x) — NEW
    experimental evidence FOR common fungal networks (cited 14x);
    (d) Lehmann et al. 2025, Functional Ecology meta-analysis (DOI 10.1111/1365-2435.70125);
    (e) Henriksson et al. 2023, New Phytologist — re-analysis of Simard's own data, "mother tree"
    inconclusive. State of play: split field; both sides agree better field experiments needed.
    RELEVANCE TO CUBE: this dispute is the epistemic template — popular narrative outran field
    evidence until critics forced controls. Same shape as fungal-spike claims today.
- [step 6] Adamatzky-2026 Europe PMC census (AUTH:"Adamatzky" AND PUB_YEAR:2026, 15 hits):
  - **Only 3 of 15 are fungi:** (a) Mougkogiannis & Adamatzky, "Voltage Spiking Synchronicity
    with Growth Transitions in Trichoderma reesei," ACS Appl Bio Mater 2026 (DOI
    10.1021/acsabm.6c01286) — NEW: fungal spiking tied to growth-phase transitions;
    (b) Adamatzky, "Propagation of electrical spike trains…oyster fungi," Sci Rep 2026
    (PMID 41935231, PMCID PMC13212958) — the NEW peer-reviewed landing;
    (c) Biosystems 262:105739 biohybrid (HELD in C17).
  - **The lab's center of gravity has pivoted to proteinoid/abiotic computing** (≥9 of 15 papers
    with P. Mougkogiannis: proteinoid microspheres, neurotransmitter assemblies, olivine/aragonite
    substrates, grape-must bioelectrochemical processor). Implication for the honest map: the
    field's most prolific figure is hedging out of fungi into proteinoids; the fungal canon is
    not being rapidly extended by its originator.
  - Red-flag association for the skeptic file: Chiolerio + **Monica Gagliano** + Adamatzky,
    "Discriminating eclipse cues from weather," Trends in Plant Science 2026 (DOI
    10.1016/j.tplants.2026.04.004) — Gagliano's plant-learning claims are heavily disputed in
    the literature; co-authorship ties the fungal line to contested plant-cognition territory.
- [step 7] Sci Rep 2026 (PMC13212958) FULL FETCH — protocol numbers now [V] (upgrades C17's [F] row):
  - Rig: SPES MEDICA sub-dermal needle electrodes, twisted pair, LINEAR array of 8 differential
    pairs; intra-pair ~1 cm; adjacent channels ~2 cm; on Pleurotus ostreatus grown on wood
    shavings. Pico ADC-24 (24-bit), **1 Hz stored sampling** (logger averages ~600 reads/s),
    **~15 days continuous, NO stimulus applied** (spontaneous only).
  - Numbers: spike amplitudes **0.2–1.4 mV (median ≈0.6 mV, mean ≈0.7, SD ≈0.3)**; spike widths
    **median ≈420 s (SD ≈260 s)** — minutes, not ms; ISIs tens of minutes–hours (CV > 1);
    bursts (2–4 spikes) 15–35% of spikes; inter-channel delay median ≈180 s over ~2 cm →
    **propagation speed ≈0.7 cm/min (~40 cm/h)**; temporally-shuffled surrogates destroy the
    delay structure (control PRESENT — the field is learning the right controls).
  - **Honesty flag: n = 1 specimen. Zero biological replicates. Single author.**
- [step 8] Materials-adjacent sweep (mycelium electronics / sensors):
  - **[NEW GROUP] Empa (Cellulose & Wood Materials lab, CH):** 3D-printed fungal biobattery
    (yeast anode + mold cathode, **~300–600 mV**, self-digesting; Reyes et al. 2024, ACS
    Sustainable Chem & Eng) + living mycelium bioplastics from Schizophyllum commune reacting
    to moisture (2025, pitched for living sensors). Power/materials line, not electrophysiology.
  - ETH Zürich "Fungal circuitry: mycelium as a living sensor for smart structures" — THESIS
    tier (structural health monitoring), not peer-reviewed paper.
  - Chitin nanopaper TENG (Khan et al. 2024, cited 33x) — fungal-DERIVED material, not living fungus.
  - Note: the retracted 2021 "Fungal sensing skin" (PMC7972235) still shows "cited by 67" —
    citation hygiene problem confirmed live: the retracted row keeps accumulating citations.
  - **[NEW — adjacent biological RC groups]**
    - INRAE (France, Faulon group) bacterial reservoir computing — bioRxiv 2024.09.12.612674
      (bacterial strains as RC reservoirs; PhD program open) + "Microbial Computing: review and
      perspectives," Biotechnol Adv 2025 (S0734975025002526).
    - Plant RC consolidation: Pieters et al. 2022 Sci Rep (held) remains foundational; Cambridge
      repository item "Learning physical coupling for homeostatic behaviours" — minimal reservoir
      physically coupled to a plant (nonlinear control).
    - Living neural cultures: chaos-controlled RC with living neural cultures (arXiv 2604.02552);
      wetware industry: Cortical Labs CL1 (held in X-mine), FinalSpark Neuroplatform (CH, 2024).
