# SWEEP: inference-efficiency via reddit (frontier_olm_2026-10-04)

source-fetched: 2026-10-04. Lane owner: sweep-inference-efficiency-reddit (workflow gopher).
House laws held: ascii only, no em or en dashes, every claim cites what was read or run this
sitting, quotes are verbatim from fetched pages, overlap is stated never silently re-confirmed.

## 0. Door status (do not rediscover)

- The ask's named door (old.reddit.com/*/top.json) is BLOCKED to this fetcher: four probes
  (r/LocalLLaMA top.json x2, r/LocalLLM top.json, top/ HTML, thread .rss) all returned the
  "Welcome to Reddit" block page this sitting.
- WebSearch fallback fired once and came back degraded (backend 1302 rate-limit storms, no raw
  reddit URLs), matching burns.md:110 "WebSearch intermittently rate-limited".
- Working engine, re-certified live this sitting per burns.md:107-111: the Arctic Shift archive
  API (arctic-shift.photon-reddit.com /api/posts/search + /api/comments/search?link_id=...).
  Empirics this sitting: date-string after= accepted, epoch after= 422s, quoted phrases 422s,
  `after` is IGNORED on title searches (a 2026-08-01 post slipped through an after=2026-09-04
  query), and the API throttles bursts with 422 (observed twice; cooled in 2 to 5 min).
- burns.md:107 said "thread permalinks via .rss endpoints" work; that variant is DEAD to this
  fetcher this sitting (old.reddit.com/r/ollama/comments/1wq9ipm/.rss = block page). Recorded so
  the next lane does not re-trust it on my say-so or burns.md's.

## 1. Pass 1: the candidate pool (40+ in-window items, all read at title/metadata level)

Title searches over r/LocalLLaMA (Arctic Shift, all-time results date-filtered by me):
- tokens+per+second: 2 hits, both August (out of window): 1wp7zyb (235/166), 1wkgb2h (135/20).
- vllm (11 in-window): 1wvt1m4 (125/116, Ascend), 1wtg12r (49/37, RAM offload), 1wrpajn
  (20/63, llama.cpp vs vLLM), 1ww6750 (12/7, SGLang/vLLM recipes), 1wuvu86 (14/14), 1wullxh
  (10/24, tp=6 padding), 1wtyc4y (shared-prefix batch), 1wvjqy8 (JEV grammar enforcer),
  1wqcki2 (26/2), 1wqokwd (1/2), 1ww5zaa (1/0).
- router (6 in-window): 1ww98tb (10-02, version drift), 1wva34v (10-01, ZeroSpend $0 router),
  1wkptdb (09-19, next-skill-router), 1wq4j6g, 1wdwhu0 (09-12), 1w7uoxa (09-06).
- quant (15 total, 3 in-window big): 1wgszma (328/40, Voodoo Dynamic Quant MIT, 09-15),
  1wa5dp9 (206/60, task-aware quant, 09-07), 1w7w2lv (2/31).
- free+tier (1): 1w7zt57 (09-05) body [removed] by moderators; cannot read = cannot bank.
- 429 (0 title matches), RouteLLM (0 title matches), cascade (422-throttled, unresolved).
- OpenRouter (9 in-window): 1wgwe4n (826/105, CrofAI exposed, 09-14), 1wnu53i (100/49),
  1wba2eu (4/38, DSV4 Flash low price, 09-08), 1whsqh7 (Kimi K3 20 endpoints priced, 09-15),
  1wj9g7m (0/9, Stealth Union Alpha, 09-17), 1wpv7pg (DeepSeek 25.3 pct of OR requests),
  1wloeeb, 1wf6np5, 1wawc8k.
- Newest-hours window (score still accruing, saved for structure): 1wxqz4g Spite (custom
  inference-engine vision), 1wxqoa3 (GLM-4.7 MXFP4 vs Q4_K_M Vulkan iGPU), 1wxqmaa (Strata vs
  NVFP4 quants), 1wxpvys (QFN llama.cpp squeeze), 1wxncki (Blackwell 6000 96GB optimization PR),
  1wxm2og (LLM Inference Dashboard, 64MB local), 1wxoqqp (kNN cache in front of Jev, author
  post), 1wxlw2c (LFM2.5 vs MiniCPM5 agentic), 1wxloam (decision models benchmark).
- r/ollama window: 1wq9ipm ("Watched my LLM router burn $11 on a 3-word prompt"), 1wqxbwa
  (25/11 Mac app), 1wqxm5z (Gemma 4 E4B split M4+3060 over Wi-Fi).

## 2. Pass 2: deep reads (8 threads opened end to end; 7 usable, 1 dropped)

Every read below went through /api/comments/search?link_id=<id> (limit 50-100) this sitting.

### 2.1 1wgwe4n: CrofAI "cheapest inference provider" exposed as a fake-name reseller (826/105, 09-14)
A leaked backend dump (via the vendor's own Discord) showed a reroute table and
`internal_model_name` plumbing: one model served under another's name, plus a passthrough
leaking that they proxied an OpenRouter feature. Refunds limited "for the value of the
company"; Discord locked down after. Verbatim from the fetched page: "The scary part isn't
even the markup, it's that the 'cheap inference' was apparently just a different model wearing
a fake name." Estate fit (Q2): the routing grid's instruments-only law
(memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53) is not paranoia, it is the exact failure mode:
a public price column can be real while the quality behind it is a different animal, which is
the fingerprint-change law (memory/rib/RIB_MODEL_GATES_20261001.md:63-67) wearing a vendor.

### 2.2 1wba2eu: "DSV4 Flash 0731 on OpenRouter. Why is the price SO LOW" (38c, 09-08)
Commenter explanations with numbers: batching/concurrency economics ("concurrency. hosted
models pass the weights through memory once for many users at a time. batching. when it's
just you at home, inference is much more expensive."), DSV4 Flash's unusually small KV cache
as a serving-cost lever, energy ~5 J/token single vs under 1 J/token at 8+ batch, Artificial
Analysis 35 vs 42 (DS Flash 0731 vs qwen3.8-flash-next). Trust side: provider roulette (top
comment: providers slipping into Chinese, failed tool calls, dropped prefix cache; "Digital
Ocean as a DSv4 provider produces tokens worth less than the bandwidth used to transport
them"), one provider at ~12 tok/s unusable for agents, hidden quant differences, three model
names one backend (no real fallback), cache-hit pricing economics (sort by cached price;
~80 pct best-case OR hit rate vs 95-98 ideal). Estate fit (Q2 + Q5): public data fills the
price/latency columns of the grid; the quality/quant columns stay UNMEASURED until a funded
probe fires, exactly the fill procedure at RIB_MODEL_GARDEN_ROUTING.md:202-209. Also a Q5
hint: KV-size is a per-model serving-cost constant worth reading off the estate's own
janitors before renting.

### 2.3 1wrpajn: "is switching from llama cpp to vllm worth it" (20/63, 09-07)
Decision table from the comments: vLLM wins on multi-user/agent serving, consistent decode at
large context, prefix caching (APC cut agentic prefill from minutes to 0.2-2 s), 20-30 t/s
faster on Qwen 3.8 27B, "three times the PP performance and double the TG on Qwen 3.8 27B at
Q8/FP8". llama.cpp wins on MoE RAM spill (512 GB boxes), mismatched-VRAM GPUs, GGUF/k-quant
day-0, Windows (vLLM unreliable; Linux or WSL2). Verbatim: "switch if you're serving multiple
users or agents and want consistent decode and prefix caching; don't if you're a single user
who likes trying new models." Estate fit (Q5): the janitor fleet (gemma:2b/gemma4/qwen2.5:7b,
single-seat, bursty) sits in the stay-on-llama.cpp column; the batch lanes (ds_workhorse
shape) are the vLLM-shaped exception. The prefix-cache number is the estate's own
cached-tokens law in another register (RIB_SELF_MY_EFFICIENCY.md:5-14 measured 6.5 to 98 pct
cost on the API side; this is the local-serve side of the same curve).

### 2.4 1wtg12r: "RAM Offloading with vLLM - tcclaviger appreciation post" (49/37, 09-09)
Expert-to-RAM offload for vLLM lives in a fork (tcclaviger), not mainline; AMD-focused; the
original-weights case "needs at least 96 GB of RAM"; llama.cpp's CPU-resident embedding trick
"saves 1GB on qwen 3.8 27B on Q4"; maintainers reject such PRs over server-focus and flag
burden; offload breaks vLLM's single optimized graph (DRAM vs PCIe bottleneck raised).
Verbatim (OP): "No, vLLM is usually much faster than llama.cpp, but more complicated to get
vLLM working, and previously no RAM offloading support." Estate fit (Q5): the consumer-box
offload lane exists but as a fork with merge risk; for the estate's free-2GB-RAM launch gate
(memory/rib/RIB_MODEL_GATES_20261001.md:54-56) the applicable lever today is the llama.cpp
embedding-offload class, not the vLLM fork. Tension recorded: 1wrpajn commenters say vLLM
"can't offload weights well"; this fork is the counterexample; both are true (fork vs
mainline).

### 2.5 1ww98tb: "writing a router to split local/remote LLMs, model updates killing me" (8c, 10-02)
Pain: routing decisions target a stale snapshot after silent upstream updates (GLM 5.2 to
5.3, DS Flash 0731); fixes offered: pin a version per endpoint and treat a version change as
a model swap, re-run a ~50-prompt calibration on hash change, keep per-version
capability/latency/cost profiles, route on task features not names, confidence-threshold
routing (one ships 0.96 and retunes one number per release). Verbatim: "So the router kept
making decisions against a snapshot that no longer existed." Estate fit (Q2 + Q3): this is
the estate's verdicts-expire law (RIB_MODEL_GARDEN_ROUTING.md:54-57) and
fingerprint-change-is-a-new-animal law independently rediscovered, and it prices the MINIMAL
funded probe: ~50 asks per fingerprint event, not a full battery. The 8-item battery
(RIB_MODEL_GARDEN_ROUTING.md:202-209) already satisfies it.

### 2.6 1wq9ipm: "Watched my LLM router burn $11 on a 3-word prompt. Here's the fix" (r/ollama)
The OP selftext is NOT in the Arctic archive (comments-only thread there); the fix mechanics
come from the fetched comments: a retry/loop failure burned $11 on a ~3-word ask ("Fix this
issue" per one reply); the cure = complaint regex routing vague cards to cheaper models,
per-kind attempt caps of 2-3, and a daily circuit-breaker budget cap. Quote (verbatim
title): "Watched my LLM router burn $11 on a 3-word prompt. Here's the fix." Estate fit
(Q1 + Q3): this is EMPTY_REASONING-adjacent burn in the wild; the estate already owns the
stronger version (classify + TERMINAL per (ask, family) + two recoveries,
mag/inference_budget.py:1-20, RIB_INFERENCE_BUDGET_20261001.md:44-74) plus per-call banking
(mag/route_chat.py:16-25 banks every call including ok:false errors to
memory/runs/route_chat/usage.jsonl); what the thread adds is the TANK side: a daily
circuit-breaker cap on total spend, which the estate's per-call usage ledgers
(memory/runs/hermes_burn/usage.jsonl rows: ts, id, model, turn, prompt_tokens,
completion_tokens, cost_usd, ok, optional reasoning_tokens/channel) do NOT enforce today.
Schema fit: the ledgers already carry cost_usd per row, so a circuit breaker is a reader
over the existing schema, zero migration.

### 2.7 1wa5dp9: task-aware quant of Qwen3.8-27B hits 99 pct of bf16 for reasoning, not coding (206/60, 09-07)
Author (devildip): 99 pct of bf16 on general reasoning at heavy quant; "it doesn't hold up
for coding. This is domain specific for reasoning." Calibration 192 items; coding corpus 512
executable tasks from 256 specs; H200 at $4.50/hr, 12-18 h runs; several hundred dollars
spent. Skepticism in-thread: "benchmax-aware" overfit concern (author answers with held-out
sets), users could not reproduce one-shot coding below Q4_K_XL, a WebGL task looped.
Estate fit (Q5 + Q3): quant choice is question-class-dependent, which is the estate's
question-class routing law (RIB_ROUTING_CLASSES_20261002.md:11-16) landing in weight-space;
the reasoning-quant ladder probe (frontier_olm_2026-10-04/lens/burns.md:118 row 7 order)
should expect a coding-split, and the thread's own failure (quant looped on WebGL) rhymes
with the EMPTY_REASONING class. Cost datum: $4.50/hr H200 with 12-18 h = ~$54-81 per
calibration run, which prices the "task-aware quant for the janitors" moonshot.

### 2.8 1wj9g7m: "What is the Stealth Union Alpha on OpenRouter?" (9c, 09-17)
Not local (mod stickied off-topic), PAID: "$2.50 / $7.50 per 1M" input/output, identity
unknown, suspected router-blend: "The 'blend' is most likely just a router based on 'magic'
assigment of a target model. Or maybe they produced a real weights-based blend? unlikely."
(typo "assigment" is verbatim). Users quit over slowness. Estate fit (Q4 + Q2): the
estate's stealth-lane caveat bank gets an external rhyme: stealth-named endpoints on
aggregators are (a) possibly paid now, (b) possibly a router wearing a model name, i.e. the
CrofAI pattern with a price tag; never bank their output as trusted work, which is already
law (RIB_FREE_USAGE_POLICY_20260823.md:3-5).

### 2.9 DROPPED: 1wxoqqp (kNN cache in front of Jev, "numbers and two negative results inside")
Image-only post, 1 point, 0 comments; the numbers live in a PNG the archive cannot render.
Cannot read = cannot bank (the 10-03 kv-cache lane applied the same rule to [removed]
selftexts, frontier_olm_2026-10-03/sweep/kv-cache-and-context-engineering-reddit.md:44).

## 3. The five research questions, answered from THIS door only

1. Tank accounting schemas (burns.md probe): the only public per-lane schema observed this
   window is the r/ollama thread's fix stack (per-call rows + per-kind caps + daily
   circuit breaker, 2.6). The estate's ledgers already carry the per-call row (ts, id, model,
   turn, prompt/completion/reasoning tokens, cost_usd, ok); the missing organ is the TANK
   reader (sum by lane per day + breaker), not a schema. No migration needed.
2. UNMEASURED cells vs funded probes (laws.md): public cost/latency data (OpenRouter
   endpoint prices, Artificial Analysis scores, provider tok/s reports) fills PRICE and
   LATENCY columns only; every quality/quant cell stays UNMEASURED per the instruments-only
   law (RIB_MODEL_GARDEN_ROUTING.md:47-53), and the window's fraud thread (2.1) is the
   falsifier for why. Minimal funded probe set: the 8-item battery per family on every
   fingerprint event (~50 asks, 2.5), plus the already-owed probes 3 and 5
   (frontier_olm_2026-10-04/lens/burns.md:117).
3. RouteLLM-lineage curves vs the tier ladder: NO title match for RouteLLM this window and
   the cascade search was throttled unresolved; what the door DID return is the practical
   cascade shape (cheap-first + prefix cache + confidence threshold + version pins, 2.5 and
   2.3) matching the estate's ladder leg-for-leg. The seven unwired carriers
   (stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire,
   ds_workhorse, RIB_INFERENCE_BUDGET_20261001.md:100-114) gain one external datum: the
   1wq9ipm stack is the same classify-terminal-cap law in a paid harness.
4. Free-tier ceilings / rate-window decay (grid line 192 contradiction): NOT resolved from
   reddit this window. Zero title matches on "429", the one "free tier" hit is [removed],
   and the stealth-endpoint thread (2.8) says the stealth class may now be PAID. The
   contradiction (RIB_MODEL_GARDEN_ROUTING.md:186-192) stays open and can only close on
   estate instruments. The door could not measure it; nothing was fabricated to fill it.
5. Local janitor serving configs: measurable-without-hardware lifts found: prefix caching /
   APC (prefill minutes to 0.2-2 s, 2.3), Q8/FP8 on vLLM (3x PP, 2x TG on a 27B, 2.3),
   llama.cpp CPU-resident embeddings (~1 GB saved on a 27B Q4, 2.4), expert RAM offload
   (fork-grade, 96 GB class, 2.4), small-KV model choice as a serving-cost constant (2.2),
   task-aware quant with a coding-split warning (2.7). The estate's owed probe 5
   (qwen2.5:7b Q4_K_M vs q8_0 A/B, burns.md:117) sits exactly on this evidence and should
   fire before any of it is adopted.

## 4. Overlap ledger (grep evidence, this sitting)

- catalog/catalog.jsonl: 0 hits for all 8 ids and names (rg over catalog/, plus grep -c on
  catalog.jsonl for 1wvt1m4 1wtg12r 1wrpajn 1ww98tb 1wva34v 1wkptdb 1ww6750 1wp7zyb 1wa5dp9
  1wgszma ZeroSpend tcclaviger, all 0).
- memory/: 0 hits for the same set (rg -li, cleaned up after a slow grep -r was killed).
- Prior register (frontier_olm_2026-10-03/register.jsonl, the 42 anti-rebank rows): 0 hits.
- Prior-round candidate pools (frontier_olm_2026-10-03/sweep/): 1wtg12r + 1wtyc4y named in
  kv-cache-and-context-engineering-reddit.md:44 and :93 as NOT deep-read candidates;
  1wa5dp9 only as a smol.ai source mention in quantization-and-compression-x.pass0.md:22.
  No register row for any: deep-reading them was new work this round.
- Same-round sibling pools (this sweep/ dir): 1wba2eu, 1wq9ipm, 1wtg12r appear in
  _amc_reddit_harvest.jsonl and 1wa5dp9, 1ww98tb in _fta_reddit_harvest.jsonl as raw
  pass-0 rows; no sibling _thread_ file deep-reads any of them (checked by rg over
  _amc_thread_*.txt and _fta_thread_*.txt, 0 hits).
- Already-banked reddit ids this week (burns.md:93-98: 1wkorli, 1wjnklv, 1wgvfpr, 1wefk8o,
  1wavhij, 1w7umnd): none re-banked here; my ids are disjoint.

## 5. What this lane did not do

- No funded probes fired (this is a read-only sweep lane; probes 3 and 5 remain owed per
  burns.md:117).
- Cascade/RouteLLM lineage on reddit is unanswered this window (0 title matches, one 422):
  the arXiv door is the right door for that question, not reddit.
- The 1wq9ipm OP body is unreadable in the archive; its fix stack is comment-sourced and
  flagged as such in 2.6.
