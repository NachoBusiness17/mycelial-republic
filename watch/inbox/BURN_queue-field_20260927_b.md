# BURN queue-field 2026-09-27 (pass b, janitor-axis drain check)

## Verdict

steal

## Evidence

- memory/corpus/LINKS.jsonl row LINKS-328: "Hermes Agent backlog turned into a vector space, agent unleashed on it: 540+ issues closed in 1.5 days"; load_bearing: "vectorized queue + agent self-selection by similarity = batch drain".
- queue/queue_index.jsonl parsed 2026-09-27: 50 rows, 42 open, 8 superseded, 0 closed; 37 stamped roamed over 6 passes (09-26 to 09-27); 13 unroamed (8 superseded, 5 open builder). All 9 open janitor rows stamped: 5 real, 3 needs-operator (Q-001, Q-002, Q-028), 1 vacuous (Q-049).
- Verdict quotes: Q-049 "a demote-candidate telemetry row"; Q-029 "queue-owner should close or rescope rather than build"; Q-044 "leftover drop-candidate pointer awaiting queue-owner close".
- BURN_queue-field_20260925.md falsifier verbatim: "run the janitor roam for 5 consecutive cycles. Metric: open items closed per cycle vs the 5 cycles prior".
- BURN_queue-field_20260927.md: "37/50 roamed"; "the backlog vector space has a dead operator axis where work parks but no rover moves it".
- EVENTS.jsonl last 80 lines: lane intel only, no queue-field event; the index above is the newest byte truth.
- Web: one search, 2026, paraphrase-only pointers (a claimed GitHub "Daily Backlog Burner", rule-based; a dev.to claim platforms "cannot proactively work through a task backlog"); no links resolved, nothing fetched. Owed, not synthesized.

## Steal or Vacuous

The substrate and roam halves of LINKS-328 are already stolen: index landed 09-25, six roam passes ran, the janitor axis is fully triaged. The un-stolen half is the drain. The field has position vectors (verdict stamps) but no closure operator: status grammar holds only open and superseded, zero rows reached closed, and four rows (Q-029, Q-044, Q-045, Q-046) sit stale or resolved-upstream waiting on a "queue-owner" with no lane or tooling. Fleet adopts: a queue-owner close pass as a registered janitor job (one writer per file, no new deps) that flips stamped-stale and resolved rows to closed with the receipt pointer in the row, mirrors closures as DONE marks in queue/todo.md, and starts the falsifier clock. Embeddings stay gated behind a UF-120-style threshold per the 09-25 ruling.

## Falsifier

Pre-registered: when the closure operator lands, run 5 consecutive roam cycles. Metric: janitor-axis rows closed per cycle (baseline starts at landing; prior cycles had no closure operator) plus verdict-flip rate on reopened rows. The LINKS-328 drain pattern is falsified for this fleet if closed-per-cycle stays 0 across those 5 cycles, or closures misroute (closed row whose todo mark contradicts its receipt) over 20 percent; then the index demotes to a static triage ledger. If any seat closes a needs-operator row without operator action, the 09-27 operator-pass stamps are falsified.

## Bibliography

- queue/todo.md; memory/frontier/HELP_WANTED.md
- queue/queue_index.jsonl, 50 rows (parsed)
- memory/corpus/LINKS.jsonl row LINKS-328
- watch/inbox/EVENTS.jsonl last 80 lines
- watch/inbox/BURN_queue-field_20260925.md, _20260926.md, _20260927.md
- watch/inbox/BURN_PLAN_20260927.md
- All repo items read or parsed 2026-09-27.
- WebSearch backlog-vector-space query (2026-09-27): paraphrase surface, no page fetched; owed: GitHub Daily Backlog Burner (claimed Jan 2026), Markus piece (dev.to, claimed May 2026). Closed.
