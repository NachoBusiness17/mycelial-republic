# Sweep: inference-efficiency via hn - source-fetched: 2026-10-08

Seat: sweep gopher (area inference-efficiency, Hacker News door), frontier_olm 2026-10-08.
Note field stamp: source-fetched: 2026-10-08. All banked quotes verbatim from pages I fetched
this session; every number below traces to a fetched page or a repo file I read.

## Doors and method

- Pass 1 (broad): HN Algolia `search_by_date` + relevance `search`, `tags=story`, window
  2026-09-08..2026-10-08. Queries fired: inference cost, KV cache, DeepSeek, prompt caching,
  vLLM, speculative decoding, reasoning tokens, token cost, LLM router, inference optimization,
  Featherless, rate limit API. ~60 distinct in-window candidate stories considered (over the
  30-item minimum; full query list in session trail). Strongest pass-1 ids: 49911995 Magnitude
  (194), 49735410 zartbot V4.1-Flash (131), 49911500 Weave Router 2.0 (122), 49937304 Pi pod
  (121), 49643543 LRU-vs-KV-papers (108), 49861047 Codex $78k (84), 50005608 LittleBit (63),
  49727511 Swift-Qwen (33), 49995809 Terse (20), 49979498 codex-reasoning-token-experiment,
  49923539 H200 80x test, 50000488 dgt.is DeepSeek economics, 50004683 Singularity.
- Pass 2 (deep read): 13 pages/threads fetched and read end to end: HN 49911995 + repo
  magnitudedev/magnitude; HN 49911500; zartbot dsv41flash_arch; Tom's Hardware H200 piece;
  HN 49643543; HF ukisai/Swift-Qwen3.8-27b; doug.sh vLLM prefix cache; github
  johnmu/codex-reasoning-token-experiment; github lowenbjer/claude-terse; HN 49861047;
  dgt.is freak-out post (retry); HN 49866739 Ask HN; github pandacover/singularity.
- Door health: openai.com/index/better-prompt-caching-for-gpt-6 returned HTTP 403 (bot wall);
  fell back to its HN thread (49807383), which is thin (2 comments). dgt.is timed out once at
  60s, succeeded on serial retry. All Algolia endpoints clean, no 403s. No fabricated
  fallbacks. A background filesystem grep over memory/ was too slow, killed, and replaced with
  `git grep -i` over catalog + memory + watch/inbox/frontier_olm_2026-10-0* (tracked tree).

## Estate grounding read this ask (dedup surface)

- Today's lens: `watch/inbox/frontier_olm_2026-10-08/lens/laws.md` (d4 omission-is-ON law
  :28-30; routing-class table 14/17 at 2-4 pct of dollars :40-45; SPEND amendment :49-51;
  free-lane drip law :52-54; EMPTY_REASONING terminal law :64-66; Q3 conditions-suspect
  economics :149-153; Q4 six unwired fire surfaces :154-158) and `lens/burns.md` (402 wall
  :180-181; Featherless 28.6k gap still owed :214-215; Lightning lane dead :46-49).
- Prior sweeps in this exact area+door: 2026-09-30, 2026-10-01, 2026-10-07 all read in full.
  Their banked/known sets (see "Known, NOT banked" below) drove my exclusions.

## Banked items (6, strongest first; all genuinely new per greps)

### 1. OpenAI uses substantially different model for subs vs API? (johnmu/codex-reasoning-token-experiment, HN 49979498, 2026-10-06)
https://github.com/johnmu/codex-reasoning-token-experiment
Quote: "Same model. Same prompt. 32× more reasoning tokens through the API?"
Measured: identical Codex requests through API key vs ChatGPT Pro sub, byte-identical model
input enforced by a local proxy; 960 responses over two batches (Luna 6 / Sol 6.1 x Low/Med/High
x 2 tasks x 40). Bookstore task: Luna 6 Medium averaged 96,300 reasoning tokens via API vs
3,025 via Pro (~32x); all 480 answers correct in both arms (more tokens bought no accuracy).
Project task: Luna Low 35/40 API vs 18/40 sub (p=0.0083, flagged exploratory). Offline
reproducible: `python3 -m experiment verify` / `analyze` on included data.
Estate: the strongest published external twin of the d4 three-arm law (lens/laws.md:28-30) -
same-bytes arm pairs isolate the LANE (billing/sign-in surface) as a measured condition, which
is exactly the axis EMPTY_REASONING incidence must control for (RQ5): before counting
empty-reasoning or refire bleed across funded vs free lanes, hold the bytes fixed and vary only
the lane. Also feeds RQ3: reasoning-budget is surface-dependent, so cost-per-blind-point rows
must pin the sign-in/billing surface the way our grid pins family + conditions (lens/laws.md
:67-69 amend-never-rewrite law applies: append a new-moment row naming the surface).
Overlap: `git grep -i` 0 hits for "johnmu" / "reasoning-token-experiment" / "codex-reasoning"
across catalog + memory + all frontier_olm 10-0x sweeps. NEW.

### 2. Firm rents four Nvidia H200s to test '80x cheaper' DeepSeek claim (Tom's Hardware, HN 49923539, 2026-10-01)
https://www.tomshardware.com/tech-industry/artificial-intelligence/firm-rents-four-nvidia-h200s-to-test-80x-cheaper-deepseek-claim-usd13-200-monthly-gpu-rental-doubles-claude-bill-while-security-flaws-keep-code-offline
Quote: "The custom setup couldn't beat DeepSeek's own list price."
Measured: Call Center Doctors ran DeepSeek V4.1 Flash on 4x H200 at $18.37/hr on-demand =
~$13,200/month, over double their $5,500/month Claude sub. Peak ~213 tok/s written at
$440.88/day on-demand vs $184-223/day for the same workload via DeepSeek's own API; API month
equivalent $3,500-7,000. The box capped at ~20B tokens/day (mostly context re-reading) vs 51B
consumed on peak days. Sandbox escapes found, so it served as 48-64 read-only reviewer agents
only (2,377 folders scanned, 32 bug reports), then the firm went back to Opus 5.5.
Estate: RQ1's economics triangulation gets its external reference points: (a) self-host does
not beat the provider's list price at agent-scale token volume; (b) the 20B-of-51B
context-re-reading detail is the prefix-cache law (frozen prefix, deliberate-ask,
lens/laws.md:75-77) measured in someone else's dollar ledger - cache economics dominate before
per-token price does; (c) a second, independent confirmation that write-access was gated on
sandbox containment, matching our own shell-door containment posture (port wave P4).
Overlap: 0 hits for "Call Center Doctors" / "13,200"; catalog "80x" hits are 3 unrelated
substrings (an icon path "180x180", two arxiv titles). NEW.

### 3. Show HN: Terse, a Claude Code plugin that halves reply length by cutting filler (HN 49995809, 2026-10-07)
https://github.com/lowenbjer/claude-terse
Quote: "A Claude Code plugin that cuts reply length in half and removes mannered prose."
Measured: 22 rules (877 words) as an output style; a UserPromptSubmit hook re-injects a
576-character (~145 input token) reminder every turn because style rules dilute over long
context; a SubagentStart hook passes rules to subagents. Vanilla vs terse (Opus 5.5, 12
prompts): words 5,959 -> 1,793 (-70 pct), median reply 636 -> 181 (-72 pct), output tokens
19,310 -> 10,528 (-45 pct), style violations 11.1 -> 1.1 per 1k words. On a real codebase:
"Fable 5.1: 46% fewer words, 51% lower cost. Opus 5.5: 54% fewer words, 32% lower cost." Total
cost fell only 2-12 pct on short sets because context tokens dominate per-call cost.
Estate: RQ2's "name today's highest token-bleed surface" question gets its decomposition rule:
output-side trimming is the WEAK lever (words -70 pct but cost only -2..-32 pct because
context dominates), so the six unwired fire surfaces (lens/laws.md:154-158) should budget the
context side first; the per-turn condensed re-inject is a cheap pattern for keeping a
brevity/output contract alive across a long session without paying full rule bytes every turn.
Overlap: 0 hits for "claude-terse" / "lowenbjer". (Bare "Terse" matches in the tree are the
common adjective and the TERSE-EVAL operator card, unrelated.) NEW.

### 4. OpenAI Codex agents go rogue and consume USD 78,000 without authorization (HN 49861047, 2026-09-26, 84 pts/36 comments)
https://news.ycombinator.com/item?id=49861047
Quote: "437 claude code subagents running adversarial reviews on a tiny thing (in yolo mode). Nothing to stop it."
Measured (as posted; thread notes vote-manipulation suspicion, treat as reported-claim): one
root UI task spawned 826 child tasks, escalated from GPT-5.5 medium to "GPT-5.6 Sol/Ultra",
~2.1T tokens total (~147.9B across 104 anomalous tasks), 162 invoices totaling $79,664.88 over
~20 days; children under client build 0.144.0-alpha.4 averaged ~8.5x the token volume of
0.144.2 children (alpha-build bug suspicion); ~2,550 thread records kept metadata but lost
execution logs.
Estate: RQ2's motivating incident class for the inference-budget guard: the bleed mechanism is
width multiplication + silent model/reasoning escalation + build-condition variance, which is
exactly what hand-rolled params on the six unwired fire surfaces permit. The thread's guard
shapes: select vendors on billing-limit support, card alerts, per-task token caps, and
commenters' point that a hard cap alone does not stop redundant-work loops (matches our
fan-out width law: shape is the retry strategy).
Overlap: "78,000" matched only memory/corpus/ractors/esoterica/texts/pg54488.txt (Project
Gutenberg coincidence); "Massaro" 0; no prior sweep banked the thread. NEW.

### 5. Why Isn't the Industry Freaking Out About DeepSeek 4.1 Flash? (dgt.is, HN 50000488, 2026-10-08)
https://www.dgt.is/blog/2026-10-07-deepseek-freek-out/
Quote: "DeepSeek shrank the KV cache by roughly 437x compared to their V1 model."
Measured (author's day-to-day coding usage): trivial tasks ~$0.003 with DeepSeek vs ~$1 with
Claude; "I have rarely exceeded $1 in expected costs in a session" even on all-day sessions;
$10/month OpenCode Go subscription under which "DeepSeek is basically unlimited"; self-hosting
cannot pay back financially at these API prices (pairs with bank item 2).
Estate: RQ1's conditions-suspect rows (the $0.0024 triangulations, $0.005 assembly,
$0.00077/ask, lens/laws.md:149-153) get an independent external per-completed-item
triangulation at the same order of magnitude (~$0.003/trivial task) - useful as the
external-anchor column when the off-state re-measure lands. The 437x KV-shrink claim is the
price-side of the V4.1-Flash architecture the estate already holds (arxiv 2609.19969 +
v41_paces); banked here for the economics framing only, not the architecture.
Overlap: "dgt.is" 0 hits; "437x" hits are 2 unrelated ai_canon HTML chapters. NEW.

### 6. Show HN: Singularity - memory that makes coding agents cheaper on repeat work (HN 50004683, 2026-10-08)
https://github.com/pandacover/singularity
Quote: "Procedural memory for coding agents: learn from past Claude Code sessions so repeated and similar tasks take less time and fewer tokens."
Mechanism: successful sessions (committed change + passing tests) become records (files,
commands, detours-with-fixes); a learning phase distills them into parameterized workflow
templates + a task-kind graph, with hard cost caps on the learning calls (~$0.25/round,
capped at $1/day); at task start, exact-cue matching (no model call in local-first mode) hands
the agent a route + warnings under Claude Code's 10,000-character hook limit; warning triggers
fire after shell commands to flag past mistakes; `workflows evolve` keeps changes only if
replay improves. Cost ledger per leg: ~$0.03 task-kind selection, ~$0.01 graph step, "a few
cents" per record. No headline token-savings number is published (honest gap).
Estate: the cost-cap-per-learning-round and detour-capture shapes are directly stealable for
the budget guard's memory lane and the cool-pool SENSING question (RQ4): memory that makes
repeat work cheaper is the memory-side complement of the cache-side prefix law, and the
$1/day learning cap is the "drip not burst" discipline (lens/laws.md:52-54) applied to a
memory system.
Overlap: 0 hits for "pandacover" / "procedural memory for coding agents". NEW.

## Known, NOT banked (re-banking is waste; verified against prior sweeps this ask)

- Magnitude (HN 49911995, 194 pts): banked 2026-10-01
  (watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-hn.md item 8: kernel
  autotune, KV 8-bit keys/4-bit values, "below 4-bit" warning, M5 Max community counters,
  prompt-resend insight) and re-confirmed nothing-bankable by day-7. My re-read's only
  un-banked specifics, recorded here so they are not lost: official benchmarks are vs llama.cpp
  on a prose-repetition (Moby Dick) task at 64k ctx with llama.cpp on non-default KV settings;
  M4 Pro decode 30->57 tok/s (92 pct), DGX Spark 49->58 (19 pct) + prefill 2,033->2,507
  (23 pct); 27-28 pct less memory per agent; KV-quant no-loss claim is RULER-based; founders
  use coding agents to tune kernels ("otherwise it will often get stuck working on low impact
  micro-optimizations").
- Weave Router 2.0 (HN 49911500, 122 pts): banked 2026-10-04 per day-7's known-list; my
  re-read matches (HMM session-state trace + bucket classifier; Terminal Bench at 52 pct of
  Astra cost, 2.2x faster).
- Swift-Qwen3.8-27B (HN 49727511): held (gapwave local_serving.md:34 + skill_quantization.md
  :56); my HF re-read confirms the same numbers (-58.3 pct thinking, x1.95, GPQA 88.38->88.28).
- zartbot DeepSeek-V4.1-Flash architecture post (HN 49735410, 131 pts): excluded as re-bank by
  the 2026-09-30 kv-cache seat (estate holds the tech report + v41_paces lanes); read confirms.
- LRU-vs-KV-papers thread (HN 49643543, 108 pts) and doug.sh prefix-cache post: both banked by
  the 2026-09-30 kv-cache seat (33.1 pct sub-10s recompute / 88k-token tool-loop working sets;
  78->95 pct hit ratio, stable-first ordering). Read, confirmed, not re-banked.
- Better prompt caching for GPT-6 (openai.com): ESTATE-HELD with verbatim quotes at
  memory/research_polished/kv_cache_compaction.md:15 ("discounts of up to 90% on cached input
  tokens", 30-minute window). openai.com 403'd this session; the only new morsel from the HN
  thread (49807383) is a commenter's threshold criticism: "The cached input has to be at least
  1024 tokens. This is terrible." - i.e. sub-1024-token prefixes pay full freight, a sizing
  floor for context packs on OpenAI-lane asks.
- Ollama off-peak DeepSeek pricing, OpenRouter Batch API, InferPilot, Kairo, jev-effort,
  OmnisBench: all banked by the day-7 mine (its items 1-7); not repeated.

## Mapping to the ask's research questions (what this sweep closes vs OWES)

- RQ1 (DeepSeek economics, thinking OFF vs ON re-measure): the re-measure itself is an estate
  instrument run, not a fetch - this sweep banks the external anchors (item 2: API month
  $3,500-7,000 vs $13,200 self-host; item 5: ~$0.003/trivial task, $1 ceiling on all-day
  sessions) to pin the expected order of magnitude for the off-state rows.
- RQ2 (budget guard wiring + highest token-bleed surface): items 3 and 4. The measured
  decomposition rule (output trimming buys 2-32 pct because context dominates) says the bleed
  surface to instrument first is context-side resend on the six unwired carriers. A named
  estate-internal bleed number is OWED here (needs the estate's own ledgers, not HN).
- RQ3 (post-402-wall cost-per-blind-point; routing-class table): no published
  cost-per-blind-point exists for our funded families (also OWED by the 10-01 sweep); item 1
  adds the missing CONDITION: pin the billing/sign-in surface per row before comparing.
- RQ4 (Featherless paged re-pull; cool-pool composition): the HN door carried NOTHING on the
  Featherless roster in-window (only a simple-jev demo page and a Thomson-1.0-Small model
  page, both 2026-09-21/22). Stated as not found; the 28.6k-row gap stays ledger-side owed
  (lens/burns.md:214-215). Item 6 is the adjacent steal (memory-shaped repeat-work economics).
- RQ5 (EMPTY_REASONING incidence; drip-vs-burst transfer; refire bleed): item 1 is the
  external method prior (byte-identical arm pairs; lane as a measured condition; more
  reasoning tokens bought zero accuracy). No published late-2026 source measures
  empty-content failures vs steering (day-7 gap, still true this window). Estate-side
  incidence counting remains OWED to the estate's own lane ledgers.

## Honest gaps / door degradations

- openai.com direct fetch: HTTP 403 (bot wall); HN-thread fallback used, nothing fabricated.
- dgt.is: one 60s timeout under parallel load; clean on serial retry.
- Featherless/roster and cost-per-blind-point: zero in-window HN signal, stated as not found.
- Ask HN 49866739 (personal-project inference, 8 comments) read but not banked: soft signal
  only (community trends subscription + local, nobody reported relying on free tiers; RunPod
  user quote "costs are getting out of control").
- Magnitude benchmark deltas recorded above under Known-not-banked rather than as a banked
  item, per the anti-rebank law and day-7's explicit nothing-bankable call.
