# INCIDENT + FIX: the 18k uncommitted shelf (2026-10-20)

**Symptom:** `git status` showed 18,507 dirty entries (18,474 staged), HEAD frozen
at `368fd55f0` (13:59) for six hours, while `logs/commit_sweeper.log` claimed
"tip" commits and the scheduled task reported Running.

**Root cause chain (five failures, any one of which was enough):**

1. **The pre-commit hook could not run.** `githooks/pre-commit` passed an MSYS
   absolute path (`/c/Users/.../python.exe`) to a Windows interpreter, which
   resolved it as `C:\c\Users\...` and died with "can't open file". Every commit
   failed, including every sweeper batch. (Fixed: `cd` to the repo root and use
   relative paths.)
2. **The hook was O(files) subprocesses.** It ran `git show :<path>` once per
   staged file. A 13,299-file memory batch meant 13k processes; one commit ran
   40+ minutes holding `.git/index.lock`, so every later sweep deferred.
   (Fixed: a single `git cat-file --batch`, binary-safe; 13k files now scan in
   seconds.)
3. **The shelf compounded.** A failed commit leaves its `git add` staged, and
   the next sweep scanned the *entire* accumulated index again. (Fixed: the
   sweeper resets the index at the start of every sweep; files stay on disk.)
4. **The secret gate blocked a public handle.** `GHOST_X_HANDLE` (an X handle
   quoted in two sealed receipts) was treated as a credential, so every batch
   touching `watch/inbox` failed. (Fixed: classified as a public identity value,
   like `_HOST`/`_URI`; values are still never printed.)
5. **The task log was truncated every run** (`*>` in PowerShell), so the 0-byte
   `logs/commit_sweeper_task.log` hid hours of deferrals. (Fixed: append +
   UTF-8.)

Secondary bugs fixed while in there:

- No singleton: the scheduled task and manual runs fought over the index.
  Now `tools/instance_guard.claim_process("commit_sweeper")` (the estate's own
  pidfile guard) makes the second runner refuse.
- Instant deferral on `index.lock`: now waits up to 6×5s for a transient lock.
- Chunk threshold 2,000 → 500 files, and the `(root)` area passes explicit
  paths instead of `"(root)/"` (which fell through to `git add -A` and staged
  the whole tree).
- Hint batches with gitignored paths: check-ignore filter + per-path retry, and
  "nothing staged" is success (so hints stop retrying forever).
- `git status --porcelain` used to decide "is there anything to commit" also
  counted untracked live-seat writes → empty-commit failures. Now it checks
  `git diff --cached --name-only`.

**Result (23:20Z):**

- dirty: **0** (1 transient file written by a live seat between sweeps is normal)
- commits landed since 13:59: **32**
- areas landed: configs, catalog, corpus, Temp, roblox_to_godot, mag, scripts,
  tests, dashboard, queue (1,860), memory (13,301), watch (2,936), leftover (64)
- `tests/test_commit_sweeper.py`: **4 passed**
- `MagCommitSweeper`: **Enabled, Ready**, next run 19:29 local
- secret gate: PASS, 55 live values, values never printed

**The real numbers behind the scare:** of the 18,507 "dirty" entries, ~16,600
were a stale staged shelf of *ignored* files (mostly `memory/biography_v2`);
the actual working-tree change set was ~1,900 files. The shelf was an artifact
of failed commits, not 18k files of lost work.

**Standing rules for this organ (add to AGENTS.md if the operator wants):**

1. Seats never run git. They write `queue/commit_hints/<seat>-<slug>.json`.
2. One writer: the sweeper, every 10 minutes, guarded by `instance_guard`.
3. A commit must never stage the whole tree. Every batch gets explicit paths.
4. If a hook edit touches path handling, test `bash githooks/pre-commit` from
   the repo root before trusting the schedule.
5. A 0-byte task log is a failure signal, not a quiet run.

**Open risk, separate from this fix:** the GitHub remote
(`NachoBusiness17/mycelial-republic`) is **public**, and HEAD already tracks
~40,000 `memory/` files plus ~24,500 `watch/` files. Nothing in this incident
leaked (nothing was pushed), but the repo currently mixes private operational
tape with public code. Decision needed from the operator: private remote, or
split the tape out of the public repo.
