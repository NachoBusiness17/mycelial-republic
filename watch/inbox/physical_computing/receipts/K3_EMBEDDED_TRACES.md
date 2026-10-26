# K3 RECEIPT — Embedded trace materials ("what metal survives a damp living block for months")

- Lane: wave K3 · physical_computing
- Date filed: 2026-09-16 (in progress — appended as evidence lands)
- Agent: ZCode subagent (web survey; no git, no paid APIs; WebSearch/WebFetch only)
- Mission: corrosion physics (Cu / Ag / Sn-plated Cu / stainless) in warm humid ion-rich organic substrate → effect on signal; printability (conductive PLA resistivity, silver epoxy/paint, mid-print wire embedding); ENIG cost at hobby tier (JLCPCB-class) vs the Fungal Potential Card precedent (iScience, 8× gold differential pairs on a mycelium-colonized PCB).
- Context: CUBE1 shopping list (~$55–60 total cube; stage-0 ear ~$31; Ag/AgCl electrodes; nV–mV differential signals, 0.0003–0.1 Hz fungal band). C17 flagged the stainless-needle Donnan-potential confound — electrode/trace material is signal-critical, not cosmetic.
- Ends with: materials decision table (metal / corrosion behavior / cost / print-integration method) + recommended trace material for the $60 cube + honest lifespan estimate before contact degradation.
- Sections: [A. corrosion physics — DONE] [B. printability — DONE] [C. ENIG cost — DONE] [VERDICT: decision table + recommendation + lifespan — DONE]

---

## A. Corrosion physics — warm humid organic substrate, ion-rich fluid

### A.1 Copper — the insulating-skin problem (CONFIRMED, disqualifying for contacts)

- Oxidation turns a 1.7×10⁻⁸ Ω·m metal into a semiconductor/insulator skin: **Cu₂O ≈ 10²–10⁴ Ω·cm; CuO ≈ 10⁵–10⁶ Ω·m bulk** (So et al. 2012, Mater. Sci. Semicond. Process., DOI 10.1016/j.mssp.2012.07.001 — films grown at 250 °C Cu₂O-dominated ≈10⁻² Ω·m, 350 °C CuO-dominated ≈10⁴ Ω·m; authors: "should be regarded as electrical insulators at typical operating temperatures"). Resistivity jump = **10–14 orders of magnitude**.
- Thin native Cu₂O forms in seconds–minutes, parabolic growth thereafter; Antler (1982, "Metallic Copper, Cuprous Oxide, and Electrical Contact Behavior") established the galvanic Cu/Cu₂O couple degrades contact behavior — foundational contact-engineering result.
- Fretting studies (IEEE Holm Conf. lineage): micromotion + air → oxide debris → rapid non-linear contact-resistance rise; self-reinforcing (higher current density at a-spots → heating → faster oxidation).
- **Cube relevance:** a bare-copper trace's *bulk* survives (etched away, not eaten through, in months) — but every *endpoint*, screw terminal, and probe junction grows the insulating skin. For nV–mV differential signals, a Cu₂O junction film is a series resistance + a noise/polarization source. Copper oxide skin = insulating. ANSWER TO TEASE 1a: yes, insulating.

### A.2 Silver — the semiconducting tarnish (survivable for bulk traces, watch the endpoints)

- H₂S + silver → black Ag₂S patina (acanthite, β-Ag₂S at RT). Alderete et al. 2023 (IEEE TCPMT, DOI 10.1109/TCPMT.2023.3231827, "Tarnishing (Ag₂S) Layer on Silver-Plated Electrical Contacts"): tarnish film *can* cause contact malfunction — but severity depends on film thickness and **contact force**: thin films are mechanically displaced / electrically fritted through by real contact asperities.
- Key material fact: **Ag₂S is a mixed ionic-electronic semiconductor — orders of magnitude LESS resistive than Cu₂O/CuO.** (α-Ag₂S above ~177 °C is famously superionic; RT acanthite is far more conductive than copper oxide.) This is why silver-plated contacts remain standard in industry despite tarnish: the soft sulfide film wipes off at contact points.
- **Cube relevance:** an embedded *continuous* silver wire sees no separable contact — tarnish on the flank doesn't matter, cross-section survives (Ag₂S growth is slow, nm-scale per month indoors; it darkens but doesn't dissolve). Endpoints: use Ag/AgCl chloride conversion (already in the CUBE1 BOM — DIY chloridized silver pair, $5–10) — that's not corrosion damage, it's THE standard non-polarizable electrode. ANSWER TO TEASE 1b: Ag₂S tarnish is semiconducting and thin — a nuisance at connectors, not a killer of embedded bulk; Ag survives best of the common metals.

### A.3 Tinned copper — the cheap armor (good bulk, same endpoint disease)

- The enemy is the same triad that kills copper, via the **volatile organic acid route**: ASM's *Corrosion of Tin and Tin Alloys* names acetic/formic acid vapor (from wood, packaging, insulation — i.e., exactly a mycelium-on-wood-shavings box) as the classic cause of non-conductive **SnO/SnO₂ + tin-carboxylate films** raising contact resistance on tin-plated conductors ([ASM chapter](https://dl.asminternational.org/books/edited-volume/chapter-pdf/537545/a0003818.pdf); [Lectromec on tin-plated conductors](https://lectromec.com/blog/what-are-the-potential-issues-with-tin-plated-conductors/)).
- **Formicary ("ant-nest") corrosion** needs oxygen + moisture + organic acids — the substrate IS this triad at 100% RH; it drills microscopic tunnels through copper *under* intact tin plating (HVAC literature, [Aloha Air summary](https://www.alamoaustinair.com/what-causes-formicary-corrosion-and-how-to-prevent-it/)). Formic acid is significantly more corrosive to copper than acetic, peaking at low concentrations (Academia.edu study of Cu in HCOOH/CH₃COOH).
- Tin whiskers (pure-Sn plating, compressive stress + humidity) = intermittent shorts; solder-alloy tinning (SAC305) largely avoids whiskers.
- **Cube relevance:** the tin/solder layer buys the *bulk* trace months-to-years — the corrosion chemistry attacks films and endpoints, and a thin oxide on a continuous trace is electrically invisible. Failure concentrates at *connectors and junctions*, same as copper. Formicary is the one mechanism that eats through plating — a slow burn, relevant at month-scale, not day-scale.

### A.4 Stainless (316/304) — survives the substrate, poisons the reading

- Self-healing nanometers-thin Cr₂O₃-rich passive film; 316 (2–3% Mo, PREN ≈ 24–26) beats 304 (PREN ≈ 18–20) in chloride; chloride still pits at oxide defects (Lund thesis; [MDPI Materials 2024](https://www.mdpi.com/1996-1944/17/24/6238)). Structurally: months-to-years in a damp block, fine.
- Bulk resistivity **0.72–0.74×10⁻⁶ Ω·m ≈ 43× copper** (304: 72 μΩ·cm; 316: 74 μΩ·cm) — trivial for signal leads (a 10 cm × 1 mm² run ≈ 0.7 mΩ), irrelevant.
- The real disqualification was already on file: **C17's Donnan-potential confound** on stainless needles — the semiconductor passive film at the metal/electrolyte junction is an unstable half-cell, i.e. it *adds* voltage noise and drift exactly where the nV–mV measurement lives. Stainless = good bones, bad ears. Use for structure, never for the sensing tip.

### A.5 The occupant is the corrosion engine — mycelium attacks copper *by name*

- Fungal biocorrosion of copper is dominated by **oxalic acid** (small dicarboxylic, strong chelator): NRL, "Understanding the Oxalic-Acid-Accelerated Corrosion of Copper"; bicarbonate leaches Cu from oxalate complexes so the protective copper-oxalate layer never stabilizes → continuous dissolution.
- **Mechanical attack is documented:** buried copper-shielded cables (36–42 yr) show initial pits forming *at hyphal tips*, which tunnel through the oxide into the metal (An et al. 2019, PubMed 33424137); *Alternaria alternata* mycelia cut deeper pits than their acid metabolites alone.
- **Pleurotus ostreatus — the cube's chosen inhabitant (CUBE1 stage 1) — is a wood-rotter and an oxalic-acid producer**, in the same guild as *Hypholoma/Serpula/Coniophora* named in proton-promoted copper-dissolution studies. This is not incidental exposure; it is a deliberately cultured oxalic-acid reactor wrapped around the wiring.
- Consequence for all four metals: organic-acid chelation + hyphal acid-concentration at the interface is the *specific* environment, warmer and more aggressive than generic "humid air." Bare copper fares worst; tin/oxygen/moisture formicary risk; silver is chelation-resistant (Ag-oxalate is poorly soluble, and Ag₂S/AgCl films self-limit); 316's Cr₂O₃ shrugs off oxalic at these concentrations (oxalic is actually used to *passivate* some steels' scale — though it will pit 304 over months).

### A.6 Tease-1 answers, stated plainly

| Corrupt film | Conductive? | Signal effect |
|---|---|---|
| Ag₂S (silver tarnish) | Semiconducting, orders of magnitude better than Cu oxides; soft, wipes/frits under contact (Alderete 2023, IEEE TCPMT) | Nuisance at connectors; near-nil on embedded bulk; Ag/AgCl conversion = the *preferred* electrode, already in CUBE1 BOM |
| Cu₂O/CuO (copper skin) | **Insulating** (10–14 orders jump; So 2012) | Series-R + drift + noise at every junction; kills contact over weeks |
| SnO/SnO₂ + carboxylates (tin) | Insulating; grows under organic-acid vapor; formicary tunnels | Endpoint contact-R rise over months; bulk under jacket fine |
| Cr₂O₃ (stainless passive) | Semiconducting film = junction potential + noise | Structurally fine; measurement confound at tips (C17 Donnan flag) |

---

## B. Printability — getting the metal into a printed block

### B.1 Conductive PLA / FDM filament (measured, printed-state)

| Filament | Filler | Volume resistivity (printed) | 10 cm × 2 × 0.4 mm trace ≈ | Cost |
|---|---|---|---|---|
| [Protopasta Conductive PLA](https://proto-pasta.com/pages/conductive-pla) | carbon black | 15 Ω·cm resin / **30 Ω·cm X-Y / 115 Ω·cm Z** | **≈ 3.75 kΩ** (X-Y) | ~$25–30/500 g |
| [Black Magic 3D graphene](https://www.blackmagic3d.com/product-p/graph-pla-p.html) | graphene | 0.6–1 Ω·cm spec; **5–10 Ω·cm real prints** | ≈ 75–125 Ω spec, **0.6–1.25 kΩ real** | ~$50/100 g |
| [Electrifi (Multi3D)](https://www.multi3dllc.com/product/electrifi/) | copper | **0.006 Ω·cm** (≈100,000 S/m) | **≈ 0.75 Ω** | **$119–215/100 g** — budget-killer |
| reference: copper wire | — | 1.68×10⁻⁶ Ω·cm | ≈ 0.2 mΩ | — |

- Print anisotropy is real (Z ≈ 4× worse than X-Y); layer interfaces are polymer joints, i.e. *moisture-sensitive resistance*. In a damp block the trace resistance is therefore **not just high, it drifts** with humidity — for a capacitive-touch toy that's fine; for nV–mV differential measurement, a drifting kΩ-scale series element is a calibration poison. Carbon/graphene PLA also cannot be soldered to (joints = clamped, oxide-prone).
- Verdict: conductive PLA is fine for *sensor-as-structure* (touch pads, resistive moisture probes, K4's composite story), **not** for measurement leads.

### B.2 Silver conductive epoxy / paint (post-print traces and joints)

- **MG Chemicals 8331** (now 8331D): 2-part silver epoxy, resistivity **7.0×10⁻³ Ω·cm** (8331 TDS) / **1.8×10⁻³ Ω·cm** (8331D); explicitly rated strong resistance to **humidity and salt water** — the right chemistry for the wet/dry boundary ([TDS via Mouser](https://www.mouser.com/datasheet/2/265/tds_8331D_2parts-3570156.pdf)). Cure: RT overnight-class (per TDS schedule); bonds PLA well.
- Price reality check: 14 g two-syringe kit lists $130–210 at industrial distributors (Hisco/RS) — street ~$30–40 at consumer channels (±, unverifiable today); you use drops, not pours, so 14 g is a *multi-year* supply for one cube.
- Conductive *paint* (silver or nickel acrylic, e.g. MG 8386-class / CW2200MTP): sheet resistance ~0.01–0.3 Ω/sq per mil — workable for post-print traces, but solvent carrier + acrylic binder = the least durable option in a 100%-RH organic box; use only outside the wet zone.

### B.3 Bare wire embedding mid-print (the zero-chemistry method)

- Standard practice on any FDM machine: **pause at layer N, lay wire into a printed trench/channel, resume** — the next layer welds PLA over the wire, giving a fully encapsulated trace with brass/copper/silver never exposed except at the exits. Design rules from community practice: trench ≥ wire diameter +0.2 mm, wire pre-formed flat/straight (or spiral for strain relief), leave 2–3 cm pigtail exiting through a planned grommet channel; PLA's ~60 °C glass transition is far above any block temperature, and the wire's thermal expansion is accommodated by the soft polymer. Works with any metal, including silver (soft — form the route, don't tension it).
- This is the only method where the *conductor metal choice is fully decoupled* from the printer — you get real metal conductivity (mΩ-class) inside a plastic body, for the price of a filament pause.

---

## C. ENIG cost at hobby tier (the FPC precedent's gold)

- The Fungal Potential Card (iScience) precedent — 8× gold differential pads on a PCB the mycelium colonizes in 3–4 days — is a standard 2-layer board with **ENIG** (Electroless Nickel Immersion Gold: ~0.05–0.1 µm Au over 3–6 µm Ni barrier), not hard gold.
- **JLCPCB-class pricing:** ENIG is **no longer free** (OSP took the free slot; lead-free HASL is default). Field numbers: **≈ $16.50 flat upcharge per order** (EEVblog thread, 100×100 mm ×5) ≈ **$3.30/board** on a 5-pack; JLCPCB's own blog pegs ENIG at **5–15% of bare-board cost**, hard **gold fingers at 20–50%+** premium ([JLCPCB hard-gold blog](https://jlcpcb.com/blog/hard-gold-pcb-finish); [EEVblog](https://www.eevblog.com/forum/manufacture/gold-plating-hasl-edge-connector/)). Reddit r/PCB datapoint: hard-gold card-edge on a 6-layer ×10 order ≈ $600.
- Bottom line: **ENIG pads on a card = +$3–4 per board, hobby-cheap, and gold doesn't tarnish in oxalic mist — the card outlives the experiment.** Hard-gold *fingers* are for insertion cycles; a cube card has none, so skip them. Gold's real role here is the *endpoint*: an ENIG pad is the ideal dry-side landing for the embedded silver/insulated lead.

---

## VERDICT

### Materials decision table

| Metal / route | Corrosion behavior in damp living substrate | Cost for a cube's worth | Print-integration method |
|---|---|---|---|
| **Fine silver wire (.999, 26 AWG)** | Best-in-class: Ag₂S tarnish semiconducting but self-limiting; oxalic/chelation-resistant; tip chlorinates to Ag/AgCl = the *correct* electrode | ~$2–3.6/ft → **$7–12** for 0.5–1 m (fits the $5–10 chloridized-silver BOM line) | Mid-print trench embed (pause-at-layer); exit via sealed gland; solder dry-side |
| **Tinned-copper hookup wire (silicone/PTFE jacket)** | Jacket = the actual barrier; metal never touches substrate; formicary risk only where stripped; endpoints worst | ~$5 drawer stock | Mid-print embed or simple run-through; seal exits with epoxy/hot-melt |
| **Bare copper** | Insulating Cu₂O/CuO skin in days–weeks; hyphal pitting documented; oxalic acid dissolves continuously | free | Any — but don't |
| **Tinned copper, exposed** | SnO₂/carboxylate films at exposed points; formicary tunnels over months | ~$5 | Mid-print embed, seal every joint |
| **316 stainless** | Passive film self-heals; structurally months–years; *junction-potential noise at sensing tips* (C17 confound) | ~$3–5 (syringe needles) | Mid-print embed as structure/ground only |
| **ENIG PCB card (FPC precedent)** | Gold: inert; Ni barrier stops Cu migration; outlives the grow cycle | +$16.50/order ≈ $3.30/board (qty 5) | N/A (it *is* the substrate wall); wire it with silver |
| **Conductive PLA (carbon/graphene)** | Polymer swells; resistance drifts with moisture; unsolderable | $25–50 spool | Print in place; touch/moisture sensing only |
| **Conductive PLA (Electrifi Cu)** | Electrically real (0.75 Ω/trace) but copper chemistry in oxalic mist | **$119+/100 g** — busts the $60 cube | Print in place |
| **Silver epoxy (MG 8331D)** | Humidity/salt-rated; metal in polymer = protected | ~$30–40/14 g, drops only | Post-print traces; glue/joint at wet-dry boundary |

### Recommended trace material for the $60 cube

**Fine silver wire is the trace AND the electrode — one material, two jobs.** Embed 26 AWG .999 silver in mid-print PLA trenches (pause-at-layer; costs only a filament swap), run each lead through a sealed gland to the dry electronics bay, solder or screw to the ADS1115, and chloridize the in-block tips into Ag/AgCl (bleach/DIY, already a CUBE1 skeptic-rider line). Rationale: (1) the metal already in the budget ($5–10 line) is the one that both survives oxalic mist and forms the reference-grade electrode; (2) bulk silver tarnish is electrically near-invisible, so an unchloridized mid-run is harmless; (3) every *connector-grade* failure mode is engineered to live on the dry side of the gland. **Silicone-jacketed tinned-copper** handles all non-sensing runs (the jacket, not the tin, is the barrier). 316 stainless needles stay out of the signal path (Donnan confound, C17). Conductive PLA is disqualified for measurement paths — its resistance is not just kΩ-scale, it *drifts with the very humidity you're studying*. ENIG card = the upgrade when the cube becomes a clonable card (+$3.30/board; skip hard-gold fingers).

### Honest lifespan estimate before contact degradation

- **Dry-side joints (solder/screw, sealed):** 12+ months; the gland seal, not the metal, is what ages.
- **In-block silver bulk:** years (tarnish film self-limits at nm-scale indoors; chelation-resistant) — it will outlive the experiment.
- **The true service item is the electrode tip:** Ag/AgCl chloridization degrades over **~4–12 weeks** of continuous immersion-class contact (gel-pad hospital electrodes dry out in *days* and are consumables — swap the pad, keep the wire; bare chloridized tips hold the low-frequency fungal band longer). Plan: **re-chloridize or swap tips every 1–3 months**; budget 30 minutes/cycle.
- **Bare-copper counterfactual, for the record:** measurably degraded junctions in **2–8 weeks** (insulating oxide + oxalic dissolution + hyphal pitting), i.e. the naive build dies roughly when the first flush fruits.
- **ENIG card path:** pads effectively immortal on experiment timescales; lifespan bounded by epoxy encapsulation and biology, not metal — the FPC card's colonization-to-data window (3–4 days to colonize, weeks of monitoring) fits inside a *years* material envelope.
- Net: **design for ~6–12 months between contact-intervention events**, with the tips (not the traces) as the wear part. Anything claiming months of zero-maintenance bare-copper contact in a living box is contradicted by the contact-engineering and biocorrosion literature above.

---

*Filed under wave-lane law: receipt first, appended as evidence landed. No git, no paid APIs. Lane convention note: sibling K-receipts do not append index_events; INDEX fold (v3) may classify this file on next derivation. Writer: zcode-wave-k3.*
