# Frontier sweep: inference-efficiency via reddit (2026-09-30)

Seat: sweep gopher (reddit lane), frontier_olm 2026-09-30. Estate map served: driving-ladder routing
(memory/rib/RIB_DRIVING_LADDER_20260928.md), tier laws, cost_ledger accounting, offpeak/janitor
deployment. Everything below was read or run this session; anything else is marked OWED.

## Door status (degraded - the recipe's primary doors are dead from this seat)

- old.reddit.com/r/*/top.json (4 subs) -> Reddit "Welcome to Reddit" login-wall placeholder, no JSON.
- old.reddit.com/r/LocalLLaMA/top/.rss -> same login wall.
- www.reddit.com/r/LocalLLaMA/top.json -> HTTP 403 Blocked (WebFetch).
- old.reddit.com thread HTML -> login wall. api.reddit.com/... -> HTTP 403 Blocked.
- Bash curl -> status 000, no remote IP: this sandbox has no direct outbound network.
- WORKING DOOR: Z.ai webReader against the redlib mirror redlib.catsarch.com (full threads, dates,
  comment authors). Later fetches intermittently hit the mirror's Anubis bot-check interstitial
  (1tbftlt, 1sc157b) - those threads were NOT read and are NOT banked.

## Pass 1 - broad sweep (~45 candidates from site:reddit.com searches; 7 query families)

Speculative decoding: 1w1je5d (spec-decode-eyes, Aug 29 '26), 1stcer1 (Qwen-3.6-27B spec decode),
1sq7grd (665% vLLM), 1h77m6u (llama.cpp tuning), 1gzm93o (spec decode lands in llama.cpp server),
1k0tkca (5000 t/s 2x3090), 1rpb1o7 (500 t/s 2x5090), 1sl18tj, 177ghdu. Continuous batching:
1vh9lx4 (vLLM C++20 port, block-paged KV + prefix caching), 1sdpxii, 1d92lau, 1p74jua, 1sj4c0x,
1w4i2id (prefill-vs-decode, ~Sep 1 '26), 1net6u3, 178j1vr, 1adr3l2, 1bnw7om. Paged attention/KV:
1qeley8 (vLLM-MLX), 1sc157b (Monarch v3 KV paging, NOT read - Anubis), 1uueuks (5090 parallel
sessions), 1dfvp4y, 19934kd (SGLang), 1n9tyle. Early exit: 1gf1rd1 (Meta LayerSkip, 2024-era).
Rate limits: 1r7xyi1 (Claude rolling windows), 1tub8oc (Spotify rolling 30s), 1r2by14. Power/energy:
1ru1g23 (France power math), 1qmrjlh (power off?), 1o528nk (idle watts), 1jc1nw1, 1fo744s, 1e8a7qd,
1j38265, 1eiwnqe, 1hh0gik, 128b5k0. LocalLLM: Qwen3.6-35B-A3B 113 t/s on 3090 thread (search-door
only, URL not resolved). Recency note: the top-month searches surfaced mostly pre-window classics;
only 1w4i2id (~Sep 1) is squarely in the last 30 days; 1w1je5d (Aug 29) is 2 days outside. Dates are
reported per item, never rounded.

## Pass 2 - deep reads (5 threads read end to end via the redlib mirror; quotes verbatim)

1. 1w1je5d "If your t/s is low enough, you can see speculative decoding with your own eyes"
   (r/LocalLLaMA, Aug 29 '26, u/IndependentBudget951, 153 pts, 13 cmts). OP measured DeepSeek4-Pro
   distill MTP/n-gram speculative decode at 2-3 t/s base: bumps exactly on predictable phrases.
   saltexx: "speculation pays out in proportion to how bandwidth bound you are, since verifying k
   drafted tokens reads the weights once instead of k times" - with 4 drafted tokens, ~1.9 tok per
   verify step at 50% acceptance, ~3.4 at 80%. General_Service_8209: llama.cpp implements n-gram
   speculative/MTP (docs/speculative.md#n-gram-cache); TensorRT's n-gram draft "nearly doubles tokens
   per second" optimally. BigYoSpeck caveat for us: n-gram shines in chat interfaces, but "In a real
   agent harness where it should be making diffs it doesn't do much."
2. 1w4i2id "Why is prefill unbelievably faster in vLLM than other inference engines?" (~Sep 1 '26,
   in-window). 486f46cf: "Prefill processes all tokens in parallel using large matmuls, while token
   generation is sequential and bandwidth-bound." Reasons given: continuous batching, paged KV
   allocation, no host syncs, graph capture; llama.cpp still wins single-stream token-gen. Direct
   read for the estate: janitor cycles (single stream) stay llama.cpp; vLLM-class batching pays only
   at fan-out (the 12-agent workflow shape).
3. 1uo32yw "Qwen 3.6 27B - VLLM Performance Benchmark Results (BF16, FP8, NVFP4)" (Jul 05 '26,
   u/live4evrr). Measured tables: FP8 decode ~= BF16 decode at half VRAM; prefill scales with
   compute, decode is bandwidth-bound (27B FP8: ~3988.83 tok/s prefill vs ~161.02 tok/s generation
   on 3x R9700 96GB). TripleSecretSquirrel, batched agents on one R9700: "roughly 5x the tokens per
   second" vs single-stream llama.cpp at 12 concurrent agents / 50k context, "runs over night where
   electricity is cheap."
4. 1ru1g23 "Self hosting, Power consumption, rentability and the cost of privacy, in France"
   (Mar 15 '26, u/Imakerocketengine, 35 pts, 46 cmts). OP: dual-3090 rig 120W idle, 700-800W
   inferencing; French tariff arithmetic (Tarif bleu EUR 435/yr at a 20% duty cycle he calls
   "totally unrealistic"). lemondrops9: 3090 power-capped 250W vs 350-400W = "little difference in
   speed" (~5% speed cost for ~30% power). ekojsalim: "Undervolting and a slight memory overclock
   can save ~10% (or more) power consumption without sacrificing throughput." Grouchy-Bed-7942:
   Strix Halo 8-9W idle, ~110W peak; GX10 auto-shutdown after 10 min idle.
5. 1r7xyi1 "Claude API Error: Rate limit reached?" (r/ClaudeAI, Feb 18 '26, u/Responsible-Ad-5024).
   OP relays Anthropic's own explanation: token-bucket model, "limits are enforced as continuous
   rolling windows, not fixed resets"; a burst can drain the per-minute bucket while hourly/weekly
   budgets look fine; parallel instances share one pool; read the anthropic-ratelimit-* headers to
   see which bucket was hit (Blitz28_).

Not banked (not read - Anubis wall or truncated fetch): 1sc157b Monarch v3 KV paging (78% claim),
1tbftlt vLLM-for-single-user, 1qmrjlh power-off thread, 1gf1rd1 LayerSkip.

## Estate grounding run this ask

- Cost ledger: `./.venv/Scripts/python.exe` aggregation over training/cost_ledger.jsonl: 2,439 rows,
  0 parse failures. deepseek: 494 calls, $126.5630, 127 success / 367 fail -> $0.9966 per success.
  ollama: 1,765 calls, $0.0055 total, 458 success / 1,307 fail (26%) -> ~$0.000012 per success.
  glm 44 calls and grok 32 calls: all fail, $0.00 (unpriced/failed rows). Ledger keys already carry
  value.usd_per_leaf and actual.cache_hit_tokens/cache_miss_tokens - the instrument exists; it has
  never been exercised on the Nous tier (COST_TRUTH_20260930.md:12 "all Nous-model spend is $9.05
  lifetime, all of it since 2026-09-29").
- Q2 verdict: the funded-vs-local cost-per-correct-verdict crossover is OWED. Greps for
  "crossover" and "per verdict/per-correct/cost per correct" across memory/, corpus/, docs/,
  training/ found only the 2026-08-09 cache-aware-batching pack's ASK-SHAPE crossovers (stack >=2
  asks on DeepSeek 50x, 4-6 asks on grok 4x; memory/research_packs/20260809T021009Z pack) and run
  logs - no tier-vs-tier cost-per-correct-verdict computation anywhere. Two gaps make it OWED, not
  just undone: (a) outcome.success is task success, not verdict correctness, so "per correct" is
  unmeasured on both tiers; (b) cost_ledger.v1 carries no wave/corr tag (COST_TRUTH_20260930.md,
  unknown #5). Closest bytes: local = ~free USD at 26% success; funded deepseek-era = $0.9966 per
  success; lifetime $135.88 in-rollup / ~$137.10 true (COST_TRUTH_20260930.md:17).
- Q5 verdict: partial hold, re-measure OWED per the ONE-BUG law (laws.md:18 ->
  RIB_DRIVING_LADDER_20260928.md:53-77). The deliberate-ask shape is live-measured in-house on the
  z.ai/GLM lane: EXP-A (mag/_exp_a_cache_retrigger.py, 08-29) measured 5.3-flash at 99.52% cache hit
  (7040/7074) on a byte-stable ~7K prefix with thinking on, novel-prefix controls 0%
  (docs/ref/ZAI_API_EXPERT_REFERENCE.md:59). But the dollar multiplier is NOT DeepSeek's 50x/120x:
  z.ai cached input = "50% of standard input price" (same doc :54, :148), so the DeepSeek-era
  $161->$3.60 (~45x) becomes roughly ~2x on z.ai at the same hit ratio. grok-4.7 DOES cache
  (cached_tokens 1152/1561 = 74% on the luncheon run, watch/inbox/GROK47_LUNCHEON_INTEL_20260929.md:3)
  but its cached-price discount is unmeasured in estate bytes. The $161->$3.60 figure itself is a
  DeepSeek-era instrument reading (RIB_SELF_MY_EFFICIENCY.md:6-9, "cache-router-measured"); its
  ratio-form (hit-ratio is the cost lever) transfers; its dollar-form does not. Re-measure on
  glm-5.3-prime + grok-4.7 with instrument/moment/context named; also settle the Nous balance
  question (402s vs ~$171 rib arithmetic; only the portal decides, COST_TRUTH_20260930.md:94).
- Q3 verdict: shape-match, no provider model published. The estate's measured envelope (AGENTS.md
  fan-out width law: "the limit is rolling throughput, not width-only"; receipt
  watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md:69,82 "Rolling throughput is the binding
  constraint after any burst") matches the published heavy-user model found on reddit (Anthropic
  token-bucket rolling windows, thread 1r7xyi1) and the Spotify rolling-30s-window report (1tub8oc,
  search snippet only). No z.ai/Nous/xAI-SD specific rate-limit model surfaced -> that piece is
  OWED. The 1302 error family the estate sees is z.ai-side; no public doc for it was found this ask.
- Q1 verdict: measured-with-receipts at janitor scale on consumer hardware in 2026 = speculative
  decoding (n-gram/MTP in llama.cpp; bandwidth-bound payoff math; thread 1) and continuous batching
  (5x at 12 concurrent agents on one R9700; thread 3; engine mechanics thread 2). Paged attention
  was invoked everywhere as the reason vLLM wins at concurrency but no in-window measured
  consumer-Windows paged-attention receipt was read; early exit (LayerSkip) had no 2026 reddit
  receipt (engine-support caveat in the 2024 thread; llama.cpp discussion #10787 open). Both are
  thin/OWED for our exact shape.
- Q4 verdict: the energy/time ceiling is self-imposed, not thermodynamic: overnight duty at 150-250W
  power-capped is single-digit dollars/night at US rates (thread 4 arithmetic), undervolting is a
  free ~10%, power-capping a ~5%-speed ~30%-power trade. At the estate's real workload scale
  (janitor scut at 26% success, 9.34s test suite, offpeak pile classification) the complexity that
  pays is: (1) llama.cpp n-gram/MTP speculative decode for chat-shaped janitor outputs, skipped for
  diff-shaped agent outputs (thread 1 caveat); (2) continuous batching ONLY for the 10-12-wide
  workflow fan-out shape (thread 3), not single-stream janitors; (3) power-cap/undervolt the box;
  skip vLLM-class serving stacks entirely at our concurrency-of-one-per-model.

## Overlap check (run this ask)

catalog.jsonl: 0 hits on every thread-specific phrase ("speculative decoding with your own eyes",
"VLLM Performance Benchmark", "prefill unbelievably faster", "continuous rolling windows",
"rentability", "KV paging", "Qwen 3.6 27B", "bandwidth bound"); generic "n-gram" = 2 unrelated rows.
memory/rib + memory/research_packs: no hits for "speculative decoding", "continuous batching",
"paged attention", "rolling window"; "early exit" matches one unrelated pack
(20260808T_steiniger-model-manipulation). One echo: memory/trajectory/steps.jsonl matched the
thread-1 phrase (session trajectory of this wave, not a holding). Nothing re-banked.

## Addendum - late-completing overlap grep (run 2026-09-30, after the SweepResult was accepted)

A final broader-tree grep (all of memory/, not just rib + research_packs) added three facts that
refine but do not overturn the overlap fields above:

1. `grep -c "speculative" catalog/catalog.jsonl` = 2: the catalog holds 2 rows containing the
   generic word; the thread-specific probes ("speculative decoding with your own eyes",
   "bandwidth bound", "nearly doubles tokens per second") still returned 0 files.
2. "rolling window" DOES appear outside ribs/packs: memory/improve/design_CLIMB_ore_pipeline_20260912.md,
   memory/runs/batch5_20260906/TOKEN_METER_20260906.md, memory/runs/compaction_eval/steps_frozen_20260920.jsonl,
   and two mimosa hook-state baseline blobs. The estate has its own rolling-window language; the
   Claude thread's token-bucket framing is still not held anywhere as a provider rate-limit model.
3. The phrase "Qwen3-Coder-Next" (from thread 4's hardware comment, the 2x5060 Ti rig running it at
   ~863 t/s prompt eval) matches a row in catalog/catalog.jsonl (plus file_dogfood manifest,
   hermes_zoo census, quote_audit inbox_concat, trajectory steps). So item 4 has a PARTIAL content
   adjacency on the model name; the thread's power-economics content itself (rentability, watts,
   tariffs, undervolting) remains unheld (rentability probe 0, rib/pack probes negative).

## OWED ledger (from this sweep)

1. Funded-vs-local cost-per-CORRECT-verdict crossover table (needs verdict-correctness on local
   successes + corr_id/wave tags in cost_ledger.v1 per COST_TRUTH unknown #5).
2. Deliberate-ask dollar re-measure on glm-5.3-prime and grok-4.7 (EXP-A covered 5.3-flash only;
   grok-4.7 cached-token discount unmeasured).
3. z.ai/Nous 1302/429 rate-limit model (rolling-window parameters) - no public source found.
4. A measured consumer-Windows paged-attention receipt (vLLM-class) if the fleet ever exceeds
   janitor concurrency 1.
