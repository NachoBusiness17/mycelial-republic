# hermes docs b2 wing 09 (docs/state-db-recovery.md)

via seat-b1 beat ext-0a1149e879 folded=True

State database and FTS recovery doc for `hermes`. It defines how `SessionDB` degrades gracefully when the FTS5 search index corrupts (detach triggers, mark `fts_stale`, fall back to `LIKE` over canonical rows), and how it quarantines the handle when the canonical `state.db` file itself is corrupt. It closes with explicit repair, snapshot-restore, and post-repair verification procedures.

Notable design patterns:
- Derived-index degradation: drop FTS sync triggers in the same transaction as the failed write, serve search via `LIKE` fallback.
- Quarantined/poisoned handle: typed `StateDbCorruptError` fails every later write immediately, forbids reopen after `close()`, and skips the explicit WAL checkpoint.
- Guarded ownership: rebuilds run only under a cross-process admission lock with a foreign-holder guard; repair goes through a snapshot-and-promotion path.

Risks:
- Single point of failure: the shared handle is poisoned for every holder in the process until restart on a repaired file.
- Hidden mutation: `close()` silently alters durability (skipped checkpoint, `SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE`), and trigger-drop mutates the schema during a message write; Python 3.11 lacks the switch, splitting behavior by version.
- Duplicate rebuild ownership: the never-`FTS5('rebuild')` live path versus the later guarded rebuild path.
