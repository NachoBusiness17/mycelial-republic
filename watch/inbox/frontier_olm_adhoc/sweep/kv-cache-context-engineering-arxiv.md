# Frontier sweep: kv-cache-context-engineering via arXiv (2026-10-11, adhoc seat)

source-fetched: adhoc · swept 2026-10-11 · seat: sweep-kv-cache-context-engineering-arxiv (run dwfrun-e68f99eb).
Supersedes the 2026-10-10 mint of this path (preserved verbatim as
kv-cache-context-engineering-arxiv.prior-2026-10-10.md, cp this sitting). The
daily twin frontier_olm_2026-10-11/sweep/kv-cache-context-engineering-arxiv.md ran
this same area hours before this seat; its bank (KVTether, CLM, P-VMI, Vosti,
ATTUNER, Correct-Now) and its 10-06..10-10 exclusion list were read in full this
sitting and nothing in them is re-banked here.

## Door status (instruments, honest)

- WebFetch on `export.arxiv.org/api/query` TIMED OUT (60s) on the first call; the
  door was then driven serially with curl (same door, different client): 7 API
  queries total, all clean, zero 429 (2s sleeps between). Queries: (1)
  all:"KV cache" AND all:agentic (30), (2) all:"KV cache" AND refusal/safety (25),
  (3) "context compaction"/"context compression" (30), (4) prefix cach/cache-aware
  (25), (5) "context engineering" (20), (6) id_list batch of 12 unclaimed
  candidates, (7) id_list for the two abstract-level reads.
- Full-text: `arxiv.org/html/` served 5 of 6 papers clean (252-719 KB each).
  2606.09864 has NO HTML rendering on arxiv (7.9 KB "No HTML" stub) and ar5iv
  returned a 6 KB stub too; it was read at abs-page depth via the API (full
  abstract + authors + dates). Flagged per-item; not claimed as an end-to-end read.
- No fabrication: every quote below was copied from bytes fetched this sitting.

## Pass 1 census (30+ candidates, last 30 days 2026-09-11..2026-10-11)

~100 API entries inspected across queries 1-5. In-window candidate pool after
dedup: ~45 items. Named and DROPPED as already-held (catalog grep, zero-hit
verification for the kept set): ReFold 2610.07863, Request-Order-Matters
2610.05833, CADOC 2609.37012, KVSET 2609.27746, RR-Evict 2609.32278, Fancy
Eviction 2609.28870, KV-provenance 2609.38706, Agent-Controlled-Forgetting
2610.10590, MCPacific 2610.05319 (all banked by the 10-10 adhoc prior); plus the
daily twins' set: KVTether 2609.39819, CLM 2609.37725, P-VMI 2610.09027, Vosti
2609.38981, ATTUNER 2609.36722, Correct-Now 2609.20045, REMORY 2610.11287,
FOCUS 2609.37590, Beyond-Token-Savings 2609.32961, HEAR 2610.06597,
Persistent-Context-Graphs 2609.40118, ICLR-forgetting 2609.29875, RaReCache
2610.11358, Lachesis 2610.08378, Persistent-Memory 2610.07782, Exact-Memory-Time
2610.02766, Optimization-Landscape 2610.05885, AttSVD 2610.06927, Tessera
2609.32259, EfficientAgent 2609.32999, TempoKV 2609.35065, RelaxKV 2609.33503,
Suffix-Replay 2609.33477, KVCMAS 2609.34060, SPIN 2610.09025, Who-Pays
2609.24991 (the 10-11 daily's exclusion list, read this sitting).

## Overlap method (run this sitting, per ask + burns lens law 5.3)

- catalog grep `grep -c -i -E "Alignment Collapse Under KV Cache|Compression-Aware
  Abstention|Refusal-Gated Decoding|AnchorKV|Tool Waiting and Re-arrival|
  Receiver-Conditioned Latent|SSD-based Sparse KV|CacheRepair"` over
  catalog/catalog.jsonl (1,136,889 rows) = 0 hits.
- memory grep (memory/frontier/, memory/research_polished/, memory/lenses/,
  memory/rib/) for the same 8 names = 0 hits.
- Both prior sweep files at this path + the 10-10/10-11 daily sweeps: 0 hits for
  all 8 arxiv ids (grep run this sitting).
- Conclusion: all 8 banked items are genuinely new to the estate.

## Research questions, answered from this sitting's reads and runs

**RQ1 (do the polished compaction claims' provenance chains hold under the
citation-lint bar?).** RUN this sitting:
`.venv/Scripts/python.exe tools/citation_lint.py check --files
memory/research_polished/kv_cache_compaction.md` ->
`CITATION-LINT: ok records=1 anchors=2 numbers-checked=0 blocking=0 warns=0
enforce-tokens=False`. The deterministic bar HOLDS. Both anchors byte-verified by
Read this sitting: models/providers.py:558-570 (DeepSeek top-level
prompt_cache_hit_tokens + OpenAI-compat prompt_tokens_details.cached_tokens
capture feeding record_usage with cache_hit/cache_miss) and models/providers.py:847-868
(the second API-style capture site, same ch/cm fields). numbers-checked=0 notes the
phantom-number pass found nothing to check in this record. Still OWED (unchanged
from laws lens + daily twin Q1): the re-MEASUREMENT of the 98 pct / $3.60 /
6.5-to-98-pct claims with named conditions (instrument+exit, moment, assumptions);
the lint proves the citations point at real bytes, not that the numbers still hold.

**RQ2 (fire the reach-ratio probe on a live seat tape).** PARTIALLY FIRED, ratio
NOT computable today, no number invented. The fold's probe (corpus/steal/
CORPUS_FOLD_FRONTIER_OLM_20261001.md:18) names the tape: memory/agent_sessions/
desk-deepseek.json. Measured this sitting (venv python, json load): tape exists,
26 messages (1 system / 1 user / 13 assistant / 11 tool), 22,426 transcript
bytes, updated 2026-08-05. The emit-side instrument is ABSENT: the tape carries
no emitted-prompt record (message keys are content+role only) and
logs/provider_usage.jsonl has ZERO rows referencing this session (grep count 0).
The probe's other leg (sha256-frozen per-session emit, fold:11 steal) is not
built. Verdict: the 96.6-pct-class catch cannot recur-invisible once the emit
freeze lands in mag/context_pack.py (MODE_CONFIG :62-90, frozen-prefix emit
:505-526 per fold:11); until then today's reach number is UNKNOWABLE from
existing bytes. OWED: wire the emit freeze, then ratio = transcript-contained
bytes / emitted bytes on this exact tape.

**RQ3 (does RR-Evict round-robin tail eviction beat freeze-the-prefix on real
tool-call-heavy sessions?).** RR-Evict itself is banked (10-10 prior, item 1);
no estate A/B was run this sitting (no local fleet experiment fired; the
$161-to-$3.60 freeze discipline stays the measured champion at laws.md:51 /
RIB_SELF_MY_EFFICIENCY.md). NEW frontier support this sitting: Tool Waiting and
Re-arrival (item 3 below) measures the actual mechanism on a REAL tool-call
distribution (TraceLab, 743,819 tool calls) and shows the honest instrumentation
trap (prefix_cache_hits_total false positives) plus the capacity-vs-policy split
(more KV slots beat clever eviction where reuse loss dominates; near-zero gain
where reuse already holds). That is the correct frame for judging RR-Evict
against freeze-the-prefix: both are policies on top of capacity and byte-stability,
and the estate's frozen prefix mostly removes the eviction question rather than
answering it.

**RQ4 (does the refusal regime-dependence extend beyond keyword-refusal to the
estate's own quant + compaction configs?).** YES in the literature, and the
answer lives in the 2-to-4-month band, not the last 30 days: zero in-window
papers extend the 2609.31678 keyword-refusal finding (all five queries + the two
twins' banks agree). The direct citations: Alignment Collapse Under KV Cache
Quantization (item 1, the quant-config answer: 11 models, refusal loss up to
15.2 pct at 1.03x perplexity, no universal safe bit-width, production FP8
confirmed) and Compression-Aware Abstention (item 2, the compaction-config
answer: compression that evicts answer evidence turns refusal into hallucination
unless abstention is trained). AnchorKV (item 7) is the compression-side
mitigation; Refusal-Gated Decoding (item 8) extends regime-dependence to the
sampling-temperature axis. For the janitor fleet the actionable: per-animal
refusal batteries at the SERVED quant (the fold's 40-prompt battery, fold:17),
because 2606.09864's phase transitions are model-specific and invisible to
perplexity.

## Banked items (8, strongest first; quotes verbatim from fetched pages)

### 1. Alignment Collapse Under KV Cache Quantization: Diagnosis and Mitigation
arXiv 2606.09864 (v1 2026-06-01, v3 updated 2026-08-08) · Xu, Kumarappan, Zhou ·
abs-page depth (no HTML rendering exists; flagged above)

The RQ4 quant-side answer. Eleven instruction-tuned models 3.8B-72B, five
benchmarks, 1,894 prompts. "low-bit quantization can silently destroy safety
alignment: Mistral-7B loses 15.2% of its refusals at only 1.03x perplexity, and
no universal safe bit-width exists, with sharp model-specific phase transitions
invisible to standard metrics." Root cause geometric (safety features in a
low-dimensional subspace 10^2-10^3x more vulnerable); Per-Channel Reduction
diagnostic classifies three failure modes, predicts mitigation direction on 9/9
primary + 1 held-out model with 20 calibration prompts, KIVI recovery up to
97.2 pct, ~35 GPU-minutes training-free. Confirmed in production vLLM FP8.
Estate fit: the janitor fleet runs quantized (gemma:2b scut, qwen janitors);
this says refusal must be re-measured per animal per quant, never inherited.

### 2. Compression-Aware Abstention: Teaching LLMs to Refuse When KV-Compression
Masks Remove Answer Evidence
arXiv 2608.29934 (2026-08-30) · Khodabandehlou, Krishnamachari (USC) · READ END
TO END (arxiv.org/html)

The RQ4 compaction-side answer: first work to train refusal conditioned on
evidence survival under compression. "A 10.1M-parameter LoRA adapter trained on
~2.6K MuSiQue 2-hop QA examples reduces base-model hallucinations by 97% under
prompt-style truncation while preserving correct answering on evidence-retaining
examples." Deployment-honest: under actual compressed-cache decoding the unaided
base nearly collapses on evidence-retaining examples (4 pct -> 25 pct aggregate,
1.4 -> 32 pct at high retention with multi-compressor training, 6-22x lift);
prompt-only abstention over-abstains on ~half of answerable high-retention
examples vs 6-10 pct for the trained adapter. Tight spans (median 3 tokens) are
the load-bearing label design; paragraph-level labels wash out (label entropy
0.000 vs 0.95). Qwen2.5-7B-Instruct main + Llama-3.1-8B held-out, single H100,
code released (github.com/mali-kh/compression-aware-abstention). Estate fit: the
compaction governor design (kv_cache_compaction.md next-action 3) gets its
refusal arm: compaction decisions need an abstain option scored like any other
typed decision.

### 3. Tool Waiting and Re-arrival in Compile-Time-Static LLM Serving: Cost
Mechanisms and Configuration Selection
arXiv 2609.34663 (2026-09-28) · Jang, Wang, Jeong (Dongguk Univ.) · READ END TO
END (arxiv.org/html)

The tool-call-heavy-session measurement RQ3 asks for, on a REAL tool latency
distribution: TraceLab v0.0.2, "743,819 tool calls in 8,058 sessions" from 52
Claude Code / Codex users (Sept 2025 - July 2026). Three mechanisms by which
re-arrival costs execution: discrete batch alignment, KV cache survival, prefill
interference. Instrumentation honesty find the estate's telemetry lane should
steal verbatim: "prefix_cache_hits_total was excluded because it was found to
report false positives, reporting hits even after the corresponding KV slot had
been evicted" (they used prompt_tokens_cached_total instead). Numbers with
conditions: Rebellions CA25 NPU, vLLM 0.22 + vllm-rbln, Qwen3-4B bf16, FIFO KV
slots; at concurrency 8 with 9/24 re-arrivals reused, batch_size enlargement
alone cut execution cost 8.25 pct, selected config 9.72 pct; where 17/18 already
reused, 0.59 pct. Padding ratio and cost can move opposite (0.235->0.120 padding
yet 1.51x decode time). 2,077 configurations explored via validated simulator.
Estate fit: the fixed-slot substrate is the janitor fleet's shape (bounded KV on
consumer hardware); capacity diagnosis before policy cleverness.

### 4. Efficient Agentic LLM Serving over SSD-based Sparse KV Storage (Janus)
arXiv 2609.36938 (2026-09-29) · READ END TO END (arxiv.org/html)

The substrate-tier item for sparse-attention frontier models (DeepSeek-V4,
GLM-5.2 are its three models) with SSD KV storage: training-free lookahead
prediction runs the model's own indexer d layers early to prefetch sparse KV off
the critical path; corrective reads preserve outputs losslessly; read packing +
CPU-assisted write packing + phase-aware write capping tune the SSD. "the recall
metric is above 96% for all three models, indicating that there are only 4% of
the sparse KV loading remaining on the critical path"; TTFT "up to 1.57-3.69x
(1.22-1.85x on average)" over existing works across three agentic traces.
Prediction distance aligns with architecture (d=2 DeepSeek-V4 interleaving, d=4
GLM-5.2 IndexShare). Estate fit: the lmcache-src shelf + RDNA1 box lane; also
the first paper this seat has read that names GLM-5.2's sparse attention
geometry (d=4 IndexShare), i.e. the serving behavior of the estate's own prime
animal family.

### 5. Receiver-Conditioned Latent Communication gives 94% CacheBack
arXiv 2609.32046 (2026-09-25) · READ END TO END (arxiv.org/html)

The interagent pass-off redesign for the swarm lane: the receiver sends the
sender its information need; the sender ships only the KV positions that need
satisfies, selected training-free from attention weights. "On FanOutQA,
CacheBack with Qwen 3 removes 75% of the state the agent would otherwise
receive, improving accuracy by 14.7 percentage points and reducing median
task-completion latency by 3.2x relative to text communication." At 16x
compression it removes 94 pct of sender positions and still beats same-size TEXT
handoffs on accuracy AND latency across dense / Mamba-hybrid / sliding-window
families (Qwen 3, Ministral 3, Gemma 4, Nemotron; +7.3-20.7 pp strict accuracy,
1.3-8.0x latency). Evidence recall at 8x: 93 pct vs 68 pct for the best
receiver-independent selector; recall rises with scale (68 pct @1.7B -> 93 pct
@32B). Code: github.com/maxr0ssi/rclc. Estate fit: the Mickey17 fan-out and
particle-flock designs pass text between actors; this measured result says
receiver-conditioned state beats text when sender/receiver share a family.

### 6. PReCache: Efficient KV Cache Sharing for Multi-LoRA Agents via Low-Rank
Precomputation and Neutral Reconstruction
arXiv 2609.34054 (v2 2026-09-28) · READ END TO END (arxiv.org/html)

Multi-agent cache sharing when each agent has its OWN LoRA adapter on a shared
backbone: "direct cache reuse causes the current agent to rely on cache states
generated by the previous agent's adapter, weakening the role-specific behavior
encoded by its own LoRA." Training-free fix: precompute every agent's compact
LR cache when context is FIRST processed (later agents skip re-prefill), and
reconstruct the shared base cache from adapter-free hidden states (neutral;
verified closer to the current agent's base than previous-agent-conditioned
state). "PreLRShared achieves up to a 3.1x TTFT speedup and a 2.3x improvement
in per-request throughput over inference without KV cache sharing"; ReBaseShared
accuracy drop only 1.1 pp on average. Two deployment schemes: lazy prefill
(single-stream) and double batching (concurrent serving). Estate fit: the
freeze-the-prefix doctrine assumes one adapter; the moment roles get adapters
(governor/judges/janitors on one backbone), this is the sharing contract.

### 7. AnchorKV: Safety-Aware KV Cache Compression via Soft Penalty with a
Refusal Anchor
arXiv 2606.17872 (2026-06-16) · Ni, Lao · abstract-depth read (API abs page)

The compression-side mitigation RQ4 needs: KV compression policies "either fail
to defend against jailbreak attacks or degrade safety alignment under aggressive
eviction"; AnchorKV biases token retention scores away from refusal-relevant
directions (soft penalty anchored on a refusal direction) as a drop-in
modification to existing compressors. Estate fit: pairs with item 1 as the two
ends of the safety-vs-compression trade (quant damage diagnosed by PCR;
eviction damage steered by anchor). Not deep-read this sitting; abstract-grade
confidence only.

### 8. Refusal-Gated Decoding: Preserving Refusal Behavior Under High-Temperature
Sampling
arXiv 2607.20791 (v2 2026-07-22) · Howard, Su, Roush et al. · abstract-depth
read (API abs page)

Extends the refusal-regime-dependence LAW to a third axis (sampling
temperature): "increasing the entropy of the token probability distribution via
high temperatures has also been shown to weaken the model's refusal response."
RGD runs a short greedy probe and preserves the greedy refusal response while
sampling everything else from the exact high-temperature distribution, minimal
latency. Estate fit: the regime-dependence class now has three members
(keyword-refusal under KV compression, refusal under KV quant, refusal under
temperature); any refusal measurement the estate banks must name its regime, the
same conditions law the one-bug rib demands for every instrument.

## Not banked, left named for the next window

- 2609.35139 CacheRepair (learned cross-chunk KV fusion repair) and 2609.12686
  (residual-vector long-context recall): on the 10-11 daily's own left-for-next
  list; claimed there, not here.
- SPLASH 2609.37626 (mid-flight parallel-layout switching): in-window, new, but
  systems-wide with no direct RQ tie; dropped for the 8 above.
- 2606.00288 Model-Native Computing Architecture (LLM-as-CPU vision survey,
  v3 2026-08-08): the KV-OS lane's map; new to catalog, skipped as vision-grade.
- The probe legs actually owed: emit-freeze wiring (RQ2), per-animal refusal
  battery at served quant (RQ4), RR-Evict-vs-freeze A/B on a real fleet tape
  (RQ3).

## Receipt

- Doors: export.arxiv.org API x7 via curl (serial, zero 429; first WebFetch
  attempt timed out at 60s and is reported); arxiv.org/html x6 (5 clean, 1 no-HTML
  stub); ar5iv x1 (stub); id_list abs reads x2.
- Local runs: catalog greps (3 commands, outputs above), memory/frontier +
  research_polished + lenses + rib grep (0 hits), prior-sweep greps (0 hits),
  `cp` preserving the 10-10 mint as .prior-2026-10-10.md, venv-python JSON census
  of desk-deepseek.json, grep of provider_usage.jsonl (0 rows),
  `tools/citation_lint.py check --files memory/research_polished/kv_cache_compaction.md`
  (ok / blocking=0), Read of models/providers.py:552-573 and :845-868.
- NOT run this sitting: any fleet A/B (RQ3), any model call, the emit-freeze
  build (RQ2), the 40-prompt refusal battery (RQ4). Each is named OWED above
  with its blocking instrument.
- ascii-only, no em-dashes; counts are instrument-tagged per the census
  denominator law.
