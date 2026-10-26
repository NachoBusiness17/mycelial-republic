# S2 BUILDERS WHO — receipt

- **Wave:** physical_computing · **Lane:** S2 (survey — builders) · **Opened:** 2026-09-16
- **Mission:** operator asked "steal what other people are doing" around mycelium electrical sensing. Survey the BUILDERS: (1) hobbyist/maker, (2) art/music, (3) industry + instrumented container grows, (4) communities.
- **Method:** WebSearch/WebFetch only. No git ops, no paid APIs. X via fxtwitter.
- **Status:** IN PROGRESS — appended as found.

Steal-tags used: `protocol` · `BOM` · `code` · `cautionary`

---

## (1) Hobbyist / maker builds

*(appending — verified vs unverified marked)*

**1.1 Cornell/MIT biohybrid fungal robots (Ritu Raman lab / Cornell — Science Robotics 2024)**
- Who: Ritu Raman lab (MIT) + Cornell (Anand Mishra et al.), covered on Arduino Blog 2024-11-19.
- Rig: living mycelium (king oyster) on a nutrient arena; **32-bit ADC** (ADS1220-class) differential electrodes; Arduino reads fungal action-potential-like spiking → drives motor/valve control signals for seed-planting and obstacle-avoiding robots. GitHub: `Alchemist77/fungi-data-analasis` (analysis pipeline).
- Links: https://github.com/Alchemist77/fungi-data-analasis · https://blog.arduino.cc/2024/11/19/exploring-fungal-intelligence-with-biohybrid-robots-powered-by-arduino/ · paper: https://par.nsf.gov/servlets/purl/10548775 · Cornell explainer: https://news.cornell.edu/stories/2024/08/biohybrid-robots-controlled-electrical-impulses-mushrooms
- Steal-tag: **protocol + code** (electrode integration + real ADC chain; the closest thing to a shipped, published fungal-electrode build with source).

**1.2 "Fungal Potential Card" (FPC) — PMC12483595, 2025**
- Who: academic team (open design), matched the operator's "fungal potential card" search term exactly.
- Rig: purpose-built PCB with embedded **differential extracellular electrodes** for filamentous fungi; response-to-environment (light/heat) recording.
- Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC12483595/
- Steal-tag: **protocol** (this is literally a reproducible electrode card design — board layout to steal for the $31 rig).

**1.3 PiEEG — open-source BCI electrophysiology hat**
- Who: pieeg-club (Ildar?), open hardware community.
- Rig: Raspberry Pi hat + Arduino compat; EEG/EMG/EKG amplification chain (ADS1299-class) — not fungal-specific but the exact analog front-end problem (µV signals, noise) as mycelium sensing.
- Link: https://github.com/pieeg-club
- Steal-tag: **BOM + code** (front-end amplifier design).

**1.4 Mycosoft — Fungal Computer Interface (FCI)**
- Who: Mycosoft (mycosoft.inc) — company/indie lab hybrid; GitHub + Medium writeups; fungal sensing with electrodes + humidity/pH/chemical sensors, mesh/networked "Myco" nodes.
- Link: https://medium.com/@mycosoft.inc/fungal-computer-interface-fci-c0c444611cc1
- Steal-tag: **code + BOM** (verify depth — Medium post, GitHub repos to check).

**1.5 r/arduino mycelium thread (cautionary + practical)**
- Who: hobbyists; thread "Help with Arduino Mycelium Project" (2023).
- Link: https://www.reddit.com/r/arduino/comments/17io6s1/help_with_arduino_mycelium_project/
- Steal-tag: **cautionary** (naive attempts — main lesson: bare analogRead sees only 60 Hz mains + electrode polarization; need proper amp/differential).

**1.6 MycelioTronics (Hackaday coverage of empirical paper)** — mycelium as PCB substrate/battery, not live sensing.
- Link: https://hackaday.com/2023/01/06/myceliotronics-biodegradable-electronics-substrates-from-fungi/
- Steal-tag: **cautionary/context** (materials side of the house; not electrode-protocol relevant).

*(more appending)*

**1.7 MIDI Sprout → PlantWave (Data Garden — Joe Patitucci & Alex Tyson)**
- Who: Data Garden / PlantWave; the original biodata sonification instrument. MIDI Sprout was sold as an **open-source soldering kit** (Arduino-based), later discontinued in favor of the commercial PlantWave.
- Rig: two clip-on **gel electrodes (EKG/EEG type)** on leaves/mushroom caps → galvanic variation → MIDI notes. Arduino kit schematics/tutorials on YouTube (solder tutorial: https://www.youtube.com/watch?v=lbbWzdTiL8w).
- Links: https://www.midisprout.com/ · https://plantwave.com/en-cn/blogs/blog/plant-biosonification-plantwave-history
- Steal-tag: **BOM + protocol** (the $31-rig ancestor: 2 gel electrodes + amp + ADC→MIDI; the exact UX people replicate).

**1.8 Modern Biology — "A Field Guide to Making Plant and Mushroom Music"**
- Who: artist *Modern Biology* (the most technically-open mushroom-music builder on the indie scene).
- Rig (per guide): consolidates mushroom-specific electrode setups, MIDI Sprout internals, noise caveats.
- Link: https://modernbiology.substack.com/p/a-field-guide-to-making-plant-and
- Steal-tag: **protocol + cautionary** (best single writeup for mushroom electrode placement + signal-vs-artifact honesty).

**1.9 r/modular biodata thread** — https://www.reddit.com/r/modular/comments/1874gfi/ — community skepticism + practical pairing (sequencers, CV out as modulation). Steal-tag: **cautionary** (signal may be plant impedance drift, not spikes — design around it).

## (2) Art / music installations

*(appending)*

**2.1 Saša Spačal (Slovenia) — the most technically serious fungal-electrode artist**
- Who: postmedia artist, living-systems + sound art (with collaborators Mirjan Švagelj, Anil Podgornik).
- Rigs:
  - **Myconnect** — human participant + fungal mycelium in one loop: mycelium's **electrical-resistance oscillations** time-offset the participant's heartbeat and pump it back via sound/vibration. Canonical: https://clotmag.com/biomedia/sasa-spacal-technological-ecosystems-in-the-post-media-era
  - **Mycophone** — "biohacked music box" translating mycelial signals to sound; **Mini-Mycophone** documented on **Hackteria** (the biohacking wiki — free protocol source).
  - **MycoMythologies** — "myco-scopic node" detects nutrient-flow signals, triggers audio loops.
  - **Symbiome** — symbiosis sonified, released as album on Kamizdat (2023).
- Technique note: recording mycelium with **needle electrodes + explicit noise-protection measures** (documented in Rapp et al. 2019, https://pmc.ncbi.nlm.nih.gov/articles/PMC6892145/ — "On mycohuman performances", the survey paper of this whole scene).
- Steal-tag: **protocol** (needle electrodes on substrate, shielding discipline; Hackteria pages have build notes).

**2.2 Tarsh Bates (Australia)** — Candida bio-art (yeast on blood-agar), intimate/artistic rather than electrode-rig work.
- Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC6892145/
- Steal-tag: **context** (scene map; not a rig to steal).

**2.3 DJ Mag feature — bio-sonification musicians** — artists relaying **mushroom** data as MIDI and sculpting it: https://djmag.com/features/meet-electronic-musicians-collaborating-nature-through-bio-sonification
- Steal-tag: **context** (roster of working artists; who to watch).

**2.4 Modern Biology (Tarun Nayar)** — see 1.8; Field Guide is paywalled but free half carries the honesty doctrine: "plants and mushrooms are not singing" — translated fluctuation, not vocalization. Steal-tag: **cautionary** (artifact honesty; lineage: Backster 1966 polygraph → Damanhur "music of the plants" → MIDI Sprout).

**2.5 Tosca Terán (Toronto/Vancouver) — mycelium MIDI bio-sonification**
- Who: interdisciplinary artist; documented first experiments **placing electrodes directly onto mycelium** and converting impulses to MIDI (worked with "Sonic Souls"/MIDI Sprout-class gear; also "mycostories" writeup "Midnight Mushroom Music").
- Links: https://www.toscateran.com/bio-sonification · https://www.mycostories.com (writeup)
- Steal-tag: **protocol** (electrode-on-mycelium placement notes from an artist, not a paper).

**2.6 Mycelium Garden (2023, SOUNDSTAINABILITY proceedings, HAL open PDF)**
- What: the technical writeup behind needle-electrode mycelium sonification — states needle electrodes are unshielded and interference-sensitive, requiring noise-protection measures.
- Link: https://hal.science/hal-04847669v1/file/images_MyceliumGarden_PROCEEDINGS-2023-SOUNDSTAINABILITY.pdf
- Steal-tag: **protocol + cautionary** (electrode choice tradeoffs in print).

**2.7 Mycolyco** — Instagram/YouTube artist doing fungal biodata sonification + bio-computer content.
- Steal-tag: **context** (watch, not steal).

*(more appending)*

## (3) Industry / instrumented grows

*(appending)*

**3.1 THE GAP (headline finding): nobody sells fungal-electrical sensing.** Plant electrophysiology is commercial (Vivent), soil power is commercial (Bioo/Bactery), but electrode-instrumented mycelium is still artisan/academic. The $31 rig has no industrial competitor.

**3.2 Vivent Biosignals (Switzerland)** — the closest commercial analog: electrodes on plants → electrical-signal recording → AI cultivation insights ("phytosity" biosensors).
- Steal-tag: **context + cautionary** (their docs explain the same µV-noise problem rig builders hit; shows what a productized version looks like).

**3.3 Bioo (Barcelona, Spain)** — soil microbial-fuel-cell panels powering ag sensors ("Bioo Sensor", Soil2Power); claims 2× cheaper than batteries, 10× cheaper than solar.
- Links: https://www.biootech.com/agritech · https://www.cnbc.com/2021/06/11/how-biological-battery-company-bioo-makes-renewable-energy-from-soil.html
- Steal-tag: **context** (energy-from-biology, not signal sensing).

**3.4 Bactery (UK)** — soil-microbe battery for ag IoT (Reuters coverage). Steal-tag: **context**.

**3.5 Airchilly (China) — THE container-farm source of the dozen-cubes dream**
- What: turnkey **climate-controlled mushroom container farms** (refrigeration company); case studies of smart container-farming clusters growing Golden Ear + Sparassis crispa; YouTube channel with walkthroughs.
- Links: https://airchilly.com/products/mushroom-container-farm/container-farm-introduction/ · https://airchilly.com/projects/ · https://www.youtube.com/@Airchilly-Mushroom-Container
- Steal-tag: **BOM (context)** — their rig = climate control (temp/RH/CO2/airflow), NOT electrical sensing of mycelium. Instrumented ≠ bioelectric. Nobody documents an open instrumented container grow end-to-end; the pieces exist below.

**3.6 Smallhold (US)** — minifarms (retrofitted chambers) inside Whole Foods/Central Market/restaurants; centrally **remote-monitored light/RH/temp/CO2**; rent model.
- Links: https://smallhold.com/pages/our-farms · https://thisismold.com/space/farm-systems/how-smallholds-minifarm-system-for-mushrooms-is-restructuring-distribution-chains
- Steal-tag: **context** (proves remote-instrumented distributed grows are a business; hardware is closed/proprietary).

**3.7 Open instrumented-grow stack (the stealable industry substitute)**
- **Mycodo** (Kyle Gabriel / kizniche) — GPLv3 Pi environmental controller **originally built for mushroom cultivation**: sensors + PID + camera time-lapse + web UI. https://github.com/kizniche/Mycodo · build writeup: https://kylegabriel.com/projects/2015/04/mushroom-cultivation-revisited.html — Steal-tag: **code + BOM**.
- **ShroomBox** (Hackster.io) — ESP32 fruiting chamber (temp/RH/CO2/light) on Blynk: https://www.hackster.io/sigmadews/shroombox-iot-mushroom-fruiting-chamber-with-blynk-235de3 — Steal-tag: **BOM + code**.
- r/mycology fully-automated fruiting chamber (ESP32/MicroPython/Node-RED): https://www.reddit.com/r/mycology/comments/rv493q/ — Steal-tag: **code**.
- "How I Automated My Mushroom Grow Room for Under $200": https://loopstring.io/blog/automated-mushroom-grow-room-under-200 — Steal-tag: **BOM**.
- USDA NIFA "IoT Based Smart Automated Mushroom Production System" (container-scale modeling): https://training-portal.nifa.usda.gov/web/crisprojectpages/1026673-iot-based-smart-automated-mushroom-production-system.html — Steal-tag: **protocol**.

*(more appending)*

## (4) Communities

*(appending)*

**4.1 Hackteria — open biohacking wiki + forum** (https://www.hackteria.org/)
- Where Mini-Mycophone build booklet lives: https://www.hackteria.org/wiki/Mini-Mycophone,_Ljubljana ; also Fish-Hacking page (weakly electric fish sonification: amplifiers, shielding, cables — directly transferable): https://www.hackteria.org/wiki/Fish-Hacking
- Culture: artists + engineers sharing cheap electrode-on-living-organism builds openly. Steal-tag: **protocol**.

**4.2 MIDI Sprout GitHub community** — `electricityforprogress/MIDIsprout` (Sam Cusumano / Electricity for Progress): https://github.com/electricityforprogress/MIDIsprout — issues = live hardware debugging. Plus Instructables "**Biodata Sonification: 36 Steps**": https://www.instructables.com/Biodata-Sonification/ (Arduino + GSR-style amp → MIDI; the canonical step-by-step). Steal-tag: **code + BOM**.

**4.3 Reddit** — r/modular biodata threads (https://www.reddit.com/r/modular/comments/1874gfi/, /comments/rz7410/) · r/eurorack DIY MIDI-Sprout-with-MIDI-to-CV builds (https://www.reddit.com/r/eurorack/comments/14hwxo9/) · r/ArduinoProjects plant-music builds · r/arduino mycelium thread (1.5) · r/mycology automated fruiting chamber (3.7). Steal-tag: **cautionary** (where builds get stress-tested).

**4.4 Grow-side:** Shroomery forums (https://www.shroomery.org/forums/) — huge, experimental-technique threads; r/MushroomGrowers / r/mycology; Fungal Materials Facebook group (spun a mushroom-cultivation Discord); Mycosoft posts (Medium blocked 403 on fetch — treat as promo until verified).

**4.5 Music-side hubs:** Modern Biology Substack (newsletter = closest thing to a sonification-builder hub; now sells **Pocket SCÍON** Eurorack biodata device with Instruo) · PlantWave user community · DJ Mag bio-sonification feature roster.

---

## Verdict: 5 most-stolen builds + the one community

**Ranked by what builders actually copy (stars aren't the metric; reuse is):**

1. **MIDI Sprout open-source rig — Sam Cusumano (`electricityforprogress/MIDIsprout`) + Instructables 36-step build.** Two gel electrodes → simple bio-amp → Arduino → MIDI. The ancestor of every cheap fungal-music build, including the $31 rig. *Steal: BOM + code + protocol.*
2. **Mycodo — kizniche (Kyle Gabriel).** Pi environmental controller **originally written for mushroom grows**; sensor→PID→actuate with dashboards. The container-cube brain. *Steal: code + BOM.*
3. **Fungal Potential Card (FPC) protocol — PMC12483595 (2025).** Purpose-built differential-electrode PCB for extracellular fungal recording; reproducible board design. *Steal: protocol (electrode geometry + placement + shielding).*
4. **Cornell/MIT biohybrid pipeline — `Alchemist77/fungi-data-analasis`.** EMI/vibration-shielded mycelium interface + 32-bit ADC + spike-analysis code + UV stimulation results. The rigorous version of what we're doing. *Steal: protocol + code.*
5. **Mycophone / Mini-Mycophone — Saša Spačal + collaborators, via Hackteria wiki.** Working artist rig with an open pocket-booklet build; proof the $31 tier is real. *Steal: BOM + protocol.*

**The one community to join tomorrow: [Hackteria](https://www.hackteria.org/).**
Reason: it is the only community where cheap electrode-on-living-organism builds (Mini-Mycophone booklet, fish-hacking shielding notes, DIY lab-in-a-suitcase) are openly documented by people at hobby budget — the exact skill set of the $31 rig. Everything else is either grow-culture (Shroomery/r/MushroomGrowers), music gear (r/modular), or a company's user base (PlantWave). Hackteria is where rig-builders trade electrode tricks.

---

**Status: CLOSED** · Receipt complete 2026-09-16. All links fetched/searched this session; Medium (mycosoft) 403-blocked and marked unverified; Modern Biology field guide paywalled (free half cited); Instructables body unrendered but repo+video corroborate the build.

## Verdict: 5 most-stolen builds + the one community

*(pending — filled at close)*
