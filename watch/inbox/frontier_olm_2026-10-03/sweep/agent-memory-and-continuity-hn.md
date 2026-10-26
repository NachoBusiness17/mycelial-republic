# SWEEP: agent-memory-and-continuity via HN - 2026-10-03 (evening rewrite)

source-fetched: 2026-10-03. Agent: sweep-agent-memory-and-continuity-hn. This file REPLACES the
10:43 morning version written by this run's earlier HN seat at the same path (house convention,
same as today's evening lens/burns.md and lens/questions.md rewrites). The morning seat's eight
banks are carried as baselines below, attributed "(via morning seat)". This evening pass adds
five genuinely new items after dedup against ALL five prior folds of this area (09-28, 09-30,
10-01, 10-02, and today's morning seat). House laws held: ascii only, no em or en dashes, every
claim cites what was read or run this sitting.

## Doors and method (what actually ran this sitting)

- Pass 1: 11 `curl` hits against `hn.algolia.com/api/v1/search_by_date`, `tags=story`,
  `numericFilters=created_at_i>1788393600` (= 2026-09-03, 30-day window), hitsPerPage 10-30,
  queries: "agent memory", "knowledge graph", "memory consolidation", "context engineering",
  "CLAUDE.md", "AGENTS.md", "entity resolution", "vector database", "long-term memory",
  "session state", "conversation memory", "compact context". Raw hit lists parsed with
  `.venv/Scripts/python.exe` per query. Roughly 49 distinct candidate stories considered (id list
  in the Pass 1 section). Door health: hn.algolia.com clean all sitting.
- Pass 2 deep reads (thread + linked page, fetched and read this sitting): 49712610 (getzep Konig
  blog via WebFetch after 301 redirect), 49828496 (swarmagent.dev spec page), 49920951 (quesma.com
  blog), 49923399 (huggingface.co blog by dacorvo), 49581240 (OKF README, 19,894 bytes raw
  fetched, read ~200 lines), 49701788 (Polign recall README, 8,541 bytes, read in full),
  49721941 (Context Freshness Ledger README, 2,423 bytes, read in full), 49877499 (Motif README,
  26,885 bytes, read head + body sections), 49657908 (SOS README, 11,374 bytes), 49743049
  (Skillsync Launch HN thread, 24 nodes, + txcript README 8,374 bytes). HN threads fetched via
  `hn.algolia.com/api/v1/items/<id>`.
- Door degradations (nothing fabricated): medium.com fact-retirement post returned 403 to
  WebFetch; direct curl with browser UA returned a 6,015-byte Cloudflare "Just a moment..."
  challenge shell (grepped `__cf_chl_tk` markers, zero article text); freedium.cfd mirror does
  not resolve from this box (curl exit 6, DNS). Its HN thread 49877124 fetched: zero comments.
  This is a second same-day independent confirmation of the morning seat's identical wall (via
  morning seat, section Doors). `mcp__web_reader__webReader` 500'd once on the same Medium URL.
  The getzep blog needed one 301 redirect follow (blog.getzep.com to www.getzep.com), succeeded.

## Anti-rebank reconciliation (read this sitting, so nobody re-banks)

Read in full this sitting: the morning seat's sweep (this path, 10:43 version), the 10-01 and
10-02 agent-memory HN sweeps, the 10-03 DIGEST and register, lens/burns.md, lens/questions.md,
lens/graph.md. Already-bank baselines this pass defers to:

- Morning seat (today, via this path's 10:43 version): 150k-tokens dacorvo post (#1), future-os
  compaction-measured, southbridge entity-resolution, memanto retention policy, A-Mem 2502.12110,
  Memory Control Signals 2609.27286, InfiniteMem, Reduck.
- 10-01 fold (via frontier_olm_2026-10-01/sweep/agent-memory-continuity-hn.md): AGENTS.md 741pt
  49760187, Backpass 49703919, Polign recall 49701788 (registry + corrections bank), Motif
  49877499, memanto retention 49807330, auto-memory rant 49921985, Awareness-Market 49594849.
- 10-02 fold (via frontier_olm_2026-10-02/sweep/agent-memory-continuity-hn.md): OKF (deep bank),
  ctx.rs, kolesnik.io BM25, Awareness-Market, Motif, past.dev, Context Freshness Ledger,
  Repligraphs; explicitly left 49877124 unread "for the next seat".
- 09-30 fold (via frontier_olm_2026-09-30/sweep/agent-memory-continuity-hn.md): memoryfields,
  post-graph-rag, compaction-measured, OKF (first bank), SubtleMemory/simba.
- 09-28 fold + 10-01 (via 10-01 sweep lines naming it): the getzep Konig blog was read by both
  the 09-28 fold's pass 2 and the 10-01 fold; NOT re-banked here. My read corroborates two extra
  specifics worth one line: Konig "marks the old fact invalid using an `invalid_at` date instead
  of overwriting it" (retire-not-mutate healing) and holds "entities and edges ... in compact,
  integer-indexed arrays with adjacency lists" (integer id normalization under the prose API).

Genuinely new this pass (banked as items below): quesma transcripts (49920951), swarmagent plans
(49828496, new to THIS area; the 09-28 kv-cache sweep named the same page for its cache-hit
numbers, different area, different mechanism), Skillsync/txcript (49743049), SOS (49657908),
and the Polign Resume extension (new sub-finding of an already-banked primary).

## Pass 1 - candidates considered (49 distinct in-window stories, queries above)

49911995, 49887024, 49877124, 49861765, 49807330, 49766795, 49749689, 49721941, 49712610,
49703919, 49701788, 49685398, 49628820, 49596543, 49595246, 49594849, 49593006, 49581240,
49911411, 49877752, 49877499, 49745176, 49740304, 49737804, 49721129, 49684835, 49828496,
49698184, 49760187, 49814947, 49867329, 49833075, 49926105, 49732569, 49911193, 49923466,
49884835, 49609014, 49610716, 49935994, 49797488, 49783671, 49657908, 49602002, 49920951,
49920621, 49743049, 49923399, 49784563, 49768617. That is 49 distinct ids, well over the ask's
30-candidate bar.

## Pass 2 - the five new banks (details also in the returned SweepResult)

1. **Agent session transcripts are precious, keep them** (quesma.com, Jacek Migdal, 2026-10-01;
   HN 49920951, 0 comments). The transcript-retention counterparty to the re-derivability law:
   re-derivability wins in context (dacorvo, via morning seat) while the raw transcript stays the
   raw leaf layer worth keeping because "they are proof of work for the tokens you paid for, and
   lessons you will pay to relearn". Numbers banked: Claude Code deletes transcripts by default
   after 30 days; Anthropic analyzed 200,000 internal Claude Code transcripts; 91 pct vs 43 pct
   task resolution with/without an AGENTS.md change; the author's example transcript is 4.7 MB
   across 933 turns with 24 subagents; sessions where an engineer corrected the agent are
   "ready-made evals". Maps to RQ2/RQ5: keep transcripts as the archive leaf, forward the
   residual, never the transcript, as context.
2. **Why agent harnesses need plans - and why you shouldn't compact context** (swarmagent.dev
   ARCH 01 spec, page undated, story 2026-09-24; HN 49828496, 2 comments). The plan-as-residual
   shape: "an agent harness is not an LLM chat wrapper - it is an authoritative finite state
   machine" carrying "a strictly typed JSON contract (checkpoints, subtasks, validation rules,
   acceptance criteria)"; "LLMs summarize concepts, not technical invariants"; the final_handoff
   contract is "~350 tokens" and Checkpoint 2 "inherits 100 percent of the verified technical
   signal while discarding 99.6 percent of the token weight". Caveat banked: vendor spec prose,
   no measurement behind the 100/99.6 figures; and the author's own risk line: "if an agent
   produces a sloppy, inaccurate final handoff, subsequent checkpoints might inherit flawed
   assumptions." Maps to RQ2/RQ5.
3. **Launch HN: Skillsync (YC W26) + txcript** (HN 49743049, 2026-09-17, 68 points, 24-node
   thread; github.com/skillsynchq/txcript README fetched raw). One transcript schema across 13+
   agent formats ("txcript is a library for converting agent sessions. Start a conversation in
   Claude Code and continue it in Codex, carrying over messages, reasoning, and tool history"),
   read-only support for Hermes Agent among them. The thread carries the journal-vs-log debate in
   the re-derivability register: "A journal comes out of a prompt, so it records one way of
   looking at the session. Whatever that prompt didn't ask about is gone" (cat-whisperer) and
   "thats like explaining what you did yesterday, vs having an immutable log of what you did
   yesterday" (agentdev001); co-founder: with long sessions "the receiving agent sometimes decides
   to compact it. But the whole transcript still exists and is accessible". Maps to RQ2/RQ5.
4. **SOS - project state between coding agent sessions** (github.com/sigmastratum/
   sigma-operator-stack README, story 2026-09-11; HN 49657908, 0 comments). Accepted-state
   continuity with a stale gate: "SOS records the project state you explicitly accept"; "Recovery
   reads the accepted project state instead of relying on chat history"; and the part
   memory/warm_state.json lacks: "A source change makes the previous state stale; SOS returns
   SOS_SOURCE_STATUS_CHANGED instead of treating the earlier pass as current." Release activation
   is fail closed. Community alpha 0.1.0a7, Linux primary, so treat as a mechanism sketch, not a
   dependency. Maps to RQ5.
5. **Polign recall Resume extension** (HN 49701788, README fetched raw and read in full this
   sitting). Extension of the 10-01 bank (which covered registry-gated typed writes and
   corrections; that bank did not mention Resume). The Resume recipe: "Resume gives an agent back
   the context it should start from, built from what it wrote down while it worked" - working
   state (goal, plan, progress, focus, open questions), pointers to where the work lives, and
   "Turns, verbatim, and large tool outputs stored by reference", "sized to a token budget and
   rendered as one briefing" (TokenBudget 8,000 in their example). Maps to RQ5: the minimal
   residual set is working state + pointers + verbatim needles, everything else by reference.

## Synthesis against the five lens questions (lens/questions.md section 3)

- RQ1 (ingest-time join rule vs other healing order): every working system surfaced this week
  heals at WRITE time, not by post-hoc graph surgery: registry-validated typed writes with
  unmatched facts parked as promotable notes (Polign, read this sitting), search-before-write
  dedup (OKF, via 10-02), refuse-merge-at-uncertainty-fences with originals never destroyed
  (Southbridge, via morning seat), retire-by-invalid_at instead of overwrite (Konig,
  corroborated this sitting). The literature's order is: real ids enforced at ingest
  (Polign-style registry is the concrete rule for the 300 `law:` duplicates at lens/graph.md:18),
  plus mark-invalid/supersede histories rather than mutation. This concurs with lens/graph.md:27
  ("give case_law rows real ids and join knot/steal/doctrine ids at ingest").
- RQ2 (does 2609.32802's re-derivability result validate residual+registry+leaf): the HN-week
  converges on the same shape from three independent doors - measured (dacorvo 8x/4x/3x weighted
  tokens and future-os 83/47/38 retention, both via morning seat), productized (swarmagent's
  plan + final_handoff), and argued (Skillsync thread's immutable-log-vs-journal exchange). The
  outcome-metric unit the fold marked OWED (lens/burns.md:88-89) now has a citable candidate:
  dacorvo's "weighted = input + 1.25 x cache_creation + 0.1 x cache_read + 5 x output" per
  successful task, with per-arm success/failure counts - with the caveat it is one model, three
  tasks, entry-selected, so a rib citing it should name it as a candidate unit to replicate, not
  a settled standard.
- RQ3 (architectures addressing content-free duplicate nodes and prose-pasted ids at ingest):
  no in-window item does post-hoc dedup of an already-collapsed id space; the working systems all
  prevent at write (Polign registry + note-parking; OKF scoped shadowing of identical concept ids
  plus --strict --drift build-time failure, via 10-02). The negative finding is the finding: the
  estate's 825-dangling-edge graph (morning seat's probe: 825 of 825 edge endpoints dangle, an
  erratum against the lens's 823) needs id migration at the ingest join, which no vendor ships
  because they never let the bad ids form.
- RQ4 (wiring the landscape agent_memory family, readable_first pattern): Konig's edge rule
  ("each fact is an edge that references the source data it was extracted from") plus
  integer-indexed adjacency is the readable_first two-resolving-edges pattern generalized:
  landscape family rows must emit module refs as resolvable ids with source pointers, never prose
  in the id field (lens/graph.md:19's mangled-id class).
- RQ5 (minimal residual set for cold-seat, tokens-to-competence): three convergent recipes this
  sitting - SOS accepted-state + stale gate, swarmagent plan + ~350-token final_handoff, Polign
  Resume briefing sized to an explicit token budget with turns stored by reference. Convergent
  residual set: goal/plan/progress/focus/open questions + pointers + verbatim needles;
  everything else by reference; and the gate warm boot lacks is staleness-on-source-change (SOS
  returns SOS_SOURCE_STATUS_CHANGED). Nearest published tokens-to-competence number remains
  Motif's 1,496-token median bundle answering 8 of 9 questions over 1.77M tokens (via 10-01
  bank); nobody in-window measured tokens-to-competence for a warm boot directly.

## OWED (could not verify this sitting)

- Medium "Five failure modes around fact retirement" (49877124): 403 + Cloudflare challenge +
  freedium DNS fail + empty thread, second same-day confirmation. Still the fold's open read
  debt; a working door is owed (candidates: archive.org snapshot, a different host mirror).
- openai.com/index/v7 institutional memory: 403 (via morning seat, not retried).
- Tokens-to-competence for hermes_warm_boot specifically: no measured instrument found; the
  nearest numbers are quoted above and none measured a cold-seat success rate.
- The dacorvo weighted-token metric as the rib's outcome unit: candidate only; replicating it on
  an estate instrument is the owed step before lens/burns.md:89's OWED can be closed.

## Overlap instrument (exact commands run this sitting)

- `grep -ci "<phrase>" catalog/catalog.jsonl` and `rg -li --no-messages "<phrase>" memory/` and
  `rg -li --no-messages "<phrase>" watch/inbox/` for: graph database service for agent memory,
  getzep, compact context, session transcripts are precious, 150k tokens, dacorvo, OKF Agent
  Memory, Polign, typed agent memory, freshness, motif-Labs, getmotif, context-freshness-ledger,
  chengyixu, swarmagent, quesma, okf-memory, Open Knowledge Format, funes, Skillsync,
  transcripts are precious, quesma.com/blog/agent-session, sigma-operator-stack|sigmastratum,
  skillsync|txcript, immutable log of what you did yesterday. Output summarized: zero hits for
  every new bank; getzep's 879 catalog rows are the in-corpus zep/graphiti codebase harvest
  (mine/raw/agent_bleeding_edge/getzep/, 2026-08-06, verified by reading two rows); the 9
  Skillsync catalog rows are zcode's skillSync.ts service files (read, unrelated); the memory/
  Polign hits are Project Gutenberg texts (false positives). Prior-fold collisions were checked
  by rg across frontier_olm_20260928, 2026-09-30, 10-01, 10-02, and the 10-03 DIGEST/register,
  which is how getzep Konig (already read by two folds) and dacorvo (lane-banked-only per
  DIGEST.md:24) were caught and handled as stated above.
