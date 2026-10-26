# SWEEP: open-local-language-models via HN (2026-10-11)

source-fetched: 2026-10-11
Seat: sweep gopher, frontier_olm_2026-10-11, area open-local-language-models, door hn.algolia.com.
Laws held: ascii only, no em or en dashes, no fabrication, every claim cites a fetch run this
sitting or a lens/rib file read this sitting. Anything not verified is marked OWED.

## Method (instruments, this sitting)

- Pass 1 (broad, 9 Algolia lanes, `search_by_date?...numericFilters=created_at_i>1789084800`
  = since 2026-09-11, plus one all-time relevance probe): queries "local llm" (30 hits),
  ollama (20), llama.cpp (20), "open weights" (18), "open source model" (8), vLLM (20),
  GGUF (20), Qwen (20), DeepSeek (20), Mistral page 1 of 3 (20), "mixture of experts" (5),
  relevance "local llm" (15). Unique candidates considered: ~100 (over the 30 floor).
  One degrade: the venturebeat Le Chonk URL returned HTTP 429 (logged below); the digitalcxo
  article for the same story was fetched instead and is the cited source for that item.
- Pass 2 (deep reads, end to end, 11 fetches): HN 50000488 (1117 pts / 980 comments) +
  the dgt.is article body itself (the HN thread page does not carry the article, so the
  article URL was fetched directly for the verbatim quote); HN 49929489 (DSH Desktop);
  HN 49911995 (Magnitude); HN 49926773 (Janus); HN 49911500 (Weave Router);
  digitalcxo Le Chonk; huggingface.co/Cloudflare/clef; HN 49859982 +
  jadidbourbaki.github.io/blog/prompt-lookup-llama-cpp/; gpufind.cloud/rent-vs-buy;
  HN 49727511 (Swift-Qwen3.8-27B); huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0;
  pentesttoday.com offensive-cyber post; HN 50016644 (Ask HN subscribed-vs-local).
- Overlap duty: `grep -c` on catalog/catalog.jsonl per candidate phrase; scoped
  `grep -r -l -i` over watch/inbox/frontier_olm_2026-10-05..2026-10-11, frontier_olm_adhoc,
  memory/research_packs, memory/steal, memory/runs (full-tree memory/ grep attempted once and
  killed as too slow; the scoped rerun plus the adhoc/10-09 register greps are the overlap
  instrument of record). A first recursive grep run was stopped mid-flight (exec_7ae53fd0);
  its partial output was superseded by the scoped rerun (exec_63c685ae, exit 0).

## Anti-rebank: already mined by prior runs, NOT re-banked (verified this sitting)

- Magnitude 49911995: substantive paragraph in frontier_olm_2026-10-10/sweep/
  open-local-models-x.md (on-device kernel-tuning quote) + listed in three 10-10 sweep files;
  never a register row. My deep read adds only the comment-thread benchmark fight (llama.cpp
  ~2x faster on M5 Max per two commenters; dual-5070ti user's app detects 2 GPUs as 4 and
  refuses models >8GB; MLX won all five Qwen metrics on M5 Max 128GB). Named here so the
  next fold does not lose those deltas.
- Cloudflare Clef + Clef-flash: 10-06 lane deep-read the HF card AND the blog
  (frontier_olm_2026-10-06/sweep/open-and-local-models-x.md, "Pass 2 (deep, 6 read end to
  end)") and captured the rungs (Clef-flash Qwen3.5-9B base, median 38.8 ms on Cloudflare
  iron; Clef Qwen3.8-27B base, 54.7 GB BF16, H200). My card read matched theirs. Dropped.
- Underdog Saluki 27B (50023055): 10-09 DIGEST item 3 carries the full numbers and the
  capability-axis caveat (tool calling 88/120 vs 84 full-size, AIME collapses), and the adhoc
  quantization lane read the same card. Dropped; the 10-09 lever line stands ("not a new
  model but a new compression recipe").
- Swift-Qwen3.8-27B (49727511): 10-06 inference-efficiency item 4 + 10-10 raw fetch
  (raw/swift_qwen3827b.txt, 76,404 bytes, in catalog). My read adds: license restricts
  companies >$1M; the AIME 98.7->94.0 regression was traced by the team to a math-token
  penalizer bug; one commenter found it too slow vs cheap API even on M1 Max 64GB. Dropped
  from the bank, deltas filed here.
- Prompt-lookup drafting (49859982): 10-10 inference-efficiency item 5 already holds the
  42x drafting speedup, the Lemire constmap, and the acceptance-rate caution. Dropped.
- LoRA over GGUF, Kisoku, Kolibri, Mozilla server benchmark, Windows ML, Sunk Cost,
  Return/Ollama: the adhoc register's 7 confirmed open-local rows (read this sitting from
  watch/inbox/frontier_olm_adhoc/register.jsonl). Untouched.

## Research questions answered from this sitting's reads

### RQ1. Open-weight releases after 2026-10-09 that would enter the funded-tier roster

None surfaced on the HN door. The two candidates are both not-yet: Mistral Large 4 "Le
Chonk" (1T total / 49B active MoE, API-only public preview as of the digitalcxo read,
"publicly downloadable version expected late October", license "has not been approved as
open source, though it's open-weight") and StepFun Step 5 Preview (600B/27B MoE, "open
weights coming Oct 15", 49796998, future-dated). The adhoc run's 7 confirmed finds name no
roster animal either: they are a quant recipe (GSQ-RCO), a rig-economics thread, a server
benchmark, a Windows runtime, a from-scratch 1.6B (Kisoku), and Kolibri (local-serve MoE).
Nothing in this sitting's pool is a paid-API open-weight animal addition to the funded tier
(Hermes primes + grok-4.7 per the DRIVING LADDER), and the ledger cannot record one anyway:
memory/burns/LEDGER.jsonl is byte-frozen at 705 rows / max ts 2026-09-28T19:30:00Z per
lens/burns.md:49-52 (five lenses in a row; not re-verified by a second read this sitting).
Watch item: re-probe Le Chonk weights on HF around late October.

### RQ2. Gates and battery cells before any roster addition fires a paid call

From lens/laws.md:38 (RIB_MODEL_GATES): every model gets its OWN harness gates (transport,
rails, failure modes); "a model whose fingerprint changed is a NEW animal, cold start, no
inherited trust". From lens/laws.md:106: the 8-column routing battery is UNMEASURED for
every family except deepseek-v4.1-flash, and rows expire at 30 days. Minimal cheapest legal
first call, composed from the ribs read this sitting: (1) descent leg 1, SHERPA cheap-first
plus prior-art sweep; (2) the per-animal harness gate (transport/rails/failure-mode probe);
(3) the ONE routing-battery cell matching the ask's question class, since question class
explains 36.3 pct of score variance vs family 3.6 pct (lens/laws.md:36), measured as
cost-per-blind-point against the incumbent; (4) the EMPTY_REASONING terminal guard armed
(lens/laws.md:39). NEW CELL this sweep contributes: provider-level cache-hit rate. The dgt.is
article read shows DeepSeek's own API holds near-full cache hits after an hour of inactivity,
and the 1117-point thread shows provider variance is decisive ("cheap OpenRouter providers
often have bad cache hit rates and short TTLs, negating token savings"; one user ran agents
constantly on 98 pct cached input for under $75/month). The battery's cache cell must name
the PROVIDER endpoint, not just the model, because two providers serving the same weights
have different cache economics. Corroborating datapoint from HN 50016644 read this sitting:
OpenCode Go's $10/month converts to about $60 of DeepSeek credits "with ZDR guaranteed"
(tacomagick comment).

### RQ3. Does the 2,957-hit "local llm" pool surface serving or gating tooling the estate lacks?

Yes, three classes, all read end to end this sitting. (a) Harness: DeepSeek Harness Desktop
(49929489) is a model-agnostic open-source agent harness ("everything is a plugin" on the
cordis architecture) that runs local models, and its desktop shell ships telemetry ON by
default; the thread names the exact disable keys (desktop-product-telemetry,
product-analytics, session-log-deepseek). That telemetry blocklist is a direct guardrail
steal for the estate's local-first law if DSH is ever evaluated. (b) Routing: Weave Router
(49911500) routes per turn with an HMM session-state classifier plus a cache-eviction
expected-value calculation, claiming Astra-level pass rates at 52-54 pct of cost; the
routing model itself is NOT open weights. This is working prior art for the estate's
routing-class doctrine and a steal-card shape, not a dependency. (c) Serving: Janus
(49926773, 106 pts) drew the community verdict "thin wrapper around llama-server" with no
benchmarks vs vLLM/SGLang; Magnitude's 194-point thread carried counter-benchmarks showing
llama.cpp still faster on M5 Max. Together with the banked Mozilla finding (config flags,
not engine churn) the serving lane says: nothing in the window beats the estate's current
llama.cpp janitor path; adopt nothing, watch the multiGPU-MoE fork (49845314) unproven.
Gating: the pentesttoday read fills a slice of the corpus's missing safety-venue lane
(lens/corpus.md:29 notes the corpus holds no ML-benchmark or safety-venue material), with
the caveat that it is a blog benchmark on Juice Shop, not a peer-reviewed venue, and
per that same lens gap it cannot be cross-checked against holdings. The pool's all-time
relevance top (Clippy 90s UI 1122 pts 2025-05-06, "local LLM ecosystem doesn't need Ollama"
648 pts 2026-04-16, Lemonade 572 pts 2026-04-02) is outside the 30-day window; the window's
fresh signal is the four classes above.

### RQ4. GPU-ladder five gates after the 10-10/10-11 carrier waves

Read the rib directly this sitting: memory/rib/RIB_GPU_LADDER_20261001.md:10-23. The five
gates are ARCH (SM90/SM100 full pay), VRAM (24 GB minimum), PRICE (24GB+ Blackwell under
~$1200, 5090-class under ~$1700, used H100 under ~$4000), SOFTWARE (CUDA 12.8+ with NVRTC
via cuda-python, plus vLLM or SGLang running FP8 in a container), WORKLOAD (real FP8/MoE
QPS demand). The estate box is AMD RX 5600 XT (RDNA1, gfx1010) (rib:5). Verdict this
sitting: all five still false. ARCH/VRAM: no new card in evidence anywhere in the sweep.
PRICE: the gpufind read shows a rent-vs-buy break-even instrument over 56 providers (e.g.
RTX PRO 6000 Blackwell $2.19/hr median from 29 providers) with an MCP tool, but rental
rates are not the rib's purchase triggers; nothing observed crossed a trigger line.
SOFTWARE: false by construction on RDNA1 (no CUDA/NVRTC path); the one software movement in
the window, DeepSeek porting DeepGEMM to Huawei Ascend 950 (HN 49942400), points further
away from this box, and the Windows ML llama.cpp work is already banked (adhoc register).
WORKLOAD: no mating->MoE export door evidence; the Swift-Qwen thread (M1 Max 64GB local
still slower than cheap API) and the dgt.is economics argue local FP8 volume is not the
binding constraint. Honest scope: this is a door check plus one instrument read, not a
price survey; PRICE is reported as no-contrary-evidence-observed, not measured. The 10-11
gstd perimeter wave (vast.ai long-term rental) rides outside the ladder's buy logic and
flips nothing.

## Banked items (8, strongest first; every quote verbatim from a page fetched this sitting)

1. Why isn't the industry freaking out about DeepSeek 4.1 Flash? (dgt.is 2026-10-07 + HN
   50000488, created 2026-10-08T00:14:48Z, 1117 pts / 980 comments). First full read in the
   estate: the 10-08 run logged "dgt.is timed out once"
   and the adhoc run explicitly marked the article and thread "NOT held". KV-cache finding
   chain: article says DeepSeek cut KV cache roughly 437x vs V1, which is what keeps all-day
   agent sessions under $1; thread cites the tech report "KV cache memory reduced by over
   50x and FLOPS by over 5x"; self-hosting 4.1 Flash "isn't economically worthwhile now"
   but cache work "to enable fully local use soon". RQ1/RQ2 load-bearing.

2. DeepSeek Harness Desktop for macOS and Windows (HN 49929489, 2026-10-02, 417 pts / 228
   comments). Open-source agent harness, model-agnostic incl. local models (one user points
   it at "my strix halo running Qwen3.8 Flash Next"); desktop telemetry ON by default with
   named disable keys; "dsh web" against a local model sends nothing to DeepSeek by default
   (wren6991). Steal card: the telemetry blocklist. Also corroborates the banked DeepSeek
   off-peak proof (rootsudo: direct API cheaper, "~50% off-peak discount during US daytime").

3. Show HN: Open-source model routing for coding agents at Astra-level performance (HN
   49911500, 2026-09-30, 123 pts / 42 comments). Per-turn router: HMM traces session state,
   classifier narrows ~10^100 routing paths to model buckets, cache-eviction EV calc avoids
   costly switches; matched Astra pass rates on Terminal Bench 4.0 / SWE Atlas at 52-54 pct
   cost, 2.2-2.5x faster. Routing model not open weights. Prior art for the routing-class
   doctrine; the EV-over-cache-eviction idea is the transferable piece.

4. Show HN: Janus, Go binary that runs GGUF models via Vulkan on AMD/Intel/Nvidia (HN
   49926773, 2026-10-01, 106 pts / 19 comments). Community verdict: thin llama-server
   wrapper, no novel features; no benchmarks vs vLLM/SGLang. Hardware rungs from comments:
   single V100 ~900 t/s prefill / ~100 t/s decode on 27B 4-bit; Intel Arc B60 ~50 t/s decode;
   Vulkan vs SYCL "in the same ballpark" per one tester. RQ4 context: cross-vendor runtimes
   exist but none beat the janitor's current path.

5. Mistral's Le Chonk Arrives with a Trillion Parameters (digitalcxo, story dated 2026-10-08;
   HN 50003636 and 49978040). 1T total / 49B active MoE, trained on 3,800 Grace Blackwell
   GPUs; API-only public preview, downloadable version expected late October; license not
   OSS-approved though open-weight. RQ1 watch item with a named re-probe date. Degrade note:
   the venturebeat source 429'd; this article is the fetch of record.

6. Show HN: Check if it is cheaper to rent rather than buying a GPU + MCP to find the
   cheapest GPU to run your model (gpufind.cloud; HN 49829063 2026-09-24 and 50031782
   2026-10-10). Rent-vs-buy break-even over 56 providers, board-power aware, MCP tool in nav.
   10-08 quant sweep flagged it as a "candidate rung ... for whoever fills the cells"; this
   sitting's read confirms the instrument shape for the RQ4 price gate. Not a roster item.

7. Open weights models are surprisingly aligned on offensive cyber (pentesttoday.com, HN
   49747378, 2026-09-17). Authorized OWASP Juice Shop eval (116 challenges) with the T3MP3ST
   harness: GLM 5.3 and Kimi K3 refused most offensive tasks; abliterated variants "failed
   to run pentests and behaved oddly"; GPT-5.6 Sol found 29. Direct model-gates datapoint
   for the estate's own seat animal (GLM family) and the first safety-lane material the
   corpus's gap (lens/corpus.md:29) has seen; blog-grade, cross-check unavailable.

8. Ask HN: Are you a subscribed LLM or a locally deployed open-source model? (HN 50016644,
   2026-10-09, 11 pts / 18 comments). Sentiment split roughly 40 pct subscribed-only, 35 pct
   hybrid, 15 pct local-only. Datapoints: OpenCode Go $10/month converts to ~$60 DeepSeek
   credits with ZDR guaranteed; one local-only user runs open models on owned hardware
   despite employer's unlimited spend. Thin but it is the independent market-side pair to
   the dgt.is economics in item 1.

## OWED

- Nothing in this file is asserted that was not fetched or grep-run this sitting. The five
  RQ4 gate verdicts are door-scope (no price survey); the price trigger state is
  no-contrary-evidence, not measured.
- The ledger writer instrument still does not exist (lens/burns.md:73-76); this file is a
  DIGEST-class mining record per that standing rule until one is minted.
- Not run this sitting: any pytest, any corpus write, any register mutation. This seat banks
  to watch/inbox only; the banking commit remains owed by the fold owner (three runs deep,
  lens/burns.md:225-228).
