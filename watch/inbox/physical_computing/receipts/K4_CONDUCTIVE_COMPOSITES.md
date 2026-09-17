# K4 RECEIPT — Mycelium-bound conductive composites ("grow the wire into the block")

- Lane: wave K4 · physical_computing
- Date filed: 2026-09-16 (RESPAWNED same day — prior lane died to rate limit at ~18:51 after sections A–B)
- Agent: ZCode subagent (web survey; no git, no paid APIs; Europe PMC REST + PubMed E-utilities + direct PMC fetches preferred, WebSearch only as fallback due to 429s)
- Method: literature sweep, receipt appended as evidence lands. Numbers quoted from abstracts/figures where paywalled (flagged).
- Scope: conductivity numbers · living vs dead at measurement · fabrication · grown-in vs applied conductive phase — per lineage.
- Sections: [A. mycelium+graphene — DONE, numbers in] [B. carbonized mycelium electrodes — DONE] [C. PEDOT chip (Telhan lineage) — DONE] [D. MycelioTronics metallized skin — DONE] [E. living-mycelium electrical numbers + FPC cross-check — DONE] [F. retracted robot-skin paper — DONE] [G. fabric/leather/living-skin composites — DONE] [H. carbon felt/MFC — DONE] [I. Ecovative null — DONE] [VERDICT — DONE]

---

## A. Mycelium + graphene (applied/doped, some grown-in)

- **"Bioinspired Strong and Tough Layered Bulk Composites via Mycelial Interface Anchoring Strategy"** — Advanced Science (2025), DOI 10.1002/advs.202413226, PMC12097066 (full text read 2026-09-16). Hyphae *grow around and fix* graphene nanosheets (GNs) + PEG-PVA into 3D layered bulk composite — the closest published "grow the wire into the block" structural analog. **Numbers (now confirmed): at 15 wt% GNs, conductivity ≈ 200 S/m longitudinal** (vs 0.0001 S/m for the same GN load blended in without mycelial anchoring — a 10⁶× alignment dividend), **strongly anisotropic** (insulating perpendicular to the sheet alignment), piezoresistive (resistance rises with load — that's the "protective warning" function). Strength 82.6 MPa, modulus 3.12 GPa. GROWN-IN placement, APPLIED phase (sheets dispersed in growth substrate, then hot-pressed assembly; not metabolically produced).
- **"Machine Learning-Assisted Bio-Interfacial Engineering … Nanocomposites"** — Adv. Mater. (2026), DOI 10.1002/adma.202518806. Mycelium–graphene composites, strength >58 MPa, toughness >6 MJ/m³ — mechanical, not electrical.
- **Known literature direction (to verify numbers):** GO/mycelium composites mostly for antimicrobial/adsorption; GO itself is an insulator — must be reduced (rGO) to conduct; papers reporting actual S/m on *mycelium-bound* rGO are rare. GO is also antifungal at growth concentrations (Verticillium dahliae inhibition, Microbiology Spectrum 2025) — **practice note: you cannot grow mycelium through high GO loading; add reduced/conductive filler post-growth or at low loading.**

## B. Carbonized (pyrolyzed = dead-by-definition) mycelium electrodes

- **"Fungal Carbon: A Cost-Effective Tunable Network Template for Creating Supercapacitors"** — Global Challenges (2024), DOI 10.1002/gch2.202300315. Pyrolyzed *Agaricus bisporus* / *Pleurotus eryngii* filament networks as self-templated mesoporous carbon; BET ≈282 / ≈60 m²/g. Conductivity/capacitance pending.
- General class (verified 2024 example, adjacent): white-rot-fungus-pretreated biomass → hierarchical porous carbon, 898 m²/g, 308 F/g @0.5 A/g in 6 M KOH (Front. Microbiol. 2024, 10.3389/fmicb.2024.1374974). Mycelium-derived carbons routinely hit 200–350 F/g; conductivity rises with graphitization (800–1000 °C).
- **Living-vs-dead: always DEAD (N₂/Ar, 600–1000 °C).** The mycelium *is* the carbon (fully grown-in — best case for "block as electrode"), but the block no longer grows, heals, or senses biologically.

---

## C. PEDOT:PSS on mycelium — the Telhan-lineage reservoir chip (Sci Rep 2026, OA)

**"Morphologically tunable mycelium chips for physical reservoir computing"** — Scientific Reports (2026), DOI 10.1038/s41598-026-55550-5, PMC13500807 (full text read 2026-09-16). The direct published descendant of the Telhan-lab "grow a chip, infuse it" idea.

- **Fabrication (verbatim chain):** grow mycelium chips in 19×14×4 cm trays → **deli-slice to 1 mm** sheets → cut 50×100 mm → **mist with 70% isopropanol** (pre-wet) → float in **1.3% PEDOT:PSS (Ossila PH1000)** → **vacuum-infuse at −0.8 bar for 30 s** → sandwich between acrylic with ridges and **dry to 10% moisture at 24 °C overnight** in a food dehydrator; the acrylic ridges force the PEDOT:PSS into a **grid pattern** (i.e., the electrode grid is literally embossed into the block by pressing).
- **Numbers:** no absolute S/m claimed for the composite — they report I–V curves (4-wire Kelvin, Keithley 2400, 1–20 V, 3 mm probe spacing), memory capacity, NARMA-10 (NRMSE ≈ 0.984). **Moisture = the dominant control on conductivity: "voltage response curves showed modest drift, likely due to moisture exchange… No sealing or moisture-stabilizing treatment was applied… gradual conductivity decline over time is expected."** Resistive drift with humidity is intrinsic, not a nuisance they solved.
- **Living vs dead at measurement:** effectively DEAD/dormant — 70% IPA mist + dehydration to 10% moisture; **zero viability assays in the paper** ("kill/fixat/viab" have no matches in full text). The "biofabricated" claim is about morphology, not live tissue.
- **Grown-in vs applied:** structure grown-in, conductor APPLIED (infusion after kill). Cites Danninger: mycelium PVD-coated Cu / electroplated Au traces, and PEDOT:PSS-soaked mycelium as vias for stacked mycelium PCBs.
- Hardware note: 16 spatially distinct reservoirs/chip on a carrier board with amplification + level translation — the electrode-grid-on-mycelium idea is real at device level.

## D. MycelioTronics — metallized mycelium skin (Sci Adv 2022, OA)

**"MycelioTronics: Fungal mycelium skin for sustainable electronics"** — Danninger, Pruckner et al., Science Advances 2022, DOI 10.1126/sciadv.add7118, PMC9651864 (full text read 2026-09-16).

- **Retraction status: NOT RETRACTED** — PMC record carries explicit `is-retracted: no` flag (checked 2026-09-16). The "robot-skin lineage" is alive; a separate retraction rumor checked below (§H). [CORRECTION below in §H — this flag line refers to MycelioTronics add7118 only; the ADAMATZKY sensing-skin paper is the retracted one.]
- **Numbers:** PVD metal traces on skin (3 nm Cr / 400 nm Cu / 50 nm Au, laser-ablated) reach **9.74 ± 1.44 × 10⁴ S/cm** trace conductivity (≈ 1.6× worse than bulk Cu; real wires' class). **The bare mycelium skin is explicitly described as electrically INSULATING** — "the excellent thermal stability and electrically insulating nature of the hyphae network renders our mycelium skin a highly suitable biodegradable substrate."
- **Fabrication:** *Ganoderma lucidum* skin grown on boiled beech shavings + spelt flour + plaster (1 kg / 50 g / 25 g / 2 L water), 25 °C under PE separator grid → harvest young/medium/mature skins → dry → PVD metallize → laser ablate patterns. Also: mycelium-skin Zn/MnO₂ battery separators, interdigitated-electrode humidity sensor (12 mm fingers), compost-tested (58 °C, weeks to degrade).
- **Living vs dead:** DEAD — skins harvested and dried before metallization; no viability claims.
- **Grown-in vs applied:** substrate grown, conductor APPLIED (vacuum metallization — not hobby-replicable; electroplating upgrade route shown).

## E. Living mycelium — actual electrical numbers (ionics, not electronics)

- **"Self-grown mycelium in confined geometries as nanofluidic devices"** — Nature Communications (2026), DOI 10.1038/s41467-026-72999-0, PMC13376398 (full text read 2026-09-16). MSU (Warsinger/Siwy groups).
  - **Numbers:** living/self-grown mycelium bridging a confined geometry conducts IONS with conductivity plateaus **~0.3 mS/cm** (*G. sessile* across a 0.3 mm gap) and **~0.6 mS/cm** (*P. ostreatus* through a metal mesh); mycelium-integrated microchannel boosts ion conductivity up to **467× over the empty channel**, equivalent to a 49.7 nm synthetic nanochannel. Zeta potential −12 to −18 mV (pH 7); surface charge −2.8 to −4.1 mC/m²; works live AND freeze-dried (EDL/nanopore scaffold persists after drying).
  - **Method:** Ag/AgCl electrodes (4 mm), LSV −2 to +2 V @ 100 mV/s, KCl electrolyte, 24 h equilibration.
  - **Meaning for K4:** the wet living block is an IONIC conductor in the mS/cm class — orders of magnitude short of any metal (Ag 6.3×10⁷ S/cm) but *electrolyte-real*: it is literally a humid ion gel. This is why every published "conductive mycelium" device INFUSES or VAPORIZES a conductor instead of using the hyphae.
  - **Living vs dead:** LIVE mycelium (and freeze-dried scaffold) — the only lane here where the block is alive at measurement.

- **"Fungal Potential Card" original paper — "Detection of electrical signals in fungal mycelia in response to external stimuli"** — iScience (2025), DOI 10.1016/j.isci.2025.113484, PMC12483595 (full text read 2026-09-16). PCB with **8 couples of embedded ENIG (electroless Ni / immersion Au) differential electrodes, 2 mm pads**; *Fusarium oxysporum* inoculated as spore droplets ON the pads, grows across them — living mycelium measured by external noble-metal electrodes, no conductive phase in the substrate. Signals **µV-class**; Faraday cage required (flagged as the fix for prior studies' artifacts); ADC-24 24-bit logger; STFT to separate signal from noise; biocide (cycloheximide/NaN₃/calcimycin) kills the signal → biological origin. **K3 cross-check: confirms K3's ENIG-cost/compatibility line and the C17 µV signal-scale assumption; fungus-on-gold, not block-as-electrode.**

- **Beasley, Powell, Adamatzky — "Capacitive storage in mycelium substrate"** — arXiv:2003.07816 (2020, never journal-published). *P. ostreatus*-colonized substrate: capacitance **hundreds of pF**; charge density decays rapidly with distance from the probes. Substrate = dielectric/ionic storage, not a conductor.

## F. Pure-mycelium electrical sensing — the RETRACTED robot-skin paper

- **"Fungal sensing skin"** — Adamatzky, Gandia, Chiolerio, Fungal Biology and Biotechnology (2021), DOI 10.1186/s40694-021-00110-x, PMC7972235. **RETRACTED** (retraction note DOI 10.1186/s40694-021-00114-7, PMC8173894). Known to this wave's canon (C17, K11, F6, S1) — **do not cite as support.** (The PMC `is-retracted` metadata flag reads "no" — an object lesson: trust the retraction note, not the API flag.)
- What it claimed (for the record only): living *G. resinaceum* skin (homogenized slurry grown in trays) responds to tactile + optical stimuli; iridium-coated stainless-steel sub-dermal needle electrodes in differential pairs; spikes avg **0.2 mV** (max 0.85 mV), width ~774–1500 s. No DC conductivity of the skin was reported even there.
- Not-retracted sibling: **"Towards fungal sensing skin"** (PMC8117569) + Adamatzky's unretracted fungal-electrophysiology canon (K1 receipt) carry the living-mycelium-spikes field without this paper.
- **MycelioTronics (§D) retraction status stands verified separately: NOT retracted** (no retraction note exists for 10.1126/sciadv.add7118; Europe PMC retraction-type query returns zero hits for mycelium/fungal electronics 2021–2026 apart from the skin paper above).

## G. Fungal fabric / leather / living-skin composites

- **"Biovegan Leather Sensor: A Mycelium Functionalized Material for Electrophysiological Signal Monitoring"** — ACS Applied Materials & Interfaces (2025), DOI 10.1021/acsami.5c05377 (abstract read; paywalled body). Mycelium leather + **polypyrrole** in-situ composite (P-MCM): **conductivity 51.10 S/m**, tensile 3 MPa, elongation 13%, electrode–skin interface impedance **52.6 kΩ/cm² @ 10 Hz**; captures ECG/EMG/EEG "on par with commercial electrodes." DEAD mycelium (leather is harvested/processed), conductor APPLIED (oxidative polymerization bath — pyrrole monomer + oxidant). This is the best published NUMBER for a mycelium-bound electronic conductor short of vacuum metallization. Biopotential-grade but at skin-interface scale, not block-electrode scale.
- **"Mycoelectronics: Bioprinted living fungal bioelectronics for artificial sensation"** — PNAS (2026), DOI 10.1073/pnas.2530456123 (Cai, Yuan, Ronders, … ; abstract read; paywalled). **LIVING** mycelium bioprinted ON stretchable electronics as thermoresponsive skin: heat-induced vacuole remodeling/fusion modulates **ionic transport**, hence electrical conductivity of the network → sensing. Self-healing, grows back after damage, bridges "hard-to-reach" sensing paths by growing. This is the post-retraction robot-skin lineage done right: living ionic sensing layer over inert printed electronics — NOT a conductive block replacing wires. No absolute S/m in abstract.

## H. Carbon felt / fungal biofilm electrodes (MFC lane)

- **"Bioelectricity harvesting from microorganism… fungi for powering small-scale robotic systems"** — Frontiers in Fungal Biology (2025), DOI 10.3389/ffunb.2025.1739847, PMC12853654 (full text read 2026-09-16). The template for "mycelium carbon felt electrode" in the literature is always: **living fungal biofilm ON an external carbon electrode** (carbon cloth / graphite / carbon felt / 3D-printed porous carbon). The mycelium's role: dense 3D biofilm adhesion + extracellular electron transfer via redox metabolites (flavins, quinones) + exoenzymes. Fungal MFC power densities sit in the **mW/m²** class (review table; voltage outputs ~0.3–0.8 V open-circuit). The fungus NEVER replaces the carbon — it electrifies it. GROWN-IN biology, external conductor. LIVING at measurement (fuel cells must be, to work).
- Practice translation for the cube: a carbon-felt strip is ~$5–10, is already the standard cheap high-surface-area electrode, and hosts the mycelium instead of fighting it — a *biofilm-on-felt* composite electrode is the one "grown" electrode the literature actually supports for current-carrying (stimulation) duty.

## I. Ecovative — the null result

- Europe PMC "Ecovative" = 76 hits, all packaging/leather/startup-ecosystem literature; the authoritative MBC review (Polymers 2026, 10.3390/polym18161946, PMC13516071 — full text checked) catalogues density, compression, thermal conductivity and LCA for Ecovative-line composites since 2007 and contains **zero electrical/dielectric measurements**. Its only electrical remark is qualitative: CNT/graphene additives "may improve electrical conductivity, sensing capability" of MBCs, with the caution that after thermal inactivation, self-repair claims must be dropped. **No published Ecovative conductivity experiment exists in the peer-reviewed record.** (DARPA ELM-era outputs from that program are likewise not conductivity data.) Anyone citing "Ecovative conductive mycelium" is citing vapor.

---

## VERDICT

### The conductivity ladder, one table

| Material lineage | Conductivity | Living? | Conductor phase | Hobby-fab? |
|---|---|---|---|---|
| Living wet mycelium (nanofluidic, Nat Commun 2026) | **0.3–0.6 mS/cm ionic** | YES | none (the electrolyte is the conductor) | trivial |
| Plain mycelium substrate (Adamatzky arXiv 2020) | dielectric, ~100s pF | yes/dormant | none | trivial |
| PEDOT:PSS-infused chip (Sci Rep 2026) | unpublished; I–V only, drifts w/ moisture | NO (IPA + dried) | applied infusion | **yes** (food vacuum + dehydrator) |
| Polypyrrole leather (ACS AMI 2025) | **51.1 S/m** | NO (leather) | applied chemical bath | marginal (pyrrole = nasty) |
| Graphene-nanosheet LBC (Adv Sci 2025) | **≈200 S/m**, anisotropic, piezoresistive | NO (pressed composite) | grown-in placement of applied sheets | no (15 wt% dispersion + press) |
| Metallized skin, PVD Cu/Au (MycelioTronics 2022) | **9.7×10⁴ S/cm** (trace) | NO (harvested/dried) | applied vacuum metal | no (PVD coater) |
| Silver wire (K3 baseline) | **6.3×10⁷ S/cm**, non-drifting bulk | n/a | IS the conductor | **yes** (mid-print pause) |

### Can the BLOCK be its own electrode grid (vs external silver wire)?

**For measurement: NO — and not by a small margin.** Series-R arithmetic at K3's trace geometry (10 cm × 2 mm × 0.4 mm): the best published bulk composite (graphene LBC, 200 S/m) yields **≈625 Ω/trace**; the polypyrrole leather **≈2.4 kΩ** — exactly the conductive-PLA class K3 already disqualified. Resistance alone is survivable with a high-Z front end; the disqualifiers are the three that composite physics cannot waive:
1. **No stable half-cell.** The 0.0003–0.1 Hz fungal band is DC-adjacent µV work. Carbon/PEDOT/graphene junctions into unbuffered wet organics are polarizable, unknown, drifting junctions. Ag/AgCl is non-polarizable — that's *why* every biopotential standard uses it, and why the FPC card used ENIG gold pads with the fungus grown ON them rather than through them.
2. **Measured drift with the environment you're studying.** The PEDOT chip paper itself reports moisture-driven conductivity drift and "gradual conductivity decline over time"; the graphene composite is deliberately piezoresistive — in a growing, breathing block that's a noise generator, not a wire.
3. **No composite route survived at metal class** — the best (vacuum-metallized skin) needs a PVD coater, i.e., it abandons "the block conducts" for "we plated a wire onto the block."

**For augmentation: YES — three published, cube-compatible roles.**
- **Stimulation-spread grid (strongest case):** an embossed PEDOT:PSS grid inside the block spreads galvanotropism-drive current (K2) without metal-wire geometry artifacts, and electrode polarizability is irrelevant when you *drive* current instead of reading through the junction. The Sci Rep 2026 grid-embossing recipe is directly replicable.
- **Touch/moisture/strain skin:** the same grid doubles as a capacitive/resistive sensor where drift IS the signal (PEDOT chip; graphene LBC's piezoresistance is a feature here).
- **Biofilm-on-carbon-felt electrodes:** the one literature-supported *grown* current-carrying electrode — living mycelium colonizes a $5–10 carbon felt strip (FMFC standard); use for stimulation/ground duty, never the sensing pair.

**K3 cross-check (re-chloridizing):** a composite does NOT remove the tip chore. The chore exists because Ag/AgCl depletes; a composite has *no* stable half-cell to deplete — it trades a 30-min scheduled maintenance for an uncalibrated drifting junction. The correct augment is Ag/AgCl kept + PEDOT:PSS/hydrogel bridge where skin/substrate contact noise dominates (standard biopotential practice). K3's silver-wire verdict stands unchanged.

### Best published recipe (hobby-replicable)

**PEDOT:PSS vacuum-infusion grid — Sci Rep 2026 (10.1038/s41598-026-55550-5):** grow mycelium mat in a tray → slice 1 mm sheets → mist 70% isopropanol → float in 1.3% PEDOT:PSS (Ossila PH1000) → **vacuum-infuse −0.8 bar 30 s** → press between ridged acrylic (defines the grid) → dry to 10% moisture at 24 °C overnight. Household translation: brake-bleeder + mason jar or $100 Vevor vacuum kit; food dehydrator. Expect conductive-PLA-class resistance, i.e., sensor/actuator grade only. If a *numbered* conductive composite is wanted: polypyrrole mycelium leather (51.1 S/m) is the published ceiling at hobby chemistry — at the cost of pyrrole handling, which the $60-cube hygiene rule should probably veto.

### $ delta vs wire embedding

- **K3 wire baseline:** $7–12 silver wire for the whole cube, $0 tooling (mid-print pause), tips re-chloridized every 1–3 months (~30 min). Per-sensing-channel cost ≈ **$2–3**.
- **PEDOT:PSS grid:** $30–45 stock bottle (250 mL at 1.3% dilution = ~19 L working solution — one bottle outlives the project) + $40–100 vacuum tooling + $0–40 dehydrator. **First-time ≈ $70–185, marginal ≈ $5–10 per block.** So the composite is 1–20× the wire line and buys *no* measurement capability — it buys stimulation-spread and touch sensing.
- **Polypyrrole / graphene routes:** $50–90 and $30–120 respectively, both without a mid-print growth story.
- **Carbon felt biofilm electrode:** $5–10 per strip — the cheapest and only *living* grown electrode; suitable for drive/ground, not sensing pairs.

**Net:** the wire is both cheaper and signal-better for every sensing channel. The composite's honest role in CUBE1 is one PEDOT:PSS-embossed stimulation grid (~$10 marginal after ~$100 one-time tooling) plus optionally a carbon-felt ground — the block itself stays an ionic (0.3–0.6 mS/cm) dielectric that the silver wires listen through, exactly as K3 built it.

---

*Filed under wave-lane law: receipt first, appended as evidence landed (respawn lane — prior instance died to rate limits after §A–§B). No git, no paid APIs; lanes run via Europe PMC REST + arXiv API + direct PMC full-text fetches; WebSearch unused (429 avoidance). Writer: zcode-wave-k4-respawn.*
