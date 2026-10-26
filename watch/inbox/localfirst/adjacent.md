# ADJACENT-PACK VERDICTS 2026-10-01 (gala localfirst-steal, division B, lane adjacent)

Class: RECEIPT · Method: raw README bytes curled from raw.githubusercontent.com per system,
sha256 manifest at `watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/SHA256SUMS.txt`,
tri-state per the citation-resolution law (bytes or UNVERIFIED). Register rows:
`watch/inbox/localfirst_memory_landscape_signals.jsonl` (9 adjacent rows appended after the
sibling ragos + ownmem rows; nothing overwritten).

## The verdict table

| System | Brief claim | Verdict | Byte quote (verbatim) | Source file:line |
|---|---|---|---|---|
| Letta | self-hostable | SUPPORTED | "Run the App Server for local or self-hosted agents" | fetched/letta.readme.md:23 |
| Letta | pages its own memory, model in charge | SUPPORTED | "They learn and evolve over long horizons through rewriting their own memory, skills, prompts, and even the harness itself" | fetched/letta-code.readme.md:5 |
| Letta | NEW vs stealth-sw-06 (had self-editing blocks only) | SUPPORTED | "All context (including memory blocks) is tracked via git" | fetched/letta-code.readme.md:24 (MemFS) |
| Mem0 | memory-infrastructure API with self-host | SUPPORTED | "Just testing? Use the library. Building for a team? Self-hosted. Want zero ops? Cloud." | fetched/mem0.readme.md:117 |
| Mem0 | two-phase extraction (prior bank + ask) | DISPUTED | "**Single-pass ADD-only extraction** -- one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten." | fetched/mem0.readme.md:57 (April 2026 algorithm replaced it) |
| Mem0 | brief adds anything new | SUPPORTED | "Scores reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK" | fetched/mem0.readme.md:54 |
| Zep | temporal KG | SUPPORTED | "Graphiti is a framework for building and querying temporal context graphs for AI agents" | fetched/graphiti.readme.md:37 |
| Zep | self-host (as Zep product property) | DISPUTED | "Zep Community Edition is no longer supported" | fetched/zep.readme.md:67 (code moved to legacy/) |
| Zep | brief adds anything new | SUPPORTED | (same deprecation quote; new vs the 09-28 bank which had Zep live) | fetched/zep.readme.md:66-70 |
| Khoj | local RAG chat | SUPPORTED | "Khoj is open-source, self-hostable. Always." | fetched/khoj.readme.md:53 |
| Khoj | no receipted diary, no claim grading | SUPPORTED_AT_README | absence: diary/receipt/claim-grading grep over 4,701 bytes = 0 | fetched/khoj.readme.md |
| AnythingLLM | local RAG chat | SUPPORTED | "runs locally by default with zero setup friction" | fetched/anythingllm.readme.md:43 |
| AnythingLLM | no receipted diary, no claim grading | SUPPORTED_AT_README | absence: grep over 26,484 bytes = 0 | fetched/anythingllm.readme.md |
| GroundMemory | small SQLite MCP memory server | SUPPORTED | "GroundMemory runs entirely on SQLite with FTS5" | fetched/groundmemory.readme.md:144 |
| people-context | small SQLite MCP memory server | SUPPORTED | "One SQLite file on your machine. No account, no cloud, no network calls." | fetched/people-context.readme.md:11 |
| Cognee | memory-infrastructure with self-host | SUPPORTED | "self-hosted knowledge graph your agents can search and reuse" | fetched/cognee.readme.md:42 |
| MemMachine | memory-infrastructure with self-host | SUPPORTED | "**Self-Hosted or Cloud**: Run locally, in Docker, or use our managed service" | fetched/memmachine.readme.md:123 |

Mechanism root for the block-paging claim (MemGPT paper abstract, fetched from
arxiv.org/abs/2310.08560): "virtual context management, a technique drawing inspiration from
hierarchical memory systems in traditional operating systems that provide the appearance of
large memory resources through data movement between fast and slow memory".

## What Letta's block-paging does that the context-pack ladder does not

The estate ladder (`mag/context_pack.py:16`, six modes janitor/route/build/audit/plan/full;
static per-mode char budgets `mag/context_pack.py:52-165`) is harness-built and never
model-written: the seat receives a pack assembled from bonds+brief+open_loops with budgets
chosen by mode and cannot rewrite any section between turns. Letta's paging is model-in-charge:
the agent itself rewrites its context (memory blocks) between turns, and MemFS git-tracks every
rewrite as a diffable commit. The missing rung is not a bigger budget, it is a model-writable
one: a selfblock section the seat edits, persisted to a file, riding every tier.

## Steal rows registered (2 with high/medium leverage, rest confirmations)

1. Letta selfblock rung (high): one model-editable memory block in the pack, git-tracked
   MemFS-style. Falsifier: seat edits it under once per 10 sessions or edits go stale within
   a week, and the rung adds nothing over the harness ladder.
2. Zep/Graphiti validity windows (medium): superseded laws stay queryable as valid-before-X
   instead of deleted; landing spot = valid_from/valid_to on the rib/law index. Falsifier:
   if rib supersessions already carry machine-readable close dates, the port is redundant.
3. Mem0 (medium): ADD-only accumulation is the receipts law in product form; the transferable
   part is multi-signal fused retrieval (semantic + BM25 + entity); the honesty clause
   (platform numbers are not OSS numbers) is the estate benchmark law self-published by a
   vendor. Falsifier: run mem0ai/memory-benchmarks LOCOMO slice on OSS SDK + local model.
4. GroundMemory mirror pattern (low): RELATIONS.md is a human-readable Markdown mirror of the
   SQLite graph, so the store greps like files while querying like a database.
5. Khoj/AnythingLLM/people-context/Cognee/MemMachine: not-an-office confirmed, no steal owed.

## Mem0/Zep: does the brief add anything over the banks?

The ask says the w4/stealth-sw-06 memory banks already cover Mem0 and Zep. Honest note: no
`watch/inbox/w4/` directory exists; the stealth-sw-06 bank lives at
`watch/inbox/burn_reset_20260927/flash50/stealth-sw-06.md` (lines 35-38: Mem0 two-phase,
Zep/Graphiti temporal KG with DMR 94.8 vs MemGPT 93.4, Letta self-editing blocks, LOCOMO
dispute). Against that bank today's bytes add three genuinely new facts:
- Mem0's April 2026 algorithm replaced two-phase extraction with single-pass ADD-only
  (mem0.readme.md:44-57), so the bank's line-35 description is now stale, and the vendor
  itself now publishes the OSS-vs-platform honesty clause (line 54).
- Zep's Community Edition is deprecated (zep.readme.md:66-70); the 09-28 bank still described
  Zep as live infrastructure. Self-host Zep is no longer a supported path; Graphiti is.
- Letta moved: letta-ai/letta main README is now a stub (1,574 bytes) handing off to
  letta-ai/letta-code, with the V1 API server retired to the archive branch
  (letta.readme.md:37-39), plus MemFS git-tracking of all context (letta-code.readme.md:24).

## Honest gaps

- docs.letta.com/letta-code/memory was fetched (75,901 bytes) but is a JS shell with no
  readable block content server-side; the block-paging mechanism is therefore cited from the
  MemGPT abstract and the letta-code README bytes, not from the docs page.
- The negative verdicts (no receipted diary, no claim grading) are verified as absence in the
  README bytes only; neither product's internals were audited this session.
- MemGPT abstract txt sha256 is recomputed by the check script rather than pinned in the
  register row (the register row's field says recomputed_by_adjacent_check).
- All fetches are README-level; no repo was cloned in this lane (the sibling ragos lane clones).

## Decision ledger

Names the decision this dance changes: the local-first steal shortlist gains one rung worth
building (the Letta-style model-writable selfblock in the context pack) and one index change
(validity windows on law supersession); Mem0's two-phase entry in the prior bank is marked
stale by bytes; Zep self-host as a product path is dead, Graphiti is the surviving surface.
