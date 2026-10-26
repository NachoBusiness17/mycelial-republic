# r-water-plasma: Underwater plasma sterilization engineering

Item: deep-dive on kV, pulse microsecond scales, electrode geometry, hobby-grade builds, mechanism (UV/shock/radicals).
Date: 2026-09-28. Gopher: gopher-r-water-plasma (flash50 dig).

## Method statement (what was actually read, run, or blocked)

Verified this session (full text read or PDF text-extracted by me):

1. Zheng et al. 2017, "Inactivation of Staphylococcus aureus in water by pulsed spark discharge", open access at https://pmc.ncbi.nlm.nih.gov/articles/PMC5583338 - fetched full text via WebFetch.
2. Estifaee et al. 2019, "Mechanism of E. coli inactivation by direct-in-liquid pulsed electrical discharge", Scientific Reports 9:2326, https://www.nature.com/articles/s41598-019-38838-7 - fetched full text via WebFetch (followed the cookie redirect chain).
3. Mentheour et al. 2022, "Coupled antibacterial effects of plasma-activated water and pulsed electric fields", Frontiers in Physics 10:895813, https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2022.895813/full - fetched full text via WebFetch.
4. Zhang et al. 2024, UV + high-voltage electric field synergy study, https://pmc.ncbi.nlm.nih.gov/articles/PMC11083544 - fetched full text via WebFetch.
5. van der Werf, Y., "Calorimetry experiments on underwater arc discharges", TU Eindhoven bachelor thesis, 2014, https://pure.tue.nl/ws/portalfiles/portal/67737645/851857-1.pdf - downloaded with curl and text-extracted with pypdf (repo venv, 59 pages, 86,500 chars extracted).
6. Namihira, Wang, Takashima, Katsuki, Akiyama (Kumamoto University), "Water purification using pulsed streamer discharges in micro-bubbled water", IEEE conference paper 2003, https://kumadai.repo.nii.ac.jp/record/21699/files/2003_291_1266-1269.pdf - downloaded with curl and text-extracted with pypdf (4 pages).
7. Wikipedia, "Electrohydraulic forming", https://en.wikipedia.org/wiki/Electrohydraulic_forming - fetched via WebFetch (history and mechanism only; the page carries no kV figures).

Blocked this session (located, not read; anything I would want from them is marked OWED below):
- Akiyama et al. 2021 review "Pulsed discharge plasmas in contact with water and their applications", IEEJ Trans. EEI, https://onlinelibrary.wiley.com/doi/full/10.1002/tee.23282 - HTTP 403 from Wiley.
- MDPI Energies 2026 disinfection-efficiency paper, https://www.mdpi.com/1996-1073/19/11/2647 - HTTP 403.
- AIP Physics of Plasmas 2025 PAW paper (search snippet says 10 kV, 500 ns pulses), https://pubs.aip.org/aip/pop/article/32/3/033505/3339252 - HTTP 403. The 10 kV / 500 ns numbers are search-snippet only, NOT verified full text: treat as OWED.
- Sun et al. 2018 (shock waves, UV, electric fields contributions), https://www.sciencedirect.com/science/article/abs/pii/S1567539417300737 - HTTP 403. OWED.
- Elsinga MSc thesis (pin-to-water discharge gap, TU/e 2023), https://research.tue.nl/files/308518032/1238384_-_Elsinga_H._-_MSc_thesis_Thesis_-_MAP.pdf - Cloudflare challenge page, not a PDF. OWED.
- 4hv.org / Energetic Forum hobby threads on underwater sparks: search engines index them poorly; no thread fetched this session. OWED.

## 1. The engineering envelope: kV and pulse scale (all numbers from the six verified sources)

Verified parameter sets, side by side:

| Source | Regime | Voltage | Pulse width | Rate | Electrode geometry | Gap |
|---|---|---|---|---|---|---|
| van der Werf 2014 (TU/e BSc) | arc, calorimetry | 3 to 4.5 kV | capacitor RC decay (no pulse shaping) | single shots | parallel flat copper electrodes, 2 mm (variable in 2 mm steps) | 2 mm |
| Estifaee 2019 (E. coli) | low-energy plasma vs field | capacitor charged to +17 kV | not reported; 0.21 J/pulse | 60 Hz rotating spark gap | plate-to-plate: 0.8 mm NiCr wire vs 3 cm stainless disc | 2.5 cm |
| Zheng 2017 (S. aureus) | fully developed spark | 30 kV peak-to-peak, 100 A p-p | 1.8 microseconds | 0.5 Hz | point-to-plane: 0.2 mm insulated stainless wire tip vs grounded 120 mm plate | 5 mm |
| Namihira 2003 (streamer, dye) | streamer, non-thermal | 50 kV square (generator to 150 kV) | 0.6 to 1.2 microseconds | 20 pulses/s | wire-to-cylinder coaxial: 0.15 mm brass wire inside 100 mm ID stainless mesh cylinder, 200 mm long | wire-to-mesh radial |
| Mentheour 2022 (transient spark, PAW) | transient spark TS-ES | 15 kV max, 27 to 30 A pulses, 15 to 20 kV collapse | voltage drop in about 20 ns; TS-B current pulses 1 to 3 A over 50 to 150 ns | 1 kHz (about 3 W) | needle-to-grid (1 cm) or needle-to-water-surface with ground ring | 1 cm |

Reading the table as an engineer:

- **kV scales with gap and regime, not with lethality.** A 2 mm tap-water arc fires at 3 to 4.5 kV (van der Werf); a 5 mm point-to-plane spark at 30 kV (Zheng); a 2.5 cm streamer gap at 17 kV charged into 0.75 nF (Estifaee); a 50 kV square pulse drives a coaxial streamer reactor across tens of mm of water (Namihira). Same water, order-of-magnitude spread, because breakdown in liquid follows field concentration at sharp tips, not bulk water strength.
- **The microsecond scale in the item's title is exactly the streamer/spark crossover zone.** Zheng's 1.8 microsecond pulse drives a true spark (channel above 10,000 K, per their text). Namihira's 0.6 to 1.2 microsecond square pulse stays streamer (non-thermal), and they show streamers propagate at constant velocity, so pulse width sets streamer length: longer pulse, longer plasma channel, more treated volume (Namihira results section). Below a microsecond you are in transient-spark/ns territory (20 ns collapse, 50 to 150 ns current pulses, Mentheour).
- **Pulse width vs polarity:** Namihira chose positive polarity on the central wire because it generates non-thermal plasma in solution more effectively than negative (their intro, citing prior work).
- **Repetition rate spans 0.5 Hz (big sparks) to 1 kHz (3 W transient sparks).** Average power is the honest budget: Mentheour's PAW rig ran about 3 W at 1 kHz; Zheng's spark was 0.3 to 2 J/pulse at 0.5 Hz.

## 2. Electrode geometry: what each shape buys

- **Point-to-plane (needle/wire tip vs plate).** Zheng's workhorse: 0.2 mm stainless wire, tip extending about 1 mm past silicone/Teflon insulation, against a 120 mm grounded plate, 5 mm gap. Sharp tip concentrates field for reliable ignition; insulated shank keeps the discharge at the tip.
- **Plate-to-plate (wire vs disc).** Estifaee's variant: 0.8 mm NiCr wire vs 3 cm stainless disc at 2.5 cm. Their clever control: for the pulsed-electric-field-only condition they flattened the HV tip to suppress plasma while keeping the same voltage and current waveforms. That is the experimental trick that let them separate electric-field killing from plasma killing.
- **Wire-to-cylinder coaxial.** Namihira's industrial-shaped reactor: 0.15 mm brass wire centered in a 100 mm diameter stainless mesh cylinder, 200 mm long, fully immersed. This is the large-volume geometry: streamers launch radially in all directions from the wire, and the mesh doubles as the ground electrode while letting water flow through.
- **Parallel flat plates.** van der Werf's calorimetry choice: flat copper plates at 2 mm. Flat-to-flat at kV-class voltage and mm-class gap forces the breakdown problem: it worked only in tap water, never deionized (see hobby section).
- **Electrode material matters beyond ignition.** van der Werf found copper oxidation chemistry may contribute materially to the heat budget, and suggests non-oxidizing electrodes (carbon) for follow-up. Zheng insulated the wire shank in Teflon so only the tip participates.

## 3. Pulse circuits: the switch is the hard part

- **Blumlein pulse forming network (Namihira):** stages of 8.5 nF + 0.66 microH at 17.6 ohms per stage, total 440 ohms, 2:10 pulse transformer, square pulses 0.6 to 1.2 microseconds at up to 150 kV, applied at 50 kV. A PFN buys square pulses, which means constant voltage during the streamer propagation window.
- **Capacitor + switch (van der Werf):** the instructive failure. With a triggered spark gap as the switch, the arc sat in the switch for several seconds and nothing happened in the water: the switch's resistance kept the voltage across the submerged gap from rising fast enough for water breakdown. Replacing it with a mechanical relay switch fixed it. Lesson: the closing switch must collapse its own voltage faster than the water gap needs; a slow switch just moves the discharge into the switch.
- **Rotating spark gap (Estifaee):** 60 Hz rep rate from a motor-driven gap, 17 kV into 0.75 nF, about 0.21 J/pulse, 13 W mean. Hobby-accessible and how old Tesla-coil gear does rep rate.
- **DC through a ballast (Mentheour TS-B):** 10 Mohm ballast resistor, needle over a water surface, streamer pulses about 10 mA growing into 1 to 3 A, 50 to 150 ns spark pulses at 1 kHz from plain DC. The discharge itself does the pulsing.

## 4. Mechanism: UV, shock, radicals, field. The honest answer is regime-dependent

Each verified paper isolates mechanisms with scavenger/control experiments, and they disagree with each other, which is the finding:

- **UV dominates in the big-spark regime (Zheng, S. aureus).** With the UV absorber BP-9 at 30 mg/L, disinfection was "almost negligible"; with ROS scavengers (90 micromolar H2O2 alone caused no change; 1 mM NAC still gave a 5 log10 reduction), ROS contribution was minimal. Hydroxyl radicals recombine too fast (k = 5 x 10^9 per M per s) to act far from the channel. Spark channel above 10,000 K emits the UV. Dose metrics: 182 J/L for 10^8 CFU/ml starting load, 83 J/L at 10^6 CFU/ml, optimized 90 J/L at 1 J/pulse. Shock waves get a secondary role: bursting colonies and anti-biofouling.
- **The electric field dominates in the low-energy regime (Estifaee, E. coli).** Plasma gave 3.5 log reduction; the pulsed electric field alone (tip flattened, same waveforms) gave 3 log, statistically indistinguishable. UV was negligible: isolated via a quartz cuvette, no inactivation, photon flux too low at 13 W. Radical scavenger (caffeine) cut H2O2 by more than 75 percent but did not change killing kinetics. At 0.21 J/pulse there is not enough energy budget for UV or shock to matter; the 2.5 cm gap at 17 kV is a 6.8 kV/cm class field and it electroporates cells, rupturing walls at the rod poles.
- **RONS chemistry dominates in plasma-activated water (Mentheour).** H2O2 alone showed no antibacterial effect even at 10 mM; the active species is peroxynitrous acid (ONOOH) from H2O2 + nitrite at acidic pH. Hydroxyl radicals peroxidize membrane lipids, lowering the electroporation threshold. And their PEF control (2.5 kV, 200 ns, 12.5 kV/cm) alone was non-lethal.
- **Synergy is real and separable (Zhang 2024).** UV 265 nm alone: 3.3 log in 5 min. DC HV electric field alone (wire-plate, 10 kV of a 50 kV-max supply): 0.17 log. Together: 4.2 log in 5 min (p < 0.001). Field damages membranes, UV damages DNA, each sensitizes the other.
- **Shock waves are the mechanism in non-sterilization applications.** Wikipedia's electrohydraulic forming article (verified): Yutkin recognized submerged-arc forming in the mid-1940s; aerospace production systems through the 1950s/60s; the arc vaporizes surrounding water and the bubble collapse drives a shock wave into the workpiece in milliseconds. Search results this session (not full-text verified, OWED for numbers) show the same physics industrialized for food: Eguchi et al. 2020 (MDPI) on shockwave non-thermal food processing electrodes that generate shock waves at lower voltage, and a 2022 Fan et al. review of underwater shockwave processing in the food industry.
- **What streamers emit, per Namihira's abstract (direct quote):** "intense electric fields at the tip of streamers, as well as high energy electrons, ozone, other chemically radical species, ultraviolet rays and shock waves." All five mechanisms on one line, which is why mechanism studies that control only one variable get contradictory answers.

**Engineering synthesis:** kill mechanism tracks energy per pulse and channel state. Sub-joule, non-thermal streamer: electroporation + near-tip radicals. Joule-class, full spark: UV from the 10,000 K channel takes over (with shock as adjunct). Post-discharge chemistry (PAW): peroxynitrite. Anyone claiming one universal mechanism is selling a regime as a law.

## 5. Hobby-grade builds: what a bench rig looks like

The van der Werf thesis is the best documented small-scale build found (student lab, TU/e 2014), built to test the Mills/Graneau "excess energy" water-arc claims:

- Rig: calorimeter bucket (about 1.5 to 1.9 kg water), parallel flat copper electrodes at 2 mm gap, capacitor charged to 3 to 4.5 kV, 450 to 1000 J per shot, RTD temperature probe, stirrer, current probe in the kA range.
- Practical lessons with receipts:
  - **Tap water fires; deionized water does not.** At 3 to 4.5 kV across 2 mm, deionized water never broke down in their rig; tap water fired reliably. Their proposed cause: leakage current through the conductive water initiates the vapor channel. (van der Werf sections 5.1.) Counterintuitive at first read: high-purity water is HARDER to break down at hobby voltages, and conductivity is a design variable.
  - **Switch dv/dt is the gate** (triggered spark gap failure, relay fix, section 5.1 and 3.4).
  - **Efficiency is about 70 percent** of stored capacitor energy landing as measurable heat; their single 160 percent anomaly (chasing Mills' claim) never reproduced across 10 to 15 later shots. The excess-energy folklore around water arcs (Mills 1.6x, Graneau) did not survive a careful student calorimeter. That is the honest hobby-grade verdict.
  - **Conductivity also taxes you downstream:** Namihira shows higher-conductivity water thickens streamer channels (more plasma volume, good) but raises joule heating (treatment efficiency saturates as conductivity climbs during processing).
- Rep-rate hardware within hobby reach, per the verified builds: rotating spark gap (60 Hz, Estifaee), relay-switched cap bank (van der Werf), DC + ballast resistor transient spark at 1 kHz (Mentheour), photoflash-class caps (0.75 nF charged to 17 kV is sub-joule, Estifaee).
- Bubbling is the cheap multiplier: Namihira's oxygen micro-bubbles (below 100 micrometers, through the water pump) raised decolorization dramatically versus nitrogen or argon, because discharges in oxygen bubbles make ozone and atomic oxygen. A fish-pump air stone plus oxygen is a hobby-trivial add with a measured effect.
- Safety, from the physics above, not boilerplate: these are capacitor banks at lethal voltage (3 to 50 kV) with joules to kilojoules stored; the discharge also makes pressure waves (the EHF industry uses them to FORM METAL), so enclosed vessels are bomb risk; spark UV is real (it is the kill mechanism in Zheng's rig) so view ports need UV-blocking material; tap-water chemistry under spark produces oxidants and byproducts not safe to drink by default.

## 6. OWED (could not verify this session; do not trust until checked)

- Typical bulk-water breakdown field figures (the "MV/cm for short pulses" lore) - I know this from training memory, found no fetchable source this session to pin it. OWED.
- Akiyama et al. 2021 review parameter tables (the most systematic kV/ns/geometry map in the field) - Wiley 403. OWED.
- AIP Physics of Plasmas 2025: "10 kV, 500 ns" - search snippet only, full text 403. OWED.
- Sun et al. 2018 relative mechanism contributions (shock vs UV vs field) - 403. OWED.
- MDPI Energies 2026 disinfection dose numbers - 403. OWED.
- Elsinga TU/e 2023 pin-to-water thesis numbers - Cloudflare-blocked. OWED.
- 4hv.org / Energetic Forum underwater-spark threads (the actual hobbyist forum corpus) - not indexed/reachable this session. OWED.
- Eguchi 2020 lower-voltage shockwave electrode numbers - search snippet only, MDPI 403. OWED.

## Source links

- Zheng 2017: https://pmc.ncbi.nlm.nih.gov/articles/PMC5583338 (full text fetched)
- Estifaee 2019: https://www.nature.com/articles/s41598-019-38838-7 (full text fetched)
- Mentheour 2022: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2022.895813/full (full text fetched)
- Zhang 2024: https://pmc.ncbi.nlm.nih.gov/articles/PMC11083544 (full text fetched)
- van der Werf 2014: https://pure.tue.nl/ws/portalfiles/portal/67737645/851857-1.pdf (PDF downloaded, pypdf-extracted)
- Namihira 2003: https://kumadai.repo.nii.ac.jp/record/21699/files/2003_291_1266-1269.pdf (PDF downloaded, pypdf-extracted)
- Electrohydraulic forming: https://en.wikipedia.org/wiki/Electrohydraulic_forming (fetched)
- Blocked/OWED links listed in the method statement.
