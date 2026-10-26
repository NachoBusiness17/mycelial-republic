# G-D_WRITE_MECHANISMS — receipt (wave lane: physical_computing / GAP G-D)

**Gap:** the myco-memory ladder's "write" claim. Two candidate mechanisms compete to be
step-2's first write: (A) mycelium **memristive hysteresis** (±0.55 V writes, hours
retention, ion redistribution claim) vs (B) **tube-remodeling memory** (Tero-rule
dD/dt = a·|Q|^γ/D − bD, Physarum habituation precedent).
**Wave law:** receipt FIRST, append as you go · no git · no paid APIs · WebSearch/WebFetch only.
**Date:** 2026-09-16

## Questions (socratic tease)

1. Exact published write parameters (voltage, duration, electrode spacing) for electrical
   memory in LIVING (not dried/infused/dead) mycelium?
2. What forcing (light / chemical / mechanical / nutritional) reliably produces
   tube-remodeling, and on what timescale?
3. Can ONE rig test BOTH mechanisms — electrical write read electrically;
   mechanical/nutritional write read via impedance topology?

## Log (appended as gathered)

- [receipt opened — searches starting]
- Provenance traced: the "±0.55 V writes, hours retention, ion redistribution" claim in the
  ladder originates from `watch/inbox/wave_20260916/receipts/R1_SWARM_RESEARCH.md` M05 — an
  LLM free-lane answer, flagged there itself as "DOIs unverified" (and R1's M10 produced a
  rickroll citation, so M05 needs independent pinning, which this GAP does).
- Search infra notes: WebSearch backend intermittently 429 (rate limit); PubMed cookie-walls
  and MDPI 403s direct fetch; Europe PMC REST (`ebi.ac.uk/europepmc/webservices/rest`) is the
  workhorse; arXiv abs pages fetch fine; Crossref/OpenAlex timed out from this lane.
- PubMed search "mycelium memristive" = ZERO results — the fungal-memristor literature lives
  in engineering venues, not biomedical indexing. Europe PMC full-text corpus "fungal
  memristor OR memristive fungi OR memristive mycelium" = 2 substantive hits only.
- **Hit A1 — LaRocco et al. 2025, PLoS One 20(10):e0328965 (PMC12513579), "Sustainable
  memristors from shiitake mycelium" (Ohio State):** the 2025 demo, BUT the material was
  **sun-dried ~7 days then misted** — NOT living during tests. Parameters: hysteresis sweeps
  200 mVpp → 20 Vpp, optimal **1 Vpp**, near-ideal pinched loop at **5 Vpp / 10 Hz** (95%
  accuracy); volatile memory demo at ~**5 V write/read pulses, 0.01–0.1 ms**, up to
  **5.85 kHz** (90±1%); **no electrode material/spacing reported**; **no hours-scale
  retention measured** (memory explicitly volatile, ~0.1 ms reads); mechanism hand-waved to
  "capacitive/memfractive/memristive proteins" + stimulus-formed conductive pathways,
  moisture-dependent. → Fails the LIVING test and the hours-retention test.
- **Hit A2 — Beasley, Abdelouahab, Lozi, Tsompanas, Powell, Adamatzky 2022,
  Bioinspir. Biomim. 16(6) 066009, DOI 10.1088/1748-3190/ac2e0c, arXiv:2002.06413,
  "Mem-fractive properties of mushrooms":** the closest LIVING-tissue claim — LIVING fruit
  bodies (grey oyster, Pleurotus ostreatus) on wood shavings. Electrodes: **iridium-coated
  stainless sub-dermal needles, ~10 mm apart in the cap** (cap-cap and cap-stem configs).
  Sweeps: **±0.5 V and ±1 V**, deliberately capped "so as not to cause electrolysis of
  water"; step-size 0.001 V used to slow sweeps. Result: hysteresis with "lobes" but the
  loop **fails to pinch at the origin** (tissue generates own potential, stores charge) →
  authors classify as **mem-fractor** (fractional-order element), not clean memristor;
  nano-amp current oscillations near 0 V. **No retention time reported.** Note: the
  ladder's "±0.55 V" is NOT this paper — published value is **±0.5 V**.
- **Hit A3 — Physarum memristor line (Gale, Adamatzky, de Lacy Costello, arXiv:1306.3414,
  "Slime Mould Memristors," 2013):** living protoplasmic tubes, memristive I-V, "active
  memristor" framing for asymmetric curves; abstract carries **no voltage/spacing/retention
  numbers**. Already registered in S4_CORPUS_STEAL T3.4 with the artifact-dispute flag.
- **Hit A4 — CRITICAL: failed independent replication.** Schmidt, Seyfried, Reutina, Seskir,
  Miranda (Plymouth PEARL + KIT), **MRS Advances 2025, DOI 10.1557/s43580-025-01198-8**:
  revisit of the Physarum bio-memristor reports **NO memristive behavior** — the elliptical
  I-V is explained by **plain RC capacitance** (electrode/electrolyte artifact). Co-author
  line reportedly includes an author of the original 2017 "growing bio-memristors from slime
  mould" method. First registered in S1_ACADEMIC_WHO.md; this GAP confirms its bearing:
  the electrical-write mechanism's flagship demos are (i) dried material, (ii) fruit bodies
  with mem-fractive (not memristive) classification, (iii) Physarum tubes with a standing
  failed replication. HN 45772497 carries the shiitake-artifact debate too.
- **Mechanism B — the habituation chain (Physarum):**
  - Boisseau, Vogel, Dussutour 2016, Proc R Soc B 283:20160446 (PMC4855389): habituation to
    **quinine AND caffeine** (bitter repellents) on agar bridges; repeated crossing days;
    stimulus-specific (not fatigue); memory persists after training stops.
  - Boussard, Delescluse, Pérez-Escudero, Dussutour 2019, Phil Trans R Soc B 374:20180368:
    memory substrate evidence = **CHEMICAL** — "circulating memory": habituation to sodium
    over 6 days survives **1 month as sclerotia** (dormancy, network dissolved);
    **2 h constrained sodium absorption incepts habituation** without morphology change.
  - Yoneoka & Takamatsu 2023, Front Cell Dev Biol 11:1249165 (PMC10667701): quinine-HCl
    **0.5 mM** in 1% agar bridges, **Days 1–4 training**; network shifts **tree → mesh**
    across days; on Day 5 **cutting the learned network (2–3 mm spatula cut) or rotating it
    90°/180° behaves "as if the memory had been deleted"** → morphology is load-bearing for
    the learned state readout (chemistry alone insufficient). Conclusion: chemistry writes
    internal state, tube morphology is the gateway the behavior reads.
  - Kramar & Alim 2021, **PNAS 118(10):e2007815118** (PMC7958412): single nutrient source
    → tubes thicken toward it, imprinting nutrient location in the **tube-diameter
    hierarchy** = externalized spatial memory. (RESOLVED below: forcing = heat-killed
    bacteria pellet or 1 µL of 0.5 M glucose + 0.1 M leucine; diameter redistribution
    ~15 min; imprint persists ≥310 min; bright-field imaging only, no electrodes.) Note: PNAS 2021 published a critique
    (10.1073/pnas.2105928118, "Missing evidence for memory in the monocellular slime mold")
    and the authors replied (PMC8040657) — the falsifier ledger must cite both sides.
  - Nishi, Tero, Nishigami, Nakagaki 2026, J Math Biol 93(3):36 (PMC13481565, published
    Aug 2026): minimal dynamical model of habituation from **non-specific intracellular
    biochemical processes** — reproduces Physarum chemical habituation; the 2026-theory
    anchor for the chemical-write branch.
  - Forcing menu so far: **chemical** (quinine 0.5 mM agar bridges; NaCl; caffeine) works
    with days-scale training; **nutritional** (single oat/nutrient source) drives
    tube-diameter remodeling; **light** forcing exists (light-trapped decision-making,
    arXiv:2506.12803 2025 → published PRX Life 4, 023026 (2026), Schick et al.; Saigusa
    2008 PRL = 3 unfavorable pulses at constant intervals → anticipatory slowing at the
    next expected pulse; period not in abstract (commonly cited ~1 h), persistence not
    stated — fetch honest, not verified); **mechanical** forcing demonstrated as an
    OVERWRITE (network cut = memory deletion, Yoneoka Day 5).
- **Hit A5 — failed replication, parameterized.** Schmidt, Seyfried, Reutina, Seskir,
  Miranda, two 2025 papers: (i) "Electrical characterization of the alleged bio-memristor
  *Physarum polycephalum*," MRS Advances, DOI 10.1557/S43580-025-01198-8 (open PDF at
  Plymouth PEARL); (ii) "From simulation to reality: experimental analysis of a slime mold
  circuit model," Front. Soft Matter 5:1588404, DOI 10.3389/frsfm.2025.1588404. Setup:
  LIVING plasmodium in a **15 mm PVC bridge** between 50 mL tubes, **3D-printed conductive
  PLA collars (Ø 4 mm outer / 1.5 mm inner)** as electrodes; **11 sinus inputs from 5 mV to
  2 V**, frequencies ~1 mHz–100 Hz (longest runs 1,000 s); 38 cultures, 289+ measurements;
  controls included cactus, basil, cheese, yogurt, waters, dummy resistors, and a real
  Knowm 1×16 memristor. Result: **94.4% of traces elliptical (RC-like), never pinched**;
  best fit = series R-C + parallel R-C (low-pass ~100 Hz, high-pass ~0.4 mHz). Conclusion
  verbatim: "The inherent capacitance of the slime mold defies the claim that slime molds
  are (bio-)memristors." Reframe: Physarum = passive **pseudo-capacitor**, usable in
  filter/timing/snubber circuits.
- Provenance nugget: the "ion redistribution" phrase in the ladder plausibly leaked from
  Buffi 2025 iScience FPC's own limitations ("unclear whether the signals convey
  information or merely reflect periodic ion redistribution during growth" — C19 P1.2),
  i.e. a stated limitation became a claimed mechanism upstream.

## Answers to the socratic teases

**Q1 — exact published write parameters for electrical memory in LIVING mycelium:**
There is no published demonstration of nonvolatile electrical write/read in living
vegetative mycelium at ±0.55 V with hours retention. The claim as filed (R1 M05,
"DOIs unverified") does not survive contact with the literature. What actually exists:
- Living **fruit bodies** (not mycelial network): Beasley 2022 — ±0.5 V and ±1 V sweeps
  (electrolysis-capped), Ir-coated SS needle electrodes ~10 mm apart, hysteresis with
  unclosed (mem-fractive) loops, **no retention measured**.
- **Dried** shiitake, remisted: LaRocco 2025 — 1 Vpp optimal / 5 Vpp pinched at 10 Hz,
  ~5 V write-read pulses of 0.01–0.1 ms, **explicitly volatile**, electrode spacing not
  reported, up to 5.85 kHz.
- Living Physarum tubes: original memristor claims (Gale/Adamatzky arXiv:1306.3414;
  Miranda/Braund "growing bio-memristors" method) now **contradicted by independent
  retests** (Schmidt 2025 ×2): elliptical RC curves at 5 mV–2 V, 94.4% RC-classified.
Verdict: correct the ladder — L1 "±0.55 V write, hours retention" is **UNVERIFIED /
FALSIFIED-AS-STATED**; replace with "mem-fractive hysteresis in living fruit bodies
(±0.5 V, no retention) + contested/dried demos elsewhere."

**Q2 — forcing that reliably produces tube remodeling, and timescales (verified):**
- **Nutritional** (strongest, cleanest): single localized nutrient source (heat-killed
  bacteria pellet or 1 µL 0.5 M glucose + 0.1 M leucine) → tube-diameter distribution
  re-established in **~15 min**; dilation propagates as a wave ~15 µm/s; the thick-tube
  imprint persists ≥**310 min** with nutrient consumed by ~90 min (Kramar & Alim 2021
  PNAS; read by bright-field imaging, no electricity involved).
- **Chemical** (habituation): quinine-HCl **0.5 mM** (or caffeine; NaCl) on agar bridges →
  habituation over **~4 days** of repeated crossings; network shifts **tree → mesh** over
  days; **cutting the learned network deletes the behavior** ("as if the memory had been
  deleted" — Yoneoka 2023); **2 h constrained sodium absorption incepts habituation** and
  6-day training survives **1 month dormancy** as sclerotia via retained chemical
  ("circulating memory" — Boussard 2019). Chemical and morphological substrates are BOTH
  real and interlocked (chemistry writes internal state; tube topology is the readout
  gateway).
- **Light**: blue-light confinement drives contraction-mode switching and escape-path
  choice (PRX Life 2026); periodic unfavorable pulses → anticipatory slowing (Saigusa 2008
  PRL). Timescales less pinned in what this lane could verify.
- **Mechanical**: not a write channel per se but the **overwrite/erase** operation
  (network cut = memory deletion; rotation = corruption — Yoneoka Day 5).
- Tero-rule status: the dD/dt flux-adaptation law is canonical (Tero 2007 JTB; Tero 2010
  Science — both paywalled, already registered S4 T3.2) but R1-M04's parameter values
  (a|Q|^γ/D − bD numerics, "30–90 min reroute") remain unverified leads. Verified physical
  timescales stand in for it: **minutes** for diameter response, **hours** for imprint
  persistence, **days** for habituated topology.

**Q3 — can one rig test BOTH?** Yes. The C19/Buffi FPC canon is already the rig: gold
differential pairs (2 mm pads, pairs 1 cm apart) that the mycelium **grows onto** (3–4
days), 24-bit differential logging. Protocol A (electrical write → electrical read):
electrolysis-safe ±0.5–1 V sweeps/pulses on pair A, hysteresis + retention scoring on the
same pair, with the Schmidt falsifiers built in (RC-surrogate fit + dead twin +
elliptical-vs-pinched classification at multiple frequencies). Protocol B (structural
write → impedance read): nutrient/oat forcing at site A, track impedance magnitude/phase
and inter-pair transfer vs time at minute cadence for hours; cross-check with camera
topology (cheap USB microscope) and the Yoneoka cut-test as the erase/intervention
control. Same box, same electrode stack, same logger.

## Two-mechanism test matrix (for the ~$530 rig)

| | **Mechanism A: memristive hysteresis** (electrical write, electrical read) | **Mechanism B: tube remodeling** (nutrient/mechanical write, impedance-topology read) |
|---|---|---|
| Published precedent | Weak/contested: living fruit bodies mem-fractive (Beasley 2022); dried shiitake volatile (LaRocco 2025); Physarum memristor **failed replication** (Schmidt 2025 ×2) | Strong, multi-group: Boisseau 2016, Boussard 2019, Kramar & Alim 2021, Yoneoka & Takamatsu 2023, Nishi 2026 |
| Write forcing | ±0.5–1 V pulses/sweeps (electrolysis cap) | Nutrient pellet / glucose+leucine drop at a site; mechanical cut as erase |
| Read | Same-electrode I-V hysteresis; retention curve | Inter-pair impedance (mag/phase, EIS-lite) + camera topology; potential mapping |
| Expected effect size | Unknown; prior claims now RC-explained | Diameter redistribution **~15 min**, imprint ≥**5 h**, habituation **days** |
| Timescale to signal | Hours (if any) | Same-night (15 min–5 h); days for habituation |
| Built-in falsifiers | Dead twin + RC-surrogate + pinched-vs-elliptical gate (Schmidt protocol); controls: agar-only, water | Shuffled-surrogate, unforced twin, cut-test (Yoneoka), sclerotia persistence (Boussard) |
| Extra hardware | $0 (electrodes already in BOM) | ~$15 (USB microscope optional; nutrient = oats/glucose/leucine) |
| Fleet consumption | Hysteresis-night tile (VOID-able rows) | before/after receipt pair → routing-table tile (DESIGN step 3) |
| Failure meaning | Strong falsification datapoint (closes R1's experiment #1 honestly) | Weak null = forcing protocol wrong; retry with light/mechanical channels |

## Verdict — what stage-2 (the first write) targets FIRST

**Mechanism B: tube remodeling via nutrient forcing, read electrically.** Reasoning:
1. **Evidence asymmetry.** B has converging, replicated, multi-group evidence with verified
   minutes-to-hours timescales; A's living-material write is not established anywhere — its
   2025 flagship is dried and volatile, its Physarum line just failed independent
   replication with RC as the explanation, and the closest living result classifies as
   mem-fractive with no retention. R1 itself wrote the branch rule: "if falsified, the
   project collapses to structural (growth-scale) memory." This receipt does not fully
   falsify A, but it shifts the burden: A is now the claim WITH the worse prior, and
   stage-2 must not bet its first write on the worse prior.
2. **Timescale fits the cadence.** Cube writes land on a nightly cycle; B gives measurable
   state change in 15 min–5 h (same night, decisive before/after rows) and habituation in
   days — exactly the DESIGN ladder's steps 2–3. A's plausible effects (if any survive the
   RC gate) live at the same minutes-hours boundary where our own electrodes' artifact
   floor (DMSO/gold, polarization) is strongest — the hardest place to claim a first bit.
3. **Same rig, zero rework.** B reads through the FPC electrode stack (impedance vs time)
   plus a $15 camera; A needs nothing new either — so A runs as a bounded CONTROL night
   (±0.5 V sweep battery with the Schmidt gate), not as the mainline. We still file R1's
   "experiment #1" falsification datapoint, at control-experiment cost.
4. **The ladder stays honest.** Correcting L1 (±0.55 V/hours → mem-fractive/no-retention)
   before stage-2 keeps the before/after receipt pairs meaningful; a stage-2 built on an
   unverified write claim would produce VOID rows forever.

Stage-2 spec, one line: **night-0 baseline impedance/topology → nutrient write at
electrode A → impedance + camera read every ~5 min for 5 h → cut-test erase on a later
night → dead-twin and shuffled surrogates throughout; hysteresis control night filed
separately as [L1-claim audit].**

## Sources (fetched this lane)

- LaRocco et al. 2025, PLoS One 20(10):e0328965 — journals.plos.org (full text fetched):
  DOI 10.1371/journal.pone.0328965 · PMC12513579
- Beasley et al. 2022, Bioinspir. Biomim. 16(6) — arXiv:2002.06413 (ar5iv full text):
  DOI 10.1088/1748-3190/ac2e0c
- Gale, Adamatzky, de Lacy Costello 2013, "Slime Mould Memristors" — arxiv.org/abs/1306.3414
  (abstract; params not in abstract)
- Schmidt et al. 2025, MRS Advances — DOI 10.1557/S43580-025-01198-8 (metadata via search;
  PEARL PDF 403'd direct) + Schmidt et al. 2025, Front. Soft Matter 5:1588404 —
  DOI 10.3389/frsfm.2025.1588404 (full text fetched: 5 mV–2 V, PLA collars, 94.4% RC-like)
- Boisseau, Vogel, Dussutour 2016, Proc R Soc B 283:20160446 — PMID 27122563 · PMC4855389
  (abstract via Europe PMC; quinine+caffeine confirmed; full-text doses fetch flaked)
- Boussard et al. 2019, Phil Trans R Soc B 374:20180368 — PMID 31006372 (abstract via
  Europe PMC: sodium circulating memory, 2 h inception, 1 month dormancy)
- Yoneoka & Takamatsu 2023, Front Cell Dev Biol 11:1249165 — PMID 38020888 · PMC10667701
  (full text fetched: quinine 0.5 mM, days 1–4, tree→mesh, cut/rotate = memory deletion)
- Kramar & Alim 2021, PNAS 118(10):e2007815118 — PMC7958412 (full text fetched:
  ~15 min redistribution, ~15 µm/s wave, ≥310 min imprint, imaging only); critique
  10.1073/pnas.2105928118 + authors' reply PMC8040657 (cited, not fetched)
- Nishi, Tero, Nishigami, Nakagaki 2026, J Math Biol 93(3):36 — PMID 42608505 ·
  PMC13481565 (abstract via Europe PMC)
- Schick et al. 2025→2026, arXiv:2506.12803 → PRX Life 4, 023026 (abstract fetched)
- Saigusa, Tero, Nakagaki, Kuramoto 2008, PRL 100:018101 —
  DOI 10.1103/PhysRevLett.100.018101 (abstract via Europe PMC)
- Grasso 2026, Biosensors 16(2):131 — DOI 10.3390/bios16020131 (review context; abstract)
- Tero 2007 JTB + Tero 2010 Science: PAYWALLED, already registered in
  receipts/S4_CORPUS_STEAL.md T3.2 — not re-fetched (rule form canonical, parameters
  unverified here — honest)
- Repo provenance: watch/inbox/wave_20260916/receipts/R1_SWARM_RESEARCH.md (M05, M04),
  receipts/S1_ACADEMIC_WHO.md, receipts/S4_CORPUS_STEAL.md, receipts/C19_XMINE_ROUND2.md
  (Buffi FPC protocol), DESIGN_MYCO_MEMORY_20260916.md

**Coverage honesty:** searches ran against Europe PMC REST, PubMed (partial), arXiv abs
pages, PLoS, Frontiers, PMC/PNAS, plus spaced WebSearch retries; Crossref / OpenAlex /
arXiv-API rate-limited from this lane; the ±0.55 V figure was not found in ANY fetched
source — closest published number is Beasley's ±0.5 V on living fruit bodies.

Status: DONE — receipt complete, no git, $0, free fetch lanes only.

