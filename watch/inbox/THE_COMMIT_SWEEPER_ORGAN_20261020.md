# THE COMMIT SWEEPER ORGAN (2026-10-20)

Operator orders: "can't we just have a cron that commits them independent of
the seat - is there a good reason, steal" + "each seat is about to attempt to
make this so don't all do it."

## Answer to "is there a good reason (not to)"

One nuance, then agreement: instant named commits matter because receipts cite
hashes - uncommitted work cannot be cited. A 10-minute cadence with hint files
preserves named, attributed commits while removing the contention class
entirely. The steal verdict: our own tesuji incidents (2026-09-06) already
wrote the law - per-seat append discipline, single writer per organ. Git was
the last unwired organ. No external steal needed; the water governor's
single-writer pattern, applied to the index.

## What shipped (ONE owner: this seat; all other seats = consumers)

- `tools/commit_sweeper.py` + `tests/test_commit_sweeper.py` (4 tests).
  Zero-direct-git-for-seats: seats write files and optionally a hint
  (`queue/commit_hints/<seat>-<slug>.json` with paths + message). The sweeper
  is the ONLY git writer: hinted batches FIFO (named messages preserved),
  then the anti-shelf leftover sweep (nothing uncommitted waits longer than
  one cycle). index.lock held = defer and retry next cycle, never force
  (seat-ops law). Malformed hints never block other batches.
- Cron: MagCommitSweeper registered, every 10 minutes, hidden window,
  next fire 12:59 today. First sweep will defer until the sibling seat's
  active lock releases, then commit the sibling's staged wave-6 work and
  this seat's round-2 battery artifacts in attributed batches.
- Manual: `queue/commit_hints/README.md` is the organ's user manual.

## The standing convention (for every seat, effective now)

- Do not run git commit/add. Write the work; drop a hint when the message
  matters; otherwise sweep catches it.
- The handwave check: a seat running git while MagCommitSweeper is armed is
  the crime; the log (logs/commit_sweeper.log) records every deferral, so
  lock fights become visible instead of silent.
- Duplicate-organ ban honored per "don't all do it": this receipt declares
  the sweeper the ONE commit organ. If another seat builds a second one, the
  genome patrol's consumer gate strikes the duplicate.

Falsifier: if commits still collide (an index.lock error surfaces in any
seat's output) while MagCommitSweeper is armed and healthy for a full day,
the single-writer design failed and reverts to per-seat worktrees
(git worktree per seat) as the heavy fix.
