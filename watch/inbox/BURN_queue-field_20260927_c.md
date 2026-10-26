# BURN queue-field 20260927 c

## Verdict
steal

## Evidence
- queue/queue_index.jsonl (mtime 2026-09-27T02:14:53Z, before tonight's 04:15Z pass): 50 rows total. Status counts by parse: 42 "open", 8 "superseded", 0 "closed". Zero writes since 02:14:53Z: nothing closed since 04:15Z.
- queue/todo.md: `grep -c "^- \[x\]"` = 81, `grep -c "^- \[ \]"` = 55, SUPERSEDED mentions = 2. Last write 2026-09-27T05:50:00Z (eigenmap fold annotation, content dated 2026-09-27). No git history exists for this file and `git diff` shows no checkbox flips, so no verifiable close in it since 04:15Z. Prior-state snapshot: owed.
- Queue-owner waiters: rows Q-029, Q-044, Q-045 name one. Byte count: "queue-owner" x2, "queue owner" x1 = 3 rows, not the 4 the prior pass reported, on identical bytes (index untouched since 02:14:53Z). Q-044: "leftover drop-candidate pointer awaiting queue-owner close." Q-045: "the board names this row verbatim: queue pointer Q-045 left for queue owner."
- Upstream work does complete: memory/frontier/HELP_WANTED.md briefs 1-3 each carry "RESOLVED 2026-09-26 by gopher t13a/t13b/t13c: PRUNE executed" with receipt paths filed. The matching index rows Q-044/Q-045 stay status "open". Triage roams; drain never fires.
- Structure: `grep -rln "roam_verdict" --include="*.py"` over the repo returns nothing. No module writes row status at all; tools/visor.py only reads queue_index.jsonl as an observability surface ("the board is a read-only view over shared surfaces"). No queue-owner is registered anywhere and no code path can emit "closed". The drain is structurally absent, not neglected.
- Web search "task queue closure automation agents done-state verification backlog 2026": thin. Two 2026 help-desk guides surfaced (devrev.ai 2026-05-05, hiverhq.com 2026-05-17), snippet-level, not fetched; nothing on done-state verification for agent task queues.

## Steal or Vacuous
Steal one law: closure is a receipt check, not a mood. The fleet registers a queue-owner with one close verb: a row flips open to closed only when the row's cited receipt path byte-exists on disk (the trust-bytes law the census carrier already runs), and superseded requires naming the successor pointer. Until that verb exists, upstream gophers finish real work (t13a/t13b/t13c) while the ledger shows 0 of 50 closed forever: true work, false ledger, the no-fabrication law run backwards. Janitor roam already writes verdicts into the index (02:14:53Z tonight); give that same pass the authority and obligation to drain rows whose receipts exist, so drain becomes a janitor cycle duty instead of an orphaned ask.

## Falsifier
Pre-registered. If the queue-owner close verb lands, then within one janitor cycle: (a) Q-044, Q-045 and Q-029 flip to closed on already-existing receipts with zero new work; (b) `grep -c '"status": "closed"' queue/queue_index.jsonl` >= 3; (c) every closed row's cited receipt path byte-exists on disk. The build fails its own falsifier if any closed row's receipt is missing, or if closing requires hand-editing the jsonl instead of running the verb.

## Bibliography
- queue/todo.md (read whole)
- memory/frontier/HELP_WANTED.md (read whole)
- watch/inbox/EVENTS.jsonl (tail -40)
- queue/queue_index.jsonl (50 rows, grep + json parse)
- tools/visor.py (header + status-write greps)
- repo-wide grep for roam_verdict writers
- WebSearch snippets: devrev.ai, hiverhq.com (surfaced, not fetched)
