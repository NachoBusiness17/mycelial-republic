---
name: operator-saves-everything
description: Operator's standing stance — "i save everything"; durable work
  lands in watch/inbox, and after incidents they want a safeguard checkpoint
  commit immediately
metadata:
  node_type: memory
  type: user
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

The operator's data stance is "i save everything" — raw exports (e.g. `matthew_export.tar.gz` at repo root) and every session drop stay on disk, durable cross-surface work goes to `watch/inbox/` per the shared-surface contract, and git is the safeguard layer.

**Why:** On 2026-09-14 a z.code window deleted itself mid-session — the operator called it unprecedented ("first time in months that a window not only failed it deleted itself") — and their immediate response was "we should do a commit." They judge recovery by whether the durable copy survived, not by session caches. A post-mortem of the self-deleting window was offered but not yet done.

**How to apply:** After any incident or substantial new work, do the checkpoint commit without being asked twice. They want breadth (commit all genuine work, including big curated corpora), not blind `git add -A` — protect the repo from logs/deps/embedded clones and report exclusions transparently. See [[repo-git-hygiene-checkpoint-20260914]], [[zcode-session-recovery-path]].
