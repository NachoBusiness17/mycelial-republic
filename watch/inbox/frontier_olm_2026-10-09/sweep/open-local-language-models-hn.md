# Frontier sweep: open-local-language-models via HN (2026-10-09)

source-fetched: 2026-10-09. Seat: sweep-open-local-language-models-hn (dynamic workflow subagent
of the frontier_olm run). Door: Hacker News via hn.algolia.com API + item threads, per the ask's
fetch recipe. Laws held: no fabrication (OWED where unreachable), byte/URL cites, ascii only,
no em-dashes. Honest frame up front: sibling seats swept this area DAILY (frontier_olm_2026-09-30
through 2026-10-08, lanes open-local-language-models-hn / open-and-local-models-hn /
quantization-compression-hn / inference-efficiency-hn / evals-self-improvement-hn), so this
sitting's pass-1 re-surfaced mostly held rows; the bank below is deltas and genuinely new content
only, per the re-banking-is-waste law.

## Door health and method (what was actually run this sitting)

- Pass 1 (broad): 13 completed Algolia search_by_date queries, tags=story, hitsPerPage=30,
  numericFilters created_at_i > 1788912000 (since 2026-09-09): Qwen, Gemma, "local LLM",
  quantization, llama.cpp, Ollama, "open weights", GGUF, Mistral, "on-device LLM",
  "decision model", "Gemma 4", "Qwen3.8". All returned valid JSON; no 403s, no timeouts.
  ~330 raw rows listed; after dedupe, 30+ distinct in-window candidates considered (the
  strongest 60 are in the session exec log). Standout pass-1 clusters: the decision-model /
  Jev-style cluster (30+ stories: Strands Decider 2B 284 pts, Ollaya 618 pts, Gutsy, Clef,
  Liquid d1, nimble/tev1), the Qwen3.8 serving cluster (Flash-Next on 8GB GPUs, Strix Halo,
  megakernel Gemma 4), and Mistral Large 4 "Le Chonk" (2034 pts).
- Pass 2 (deep reads, 15 fetches of 13 distinct targets, all read end to end by this seat):
  strandsagents.com introducing-strands-decider + HN 49987076 thread; huggingface.co/blog/
  ggml-org/decision-models-in-llamacpp + HN 49942092; ollama.com/blog/
  ollama-now-supports-jev-style-decision-models + HN 49906337; weaviate.io/blog/
  4-bit-rotational-quantization + HN 49743523; blog.mozilla.ai benchmarking-local-llm-servers
  + HN 49742415; github.com/firelex/jeff-code + HN 49968868; discuss.huggingface.co VeriLoop
  E2 thread 180723; ollama.com/library/clef; sota.borgcloud.ai; synthpop.ai guessing post 1;
  github.com/kouhxp/gutsy; news.ycombinator.com/item?id=49977979 (Mistral Large 4 thread);
  huggingface.co/spaces/multimodalart/jev-decision-index (DEGRADED, see item 8).
- Overlap instruments run this sitting (scripts persisted in this directory):
  `_overlap_catalog.ps1` (16 patterns over catalog/catalog.jsonl, all rows scanned),
  `_overlap_memory.ps1` (12 patterns over memory/*.md,*.json,*.jsonl excluding broken
  biography/knots symlinks; was still grinding huge trajectory logs at submit time; the
  patterns that completed are quoted in item notes), and `_overlap_siblings.ps1` (12 patterns
  over all nine prior frontier_olm sweep dirs). Plus a verified shelf count:
  `grep -c "ms-genai" catalog/catalog.jsonl` = 12142 and `grep -c "openai-cookbook"
  catalog/catalog.jsonl` = 3120 (both match the ask's LENS 1 figures exactly);
  agent_platform reads 72347 today (+18 vs the ask's 72329).

## What the overlap greps found (the frame for everything below)

- The estate is NOT new to the decision-model category: catalog has 152 "Jev" rows including
  corpus/library/jev_steal_library/ and corpus/library/kev/ ("Kev - prototype of a Jev-style"
  model, catalog.jsonl L27777; corpus/library/kev/PLAN_27b.md is a Qwen3.8-27B Kev-scale-up
  proposal, read this sitting, with night-2 runs at 4B, 9B, 35B-A3B on Qwen3.5 bases per its
  line 35), 22 "decision model" rows, 11 "System One" rows. The category mainstreaming
  (llama.cpp /v1/systemone, Ollama 0.35, 70-reproduction Decision Index) is therefore
  VALIDATION of an estate bet, not news.
- Already banked by siblings, do NOT re-bank (verified by _overlap_siblings.ps1): Strands
  Decider 2B (10-07 olm-hn item 1), Jeff-Code (10-07 item 2 + 10-08 item 7), Synthpop
  calibration (10-06 + 10-07 item 3), Clef thread (10-08 item 1), Reflex (10-08 item 3),
  Jiwo (10-08 item 2), Weaviate 4-bit RQ (10-03 c2 + 10-06 inference-efficiency item 7),
  VeriLoop ladder (09-30 quant lane + register row 15), SoTA Feed (09-30 arxiv sibling BANK),
  Mozilla server bench (10-04 inference-efficiency item 7, READ FULL TEXT), Mistral Large 4
  announcement (10-06 open-and-local-models-hn.md:118-119, listing level).

## Banked items (8, strongest first; deltas and new content only)

### 1. Gutsy 0.8B deep read: the "subsecond CPU" listing line does not survive hard tiers

- Source: https://github.com/kouhxp/gutsy (README read end to end this sitting); Show HN
  49923223 (2026-10-01) + 49939547 + 49961971.
- What I read: gutsy-0.8b v0.4 is a fine-tune of Qwen3.5-0.8B returning calibrated per-option
  probabilities (choice/score/yes-no) with margin, confidence and a REJECT option, up to 255
  options; Apache 2.0 code+weights; GGUF Q8_0 775 MB / Q4_K_M 505 MB; llama.cpp-based
  `gutsy-inference` HTTP server on port 8765 speaking the Jev-style Decisions format.
  Latency (README's own table, JevBench hard tier, Q8_0): median 4.3 s, p95 27 s on long
  states. Verbatim: "Local decision models with calibrated probabilities. Send a state
  (text or JSON) and typed questions (yes/no, choice, score); get a probability for every
  option back."
- Why (estate map): the first sub-1B decision model whose Q4_K_M GGUF exists and whose own
  README publishes an unflattering hard-tier latency: the estate's scut tier lives on easy
  tiers, but any gate cell must pin tier and state length or the "subsecond" framing from
  the 10-06 listing line (finetuning-adaptation-hn.md:76) mismeasures it. The reject option
  is also the API shape the consent laws want (a janitor that can say "not confident").
- Overlap: held listing-only by day-6 (sweep/finetuning-adaptation-hn.md:76, 294) plus a raw
  harvest mention (10-02 open-and-local-language-models-hn.md:51, supply-line note); grep
  "Gutsy" = 0 in catalog.jsonl. README content (latency table, reject option, Q4_K_M tag,
  port 8765) was in no prior bank. Delta bank, not a re-bank.
- Confidence: 0.85.

### 2. VeriLoop E2 delta: Q4 ties Q8 at task level while carrying 4.5x the drift (LENS 4)

- Source: https://discuss.huggingface.co/t/veriloop-e2-release-27b-post-trained-model-and-
  full-gguf-precision-ladder-from-bf16-to-iq1-m/180723 (thread read end to end this sitting).
- What I read: a 27B (Qwen3.8-27B base, 1,841,831 training records) shipped with a full GGUF
  ladder quantized each from canonical BF16 (Q8_0, Q6_K, Q5_K_M, Q4_K_M, Q3_K_M, IQ2_S,
  IQ1_M) plus a per-tier retention table: Q8_0 mean KLD 0.002176 / same-top-p 98.815%,
  Q4_K_M KLD 0.009700 / 96.786% (4.5x Q8_0's drift), all tiers under ~1% PPL drift. A
  community canary checked IQ1_M vs Q4_K_M: agreement on ALL 8 test items (5/8 correct
  each). The post itself cautions these are quantization-retention metrics, NOT rerun
  downstream benchmarks. Verbatim: "Generation and verification should not belong to the
  same authority."
- Why (estate map): this is the cleanest external answer yet to LENS 4's open question
  (does the qwen2.5:7b Q4-vs-q8 TIE generalize): a task-level tie (8/8) and a distribution
  drift that differs 4.5x between the same two tiers are BOTH true at once, which means a
  tie verdict is instrument-narrow, and n=8 canaries are the weakest instrument that can
  still produce one. The estate's own qwen2.5:7b Q4_K_M vs q8_0 A/B remains UN-RUN
  (frontier_olm_2026-10-07/lens/burns.md:97); this says run it at n>=40 and report drift
  (KLD/same-top-p) next to task accuracy, not accuracy alone.
- Overlap: the ladder itself is banked (09-30 quantization-compression-hn.md:23, register
  row 15, referenced 10-08 steal/quantization-compression via hn.md:100); the per-tier KLD
  table, the same-top-p column, and the 8/8 canary row were in no bank I read
  (10-07/lens/questions.md:83 holds only the decision-model bf16/Q8/Q4 row 0.757/0.750/0.703).
  Delta bank.
- Confidence: 0.8 (canary numbers are a community post's claim inside the thread).

### 3. llama.cpp decision-models delta: the license split gates adoption (OpenJev is CC BY-NC)

- Source: https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp (read end to end
  this sitting); HN 49934323 / 49942092 (2026-10-02/03, low-traction threads, no comments).
- What I read: decision models are served via llama-server's /v1/systemone endpoint in the
  System One format introduced with TypeSafe's Jev (implementation PR #29818); question
  types choice / score / noul, each answer carrying a confidence value, batching encouraged.
  Supported-models table with licenses: Julia-1 (144M, mmBERT-small, 3 ms), Laya (421M,
  ModernBERT-large, 5 ms), Kev-4B (4B, Qwen3.5-4B-Base, 12 ms), lev (4B, Qwen3.5-4B,
  36 ms) all Apache 2.0; OpenJev (27B, Qwen3.8-27B, vision, 43 ms) is CC BY-NC 4.0
  (NONCOMMERCIAL); Clef (27B) listed next. Verbatim: "What is a decision model? A model
  that answers by scoring the options you give it, instead of generating text."
- Why (estate map): two adoption-gate facts the prior banks did not hold. (a) The license
  split: every sub-5B decision model in the llama.cpp table is Apache 2.0, the one
  vision-capable 27B (OpenJev) is noncommercial, so a consent-law-clean vision decision
  rung has NO in-table candidate today. (b) The table's "Kev-4B" row intersects the
  estate's own Kev program (corpus/library/kev/, night-2 runs at 4B on Qwen3.5) but
  identity is UNVERIFIED: an external github.com/jaredpalmer/kev exists in the 10-02 raw
  harvest (open-and-local-language-models-hn.md:20). OWED: one HF/GitHub fetch to settle
  whose Kev-4B llama.cpp serves.
- Overlap: blog held day-6 (register row 3) with the 10-07 delta holding per-model latencies
  and the "27B Apache-2.0 Clef table entry" (10-07 olm-hn.md:168-169); the OpenJev CC BY-NC
  row, the all-Apache sub-5B pattern, and the Kev-4B identity question are new. Delta bank.
- Confidence: 0.9.

### 4. Strands Decider 2B delta: v21 adds vision; author concedes JevBench confidence weakness

- Source: https://strandsagents.com/blog/introducing-strands-decider/ + HN thread
  https://news.ycombinator.com/item?id=49987076 (284 pts, 2026-10-07; both re-read end to
  end this sitting).
- Delta over the 10-07 bank (which held the architecture, 115/153 ms latencies, v19
  option-order bias, LoRA-to-GGUF failure): (a) author mjb in-thread: "Notes v21 supports
  vision and admits JevBench has weaknesses (confidence handling)" - the first
  vision-capable sub-5B decision model, but with the author's own admission that the
  category benchmark under-tests calibration; (b) pointer-head mechanics: per-option
  end-of-line hidden state as key, question state as query, per-option logit is a dot
  product scaled by sqrt(256); (c) gopalv's CPU measurement: Docker on an M3 Mac,
  ~1.7 s per decision, 1 output token (third user-grade number alongside the 10-07 bank's
  0.5 s six-core and vendor 115 ms). Verbatim (blog): "In exchange for this reduction in
  flexibility, decision models are faster and more capable at a given size, always produce
  an answer from the selected options."
- Why (estate map): the 2B category leader is converging on exactly the estate's
  rung-under-gemma:2b shape, and v21-vision widens it to screenshot states (the estate's
  dashboard/museum surfaces produce those). The calibration concession strengthens the
  synthpop-held lesson: any estate gate on this rung must include a calibration term, not
  accuracy alone.
- Overlap: fully banked 10-07 (same seat name, items 1); memory grep found 7
  "Strands Decider" hits, all memory/trajectory/steps.jsonl session-log rows from the
  10-07 sibling session. Update row, not a re-bank.
- Confidence: 0.88.

### 5. Mistral Large 4 thread: the window's flagship release, with a benchmark-integrity catch

- Source: HN https://news.ycombinator.com/item?id=49977979 (2034 pts, 1210 comments,
  2026-10-06; thread read end to end this sitting; mistral.ai blog not fetched).
- What I read: (a) oh_no's cherry-pick accusation with specific numbers: Mistral's own
  benchmark chart shows Sol 5.6 at 12.8 while Artificial Analysis lists Sol 5.6 Max at 27 -
  "I'd love AI companies to stop lying about this stuff." (b) simonw: only "none"/"high"
  reasoning modes exist, the setting made little difference, and "high" produced FEWER
  output tokens. (c) Cross-lab random-word clustering: asking many labs' models for "a
  single random word" clusters on the same tokens ("Lantern", "Zephyr", "Petrichor"),
  read in-thread as a distillation/training-data fingerprint; bityard's caution that this
  reveals training-set bias, not non-randomness. Reasoning levels: "none" or "high" only.
- Why (estate map): answers RQ1's release-census leg - the biggest open-model event since
  10-01 (open weights promised per the held 10-06 listing, 1T params, OUT of the janitor
  band - it replaces nothing at T0/T1) - and banks a benchmark-integrity pattern (vendor
  chart vs third-party ruler) that the model-garden intake should screen every release
  card against, the same way the 10-06 bank flagged Bongard-mini's 100/57.7 split.
- Overlap: announcement held listing-level (10-06 open-and-local-models-hn.md:118-119
  "open weights only promised soon"); the X lane read the primary blog, not the thread
  (10-08 open-local-models-x.md:76 "READ primary, out of band"). Thread content (the 12.8
  vs 27 chart catch, reasoning-mode finding, random-word clustering) is new to the banks.
  Delta bank. Confidence: 0.82 (the 12.8-vs-27 numbers are a commenter's claim, not
  verified against Artificial Analysis this sitting).
- Quote: "I'd love AI companies to stop lying about this stuff." (oh_no, verbatim).

### 6. Clef on the Ollama library: the 10-08 thread bank is one pull away from a measured cell

- Source: https://ollama.com/library/clef (page read end to end this sitting); Show HN
  49963695 (2026-10-05).
- What I read: two tags, clef:latest and clef:27b, both 18 GB, 256K context, text+image
  input, updated days ago; Cloudflare's 27B decision model fine-tuned from Qwen3.8-27B,
  speaking choice/noul/score over /v1/systemone. Verbatim: "One forward pass: Every option
  of every question is scored jointly in a single non-autoregressive pass."
- Why (estate map): converts the 10-08 Clef thread bank (which held third-party accuracy
  and latency rows) into the cheapest testable cell in this window's crop: `ollama pull
  clef` lands it in the janitor runtime with zero new serving code, after which the
  estate gate (beat-embeddings baseline AND >=0.880 on n>=40, per the held laws context)
  can fire. The 18 GB size also bounds it out of the laptop tier; it is a desk/GPU-lane
  animal, not a gemma:2b replacement.
- Overlap: thread fully banked 10-08 (item 1); the library page itself held as raw HTML
  since 10-05 (catalog.jsonl:1073386, watch/inbox/frontier_olm_2026-10-05/sweep/_clef.html);
  tag sizes, 256K context, and the one-pull deployment fact are the delta. Delta bank.
- Confidence: 0.85.

### 7. Mozilla local-server bench delta: config beats engine, and the quant artifact caveat

- Source: https://blog.mozilla.ai/benchmarking-local-llm-servers-llama-cpp-llamafile-lm-
  studio-and-ollama/ (read end to end this sitting) + HN 49742415 thread (2 comments).
- What I read: four servers, same GGUF weights, three platforms (M4 Max Metal, L40S CUDA,
  Deck Vulkan), Qwen 0.8B/9B/27B. Findings: configuration beat engine choice (all four
  share the llama.cpp core, within a few percent on prefill); build flags moved decode
  16.8% and Deck prefill 63.3%; server overhead is mostly fixed host cost (~0.4 ms/token
  Mac, 1.8 ms L40S, 5.4 ms Deck) and is largest in percentage terms exactly on the 0.8B
  class the estate's scut tier lives at; the speculative-decoding optimum flips by
  platform (draft 2 on Metal, draft 4 on CUDA). Quant caveat on the MLX 27B cell: the
  three servers shipped DIFFERENT quantizations (Q4_K_M 17.7 GB vs 4-bit 15 GB vs nvfp4
  18.2 GB) and Ollama self-enabled speculative decoding, so those numbers are
  non-comparable. Thread critique (Lockal, the only substantive comment): "There are no
  results in this page - 'we tested exact model on exact hardware' and then (slop slop
  slop) we don't know what we did". Verbatim (article): "One compiler flag we'd left off
  in llamafile was costing us seventeen percent."
- Why (estate map): RQ4's small-model-serving shelf content, and its two warnings are
  LENS 2 UNMEASURED-cell lessons: (a) on the 0.8B class, serving overhead is a
  first-order percent, so any janitor A/B must pin the server and flags; (b) the
  quant-per-server artifact row is the same trap LENS 4's grid has (a "Q4" cell is not
  one cell unless the quant recipe is pinned).
- Overlap: banked READ FULL TEXT by the 10-04 inference-efficiency lane
  (inference-efficiency-hn.md:56-57) and re-fetched by the 10-01 X steal lane. The thread
  critique, the per-platform overhead numbers as stated here, and the MLX quant-artifact
  row are the delta I can add. Delta bank; low priority.
- Confidence: 0.85.

### 8. Jev Decision Index space: second failed read, still OWED (negative row)

- Source: https://huggingface.co/spaces/multimodalart/jev-decision-index (fetched this
  sitting; DEGRADED).
- What I got: the page returned only "Refreshing" - no leaderboard rows, no metric
  definitions, nothing to read end to end. Verbatim (all the page yielded): "Jev Decision
  Index - a Hugging Face Space by multimodalart". I am NOT banking any index contents;
  nothing about the 70 reproductions was verified by me this sitting.
- Why (estate map): keeps an OWED honest. The 10-07 bank listed the Decision Index 0.2.1
  leaderboard as instrument debt (10-07 DIGEST.md:83); the 10-08 bank partially paid it
  via jiwo's self-reported scores; my fetch is a second independent failure on a second
  day, which suggests the space renders client-side and will not yield to the WebFetch
  door. OWED: read it through a JS-capable browser door or the HF datasets API before any
  bank cites Decision Index scores as anything but self-reported.
- Overlap: index held listing-level day-6 (finetuning-adaptation-hn.md:87) and day-5
  arxiv sibling (open-and-local-models-arxiv.md:88); no prior bank claims a successful
  end-to-end read. Negative row, new.
- Confidence: 0.9 that MY fetch degraded (the fetch itself is the evidence).

## Per-research-question verdicts (this seat's read; every number above is a fetched
external number or a locally run grep; no estate instrument was fired)

- RQ1 (releases since 10-01 justifying a janitor-tier replacement): NO new 0.5-8B chat
  model surfaced that justifies replacing gemma:2b/gemma4 on today's evidence, replicating
  the 10-07 and 10-08 Q1 verdicts from a fresh 13-query pass. The band's measured action
  stays decision models (Gutsy 0.8B, Clef 27B/flash, Strands 2B v21, nimble 9B / tev1
  0.8B), and NONE clears the estate gate by existing - cells stay UNMEASURED until the
  gate fires. Mistral Large 4 (item 5) is the window's flagship release but is 1T and
  open-weights-promised, irrelevant to T0/T1.
- RQ2 (does the Q4-vs-q8 TIE AT CEILING generalize): the external evidence this window
  says treat the tie as instrument-narrow. VeriLoop's own ladder (item 2): Q4_K_M carries
  4.5x Q8_0's mean KLD while an 8-item canary shows an 8/8 task tie - both true at once.
  Jeff-Code (held 10-07): Q4_K_M loses 6% of decisions vs Q8_0 on the decision rung.
  Weaviate RQ4 (held 10-03/10-06): raw 4-bit recall clearly below 8-bit (72.0 vs 93.4 on
  nfcorpus), closed only by rescoring. Mozilla (item 7): servers shipped different quants
  under the same "Q4" label. Verdict: the tie does not transfer across architectures,
  tiers, or even quant recipes; the estate's own A/B (qwen2.5:7b Q4_K_M vs q8_0, un-run
  per 10-07 lens/burns.md:97) remains the only verdict that counts for our cell, and it
  should report a drift statistic (KLD / same-top-p) beside accuracy.
- RQ3 (wire the green arXiv door into model-garden intake): the shortcut already exists
  and is banked: SoTA Feed (sota.borgcloud.ai) publishes RSS + Atom feeds of open-weights
  releases with date/lab/size/architecture/license per row (read end to end this sitting;
  banked as the release tracker by the 09-30 arxiv sibling). HN-first search_by_date
  feeds major releases within days but misses the 1-2 pt Show HN long tail unless every
  pass carries family-keyword queries (this sitting's 13 queries caught jiwo-class and
  Gutsy-class items only through the targeted "decision model" query; 10-08 Q5 reached
  the same conclusion independently). The llama.cpp decision-models table (item 3) is
  itself a third intake surface: models appear there within days of release, license
  included.
- RQ4 (which shelves document small-model serving, which cells need fresh pulls): the
  serving lineage lives OUTSIDE the two library shelves the ask names - catalog greps
  this sitting: corpus/library/kev/ (decision-model serving plans, PLAN_27b.md read),
  corpus/library/jev_steal_library/ (152 Jev rows), corpus/library/second-brain-os/docs/
  track-jev/system-one-models.md, plus memory/runs/gapwave/ live-run rows (splash/bonsai,
  2026-09-20). The named shelves verify at exactly the ask's counts (ms-genai 12,142;
  openai-cookbook 3,120; command + output in the receipt) and are generic serving/docs
  corpora, not decision-rung or quant-ladder references. Cells needing fresh pulls, in
  priority order: (1) the estate's own qwen2.5:7b Q4_K_M vs q8_0 A/B (owed since before
  this window); (2) one decision-rung gate cell - Gutsy-0.8b Q4_K_M (505 MB, cheapest) or
  Clef (18 GB, desk lane); (3) nothing from Mistral Large 4 until weights actually ship.

## Not run / OWED (do not assert these)

- No estate instrument fired: no ollama pulls, no gate runs, no battery rows, no pytest.
  Every model number above is fetched external, vendor- or user-grade.
- Kev-4B identity (llama.cpp table vs corpus/library/kev/ vs github.com/jaredpalmer/kev):
  UNVERIFIED, one fetch owed.
- Jev Decision Index leaderboard: still unread (item 8); needs a JS-capable door or HF API.
- The `_overlap_memory.ps1` run had not finished the large trajectory/agent_sessions logs
  at submit time; patterns that completed are quoted per item. The content-level dedup
  that matters was done against the nine prior sweep banks via `_overlap_siblings.ps1`,
  which did complete.
- The ask's mine-row figure (97,867) is taken from the ask (LENS 1), not re-derived; my
  loose "mine" substring grep reads 103,672 and matches inside unrelated words, so it
  verifies nothing either way.

## Receipt

Fetches this sitting: 13 Algolia search_by_date calls (all valid JSON, zero 403s), 15 page
fetches over 13 distinct targets (5 HN threads, 6 primary articles/pages, 2 repo READMEs,
1 HF space that degraded to "Refreshing"). Local instruments: `_overlap_catalog.ps1`,
`_overlap_memory.ps1` (partial), `_overlap_siblings.ps1` (all persisted in this directory),
plus `grep -c` shelf counts (ms-genai 12142, openai-cookbook 3120, agent_platform 72347)
and two Read calls into corpus/library/kev/. This file is the bank; the JSON result carries
the same 8 items. Helper scripts only; no other repo files touched.
