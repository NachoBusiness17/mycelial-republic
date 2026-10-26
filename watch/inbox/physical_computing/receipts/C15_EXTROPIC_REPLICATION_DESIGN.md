# C15 — EXTROPIC Z1T 140× REPLICATION DESIGN — receipt

Lane: physical_computing / new $0 stone from the Sep-16 X mine (pack §6.2).
Method: WebSearch + WebFetch only (free), no paid APIs, no git. Append-as-you-go.
Status: CLOSED 2026-09-16 — design complete, GO scoped (Lane 1 immediately, Lane 2 reduced config; NO-GO this week on full-config).
Sources already on disk: `docs/ref/EXTROPIC_Z1T_DIGEST_20260904.md` (vendor fine-print
digest), `receipts/X_MINE_PHYSICAL_20260916.md` (E1/E2, the open replication seat),
`PHYSICAL_COMPUTING_PACK_20260916.md` §4 (DAD discipline), `receipts/SALON_FREE_20260916.md`
(Landauer ceiling ≈ 1.05×10¹³ samples/J).

## Deliverable

A $0 replication protocol the fleet (or anyone) can execute: named workload, our-side
full-system energy/time accounting (encode → simulate → decode → verify), tuned digital
baseline, pre-registered confirm/kill thresholds — plus an honest scope note on what a
simulator run can and cannot falsify, an effort estimate, and a go/no-go for this week.

<!-- APPEND BELOW THIS LINE -->

## §1 Artifact hunt — what is actually public (appended as found)

### 1.1 The two canonical pages (fetched 2026-09-16)

**Aug 4 drop** (https://extropic.ai/writing/from-one-to-one-billion/):
- Z1 revealed: ~269k pbits (269,568 per die figure), sparse 16-neighbor graph, chromatic
  Gibbs on an Ising EBM, >50 MHz, <1 W, <12 mm die. Form factors (M.2 stick 2-chip,
  PCIe card 16-chip, billion-pbit cluster) — **"early access" in 2027**. No chips to us.
- **Torx**: open-source stochastic differentiable programming framework, live day-of at
  docs.torx.ai + GitHub (`extropic-ai/torx`), whitepaper arXiv 2608.01612. Pitch:
  "Torx is to THRML what PyTorch is to CUDA."
- **Thermalizers**: variational compiler mapping Torx kernels onto Z1 hardware-aware EBMs.
  Blog says "LIBRARY COMING SOON" (GitHub release promised); whitepaper arXiv 2608.01615.
  Headline on suitable workloads: "up to 10,000x greater energy efficiency than GPUs."
- **Simulator API**: the page says only "Early access to a GPU simulator for Torx and
  THRML programs on high-performance GPU simulators," with **extropic.dev** as the sole
  access path. NO pricing, NO sign-up mechanics, NO approval criteria published on the page.

**Z1T page** (https://extropic.ai/writing/z1t): matches our digest exactly (139×/28×/14×
table, 294.52 nJ/token = 8.74 nJ Z1 + 285.78 nJ FPGA, projection-anchored, logit readout
excluded). Open artifacts: HF `extropic-ai` weights + GitHub `extropic-ai/sparse-transformers`
training recipe. **Fashion-MNIST is NOT named on either canonical page.**

### 1.2 Access path recon

- **extropic.dev** = "Extropic // Console" — a JavaScript SPA; zero static content. The
  sign-up/tier/approval reality is behind an interactive console, not published prose.
  Blog wording is **"Early access"** — i.e., an application/waitlist posture, not a
  self-serve free tier (as of fetch). Treat hosted-GPU-simulator access as UNVERIFIED
  until someone with a browser session walks the console.
- **Torx is locally runnable, free, no key**: docs.torx.ai (redirects to
  extropic-torx.readthedocs-hosted.com) — "Install with `pip install extro-torx`
  (Python 3.11+)", JAX-based, primitives pbit/pdit/pmode, gates structure-only with
  parameters as "logit leaves", quickstart runs `BranchingSimulator(num_samples=20_000)`
  **entirely locally**. No API key, quota, pricing, or approval anywhere in the docs.
  => The free lane is: **Torx local simulation, our GPUs, our joules metered by us.**
- **Hugging Face org** (huggingface.co/extropic-ai): exactly one public model —
  **Z1T-0** (text generation, 639 downloads, 30 likes, updated ~2026-09-04). No datasets
  public, no Fashion-MNIST DTM artifacts on the org page. Team: extropico, seth-morton.
- GitHub org fetch timed out twice (github.com/extropic-ai and /thrml) — retrying via
  raw.githubusercontent.com. Known repo names from the blogs: `torx`, `sparse-transformers`,
  `thrml` (pre-existing THRML framework Torx supersedes).

### 1.3 The named workload located — Fashion-MNIST DTM (found via WebSearch)

- **Primary paper**: arXiv **2510.23972** "An efficient probabilistic hardware architecture
  for diffusion-based modeling" — Jelinčič, Lockwood, Garlapati, Schillinger, Chuang
  (yes, that one), Verdon, McCourt. v1 2025-10-28, v2 2025-12-10, 13 pp, CC BY-NC-ND 4.0.
  Peer-reviewed version: **npj Unconventional Computing** (s44335-026-00075-3, 2026).
- Claim shape (abstract): an "all-transistor probabilistic computer" implementing denoising
  at the hardware level reaches "performance parity with GPUs" on "a simple image benchmark"
  using "approximately 10,000 times less energy". **Note the verb: "could reach" — device-
  based projection**, same posture as the Z1T table.
- **Fashion-MNIST is the benchmark** (28×28 grayscale, per the HN thread on the paper,
  news.ycombinator.com/item?id=45750995 — community flag: benchmark simplicity). The
  vendor blog telling the same story is "Thermodynamic Computing: From Zero to One"
  (extropic.ai/writing) — Fashion-MNIST-like images, ~10,000× less energy than a GPU VAE.
- Mechanism: DTM = Denoising Thermodynamic Model — an EBM trained via THRML that reverses
  a noising chain by Gibbs-sampling on the TSU/pbit fabric; each denoise step is native
  EBM sampling instead of a monolithic diffusion net.

### 1.4 THRML — the free software lane (extropic.ai/software, fetched 2026-09-16)

- THRML = JAX library for probabilistic graphical models: "thrml uses JAX to massively
  accelerate simulations of PGMs", supports **simulating TSUs**, exploring chip
  architectures (connection graph, node type, design parameters), and **gradient
  computation to train EBMs**. Tagline: "Library and examples available now."
  Labeled **Open Source**; repo github.com/extropic-ai/thrml. License string not shown
  on the marketing page (repo check pending — GitHub timing out).
- Relationship: "Torx is to THRML what PyTorch is to CUDA" — Torx (pip `extro-torx`,
  JAX, pbit/pdit/pmode, local `BranchingSimulator`) is the upper framework; THRML is the
  PGM/simulation layer. Both run **locally, free, no API key**.
- Hardware/simulated-hardware access: the software page offers only a **research grant
  application** ("Submit a proposal") and an org collaboration form for large probabilistic
  workloads. **No published pricing, no self-serve tier, no approval SLA.** => the hosted
  GPU-simulator console (extropic.dev) is gated on an application we have not filed;
  everything replication-relevant is available without it.

### 1.5 Access-tier verdict (step 1 answer)

| Artifact | Public? | Tier / gate |
|---|---|---|
| THRML (PGM sim + EBM training, JAX) | Yes — "available now", open source | Free, local, no key (repo/license to verify when GitHub unthrottles) |
| Torx (stochastic programming framework) | Yes — pip `extro-torx`, docs live | Free, local, no key, Python 3.11+, JAX |
| Thermalizers (compiler, Torx→Z1 EBMs) | Whitepaper only (arXiv 2608.01615) | Library "COMING SOON" — not usable yet |
| Z1T-0 weights | Yes — HF `extropic-ai/Z1T-0` (639 downloads) | Free download; model card not yet inspected |
| Z1T training recipe | Yes — GitHub `extropic-ai/sparse-transformers` | Free (repo inspection pending) |
| Hosted GPU-simulator API (extropic.dev) | Console exists; blog says "early access" | **Application/waitlist posture; no published tier, quota, or pricing — treat as NOT self-serve today** |
| Z1 silicon | No | 2027 "early access"; grant/collab forms only |

**Consequence for the mission:** the replication does NOT need the hosted simulator.
The published claims were themselves produced on GPU simulation of the pbit dynamics
(THRML/Torx are simulation-first), so a same-tier replication — our JAX sim vs our tuned
digital baseline, both metered on our hardware — is a like-for-like audit of the SOFTWARE
claim. The hosted console would only matter for vendor-optimized kernels; note it as an
optional stretch (file the free grant application in parallel; costs nothing but prose).

### 1.6 The replication kit exists (GitHub API, anonymous curl — free)

- **`extropic-ai/thrml`** — "Thermodynamic Hypergraphical Model Library in JAX",
  **Apache-2.0**, 1,160 stars. PyPI `thrml` 0.1.4 (Python ≥3.10, deps equinox +
  jaxtyping): block-Gibbs sampling of sparse heterogeneous PGMs, `SpinNode`/`IsingEBM`,
  `SamplingSchedule`, two-color Gibbs quickstart. docs.thrml.ai ships 4 notebooks
  (Getting Started; All of THRML; Spin Models — block-Gibbs throughput measured on
  8×B200s; +1) and a codon-optimization walkthrough with repro code.
- **`pschilliOrange/dtm-replication`** — the DTM paper's own research code (Peter
  Schillinger, co-author), built on thrml, pushed 2025-10-29, 37 stars. README:
  "Training and FID evaluation are currently setup for **MNIST and Fashion-MNIST**";
  `DTM()` class with fully configurable hyperparameters/graph topology; logs **FID and
  autocorrelation** per epoch; `figures/` ships **scripts + CSV data** for the paper's
  Figure 5 (grayscale binomial nodes; MEBM vs DTM vs DTM+ACP; degree + chain-depth
  ablations). **No LICENSE file** — readable and runnable, but do not redistribute;
  we publish OUR harness + numbers, not their code.
- **Z1T-0 model card is a stub** ("Open weight for the first Z1T-0" — one line; no
  license, no params, no benchmark). The `sparse-transformers` recipe repo carries the
  substance (direct fetch timed out; inspect when GitHub unthrottles).

## §2 The DAD-accounting replication protocol (pre-registered)

Law in force: pack §2 canon #2 ("device-only numbers are reports; DAD instrumentation is
bytes"), pack falsifier §4.2 ("any substrate claim carried forward must publish its
encode/decode/verify overhead share"), brief §2.4 ("until someone publishes measured joules
per **independent** sample on a **named workload**, the commercial claim is a
well-motivated extrapolation"), salon Landauer ceiling (receipt
`SALON_FREE_20260916.md`: ESS/J "hard physical ceiling ≈ 1.05×10¹³ samples/J" — lane lead,
re-derive before relying, see step 0).

**Named workload**: Fashion-MNIST DTM (arXiv 2510.23972; vendor config in
`dtm-replication`, `data.dataset_name="fashion_mnist"`). This is the published benchmark
behind the "parity with GPUs at ~10,000× less energy" claim, and the same sampling engine
underlies the Z1T 140× table — one workload audits both claims' software half.

**Full-system segments metered on our side** (each segment: wall-clock + CPU time +
energy-bytes where obtainable + bytes moved; overhead share published per pack §4.2):
1. **ENCODE** — Fashion-MNIST batch → pbit graph (binarize/grayscale-level map, Ising EBM
   embedding, hypergraph build).
2. **SIMULATE** — the native step: block-Gibbs sampling of the DTM denoise chain (THRML
   runtime; this is the vendor's own substrate-simulation path).
3. **DECODE** — pbit sample means → pixel values → images (dy4p-style averaging cost).
4. **VERIFY** — FID + autocorrelation → ESS computation.

**Baselines, same machine, same workload, same accounting:**
- **B1 — plain Gibbs**: hand-written JAX/PyTorch block-Gibbs on the *identical* EBM and
  schedule, no THRML machinery. Tests whether the framework's compiled block sampling
  beats a tuned straightforward implementation (framework value, positive or negative).
- **B2 — tuned digital sampler**: best digital Gibbs we can write, tuning budget logged.
  (Full VAE/diffusion baselines are GPU-class; on CPU we compare sampler-to-sampler and
  read the paper's GPU-quality numbers from their CSVs as reference, marked REPORT.)
- **B3 — vendor CSV audit (zero training)**: their shipped `figures/**.csv`
  autocorrelation data → integrated autocorrelation time → **ESS per raw sample**.

**Normalization**: all rows reduce to **ESS/Joule and ESS/second, full-system** (raw
samples → ESS via the autocorrelation the vendor itself logs — "independent sample" is
the brief's own word, and it is where samples-based claims usually inflate).

**Step 0 — ceiling re-derivation (before any run):** recompute the salon ceiling from
k·ln2 at 300 K and the assumed flips-per-independent-sample, and state the derivation in
our CSV. Then apply it: the vendor projection 1.3×10⁻¹⁴ J/sample ⇒ **7.7×10¹³ samples/J
claimed — already ≈7× ABOVE the salon ceiling of 1.05×10¹³ samples/J** as written. If the
step-0 derivation survives, the Z1 sampling-energy projection is flagged physically
implausible *before we measure anything*; if it doesn't survive, we correct the salon
number (also a win — receipts over canon).

**Pre-registered thresholds (set now, before execution):**
- **CONFIRM (software claim survives us):** (a) our reduced-config DTM Fashion-MNIST FID
  within 2× of the paper's value at comparable config (read from their CSV); (b) the
  sparse-FLOP penalty reproduces at 5–20× (their claim ~10×, stated against interest);
  (c) THRML-simulated dynamics ≥ parity vs B1 per ESS/s; (d) DAD overhead share published
  with every number. => "140× survives as a software claim to the extent testable; the
  remainder is silicon-borne and pre-registered below."
- **KILL:** (1) our FID > 2× paper value under their config at replicated scale;
  (2) **ESS/raw-sample < 0.01 from their own CSVs** → every samples-based claim inflates
  >100× regardless of silicon; (3) **B1 ≥ 10× faster per ESS than the THRML sim** → the
  algorithm carries no advantage and 100% of the claimed win rests on unmeasured silicon
  physics; (4) step-0 ceiling stands ⇒ the 1.3e-14 J/sample projection is marked
  physically implausible and the 140× headline inherits the flag.
- **The 140× headline itself is unreachable by simulation in either direction** — it is a
  device projection (digest: Z1 side of every number is "theoretical chip energy ... best
  estimates"). What we can do is bound its software components (a–d above) and audit its
  arithmetic (digest already found the logit-readout exclusion drops it to ~2.9×).

## §3 Honest scope note — what a simulator run can and cannot falsify

**CAN falsify (software claim):** that the DTM trains to GPU-parity quality on
Fashion-MNIST; that sparsity costs only ~10× FLOPs; that the sampled bits are effectively
independent (ESS); that the open artifacts reproduce at all; that the framework adds value
over a tuned Gibbs baseline; the internal arithmetic of the energy table.
**CANNOT falsify (silicon claim):** 1.3×10⁻¹⁴ J/sample on-die; 50 MHz native sampling;
<1 W at 269k pbits; fab-portability; the 2027 form factors; therefore **not the 140×
number itself** — a simulation agreeing with the vendor tells us the *algorithm* is sound,
and a simulation disagreeing tells us the algorithm alone cannot carry the claim.
**Per pack falsifier §4.5** (no sim stone counts as substrate evidence until a physical
artifact confirms a sim prediction): this stone's honest output is **a bounded independent
audit of the software claim + a pre-registered silicon test protocol** for whoever next
has hardware access (grant route or 2027 early access). It is NOT substrate evidence, and
saying so is the pack working. The Z1's own X0-successor chip is the missing third
channel; our protocol hands its future operator the exact metering script.

## §4 Effort estimate and $0 fit

- **Lane 1 — vendor CSV ESS audit** (~1 session, pure pandas): read their
  autocorrelation CSVs → ESS/raw-sample → claimed samples/J → ESS/J vs step-0 ceiling.
  Deliverable: the >100×-inflation check on their own data. **No training, no install
  risk, falsifier-grade either way.**
- **Lane 2 — reduced DAD replication** (~2–4 sessions, WSL2 CPU): `pip install
  "jax[cpu]" thrml` + clone `dtm-replication`; run `smoke_testing`; then reduced
  Fashion-MNIST config (1 denoise step, class subset or 14×14 downscale, small graph);
  B1 baseline; segment metering; publish CSV + receipt. Friction recorded now: JAX on
  native Windows is unsupported → **WSL2 lane** (durable write root already defined in
  the shared-surface table); pyRAPL needs Linux MSRs → on Windows, energy = wall-clock +
  TDP-normalized estimate **marked REPORT**, or one wall-meter session if the fleet owns
  a meter (record if missing — the $15 instrument from falsifier §4.5 covers this later).
- **Lane 3 — optional rented acceleration** (still $0, free accounts only): Colab-free /
  Kaggle weekly GPU for a full-config train. Not required for lanes 1–2 verdicts; if a
  free lane dies mid-run, record and fall back — the budget law holds either way.
- **Hard cost: $0.** All artifacts free (thrml Apache-2.0; paper CC BY-NC-ND — cite, don't
  republish figures; dtm-replication unlicensed — run, don't redistribute). No paid APIs
  touched. Hosted extropic.dev console NOT required; filing the free grant application is
  optional prose, one parallel action, no dependency.

## VERDICT — GO (scoped), this week

**GO on Lane 1 immediately** (one session, zero risk, audits their own bytes — highest
falsifier value per minute the pack has seen). **GO on Lane 2** at the reduced
pre-registered config. **NO-GO this week** on full-config replication (CPU-only makes it
multi-week; pre-register it as the follow-up stone for a free-GPU-lane session).
**Do not block on** extropic.dev console access, the Thermalizers library (still "coming
soon"), or Z1 silicon (2027). Either outcome mints the same ink: a measured ally or the
independent falsifier the field was missing — and both are filed here before the first
joule is spent.

---
Receipt closed 2026-09-16. Method: WebSearch + WebFetch + anonymous GitHub API curl + PyPI
JSON — all free; no paid APIs, no git commands. Sources: extropic.ai (2 writing pages +
/software), docs.torx.ai (readthedocs redirect), docs.thrml.ai, pypi.org/pypi/thrml/json,
arxiv.org/abs/2510.23972, api.github.com (thrml, dtm-replication + trees), HN 45750995 via
search index. Local probes: nvidia-smi (absent — CPU-only box), repo venv jax (absent).

