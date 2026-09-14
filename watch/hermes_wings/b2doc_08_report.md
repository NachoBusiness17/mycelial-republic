# hermes docs b2 wing 08 (docs/session-lifecycle.md)

via seat-b1 beat ext-fa6b348554 folded=True

SESSION LIFECYCLE (b2doc_08.md) — REPORT

WHAT IT DOES
The gateway maps each inbound message to a deterministic session key (`build_session_key`) and manages a `SessionEntry` per key in `SessionStore`, persisted to `sessions.json` with SQLite as the canonical transcript store. It decides when sessions reset or resume (policy + flag state machine), queues concurrent messages per session, and evicts cached `AIAgent` instances via a 5-minute background watcher.

DESIGN PATTERNS
- Value object: frozen `SessionSource` records message origin and round-trips via `to_dict`/`from_dict`.
- State machine by boolean flags: `suspended` > `resume_pending` > policy expiry, evaluated in priority order in `get_or_create_session`.
- Single-slot mailbox plus overflow list (`_pending_messages` + `_queued_events`) gives burst collapse with FIFO promotion.

RISKS
- SPOF: one `_session_expiry_watcher` task drives finalization, idle sweep, memory-pressure eviction, and pruning; if it stalls, RSS climbs unchecked between 300s ticks.
- Hidden mutation: read-named `get_or_create_session()` clears `resume_pending`, consumes `was_auto_reset`, and writes `sessions.json` as side effects.
- Duplicate reset paths: policy expiry is evaluated both inline on access and by the watcher; `expiry_finalized` force-set after 3 failures silently skips cleanup.
