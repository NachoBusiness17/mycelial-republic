# G-G RECEIPT — Slow readout architecture for the myco-RAM layer (fading trace, minutes-scale)

- **Date opened:** 2026-09-16 · **Lane:** wave-lane (physical_computing) · **Law honored:** receipt FIRST, appended as I go. No git. No paid APIs (WebSearch/WebFetch only).
- **Inputs read before opening:** `watch/inbox/physical_computing/DESIGN_MYCO_MEMORY_20260916.md` (pyramid row: "VRAM/RAM = reservoir fading memory, seconds-minutes, capacity 0.048–0.209 (Telhan 2026)"); `receipts/C17_CUBE_INSTRUMENT_PLAN.md` (rig: ESP32-WROOM-32 + 2× ADS1115 differential, 8–16 SPS nominal / 1 Hz logging; PRBS-7 optical drive; Telhan-methodology ridge readout; S1 gate MC_peak > 0.05).
- **The gap:** RC literature assumes fast sampling vs substrate dynamics. Our channel: spikes last **~400 s** (minutes-scale). Three socratic questions, to be answered with sources:
  1. What readout architectures work at minutes-scale dynamics, beyond Telhan's ridge-on-slow-features? (delay-embedding · echo-state with long leaks · symbolic aggregation)
  2. Minimum sampling rate that preserves capacity for ~400 s spikes (Nyquist for the slowest meaningful feature)?
  3. What readout runs on ESP32-class silicon vs needs a host?
- **Deliverable at EOF:** recommended readout for cube 1 (algorithm + where it runs), the sampling answer, the capacity ceiling to pre-register.

---

## Research log (appended as gathered)

### Batch 1 — Telhan baseline pinned · leaky-ESN timescale law · delay-embedding/virtual nodes

**Telhan 2026 (the baseline we must beat/extend) — "Morphologically Tunable Mycelium Chips for Physical Reservoir Computing", O. Telhan et al., Sci Rep (2026), [nature.com/articles/s41598-026-55550-5](https://www.nature.com/articles/s41598-026-55550-5) · preprint [bioRxiv 10.1101/2025.08.20.671348](https://www.biorxiv.org/content/10.1101/2025.08.20.671348v1) · code MIT [github.com/otelhan/NeuromorphicMyceliumChip](https://github.com/otelhan/NeuromorphicMyceliumChip).** Standard RC characterization of hyphal chips: ridge-regression readout on nonlinear expansions of the measured signal (per C17 receipt: [x, x², sin3x, cos2x]), NARMA-10, dt=300 ms, linear memory capacity MC(K=10, 3 s lookback) = 0.209/0.052/0.048 across chips. Key structural fact: **Telhan's readout is offline, host-side, non-adaptive** — features are static nonlinearities of the channel, no reservoir state recursion on-device, no slow-timescale design. That is exactly the gap: nothing in the pipeline is *designed for* the 400 s scale; MC was measured at a 3 s lookback.

**Echo-state with long leaks (timescale matching) — the canonical law:** Jaeger & Lukoševičius, "Optimization and applications of echo state networks with leaky-integrator neurons" ([Neural Networks 2007](https://www.sciencedirect.com/science/article/abs/pii/S089360800700041X)): the leak rate α ∈ (0,1] sets the reservoir timescale; **Scholarpedia ESN (Jaeger)** states it explicitly: *"if the original system is evolving on a slow timescale, the ESN should do the same"*. Multi-scale control via leaking rate: [Frontiers in AI 2024](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1397915/full); time-history terms and reservoir dynamics: [Sci Rep 2024](https://www.nature.com/articles/s41598-024-59143-y); edge-of-stability leak analysis: [arXiv 2308.02902](https://arxiv.org/pdf/2308.02902). Filter neurons as an alternative timescale knob (TWIESN): [tech report](https://www.ai.rug.nl/minds/uploads/techreport2.pdf); delay&sum readout variant: [PDF](http://grh.mur.at/sites/default/files/ESNFilterDelaySum_0.pdf). **Implication for us:** an on-device ESN whose leak time constant is tuned to ~τ≈100–400 s (α = dt/τ) gives the readout a fading-memory buffer matched to the substrate instead of fighting it.

**Delay-embedding / virtual nodes — Appeltant et al. 2011, "Information processing using a single dynamical node as complex system", [Nature Comms 2:468](https://www.nature.com/articles/ncomms1476)** (thesis: [PDF](https://dspace.uib.es/xmlui/bitstream/handle/11201/2487/Appeltant_Lennert.pdf); review chapter: [CSIC PDF](https://digital.csic.es/bitstream/10261/189795/3/Photonic_Reservoir_Computing__Chapter5_2019.pdf); next-gen RC review: [PMC8455577](https://pmc.ncbi.nlm.nih.gov/articles/PMC8455577/)). Single nonlinear node + delayed feedback, input time-multiplexed into N **virtual nodes**; the delay length acts as the embedding dimension. **Transfer to slow channels:** the "delay loop" becomes a plain software ring buffer at minutes-scale — N taps × dt_sample spanning ≥ one spike width (400 s). This is Takens-style delay embedding wrapped in a linear readout: zero hardware cost, runs on anything, and unlike LI-ESN it needs no stability tuning.

**Next-generation RC (delay-embedding readout without a reservoir) — Gauthier et al., "Next generation reservoir computing", Nat Commun 2021, [PMC8455577](https://pmc.ncbi.nlm.nih.gov/articles/PMC8455577/)** (fetched full text). Trainable layer is *only* a ridge/Tikhonov linear readout over **delayed observations + low-order Volterra nonlinearities** ("observations of the input vector X at the current and at k-1 previous time steps spaced by s"); k=2–4 suffices because "the Volterra series converges rapidly"; sparse delay spacing s=5 used deliberately to form a Takens embedding. Warm-up drops from 10³–10⁵ steps to sk steps; training "<10 ms using Python on a single-core desktop processor". Sampling note: dt set relative to the system's Lyapunov time (~1/31–1/44) and adjusted when the dynamics got slower. **Implication:** the NG-RC recipe is a *reservoir-free* readout that inherits its memory from an explicit delay line — exactly the right shape for a 400 s substrate, and cheap enough for ESP32 inference.

**Interim architecture scorecard (Q1):**
| Approach | Slow-dynamics fit | On-device fit | Risk |
|---|---|---|---|
| Telhan-style static ridge [x, x², sin3x, cos2x] | none — no temporal features, 3 s lookback only | trivial (1 MAC row) | it's the status quo; cannot read minutes-scale trace |
| Delay-embedding + ridge (Takens / NG-RC-lite) | direct — buffer span set in seconds, not samples | trivial (N_tap × K MACs) | needs delay-buffer RAM; feature count grows with taps |
| LI-ESN with long leak (α = dt/τ, τ≈100–400 s) | canonical — Scholarpedia timescale-matching law | easy inference (N MACs/step); training host-side | stability/edge-of-chaos tuning; drift may move optimum |
| Full NG-RC Volterra on delays | good — adds pairwise nonlinear terms | fine at k=2, few taps | feature count blows up if taps many (quadratic terms) |
| Symbolic aggregation (SAX/PAA) | good for classification, loses amplitude gradations | cheapest of all (integer ops) | readout only discrete/categorical states |

### Batch 2 — edge-RC reality check (Q3, part 1)

**No off-the-shelf "ESN library for ESP32" exists**; the published pattern is: **train offline on host (Python/Julia), export fixed reservoir + trained readout weights as C/C++ to the MCU**. ESN inference is tiny (sparse fixed weights, only the linear readout is learned), which is why ESNs are repeatedly positioned as edge-friendly vs CNN/RNN.

- [Nanoelectronics-enabled reservoir computing hardware for edge AI, Sci Adv 2025](https://www.science.org/doi/10.1126/sciadv.adu2663) ([PMC11939057](https://pmc.ncbi.nlm.nih.gov/articles/PMC11939057/)) — memristor RC edge system that literally uses an **ESP32-CAM** as its real-time wireless vision front-end; RC inference at the edge is the demonstrated regime.
- [Hardware-oriented ESN on FPGA, Atlantis Press](https://www.atlantis-press.com/journals/jrnal/125940366/view) — fixed-point math + sparse reservoir design principles transfer directly to MCU (cited 29+).
- [Minimal Deterministic Echo State Networks, arXiv 2507.06050](https://arxiv.org/html/2507.06050v1) — deterministic reservoir weights outperform random ones → reproducible on-device, no seed lottery.
- [ESNv2/ParalESN, OpenReview](https://openreview.net/forum?id=N6G2Mmz8qs) — diagonal/deterministic linear reservoirs, cheapest possible state update (pure leak integration) — MCU-native shape.
- [Physical reservoir computing for Edge AI, The Innovation Materials 2024](https://www.the-innovation.org/data/article/materials/preview/pdf/XINNMATERIALS-2024-0101.pdf) — survey framing physical RC as the edge-AI substrate.
- Tooling for the host side: [ReservoirComputing.jl](https://github.com/SciML/ReservoirComputing.jl) (or plain sklearn ridge — Telhan's own repo uses Python ridge).
- ESP32 budget check vs rig (C17): WROOM-32 = 240 MHz dual-core + single-precision FPU, 520 KB SRAM (+ optional PSRAM); ADS1115 is 8–16 SPS nominal — **the sensor bus, not the CPU, is the bottleneck**; any of the candidate readouts (delay+ridge inference, LI-ESN inference, RLS online adaptation at K≤64 features) fits in microseconds-per-sample at 0.1 Hz.

### Batch 3 — sampling rate vs capacity (Q2)

**The governing relation (standard RC result, stated across the canon):** a reservoir's linear memory capacity in *samples* is roughly the integral of the memory curve ≈ **forgetting time constant τ_mem measured in units of the sampling interval Δt** — MC_samples ≈ τ_mem/Δt (see [Integer ESNs, arXiv 1706.00280](https://ar5iv.labs.arxiv.org/html/1706.00280) "forgetting time constant"; [Tailoring ESNs, PMC7452343](https://pmc.ncbi.nlm.nih.gov/articles/PMC7452343); [Dynamic memristor RC, RSC 2024](https://pubs.rsc.org/nr/article/16/29/13847/859311/Dynamic-memristor-for-physical-reservoir-computing) defines MC = Σ_k MC_k). Corollary: **lookback in seconds ≈ τ_mem regardless of Δt; what Δt buys is independent taps per spike and Nyquist protection.**

Applied to our channel (spike width ~400 s, PRBS-7 bit = 300 s per C17):
- **Nyquist floor:** slowest meaningful feature f ≈ 1/400 s = 2.5 mHz → fs ≥ 2·f = **5 mHz (Δt ≤ 200 s)**. This preserves *existence* of the trace, nothing more.
- **Capacity-preserving rate:** linear readouts want ≥ 10 independent samples per shortest feature → **Δt ≈ 20–40 s (0.025–0.05 Hz)** keeps MC_samples ≈ 10–20 *inside one spike window* and keeps the delay buffer ≤ 60 floats.
- **Anti-alias guard:** faster biology exists (fungal spikelets at 1–10 Hz in the Adamatzky canon; LaRocco switching at 5.85 kHz per C17). Undersampled fast events fold into the slow band and masquerade as "memory". Mitigation: keep the rig's cheap 1 Hz raw log (it already exists) and run the slow readout on block-aggregated features — dual-rate, not downsampling.

### Batch 4 — symbolic aggregation + slowness principle (completing Q1's option space)

- **SAX** — Lin, Keogh et al.: first symbolic time-series representation with dimensionality reduction + lower-bounding distance ([UCR SAX page](https://www.cs.ucr.edu/~eamonn/SAX.htm); ["Experiencing SAX"](https://tslearn.readthedocs.io/en/stable/gen_modules/piecewise/tslearn.piecewise.SymbolicAggregateApproximation.html); PAA+symbol lookup = integer ops only — the cheapest possible on-device readout; modern multivariate variant: [Inf. Sci. 2026](https://www.sciencedirect.com/science/article/pii/S0020025526007504)). Fits the "symbolic aggregation" option: each 400 s window → a short symbol string; the myco-RAM "word" becomes inspectable, and mismatch detection is Hamming distance.
- **Slowness principle / SFA** — Wiskott & Sejnowski, "Slow feature analysis: unsupervised learning of invariances", Neural Computation 14(4):715–770 (2002), [PubMed 11936959](https://pubmed.ncbi.nlm.nih.gov/11936959/) (cited ~1,950): learn features that *change as slowly as possible* via nonlinear expansion + slow-component extraction. This is the principled version of what Telhan does by hand ([x, x², sin3x, cos2x] + ridge) — SFA picks the slow coordinates *by objective*, not by folklore. Incremental SFA exists (IJCAI 2011) if adaptation is ever needed on-device (still host-trained initially).
- Survey anchor: Tanaka et al., "Recent advances in physical reservoir computing: A review", Neural Networks 115:100–123 (2019), DOI 10.1016/j.neunet.2019.03.005 [canon, not re-fetched this session — verify before promotion]; fetched-survey substitute: Gauthier 2021 (above). Edge-RC survey: [The Innovation Materials 2024](https://www.the-innovation.org/data/article/materials/preview/pdf/XINNMATERIALS-2024-0101.pdf).

---

## SYNTHESIS — answers to the three socratic questions

### Q1. Readout architectures for minutes-scale dynamics (beyond Telhan's ridge-on-slow-features)

Telhan's readout has **no temporal design in it** — static nonlinearities + ridge, MC measured at 3 s lookback. It works because the chip's transient is fast (step response relaxes in 1–2 samples at 300 ms). At 400 s scale that pipeline is blind. Four graded upgrades, all ridge-trained (so Telhan-methodology comparability survives), differing in where the memory comes from:

1. **Delay-embedding ridge (Takens / NG-RC-lite) — recommended for cube 1.** Features = delayed observations spanning ≥ 1 spike width (e.g., taps at 0, 20, 40, … 400 s) + low-order Volterra terms on adjacent taps (k=2 like NG-RC). Memory is *explicit* — a ring buffer, not a tuned dynamical system. Nothing to destabilize, trivially auditable, exactly reproduces Gauthier's finding that k=2 suffices when the Volterra series converges fast.
2. **LI-ESN with leak matched to the substrate** (α = Δt/τ, τ ≈ 100–400 s). Canonical timescale-matching law (Jaeger/Lukoševičius 2007; Scholarpedia: "if the original system is evolving on a slow timescale, the ESN should do the same"). Use only if stage 1 under-delivers — it adds edge-of-chaos tuning burden and a seed lottery (mitigated by deterministic reservoirs, arXiv 2507.06050).
3. **SFA-preprocessed ridge** — replace hand-picked [x, x², sin3x, cos2x] with slow features extracted by objective (Wiskott & Sejnowski 2002). Orthogonal to 1 and 2; do it at analysis time on the host.
4. **Symbolic aggregation (SAX over 400 s windows)** — the fallback/heartbeat readout: integer ops, Hamming-distance "did the trace change" checks, survives quantization of the 16-bit ADC. Loses amplitude gradation; never the primary capacity measurement, always the cheap on-device tripwire.

### Q2. Minimum sampling rate for ~400 s spikes

- **Nyquist floor:** fs ≥ 2/400 s = **5 mHz (one sample per 200 s)** — preserves existence of the slowest meaningful feature, nothing more.
- **Capacity-preserving operating point: 0.025–0.05 Hz (Δt = 20–40 s)**, because MC_samples ≈ τ_mem/Δt and a linear readout wants ~10+ independent taps inside one spike window. At Δt = 20 s: ~20 usable samples per spike, buffer = 20–60 floats.
- **Do not actually downsample the rig:** keep the 1 Hz raw log (already running per C17) and compute the slow readout on block features. This protects against aliasing of 1–10 Hz spikelets into the "memory" band and preserves the spike-count feature used in the S2 trials.

### Q3. ESP32-class vs host

**On the ESP32 (inference + light adaptation):** delay-buffer + ridge dot product (≤ 64 features → microseconds per update at 0.05 Hz), SAX symbol emission, optionally **online ridge adaptation via recursive least squares at K ≤ 64** (K² work per step ≈ 4k MACs — trivial); determinstic LI-ESN inference likewise fits. Precedent: ESNs are standard edge-AI recommendations; an ESP32-CAM is literally the front-end of the 2025 Science Advances memristor-RC edge system. **On the host (training + audit):** the ridge solve itself (SVD/Cholesky over full trial history), permutation surrogate tests (100 shuffles), SFA feature extraction, LI-ESN training, drift retraining, and weight export to flashed constants. **Rationale:** the pipeline stays Telhan-comparable (analysis code committed first, host-side, same MC methodology per C17 S1) and the rig's bottleneck is the ADS1115 bus, not the CPU. The device never needs to train from scratch; it re-fits readout weights incrementally at most.

---

## FINAL — G-G closure (per lane law)

**Recommended readout for cube 1:** **Host-trained ridge regression over a 20-tap delay embedding (taps every 20 s, span 400 s) of block-aggregated slow features, plus pairwise (Volterra k=2) terms on adjacent taps — i.e., NG-RC-lite — trained on the host with Telhan's MC methodology, deployed to the ESP32 as fixed weights for on-device inference with optional RLS re-fit.** SAX symbol stream (window = 400 s, alphabet ≤ 4) runs alongside as the integer-ops tripwire. Escalation path if MC is under pre-registered gate: swap delay ridge → leak-matched LI-ESN (α = Δt/τ) and SFA-selected features — both still host-trained.

**Sampling answer:** Nyquist floor = 5 mHz (Δt ≤ 200 s) for 400 s features; **pre-registered slow-rate = 0.05 Hz (Δt = 20 s)**, giving ~20 independent taps per spike window (MC_samples ≈ τ_mem/Δt); raw 1 Hz log retained for anti-alias protection and spikelet census.

**Capacity ceiling to pre-register (falsifiable):**
1. **Trace depth:** fading-trace memory does not extend past **2 spike widths (≈ 800 s)**. MC(k) at k > 800 s must sit at the shuffled-surrogate floor (p < 0.05, 100 surrogates). Anything beyond 800 s is the *disk* layer (hyphal remodeling) stealing RAM-layer credit — pyramid says reclassify, not celebrate.
2. **Amplitude ceiling:** linear readout resolves **≤ 4 trace levels (≤ 2 bits) per 400 s window** per channel. Beating this reliably = ceiling falsified in the interesting direction → upgrade the pyramid row, with surrogates attached.
3. **Absolute MC bar:** MC_total = Σ MC(k) ≤ **25** (τ_mem ≈ 500 s / Δt = 20 s), MC_peak ≤ **0.25** at lags 20–400 s, with the C17 proceed gate (MC_peak > 0.05) unchanged. Telhan's chips (0.209 peak at 3 s lookback) remain the cross-substrate comparison bar.

*Receipt closed 2026-09-16. Sources free-tier (WebSearch/WebFetch). No git, no paid APIs. Next promotion step: fold §FINAL into C17 stage-1 analysis plan as S1.2b (delay-embedding readout) before the first 72 h log lands.*

