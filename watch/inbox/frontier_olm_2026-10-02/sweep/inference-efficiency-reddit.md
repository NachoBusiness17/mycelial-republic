# SWEEP: inference-efficiency via reddit (frontier_olm 2026-10-02)

source-fetched: 2026-10-02. Area: inference-efficiency. Door: reddit.
Seat: sweep gopher (dwf actor_3). RQs: the four at
`watch/inbox/frontier_olm_2026-10-02/lens/questions.md:106-113`.

## Door status (all probed this sitting, nothing assumed)

- `https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` -> HTTP 403 Blocked (WebFetch).
- `https://old.reddit.com/r/LocalLLaMA/top.json...` -> login-wall page shell ("Log in to use old
  Reddit") via WebFetch AND via web_reader (two different fetchers).
- www comments page via WebFetch -> login wall. www comments via web_reader -> "Prove your
  humanity" bot challenge. So: recipe's primary door DEGRADED, as the doors lens already held
  (`lens/burns.md:108-112`).
- PullPush archive (`api.pullpush.io/reddit/search/submission/?ids=1wiu7xj`) -> answers but
  `{"data":[]}`, no records for current-era ids. Dead for this window.
- Redlib mirrors: redlib.catsarch.com 429, rl.bloat.cat ECONNRESET, redlib.privacyredirect.com
  socket closed, redlib.perennialte.ch Cloudflare challenge via web_reader. All dead today.
- WORKING DOOR: `arctic-shift.photon-reddit.com` API. `/api/posts/ids?ids=...` returns full
  records (date, score, selftext); `/api/posts/search?subreddit=X&after=YYYY-MM-DD&limit=100&sort=asc`
  walks the archive chronologically. Text-search params (`title=`, `selftext=`) return HTTP 422
  on this network, so relevance discovery ran through WebSearch `site:reddit.com` and every hit
  was then date-verified and full-text-verified through arctic-shift.
- WebSearch also 429'd intermittently mid-run (1302s); pauses cleared it. No fabrication needed.

## Pass 1 census (the 30+ bar, date-verified)

Every id below was read from arctic-shift JSON this sitting, not from search snippets.

In-window candidates (created 2026-09-02 or later), 35:

| id | date | sub | score/cmts | note |
|---|---|---|---|---|
| 1w6c3ad | 09-05 | LocalLLaMA | 3/8 | Strix Halo coding agent, 94 pct hit rate claim |
| 1wb35xo | 09-10 | LocalLLaMA | 15/20 | 2x4090 agent concurrency, three weeks of data (DEEP-READ) |
| 1wd99iw | 09-11 | LocalLLaMA | 13/12 | agent-runtime benchmark: cost per successful task (DEEP-READ) |
| 1wi17z6 | 09-16 | LocalLLaMA | 1/35 | harness that will not invalidate cache (DEEP-READ) |
| 1wiu7xj | 09-17 | LocalLLaMA | 60/12 | vLLM prefix cache warm (doug.sh thread; REBANK-DELTA) |
| 1wn1t6a | 09-19 | LocalLLaMA | 20/6 | Complex KDA paper thread (NOT deep-read: marked) |
| 1wsijnv | 09-21 | ClaudeAI | 9/40 | headless Claude Code 3x limit burn (DEEP-READ) |
| 1woq45i | 09-24 | LocalLLaMA | 1/1 | SPLASH port to M1 Max, 39 tok/s -> [removed], unreadable |
| 1wou3gr | 09-24 | LocalLLaMA | 83/33 | BC-250 mining APUs, Qwen 3.6 35B at 60 tok/s, 64k ctx |
| 1wpodl1 | 09-25 | LocalLLaMA | 1/0 | KV quant (Q4/FP8) hurts needle retrieval (10-02 repost 1wvwdn1 also [removed]) |
| 1wpinky | 09-25 | LocalLLaMA | 8/2 | CachyOS Qwen 3.8 27b on 2x5090 vLLM |
| 1wpjhkf | 09-25 | LocalLLaMA | 13/20 | how are you thinking about context now |
| 1wpkwiw/kz2p/l8aw | 09-25 | LocalLLaMA | 1/1/0 | agent-loop durability reposts |
| 1wpqbxp | 09-25 | LocalLLaMA | 1/1 | 300 most-downloaded LLMs vs vLLM: rope_scaling silently changes RoPE base (64 of 180) -> [removed], unreadable |
| 1wr5ylm | 09-27 | LocalLLaMA | 607/172 | 42x faster prompt lookup drafting (DEEP-READ via blog primary) |
| 1wr7nso | 09-27 | LocalLLaMA | 1/1 | Qwen 3.8 27B NVFP4+DFlash-2+MTP multi-turn benchmark -> [removed by moderator] |
| 1wra7vu | 09-28 | LocalLLaMA | 2/0 | llama.cpp -cb -np determinism -> [deleted] |
| 1wugwtw | 09-29 | LocalLLaMA | 1/16 | benchmark harness/model/hardware help, ~89 pct prefix hit |
| 1wvt1m4 | 10-01 | LocalLLaMA | 1/0 | two 96 GB Ascend cards, Qwen3.8FlashNext, vLLM work |
| 1wvtxkx | 10-01 | LocalLLaMA | 1/0 | tuned Qwen3.8-27b on 24 GB, draft acceptance |
| 1wvtc1j | 10-01 | LocalLLaMA | 1/0 | CalDec v1 open decision model |
| 1wvumyu | 10-01 | LocalLLaMA | 1/0 | hardware setup help |
| 1wvxph8 | 10-02 | LocalLLaMA | 1/0 | benchmark: LMs fixing bugs before users hit them |
| 1wvwssq | 10-02 | LocalLLaMA | 1/0 | Strata on power-limited 5090, 5-6k prefill |
| 1wvwmb5 | 10-02 | LocalLLaMA | 1/0 | multi-agent app on CPU-only machines |
| 1wvwgaz | 10-02 | LocalLLaMA | 1/0 | KernelOPT: dispatch-aware agentic GPU kernel optimization |
| 1wvwdn1 | 10-02 | LocalLLaMA | 1/0 | KV quant FP8/INT4 degrades needle retrieval -> [removed] |
| 1wvvjsq | 10-02 | LocalLLaMA | 1/0 | shardr model serving |
| 1wvv6im | 10-02 | LocalLLaMA | 1/0 | llama.cpp Decision Models |
| 1wvvxyz/1wvw2up/1wvutak/1wvxl4n/1wvxjwk/1wvx5nv | 10-02 | LocalLLaMA | <=1 | noise census |
| 1wjnkgm | 09-19 | ollama | 78/30 | stopped using the smartest models, faster and cheaper |
| 1wkajnc | 09-18 | ollama | 3/0 | GLM-5.2-cloud token savings |
| 1wjy9rh | 09-19 | ollama | 13/1 | Bonsai 2 27B on 8 GB M2 mini, 7.6 tok/s |

Considered from WebSearch and DATED OUT of the 30-day window by arctic-shift (43, excluded from
banking per the anti-rebank recency rule at `lens/questions.md:23-26`): 1sp216x (04-18), 1on25fn
(2025-11-03), 1tjvl4h (05-21), 1td9stc (05-14), 1uztipo (07-18), 1sg076h (04-08), 1rplb3r
(03-10), 1u2a1s8 (06-10), 1w0impd (08-28), 1vz2el8 (08-26), 1wnapgs (08-22), 1whx5xi (08-16),
1w0vrrx (07-28), 1wropen (08-27), 1uatrbg (06-20), 1uai5wa (06-19), 1uqs4gq (07-07), 1tja697
(05-21), 1syy78d (04-30), 1oplxlb (2025-11-05), 1uszk3d (07-09), 1vk1bp8 (08-09), 1wn41b1
(05-30), 1wu0m53 (06-06), 1wabrlq (05-08), 1vtsid0 (04-17), 1w11mi5 (04-25), 1wkfp68 (05-26),
1w2r37q (04-27), 1rydtag (2025-11-17), 1ujohad (03-04), 1tgecrq (05-19), 1wrez7j (04-28),
1ru6hgp (03-13), 1qxf7sf (02-06), 1ojzekg (2025-10-30), 1w1fpxi (08-29), 1uwbsy0 (07-16),
1unrse9 (07-06), 1vv9oe2 (08-15), 1uohsov (07-04), 1w33bff (08-24), 1rnudeg (2026-03-01).

Not walked: r/MachineLearning (budget went to the four recipe subs' walks plus date
verification of ~75 ids). Stated as not done.

## Pass 2 deep reads (7, all read end to end this sitting)

### D1. 42x prompt-lookup drafting in llama.cpp (RQ1, decode-side) - STRONGEST

Thread 1wr5ylm (09-27, 607 pts, 172 cmts) is a link post to
`https://jadidbourbaki.github.io/blog/prompt-lookup-llama-cpp/`, fetched and read in full.
Author Hayder Tirmazi, "originally published on 2026-09-26". Verbatim:
"I make drafting for prompt lookup decoding in llama.cpp up to 42x faster while using up to
2.6x less memory". Mechanics: algorithm unchanged, data structures replaced (segmented flat map,
sorted-vector inner maps with branch-free binary search, Lemire constmap + early-exit).
Staged numbers (medians of 3, WikiText-103 replay, 4096 ctx, M4 Pro 48 GB): copy fix alone
"4.5x to 25.6x faster"; constmap loading "from 3.76 s to 0.23 s with the 541 MB corpus";
Lemire's PR stacks "up to 4.2x... overall speedup upto 140x". Acceptance rates unchanged:
"my changes still have almost identical acceptance rates to the original implementation".
Limits, stated by the author: benchmarks are drafting-simulation only (no end-model tok/s),
and the PRs (#2,#5,#7,#10,#12) live in his fork, NOT merged upstream.
RQ1 fit: does not move the 17.5/33.1/~49.4 recompute decomposition (no TTFT/prefill table);
it attacks the OTHER side of agentic cost: the drafting step that makes speculative decoding
affordable exactly when output echoes input (tool calls, edits). For the estate: the
FAMILY_TABLE wiring debt (`lens/laws.md:61`) should record drafting cost as a separately
tunable row, and the fork-not-merged status means reproduction requires his branch.
Overlap: `grep -ic "prompt lookup\|prompt-lookup" catalog/catalog.jsonl` = 0; memory hits only
this run's own trajectory steps. UNHELD.

### D2. Three weeks of 2x4090 agent-concurrency data (RQ1+RQ3)

Thread 1wb35xo (09-10, 15/20), full selftext via arctic-shift. Verbatim title:
"How many agents can 2x4090 actually run at once? Three weeks of llama.cpp concurrency data -
soft cap 5 @ 64k, hard cap 9, and why". Measured findings (fetcher-summarized, numbers quoted
in its output): aggregate prefill throughput is CONSTANT ~1,500 tok/s regardless of slot count;
soft cap 5 agents at 64k ctx, hard cap 9 at 44.6 GiB VRAM; KV q8_0 matches f16 on quality and
speed while saving 1.4 GiB; a 125B Flash-Next preview is bandwidth-bound at 14.1 GB/s measured
vs 83.2 GB/s peak (half-populated memory channels); retrieval probes tie at ceiling (1.00) up to
a 251,557-token prompt, "not equal" (the author's caveat that a tie at ceiling is not equality).
RQ1 fit: this is the concurrency axis of the recompute-vs-prefill tradeoff measured OUTSIDE any
vendor stack: when aggregate prefill is the invariant, per-agent TTFT degrades linearly with
concurrent agents, which is the fill-cliff mechanism (`lens/burns.md:69`) under multi-agent
load rather than single-stream. RQ3 fit: consumer 2x4090 is exactly the hardware class the five
GPU gates (`lens/laws.md:35`) would admit, with a measured envelope, not a vendor table.
Overlap: unheld (catalog/memory greps for the concurrency-cap framing returned nothing outside
this run's steps; the width laws in AGENTS.md are dispatch-shape, not serving-slot, economics).

### D3. The harness cache-invalidation class, surveyed by users (RQ2)

Thread 1wi17z6 (09-16, 35 cmts), full selftext AND the comment array fetched. Selftext
verbatim: "I don't think it's normal to invalidate 100k of context cache for no reason."
The thread's value is the CLASS TAXONOMY in comments, each verified in the fetched JSON:
timestamps/session-ids injected into the system prompt ("one harness was injecting the current
time into the system prompt so every single turn was a fresh prefix", Independent_Train697);
reordered tool history and compaction rewrites (ShowerAnnual9741); tool-response truncation
(fgk55555 on OpenCode); "official claude models are fine, they screw with third party and local
apis" (Saren-WTAKO); the `--chat-template-kwargs '{"preserve_thinking": true}'` flag
(SeriousPanic34). Measured counterpoint, verbatim: "My OpenCode cache hit rate ranges between
92-98%. What is 'particularly egregious' to you?" (milkipedia). Diagnosis pattern repeated by
two commenters: capture 2-3 consecutive requests and diff the shared prefix, do not infer from
latency alone ("The 40-second delay alone doesn't tell you whether the prompt changed or the
server lost its cached state", Marcus_MSC).
RQ2 fit: this is the invalidation CLASS around the estate's held single instance (the
tool-schema key-order bug, `lens/burns.md:90`), plus the field's diagnosis instrument, which is
the same byte-identity diff the estate already runs (`lens/burns.md:68`). Community consensus
answer to "which harness": Pi Coding Agent (top comment, 27 pts).
Overlap: the doug.sh/tool-schema row is HELD (`memory/runs/gapwave/context_economics_1m.md:46`,
`lens/burns.md:90`); this thread and its taxonomy are NOT held (no catalog/memory hits).

### D4. The doug.sh row's upstream fixes have SHIPPED (RQ2, rebank-delta)

The 09-15 doug.sh post behind held row `lens/burns.md:90` was fetched end to end today
(`https://doug.sh/posts/vllm-kv-cache-agents`). The held numbers confirm at the primary
(cached-prompt share 55 pct morning -> 78 pct mid -> 95 pct after the template fix; TTFT
26-28 s -> 7.3 s, worst 514 s -> 54 s; verbatim: "took it from 78% to 95%, and the average wait
from 21 seconds to 7.3"). NEW DELTA the estate does not hold: the root cause is mcp-go decoding
tool lists into Go maps (unordered) with Bifrost re-serializing in range-loop order, shuffled
on the 10-minute refresh cadence, hitting 8 pct of consecutive turns, and BOTH fixes are merged
upstream: bifrost#7170 and mcp-go#984. Also new at primary: the host-RAM (48 GiB /dev/shm) cache
tier was ineffective on the hybrid model because saved linear-attention states rarely sit at the
restore boundary; and track cached-SHARE not hit counters ("The GPU hit counter alone looked
healthy on my morning run while that share was 55%").
RQ2 answer, direct: yes, this invalidation class has shipped fixes as of the 09-15 post.
Overlap: REBANK of the held row except the fix-PR status; the hn_x_fanout banked copy
(`memory/runs/gapwave/hn_x_fanout/compaction_memory.md`) greps clean for 7170/984.

### D5. Headless agent burn: ~3x the limit per token (RQ4)

Thread 1wsijnv (09-21, 9/40), selftext via arctic-shift. Verbatim: "TL;DR: I ran the same
coding task six times through four ways of running Claude Code, with the same model and effort,
and checked `/usage` before and after". Measured: headless (Agent SDK / `claude -p`) consumed
~5.2 pct of the 5-hour limit per $1 of API-equivalent tokens vs ~1.6-1.8 pct interactive,
~3x per token, on Opus 5, effort medium; headless runs used FEWER API-dollar tokens yet ~2x the
limit per run; an ~$18 headless task approx 90 pct of a window vs ~30 pct interactive.
Author-stated limits: n=6, one task/model/account, whole-percent /usage granularity, the
accounting signal itself unknown.
RQ4 fit: the frontier's efficiency-per-deliverable denominator is being measured in
LIMIT-BURN per artifact, not dollars per artifact. That is a THIRD denominator the descent
falsifier (`lens/laws.md:32`) does not currently track: the estate banks tokens+cost per turn
(usage.jsonl) and delivers per artifact, but subscription-plan seats (the operator's own
ZCode/GLM lanes) burn a renewable quota whose price-per-token is not the binding constraint,
quota-per-window is. Folding a quota-burn column next to cost in the usage ledger is the
concrete steal.
Overlap: unheld (no catalog/memory hits for the headless-3x claim; AGENTS.md tier laws price
tokens, never quota).

### D6. The frontier is ASKING for our denominator (RQ4)

Thread 1wd99iw (09-11, 13/12), full selftext + all 13 comments fetched. Selftext verbatim:
"task success rate, cost per successful task, wall-clock time, tool calls / retries,
reliability over long-running tasks" - the poster's wanted columns for an agent-RUNTIME
benchmark that "control[s] for both sides": same model different harness, same harness
different model. Comment-thread state of the field: Terminal Bench's Terminus already
parameterizes the agent software (suprjami); FrontierHarness Eval exists as a named eval
(already known to the estate: `memory/continuity/seat_memory_20260927/x-drops-20260918-afternoon.md:28`,
LINKS-279, flagged there as a naming collision); the sharpest gap named is pass^k determinism
and error-recovery efficiency, not pass@1 (Enough-Photo9140, 5 pts); the cost objection is
combinatorial blowup of the matrix (snmnky9490, 9 pts).
RQ4 fit: as of 09-11 nobody in this thread could name a published tokens-or-dollars-per-
landed-deliverable table for agent runtimes. The estate's usage.jsonl + per-artifact receipts
are ahead of the asked-for instrument on the measurement axis; what the estate lacks is the
harness-controlled matrix (same model, our harness vs another), which is exactly a rung the
workflow-gate dogfood could finance. The pass^k/error-recovery metric is a free import for the
duel harness.
Overlap: FrontierHarness KNOWN (x-drops LINKS-279); the thread, its matrix framing, and the
pass^k metric NOT held.

### D7. Cross-datacenter prefill-as-a-service (RQ1/RQ3, OUT OF WINDOW, new primary)

Reddit thread 1sp216x is 2026-04-18 - five months stale, fails the window bar. Banked only as
a new primary under the anti-rebank's second clause (`lens/questions.md:24` "or carry a
genuinely new primary"): arxiv 2604.15039 "Prefill-as-a-Service: KVCache of Next-Generation
Models Could Go Cross-Datacenter" (v1 2026-04-16, v2 2026-04-22), abstract page fetched in
full. Verbatim: "a PrfaaS-augmented heterogeneous deployment achieves 54% higher serving
throughput and 64% lower P90 TTFT than a homogeneous PD baseline". Hybrid Kimi Linear
(KDA+MLA 3:1) shrinks KVCache so prefill can run in a DIFFERENT datacenter over commodity
Ethernet; the r/LocalLLaMA search snippet adds 1.54x throughput and Kimi-Linear KV reduction at
32k (Table 3, NOT verified - I read the abstract page only, not the PDF tables).
RQ1 fit: this decomposes the prefill/decode tradeoff along an axis the banked 17.5/33.1/~49.4
decomposition does not model: WHERE prefill runs. The estate's ram-cache/verkle stack could
model prefill-site choice the same way for CPU-vs-GPU lanes. Not on the five-gate hardware
path (it is datacenter economics), so RQ3-admitting hardware it is not.
Overlap: `grep -ic "prefill-as-a-service\|2604.15039" catalog/catalog.jsonl` = 0; memory hits
are only this run's trajectory steps. UNHELD, but stale-dated: rank it last.

## RQ-by-RQ verdicts (what this door could and could not answer)

1. KV-recompute-vs-prefill beyond 17.5/33.1/~49.4 and the ~60 pct fill cliff: NOTHING read
   today re-derives or extends that decomposition post-10-01. Nearest in-window movement:
   D2 (aggregate prefill invariant under concurrency) and D1 (drafting cost separable). The
   removed thread 1wpqbxp (RoPE base silently changed on 64 of 180 models under vLLM) names a
   byte-identity BREAK CLASS that would corrupt any recompute decomposition, but its body is
   [removed] and unreadable - recorded as a lead, not a finding.
2. Cache-invalidation classes with shipped fixes or reproductions: YES - D4 (the exact held
   bug class, fixes merged upstream) and D3 (the wider class taxonomy + the field's
   request-diff diagnosis instrument). KVarN stays unconfirmed per `lens/burns.md:99-100`;
   nothing read today touches it either way.
3. Linear-attention/hybrid/neuromorphic TTFT tables on gate-admittable hardware: NO new
   SpikingBrain-comparable table found in-window through this door. 1wn1t6a (Complex KDA,
   09-19) is the one live lead, NOT deep-read this sitting (paper unread) - OWED. 1woq45i
   (SPLASH on M1 Max) would have been the consumer-hardware data point; post removed before
   archive capture. D2's 2x4090 envelope is the closest measured consumer-hardware table that
   survived.
4. Efficiency per landed deliverable: the reddit frontier measures it as quota-burn per task
   (D5) and wants it as cost-per-successful-task (D6); no published tokens-per-artifact table
   was found through this door. The estate's falsifier denominator has no reddit-built rival
   in evidence today; the importable deltas are the quota-burn column and the pass^k metric.

## OWED and not done (stated, not glossed)

- r/MachineLearning not walked (budget). r/ollama walked 09-18..09-19 slice only.
- 1wn1t6a Complex KDA paper not read; no arxiv id captured.
- 1wb35xo and 1wsijnv comment arrays not pulled (selftext + title verified only).
- arxiv 2604.15039 read at abstract page only; PDF tables (KV size at 32k, testbed) unverified.
- `lens/burns.md:76-77` rank-10 fill (r/LocalLLaMA 1sy7srk KV tables): id NOT PRESENT in
  arctic-shift (`/api/posts/ids?ids=...,1sy7srk,...` returned 11 of 12 rows; 1sy7srk absent).
  Cannot heal it from this door; the id itself may be wrong in the banked ledger.
- Quotes for D2/D5 pass through the fetch instrument's summarizer (arctic-shift selftext is
  verbatim on the wire; the summarizer quotes numbers but paraphrases prose). Verbatim-quoted
  strings above are the ones it emitted as quotes or that came straight from title/selftext
  fields. The 125-char quoting limit the summarizer enforces is why selftexts are summarized
  rather than pasted whole.

## Fold

The reddit inference-efficiency frontier this month is converging on exactly the estate's
banked spine: prefix byte-identity is the invariant, cache-share not hit-count is the metric,
and harnesses are the dominant cache killer. New this window: the tool-schema class has SHIPPED
fixes upstream (bifrost#7170 + mcp-go#984), drafting cost is separable and 42x-optimizable
without algorithm change, aggregate prefill is the invariant under agent concurrency on
2x4090s, and the per-deliverable denominator the descent falsifier demands is still unbuilt in
public - quota-burn per task is the closest the frontier gets.
