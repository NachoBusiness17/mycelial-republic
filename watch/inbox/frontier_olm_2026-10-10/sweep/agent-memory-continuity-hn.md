# SWEEP: agent-memory-continuity via Hacker News (2026-10-10)

source-fetched: 2026-10-10. Door: HN Algolia `search_by_date` + `search` (query=agent memory, memory
consolidation LLM, knowledge graph agents, LLM long-term memory, memory supersession, agent session
handoff context, agents forgetting memory update, Letta memory, agent memory graph schema; tags=story),
then deep fetches of the strongest primary pages and one full comment thread. Both Algolia doors
answered clean; no 403 or degradation, no fallback needed.

Pass 1: 6 search calls returned ~150 raw rows, deduped to ~90 unique stories, of which ~45 fall inside
the last 30 days (2026-09-10 onward); 30+ fresh candidates considered as required. Pass 2: 9 primary
pages fetched and read end to end (knowl.cloud, AgentMemoryRepo spec, Motif, Singularity, the
49945933 HN thread, CTWM blog, galahad-kv HF paper page, Memdebug repo, arXiv 2602.11243 abstract).
Everything banked below was read this sitting; nothing is secondhand.

## Anti-rebank (overlap verified by grep, see per-item overlap fields)

- The 2026-10-04 sweep already cached pages for liao.gg 49945933, SuperLocalMemory 49950478, Aura
  49951895, reduck 49910148, cognee 49861765 (`watch/inbox/frontier_olm_2026-10-04/sweep/_am_page_*`,
  confirmed by grep of `catalog/catalog.jsonl`). Those four products are therefore NOT re-banked.
- Registers 10-04 through 10-09 already hold: day-9 supersession arXiv trio (2610.10265, 2610.08586,
  2610.03902), retrieval admissibility 2610.07309, retention-vs-abstain 2610.07100, multi-agent
  persistent memory 2610.07782, execution consistency 2610.08101, consolidation-flattens 2609.36457,
  Cognition Dreaming X post, walden_yan AMR X post, four mem0 threads. None of tonight's 8 items
  appear in any register, DIGEST, or memory/ grep (verified `grep -r -l` over those surfaces: zero
  hits for galahad, 2610.10845, StructMemEval, 2602.11243, 2610.00010, memdebug, motif-labs,
  pandacover).
- The estate already parks a library named `agentmemory` with a temporal-graph module
  (`library_parked/agentmemory/src/functions/temporal-graph.ts`, per catalog grep). Unverified
  whether Knowl's benchmark table row "agentmemory 79%" is that library. OWED if it matters.

## Banked items (strongest first; full JSON in the SweepResult)

1. **Knowl, write-time supersession** (https://knowl.cloud, HN 49465138, 2026-08-27, 13 days outside
   the 30d window, flagged honestly). Facts record "what it replaced and what replaced it"; "there is
   no delete verb in the product at all"; superseded facts retire into queryable history; provenance
   labels (observed / stated by a person / inferred); review queue attaches "a name, not just a
   timestamp"; disagreements surface as "disputes, not silence". Benchmark: SubEM 0.90 on
   MemoryAgentBench FactConsolidation-SH at 262K context vs listed agentmemory 0.79, MemGPT 0.28,
   Mem0 0.18, Zep 0.07. Open source github.com/dat999zx/knowl, MCP server, local replica read path.
   This is a working supersession CHAIN (bidirectional replaces/replaced-by edges), exactly what
   RQ1 asks the day-9 trio to become; the 6 placeholder pairs in memory/knowledge_graph.json
   (verified: 6 "superseded" + 6 "superseder" kind rows) could be typed with replaces/replaced-by +
   provenance + retire-date instead of blanket deletion.
2. **Agent Memory Repo spec** (https://github.com/AgentMemoryRepo/agentmemoryrepo, HN 49968066,
   2026-10-05; 675 stars, MIT, "originally developed by Cognition and released as an open
   standard"). The read-path contract: a separate git repo of markdown notes; MEMORY.md loaded at
   session start, kept short, indexing everything; one-line bullets with [source: session-link,
   added: date]; [[path]] cross-links; agents "update entries ... with no human in the loop"; push
   after every edit; a periodic "dreaming" pass merges duplicates and "checks sources to resolve
   contradictions"; multiple per-person repos clone into one machine and the agent writes by
   ownership. This is a competitor schema for exactly our warm-boot chain (warm_state.json + zknot
   recap): read-path = short index + grep, write-path = edit-in-place + git history as the
   supersession ledger.
3. **Motif** (https://github.com/motif-Labs/motif, HN 49877499, 2026-09-28, Apache-2.0). Builds a
   SQLite knowledge graph from coding-agent history: sessions, decisions, files, topics as nodes;
   edges are "a session that informs an entity, a note that contests another, a handoff lineage";
   "New knowledge supersedes old rather than overwriting it"; contradictions flagged in
   distillation; deterministic ranking (FTS5 + graph relations + pinned human notes) with per-claim
   confidence; `motif blame`, `motif handoff`, `ask_session` resumes a past session read-only.
   Measured: "8 of 9 questions inside a 1,500-token budget" against 1.77M tokens of history (1,186x
   compression), ~14MB DB at 130 sessions. RQ2 (already_inside automation) and RQ4 (contest edges =
   tension links; handoff lineage edges) both answered by one working schema.
4. **Singularity** (https://github.com/pandacover/singularity, HN 50004683, 2026-10-08, MIT).
   Distills agent-committed changes every 3 commits into parameterized "workflows" (steps, blanks,
   code-anchored locations that survive movement, known-mistake warnings); injects matched workflows
   into the first prompt via plain-text matching ("no model call, a fraction of a millisecond").
   Medians over 3-4 pre-registered runs: learned task turns 28.5 to 9.5, tokens 1.90M to 423k,
   cost $0.81 to $0.30; two-of-four kinds learned ~30% fewer turns; UNLEARNED kinds ranged from 25%
   fewer to 17% MORE turns. Explicitly supports Hermes Agent. RQ3: this is the honest generalization
   envelope for route-map-class boot cuts, including the failure condition (no learned workflow =
   neutral to negative, warning overhead).
5. **HN thread 49945933** (https://news.ycombinator.com/item?id=49945933, 2026-10-03, 388 pts, 311
   comments; page-only was banked 10-04, the thread is the delta). kaydub's top counter: "The code
   IS the documentation", stale docs make the model revert past decisions, a senior dev's 6-8 week
   skill/plugin build moved 5 repos while vanilla Claude finished one in ~20 minutes. Working
   practices named: CLAUDE.md/AGENTS.md under 100 lines; JohnBooty's "only document repeated
   friction ... paying 500 tokens in AGENTS.md beats burning 5000 rediscovering"; crazygringo's
   "replace, don't append" staleness rule; sub-agent delegation preferred over similarity RAG;
   panarky's warning that memory plugins injected above AGENTS.md are a prompt-injection surface.
   RQ1 read-path contract as fought out by practitioners.
6. **CTWM, Core-Tail World Model** (https://redreamality.com/blog/ctwm-heavy-tailed-memory-traces-
   long-horizon-agents/, HN 49955466, 2026-10-04; paper arXiv 2610.00010, code github.com/Hik2899/
   world-model-self-organized-criticality). Under finite context, "memory is no longer a neutral
   ledger; it is a resource-allocation mechanism": retrieval itself concentrates memory (Gini 0.44+
   vs 0.29 disabled); rank-based budget b_t = r^-tau/Z with a summarized RETAINED tail (not deleted);
   CTWM cuts prompt tokens 5.9% and bottom-half tail error 13.6% vs graph memory; LongMemEval -24.5%
   tokens at parity with a multi-session recall blind spot; "check the visit histogram before
   lengthening the window or swapping a larger model". RQ3/RQ5: gives the retention-decay dial (tau)
   the world-rib contract would need, plus the law that visit-count shape is the diagnostic.
7. **galahad-kv, 50M-token window** (https://huggingface.co/papers/2610.10845, HN 50018178,
   2026-10-09, Corbenic AI preprint, single-author class: treat with two-family corroboration before
   trusting). KV-transfer connector for vLLM persists each ~16k-token block's KV state to encrypted
   NVMe and grafts it back byte-exact: 100/100 restores, 2.8-4.3x faster and 8.8-12.3x less GPU
   energy than recompute, planted-fact recall 98/100 (31B), at 1.86-6.25 TB storage on an H100.
   RQ3 boundary evidence: the 25x-class boot cut generalizes ONLY when memory is byte-identical KV
   state on identical model+stack; our warm boot is JSON state re-read by prompt, so the applicable
   steal is the deposit/restore split, not the numbers.
8. **Memdebug** (https://github.com/juraj-jumic/memdebug, HN 50026431, 2026-10-09, Apache-2.0,
   alpha v0.6). Observer-only CLI that snapshots agent memory into a tamper-evident ledger, diffs
   ("catches edits that bypassed the store's own history"), flags suspicious wording, and rolls back
   markdown memory with dry-run-first undo; "it never sits between the agent and its memory".
   Adapters: markdown folders/git, Open WebUI, self-hosted Mem0; Claude Code session attribution
   "as evidence and never as proof". RQ1 audit side: supersession chains need forensics when the
   write path is poisoned (runtime text "can be planted: an email, a web page, a document"); maps
   onto enforcement_trail.jsonl and the memory-poisoning class the shared-surface contract already
   fears.

Context (read, not in the JSON eight): arXiv 2602.11243 "Evaluating Memory Structure in LLM Agents"
(v4 2026-10-01) argues current benchmarks only test fact recall so RAG passes; its StructMemEval
probes whether agents can organize "transaction ledgers, to-do lists, trees and others", finding
memory agents succeed when prompted on structure but LLMs fail to pick structure unprompted. Direct
RQ4 support: schema v3 should type steals/knots by structure class, not only by edge kind.

## RQ synthesis (one line each, evidence above)

- RQ1: yes, a real chain model exists to port: Knowl's replaces/replaced-by + provenance + retire
  (item 1), AMR's git-history-as-ledger (item 2), Motif's supersede-not-overwrite (item 3); the
  day-9 trio's read-path contract is corroborated by practitioners in item 5.
- RQ2: Motif (item 3) is the closest working already_inside automation (distillation proposes,
  human admits; contradictions flagged); nobody does it fully hands-off.
- RQ3: generalizes only for matched repeat work (item 4's learned-kinds split), is bounded by
  retrieval concentration (item 6), and the byte-exact KV class (item 7) does NOT transfer to
  JSON-state warm boots.
- RQ4: schema v3 wants replaces/replaced-by typing with provenance (item 1), contest/tension edges
  and handoff-lineage edges (item 3), structure-class typing (2602.11243), and rank/visit-count
  weight fields (item 6).
- RQ5: the world-rib lowering needs a retention dial and a retained summarized tail (item 6) plus
  ownership-scoped write paths (item 2); the current shape cannot express budget policy per field.

OWED: Knowl-to-parked-agentmemory identity check; Knowl github FINDINGS.md raw-numbers read; CTWM
paper full text (only blog+abstract read); galahad-kv independent corroboration before any steal of
its numbers; the 49945933 thread was truncated by the fetcher (roughly a third of 311 comments
visible), the rest unread.
