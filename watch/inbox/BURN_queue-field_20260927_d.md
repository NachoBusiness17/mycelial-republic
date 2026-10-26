# BURN queue-field 2026-09-27 d (drain-holds verification)

## Verdict

green

## Evidence

- `grep -c '"status": *"closed"' queue/queue_index.jsonl` = 3 (expected 3, met). Full tally by status over 50 lines: 3 closed, 39 open, 8 superseded.
- Open rows by source: todo 34, help_wanted 5, events 0.
- Q-029 (index line 29): `"closed_by": "queue-owner"`, `"close_receipt": "watch/inbox/CORPUS_MAP_SALON_20260918.md"`, closed_ts 2026-09-27T09:27:44Z, close_note "scanner v3 landed by other hands".
- Q-044 (line 44): closed, `"close_receipt": "memory/frontier/help_wanted/resolved/research_A.md"`, "upstream RESOLVED by gopher t13a 2026-09-26".
- Q-045 (line 45): closed, `"close_receipt": "memory/frontier/help_wanted/resolved/research_B.md"`, "upstream RESOLVED by gopher t13b 2026-09-26".
- All three close_receipt paths stat EXIST on disk (byte check this pass).
- watch/inbox/QUEUE_CLOSE_VERB_20260927.md claims "Queue state after: 39 open / 8 superseded / 3 closed of 50"; the live bytes match exactly, so the drain holds.
- Cross-check of pass-c arithmetic: 42 open rows triaged = 39 still open + 3 now closed. Consistent.
- queue/todo.md: janitor section is mostly checked rows; open lines are estate and operator items (Studio smoke, archive drop, burn stones), no queue-closure debt.
- watch/inbox/EVENTS.jsonl tail 30: no queue-kind events; tail is lane-denominator findings (Groq fleet ids gone, Cerebras trial gate, NVIDIA re-probe) plus two mirrored Oracle rows. Backlog surface quiet on the queue axis.

## Steal or Vacuous

Nothing new to adopt; the drain verified. Fleet canon already carries the close verb (tools/queue_close.py exists, RECEIPT_BINDINGS-strict form) and this pass confirms its output is durable: the closed count is byte-stable across sessions and every close cites a byte-existing receipt. Standing bar for future roams: grep count 3 with all three close_receipt fields intact; any drift without a matching close receipt is a fabrication smell and goes to the ledger as owed. The 39 open rows are the roam space, not debt: 34 todo and 5 help_wanted, each awaiting a janitor roam verdict, and events contribute zero rows.

## Bibliography

- queue/todo.md (read whole)
- watch/inbox/EVENTS.jsonl (tail 30)
- queue/queue_index.jsonl (status/source greps; lines 29, 44, 45 read)
- watch/inbox/QUEUE_CLOSE_VERB_20260927.md (read head)
- tools/queue_close.py (existence confirmed only)
