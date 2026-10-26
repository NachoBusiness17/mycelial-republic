# Sweep: agent-memory-continuity via x (2026-10-06)

source-fetched: 2026-10-06
Seat: sweep gopher, area agent-memory-continuity via x. Feeds the named next-loop targets
(memory propagation clock, two-law-stack merge, belief-retirement depth) which live in
memory/rib/, memory/zknot/, memory/warm_state.json, and memory/knowledge_graph.json.

## Door status (honest)

- WebSearch (Z.ai backend) fired 13 X-targeted queries this sitting; at least 8 came back
  429 ("code":"1302","message":"Rate limit reached for requests"), matching the 10-05
  sibling's experience (watch/inbox/frontier_olm_2026-10-05/sweep/agent-memory-continuity-x.md:8).
- The site:x.com door degraded worse than 10-05: successful queries returned profile-level
  or bare-domain URLs (https://x.com with no status id) for most hits. Only one query shape
  returned URL-shaped posts (Saboo_Shubham_ article/2022014147450614038 and
  status/2027463195150131572); both snowflake-decode to 2026-02-12 and 2026-02-27 via
  `(id >> 22) + 1288834974657` (run this sitting with the repo venv), so both are OUT of the
  30-day window and dropped to context.
- The fxtwitter door fired ZERO times this sitting: there was no in-window status id to
  resolve. No fallback success is claimed. Per the recipe, snippet-level items are banked
  with their (degraded) URL and marked SNIPPET-ONLY.
- Deep reads ran through curl (WebFetch and the web_reader MCP both 429'd on cohorte, and
  PyPI serves a Cloudflare challenge to plain fetches; the PyPI JSON API worked). All raw
  bytes kept under watch/inbox/frontier_olm_2026-10-06/sweep/_raw/.

## Pass counts

Pass 1: 34 candidates enumerated from the searches, each dispositioned with a date where the
source showed one (list below). Window = 2026-09-06..2026-10-06. Pass 2: 5 in-window items
fetched and read end to end (cohorte 20,586-char stripped text read in full; matrixorigin
Memoria README 22,207 bytes, lines 1-259 read plus API tables at 332-362/389/425/449;
getzep comparison page 11,517-char stripped text read in full; arXiv 2609.12320 abstract
page parsed in full; memsearch PyPI JSON long description 29,322 chars, key sections read,
release history parsed). One extra item (kau.sh AGENTS.md sync) was fetched and read in full
(6,031 chars) but its revision log ends 2026-03-08, so it is out-of-window context, not a
banked item. One Medium post returned 60 chars (blocked); it stays snippet-level and unbanked.

## Overlap check (what the estate already holds)

rg against catalog/catalog.jsonl, memory/, and corpus/ this sitting:

- Day-5 banked set (lens burns.md:71-79) already holds: mem0 placement-vs-compaction-cliff,
  Compaction Cliff 2608.22752, DolphinBench (catalog rows 13c521a935e6, fab2cb0fd372, plus
  sweep _raw mem0_dolphinbench.txt), StateMemBench, ibl.ai, akshay two-clock/Zep,
  mem0 infer=True/False. None re-banked.
- Prior X sweeps of this area (09-28, 09-30, 10-01, 10-02, 10-03, 10-05) hold the X items
  akshay_pachaar/2104938749679607902, RaulJuncoV/2095494698257301548,
  OracleDevs/2095294453065908432, DanKornas, S_BatMan, alphabatcher, hwchase17,
  pauliusztin_, simplifyinAI, towards_AI, plus the fxtwitter ids 2102897972484686221,
  2104478985614704756, 2104602215440666826 (rg of x.com/status URLs across those five
  sweep files this sitting). None re-banked.
- My banked candidates: "governed writes", "retraction latency", "write-permission",
  "MUMBench", "2609.12320", and "Git for AI Agent Memory" all return ZERO hits across
  catalog/memory/corpus. "Memoria" catalog hits are the Italian/Spanish course chapters
  "Memoria para/per Agenti AI" (corpus/library lsa zone), not matrixorigin/Memoria.
  "memsearch" catalog hits are Ghidra pypredef stubs. "Hindsight" hits are unrelated arXiv
  titles (hindsight-distilled sentinel; rare-disease rationale distillation). "MINJA" hit
  in dlb_intro.html is a base64 substring, a false positive. All five primary items are
  genuinely new holdings.

## The five research questions, answered from what was read this sitting

1. Memory propagation clock: the strongest find is that the frontier has TWO named versions
   of the estate's clock. Cohorte names the inverse instrument: "retraction latency", how
   long after a retraction the memory stops influencing decisions, proposed as a dashboard
   number (cohorte_governed_writes.txt, FAQ section "How do you roll back a bad memory?").
   Memoria ships the forward direction as a mechanical re-stamp: steering rules are written
   into per-tool boot files (.kiro/steering, .cursor/rules, .claude/rules, AGENTS.md for
   Codex, GEMINI.md) and "After upgrading: `memoria rules --force`" re-propagates them
   (memoria_readme.md:241-243). That is a propagation clock you can time per seat class:
   stamp once, then poll each tool's file until the new row appears. The estate's own gap
   (compile coverage is not propagation, next-loop target 1 per commit ba03060bb) is the
   same shape: memsearch solves it with a shared markdown source of truth plus a rebuildable
   shadow index per seat (memsearch PyPI description), which is the corpus FTS5 pattern
   (B2-465) applied to boot packs.
2. Two-law-stack merge (AGENTS.md vs the 56-rib vault, ~326,713 bytes, lens laws.md:6):
   cohorte's six-class table is a merge contract in miniature. Each class carries "who may
   write it" and "default authority": procedural = "a versioned skill, not model-authored
   memory" (= the rib vault), policy = "the policy registry only; never promoted from
   conversation" (= law rows), and the closing rule "anything in the procedural or policy
   rows that was written from a conversation gets deleted today" is a one-line retirement
   test for duplicated rows (cohorte_governed_writes.txt, framework-fit and what-I'd-do
   sections). kau.sh (out-of-window context) shows the field's merge contract in the wild:
   one source-of-truth repo, symlinks per tool, and a CLAUDE.md shim that "just says
   See @AGENTS.md" (kaush_agentsmd.txt lines 48-49).
3. Placement-vs-compaction on our archives: cohorte independently restates the mem0/Passau
   placement result as a compaction boundary: externalize state, owners, approvals with
   hashes, ids and amounts BEFORE compressing; "If the summary is the only place an approval
   or an unresolved payment exists, the design failed before compaction began"
   (cohorte_governed_writes.txt, compaction section). Applied to the estate: the zknot
   recap's 0.59 percent stable-leading-block share (lens burns.md:88-89) plus the 13/338
   compiled rows losing a literal to truncation (burns.md:89) say summarize-at-window-close
   already sits on the cliff; the cohorte boundary checklist is a concrete placement spec to
   A/B against it on the same asks. The Zep/Hindsight page adds the conditions law for any
   such A/B: the same benchmark score at double the retrieval budget is not the same result
   (getzep_hindsight.txt, key takeaways).
4. Addressability: memsearch runs content-id addressing in production at the sync layer:
   "SHA-256 content hashing skips unchanged content" with the vector store as a derived,
   rebuildable shadow index (memsearch PyPI description). AIM enforces addressing with
   index-level per-owner access control and grades update/delete as first-class operations
   (arXiv 2609.12320 abstract). Neither contradicts the trailing-space id disease (lens
   graph.md:30, exact-match lookups silently undercount); both hash canonical bytes before
   indexing, which is exactly the normalization step that kills whitespace-variant ids.
   What breaks first under content-id addressing stays OWED: none of the reads stress-tests
   id mutation on edit.
5. Belief-retirement depth: cohorte's answer is descendant quarantine via source_units
   ("quarantine everything descended from the poisoned source, which is what source_units
   is for") plus "Rebuilding only the vector index is not a rollback" - the freshness-
   theater pattern (fixed at layer N, alive at layer N+1) named and instrumented. Memoria
   makes retirement reversible instead of irreversible: point-in-time memory_rollback,
   branch, merge (memoria_readme.md:346-351). AIM quantifies how deep the disease runs:
   58.8 percent strict operation accuracy on update/delete operations means production-
   class systems fail retirement roughly 4 times in 10 (2609.12320 abstract). R4B took the
   estate's dangling welds 29 -> 0 (lens burns.md:139-140); these three reads say the
   unbanked half is descendants: summaries, caches, and compiled packs derived from the
   falsified row.

## Banked items (6, strongest first)

1. cohorte.co "AI Agent Memory Architecture: Governed Writes, Not Storage" (2026-09-13).
   Full read. Memory as a write-permission problem; six memory classes with per-class write
   authority; CANDIDATE -> QUARANTINED -> CORROBORATED -> ACTIVE promotion lifecycle with
   supersession keys and source_units descendant quarantine; MINJA >95 percent injection /
   ~70 percent attack success; retraction latency as a dashboard metric; ACL-baseline 0
   leaks vs elaborate architecture 307 leaks over 200 queries (negative-result discipline).
   URL: https://cohorte.co/blog/ai-agent-memory-architecture-governed-writes
2. matrixorigin/Memoria README (repo created 2026-03-09, pushed_at 2026-10-03 per the
   GitHub API, 607 stars; README itself undated, banked as a live-surface read with both
   dates stated). Git-for-memory: snapshots, branches, merge, rollback on MatrixOne
   copy-on-write (arXiv 2604.03927 foundation); memory_governance quarantine (1h cooldown),
   memory_consolidate contradiction detection (30min), memory_purge/correct; steering rules
   stamped into per-tool law files, re-propagated by `memoria rules --force`.
   URL: https://github.com/matrixorigin/memoria
3. arXiv 2609.12320 "AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent
   Multi-User LLM Systems" (submitted 2026-09-11). Abstract read in full. Index-level
   access control over private-vs-public memory classification; MUMBench grades retrieval,
   creation, update, and deletion; 96.0 visibility / 58.8 strict / 70.5 state-aware
   operation accuracy across three runs.
   URL: https://arxiv.org/abs/2609.12320
4. memsearch (ZillizTech), PyPI 0.4.21 uploaded 2026-09-24. Long description read via the
   PyPI JSON API (the HTML page serves a Cloudflare challenge). Cross-seat semantic memory:
   Claude Code, Codex, DeepSeek Harness, OpenClaw, OpenCode on one markdown source of
   truth; Milvus as a derived rebuildable shadow index; SHA-256 content hashing for
   incremental sync; skills-from-memory procedural layer; background PROJECT.md/USER.md
   maintenance. URL: https://pypi.org/project/memsearch/
5. Zep "Zep vs. Vectorize Hindsight: A Neutral Look" (page carries no date; regex over the
   fetched text found none; banked with date unknown). Vendor-number conditions done right:
   91.4 at an 8,192-token retrieval budget vs 90.2 at ~4,408 tokens on the same benchmark;
   bi-temporal automatic fact invalidation; ABAC governance in the data layer.
   URL: https://www.getzep.com/vectorize-hindsight-alternative
6. SNIPPET-ONLY, degraded door: X thread "Holistic Context" (Chinese) - the author checked
   three memory mechanisms against open-source code and cross-reads MemGPT 48.7 / Mem0 52.0
   / Hindsight 91.4, with a memory-consolidation graph-contracts code path named
   (packages/ai/memory-consolidation/src/graph-contracts). The search backend returned the
   bare domain https://x.com with no status id; the thread could not be resolved through
   fxtwitter (no id) and no date could be verified. Banked at snippet level per the recipe
   fallback, clearly marked unverified beyond the snippet.
   URL: https://x.com (bare domain as returned by the search backend)

## Pass-1 census (candidates considered, with dispositions)

In-window banked: cohorte (Sep 13); Memoria (pushed Oct 3); AIM 2609.12320 (Sep 11);
memsearch 0.4.21 (Sep 24); Zep page (undated). Out-of-window, excluded: Saboo_Shubham_
article (decode 2026-02-12) and status (2026-02-27); kau.sh AGENTS.md sync (revisions end
2026-03-08; read in full, kept as context); Hindsight Agent Memory Benchmark manifesto
(2026-03); Letta governance hooks (2026-07-24); AriadneMem (2026-02); hyperdev Claude Code
compaction (2025-12); dev.to markdown memory (2026-02-18); mem0 footprint-by-97 (2026-08-31);
mem0 Beyond AGENTS.md (2026-08-04, directly two-law-stack relevant - named as owed context);
"Why Every AI Agent Forgets Everything" (2026-06-05); KV memory sharing (2026-04-10).
Snippet-level, unresolvable or unread: Holistic Context thread (banked as item 6, marked);
Software Factory post (MEMORY.md vs CLAUDE.md layering, no URL); stable-rules-in-CLAUDE.md
post (Anthropic /memories directory, no URL); milvusio profile (v1.3.0 agent-memory
indexing, no status id); Medium AGENTS.md sync-script post (fetch blocked, 60 chars);
dev.to deployhq config files; Real Python AGENTS.md; memorypapers.org category; yarnit
outgrown-retrieval; continuousagentic tradeoffs; OpenReview Memory-is-Reconstructed;
ZLKong token-reduction collection; ECC 2.1 cross-harness vault; ai-memory routing package.
Census total: 34 candidates dated or dispositioned.

## Checks run / not run

Ran this sitting: snowflake decode of both Saboo ids (repo venv python); GitHub API reads
for Memoria created_at/pushed_at/stars; PyPI JSON API read for memsearch releases; HTML
strips of cohorte + getzep + kau.sh; arxiv abs page parse; overlap greps named above.
NOT run: fxtwitter resolutions (zero in-window ids found - stated, not assumed); no pytest
(a research sweep; nothing to collect); export.arxiv.org API not retried (10-05 sibling
measured it timing out twice; I used arxiv.org/search instead, which worked).

## OWEDs surfaced

1. Time the propagation clock per seat class the Memoria way: stamp a law row, poll each
   tool's boot file until it carries the row, publish hours-per-seat-class. Memoria's
   `rules --force` is the mechanical template (memoria_readme.md:243).
2. Adopt "retraction latency" as the estate's name and dashboard metric for the inverse
   clock (cohorte FAQ); R4B fixed the welds (29 -> 0) but no instrument times how long
   derived artifacts (summaries, caches, compiled packs) take to stop reflecting the
   falsified row.
3. Two-law-stack merge contract candidate: cohorte's two-column test (who may write it /
   what it may authorize) applied row-by-row to AGENTS.md vs the 56-rib vault; rows whose
   writer is the operator are law-stack, rows whose writer is a run are conversation-stack,
   duplicated rows get one home and one shim (kau.sh pattern).
4. Find the Holistic Context thread's status id (X search inside a logged-in surface) and
   resolve through fxtwitter; the memory-consolidation graph-contracts code path it names
   is worth a direct read.
