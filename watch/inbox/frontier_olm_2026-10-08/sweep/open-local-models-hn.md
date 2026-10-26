# Frontier sweep: open-local-models via HN (2026-10-08)

source-fetched: 2026-10-08. Seat: sweep-open-local-models-hn (dynamic workflow subagent of the
frontier_olm run). Area: open-local-models. Door: Hacker News via hn.algolia.com API + item
threads, per the ask's fetch recipe. Laws held: no fabrication (OWED where unreachable),
byte/URL cites, ascii only, no em or en dashes.

## Door health and method (what was actually run this sitting)

- search_by_date RE-VERIFIED live (the 10-08 doors lens left it OWED at
  lens/doors.md:54): WebFetch GET
  `https://hn.algolia.com/api/v1/search_by_date?query=open%20weights&tags=story&hitsPerPage=30`
  returned valid JSON, nbHits 905, first hit created_at 2026-10-08T12:51:44Z
  (objectID 50005230, "Show HN: Gauze fixes (some) open-weight LLM deficiencies"). The
  index carries current dates, so the ask's 30-day window 2026-09-08..2026-10-08 is
  feedable from this door. No 403s, no timeouts on any Algolia call this sitting.
- Pass 1 (broad): 6 completed Algolia search_by_date queries, tags=story, hitsPerPage=30:
  "open weights", "ollama", "qwen", "gemma", "embeddinggemma", "kimi OR minimax OR
  nemotron". 149 hits returned total; after dedupe and window filtering, 55+ distinct
  in-window candidates were considered; the 36 strongest are tabled below. The compound
  kimi/minimax/nemotron query returned only 1 hit (2026-02-02, out of window): no
  in-window release from those families surfaced on HN.
- Pass 2 (deep reads): 9 WebFetch fetches over 8 distinct targets, all read end to end:
  HN 49923692 (Clef thread, fetched twice; second pass re-verified the dgacmu,
  andrewingram and okpatil comment texts comment-ids 49933256, 49932476, 49925771/94),
  HN 49969183 (Beam), HN 49942706 (Kolibri), HN 49980487 (EmbeddingGemma 2),
  github.com/firelex/jeff-code, github.com/lateos-ai/reflex, github.com/jiwidi/jiwo,
  huggingface.co/AgentBull/bongard-mini.
- Overlap instrument: venv python substring probe over catalog/catalog.jsonl (path fields)
  plus git grep over memory/ and the day-7 sweep lanes
  (watch/inbox/frontier_olm_2026-10-07/sweep/). Catalog rows are file-path metadata, so
  name hits on raw harvest files are listing-level, not content-level; content-level
  dedup is against the day-7 lane bank, read in full this sitting
  (open-local-language-models-hn.md, 241 lines).

## Pass 1: in-window candidates considered (36 of 55+, newest first; objectID | date | pts | title)

50005230 10-08 1 Gauze fixes (some) open-weight LLM deficiencies; 50006071 10-08 (noise);
50007516 10-08 5 German search engine ditches Mistral, bets on Chinese open-source AI;
50003695 10-08 2 Embedding Gemma2 Use Cases; 50003460 10-08 2 Java vLLM-like framework claims
90% of llamacpp; 50002660+49997807 10-07/08 3 AI Development on Windows: PyTorch and
Llama.cpp to Windows ML; 49998043 10-07 2 MS announces DeepSeek V4 Flash and Nemotron
locally, llama.cpp comes to Win ML; 50002054 10-08 1 Prism-ML Bonsai 2 joins ByteShape
Qwen3.8 quantization comparison; 49997488+49995052+49984322+49982845+49981488 10-06..07
EmbeddingGemma 2 cluster; 49991780 10-07 3 Moefit: Fit Qwen 3.8 Flash on your Mac; 49996594
10-07 64 Ask HN: Which frontier model can do code security reviews; 49984522 10-06 6
Westernized Qwen3.6-35B-A3B; 49981275 10-06 1 TOD universal Decision model; 49980487 10-06
427 EmbeddingGemma 2 (banked, item 4); 49978040 10-06 2 Mistral Large 4 Le Chonk 1T; 49974431
10-06 1 Qwen Flash Next Q4 on a Mac Mini (360 tks read); 49969183 10-05 549 Beam:
Reflection's 501B (banked, item 6); 49968868 10-05 2 Jeff-Code 0.8B (delta, item 7); 49968012
10-05 1 Cloudflare Clef Open Weights (HF); 49967455 10-05 1 Jiwo small decision models
(banked, item 2); 49967425 10-05 1 Interfaze-1-lite; 49963695 10-05 2 Clef and Clef Flash on
Ollama library; 49966238 10-05 6 1.5B Qwen finetuned to near GPT-4o bash; 49964046 10-05 5
Abliterated LLM provider; 49955908 10-04 1 Axios on Reflection release; 49958869 10-04 1
Shlexball local 1.5B file finder; 49957671 10-04 2 VHDL LLM inference engine; 49943381 10-03
6 Anthropic Mythos-class hacking claims on Chinese open model; 49942706 10-03 706 Kolibri
(banked as delta, item 8); 49943034 10-03 423 tej.as Kolibri teardown (held day-7); 49942092+
49934323 10-02/03 New in Llama.cpp: Decision Models (held day-6/7); 49939683 10-02 2 Enclave
cyber-model router; 49938916 10-02 6 LLaMA Now Goes Faster on CPUs (day-7 struck: 2024
resubmit); 49935357 10-02 4 Hacktoberfest open-weight pivot; 49929508 10-02 1 funcroute
Ollama-like router; 49926327 10-01 1 Laya free hosted API; 49923692 10-01 641 Clef decision
models (banked, item 1); 49921892 10-01 1 Snap local decision engine; 49921077 10-01 1 book
memorization study; 49911995 09-30 194 Magnitude inference engine; 49909963 09-30 2
Bongard-mini (banked, item 5); 49908997+49906337 09-30 Ollama 0.35 decision models (held
day-6); 49903234 09-30 1 Reflex Engine (banked, item 3); 49899734 09-29 17 Is open-weight AI
banned yet; 49896315 09-29 2 Jev-compatible doc classification with VLMs; 49893215 09-29 1
browsers native API for open-weight models; 49889447 09-29 1 ContextMemory; 49882932 09-28 1
Why we removed Ollama from Return; 49882129 09-28 1 Nibia Fabric shared compute; 49879581
09-28 2 Echoleak Beaten almost (Llama-3.1-8B immunized); 49878572 09-28 3 Jeva.cpp JEV-API
fork; 49876817 09-28 4 llama.cpp 2.2x on Intel Arc; 49873880 09-28 1 Vektor v1.9.7; 49872147
09-28 1 OllamaMQ 0.5 SystemOne support.

## Pass 2: banked items (8, strongest first)

### 1. Clef: Cloudflare's open-weight decision models (641-pt thread)

- Source: HN https://news.ycombinator.com/item?id=49923692 (fetched twice this sitting;
  second fetch re-verified the quoted comments at ids 49933256, 49932476, 49925771/94);
  story URL https://blog.cloudflare.com/clef-decision-models/ (2026-10-01).
- What the thread holds: Clef is post-trained from Qwen (thread consensus: Qwen3.8-27B for
  Clef; Clef-flash from "Qwen/Qwen3.5-9B" per the model card, with a claimed Qwen3.8-9B
  corrected in-thread); multimodal vs text-only Jev; weights open, training pipeline not.
  Verified verbatim: dgacmu (49933256): "About 41% accuracy. My local gemma4:27b gets 53%
  and runs 4x faster." (8-bit quant, his US-coin classification task, phone photos).
  andrewingram (49932476): "I ported a Jev-based prototype i've been working on to Clef,
  and it ended up being significantly slower and the results were worse." okpatil
  (49925794): "At0M: A 60M local Jev at 16 ms latency and 79% accuracy on Typed Decision".
  Latency measurements in-thread: Clef Flash 661 ms median vs Jev/TypeSafe 230 ms (ralusek);
  hosted p50 ~850 ms vs ~110 ms (pdlug). Pricing: Clef $0.24/M input vs Jev $0.042/M
  (ssiddharth). Local serving: Clef and Clef Flash are on the Ollama library
  (story 49963695, 10-05), runnable in llama.cpp; "Ollaya" aspires to be Ollama for
  decision models; OpenRouter lists nine decision models.
- Why (estate map): this is the decision-rung band's biggest in-window release thread, and
  it is estate-testable end to end: pull clef / clef-flash from the Ollama library, fire the
  estate's own gate (beat-embeddings baseline AND >=0.880 on n>=40,
  watch/inbox/frontier_olm_2026-10-08/lens/laws.md:159-161 context,
  mag/verb.py:493-505 meter). The dgacmu datum is a third-party replication of
  harness-dominates-small-models (local model beats the hosted decision model on a real
  task at 4x speed), the day-7 confirmed finding (lens/burns.md:87-89). At0m (60M, 16 ms,
  79 percent self-reported) is a below-band floor candidate for the meter's lower rung.
  The wongarsu caveat (median-latency framing hides Jev's flat curve at larger contexts)
  is a conditions-law lesson: any estate Clef-vs-Jev cell must pin input-length buckets.
- Overlap: grep clef = 2 catalog rows, both listing-level: day-5 raw page save
  (catalog.jsonl:1073386, watch/inbox/frontier_olm_2026-10-05/sweep/_clef.html) and the
  day-7 lane's ggml-blog listing mention "Cloudflare's Clef is next" with a 27B Apache-2.0
  table entry (watch/inbox/frontier_olm_2026-10-07/sweep/open-local-language-models-hn.md:
  168-169). The thread content (dgacmu measurement, At0m, the Jev-vs-Clef port reports,
  latency and pricing rows) was in no prior bank. Genuinely new.
- Confidence: 0.93 (thread read twice; quotes re-verified against comment ids).

### 2. Jiwo: 0.75B and 4B self-hosted decision models topping the Decision Index under-1B class

- Source: Show HN 49967455 (2026-10-05, 1 pt) ->
  https://github.com/jiwidi/jiwo (read end to end this sitting).
- Verbatim (README): "jiwo models read a state and typed questions, and return a probability
  for every option in one forward pass." "They do not generate text. On one H100, the median
  request takes about 50 ms." jiwo-0.8b (base Qwen3.5-0.8B, 0.75B params) scores 28.00 on
  Decision Index 0.2.1, "1st of 23 (under 1B)" live, "1st of 33 (under 1B)" with open
  submissions; jiwo-4b (base Qwen3.5-4B, 4.2B params) scores 44.97, "1st of 18 (3-6B)" live.
  Scores come from "complete runs of the suite (150,317 requests per model)" and the README
  says maintainers have not verified them. Jev-API compatible (POST /v1/systemone); MIT
  code, Apache-2.0 weights; self-hosted only, CUDA/MPS/CPU.
- Why (estate map): both models sit inside the 0.5B-8B band and the exact decision-rung
  shape the estate's gate meters (mag/verb.py:493-505); the /v1/systemone endpoint is the
  one the estate already landed in llama.cpp (day-6 register row 3, via
  frontier_olm_2026-10-08/lens/burns.md:90-92 context). jiwo-0.8b is the first sub-1B
  self-hosted decision candidate found in-window that a $0 estate battery can fire
  directly; this also lands a piece of the day-7 instrument debt "Decision Index 0.2.1
  leaderboard" (frontier_olm_2026-10-07/DIGEST.md:83).
- Overlap: jiwo grep = 0 in catalog paths and memory; the only hit class was dl_book HTML
  substring false positives. The day-7 HN lane's queries did not surface it (1-pt Show HN).
  Genuinely new.
- Confidence: 0.9.

### 3. Reflex Engine: same weights, serving stack alone moves cold-start 1.1x to 150x

- Source: Show HN 49903234 (2026-09-30, 1 pt) -> https://github.com/lateos-ai/reflex
  (read end to end this sitting).
- Verbatim (README benchmark tables, conditions stated on-page: Tesla T4, Qwen3-0.6B-Q4_K_M,
  cold start from outside the process): vs llama.cpp llama-simple "Reflex 1.13x faster
  (0.83 s vs. 0.94 s)"; vs Ollama "2.6x faster (0.83 s vs. ~2.1 s)"; vs vLLM "Reflex 48-150x
  faster (0.83 s vs. 39.8-127.3 s)"; headline "~483 ms cold start, p50: reflex system1 from
  process start to its scored result". Scope line: "Reflex is a local execution engine for
  single-tenant decisions: one request at a time, no scheduler, no batching, no network
  server inside the engine." Also reads: Kolibri-1 78B Q4_K_M served in 47.5 GB on a 48 GB
  card (lazy experts cut cold first token 8.6 s -> 2.3 s on an RTX A6000); MIT; GGUF-native
  Rust/CUDA; TypeSafe Jev "Reflex 1.1-2.0x slower (0.63 s vs. 0.31-0.57 s)" since Jev is
  always warm.
- Why (estate map): this is the cleanest external instrument yet for research question 2
  (how much of gemma:2b's janitor pass-rate is serving choice vs weights): identical weights
  measured across five serving stacks with an up to 150x spread, plus the Strata thread's
  same-weights quality regression held by day-7
  (open-local-language-models-hn.md:124-128). Adoption caveat, stated as condition: Reflex
  is CUDA/NVIDIA-only and the estate box runs Vulkan/CPU lanes (the estate's own 72.97 tok/s
  Vulkan measurement, day-7 context), so this is instrument evidence, not an adoptable
  engine, until an NVIDIA lane exists.
- Overlap: lateos and "reflex engine" greps = 0 in catalog.jsonl and memory. Genuinely new.
- Confidence: 0.88.

### 4. EmbeddingGemma 2 thread: the estate's owed baseline has a text-parity caveat

- Source: HN https://news.ycombinator.com/item?id=49980487 (2026-10-06, 427 pts, 46
  comments) -> https://blog.google/innovation-and-ai/technology/developers-tools/
  embeddinggemma-2/ (thread read end to end this sitting; blog not fetched).
- Verbatim from the thread: size split per djoldman: "740M total (270M text, 170M vision,
  300M audio)"; the load-bearing caveat per sourcecodeplz: "for text, benchmarks are
  identical to the first EmbeddingGemma."; production user piyh: "this model is a drop in
  replacement for gemma embedding v1 and HQ-CLIP. Better quality, less RAM usage, faster
  embeddings."; minimaxir throughput on M3 Pro: "78 embeddings/second on small texts";
  license Apache 2.0 (per simonw in-thread). Criticism read: no OCR encoder; no
  MatFormers-style weight shrinkage with MRL dims (aabhay); Google's own demo case failed
  for Zambyte locally (p(true) 0.22 on a financial example); jraedisch: not better or
  faster for text-only retrieval.
- Why (estate map): the beat-embeddings baseline is half of the estate's decision-rung gate,
  and day-7 held "the embeddinggemma-2 baseline instrument is NOT live on the estate box
  yet" (frontier_olm_2026-10-07/DIGEST.md:23). The weights now ARE on disk
  (models/embeddinggemma-2-onnx/, 9 catalog rows, mtime 2026-10-08T00:22-00:23Z,
  catalog.jsonl:1265427-1265435, including model_q4.onnx) so the remaining gap is wiring,
  not pulling. The thread's text-parity caveat says the baseline choice between EG1-300M
  and EG2 must be measured, not assumed: for text-only scut, EG2 may be EG1-class.
- Overlap: estate holds the weights (rows above; commit 56b836d5a banked EmbeddingGemma 2
  under models/ per lens/burns.md:132) and the day-7 reddit lane held the Ollama-0.40
  runner-list note. The HN thread content (740M split, text-parity caveat, M3 throughput,
  the four criticisms) was in no prior bank. Delta bank, not a re-bank.
- Confidence: 0.88.

### 5. Bongard-mini: 7.5B open decision model whose JevBench spread is the contamination shape

- Source: Show HN 49909963 (2026-09-30, 2 pts) ->
  https://huggingface.co/AgentBull/bongard-mini (model card read end to end this sitting).
- Verbatim (card): "7.51 billion total parameters" with "7.09 billion trainable"; "an
  open-weight System One model for machine intuition and Jev-like judgment, built on the
  T5 encoder-decoder architecture of T5Gemma 2 4B-4B"; JevBench v1.4: "100% / 97.2% / 57.7%
  accuracy"; DecisionBench 1.0: "78.05% accuracy; 77.73% on the 20,959 rows with no
  detected source-text overlap"; "36.1 ms median" per decision; "Bongard-mini ranks fourth
  among the 61 systems". License: Gemma terms on weights, Apache-2.0 runtime; BF16
  safetensors only, no GGUF listed.
- Why (estate map): the only in-band (7.5B) open decision-model release this window outside
  the Qwen-derived families, and its scorecard is the exact shape the estate's P2
  contamination tripwire watches (paired seen/unseen divergence, port wave 6685db6bc): a
  100 percent top-line next to a 57.7 percent third split is a benchmark-fitting flag, and
  the card's own no-overlap row (77.73 vs 78.05, a 0.32-point delta) is the published
  paired-delta form to imitate. No GGUF means the Ollama/llama.cpp janitor path cannot
  serve it today; any estate cell stays UNMEASURED until a safetensors lane exists.
- Overlap: catalog "bongard" hit = state/arxiv/2026-10-01/2609.39111v1.txt, a Bongard-problems
  paper (name collision, not a holding); memory grep = 0; no prior sweep bank named it.
  Genuinely new.
- Confidence: 0.85.

### 6. Beam: Reflection's 501B/23B-active announcement, weights promised not shipped

- Source: HN https://news.ycombinator.com/item?id=49969183 (2026-10-05, 549 pts, 174
  comments) -> https://reflection.ai/blog/introducing-beam (thread read end to end this
  sitting; blog not fetched).
- Verbatim (thread): wren6991: "At first blush the benchmarks are impressive, but to
  paraphrase Linus: 'Talk is cheap, show me the weights.' :-)"; htrp quoting the
  announcement: 501B total / 23B active, pretrained on 23.8T tokens, RL "over 100 million
  rollouts on 10.5K NVIDIA GB300 GPUs over 4 weeks"; weights, technical report and model
  card promised "later this month". In-thread comparison (wren6991): DeepSeek V4.1 Flash at
  552B total / 8-16B active, MIT-licensed, 45T tokens, ahead of Beam on measured metrics;
  commenters place Qwen and GLM 5.3 Flash ahead as well. Land/water puzzle contamination
  claim retracted in-thread by a Reflection team member (the puzzle dated to August 2025).
- Why (estate map): a garden-grid family event for the 30-day row-expiry law
  (lens/laws.md:67-69): a new US frontier family entering the open-weight set, with the
  vendor's own benchmark chart contested in-thread and no weights to measure. Out of the
  0.5B-8B band: it does not touch the janitor seats; its value is the routing-grid row and
  the release-velocity datum for question 5 (HN carried it at 549 points within a day of
  the blog post).
- Overlap: "introducing-beam" grep = 0 in catalog and memory; the 92 catalog "reflection"
  hits are the generic word in unrelated paths. Genuinely new.
- Confidence: 0.9.

### 7. Jeff-Code delta: pass-rate CI crosses zero, thinking-gate mechanics (update to a held bank)

- Source: https://github.com/firelex/jeff-code (re-read end to end this sitting); HN
  49968868 (2026-10-05). Day-7 banked the repo deep-read at
  watch/inbox/frontier_olm_2026-10-07/sweep/open-local-language-models-hn.md:69-88.
- Delta only (verbatim from today's fetch; minus signs normalized to ascii hyphens):
  "62.4% vs 62.8%; paired difference -0.2 points (95% interval -2.6 to +2.1), 1,242 paired
  tasks"; decisions take "about 0.2 s each"; the thinking gate: thinking stays off unless
  Jeff's probability reaches 0.6, "about three quarters of Qwen's turns ran with thinking
  off", and thinking-off-always costs "-7.6 points"; per-benchmark time ratios SWE-bench
  Verified 0.63x down to Terminal-Bench 2.0 0.96x.
- Why (estate map): day-7 held the headline (47 percent faster at the same pass rate,
  0.68x, Q4_K_M loses 6 percent of decisions). Today's read adds the three numbers the
  estate's own meter design needs: the pass-rate delta's CI crosses zero (the paired form
  to copy), the 0.6 probability threshold for the thinking gate (the same axis as
  RIB_INFERENCE_BUDGET's thinking-default law), and the measured cost of the always-off
  extreme (-7.6 points). This is the working reference implementation of the estate's
  own janitor-gates-worker architecture.
- Overlap: stated above; update, not a new bank. No other estate holding (jeff-code grep = 0
  outside the day-7 lane).
- Confidence: 0.9.

### 8. Kolibri thread delta: the incumbent beats the sovereign release on its own harness

- Source: HN https://news.ycombinator.com/item?id=49942706 (2026-10-03, 706 pts, 336
  comments), read end to end this sitting. Kolibri is held: 10-03 sweep + day-7 lane
  (frontier_olm_2026-10-07/sweep/open-local-language-models-hn.md:170-173: 78.1B / 3.46B
  active, Apache 2.0, out of the estate band).
- Delta (verbatim, thread): amoshebb: "Qwen3.8 27B beats Kolibri 79.9 vs 70.8 in German in
  Kolibri's harness on Kolibri's benchmark."; ekidd: "It's 78B A3B and performs about like
  Qwen3.6 35B A3B. You can probably run it comfortably in 96B of RAM with a decent quant";
  hallucination report (Glitch752): Kolibri confidently invented an interpretation of a
  made-up song "while Qwen3.8-27B correctly refused without web search."
- Why (estate map): another third-party harness-dominates datapoint (the incumbent 27B
  dense beats the new 78B-A3B release on the vendor's own benchmark), consistent with the
  day-7 confirmed finding (lens/burns.md:87-89) and with this window's Beam thread pattern
  (announced frontier entrants benchmarking below the Chinese incumbents). The 96GB-RAM
  serving note plus Reflex's 47.5GB-on-48GB Q4_K_M row bound what a Kolibri cell would cost
  if the garden ever wants one: roughly one 48GB accelerator, which the GPU-ladder gates
  (RIB_GPU_LADDER_20261001.md:10-23) do not currently justify.
- Overlap: held rows named above; catalog hit = raw search xml only (catalog.jsonl:1195673).
  Delta, not a re-bank.
- Confidence: 0.88.

## Per-research-question verdicts (this seat's read, all cited above)

- Q1 (0.5B-8B band vs gemma:2b, measured): NO new in-band open-weight chat model surfaced
  on HN this window with instrument-measured scut evidence; the band's measured action
  stays decision models and routers (Clef-flash 9B just above the band edge, jiwo-0.8b
  0.75B, Jeff 0.8B, Bongard-mini 7.5B, At0m 60M). This replicates day-7's Q1 verdict from
  a fresh 30-day pass; estate cells stay UNMEASURED until instruments fire
  (lens/burns.md:85-86).
- Q2 (harness vs weights on the estate stack): the estate A/B itself is NOT RUN by this
  seat and stays owed; the window added two external fixed-weights instruments: Reflex's
  five-stack cold-start table (item 3) and the Clef thread's port reports plus local
  gemma4-beats-hosted measurement (item 1). Both say serving and harness choices move
  outcomes at fixed weights, which raises the prior that gemma:2b's pass-rate has a
  serving-stack component the estate has never partitioned.
- Q3 (alias classes after P3 digest pinning): MEASURED LOCALLY this sitting
  (watch/inbox/frontier_olm_2026-10-08/sweep/_alias_check.py, run with the repo venv
  python over C:\Users\foste\.ollama\models\manifests): 18 manifests, 18 distinct
  manifest shas, ZERO byte-identical manifests today (the 10-07 qwen3 4b / 4b-thinking
  manifest alias, sha256 359d7dd4..., is not present in today's listing; whether that tag
  pair was re-pulled or removed is not established by this check). The surviving alias
  class is weights-blob aliasing under distinct manifests: gemma4:latest ==
  gemma4-desk:latest == gemma4-hermes:latest (sha256:4c27e0f5b5adf02ac956c73...),
  qwen2.5:3b-instruct == qwen-desk:latest (sha256:5ee4f07cdb9beadbbb293e8...),
  qwen2.5:32b == maze-keeper:latest (sha256:eabc98a9bcbfce7fd70f3e0...). Manifest-digest
  pinning alone sees three animals where the weights are one; a boot-time blob-digest
  column would close it. Two of the three classes touch estate janitor/worker animals
  (gemma4, qwen2.5).
- Q4 (grok-4.7 champion cell re-measure, fable-5.1 plan_call re-measure): NOT RUN, and HN
  offered nothing that changes their priors; both stay owed per
  watch/inbox/frontier_olm_2026-10-08/lens/laws.md:159-164.
- Q5 (does hn.algolia-first feed the 30-day expiry fast enough): YES for major releases,
  with a measured caveat. Every major release this window (Clef 10-01, Kolibri 10-03,
  EmbeddingGemma 2 10-06, Beam 10-05) appeared in my first-pass queries within days of
  release, and search_by_date is re-verified live (header above). The caveat: the three
  strongest small-band finds (jiwo, Reflex, Jeff-Code) rode 1-2 point Show HNs that only
  keyword-targeted search_by_date surfaces; day-7's 8-query pass missed jiwo and Reflex
  entirely and caught Jeff-Code only via deep-read. HN-first feeds the garden's expiry law
  only with family-keyword queries per pass; reddit/arctic doors remain needed for the
  long tail (reddit JSON still walled for WebFetch per lens/doors.md:56-64; not re-probed
  by this seat, curl+UA bypass stays OWED).

## Receipt

Fetches this sitting: 6 Algolia search_by_date calls (all valid JSON, no 403s), 9 page
fetches over 8 distinct targets (4 HN threads, 4 repos/cards, 1 re-verification fetch of
the Clef thread). Local instruments: the alias check above (script + venv python run,
output in-session). Overlap greps: catalog substring probe + git grep over memory/ + full
read of the day-7 lane bank. Not run: any estate model pull, any battery or gate run, any
pytest, any reddit re-probe. The one temp helper script written this sitting is
sweep/_alias_check.py; no other repo files touched.
