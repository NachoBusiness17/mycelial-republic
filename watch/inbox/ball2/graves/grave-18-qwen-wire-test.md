# GRAVE 18: queue/handoff/qwen-wire-test-20260807.json

- **Filed:** 2026-09-29 by lane grave-supersede (division C, GRAVEDIGGER, ball 20260929)
- **Classification:** FOSSIL (machine row watch/inbox/ball2/graves/grave-supersede.jsonl)
- **Buried entry:** `queue/handoff/qwen-wire-test-20260807.json` (handoff.v1, owner clerk, assignee watcher, T3, created 2026-08-07T05:55Z: "Write a Python one-liner that prints Hello Mag")
- **Nothing was deleted, moved, or edited. Deletions are operator-gated.**

## What justifies the burial

This is a one-shot wire test, not owed work: its "work" was the act of
dropping a handoff.v1 file and watching the ingest classify it. That
mechanism is standing code now - `mag/handoff_inbox.py` lines 19-29 classify
by filename prefix and schema (`handoff.v1` -> class "grok"), and the
queue/handoff/README.md schema map documents the six v1 families against
that gate. A 53-day-old hello-world fixture has no forward content and no
living successor needed; FOSSIL.

## Note

`return_path` pointed at `memory/working.md` with rollback "keep prior
working.md"; no result artifact was claimed. Recorded as-is; nothing chased.
