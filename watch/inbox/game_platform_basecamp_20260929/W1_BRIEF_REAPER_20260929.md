# W1 BRIEF REAPER - Receipt (2026-09-29)

Mickey17 Wave 1 lane: fix wave-ledger return 15 (all 10 FL briefs armed,
zero fired; .md boards invisible to the stealth driver; t_backlog counts
a drained queue instead of the live brief board).

## What landed

- `tools/brief_reaper.py` (new): scans `watch/inbox/**/*BRIEFS*.md`,
  parses `## BRIEF FL-N - TITLE` headers (em-dash or hyphen separator),
  emits queue rows in the driver's own queued-row schema, dedupes on the
  FL id as stable key (holds across lifecycle: queued/sensed/done), appends
  idempotently, prints a live-board backlog census. `--dry` writes nothing.
- `tests/test_brief_reaper.py` (new): fixture parsing, row-schema match
  against a real live queue row, idempotency, dedupe, dry-run no-write,
  census counts, live FREE_LANE_BRIEFS.md parse (10 briefs).
- `tools/stealth_driver.py`: UNTOUCHED (read-only law; schema learned from
  its queue rows and selffeed/impfeed appenders, ~line 301/967 context).

## Row schema (verified against real rows first)

Live queued rows carry `ask, depth, id, parent_id, queued_ts, selffed_ts,
status, tier` (selffeed roots) or `id, ask, tier, status, queued_ts,
source, depth` (impfeed). Reaper rows follow the impfeed analog (external
producer): `id, ask, tier=free, status=queued, queued_ts, depth=0,
parent_id=null, source=brief_reaper`, plus `brief_file`/`brief_title`
metadata. `selffed_ts` deliberately omitted: it marks selffeed provenance
and is operator property (driver line ~1034); the verify sweep reads
`queued_ts` first, so TTL anchoring is intact. Ask is self-contained per
estate law: board preamble (context capsule) + title + body (~1.5k chars).

## Real run evidence

- Dry run first: `boards=1 briefs=10 armed(in-queue)=0 new=10 [DRY]`.
- Real run: appended FL-1..FL-10 to `state/fuel/stealth_work_queue.jsonl`
  (queue ids 23 -> 33). First row spot-check: `FL-1 queued free
  brief_reaper ask_len=1496`.
- Second real run: `armed=10 new=0 appended: none` (idempotency proven
  live, not just in tests).

## Tests (real line)

`./.venv/Scripts/python.exe -m pytest tests/test_brief_reaper.py -q`
-> `7 passed in 0.52s` (2026-09-29, this seat).

## Census fix

t_backlog remains untouched; brief_reaper exists alongside it and its
census line is the live-board truth: `boards=1 briefs=10 armed=10 new=0`
post-run. The loop now consumes its own exhaust instead of re-sensing.

Em-dash count in new files: 0.
