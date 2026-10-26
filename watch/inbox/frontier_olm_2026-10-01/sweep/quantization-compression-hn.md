# Frontier sweep: quantization-compression via Hacker News (2026-10-01)

source-fetched: 2026-10-01

Seat: sweep-quantization-compression-hn (dynamic-workflow gopher). Door: Hacker News via
hn.algolia.com API + the linked primary pages. Every claim below was fetched or run in this
session; verbatim quotes are copied from strip_html extractions of the fetched pages, preserved
in session logs `call_14c4f1e6d8b6418cb728f776-stdout.log` (8 items) and
`call_f9521e9246d54e06bedd513f-stdout.log` (Swift re-fetch).

## Method

- Pass 1 (broad): 17 queries against `https://hn.algolia.com/api/v1/search_by_date?tags=story`
  (quantization, GGUF, llama.cpp, KV cache, AWQ, GPTQ, EXL2, distillation, reasoning model,
  Ollama, on-device LLM, model compression, quantize, speculative decoding, low-bit, 4-bit,
  small language model). Zero query errors. 588 unique hits, **278 candidates in the 30-day
  window 2026-09-01..2026-10-01** (well over the 30-candidate bar). Candidate table:
  `%TEMP%\hn_qz_sweep\pass1.json` + pass1 stdout log.
- Pass 2 (deep): fetched end to end (HN thread JSON via `/api/v1/items/<id>` AND the linked
  article, read in full): 49611128 Quesma, 49735410 zartbot/DSv4.1-Flash, 49869861 arXiv
  2606.00206, 49676635 bartowski per-tensor, 49643543 agentic-kv-cache (thread + full README),
  49523381 burrito-core, 49812339 transformers-llama-cpp-quants, 49727511 Swift-Qwen (corrected
  ID; my first attempt used 49740835 which resolved to an unrelated Ask HN - caught and
  re-fetched, nothing banked from the bad ID).
- Friction: the Mimosa pre-write hook blocked three script drafts (SSRF/path-traversal pattern
  flags). Resolved by hard https-host allowlist, no-redirect opener, and print-only scripts; no
  fallback was fabricated - the final scripts ran clean and their stdout is the evidence.
- Overlap grep run this session: `grep -i` per pattern over `catalog/catalog.jsonl` (0 hits for
  6 of 7 banked items) and `memory/` (hits are either this session's own trajectory tape
  `memory/trajectory/steps.jsonl:40215` or a 2026-09-29 sibling sweep's grep list at
  `memory/trajectory/steps.jsonl:33689` with no landed holding; Swift-Qwen IS partially held,
  see item 3).

## Answers to the four research questions (steal-map)

**Q1+Q2 (formats, Q4-vs-Q8 delta with conditions).** The Quesma benchmark (item 1) is the
cleanest measured answer: on GPQA Diamond, IFBench, and Terminal-Bench 2.1 with named
conditions (llama.cpp build 2026-08-16, F16 KV cache 2.3 GB per 32k tokens, L40S/H100/H200 on
Modal, ~$3,000 spend, Unsloth GGUFs), 17 GB Q4_K_M ties 55 GB BF16; UD-Q2_K_XL drops but stays
"the level of Opus 4.7 or Gemini 3.1 Pro"; 1-bit collapses to random-guessing and xhigh thinking
makes it WORSE. Q8_0 was skipped as unnecessary (interpolated). Thread counterweight: one user's
private coding benchmark is solved by Q6_K_XL and NOT by Q5 - the "4 bits is free" folklore
fails at the edge of a model's capability; and a commenter showed KL-divergence folklore metrics
computed on wikitext are 10x too optimistic vs agentic traces. Bartowski (item 5) supplies the
GGUF-internals ground truth for where bits matter. burrito-core (item 6) quantifies the harness
term the honesty law requires: same weights score ~0% to ~87% depending on template/tool
format/wire API.

**Q3 (KV/context compression).** Two complementary finds. (a) agentic-kv-cache (item 4): a
measured null result - 68,266 replayed requests from 393 real Claude Code sessions, three
mechanisms all lost to radix-leaf LRU; recompute waste is capacity-bound (33.1% of it from
requests <10 s apart with 88k-token working sets), not TTL/liveness-bound; "does Belady beat
LRU" is the harness-validity test. Directly applicable to a local-first harness's prefix-cache
sizing. (b) Frontier: DeepSeek-V4.1-Flash pushes KV to FP4 + cross-layer sharing at ~890 bytes
per token (zartbot read end to end) - NOT re-banked because the estate already holds the
primary tech report (`catalog/catalog.jsonl:444521`, state/arxiv/2026-09-18/2609.19969v1.txt)
plus `watch/inbox/DESK_DSV41FLASH_20260911.md`. Its architecture tricks (YOCO-style CED,
cross-layer KV reuse, SWA-128 + sparse top-512) are weight-native, not portable to off-the-shelf
GGUF janitors; the LRU paper's capacity law is the portable half.

**Q4 (distilling reasoning into small deployables).** arXiv 2606.00206 (item 2): PTQ increases
CoT length; up to 52% of quantized failures had the right answer mid-trace; a training-free
logit penalty on overthinking markers ("wait", "but", "alternatively") cuts CoT 12-23% while
preserving/improving accuracy across 5 models 1.5B-32B, 3 quant methods, 5 benchmarks.
Swift-Qwen3.8-27B (item 3) is the shipped productization of exactly that idea and it is
reproducible WITHOUT datacenter hardware at the deployment end: the artifact is a LoRA adapter
+ 20+ community GGUF quants; the author's HN TLDR names the full recipe (marker-token mining on
OOD traces, penalizer beats the paper's token set, LoRA SFT alone lost accuracy, restored via
RL(GSPO) + on-policy distillation + ThinkingCap adapter transfer) - training used 8xH100, so
recipe-reproducible, not train-reproducible, on a desk. Quantized evals included: W4A16 and
AWQ INT4 rows keep the token savings; AWQ INT4 AIME 82.67% -> 84.00% with the adapter.

## Banked items (strongest first)

### 1. Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses
source-fetched: 2026-10-01 - https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/
(article dated 26 August 2026, Piotr Migdal; HN 2026-09-08, 286 pts / 139 comments)
Quote: "Yet the 17 GB Q4_K_M matches the full model on a popular agentic coding benchmark,
Terminal-Bench 2.1."
Conditions named in the article: F16 KV cache regardless of quant, ~2.3 GB/32k tokens;
llama.cpp build from 16 August 2026; Terminal-Bench 2.1 = 89 tasks, 3h timeout, xhigh effort,
98k context; GPQA Diamond / IFBench one-shot at low/medium/xhigh; ~$3,000 on Modal
(L40S/H100/H200); Unsloth v2/v3 GGUFs (v2 replaced 2026-08-19). 2-bit UD-Q2_K_XL: same turns,
about a quarter more tokens than BF16 on solved TB tasks. 1-bit: random-guessing level, and
xhigh scores below low because reasoning runs out the token budget into empty answers. Author
in-thread: "~$500 per a single combination" to replicate.

### 2. Quantized Reasoning Models Think They Need to Think Longer, but They Do Not
source-fetched: 2026-10-01 - https://arxiv.org/abs/2606.00206 (submitted 29 May 2026; Lotfi,
Kirichenko, Li, Liu; HN 2026-09-27)
Quote: "simply introducing a training-free logit penalty on a curated set of overthinking
markers can reduce CoT length by 12--23% while preserving or improving accuracy across 5 models
(1.5B-32B parameters), 3 quantization methods, and 5 benchmarks"
Abstract also states: aggressive PTQ reduces accuracy while increasing CoT length; in up to 52%
of quantized models' failures the right answer appears in intermediate steps but is not output;
high-KL positions correlate with high next-token entropy and disproportionately sample "wait",
"but", "alternatively"; overthinking errors reduced up to 58%. Thread (1 comment) adds the
caveat that the paper "hyperfocuses on one type of error compensation".

### 3. Swift-Qwen3.8-27B (Show HN)
source-fetched: 2026-10-01 - https://huggingface.co/ukisai/Swift-Qwen3.8-27b (repo created
2026-09-08, modified 2026-09-24; HN 2026-09-16, 33 pts)
Quote: "Swift-Qwen3.8-27B is UkisAI's reasoning-efficient derivative of Qwen3.8-27B, using
58.3% fewer thinking tokens while maintaining near-identical performance"
Measured table with conditions: BF16, vLLM 0.27.1, Qwen3 parser, ctx 262,144, thinking xhigh,
temp 1.0 / top_p 0.95 / top_k 20, 5 seeds. Terminal-Bench 2.1: 66.74% -> 65.84% with mean
thinking tokens 37,086 -> 27,272 (-38.7% median -38.7%/mean 26.5% per table). GPQA-Diamond
88.38% -> 88.28% at -41.0% mean tokens. LiveCodeBench v6 IMPROVES 76.76% -> 81.55%. Quantized
rows: W4A16 GPQA 88.69% -> 88.38%; AWQ INT4 AIME 82.67% -> 84.00%, output-cap failures -31-33%.
Method (author TLDR in thread): extends arXiv 2606.00206 with own mined marker tokens from OOD
coding/language/vision/agentic traces; plain SFT on penalized traces failed; accuracy restored
with RL(GSPO) + On-Policy Distillation + ThinkingCap-Qwen3.6-27B adapter transfer; trained on
an 8xH100 box. License: Swift Open License v1.0, free under US$1M revenue.
Overlap: PARTIALLY HELD - `memory/runs/gapwave/hn_x_fanout/local_serving.md` item 4 and
`memory/runs/gapwave/hn_x_fanout/skill_quantization.md` item 5 already carry the headline and
flagged "quant level unvalidated"; this fetch supplies the missing quantized-eval table.

### 4. LRU is harder to beat than the KV-cache papers suggest
source-fetched: 2026-10-01 - https://github.com/gauravapiscean/agentic-kv-cache
(HN 2026-09-10, 108 pts / 58 comments)
Quote (author, in-thread): "The dominant waste is tight tool loops whose 88k-token working sets
exceed cache capacity, not sessions idling past a TTL."
README (read in full): 68,266 requests from 393 real Claude Code sessions + 23,608 Mooncake
requests replayed through a prefix-cache simulator; Mooncake's published hit-rate curve
reproduced with a published-unresolved +4-6pp offset; p50 inter-request gap 2.1 s, p50 input
88,768 tokens, median duty cycle 13.9%; recompute by gap: <10 s = 33.1%, >5 min = 17.5%;
TTL-300s byte-identical to LRU-leaf in every run; hazard/recompute-cost/coherent-eviction
policies all monotone worse than LRU-leaf (LFU -434% at 20k blocks); Belady losing to LRU =
broken harness signature (unpinned in-flight chain); "make your first test 'does Belady beat
LRU?'". License MIT, pure-stdlib simulator, `make repro`.

### 5. Per-tensor layout maps for GGUF quantization (bartowski)
source-fetched: 2026-10-01 -
https://huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization
(published 2026-09-10; HN 2026-09-12)
Quote: "Q4_K_M ended up having a slightly worse overall KLD, but came in just over 5% smaller,
meaning per bit it was a better model."
Measured: 1000+ quants over ~96 hours of degrade-one (all tensors q8_0, one q2_K) sweeps on
Qwen3.5-0.8B/4B; KLD via `llama-perplexity --kl-divergence` on wikitext-2-raw @512. Findings:
token_embd dominates sensitivity (~8x worst weight tensor at 0.8B, 16x at 4B, mostly recovered
at q4_K); depth is a U shape; attn_v, attn_output, ffn_up, ssm_out are the per-bit standouts;
ffn_gate is never worth extra bits; K-quants never benefit from crushing, IQ quants do; below
~3 bits dense models tie the old heuristic. New _S/_M/_L naming = 90/70/50% named-type body.
Canary test: any map above the KLD-per-bit line is rejected with fallback to the old heuristic
(MiniCPM5-2B failed it in testing and the pipeline fell back). Stated limit: KLD run on
wikitext only - cross-reference the Quesma thread's finding that wikitext KLD understates
agentic-trace divergence.

### 6. burrito-core: fixing GPT-OSS (320,192 runs, 1,062 GPU hours, 1x RTX 3090)
source-fetched: 2026-10-01 - https://github.com/iamskeole/burrito-core (HN 2026-09-01)
Quote: "Configuration matters more than model capability. The same weights score from ~0% to
~87% depending on template, tool format, wire API, and effort level."
burrito-evals ran gpt-oss-20b across 320,192 runs / 3.49B tokens / batch size 1 / 8 seeds on a
single 3090 over Big Function Calling Leaderboard + AIME25 + GPQA, 7 backend configs; full
report, 44 figures, per-run dataset and traces shipped. Specifics: default jinja template
breaks the model (live-test ~3% -> ~40% when fixed); on vLLM /v1/responses errors on 73.5-83.5%
of multi-turn runs vs 29.0-36.0% on /v1/chat/completions; structured tool schemas triple
multi-turn accuracy over AST parsing; at a fixed ~1.4k reasoning-token budget AIME25 =
38/97/100% for low/medium/high effort, and more tokens past an effort level's optimal zone
DEGRADE accuracy.

### 7. Transformers now runs llama.cpp quants
source-fetched: 2026-10-01 - https://huggingface.co/blog/transformers-llama-cpp-quants
(published 2026-09-22)
Quote: "More aggressive quantization can help larger models fit, but the quality tradeoff
depends on the model and the task. Evaluate it on the work you actually want the model to do."
transformers loads GGUF via `from_pretrained(gguf_file=...)`, reusing ggml Metal kernels
(ggml-quantization, ggml-norm, ggml-attn, ggml-gated-delta-net + own topk) through the kernels
library; packed path is MPS-only, Qwen3.5 dense/MoE + compatible Qwen3.8 first. Size table for
Unsloth Qwen3.5-4B: BF16 8.42 GB / Q6_K 3.53 / Q5_K_M 3.14 / Q4_K_M 2.74; "starting with
Q4_K_M" is the official suggestion. Benchmark honesty note: llama-bench tg128 decode-only vs
transformers including prefill, M2 Max 32 GB, 90 s cooldown because "back-to-back runs decay by
10% or more". Estate nerve: the window-1 carrier commit (b2ca54422, 2026-10-01) records C1
re-deriving "the Ollama/transformers fork" by hand because the skill bytes were not in
evidence - this blog is the upstream primary for exactly that interop surface.

## Read but NOT banked (duplicate of holdings)

- zartbot, "DeepSeek-V4.1 Flash: Pushing the Limits of KV Cache Compression" (HN 2026-09-17,
  131 pts; article read end to end): FP4 KV + channel/sequence/layer cross-sharing, ~890 bytes
  per token global KV, runtime KV 1/4 and persistent KV 1/8 of DSv4-Flash at equal sequence
  length. Already held as PRIMARY: `catalog/catalog.jsonl:444521` ->
  `state/arxiv/2026-09-18/2609.19969v1.txt` + `watch/inbox/DESK_DSV41FLASH_20260911.md`
  (catalog rows 448561/691046). Re-banking the interpretation adds no bytes the estate lacks.

## Caveats (honesty law)

- All quotes are verbatim from my own strip_html extractions (session logs cited at top);
  HTML stripping can shift whitespace but not wording.
- The Algolia search window is data-derived: newest hit 2026-10-01, cutoff 2026-09-01; zero
  query errors; 278 in-window candidates considered.
- One pass-2 ID error (49740835) was caught because the fetched thread title did not match the
  pass-1 row; corrected to 49727511 and re-fetched. Nothing was banked from the bad fetch.
- Not run: no local benchmarks; this is a public-source sweep only. Terminal-Bench/GPQA numbers
  above are the authors' reported conditions, not our measurements.
