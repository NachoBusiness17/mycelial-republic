# G-C_ZONE_TOPOLOGY — receipt (wave lane: physical_computing / GAP G-C)

**Gap:** adaptive electrode placement along species-boundary zone lines — cube-2 barrage-zone design.
**Wave law:** receipt FIRST, append as you go · no git · no paid APIs · WebSearch/WebFetch only.
**Date:** 2026-09-16 · **Respawn note:** prior generation died to a rate limit (Mickey17); this generation re-anchors from sibling receipts G-B (species/barrage canon) + C17 (cube-1 rig: ECG pads, ADS1115 differential) + DESIGN_MULTISPECIES_LATTICE (cube-2 = electrodes AT zone lines, hypothesis "boundaries are the active regions").

## Questions (socratic tease)

1. What optical tracking of mycelial fronts exists at hobby tier (time-lapse + colony-edge detection, image-diff on a fixed camera)?
2. Is electrode position adaptive on a fixed PCB, or does adaptivity mean MANY electrodes with SOFTWARE selecting the active pair?
3. What does the Fungal Potential Card's 8-pair layout (PMC12483595) imply — is software-selected pairs enough to follow a moving boundary?

## Gather targets

- Time-lapse mycelium imaging projects (hobby/DIY tier)
- Colony-edge detection code (OpenCV / image-diff, fixed camera)
- The Fungal Potential Card (FPC) 8-pair electrode layout

## Log (appended as gathered)

- [receipt opened — searches starting]
- **Search 1 (hobby time-lapse rigs):** **PiRamid** (HardwareX 2022, S2468-0672(22)00122-5) — open-source 3D-printable Raspberry Pi imaging box, automated capture every ~10 min for 20+ h, built for bacterial/fungal colony growth measurement on plates. General Pi time-lapse builds abundant (Instructables PiCamera V3 wide w/ autofocus+HDR; diyphotography build; Mycodo mushroom-cultivation automation w/ live cam + timelapse). Also: 3D-printed DIY time-lapse multi-well imager (PubMed 42224137) with open Python software. Hobby pipeline consensus: fixed camera + interval capture + OpenCV segmentation (Otsu threshold / Canny) → colony area/radius → radial growth rate.
- **Search 2 (colony-edge detection code):** MII model (PMC8683468, 2021) — image-intensity-based mycelial growth quantification (rapid, no full segmentation). Open-source filamentous-fungi tool survey (ScienceDirect S0167701226000771). Deep-learning time-lapse fungal ID (MDPI Information 16:109, 2025). BioImage-informatics hyphal-network extraction (10⁵–10⁶ edges). GIS/hal-01559627 hyphal edge tracking. OpenCV official + LearnOpenCV Canny/Sobel tutorials as the code substrate. Key: edge detection on a FIXED camera = mostly threshold+diff, no registration needed if rig doesn't move.
- **FETCH — Fungal Potential Card (PMC12483595) [V]:** PCB card with **8 couples (8 differential pairs = 16 electrodes) of embedded ENIG (Electroless Nickel/Immersion Gold) electrodes** (Prototypos Sarl, prototypos.ch). Four electrode diameters on one card (1/2/3/4 mm, 2 couples per size); **2 mm selected** for experiments; pairs **1 cm apart center-to-center**. 20 µl spore suspension (~350 spores) deposited ON one electrode of a pair (electrodes 1,3,5,9,11,13 inoculated); mycelium grows to bridge the pair. Electronics: Pico ADC-24 data logger, 60 ms conversion/channel ≈ **17 Hz**, shielded D-Sub cabling, **Faraday cage** (ALUTEC 40×30×25 cm), PicoLog 6 → HDF5, MATLAB STFT (Blackman–Harris, 1024 samples, 80% overlap). Microvolt-scale field potentials. **No software channel-selection scheme described; no repositioning; geometry FIXED on the PCB.** The only "dynamics" is the mycelium growing into the fixed grid.
- **Search 3 (front-tracking × electrodes combo):** **No published source combines camera image-diff front tracking at an interspecies zone line with electrode recording** — search returned the halves separately: Fungal Feature Tracker (PMC6822706) quantifies mycelium length/area; NeuroTrack (mBio 2019) growth/branching analysis; microfluidic real-time two-species hyphal contact imaging (Comm Biol, s42003-021-01767-1); Cornell biohybrid robots (Science Robotics 2024, adk8019) = closest COMBO (mycelium growth monitoring + electrical recording over 4 wk). Gap G-C is genuinely open — nobody has published optical-guided electrode selection at a zone line.
- **Search 4 (ESP32-CAM timelapse):** deep-sleep interval capture is the standard multi-week hobby pattern (Arduino Forum ESP32-CAM timelapse thread; brettb.com long-duration guide; solar ESP32-CAM rig). Off-the-shelf alt: **Wyze v3** inside fruiting chambers (grower groups). Hobby-image-diff constraints surfaced: fixed camera distance + consistent lighting are make-or-break; light drift = false diff positives; lid condensation = the classic killer.
- **Search 5 (mux = the adaptivity hardware):** **CD74HC4067 16-ch analog mux + ADS1115** = canonical hobby pattern for software-selected channels (StudioPieters: "ADS1115 behind a CD74HC4067 gives 16 channels of 16-bit precision"; Arduino Forum confirms no 2-in-1 chip exists, pairing is standard). 4 GPIO address pins select channel 0–15; **ESPHome ships a native cd74hc4067 component** (software selects channel on read). Mux on-resistance ~70 Ω. Caveat: true differential through muxes needs **two muxes** (one per leg) or common-reference wiring.
- **Anchor (C17 re-scope):** cube-2 **rung 2** = "printed two-species lattice → GROWN barrage-zone boundary with optically-tracked, adaptive electrode placement. Printed boundaries are predicted to fail first; the zone line grows where the electrodes go." This receipt is the design + falsifier for exactly that rung.

## Sources

- **FPC (primary, fetched):** https://pmc.ncbi.nlm.nih.gov/articles/PMC12483595/ — 8×ENIG differential pairs on PCB, 2 mm electrodes, 1 cm pair pitch, Pico ADC-24 ~17 Hz, Faraday cage, no channel-selection scheme
- **Rigs:** PiRamid — https://www.hardware-x.com/article/S2468-0672(22)00122-5/fulltext · DIY multi-well timelapse imager — https://pubmed.ncbi.nlm.nih.gov/42224137/ · ESP32-CAM deep-sleep timelapse — https://forum.arduino.cc/t/esp32-cam-timelapse/682370 · https://www.brettb.com/coding-tutorials/esp32-cam-time-lapse-photography/ · Mycodo mushroom automation — https://kylegabriel.com/projects/2021/09/mushroom-cultivation-automation.html
- **Edge/growth CV:** MII model — https://pmc.ncbi.nlm.nih.gov/articles/PMC8683468/ (= nature.com/articles/s41598-021-03512-4) · Fungal Feature Tracker — https://pmc.ncbi.nlm.nih.gov/articles/PMC6822706/ · NeuroTrack mBio — https://journals.asm.org/doi/abs/10.1128/mbio.00673-19 · open-source fungi tool survey — https://www.sciencedirect.com/science/article/pii/S0167701226000771 · microfluidic two-species contact imaging — https://www.nature.com/articles/s42003-021-01767-1 · OpenCV Canny — https://learnopencv.com/edge-detection-using-opencv/
- **Mux:** StudioPieters CD74HC4067 guide — https://www.studiopieters.nl/cd74hc4067-16-channel-analog-multiplexer-complete-guide/ · ESPHome component — https://esphome.io/components/sensor/cd74hc4067/ · TI datasheet — https://www.ti.com/lit/ds/schs209d/schs209d.pdf
- **Combo (closest published):** Cornell fungal biohybrid robot (growth monitoring + ephys, 4 wk) — https://www.science.org/doi/10.1126/scirobotics.adk8019 · Dehshibi & Adamatzky spiking analysis — https://arxiv.org/html/2008.10276v1
- **Carried from G-B (barrage canon):** Wei et al. 2023 Microbiome (S. commune melanin zone lines) · Ohira 2007 BioControl · Adaskaveg & Gilbertson 1986 Mycologia · Wang et al. 2017 FEMS Microb Lett · King et al. 2025 Molecules "Fungal Wars"

---

## FINDINGS (final — receipt closes with these three, as wave law requires)

### Recommended tracking method (hobby-tier)

**Fixed camera + interval capture + two-pass OpenCV: species-pigmentation segmentation first, frame-diff second.**

1. **Hardware:** ESP32-CAM (~$6–10) in a deep-sleep interval rig (the standard multi-week pattern) or Raspberry Pi in a PiRamid-style printable box. Fixed distance, fixed exposure, **diffused constant LED** — light drift is what breaks diff. Vent/anti-fog the lid; condensation is the classic killer.
2. **Cadence:** 1–6 h interval is massively oversampled — oyster-class fronts advance ~5–10 mm/day (textbook radial rates; consistent with G-B's 7–14 d full-grain colonization). ~4 shots/day suffices; nightly analysis batch is fine.
3. **Detection:** (a) segment each species by pigmentation (HSV/Otsu on color channels) — the handle is real: S. commune builds **dark melanin barrage lines** (G-B, Wei 2023) against pale oyster mycelium; (b) frame-diff vs previous frame isolates the *moving front*. MII model (PMC8683468) shows even raw intensity-integral tracks growth if color segmentation fails — cheap fallback.
4. **Geometry → electrodes:** extract the boundary polyline; map image coords → PCB coords by homography from 4 printed fiducials on the cube lid; select the 1–2 electrode pairs bracketing the polyline as active differential pairs.
5. **Honest wall:** no published project does camera-diff front tracking at an interspecies zone line *correlated with electrodes* (halves verified separately; Cornell adk8019 closest combo). This method is an assembly of verified hobby parts, not a copied recipe.

### Electrode count that makes adaptivity real

**16 electrodes (4×4 grid), software-muxed — not 8 fixed pairs.** On a fixed PCB, position can never be adaptive; adaptivity = many fixed electrodes + software selecting the active pair (Q2 answered: always the latter). Two CD74HC4067 muxes (one per differential leg, ~$2 ea) in front of the existing cube-1 ADS1115 give any of C(16,2)=120 candidate pairs on 4 GPIO pins; ESPHome's native component selects channels transparently. The FPC's 8 fixed pairs (verified: 2 mm ENIG electrodes, 1 cm pitch, ~17 Hz) prove density-and-recording but have **no selection mechanism, no repositioning** — they work only because inoculation geometry pre-decides where mycelium grows. Design law: **pitch (1 cm) ≤ daily front advance, count ≥ corridor length ÷ pitch + re-selection headroom.** At 1 cm pitch and ~1 cm/day fronts, *daily* re-selection keeps an active pair within ~5 mm of the moving line; 8 pairs die within days against a wandering boundary; 16 tracks a 1-D-ish corridor; 24–32 if it wanders in 2-D. BOM delta over cube-1 ≈ **$4–6**.

### Falsifier this creates for cube-2 rung 2

Rung 2 (C17 re-scope: "GROWN barrage-zone boundary with optically-tracked, adaptive electrode placement") becomes falsifiable as:

**Prediction (pre-register):** electrode pairs straddling the optically-localized zone line show spike statistics (rate/amplitude/burst structure) **≥2× distinct** from bulk same-species control pairs during boundary-contact week, and the camera's front track **leads** the electrode signal — optical tracking predicts which pair becomes active before it does. That lead is the whole point of adaptivity; without it the camera is decoration.

**Falsified if either:**
- **(a) Boundary blindness:** boundary pairs indistinguishable from bulk pairs → "boundaries are the active regions" (cube-2 hypothesis) dies; adaptivity is dead weight; rung 2 auto-retreats to cube-1-style fixed bulk pairs.
- **(b) Tracker blindness:** pigmentation/condensation/light drift defeats hobby segmentation → the adaptive loop has no input signal → "the zone line grows where the electrodes go" is untestable at this budget → auto-retreat per ladder discipline.

**Pre-register the alternative too:** G-B's barrage evidence permits the zone line being an electrical **insulator** (dense hydrophobic melanin wall) rather than a spiker — cross-line coupling *asymmetry* then localizes the line (a pass for zone-line detection) while killing the "spiking boundary" reading. Decide before the run which counts as pass; do not grade post-hoc.

**Status: FILED** (proposal tier; two-eyes pending; stage-0 spend requires operator word). Receipt complete — 3/3 wave-law closers delivered.
