# COMMIT HINTS - how seats talk to the sweeper (2026-10-20)

THE LAW: seats never run git. One writer owns the index (tools/commit_sweeper.py,
cron MagCommitSweeper, every 10 min). Two seats committing directly = index.lock
fights (this file's reason for existing: two seats blocked each other twice on
2026-10-20).

To get a NAMED commit, drop a hint file here:

    queue/commit_hints/<seat>-<slug>.json
    {"paths": ["watch/inbox/FOO.md", "src/bar.py"],
     "message": "SEAT: what landed and why (one line)"}

The sweeper commits hinted batches FIFO (named messages preserved) then sweeps
everything unattributed with a generic message. Consumed hints are deleted.
No hint needed for routine work - the leftover sweep catches it within 10
minutes; hints are for when the commit message matters.

If index.lock is held, the sweep defers and retries next cycle. Never force-
remove a lock (seat-ops law).
