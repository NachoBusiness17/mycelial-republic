# O3 — OPTICAL INTEGRATION (fiber add-on to a fully colonized mycelium tub)

- **Lane:** wave / physical_computing
- **Opened:** 2026-09-16
- **Status:** WAVE-OPEN (appended as researched; receipt-first law)
- **Method:** web lit-research only (no paid APIs), hobby-tier parts, no git
- **Question:** if fibers go into a fully colonized mycelium tub, what does the integration actually look like?

## §0 Scope

Four deliverables: (1) OPTICAL WRITE evidence from published fungal light responses — wavelength / intensity / pulse structure, and whether a $5 laser diode + $3 LED set suffices; (2) FIBER FEEDTHROUGH — sterile port design for post-colonization insertion; (3) READOUT — hobby-tier fiber photometry (LED + photodiode through the same fiber); (4) INTEGRATION SPEC — entry points, fiber count, spacing vs electrode grid, and the falsifier with S3 skeptic controls.

Receipts appended below as each section completes. Ends with: §BOM ($40-class), §DRAWING, §CONTROLS.

---

## Search log (append as you go)

- [x] Q1: Adamatzky light-response paper hunt — done 2026-09-16 (findings below)
- [x] Q2: WC-1 / white-collar action spectrum — done 2026-09-16 (rate-limited partial; numbers below)
- [x] Q3: Phycomyces action spectrum (Delbrück & Shropshire 1960) — done 2026-09-16
- [x] Q4: injection-port tek (grow community) — done 2026-09-16
- [x] Q5: hobby fiber photometry cheapest lineage — done 2026-09-16
- [x] Q6: blue-LED mycelium growth study (intensity units) — done 2026-09-16

## Finding 1 — Adamatzky 2022 is a passive recording, NOT the light paper (2026-09-16)

Checked primary text: Adamatzky 2022, *R. Soc. Open Sci.* 9:211926 ("Language of fungi...") recorded **spontaneous** activity in darkness — no optical stimulation experiments, no wavelength/intensity anywhere. Its intro cites prior work claiming fungi "respond to mechanical, chemical and optical stimulation by changing pattern of its electrically activity" → pointers: **Adamatzky et al. 2021 "Fungal sensing skin"** and **"Reactive fungal wearable"** (Biosystems 2021 lineage). The optical-stim parameter hunt continues in those papers (Finding 2).

**What 2022 DOES give (rig baseline to match):** iridium-coated stainless-steel sub-dermal needle electrodes (Spes Medica), differential twisted pairs, 1–2 cm inter-electrode spacing, Pico ADC-24 (24-bit, galvanically isolated), range 78 mV, 1 saved sample/s, 21 °C, ~80 % RH, dark. Four species incl. *Schizophyllum commune* + *Flammulina velutipes* — the two most hobby-available.

## Finding 2 — ⚠️ RETRACTION in the Adamatzky optical-stim lineage (2026-09-16)

The papers Adamatzky 2022 cites for "fungi respond to… optical stimulation" resolve to **"Fungal sensing skin"** (Adamatzky, Gandia, Chiolerio, *Fungal Biol Biotechnol* 8:3, 2021-03-17, PMID 33731205) — which is **RETRACTED** (retraction note: same journal 8:7, 2021-06-02, PMID 34078474, **no stated reason** in the notice). Its abstract did claim the mycelium sheet "reacts differently to… switching illumination on and off" (light on/off, no wavelength/intensity ever published). Successor paper: "Fungal skin for robots" (Biosystems 2024, PMID 38128872). **Receipt consequence:** the only citable optical-evoked-response evidence must come from outside that retracted lineage → Finding 4 (which independently supplies it).

## Finding 3 — Photobiology sets the write channel: blue/near-UV only, µmol-level thresholds (2026-09-16)

**Receptors.** Fungal blue-light sensing runs on LOV-domain flavoproteins (FAD chromophore): **WC-1/WC-2** White Collar Complex (*Neurospora*), **BLR-1/BLR-2** (*Trichoderma*), **MadA/MadB** (*Phycomyces*). Action spectra: peak **~450–480 nm** blue + near-UV shoulder **~370–390 nm**, sensitivity collapsing above ~500–510 nm (classic Delbrück & Shropshire 1960, *Plant Physiol* 35:642 — *Phycomyces* "three-fingered" spectrum, peaks ~280/~385/~455–475 nm, no phototropic response >510 nm; Hardy et al. 1989 — *Neurospora* carotenogenesis action spectrum, peak ~460 nm). Numbers above the ~500 nm cutoff are synthesis from search-engine literature summaries consistent with the classic texts; peak positions are textbook-stable.

**Doses.**
- *Neurospora* photoresponses are **fluence-based (Bunsen–Roscoe reciprocity)**: single brief pulses work; frq induction saturates around ~1 W·s/m² ≈ **3–4 µmol/m²** at 460 nm; thresholds well below 1 µmol/m².
- *Phycomyces* phototropism threshold ≈ 10⁻⁸ Einstein·m⁻² ≈ **0.01 µmol/m²** (near-UV peak).
- Living-colony growth effect (primary, fetched): **Hericium erinaceus on sorghum grain — 450 nm LED, 40 ± 5 µmol m⁻² s⁻¹, 8 h/day × 30 d** → fastest colonization (day 15 vs day 30 dark), +76 % mycelial density (PMC12689372). This doubles as a warning: continuous blue writes change growth *phenotype*, so write dose must be pulsed and logged.

**Link budget for a $3 LED.** 1 µmol m⁻² s⁻¹ @ 470 nm = 25.5 µW/cm². A 20 mA 5 mm blue LED butt-coupled into 1 mm POF yields ~50–200 µW at the fiber tip; as a point source at 5 mm radius (≈0.3 cm²) that is ~0.2–0.7 mW/cm² ≈ **8–25 µmol m⁻² s⁻¹** — same order as the 40 µmol growth-effective dose and 1–3 orders above receptor thresholds. A 10 s pulse ≈ 80–250 µmol/m² ≈ 0.02–0.06 % of one Hericium photoperiod day. **Verdict: LED is sufficient; the laser buys nothing biologically.**

## Finding 4 — Light → electrical response in mycelium: the citable evidence (2026-09-16)

| Paper | Stimulus | Measured response |
|---|---|---|
| **Mishra et al. 2024, Science Robotics 9:eadk8019** (Cornell; open PDF: par.nsf.gov/servlets/purl/10548775) | UV + wavelength screen on *Pleurotus eryngii* mycelium on a 3D-printed scaffold with embedded electrodes, shielded EMI/vibration interface | Full text (via index snippet): *"at longer wavelengths beyond UV, our mycelium scaffold only responded to blue light stimulation, with 'V-light' potentials"* — used to actuate robots. **Blue-only specificity at long wavelengths = exactly our sham design assumption.** Gap: exact nm/irradiance/pulse numbers not recovered (11.7 MB PDF exceeds fetch limit) — treat as open. |
| **Levina, Dunina-Barkovskaya, Shabala, Lew 2002, J Membr Biol** (PMID 12181612) | "Blue light", patch-clamped *Neurospora* slime mutant | Conductance **decreases within 2–5 min**, reversal potential shifts negative (Cl⁻ conductance becomes dominant, K⁺ drops); vibrating probe: ↑K⁺ efflux, ↑Cl⁻ influx within 5 min. |
| **Grenader et al. 1982, Biofizika** (PMID 7138947) | blue-violet illumination, *Neurospora* microelectrodes | **Transient hyperpolarization, additional −38 ± 5 mV at 25 min** (resting −156 mV). |
| Adamatzky 2022 RSOS 9:211926 | none (passive, darkness) | Hardware baseline only (see Finding 1). |
| "Fungal sensing skin" 2021 | light on/off | **RETRACTED — do not cite** (Finding 2). |

Pulse-structure synthesis for the spec: photoreceptor responses follow fluence reciprocity (Finding 3) and run 2–5 min (conductance) to tens of minutes (hyperpolarization) — so **pulse trains of seconds with minutes of gap are the literature-matched write pattern**, not kHz stimulation. Latency expectation for a real response: ≥ tens of seconds, NOT instantaneous.

---

## Finding 5 — FIBER FEEDTHROUGH: the grow community already solved sterile post-colonization access (2026-09-16)

**Precedent (verified).** Unicorn Bags ships commercial **"Injector Port Bags"** (unicornbags.com, confirmed product category) — the standard spawn-production vessel. Community DIY tek (r/MushroomGrowers, Shroomery, vendor guides: zombiemyco.com, out-grow.com, coloradoculturesllc.com, YouTube "self-healing injection port lid" builds): **melt/punch a hole in lid or bag → high-temp RTV silicone poured in layers, sandwiched between polyethylene/plastic films → cure → a self-healing port that reseals after each needle pass**; sterilized in the normal pressure-cooker cycle; 70 % IPA swab before each piercing. Hospital analogue: butyl-rubber septum (injection port), identical mechanics, ~$0.30/pc.

**Adaptation for a fiber (not a one-shot needle).** The fiber stays in permanently, so the port must seal *around* the fiber:
1. **Port**: lid hole (8–10 mm) + cured RTV silicone disk (community SIP recipe) or commercial butyl septum pressed into a grommet. Sterilize in place with the tub's standard care cycle or IPA/UV-C.
2. **Insertion (post-colonization)**: 70 % IPA swab of port; pre-sterilize fiber run (70 % EtOH or 6 % H₂O₂ soak 30 min, air-dry in a covered sterile dish — **no flame, no autoclave**: 1 mm PMMA POF service temp ≈ 70–85 °C, it will slump); pierce port with fiber (optionally through a blunt 16G needle as a guide sleeve); seal the fiber/port interface with a dab of sterile silicone grease (kills wicking, the one real contamination path: moisture climbing the fiber–septum junction).
3. **Geometric seal**: fibers pass through a **compression grommet** (nylon bulkhead fitting + silicone washer) above the septum so neither fiber nor port takes bending load.

**Entry choice — LID, not side wall.** Lid entry: ports live in the headspace, away from wet substrate; no condensation channel along the port; fibers hang plumb to a fixed depth; fruiting bodies don't crush them; all optics mounts on one bracket on the lid. Side entry buys a horizontal beam geometry we don't need (mycelium is a diffuser — see O2 receipt — so in-plane vs vertical matters little) and costs a wet contamination path.

## Finding 6 — READOUT: what fiber photometry looks like when you strip it to the studs (2026-09-16)

The neuroscience lineage, cheapest-first:
- Commercial floor (Doric-class): **~$17k** (Simone et al. 2018 cost table).
- **Simone et al. 2018, Neurophotonics, "CICLoPS"** (PMC5895965) — the classic "cheap" build: still ~**$6.9k** (PMT $2.8k + cage optics $2.1k + DAQ $1.8k). But its headline result is the physics gift: **SNR 231 at only 100 nW of 465 nm excitation at the fiber tip** — GFP-class fluorescence detection needs nW. 465 nm LED, modulated at 211 Hz to dodge mains harmonics, dichroic 495LP, PMT + 100 MΩ TIA.
- **pyPhotometry (Akam et al. 2019, eNeuro)** — the hobby standard: acquisition board **€364 assembled / buildable for ~$50–100 from the published BOM**, built-in LED drivers, PyBoard, open everything (pyphotometry.readthedocs.io).
- Our case is even easier than all of them: **no fluorophore**. We read reflectance/backscatter, where the returned power is μW–mW, not nW — so filters, dichroics, PMTs, and lock-ins all delete. The floor is a **$2 LED + $1 BPW34 photodiode + single op-amp TIA + $5 MCU ADC** (the pulse-oximeter architecture). One honest physics note from O2 (Carrillo-Acuña 2023 APL): mycelium converts transmitted light to Lambertian speckle — so the readout signal is diffuse backscatter, sensitive to density/geometry/hydration at the tip neighborhood, which is exactly the proxy channel: **write blue → photoreceptor-driven morphology/ion changes → change in red backscatter (and electrode band power) → detect**.

**Wavelength discipline:** the readout illuminator MUST be 650 nm red, not blue — blue would be a continuous write dose on the WC-1/BLR action spectrum. Red sits past the ~510 nm cutoff (Finding 3) and past Mishra's blue-only response edge (Finding 4): read light is optogenetically inert by construction. A $1 red gel filter on the PD blocks write-channel crosstalk; sampling is gated out of write pulses anyway.

---

## §INTEGRATION SPEC (the engineering answer)

**Tub assumption:** standard monotub (~50 L), fully colonized (grain/cvG substrate), lid sealed, kept dark except fiber tips (ambient light is itself a stimulus — WC-1 sees it).

**Fiber complement: 2 write + 1 read pair (= 4 fibers / 4 lid ports).** The mission's "2 write + 2 read" is the $50 build; the $40 build runs one read pair (R-ill + R-col). Layout along the tub long axis, 10 cm spacing, all at **depth 1.5 cm** (same plane as electrode tips):

```
TOP VIEW (lid underside)          W1        E1      R-ill  R-col        E2        W2
length axis ──────────────────────●─────────▶───────●──────●◀───────────▶─────────●──────
                                  │write     │pair   │read pair (5 mm gap, fixed comb) │pair  │write
side view: all fibers vertical, tips at −1.5 cm; electrode pairs horizontal, same depth
```

- **W1, W2 (write):** 1 mm POF, blue 470 nm LED outside the lid butt-coupled (heat-sinked LED, zero heat into tub), each fiber independently PWM-switched. Pulse grammar (Finding 3/4): 1 s / 10 s / 100 s pulses, ≥ 60 min between pulses, fluence ladder for dose-response.
- **Read pair (R-ill → R-col):** red 650 nm LED (continuous, 1 % duty PWM — μmol-dose negligible) + collection fiber 5 mm away in a fixed silicone comb → BPW34/OPT101 → TIA → MCU ADC, 10 Hz. Output = DC backscatter in relative units (percent-of-baseline, CICLoPS-style reporting).
- **Electrode grid (E1, E2):** Buffi-iScience geometry — 2 mm gold/ENIG pads (or hobby: 2× Ag/S-S pairs per channel), **1 cm intra-pair spacing**, differential, same depth as fiber tips. E1 straddles the W1→R path (sees the blue write first); E2 sits between R and W2 as the spatial-gradient witness.
- **Spacing rationale:** 10 cm ports keep every penetration >5 cm from tub walls (edge-aeration artifacts per Buffi A2/A12); write-to-witness distance is 2 write→2 electrode hops ≈ 20–30 cm, which is inside the 40 cm propagation distances Mayne et al. 2023 reported for *Schizophyllum* blocks — if signals propagate at all, the geometry can see it.
- **Electronics all outside the lid** on one bracket; darkness preserved (port glow sealed with opaque heat-shrink); a $2 NTC thermistor on fiber W1's tip neighborhood + one ambient = the thermal control channels.

## §FALSIFIER — what counts as "the mycelium responded to the optical write"

A PASS requires **all** of (analysis window + 3σ threshold pre-registered before trial 1):

1. **Time-locked deviation:** after blue write pulses, electrode channel shows spike-rate / 1.5–8 Hz PSD shift (Buffi band) within a **0–30 min latency window**, AND/OR red backscatter deviates >3σ from 10-min pre-stimulus baseline sustained >60 s — with onset NOT synchronous with the LED current envelope (anything simultaneous-with-drive is pickup/thermal by definition; literature latency floor is minutes, Finding 4).
2. **Dose-response:** deviation magnitude orders with the fluence ladder (1 s < 10 s < 100 s).
3. **Wavelength specificity:** same-irradiance **650 nm red write** (the $5 laser's job) produces no deviation → matches flavin action spectrum + Mishra blue-only result.
4. **Dead-substrate twin:** identical write train into an **autoclaved twin tub**, same fiber/electrode geometry → no deviation. Kills thermal expansion, moisture migration, pickup.
5. **Sham-light control (shutter-on):** write electronics fire at identical duty into a **blocked/unmated fiber** (light never enters) → no deviation. Kills driver-EMI and click-artifacts.
6. **Spatial gradient:** deviation largest at the electrode pair nearest the written fiber (E1 for W1), decaying with distance — not a whole-tub simultaneous step (ambient swings move everything at once).
7. **Thermal bound:** tip thermistor ΔT < 0.1 °C during max write (link budget says ≪; the thermistor proves it).
8. **Slow channel (optical-only fallback):** 7-day written-side vs sham-side hyphal-density asymmetry under daily blue pulses (lid photographs) — the phototropism/growth falsifier, pre-recedented by the Hericium dose.

Fail rule: if only (4) or (5) conditions reproduce the live-tub signal, the "response" is an artifact of the rig and O3 closes negative.

## §CONTROLS (S3-inherited + optical)

| # | Control | Kills |
|---|---|---|
| C1 | Sham-light / shutter-on (electronics identical, fiber unmated or blocked) | driver EMI, relay click, pickup (S3 A11) |
| C2 | Dead-substrate twin (autoclaved, same geometry) | thermal, moisture, Donnan drift (S3 A1/A3/A12) |
| C3 | 650 nm red write, matched tip irradiance | non-specific photic/thermal explanation (wavelength spec) |
| C4 | Tip + ambient NTC thermistors, logged every write | unmeasured heating (S3 A12) |
| C5 | Uncolonized-substrate electrode pair (Buffi's differential control) | substrate-only potentials (S3 A3) |
| C6 | Positive control: mechanical touch + sodium-azide chemical stim (known evoked/suppressed responses, Buffi iScience) | rig-can't-see-anything |
| C7 | PD input shorted + LED disconnected during one run | detector-side pickup |
| C8 | Randomized write order, ≥60 min inter-stimulus interval | carryover/refractory confounds |
| C9 | Pre-registered window + threshold + endpoints | post-hoc story-telling (S3 §1 critique #3) |
| C10 | End-of-run port swab → agar plate | contamination masquerading as signal (S3 A9) |

## §BOM — $40-class optical add-on (street prices, 2026-09)

| Part | Qty | Price |
|---|---|---|
| 5 mm blue LED 470 nm (write W1+W2) | 1 pack | $6 |
| 650 nm laser diode module 5 mW (red write-sham + alignment) | 1 | $5 |
| 5 mm red LED 650 nm (read illumination) | 1 pack | $2 |
| BPW34 PIN photodiode ×2 + LM358/op-amp TIA parts | — | $4 |
| OPT101 (photodiode+amp, drop-in upgrade for BPW34) | opt | +$8 ea |
| 1 mm PMMA plastic optical fiber, 10 m | 1 | $8 |
| RTV silicone (ports) or butyl septa ×10 + grommets | — | $6 |
| Arduino Nano clone (write PWM + ADC + logging) | 1 | $5 |
| NTC thermistors ×2, resistors, red gel filter, heat-shrink | — | $4 |
| **Total (base build)** | | **$40** |
| + second read pair (2 fibers + PD, "2 write + 2 read") | opt | +$8 → $48 |

Excluded (already in the electrical lane's budget): electrodes, ADC-24-class logger (hobby: sound-card/MCU ADC), tub.

## §DRAWING (description for the integration sketch)

Cross-section, side view of the monotub: rectangular tub, wet substrate slab filling lower 20 cm; lid on top carrying **4 compression-grommet ports in a line along the long axis** (10 cm pitch, centered, >5 cm from walls). Through each port, vertical: two **write fibers** (blue LEDs mounted on an external bracket above the lid, heat-sink outward, opaque sleeve down the port) and the **read comb** (one red-illum fiber + one collection fiber in a shared silicone block, 5 mm tip gap). All fiber tips end at a dashed line at **−1.5 cm depth** — the "sensing plane". On the same plane, **two differential electrode pairs** (2 mm pads, 1 cm intra-pair) sit between the fiber columns: E1 under the W1→R gap, E2 between R and W2. A small external board (Nano + TIA + LED drivers + thermistor leads) hangs off the tub's short side; a thermistor bead sits beside fiber W1's tip. Callouts: port zoom (lid → grommet → RTV septum → silicone-grease bead around fiber), fluence table (1/10/100 s → µmol/m²), and the C1–C10 control map pinned to each element.

## §VERDICT

1. **Write channel: yes, and it's an LED, not a laser.** Blue 470 nm pulsed light is the literature-validated stimulus (WC-1/BLR/Mad action spectra; Hericium growth dose; Mishra blue-only evoked potentials). $3 LED ≥ thresholds by 1–3 orders; the $5 red laser earns its slot as the inert-wavelength sham + coupling aid. Pulse grammar: seconds-scale pulses, minutes gaps, fluence ladder.
2. **Honesty flag:** the flagship "fungi respond optically" citation in the Adamatzky lineage is **retracted**; the load-bearing positive evidence is Mishra 2024 (blue-only V-light potentials, extracellular, *P. eryngii*) + 1970s–2000s *Neurospora* membrane-potential photobiology. Exact Mishra stimulus numbers remain unfetched (PDF > limit) — retrieve before build.
3. **Feedthrough:** solved problem — grow-community SIP tek + hospital septum, adapted with a compression grommet + silicone-grease wick-seal; no autoclave (POF slumps at ~80 °C); EtOH/H₂O₂/UV-C pre-sterilize.
4. **Readout:** red backscatter through a 5 mm-gap fiber pair at BPW34+op-amp tier — neuroscience's photometry stripped of filters/dichroics/PMTs because our signal is 3–4 orders brighter than the 100 nW that CICLoPS already resolves at SNR 231.
5. **The claim this rig can kill:** "backscatter/electrode deviations after blue writes that pass C1–C9 = photoreceptor-mediated biology, not thermal/pickup artifact." If only the dead twin or the shutter condition reproduces it — O3 closes negative, receipt stands.

**Status: SECTIONS COMPLETE — receipt open for the next wave (Mishra number retrieval, build).**



