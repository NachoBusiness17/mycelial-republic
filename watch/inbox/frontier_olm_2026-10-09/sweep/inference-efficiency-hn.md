# SWEEP: inference-efficiency via hn (frontier OLM 2026-10-09)

source-fetched: 2026-10-09. Gopher seat: sweep-inference-efficiency-hn (dynamic workflow child,
branch mag/run-beta1-factory-build-audi-20260806T231709Z). Door: hn.algolia.com (search_by_date
and search variants, tags=story, numericFilters created_at_i>1788912000 = since 2026-09-09),
per the fetch recipe. No 403s on the Algolia door all session.

## Method (two passes, this session)

Pass 1 (broad): 8 Algolia queries (speculative decoding; vLLM; continuous batching; LLM
inference; llama.cpp; inference GPU throughput; SGLang; KV cache; tokens per second; Ollama),
hitsPerPage 30, 30-day numeric filter. 60+ raw hits surfaced; 45 distinct in-window candidates
considered, including: Magnitude Launch HN 49911995 (194 pts), Mercury 2.5 49823348 (151 pts),
DeepSeek v4.1 Flash KV compression 49735410 (131 pts), LRU-vs-KV-papers 49643543 (108 pts),
prompt-lookup drafting 49859982 (89 pts), Sub-1-Bit LittleBit 50005608 (87 pts), Ollaya
49848269 (618 pts), getunblocked AIMD routing 49897322, Mozilla local-server bench 49742415,
SGLang prefill 49856359, Reflex TTFT 49903234, Intel Arc 2.2x 49876817, MoE multiGPU fork
49845314, InstinctFlash 49802789, KV memory wall 49945575, Fathom 49893944, prefix-cache-warm
49758259, cache-hit-truth 49699918, token-compression CLI 49911910, echohive 1M tok/s 49941327,
solo-dev moat 49951356, decision models 49906337, and the fresh tail: Narwhal 50019698,
Rai 49936094, Phobos 50005280, level1techs DSV4.1 Flash 49760482, ALHR 50020238,
Self-Pruning Transformer 50013834.

Pass 2 (deep): 9 sources read end to end via WebFetch: HN thread 49911995; the prompt-lookup
blog (jadidbourbaki.github.io); artificialanalysis.ai/models/mercury-2-5; HN thread 49643543;
getunblocked.com AIMD routing post; blog.mozilla.ai local-server benchmark; the Narwhal README;
the DeepSeek v4.1 Flash arch post (zartbot.github.io); the Rai README; the Phobos post
(joa-ebert.com); ollaya.dev; the level1techs forum thread. (12 fetches total.)

## The anti-rebank finding that shaped this bank

Before banking, git grep over the tracked tree plus the sibling sweep dirs for every candidate:
the estate's own OLM run has mined this exact door daily since 2026-09-30, and days 0-5 already
BANKED the heavyweights with receipts: Magnitude (10-01 sweep item 8, thread numbers included),
prompt-lookup 42x (10-01 kv-cache sweep item 7), Mozilla bench (10-01 sweep, plus
memory/runs/gapwave/hn_x_fanout/local_serving.md:22), getunblocked AIMD routing (10-04 sweep
item 1, READ FULL TEXT, overlap receipt "catalog 0, memory 0 ... NEW" at :24; re-held 10-05
:94-109), OpenRouter pitfalls 49621546 (10-04 item 2), LRU-vs-papers (09-30 kv sweep + DIGEST +
register + steal, and the estate already built tools/lru_null_arm.py from it), DeepSeek v4.1
Flash arch (09-30 kv steal), SGLang prefill (10-01 + 10-05), KV memory wall (10-03), LittleBit
(10-08 inference-efficiency-hn sweep + watch/inbox/LINK_DROP_LITTLEBIT_20261008.md), Mercury
2.5 (10-01 sweep:57 explicitly held unbanked as marginal), claude-terse and the Tom's Hardware
H200 story (10-08 steal card). Per the anti-rebank law, none of those are re-banked here.
Today's kv-cache sibling sweep independently confirms at :41 that it left Magnitude, 49945575,
LittleBit, and 50013834 unfetched, so no same-day double-bank either. What remains genuinely
new is below; the mid-tier local-rung posts (Intel Arc 2.2x, MoE fork, Reflex, InstinctFlash,
token-compression CLI, Ollama decision models, Fathom, prefix-cache-warm) are all held in
day 0-3 sweeps, dropped.

## Banked items (strongest first, all read by this seat)

### 1. Ollaya, 618 pts, 2026-09-25 (HN 49848269) - local decision-model runtime; first bank of a raw-held item
https://ollaya.dev/ (page raw-held day-4 as intake row _ihn_page_49848269_ollaya.txt in
catalog/catalog.jsonl, never banked as a finding by any sweep; the 10-09 open-local sibling
sweep:20 lists it only in its pass-1 pool).
Quote: "Ask typed questions about any text or JSON and get calibrated answers in milliseconds.
Private, open source, on your own hardware."
Measured: Apache-2.0 Ollama-like runtime for decision models (typed single-forward-pass
classification, no decode loop); ~19 model families (winnow Gemma-based, laya, decider
Qwen3.5-based, kev, nli, gliclass, qwen3guard, jeb); CPU everywhere, CUDA/Vulkan/MLX. Bench vs
Ollama 0.35 on RTX 5090 over 3,880 questions: winnow:12b 0.773 accuracy at 160 ms/question vs
Ollama Nimble 0.749 at 210 ms; calibration error ECE 0.022 vs 0.122 (5.5x lower); winnow:e4b
five questions in ~89 ms on RTX 4090 at 0.722 vs TypeSafe hosted Jev 0.738 at 236-276 ms.
Estate map (RQ1): this is the strongest ladder-down move found today, because it is not a
smaller LLM, it is no decode loop at all: the classifier-guard class the Q4 wiring gap needs
(day-8 lens/laws.md:154-158 six unwired fire surfaces; mag/inference_budget.py:268 plan_call,
:349 guard_terminal) can run as a local calibrated decision model instead of hand-rolled
params. Direct tension to carry: the day-8 arxiv sweep item 3 (arxiv 2610.02267) measured this
exact model class and found reported savings shrink under audit ("reported 23.9% saving,
actual 4.3%"), so wire one carrier, audit it charged, then scale. The ECE 5.5x calibration
delta is the number that makes the classifier trustworthy enough to gate on.
Overlap: raw-held day-4 (intake row only); no sweep or steal ever carried its numbers; git
grep "Ollaya"/"49848269" otherwise 0 in tracked tree. NEW as a finding.

### 2. Production self-host of DeepSeek v4.1 Flash on 4x RTX6000 Pro Max-Q (HN 49760482, 2026-09-18)
https://forum.level1techs.com/t/llm-inference-workstation-4x-rtx6000-blackwell-pro-max-q-384gb-vram-threadripper-pro-7985wx-wrx90e-sage-se-512gb-ram-1700w/252181
Quote: "Per-request decode averaged 102.0 tok/s, batch generation 191.9 tok/s, prefill
5,955 tok/s" (rendered fetch digest of the thread's table; confidence capped accordingly).
Measured: real production traffic on a ~$54K Threadripper/4x-96GB box, sglang, TP4, MXFP4 MoE:
per-request decode 48.8 to 102.0 tok/s (the 2.1x claim), batch 137.4 to 191.9, prefill 2,444
to 5,955; gains from TP4/EP4 expert parallelism, DSPARK speculative decoding (block size 5,
acceptance length 3.71, rate 0.542), and a 256 GB RAM HiCache. The honest tax row: cache hit
rate fell 96.58% to 78.64% on the change, tuned back to ~97.8% combined L1+L2, while queue and
TTFT p95 worsened and 1,470 allocator OOM warnings appeared; context limit dropped 1M to 524K.
Estate map (RQ1 + RQ2): this is the counterweight measurement to day-8's banked Tom's Hardware
verdict (self-host at $13,200/month lost to DeepSeek's list price at that firm's volume): here
self-host WORKS at 102 tok/s per request, but the receipt shows the cost moved into the cache
(hit-rate drop) and the tail latency, exactly the two axes the estate's prefix-cache law and
day-4's AIMD bank say are where serving money actually lives. The DSPARK acceptance-rate row
(0.542, 3.71 tokens) is the first production spec-decode acceptance datum in estate holdings
and the instrument shape for the local-rung spec-decode re-measure.
Overlap: git grep "49760482" 0 hits estate-wide. NEW. Converges with, does not duplicate, the
10-08 steal card's find 1 (different story, different numbers, same verdict axis).

### 3. Phobos: JIT kernel language runs LLMs on a 2019 GPU (HN 50005280, posted 2026-10-08)
https://www.joa-ebert.com/posts/2026-10-06-phobos-inference/
Quote: "On my old RTX 2080 SUPER it generates text as fast as llama.cpp or faster on every
model I tried but two: 324 against 247 tokens a second on a 0.8B model"
Measured: no cuBLAS/CUTLASS/CUDA toolkit, driver only, Phobos to MLIR to PTX at runtime;
int8 dp4a, CUDA graph replay, fused dot product, slab allocator; Qwen3.5-0.8B Q8_0 324 vs 247
t/s; Qwen3.8-27B IQ1_M 43% faster decode; Qwen3.6-35B-A3B MoE 54.3 vs 29.9 t/s with experts
streamed via a GPU cache plus CPU-computed misses, keeping ~75% of decode speed when 2 GiB is
taken mid-session where llama.cpp keeps 30%. Weak spot named by the author: prompt processing
on small models still 60-80% of llama.cpp.
Estate map (RQ1): the local janitor rung has kernel-level headroom independent of llama.cpp,
and the MoE expert-cache retention number (75% vs 30% under memory pressure) is the directly
stealable mechanism for the estate's consumer-GPU janitors when VRAM is contended: keep the
hot expert set resident, stream the tail. Also a fresh existence proof that the llama.cpp
mono-stack is not the ceiling on old hardware.
Overlap: git grep "50005280"/"Phobos" 0 relevant hits. NEW.

### 4. Mercury 2.5 instrument delta: three estate instruments now disagree on its speed (HN 49823348, 2026-09-23)
https://artificialanalysis.ai/models/mercury-2-5 (title verbatim from the Algolia payload:
"Mercury 2.5 LLM hits 770 tokens per second")
Quote: "Mercury 2.5 LLM hits 770 tokens per second"
Measured today: the page render reads 719.7 output tok/s, rank 2 of 182, $0.25/$0.75 per M,
90% cache discount, Intelligence Index 12 (median 13, rank 97), 260k context, 35M output
tokens per 100M median. The estate's three reads: the watch line clocks 1107 tok/s on
OpenRouter (memory/runs/quote_audit_wide_20260925/inbox_concat.txt), day-1's read of the same
page got 591.2 tok/s (10-01 sweep:57), today 719.7. Same URL, three numbers, plus the HN
title's 770.
Estate map (RQ2): the serving-stack board is a rolling instrument, not a constant; per the
census denominator law (B2-216) generalized to benchmark boards, a tok/s claim without its
instrument moment is not bankable. Useful as the canonical example when the burns ledger or
driving-ladder rows cite provider speed: stamp moment and door or do not cite. Fast-cheap-dumb
verdict from day-1 stands (Intelligence 12, below median): it is a workhorse-tier speed
option, not a judgment-tier candidate.
Overlap: held day-1 sweep:57 (explicitly unbanked as marginal) + endpoint_news + watch line.
This is an instrument-delta bank, not a re-bank: the new fact is the disagreement itself.

### 5. Rai: CPU-only Rust LLM inference, no GGML (HN 49936094, 2026-10-02)
https://github.com/Classevelabs/rai
Quote: "no GPU, no CUDA, no Python runtime, no PyTorch, no GGML, no BLAS" (verbatim fragment
of the README's opening sentence)
Measured: hand-written AVX2/FMA/F16C kernels, 4-bit uniform weights with per-group f16 scale,
.raimodel single-file format, HTTP chat + REST/MCP server for agentic backends. 4-core laptop:
TinyLlama-1.1B 21.8 tok/s decode in 629 MB RSS, Zephyr-7B 2.96 tok/s, ~5.1x HF fp32 in 1/7
the memory, decode at ~45% of the machine's 26.4 GB/s bandwidth ceiling. Honest caveats in
the README itself: RTN 4-bit raises wikitext-2 perplexity 13-30% vs fp16, and llama.cpp
Q4_K_M loses 3-8x less quality; ARM path scalar and unmeasured.
Estate map (RQ1): a documented CPU baseline and, more usefully, a self-auditing README: the
author ships his own quantization-quality loss next to the speed claim. The estate's model
grid census (UNMEASURED cells, LENS 2) can steal the audit shape: every speed row carries its
perplexity tax row or it does not land.
Overlap: git grep "49936094" 0 hits. NEW.

### 6. Narwhal: GPUs move between prefill and decode roles in seconds (HN 50019698, posted 2026-10-09)
https://github.com/athrael-soju/Narwhal
Quote: "The installed template starts two engines on an NVIDIA GPU with 8 GB of VRAM or less.
The RTX 5090 reference template starts four engines on an RTX 5090"
Measured: adaptive disaggregated serving; a role controller scores the current prefill/decode
split and each one-move-adjacent split by worst projected SLO ratio across TTFT, TPOT, and
decode queueing, with improvement-margin guards, cooldowns, and an arrival-evidence window;
KV state transfers via NIXL; builds on the Arrow scheduling paper (arXiv:2505.11916). Honest
limit: the README carries NO latency or throughput numbers; it links an external evaluation
blog not fetched this session.
Estate map (RQ1/RQ2): the role-split controller is the serving-stack formalization of the
estate's own lane-shape intuition (batch work and interactive work should not share a
configured engine); the estate's ds_workhorse hollow-batch lane already separates these at
the process level. Low traction (1-2 pts) and no published numbers in the README: bank the
mechanism, not a benchmark. Follow-up OWED: fetch the linked evaluation blog before citing
any Narwhal number.
Overlap: git grep "athrael-soju"/"50019698" 0 hits. NEW.

## Answers to the four research questions (each traceable to items above and to estate files read this session)

RQ1 (spec-decode / continuous batching shifting work down the ladder without violating the
inference-budget terminal rule): the ladder-down moves since 10-01 are (a) decision models,
which remove the decode loop entirely for the classifier-guard class (item 1: local calibrated
typed classification at 89-160 ms; Ollama 0.35 already supports the genus per the day-0/1
sweeps); (b) production spec-decode on self-host with acceptance-rate observability (item 2:
DSPARK 0.542 acceptance, 3.71 tokens); (c) kernel headroom that keeps the local rung competitive
on old GPUs (item 3, plus the day-1-banked prompt-lookup 42x which erased drafting cost, the
main historical tax on local spec-decode); (d) CPU-only baselines (item 5). None touch the
terminal rule: mag/inference_budget.py guard_terminal (:349) and plan_call (:268) govern
per-ask budget semantics, and items 1-6 are serving-mechanics, not budget-policy, changes. The
one caution is the day-8 arxiv audit finding (2610.02267: claimed 23.9% guard saving, actual
4.3%): any classifier-gate adoption must charge its own token and error cost or it violates
the estate's trust-bytes-not-reports law while claiming ladder-down savings.

RQ2 (frontier serving-stack benchmarks vs estate free-lane row counts): they do not reconcile,
and should not be forced to. The digest-commit rows (openrouter 469 adds, groq 11, mistral 46,
verified this session via git show f80961cd9 --stat and the full message) count ROSTER BREADTH;
the frontier serving benchmarks price per-token latency on dedicated hardware (item 2: 102
tok/s per-request on a $54K box; item 4: 719.7 tok/s on a rolling vendor board). The estate's
envelope economics are rate-window economics: day-4's banked AIMD design showed measured cost
moves with cache state and provider health (cost 14% below round-robin, median task time -55%,
warm-cache ranking distortion), and day-5's sweep:108 records the estate's 109.4M tok/h as
estate-original with no published numeric rolling-throughput cap found. The reconciliation law
shape already in the ledger stands: serving-stack tok/s numbers are hardware prices; free-lane
row counts are rate-limit-window prices; only the estate's own per-door probes (burns probe 3
class) can convert between them.

RQ3 (which of the day-8 mine's 32 unbanked sweeps carry inference-efficiency claims that
descent leg 3 should re-measure first at funded tier): the day-8 mine's sweep files are on
disk (8 categories x 4 doors; watch/inbox/frontier_olm_2026-10-08/sweep/, 32 sweep files plus
scratch). I read its inference-efficiency-arxiv.md in full this session; its banked claims
that are one-GET-verifiable and estate-portable, ranked for leg 3 (one landed deliverable per
premium turn): (1) AgentLoop slot-closed execution guard, arxiv 2609.33315, "total token cost
reduced by up to 88.44% and average service invocations reduced by up to 76.85% against
baselines" (day-8 sweep:126-138) - re-measure by wiring ONE of the six unwired fire surfaces
through plan_call with the slot-completeness check and diffing token rows; the deliverable is
a landed carrier, exactly leg 3's shape; (2) SELF-POT replay, arxiv 2610.01110 (day-8
sweep:47-61) - replay selection rules over already-logged candidate pools instead of refiring
paid lanes, near-$0 re-measure; (3) the fast-gate audit discipline, arxiv 2610.02267 (day-8
sweep:63-78) - not a re-measure itself but the audit harness for (1). The SoT claim (582-param
controller, 62.6% token cut, day-8 sweep:140-155) is fourth: interesting, but it needs a new
artifact before it can be measured, so it fails the one-landed-deliverable-per-turn test
today. Note the day-8 steal card already extracted the ledger-probe legs (hermes_burn 80.5%
prompt share); legs A/B there are still OWED, not duplicates of the above.

RQ4 (is inference efficiency zero-coverage like biology/web3): no. The library shelf holds
serving-stack canon: corpus/library/lmcache-src is 2,331 rows (lens/corpus.md:20, counted this
window by the lens seat), docs/ref/VAST_DEEP_GROK_THROUGHPUT.md is cataloged (catalog row id
8c580bafa6e1), and my substring greps of catalog/catalog.jsonl this session read 475 rows for
"inference", 157 for "vllm", 57 for "speculative", 21 for "batching". The genuinely zero rows
remain biology/biotech/drug/web3 (lens/corpus.md:31). What the shelf does NOT hold is today's
production measurements (DSPARK acceptance rates, decision-model ECE comparisons, expert-cache
retention under pressure), which is what this sweep banks.

## Door health and degraded instruments

- hn.algolia.com search_by_date and search: green all session, no 403, no fallback needed.
- github.com WebFetch: worked for Narwhal and Rai READMEs; 404 on
  bmartin-systems/cortex-serving-arena-preview (HN 49711702, the "191k tok/s continuous
  batching on 1 vCPU" Rust scheduler, 2 pts): the repo URL is dead or renamed. DEGRADED, so
  that candidate is NOT banked and no claim is made about its content. The thread had 0
  comments, so the HN side carries nothing either.
- news.ycombinator.com HTML threads: fetched clean for 49911995 and 49643543.
- level1techs forum: fetched clean, but the render is a digest of a table-heavy page; item 2's
  quote confidence is capped at 0.7 accordingly.
- artificialanalysis.ai: fetched clean; board values are rolling, so item 4 carries the
  instrument-moment framing.

## OWED (named, not done here)

- Fetch Narwhal's linked evaluation blog before any Narwhal number is cited (this seat read
  only the README; it publishes no numbers).
- The day-8 steal card's ledger legs A (formal per-family prompt-share cut) and B
  (self-host breakeven) remain OWED; item 2 gives leg B a second external anchor curve.
- The leg-3 re-measure itself (AgentLoop guard on one carrier) is estate instrument work; no
  sweep substitutes for firing it.
- catalog.jsonl carries an intake row for the raw Ollaya page; if the operator wants the
  raw-held-vs-banked distinction machine-checkable, the register should carry a "raw-held"
  flag, which today only the sweeps' prose records.
