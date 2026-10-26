# Steal card: agent-memory-and-continuity via X (frontier_olm 2026-10-04, round 1)

Banked by the steal gopher. Grounding tiers, tagged on every claim: [re-run] = command executed this session; [read] = file read this session; [ask] = carried in the ask's confirmed find list (quotes, dates, prior overlap greps), not independently re-fetched here. The miner's own sweep is at `watch/inbox/frontier_olm_2026-10-04/sweep/agent-memory-and-continuity-x.md` (43 lines) [read]; its window-honesty note (only one in-window post, funes 2026-10-04) is sweep line 10.

## The steal, as one mechanism

Adopt the addressability law for agent memory: raw rows (sessions, skill fires, verkle knots) stay individually addressable forever, and every continuity artifact becomes a REGENERATED VIEW over those rows instead of a hand-shaped summary. Five sub-mechanisms, all seven finds converge on them:

1. Rows-and-views split: sessions are raw rows, the brief is a view, and every recalled claim carries its turn pointer (funes: `recall` returns ranked passages, `get` reassembles one cited turn) [ask + sweep:14].
2. Offline consolidation as propose-accept: a background pass analyzes trajectories and proposes memory updates; only accepted results are stored (LangSmith Engine sleep-time compute) [ask]. This is exactly the shape zknot's logon window should take: `tools/zknot.py` already rewrites LATEST.md deterministically from the last 3 sessions (`last3 = [cards[s["id"]] for s in real[:3] ...]` at tools/zknot.py:273, write at :285) [read]; the port is to log proposals to the percolator instead of overwriting in place.
3. Compile-at-ingest + scheduled lint: regenerate wiki/graph views from source rows at ingest, then lint for disagreement, staleness, and orphans (mem0 agent wikis) [ask]. The lint classes map 1:1 onto the estate's verified graph defects: 1,057 of 2,086 nodes have zero edges (orphans), all 400 knots are content-less stubs (staleness), all 300 case_law share the empty id `law:` (identity collapse) [read: lens/graph.md:9,26,27,28].
4. Identity schema: per-entity link keys so precedent rows stay separately retrievable (mem0 token-efficient memory's entity-link layer) [ask]. The graph builder currently does the opposite: `law:{str(r.get('id') or '')[:12]}` at mag/knowledge_graph.py:123 builds `law:` from rows that carry no id field [read], collapsing 300 skill_ledger rows onto one node.
5. Budget law with a drift guard: retrieval beats stuffing on long-horizon tasks at any window size, and competitive accuracy holds under ~7,000 tokens per retrieval call, so warm state stays brief-plus-tips (below the knee) and the real risk is drift, not size (BEAM/MEM1 + mem0 + the Claude Code silent 200-line index cap) [ask x3]. The drift guard is the estate's own census-carrier lesson in shipped-product form: index carriers that truncate silently with freshness warnings only on loaded rows are how census claims rot; `memory/warm_state.json` is 998 B today [re-run: ls] and must never shed rows without a gate.

## Find-by-find: organ, port move, probe

1. **funes (DanKornas, 2026-10-04, in-window)** [ask; detail read at sweep:14]. Organ: context pack + continuity (zknot LATEST.md, memory/warm_state.json). Port: split zknot into rows-plus-view, add recall(rank)/get(cited-turn) over the session SQLite it already reads (tools/zknot.py:89 load). Probe: rebuild the boot recap for one real logon as top-k cited passages and score answer-presence for the 10 most recent boot questions against the current hand-shaped recap; falsified if the cited-passage view loses on answer presence.
2. **Hivemind LoCoMo measurement (DanKornas/Activeloop, 2026-06-09)** [ask; read at sweep:22]. Organ: gopher fleet skill cards + percolator. Port: capture-codify-propagate, session traces promote recurring patterns into SKILL.md cards via percolator candidates. Probe: replay one closed lane's trace through the pipeline and falsify-or-confirm the banked 25% cheaper / 1.7x fewer tokens / 31% fewer turns envelope on our own workload.
3. **LangSmith Engine as sleep-time compute (hwchase17, 2026-06-24)** [ask]. Organ: percolator + zknot window. Port: logon pass writes PROPOSED rows, registry holds only accepted ones. Probe: flip one zknot section to propose-accept and count how many proposals a human gate would reject; a near-zero reject rate falsifies the need for the gate (and a high one falsifies silent overwrite).
4. **mem0 agent wikis (2026-07-21)** [ask]. Organ: knowledge graph builder (mag/knowledge_graph.py) fed by verkle_chain.jsonl + skill_ledger.jsonl. Port: compile-at-ingest regeneration plus the disagreement/staleness/orphan lint. Probe: see headline probe below.
5. **Claude Code silent 200-line index cap (mem0, 2026-03-31)** [ask]. Organ: every index carrier (zknot, warm_state, census carriers). Port: no-silent-truncation gate in tools/zknot.py: fail loudly when a rewrite drops rows or the index overflows. Probe: add the gate, then feed it a synthetic 250-row index and assert exit 2; the cap thesis is falsified for us if any carrier can be shown to warn on truncation today (none does; zknot.py:273 silently takes [:3]) [read].
6. **mem0 token-efficient memory (2026-04-16)** [ask]. Organ: quantizer/context pack budget + graph identity schema. Port: entity-link keys on graph rows; retrieval budget pinned under ~7k tokens/query. Probe: headline probe below.
7. **mem0 ICLR 2026 roundup (2026-04-24)** [ask]. Organ: quantizer (context budget doctrine) + continuity drift guard. Port: record the verdict (stuffing loses at any window on long-horizon tasks; brief-plus-tips is below the knee, its risk is drift) as the budget law the warm-state organ already obeys by accident. Probe: none separate; it is verdict material that justifies probes 1 and 6.

## Estate map (consolidated)

Feeds the continuity organs (tools/zknot.py LATEST rewrite at :273-285, memory/warm_state.json), the memory-graph builder mag/knowledge_graph.py and its source ledgers (memory/biography/verkle_chain.jsonl 8.0 MB, memory/improve/skill_ledger.jsonl 2.4 MB, both live per lens/graph.md:27-28) [read], the percolator candidate pipeline, the gopher fleet's skill cards, and the context pack/quantizer token budget. Concrete port move, smallest-first: fix the four verified builder defects, then regenerate: knot rows read theme/summary fields the source never carries (mag/knowledge_graph.py:102-104); case_law id builder collapses onto `law:` (:123); 794 has_invariant edges dangle on invariant: targets that are never materialized as nodes (:165, with the [:4] per-module cap at :164); the maps_to builder never fires because no node carries a non-empty maps_to (:171-173). All four line numbers [re-run: grep on mag/knowledge_graph.py this ask].

## Headline probe (falsifiable, cheap, this week)

Patch one builder line: key case_law nodes on hash(skill_id + job + ts) instead of the empty `law:` prefix (mag/knowledge_graph.py:123), backfill each node's summary from the fields skill_ledger rows actually carry (schema, skill_id, job, pack_mode, chars_injected, ts; verified on the last row per lens/graph.md:28), regenerate, and assert (a) 300 distinct case_law ids exist where today all 300 share `law:`, and (b) an id-keyed lookup returns one specific skill_fired event's content. Falsified if any two source rows still collide on the key or if distinct ids still fail per-row retrieval; runs in minutes on the live 2.4 MB ledger with no LLM in the loop.

## Verified this ask vs carried

[re-run] catalog greps all zero, confirming the overlap claims for four terms: `grep -ci funes|hivemind|"LangSmith Engine"|"token-efficient memory" catalog/catalog.jsonl` returned 0/0/0/0. [re-run] organ line checks: grep on mag/knowledge_graph.py and tools/zknot.py (numbers above); `ls memory/warm_state.json` (998 B, mtime Oct 3 18:55). [read] sweep file, lens/questions.md (Q1-Q5 at lines 43-47, estate map at :49), lens/graph.md. [ask, not re-verified] the seven quotes and dates; prior-sweep overlap lines (10-03 HN sweep :181, 10-02 :69, 09-30 "189 sessions"); the LangSmith Engine/Context Hub and MEM1/MemoryAgentBench zero-greps (sweep:38 carries the miner's fuller grep census, which I did not re-execute term by term).

## OWED

funes GitHub repo not read (sweep:43 carries the same debt; bank the recall/get implementation before any adoption lane). No X post re-fetched this ask; quotes rest on the ask's confirmed-find status plus the sweep's fetch receipts. The DSEWiki 09-21/09-23 X-door cluster remains unrecovered (sweep:43).

## Sources

- Find list (this ask), 7 items with URLs: x.com/DanKornas/status/2106711943067148598, x.com/DanKornas/status/2064377228977205529, x.com/hwchase17/status/2069857129272627626, x.com/mem0ai/status/2079585032587694582, x.com/mem0ai/status/2039041449854124229, x.com/mem0ai/status/2044823522560901120, x.com/mem0ai/status/2047700288321331551
- watch/inbox/frontier_olm_2026-10-04/sweep/agent-memory-and-continuity-x.md
- watch/inbox/frontier_olm_2026-10-04/lens/questions.md, lens/graph.md
- mag/knowledge_graph.py, tools/zknot.py, memory/warm_state.json, catalog/catalog.jsonl (re-run/read this ask)
