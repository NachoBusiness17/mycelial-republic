# Sweep: agent-memory-and-continuity via reddit (frontier_olm 2026-10-03)

source-fetched: 2026-10-03. Seat: sweep-agent-memory-and-continuity-reddit (dynamic workflow child). Bank only what was fetched and read this session; every quote below is verbatim from a page fetched this session. No em-dashes outside verbatim quotes.

## Door status (the reddit door is SHUT at every path; nothing passed off as read)

- Recipe primary `https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` via WebFetch: returned only a "Welcome to Reddit" HTML shell, zero `data.children`. Same shell for r/MachineLearning, r/LocalLLM, r/ollama. This re-confirms lens/doors.md:42-52 (SHUT, working recipe OWED).
- curl with browser User-Agent on the same URL: HTTP 302, follows to `old.reddit.com/login/?reason=lor2` and lands a 324,399-byte login HTML page, not JSON. The doors.md candidate "browser-like User-Agent via curl" is now tested and DEAD: reddit demands login for all anonymous .json from this IP (reason=lor2).
- Thread-level: `old.reddit.com/r/LocalLLaMA/comments/1u21vgq.json` and the plain thread HTML both land the same login wall (HTTP 200 on the redirected login page, 324,267 bytes). WebFetch on the thread URL: same shell.
- `www.reddit.com/r/LocalLLaMA/top/?t=month`: JS shell ("Reddit", no posts).
- RSS `old.reddit.com/r/LocalLLaMA/top/.rss?t=month`: HTTP 302.
- pullpush.io archive: HTTP 429 with body "Rate limit exceeded. This website does not provide free scraping resources for agents." (retried after 45s backoff, same).
- r.jina.ai reader: 403. redlib.catsarch.com: connection failure (exit 35). redlib.perennialte.ch: 403.
- Wayback availability API alive (HTTP 200) but zero archived snapshots for all 8 candidate threads probed (1tq6sd0, 1u21vgq, 1r8cnwq, 1r5tkl3, 1sb9dex, 1s7l59p, 1u7i39v, 1rsm45d).
- Recipe fallback WebSearch (z.ai): intermittent HTTP 429 bursts (several queries returned `1302 Rate limit reached` three times in a row); sequential single queries went through. All discovery below came through this fallback; recorded as a degraded door.

Consequence, stated plainly: zero reddit thread pages were readable end to end this session. The deep-read pass was therefore executed on the primary artifacts the strongest candidates discuss (the estate's own evidence law prefers a primary record over forum chatter: memory/rib/RIB_GAME_CLAIMS_DESK.md, per lens/laws.md:14). Thread-only leads are recorded as leads with no quote, never banked.

## Method

Pass 1 (broad sweep), via the WebSearch fallback, sequential queries: site:reddit.com agent memory knowledge graph entity resolution deduplication; r/LocalLLM persistent memory knowledge graph; r/ollama agent memory SQLite knowledge graph; agent memory decay forgetting stale prune; Mem0 Zep Letta Graphiti comparison; r/MachineLearning agent memory paper benchmark; LongMemEval LoCoMo discussion; ContextBench coding agents; Graphiti entity resolution. Named candidates considered, 30-plus (in-window unless marked old):

1. r/LocalLLaMA 1u21vgq "Benchmarking Coding Agent Memory" (ContextBench thread)
2. r/LocalLLaMA 1tq6sd0 "I built an enforcement layer for AI coding agents using a knowledge graph" (Neo4j rules/skills/playbooks as typed nodes)
3. r/LocalLLaMA 1r5tkl3 "The Contradiction Conundrum in LLM Memory Systems"
4. r/LocalLLaMA 1rsm45d "How are people handling persistent memory for AI agents?"
5. r/LocalLLaMA 1r8cnwq "Analyzed 8 agent memory systems end-to-end"
6. r/LocalLLaMA "A/B Test: Claude Code Agents with Knowledge Graph vs. Grep" (permalink unresurfaced)
7. r/Neo4j "AI agents with graph memory, scaffolded in seconds" (permalink unresurfaced)
8. r/LocalLLM 1quntpp "Memora v0.2.18 persistent memory with knowledge graphs"
9. r/LocalLLM 1rujpjr "Using Obsidian Access to Give Local Model Persistent Memory"
10. r/ollama 1u7i39v "Handling context management in a local-first personal AI"
11. r/ollama 1rvpe2s "Chetna: A memory layer for AI agents" (SQLite WAL)
12. r/ollama 1sb9dex "Agent memory that keeps the story, not just the facts"
13. r/ollama 1vnhojf "Hillock v0.4" (SQLite SPO triples)
14. r/ollama 1tszsp5 "Open-source Desktop App for persistent memory, 100% local SQLite"
15. r/ollama 1syaumv "Memory for Personal AI Agents, Thoth" (local structured KG)
16. r/ollama 1skmbsh "cuba-memorys v0.7.0"
17. r/ollama 1u7i39v-adjacent r/LowEndLocalAI snippet: KG that fails mathematical overlap "blocks the LLM call entirely" (Aug 2026)
18. r/LLMDevs 1r35hlc "How are you handling persistent memory in LLM apps?"
19. r/LLMDevs 1rksuyg "Nomik open-source codebase knowledge graph (Neo4j)"
20. r/LLMDevs Memanto "Typed Semantic Memory with Information-Theoretic Retrieval" (permalink unresurfaced, unverified on arXiv)
21. r/MachineLearning "[D] Benchmarking memory systems for Agents" (LoCoMo dominance; cites the Letta blog)
22. r/LangChain 1s7l59p "Agentic AI persistent memory with auto pruning"
23. r/AgentsOfAI 1ucg4cf "Which long-term memory system are you using" (Zep temporal KG)
24. r/opencodeCLI 1r35jl4 "Reliable long term memory architecture?"
25. r/ArtificialSentience 1q54w2n "Building a knowledge graph memory system with 10M+ nodes"
26. r/LLMDevs 1k0g15e "AI Memory solutions first benchmarks 89.4% HotPotQA (cognee/Mem0/Zep-Graphiti)" (old, out of window by ID)
27. r/ollama 1q0rzbw "Jarvis" KG memory beta (old), 1gsb0ny Memoripy adaptive decay (old, out of window)
28. r/LocalLLaMA 1mj3q15, 1gvhpjj, 1ku95nk (old, out of window)
29. Primary follow: Zep paper arXiv 2501.13956 (surfaced by Zep/Graphiti threads)
30. Primary follow: Graphiti README (getzep/graphiti main)
31. Primary follow: Mem0 paper arXiv 2504.19413 (surfaced by Mem0 threads)
32. Primary follow: Letta blog benchmarking-ai-agent-memory (surfaced by the r/MachineLearning thread)
33. Primary follow: "What Eviction Destroys" arXiv 2609.08279 and "Forgetting Without Restarting" arXiv 2609.04875 (surfaced by the decay/eviction query, both also in the estate's own mirror)
34. Adjacent: FakeContextBench 2609.27603 (estate mirror, misleading-context authority)
35. Unresolved: "Always-On Agents: A Survey of Persistent Memory" (arXiv Jun 2026, search-level only)

Window honesty: reddit thread creation dates could not be verified (door SHUT), so thread candidates carry ID-ordering recency only; the banked items below carry dates read from the fetched pages themselves.

Pass 2 (deep read), fetched and read this session: arxiv.org/abs/2609.08279 (end to end), arxiv.org/abs/2609.04875 (end to end), arxiv.org/html/2501.13956v1 Zep full text (entity resolution + invalidation sections), arxiv.org/abs/2504.19413 Mem0, letta.com/blog/benchmarking-ai-agent-memory (end to end), raw.githubusercontent.com/getzep/graphiti/main/README.md (28,280 bytes fetched; key lines read). That is 5 end-to-end page reads plus the README, satisfying the 5-floor on readable primaries.

## Estate grounding probe (run this ask, first-hand)

`.venv/Scripts/python.exe` parse of `memory/knowledge_graph.json` (772,996 bytes) this session: nodes 2086, edges 825, nodes with id exactly "law:" 300, dangling edges 825 of 825 (no edge endpoint resolves to a registered node id), zero-edge nodes 2086 of 2086. This updates lens/graph.md:18-20 (1,057 zero-edge, 823 dangling) and matches the HN sibling's same-day re-parse (sweep/agent-memory-and-continuity-hn.md:13): by current bytes the graph joins nothing; repair is total, not partial.

## Answers to the four questions (from what was read)

### Q1. Entity resolution / id-dedup for KG repair (300 `law:` dups, 825 dangling edges)

Shipped-framework practice (Zep/Graphiti) resolves entities with a retrieve-then-judge loop: embed entity names in a 1024-dim space, cosine similarity plus full-text search for candidate nodes, then an LLM entity-resolution prompt decides duplicates and emits merged name/summary/uuid ("return 'is_duplicate: true'... plus the uuid of the existing node", arxiv.org/html/2501.13956v1). The README pins the dependency: "Graphiti depends on structured (JSON) output for entity/edge extraction and deduplication" (getzep/graphiti README, line 594). Estate translation: this mechanism needs a distinguishing surface to match on, and the 300 `law:` nodes have none (identical id, empty summary, per lens/graph.md:19 and today's re-parse). The applicable order is the percolator identity-fix first (full normalized law-text ids, the candidate already citing mag/knowledge_graph.py:165 in memory/percolator/candidates.jsonl per the arxiv sibling's census), and only then similarity-based dedup becomes runnable. For the dangling edges, Graphiti's provenance law ("Every entity and relationship traces back to the episodes (raw data) that produced it", README line 121) is the repair shape: re-key each edge endpoint from its source row (skill_ledger.jsonl for the `has_invariant` spokes), not fuzzy-matching on mangled ids.

### Q2. Memory architectures with measured long-horizon gains

The scoreboard remains LoCoMo/LongMemEval. Measured reads this session: Zep paper claims DMR 94.8% vs MemGPT 93.4% and "accuracy improvements of up to 18.5% while simultaneously reducing response latency by 90%" (arxiv.org/abs/2501.13956); Mem0 claims 26% relative LLM-judge gain over OpenAI, graph variant +2% overall, "91% lower p95 latency and saves more than 90% token cost" (arxiv.org/abs/2504.19413); Letta's rebuttal post shows a plain filesystem agent at 74.0% LoCoMo beating Mem0's reported graph 68.5% and concludes "The quality of an agent's memory often depends more on the underlying agentic system's ability to manage context and call tools than on the memory tools themselves" (letta.com blog, 2025-08-12). Community comparative threads (1r8cnwq, 1k0g15e, the r/ML benchmarking thread) orbit these same three families; no in-window episodic/semantic-split ablation surfaced through this door. The estate's files-are-truth spine gets outside corroboration from the Letta filesystem result, with the caveat that all three claims are vendor-authored.

### Q3. Decay/expiry policies with ablations vs the 30-day row expiry spend law

The only per-policy, per-item ablation found in this window is "What Eviction Destroys" (2609.08279, 2026-09-08, sole author Chen Shen): FIFO, random, redundancy-aware, and LLM-importance eviction audited on LongMemEval-S at three budgets, with a restore-counterfactual that separates irreversible eviction loss from recoverable retrieval failure. Numbers: at 80k budget with top-k retrieval the irreversible share is 0.67-0.73 for FIFO/random/redundancy-aware vs 0.60 for LLM-importance; at 8k it is 1.00 for all four; a matched-accuracy analysis detects no difference among accuracy-matched pairs (resolution 1.2-6 points). Two honest gaps: no time-decay or TTL policy is in the audited set, and the null result means no published evidence ranks wall-clock expiry over importance at matched accuracy. The 30-day law therefore has no published direct ablation anywhere this door reached; the estate-side test worth running is the HN sibling's EngramRAG-derived one (rank routing rows by routed-dispatch load vs age) plus this paper's restore-counterfactual as the audit instrument.

### Q4. Stale memory/context invalidation, measured best practice

Two independent shipped/published mechanisms converge with the estate's stale-cache law (memory/rib/RIB_RAM_CACHE_STALE_SNAPSHOT_20260825.md per lens/laws.md:48): (a) Zep/Graphiti bi-temporal edges carry four timestamps and contradictions are handled by invalidation, never deletion: "When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge" (arxiv.org/html/2501.13956v1); README: "When information changes, old facts are invalidated, not deleted" with history queryable at any point in time. (b) "Forgetting Without Restarting" (2609.04875, 2026-09-04) proves deletion-only forgetting leaves every derived artifact tainted (summaries, plans, KV cache): instruction-based forgetting collapsed under elicitation (Leak@probes = 1.00), and exact unlearning needs at least T-tau+1 recomputed transitions; Provenance-Guided Selective Replay hits full-reset quality "at up to 9x fewer recomputed tokens". The measured best practice is therefore invalidation-with-history plus provenance-closed recomputation, which is the chain-owns-the-record + freshness-fingerprint shape the estate already holds; the new steal is the four-timestamp edge schema and the derived-artifact closure argument.

## Banked items (full detail in the submitted SweepResult)

1. What Eviction Destroys (2609.08279, 2026-09-08) - Q3 eviction-policy ablation + restore-counterfactual audit
2. Zep: A Temporal Knowledge Graph Architecture (2501.13956, 2025-01-20, shipped framework) - Q1 entity resolution + Q4 edge invalidation mechanics
3. Forgetting Without Restarting (2609.04875, 2026-09-04) - Q4 execution-state unlearning bound, PGSR
4. Graphiti README (getzep/graphiti main, fetched 2026-10-03) - Q1/Q4 shipped bi-temporal practice, provenance, structured-output dedup dependency
5. Mem0 paper (2504.19413, 2025-04-28, shipped framework) - Q2/Q4 consolidation ops, latency/token numbers
6. Letta benchmarking-ai-agent-memory (2025-08-12, out of window, surfaced by the r/MachineLearning thread) - Q2 filesystem-vs-graph scoreboard + benchmark critique

Items 2, 5, 6 are outside the 30-day window by publish date and are banked as shipped-framework/primary context the reddit candidates point at, dates marked. Reddit thread pages: none readable, none quoted, none fabricated.

## Overlap census (run this session)

- `grep -c "What Eviction Destroys" catalog/catalog.jsonl` = 1, row `catalog/catalog.jsonl:443305` = the raw daily-mirror abstract pull `state/arxiv/2026-09-09/2609.08279v1.txt` (1,950 bytes); no memory/ hits. Same pattern for "Forgetting Without Restarting": 1 catalog row `:443100` = `state/arxiv/2026-09-07/2609.04875v1.txt`, plus memory/trajectory/steps.jsonl (this session's own step log, self-echo). Zero hits for both ids in `memory/runs/corpus_gap_research/ARXIV_REGISTER.json` and every `watch/inbox/burn_reset_20260927/flash50/*.md`. Neither paper has any prior estate research holding. Today's arxiv sibling names 2609.04875 feed-level-unbanked (sweep/agent-memory-and-continuity-arxiv.md:45); this seat adds the end-to-end read and the leakage numbers.
- "Temporal Knowledge Graph Architecture" = 1 catalog row `:351317` = `mine/raw/agent_bleeding_edge/getzep/zep/benchmarks/longmemeval/README.md` (the Aug 2026 getzep raw mine), PLUS memory/ hits this seat initially missed: `memory/runs/corpus_gap_research/ARXIV_REGISTER.json:2525` (the Zep paper IS registered) and `MAP_BACKFILL.md:416` mapping it to `watch/inbox/burn_reset_20260927/flash50/stealth-sw-06.md`, which already banked the Zep ABSTRACT-level claims (stealth-sw-06.md:36: DMR 94.8% vs 93.4%, LongMemEval +18.5% / ~90% latency) with the caveat "I fetched the abstract only; the bi-temporal model internals, community detection, and edge-construction details were not verified this session." This seat's item is therefore a GAP-CLOSE, not a first find: it adds the full-text entity-resolution and edge-invalidation mechanics the prior receipt flagged unverified.
- "Graphiti" (catalog.jsonl case-sensitive count 0; case-insensitive 2 rows) = the local Zep repo mine incl. legacy Graphiti source (`mine/raw/agent_bleeding_edge/getzep/zep/legacy/src/lib/graphiti/service_ce.go`) and an ALREADY-FETCHED Graphiti README copy at `watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/graphiti.readme.md` (09-25 gala lane). 4 memory/agent_sessions tapes (`orc-t07cf6a2b23`, `orc-t61dc81118b`, `orc-ta62b75c0fe`, `orc-tb9c265c8bc`) show prior seats reading the mirrored Graphiti source. The README item below is a RE-READ of current main with three load-bearing lines extracted, not a first fetch; the artifact was already in-house.
- "Mem0": 43 catalog rows, all mined integration source files from repo mirrors (Mem0SidebarGUI.tsx, Mem0Api.credentials.ts, Mem0.node.test.ts, etc.), 0 agent_sessions rows in catalog. CORRECTION below: the Mem0 paper itself is already deep-held.
- "benchmarking-ai-agent-memory", "Always-On Agents", "restore counterfactual", "execution-state unlearning", "edge invalidation": zero catalog rows and zero memory/ hits beyond this session's own steps.jsonl self-echo (and one week-old raw concat, memory/runs/quote_audit_wide_20260925/inbox_concat.txt). The Letta post and both in-window papers are unheld.
- Sibling sweeps checked for double-banking: today's arxiv sibling (8 banked items, none of mine), today's HN sibling (8 banked items, none of mine), the 2026-09-28 arxiv sibling (7 banked items, none of mine).

## Checks run / not run

- RUN: four WebFetch reddit-JSON door probes (all shells); curl browser-UA probes on .json, thread .json, thread HTML, RSS (login wall reason=lor2, outputs above); www.reddit HTML probe; pullpush x3 (429, body quoted); r.jina.ai (403); redlib x2 (403, conn fail); wayback availability x8 (zero snapshots); 10+ sequential WebSearch fallback queries; 6 primary-page fetches (5 end to end + README); first-hand knowledge_graph.json parse (command and outputs above); overlap greps (outputs above).
- NOT RUN: any reddit thread page read (impossible through every door; leads listed unquoted); ContextBench primary (no arXiv id resurfaced; the estate mirror's ContextBench hit 2609.27603 is FakeContextBench, a different benchmark); Memanto reddit post verification (not on arXiv by search; OWED); any estate-side repair or benchmark execution.
- OWED: a working anonymous reddit read recipe (candidates exhausted this session: .json, www, RSS, pullpush, jina, redlib x2, wayback x8; none readable); full-text bodies of 2501.13956 beyond the HTML sections read; Memanto's reproducible datasets.

## ERRATUM (2026-10-03, same session, appended per open-append law)

The background overlap grep completed AFTER this file's first write; its full log contradicted two first-pass claims and sharpened a third. Corrections:

1. RETIRED from the banked list: item 5, the Mem0 paper (2504.19413). It is already deep-held: `watch/inbox/burn_reset_20260927/flash50/w3-research-memai.md:12` records a full-HTML read ("5 WebFetch primary-source reads: arxiv.org/html/2504.19413v1 (Mem0 full te[xt]") and `:60` headings the same ("### 2.2 Mem0 (arXiv 2504.19413, fetched full HTML this pass)"), and the paper id is registered in ARXIV_REGISTER.json and MAP_BACKFILL.md. Re-banking known work is waste; this seat's abstract-page read added nothing over the in-house full-text read. The submitted SweepResult (6 items) should be read as 5 standing items plus this retired pointer: eviction audit (2609.08279), Zep gap-close (2501.13956), unlearning bound (2609.04875), Graphiti README re-read, Letta post.
2. CORRECTED: "Graphiti zero memory/ hits" was wrong. Estate holdings: already-fetched README copy (gala 09-25), legacy Graphiti source in the zep repo mine, 4 seat-session tapes that read it. The item stands only as a current-main re-read extracting the dedup-dependency, invalidation, and provenance lines.
3. CORRECTED: the Zep paper was already registered (ARXIV_REGISTER.json:2525, MAP_BACKFILL.md:416) with an abstract-only read at stealth-sw-06.md:36 that explicitly flagged the internals unverified. The item's newness is precisely the flagged gap it closes (entity-resolution prompt mechanics, four-timestamp invalidation), which stands.
4. UNCHANGED, now verified harder: 2609.08279 and 2609.04875 have zero holdings in ARXIV_REGISTER.json, all 400-plus flash50 files, catalog (beyond raw mirror rows), and memory/ (beyond this session's own step log). These two are the sweep's genuine finds, and they are the two in-window ones.

## Falsifiers / next probes for the estate

1. If the percolator identity-fix lands, re-run this seat's parse: the 300 `law:` dups should go to 0 and the Zep retrieve-then-judge dedup becomes runnable on real surfaces; if dups persist, the fix was not landed and similarity dedup stays unrunnable.
2. Run 2609.08279's restore-counterfactual shape on the estate's own routing-grid staleness: reinstate a stale row's fresh re-measure beside the stale row and classify seat errors as recoverable vs irreversible; if the 30-day law's expiries are mostly recoverable retrieval failures, the law is over-pruning.
3. Adopt the four-timestamp edge schema (t_created/t_expired + t_valid/t_invalid) on knowledge_graph edges during repair: it converts the 825 dangling-edge repair from a destructive rewrite into a recorded invalidation, matching the open-append single-item law (lens/laws.md:17).

---

# AMENDMENT (2026-10-03, second seat, same ask re-run): THE REDDIT DOOR WAS NOT SHUT

source-fetched: 2026-10-03. This seat re-ran the same ask after the first seat declared the door SHUT. The first seat's door census was correct for every path it tried, but it missed one: **the Arctic Shift public archive API (`arctic-shift.photon-reddit.com`)** served full post objects (selftext, score, num_comments, created_utc, permalink) and full comment trees anonymously all session. Every path it exhausted was re-confirmed dead this session: old.reddit .json 302→login `reason=lor2` (curl, browser UA), www.reddit "blocked by network security" wall, RSS 403, pullpush 429 with the anti-agent body, redlib.catsarch gandalf JS challenge, safereddit Anubis PoW, red.arancia.click a parked for-sale domain, web_reader MCP landed the "Please wait for verification" page. Recipe fallback WebSearch ran degraded (z.ai 1302 rate-limit bursts; the site:reddit.com filter not honored). The OWED item at the bottom of the first seat's report ("a working anonymous reddit read recipe") is therefore CLOSED: arctic-shift is the recipe.

## Method (this seat)

Pass 1: harvested 7,800 posts from r/LocalLLaMA (2,600), r/LocalLLM (3,900), r/MachineLearning (700), r/ollama (600), window 2026-09-04..2026-10-04, via `arctic-shift.photon-reddit.com/api/posts/search` paged by `before` (script: `%TEMP%/arctic_harvest.py`, run with the repo venv). Keyword-scored to 61 on-topic candidates (`arctic_rank.py`, `arctic_rank2.py`), considered all 61; well past the 30-candidate floor.

Pass 2: deep-read end to end (selftext in full plus top-scored comment trees via `/api/comments/search?link_id=`): 1wl3828, 1wlbqnl, 1wtgyzm, 1wh7ti0, 1wanjup, 1wak3fy, 1wpvr1u, 1wvmps7, 1wi0som, 1wbgqnp, 1wklq52, 1wezs4q, plus the 1wtgyzm image artifact fetched and read directly (i.redd.it/eh3u2h19yhsh1.png, 2600x1160 benchmark chart). 13 artifacts read. Two threads were moderator-removed (`[removed]` selftext, zero comments: 1wanjup/1wak3fy "We beat mem0 on LongMemEval-S", 1wezs4q) - titles only, nothing quoted, NOT banked. Quote rule: quotes below are verbatim from fetched bytes; whitespace-normalized only.

## The 8 banked items (strongest first; full schema in the submitted SweepResult)

1. **1wbgqnp r/LocalLLaMA 2026-09-09 "Is anyone working on conversation compaction?" (16pts, 39c)** - THE re-derivability convergence. Top comment (15pts): "I keep durable facts in a searchable store, one-line pointers in a small fixed buffer, and compiled knowledge from an append-only log." and "Each rollup is a new chance to drift, and you can't verify against the original once it's gone." A second commenter names the failure "autophagy" ("by message 130 it's several generations deep on its own writing with nothing external to anchor against") and contributes the cold-replay diagnostic (replay the exact payload that broke as a single cold request to separate summary poisoning from KV-cache staleness). This is independent practitioner convergence with the estate's banked re-derivability result (2609.32802, burns.md:88): summaries-of-summaries drift; re-derive from the append-only log. Overlap: tagged considered-not-deep-read and explicitly left UNCLAIMED by the 10-01 swarm-orchestration sibling (sweep/swarm-orchestration-reddit.md:51). First deep claim is this seat's.
2. **1wtgyzm r/LocalLLM 2026-09-29 "An imported doc repeats a lie 8 times. Vector RAG served the lie instead of the truth on 22/60 questions..."** - the content-free-duplicate failure mode measured as a function of repetition count R (1x/2x/3x/8x arms, 60 questions, k=6, zero LLM tokens): vector RAG displacement grows with R (22/60 at 8x) while a deduplicated keyword arm stays at 0 and the author's memory layer holds 60/60. Chart footer, read off the fetched PNG: "Plain keyword search never drops the truth, but it serves both versions every time and leaves the model to guess." Source line names the instrument: "Dermioz - scripts/banc_document_menteur.py @ 99df31d - membench corpus - 29 Sept 2026". This is lens/graph.md's 300 `law:` duplicates restated as a retrieval law: multiplicity without identity displacement truth, so ingest-time dedup (identity, not count) is the healing order. Overlap: listed as an RQ4 candidate lead by the 10-01 kv-cache sibling (sweep/kv-cache-context-engineering-reddit.md:16), candidate list only; first deep claim (including the image read) is this seat's.
3. **1wlbqnl r/LocalLLaMA 2026-09-20 "Building better memory for your agents - you don't need a product, just a philosophy" (20c)** - the comment tree carries the Q1/Q2 gold (the selftext was already partially read by the 09-30 sibling; the comment tree is this seat's fresh material): u/Danculus: "Superseding has to be keyed on the value itself: once a value is retired for a key, a plain restatement does not un-retire it" - supersede keyed on value identity, not write recency, i.e. the ingest-time identity discipline lens/graph.md demands. Same commenter on the outcome-metric unit (Q2): "I ended up trusting only memories whose outcome something outside the agent had confirmed" after a self-grading agent confirmed a planted memory. Externally-confirmed outcome is a citable unit for a rib.
4. **1wpvr1u r/LocalLLM 2026-09-25 "Show HN: DeltaLayer - Carry changes, not entire context, across AI coding sessions"** - a residual model matching docs/DNA.md: "persist change ownership, not context": a rebuildable PROJECT.md plus one Delta per conversation; "A conversation can revise its own Delta while it is active, but a later conversation never takes ownership of an older one." Author is honest about evidence limits ("not enough to claim that it reduces total token usage"). Direct input for Q5's what-warm-boot-carries: carry deltas plus a rebuildable view, verify against present reality (git/tests) before trusting.
5. **1wvmps7 r/LocalLLaMA 2026-10-02 "I built a cross-client AI memory hub - 23 AI coding agents sharing one SQLite file (MemTether)"** - the shared-surface pattern (watch/inbox contract, many clients one store) with three features the estate's knowledge-graph repair wants: "Source attribution (knows which agent wrote each memory)", "Bi-temporal (what was true vs what the system knew)", and Q-value ranking (memories that get used rank higher) - attribution is exactly the join key the 825 dangling edges lack, and every client writing one shared file with provenance is the shared-surface contract enforced in schema. No comments yet; feature claims are author-stated.
6. **1wi0som r/LocalLLM 2026-09-16 "Ai agent lost memory.md then remember the time it was losing a memory"** - the continuity fail-closed lesson, in vivo: a migration script's string-typed path made all writes fail, the keep set went empty, and the rewriter obediently wrote emptiness: "It did exactly what it was told. 'Here's what to keep: . Rewrite the file.' Poof." Continuity state (warm_state.json, memory.md, registry) must refuse to rewrite from an empty keep set - fail-closed, the dd-not-clear-room-gate reflex applied to memory. Recovery ran off a layered store (SQLite working memory + Obsidian vault + ChromaDB), which is also the residual+registry+leaf argument.
7. **1wh7ti0 r/LocalLLaMA 2026-09-15 "Measured: how much does cross-book retrieval degrade when the index grows 9x?" (LOW CONFIDENCE)** - self-reported 275-question gold set: Recall@8 100→98.1%, MRR 0.952→0.926 at 9x index growth; the 4 misses are cross-content duplicates outranking the true source ("citation points at the wrong book"); and the stale-key incident is the prose-pasted-id failure verbatim: gold-set chunk keys "pointed at nothing" after re-chunking, fixed by "put an index fingerprint in the retrieval cache key so a stale set can't silently corrupt a baseline" - id normalization at ingest (keys bound to the index generation), with the practical corollary that the same fingerprint belongs in any re-derived summary's cache key. CONFIDENCE PENALTY, stated: two commenters report the post was removed and reposted ("your post was removed yesterday, so you come again today with a slightly modified version of the same slop?"), and the numbers are unverified self-report; banked for the mechanism, not the magnitudes.
8. **1wklq52 r/LocalLLM 2026-09-19 "Harness Implementation of Long Term Memory" (3pts, 8c)** - practitioner warm-boot contract in one comment (u/MaxSpecs' takeover prompt): "Do not try to reconstruct the history of the previous conversation. Your reference source is: PROJECT_STATE.md" followed by read-only-first and batch scoping rules - the minimal residual set as an operating instruction: one canonical state file, no history reconstruction, verify against the repo. Corroborates Q5's direction (state file + pointers, not transcript).

## Overlap census (this seat, run via git grep over catalog/memory/watch/inbox plus direct greps)

- "DeltaLayer", "MemTether", "banc_document_menteur", "re-derive summaries from the log", "retired for a key": zero hits in catalog/catalog.jsonl, memory/, and all sibling banks - first holdings. The only DeltaLayer/arctic hits inside sweep/ are this run family's own scratch harvests (sweep/arctic_LocalLLM.json, sweep/tmp/candidates_full.jsonl), i.e. self-echo from the earlier crashed attempt of this same ask.
- 1wl3828 and 1wlbqnl were already read by the 09-30 sibling (fully / partially, sweep/agent-memory-continuity-reddit.md:32,134): 1wl3828 is therefore NOT re-banked (re-banking known work is waste); 1wlbqnl is banked only on its comment-tree material, which the 09-30 partial selftext read does not cover.
- 1wbgqnp: explicitly unclaimed (10-01 sibling, :51). 1wtgyzm: candidate list only (10-01 sibling, :16). "conversation compaction" phrase also appears in corpus/telegram MrPool quote files - coincidence of phrasing, different content. "autophagy" in MrPool files is the biology term, unrelated.
- "second brain" hits (16 files) are estate self-descriptions and the yonatankarp write-up mentions, not any of this seat's threads. "memory gateway" catalog row is the head-museum "Interface as Memory Gateway" principle - phrase coincidence.
- LongMemEval holdings (getzep benchmark clone under mine/raw/agent_bleeding_edge, ARXIV_REGISTER Zep row) are about the benchmark, not the [removed] "we beat mem0" posts, which stay unbanked.

## Checks run / not run (this seat)

- RUN: 4-subreddit 30-day arctic harvest (7,800 rows), keyword ranking (61 candidates), 13 deep artifact reads (12 threads selftext+comments, 1 image), door probes on old/www reddit, RSS, pullpush, 5 redlib hosts, web_reader; overlap greps (git grep phrase census above, plus the earlier direct greps for the same phrases); sibling-bank overlap reads (09-30 continuity, 10-01 kv-cache and swarm-orchestration, today's first-seat reddit receipt).
- NOT RUN: any estate-side repair (knowledge_graph.json untouched); no independent verification of self-reported benchmark numbers (1wtgyzm chart, 1wh7ti0 tables); the [removed] LongMemEval posts' content is unrecoverable through this door.
- OWED: replicate the 1wtgyzm bench shape (a repeated-fact arm) against memory/knowledge_graph.json before and after the identity fix, as the falsifier for the dedup-at-ingest order; DiffBot-style re-read of 1wl3828's comment tree for comments newer than 2026-09-30 (its thread is still growing: 93c at read time).

