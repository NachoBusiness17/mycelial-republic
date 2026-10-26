# Committee on Records - Standing Agenda

Jurisdiction: the single writer, the append-only ledger, the batch commits, the tombstone law.

## Open Questions

1. Has any index.lock collision surfaced in any seat's output in the last 24 hours?
2. Is the backlog under 10 files?
3. Are all hint files consumed (none stale)?
4. Has the tombstone law been tested in the battery rounds (the door's own erasure handling, graded against the derived law)?

## Clock

Every 10 minutes (MagCommitSweeper cron). Batch commits per area.

## Receipt format

One git commit per area batch: "commit sweeper: {area} batch ({N} files) {timestamp}".

## Current status

Backlog drained from 18,490 to single digits. All hints consumed. The organ survived three timeout lessons, two lock collisions, one duplicate-organ incident, and one nul-file landmine.

## Laws this committee carries

- One writer owns the index. No exceptions.
- The record only grows. Deletion is the only real theft.
- The tombstone: erase the content, preserve the fact of erasure.
- The anti-shelf law: nothing uncommitted waits longer than one cycle.
