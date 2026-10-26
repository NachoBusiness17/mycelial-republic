# PA-S5stores-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

(1) Lock class bugs

- **Lock ordering**: No global order between `.lock` file acquisition and `tmp` file creation. Two paths `a/b.json` and `a/c.json` have independent `.lock` files; a transaction touching both can deadlock if threads acquire in different orders. The code has no multi-path API, so this is UNVERIFIED as a bug but architecturally latent.

- **Crash-with-lock**: The OS byte lock (`msvcrt.locking` or `fcntl.flock`) is process-scoped and released on `fh` close, which happens in the `finally` block. If the process crashes inside `yield`, the lock file handle closes and the lock releases. This is correct behavior, not a bug. However, the `.lock` file itself is never unlinked, leaving stale lock files on disk. Harmless but messy.

- **Reader starvation**: `exclusive()` uses `LOCK_EX` (exclusive) on the byte lock; there is no shared/reader mode. Readers that want consistency must also call `exclusive()`, meaning all access serializes through writers. This prevents reader starvation by eliminating readers, not a bug but a performance limitation.

- **NFS/WSL semantics**: `fcntl.flock` is advisory and works on NFS if both sides cooperate, but `msvcrt.locking` is mandatory (blocks at the OS level). On WSL1, `fcntl.flock` on NTFS is emulated and may not block cross-Windows-process; on WSL2 it's native Linux and works. The code does not detect or warn about these environments. UNVERIFIED as a bug.

(2) `os.replace` atomicity on Windows NTFS

Yes, for the access pattern. NTFS `MoveFileEx` with `MOVEFILE_REPLACE_EXISTING` is atomic at the metadata level (file:90-96). The retry loop handles `PermissionError` from open handles, not atomicity failure. The pattern (write to temp, fsync, rename) matches NTFS atomic rename guarantees.

(3) The one test

A stress test spawning 16 processes, each with 8 threads, all racing to increment a counter in a shared JSON file for 10 seconds, then verifying the final count equals total increments. This catches the remaining hole: **lock file deletion races** if someone adds `unlink(lock_file)` later, or **byte lock not covering the data file** (if a reader bypasses `exclusive()` and reads the JSON directly, seeing torn writes from `atomic_write_text` mid-rename on non-atomic filesystems). The test falsifies: `assert final_count == expected` fails if any update is lost to last-writer-wins or torn reads.

Deliverable falsifier: `pytest tests/store_io_race.py -v --count=100` must pass; if it fails, the locking protocol is insufficient for the claimed serialization.
