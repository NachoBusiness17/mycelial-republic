# G-E: Fluid Logic Gate Library (receipt)

- **Lane:** wave / physical_computing / GAP G-E
- **Opened:** 2026-09-16
- **Agent:** research subagent (WebSearch/WebFetch only; no git; no paid APIs)
- **Scope:** What fluid/water logic gates exist (published + hobby), which compose (clock/register/memory), and what the MUD sim must support so $13 physical builds predict correctly.
- **Anchors:** `receipts/C18_HYDRAULIC_THIRD_CHANNEL.md` (siphon = NOT(A AND B) spec), `receipts/U3_UNION_HYDRAULIC_SIM.md` (MUD sim), two-bucket XOR (existing Dirac-layer primitive).
- **Status:** OPEN — gathering.

## Append log

(work appended below as research lands; receipt is written first, per wave-lane law)

### R1 — The anchor paper: Prakash & Gershenfeld 2007 (bubble logic)

**"Microfluidic Bubble Logic," M. Prakash & N. Gershenfeld, Science 315, 832–835 (Feb 2007).** Bits = air bubbles in liquid flowing through microchannels; interaction = bubbles passively routed at channel junctions by hydrodynamic resistance (low-Reynolds laminar flow, surface-tension dominated). This is the complete published gate set:

- **Combinational:** AND, OR, NOT, XOR (bubble presence at a junction diverts following bubbles — "a bubble is a bit").
- **Sequential:** **toggle flip-flop** (the published fluidic memory element — one-bit memory), **ripple counter**, **timing restoration**, **ring oscillator** (the published fluidic clock), electro-bubble modulator (active input).
- Physics of gain: bubble formation via surface tension amplifies small pressure perturbations into full-channel blockage — the fluidic transistor analogy.
- Sources: [Prakash Lab page](https://prakashlab.stanford.edu/publications/microfludic-bubble-logic) · [PubMed 17289994](https://pubmed.ncbi.nlm.nih.gov/17289994/) · [Prakash MIT thesis PDF](https://cba.mit.edu/docs/theses/08.09.Prakash.pdf) · [Physics World coverage](https://physicsworld.com/a/bubbles-compute-in-logical-devices/) ("one-bit memory, giving all components needed for a complete computing architecture").

**Answer to tease (2) starts here:** published fluidic memory = toggle flip-flop; published fluidic clock = ring oscillator (loop of NOT gates); published counter = ripple counter (T flip-flops chained). XOR + AND + delay → clock/register is exactly the bubble-logic architecture, demonstrated at the microscale, not at bucket scale.

### R2 — Microfluidic logic family tree (mechanisms beyond bubbles)

- **Droplet / hydrodynamic-resistance logic** (Cheow & Yobas, "Digital Microfluidics: Droplet Based Logic Gates"): a droplet occupying a channel changes hydrodynamic resistance; that change IS the signal. AND, OR, NOT implemented; cascadable. [ResearchGate](https://www.researchgate.net/publication/252819028_Digital_microfluidics_Droplet_based_logic_gates) · [HKUST portal](https://researchportal.hkust.edu.hk/en/publications/digital-microfluidics-droplet-based-logic-gates)
- **Non-Newtonian droplet logic** (PMC7283233): droplet gates that cascade into larger circuits for diagnostics. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7283233/)
- **Pneumatic logic** (PDMS Quake-style elastomeric valves controlled by pressure): the dominant "many-layer soft lithography" logic family — boolean ops via valve stacks; effectively a pneumatic transistor.
- **Passive flow-network logic:** combinations of fluidic valves / flow resistors, no external control; reviewed in "Logic Digital Fluidic in Miniaturized Functional Devices" (Electrophoresis 2016) and "Logic Operations in Fluidics as Foundation for Embedded Biohybrid Systems" (2023). [Wiley](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/10.1002/elps.201600429) · [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666998623003605)
- Common taxonomy across all families: (a) **pressure/resistance gates** (AND = series valves, OR = parallel, NOT = normally-open valve), (b) **threshold/stream gates** (Coanda wall attachment, turbulence amplifiers), (c) **volume/threshold gates** (siphon/fluid-diode — C18's family).

### R3 — MONIAC-era and classic 1960s fluidics (the digital branch)

**MONIAC (1949) is analog, not gate logic** — tanks/valves model continuous economic flows (C18 receipt already files it as lineage). The *digital* fluidics of that era is the 1959-onward **fluid amplifier** wave, which is the largest published gate library in any fluid:

- **NOT / NOR — wall-attachment (Coandă) amplifier:** a power jet pins to one wall via entrainment low-pressure bubble; a control pulse detaches it. Asymmetric bias → OR/NOR element; symmetric → bistable. Universal set = NOR. Harry Diamond Labs lineage: Horton patent US 3,185,166 (1959/1965), Warren bistable element US 3,228,410, Warren HDL TR-1061 (1962).
- **AND / NAND — jet-interaction (momentum) element:** two perpendicular control jets must both fire to deflect the supply jet into the AND port.
- **NOT — turbulence amplifier:** a laminar power jet is broken up by a small control jet; collector pressure drops. High fan-out, logically universal (NOR).
- **MEMORY — symmetric Coandă bistable flip-flop:** outputs partially feed back into the opposite control port; state persists with no moving parts. **This is the 1960s published fluidic memory element**, alongside **decade counters and shift registers** (serial memory; Warren TR-1061 covers both).
- **Systems built:** GE FLUIDIC-1 computer, TIMS + Sidewinder fluidic autopilots, Oak Ridge reactor monitoring, HDL no-moving-part respirator. Vortex amplifiers in Honeywell/GE engine fuel controls (RPM sensing >600 °C).
- **Hobby-reproducibility warning (directly relevant to the sim):** classic elements were photoetched (Dycril/Fotoform) and diffusion-bonded; nozzles 10–100 µm clog easily; lumped-parameter sims miss 3D vortex eddies — the archaeology doc proposes modeling channels as **R/L/C transmission-line elements** (acoustic delay, back-pressure reflections). At bucket scale the geometry is 1000× larger, which is exactly why C18 chose the siphon family instead.
- Source: [t81dev/digital-archaeology — Fluidic Logic Systems](https://github.com/t81dev/digital-archaeology/blob/main/excavations/fluidic-logic-systems.md) (aggregates Bowles & Horton 1961, Kirshner *Design Theory of Fluidic Components* 1966, Warren HDL TR-1061 1962, Foster & Parker 1970); [Britannica — Coandă effect](https://www.britannica.com/science/Coanda-effect).

### R4 — Bucket-scale water logic: the siphon family (C18's closest published kin)

- **Taberlet, Marsal, Ferrand & Plihon, "Hydraulic logic gates: building a digital water computer," European Journal of Physics 39, 025801 (2018, ENS Lyon):** an elementary **binary adder combining AND and XOR in a single device**, built from **test tubes and pipes**; bit = "a cup filled with water representing a 1, empty cup a 0"; mechanism = "**a siphon and a slow drain**"; units compose into a **full 4-bit adder**; and — the composability answer at water scale — "**a water clock can be incorporated**" so the machine runs "without any exterior intervention." [HAL hal-02408701](https://hal.science/hal-02408701v1) · DOI 10.1088/1361-6404/aa97fc. (Full PDF not fetchable from this tool — application/pdf unsupported; gate-level mapping quoted is abstract-level.)
- **Steve Mould hobby build (2021):** working 4-bit binary adder from **2D self-starting siphons** ("greedy cup" cells); "diverting water down one output or another depending on the TRUE or FALSE result"; first gate attempts "very illustrative, even if they didn't work very well" — iteration was required, i.e. real tolerance-fitting, same as C18's calibration gate. Hackaday commentary: gates "depend on water level and siphon action"; a commenter pairing the gates with a Pythagorean-siphon reset: "**We are very close to a counter here**" — the community's own composability gap statement. [FYFD writeup](https://fyfluiddynamics.com/2021/06/building-a-water-based-computer/) · [Mould video](https://www.youtube.com/watch?v=IxXaizglscw) · [Hackaday](https://hackaday.com/2021/04/26/logic-flows-literally-in-this-water-adder/)
- **Note vs C18:** both Taberlet and Mould use the SAME component C18's XOR uses — the crest-threshold siphon — confirming C18's "threshold instability beats steady-state flow balance" choice as the family with the best hobby track record at macro scale.

### R5 — Modern hobby air logic (the "PCB fluidic" question) and clocks

- **"PCB fluidic gates" verdict (honest):** no dedicated verified publication for etched-PCB *water* logic gates found this session (search rate limits blocked exhaustive confirmation; flagged, not fabricated — one search-tool fallback offered arXiv:2407.08660 as a fluidic-computing paper; verified it is a QCD physics paper, discarded). Nearest verified analogs: (a) the 1960s **photoetched Dycril/Fotoform fluidic panels** — literally that era's printed-circuit-style fluidic fabrication; (b) **3D-FDM-printed pneumatic ICs** — soiboi soft, 2025: printed membrane "air transistors" (flexible silicone membrane + rigid channels; vacuum on gate channel opens flow), cascaded into a **5-stage ring oscillator driving a walking soft robot from one air input**. [Hackaday](https://hackaday.com/2025/10/15/printing-an-air-powered-integrated-circuit-for-squishy-robots/); (c) **silicone "air transistor" dot-matrix display**, 2026: 2-input AND pixels (row AND column vacuum), multiplexed, electronics-free. [Hackaday](https://hackaday.com/2026/02/15/microfluidic-display-teaches-the-basics/) · [video](https://www.youtube.com/watch?v=VZ2ZcOzLnGg)
- **Fluidic logic primer (Hackaday "Computing Fluidly", 2022):** OR = merge two streams; NOT = control stream diverts a supply; "given enough inverters and OR gates, you can build everything else"; **bistable wall-attachment flip-flop = RS memory** (attributed to Ahem's 1966 patent US3348773A). Also cites **Univac FLODAC (1964)** — a digital fluid-logic computer prototype, the MONIAC-era's actual *digital* descendant — and a scanned Lukyanov integrator paper on archive.org. [Hackaday](https://hackaday.com/2022/10/27/computing-fluidly/)
- **Fluidic clocks in the wild:** Prakash & Gershenfeld ring oscillator (micro, 2007); Octobot's fluidic oscillator alternating soft-robot limbs (Harvard, 2016); soiboi 5-stage ring oscillator (macro air, 2025); Taberlet's "water clock can be incorporated" (water scale, 2018).

---

## SYNTHESIS

### (1) The gate library — NOT/AND/OR/XOR by physical principle

| Family | Bit encoding | NOT | AND | OR | XOR | Gain mechanism |
|---|---|---|---|---|---|---|
| **Siphon/water (C18's family, macro gravity)** | cup level = bit (filled=1) | constant weep-feed + input pushes level over overflow drain (output cuts); or self-priming siphon one-shot | shared cup, output crest reachable only if both inputs deliver (Taberlet carry) | merge streams into one cup (T junction) | **pulsed two-bucket: siphon = NOT(A AND B)** — one mark below crest, two marks prime + dump (C18, $13.04 spec) | threshold instability (prime/no-prime), binary and drift-immune |
| **Bubble logic (Prakash & Gershenfeld 2007, micro)** | bubble present/absent in channel | NOT via junction routing + surface-tension amplification | bubble blocks follower stream at junction | bubble merges streams | junction divert on bubble presence | surface tension amplifies pressure perturbation to full-channel blockage |
| **Droplet/hydrodynamic resistance (Cheow & Yobas)** | droplet occupancy = changed channel resistance | normally-open valve analog | droplet + droplet in series path | parallel paths | resistance-difference junction | hydrodynamic resistance change, cascadable |
| **Classic wall-attachment fluidics (1959–, gas or liquid jets)** | jet attached left/right (bistable) or flow present | **NOR = asymmetric wall-attachment amplifier** (universal); turbulence amplifier = high-fanout NOR | jet-momentum interaction: both control jets deflect supply into AND port | biased wall-attachment (OR path) | combinations of NOR elements | jet entrainment (Coandă low-pressure bubble); no moving parts |
| **Pneumatic membrane "air transistor" (1966–today; FDM-printed 2025)** | pressure present/absent | membrane valve, normally-closed/normally-open inversions | series membranes (AND pixels in the 2026 display) | parallel membranes | via NOR/NAND composition | membrane displacement; vacuum/pressure source |

### (2) Composability — what actually composes to clock and register

- **The complete published architecture is bubble logic:** AND/OR/NOT/XOR + **toggle flip-flop (memory)** + **ripple counter** + **ring oscillator (clock)** + timing restoration — "all components needed for a complete computing architecture" (Physics World on Prakash & Gershenfeld 2007). So yes: XOR + AND + delay builds a clock/register, and it has been demonstrated in fluid — at microscale.
- **The memory element, published:** (a) bubble-logic **toggle flip-flop** (2007); (b) classic fluidics **bistable wall-attachment flip-flop** (Ahem 1966, US3348773A) chained into **shift registers and decade counters** (Warren HDL TR-1061, 1962) — the 1960s serial memory; (c) at water scale, **still the open gap**: Taberlet 2018 gets the 4-bit adder and says a "water clock can be incorporated" (self-timed), and the Hackaday thread's own conclusion on Mould's adder is "**we are very close to a counter here**" — close, because the missing piece is a settable/resettable bistable, and the proposed mechanism (Pythagorean-cup siphon reset) is in the C18 component family.
- **The clock, published:** ring oscillator = odd chain of inverters + transport delay. Demonstrated in bubble logic (2007), soft-robot fluidics (Octobot 2016), and FDM-printed air logic (2025, 5 stages). At water scale the direct analog is a fill/drain loop through NOT stages with a drip-column delay — Taberlet's "water clock."
- **Ladder logic consequence:** with XOR (C18) + OR + NOT, the set {OR, NOT} is already universal (NOR); with the C18 siphon reinterpreted as NAND, {NAND} alone is universal. The library doesn't need many gates — it needs OR, NOT, and the siphon it already has.

### (3) What the gate library implies for the MUD sim (`water_computer.v1` + `mag/hydro_xor_sim.py`)

Sim must support, for physical builds to be predicted correctly:

1. **Merge/OR junction** — two inflows, one node, mass addition per tick (currently the sim has one intake per source; trivial but must be explicit).
2. **Generalized crest primitive** — the siphon state machine (prime height / dump rate / break hysteresis) exists in U3's code but must become a *parameterized reusable component*, since every siphon-family gate is the same primitive with a different crest-vs-mark ratio (XOR crest 150 mL; AND crest ~180 mL; NAND dump event; NOT overflow).
3. **Constant source entity** — a weep feed ("always 1") — new; needed for NOT and for the oscillator's bias.
4. **Overflow/drain-to-waste with system loss** — output that leaves the accounted system (sim currently reconciles mass into OUT/waste catch; NOT's overflow is a deliberate unaccounted-path loss that must still mass-balance to "waste").
5. **Transport delay** — tick-quantized latency per edge (pipe/drip column); required to predict the water clock, and it is exactly where U3 already found real physics (the ~8.3 mL post-break refill = closing-skew delay effect).
6. **Bistable latch entity** — a component with two stable level regimes plus input-driven switching and hysteresis; required the day the ladder attempts the memory element; can be pre-registered in sim before any physical attempt (that's a free falsifier).
7. **Scope declaration (the honesty rule):** the mark/tick lumped-parameter sim predicts the **threshold/volume family only**. The classic-fluidics recreators state wall-attachment/turbulence elements need PDE or transmission-line R/L/C models (acoustic delay, back-pressure reflections, 3D vortices) — so sim stones must NOT claim to predict Coandă-family builds without that machinery.

---

## APPENDIX — GATE LIBRARY TABLE + FIRST THREE GATES

### Gate library table (gate / principle / build difficulty at $13 scale / sim requirement)

| Gate | Principle | Build difficulty (bucket scale) | Sim requirement |
|---|---|---|---|
| OR | merge streams into one cup | trivial — one T junction, $0 | mass-add at node |
| AND | shared cup; output crest only both inputs reach | easy — one crest pipe | shared-volume accumulation + crest threshold |
| **NAND** | **C18's own spec: siphon = NOT(A AND B)** — the dump pulse is the output | easy — reuses the already-specced siphon + one AND cup | siphon primitive (exists) + waste path |
| XOR | pulsed two-bucket siphon (C18) | done — specced at $13.04, sim 15/15 (U3) | exists (siphon state machine) |
| NOT | constant weep-feed + overflow drain inverts presence | easy-medium — needs a steady low-rate source (new physics: dribble ≪ dump) | constant-source entity + overflow-to-waste + mass balance with loss |
| DELAY | drip column / long pipe; tick-quantized | trivial — tubing length | transport latency per edge |
| CLOCK (ring osc.) | odd chain of NOT + DELAY loop (water clock) | medium — 3 inverters + delay, self-timed | oscillator loop entity; divergence/limit-cycle check |
| MEMORY (T flip-flop) | bistable fill-state + siphon reset (Pythagorean-cup release) | hard — the published open gap at water scale | bistable latch entity with hysteresis (pre-register before building) |

### Recommended FIRST three gates for the $13 physical ladder after XOR

1. **OR** ($0): T-join the two C18 input lines into one cup; one tick each enabled → cup holds 1 or 2 marks. Tests mark conservation under merge (P6-style mass balance) — cheapest possible second data point.
2. **NAND** (~$0–2): C18's siphon reinterpreted — an AND cup (crest above single-mark level) whose crest pipe feeds the existing siphon; the dump pulse is NAND output. Smallest step on the ladder because the mechanism is already validated hardware; the spec itself names it ("siphon = NOT(A AND B)").
3. **NOT** (~$2): constant weep-feed cup + overflow drain; input water pushes level over the drain and cuts the output. Adds the one genuinely new physical mechanism (steady source vs dump rate) and completes a universal set: {OR, NOT} = NOR-universal; {NAND} = universal; XOR + AND + NOT = the full half-adder algebra.

After those: DELAY + NOT loop → water ring oscillator (the Taberlet "water clock" prediction the sim can pre-register); memory element last (hard, and the sim latch entity should be pre-registered first as a free falsifier).

---

**Receipt closes.** Sources: [Prakash Lab](https://prakashlab.stanford.edu/publications/microfludic-bubble-logic) · [PubMed 17289994](https://pubmed.ncbi.nlm.nih.gov/17289994/) · [Prakash thesis](https://cba.mit.edu/docs/theses/08.09.Prakash.pdf) · [Physics World](https://physicsworld.com/a/bubbles-compute-in-logical-devices/) · [HAL hal-02408701 (Taberlet et al. 2018)](https://hal.science/hal-02408701v1) · [FYFD on Mould](https://fyfluiddynamics.com/2021/06/building-a-water-based-computer/) · [Mould video](https://www.youtube.com/watch?v=IxXaizglscw) · [Hackaday water adder](https://hackaday.com/2021/04/26/logic-flows-literally-in-this-water-adder/) · [Hackaday Computing Fluidly](https://hackaday.com/2022/10/27/computing-fluidly/) · [Hackaday air-powered IC](https://hackaday.com/2025/10/15/printing-an-air-powered-integrated-circuit-for-squishy-robots/) · [Hackaday air-transistor display](https://hackaday.com/2026/02/15/microfluidic-display-teaches-the-basics/) · [digital-archaeology fluidic logic](https://github.com/t81dev/digital-archaeology/blob/main/excavations/fluidic-logic-systems.md) · [Cheow & Yobas droplet gates](https://www.researchgate.net/publication/252819028_Digital_microfluidics_Droplet_based_logic_gates) · [Britannica Coandă](https://www.britannica.com/science/Coanda-effect)

**Gaps/honesty flags:** (1) Taberlet full PDF not fetchable from this tool (application/pdf) — gate mapping quoted at abstract level; (2) "PCB fluidic gate" as a distinct water-scale publication not verified this session (rate limits; nearest verified analogs filed in R5, one hallucinated search result caught and discarded); (3) all WebSearch ran through a 429-prone proxy — repeated retries, some queries unanswerable.

— G-E out. Receipt ends with the gate library table and the FIRST-three-gates recommendation above.
