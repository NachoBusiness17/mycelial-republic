# RIB — MD RECORD (everything md, tracked, open-append single item)
**Schema:** rib.md.record.v1 · **ts:** 2026-09-21T12:50Z
**Source:** operator, Sept 21: "Everything should be md rib and tracked open append single item self steal"
(extends the prompt-of-record finding from the long-prompt retest)

## Invariants
- id: everything-md — predicate: every durable prompt, brief, receipt, decision and
  dispatch input is an md file (or structured file with a register event) on disk.
  Chat and code strings are heat. action: write. anchor: this card + QUIET_RADAR
  2026-09-21 prompt-of-record entry.
- id: prompts-are-records — predicate: the exact prompt sent to any model is filed
  as md beside its outputs, before or at dispatch. A failure against an unfiled
  prompt is not reproducible and therefore not a finding. action: gate.
  anchor: brief-v2 gap (never filed; failure unreproducible; radar 09-21).
- id: tracked — predicate: every durable write gets a register event in
  index_events.jsonl. Untracked = not filed = heat. action: register.
  anchor: shared-surface contract + index_events register.
- id: open-append-single-item — predicate: records (events, kifu, receipts,
  verdicts) are written open-append, ONE item per record, never rewritten.
  Corrections append; they do not edit history. Artifacts may evolve, but every
  evolution appends an amendment event. action: write pattern.
  anchor: index_events.jsonl shape (one JSON line, one item).
- id: self-steal-audit — predicate: this law is metered against our own estate —
  tools/md_record_audit.py reports unindexed files and violations by number.
  Prose about compliance is heat. action: meter. anchor: MD_RECORD_AUDIT output.

## Fold with existing doctrine
- Residual-on-disk-is-truth (AGENTS.md): this law names the FORMAT of that truth.
- Monkey-patch ruling honored: no new gates over existing ones — the audit cites,
  the register tracks, nothing retroactively rewrites.
