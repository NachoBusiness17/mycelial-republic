# Sweep: agent-memory-continuity via reddit (2026-10-05)

Area: agent-memory-continuity. Door status, method, then per-item findings with verbatim
quotes from pages fetched this session. Stamp: source-fetched: 2026-10-05.

## Doors (what actually worked)

- Primary door per recipe (old.reddit.com/*.json) BLOCKED: reddit serves a "Welcome to
  Reddit" gateway shell instead of the feed to WebFetch and to curl with a browser UA.
  Evidence saved: sweep/raw/reddit_block_evidence_20261005.html (324,365 bytes of shell,
  1 shreddit-post tag, zero post data). www.reddit.com thread pages via WebFetch return
  only the word "Reddit". pullpush.io archive API explicitly refuses agents:
  `{"error":"Rate limit exceeded. This website does not provide free scraping resources
  for agents."}` (sweep/raw/pullpush_test.json, 191 bytes).
- WORKING door found this session: reddit Atom feeds. Top-of-subreddit
  `https://www.reddit.com/r/<sub>/top/.rss?t=month` and per-thread
  `https://www.reddit.com/r/<sub>/comments/<id>/.rss` and search
  `https://www.reddit.com/r/<sub>/search.rss?q=<terms>&restrict_sr=on&sort=top&t=month`
  all return full post + comment bodies when paced (~6-25 s between calls; bursty
  requests return 0 bytes and need one retry). r/LocalLLM's top feed returned 0 bytes on
  three tries across 10+ minutes: recorded as un-fetchable, not fabricated.
- WebSearch (site:reddit.com) degraded: intermittent backend 429/1302; it contributed one
  candidate (1r9w84r) which on fetch proved to be dated 2026-02-20, outside the 30-day
  window, so it was dropped from banking. Threads readable but out of window do not count
  as window items.

## Method

Pass 1: three top-month RSS feeds (r/LocalLLaMA 25, r/MachineLearning 25, r/ollama 25)
plus four search-RSS queries ("agent memory", "long-term memory", "knowledge graph" on
r/LocalLLaMA; "long-term memory" on r/ollama) = 85 distinct candidates, all dated
2026-09-05..2026-10-05. Pass 2: eight threads fetched end to end through the per-thread
RSS door and read in full (sweep/raw/threads_readable.txt, 418 extracted entries:
post + every comment). Only items read in full are banked.

## Overlap check (run this session)

grep of catalog/catalog.jsonl (1,096,848 non-empty lines) and memory/ for "repopedia",
"OntoPrune", "JevGraph", "fractal journal", "written-at", "Persistent Memory Solutions",
"long term project/conversational memory", "code knowledge graph", "400+ LLM agents",
"recover from its own failed": zero hits. "Hindsight" hits are a different sense: arxiv
titles ("Hindsight-Distilled Sentinel", catalog id e280d985695b; "Hindsight-Guided
Rationale Distillation", 8ccefefd166d) plus incidental biography prose. Conclusion: all
banked items are new to the estate.

## Ask premise verified

mag/knowledge_graph.py:236-239 read this session: for landscape nodes, each free-text
`we_have` entry becomes an edge whose target id is `module:{Path(str(m)).name}` with rel
`already_inside` (mag/knowledge_graph.py:236-239). The target id is a filename string
built from prose, so it dangles whenever no module node was materialized under that exact
string. That is the phantom-weld mechanism the research questions target.

## Items (strongest first)

### 1. r/LocalLLaMA: "What are you all using for long term project/conversational memory these days?" (2026-09-20, 96 comments)
URL: https://www.reddit.com/r/LocalLLaMA/comments/1wl3828/what_are_you_all_using_for_long_term/
The single richest source: a community state-of-practice survey covering all four
research questions. C63 ( nitish-kmr) states the supersession law and an eval for it:
"Store a written-at date on every memory and put it in the text you embed and in what you
pass to the model, so recency is something the model can see rather than something you
hope the ranker encoded." Their eval: write ten facts that changed at least once, ask the
questions they answer, count old-version returns; "usually wrong on more than half", and
the fix is to mark the old row superseded on write when retrieval with the new text
returns it above a similarity floor. C55 (Danculus) supplies a measured failure number
for read-time reconciliation: mem0 "still brought the retired value back about half the
time (0.53, n=30)" and "The failure is silent." For RQ1: C38 reports the Hindsight
plugin's entity bank at "53K memories, 73K entities and 1.2M links between them" with a
0.9-confidence re-rank floor, session dedup, and 1.5-2k-to-300/800-token synthesis; C57
describes a SQLite entity-relationship repo memory with typed relationships pointing
"from entity to entity". For RQ4: C47 (Oriens7) splits recall from durable project state
("structured canonical state that persists independently of whichever model/session
happens to be running"), which is the community's independent rediscovery of the estate's
rib + registry doctrine; C70 proposes hot/warm/cold tiers; C29 describes a 3-tier
short/long/core-identity design with promotion and top-10 vector recall. For RQ3: C45
names two continuity evals (read a novel chapter by chapter with prediction; play text
adventure games) plus a "self-regulating retrieval bias mechanism". Overlap: none in
catalog or memory for the thread's distinctive phrases.

### 2. r/ollama: "Anima, a local persistent AI companion, powered by ollama" (2026-10-04)
URL: https://www.reddit.com/r/ollama/comments/1wxgqir/anima_a_local_persistent_ai_companion_powered_by/
The most complete shipped memory-tier architecture found, directly comparable to the
zknot recap + rib stack (RQ4). Fixed identity pages (self.md, projects.md, destiny.md,
keeper.md) ride whole every call; a fractal journal keeps yesterday verbatim, folds each
falling-out day into a ~2,000-char page the agent herself writes nightly, weeks into
~4,000-char pages, months into quarters ("it never forgets, it just fades like a person
does"); long-term facts are SQLite + nomic-embed embeddings injected as top-30 cosine +
MMR + the 6 newest, deduped across the conversation. The cache lesson is the steal for
boot freshness: "The system prompt is built once per conversation and kept byte-identical
- date without the minute, no retrieved stuff in it - so Ollama's prefix cache holds and
each reply only reads the new turns." Map to the estate: memory/zknot/LATEST.md is the
Anima "self page" layer; the biography shelf (258,840 + 65,934 rows) is the SQLite layer
lacking only the MMR + newest-N injection contract and the nightly fold job. The
byte-identical-prefix law is testable against warm boot (mag/hermes_warm_boot). Overlap:
none.

### 3. r/LocalLLaMA: "I built a code knowledge graph tool that's actually MIT licensed" (repopedia) (2026-10-03, 42 comments)
URL: https://www.reddit.com/r/LocalLLaMA/comments/1wws6o6/i_built_a_code_knowledge_graph_tool_thats/
Direct RQ2 hit: a published design that welds narrative to code. tree-sitter parse into
one local SQLite graph, no embeddings, MCP server so the agent "asks the graph directly
and gets the exact answer with file:line in one call"; blast-radius = transitive callers;
the wiki generator attaches "file:line" to every claim, which is exactly the
narrative-record-cites-implementing-module shape the estate needs for welding session
records to the modules that produced them. Incremental indexing is git-diff based at file
level (C5: only re-parse changed files, patch the graph). Crucially the author names the
estate's exact failure mode as his own: "Method calls through self. get resolved by name
matching, which is exactly as sketchy as it sounds for big class trees." That is the
same identity sin as mag/knowledge_graph.py:238's `module:{Path(str(m)).name}` target
built from free text; the fix direction is AST-resolved symbols plus file:line anchors
instead of name strings. Comment thread also surfaces sibling tools: code-review-graph
(30k stars, review workflow), codebase-memory-mcp (C binary, indexes the kernel),
codegraph (Rust), Graphify, and the LSP-with-MCP-wrapper counterpoint (C22-C23).
Overlap: none.

### 4. r/LocalLLaMA: "[Project] OntoPrune: 6.7x faster TTFT on local CPU with Ollama by neuro-symbolic context pruning" (2026-10-05)
URL: https://www.reddit.com/r/LocalLLaMA/comments/1wy6qvf/project_ontoprune_67x_faster_ttft_on_local_cpu/
RQ2 + RQ1: compiles source into an in-memory ontology KG, pulls the 1-hop SPARQL closure
of the function under edit, renders typed stubs (2,390 -> 406 tokens, -83 percent), and
then "Verifies the model's generated code against the contract AST to catch any API
hallucinations" (0 invalid calls vs 1 hallucinated with full-file context; TTFT 22.4 s ->
3.3 s on a 3B model on CPU; 9.9 ms graph overhead; ships with an MCP server). The
contract-verification leg is a deterministic anti-phantom gate: generated welds/claims
are checked against the AST before landing, which is the shape of a fix for
mag/knowledge_graph.py dangling ids (verify every weld target resolves in the module
registry at write time). One commenter pushes back on the model choice (Qwen 2.5 Coder
"vibecoded slop"); the author answers the benchmark is reproducible per-model via
`python -m ontoprune.benchmark`. Treat numbers as author-reported, unreplicated.
Overlap: none.

### 5. r/ollama: "400+ LLM agents living in a 2004-era MMO server, all local on Qwen3-4B" (2026-09-29, 36 comments)
URL: https://www.reddit.com/r/ollama/comments/1wt0tot/400_llm_agents_living_in_a_2004era_mmo_server_all/
Fleet-scale memory-tier practice (RQ4). 400+ agents, each "with its own backstory, goals,
and memory"; tier split: Qwen3-4B at 4k context runs "goals, trades, reflection, the
plausibility checks, and the short in-character replies when nobody is watching" while a
27B handles rich one-on-one talk; "When the queue backs up, low-priority reflections get
shed so chat stays responsive." That is load-shedding as a memory-tier policy: cheap
reflection jobs are the first casualty under pressure, which maps onto the estate's
janitor-first tier ladder and the sibling ractor fleet's night lanes. The OP explicitly
asks the community "how you'd handle memory at this scale"; the comment thread does not
answer that question deeply (it derails into model picks and licensing), so the value is
the architecture disclosure plus the license repair (GPL-2.0 + NOTICE listing
cmangos/playerbots upstream after being called out in C5/C6). Overlap: none.

### 6. r/ollama: "I'm testing whether a local 9B/14B coding agent can recover from its own failed code changes" (2026-09-21)
URL: https://www.reddit.com/r/ollama/comments/1wmprwb/im_testing_whether_a_local_9b14b_coding_agent_can/
RQ3: a continuity/recovery eval design. Cody runs a "graduation process" with "1,222
mandatory tests fixed in its test inventory" and deliberately trains on real failures:
a candidate that compiles but regresses a UI behavior "was kept isolated and the failure
was fed back into the development loop." The core lesson matches the estate's gate
philosophy: "simply giving the model more retries was not a good solution"; the work went
into infrastructure, "making sure the correct failure information reaches it, preventing
repeated history-reading loops, preserving failed attempts as useful diagnostic context."
Map: the estate's FIRE_LEDGER / gate stop-cert work and the biography shelf eval could
adopt the fixed-inventory graduation shape (an inventory frozen in advance, failures fed
back as diagnostic context, no success credit for prepared examples). Overlap: none.

### 7. r/LocalLLaMA: "I built JevGraph, an open-source pipeline to turn documents into evidence-backed knowledge graphs" (2026-09-21)
URL: https://www.reddit.com/r/LocalLLaMA/comments/1wm2fpf/i_built_jevgraph_an_opensource_pipeline_to_turn/
RQ1/RQ3: an entity/relation extraction benchmark template: "We froze 160 positive cases
from FewRel 1.0 train_wiki: 16 relations × 10 cases, seed 17"; all systems see the same
cases, order, and scoring; latency p95 431 ms vs 1,242/1,699 ms; cost per 100 planned
decisions 0.410 vs 1.225/1.462 cents; accuracy with uncovered cases counted as incorrect:
87.5 vs 89.375 vs 93.125 percent, reported honestly as a speed/cost-vs-accuracy tradeoff.
The template (frozen case set, fixed seed, uncovered-counts-as-wrong scoring) is directly
liftable for scoring graph-weld quality. Two cautions recorded from the same fetch: a
separate 2026-09-23 thread title (seen in the top-month feed, not deep-read:
https://www.reddit.com/r/LocalLLaMA/comments/1wo6o0f/) says "Mods: can we do something
about half the forum getting filled with these advertising posts for Jev?", and commenters
on this thread note Jev and Luna are not local models (C1, C2). Bank the benchmark
design, discount the marketing. Overlap: none.

## Out-of-window / dead doors (not banked)

- r/LocalLLaMA "Persistent Memory Solutions" (1r9w84r): fetched in full; genuinely useful
  content (structured-fact extraction vs raw embeddings; Claude Flow SQLite memory shared
  across two agent CLIs via a ~90-line MCP wrapper) but the feed dates it 2026-02-20,
  outside the 30-day window. Not counted toward the window census; recorded here so the
  door degradation is auditable.
- r/LocalLLM top feed: 0 bytes on three attempts. Not fetched, not read, not banked.

## Fix-design seeds for the estate (from what was read, not invented)

1. Weld identity: replace free-text `module:{Path(str(m)).name}` targets
   (mag/knowledge_graph.py:236-239) with AST-resolved symbol ids plus file:line anchors
   (repopedia shape), and add a write-time contract check that every weld target resolves
   in the registry (OntoPrune shape). Phantom welds become a write-time error instead of
   29-of-31 dangling edges.
2. Supersession: store written-at on every biography/registry row, embed the date in the
   indexed text, and on write run one retrieval with the new text and mark near-duplicate
   old rows superseded (nitish-kmr's law). The eval: ten changed facts, count stale
   returns; the estate's analog is ten changed state facts pulled from biography rows.
3. Boot freshness: keep the zknot recap byte-stable within a session (date without the
   minute, no per-turn retrieval inside the stable prefix) so prefix caches hold; put
   per-message deltas below the cache line (Anima C2).
4. Shelf evals: the biography shelf (258,840 + 65,934 rows) can be scored with three
   liftable designs: the frozen-case extraction benchmark (JevGraph's FewRel template),
   the supersession-stale-return count (nitish-kmr/Danculus), and the fixed-inventory
   graduation suite with failure feedback (Cody's 1,222-test inventory).
