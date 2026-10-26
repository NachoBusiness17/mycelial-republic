# Sweep: kv-cache-context-engineering via X (frontier_olm_2026-10-02)

source-fetched: 2026-10-02. ASCII only, no em or en dashes, every claim below was read
or run this sitting. Sweep gopher seat, one ask: two passes, bank only read items.

## Doors used and their condition

- X door: WebSearch with site:x.com queries. The first two queries surfaced zero x.com
  rows; the third ("KV cache" OR "context compaction") surfaced 10. The search backend
  threw intermittent MCP 429/1302 rate-limit bursts mid-query and self-retried clean
  each time; no query was lost.
- fxtwitter door: https://api.fxtwitter.com/<user>/status/<id> resolved BOTH article
  attempts (RampLabs, CompleteSkeptic) as HTTP 200 JSON carrying tweet text, article
  title, TLDR and engagement stats. Long-form article BODIES were not retrievable
  through it (matches the 10-01 lens note that X article paths degrade); quotes are
  from tweet text and TLDR only, stated per item.
- Fallback primaries reached and read: arxiv.org abs pages (2), github.com README (1),
  github PR page (1), arctic-shift.photon-reddit.com API (1), hn.algolia.com API (1).
  All clean, no 403s.

## Q1 verdict: KVarN CONFIRMED, the llama.cpp kv-rotation clause now SOURCED

The 10-01 fold banked KVarN UNCONFIRMED with its llama.cpp clause UNSOURCED and ruled
"do not repeat the clause until a concrete PR reference is produced"
(frontier_olm_2026-10-01/DIGEST.md:109-115). This sweep produced the reference:

- The arXiv abstract page (fetched this sitting) is real: "KVarN: Variance-Normalized
  KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks", Muller,
  Bich, Boretti, Chang, Zhuang, Cavigelli, submitted 2 Jun 2026, vLLM implementation
  at github.com/huawei-csl/KVarN. Neither abstract nor comments field mentions
  llama.cpp.
- The GitHub README (fetched): full vLLM fork (Apache 2.0, vLLM v0.23.0 base, 506
  stars), shipped preset kvarn_k4v2_g128 (4-bit keys, 2-bit values), Hadamard rotation
  along channels plus Sinkhorn-like variance normalization, AIME25 53.3 pct parity
  claims. No llama.cpp mention there either.
- The clause's public carrier exists: r/LocalLLaMA post 1s720r8 by Betadoggo_
  (created_utc 1774807042 = 2026-03-29), title verbatim: "In the recent kv rotation PR
  it was found that the existing q8 kv quants tank performance on AIME25, but can be
  recovered mostly with rotation". Selftext points at
  github.com/ggml-org/llama.cpp/pull/21038#issuecomment-4150413357.
- PR #21038 (fetched): "llama : rotate activations for better quantization", authored
  by ggerganov, merged to master Apr 1 2026. Rotates Q/K/V with a normalized Hadamard
  matrix before caching. AIME25 gpt-oss-20b low reasoning x8: F16 37.9 pct; Q8_0
  31.7 pct unrotated rising to 37.1 pct with rotation; Q4_0 2.0 pct to 21.7 pct
  (ggerganov quote: "the model completely breaks down - it cannot solve even 1
  problem" for unrotated Q4_0). ggerganov on q8_0: "there is some non-negligible
  quality benefit of applying the rotation here too (31.7% -> 37.1%)".
- HN comment 48739846 (story 48721903, fetched via algolia) corroborates
  independently: "Llama.cpp implemented some rotation optimizations for quantized kv
  cache to improve the preservation of attention quality", with the situational caveat
  that small differences can matter for long-form reasoning.

So: the paper is CONFIRMED from two fetched primaries (arXiv + GitHub), and the
clause is SOURCED (PR #21038 + 1s720r8). The 10-01 "do not repeat" ruling can be
upgraded by the burns lens. Still true: the KVarN paper itself never cites the
llama.cpp PR; "same family" is the sweep's own connection (both apply Hadamard
rotation to fix quantized-KV error), not an assertion either primary makes.

QUEUED ACTION STILL OWED: the 10-01 queued append of arXiv 2606.03458 to
memory/runs/corpus_gap_research/ARXIV_REGISTER.json has NOT been executed. Grep today
for "kvarn|2606.03458" against that file (5,618 rows) returned zero rows.

## Q2: degradation curves over long agentic sessions (the KV ladder surface)

- No post-10-01 method paper surfaced anywhere in this window. Nearest: ActKV
  (arXiv 2609.31395, action-guided KV compression for agentic inference) and AgentKV
  (arXiv 2609.14872, phase-aware eviction with compressed KV carried across turns),
  BOTH already rows in ARXIV_REGISTER.json (ActKV row 5417, AgentKV row 4694), so
  overlap, not new. CommitKV (arXiv 2608.07855, fetched) is lifecycle-aware KV
  compression via commit transitions for multi-turn ReAct agents, claims "higher
  accuracy than existing KV cache compression methods", but the abstract carries NO
  numbers; not banked (qualitative abstract only).
- The X-door economics frame that motivates the ladder: Diogo Almeida
  (@CompleteSkeptic) 2026-09-09 "(KV) Cache Rules Everything Around Me", TLDR: "The
  biggest cost to devs of an agent is re-reading its own context, which costs the
  provider close to nothing to serve."

## Q3: isolation / sandboxing responses for the shared-KV flaw class

No vendor fix or advisory responding to arXiv 2609.18526 (llama.cpp cross-tenant
state-restore flaw, banked 10-01 row 21) was found; searches surface the paper itself
and societyforaisecurity.com's summary, nothing from ggml. The response class lives
on the cache-sharing surface and in adjacent advisories:

- PrefixWall (arXiv 2603.10726, fetched): selective isolation. "PrefixWall monitors
  cache reuse across users, flags suspicious sharing, and selectively isolates
  prefixes", up to 70 pct higher cache reuse and 30 pct lower latency vs the
  sledgehammer disable-APC defense. This is the isolation blueprint for the estate's
  shared KV surfaces.
- Leads surfaced but NOT deep-read this sitting (snippets only): SafeKV (selective
  KV sharing with detection), the NDSS 2025 paper on prompt leakage via KV-cache
  sharing, vLLM security docs on prefix-cache timing channels, VulnCheck advisory
  "llama.cpp b4882-b9058 buffer overflow in KV cache state restore" (memory-safety
  flaw on the same restore path), UpGuard "Analyzing llama.cpp servers for prompt
  leaks", llama.cpp issue #24746 (slot requests bypass prompt cache restore).

## Q4: compaction that preserves law-critical context; worst-event reach

- Governance Decay (arXiv 2606.22528, fetched, v2 2026-06-27): the direct
  counterpart to the estate's 96.6-pct-removal / ~11-pct-worst-event-reach
  instrumentation. Violation of in-context governance constraints rises from 0 pct
  with the policy in full context to 30 pct after compaction, 59 pct for some models;
  when the constraint survives the summary violation stays 0 pct, when dropped it
  reaches 38 pct; an adversarial Compaction-Eviction Attack biases the summarizer to
  omit legitimate policy, and "optimized injections defeat every evaluated model".
  Mitigation "Constraint Pinning" quarantines governance constraints from lossy
  compaction and restores violation to 0 pct. ConstraintRot is the benchmark. This
  names exactly what the reach-ratio meter should meter: does the LAW survive.
- Ramp Labs "Latent Briefing" (X article, 2026-04-10, resolved via fxtwitter):
  task-guided KV compaction sharing memory between orchestrator and worker agents;
  up to 49 pct median token savings on 32k-100k token documents, 65 pct worker token
  reduction, ~1.7 s median compaction overhead scaling linearly, ~3 pp accuracy GAIN
  on LongBench v2. A compaction policy measured on accuracy plus overhead, not
  perplexity. Article body not pulled (fxtwitter carries TLDR + stats only).
- Snippet-level leads not deep-read: Factory.ai "context compaction must preserve the
  next step"; Claude Code's compaction reusing the exact same system prompt, user
  context, system context and tool definitions as the parent conversation
  (x.com/trq212/status/2024574133011673516); TestingCatalog's Adeline 1 compacting
  settled agent loops to ~9 pct of size without changing the system prompt; jchudnov
  on compaction losing details and "prefix sliding".

## Pass 1 candidate inventory (45 considered, last-30-days unless noted)

From the X door: RampLabs article 2042660310851449223; hamandcheese status
2020238406593245516; CompleteSkeptic article 2097738214589215173; theo status
2100762304862384257; _avichawla article 2096491130489872479 + statuses 2091078211904
13977 and 2044670188998803855; DimitrisPapail article 2041974013950373901 (Memento);
cwolferesearch status 2072435980494119136; himanshustwts status 2042701342645657896;
trq212 status 2024574133011673516; ByteMohit article 2063493300884246598; nicbstme
status 2051131906327298; theRedbeardIO context-lens thread; rohit4verse status
2039039787475353821; testingcatalog status 2073031325246726196; jchudnov prefix
sliding thread. From search sweep: AgentKV 2609.14872 (registered), ActKV 2609.31395
(registered), CommitKV 2608.07855, DeepSeek-V4.1-Flash 2609.19969, CONTINUUM
(openreview), vLLM AgentX blog, AMD ROCm TurboQuant blog, SGLang RFC #24656, WEKA KV
economics, HPE offload-vs-TurboQuant, vLLM Mooncake blog, HotCarbon 2026 paper 20,
arXiv 2605.09649, Ken Huang KV wars, GRAID blog, societyforaisecurity 2609.18526
page, llama.cpp SECURITY.md, CVE-2026-27940, TurboQuant PR #21089, llama.cpp
discussion #23470, LocalBench q8/q4 KV benchmark, Particula KV quant blog, SotaAz
q8_0 throughput, arXiv 2609.04263 (cites KVarN), 1s720r8, HN 48739846, PrefixWall
2603.10726, Governance Decay 2606.22528, SafeKV, NDSS 2025 KV sharing, UpGuard prompt
leaks, VulnCheck state-restore advisory, KVarN arXiv 2606.03458 (June, the named Q1
target), KVarN README, PR #21038 (April, the named Q1 target).

## Pass 2 deep reads (9, all fetched and read this sitting)

arXiv 2606.03458 abs; github.com/huawei-csl/KVarN README; llama.cpp PR #21038;
arctic-shift API for 1s720r8; hn.algolia.com item 48739846; arXiv 2603.10726 abs;
arXiv 2606.22528 abs; fxtwitter RampLabs 2042660310851449223; fxtwitter
CompleteSkeptic 2097738214589215173. Only these are banked as items.

## Overlap evidence (greps run this sitting)

- catalog/catalog.jsonl "kvarn": 9 rows (the 10-01 reddit harvest kvarn_comments.json
  13 rows / kvarn_pullpush.json plus receipts); memory/: zero kvarn hits.
- ARXIV_REGISTER.json: "kvarn|2606.03458" zero rows (append still owed);
  AgentKV row 4694, ActKV row 5417, 2609.31678 row 5450 present; "2606.22528" zero.
- catalog "CommitKV|2608.07855|CONTINUUM|RampLabs|CompleteSkeptic|Memento|avichawla|
  2609.04263|TurboQuant": only lmcache-src TurboQuant implementation files (held) and
  VS Code memento API files (false hit). CommitKV/PrefixWall/Governance Decay/PR
  #21038/1s720r8: no catalog rows.
- memory/ "CompleteSkeptic": 7 files, the load-bearing one is
  memory/runs/x_reply_radar/out_2026-09-16.json which carries the author row
  ("After co-inventing ChatGPT..."), so the ACCOUNT is radar-known; the KV-cache
  article framing is not in holdings.
- memory/ "RampLabs": memory/trajectory/steps.jsonl carries a prior X-door id map
  ('RampLabs':2104634941405266021, a different status than this article) and this
  session's own command echoes; the Latent Briefing article itself is not held.
- memory/ "CommitKV": only percolator invariants sealing the CommitKVStore code
  symbol, not the paper.

## Steal-card hooks (for the probe queue)

1. Reach-ratio meter should meter LAW survival, per Governance Decay's
   constraint-dropped vs constraint-survived split (0 vs 38 pct violation); pinning
   is the mitigation to copy for the KV degradation ladder's law-critical tier.
2. KVarN k4v2 preset (4-bit K / 2-bit V, g128) joins the SAELIS q8_0 bet as a
   ladder rung; PR #21038 shows unrotated q8_0 costs 5.4 points of AIME25 on
   gpt-oss-20b, rotation recovers to F16 parity, at a measured 10-12 pct
   token-generation slowdown plus an opt-out env var LLAMA_ATTN_ROT_DISABLE.
3. PrefixWall's selective-isolation shape is the response blueprint if any shared
   KV or session-restore surface is exposed multi-tenant.
4. The ARXIV_REGISTER one-line append (2606.03458) is still owed from 10-01 and
   remains zero-spend.
