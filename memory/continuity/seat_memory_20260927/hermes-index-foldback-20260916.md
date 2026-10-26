---
name: hermes-index-foldback-20260916
description: Hermes seat's first real directive seeded — INDEX foldback (388 unindexed inbox files, 84 dead pointers, 13 hash mismatches, wrong root); nudge command noted, not run; loop closes on Hermes' own receipt
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

2026-09-16 night (lane H1): the Hermes seat received its first real directive via the
directing-seats pattern — the shared-surface INDEX foldback.

Baseline quantified (parked at wave_20260916/receipts/H1_validate_baseline_20260916.json):
`mag.shared_surface validate` → exit 1, 98 errors — 1 wrong INDEX root (C:/…/watch/inbox
instead of /board/inbox), 84 indexed items missing from disk (54 unreachable /board/ paths),
13 hash mismatches, 388 of 443 top-level inbox files unindexed (~4.01 MB; biggest:
dogfood-trajectory save.txt 314 KB, kirk_*.jpg 239 KB, ractor-salon-001.txt 190 KB).

Load-bearing discovery: mag/shared_surface.py is deliberately READ-ONLY (path|status|validate
— no indexer), and watch/inbox/index_events.jsonl already carries the register/amend event
convention the fold appends to.

Directive: watch/inbox/HERMES_DIRECTIVE_INDEX_FOLDBACK_20260916.md — ONE artifact
(append-only fold: root fix, 84 verbatim tombstones, 13 event-log amends, 388 registers,
events log registered last), output contract (validate clean or every residual exception
itemized), falsifiers (no file deleted, hashes preserved verbatim, append-only, double-
validate idempotence). Handoff: queue/handoff/HANDOFF-2026-09-16-index-foldback.json; seeded
to queue/handoff/hermes/INBOX/20260916T2054Z-zcode-index-foldback.md.

Hermes binary verified present (hermes.EXE v0.21.1); nudge command noted (`hermes -z "…"`)
but NOT run (no-paid-inference law). LOOP CLOSES on Hermes'
HERMES_INDEX_FOLDBACK_RECEIPT_20260916.md — until then the INDEX stays an F on every audit.
See [[hermes-wow-bones-azerothcore-20260916]], [[directing-seats-lesson]].
