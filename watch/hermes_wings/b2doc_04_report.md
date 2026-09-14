# hermes docs b2 wing 04 (docs/micro-compaction.md)

via seat-b1 beat ext-bf2689a3a4 folded=True

B2DOC_04 — Micro-compaction

1. What it does
After each completed turn, `finalize_turn` absorbs one un-summarized exchange into a single running summary, replacing its messages with one assistant-role summary marker. It keeps a cursor into the transcript, rewrites already-sent history, and syncs that splice into the append-only session DB via `archive_and_compact`. (Note: this file is prose documentation, not source; everything below is stated in it.)

2. Design patterns
- Cursor + transcript-as-truth recovery: a lost in-memory cursor is rebuilt by scanning for the last summary marker.
- Single rolling summary with in-place marker replacement: superseded markers are dropped rather than stacked.
- Bounded-retry skip: the same exchange failing three times advances the cursor past it.
- Soft-archive over append-only storage: rows marked archived and replacements stamped already-persisted.

3. Risks
- Duplicate scheduler: batch (threshold) compaction coexists with per-turn micro-compaction; both emit the same marker format and can act on the same transcript.
- Swallowed exceptions: `finalize_turn` wraps the pass and logs-and-continues; `archive_and_compact` failure silently leaves a session that double-loads on resume.
- Hidden mutation: each pass rewrites sent history, invalidating the provider prompt-cache prefix every turn; no reclaim-size gate exists.
