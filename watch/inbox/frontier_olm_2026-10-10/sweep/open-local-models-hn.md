# Sweep: open-local-models via HN (2026-10-10)

source-fetched: 2026-10-10
seat: sweep-open-local-models-hn (dynamic workflow subagent, frontier_olm run)
area: open-local-models via hn. Doors: hn.algolia.com search_by_date + search
(numericFilters created_at_i>1788998400, window 2026-09-10..2026-10-10), HN item
threads, primary pages (vendor blogs, GitHub, HF cards, substack), one raw
README fallback after a github.com 504, one webReader re-fetch after a
title-only WebFetch. Laws held: no fabrication, verbatim quotes under 40 words,
ascii only, no em or en dashes, overlap greps before banking.

## Instruments actually run this sitting

Pass 1 (broad): 6 Algolia probes (local llm by_date + relevance, ollama, open
weights, decision model, small language model, qwen, free llm api). nbHits
seen: 94 (local llm by_date), 2952 (local llm relevance; the doors lens's 2957
is the same door a few hours stale), 78 (ollama), 79 (open weights), 147
(decision model), 14 (small language model), 235 (qwen), 17+ parsed (free llm
api, truncated). Well over 30 distinct in-window candidates considered (roughly
90 listing lines kept); strongest by points: Kolibri 709 (held), Clef 641
(held), Beam 549 (held), Cactus Needle 3 236 (held), Qwen-0.6B categorization
215 (relevance door, June), Magnitude 194 (held), Microsoft-Decision-1 192,
Apogee 64, plus the 1-2 pt Show HN long tail where this window's band finds
actually live (THX-01, Kisoku, Jevfree, FreeLLMAPI).
Pass 2 (deep reads, fetched and read end to end): cactuscompute.com/needle +
its HN thread, blog.cloudflare.com/clef-decision-models + its HN thread,
teachmecoolstuff.com 0.6B article + its HN thread,
huggingface.co/blog/ggml-org/decision-models-in-llamacpp,
aleph-alpha.com Kolibri blog, github.com/0arch-io/kisoku,
devblogs.microsoft.com WinML post, commandline.microsoft.com
microsoft-decision-1 + its HN thread, liquid.ai/blog/d1-open (later dropped as
held), ollama.com Jev blog (cross-check vs held bank), raw.githubusercontent
freellmapi README, johnnys.news Jevfree article (via webReader),
huggingface.co/doofz/THX-01 + doofz.substack.com THX-01 post. That is 14+
distinct targets, above the 5-item floor.

## Dedup ledger (excluded as already held; re-banking is waste)

- Clef HN thread (dgacmu gemma4:27b, pdlug 850 ms, ralusek 661 ms, At0M):
  banked in full by watch/inbox/frontier_olm_2026-10-08/sweep/open-local-models-hn.md:75-109.
- Kolibri (blog + thread delta): held 10-03 and 10-08 (item 8, lines 255-275).
- Beam 501B, jiwo, Reflex, Bongard-mini, Jeff-Code, EmbeddingGemma 2 thread:
  all banked by the 10-08 sweep.
- LiquidAI d1-3B / d1-omni-600M and h2o-lightning-4b: banked by the 10-08
  arxiv lane (open-local-models-arxiv.md:115-126, same Decision Index 48.57 /
  15.95 and 8 ms RTX 4090 numbers I independently gathered, then dropped).
- Windows ML llama.cpp core announcement: banked by the 10-08 reddit lane
  (open-local-models-reddit.md:118-127). My bank below is a delta only.
- Cactus Needle 3: fully held since 09-28 including the Scaevolus
  FunctionGemma falsifier (32.2/20.4 vs 90.9/85.2), per the 09-30 sweep's
  dedup ledger; my thread read re-confirmed, nothing new.
- Ollama 0.35 decision models, llama.cpp /v1/systemone blog: held 10-05/10-07.

## Banked items (7, strongest first)

### 1. THX-01: 322M Apache-2.0 decision model, third-party-measured beating Jev 1.13 on ticket routing

Primary: https://huggingface.co/doofz/THX-01 (card read end to end);
secondary: https://doofz.substack.com/p/introducing-thx-01-an-open-source
(2026-10-09); HN Show 50023978 / 50024061 (1-2 pts). Verbatim (card): "a
calibrated answer to every question in a single forward pass of about 10 ms on
one GPU." Facts: 322M total (307M mmBERT-base encoder + 15M decision head),
RLCD-trained with a strictly proper scoring-rule reward, F16 safetensors,
pip install thx01, Apache 2.0. Measured: support-ticket classification (15
classes, 2,843 tickets) 98.4 accuracy, ECE 0.003, vs TypeSafe Jev 1.13 at 97.4
(ECE 0.007, 331 ms) and Claude Sonnet 5.5 at 98.5 (1.5 s); Jev still wins
number lookup (96.6 vs 93.4); multi-task mean 84.2, ECE 0.066. Estate bearing:
this is question-class routing (Q3's exact task shape) at a third of
gemma:2b's size, measured against Jev by a third party, pip-installable, and
its ECE row is the calibration column the estate's gate should copy. Vendor
numbers until the estate battery fires. Overlap: THX-01 grep = 0 rows in
catalog.jsonl, 0 holdings in memory (only this session's trajectory log).
Confidence 0.9.

### 2. Jevfree: EmbeddingGemma 2 repurposed as a decision maker, in-browser, zero training

Primary: https://johnnys.news/2026/10/Jevfree-repurposing-an-embedding-model-for-decisions/
(read in full via webReader after WebFetch returned title-only; published
2026-10-08T20:15Z; HN 50024668). Verbatim: "It's a quick and dirty experiment
to play with the idea. An embedding model only compares 'meanings', it
doesn't reason about the situation." Method: embed the situation, embed each
option, whitening, dot-product scores, softmax at temperature 0.05, confidence
from winner margin plus flatness; MediaPipe Decision Maker recipe;
transformers.js with EmbeddingGemma 2 ONNX weights (fp16 about 1.5 GB, q4
fallback), WebGPU/WASM, example run 766 ms on q4, no server, no API key.
Honest limits stated by the author: negations and numbers fail, probabilities
are "more of a 'vibe' than an answer you should rely on." Estate bearing: the
estate already holds these exact weights (models/embeddinggemma-2-onnx/,
catalog rows 1265427-1265435 per the 10-08 sweep) and the decision-rung gate
is "beat the embeddings baseline": Jevfree IS that baseline, implemented, with
its failure modes mapped. Zero-cost scut-rung decision floor; the gate's
baseline column now has a reference implementation to beat. Overlap: Jevfree
and johnnys.news grep = 0 rows in catalog.jsonl, 0 in memory. Confidence 0.9.

### 3. Microsoft-Decision-1: the vendor wave arrives (and hands us a quantization law datum)

Primary: https://commandline.microsoft.com/microsoft-decision-1-model-foundry/
(2026-10-09, read end to end); HN thread 50024913 (192-194 pts, 64 comments,
read end to end). Verbatim (blog): "we post trained Qwen3.5-9B for fast,
single-pass decision scoring." Facts: 83.5 percent average accuracy over 36
benchmarks / 147,137 questions vs Jev 1.13.0 at 82.3 (Jev keeps calibration,
93.7 vs 92.2); p50 85 ms, called 2.8x faster than Jev (240 ms) and 35x faster
than GPT-6 Sol (3,010 ms); served via Foundry and OpenRouter at 0.042 USD/M
input (thread-established parity with Jev); not open-weight, not local; plans
to rebase on MAI/OpenAI models. Thread adds: manmal measured "a BF16
(unquantized) Qwen beats a Q8 of double its size for decisions" (4B BF16 beat
8B Q8 in E2E UI-agent tests) - a direct input to the estate's quant and
fingerprint doctrines; Topfi measured it "cheaper (by 0.72x) but higher
latency (283ms vs 369ms p50) than Jev"; astroturf suspicion flagged on one
pro-MS JevBench claim; nejch: the whole field is "based on one of the smaller
Qwen models." Estate bearing: Q1 landscape (the decision rung is now
first-party at MS scale) plus the BF16-vs-Q8 datum for RIB_MODEL_GATES.
Overlap: catalog 0; memory holds only the sibling x_reply_radar tweet-sentiment
row (satyanadella announcement, "Jev not ranked" top reply) - no model-facts
bank. Confidence 0.92.

### 4. Qwen 3:0.6B fine-tuned to categorize questions: 10 to 92 percent, and the classical-ML falsifier

Primary: https://www.teachmecoolstuff.com/viewarticle/fine-tuning-a-local-llm-to-categorize-questions
(published 2026-06-16, updated 06-22; relevance door, outside the 30-day
window, flagged as such); HN thread 48623434 (215 pts, 49 comments, read end
to end). Verbatim (article): "As you can see, prediction accuracy is now at
~92%." Facts: 18-class routing for RAG narrowing; prompting-only 13/131
(about 10 percent); QLoRA fine-tune v1 79 percent; v2 (labels remapped to
two-letter codes) 92 percent; Ollama + Unsloth; about 850 rows, 70/15/15
split. Thread falsifier (Q3's question, answered by others' data): nl argues
an SGDClassifier on 2-grams would land within 1 MB and train in under a
minute; the article's own author (dev-experiments) replies "Using logistic
regression actually improves accuracy, but also performance during both
runtime and during training"; kamranjon measured ModernBERT Large beating
Gemma 1B on binary classification; armcat prescribes embeddings+kNN first,
MLP head second, LLM last. Nobody reports variance, CIs, or a variance
decomposition - the estate's 36.3-vs-3.6 percent routing-variance claim is
neither replicated nor falsified in any outside data found this sitting
(OWED stands). Outside evidence supports the conclusion (a 0.6B local model
routes at 92 percent after a cheap fine-tune) while contesting the family
choice (encoder or classical baselines beat tiny decoders on fixed label
sets). Overlap: teachmecoolstuff grep = 0 catalog rows, 0 memory holdings.
Confidence 0.9.

### 5. FreeLLMAPI: a live map of the free-provider lanes (Q4, starting today)

Primary: https://github.com/tashfeenahmed/freellmapi README (github.com fetch
returned HTTP 504; verified instead via
https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/README.md -
fallback door named honestly); Show HN 49989005 (2026-10-07). Verbatim
(README): "7.4 billion tokens per month. 34 free LLM providers. 635 free model
endpoints. One OpenAI-compatible endpoint." Facts: MIT, self-hosted Node 20+
router; providers named include Google, Groq, Cerebras, OpenCode Zen, Mistral,
OpenRouter, Cloudflare, Cohere, Z.ai, NVIDIA, HuggingFace, ModelScope plus a
custom provider for any OpenAI-compatible endpoint (llama.cpp, LM Studio,
vLLM, Ollama); AES-256-GCM key storage; on 429/5xx it cools the key and
retries the next model in the chain; per-key RPM/RPD/TPM/TPD counters; signed
model catalog self-updates twice daily (free tier gets a 30-day-delayed
monthly snapshot); daily caps reset at UTC midnight; per-model rate limits
live at freellmapi.co/models (not fetched this sitting); "for personal
experimentation and learning, not production." Estate bearing: Q4's map - the
retired ling-3.0-flash-fin rows now have a successor list (Groq, Google,
Cerebras, Z.ai, Mistral, OpenRouter, Cloudflare, NVIDIA, HF, ModelScope
confirmed alive as of 2026-10-07), with retirement/quota drift tracked by the
catalog itself. Overlap: 4 catalog rows, all the 10-03 sweep's raw Algolia
harvest JSONs (p1_freellmapi.json x 2 zones) - listing-level, no content bank;
memory 0. Confidence 0.82 (README-only; site rate-limit tables unverified).

### 6. Kisoku 1.6B: the honest janitor-scale family datum (no displacement)

Primary: https://github.com/0arch-io/kisoku (README read end to end); HN
50025042 (2026-10-09). Verbatim (README): "it matches Meta's Llama 3.2 1B
(five wins each) while using about 18 times less training data." Facts: 1.6B
from scratch by one person on a TPU v4-32 grant, about 0.5T tokens, Llama 3
tokenizer, 64K context; suite wins GSM8K 15.0 vs 5.8, MMLU 34.2 vs 31.3;
losses TriviaQA 23.1 vs 40.7, HumanEval 14.6 vs 18.9; README's own limit
lines: "Qwen2.5 1.5B and SmolLM2 1.7B outperform it on most benchmarks" and
"This is a token-efficiency result on one suite"; Apache 2.0, corpus not
redistributable. Estate bearing: Q1 - no janitor displacement; the 1-2B
reference remains Qwen2.5-1.5B / SmolLM2-1.7B, and the sweep's measured action
stays in decision models (items 1-3), consistent with the 10-08 Q1 verdict.
Overlap: kisoku / 0arch grep = 0 catalog rows, 0 memory holdings. Confidence
0.88.

### 7. Windows ML experimental llama.cpp (delta bank: operational specifics)

Primary: https://devblogs.microsoft.com/foundry-on-windows/build-on-winml-oct-7-26/
(2026-10-07, read end to end). Verbatim: "Windows adds experimental llama.cpp
support to Windows ML so you can run GGUF models locally through new
task-specific APIs." Held core (10-08 reddit lane item 3): the announcement
itself, the Qwen2.5-0.5B example, the fourth-serving-arm framing. Delta
banked here: Windows ML 2.7.2021-experimental NuGet
(Microsoft.Windows.AI.MachineLearning), winml-cli 0.3.1 via pip,
WinMLServer.exe model.gguf runs the OpenAI-compatible local endpoint, a
native Runtime API for ONNX and GGUF across AMD/Intel/NVIDIA/Qualcomm
GPU/NPU/CPU, and the Windows Arm64 stack (pymanager 3.14-arm64, torch
2.14.0+cu134, triton-windows 3.8.0.post29) plus Eagle-3, MTP, D-Flash2
speculative decoding and NVFP4 from the NVIDIA llama.cpp collaboration.
Estate bearing: Q2 - the estate host's own OS now ships a fourth serving arm
(Ollama, llama.cpp-native, vLLM, WinML) with an OpenAI-compatible endpoint;
if the serving-choice A/B ever fires, the arm is installable today with exact
version pins. Experimental-flagged; known-limitations review advised before
production. Overlap: core held at
watch/inbox/frontier_olm_2026-10-08/sweep/open-local-models-reddit.md:118-127;
this bank adds only the install/version specifics. Confidence 0.85.

## Per-research-question verdicts

- Q1 (janitor-scale families beating gemma:2b / gemma4 on measured,
  non-vendor benchmarks): still NO chat-family displacement. Kisoku (honest)
  does not beat the Qwen2.5-1.5B/SmolLM2-1.7B reference; no in-window page
  benchmarks gemma:2b or gemma4 against a named challenger. The band's
  measured action remains decision models: THX-01 (322M, third-party vs Jev)
  and Jevfree (embedding floor) are this sitting's adds; MS-Decision-1 shows
  the category going vendor-mainstream. Instruments-only law: all vendor
  numbers stay UNMEASURED until the estate battery fires.
- Q2 (local-serving stacks mature enough to move work off the funded-remote
  tier): for decision/classification work, yes and compounding: llama.cpp
  /v1/systemone and Ollama 0.35 (held), WinML llama.cpp with exact pins
  (delta above), browser-grade transformers.js+WebGPU (Jevfree). For
  generative work, the held Magnitude thread still says llama.cpp/MLX is the
  floor; nothing new contradicts it.
- Q3 (does the 36.3-vs-3.6 percent routing-variance dominance replicate
  outside): unreplicated and unfalsified - no outside source publishes a
  variance decomposition (the 0.6B thread explicitly lacks CIs; stratified
  5-fold CV was suggested, not run). The conclusion (tiny routers work after
  cheap fine-tunes) replicates at 92 percent; the family choice is contested
  by the logreg/ModernBERT falsifier. OWED: an estate-side replication note.
- Q4 (free-tier provider map today): FreeLLMAPI's live catalog names the
  lanes alive as of 2026-10-07 (Google, Groq, Cerebras, OpenCode Zen,
  Mistral, OpenRouter, Cloudflare, Cohere, Z.ai, NVIDIA, HF, ModelScope);
  retirement and quota drift are tracked by its twice-daily signed catalog;
  seat-hunt cadence should start from that list plus the Laya free hosted API
  (Vercel, listing-level 49926327) and the Clef Workers AI free-adjacent
  lanes already held.

## OWED (stated, not guessed)

- freellmapi.co/models rate-limit tables: not fetched (site not probed).
- Any estate battery run (THX-01 vs gemma:2b, Jevfree baseline wiring,
  WinML arm): NOT RUN by this seat; all vendor numbers above stay
  UNMEASURED under the instruments-only law.
- Variance-decomposition replication for Q3: no outside data found.
- THX-01 phone claim: the substack says phones, the HF card reports GPU
  latencies only; phone-class performance is unverified.

## Receipt

Fetches: 6 Algolia probes (all valid JSON, no 403s), 14+ distinct page reads
(2 HN threads among them), 1 raw-README fallback after a github.com 504, 1
webReader re-fetch after a title-only WebFetch. Local instruments: overlap
greps over catalog/catalog.jsonl (single-pass alternation; freellmapi 4 rows
naming the 10-03 raw JSONs, everything else 0) and over memory/ plus all
frontier_olm_2026-09-30..10-10 sweep dirs (dedupe ledger above). Not run: any
model pull, battery, pytest, or estate gate. No em or en dashes in this file.
