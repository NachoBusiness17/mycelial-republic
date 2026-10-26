# K10 — MYCELIAL STEERING TOOLKIT (receipt, append-as-you-go)

- **Lane:** K10 (wave-lane law: receipt first, append as you go; no git; no paid APIs)
- **Date opened:** 2026-09-16
- **Mission:** Survey and rank ALL known growth-steering levers for mycelium, for the printed block (cube-2 zone-line engineering).
- **Levers in scope:** (1) chemotaxis / nutrient gradients, (2) galvanotaxis / DC fields (integration view — K2 lane holds the deep electrophysiology; K10 holds read-write dual-use + electrode placement), (3) phototropism / blue light, (4) mechanical / thigmotropism (grooves, channels), (5) moisture gradients.
- **Per-lever contract:** evidence strength (published / nickname / folklore), timescale, cost, composes-with-printed-geometry verdict.
- **Required ending:** toolkit ranked by evidence × cost · recommended COMBINATION for cube-2 zone-line engineering · the one lever the literature has never tried on mycelium.

---

## Findings log

### LEVER 1 — CHEMOTAXIS (nutrient gradients) — appended 2026-09-16

**Flagship (verified live, Europe PMC REST, DOI checked):** Yamamoto R, Miki H, Itani A, Takeshita N (2024) "Hyphae of the fungus *Aspergillus nidulans* demonstrate chemotropism to nutrients and pH." *PLoS Biol* 22(7):e3002726, DOI 10.1371/journal.pbio.3002726, PMC11288418, open access.

Key facts from abstract (read directly):
- Microfluidic two-layer laminar-flow assay: hyphae choose growth direction between adjacent non-mixing flows.
- **Positive chemotropism to carbon**: hyphae change growth direction to REMAIN in the carbon-source flow (vs no-carbon control).
- **NEGATIVE chemotropism to nitrogen**: hyphae steer to AVOID ammonia/nitrate flows, transporter-dependent. Counterintuitive and load-bearing: nitrogen is NOT a tip-level attractant even though it is required for growth.
- **Chemotropism to acidic pH** (attract to low pH), PmaA proton-pump-dependent; growth-rate effects explicitly separated from directional effects.
- Direction decision happens AT the hyphal tip, not via colony-level metabolism.

**Consequences for printed-block steering (K10 analysis):**
- C/N ratio is not just a growth-rate dial — it is a DIRECTION dial, and the two axes point opposite ways: carbon attracts, nitrogen can repel. A printed substrate can lay a carbon-rich lane and a nitrogen-rich lane and get a push-pull pair: hyphae crowd into the carbon lane and veer off the nitrogen lane. The line where an attractor lane meets a repeller lane is where a boundary WANTS to form — zone-line placement by ink formulation.
- Caveat: Yamamoto 2024 is *A. nidulans* (ascomycete, microfluidic scale). Our species are basidiomycetes (per G-B) in bulk substrate — evidence transfers as mechanism, not as numbers. Basidiomycete-specific chemotropism numbers: open gap.

**Evidence tier (chemotaxis):** PUBLISHED (strong at hyphal scale, ascomycetes; mechanism-level transfer to basidiomycetes).

---

### LEVER 2 — GALVANOTAXIS (DC fields) — INTEGRATION VIEW (deep science = sibling lane K2) — appended 2026-09-16

K10 scope: not the electrophysiology canon (K2 owns it) but WHERE electrodes live for steering and whether READ and WRITE share traces.

**Read-side anchor (verified live):** Adamatzky A (2026) "Propagation of electrical spike trains in substrates colonised by oyster fungi," *Sci Rep*, DOI 10.1038/s41598-026-47035-2. Eight differential channels as a linear array IN SUBSTRATE, 15-day recording @1 Hz, spikes mV-scale, **directional propagation ~0.7 cm/min (~40 cm/h) between channels ~2 cm apart** — ionic wave dynamics, shuffled controls passed. This is OUR species (*Pleurotus*), OUR geometry (substrate-embedded array). The 2 cm channel pitch is the natural steering electrode pitch.

**Where electrodes live for steering (K10 analysis):**
- At the zone-line FLANKS, bracketing the seam — not on it. G-C's hypothesis is that the boundary is the active region; steering electrodes sit 1–2 cm upstream of the desired line and bias the fronts toward it. Read pairs straddle the line (G-C design); write pairs bracket it. Same array can do both roles positionally.
- Bulk wet substrate is an ionic conductor: current follows moisture, so electrode placement inherits the moisture lever's map — steer where it is wet, or wet where you steer (the levers couple).

**Read-write dual-use (K10 analysis):**
- READ (C17 rig: ECG pads / sub-dermal needles → ADS1115 differential) is high-impedance, AC/spike-band. WRITE (galvanotropism DC bias) is low-impedance, DC/low-frequency. Electrically shareable with a series capacitor + T-switch per trace (~$2); or duty-cycled: write bursts between read windows.
- Standard practice in neural engineering (DBS, cochlear implants: same-electrode record+stimulate). **Never published for mycelium** — closest prior art (Telhan 2025 PEDOT mycelium chips, Adamatzky 2026 substrate arrays) is read-only. The dual-use step is K10-original.
- Write-side hard requirements: current limiting (<1 mA class) and electrolysis management (buffer/salt-bridge electrodes) — bare-DC into wet substrate etches electrodes and shifts pH.

**Cross-lever interaction (important):** the electrolysis byproduct front is a pH front, and hyphae steer toward acidic pH (Yamamoto 2024). So galvanotaxis may partly BE chemotaxis-by-byproduct in our block. They compose, but attribution confounds any K2 falsifier — pH must be instrumented or bridged out.

**Evidence tier:** PUBLISHED at agar/hyphal scale (classical galvanotropism canon; numbers pending K2). INTEGRATION (steer-in-3D-printed-block via embedded traces): unpublished.
**Timescale:** tip turn minutes–hours (canon); block-front redirection days.
**Cost:** ~$0 incremental — the C17 read rig already exists; write side is a MOSFET + current-limit + bridge electrodes.
**Composes with printed geometry:** yes — traces ARE printed geometry; the only lever that shares hardware with the sensor layer.

---

### LEVER 3 — PHOTOTROPISM (blue light) — appended 2026-09-16

**Verified live searches:**
- Exact phrase **"hyphal phototropism": 0 hits** in Europe PMC. The term essentially does not exist for hyphae — evidence by absence.
- Umbrella review (verified): "How fungi see the world: fungal photoreceptors and their role in the regulation of fungal biology," *Microbiol Mol Biol Rev* 2025, DOI 10.1128/mmbr.00149-22 — photoreceptors (White Collar, cryptochromes, opsins) regulate development broadly.
- OUR species, verified: "The blue light receptor gene PoWC-1 plays a role in the formation of *Pleurotus ostreatus* primordia," *Can J Microbiol* 2026, DOI 10.1139/cjm-2026-0052 — blue light gates FRUITING INITIATION, not hyphal direction.
- Canon-knowledge (not re-fetched, flag): *Phycomyces blakesleeanus* sporangiophore phototropism is the classic extreme-sensitivity system (blue light, thresholds near 10⁻⁹ W/m² in old literature) — but sporangiophores are zygomycete fruiting structures, not vegetative basidiomycete mycelium.

**K10 verdict:** light is a DEVELOPMENTAL trigger (pinning, pigmentation, photolyase damage response) and a WEAK or unproven directional cue for vegetative basidiomycete hyphae. For zone-line engineering its real role is INDUCTION, not placement: zone lines are pigmented/melanized structures (Wei 2023, carried from G-B), and light exposure plausibly darkens/hardens a chosen seam after it forms.
**Evidence tier:** PUBLISHED for fruiting structures/zygomycete sporangiophores; NICKNAME for vegetative-hyphae steering (mechanism exists, direction evidence absent); FOLKLORE for "mushrooms grow toward the window."
**Timescale:** hours–days (developmental). **Cost:** $2–5 (blue LED).
**Composes with printed geometry:** only via optical windows or printed light pipes (O2/O3 lanes) — the block is opaque, so surface light cannot reach interior hyphae at all. That failure is itself the never-tried lever (see final section).

---

### LEVER 4 — MECHANICAL (thigmotropism: grooves, channels, pores) — appended 2026-09-16

**Verified live:**
- Montiel-Rubies G, Held M, … Nicolau DV (2025) "Hierarchical Structure of the Program Used by Filamentous Fungi to Navigate in Confining Microenvironments," *Biomimetics* 10(5):287, DOI 10.3390/biomimetics10050287. Microfluidic navigation by THREE species including **basidiomycetes** (*Pycnoporus cinnabarinus*, *Armillaria mellea*) plus *Neurospora*. Hyphae: (i) sense narrow passages remotely or by contact; (ii) keep DIRECTIONAL MEMORY (continue straight); (iii) branch on collision; (iv) negative autotropism between branches; (v) anastomosis as robustness subroutine.
- Review canon (verified): "Thigmo Responses: The Fungal Sense of Touch," *Microbiol Spectr* 2017, DOI 10.1128/microbiolspec.funk-0040-2016.
- Mechanism (verified): "Regulation of vectorial supply of vesicles to the hyphal tip determines thigmotropism in *Neurospora crassa*," *Fungal Biol* 2014, DOI 10.1016/j.funbio.2013.12.007 — thigmotropism has a defined cell-biological mechanism (tip vesicle traffic), not just correlation.
- Plant-pathogen tradition: germ tubes track leaf-surface ridges toward stomata (classic canon; synthetic-substrate replication verified: Botrytis vs tomato microstructure, *Front Plant Sci* 2022, DOI 10.3389/fpls.2022.1023502).

**K10 verdict:** YES — hyphae follow grooves/ridges/channels; this is the strongest published, geometry-native lever, and it is proven in BASIDIOMYCETES at channel scale. The Biomimetics programs (narrow-passage sensing + directional memory) mean a printed groove does not just permit a path, it PULLS the tip (contact/remote sensing) and then HOLDS it (memory).
**Evidence tier:** PUBLISHED (strong; includes basidiomycetes).
**Timescale:** continuous/instant — it acts on every tip every minute.
**Cost:** $0 — it IS the print. **Composes with printed geometry:** perfectly; the lever and the geometry are the same object.

---

### LEVER 5 — MOISTURE (moisture gradients as steering) — appended 2026-09-16

**Verified live:**
- Guhr A, et al. (2015) "Redistribution of soil water by a saprotrophic fungus enhances carbon mineralization," *PNAS* 112(49), DOI 10.1073/pnas.1514435112 — a saprotrophic network actively moves water through hyphae to bridge dry zones: hyphae don't just follow moisture gradients, they MANUFACTURE them.
- Canon review (verified): "The Mycelium as a Network," *Microbiol Spectr* 2017, DOI 10.1128/microbiolspec.funk-0033-2017.
- Cord-forming ecology (canon, Boddy/Wells line): hyphal cords translocate water across air gaps to reach new substrate — the grower-empirical "damp spot gets colonized first" has a formal mechanism behind it.
- Industry tier: mycelium-composite process reviews (verified e.g. *Polymers* 2026, DOI 10.3390/polym18131652) treat moisture content as THE process variable — anisotropic growth vs hydration is standard fabrication knowledge (cf. also *ACS Appl Bio Mater* 2025 anisotropic growth in wood hydrogels, DOI 10.1021/acsabm.5c00374).

**K10 verdict:** the strongest GROWER-EMPIRICAL lever and the least formally tested as a directional tool at tip scale. Hyphae reliably colonize along wet lanes and stall at dry seams (dry seam = containment tool too, not just wet lane = attractor).
**Evidence tier:** PUBLISHED at network/ecosystem scale (water redistribution); GROWER-EMPIRICAL at steering scale (universal practice, few controlled directional studies); FOLKLORE nowhere — it survives contact with growers.
**Timescale:** hours–days. **Cost:** $0–3 (mister, drip wick, printed wicking lane).
**Composes with printed geometry:** excellent — printed wicking channels and porosity gradients carry the gradient; and moisture couples to the electrical lever (ionic conduction paths).

---

### BONUS LEVERS (completeness sweep) — appended 2026-09-16

- **CO2/aerotropism:** CO2 sensing and hyphal response published at yeast/germ-tube scale (medically relevant fungi; verified umbrella: *Med Gas Res* 2026 review, DOI 10.4103/mgr.medgasres-d-26-00038). Basidiomycete directional steering: thin. Composes free with printed vent channels. Tier: NICKNAME (for our species).
- **Thermotropism:** old literature (zygomycete canon), poorly indexed (15 hits, mostly noise); a heat gradient doubles as a drying gradient, so it is mostly the moisture lever wearing a coat. Tier: NICKNAME. Printed resistive traces could dose it, but why.
- **Gravity:** published review exists ("Fungal graviresponses," *Fungal Biol Biotechnol* 2025, DOI 10.1080/21501203.2025.2474154) — relevant to fruiting-body orientation; vegetative hyphae at our scale ignore it. Tier: PUBLISHED, IRRELEVANT for cube-2.
- **Volatile gradients:** fungal VOCs (1-octen-3-ol etc.) modulate growth and inter-fungal interactions; directional steering by printed volatile lanes unpublished. Tier: NICKNAME at steering scale.

---

## FINAL SYNTHESIS — appended 2026-09-16

### The steering toolkit, ranked by evidence × cost × composition-with-print

| Rank | Lever | Evidence | Cost | Composes w/ print | Timescale | One-line |
|---|---|---|---|---|---|---|
| 1 | MECHANICAL (grooves/channels/seams) | Published, basidiomycete-proven in channels | $0 | It IS the print | continuous | Narrow-passage sensing + directional memory pull AND hold tips (Montiel-Rubies 2025) |
| 2 | CHEMOTAXIS (C/N ink lanes) | Published, strong mechanism (ascomycete flagship); basidiomycete numbers open | $0–5 | Ink formulation = print | hours–days | Carbon attracts, nitrogen repels: push-pull pair draws the boundary line (Yamamoto 2024) |
| 3 | MOISTURE (wet/dry lanes) | Network-scale published + strongest grower-empirical | $0–3 | Wicking lanes/porosity | hours–days | Hyphae follow wet lanes; dry seams contain; network self-manufactures gradients (PNAS 2015) |
| 4 | GALVANOTAXIS (embedded DC traces) | Published on agar-scale hyphae (K2 verifying); in-block steering unpublished | ~$0 incremental (C17 rig exists) | Traces = printed hardware | min–hours (tip), days (front) | Read-write dual-use is novel; beware pH-byproduct confound (composes WITH chemotaxis) |
| 5 | PHOTOTROPISM (blue light) | Published for fruiting structures; vegetative-hyphae steering ~absent (0 exact-phrase hits) | $2–5 | Needs windows/waveguides | hours–days (developmental) | INDUCTION lever (pinning/pigmentation), not a placement lever |

### Recommended COMBINATION for cube-2 zone-line engineering

Steer with the passive, published, $0 levers; observe with the electrical rig; write electrically only if passive steering under-shoots; use light for induction, not placement.

1. **Placement — MECHANICAL base layer:** print the target zone-line path as a groove/porosity seam. The tip's narrow-passage sensing homes to it; directional memory keeps fronts parallel; the seam also doubles as the printed feature G-C already plans electrodes around.
2. **Attraction/repulsion — CHEMOTAXIS ink pair:** carbon-rich lane along the seam, nitrogen-lean (higher C/N) flanks. Push-pull concentrates growth exactly on the seam; at the boundary contact itself the co-culture barrage chemistry (G-B canon: Wei 2023; MAPK stalemate 2026, DOI 10.3390/jof12050327) maintains the line once formed.
3. **Lock-in — MOISTURE:** wick along the seam (wet lane attracts, self-reinforcing via network water redistribution); keep flanks drier for containment. This also guarantees ionic paths for the electrical layer.
4. **Induction — PHOTOTROPISM (re-purposed):** small blue-LED window over the seam AFTER contact to promote pigmentation/darkening of the zone line (developmental lever applied where it is actually strong).
5. **Calibration/actuation of last resort — GALVANOTAXIS:** the existing differential channels straddle the seam (read, G-C design); if the passive combination misplaces the line, duty-cycled DC write bursts from flank pairs nudge the front. Same-trace read-write with a series-cap/T-switch is the phase-2 upgrade — and the pH front it makes is itself a steering agent (instrument or bridge it).

Pre-register the falsifier: printed-seam + C/N + wetting places the zone line within ±X mm of the seam (camera diff, G-C tracker) vs printed-seam-only control; electrical write arm only arms if passive placement fails its own pre-registered window.

### The one lever the literature has never tried on mycelium

**Interior phototropism: blue light piped through printed waveguide channels to steer hyphal growth deep inside an opaque 3D substrate.**
- All light-fungus canon is surface-level: agar plates, sporangiophores, fruiting bodies, transparent microfluidics. "Hyphal phototropism" has ZERO Europe PMC exact-phrase hits.
- An opaque block makes exterior light useless for interior steering; an embedded printed waveguide (O2/O3 lanes already verify waveguides and optical integration) delivers a directional cue to exactly the tips you want — light becomes a PRINTABLE, locally addressable steering layer, uniquely strong where mechanical grooves cannot go (across open volume) and chemotaxis is slow to reconfigure.
- Receptors exist in our species (PoWC-1 in *P. ostreatus*, verified 2026) — the biology is installed, the delivery has never been built.
- Runner-up: same-electrode closed-loop read-AND-write steering on printed traces (standard in neuroengineering, never on mycelium) — K2/K10 phase-2.

---

**Lane close:** receipt complete 2026-09-16. Live-verified citations: Yamamoto 2024 (PLoS Biol), Montiel-Rubies 2025 (Biomimetics), Thigmo review 2017 (Microbiol Spectr), vesicle-thigmotropism 2014 (Fungal Biol), Mycelium-as-Network 2017 (Microbiol Spectr), Guhr 2015 (PNAS), photoreceptor review 2025 (MMBR), PoWC-1 2026 (Can J Microbiol), Adamatzky 2026 substrate spike propagation (Sci Rep), barrage MAPK stalemate 2026 (J Fungi), chemotropism 3D-print assay 2020 (Front Microbiol, DOI 10.3389/fmicb.2020.584525), graviresponses 2025, myco-composite process review 2026 (Polymers), anisotropic wood-hydrogel growth 2025 (ACS ABM). Canon-knowledge flagged inline where not re-fetched (Phycomyces thresholds, Boddy cord-water line, Hoch rust-ridge tradition, DBS record-stimulate practice). K2 dependency: DC field threshold numbers deliberately NOT duplicated here — sibling lane owns them.
