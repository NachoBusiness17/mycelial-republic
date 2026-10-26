# PA-S5stores-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## 1. Remaining Lock-Class Bugs

**Deadlock via lock-order inversion.**
`exclusive()` acquires per-path RLock then byte lock (store_io.py:98-109).
If thread A calls `exclusive("users.json")` then `exclusive("orders.json")` while thread B does the reverse, the RLocks block each other.
No ordering discipline is documented or enforced.
Falsifier: two threads acquiring two paths in opposite order will hang.

**NFS / WSL byte-lock bypass.**
POSIX branch uses `fcntl.flock` (store_io.py:49).
`flock` is not enforced on NFSv3 mounts; on WSL2 accessing `/mnt/c/`, the lock is a Linux-side advisory lock invisible to the Windows process holding the same file via `msvcrt.locking`.
Two processes on opposite sides of the WSL boundary will both "acquire" the lock.
Context assumption: any deployment where the store path sits on a network share or a WSL-mounted Windows volume.

**Unbounded `_THREAD_LOCKS` growth.**
The dict at store_io.py:57 is never pruned.
Long-lived processes cycling through many store paths leak one RLock per unique path string.
Not a correctness bug; a slow leak.

**No reader-writer distinction.**
The byte lock is always exclusive (`LOCK_EX`, `LK_NBLCK`).
A read-only consumer that needs consistency must take `exclusive()`, serializing behind writers unnecessarily.
Not a bug today because `atomic_write_text` makes lockless reads safe, but any future read-modify-write that only reads will over-lock.

## 2. `os.replace` Atomicity on Windows NTFS

`os.replace` maps to `MoveFileExW` with `MOVEFILE_REPLACE_EXISTING`.
The rename itself is atomic on NTFS: readers observe old or new bytes, never a torn file.
The code correctly documents and handles the Windows-specific failure mode: `PermissionError` when another handle holds the target open (store_io.py:119-121).
The 5-second retry loop (store_io.py:122-127) is the mitigation.
Residual risk: under sustained concurrent readers the retry can exhaust and raise, losing the write.
No data corruption, but a liveness gap.

## 3. The One Test for the Worst Hole

**Test: cross-path lock-order deadlock detection.**
Spawn two threads. Thread A: `exclusive(pathA)` then `exclusive(pathB)`. Thread B: `exclusive(pathB)` then `exclusive(pathA)`. Join both with a 10-second timeout. Assert both completed.
This will hang today, proving the ordering bug is live.
It is the worst hole because it is silent (no exception, just a hang) and depends entirely on caller discipline that the module does not enforce.

**Deliverable falsifier:** if no caller in the estate ever nests `exclusive()` on two different paths, the deadlock is unreachable and the test is vacuous. Grep for nested `exclusive` calls to confirm.
