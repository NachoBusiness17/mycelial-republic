# sweep: kv-context-engineering via x, 2026-10-06

source-fetched: 2026-10-06. Window: 2026-09-06 to 2026-10-06. Area feed: the day-5 probe
order (DIGEST.md:83-92 via lens/burns.md:205: Theo falsifier B first), the day-4 strict-prefix
cache-resume steal (lens/burns.md:56), the confirmed 2609.22114 gateway-cost and 2608.22752
compaction-cliff rows (lens/burns.md:77-79), the two-axes finding (lens/burns.md:81-82), and
B4's q8_0 KV decode win 100.8 vs f16 55.9 t/s (lens/burns.md:59). Successor to the day-5
sweep of the same area+door (frontier_olm_2026-10-05/sweep/kv-cache-context-engineering-x.md,
read in full this sitting, 121 lines): its banked set is the anti-rebank baseline.

## Door log (honest, this sitting)

- fxtwitter JSON door (`https://api.fxtwitter.com/<user>/status/<id>`): worked on all 11
  resolved posts, zero 403/404 once the `/status/` path segment is present. Instrument note
  for the next seat: calls shaped `api.fxtwitter.com/<user>/<id>` (no `/status/`) return
  `{"code":404}` on VALID ids; the day-5 recipe string includes `/status/`, keep it verbatim.
  A summarizer-passed walden_yan id (2107185314144357) was missing digits vs the page's real
  link (2107185315014144357); ids must come from the raw page grep, not from summaries.
- vxtwitter (`api.vxtwitter.com`) verified live as the alternate door (one control call on
  theo/2106847019319062819 returned full JSON with likes/replies); not needed after the path fix.
- Z.ai WebSearch: heavy 429/1302 rate limiting this sitting (5+ retries burned inside single
  calls); `site:x.com` queries again surfaced zero resolvable status URLs, matching day-5.
- Latent Space route (day-5's proven fallback): section RSS listed one NEW edition since
  day-5 (Oct 6 "Reflection Beam"); its page raw-fetched via curl (203,047 bytes) and all
  93 tweet URLs extracted by grep. Oct 2 "Pi 1.0" edition (157,134 bytes, 14 URLs) and the
  Gemini 4 Argon edition (208,510 bytes, 60+ URLs) also raw-fetched; both mostly
  video-model/launch chatter, rejected on RQ fit.
- arXiv doors: `export.arxiv.org/api/query` over plain http returned 0 bytes; the https form
  works. ReCAP resolved through https arXiv API + abs page (42,837 bytes).

## Pass 1 tally

167 tweet URLs listed across three AINews editions (93 + 14 + 60+), ~40 considered on RQ
fit, plus 10+ search-engine candidates. Rejected outright with reasons: theo/2106847019319062819
(Oct 4: Anthropic-vs-OpenAI code-model pricing, off-RQ); thsottiaux/2107158998495748264
(GPT-6 speed claim, no mechanism); cognition/2105408461701824732 (Vera Rubin hardware);
qvac/2107043339799593421 (speculative decoding on Metal, off-RQ); ggerganov/2107190267887632462
(llama.cpp v0.6.0: Clef + Metal + llama_batch_ext; no KV-cache-quant content in the tweet
itself, read end to end and rejected as an item); the Oct 2 and Argon editions' video-model
blocks (fal/krea/robrombach/synthesia/tavus/Luma); Bengalio/OpenAI/sama/arena benchmark
chatter. Search-level candidates rejected on date: HF "Running Qwen3.8-27B on a Single
RTX 3090" (Aug 17), silverkeytech 1-bit probe (Sep 1), daily.dev Qwen overview (Aug 22),
NVIDIA forum 256K-on-24GB thread (Aug), jpmrblood Qwen3.6 RTX 5090 post (Jun), all pre-window.

## Pass 2 deep reads (end to end, fetched this seat)

fxtwitter full JSON for: cognition/2107165034463867001, walden_yan/2107185315014144357,
realchendahuang/2106739355754869217, pidotdev/2107033061905104941,
ekzhang1/2105444878716932411, dair_ai/2107264582687584567, omarsar0/2106927371366596692,
dair_ai/2107146326639358188, ggerganov/2107190267887632462, theo/2106847019319062819.
Plus arXiv 2609.40118 abstract page, and the three AINews raw pages. 14 end-to-end
fetches; the >=5 bar passed with margin.

## Overlap adjudication (grep instruments run this sitting; the day's main event)

Four of the day's strongest-looking candidates are ALREADY IN OUR CORPUS; the overlap grep
caught all four before banking:

- arXiv 2609.32961 "Beyond Token Savings" (UT Austin, the omarsar0 tweet's paper):
  catalog row 00145d157732, FULL TEXT held at
  watch/inbox/frontier_olm_2026-10-03/sweep/_raw/2609.32961v1.txt (84,770 bytes, banked
  10-03). The Oct 5 tweet restates held numbers (35,000 runs, compression policies tuned to
  cut tokens run 20-80% slower than full context on Terminal-Bench; step-triggered policies
  need 10-27% more model calls; threshold-triggered cut 22-55% with call counts near full).
  NOT re-banked; treat the tweet as the paper's pointer. Its numbers are the freshest
  quantification of the recompute axis behind falsifier B and 2609.22114's two-axes claim.
- arXiv 2609.40118 ReCAP "Persistent Context Graphs" (Sep 30): catalog row 84a0d39ec7c1,
  abstract held at state/arxiv/2026-10-01/2609.40118v1.txt. Deep-read of the abs page this
  sitting confirms the load-bearing sentence: stores attention-derived importance scores and
  dependency links in a persistent context graph; per-request selection without additional
  model calls; vs Codex default summarization compaction it cuts estimated compaction+cold
  restoration latency ~95% on Qwen3-Coder and gpt-oss, halves historical context per call on
  SWE-Together at comparable quality, and BEATS full history by 19.8/41.2 points on
  Lost-in-Conversation code tasks. NOT re-banked as an item; the 95% cold-restoration number
  is the strongest fresh anchor for the zknot/warm_state compaction-cliff probe.
- arXiv 2609.37226 CorpusMap "Follow the Entities": catalog row 9357c7e09d70, abstract held
  at state/arxiv/2026-09-30/2609.37226v1.txt. The dair_ai tweet (entity pages, +6.4-11.7
  answer quality, -34-57% input tokens, built without LLM calls) restates held abstract
  content. NOT re-banked.
- PAIR 2609.36526: day-5 confirmed register row verified in
  watch/inbox/frontier_olm_2026-10-05/register.jsonl (area quantization-compression via
  arxiv, url arxiv.org/abs/2609.36526); catalog has 0 rows by id (register/intake lag), but
  burns.md:78 names it in the do-not-re-bank set. The Oct 6 dair_ai tweet DOES carry
  tweet-only practitioner lines absent from the abstract: the Venmo example (a summary
  dropped the "only from coworkers" filter and reported the total of all 36 payments),
  vague-prose API specs forcing ~5 steps of re-reading and re-login, and the eval-law
  sentence banked as item 6 below. Banked as an overlap-with-delta item only.

## Findings by research question

### Falsifier B (cache-writes-dominate-spend on our dispatch shape)
No fresh X evidence this window: Theo's Sep 18 economics posts remain the day-5 banked
baseline, and his only new post (Oct 4) is off-RQ. What the window DID surface is the
spend-side counterpart: 2609.32961's held measurement (token-cutting compression can be
20-80% SLOWER end to end; step-triggered cuts cost 10-27% more model calls) is the same
lesson as falsifier B in latency form: where context mutates dominates whether it shrank.
The probe order's falsifier B stays OWED and unmined; nothing banked today contradicts the
cache-writes thesis at our shapes.

### Strict-prefix cache-resume (day-4 steal, burns.md:56)
Pi Durable is a production harness built on exactly this contract: pidotdev announces
"a harness build around a small task-based workflow engine so long-running, multiplayer
agents can suspend and resume anywhere" (Oct 5); the realchendahuang design review (Oct 4,
Chinese, read in full via fxtwitter) carries the mechanism: every agent step is an
independent checkpointed task; after crash, restart or maintenance the new process attaches
to storage and continues from the exact breakpoint WITHOUT re-consuming tokens by re-walking
the long context. Storage is SQLite + JSONL with zero native bindings (runs on Bun and
Cloudflare Durable Objects); parallel session branches per instance with document-style
externalized app state; control plane (scheduling/storage) split from execution plane
(pluggable file/terminal environments); ~15K lines core; background automatic long-context
compression; repo github.com/earendil-works/pi. This is the harness-level shape of the
estate's own lane-runner resume (queue/lanes/*/runner_state.json + trail.jsonl): checkpoints
append, the prefix is never mutated mid-history. Steal: the checkpoint-per-step granularity
and the storage-attach resume (no prompt replay) as the reference implementation for the
strict-prefix cache-resume card.

### Two-axes transfer to mag.cmd context-pack (2609.22114, burns.md:77,81-82)
Transfers, now with two fresh external confirmations already in holdings (2609.32961 full
text; 2609.40118 abstract): keep-vs-recompute is decided at WRITE time (ReCAP stores
importance + dependency links when the message is fresh, then selects per request with zero
model calls; 95% off the cold-restore half of the cost) and trigger timing is a third axis
(step- vs threshold-triggered changes call counts by 10-27% at equal token cuts, per the
held full text). For context-pack composition the steal is: precompute per-block importance
and dependency links into the pack build (the catalog/FTS index already exists for this),
and prefer threshold-triggered compaction in window-close so call counts stay near
full-context baselines.

### Compaction Cliff placement (2608.22752, burns.md:78-79) and the filter pattern
Devin Dreaming (cognition, Oct 5, 2,286 likes) moves the compaction question off the context
window and onto the memory archive: "At night Devin self-improves its memory to remove
stale records and discover latent information" - maintenance as a scheduled night job over
a memory GRAPH, not a summarization filter over live context. That matches the estate's
shape (night lanes + zknot/warm_state archives) and the Open WebUI compaction-filter fit
question: the filter belongs at window close on the ARCHIVE (prune stale records, keep
dependency links), never mid-history on the live prefix (the day-5 Theo critique). The
Devin/walden_yan Agent Memory Repo standard (git + markdown backing, graph relationships,
historical records) is the concrete schema to steal for zknot continuity: the estate's
zknot re-tokenization disease (0.59% stable-leading-block share, DIGEST.md:10) is exactly
what a frozen-prefix memory substrate with append-only history attacks.

### KV q4_0 at 128k-class contexts on 7b (B4 follow-up, burns.md:59)
The X door could NOT resolve this one. Search surfaced a practitioner post claiming Qwen
3.8-27B at RTX 3090 24GB with "K/V cache quantization type to Q4_0" reaching "210k context
on 24Gb VRAM" (search snippet, engagement "5 - 321"; the engine returned the bare domain
https://x.com with NO status path, and three re-searches failed to recover the id; X is
unindexed per both day-5 and today's door log). Per the recipe fallback the snippet is
banked as a SWEEP-LEVEL LEAD with its degraded URL and explicit no-fabrication caveat: no
status id was found, so no item row is filed, and the accuracy half of the question
(q4_0 vs q8_0 quality at 128k on 7b-class models) found NO in-window X measurement at all.
Community text found is pre-window or non-X (llama.cpp GGUF cards repeating the q8_0
"low quality loss - recommended" line). The B4 A/B probe stays the estate's own instrument
for the KV cliff vs quant level; nothing banked today moves it.

## Estate steal-list (one line each)

1. Pi Durable's checkpoint-per-step + storage-attach resume is the reference implementation
   for the strict-prefix cache-resume card; map it onto lane runner_state/trail resume.
2. Agent Memory Repo (git+markdown, graph relationships, historical records) is a schema for
   zknot continuity that keeps the boot prefix byte-identical while memory grows.
3. Dreaming's night-job memory pruning is the compaction-filter pattern placed where it
   belongs: on the archive at window close, never mid-history on the live prefix.
4. ReCAP's write-time importance+dependency storage (95% off cold restoration) is the
   two-axes answer for context-pack: precompute selection signals, never reselect by model.
5. ekzhang1's PD-disagg steady-state model (prefill-heavy workloads gain most; ultra-low
   latency does not) sharpens where the fleet pays prefill vs decode on remote dispatches.

## Banked items (6, strongest first; full rows in the SweepResult)

1. cognition/status/2107165034463867001 (2026-10-05, 2,286 likes) - Devin Dreaming night
   memory-graph pruning + Agent Memory Repo OSS standard.
2. walden_yan/status/2107185315014144357 (2026-10-05, 2,196 likes) - the Agent Memory Repo
   format itself: graph relationships, historical records, git+markdown, agent-agnostic.
3. realchendahuang/status/2106739355754869217 (2026-10-04, 106 likes) - Pi Durable design
   review: checkpoint-per-step, resume without re-consuming the long context, SQLite/JSONL.
4. pidotdev/status/2107033061905104941 (2026-10-05, 851 likes) - Pi Durable announce:
   suspend and resume anywhere; why not Temporal or Effect.ts.
5. ekzhang1/status/2105444878716932411 (2026-09-30) - PD disaggregation analysis: mean
   per-token latency improves; prefill-heavy gains most; not for ultra-low latency.
6. dair_ai/status/2107264582687584567 (2026-10-06, 75 likes) - PAIR tweet, overlap-with-delta:
   compression lowers run-to-run reliability before it makes tasks unsolvable.

## Instrument receipts (this sitting)

- Reads: lens/burns.md (217 lines) in full; day-5 sweep file kv-cache-context-engineering-x.md
  (121 lines) in full; three AINews pages raw; 11 fxtwitter JSON; arXiv abs 2609.40118.
- Greps: 17 distinctive phrases vs catalog/catalog.jsonl + memory/ (md+json, agent_sessions
  excluded), two background walks, outputs quoted in-line above; 2 catalog row dumps
  (00145d157732, 84a0d39ec7c1, 9357c7e09d70, 367bcaa186eb); 1 day-5 register row dump
  (2609.36526).
- Commands: curl fxtwitter/vxtwitter/latent.space/export.arxiv.org/arxiv.org; grep extraction
  of tweet URLs from raw HTML; repo venv python for JSON parsing (bare python blocked by seat
  law, one call corrected to .venv/Scripts/python.exe).
