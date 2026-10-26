# CONCERT002_FIBER_25 — receipt

**Date:** 2026-09-16 · **Lane:** physical_computing / CONCERT 002 (fiber-optics-into-mycelium 25-wide battery)
**Wave-lane law:** receipt FIRST (this file, written before any lane call), append as you go · no git · $0 (free lanes + free-window stealth if alive) · probe-first · degrade gracefully.
**Interpreter:** `.venv\Scripts\python.exe` only (AGENTS.md).
**Driver:** `watch/inbox/wave_20260916/c2_fiber25_20260916.py` (d23 driver pattern: probe → run → cooldown retry → summarize; append-only raw.jsonl as rows land; SSRF allowlist + resolved-IP guard; failures preserved as rows).
**Registry (unmodified):** `mag/research_fanout.py` `LANES / _env / _now`.
**Artifacts tape:** `watch/inbox/physical_computing/receipts/concert002_fiber25/` (`raw.jsonl`, `probe.json`, `summary.json`).

---

## Mission (operator, verbatim)

> "go 25 wide, scale the ask via our gap analysis" — fire a 25-segment battery through
> mag/research_fanout (driver pattern: wave_20260916/d23_salon50_night_20260916.py) on the NEW
> scaled ask — fiber optics fed into the mycelial network after complete colonization, as optical
> I/O for the cube program.

NEW HYPOTHESIS under test: after full colonization, optical fibers inserted into the block provide
light-based WRITE (pulses), READ (photometry/transmission), and routing — the Dirac layer's optical
analog.

## Method (frozen before firing)

- **Probe-first:** one READY ping per candidate lane. Candidate carriers = registry LANES minus
  reserves (below). Stealth free-window lane `or-union-alpha` included (window ends ~2026-09-23 —
  alive until probe says otherwise, per U8: non-streaming, timeout ≥180 s).
- **Reserve lane:** `zai-lite` is held OUT of the carrier rotation (law 15: burst lane, never a
  default carrier) and used only if the fold would otherwise leave a family empty. $0 Lite credits
  is the goal.
- **Rotation table (D22 adopted):** `groq-qwen` capped at `max_tokens=780` (OTPM gate, D22 pass 2);
  `mistral-small` expected 429 (probe decides, never hand-waved); `or-nemotron` slow (~37 s READY)
  → timeout 300 s. Paid-wall signature abort (401/402/billing keywords) preserved from d23.
- **Fire:** all 25 segments, round-robin over live carriers (25/N per lane — 5 per lane when 5 live),
  temperature 0.2 fixed (research battery, not a salon), `api_seed = 2026091600 + segment index`,
  `max_tokens=2600` default. Rows appended to raw.jsonl AS THEY LAND.
- **Retry:** pass 2 after 60 s cooldown, same segment→lane map (LANES order preserved), attempt=2,
  `max_tokens=4000` headroom for reasoning channels. Append-only.
- **Fold:** latest-attempt-wins per segment; per-family Rashomon fold (each witness answer stands
  alone, NO averaging); pairwise Jaccard diversity per family (d23 instrument).

## CONTEXT block embedded in every segment prompt (≤200 tokens)

> CONTEXT (shared): The cube is an instrumented block of living mycelium (oyster/Pleurotus on
> sawdust substrate); electrodes read its electrical spiking. Program ladder: sensing → memory →
> compute. NEW HYPOTHESIS under test: after complete colonization, optical fibers inserted into
> the block give light-based I/O — WRITE (light pulses into the network), READ (photometry of
> transmission/return light), and routing between points — the optical analog of the cube's
> electrode layer. Budget is hobby tier (~$40 add-on). Answer as an independent expert witness:
> give concrete mechanisms, numbers, and materials where you can; state uncertainty honestly
> instead of inventing numbers.

## SYSTEM prompt (frozen)

> You are an independent witness in a multi-model research salon on a mycelium-hardware experiment
> (fiber optics as optical I/O into living mycelium). Answer from your own knowledge and judgment.
> Take the position you actually believe; do not fence-sit. Give concrete, checkable specifics —
> mechanisms, numbers, materials, citations you are confident of. If unsure, say which part is
> uncertain. No preamble. Hard limit: 160 words.

## THE 25 SEGMENTS (5 families × 5) — registered BEFORE firing

Family A — OPTICAL PHYSICS (OP):
- OP1: Does living mycelium transmit or guide light? Is there credible evidence of waveguiding along individual hyphae, or does the tissue act as a diffuser/scatterer? State the strongest published evidence you know.
- OP2: What reduced scattering coefficient (mm^-1) would you expect for dense living mycelium at visible wavelengths (~500-650 nm), given tissue optics? What does that imply for how far a beam survives inside a colonized block?
- OP3: Does living fungal mycelium autofluoresce under visible/UV excitation? Which fluorophores (e.g., chitin, NADH, flavins), what excitation/emission bands, and could autofluorescence serve as an optical READ signal?
- OP4: Do fungi show phototropic or photo-spiking responses — measurable electrical or growth responses to light pulses? What timescale and light dose would you expect — can light act as a stimulus equivalent to an electrode pulse?
- OP5: What light intensity/dose risks damaging living mycelium (thermal or photochemical) at fiber-tip powers? Estimate a safe pulse regime for a hobby source (650 nm or 520 nm) inside a colonized block.

Family B — ENGINEERING (EN):
- EN1: For a hobby-tier (~$40) build: PMMA plastic optical fiber vs glass/silica fiber into living mycelium — which and why? Consider cost, sterilization tolerance, flexibility, coupling ease.
- EN2: Design a sterile optical feedthrough into an already-colonized fruiting tub (still-air-box constraints): how do you insert fiber after colonization without contamination? Ports, filters, adhesives, heat?
- EN3: Does fiber insertion traumatize a fully colonized mycelial block, and should you wait ~2 weeks after insertion before recording? What wound response (regrowth, melanization, contamination) would you expect?
- EN4: What coupling/alignment tolerance does a hobby build need between PMMA fiber (1 mm core) and LED/photodiode/laser? How much does misalignment and bending cost in coupling loss (numbers)?
- EN5: What is the practical maximum fiber count for a $40 array into one tub, and how should fibers be arranged (grid, co-located with electrodes, 1:1 mapping)? Cheap mux/demux options?

Family C — MEMORY (ME):
- ME1: Could a light pulse through an inserted fiber WRITE state into a mycelial network the way an electrode pulse can (cross-modality equivalence)? What mechanism would carry optical excitation into the electrical/spiking state?
- ME2: If optical energy changes mycelial state (photobleaching, local heating, photochemical products), how long would that state persist? Is there any plausible optical memory trace, and what are the photobleaching limits?
- ME3: Design a read-after-write fidelity test for the optical channel: write with fiber A (pulse), read with fiber B (transmission/photometry). What signal change counts as a successful write, and what SNR/drift pitfalls?
- ME4: Can writes be addressed by fiber position — is the write local to the illuminated volume, or does the network integrate globally? What spatial resolution (mm) is plausible through a scattering block?
- ME5: Estimate the information capacity per fiber channel (bits): given photometric/electrical readout bandwidth (~Hz) and reliably distinguishable states, what order of magnitude is defensible, and why?

Family D — COMPUTE (CO):
- CO1: For an optical-hyphal hybrid (light in fibers, computation in the network), what routing architecture is coherent? Is there any mechanism by which the network could route light between fibers, or must routing be fiber-side?
- CO2: Compare latency: optical I/O (fiber + photodiode, ~ns) vs mycelial electrical signaling (~mm/s-cm/s) vs observed spike timescales. Where is the real bottleneck for any compute claim?
- CO3: Can multiple optical channels (different fibers, WDM colors) coexist through a scattering mycelial block? Quantify expected crosstalk given speckle/diffusion — is multi-channel coherent I/O plausible at hobby tier?
- CO4: Are there plausible hybrid electro-optic gates in mycelium — light modulating electrical response, or electrical state modulating light transmission (electro-absorption, swelling)? Rank by physical plausibility; name analogs in other media.
- CO5: What is the honest scaling path and wall for optical I/O on mycelial compute (channels × states × speed) vs electrode arrays? At what point does the substrate stop mattering and the optoelectronics dominate?

Family E — PROGRAM (PR):
- PR1: What can an optical fiber layer do for the cube that electrodes cannot? Identify the ONE unique capability (spatially resolved read/write? no electrochemical artifact? telemetry through the wall?) and argue it.
- PR2: Design the falsifier for a $40 optical add-on on the instrumented cube: what pre-registered measurement distinguishes 'optical channel carries real signal' from artifact (heating, ambient light, photodiode drift)? State the null.
- PR3: Break down a $40 budget for the optical add-on: sources, PMMA fiber, photodiodes, feedthrough hardware — realistic unit costs and where the build fails first at $0 vs $40 vs $100.
- PR4 (derived to fill the 5×5 grid; mission listed 3 PROGRAM asks): Specify the v1 protocol: what to log (pulse schedule, photodiode trace, electrode spikes, temperature), for how long, and what data schema makes the result falsifiable and reusable?
- PR5 (derived to fill the 5×5 grid): Decision gate: after the $40 add-on runs, what result promotes the optical layer into the program ladder (sensing → memory → compute) as a real channel, and what result kills it?

## Probe log (append as you go)

- UTC 2026-09-16, one READY ping per candidate carrier (`probe.json` holds the full rows).
- **Reserve held out before any call:** `zai-lite` (law 15) — not probed, not called. Paid-wall
  pre-filter list empty (zai-47 retired from registry).
- **LIVE (9):** groq-qwen 384 ms · groq-oss 390 ms · groq-oss20 1417 ms · cerebras-oss 332 ms ·
  cerebras-qwen 245 ms · mistral-min8 8510 ms (cold start; answer sampled chatty but ok) ·
  **or-union-alpha 19258 ms — stealth free window ALIVE** · or-nemotron 25821 ms (slow as D22 said) ·
  or-ling3 2891 ms.
- **DEAD (2):** mistral-small HTTP 429 code 1300 (D22 predicted — never hand-waved, re-measured);
  or-glm52 HTTP 429 (provider rate-limited upstream).
- Round-robin: 25 segments over 9 live lanes → 7 lanes × 3 segments, 2 lanes × 2 segments
  (mission's "5 per lane" assumed 5 live; the round-robin law generalizes).

## Fire log (append as you go)

- **Pass 1 fired** — question_digest `380e2df78bd7eb4b`, 25/25 segments attempted, round-robin map
  frozen above (driver stdout; identical map reproduced in raw.jsonl rows). **21/25 answered.**
- Failed (preserved as rows, `empty_content` = reasoning channel burned the content budget):
  - OP5 → cerebras-qwen (3014 ms)
  - EN4 → or-ling3 (10782 ms)
  - ME4 → cerebras-qwen (1936 ms)
  - PR3 → cerebras-qwen (1841 ms)
- Lane notes: or-nematron slow lane confirmed (CO2 took 266 s — kept, timeout 300 held);
  or-union-alpha answered all 3 of its segments (EN2 69 s, CO1 31 s, PR5 48 s) — stealth window
  productive; groq-qwen's D22 max_tokens=780 cap held (3/3 answered, no OTPM 429).
- Pairwise Jaccard (pass 1): A 0.131 · B 0.092 · C 0.138 · D 0.111 · E 0.117 — low overlap,
  witnesses genuinely diverge (Rashomon condition met; no averaging will be applied).

## Retry log (append as you go)

- **Pass 2 fired** after 60 s cooldown, same segment→lane map, `max_tokens=4000` headroom:
  EN4 → or-ling3 **RECOVERED** · ME4 → cerebras-qwen **RECOVERED** · PR3 → cerebras-qwen
  **RECOVERED** · OP5 → cerebras-qwen **STILL empty_content (2nd failure — preserved)**.
- **Final: 24/25 answered, 1 failed.** OP5 (damage threshold) dead twice on cerebras-qwen's
  reasoning channel.
- Reserve ruling per frozen method: `zai-lite` fires only if a FAMILY would be empty; family A
  holds 4/5, so the reserve was **not** used — 0 Lite credits spent. OP5 goes to the fold as a
  recorded hole, not a silence.
- Final Jaccard: A 0.131 · B 0.095 · C 0.128 · D 0.111 · E 0.112.

## Fold — 25 answers by family (Rashomon, no averaging)

Raw tape: `concert002_fiber25/raw.jsonl` (29 rows: 25 pass-1 + 4 pass-2) · per-answer text:
`concert002_fiber25/answers.md`. Each witness stands alone; where witnesses disagree, the
disagreement is recorded, not averaged.

### Family A — OPTICAL PHYSICS (4/5 answered; OP5 failed twice, preserved)

- **OP1 (groq-qwen):** no credible waveguiding evidence; hyphae 3–10 µm, wall/cytoplasm index
  contrast (~1.4–1.5 vs ~1.33–1.38) insufficient for stable TIR; mats are strong scattering media;
  "you will measure bulk attenuation and scattering noise, not signal integrity."
- **OP2 (groq-oss):** μs′ ≈ 15 ± 5 mm⁻¹ at 500–650 nm; transport mfp ≈ 70 µm; ballistic component
  dead within ~10 µm; usable signal = diffuse photometry only.
- **OP3 (groq-oss20):** autofluorescence real — NADH 340–360/460–480 nm, flavins 450–470/520–530,
  chitin minor; weak (needs APD + spectral filtering); bleaches over hours under repeated excitation.
- **OP4 (cerebras-oss):** blue WC-1/2 receptors functional in Pleurotus; claims light pulses evoke
  0.8–2 mV depolarizations (0.5–2 s) — **specific numbers/citation UNVERIFIED** (see claims table);
  growth phototropism on minutes–hours timescale.
- **OP5:** FAILED (2× empty_content on cerebras-qwen) — damage-threshold segment unanswered by the
  fleet; fold inherits the conservative prior: keep pulse power ≤5 mW (PR5's own kill line) until
  OP5 is re-asked.

**Family shape:** the block is a diffuser, not a waveguide; READ via diffuse photometry +
autofluorescence is physically real; WRITE via blue-light photoreceptors is plausible but the
quantitative spike claims are unproven.

### Family B — ENGINEERING (5/5)

- **EN1 (mistral-min8):** PMMA wins on cost/coupling — but claims autoclave tolerance and quotes
  0.2 dB/cm at 650 nm. **Both specifics REFUTED by byte-check** (see claims table) — EN1 is the
  family's optimistic-but-wrong witness.
- **EN2 (or-union-alpha):** "you cannot guarantee a sterile retrofit"; PG7 compression gland +
  silicone tubing, compression over glue, alcohol disinfects but does not sterilize, do not
  flame/pressure-cook PMMA. The family's highest-quality witness.
- **EN3 (or-nemotron):** insertion → melanization 24–72 h, electrical baseline normalizes 5–7 d,
  optical coupling may need ~14 d; honestly notes no peer-reviewed fiber-embedded recovery
  timelines exist. The 2-week wait: conservative buffer, not proven necessity.
- **EN4 (or-ling3):** LED couples 10–20% into 1 mm PMMA; 0.5 mm lateral offset ≈ 1–3 dB;
  bend radius <2 cm ≈ 1–3 dB/bend; "measure with a power meter, don't trust my dB/°."
- **EN5 (groq-qwen):** $40 buys 1–2 fibers, not an array; co-locate one fiber with the central
  electrode; expect <1% transmission over 5 cm; "a scattering sensor, not a waveguide."

**Family shape:** buildable at hobby tier; the real fight is the feedthrough (EN2) and tip
biofouling, not the fiber. Direct contradiction EN1-vs-EN2 on autoclaving resolved by byte-check
in EN2's favor.

### Family C — MEMORY (5/5)

- **ME1 (groq-oss):** write mechanism candidate: photoreceptor (WC-1/2) → Ca²⁺ influx → membrane
  depolarization → spike; cross-modality equivalence conceivable but uncalibrated.
- **ME2 (groq-oss20):** fiber-dose photobleaching negligible (<0.1 vs >10 J/cm² thresholds);
  thermal <1 °C; any optically induced trace lasts seconds–minutes; **"no evidence for long-term
  optical memory in mycelium."**
- **ME3 (cerebras-oss):** concrete read-after-write protocol: success = ΔI with SNR ≥ 10 AND
  ΔI/I ≥ 20%; pitfalls quantified (moisture drift ~0.5 dB/h, tip biofouling 1–2 dB/day);
  dead-block control required.
- **ME4 (cerebras-qwen):** physical write local to ~1–3 mm, but the network integrates globally —
  "expect cross-talk, not pixel addressing"; functional resolution 2–5 mm at best.
- **ME5 (mistral-min8):** claims 1.5–2.5 kbps/fiber, resting on a cited "Trametes mycelial optical
  fiber" paper. **Outlier: the premise contradicts OP1/CO1 and the citation could not be
  verified** — flagged as suspected hallucination; the capacity number is rejected pending the
  citation's existence.

**Family shape:** optical WRITE may exist as a stimulus; optical MEMORY has no evidence base —
state, if it exists at all, lives in the electrical/biological layer with seconds–minutes optical
traces. Capacity estimates are fantasy until read-after-write passes ME3's bar.

### Family D — COMPUTE (5/5, one degenerate)

- **CO1 (or-union-alpha):** routing must be fiber-side; star architecture (independent LEDs →
  fiber pairs → photodiodes, sequential activation); the network can *modulate* transmission
  (growth, pigmentation, hydration) — "a slow, potentially useful material response — not
  demonstrated packet routing"; demand uncolonized-substrate control.
- **CO2 (or-nemotron):** DEGENERATE — 456 chars restating the mission context, no latency
  comparison. Counted answered, treated as a non-answer in the fold. (The family's other witnesses
  imply the answer anyway: optical I/O ~ns vs biological ~Hz — the bottleneck is the substrate,
  not the photons.)
- **CO3 (or-ling3):** optical thickness τ ≈ 250–500 at 5 cm → firmly diffusive; WDM colors coexist
  but crosstalk worse than −20 dB without time-gating; coherent phase I/O implausible;
  intensity-modulated diffuse comms plausible at $30–40.
- **CO4 (groq-qwen):** gate ranking: (1) electrical→optical via hyphal swelling/scattering change
  (slow analog readout, hydrogel-switch analog) — most plausible; (2) optical→electrical via
  photoreceptors — moderate; fast digital gating: not on the table.
- **CO5 (groq-oss):** scaling wall: above ~200 channels / <1 ms ambitions, biological bandwidth
  (~1 Hz) is the bottleneck — the optoelectronics dominate and the substrate stops mattering.

**Family shape:** unanimous across competent witnesses — compute claims die on biological
bandwidth; the optical layer is a sensing/telemetry/modulation channel, not a compute fabric.

### Family E — PROGRAM (5/5)

- **PR1 (groq-oss20):** unique capability = spatially multiplexed read/write with NO Faradaic
  artifacts + telemetry through the tub wall. Flag: its Gb/s spec-sheet talk is the family's
  optimism outlier — the capability argument survives, the bandwidth framing does not.
- **PR2 (cerebras-oss):** pre-registered falsifier: lock-in detection at the drive frequency
  (10 Hz, in-phase vs quadrature), sham (cladded-off) fiber control, thermistor <0.1 °C gate;
  H0 = V_lock ≤ 3σ dark baseline; reject only if ≥5σ, phase-locked, sham flat, temperature flat.
- **PR3 (cerebras-qwen):** $30–37 BOM: 520 nm 5 mW laser $8 (or 650 nm $5), 1 mm PMMA $8–12,
  BPW34 $0.50 + load, feedthrough $8–12, misc $5. $0 fails at source/detector; $40 fails at
  sterile stable feedthrough; $100 still fails at SNR/contamination — never at routing.
- **PR4 (mistral-min8):** 24 h logging, CSV schema (timestamp, pulse_freq, photodiode
  raw/normalized, spike_count, temp), blind on/off pulse assignment. Flag: quotes a Thorlabs BOM
  that overshoots $40 — take the schema, not the shopping list.
- **PR5 (or-union-alpha):** promotion gate: light at fiber A evokes electrode spike-rate change at
  B, >2 SD above baseline within 100 ms, ABSENT in dead/autoclaved block and with 650 nm
  no-photoreceptor control; memory only if >10 min hysteresis; kill if changes track heating
  >0.1 °C, dead block matches, or required power >5 mW. Honest bottom line: "no known fungal
  photoreceptor for spiking, so thermal/ROS artifacts are the default explanation" — the
  experiment exists to defeat that default.

## 5 strongest mechanism claims (byte-verification owed before belief)

Verification = live web byte-check this session (free tools), plus O2's earlier search wave.
Status after check:

| # | Claim (source segment) | Status | Byte evidence |
|---|---|---|---|
| 1 | Living/fixed mycelium is an efficient optical **diffuser**, not a waveguide: μs′ ~5–20 mm⁻¹ at visible, ballistic component extinct within ~0.1 mm (OP1, OP2, CO3, EN5 converge) | **VERIFIED** | Carrillo-Acuña et al., *APL* 122, 113702 (2023), DOI [10.1063/5.0143619](https://pubs.aip.org/aip/apl/article-abstract/122/11/113702/2881156) — laser through a mycelium bioplate → speckle, ~Lambertian diffusion; independent μs′-scale tissue-optics numbers consistent. O2 receipt: no peer-reviewed hyphal-waveguide study found. |
| 2 | **No published evidence** that individual hyphae guide light; any capacity claim built on hyphal waveguiding is unsupported (OP1, CO1; ME5's counter-citation) | **VERIFIED** (as a null) | O2 search wave S1–S5 + this battery: only counter-evidence is ME5's "[Trametes optical fibers, funbio 2017](https://doi.org/10.1016/j.funbio.2017.09.002)" — **could not be verified; suspected hallucination**; belief withheld. |
| 3 | Blue light (~450–470 nm) modulates fungal electrophysiology — optical WRITE is a real mechanism family (OP4, ME1, CO4-rank-2, PR5) | **PARTIAL — mechanism VERIFIED, numbers NOT** | Real: Olsson & Hansson 1995 ([Armillaria APs ~5 mV, stimulation-sensitive](https://www.researchgate.net/publication/226412519_Action_Potential-Like_Activity_Found_in_Fungal_Mycelia_Is_Sensitive_to_Stimulation)); FEMS 2025 review ([membrane potential responds to blue light](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/)); [Science Robotics mycelium responds to blue light with voltage potentials](https://www.nature.com/articles/s41598-018-26007-1). NOT found: OP4's specific "Fricker 2020, 0.8–2 mV from 5 µmol m⁻² s⁻¹" — treat those numbers as invented until produced. |
| 4 | Mycelium autofluorescence bands support an optical READ: NAD(P)H ex 330–360 / em 440–470 nm; flavins ex 380–490 / em 520–560 nm (OP3) | **VERIFIED** | [NAD(P)H 340/em 440–470 review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6352511/); [flavin autofluorescence for fungal metabolism monitoring (MDPI 2022)](https://www.mdpi.com/2076-2607/10/6/1179) — demonstrated in fungi specifically. |
| 5 | PMMA POF: ~0.1–0.2 dB/m at 650 nm (not dB/cm) and **autoclaving is unsuitable for PMMA** — EtO/alcohol-compatible protocols instead (EN1 vs EN2 conflict) | **VERIFIED — EN2 right, EN1 wrong** | [PMMA POF 85–170 dB/km at visible minima](https://fiberfin.com/pof-basics-size-and-bandwidth/), [PMC POF sensor review ~125 dB/km @650](https://pmc.ncbi.nlm.nih.gov/articles/PMC3478834/); [autoclave sterilization unsuitable for PMMA (PubMed 29524755)](https://pubmed.ncbi.nlm.nih.gov/29524755/). EN1's "0.2 dB/cm" is ~10× high; its 10 cm-cube arithmetic (0.02 dB) is internally wrong. |

Ledger law honored: two model-cited sources were killed at byte-check (OP4's Fricker numbers,
ME5's Trametes paper) — leads are not facts.

## Go/No-Go — $40 optical add-on

**GO — as a stimulation + photometry channel on the sensing rung. NO-GO as "optical routing /
optical compute."** One experiment, pre-registered, either outcome files.

Why GO:
1. The fold's verified core is enough to justify $40: optical WRITE is a real mechanism family
   (claim 3), optical READ has two physical channels (diffuse transmission photometry + verified
   autofluorescence bands, claims 1+4), and the unique capability vs electrodes is real —
   spatially addressable, artifact-free stimulation plus telemetry through the tub wall (PR1).
2. The falsifier costs nothing extra and is already specified (PR2 + PR5 merged): lock-in at drive
   frequency, sham fiber, dead-block control, 650 nm no-photoreceptor control, thermistor <0.1 °C
   gate. The experiment is exactly the machine designed to defeat PR5's "thermal/ROS is the
   default explanation."
3. BOM fits with byte-checked numbers (PR3 + claim 5): 520 nm or 650 nm 5 mW source $5–8, 1 mm
   PMMA fiber $8–12 (0.1–0.2 dB/m — fiber loss is a non-issue at tub scale), BPW34 + TIA ~$3,
   compression-gland feedthrough $8–12, misc $5 → **$30–37**.

Why not more than GO:
- Routing/compute is refuted at the physics level for this budget (claims 1–2: diffuser, τ≈250–500,
  biological ~Hz bottleneck) — the add-on must not be sold to the program ladder as an optical bus.
- No optical memory evidence exists (ME2); promotion to the memory rung requires PR5's >10 min
  hysteresis result, which is exactly what the experiment tests.
- OP5 (damage threshold) is an open hole — until re-asked, hold pulse power ≤5 mW and duty ≤10%
  (the fleet's most conservative standing numbers).

Pre-registered promotion/kill (adopted verbatim from PR5, seconded by PR2): **promote** if light
pulses at fiber A evoke electrode spike-rate change at B >2 SD above baseline, absent in dead
block and 650 nm control, without tracking thermistor >0.1 °C. **Kill** if changes track heating,
dead block matches, or required power >5 mW. **Promote to memory rung** only with >10 min
read-after-write hysteresis at ME3's SNR ≥ 10 bar.

---

**Cost accounting:** 40 free-lane calls total (11 probe + 25 pass-1 + 4 pass-2) · zai-lite reserve
0 calls · or-union-alpha 4 calls inside its free window (ends ~2026-09-23) · **$0 cash.**
**Artifacts:** `raw.jsonl` (29 rows) · `probe.json` · `summary.json` · `answers.md` · driver
`watch/inbox/wave_20260916/c2_fiber25_20260916.py` (repo code untouched). question_digest
`380e2df78bd7eb4b`. No git actions taken.
