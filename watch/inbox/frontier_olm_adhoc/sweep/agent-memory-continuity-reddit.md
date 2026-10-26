# Frontier sweep: agent-memory-continuity via reddit - 2026-10-11 (second adhoc pass)

source-fetched: adhoc

Seat: sweep-agent-memory-continuity-reddit (dwfrun e68f99eb, actor_3_11). This file supersedes the 2026-10-10/11 mint at this path (that run's dwfrun 5d623493; its four banked items - arXiv:2610.10845 galahad-kv eval, Compaction Memory gist, a16z Why We Need Continual Learning, Letta Benchmarking blog - remain banked there and are NOT re-banked here; its OWED thread-body list is partly cured below). Two passes run as ordered: Pass 1 considered 229 listing entries (100 from the four recipe subreddits' top/month feeds + 129 from ten targeted search feeds), all fetched this session; Pass 2 deep-read 8 threads end to end (post + comment tree rendered from thread RSS; two feeds returned post-only). Every quote below is verbatim from RSS text this seat fetched and rendered (raw XML kept as _amc_*.xml, renders as _amc_read_*.txt, scripts _amc_parse_rss.py / _amc_parse_search.py / _amc_render_threads.py in this directory). Reddit em/en-dashes are transcribed as plain hyphens per seat law; quote text is otherwise unmodified. Dates are the threads' published dates from the feeds, not fetch dates (fetched 2026-10-11 19:00-19:44 UTC).

## Door status (all three doors probed this session; degradations recorded)

| Door | Method | Result |
|---|---|---|
| old.reddit.com `/r/LocalLLaMA/top.json?t=month&limit=50` | WebFetch | WALLED: HTML "Welcome to Reddit" shell, zero posts (4th consecutive session; matches lens/doors.md:14 verdict) |
| WebSearch `site:reddit.com ...` (recipe fallback) | WebSearch | DEGRADED: first attempt returned MCP 429 rate-limit; subsequent attempts ignored the site: operator and returned neo4j.com/mem0.ai/github.com results, zero reddit threads (same failure the open-local-language-models sweep recorded) |
| www.reddit.com Atom RSS via curl + browser UA | curl (scripts inline in bash) | OPEN: subreddit top feeds (`/r/X/top/.rss?t=month`), search feeds (`/r/X/search.rss?q=...&restrict_sr=on&sort=top&t=month`), per-thread feeds (`reddit.com/comments/ID/.rss`) all returned real XML. Logged-out rate limit ~1 req/8-12s; several 0-byte replies recovered on retry (retry loops in the bash history of this session). This is the same door the kv-cache sweep proved on 2026-10-11 04:40 UTC |

The recipe's named fallback (WebSearch) was engaged and recorded as degraded; the operative door was the RSS side door. No fabrication: nothing below cites a page this seat did not fetch.

## Pass 1 - candidate inventory (229 entries considered)

- Top/month feeds (25 entries each, in-window by construction): r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama. Mostly general news; area-relevant finds: EmbeddingGemma 2 local file-search app (r/LocalLLaMA 10-10), self-hosted 35B MoE team server (r/LocalLLM 10-06).
- Search feeds on r/LocalLLaMA (and one r/MachineLearning): "agent memory" 25, "persistent memory" 17, "knowledge graph" 5, "Letta" 1, "GraphRAG" 3, "mem0 memory" 2, "self improving agent" 25, "context compaction" 25, "agent memory" r/ML 1, "LoCoMo memory benchmark" 25. NOTE: reddit search RSS leaked out-of-window posts into t=month results (1r8cnwq Feb 2026, 1mon8it Aug 2025, 1r5q7xd Feb 2026); window position of every banked item is stated below.
- Area-relevant candidates triaged and NOT deep-read (still open): pi-optchat memory tree 1wzh1i7 (banked by kv sweep), Memoria 1wyt020 (banked 10-06 amc sweep), code-KG repopedia 1wws6o6 (banked 10-05 amc sweep), JevGraph 1wm2fpf (banked 10-05 amc sweep), FRAMES 18-RAG-vs-agent-loop 1wv0lww (banked by kv + evals sweeps), KV transplants 1wq76f6 (banked kv), Spomin live KV compaction 1wdaq1v (kv-area), pi.dev compaction plugin survey 1weolwq, OpenCode cache-friendly compaction plugin (2026-09-22), Tencent Octop self-hosted assistant (10-06), Muse-open-source-on-Android 1wyhzlc, Eidon self-hosted alternative (10-05), VeriLoop E2 state-commit question 1wrmgf0 (quant ladder already held by quantization sweeps), "My AI Memory system updated" 1wltze2, AkbasCore MAM memory cartridges (r/LocalLLM 10-08, kv-flagged unread).

## Pass 2 - deep reads (8 threads fetched and read end to end this session)

All 8 rendered in full from _amc_thread_*.xml; entry counts and window position stated per item. Three of the eight are the prior mint's named OWED bodies (it could not read them: its doors were all walled).

1. 1r5q7xd "How are you handling persistent memory for AI coding agents?" (r/LocalLLaMA, published 2026-02-15, OUTSIDE 30-day window, 46 entries all read). Prior mint's #1 OWED cluster item.
2. 1r8cnwq "Analyzed 8 agent memory systems end-to-end" (r/LocalLLaMA, 2026-02-18, OUTSIDE window, 10 entries read). Prior mint's OWED.
3. 1mon8it "Woah. Letta vs Mem0." (r/LocalLLaMA, 2025-08-12, OUTSIDE window by 14 months, 53 entries read). Prior mint's OWED.
4. 1wwn7xf "Replacing vector databases with SQLite and SIMD hypervectors (Hillock)" (2026-10-03, in-window, 20 entries read).
5. 1wz12i1 "Are coding agents solving the wrong problem with code search?" (2026-10-06, in-window, post-only feed, 1 entry; comments not retrievable this session).
6. 1wmf590 "WarpState: dual-timescale associative memory + local attention" (2026-09-21, in-window, 2 entries read).
7. 1wyow7y "mem0 vs Memori for local agent memory?" (2026-10-06, in-window, 8 entries read).
8. 1wvmps7 MemTether cross-client memory hub (2026-10-02, in-window, post-only feed, 1 entry read) - read, then DROPPED from the bank: overlap check found it banked by the 10-06 swarm-orchestration sweep as its item 2.

## Overlap method and findings

Greps ran against catalog/catalog.jsonl, curated memory/ prose dirs (frontier, rib, improve, press, workflows, briefs, lenses, game, zknot, research_polished, research_packs), and all frontier_olm_2026-10-*/sweep + frontier_olm_adhoc/sweep reports. Findings that shaped the bank:

- MemTether (1wvmps7): banked 10-06 swarm-orchestration-reddit.md item 2 -> NOT banked here (its post body confirmed that bank: 23 adapters, source attribution, bi-temporal, Q-Value ranking, FTS5+bge-m3, MCP).
- Hillock: registered 10-03 as "Hillock v0.4 (SQLite SPO triples)" (agent-memory-and-continuity-reddit.md item 13, r/ollama 1vnhojf) and the 10-08 open-local sweep dropped the follow-up 1wuv6oh as same-product churn. My read is v0.8 (r/LocalLLaMA 1wwn7xf); banked below ONLY as the v0.4->v0.8 design delta (supersession columns, contradiction-edge roadmap, TALON canonicalization), with the overlap named.
- "Memori" catalog hits (19) are all translation false positives (ms-agents-beginners README translations: "Memoria para Agentes", "Memorija", "Memori untuk Agen"); the Memori product is not held.
- "re-anchor" catalog hits (4) are estate-internal verkle receipts (B2_186_uf122_eval, B2_82_verkle_reanchor), a different sense of the word; the external re-anchor handoff pattern is not held.
- birkin-mnemosyne README was deep-read by the prior amc-x sweep (held); my 1wyow7y bank carries the thread's other content and names this overlap.
- synix.dev / EverMemOS / Tacnode / Hyperspell / KAPEX / getkapex / AxiomCode / axiomcodegraph / basicmemory / mnemory / roandejager: zero hits anywhere -> genuinely new.
- Known trap (inherited from prior mint, avoided): memory/trajectory/steps.jsonl absorbs this session's own fetches as self-echo; curated dirs only, catalog + committed sweep reports are the honest signal.

## Research-question synthesis (what the fetched evidence supports)

- RQ1 (graph builder + authored cross-links surviving regen): no reddit item names our internal builder (that trace stays OWED, graph.md:18); the fetched evidence supplies three survival patterns: (a) cline's position quoted in 1r5q7xd - don't maintain a hand-built index over a moving codebase, recreate context from the source of truth; (b) Hillock v0.7's non-destructive supersession (timestamps + source_doc + confidence columns; historical rows kept, retrieval prioritizes newest verified) plus its contradiction-edge roadmap "so the model remembers why something was wrong" - the exact why_context shape the regen dropped; (c) 1r5q7xd's kernelobserver split: execution history as atomic, hash-addressed, system-level records ("So even if the model forgets, the system doesn't") and SeekratesIyer's re-anchors (session-end YAML with decisions-with-why). Read together: authored cross-links survive regen only if they live in the source artifacts the regen re-reads, not in the graph layer the regen overwrites.
- RQ2 (verkle coherence vs vector, build cost): the estate-held FRAMES bank (kv sweep item 7) already shows an agent loop with fetch tools (92.7%) beating 18 fixed RAG pipelines (78.9%); today's adds are Hillock's third way (deterministic canonical predicates in SQLite + HDC bit-packed hypervector gates, popcount gating under 0.01 ms on CPU, ingestion via bi-encoders in ~5 s with no generative LLM) and AxiomCode's deterministic-first code KG (compiler/type-grounded graph queried before the LLM spends tokens). Both are precision-over-recall structures with honest-refusal gating - the same family as verkle coherence, at measured local costs.
- RQ3 (ten-minute-self falsifiers): WarpState's author designs the exact falsifier shape the rib demands - matched triples (local-attn only / +1 memory bank / +dual) tested on retrieval at 2K->8K->32K->128K with RULER/BABILong; and the KAPEX sustained-use result in 1mon8it ("governed vs ungoverned gap only appeared after enough history accumulated", 1,655 participants, blind) is the longitudinal-divergence template for the recurring-pitfall-rate falsifier.
- RQ4 (40-day-stale fold): the recall-vs-maintenance split in 1wyow7y (compare wrong recalls AND stale recalls, not just retrieval) plus LoveMind_AI's point in 1r5q7xd ("early information that gets summarized away doesn't generate its own retrieval cues") define what a fold-cure test must measure: not can-it-retrieve, but does-fresh-fold-reduce-stale-recalls.
- RQ5 (evidence-layer designs): 1r8cnwq maps eight systems at pinned versions (four bets; "Systems with real infrastructure discipline don't do knowledge construction... Nobody's bridged that split yet"; Graphiti's bi-temporal edges + MinHash dedup; Hindsight's four retrievers on one PostgreSQL); 1r5q7xd's Signal-Tadpole-4432 supplies the claim-with-provenance schema ("where did this come from, was it observed in the repo or inferred... what would make it stale?"); mem0's only real edge per 1wyow7y is automatic conflict resolution (deciding an older memory is stale).

## Banked items (7, strongest first - see SweepResult JSON)

1. **1r5q7xd persistent memory for AI coding agents** (2026-02-15, outside window stated). Densest RQ1 answer set in one thread: re-anchor YAML handoffs, execution-history-vs-context split, claims-with-provenance, memory-as-security-boundary, Letta cache-batching internals, cline source-of-truth position.
2. **1r8cnwq 8 agent memory systems analyzed end-to-end** (2026-02-18, outside window stated). The RQ5 map at pinned versions; the infrastructure/extraction split is the estate's evidence-layer opening.
3. **1mon8it Letta vs Mem0** (2025-08-12, outside window stated). KAPEX sustained-use divergence; Letta's KG-too-hard verdict; MemGPT author's agentic-context-manager frame; LoCoMo's full-context-baseline problem. Overlaps the banked Letta blog on files-beat-extraction; the KAPEX and governance-benchmark content is the delta.
4. **1wwn7xf Hillock v0.8** (2026-10-03, in-window). Banked as the v0.4->v0.8 delta: non-destructive supersession, contradiction-edge roadmap, TALON canonicalization, HDC gating costs.
5. **1wz12i1 AxiomCode code KG** (2026-10-06, in-window, post-only). Deterministic-first retrieval for RQ2.
6. **1wmf590 WarpState dual-timescale memory** (2026-09-21, in-window). Weight-tier memory design + the matched-triple falsifier template for RQ3/RQ5.
7. **1wyow7y mem0 vs Memori** (2026-10-06, in-window). Recall-vs-maintenance split, cache-stable injection discipline, plain-files consensus.

Not banked, with reasons: 1wvmps7 MemTether (banked 10-06 swarm sweep; post body confirmed it); pi-optchat/Memoria/repopedia/JevGraph/FRAMES/KV-transplants (banked by sibling sweeps); VeriLoop E2 (quant ladder held by quantization sweeps); all remaining prior-mint OWED bodies not deep-read this session (below).

## OWED (stated, never asserted)

- Comment trees for 1wz12i1 and 1wvmps7 (feeds returned post-only this session; 1wvmps7 moot since dropped).
- Prior mint's remaining OWED bodies still unread: 1mlnvob (Letta/MemOS/Cognee kits), 1raqi5w (too many memory implementations), 1ra0ude (3 things missing), 1wbgqnp (L1-L3 hierarchical compaction), 1qrbs69, 1rejuyw, 1r6aidx (infinite context by training), 1pu9og6 (continual learning solved), 1pdy1ut (nested learning).
- The internal knowledge_graph.json builder trace (graph.md:18 OWED) - not a reddit question; no external item names it.
- Spomin, pi.dev plugin survey, OpenCode compaction plugin, AkbasCore MAM, Octop, Muse-Android, Eidon: candidate-grade only, bodies unread.

## Receipt

- Instruments: WebFetch (old.reddit probe, 1 call), WebSearch (fallback, 1 call, degraded both ways), curl with browser UA (Mozilla/5.0 ... Chrome/124.0) for all RSS fetches; parsing/render via repo venv `.venv/Scripts/python.exe` over ElementTree.
- Fetched this session (moments EDT 2026-10-11, from stat): 4 top feeds 15:00-15:04 (67,289 / 81,946 / 75,869 / 120,740 bytes); 10 search feeds (sizes in dir, several 0-byte retries recovered); 8 thread feeds 15:32-15:44 (raw XML retained as _amc_thread_*.xml).
- Overlap greps: 16 distinctive terms + 9 thread IDs over catalog/catalog.jsonl (1,136,889 lines), curated memory/ dirs, and all frontier_olm sweep reports (commands in session history; key results quoted above).
- No tests fired, no estate instruments modified; read-only sweep plus the raw-fetch artifacts named above.

Gopher: sweep-agent-memory-continuity-reddit (dwfrun e68f99eb, actor_3_11)
