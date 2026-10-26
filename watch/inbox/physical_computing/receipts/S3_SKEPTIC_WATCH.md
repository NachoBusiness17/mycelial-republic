# S3 SKEPTIC WATCH — Devil's Brief on fungal computing / mycelium electrical sensing

- **Date:** 2026-09-16
- **Lane:** wave S3, physical_computing
- **Operator question on file:** "is this real, am I losing my mind" (mycelium electrical sensing, fungal computing)
- **Mission:** assemble the strongest honest case AGAINST the field so tri-state stays fair. Adversarial by pre-commitment: stage-2 has an automatic retreat trigger, so sharpness is a gift.
- **Method:** WebSearch/WebFetch only (free), no paid APIs, no git. Receipt-first, appended as evidence lands.

## Status: IN PROGRESS — sections appended below as found

---

## §1 THE CRITICS (working list — primary-source checks pending)

**1. Blatt et al. 2024, Functional Ecology — "Does electrical activity in fungi function as a language?"** The central direct rebuttal to Adamatzky's fungal-language claims. Argues on methodological grounds that the presumption of a fungal language is premature and unsupported; questions whether the spiking is even a genuine biological phenomenon vs. artifact. ~15 citations, plant electrophysiology establishment (M.R. Blatt is a serious membrane-biophysics figure, not a blogger). Link: ui.adsabs.harvard.edu/abs/2024FunE...6801326B/abstract

**2. Karst et al. 2023, Nature Ecology & Evolution** (Karst, Hoeksema et al.) — the wood-wide-web correction. Found positive citation bias and inflated claims in the interplant-communication-via-mycorrhizal-networks literature: most reviews' central claims trace to a handful of weak studies; few demonstrate CMNs in natural forests, fewer show meaningful transfer. Not about electrophysiology directly, but it is the field-adjacent case study of how hype outran evidence — and it triggered the "bitter fight among scientists" (Guardian, 2024-07-09).

**3. Linguists vs. "fungal language": Language Log (U. Penn) "Mushroom language?"** — statistical-methodology takedown of Adamatzky 2022 (R. Soc. Open Sci.) treating voltage-train n-grams as "words" and comparing their "lexicon" to human languages. Complaint: distributions compared without the properties that make a lexicon,Zipf-style fits over-interpreted.

**4. Mayne, Roberts, Phillips, Weerasekera, Adamatzky — "Propagation of electrical signals by fungi" (arXiv:2304.10675, 2023).** Damning detail from inside the Adamatzky lab itself: significant spikes were recorded in electrode pairs where **no electrical connection was made with the organism** — i.e., their own controls show the measurement chain can produce "spikes" without mycelium between electrodes. (Verify exact wording from the arXiv text below.)

**5. Science-press skeptical turn:** Undark 2023-05-25 "Where the 'Wood-Wide Web' Narrative Went Wrong" (journalists amplified "speculations of a few scientists"); Guardian 2024 piece by Sophie Yeo; Scientific American on ephemeral fungal networks undermining tree-helping claims.

**6. Adamatzky's own hedging:** "We do not know if there is a direct relationship between spiking patterns in fungi and human speech. Possibly not." The field's loudest advocate concedes the interpretive leap is unproven.

**Shape of the criticism:** (a) is the signal even biological (artifact doubt); (b) even if biological, does it carry information (semantics doubt); (c) even if informative, is "language/cognition/computing" a hype word (framing doubt). Note the critics concede MORE as you go down: (c) is near-universally conceded, (b) is the live fight, (a) is the killer for our rig.

---

## §2 THE ARTIFACT CATALOG (anchored on Buffi et al. 2025, FEMS Microbiol Rev 49:fuaf009)

**Primary source confirmed:** Buffi M, Kelliher JM, Robinson AJ, Gonzalez D, Cailleau G, Macalindong JA, Frau E, Schintke S, Chain PSG, Stanley CE, Künzler M, Bindschedler S, Junier P. "Electrical signaling in fungi: past and present challenges." FEMS Microbiol Rev, 2025-03-21, 49:fuaf009. doi:10.1093/femsre/fuaf009 (PMC11995700). University of Neuchâtel group — they REPLICATED the needle-electrode method themselves, so their checklist is confessional, not polemical.

**Catalog (every non-fungal explanation for a measured signal):**

| # | Artifact | Mechanism | Status in Buffi 2025 |
|---|----------|-----------|----------------------|
| A1 | **Donnan potentials** | Agar/ionic substrate acts as semipermeable membrane; stainless-steel needle electrodes are "prone to the recording of Donnan potentials." Ion-gradients at electrode–gel interfaces generate mV-scale drifts that look like events. | Named explicitly |
| A2 | **Environmental mechanical/EM noise** | In Buffi's own Pleurotus pulmonarius runs, spikes correlated with incubator door opening, people walking nearby, automatic window shades closing — appearing in BOTH fungus and uncolonized control channels. | Named, first-hand |
| A3 | **Passive field potentials from the substrate** | Proximity/extracellular electrodes pick up "movement of ions on a matrix" — e.g., moisture fronts, evaporation, capillary flow. Origin (biological vs physical) indistinguishable at the electrode. | Named |
| A4 | **Non-biological background as "signal"** | Buffi's MEA signal (±50 µV) did NOT change when the fungus was stimulated with a calcium ionophore, nor when it was KILLED with cycloheximide. → the entire signal was noise. | Named, first-hand |
| A5 | **Frequency-band mismatch** | Fungal events claimed at ~0.0003–0.1 Hz; commercial gear (MEA chips) is built for 5–10 Hz–2–3 kHz. Hobbyist rigs have no idea what band they're in; mains hum (50/60 Hz) and its harmonics live in any unfiltered band. | Named (band mismatch); mains hum is our addition — classic bench-electrophysiology confound, line frequency coupling into high-impedance inputs |
| A6 | **No-contact recording** | In Buffi's MEA trials the fungus grew at the air–liquid interface and never touched the electrodes. Whatever was recorded was not fungal. | Named, first-hand |
| A7 | **Electrode polarization / drift** | (Our extension — Buffi implies via Donnan + "difficult to operate correctly") Non-Ag/AgCl or dirty metal electrodes in ionic media build up polarization potentials that wander and reset, producing step "spikes." | Implied |
| A8 | **Movement / growth displacement artifacts** | Hyphae physically displace electrodes (tip pressures ~µN but cumulative); growth over/around the electrode changes contact impedance → baseline steps and transients. Also matrix settling, condensation drips. | Partially (vibrating probes "disturb biological processes"; growth contact issues) |
| A9 | **Microbial contamination, not fungal** | Bacteria in unsterile substrate generate their own bioelectric and redox potentials; a dirty rig measures the community, not the mycelium. | NOT explicitly covered in Buffi 2025 (they discuss fungal viability, not bacterial biofilms) — **gap the checklist missed** |
| A10 | **Galvanic / dissimilar-metal potentials** | Any two different metals touching the moist substrate (e.g., pin + wire + staple) form a battery (tens–hundreds of mV). Temperature swings on that couple = slow "events." | NOT in Buffi — **gap missed** |
| A11 | **EM pickup (mains, switching supplies, RF)** | High-impedance input + unshielded leads = antenna. Mains hum, USB/PSU switching noise, Wi-Fi/bench RF all rectify into low-frequency envelope noise that mimics bursts. | Partially ("Faraday cage in some but not all studies"; called "essential") |
| A12 | **Moisture/temperature transients** | Substrate watering, humidity swings change electrolyte conductivity between electrodes → baseline shifts indistinguishable from slow "spikes" at the 0.001–0.1 Hz band fungal work claims. | Partially (ion movement on matrix) |
| A13 | **Spatial generalization error** | Activity is localized (only trunk hyphae signaled during nematode attack in cited work); a single electrode pair reads one point and the literature narrates the whole mycelium. | Named |

**The most damning artifact demonstration in the adjacent literature:** Thomas & Cooper 2022 (plant-to-plant signal "through" mycorrhizal bridges) was criticized by Blatt et al. 2023 because **a signal still appeared when the mycelium was replaced by a plain thread** — physics of the measurement chain, not biology.

**Buffi 2025's recommended controls (free to steal for our stage 2):**
1. Faraday cage / controlled enclosure — "essential."
2. Uncolonized substrate, identical electrodes, identical geometry — the differential control.
3. Kill control (cycloheximide or equivalent) — signal that survives death is artifact.
4. Positive control (ionophore) — proves the rig CAN see a biological change.
5. Validate extracellular spikes against intracellular recording before trusting them.
6. Don't extrapolate one electrode pair to the whole organism.

---

## §3 RETRACTION / DISPUTE / REPLICATION LEDGER 2020–2026 (verified against primary texts)

**Formal retractions found: NONE (so far).** No Adamatzky fungal-electrophysiology paper is known retracted as of this filing (retraction-watch query pending final confirmation below). The disputes live in critique papers and post-publication commentary, not the retraction ledger.

| Year | Item | What happened | Status |
|------|------|---------------|--------|
| 2021 | Dehshibi & Adamatzky, Biosystems 203:104373, "Electrical activity of fungi: spikes detection and complexity analysis" | Baseline spiking-claim paper in the lineage later criticized wholesale by Blatt et al. 2024. | Unretracted; methodological basis contested |
| 2022 | Adamatzky, R. Soc. Open Sci., "Language of fungi derived from their electrical spiking activity" | Claimed up to ~50-word "lexicon" in voltage-train n-grams. Publicly disputed by linguists (Language Log) and formally rebutted by Blatt et al. 2024. Adamatzky himself: "We do not know if there is a direct relationship… possibly not." | Unretracted; heavily disputed |
| 2022 | Thomas & Cooper (plant–plant signal via mycorrhizal bridge) | Blatt, Draguhn, Taiz & Robinson 2023, Plant Signaling & Behavior 18:2222957, "A challenge to claims for mycorrhizal-transmitted wound signaling" (PMC10259323): per Buffi 2025's account, signal still appeared when mycelium was replaced by a plain thread; proximity-electrode placement and Donnan-potential concerns. → flagship artifact demo for the whole field. (Exact thread-control wording not verified from primary text — fetch timed out; Buffi 2025 is the peer-reviewed secondary source.) | Rebutted in print |
| 2023 | Karst et al., Nat. Ecol. Evol., "Positive citation bias and inflated generated claims in interplant communication via mycorrhizal networks" | Review found CMN claims rest on few weak studies; citation network amplifies unsupported statements. Sparked the public "bitter fight" (Guardian 2024-07-09). | Field correction, ongoing |
| 2023 | Mayne, Roberts, Phillips, Weerasekera, Adamatzky, BioSystems, "Propagation of electrical signals by fungi" (arXiv:2304.10675) | **CORRECTION to our own §1 draft (receipt integrity):** the earlier web-summary claim that spikes occurred "when no electrical connection was made" is wrong — the paper says the OPPOSITE. Verbatim: "No signals were measured in control experiments, indicating that neither the growth medium or interstitial moisture were capable of conducting the input signals between blocks A and B." The "no electrical connection" sentence refers to samples where propagation FAILED (electrode–mycelium contact area insufficient). | In-house "positive"; but see skeptic read below |
| 2023–24 | Phillips et al., Fungal Biol. Biotechnol., "Electrical response of fungi to changing moisture content" | Adamatzky-lab's own concession that moisture changes dominate the signal: humidity/moisture is a first-order input to the recording. | Unretracted |
| 2024 | Blatt et al., Functional Ecology, "Does electrical activity in fungi function as a language?" | The formal rebuttal: methodological grounds; spiking not shown to carry information; nonbiological origins not excluded. | Active critique |
| 2024–25 | Buffi et al., FEMS Microbiol Rev 49:fuaf009 | Independent lab (Neuchâtel) attempted replication of needle-electrode and MEA methods: environmental-noise spikes in fungus AND control; MEA signal (±50 µV) unchanged by ionophore stimulation OR by killing the fungus (cycloheximide); fungus never touched electrodes in MEA setup. Their needle-electrode replication DID show spikes that vanished when the fruiting body was cut (matching uncolonized control) — the one pro-signal datum with a proper negative control. | Partial replication failure; honest self-report |
| 2025–26 | Buffi et al., iScience (2025), PCB-embedded differential electrodes | Same group's constructive rebuild: differential electrodes + uncolonized-substrate control as the corrected method. | Ongoing |

**Skeptic read of Mayne 2023 (the strongest honest attack):** the paper injects ±5 V, 100 Hz–10 kHz square waves into wet colonized blocks and recovers them 10 mm away. Buffi 2025 establishes claimed fungal events live at 0.0003–0.1 Hz. 100 Hz–10 kHz is 6–8 orders of magnitude faster than anything biological in fungi — at those frequencies the colonized block is just a moist ionic dielectric, and "recovered frequency" is passive capacitive/ionic conduction through a heterogeneous medium. The blank-medium control failing to conduct proves the wet colonized block is more conductive than dry compressed medium — a physics result, not a biology result. The paper's own NARX fit (five-term first-order polynomial, validation RRSE 0.748) says the transfer channel is a crude RC filter. Median amplitude not reproducible among replicates. This is the field's flagship "propagation" paper, and it does not demonstrate one fungal action potential.

**Failed replication scorecard (external, independent labs):** Buffi/Neuchâtel = partial failure + one controlled positive. Word-like/lexicon claims (Adamatzky 2022) = zero independent replications found 2022–2026. Everything else positive remains in-house (Unconventional Computing Lab, UWE Bristol) — meaning the entire edifice is one lab's data plus one partial external attempt.

---

## §4 VERDICT — the devil's honest ranking

**Operator's actual question ("is this real, am I losing my mind"):** You are not losing your mind. The voltage you measure is real — something physical is happening at the electrode. What is NOT established, by anyone, anywhere, is that it is fungal information processing. The entire honest field position as of 2026-09: some extracellular events are plausibly biological in origin (best evidence: Buffi's needle-electrode replication where spikes vanished when the fruiting body was cut, matching the uncolonized control; localized trunk-hypha events during nematode attack), the information/language/computing layer has ZERO independent replications and was formally rebutted (Blatt et al. 2024). Separate the three claims and the panic dissolves:
1. "A voltage changes when mycelium is present" — plausibly TRUE in controlled settings.
2. "The voltage changes carry information" — UNPROVEN.
3. "Fungi compute / speak" — HYPE, rebutted on methodological grounds.

**Probability-wise ranking for a $31 hobbyist rig reading "a signal" from living mycelium** (prior, before controls — each rank includes the mechanisms from §2):

| Rank | Explanation | Why it outranks fungal spiking |
|------|-------------|-------------------------------|
| 1 | **EM pickup / mains hum / switching-supply noise** (A5, A11, A2) | Unshielded high-impedance input is an antenna; Buffi's CONTROLLED lab saw spike-events from a door and window shades — in fungus and control channels. A $31 rig has no Faraday cage, no battery isolation. |
| 2 | **Electrode-interface chemistry: polarization, Donnan potentials, galvanic couples** (A1, A7, A10) | Dissimilar metals in ionic substrate make batteries; Donnan potentials are named as the needle-electrode failure mode; produces slow steps that threshold beautifully into "spikes." |
| 3 | **Moisture / temperature / ion-front transients in the substrate** (A3, A12) | The nastiest confound: its time band (minutes) is EXACTLY the claimed fungal band (0.0003–0.1 Hz). Adamatzky's own lab concedes moisture is a first-order driver (Phillips et al. 2023). |
| 4 | **Mechanical disturbance & contact-impedance drift** (A8, A6) | Growth displaces electrodes, condensation changes contact, your own footsteps register. |
| 5 | **Microbial contamination bioelectrics** (A9) | Unsterile substrate is a bacterial electrophysiology rig that never sleeps. |
| 6 | **Genuine fungal extracellular potential change** | Possible — but it must survive 1–5 AND match a pre-registered band AND be stimulus-locked AND disappear in the dead twin. Even then it is a volt, not a word: information content is a separate, unproven claim. |

Honest odds for an uncontrolled $31 rig: artifact:signal ≈ 95:5 or worse. The Buffi experience (±50 µV signal that ignored both stimulation and death) says even careful labs lose to the artifact stack.

**The single control that best separates them: the simultaneous dead twin.** An adjacent channel — identical electrodes, identical substrate (uncolonized), identical electronics, identical environment, recorded at the same instant — is the differential control Buffi 2025 recommends. It subtracts ranks 1–5 all at once. A fungal claim survives only if the live channel differs from its twin in a way that is (a) time-locked to a stimulus, (b) in the pre-registered band, and (c) disappears when the organism is killed or removed. Nothing else on a hobby budget does this much work.

### TOP-3 THREATS TO STAGE-2 VALIDITY + cheapest instrument change that neutralizes each

1. **Threat: environmental EM/mechanical pickup mimics spikes.** (Buffi saw it in a proper lab; our bench is noisier.)
   **Cheapest fix:** a foil-lined steel or biscuit-tin Faraday box, grounded, rig run on battery — ~$10–15. Kills mains hum, RF, and much footfall/vibration coupling in one move.
2. **Threat: electrode-interface chemistry (Donnan/polarization/galvanic) reads as events.**
   **Cheapest fix:** true differential input with a matched pair of Ag/AgCl electrodes (chloridize silver wire in bleach — pennies) + the dead-twin channel. Common-mode rejection removes substrate-chemistry noise shared by both electrodes; ~$5–10 total.
3. **Threat: analysis overfit — thresholding noise into "spikes" and post-hoc pattern language.**
   **Cheapest fix:** pre-register the spike definition (amplitude threshold, dead time, band) and a known-input calibration (inject a 1 Hz known-amplitude signal via resistor + phone signal-generator app, verify the chain reproduces it; add a $5 DHT22 to log temperature/humidity for regression). Cost ≈ $6. A rig that has never seen a known input has no idea what it is measuring.

**Bottom line for the pre-commitment:** stage 2 should be designed so that "we detected something" is the LEAST interesting possible outcome — only a live-vs-twin, stimulus-locked, kill-switchable difference is worth reporting. If stage 2 can't clear the dead twin, retreat is the correct and expected move, exactly as pre-committed.

---

## Sources (all fetched/searched 2026-09-16)

- Buffi et al. 2025, FEMS Microbiol Rev 49:fuaf009 (PMC11995700) — artifact checklist, own-replication failures, controls: https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/
- Mayne et al. 2023, BioSystems (arXiv:2304.10675) — full text read; control result and variability caveats: https://arxiv.org/abs/2304.10675
- Blatt et al. 2024, Functional Ecology — "Does electrical activity in fungi function as a language?": https://ui.adsabs.harvard.edu/abs/2024FunE...6801326B/abstract
- Blatt, Draguhn, Taiz & Robinson 2023, Plant Signaling & Behavior 18:2222957 (PMC10259323) — Thomas & Cooper rebuttal: https://pmc.ncbi.nlm.nih.gov/articles/PMC10259323/
- Karst et al. 2023, Nature Ecology & Evolution — positive citation bias in CMN claims (context: Undark 2023-05-25; Guardian 2024-07-09 Sophie Yeo)
- Language Log (U. Penn), "Mushroom language?" — linguistics critique of Adamatzky 2022: https://languagelog.ldc.upenn.edu/nll/?p=62109
- Adamatzky 2022, R. Soc. Open Sci., "Language of fungi…" + Guardian coverage with Adamatzky's own hedge
- Retraction Watch searches (site-restricted and broad, 2026-09-16): no retractions of Adamatzky fungal-electrophysiology work found
- Buffi et al. 2025, iScience — PCB differential-electrode methods paper: https://www.sciencedirect.com/science/article/pii/S2589004225017456

**Receipt integrity note:** one initial web-search summary (claimed Mayne 2023 recorded spikes on unconnected electrodes) was checked against the full text and found WRONG (inverted); corrected in §3. Two search-engine summaries disagreed on the Mayne control; the arXiv full text is authoritative here. Trust bytes, not reports — verified.

— S3 skeptic watch, closed 2026-09-16. Tri-state stays fair: the fungi are not proven innocent; the rig is definitely not proof of guilt.
