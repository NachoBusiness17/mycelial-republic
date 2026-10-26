# SWEEP: finetuning-adaptation via Hacker News (frontier_olm_2026-10-08)

source-fetched: 2026-10-08. Door: hn.algolia.com search_by_date + search (relevance),
numericFilters=created_at_i>1788825600 (2026-09-08, 30-day window), tags=story; deep
reads on news.ycombinator.com item pages + primary pages. Both doors answered 200; no
403, no degradation. Fetched with WebFetch (small-model renderer instructed to quote
verbatim); every quote below is from a page fetched this sitting.

Instruments this sitting (all run by me): 11 Algolia API queries (fine-tuning, PEFT,
distillation, LoRA quoted-relevance, "prompt tuning", "logit bias", "embedding model",
quantization, "small model", logit, sampler, checkpoint, "model merging"), 5 HN item
threads read end to end (49783349, 49807413, 49980487, 49611128, 49923692, 49727511),
7 primary pages read (github.com/AaravGaurdev/deltatensors, blog.google
EmbeddingGemma 2, quesma.com quant benchmark, github.com/PraveenNimilka/MOLT,
cactuscompute.com/needle, dirac.run/posts/easycommand, github.com/Hantlowt/laya-studio,
duane.sh/a/fine-tuning-qwen-local-minutes). Overlap instruments: grep of
catalog/catalog.jsonl and memory/ (see per-item overlap fields) plus grep of today's
sibling sweeps in this same directory. No estate tooling was run (no pytest, no ollama);
this is a read-and-bank sweep.

## PASS 1 - candidate census (60+ items considered, 30-day window)

Queries and their yield (points|comments as Algolia reported):

- query=fine-tuning: 18 story hits. Strongest: 49923692 Clef (641|218), 49807413 Ask HN
  "When is fine-tuning a small LLM worth it?" (10|14), 49748553 Cactus Needle 3
  (236|93), 49897103 Fine-tuning Qwen3.5-4B to replace Gemini Flash-Lite in RAG (1|0),
  49966238 finetuned 1.5B Qwen bash (6|0), 49687253 Molt QLORA Windows laptops (2|0),
  49854499 Laya Studio specialize without fine-tuning (1|0), 49949900 entropy-rate
  filtering mitigates iterative fine-tuning (arXiv 2610.01493), 49889028 the dataset
  where fine-tuning turned actively harmful (1|0), 49896983 fine-tuning for
  long-context sparse attention (arXiv 2608.19920).
- query=distillation: 22 hits, mostly the IP/policy wave (OpenAI/Anthropic/CISA
  campaign stories, Jensen Huang) - adjacent to estate adaptation questions only via
  RQ4 technique rows (49807276 Shrewd distilling LLM labels into local classifiers;
  49727511 Swift-Qwen3.8 on-policy distillation, held, see below).
- query=embedding model: 14 hits. 49980487 EmbeddingGemma 2 (427|46), 49908514 Cohere
  Embed 5, 49636147/49605110 EmbedFlow zero-downtime embedding upgrades, 49685838 Ask
  HN "If embeddings are so powerful, why are they mostly used for retrieval?" (2|2).
- query=quantization: 14 hits. 49611128 Quesma Qwen3.8 27B ladder (286|139, held),
  49778955 QLoRA explained, 49823211 quant-delta-predictor stress test, 49727511
  Swift (held), 49703818 GSQ-RCO Flash-Next.
- query="LoRA" (relevance): 7 hits incl. 49783349 DeltaTensors (the RQ3 hit) and
  49756840 HyperFlow one-LoRA-for-all-tasks. NOTE: the unquoted search_by_date
  query=LoRA and query=PEFT returned fuzzy noise (local-first app stories), so the
  quoted relevance query is the working door for this term.
- query=logit / sampler / checkpoint / "model merging": ~25 further hits, mostly noise;
  usable: 50006224 From Sampling to Reinforce (srush, RQ1-adjacent theory, 1 pt, not
  deep-read), 49933055 Jane Street activation checkpointing (training-time, out of
  scope), 49969447 Smolvm CRIU microVM checkpointing (VM not model deltas, adjacent to
  ReFold only by analogy). "model merging" and "prompt tuning" returned nbHits=0.
- query="small model": 7 hits incl. 49994369 Training a small model to run a house,
  49767564 CUA-S1 (95|10).

Census law: counts above are one instrument (Algolia JSON) at one moment
(2026-10-08 ~18:00Z), not constants.

## PASS 2 - the 8 banked items (strongest first; all read by me this sitting)

### 1. DeltaTensors: Git for model fine-tunes (HN 49783349, 2026-09-21)

- URL: https://github.com/AaravGaurdev/deltatensors (HN item 49783349 also read).
- Quote (README, verbatim): "Each .wdelta records a parent_hash (SHA-256 of the model
  it was computed against)."
- Why it matters: this is the RQ3 steal. Post-training delta compression: "294 MB
  delta vs 953 MB fine-tuned model (3.2x smaller)", reconstruct perplexity 19.11 to
  19.22 (0.58 percent), "You get the quality of a real full fine-tune with the storage
  footprint of LoRA", chained deltas where "Each delta is computed against the prior
  reconstructed model, not the original base". The restore-door failure modes are the
  real gift for ReFold transfer (all README verbatim): "apply deltas in the wrong order
  and it raises ValueError instead of silently handing you a corrupted model"; the
  hot-swap path "never subtracts the old one: bf16 addition isn't reversible" and
  instead copies touched weights back from base_state first; wrong-order application
  and non-reversible float arithmetic are exactly what breaks naive shed restore.
  Estate map feed: ReFold sheds (watch/inbox/port_wave_20261007/p5_refold.md, restore
  door proved 4290 chars, via lens/burns.md:118-121) gain a second shape: adapter and
  checkpoint deltas as sha-parented chains with explicit rebuild-vs-swap doors.
- Overlap: catalog grep DeltaTensors=0; memory grep 0 prior rows (only this session's
  own trajectory echo); id 49783349 absent from all sibling sweeps. New.

### 2. Ask HN: When is fine-tuning a small LLM worth it? (HN 49807413, 2026-09-22)

- URL: https://news.ycombinator.com/item?id=49807413 (thread read end to end).
- Quote (spottedmarley, verbatim): "the biggest and most time intensive part is
  generating the training dataset. building the LoRa is the easy part."
- Why it matters: RQ2 answered by 14 practitioners, and the consensus matches the
  estate's serving-layer-dominates prior (lens/burns.md:87-89): speedgoose "I think
  it's almost never worth it now" because prompting an up-to-date LLM "will likely
  outperform a small finetuned LLM, at a lower cost with more flexibility"; minimaxir
  conditions it on "a decent sample size of data" plus "cost-effective infra to host
  it"; Vicmed13 only for "a highly specialized problem that requires every inch of
  privacy"; spottedmarley trained Qwen3.5:2b on a 128GB Dell GB10. Survivors' pattern:
  narrow closed task + cheap local serving + privacy. That is the gemma:2b janitor
  shape exactly, and the failure pattern (dataset cost dominates) is the five-gate
  answer before any GPU gate fires.
- Overlap: catalog "small LLM worth it"=0; id 49807413 absent from sibling sweeps;
  memory 0. New.

### 3. Cactus Needle 3: 8-29MB automation models (HN 49748553, 2026-09-18, 236 pts)

- URL: https://cactuscompute.com/needle (HN thread 93 comments not yet read; primary
  page read in full).
- Quote (verbatim): "LoRA on the frozen base at the full 20 layers, then a 4-bit .cact
  of any subnetwork that runs on the same engine."
- Why it matters: RQ2/RQ4 boundary evidence at the extreme small end. 29-121M "Laddered
  Simple Attention Networks", CQ2 quantization, "Needle 3 beats models 10x its size on
  mobile tool calls", "4L can match DeepSeek V4 Flash when tuned on downstream tasks
  for one epoch", and "fine-tuning on DroidCall lifts every subnetwork by 18 to 36
  points" - i.e. at tiny scale, downstream fine-tuning is not marginal, it is the
  product. Also returns text embeddings from the same model ("an app can search, match
  and route locally"), an RQ5 data point: one resident tiny model serving both decision
  and embedding duty on-device (400-4k tok/s decode on a Raspberry Pi 5).
- Overlap: catalog cactus=9 rows, ALL WoW game assets (CactusSourCandy .png/.tres,
  library_parked), not Cactus Compute; id 49748553 absent from sibling sweeps. New.

### 4. Fine-tuning Qwen3.5-4B for the Local Minutes pipeline (duane.sh, HN 49897103,
### 2026-09-29)

- URL: https://duane.sh/a/fine-tuning-qwen-local-minutes (read in full).
- Quote (verbatim): "Training went through the 24,000 examples once, on one rented H100
  GPU, in 1.6 hours, for about $7."
- Why it matters: the exact cost datum RQ1/RQ2 lack. LoRA + DPO + GRPO (graded by
  Claude Opus 5.5) on Qwen3.5-4B over 25,206 sampled excerpts; result "It makes fewer
  mistakes than Gemini 2.5 Flash-Lite at 71% less cost", served on a serverless RTX
  4090 that "spins up, works through them, and shuts down". The motivating sentence is
  estate-shaped too: they moved local to stop being hostage to API model churn
  ("don't need to worry about it being changed or deprecated"). For the five-gate
  hardware law (memory/rib/RIB_GPU_LADDER_20261001.md:10-23 via lens/laws.md:98-99):
  the adapter tier now rents for single-digit dollars - no local GPU gate needs to
  fire to reach a LoRA; the gate guards SERVING, not training.
- Overlap: catalog easycommand=0, dirac.run=0; id 49897103 absent from sibling sweeps;
  memory 0. New.

### 5. Teaching a 1.5B model bash at gpt-4o level, 400k synthetic examples
### (dirac.run, HN 49966238, 2026-10-05)

- URL: https://dirac.run/posts/easycommand (read in full).
- Quote (verbatim): "The model was learning the supplied answers. That wasn't the same
  as reliably applying them elsewhere."
- Why it matters: RQ4 distillation row with the honest caveat the estate's
  contamination law loves. 401,975 synthetic pairs, synthetic generation + review +
  execution checking; "the released 1.5B 4-bit model passed 212/300 ALFA-updated tasks
  (70.7%), versus whatisit's 191/300 (63.7%)"; GPT-4o published 73-74 percent was on
  original ALFA, so "similar scores don't establish parity". Served via llama.cpp on
  CPU. The memorization-vs-transfer sentence is the eliminate-before-frontier lesson:
  a fine-tune that aces its own dataset is not an adapter until transfer is measured
  on held-out tasks (estate twin: contamination law, paired seen/unseen score
  divergence, commit c7d364ab6).
- Overlap: catalog dirac.run/easycommand=0; sibling sweeps list id 49966238 as an
  UNREAD pass-1 candidate only (open-local-models-hn.md:53,
  quantization-compression-hn.md:61); neither fetched nor banked it (no dirac.run or
  easycommand text anywhere in their files). My read is the first. New.

### 6. Laya Studio: specialize a model without fine-tuning (HN 49854499, 2026-09-26)

- URL: https://github.com/Hantlowt/laya-studio (read in full).
- Quote (verbatim): "Residual transforms are explicit small matrices derived by ridge
  linear algebra. No strategy calls an optimizer or backward"
- Why it matters: RQ1's "adapter substitute" question has a third answer besides
  sampler profiles and LoRA: gradient-free geometric specialization over a frozen
  model. The repo "specialize[s] a frozen Laya model for a new domain or decision
  task--without gradients, without changing its weights" (dash rendered as --, ascii
  law) by generating synthetic examples then deriving "centroids, contrastive
  directions, transforms, or steering vectors", including "Activation steering: where
  the backend exposes a safe hook, inject a derived task vector"; "One Laya
  installation can support many independent specializations without duplicating its
  weights." No numbers published (honest: "It does not work universally"). For the
  estate: this is the sampler-profile idea extended into representation space, and it
  converges with the frozen-centroid thread already held (day-7, c7d364ab6).
- Overlap: catalog laya-studio/Hantlowt=0; id 49854499 absent from sibling sweeps; the
  Laya MODEL appears in the banked Clef thread (open-local-models-hn.md) but this
  Studio repo does not. New.

### 7. EmbeddingGemma 2 primary announcement (blog.google, HN 49980487, 2026-10-06)

- URL: https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/
  (read in full; the 46-comment HN thread was banked by the sibling, see overlap).
- Quote (verbatim): "With quantization, on a Google Pixel 11 Pro, EmbeddingGemma 2
  requires as little as ~191MB active RAM for text-only weights"
- Why it matters: RQ5 residency math, primary-source numbers. "Requires as little as
  270M parameters for text-only" (740M full multimodal; thread: 270M text / 170M
  vision / 300M audio), Apache 2.0, and the two load-bearing facts for the RAM-cache
  residency law (memory/rib/RIB_RAM_CACHE_STALE_SNAPSHOT_20260825.md:8-41 via
  lens/laws.md:103-105): MRL truncation "from 768 dimensions down" to "512, 256, or
  128 dimensions" giving "up to 6x storage reduction for local vector databases and
  memory usage", and a non-router use named by Google itself: "Create real-time
  decision engines leveraging multimodal context for classification, routing, and
  predictive capabilities". Thread adds a local M3 Pro datum: "Text: 78
  embeddings/second" (minimaxir) and the residency pattern "The embedding model stays
  loaded in memory" (reacharavindh) - exactly the always-on RAM cost the residency law
  prices. Against GPS-embed being killed (lens/burns.md:129-131), the surviving
  non-router use is cheap classification/routing features, not kNN routing.
- Overlap: PARTIAL. Catalog holds 10 rows: the ONNX weights
  (models/embeddinggemma-2-onnx/, incl. model_q4.onnx_data 174MB) plus the estate's
  own GPS_EMBED_TRIAL intake row; sibling open-local-models-hn.md:160-181 banked the
  HN thread read and explicitly did NOT fetch the blog ("blog not fetched"). This
  bank adds the primary page only; the thread is NOT re-banked.

### 8. MOLT: thermally aware QLoRA for Windows laptop GPUs (HN 49687253, 2026-09-13)

- URL: https://github.com/PraveenNimilka/MOLT (read in full).
- Quote (verbatim): "This is complete single-seed development evidence, not a
  universal superiority claim."
- Why it matters: the five-gate hardware law's missing instrument on the exact estate
  platform (Windows 10/11 + consumer NVIDIA). "Thermally aware, memory-efficient QLoRA
  fine-tuning for consumer NVIDIA GPUs", Qwen/Llama/Gemma-family inputs, exports a
  "PEFT-compatible safetensors adapter"; measured vs Unsloth on RTX 4060 Laptop
  (Qwen 1.5B): session time "23.00% lower", throughput "38.45% higher", peak VRAM
  "12.09% lower", peak temp 7 C higher, final NLL 2.4415 vs 2.5169. The single-seed
  caveat is the estate's own honesty law applied. License note: PolyForm Shield,
  source-available NOT OSI open source - read terms before any estate reuse.
- Overlap: catalog MOLT word-boundary=0 (58 substring hits all molten_core /
  molt_instructor_service game files); id 49687253 absent from sibling sweeps. New.

## HELD GROUND - surfaced in pass 1, NOT re-banked (anti-rebank law, lens/burns.md
## section 5)

- 49727511 Swift-Qwen3.8-27B (-58.3 percent thinking, x1.95 speed): banked day-7 +
  resurfaced-not-rebanked by the quantization sibling
  (quantization-compression-hn.md:67-68). Its pipeline (inference-time token
  penalizer, then LoRA SFT over the identified tokens, then RL + on-policy
  distillation to restore accuracy; AIME26 -4.6 percent traced to one wrongly
  penalized math token) is the strongest public RQ1 evidence and the estate already
  holds it; my re-read confirmed the sibling's holding, it adds nothing new.
- 49611128 Quesma Qwen3.8 27B quantization ladder: day-7 banked
  (quantization-compression-hn.md:65-66). My primary-page read matched: "there is
  little difference down to 4-bit", "Quality drops off a cliff at 1-bit".
- 49923692 Clef decision models + RL fine-tuning platform (641 pts): banked by the
  open-local-models sibling as its item 1 (open-local-models-hn.md:75-108), including
  the latency/pricing tables and the "needs fine-tuning to be useful" thread shape.
- 49980487 EmbeddingGemma 2 HN thread: banked by the sibling (item 4); only the
  primary blog is banked here (item 7 above).

## ANSWERS INTO THE ESTATE MAP

- RQ1 (marker-penalty logit_bias toggle vs adapter): public evidence now runs
  sampler-penalty -> LoRA -> RL as ONE pipeline (Swift, held); nobody reports a
  standalone logit_bias toggle moving task accuracy on a small model - that cell is
  UNMEASURED publicly and on the estate (P6 profile OFF by default,
  lens/burns.md:120-121). Laya Studio (item 6) is the gradient-free middle rung.
  The A/B the estate owes: P6 ON vs OFF on the janitor battery, four pinned choices,
  before any adapter talk.
- RQ2 (LoRA under the five-gate law): practitioner consensus (item 2) says almost
  never, and the surviving pattern is narrow-task + privacy + cheap local serving.
  The $7/1.6h rented-H100 datum (item 4) separates the question: TRAINING no longer
  needs a local GPU gate at all; only SERVING the adapter does. Cactus (item 3) shows
  the one regime where fine-tuning IS the product (tiny task-specific nets, +18 to 36
  points). So the five-gate law stays a serving law; a LoRA pass is justified only
  after a P6-class serving-profile A/B fails to close the gap.
- RQ3 (ReFold shed transfer): DeltaTensors (item 1) proves the pattern transfers to
  weight deltas and names the exact restore-door breakers: unordered chain
  application (must ValueError, not corrupt), and non-reversible bf16 arithmetic
  (never subtract deltas; copy touched tensors from the verified base). Estate
  adapter sheds should copy both doors.
- RQ4 (techniques with zero estate instruments): LoRA (instruments: none; nearest is
  the P6 sampler profile), PEFT-adapter tooling (none; MOLT exports the format),
  distillation (none end to end; dirac item 5 + Shrewd 49807276 are the recipes),
  prompt-tuning (zero public hits in 30 days AND zero estate instruments - the
  emptiest cell). This list is the eliminate-before-frontier map for any adaptation
  ask (lens/laws.md:88-91).
- RQ5 (embedding model residency): Google's own non-router framing (classification,
  routing, prediction) + MRL 6x storage cut + ~191MB quantized text-only RAM (item 7)
  is the strongest public justification for keeping EmbeddingGemma 2 resident; the
  residency law still demands an mtime-fingerprint invalidation story for anything it
  caches. GPS-embed's kNN-routing death (lens/burns.md:129-131) does not kill the
  feature-extractor use.

## RECEIPT

- Read this sitting, by me: all URLs named above (13 fetches, all HTTP 200); the lens
  anchors lens/burns.md (full, 244 lines) and lens/laws.md (full, 216 lines);
  sibling sweep files via grep (open-local-models-hn.md, quantization-compression-hn.md
  hit lines shown above).
- Greps run (bash, this box): catalog/catalog.jsonl per-title (results in overlap
  fields); memory/ per-title grep with --exclude-dir game, mesh, runs, collections,
  trajectory (final run exited 0 with ZERO hits for all 9 terms: DeltaTensors,
  easycommand, Cactus Needle, cactuscompute, PraveenNimilka, laya-studio, Hantlowt,
  duane.sh, "fine-tuning a small LLM worth it"); sibling-sweep id grep. One grep typo
  corrected in-session (48107413 -> 49807413, rerun clean). memory/trajectory/steps.jsonl
  hits on my own titles were verified to be THIS session's logged commands
  (self-echo), not prior holdings. The five excluded memory/ subdirs were not grepped
  term-by-term; they hold game/mesh/runs telemetry outside the frontier corpus.
- Not run: any estate tool (pytest, ollama, corpus tools); no quotes were verified
  against raw HTML beyond the fetch renderer (WebFetch small-model verbatim
  instruction); confidence per item reflects that.
- Door health: hn.algolia.com and news.ycombinator.com both clean all sitting; the
  unquoted query=LoRA / query=PEFT doors return fuzzy noise (use quoted relevance
  query). "prompt tuning" and "model merging": nbHits=0 in the window.
