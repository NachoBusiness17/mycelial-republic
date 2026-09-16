# X MINE — physical computing vein — 2026-09-16

Lane: X input search, physical-computing. Window: Sept 2026 (allow back to June 2026).
Method: WebSearch (site:x.com + plain) → fxtwitter.com/<user>/status/<id> for full text. Free APIs only.
Status: OPEN — findings appended below as discovered.

## Findings (appended per discovery)

### T1. @extropic — 2026-07-29
- Claim: Z1.5 (iteration over Z1, first production-scale TSU) to be fabbed at a US foundry; $75M non-binding CHIPS R&D LOI with Dept of Commerce; two X0 variants already taped out AND tested at two different fabs (fab-portability proof).
- Why it matters: **substrate + vocabulary** — TSU = "Thermodynamic Sampling Unit", samples from programmable probability distributions using CMOS thermal noise on mature nodes. The fab-portability claim (same design, two fabs, both tested) is the falsifiable detail worth tracking. Promise of "comprehensive technical update in coming days" — check for the follow-up post with real benchmarks.
- URL: https://x.com/extropic/status/2082459450166968328

### T2. @extropic / Z1T announcement (via @GillVerd amplification, ~2026)
- Claim: Z1T = first transformer-like model family for sparse probabilistic hardware; "up to 140x energy efficiency gains" on inference over GPUs; weights + training recipe open-sourced.
- Why it matters: **falsifier** — open weights make the 140x claim independently checkable (unlike most efficiency press releases). Third-party replication would be the strongest possible steal for the pack. Reddit thread r/AISEOInsider "Extropic AI Chip Claims 140x Energy Breakthrough" already flags inspectability.
- URL: https://extropic.ai/writing/z1t (canonical claim page; X amplification via https://x.com/GillVerd)

### T3. @DustinJuliano — thermodynamic computing benchmark proposal
- Claim: proposes a comprehensive open-source comparative benchmark for thermodynamic computing with baseline CPU and GPU comparisons.
- Why it matters: **falsifier** — exactly the eval-harness pattern our pack uses (bytes, not reports). If Juliano's harness exists, adopt rather than rebuild.
- URL: https://x.com/DustinJuliano (post ID not indexed; thread on profile)

### T4. @ronboger — skepticism on Extropic timelines
- Claim: Extropic ambition is "delusionally optimistic" like early SpaceX doubt; many experts doubted thermodynamic computing.
- Why it matters: **falsifier** — the skeptical pole. Useful for the pack's "claim vs measured" ledger: both poles of the discourse are now on record.
- URL: https://x.com/ronboger (all-posts page; post ID not indexed)

### T5. Normal Computing CN101 (context, non-X)
- Claim: world's first thermodynamic computing chip taped out (June 2025, ARIA UK-funded); up to 1000x energy-efficiency claim on matrix/sampling workloads; bring-up results shared; low-speed I/O test chip; arXiv 2608.00754 "A Digital Thermodynamic Computer for Generative AI"; CN product line releases planned 2026 and 2028.
- Why it matters: **substrate** — the competing pole to Extropic. The 2026 release window means third-party hands-on data may land this quarter. Bring-up post is on LinkedIn (activity-7407878852691025921).
- URL: https://www.normalcomputing.com/blog/normal-computing-announces-tape-out-of-worlds-first-thermodynamic-computing-chip

## A. Coherent Ising machines / annealers — 2026 results

### A1. @peterlmcmahon — 2026-04-21 (thread, post 9/9)
- Claim: McMahon lab (Cornell) + Ruomin Zhu + USRA + Princeton preprint on arXiv 2604.17109: "A fully parallel densely connected probabilistic Ising machine" — p-bit hardware, established as promising alternative to [quantum annealers per truncated card].
- Why it matters: **substrate + falsifier** — fully parallel + densely connected is the hard combo (most p-bit machines fake one or the other). Thread root likely has measured perf. Group also ships `mcmahon-lab/cim-optimizer` (open CIM simulator) — free baseline for any annealing claim we test.
- URL: https://x.com/peterlmcmahon/status/2046424810624831630 · paper: https://arxiv.org/abs/2604.17109

### A2. Toshiba "Edge of Chaos" simulated bifurcation — April 2026 (press + APS; X coverage sparse/not yet indexed)
- Claim: third-gen GSB algorithm harnesses edge-of-chaos dynamics; ~99% success / ~100x speedup claims on fully-connected 2,000-spin Ising problems; Goto et al., Phys Rev + arXiv 2508.17655.
- Why it matters: **vocabulary + falsifier** — "edge of chaos" is the exact regime word our mycelial pack uses for substrate dynamics; here it is quantitatively measured (time-to-solution on 2k spins). Classical quantum-inspired algorithm beating annealers = baseline every annealing claim must now clear.
- URL: https://www.global.toshiba/ww/technology/corporate/rdc/rd/topics/26/2604-01.html · https://arxiv.org/html/2508.17655v1

### A3. Reality-check literature (context)
- 2026 arXiv "A Reality Check on Quantum Optimisation" (2607.13325) treats Fujitsu Digital Annealer as the practical lower bound quantum must beat; CIM field: Nature Comms 2026 polarization-symmetry-breaking CIM (s41467-026-68794-6), 4,096-spin programmable optoelectronic IM (Light Sci Appl 2026), million-spin photonic IM roadmap (arXiv 2607.13446).
- Why it matters: **falsifier** — the field is converging on honest baselines (DA/GPU) before claiming quantum advantage; matches our "trust bytes" doctrine.
- URL: https://arxiv.org/html/2607.13325v1

## B. Fungal / slime-mold / wetware computing

### B1. @NODEfather (Morgan Rockwell, Mycosoft founder) — 2025-01-06 (pre-window, instrumentation reference)
- Claim: built a new version of the FCI (Fungal Computer Interface) Probe — "can be plugged anywhere on earth directly into the soil… connect the Mycelium in the ground to the Internet." Media: 2 photos + 2 videos incl. ~2 min walkthrough (specs not in text).
- Why it matters: **sensor** — the only hobbyist-scale, deployable mycelium-to-internet probe found. Direct template for our mushroom-cube instrumentation (soil-insertable probe, remote telemetry). Mycosoft.com/sensing/fungi-compute-fci documents signal types: bioelectric activity, substrate contact, soil state, stimulation response.
- URL: https://x.com/NODEfather/status/1876130439133643221 · docs: https://mycosoft.com/sensing/fungi-compute-fci

### B2. @Mycosoft — 2025-05-06 (pre-window, vocabulary)
- Claim: "All Will Be Fungi" — interview with Morgan Rockwell "He Talks to Mushrooms and Builds Computers" (YouTube bC-ObnNatfo). Account: "We Build Sensors, AI & Droids For The Outside."
- Why it matters: **vocabulary + sensor** — Mycosoft is the live hobbyist-grade mycelium-computing stack (sensors + AI + DAO). Also: Global Fungal Computer Interface *market report* (Sept 2026, $12.76M by 2028 → $672M by 2040) — the discourse has a market-forecast layer now, all claim, no measured bytes.
- URL: https://x.com/Mycosoft/status/1919799851988222097

### B3. @PaulStamets — ~2025-12 (via search index)
- Claim: "mycelial networks that have sustained ecosystems for hundreds of millions of years may soon inspire sustainable, living technologies."
- Why it matters: **vocabulary** — the amplification layer. Big-reach accounts echo "living compute" without measurements; contrast lane for our falsifier stance.
- URL: https://x.com/PaulStamets/status/1991944643630838127

### B4. Adamatzky lineage (non-X context for the mushroom-cube test)
- "Towards fungal computer" (Royal Society Open Sci 2018): info = electrical spikes; computation needs controlled mycelium geometry; electrodes standard. "Mining logical circuits in fungi" (Sci Rep 2022). Fungar project. Physarum: tactile sensor (arXiv 1306.0258), PhyChip EU project, color-sensor protocols (RGB illumination → pattern response).
- Why it matters: **protocol** — the RGB-illumination response protocol and spike-recording electrode setup are directly liftable for the instrumented mushroom-cube falsification test.
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6227805/

### B5. @The_AI_Investor — 2026-03-08 (quoting @MAstronomers "petri dish of human brain cells learned to play DOOM")
- Claim: Cortical Labs CL1 = first commercial wetware computer. ~800k iPSC-derived human neurons on silicon MEA in sealed bioreactor; demo: ~200k neurons learned basic Doom gameplay in ~1 week via electrical reward/punishment (no code, no backprop). Specs: perfusion of glucose/amino acids, automated O2/CO2 + waste exchange, 37C, pH buffering, ~6-month viability then regenerate; ~30-33 W/unit, 30-unit rack 850-1000 W; $35k/unit, ~$20k/unit at rack scale, Cortical Cloud ~$300/wk per culture slot.
- Why it matters: **sensor + protocol** — the most complete published instrumentation stack for wetware (MEA + perfusion + thermal/pH control with real numbers). The 30 W/box figure gives our pack an energy baseline to falsify "living compute is cheap" claims. Caveat: single-account claims, not independently verified.
- URL: https://x.com/The_AI_Investor/status/2030483032738807943

### B6. @PulseLegacyAI — 2026-08-19
- Claim: "Organoid Web3" — bioreactors with living neurons as DePIN mining farms; AI agents pay stablecoins for nutrient solutions; claims wetware needs "six orders of magnitude" less energy than H100/Blackwell clusters and that living tissue "organically rewires" to evade censorship. ~66k views.
- Why it matters: **falsifier (negative)** — the crypto-speculative extreme of the wetware discourse. Both the 1e6x energy claim and the censorship-rewiring claim are unmeasured narrative — prime contradiction material for our pack.
- URL: https://x.com/PulseLegacyAI/status/2090154875699032552

### B7. OSU shiitake memristor (context; viral as "Shiitake > Silicon" reel, no canonical X post indexed)
- Claim: Lentinula edodes mycelium grown/trained as organic memristors, switching between electrical states thousands of times (LaRcco et al., PMC12513579, Oct 2025); Ohio State News coverage; viral reels on Facebook/Instagram.
- Why it matters: **falsifier + protocol** — the closest peer-reviewed substrate result to our planned mushroom-cube test: mycelium as memristive element with a repeatable grow-and-train protocol we can replicate and instrument. If our cube shows no memristive hysteresis under matched conditions, that is a real (small) falsification datapoint.
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC12513579/ · https://news.osu.edu/powered-by-mushrooms-living-computers-are-on-the-rise/

### B8. Wetware-adjacent X accounts to watch
- @koeng101 (Keoni Gandall): launched "American Wetware," a design studio for building with biology, biological compute layer.
- @ClariceDAiello: "totally open-source biotech wetware/hardware startup, zero IP, zero VC" — quantum-bio instrumentation person going open.
- Why it matters: **vocabulary + sensor** — open-hardware wetware is emerging as a lane; both are candidate collaborators/baselines for instrumented substrate tests.
- URL: https://x.com/koeng101 · https://x.com/ClariceDAiello

## C. Water / fluid / analog computing

### C1. Steve Mould — "I Made A Water Computer And It Actually Works" (YouTube IxXaizglscw; widely reshared on X, no single canonical X post indexed)
- Claim: working binary adder built from greedy-cup siphons + tubing + 3D-printed parts; logic gates from fluid dynamics.
- Why it matters: **falsifier + vocabulary** — the current gold-standard demo that substrate logic must actually compute (not just oscillate). Greedy-cup gate = bistable fluid element; directly comparable to our mushroom-cube "does it gate?" question.
- URL: https://www.youtube.com/watch?v=IxXaizglscw

### C2. MONIAC / Phillips machine landscape (context)
- Daniel de Bruin (NL artist): working hands-on MONIAC-inspired replica, operable by 1-4 people (danieldebruin.com/moniac). FT digital rebuild (2024); Cambridge + Erasmus virtual Phillips machines; NZIER machine (only working one in Southern Hemisphere) on loan at Reserve Bank Museum Wellington.
- Why it matters: **vocabulary** — MONIAC = the archetype of "analog computation of a living system (economy)" — the same move our pack makes with residual/registry/leaf as hydraulic metaphor. No new 2026 physical build announced as of this search.
- URL: https://danieldebruin.com/moniac/

### C3. Hackaday fluidic corpus (2021-2022, still the DIY canon)
- Water adders, Anderson ping-pong-ball water computer, pneumatic logic gates; Prakash lab water-drop synchronous computer (Stanford 2015) as the academic pole.
- Why it matters: **protocol** — gate topologies for fluidic XOR/AND are documented step-by-step; lowest-cost instrumented-substrate control experiment (fluid cube vs mushroom cube).
- URL: https://hackaday.com/2022/10/27/computing-fluidly/

## D. Local chip fabrication / ghetto fab

### D1. @szeloof (Sam Zeloof) — 2026-07-04
- Claim: "New name, same mission. Atomic Semi is now Fab2. Fab2 prints chips and fabs" (370k views). Prior post (~June 2026): "Next Phase is in Texas", hiring shift; 3rd building "FF1" under construction. SVIC page claims $500M Series A (unverified).
- Why it matters: **substrate + vocabulary** — the garage-fab lane institutionalizing into a company whose product is the fab itself. Watch fab2.com for published process docs.
- URL: https://x.com/szeloof/status/2073527770525614233 · https://x.com/szeloof/status/2048862460254523890

### D2. HackerFab IIT Bombay (student X/LinkedIn amplification, 2026)
- Claim: student-run DIY semiconductor fab built in 10 months for under ₹30 lakh (~$35k): DLP maskless lithography (~10 um), quartz tube furnace to 1200 C, DC plasma sputter. Open-source; descendant of CMU HackerFab.
- Why it matters: **protocol + falsifier** — a complete, costed, open bill of materials for benchtop silicon. The strongest existence proof that "fab" is a hobbyist-scale word now.
- URL: https://hackerfabiitb.github.io/

### D3. IIT (BHU) Varanasi — via Tiny Tapeout MPW (X, ~2026)
- Claim: institute's first-ever silicon tape-out completed through the Tiny Tapeout MPW Shuttle Program.
- Why it matters: **substrate** — Tiny Tapeout remains the cheapest real-silicon path (~$100-300 a design); the shuttle pipeline is the pack's realistic route to "our own silicon" without owning a fab.
- URL: https://twitter.com/user/status/2065122180615246085

## E. Thermodynamic computing — the promised follow-through (late additions)

### E1. @extropic — 2026-08-04
- Claim: full-stack announcement "Scaling Thermodynamic Computing: From One to One Billion": Z1 chip + hardware systems; Torx (stochastic programming framework); Thermalizers (thermodynamic compiler); live simulator API.
- Why it matters: **substrate + falsifier** — the live simulator API means the pack can probe thermodynamic sampling behavior WITHOUT silicon access. Z1 specs per press: 269,000 pbits, 8 cores, sub-12 mm die, <1 W; vendor claim 10,000x vs GPUs (chip-level) — not independently validated; skepticism centers on cherry-picked sparse/probabilistic workloads.
- URL: https://x.com/extropic/status/2084724127039115757 · https://extropic.ai/writing/from-one-to-one-billion/

### E2. Z1T technical overview — 2026-09-05 (Extropic publishing day)
- Claim: Z1T transformer-like model family for sparse probabilistic hardware; 140x inference energy-efficiency claim; weights open.
- Why it matters: **falsifier** — open weights + published recipe = the single most checkable efficiency claim in exotic compute right now. Nobody prominent on the timeline appears to have run the replication yet — that seat is open.
- URL: https://extropic.ai/writing/z1t

<!-- APPEND BELOW THIS LINE -->

## 8 best steals (ranked)

1. **Extropic full Z1 stack (E1/E2, Aug-Sep 2026)** — Z1: 269k pbits <1 W; Torx + Thermalizers + **live simulator API**; Z1T open weights with 140x claim. Best steal because it is *checkable now*: simulator API needs no chip; open weights need no NDA. One honest third-party number here reframes the entire exotic-compute discourse. (substrate + falsifier)
2. **Toshiba edge-of-chaos GSB (A2, Apr 2026)** — ~99% success, ~100x time-to-solution on 2,000-spin fully-connected Ising. "Edge of chaos" — the mycelial pack's favorite regime word — is now a *measured algorithmic dial* in a classical solver. Steal the framing: chaos injected on purpose, benefit measured in bytes. (vocabulary + falsifier)
3. **OSU shiitake memristor protocol (B7, PMC12513579)** — grow-and-train Lentinula edodes as memristors, thousands of switching cycles. Direct peer-reviewed baseline for the mushroom-cube test; matched conditions make our null result (if any) publishable-quality contrast. (protocol + falsifier)
4. **Cortical Labs CL1 instrumentation stack (B5, Mar 2026)** — MEA + perfusion + 37 C + pH + ~6-month viability + 30 W/unit at $35k. The most complete wetware sensor spec in circulation; gives the pack a hard energy baseline against "living compute is cheap." (sensor)
5. **McMahon lab fully-parallel densely-connected p-bit Ising machine (A1, arXiv 2604.17109)** + open `cim-optimizer` simulator. The hard combo (parallel AND dense) done in hardware, with a free software baseline for any annealing claim. (substrate + falsifier)
6. **Mycosoft FCI Probe (B1)** — soil-insertable mycelium-to-internet probe with documented signal classes (bioelectric, substrate contact, soil state, stimulation response). The instrumentation template for our cube; hobbyist-accessible. (sensor)
7. **HackerFab IIT Bombay (D2)** — full open DIY fab, ~$35k, 10 months, DLP litho ~10 um + 1200 C furnace + sputter. Ghetto fab made reproducible; a costed BOM beats a hundred threads about EUV. (protocol)
8. **Physarum RGB-response sensing protocol (B4)** — illuminate with R/G/B/white, read pattern response; plus spike-recording electrode canon from Adamatzky. Cheapest instrumented-substrate falsification protocol that predates the hype. (protocol + sensor)

## 3 things the timeline believes that our pack contradicts

1. **"Living compute is nearly free."** The timeline trades on 20 W exaflop brains (PulseLegacyAI's "six orders of magnitude" arbitrage), $672M FCI market forecasts, and Shiitake-greater-than-silicon reels — all claim, no measured workloads, no instrumentation published with error bars. Our pack contradicts: trust bytes, not reports — and the mushroom-cube falsification test exists precisely because nobody in this discourse files their raw signal. The CL1's own spec sheet (30 W per 800k neurons, 6-month lifespan, $35k) already contradicts its own hype, if you read the bytes.
2. **"Announcement = capability."** Tape-outs, $75M LOIs, $500M Series A claims, die shots and floorplans are treated as results (Z1's 10,000x is vendor-reported on cherry-pickable sparse workloads; Extropic's own LOI is explicitly non-binding). Our pack contradicts: DNA = residual + registry + leaf = *filed workdays* — a tape-out is not a benchmark; only third-party runs and open weights (Z1T) count as ore. The ronboger-vs-@georgeb poles are both narrative; the missing seat is the replication, and it is open.
3. **"The frontier is where compute happens."** The timeline's center of gravity is rack-scale, cloud wetware at $300/week, DePIN organoid mining farms, EUV. Our pack contradicts: sovereignty is local-first — and every genuinely falsifiable experiment found in this mine is benchtop-scale and nearly free: greedy-cup water gates, Physarum RGB protocols, a $35k open fab, a soil probe on a hobbyist BOM. Biology won as *metaphor* (edge of chaos is now literally a Toshiba algorithm parameter) while silicon and bytes remain the only place the evidence lives — which is exactly the pack's stance.

---
Mine closed 2026-09-16. Method note: X posts are poorly search-indexed; several findings are X-anchored via fxtwitter with press/paper cross-checks. No paid APIs; WebSearch + WebFetch only. No git commands run.

