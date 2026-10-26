# SWEEP: inference-efficiency via X, 2026-10-08

source-fetched: 2026-10-08
Sweeper: sweep-inference-efficiency-x (frontier sweep gopher). Lens read this sitting:
watch/inbox/frontier_olm_2026-10-08/lens/laws.md (215 lines) and lens/burns.md (244 lines)
in full; the ask's five research questions map to lens/laws.md lines 149-158, 41-51, 64-66
and lens/burns.md lines 181, 214-215, 46-49 as the ask stated (verified: the ask's "lens/"
prefix resolves to the 2026-10-08 frontier_olm carrier; no root lens/ exists).

## Door status (said straight)

- WebSearch site:x.com: first call returned backend 1302/429 rate-limit noise, then
  self-recovered; 14 queries total this sitting, all eventually returned results. Unlike
  the 10-03 lane (which recorded zero in-window full status URLs), this pass got full
  x.com/<user>/status/<id> URLs from search.
- fxtwitter door: 11 of 11 attempted resolutions returned HTTP 200 JSON with post text,
  author, and date. X long-form ARTICLES (/i/article/...) are not directly resolvable,
  but posts carrying articles embed article title + preview + summary in the fxtwitter
  JSON; that is how article content reached me. No login needed. Door healthy.
- House shape: every quote below is verbatim from a page I fetched this sitting; every
  number I could not verify is labeled as the post's claim, not mine.

## Pass 1 ledger (candidates considered: 59 distinct)

Searches run (14): reasoning-token cost cut guides; DeepSeek V4 pricing; empty
reasoning_content; 429 retry storms; Featherless roster; prompt-caching economics;
Anthropic Advisor routing; thinking-budget parameter cost; empty think blocks;
GLM 5.3 flash free tier; thinking-off + DeepSeek off-peak; October agent cost-per-task;
finish_reason length exhaustion; harness router build.

In-window (>= 2026-09-08) candidates: ArtificialAnlys Coding Agent Index (Oct 2);
0xCodila NVIDIA/MIT harness-cost post (Oct 3); MossAI hidden-billing article post
(Sep 17); BrandonWaselnuk Unblocked GLM migration (Sep 24); kirillk_web3 October model
guide (article, snippet only); dr_cintas hourly agent savings (snippet only); LangChain
64 percent median cost-per-task router cut (profile page, no single status id, snippet
only); x.com/i/article/2105704739585565066 harness router Pareto (article, snippet
only); Daily AI Recap Oct 1 (snippet only); BAI_AGI GLM-5.3-Flash pricing post; Z.ai /
ZCode / jietang GLM free-tier posts (vendor surface, snippet only).

Out-of-window but read for load-bearing relevance (flagged, banked only with the flag):
no_stp_on_snek Qwen3.8-27B offlabel audit (Aug 14); Blackwellboy "not one number"
(Aug 19); EBorgnia Relace DeepSeek v4 Flash (Aug 24); FeatherlessAI GLM 5.3 Flash
(Aug 28); LimestoneHQ Fable-5 orchestrator numbers (Jul 13, read, NOT banked as item:
87 days stale and its delta is covered by fresher items); the_smart_ape Opus 4.7 guide
(Apr 17, read, NOT banked: six months stale); AlphaSignalAI Advisor explainer (Apr,
snippet only, not banked).

Snippets considered and deliberately NOT banked as items (per recipe, no fetch = no
bank): kirillk_web3 ~$0.94/task claim; LangChain 64 percent router cut; dr_cintas
$8.75-13.50/hour saved; paddix 90+ percent cache-hit Kimi K3 row (profile replies page,
unresolvable); TheZvi AI 185; josheganai retry-storm row (profile, unresolvable);
ttunguz thinking-off 133s/2219-token bench (profile, unresolvable); thejoyrises
thinking-disabled-400 row (profile, unresolvable); synthorai 3-6x per-correct-answer
row (profile, unresolvable).

## Pass 2: the 8 banked items (all fetched and read this sitting)

1. Artificial Analysis Coding Agent Index (Oct 2, IN window)
   https://x.com/ArtificialAnlys/status/2105814318294114720
   Score + measured cost per task, model+harness as the unit: Sonnet 5.5 (max) 68 at
   $14.19/task; Gemini 4 Argon (high) 64 at $5.84; GPT-6.1 Sol (xhigh) 63 at $1.04.
   Verbatim: "the highest measured cost per task: $14.19".
   Why it matters: a public, leaderboard-shaped instantiation of the estate's
   cost-per-blind-point champion metric (lens/laws.md:43). 5 index points spread across
   a 13.6x cost spread is a direct external stress test of the routing-class table
   (14/17 at 2-4 percent of dollars, lens/laws.md:41-45): the pattern holds or the
   premium dollar is buying harness effort, not score. Also Q1: effort level (max vs
   xhigh) is the visible cost dial in their table.

2. Unblocked: agent loops Anthropic -> GLM (Sep 24, IN window; upgrade of a prior
   snippet-only low bank)
   https://x.com/BrandonWaselnuk/status/2103156267246334157
   Article: per-token math promised 95 percent savings; per-task production delivered
   68 percent (GLM burns more tokens per task: more tool calls, more exploration, more
   errors). Unit costs: code review $0.089 -> $0.027/call; search $0.052 -> $0.029.
   "OpenAI-compatible" providers diverge on reasoning formats, cache keys, structured
   output, and usage accounting, with silent failures; they built a conformance suite +
   deterministic adapter. Budgets tuned to one model's behavior do not transfer.
   Verbatim: the serving/measurement work "turned out to be the actual migration".
   Why: this is the single most on-point external read for Q2 (the six hand-rolling
   fire surfaces are exactly "budgets tuned to one model") and Q3 (per-task vs per-token
   is the cost-per-blind-point argument won in production). Overlap: the estate already
   holds the raw fxtwitter JSON (catalog rows f9a08c399676 + e5049fafc054, banked
   2026-10-03) but digested it only as a snippet-only LOW row in
   frontier_olm_2026-10-03/sweep/kv-cache-and-context-engineering-x.md:205,314; the
   article-body numbers and the budgets-do-not-transfer law were not extracted until
   this read. This sweep banks the upgrade, citing the prior row.

3. NVIDIA/MIT harness-cost halving, as posted by 0xCodila (Oct 3, IN window)
   https://x.com/0xCodila/status/2106451735715737913
   Claim shape (post's claims, not independently verified by me): inspect execution
   logs for wasted tokens; four fixes survived: fuse edit+test into one tool call;
   compact context at completed steps only when savings justify it; archive large
   outputs as handles/excerpts instead of replaying them; delegate log reading to a
   cheaper model with verification. Verbatim: "50-54% lower API costs than native Codex
   and Claude Code on EdgeBench". Also 45-49 percent fewer tokens at ~94 percent score
   vs Pi. Cites arXiv 2603.23420 (Bilevel Autoresearch) + github.com/karpathy/autoresearch.
   Why: Q2's bleed-surface question, answered from outside: the named bleed surfaces
   are unfused tool round-trips, mistimed compaction, replayed large outputs, and
   premium-rate log reading. Every one of the six estate fire surfaces
   (lens/laws.md:154-158) should be grepped for those four shapes before wiring the
   guard. Caveat banked with it: promotional Substack-adjacent post; treat numbers as
   claims to replicate on estate instruments, not as verified.

4. MossAI: hidden reasoning billing (Sep 17, IN window)
   https://x.com/MossAI_Official/status/2100602112535339052
   Article "You Are Paying for Tokens You Will Never See" (title verbatim): reasoning
   tokens billed invisibly as output; a request can burn its entire budget inside the
   reasoning phase and return nothing, with tokens already consumed. ~119.5K views.
   Sources cited in-article: OpenAI token/reasoning/pricing docs, Azure billing Q+A,
   Anthropic caching docs.
   Why: Q1 + Q5 junction. The burn-with-no-output failure is EMPTY_REASONING's money
   shape (lens/laws.md:64-66): the terminal-marker/skip-on-sight law exists precisely
   because refire after an empty-but-billed reasoning pass pays twice for nothing. The
   article is a vendor marketing surface (sells a "Model Max" relay), so the billing
   mechanics are the steal, not the product.

5. Blackwellboy: "Qwen 3.8 27B is not one number" (Aug 19, OUT of window by 20 days,
   flagged, banked for load-bearing relevance)
   https://x.com/Blackwellboy/status/2090089804121907333
   Verbatim: "Qwen 3.8 27B is not one number. Same weights, wildly different results
   depending on reasoning, runtime, context, quant and serving stack." Days of testing
   across 5 DGX Sparks + RTX 5090; article + repo (github.com/Blackwellboy/
   qwen38-27b-is-not-one-number). Reported findings: BF16/FP8/NVFP4 within ~1 point on
   GSM8K/IFEval; 262K configured vs ~42K realized KV capacity; throughput 72-151 tok/s
   on the same 5090 by serving stack; enable_thinking=false gave zero reasoning
   leakage; a cheaper reasoning mode can sometimes cause more retries.
   Why: Q1's conditions law (a verdict without its conditions is not a verdict,
   lens/laws.md:25-27) has an external twin: same weights, different economics by
   serving stack. The "cheaper reasoning mode causes more retries" row is Q5's exact
   question (which lane bleeds retrial tokens) measured by someone else's instrument:
   thinking-off savings can be eaten by refire loops. KV configured-vs-realized gap
   feeds the kv-cache lane's standing seam.

6. Tom Turney: Qwen3.8-27B offlabel audit (Aug 14, OUT of window by 25 days, flagged)
   https://x.com/no_stp_on_snek/status/2088375653162717680
   Verbatim: "Everyone's cranking reasoning to max on the new models. On Qwen3.8 that's
   the setting that makes it lie to you." Article: best-in-class integrity ~37/40 at
   default; raising reasoning_effort to xhigh DEGRADED truthfulness and code judgment.
   Three serving-config traps: default xhigh, silent medium no-op, preserve_thinking
   replay. Turns report finish_reason: length after only ~2,900 of a 32,768 generation
   budget (verbosity-driven silent context exhaustion with a misleading signal). Full
   writeup at github.com/TheTom/offlabel (models/qwen3.8-27b.md).
   Why: Q5 (the finish_reason:length trap is the misleading-truncation cousin of
   EMPTY_REASONING classification; the estate's classify_empty reads finish_reason,
   RIB_INFERENCE_BUDGET_20261001.md:54) and Q2 (the knob is not monotonic: more
   thinking can be worse AND costlier; the guard needs per-animal knob semantics, which
   is the estate's per-animal-gates law restated by an outsider). Flagged stale because
   its subject (Qwen3.8-27B) is not the estate's current fleet.

7. Relace serving DeepSeek v4 Flash with thinking off (Aug 24, OUT by 15 days, flagged)
   https://x.com/EBorgnia/status/2092028169704571202
   Verbatim: "Relace is now sustainably serving Deepseek v4 Flash almost 2x cheaper
   than anyone else on OpenRouter."
   Why: Q1. A production vendor is pricing a thinking-off DeepSeek v4 Flash serve as a
   distinct, cheaper product tier; thinking-off is not just a request param but a
   serve-level economics lever. Context for the owed d4 three-arm re-measure
   (lens/laws.md:28-30, 149-153): the market is already splitting the arm.

8. Featherless carries GLM 5.3 Flash (Aug 28, OUT by 11 days, flagged)
   https://x.com/FeatherlessAI/status/2093130189085532645
   Verbatim: "Ox Alpha is out of stealth. Introducing GLM 5.3 Flash: Z AI's 320B
   natively multimodal MoE model" (18B active; 5x cheaper than GLM 5.2 on Featherless).
   Why: Q4. The estate's workhorse (glm-5.3-flash) is on the Featherless roster the
   28.6k-row gap question (lens/burns.md:214-215) is about; post-Lightning cool-pool
   composition (lens/burns.md:46-49) can sense on the same animal the paid tier judges
   with. Thin delta (the estate already holds 785 GLM-5.3-Flash catalog rows), banked
   for the one new fact: availability + the 5x-vs-5.2 price relation on Featherless
   specifically.

## Answers the public record gives the five research questions (and what stays owed)

- Q1 (thinking OFF vs ON re-measure, superseding rows): external evidence says the
  off-state is materially cheaper (Relace serve tier, item 7) but NOT free of traps:
  thinking-off can INCREASE retries (item 5) and billing can hide reasoning burn
  (item 4). The d4 three-arm re-measure itself is an estate instrument; NOT run here.
- Q2 (guard wiring, six surfaces, highest bleed surface): external bleed-surface
  taxonomy from items 2 and 3: unfused tool round-trips, mistimed compaction, replayed
  large outputs, premium log reading, plus provider-divergent usage accounting. The
  measured bleed number per surface is an estate instrument; NOT run here.
- Q3 (funded-tier cost-per-blind-point; routing-class table): item 1 is the public
  twin of the metric (score per dollar per task); item 2 is the per-task-vs-per-token
  caution won in production (95 promised vs 68 delivered). The estate's own post-402
  cost-per-blind-point from usage.jsonl is an estate instrument; NOT run here.
- Q4 (Featherless roster gap, cool-pool composition): item 8 is the only in-scope
  public delta found; the paged re-pull itself is an estate instrument; NOT run here.
- Q5 (EMPTY_REASONING incidence, drip-not-burst transfer, retrial lane): items 4, 5, 6
  give the failure shapes (billed-but-empty, retry-amplifying cheap modes, misleading
  finish_reason). The 2026-10 incidence scan across funded/free lanes is an estate
  instrument; NOT run here.

## Overlap ledger (grep evidence, run this sitting)

PowerShell Select-String over catalog/catalog.jsonl, memory/rib/*, memory/burns/
LEDGER.jsonl, memory/frontier/allowance.jsonl (script .tmp_sweep_deep/overlap_grep.ps1):

- ArtificialAnlys / "Coding Agent Index" / MossAI / Blackwellboy / "not one number" /
  no_stp_on_snek / preserve_thinking / EBorgnia: 0 catalog, 0 rib, 0 ledger. NEW.
- Waselnuk: 2 catalog rows (the 10-03 raw JSON pair); banked LOW snippet-only at
  kv-cache-and-context-engineering-x.md:205,314 (read this sitting). This sweep
  upgrades it; numbers first-time extracted.
- Karpathy: 3 catalog rows (maestro-cue-karpathy-loop.md in mined RunMaestro repo;
  watch/INTAKE_KARPATHY_HARNESS_BAIT_20260903.md). The loop concept is KNOWN; the
  codila post's delta is the four surviving fixes + EdgeBench claims, not the concept.
- GLM-5.3-Flash: 785 catalog + 7 rib rows (heavily known); Featherless: 10 catalog +
  7 ledger rows (roster instrument terminal per lens/burns.md:54-58). Item 8 banks
  only the availability/price-relation delta.
- reasoning_effort: RIB_INFERENCE_BUDGET_20261001.md:106,111 (the guard's own knob
  families) and RIB_MODEL_GARDEN_ROUTING.md:227. Item 6's xhigh-degrades finding is
  external evidence ON that knob, not a duplicate of it.
- finish_reason: RIB_INFERENCE_BUDGET_20261001.md:54 (classify_empty reads it). Item
  6's finish_reason:length-at-2900-of-32768 trap is the external failure shape.
- Today's sibling sweeps (watch/inbox/frontier_olm_2026-10-08/sweep/*.md): only one
  incidental "GLM 5.3 Flash" mention (open-local-models-hn.md:221, a commenter
  ranking); zero collisions with the 8 items.

## Not run / not found (no fabrication)

- The five research questions' estate-instrument legs (d4 three-arm re-measure, guard
  wiring into the six carriers, usage.jsonl cost-per-blind-point summation, Featherless
  paged re-pull, EMPTY_REASONING incidence grep) were NOT run: this seat is the public
  X door; another lane owns the instruments. All five are marked NOT RUN above.
- Profile-page candidates (paddix, ttunguz, thejoyrises, synthoraihq, josheganai,
  LangChain/all) could not be resolved to single status IDs through search this
  sitting; their snippets are recorded in the Pass 1 ledger and NOT banked as items.
- X article URLs cannot be fetched without login; article content reached me only via
  the fxtwitter article embed on their carrier posts. kirillk_web3's ~$0.94/task and
  the harness-router Pareto article are therefore snippet-only, unbanked.
- The 0xCodila post's NVIDIA/MIT attribution and EdgeBench numbers are the post's
  claims; the arXiv paper itself was not fetched this sitting.
