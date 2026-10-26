# Frontier sweep: agent-memory-continuity via reddit - 2026-10-10

source-fetched: 2026-10-10. Seat: sweep-agent-memory-continuity-reddit (dwf run).

## Door status (recorded per recipe)

- Primary door FAILED: `old.reddit.com/r/*/top.json?t=month` (all four subs) returns Reddit's
  "Welcome / Log in" interstitial to anonymous fetchers. curl with browser UA gets HTTP 302 to
  `old.reddit.com/login/?reason=lor2&dest=...` (verified this session, both listing and thread
  URLs). `www.reddit.com/*.json` returns "You've been blocked by network security" (verified via
  webReader). Live thread pages via WebFetch return a bare "Reddit" JS-challenge shell; via
  webReader they return "Reddit - Prove your humanity" (CAPTCHA).
- Recipe fallback (WebSearch site:reddit.com) DEGRADED: the engine ignored `site:` and
  `allowed_domains`, returned non-reddit summaries, and 429/timeouted under load. It did surface
  verbatim thread snippets (used, marked degraded below).
- Working substitutes used this session: (1) Wayback CDX enumeration of reddit thread URLs
  archived 2026-09-10..2026-10-11 (discovery), (2) Wayback snapshots of reddit RSS feeds (the
  only end-to-end read door: RSS `<content>` carries verbatim post bodies served by reddit),
  (3) WebSearch engine snippets for two partial reads. Mirrors tested and dead: safereddit
  (Anubis challenge), 8 other redlib instances (down/403/418), pullpush.io (stale index, empty
  for 2026 IDs), arctic-shift (522), archive.today (no captures of targets), r.jina.ai (blocked
  for reddit until 17:01Z this session; one retry scheduled before submit).

## Pass 1 (broad sweep)

150+ in-window thread URLs enumerated via CDX (slugs grepped: memory/agent/context/session/
memoria/letta/mem0/zep/recall/remember) plus 136 titles read from six archived RSS listings
(hot Sep 11, top-day Oct 1, new Oct 3, r/ML front Sep 10, r/ML top-day Oct 2, r/ollama front
Sep 10). 30+ candidates triaged. Hardware-memory sense (VRAM/RAM bandwidth threads) excluded.

Excluded as estate-known before deep read (overlap grep hits shown):
- Memoria 1.0.0 (r/LocalLLaMA 1wyt020): README already banked
  `watch/inbox/frontier_olm_2026-10-06/sweep/_raw/memoria_readme.md` (3 catalog hits).
- FactorEngram paper thread (1wz59xj): paper already pulled `state/arxiv/2026-09-29/2609.35578v1.txt`.
- Declarative Attention (r/ML 1w7sgf3): estate built `watch/PURPLE_HARVEST_B3_DECL_ATTENTION_20260906.md`.
- Percepta Spotlight (1ww09ab): banked yesterday `watch/inbox/frontier_olm_2026-10-09/sweep/tmp/as_c_spotlight.json`.
- "I made a local LLM memory planner" (r/LocalLLM 1wdp7f2): VRAM capacity planning class, not continuity.

## Pass 2 (deep reads - items I read end to end, verbatim, via archived RSS)

1. embedflow: migrate embedding models without re-embedding (r/MachineLearning 1wc34d2, twin
   post 1wabmm7). K-doc rerank from the old index reaches native retrieval quality (qwen4b->8b
   at K=50); 63 migrations tested to 1M docs; pypi `embedflow`, github arnsri33/embedflow.
2. KV cache as an agent runtime [R] (r/MachineLearning 1w9myqc, Yandex research). Cites
   Hogwild! Inference + AsyncReasoning (arXiv 2512.10931), preview of a Qwen3.8-27B agent
   playing DOOM on KV-state techniques; thesis: runtime is an under-explored axis between
   model and harness.
3. Memory-graph schema "overfitting" [D] (r/MachineLearning 1w8ph8b). Schema of people, facts,
   claims, events, timestamps, relations benchmarked on LoCoMo; asks the cleanest test that
   the schema is not leakage.
4. ThoughtDAG (r/ollama 1wbf204). Branch a side question off a phrase, reconnect what matters;
   open source, Ollama + OpenAI-compatible.
5. Claude Code caching desperation (r/ollama 1wb4ym3). One session: 248.7M input tokens vs
   485.2k output, 0% cache read, $1255.92; the re-sent-context tax in the wild.
6. (Off-topic but read in full with comments, proves the door: "Self-hosting AI does not save
   money" 1ww2jsu, 126 RSS entries.)

Partial reads (engine snippets only, degraded door, quotes are the exact snippet bytes):
- Hillock, SQLite memory engine for Ollama, u/raondejager (r/ollama 1wwqb60). Corroborated by
  a second engine snippet surfacing the project's Show HN: "Hillock: Local neuro-symbolic
  memory engine", described as 100% local/offline, <1.2 GB VRAM on a GTX 1070 or CPU-only,
  write-up at nicheloom.com.
- "Native memory for local LLMs" (r/LocalLLaMA 1wzbnbr). TL;DR snippet only; second probe
  added nothing; thread is small (5 upvotes, 4 comments).

jina final status: retried once inside the reopened window; the block slid forward again
(403, "blocked until 17:45:28 GMT"), so the two partials stayed partial. No further retries.

## What the evidence says against the five research questions

Q1 (read-path contract of the day-9 supersession finds): the reddit layer does NOT restate the
arXiv contract (I did not fetch 2610.10265/2610.08586/2610.03902 this ask; that comparison is
OWED to the paper seats). What it adds: embedflow is a working supersession chain for the
representation layer - old index stays servable while K-doc reranking migrates quality to the
new model; no rewrite-from-scratch. A read-path contract the estate can steal: supersession
rows should carry a migration cost field (K, docs reranked) and a "native-quality reached"
threshold, not a boolean replace flag.

Q2 (automating the already_inside link): the only architecture in this window that automates
linkage at read time is Spotlight (learned sparse indexing into unbounded memory) - already
banked 10-09, so excluded from items but noted: it is the estate's closest prior art for
automatic steal-to-module edges. embedflow automates the temporal version (new model links to
old corpus without re-embedding). Nothing else in-window does the link automatically; Hillock
is a substrate (SQLite engine) not a linker - verdict: OWED, frontier is thin here.

Q3 (route-map 25x boot cut generalizing to warm_state + zknot): the Yandex KV-cache-as-runtime
thread is the strongest support with a condition: the boot cut generalizes when continuity
lives in runtime state (KV/prefill persistence, cache reads) rather than in re-read text. The
Claude-Code 0%-cache thread is the counter-condition in money form: when the harness re-sends
context and the provider never caches, warm-boot savings vanish and the tax is ~500x
(input/output ratio). Condition extracted: route-map boot cut holds iff the read path is
cache-stateful; it fails on stateless re-send harnesses.

Q4 (knowledge_graph schema v3): the memory-graph [D] thread is a live peer building exactly a
typed graph (people/facts/claims/events/timestamps/relations) and facing the estate's novelty-
check problem from the other side: is schema-aware typing overfitting? Their answer solicits a
leakage test; ours (122 orphan steals) is the mirror image - typing too poor to check novelty.
Schema v3 should steal: relation typing from their schema (claims vs events vs facts),
timestamp fields for supersession ordering, and embedflow-style migration-cost fields.

Q5 (world-rib contract): the Yandex thesis ("do we need something in between model and
harness?") names the layer the rib contract wants: runtime-level state the model reads/writes
but the harness only addresses. ThoughtDAG shows the minimal user-facing shape of that layer
(branch-and-reconnect). No thread in this window expresses a rib lowering to field/world/code;
that remains the estate's own frontier (OWED).

## Items excluded for overlap (grep receipts)

- "Memoria" -> 3 catalog hits incl. memoria_readme.md (banked 10-06).
- "FactorEngram" -> state/arxiv/2026-09-29/2609.35578v1.txt.
- "Declarative Attention" -> PURPLE_HARVEST_B3 receipt 09-06.
- "Spotlight" -> frontier_olm_2026-10-09/sweep/tmp/as_c_spotlight.json.
- "Hogwild" -> corpus/library/ai-engineering-from-scratch/.../22-async-hogwild-inference/.
- "LoCoMo" -> 82 hits (getzep benchmark code mined 08-06).
- embedflow/ThoughtDAG/"KV cache as an agent runtime"/Hillock -> 0 hits each (new).

Grep instrument: `grep -ci "<term>" catalog/catalog.jsonl` (1,469,737 lines), run 2026-10-10 this session.
