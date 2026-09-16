# G-A — SIGNAL MAGNITUDE GAP: nV–µV vs >100 mV (receipt, wave-lane)

- **Gap:** G-A — the field's own literature contradicts itself on fungal signal magnitude.
- **Camps:** FEMS/Buffi camp: nV–µV extracellular signals. Adamatzky camp: mV-scale spikes reported (his own papers: 0.03–2.1 mV typical, ≤38 mV for burn stimuli; the >100 mV excursions live in the needle-rig fruiting-body *replication* (−300 to +50 mV) and in classic *intracellular* work (50–100 mV)).
- **Verdict sought:** our cube's first measurement must adjudicate which regime we are in.
- **Lane:** wave / receipt-first / no git / no paid APIs / Europe PMC + CrossRef (free) full-text method mining.
- **Status:** DONE — adjudication plan filed below (regime-decision table + protocol-steal).

## Log

- [t0] Receipt opened before any research action.
- [t1] Rig specs confirmed from `CUBE1_SHOPPING_LIST.md`: ESP32 + 2× ADS1115 (16-bit, differential, PGA×16 = ±0.256 V FS, 7.8 µV/LSB), Ag/AgCl ECG pads, foil Faraday box + battery (skeptic's rider), dead-twin control tub. Aligned with `C17_CUBE_INSTRUMENT_PLAN.md` (8–16 SPS, 72 h stage-0, spike-count > 3×stage-0-σ feature).
- [t2] Both camps' methods mined from full text (Europe PMC fullTextXML; NCBI E-utilities). Downloaded and grepped by byte: Buffi FEMS Microbiol Rev 2025 (PMC11995700), Buffi iScience 2025 (PMC12483595), Adamatzky Sci Rep 2018 P. djamor (PMC5959856), Adamatzky RSOS 2022 (PMC8984380), Adamatzky-camp Sci Rep 2026 oyster substrate (PMC13212958), S. commune multiscalar 2023 (PMC10406843). Blatt 2024 citation resolved via the FEMS review's reference list.
- [t3] Answers + regime-decision table + protocol-steal filed. Receipt closed.

---

## 1. The two camps, rig by rig (verified from full text, not summaries)

### Adamatzky camp (mV "spikes")

| Paper | Electrodes | Amplifier / ADC | Shielding | Sampling | Species / geometry | Reported amplitude |
|---|---|---|---|---|---|---|
| Adamatzky 2018, "On spiking behaviour of oyster fungi *Pleurotus djamor*", Sci Rep 8:7873, doi:10.1038/s41598-018-26007-1 (PMC5959856) | SPES MEDICA **subdermal needles** (stainless), twisted cable; one in stalk, reference in cap translocation zone, **3–5 cm apart**; tissue resistance measured **1.5 MΩ** cap–stalk, **2 MΩ** fruit-to-fruit (Fluke 8846A) | **Pico ADC-24**: differential, galvanically isolated, 24-bit, gain error 0.1%, **input impedance 2 MΩ differential**, offset error 36 µV in ±1250 mV range | **None** (cardboard box, room air) | **1 sample/s saved** = average of up to 600 internal readings/s (600:1 averaging) | *P. djamor* fruiting bodies, 4–6 bodies per cluster, 2–3 days | H-spikes **0.88 mV** (σ 0.14), L-spikes **1.3 mV** (σ 0.21), period 2.6/14 min; burn response depolarizes **+38.2 mV in 18 s**; water response 6.1 mV; "slow (hours) drift of base potential" acknowledged |
| Adamatzky 2022, "Language of fungi derived from their electrical spiking activity", R Soc Open Sci 9:211926, doi:10.1098/rsos.211926 (PMC8984380) | Same subdermal needles | Same ADC-24 family, **acquisition range 78 mV** | None | 1 Hz (600:1 average) | *O. nidiformis*, *F. velutipes*, *S. commune*, *C. militaris* | spikes "duration 1 to **21 h** and an amplitude from **0.03 to 2.1 mV**" |
| Adamatzky-lab lineage, "Propagation of electrical spike trains in substrates colonised by oyster fungi", Sci Rep (2026), PMC13212958 | SPES MEDICA subdermal needles, **8 differential channels**, 1 cm within pair, 2 cm between channels, linear array | ±1250 mV range logger | None stated | **1 Hz**, ~15 days | *P. ostreatus* colonized wood shavings (our species!) | spikes **0.2–1.4 mV**, median 0.6 mV, mean 0.7 mV; propagation delays across array claimed |

Note: Adamatzky himself writes in the 2018 paper: "Amplitudes of spikes measured were very low comparing to amplitudes reported in [Slayman 1976; Olsson & Hansson 1995] because the works cited used **intra-cellular** recording while we used **extra-cellular**." The genuinely >100 mV numbers come from elsewhere: (a) the Buffi lab's *replication of this exact method* on *P. pulmonarius* fruiting bodies — spikes "ranging from above 50 to up to **−300 mV**"; (b) classic intracellular glass-microelectrode work: Slayman, Long & Gradmann 1976 (*Neurospora*, damped oscillations **50–100 mV**, quasi-sinusoidal 10–20 mV), Olsson & Hansson 1995 (resting −70 to −100 mV, spikes **5–50 mV**, 0.5–5 Hz).

### FEMS/Buffi camp (nV–µV)

| Paper | Electrodes | Amplifier / ADC | Shielding | Sampling | Result |
|---|---|---|---|---|---|
| Buffi et al. 2025, "Electrical signaling in fungi: past and present challenges", FEMS Microbiol Rev 49:fuaf009, doi:10.1093/femsre/fuaf009 (PMC11995700) | Replication of Adamatzky's exact rig: ADC-20 + Neurodart subdermal needles, twisted cables; *plus* their survey of the field | Same ADC instrument as Adamatzky | Open incubator | — | Fruit-body spikes **+50 to −300 mV**; but signal **matched uncolonized-substrate control** after detaching the fructification; "opening of the incubator door, presence of people walking… automatic closing of window shades" produced spikes **in both live and control**. Anchors the nV–µV claim: hyphal currents "either of low intensity (µA cm⁻²) (Gow & Morris 1995) or **low voltage (nV to µV)**" citing Olsson & Hansson 1995 |
| Buffi et al. 2025, "Detection of electrical signals in fungal mycelia in response to external stimuli", iScience 28:113484, doi:10.1016/j.isci.2025.113484 (PMC12483595) | **PCB with embedded differential electrodes** (2 mm electrodes) on *F. oxysporum* mycelium | **Same ADC-24 instrument** as Adamatzky's rig | **Faraday cage + shielded cables + humidity-stabilized incubation chamber** | ~17 Hz (60 ms conversion) | "The addition of the Faraday cage reduced the effect of external noise and artifacts for accurate measurements of voltage changes **in the order of microvolts**. In previous studies lacking a Faraday cage **and employing the same recording instrument**, the presence of people walking near the incubator or even the automatic closing of window shades affected voltage measurements." Warns agar media form "abiotic electrochemical gradients… mistakenly interpreted as true electrical signals" |
| Blatt, Pullum, Draguhn et al. 2024, "Does electrical activity in fungi function as a language?", Fungal Ecology 68:101326, doi:10.1016/j.funeco.2023.101326 | — | — | — | — | The formal critique: "use of **stainless-steel needles is prone to the recording of Donnan potentials**"; "part of the electrical activity likely originates from voltage fluctuations that do not have a biological origin"; extracellular surface electrodes reflect "synchronous behavior of multiple cells", not transmembrane action potentials |
| Blatt, Draguhn, Taiz, Robinson 2023, "A challenge to claims for mycorrhizal-transmitted wound signaling", Plant Signal Behav 18, doi:10.1080/15592324.2023.2222957 | — | — | — | — | Companion critique: a *thread* replacing mycelium still "recorded" signal → physical, not biological phenomenon; agar + ionic media → Donnan potentials |
| Olsson & Hansson 1995, "Action potential-like activity found in fungal mycelia is sensitive to stimulation", Naturwissenschaften 82:30–31, doi:10.1007/BF01167867 | Intracellular microelectrode, reference in agar | — | — | — | The nV–µV camp's physiological anchor for *extracellular* magnitudes (their own intracellular numbers were 5–50 mV) |

## 2. SOCRATIC ANSWERS

### Q1 — What exactly differs between the rigs?

Five differences carry the 5-orders-of-magnitude disagreement:

1. **Electrode chemistry.** Stainless-steel subdermal needles (Adamatzky camp; polarizable, Donnan-potential-prone in ionic agar/substrate) vs PCB-embedded differential electrodes in a humidity-stabilized chamber (Buffi iScience) and vs the critique's demand for non-polarizable interfaces (Ag/AgCl). Donnan potentials from stainless needles in semi-permeable agar are mV-scale by nature — Blatt et al. name this directly.
2. **Impedance matching.** This is the quantitative nail: Adamatzky 2018 reports tissue resistance of **1.5 MΩ** (cap–stalk) / **2 MΩ** (fruit–fruit) while his own ADC-24 input impedance is **2 MΩ differential**. Source impedance ≈ input impedance → the recording is a near-50% voltage divider under the best conditions, and *any* environmental or electrochemical EMF behind a MΩ source impedance (mains pickup, motion of the cable, moisture shifts) appears at nearly full scale in the reading, unattenuated and unguarded. A proper extracellular bioamp input is ≥100 MΩ–GΩ so the amplifier, not the electrode interface, defines the node voltage. The FEMS review flags exactly this class of failure ("voltage fluctuations that do not have a biological origin").
3. **Shielding / environment.** Adamatzky: cardboard box in room air, no cage. Buffi iScience: Faraday cage + shielded cables + sealed humid chamber — and demonstrates the cage is *the* variable that collapses readings to the µV scale on the *same instrument*. The FEMS replication shows door-openings, pedestrians, and motorized blinds imprinting mV spikes on live and dead channels alike.
4. **Sampling/averaging.** 1 Hz saved from a 600:1 internal average (Adamatzky) low-passes and aliases everything below 300 Hz — mains hum, fluorescent ballasts, cable microphonics — directly into the "slow spike" band (their spikes last minutes to 21 h). Buffi iScience: 17 Hz, no averaging trap; STFT band analysis instead of threshold spike-counting.
5. **Geometry and invasiveness.** Needles stabbed through stalk and cap (wounded tissue, 3–5 cm apart, translocation zone) vs electrodes *on/in* undisturbed mycelium on a PCB. Plus the transmembrane-vs-extracellular confusion the review highlights: intracellular APs genuinely are 5–100 mV (Slayman 1976; Olsson & Hansson 1995); extracellular field potentials of distant hyphae are not.

### Q2 — Which difference is most likely THE cause?

**The absence of a Faraday cage acting on a MΩ-impedance polarizable-electrode front end — with the electrode chemistry as the substrate the cage protects.** The field has effectively already run the controlled experiment for us: Buffi's iScience study used the **identical ADC-24 logger** as the Adamatzky rig and changed the environment (cage + shielded cable + stable humidity) and the electrode interface (PCB differential). Result: mV "spikes" → µV fluctuations, and every room event (door, people, blinds) that had imprinted mV excursions disappeared from the record. Meanwhile the FEMS replication with the *original* needle method reproduced the −300 to +50 mV excursions *and* showed they are not fungus-specific (dead substrate and detached fructifications match). Second-place culprit: the stainless-needle Donnan interface, which manufactures slow mV potentials even without EM pickup (Blatt 2024); third: the 2 MΩ input impedance that lets all of the above reach the digitizer undivided. Our own skeptic's rider ("EM pickup — the #1 false signal", foil box + battery) independently predicted this ordering.

### Q3 — The single measurement that names our regime

**One simultaneous, side-by-side differential recording session: live tub vs dead twin, identical electrodes, same room, same clock — run at full gain with a mid-session cage-off/cage-on A/B.** (Stage 0 already mandates the dead twin; the adjudication is just reading its first hours correctly.) It settles the question because the regime is *defined* by where the excursions sit and whether the dead twin co-sees them:

- Excursion amplitude ≥ ~1 mV → outside any defended µV regime → artifact regime unless live-only.
- Presence in the dead twin or correlation with logged room events → artifact by definition (Buffi replication's exact criterion).
- Live-minus-dead structure confined to 1–100 µV → FEMS regime.
- Rail-saturation at PGA×16 (±256 mV FS) → mV regime flagged by a single sample, no analysis needed.

The cage A/B quantifies our own EM-pickup amplitude in situ, so artifact-vs-biological is measured, not assumed. Session length must respect the literature: spikes as long as **21 h** (RSOS 2022) mean minutes-long pilot runs cannot adjudicate anything — the decision window is hours (see steal).

## 3. REGIME-DECISION TABLE (day-one verdict, from the first ≥4 h of stage-0 logging)

| # | Observation (live vs dead twin, PGA×16, cage A/B) | Named regime | Verdict on camps | Action |
|---|---|---|---|---|
| R1 | Excursions ≥1 mV **or** ADC rails (|V| ≥ ~230 mV) present in **both** tubs, or vanish when cage closes, or correlate with operator/room log | **ARTIFACT REGIME** | Blatt/Buffi verdict confirmed: mV camp confounded | Cage+battery become permanent; analysis restricted to µV-band; no spike claims until R1 is silent for a full 72 h |
| R2 | Excursions ≥1 mV **live-only**, dead twin flat, survives cage-closed and battery | **MILLIVOLT REGIME** | Adamatzky camp validated on our bench — publishable delta vs Buffi | Raise SPS to 860, steal the 8-channel linear-array geometry (1 cm/2 cm) for propagation delays, pre-register n≥3 replication |
| R3 | Live−dead difference confined to **1–100 µV** band, no mV excursions anywhere | **MICROVOLT REGIME** | FEMS camp confirmed | Drop mV thresholds; adopt µV features (spike count >3×σ, C17) + STFT bands (iScience steal); run 24–72 h windows |
| R4 | Both channels <10 µV, no structure for the whole window | **UNRESOLVED — duration-bound** | Neither named yet | Extend to full 72 h stage-0 log (spike durations 1–21 h in RSOS 2022); if still flat, rig is clean-but-deaf: stage-1 gate runs on µV σ only |

## 4. THE PROTOCOL-STEAL — stage-0 "name the regime" procedure (drops into the C17 plan)

**Channels.** 2 differential pairs: ADS1115 #1 (addr 0x48) A0−A1 = live tub, ADS1115 #2 (addr 0x49) A2−A3 = dead twin. Ag/AgCl ECG gel pads (already in the BOM — non-polarizable, the one spec both camps agree on). Pair geometry stolen from the Sci Rep 2026 oyster array: **~1 cm within a pair, pairs ≥5 cm apart**, pads flat against substrate surface, identical depth and orientation in both tubs. Symmetric lead dress (twisted pair runs, same length).

**Gain.** PGA ×16 → ±0.256 V FS, **7.8 µV/LSB** (per C17; below even Adamatzky's 78 mV acquisition floor, 4 decades above the nV camp's floor). Log a saturation flag when |raw| ≥ 0.9×FS — a rail *is* a regime verdict (R1/R2 discriminator).

**Rate.** 8–16 SPS per C17. Deliberately above both camps: exposes 45–65 Hz mains as its own band instead of folding it into slow spikes via 600:1 averaging (the Adamatzky sampling trap). Bands to report every window: 0.01–1 Hz (fungal slow band), 45–65 Hz (mains), 1–8 Hz (cable/motion microphonics).

**Duration.** Adjudication window = **first 4 h minimum** of the 72 h stage-0 run, plus one **30 min cage-off / 30 min cage-on A/B** inside it. Do not call the floor from minutes-long records: published spike durations run to 21 h.

**Controls (five, all cheap, all stolen from the camps' own failure modes):**
1. **Shorted-input 10 min** at head and tail of the session (both channels strapped) → instrument noise floor + LSB sanity.
2. **Dead twin simultaneously, same room** (never sequential) → the Buffi replication's criterion: any event seen in both tubs is environment, not fungus.
3. **Cage A/B** → measures our EM-pickup amplitude directly; the one variable iScience isolated with the same instrument.
4. **Operator event log** (timestamp every door/hand/movement near the bench) → correlates R1-class excursions with causes; stolen from the door/blinds artifact observations.
5. **Drift metric** (slow monotonic offset per hour, per channel) → the Donnan/polarization signature of a dying electrode interface (Blatt 2024); separate column, never merged into "signal".

**Day-one analysis.** Per channel: max excursion, rail count, band RMS × 3, spike counts at 20 µV / 100 µV / 500 µV / 1 mV, live-minus-dead event coherence, drift rate. Read the top row of the regime-decision table that matches → name the regime → proceed or harden. Hash-chained ledger per C17; flatlined channel files EVIDENCE_DEAD against itself.

## 5. Sources (all free full text; mined by byte, not summary)

- Buffi M, et al. FEMS Microbiol Rev 49:fuaf009 (2025). doi:10.1093/femsre/fuaf009 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/
- Buffi M, et al. iScience 28:113484 (2025). doi:10.1016/j.isci.2025.113484 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12483595/
- Blatt MR, Pullum GK, Draguhn A, et al. Fungal Ecology 68:101326 (2024). doi:10.1016/j.funeco.2023.101326
- Blatt MR, Draguhn A, Taiz L, Robinson DG. Plant Signal Behav 18 (2023). doi:10.1080/15592324.2023.2222957
- Adamatzky A. "On spiking behaviour of oyster fungi *Pleurotus djamor*." Sci Rep 8:7873 (2018). doi:10.1038/s41598-018-26007-1 · https://pmc.ncbi.nlm.nih.gov/articles/PMC5959856/
- Adamatzky A. "Language of fungi derived from their electrical spiking activity." R Soc Open Sci 9:211926 (2022). doi:10.1098/rsos.211926 · https://pmc.ncbi.nlm.nih.gov/articles/PMC8984380/
- Adamatzky-lab lineage. "Propagation of electrical spike trains in substrates colonised by oyster fungi." Sci Rep (2026). PMC13212958
- Adamatzky A. "Multiscalar electrical spiking in *Schizophyllum commune*." Sci Rep 13 (2023). PMC10406843
- Olsson S, Hansson BS. Naturwissenschaften 82:30–31 (1995). doi:10.1007/BF01167867
- Slayman CL, Long WS, Gradmann D. Biochim Biophys Acta 426:732–744 (1976) [intracellular 50–100 mV context, via Adamatzky 2018 intro]

**Caveats:** "Towards fungal computer" (Interface Focus 2018) full text is publisher-blocked from XML download; its rig is characterized here via the FEMS review's description + the identical ADC-24/needle setup verified in Adamatzky 2018 (Sci Rep). Adamatzky's own reported amplitudes top out at ~2.1 mV (38 mV for open-flame burn); the task's ">100 mV" figure is attributable to the needle-rig fruiting-body replication (−300 mV, FEMS review Fig. 2H) and to intracellular classic work — the receipt states this precisely so the cube's verdict is against the *right* numbers.
