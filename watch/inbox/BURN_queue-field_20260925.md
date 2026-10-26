# BURN receipt: queue-field (2026-09-25)

## Verdict

steal

## Evidence

- "43 open checkbox items, 74 closed" in `queue/todo.md` (counted 2026-09-25 by grep). Items are tagged checklist lines: seat tag, one-line pointer-dense prose, $0 cost, section-dated. The FIFTY WIDE 20260917 board compresses FW-01..FW-50 into 9 bullets; most items carry no stable ID.
- `memory/frontier/HELP_WANTED.md`: generated 2026-09-22, "Stack: 5", 7 asks, "journal signals: 0". Three asks are degenerate placeholders ("research A/B/C"). Two are shape slots: frontier_gap "route" and "audit", each marked "cheap success below bar". Only 2 of 7 asks are real text.
- Retrieval substrate today: `catalog/catalog.jsonl` + `catalog/tags.jsonl` (946,773 rows, kind+age_class, per CORPUS MAP row in todo.md), corpus_search/get/tail/stats tools in tools.TOOL_MAP, and `tools/index/projects_index.py` (ESTATE_INDEX, "one master JSONL with a 'proj' field per row", read-only, constant-name outputs). No embedding index exists: grep of tools/ and mag/ shows "embedding" only as incidental comments (bare_numpy normalize helpers). FTS5 decision explicitly deferred to UF-120's measured threshold.
- Web: "Engineers devote countless hours to managing issue backlogs, chasing down unstable build pipelines and updating stale documentation"; GitHub's Agentic Workflows "can review issues, suggest code changes, generate reports, or flag problems in test coverage"; teams "begin with low-risk experiments and keep humans involved in close oversight" (DevOps.com, 2026-02-18).

## Steal or Vacuous

The LINKS-328 vector-space framing is vacuous at current scale: 43 open items do not need embeddings, and the fleet already runs bulk roam (FIFTY WIDE boards, janitor sections). What is worth stealing is the substrate step: the backlog is not machine-readable as records. Build spec, kept minimal:

- Index shape: `queue/queue_index.jsonl`, one row per checkbox item: {id (Q-NNN), status, seat_tag, section_date, text, pointers[], cost}. Regex parse; no new deps; idempotent rebuild like the estate indexer.
- Retrieval key: seat_tag first, then pointer basenames (they resolve into the tag catalog). No vectors. Embeddings gate on the same UF-120-style measured threshold, not before.
- Janitor roam protocol: each janitor cycle reads the index, filters seat_tag=janitor + status=open + cost $0, takes the lowest pointer-resolved item, closes with a receipt pointer back into the row. Mirrors the existing FKB/janitor loop; no effect authorization changes.
- Side fix: HELP_WANTED placeholder asks (research A/B/C) should be dropped at generation time; they poison the ask surface.

## Falsifier

Pre-registered: build `queue/queue_index.jsonl` and run the janitor roam for 5 consecutive cycles. Metric: open items closed per cycle vs the 5 cycles prior (hand-sectioned roam), plus misroute rate (rows whose seat_tag does not match the work actually done, target under 10 percent). The pattern is falsified for this fleet if closed-per-cycle does not improve or misroute exceeds 20 percent; then file queue-index as dead and keep the markdown-only roam.

## Bibliography

- `queue/todo.md` (read 2026-09-25)
- `memory/frontier/HELP_WANTED.md` (read 2026-09-25)
- `memory/corpus/MANIFEST.md`, `catalog/`, `tools/index/projects_index.py`, grep of tools/ + mag/ (read 2026-09-25)
- "GitHub Tests AI Agents to Handle Repository Upkeep", James Maguire, DevOps.com, 2026-02-18 (fetched 2026-09-25)
- OWED: GitHub Docs "Triaging an issue with AI" (URL from search summary, fetch 404); Augmentcode "AI Sprint Planning Tools" piece (claimed July 2026 by search summary, URL not resolvable, fetch 404). Not synthesized.
