# PA-S5stores-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

**STANGER AUDIT VERDICT: mechanism is sound in-process; one platform bug and two unverified externals.**

## 1. Remaining lock-class bugs

**BUG (Windows): the 30s timeout is dead code on win32.** `exclusive` computes `deadline` and raises `TimeoutError` when `_lock_byte` raises (00__store_io.py:147-153). But the win32 `_lock_byte` (lines 56-66) catches `OSError` itself and loops `time.sleep(0.01)` forever - it only ever returns on success or hangs. So `TimeoutError` is unreachable on Windows; a stuck lock-holder means infinite wait. The POSIX branch (`flock`, blocking, lines 72-78) also never raises, so the deadline never fires there either - `exclusive`'s timeout path is dead on both platforms.

**Crash-with-lock: OK.** Byte locks are OS-owned fds; process death releases `msvcrt`/`flock` locks, and the never-unlinked lock file (docstring, lines 109-112) correctly avoids the unlink race.

**Reader starvation: none structurally.** Readers never take the lock; `os.replace` gives them a fresh inode (POSIX) or a retry-bounded swap (Windows, lines 172-185). Residual: a Windows `read_text` longer than `_REPLACE_TIMEOUT_S = 5.0s` turns into `PermissionError` - measure context: cold NTFS, small JSON, fine.

**Ordering hazard (can't falsify from this file):** single lock per path, but nothing forbids thread A doing `exclusive(a)` then `exclusive(b)` while B does the reverse. No internal nesting exists here; callers are the risk. `UNVERIFIED` without call sites.

**NFS/WSL: UNVERIFIED.** `flock` on NFSv3 depends on lockd; on WSL2 `/mnt/c` (9p/drvfs) `flock` is reported to succeed on all hosts without mutual exclusion. The docstring's allowlist (lines 87-90) refuses non-repo paths, which mitigates but the repo on a share would pass resolution.

## 2. os.replace on NTFS

Atomic per-call, same volume (mkstemp in `path.parent`, line 169): yes, it is `MoveFileEx(REPLACE_EXISTING)`, an atomic metadata swap. Durability: no - the docstring explicitly skips fsync-dir (lines 20-21), so power loss can resurrect old bytes. Crash-atomic, not power-atomic. That matches the stated contract.

## 3. The one test

Windows, two processes: P1 holds `exclusive(p)`; P2 calls `exclusive(p)` with a monkeypatched `_LOCK_TIMEOUT_S = 0.1` and must raise `TimeoutError` within 2s. Current code hangs forever (bug above). **Falsifier:** the test passing on win32 without a `_lock_byte` change proves my line 56-66 reading wrong.
