# SWEEP: inference-efficiency via X (frontier_olm_2026-10-04)

source-fetched: 2026-10-04
Seat: sweep gopher, area inference-efficiency. Sweep window 2026-09-04 to 2026-10-04.
House laws held: ascii only, no em dashes, every claim cites what was read or run this sitting.
Every banked item was fetched and read by this seat during this ask; quotes are copied from the
fetch output (fxtwitter article fetches render long-form posts as summaries with figures, and
that is flagged per item below).

## 1. Door health (this sitting, instruments named)

- WebSearch backend: 1302/429 rate-limit storms on 7 of 12 issued queries (the raw MCP error
  blocks are quoted in the transcript of this session); 5 queries returned results, and only 1 of
  those (the Ollama/vLLM tok/s query) surfaced actual x.com items. This matches the door-health
  certification already on file: "X discovery degraded (1302/429 storms) with fxtwitter resolution
  alive" (watch/inbox/frontier_olm_2026-10-04/lens/burns.md:109-111). Do not rediscover this.
- fxtwitter door: 6 of 6 status resolutions succeeded end to end (RituWithAI, TheValueist,
  exolabs, Mayhem4Markets, itsharmanjot, TheAhmadOsman). One limitation found: the fxtwitter USER
  endpoint (api.fxtwitter.com/dr_kabanov) returns profile metadata only, no posts, so the
  CacheBlend/LMCache post seen in search results could not be resolved to a status body.
- arXiv door: clean (arxiv.org/html/2609.32213v1 fetched in full).
- Vendor docs door: clean (openrouter.ai/docs/api-reference/limits fetched in full).
- One X-native item is unresolvable: "DeepSeek's Permanent Discount Lasted 83 Days. The Tax"
  (Aug 26, 2026) surfaced in search with only a root x.com URL, no status ID, so it stays a
  snippet banked at section 5 with its search snippet, per the recipe's fallback rule.

## 2. Pass 1 census: 42 candidates considered (moment: this sitting)

X-door candidates (11): TheAhmadOsman article 2057183854444843202; QuantumindSSI article
2075117605690458118 (not fetched; by snowflake ordering it predates the Jul 8 post, out of
window); TheValueist status 2006375989547262359; itsharmanjot status 2074872742487445651;
RituWithAI status 2095015333321142344; exolabs status 2103617535765573959; hooeem article
2068752941553476002 (not fetched, out of window by ID ordering); Mayhem4Markets status
2082487427138994230; dr_kabanov CacheBlend post (profile-only, unresolvable); the DeepSeek
83-days post (snippet only, root URL); one irrelevant site:x.com noise hit ("nanny function",
Sep 7 2026, domestic employment, not inference).

Non-X corroboration candidates (31): TrueFoundry OpenRouter pricing 2026 (Aug 25 2026); APIMart
OpenRouter pricing; explainx.ai OpenRouter routing guide (Aug 21 2026); dev.to "7 Best Model
Routing Tools" (40-85 pct savings claim, snippet only); intelligentfounder.ai GPT-5 mini pricing;
routerpark.com GPT-5-mini routing (75-90 pct claim, snippet only); ResearchGate HM-Router entry;
SSRN Cost-Quality Frontiers in LLM-Assisted Policy Analysis (GPT-5 approx 5.3x GPT-5-mini);
ACL SELECT-THEN-ROUTE taxonomy; grislabs AgentMeter "Cost Anatomy of 1127 Agent Runs" (Mar 26
2026, out of window); blog.tonic3.com AI budgeting; dev.to economic firewalls / agent spending
limits; ainativelang token budget monitoring; techresolve.blog track LLM spend; heygovind.com
FinOps attribution (providers bill per API key, not per customer); paid.ai per-agent cost
tracking; gamesbeat NIM 3x tokens (Jun 2024); rfp.wiki Perplexity vs NIM (2026); vmblog Cloudera
NIM (Oct 2024); NVIDIA developer forums NIM 2.4x; PromptQuorum "Enterprise Inference Servers
2026: vLLM vs TGI vs NIM" (Sep 2026, in window, not fetched); Alibaba Cloud NIM deploy guide
(Sep 2026); openrouter.ai docs limits page; requesty.ai LLM API Rate Limits survey (Jun 13 2026);
reddit r/Bard Gemini free-tier 429 thread; stackoverflow Gemini "limit: 0" case; OpenAI rate
limits docs; futureagi agent harness 5 dimensions; arxiv cs listing hits (hardware-aware MoE
scaling); x.com root-URL generic hits from two degraded queries (no resolvable posts).

## 3. Pass 2: 8 items read end to end this sitting

1. HM-Router, arXiv 2609.32213v1 (fetched in full).
2. exolabs DGX Spark Handbook via fxtwitter (fetched in full).
3. OpenRouter free-model limits doc page (fetched in full).
4. requesty.ai rate-limits survey (fetched in full).
5. RituWithAI club-3090 post via fxtwitter (fetched in full).
6. TheValueist LLM serving economics via fxtwitter (fetched in full; see overlap verdict 5.3).
7. Mayhem4Markets EXL3 article via fxtwitter (fetched in full; out of window, held).
8. itsharmanjot Qwen4-Coder claim via fxtwitter (fetched in full; REJECTED, see 5.2).

## 4. Banked register (6 items, strongest first)

### 4.1 HM-Router: joint model AND harness routing (Q3, direct hit)

arXiv 2609.32213v1, 26 Sep 2026, Chen et al (Imperial/Samsung/IST). Verbatim: "We evaluate on 12
benchmarks from hm-router-bench, covering 293 routes, 73 models, and 25 harnesses." It jointly
selects model + harness per query, learns separate factorized embeddings plus a CP-decomposition
interaction term so unseen (query, model, harness) pairs generalize. Under dollar budgets it
"leads at all seven evaluated dollar budgets, exceeding Av-Pro by 8.5 percentage points at $2 per
task" (61.86 vs 58.41 Av-Pro at <=$1.50/task; 69.21 pct at <=$2). Router signals: frozen
Qwen3-Embedding-8B query features, learned identity embeddings, per-component behavioral success
vectors over training queries, harness text descriptions, and predicted cost, scored
r = argmax(y_hat - lambda*c_hat). Overhead 25.6 ms/query against >100 s/task agent execution;
training under four seconds per benchmark; code open (github.com/hmarkc/HM-Router).
Estate fit: this is the published formalization of RIB_MODEL_GATES_20261001.md:8-11 (per-animal
harness profiles: "every model gets its OWN transport, rails, and failure profile") and of the
grid row shape (RIB_MODEL_GARDEN_ROUTING.md behavioral success vector == the estate grid row;
their 25 harnesses == the estate's carriers incl the seven unwired jackets at
RIB_INFERENCE_BUDGET_20261001.md:100-114). The lambda-scalarized score is a published cousin of
the estate's cost-per-blind-point champion metric (RIB_ROUTING_CLASSES_20261002.md:24-26).
Overlap: "HM-Router" = 0 hits in catalog/catalog.jsonl (1,040,765 lines scanned this sitting) and
0 in memory/rib + memory/burns + memory/improve; RouteLLM lineage is known estate-side
(memory/runs/corpus_gap_research/ARXIV_REGISTER.json, "the RouteLLM steal" named in
RIB_ROUTING_CLASSES_20261002.md), HM-Router itself is absent. Genuinely new.

### 4.2 exolabs DGX Spark Handbook (Q5, direct hit)

X post by @exolabs, Sep 25 2026 22:47 UTC (status 2103617535765573959), linking the handbook by
@0xSero (reviewed by exo's founders). Figures via the fxtwitter fetch: 128 GB at 273 GB/s
(approx 6.5x slower than RTX 5090); two-Spark scaling 546 GB/s, four 1,092 GB/s; NVIDIA's own
tests show writes scaling 2x/3.7x on 2/4 units but reads only 1.6x/2.1x. Model table:
Qwen3.6-35B MoE (3B active) at NVFP4 approx 95 tok/s single user, 317 total across 8 users;
Qwen3.8-27B approx 51 tok/s code with a draft helper vs approx 23 chat; Qwen3.8-Flash-Next 48.7
tok/s one Spark, 52.1 on two with MTP; GLM-5.3-Flash 10-25 tok/s one, 62.9 two, approx 45 on a
four-Spark ring (approx 100 warm), author's best 118 tok/s with DFlash2 speculative decoding,
and 27 tok/s prose vs 65 on structured output; DeepSeek-V4.1-Flash 45.4 single / 134.2 across
sixteen users on four; prefill 3,360 tok/s reading a 32K prompt on four Sparks. NVFP4 shrinks
Qwen3.6-35B from 72 GB to 24 GB; MoE expert pruning to 168 of 256 experts (197 GB) measured by
KL divergence 0.089 unpruned vs 0.511 pruned. Verdict line: "The author would buy again and
would start with two units; most people should stop at two." Price context $3,999 to $7,999.
Estate fit (Q5): the no-hardware-change lifts are exactly spec decode (DFlash2/MTP/draft helper:
2-4.7x), batching (3.3x aggregate at 8 users), structured output over prose (2.4x), and quant
(NVFP4 3x memory shrink); the KL-divergence pair is a copyable quality-tax measurement for the
estate's own quant ladder (the re-owed qwen2.5:7b Q4_K_M vs q8_0 A/B probe,
frontier_olm_2026-10-04/lens/burns.md:116-117). Caveat: figures are the fxtwitter resolver's
rendering of the article, not byte-quotes from x.com; treat numbers as UNVERIFIED-by-primary and
per the instruments-only law they fill NO routing cell
(RIB_MODEL_GARDEN_ROUTING.md:47-53).
Overlap: phrase "DGX Spark" = 0 in catalog; "DGX" alone = 72 hits all unrelated (checked
context); "DFlash2" = 0; "NVFP4" = 5 catalog hits and the NVFP4 quant format is already known
estate-side (round-2 banked "2609.04098 GDN NVFP4 deep read",
frontier_olm_2026-10-04/lens/burns.md:97-98); the Spark tok/s table is new.

### 4.3 OpenRouter free-model limits, primary doc (Q4, partial resolution)

openrouter.ai/docs/api-reference/limits, fetched in full this sitting (living doc, no date
shown). Documented constants: FREE_MODEL_RATE_LIMIT_RPM = 20; FREE_MODEL_NO_CREDITS_RPD = 50;
FREE_MODEL_HAS_CREDITS_RPD = 1000; threshold 10 credits purchased all-time, and "the higher
daily ceiling is granted starting one credit below the table's threshold". Counting basis is per
REQUEST (free_model_daily_requests tracks used/limit/remaining daily requests), not per token;
no tokens-per-minute ceiling is documented anywhere on the page, and "The per-minute limit is
not reported there" in the key endpoint response. Exempt: BYOK and exempt accounts.
Estate fit (Q4): this resolves HALF the free-lane forcing contradiction
(RIB_MODEL_GARDEN_ROUTING.md:186-192) from public evidence: the documented ceiling is a
request-count quota (50/1000 per day at 20 rpm), so a request-sparse forced lane (the estate's
69h+/459-row stealth census with zero 429s) is consistent with documented policy, and "forcing
free lanes throttles them into empty 429s" is NOT explained by any documented token ceiling or
decay window. The decay half stays OWED: this sweep found no published rate-window-decay
evidence for any provider (the requesty survey, 4.5, names no decay model either; my
"decay"-phrased searches matched no content). Minimal funded probe: fire probe 3 as a
per-request counter against the documented daily quota (design now sharpened: count requests,
not tokens, and log whether 429s correlate with the 20-rpm bucket or the daily total, since
"failed requests still count toward your rate limit in many cases" per 4.5). Note the estate
already measured "both hot free doors expose zero rate-limit headers"
(frontier_olm_2026-10-04/lens/burns.md:115-117), so header-driven adaptive pacing is dead;
only the counter can decide it.
Overlap: "FREE_MODEL" = 0 catalog; "20 requests per minute" = 0 catalog; the 10-03/10-04 burns
ledger tracks OpenRouter roster counts (460 vs 458 models) but no limit-policy record; new.

### 4.4 RituWithAI club-3090 serving stack (Q5, consumer-hardware configs)

X post by @RituWithAI, Sep 2 2026 (status 2095015333321142344; TWO DAYS OUTSIDE the sweep
window, banked with that caveat because it is the strongest consumer-GPU config set found).
Apache-2.0 open-source "club-3090" stack: vLLM dual-GPU for throughput vs llama.cpp single-GPU
for robustness, Docker Compose, OpenAI-compatible API on localhost:8020. Figures via fxtwitter
fetch: Qwen3.6-27B on 2x RTX 3090 vLLM dual 89-127 tok/s code tasks at 262K context, 4
concurrent streams, speculative decoding on; single 3090 llama.cpp approx 51-60 tok/s, 200K
context, passes a 91K needle ladder, handles 25K-token tool returns; Gemma 4 31B dual 106-141
tok/s; Qwen3.6 35B-A3B MoE 103-149 single card, 178 dual; methodology 3 warmup + 5 measured
passes per config. Closing line quoted: "Apache 2.0 License. 100% Open Source."
Estate fit (Q5): dual consumer cards + batching + spec decode land in the same band as the Spark
handbook's numbers (89-127 vs the estate-class single-card 51-60), and the MoE A3B result
(103-149 on ONE card) is the shape worth probing for the janitor fleet's next local workhorse;
the warmup+measured methodology matches the estate's one-bug conditions law.
Overlap: "RituWithAI" = 0, "club-3090" = 0 in catalog and memory; "3090" = 313 generic catalog
hits (RTX chatter), none this stack. New.

### 4.5 requesty.ai rate-limits survey (Q4 corroboration; out of window, reference page)

"LLM API Rate Limits (2026): OpenAI, Anthropic & DeepSeek", requesty.ai, "Last updated June 13,
2026" (3.5 months before the sweep window; banked as a living reference page). Verbatim quotes
from the fetch: DeepSeek "it does not enforce explicit rate limit quotas on its users" (load
shows up as latency, 30-minute hard connection close); "Always honor any Retry-After headers if
the API provides one"; "failed requests still count toward your rate limit in many cases";
Anthropic returns anthropic-ratelimit-requests-remaining with a reset timestamp; sub-minute
enforcement: "an official 60 RPM limit might internally be enforced as '1 request per second'
evenly". No decay/exponential window model is named anywhere in the piece. Internal
contradiction on file: its FAQ says "DeepSeek allows 60 RPM on their free tier" while the body
says no explicit quotas; treat DeepSeek quota claims as disputed.
Estate fit (Q4): corroborates 4.3 (request-counted buckets, Retry-After as the only decay-ish
signal) and adds the failed-requests-count caveat that shapes probe 3's design. Also names the
only provider-side adaptive signal the estate's lanes could consume if a door ever exposes it.
Overlap: "requesty" = 8 catalog hits, all opencode/cline source assets (a provider svg icon, an
auth controller file), the survey itself not banked. New as a record.

### 4.6 TheAhmadOsman inference-engine matrix (Q5 methodology; out of window)

X article "Inference Engines for LLMs & Local AI Hardware (2026 Edition)", May 20 2026 (status
2057183854444843202; 4.5 months outside the window; kept because it banked a measurement
doctrine, not a number). Quotes from the fetch: "Fit is not speed. Capacity is not bandwidth.";
"Bad benchmark: 'I got 180 tok/s'"; FP8 "can double performance and halve memory consumption
versus 16-bit"; "Note: DO NOT USE Ollama."; engine matrix llama.cpp (laptop/edge, not
multi-GPU), MLX (Mac), ExLlamaV2 (single RTX), ExLlamaV3/EXL3 (2-4+ consumer NVIDIA, QTIP
lineage), vLLM (production default), SGLang (long-context/MoE/routing, RadixAttention, prefill-
decode disaggregation), TensorRT-LLM (NVIDIA max), Dynamo (cluster). It explicitly rejects raw
tok/s benchmarks and prescribes TTFT, TPOT, p50/p95/p99, and cost per 1M tokens under realistic
workload shape and concurrency.
Estate fit (Q5): the prescribed metric set is exactly the estate's one-bug conditions law
applied to serving; adopt TTFT/TPOT/percentiles as the required condition triple for any future
janitor tok/s claim. The "DO NOT USE Ollama" line is a vendor-loud opinion, not an estate
instrument result; it routes nothing (instruments-only law), but it flags that Ollama's comfort
defaults (no paged attention tuning exposed) are the known cost.
Overlap: "TheAhmadOsman" = 0 catalog, 0 memory. New.

## 5. Rejected and held (anti-rebank)

5.1 TheValueist "LLM Serving Architecture and the Economics of Inference" (Dec 31 2025, status
2006375989547262359): read end to end this sitting; richest cascade/caching compendium found
(vLLM 24x vs HF / 3.5x vs TGI; SGLang up to 5x vs vLLM in specific workloads; 60-80 pct GPU
memory waste from KV fragmentation; prompt caching cuts latency up to 80 pct and input cost up
to 90 pct; Vertex charges 10 pct for cached tokens; 50 pct batch discounts; cache TTL 5-10 min,
up to 24h via KV offload; OpenAI routes on first-256-token prefix hash, needs 1,024+ token
prompts, overflow near 15 rpm same-prefix). NOT banked as new: catalog holds
watch/inbox/frontier_olm_20260928/sweep/_raw/fx_thevalueist.json (59,866 bytes) and its
lsa_reboot_staging twin (catalog ids 0abde563fb4c, 6efd44f32c83), i.e. the 09-28 sweep already
fetched this author via fxtwitter. Re-banking would be waste. Its cache-TTL/offload numbers DO
feed Q5's KV-offload question and are on file in that prior raw file.

5.2 itsharmanjot "Qwen 4 Coder 32B 82 pct SWE-Bench" (Jul 8 2026, status 2074872742487445651):
REJECTED. A community note on the post disputes it: Alibaba has released no such model and no
Qwen model tops SWE-Bench Verified. This is the round-2 unconfirmed class
(frontier_olm_2026-10-03 DIGEST holds unconfirmed items out of the register); do not cite the
82 pct or the 135 tok/s M5 Max figure anywhere.

5.3 Mayhem4Markets EXL3 article (Jul 29 2026, status 2082487427138994230): read end to end, out
of window, HELD in this file rather than the register. Useful fragments if the estate ever goes
EXL3: memory-bound decode throughput approximates batch size x bandwidth / model size; a
repeatable quality bump near 3 bpw is noted; EXL3 is NVIDIA-only (no AMD/CPU, not in vLLM/
SGLang, served via TabbyAPI), which on the estate's AMD box means the quant lane stays
GGUF/llama.cpp-side (consistent with RIB_GPU_LADDER_20261001.md:10-31). "EXL3" = 0 catalog.

5.4 dr_kabanov CacheBlend/LMCache post: unresolvable (fxtwitter user endpoint returns profile
only). Not banked. The estate already holds the primary in-corpus: lmcache-src docs including
cacheblend.rst (catalog: corpus/library/lmcache-src/docs/source/kv_cache_optimizations/
cacheblend.rst; "CacheBlend" = 25 catalog hits, "LMCache" = 2,333). No new angle found on X.

5.5 DeepSeek 83-days discount post (Aug 26 2026): snippet only, root x.com URL, no status ID.
Snippet on file: "KV cache does not delete the physics: a hit still occupies memory bandwidth"
+ "A cache hit is a promise about prefix stability." Relevant to the OWED DeepSeek
invoice-strength discount check (memory/burns ledger line 680 via the 10-04 lens :69-70) only as
a rumor of pricing volatility; no number was verifiable. UNVERIFIED, do not cite.

## 6. Answers to the five research questions (sweep-level synthesis)

Q1 tank accounting: the hermes_burn ledger row shape is
{ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}
(memory/runs/hermes_burn/usage.jsonl lines 1-3 read this sitting). Published harness schemas
found (AgentMeter per-task cost SDK, heygovind's attribution problem "providers bill per API key,
not per customer", paid.ai per-agent tracking) all reduce to per-dispatch-id cost attribution,
which is exactly the ledger's id-keyed shape: NO schema migration is needed for parity. The one
real gap is probe 3's requirement to COUNT REQUESTS (the estate's own finding that hot free
doors expose zero rate-limit headers, 10-04 lens :115-117): that is one additive field
(requests: 1) per row, not a migration. The 09-28 sweep's TheValueist raw file already holds the
vendor-side accounting context (batch discounts, cached-token pricing) for the cost side.

Q2 unmeasured cells: the instruments-only law is explicit that public/vendor numbers fill NO
cell (RIB_MODEL_GARDEN_ROUTING.md:47-53), so OpenRouter stats, NIM listings, and leaderboards
can only seed priors and probe design, never cell values. What this sweep adds: HM-Router's
method is the published template for filling cells cheaply, its behavioral success vector over
training queries is a grid row, its predicted-cost term is estimable from public price sheets
BEFORE any probe, and its 25.6 ms/query overhead shows the battery is cheap enough to run
estate-wide. Minimal funded probe set: the sanctioned battery fill
(RIB_MODEL_GARDEN_ROUTING.md:202-209) over the funded animals' UNMEASURED columns (grok-4.7: 7
of 8 unmeasured; glm-5.3-prime: 4 of 8), question-class-first, one receipt file per cell.

Q3 router/cascade curves vs the tier ladder: published designs converge on the ladder's shape.
HM-Router: quality parity by construction (route selection maximizes y_hat - lambda*c_hat),
+8.5 pp at $2/task budgets. Snippet-level claims (dev.to 40-85 pct; routerpark 75-90 pct) are
consistent but unfetched, cited here as snippets only. The estate's question-class-first law
(36.3 pct of score variance from question class, RIB_ROUTING_CLASSES_20261002.md:11-16) is
stronger than a learned router for the estate's scale: HM-Router needs per-route training
queries, the class law is closed-form. Wiring the seven unwired carriers
(RIB_INFERENCE_BUDGET_20261001.md:100-114: stealth_driver, duel_harness, tesuji_fire,
lane_runner, lite_scale, wave_fire, ds_workhorse): adopt HM-Router's two published halves, the
behavioral success vector (already the grid row shape) and the terminal-marker jacket (already
proven in the two wired carriers tools/hermes_burn.py + tools/model_garden.py); the missing
piece in the other seven is only the jacket plumbing, not the theory.

Q4 free-lane forcing contradiction: PARTIALLY RESOLVED from public evidence. Documented policy
(OpenRouter primary doc, fetched this sitting) is request-counted: 20 rpm, 50/day, 1000/day at
the 10-credit threshold, no token ceiling, per-minute usage not even reported in the key
endpoint. No provider publishes a decay window (requesty survey names none; decay-phrased
searches matched nothing). Therefore the forced-lane census result (69h+ sustained, zero 429s)
is consistent with documented policy for request-sparse lanes, and the rib's "forcing throttles
them into empty 429s" can only be a sub-documented behavior: unresolved by any public source.
Resolution path is measured, not editorial: fire probe 3 as a per-request counter (per 4.3
design), plus honor Retry-After when a door finally exposes one. Per the grid's own order, this
resolves with instruments, never by silently editing either rib
(RIB_MODEL_GARDEN_ROUTING.md:186-192).

Q5 local janitor fleet lifts without hardware change: four measured, convergent leaders from
4.2 + 4.4: (a) speculative decoding, 2-4.7x on consumer silicon (DFlash2 118 vs 62.9 tok/s;
draft helper 51 vs 23 tok/s; spec-decode on in the club-3090 vLLM config); (b) batching, 3.3x
aggregate (95 single vs 317 across 8 users; 134.2 across 16 users on the Spark table); (c)
structured output over prose, 2.4x (65 vs 27 tok/s GLM-5.3-Flash), directly applicable to
janitor scut tasks that already emit JSON; (d) quant, NVFP4 72 GB to 24 GB for a 35B MoE, with
the KL 0.089 vs 0.511 pair as the copyable quality-tax instrument for the estate's own ladder
(the re-owed qwen2.5:7b Q4_K_M vs q8_0 A/B). Measurement doctrine from 4.6: TTFT/TPOT/p50/p95/
p99 + cost per 1M tokens, never bare tok/s. None of these numbers may enter a routing cell
without an estate instrument reproducing them on the estate's own AMD box (instruments-only
law); they are probe designs, not verdicts.

## 7. What this sweep did not do

Fired no models, ran no estate probes, spent nothing. All findings are public-source reads
fetched this sitting. The X search door degraded the pass-1 net toward tech-blog corroboration;
the register's X-native share (3 of 6) reflects that degradation, reported plainly rather than
papered over. The DeepSeek-83-days and dr_kabanov items are unresolved, held at section 5.
