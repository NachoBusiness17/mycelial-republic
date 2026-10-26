# BURN b2-wave-fold 20260927 b: visor v2 writer-liveness (fix Q3, GAP 3)

## Verdict

STEAL. The visor now answers GAP 3's question ("which surfaces still have a living writer, which lane is starving now") in one read-only console section.

## Evidence

- tools/visor.py gained scan_billboards(): hardcoded 10-surface table (deck.html, DAY_WORK_DIGEST.md, trails/day_work.jsonl, latest.md, CURRENT.md, attention.md, bonds_active.md, drift_board.html, INDEX.json, queue_index.jsonl); each row prints mtime age + classification + writer identity.
- Classes verified by temp-file unit run: LIVE < 24h, STALE < 7d, DEAD > 7d, MISSING, FROZEN banner.
- FROZEN check mirrors the sealed writers' own contract byte-for-byte (first 240 chars, BOM stripped, startswith "# FROZEN": mag/brief_local.py:168, mag/session_state_brief.py:350) so the visor and the seal can never disagree.
- Live run 2026-09-27 (exit 0): brief shows FROZEN at 7h despite fresh mtime (banner beats age math); tally FROZEN 1 / LIVE 9; "stalled lanes (digest self-report): elder", extracted from the on-disk "**elder STALLED-TRAIL**" inline marker; a "## STALLED" section shape also parses (temp test returned economist, prose).
- New finding surfaced by the table itself: queue/queue_index.jsonl has no writer anywhere in the repo (only the visor reads it); the row is labeled unattributed with the audit date.
- Read-only preserved: no surface file modified; em-dash byte scan over visor.py returns zero.

## Steal or Vacuous

Steal: the hypervisor-board pattern (the surfaces ARE the communication) extended with the writer-identity column, and the freeze-banner detector is a self-steal of the P0-1 warm-face seal law rather than a reimplementation that could drift.

## Falsifier

Classify any billboard DEAD while its writer demonstrably ran within 24h, or show a FROZEN verdict on a brief whose first 240 chars lack the banner: either outcome breaks the table.

## Bibliography (closed)

- watch/inbox/ATLAS_SELF_STEAL_20260927.md (GAP 3, fix queue Q3)
- tools/visor.py (pre-edit read, post-edit run)
- memory/briefs/latest.md (banner shape)
- dashboard/static/DAY_WORK_DIGEST.md (stall marker shape)
- mag/brief_local.py and mag/session_state_brief.py (seal contract)
