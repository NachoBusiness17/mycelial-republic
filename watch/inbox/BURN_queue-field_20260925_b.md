# BURN receipt: queue-field _b (2026-09-25)

## Verdict

steal

## Evidence

- `queue/todo.md` read in full: raw checkbox count is 43 open, but the FIFTY WIDE 2026-09-15 section header states "(SUPERSEDED 2026-09-17 by FIFTY WIDE 20260917 below ... still-open stragglers re-seeded as FW-37..FW-49)". True open in todo.md is 35; a bare grep census overcounts by 8.
- `memory/frontier/HELP_WANTED.md` (generated 2026-09-22, "Stack: 5"): asks 1-3 are literally "research A", "research B", "research C"; asks 6-7 are shape slots marked "cheap success below bar". Only 2 of 7 asks carry real text.
- Web (search 2026-09-25): the search summary attributed to hypertask.ai the line "Structured task data (JSON, not HTML) is the minimum bar. If the tool can't return a task as machine-readable output, agents can't use it." Fetch of that page contradicts the summary: no such sentence on the page, no publication date, only product copy ("AI Triage via CLI, MCP or built-in Hyper AI"). No canonical agent-task-index standard surfaced; the space fragments across MCP/A2A papers (arxiv, Jul 2026, seen only as summary) and vendor blogs. Unverified material filed as owed, not synthesized.

## Steal or Vacuous

The prior burn's build step is executed. Built `queue/queue_index.jsonl`: 50 rows, ids Q-001..Q-050, fields id / ts / source / title / pointer / seat_hint / status / effort. 42 open (35 from todo.md + 7 from HELP_WANTED.md), 8 superseded (kept and tagged so the census stays honest rather than silently dropped). Open seat distribution: builder 14, janitor 9, operator 7, judge 7, scout 5. Effort: medium 19, small 15, trivial 6, large 2. Two corrections landed with the build: (1) open census corrects from 43 to 35 once the superseded section is separated; (2) the HELP_WANTED placeholder asks are now named rows (Q-044..Q-046, drop candidates; Q-049/Q-050 demote candidates) instead of invisible poison in the ask surface. The janitor roam set is the 9 janitor-open rows (Q-001, Q-002, Q-003, Q-008, Q-021, Q-023, Q-028, Q-035, Q-049), all $0-class. Known limit: FW-01..50 stay packed at bullet granularity (9 rows); full per-FW expansion needs memory/plans/fifty_wide_20260917.md, an owed pointer outside this burn's KL set. The generator was a one-shot temp script; a durable idempotent rebuild script is the next rung.

## Falsifier

Pre-registered, now measurable on the built index: run the janitor roam 5 consecutive cycles against the 9-row janitor-open set. Metrics: open items closed per cycle vs the 5 prior hand-sectioned cycles, and misroute rate (seat_hint not matching work actually done; target under 10 percent, pattern falsified over 20 percent). Second falsifier on the census fix: any future tool that recounts open items by bare checkbox grep and reports 43 is wrong by 8; recounts must exclude status=superseded rows in the index.

## Bibliography

- `queue/todo.md` (read in full, 2026-09-25)
- `memory/frontier/HELP_WANTED.md` (read in full, 2026-09-25)
- `watch/inbox/BURN_queue-field_20260925.md` (prior burn, read 2026-09-25)
- `queue/queue_index.jsonl` (built this burn, 50 rows)
- hypertask.ai "AI Agents in Project Management" page (fetched 2026-09-25; negative result: the quoted sentence in the search summary is NOT on the page)
- OWED: cellcog.ai agent-handoff-protocols piece; arxiv "Comparative Study of MCP and A2A" (Jul 2026). Seen only as search summaries, not fetched. Not synthesized.
