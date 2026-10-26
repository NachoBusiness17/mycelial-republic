# Frontier sweep: open-local-language-models via HN (2026-10-07)

source-fetched: 2026-10-07. Seat: sweep-open-local-language-models-hn (dynamic workflow
subagent of the frontier_olm run). Door: Hacker News via hn.algolia.com API + item threads.
Laws held: no fabrication (OWED where unreachable), byte/URL cites, ascii, no em-dashes.

## Door health and method (what was actually run)

- Pass 1 (broad): 8 completed Algolia queries over the 30-day window
  (numericFilters created_at_i > 1788739200, i.e. since 2026-09-07), tags=story:
  ollama, llama.cpp, qwen, gemma, "open weights", "decision model", "tool calling",
  diffusion. Each returned 200 with 11-30 story hits; total distinct candidates
  considered well over 100 (the qwen query alone reported 220 total results). One
  further query ("small language model") timed out and was NOT completed; two
  compound OR queries returned nbHits 0 (syntax, not absence). No 403s anywhere.
- Pass 2 (deep reads, 11 fetches of 10 distinct targets): strandsagents.com
  introducing-strands-decider (WebFetch, succeeded on retry after a 60 s timeout);
  HN item 49987076 thread; synthpop.ai guessing post 1 (alternate reader after
  timeout); huggingface.co/blog/ggml-org/decision-models-in-llamacpp (WebFetch
  retry); tej.as Kolibri teardown; github.com/firelex/jeff-code;
  github.com/githubnext/localjev; dirac.run/posts/easycommand; justine.lol/matmul;
  HN item 49953495 thread; arxiv.org/abs/2608.08188 abstract.
- Overlap instrument: grep of catalog/catalog.jsonl plus memory/rib, memory/burns,
  memory/lenses, memory/research_packs, memory/frontier, memory/steal, memory/improve,
  memory/press, memory/zknot, memory/briefs, and all prior frontier_olm sweep dirs
  (09-30 through 10-07). Note: catalog.jsonl rows are file-path metadata only, so
  title greps hit paths (e.g. the one "kolibri" hit is a raw search xml filename,
  catalog/catalog.jsonl:1195673); content-level dedup lives in the sweep banks and
  memory, which were grepped directly.

## Banked items (5, strongest first)

### 1. Strands Decider 2B (blog + 238-pt thread, today)

- Source: https://strandsagents.com/blog/introducing-strands-decider/ (read this
  session) + HN thread https://news.ycombinator.com/item?id=49987076 (238 pts,
  67 comments, 2026-10-07).
- What it is: "we take a pre-trained LLM torso (Qwen3.5-2B), and remove the LM head,
  taking away its ability to generate text" (blog, verbatim); decisions come from a
  pointer head scoring option end-of-line hidden states against the question state
  (author mjb in-thread: "the hidden state at the end of the question is the query q").
  "It's a 2 billion parameter model, suitable for running on a local CPU or GPU,
  which can return answers to meaningful questions in tens of milliseconds."
- Self-reported measurements: "3rd of 33 in the 2B class" on accuracy+calibration;
  "100% of the easy tasks on JevBench correctly"; "median of around 115ms on widely
  available hardware" (153 ms small tasks on an M3 MacBook). Thread users measured
  0.5 s (six cores) to 1.7 s (Docker, M3 CPU) on their own prompts: conditions
  differ, both are user-grade not vendor-grade numbers.
- Thread cautions (read in 49987076): option-order sensitivity with first-position
  bias on v19 ("v21 is much less sensitive to ordering, but still shows a first
  position bias", fxwin); LoRA-to-GGUF conversion fails today
  ("Can not map tensor 'layers.0.linear_attn.in_proj_a.weight'", hrpnk); the 2B base
  has "fairly limited single-pass reasoning ability" on JevBench hard (author).
- Why the estate cares: this is the first 2B-class open decision model from a major
  player (AWS Strands) that matches the estate's rung-under-gemma:2b shape: local,
  CPU-tens-of-ms, typed outputs. It does NOT clear the estate gate by existing
  (gate: beat-embeddings baseline AND >=0.880 accuracy on n>=40 non-model-provenance
  rows, lens/burns.md:92-94); no public source reports that shape. It is the first
  candidate worth firing the estate's own gate on.
- Overlap: grep "strands-decider"/"Strands Decider" = 0 in catalog.jsonl and
  memory/; day-6 held only the 10-01 6-pt submission at title level
  (watch/inbox/frontier_olm_2026-10-06/sweep/_hn_census_1006_out.txt:40,
  sweep/open-and-local-models-arxiv.md:195). No content banked before this sitting.
- OWED: exact license (the blog does not state one; says open source on GitHub,
  weights + training data on Hugging Face; repos not fetched this sitting);
  v21 option-order re-test on estate prompts; brooker.co.za "engineering-system-one"
  pointer-head deep post (linked from thread, not fetched).

### 2. Jeff-Code: 0.8B decision model gating a 27B worker (repo deep-read)

- Source: https://github.com/firelex/jeff-code (read this session); HN 49968868,
  2026-10-05.
- Measured claim (README, verbatim): "Jeff takes the routine steps itself and
  decides when Qwen should think. 47% faster (32% less time) per task at the same
  pass rate." Pairwise instrument: 1,242 paired tasks across 4 workspaces,
  per-task wall time 0.68x, same pass rate, p95 0.75x.
- Estate-relevant details: GGUF weights on HF firelex/jeff with "Q8_0 recommended,
  Q4_K_M loses 6% of decisions" - the first quant-ladder penalty number I have read
  for the decision rung class (echoes day-6's bit-ladder row at 0.6B,
  lens/burns.md:95-98). Also documents the serving gap: systemone not in vLLM/HF
  TEI yet (TEI roadmap mention), llama.cpp path via llama-systemone / llama-run.
- Why: this is the estate's own architecture (cheap local decision rung gating an
  expensive worker) shipped by a third party with a paired-task instrument. The
  instrument (same task, both configs, compare time AND pass rate) is stealable for
  the estate's n>=40 meter design.
- Overlap: jeff-code grep = 0 in all sweep mds and registers; present only in raw
  harvests (watch/inbox/frontier_olm_2026-10-06/sweep/_raw/as_LocalLLaMA_p1.json,
  sweep/doors/ff_arctic_posts.jsonl), never banked as content. Genuinely new bank.

### 3. Synthpop calibration audit: 575,442 calls against Jev (deep-read upgrade)

- Source: https://www.synthpop.ai/resources/does-a-decision-model-know-when-it-is-guessing-post-1
  (read this session); HN 49933643, 2026-10-02.
- Verbatim: "We ran about 575,000 queries against Jev, a decision model. Its
  confidence worked on familiar tasks and stayed high when it had nothing to go on."
- Measured rows read this session: Banking77 with no hints: accuracy 0.010 at
  confidence 0.320 (calibration error 0.310); CLINC with 8 examples per category:
  accuracy 0.979 at confidence 0.974 (cal error 0.005); knowledge boundary: past a
  late-2024 cutoff, accuracy 51% while confidence ROSE to 82%; recalibration cannot
  fix it (reliability gaps of 17-31 points persist). Open comparison model
  GLiNER2.5-Decide "stayed close to even split with no information (1.7%)" but was
  less accurate than Jev with category names.
- Why: this is the instrument-measured half of research question 2. The estate gate
  tests accuracy vs an embeddings baseline; this audit shows the OTHER failure mode
  (confidence decoupled from information) that an accuracy-only gate will not
  catch. The needle-corpus knowledge-boundary probe is a stealable falsifier for
  any decision rung the estate adopts.
- Overlap: day-6 banked this sweep-level with one quote (51%/82%,
  watch/inbox/frontier_olm_2026-10-06/DIGEST.md:11, sweep/finetuning-adaptation-hn.md);
  this bank adds the full tables, the GLiNER contrast, and the recalibration
  negative result. Upgrade, not re-bank.

### 4. Strata engine thread: 3x local MoE throughput, with a quality-regression catch

- Source: HN thread https://news.ycombinator.com/item?id=49953495 (924 pts, 422
  comments, 2026-10-04; repo github.com/Niko1221/Strata, not fetched).
- Verbatim (thread): "On llama.cpp I could only run the IQ3_XXS quant at 21 t/s on
  my R9700 + system RAM, and on Strata I can run it at 60 t/s."
- Also read in-thread: multi-token-predict drafting "> 110 tokens/sec", described as
  lossless ("Drafted tokens are not accepted if the original model would not have
  selected them"); DeepSWE self-report "neck and neck with Opus 4.7 and Sonnet 5" at
  a 3-bit quant; "upstream llama.cpp ... they just got System1 support too"
  (corroborates the day-6 systemone row from a second direction).
- The catch (why this is banked as caution, not adoption advice): a commenter ran
  the SAME GGUF + vision adapter on both engines: "median error distance of 154.8
  pixels" on Strata vs "a median error of 46.5" on llama.cpp, plus hallucination
  reports - an engine-level quality regression at identical weights. Any fork
  adoption must re-run an estate quality bench, not just a speed bench.
- Overlap: Strata engine intel held at reddit tier by the 10-03 quant sweep
  (threads 1wtv43r, 1wwceh8 with NVFP4 4,112 tok/s prefill / 125 tok/s decode /
  94.87% MTP acceptance, watch/inbox/frontier_olm_2026-10-03/sweep/quantization-and-compression-reddit.md:34-37);
  the 924-pt HN thread itself and the same-weights quality regression are new.

### 5. localjev: DiffusionGemma as a local /v1/systemone engine (repo deep-read)

- Source: https://github.com/githubnext/localjev (read this session); HN 49766255,
  2026-09-19; repo sections dated Sep 17-18, 2026.
- Verbatim (README): "LocalJev takes between 200 and 400 ms on a laptop with GGUF
  weights. oMLX with the safetensors checkpoint serves each request in 24.6-28.7 ms
  (median 26.8)." Bake-off: 1,200 requests across 5 users, 4/5 rated the local
  setup "extremely fast".
- Production-viability facts read this session: the diffusion lineage's structured
  reads need read-only denoising + seeded diffusion canvases (deterministic answers,
  logprobs readable); GGUF is the wrong container (3-6x slower, strips adapter
  configs, zero determinism); oMLX serves safetensors correctly today; LM Studio
  cannot load it (truncated config schema, wrong rope settings).
- Security caution read in the same README: a weight-poisoning probe (mallory
  variants, safetensors header lists float32 - suspicious for a 26B A4B checkpoint)
  was "NOT DETECTED by either" LM Studio or oMLX loader checks. Local-weights
  supply chain has no loader-level verification: directly relevant to any
  estate adoption of open-weights diffusion checkpoints.
- Why (question 4): ALoDLM (arXiv 2610.04198, held since 10-06,
  lens/burns.md:119-122) is the research edge of this family; localjev is the
  production-shape evidence that the diffusion lineage is viable locally only via
  safetensors + a real runtime, not via the GGUF/Ollama path the estate's janitor
  tier uses. QUEEN-style silent-expert welds stay research-only (no new runtime
  evidence appeared in the window).
- Overlap: DiffusionGemma ecosystem is held (memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md;
  10-03 DIGEST.md:264 license-flip scrutiny; 10-03 arctic harvests carry
  TensorSharp-vs-LocalJev benchmarks). The repo-level bake-off, oMLX latency table,
  and the poisoning non-detection are not in any prior bank.

## Updates to already-held rows (no re-bank, deltas only)

- llama.cpp decision models blog (held, day-6 register row 3): delta read this
  session from the same blog - per-model median latencies (Julia-1 3 ms, Laya 5 ms,
  Kev-4B 12 ms, lev 36 ms, OpenJev 43 ms on one RTX PRO 6000), router mode (model
  per request via /v1/models), "Cloudflare's Clef is next" with a 27B Apache-2.0
  Clef table entry, and a community batch-size-512 error on 11,982-token inputs.
- Kolibri (held, 10-03 sweep): my read of the same tej.as teardown confirms
  78.1B/3.46B active, BFCL multi-turn 39.8, Apache 2.0; adds only trivia/party-game
  German strength and MMMLU german 78.5. Out of the estate band (needs ~78 GB);
  no change to the held verdict.
- EasyCommand (held, 10-05 finetuning sweep): confirmed 1.5B Qwen2.5-LC LoRA r=32,
  400k synthetic examples, ALFA 70.7% vs GPT-4o 73.0% (published numbers), 2.8x
  faster generation. Still the only measured 0.5-8B chat-band finetune in the
  window; already banked, nothing new to add.
- justine.lol/matmul (HN 49938916, 2026-10-02): the fetched page's own dateline is
  "Mar 31st, 2024" - the submission is a resubmit of the 2024 article, NOT a new
  runtime change since 10-01. Not banked.

## Per-question verdicts

- Q1 (0.5B-8B beating gemma:2b / gemma4 / qwen2.5:7b, measured): NO new open-weight
  chat model in the band surfaced on HN in the window with instrument-measured
  instruction-following/tool-calling/long-session evidence. The band's measured
  action is decision models (items 1-2; Gutsy 0.8B and Wazn-2B held at listing
  level by day-6, sweep/open-and-local-models-hn.md:235) plus the held EasyCommand
  bash finetune. Cells stay UNMEASURED until estate instruments run
  (lens/laws.md:48 stands).
- Q2 (sub-1B router clearing an embedding-baseline bar at >=0.880 on n>=40): the
  rung stays UNSUPPORTED. No public source I read reports that shape. Closest
  public instruments: synthpop calibration audit (item 3) and JevBench-style
  leaderboards - an estate-held reddit harvest (read this session,
  watch/inbox/frontier_olm_2026-10-06/sweep/doors/ff_arctic_posts.jsonl:59, ARC-1
  selftext) quotes JevBench public 231: Jev 86.6, Strands Decider 2B 72.3
  self-reported, ARC-1 68.4, Laya 58.4 - note 0.880 is not cleared even by hosted
  Jev on that instrument, and these are vendor/self numbers, not estate
  instruments. Corroborating context read in-thread (49987076): Intern-Decision
  0.8B/2B/4B share the Qwen3.5 base + pointer head.
- Q3 (Ollama/llama.cpp lineage since 10-01): (a) /v1/systemone decision models in
  llama.cpp (held day-6; deltas above); (b) Strata-class expert-caching forks +
  MTP drafting (item 4, with the quality-regression caution); (c) no new
  Ollama-side feature since 0.35 nimble (held) appeared in the window's HN stream.
- Q4 (non-standard lineages, viable vs research-only): production-viable now =
  DiffusionGemma via safetensors/oMLX-style runtimes (item 5, with the
  supply-chain caution). Research-only (no runtime evidence in window): ALoDLM
  (project page alo-dlm.github.io hit HN 10-06 at 2 pts; not fetched, held via
  lens/burns.md:119-122), QUEEN (held), Bonsai 2 ternary (read in Strata thread:
  "vastly improved but still requires a custom llama.cpp fork" vs "really bad when
  you actually use them"), Mercury 2.5 diffusion (hosted, openrouter).
- Q5 (frontier_thinking shelf candidates, so state/arxiv's 4,998 files are not
  re-derived): (1) arXiv 2608.08188 "Quantization Degradation in Large Language
  Models: A Signal-Noise Perspective" (submitted 2026-08-08; abstract fetched this
  session; grep 2608.08188 = 0 hits in catalog + memory + prior sweeps) - anchors
  the "4-bit usually preserves, 2-bit broadly degrades, 3-bit varies" ladder the
  estate keeps re-measuring; (2) the pointer-head decision architecture (Strands
  blog + the brooker.co.za post it links, OWED); (3) the knowledge-boundary
  needle-corpus probe (synthpop post 1); (4) the paired-task time-and-pass-rate
  instrument (Jeff-Code README).

## Not run / OWED (do not assert these)

- No estate instrument fired (no ollama pulls, no meter rows, no gate runs); every
  number above is a fetched external number, vendor- or user-grade.
- Not fetched: Strands Decider GitHub/HF repos (license unverified); the Decision
  Index 0.2.1 HF space (70 open reproductions leaderboard); ARC-1 live sources
  (only the estate harvest selftext was read); brooker.co.za deep post; the Strata
  repo itself; Ollama release notes beyond what HN carried.
- The "small language model" Algolia query timed out: that slice was not swept.

## Receipt

Fetches this session: 8 Algolia search calls (all 200), 3 HN item pages
(49987076, 49953495 via WebFetch; 49953495 content also via alternate reader), 8
primary pages (strandsagents blog x2, synthpop, HF ggml blog, tej.as, jeff-code,
localjev, easycommand, justine.lol, arxiv 2608.08188). Overlap greps: 3 Bash grep
passes over catalog.jsonl + memory dirs + all frontier_olm sweep dirs (outputs
persisted in the session exec log). This file is the bank; the JSON result carries
the 5 items.
