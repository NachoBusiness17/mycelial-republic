# PUSH DIET PRESTATE 2026-10-25 (operator GO: "Just keep going sounds good")

Written BEFORE any history rewrite so the pre-diet truth survives a mid-rewrite
session death. Receipt for the full operation lands as PUSH_DIET_DONE_20261025.md.

## Pre-diet measured state (moment 2026-10-25 ~19:40Z)

- Local branch (working): mag/run-beta1-factory-build-audi-20260806T231709Z
  HEAD at rewrite start: (see git log -1; last known 02bb44e8eb ledger-untrack
  + subsequent sweeper commits)
- github remote: https://github.com/NachoBusiness17/mycelial-republic.git
  - refs/heads/mag/run-beta1-factory-build-audi-20260806T231709Z = 3a65384d582e1349d60230a212592f38272253e3
  - refs/heads/main = 7e637a970174041bffdf67fcad9fb4d16afd9916
  - refs/heads/mag-public = 0d77a2ed9d50cd4dffe68703f8ef9e749c7b8330
  - refs/heads/master = dc66499434b050343e81dabcb45b849c5f1fda29
  - refs/heads/standing-wave = 8cf2520eafeb0154d524b20bfae09a822f19e97e
- Delta HEAD vs remote branch tip: 2,928 commits (last push 2026-09-18).
- Object census (git cat-file --batch-all-objects, read-only):
  blobs >100 MB: 211, total 78.688 GiB (github hard-block class)
  blobs 50-100 MB: 18, total 1.145 GiB (warn class, KEPT)
  largest at HEAD tree: watch/inbox/lite_leak_audit_20261023/pc_repo_list.txt
  = 4,431.07 MB (runaway repo-walk dump; the only >100 MB blob at HEAD)
- fsck --connectivity-only: zero missing/broken. 15 orphaned .idx without
  .pack are repack leftovers, harmless.
- local remote (C:\...\Mag-backup.git, same disk) left untouched: it remains
  the full-fat local history archive.

## The blessed plan

1. Untrack pc_repo_list.txt (on-disk truth kept, gitignored) + commit.
2. git-filter-repo 2.47.0 --strip-blobs-bigger-than 100M IN PLACE (local
   history rewritten, data lakes leave git but stay on disk; only HEAD-tracked
   giant is the monster file, restored to disk after).
3. Force-push rewritten branch to github (old tips above are the recovery
   record; github retains unreferenced old objects until its GC).
4. Verify remote tip, fsck, size; receipt.

Data-lake doctrine per the 2026-10-24 large-blob gate: data lakes stay on
disk; git carries the text record (messages + small files), which is the
durable work log.
4c2fe1d2834f80a70885388d898f14f0326a3c28 2026-10-25 15:11:50 -0400
