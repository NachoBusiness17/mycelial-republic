# SWEEP: agent-memory-continuity via reddit - frontier_olm 2026-09-30

source-fetched: 2026-09-30. Seat: sweep-agent-memory-continuity-reddit. Area questions:
`watch/inbox/frontier_olm_2026-09-30/lens/questions.md:96-113` (5 research questions), estate
map `questions.md:115-118` (mag/knowledge_graph.py three id defects, mag/hermes_warm_boot.py,
tools/corpus_fts_rebuild.py B2-465 heal loop).

## Doors (honest status)

- old.reddit.com `.json` top: **WALLED, re-confirmed live this session** - `curl` followed the
  302 to `https://old.reddit.com/login/?reason=lor2&dest=...` (login wall); www and np reddit
  `.json` return 403. WebFetch on old.reddit thread HTML and www.reddit thread HTML both
  returned only the JS shell ("Welcome to Reddit" / bare "Reddit"). This matches the 09-28
  door state (questions.md:13-16, doors.md:41-44).
- Fallback used per recipe: WebSearch `site:reddit.com` (worked, surfaced ~40 candidate
  threads, but the engine's index skews old - only 1 of 40 was inside the 30-day window).
- Route-around found and used: **pullpush.io API** (api.pullpush.io/reddit/search/submission
  and /comment). `ids=` lookups reliable (200); `q=` search endpoints heavily 429-throttled.
  **arctic-shift API** (arctic-shift.photon-reddit.com/api/posts/search) worked with 55-65s
  spacing; 422-throttled otherwise. Landed windows: r/LocalLLaMA title=memory/graph, r/AI_Agents
  title=graph, r/Rag title=memory/graph, r/ollama title=memory, r/ClaudeCode title=memory,
  r/LLMDevs title=memory, r/AIMemory full, r/KnowledgeGraph title=memory (empty). **Never
  landed (422 x3 each): r/MachineLearning title=memory, r/LocalLLM title=memory, r/AI_Agents
  title=memory, r/LocalLLaMA title=session** - those cells are gaps, not silently covered.

## Pool

In-window (2026-08-31..09-30) candidates considered: **142 unique arctic rows + 12 pullpush
AIMemory rows + ~40 WebSearch rows, >= 160 considered, well past the 30 minimum.** Deep reads
(selftext end to end, most plus comment trees via pullpush): 1wkdoqn, 1veeix3(+100 comments),
1ujp3pq(+comments), 1s1jlnd, 1sc5zpf(+comments), 1tod2hv(+comments), 1tgm63n, 1ta42fo,
1wo6qew(+26), 1w9sklm(+36), 1wl3828(+100), 1wj4yry, 1wm5iiy, 1wmrgcg, 1wlbqnl(partial),
1wmf590(partial), 1w5aqrr. All quotes below were read from bytes fetched this session.

Door observation: r/AIMemory and r/LLMDevs 09-29/30 are flooded by a same-day "Hindsight"
(Vectorize) post wave (20+ threads, score 1, near-identical titles) and a "Jev" wave crosses
r/ClaudeCode/r/Rag; three candidate threads (1wo1t2k, 1w9mh53, 1wocuw0) were [removed] after
posting. Product claims from those waves were not banked.

## Answers to the five questions

**Q1 - id-resolution / edge-integrity discipline (823/825 dangling, graph.md:13-19; three-fix
list graph.md:37).** The strongest published-adjacent discipline on reddit is 1sc5zpf
(ontology-first GraphRAG): deterministic string ids for BOTH nodes and edges
(`person:alice`, edge id `person:alice|todo|task:write book`), typed-edge endpoint constraints
enforced at write time (pipeline REJECTS edges whose endpoints violate the ontology), and the
LLM/code split: structural nodes (DOCUMENT/CHUNK) and PART_OF/NEXT/MENTS edges are created by
deterministic code, never by the model. Author is honest that entity resolution remains "a
nightmare" (fuzzy matching misses "Paul" vs "Iusztin, Paul") and embeddings go stale after
node updates. This is stealable BEFORE the graph.md:37 fix order: give every edge a
deterministic composite id and reject non-conforming endpoints at fold() time, which converts
the estate's dangling-edge class from a measurement into a write-time impossibility. Second
steal: 1wj4yry's erasure self-check (positive control + grep raw bytes) is a ready-made
integrity instrument for memory/knowledge_graph.json: delete a marker through the estate's own
API, run the compaction the estate exposes, grep the file bytes. Third: 1wm5iiy's gy refuses
invalid memory writes at write time and retracts decisions by quoting the superseded passage
with the quote verified against the old text - lifecycle enforcement the estate's law: x300
id-collapse needs. TypeGraph/1tod2hv (2026-05-26, outside window) adds scoped unique
constraints + atomic getOrCreateByConstraint so concurrent ingestion cannot split/merge ids.

**Q2 - world-rib lowering contract (laws.md:61) + cathedral ties (laws.md:70).** No reddit
thread publishes a "lowering contract" instrument under that name. The nearest published
stance is 1tod2hv's contrast: keep the world structure "a first-class declarative thing you
query, not an LLM-summarized artifact you regenerate" - i.e. a RIB should lower to a typed,
queryable substrate, not to prose renders; GraphRAG's LLM-summarized community reports are the
anti-pattern half. The two contested cathedral ties (descent order, gate style) are
estate-internal; nothing on this door tiebreaks them - reported OWED, not forced.

**Q3 - SubtleMemory (laws.md:71 cold edge). RESOLVED POSITIVE.** The estate's cold claim edge
is real and verifiable: huggingface.co/papers/2606.05761, "SubtleMemory: A Benchmark for
Fine-Grained Relational Memory Discrimination in Long-Horizon AI Agents" (Wang et al., HIT /
Shanghai AI Lab / SJTU et al.), fetched this session: "contains 1,522 evaluation instances
over 10 long histories, grounded in 1,090 relation-controlled memory-variant sets" (361
complementary / 352 nuanced / 377 contradictory; ~236 sessions and ~211.6K tokens per
history). The estate already built on it honestly: REL-MEM-1 + mag/rel_mem_eval.py
(memory/agent_sessions/orc-t27c4ffccad.json, 2026-08-26 beat) and the naive-lexical 33%
finding stand. Reddit adds the surrounding instrument landscape and its rot: 1s1jlnd audited
LoCoMo (99 score-corrupting errors / 1,540 = 6.4%; its gpt-4o-mini judge accepts 62.81% of
intentionally wrong vague answers) and shows LongMemEval-S fits whole in a modern context
window (context-window test, not memory test), then lists what a real instrument needs
(corpus larger than context, current judge models, judge that rejects wrong answers,
realistic ingestion). 1ujp3pq names the gaming patterns (content stuffing, agent swarms,
judge-prompt swaps, oracle leaks). The only in-window reddit "Subtle Memory" hit (1wkdoqn,
r/Unrouted_AI 2026-09-19) is an OpenAI product-FAQ watch post - name collision, not the
benchmark; no reddit chatter about the SubtleMemory paper itself was found.

**Q4 - 350k+ rows without index decay (B2-465 disease).** Reddit's largest measured signal:
1veeix3's Agentic Memory Index (8 systems x 272 scored tasks + 72 invented-memory traps,
judge calibrated against two human labelers, separate 5,000-page scale test): a plain
markdown wiki the agent curates itself beat every product (98.5); Zep's weakness was
freshness (162.7s median before a just-stored fact became answerable); Mem0 cheapest at $341
per 1,000 successful answers. Structural anti-decay answers on this door: single-store hybrid
retrieval so there are no cross-store sync pipelines to rot (1tod2hv: BM25 FTS5 + vectors +
graph traversal in one SQL round trip; 1shoz37, 2026-04-10, outside window: FTS5+vector
92.3% R@5 on LongMemEval-S); and 1wo6qew's billion-edge war story where the disease is
named exactly - the keyword/BM25 fallback "quietly, was often" absorbing retrieval while
users got answers, and the fix comment: "A big chunk of 76x was fixing a missing index."
That is the estate's B2-465 shape at enterprise scale: silent text-search fallback is the
symptom that hides the dead index.

**Q5 - cross-session continuity with measured numbers.** Best find: 1wmrgcg moved per-session
index processes to a shared warm daemon per checkout and MEASURED it: median startup plus one
context request 37.2 ms -> 16.4 ms across ten paired samples - and honestly flags that speed
is not sufficiency (open question: "retrieved enough code to complete the change?"). This is
the shape warm boot should be evaluated in: paired samples, one metric, honest limit. Second:
1w9sklm's top comment (u/izgorodin) gives the decay-measurement instrument: "periodic
state-reconstruction probes... time-indexed questions whose answers change across known
events, replay the same event log through each memory version, and score current-state
accuracy, as-of accuracy, stale-fact leakage, and provenance recovery. That turns months of
drift into a regression test" - directly adoptable as the warm-boot eval. Third: 1w5aqrr's
CrewAI prod post-mortem (restarts wiping state, multi-tenant scope leaks, scope-filter
applied AFTER ranking so scoped recall needs 20x overfetch) is the failure-mode checklist
for memory/warm_state.json hygiene. LongMemEval-S itself (1ta42fo) is the published
instrument with a held-out protocol (450-question held-out split, 5-seed CV, R@5 97.24%
+/- 0.12) the estate can grade warm-boot recall against.

## Overlap checks (run this session)

grep against catalog/catalog.jsonl (691,788 lines): LongMemEval 11, LoCoMo ~80, FTS5 19,
memweave 41 (estate's own doctrine name - NOTE: r/LangChain 1ta42fo's "memweave" Python
library is an unrelated name collision, not our memweave), SubtleMemory 2 (the cold edge
itself), agent_memory 6. ZERO catalog hits for: "Agentic Memory Index", "erasure_selfcheck",
"Ghost Vectors", "ontology-first", "ArcadeDB", "verginglabs", "markdown wiki". Zero matches
in watch/inbox/frontier_olm_20260928/register.jsonl for any of this sweep's item terms. No
re-banks.

## OWED / not done

- 4 subreddit x query cells never landed through arctic-shift (422 x3): r/MachineLearning
  title=memory, r/LocalLLM title=memory, r/AI_Agents title=memory, r/LocalLLaMA title=session.
  pullpush q= search stayed 429 for all subreddits after the first call per window.
- Q2 (world-rib lowering contract, cathedral tiebreaks): no reddit instrument found; reported
  open, not forced.
- Long selftexts read partially (not end to end): 1wlbqnl (10,580 chars, read ~2,800),
  1wmf590 (8,483, read ~2,800), 1s1jlnd (7,959, read ~5,600 of the LongMemEval section + all
  LoCoMo/requirements sections). Marked so nobody counts them as full reads.
- Old-window items banked with dates visible: 1sc5zpf (2026-04-04), 1veeix3 (2026-08-03),
  1s1jlnd (2026-03-23) - they are the strongest finds for Q1/Q3/Q4 respectively; the 30-day
  consideration pool itself is satisfied by 142+ in-window rows.
