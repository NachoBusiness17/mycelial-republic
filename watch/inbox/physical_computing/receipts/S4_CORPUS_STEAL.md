# S4 RECEIPT — CORPUS STEAL: the fungal-compute canon as a reading register

- **Date:** 2026-09-16
- **Lane:** wave S4, physical_computing
- **Operator question on file:** "steal existing research and journals around this"
- **Mission:** assemble the actual canon — key papers on fungal/mycelial electrophysiology, fungal computing, organismal/wetware reservoir computing — as a reading register with full-text links and protocol extractions. Target 15–25 works, tiers T1–T4. Per paper: full citation, DOI + best free full-text link, 3-line extract (what was measured / instrument + sample rate / result + magnitude).
- **Held already (verify + extend, don't re-litigate):** Telhan 2026 Sci Rep (PMC13500807), LaRocco 2025 PLOS ONE (shiitake memristors), Buffi 2025 iScience FPC (PMC12483595), Buffi 2025 FEMS review (PMC11995700), Adamatzky star-array arXiv 2601.08099, Adamatzky "Towards fungal computer" 2018, retracted "Fungal sensing skin" 2021, Karst wood-wide-web critique.
- **Method:** WebSearch/WebFetch + free APIs (arXiv, Europe PMC REST, Semantic Scholar) — no paid APIs, no git. Receipt-first, appended as evidence lands.
- **Ledger law:** each paper registered via `./.venv/Scripts/python.exe -m mag.link_library add <best-url> --note "fungal-compute canon: <title one-line>" --writer canon-fungal-20260916`. Duplicate status marked honestly per row.

## Status: DONE 2026-09-16 — 26 canon works filed to ledger, 0 duplicates, hunt log + register + filing table below

---

(sections appended as research proceeds)

## Hunt log — Europe PMC batch 1–3 (2026-09-16, curl + .venv python, free APIs only)

**CONFIRMED RETRACTION CHAIN (T4):** "Fungal sensing skin" (2021), Fungal Ecology and Biology,
DOI 10.1186/s40694-021-00110-x, PMC7972235, Adamatzky — retracted via "Retraction Note to:
Fungal sensing skin," DOI 10.1186/s40694-021-00114-7, PMC8173894. Companion "Towards fungal
sensing skin," DOI 10.1186/s40694-021-00113-8, PMC8117569 (cited 16) is NOT retracted and
remains live. Withdrawn preprint v2 also on file (DOI 10.21203/rs.3.rs-113217/v2).

**KEY T1 ADDITIONS FOUND:**
- Slayman CL, Long WS, Gradmann D (1976). "Action potentials" in Neurospora crassa, a mycelial
  fungus. Biochim Biophys Acta 426:732-744. DOI 10.1016/0005-2736(76)90138-3. Cited 62. Paywalled.
  This is the founding intracellular recording of action potentials in a fungus.
- Adamatzky (2022). Language of fungi derived from their electrical spiking activity.
  R. Soc. Open Sci. 9:211926. DOI 10.1098/rsos.211926. PMC8984380. OPEN. Cited 33.
- Adamatzky (2023). Electrical response of fungi to changing moisture content.
  Fungal Ecol. Biol. DOI 10.1186/s40694-023-00155-0. PMC10069029. OPEN. Cited 10.
- Adamatzky (2022). Electrical spiking of psilocybin fungi. DOI 10.1080/19420889.2022.2136118.
  PMC9601536. OPEN. Cited 3.
- Adamatzky (2026). Propagation of electrical spike trains in substrates colonised by oyster
  fungi. Sci. Rep. DOI 10.1038/s41598-026-47035-2. PMC13212958. OPEN. — NEEDS comparison vs
  arXiv 2601.08099 (held): preprint DOI differs (10.64898/2026.01.12.699130 vs Research Square
  10.21203/rs.3.rs-8450263/v1); may be a second 2026 paper or the published twin. Verify below.
- Adamatzky (2023). Propagation of electrical signals by fungi. Biosystems 233:104933.
  DOI 10.1016/j.biosystems.2023.104933. Cited 14. Paywalled.
- Adamatzky (2023). Responsive fungal insoles for pressure detection. Sci. Rep.
  DOI 10.1038/s41598-023-31594-9. PMC10030783. OPEN. (wearable-sensing protocol)

**KEY T2 ADDITIONS FOUND:**
- Adamatzky (2020). On Boolean gates in fungal colony. Biosystems 198:104138.
  DOI 10.1016/j.biosystems.2020.104138. Cited 18. Paywalled.
- Kagan BJ et al. (2022). In vitro neurons learn and exhibit sentience when embodied in a
  simulated game-world. Neuron 110:2029-2041. DOI 10.1016/j.neuron.2022.09.001. PMC9747182.
  OPEN. Cited 198. (DishBrain — wetware computing canon)
- Sumi T et al. (2023). Biological neurons act as generalization filters in reservoir computing.
  PNAS 120:e2217008120. DOI 10.1073/pnas.2217008120. PMC10288593. OPEN. Cited 34.
- Adamatzky (2024). Fungal skin for robots. Biosystems 236:105106. DOI 10.1016/j.biosystems.2023.105106.
  Cited 7. Paywalled. (successor line to retracted sensing-skin; live, NOT retracted)

**KEY T3 ADDITIONS FOUND:**
- Nakagaki T, Yamada H, Tóth Á (2000). Maze-solving by an amoeboid organism. Nature 407:470.
  DOI 10.1038/35035159. Cited 297. Paywalled.
- Tero A et al. (2010). Rules for biologically inspired adaptive network design. Science
  327:439-442. DOI 10.1126/science.1177894. Cited 263. Paywalled.
- Volkov AG, Adesina T, Jovanov E (2007). Closing of Venus flytrap by electrical stimulation of
  motor cells. Plant Signal. Behav. 2:139-145. DOI 10.4161/psb.2.3.4217. PMC2634039. FREE PMC.
  Cited 74. (+ Volkov 2014 "Memristors in the Venus flytrap," PMC4203580, FREE PMC.)
- Toyota M et al. (2018). Glutamate triggers long-distance, calcium-based plant defense
  signaling. Science 361:1112-1115. DOI 10.1126/science.aat7744. Cited 674. Paywalled at NCBI
  (science.org free after 12 months).

**KEY T4 CONFIRMATION:**
- Karst J, Jones MD, Hoeksema JD (2023). Positive citation bias and overinterpreted results lead
  to misinformation on common mycorrhizal networks. Nat. Ecol. Evol. 7:1107-1112.
  DOI 10.1038/s41559-023-01986-1. Cited 67 (+ author correction DOI 10.1038/s41559-023-02035-7).
  Paywalled at publisher.

**STILL TO HUNT (non-biomedical venues, not in Europe PMC):** Fernando & Sojakka 2003 "Pattern
recognition in a bucket"; Physarum memristor (Gale/Whiting/Adamatzky, arXiv); Physarum reservoir
computing; "shrinking blob" TSP (Jones & Adamatzky); LaRocco shiitake memristor exact record
(author search polluted by other LaRoccos — retry by title/PMCID); "Thomas & Cooper 2022"
thread-control critique (cited inside FEMS review — locate source).

## CORRECTIONS to hunt log above

- Karst 2023 pages: Nat. Ecol. Evol. **7:501-511** (hunt log's "1107-1112" was wrong).
- Blatt et al. 2024 "Does electrical activity in fungi function as a language?" (Fungal Ecology
  68:101326) is NOT in Europe PMC — filed from the FEMS review bibliography; paywalled.
- Thomas & Cooper 2022 is the CONTESTED CLAIM paper (mycelium bridges conduct wound signals);
  the thread-control critique is Blatt et al. (2023 challenge + FEMS). C19's one-line summary
  attributed the thread experiment to Thomas & Cooper — this register fixes that attribution.
- "On Boolean gates in fungal colony" has a free arXiv version: arXiv:2002.09680.

---

# THE REGISTER — fungal-compute canon, tiered (26 works + 1 appendix)

Per row: full citation · DOI · best free full-text · 3-line extract (measured / instrument + rate / result + magnitude).

## T1 — Fungal electrical spiking + measuring protocols

**[T1.1] Slayman CL, Long WS, Gradmann D (1976). "Action potentials" in Neurospora crassa, a mycelial fungus. Biochim. Biophys. Acta 426:732-744.** DOI 10.1016/0005-2736(76)90138-3 · PAYWALLED (ScienceDirect), no free copy found.
- Measured: spontaneous action potentials in mature hyphae — the founding intracellular recording in a fungus.
- Instrument: glass intracellular microelectrodes on hyphal membrane potential; analog electrophysiology.
- Result: APs 1-2 min long, upstroke triggering 5-20 mV depolarized from ~-180 mV resting, peak near -40 mV (≈140 mV swing), 2-8x membrane-conductance rise; mechanism debated (H+/Cl- permeability vs H+-pump suppression).

**[T1.2] Adamatzky A (2018). Towards fungal computer. Interface Focus 8:20180029.** DOI 10.1098/rsfs.2018.0029 · FREE: PMC6227805 · **HELD (C17 verified abstract-level; full record now filed)**
- Measured: extracellular spike activity of fruit bodies as indicator of response to thermal and chemical stimulation; distant transfer between fruit bodies of a cluster.
- Instrument: differential electrode pairs on basidiomycete fruit bodies/substrate, long-term logging (same lab rig later specified as Pico ADC-24-class, 1 Hz — rate from lab companion papers).
- Result: proof-of-concept "fungal computer": spikes = information, mycelium geometry determines which logical functions the network computes (automaton model).

**[T1.3] Adamatzky A (2022). Language of fungi derived from their electrical spiking activity. R. Soc. Open Sci. 9:211926.** DOI 10.1098/rsos.211926 · FREE: PMC8984380
- Measured: extracellular spiking in 4 species (incl. Flammulina velutipes, Omphalotus nidiformis) as spike trains → "words".
- Instrument: 8 differential electrode pairs inserted in colonized substrate/fruit bodies; long-term lab rig (1 Hz-class, Pico ADC-24 in companion papers).
- Result: species-specific spiking: durations 1-21 h, amplitudes 0.03-2.1 mV; e.g. one 12-spike train avg 2.1 mV (σ 0.1), 64-min spikes; low-amp species avg 0.007 mV. (The "language" framing is the part Blatt 2024 attacks — keep the numbers, drop the poetry.)

**[T1.4] Adamatzky A (2023). Electrical response of fungi to changing moisture content. Fungal Ecol. Biol. 3(1).** DOI 10.1186/s40694-023-00155-0 · FREE: PMC10069029
- Measured: extracellular spiking vs substrate drying/wetting on oyster-mushroom blocks.
- Instrument: Pico ADC-24 (24-bit) + PicoLog, stainless sub-dermal needle pairs (Spes Medica), 1 s sampling, ±39 mV range; moisture cross-logged via EC-5/HOBO.
- Result: drying → spontaneous trains ~3 mV peak with ~10 h period; deionized-water spray → ~6 mV peaks; some double-peak pulses ~15 mV. Artifact lesson filed: the HOBO/EC-5 logging path itself injected interference into the ADC — loggers must not share conductive paths.

**[T1.5] Adamatzky A (2026). Directional Electrical Spiking, Bursting, and Information Propagation in Oyster Mycelium Recorded with a Star-Shaped Electrode Array. arXiv 2601.08099.** arXiv 2601.08099 (preprint of Research Square DOI 10.21203/rs.3.rs-8450263/v1) · FREE: arxiv.org/abs/2601.08099 · **HELD (C19, full protocol extracted)**
- Measured: directional spike propagation across a colonized substrate disc.
- Instrument: 16 electrodes radial star → 8 differential compass channels, Pico ADC-24 (24-bit, galvanically isolated, ~2 MΩ), 1 Hz with per-second averaging, up to 5 days.
- Result: >10x spike-rate spread between directions; bursts with minutes-long quiescence; local coupling, NO global synchrony; recruitment delays seconds→thousands of seconds. Author's own framing: "spatially extended excitable medium."

**[T1.6] Adamatzky A (2026). Propagation of electrical spike trains in substrates colonised by oyster fungi. Sci. Rep. (in press 2026).** DOI 10.1038/s41598-026-47035-2 · FREE: PMC13212958 · **NEW — twin paper to T1.5 (different instrument, same lab/year)**
- Measured: direction and speed of slow travelling spikes along a linear transect of colonized substrate.
- Instrument: linear array of 8 differential electrode channels, 1 Hz continuous, ~15 days.
- Result: spikes millivolt-scale, durations tens of seconds→tens of minutes; directional propagation with monotonic lead-lag ordering; median delay ~180 s per ~2 cm ⇒ **~0.7 cm/min (~40 cm/h) propagation speed**; temporally-shuffled spike trains as control confirm biological origin. The shuffled-control is a stealable falsifier for our own rig.

**[T1.7] Buffi G et al. (2025). Detection of electrical signals in fungal mycelia in response to external stimuli. iScience 28(10):113484.** DOI 10.1016/j.isci.2025.113484 · FREE: PMC12483595 · **HELD (C19)**
- Measured: mycelium-vs-control differential response on a purpose-built sensor card (Fungal Potential Card).
- Instrument: PCB with 8 pairs of ENIG gold differential electrodes (2 mm optimal, 1 cm apart), mycelium grows onto card in 3-4 days (~20 µL droplet), Pico ADC-24 direct differential ~17 Hz, Faraday cage, shielded D-Sub.
- Result: colonization adds 1.5-8 Hz components, **+1604.75% PSD vs uninoculated control (p<0.001)**; biocide kills >1.5 Hz content; DMSO interferes with gold electrodes (own artifact confession).

**[T1.8] Buffi G et al. (2025). Electrical signaling in fungi: past and present challenges. FEMS Microbiol. Rev. 49:fuaf009.** DOI 10.1111/1574-6976.70021 (PMC11995700) · FREE: PMC11995700 · **HELD (C19) — doubles as the T4 methods-checklist**
- Measured: field-wide audit of fungal electrophysiology claims + own replication attempts.
- Instrument: critical review; own Pico ADC-20/24 rig with sub-dermal needles, uncolonized-substrate controls.
- Result: fungal voltages likely **nV-µV** (vs Adamatzky mV claims); stainless needles read Donnan potentials; recorded spikes correlate with door-opening/people/walking shades IN CONTROLS; relevant band 0.0003-0.1 Hz; commercial MEAs pick up noise only; demands Faraday cage + killed/uncolonized controls + intracellular validation.

## T2 — Fungal/bio-matter as computational substrate

**[T2.1] Telhan O, Winiski M, Schaak C, Siegel A, Petrillo M, Bayer I — Ecovative (2026). Morphologically tunable mycelium chips for physical reservoir computing. Sci. Rep. 16.** DOI 10.1038/s41598-026-55550-5 · FREE: PMC13500807 · code github.com/otelhan/NeuromorphicMyceliumChip (MIT) · **HELD (C17)**
- Measured: memory capacity (MC) of non-living electrolyte-infused mycelium chips as physical reservoirs.
- Instrument: infused-chip electrode rig per their open GitHub; NARMA-10 benchmark; 8-month retest stability.
- Result: chips score MC_peak > 0.05, drift < 1 mV/h after warmup; mycelium morphology tunes reservoir properties; the RC methodology our stage-1 mirrors for comparability.

**[T2.2] LaRocco M et al. (2025). Sustainable memristors from shiitake mycelium for high-frequency bioelectronics. PLOS ONE.** DOI 10.1371/journal.pone.0328965 · FREE: PMC12513579 · **HELD (C17)**
- Measured: memristive switching in shiitake mycelium devices (pinched-hysteresis I-V).
- Instrument: two-terminal device sweeps + HF characterization (Ohio State; bioRxiv 2025.07.11.664296 preprint).
- Result: switching up to 5.85 kHz, ~90±1% consistency, functions after dehydration — duty-cycle- and desiccation-tolerant bio-memory.

**[T2.3] Adamatzky A, Tsompanas M (2020). On Boolean gates in fungal colony. Biosystems 198:104138.** DOI 10.1016/j.biosystems.2020.104138 · FREE: arXiv 2002.09680
- Measured/modelled: excitation-wave logic in an Aspergillus niger colony; binary inputs as electrical impulses on an electrode pair, responses recorded on 16 electrodes; FitzHugh-Nagumo simulation of propagation.
- Instrument: 16-electrode recording + F-N model (hybrid experiment/model).
- Result: sets of two-inputs-one-output Boolean gates derivable from colony response distributions — computation is colony-geometry-dependent (same caveat as T1.2).

**[T2.4] Adamatzky A et al. (2026). Fungal biohybrid substrates for resilient sensing and embodied anomaly detection. Biosystems 261:105739.** DOI 10.1016/j.biosystems.2026.105739 · PAYWALLED, no free copy · **HELD (C17, abstract-verified)**
- Measured: living fungal biohybrid substrates as self-repairing sensor layers for anomaly detection.
- Instrument: Adamatzky-lab differential electrophysiology rig (per abstract).
- Result: biohybrid sensing survives partial damage; embodied anomaly detection demonstrated. Paywalled — treat as claim + abstract until library access.

**[T2.5] Kagan BJ et al. (2022). In vitro neurons learn and exhibit sentience when embodied in a simulated game-world. Neuron 110:2029-2041.** DOI 10.1016/j.neuron.2022.09.001 · FREE: PMC9747182
- Measured: learning in embodied cortical cultures (DishBrain) playing Pong.
- Instrument: HD-MEA arrays, 512x gain, 300 Hz high-pass; feedback stimulation (unpredictable: 150 mV 5 Hz 4 s; predictable bursts 100 Hz 100 ms); blinded analysis with >75 mV large-spike masking.
- Result: cultures improve at Pong (rally length correlates with organized activity) — the wetware closed-loop template any organismal reservoir wants to copy.

**[T2.6] Sumi T et al. (2023). Biological neurons act as generalization filters in reservoir computing. PNAS 120:e2217008120.** DOI 10.1073/pnas.2217008120 · FREE: PMC10288593
- Measured: reservoir properties of microphysiological brain neural networks (mBNNs) on RC tasks.
- Instrument: calcium fluorescence imaging (ΔF/F, 20 Hz sampling) + CASCADE spike inference; standard RC task battery.
- Result: bio-reservoirs act as "generalization filters" — better on unseen inputs than tuned baselines; the honest performance bar for wetware RC.

**[T2.7] Adamatzky A (2024). Fungal skin for robots. Biosystems 236:105106.** DOI 10.1016/j.biosystems.2023.105106 · PAYWALLED (preprint free: DOI 10.21203/rs.3.rs-3292325/v1)
- Measured: fungal skin (mycelium + electrodes) as robot tactile/chemical sensing layer.
- Instrument: Adamatzky-lab differential rig on flexible substrate.
- Result: tactile and chemical sensing demonstrated on robotic skin; NOT retracted (distinct from the retracted 2021 sensing-skin, T4.2). Live successor of the retraction lineage.

## T3 — Adjacent machinery we borrow method from

**[T3.1] Nakagaki T, Yamada H, Tóth Á (2000). Maze-solving by an amoeboid organism. Nature 407:470.** DOI 10.1038/35035159 · PAYWALLED (Nature)
- Measured: Physarum plasmodium solving a maze by connecting food sources.
- Instrument: time-lapse imaging of agar-grown plasmodium (morphological readout).
- Result: tube thickening selects the shortest path — substrate-adaptive network computation without neurons.

**[T3.2] Tero A, Takagi S, Saigusa T, Ito K, Kobayashi R, Nakagaki T et al. (2010). Rules for biologically inspired adaptive network design. Science 327:439-442.** DOI 10.1126/science.1177894 · PAYWALLED (author PDFs circulate; honest: paywalled)
- Measured: Physarum re-creating the Tokyo-area rail network from food-source city placement.
- Instrument: time-lapse + fitted mathematical model (the "Physarum equation").
- Result: plasmodium network matches real infrastructure at low cost/high efficiency — founding slime-mold-routing result.

**[T3.3] Jones J, Adamatzky A (2013; pub. Natural Computing 2014). Computation of the Travelling Salesman Problem by a Shrinking Blob.** arXiv 1303.4969 · FREE: arxiv.org/abs/1303.4969
- Measured: Physarum vascular network shrinking toward TSP city markers.
- Instrument: wet Physarum on agar with food markers + imaging; offline tour extraction.
- Result: near-optimal TSP tours emerge from shrinking dynamics — organismal optimization on a budget.

**[T3.4] Gale E, Adamatzky A, de Lacy Costello B (2013). Slime Mould Memristors.** arXiv 1306.3414 · FREE: arxiv.org/abs/1306.3414
- Measured: memristive (pinched-hysteresis) I-V behavior in Physarum protoplasmic tubes.
- Instrument: two-terminal electrical sweeps.
- Result: living slime mould shows memristor-like switching — with a standing artifact dispute (electrode/electrolyte vs true memristance; HN thread + memristor-literature caution applies to our own DC sweeps too).

**[T3.5] Pershin YV, La Fontaine S, Di Ventra M (2008; pub. Phys. Rev. E 82:021926, 2010). Memristive model of amoeba's learning.** arXiv 0810.4179 · FREE: arxiv.org/abs/0810.4179
- Measured/modelled: habituation-like learning in Physarum reproduced by a memristive circuit model.
- Instrument: re-analysis of published amoeba learning experiments + memristive-model simulation.
- Result: adaptive-frequency oscillations map onto memristor state dynamics — the theory link between bio-learning and memristive hardware.

**[T3.6] Volkov AG, Adesina T, Jovanov E (2007). Closing of Venus flytrap by electrical stimulation of motor cells. Plant Signal. Behav. 2:139-145.** DOI 10.4161/psb.2.3.4217 · FREE: PMC2634039
- Measured: trap closure driven purely by electrical stimulation of motor cells (no mechanical trigger).
- Instrument: stimulation electrodes midrib↔lobe + ultra-fast acquisition of closing kinematics.
- Result: closure in 0.3 s (same as mechanical), mean closing charge **13.6 µC**; ion-channel blockers (Ba2+, TEACl) and uncouplers (FCCP, DNP, PCP) slow closure dramatically — full closed-loop bio-actuation characterization; the plant-AP measurement template.

**[T3.7] Bajpai S, Lucas-DeMott A, Murugan NJ, Levin M, Kurian P (2025). Morphological computational Capacity of Physarum polycephalum.** arXiv 2510.19976 · FREE: arxiv.org/abs/2510.19976
- Measured: the slime mould's body as a living reservoir — spatial ATP distribution + network exploration under stimuli.
- Instrument: imaging of morphology/ATP maps + reservoir-computing analysis.
- Result: growth dynamics carry exploitable computational capacity ("living substrate akin to a reservoir computer") — current Levin-lab framing of organismal RC.

## T4 — Critics, retractions, contested claims

**[T4.1] Karst J, Jones MD, Hoeksema JD (2023). Positive citation bias and overinterpreted results lead to misinformation on common mycorrhizal networks. Nat. Ecol. Evol. 7:501-511.** DOI 10.1038/s41559-023-01986-1 (+ correction DOI 10.1038/s41559-023-02035-7) · PAYWALLED at publisher (correction free) · **HELD as "Karst critique" (C17/S1); full record now filed**
- Measured: citation audit of "wood-wide-web" mycorrhizal-network claims back to primary evidence.
- Instrument: systematic citation-bias analysis (hundreds of papers screened; few primary studies traced).
- Result: the famous claims rest on very few underpowered sites; most citations amplify overinterpretation — the template for auditing any hype-adjacent bio-computing claim, including fungal-language claims.

**[T4.2] Adamatzky A (2021). Fungal sensing skin. Fungal Ecol. Biol. — RETRACTED.** DOI 10.1186/s40694-021-00110-x · FREE: PMC7972235 · Retraction note: DOI 10.1186/s40694-021-00114-7 (PMC8173894) · **HELD (C17 retraction watch); chain now fully documented**
- Measured: claimed fungal sensing-skin electrophysiology.
- Instrument: lab differential rig (per retracted paper).
- Result: RETRACTED; withdrawn preprint v2 also on file (DOI 10.21203/rs.3.rs-113217/v2). The live companion "Towards fungal sensing skin" (DOI 10.1186/s40694-021-00113-8, PMC8117569) was NOT retracted — cite it, not the dead one.

**[T4.3] Thomas MA, Cooper RL (2022). Building bridges: mycelium-mediated plant-plant electrophysiological communication. Plant Signal. Behav. 17:2129291.** DOI 10.1080/15592324.2022.2129291 · FREE: PMC9673936
- Measured: wound-response electrical signals claimed to cross mycelial bridges between plants.
- Instrument: surface electrodes at plant/root/bridge junctions.
- Result: authors claim reliable conduction across mycelium — BUT the FEMS review and Blatt 2023 note the design flaw: a current is still recorded when the mycelium is REPLACED BY A THREAD ⇒ physical artifact, not biology. Contested claim; use as the worked example of what our controls must exclude.

**[T4.4] Blatt MR, Pullum GK, Draguhn A et al. (2023). A challenge to claims for mycorrhizal-transmitted wound signaling. Plant Signal. Behav. 18:2222957.** DOI 10.1080/15592324.2023.2222957 · FREE: PMC10259323 · (+ Blatt et al. 2024, "Does electrical activity in fungi function as a language?", Fungal Ecol. 68:101326, DOI 10.1016/j.funeco.2023.101326, PAYWALLED — same group, fungal-language critique)
- Measured: re-analysis of the mycorrhizal-bridge signaling claim (T4.3) for electrical artifacts.
- Instrument: control-experiment critique (thread/physical-conduction controls, electrode physics).
- Result: the conduction signal is explained by physical conduction paths, not living mycelium — the strongest published falsifier methodology in the adjacent-claims space, and the direct ancestor of the FEMS checklist we inherit.

## Appendix — held in repo canon, not re-registered

- **Fernando C, Sojakka S (2003). Pattern Recognition in a Bucket. ECAL 2003, LNCS 2801:588-597.** DOI 10.1007/978-3-540-39432-7_63 · paywalled at Springer; free copies via Semantic Scholar page (semanticscholar.org/paper/af342af4d0e674aef3bced5fd90875c6f2e04abc). Held in repo canon (`docs/ref/MYCELIAL_SCIENCE_MAP.md`): vibrating-bucket water waves sensed by camera as liquid-state-machine reservoir — the original "the reservoir can be anything wet" result.
- Hunt-logged but NOT in the 25-row register (secondary): Adamatzky 2022 psilocybin spiking (PMC9601536, free), Adamatzky 2023 fungal insoles (PMC10030783, free), Adamatzky 2023 Propagation of electrical signals by fungi (Biosystems 233:104933, paywalled; superseded for us by T1.6), Toyota 2018 Science glutamate Ca2+ imaging (paywalled at PMC; science.org delayed-free), Nikolić 2023 organoid RC (PMC10079015, free), Dale/Miller/Stepney 2018 RC characterization framework (arXiv 1810.07135, free — recommended reading for our echo-state test design).

---

(ledger filing table appended below)

---

# LEDGER FILING TABLE — 2026-09-16, writer `canon-fungal-20260916`

Ledger: `watch/inbox/LINKS.jsonl`, 146 → 172 lines (26 new rows, tool `mag.link_library add`, one URL per row). Prior lanes held the SCIENCE but had NOT registered these URLs — all 26 registered fresh, 0 duplicates. The only dupe the tool reports (`dupes`) is a pre-existing X-post pair, not this lane's.

| # | Row | Ledger URL (best free text) | Status |
|---|-----|------------------------------|--------|
| 1 | T1.1 Slayman 1976 | doi.org/10.1016/0005-2736(76)90138-3 | REGISTERED (paywalled, honest) |
| 2 | T1.2 Adamatzky 2018 Towards fungal computer | PMC6227805 | REGISTERED |
| 3 | T1.3 Adamatzky 2022 Language of fungi | PMC8984380 | REGISTERED |
| 4 | T1.4 Adamatzky 2023 moisture response | PMC10069029 | REGISTERED |
| 5 | T1.5 Adamatzky 2026 star array (HELD C19) | arxiv.org/abs/2601.08099 | REGISTERED |
| 6 | T1.6 Adamatzky 2026 Sci Rep linear array (NEW twin) | PMC13212958 | REGISTERED |
| 7 | T1.7 Buffi 2025 iScience FPC (HELD C19) | PMC12483595 | REGISTERED |
| 8 | T1.8 Buffi 2025 FEMS review (HELD C19) | PMC11995700 | REGISTERED |
| 9 | T2.1 Telhan 2026 Sci Rep (HELD C17) | PMC13500807 | REGISTERED |
| 10 | T2.2 LaRocco 2025 PLOS ONE (HELD C17) | PMC12513579 | REGISTERED |
| 11 | T2.3 Adamatzky 2020 Boolean gates | arxiv.org/abs/2002.09680 | REGISTERED |
| 12 | T2.4 Adamatzky 2026 biohybrid substrates (HELD C17) | doi.org/10.1016/j.biosystems.2026.105739 | REGISTERED (paywalled, honest) |
| 13 | T2.5 Kagan 2022 DishBrain | PMC9747182 | REGISTERED |
| 14 | T2.6 Sumi 2023 PNAS | PMC10288593 | REGISTERED |
| 15 | T2.7 Adamatzky 2024 Fungal skin for robots | doi.org/10.1016/j.biosystems.2023.105106 | REGISTERED (preprint free, honest) |
| 16 | T3.1 Nakagaki 2000 | doi.org/10.1038/35035159 | REGISTERED (paywalled, honest) |
| 17 | T3.2 Tero 2010 | doi.org/10.1126/science.1177894 | REGISTERED (paywalled, honest) |
| 18 | T3.3 Shrinking blob TSP | arxiv.org/abs/1303.4969 | REGISTERED |
| 19 | T3.4 Slime Mould Memristors | arxiv.org/abs/1306.3414 | REGISTERED |
| 20 | T3.5 Pershin amoeba memristive learning | arxiv.org/abs/0810.4179 | REGISTERED |
| 21 | T3.6 Volkov 2007 Venus flytrap | PMC2634039 | REGISTERED |
| 22 | T3.7 Bajpai/Levin 2025 Physarum RC | arxiv.org/abs/2510.19976 | REGISTERED |
| 23 | T4.1 Karst 2023 citation bias | doi.org/10.1038/s41559-023-01986-1 | REGISTERED (paywalled, honest) |
| 24 | T4.2 Fungal sensing skin RETRACTED (HELD C17) | PMC7972235 | REGISTERED (retraction note cross-ref'd in note) |
| 25 | T4.3 Thomas+Cooper 2022 contested claim | PMC9673936 | REGISTERED |
| 26 | T4.4 Blatt 2023 challenge | PMC10259323 | REGISTERED |

Appendix row (NOT re-registered): Fernando+Sojakka 2003 bucket — held in repo canon (`docs/ref/MYCELIAL_SCIENCE_MAP.md`); best free route via Semantic Scholar page; Springer paywalled.

Free-text score: 17 of 26 rows registered at open full text (PMC/arXiv); 5 honestly marked paywalled with DOI; 2 paywalled-with-free-preprint; 2 paywalled-but-held.

---

# THE 5 THAT MATTER MOST FOR THE $31 INSTRUMENTED CUBE

1. **Buffi 2025 FEMS review (PMC11995700)** — costs $0 of the budget and decides whether the other $31 buys evidence or artifacts: Faraday cage mandatory, uncolonized-substrate + killed-fungus controls, target band 0.0003-0.1 Hz (1 Hz sampling suffices — spend on isolation, not speed), steel needles read Donnan potentials, reference-electrode placement discipline.
2. **Adamatzky 2026 star array (arXiv 2601.08099)** — the exact characterization instrument to clone: electrode pairs → differential channels (common-mode suppression), 24-bit galvanically isolated logger (Pico ADC-24-class), 1 Hz with per-second averaging, days-long runs, detrend + adaptive per-channel threshold. Its own honest prior (slow, anisotropic, NO global synchrony) is the null the cube must beat.
3. **Adamatzky 2026 Sci Rep linear array (PMC13212958)** — the analysis-and-falsifier template: temporally shuffled spike trains as control + lead-lag propagation measurement. If the cube's "signals" survive shuffling like the mycelium's do, the cube measured something real; if not, it measured noise.
4. **Buffi 2025 iScience FPC (PMC12483595)** — the sensor BOM upgrade: PCB with 8 pairs of 2 mm ENIG gold differential electrodes, 1 cm spacing, mycelium grows onto the card in 3-4 days (no needles), ~17 Hz optional; +1605% PSD vs uninoculated. A dozen cubes collapses into a dozen clonable cards.
5. **Telhan 2026 Sci Rep mycelium chips (PMC13500807 + MIT GitHub)** — the "is it COMPUTING" bar: memory-capacity (MC) methodology, NARMA-10 benchmark, drift spec (<1 mV/h), open code to run unmodified on our rig's traces for direct comparability. Spiking without MC is just electrophysiology.

Runners-up folded into the above: Blatt 2023 + Thomas/Cooper 2022 = the thread-control lesson (a conductor is not a fungus) — inherited via row 1; LaRocco 2025 = the stage-2 DC-sweep memristance method if the cube grows into I-V.

---

[done] 2026-09-16 — S4 lane closed: 26-work tiered canon filed (receipt + ledger), 0 duplicates, 4 held papers verified and extended (Telhan, LaRocco, Buffi x2, Adamatzky x2 incl. NEW twin paper PMC13212958), retraction chain documented, free-text honesty marked per row. No git, no paid APIs; free APIs used: Europe PMC REST, arXiv API, WebSearch/WebFetch; Semantic Scholar rate-limited (429) and unused.
