# PA-S5stores-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

### Deliverable: Concurrency Vulnerability Patch / Design Spec

**Context Assumptions:**
*   **Instrument:** `server/store_io.py` (L1-L78).
*   **Moment:** Read-Modify-Write operations protecting user account state via file system locking and atomic renaming.
*   **Assumptions:** Process crashes are instantaneous relative to atomic operations. Network connectivity remains stable (i.e., no partition during `os.replace`).

**Falsifier:**
The system fails if a reader thread observes the state *after* the `fsync` (L82) but *before* the `os.replace` (L101) successfully completes, coupled with an external process that deletes the *original* target path (Path) just before the rename.

---

#### (1) Remaining Lock Class Bugs

**a. Lock Ordering and Deadlock:**
The pattern `exclusive(path)` (L63) acquires a per-path `RLock` (`tlock`) and then an OS byte lock (`_lock_byte` or `fcntl.flock`).
*   **Bug:** Attempting an operation that requires locks on `path_A` and then `path_B` without consistent ordering is vulnerable. If two threads require `A` then `B`, and a third requires `B` then `A`, a deadlock is possible.
*   **Mitigation:** The current API requires the caller to ensure lock order externally. A helper function that acquires a map of required paths and sorts them lexicographically before acquiring the locks would be necessary to enforce lock order.

**b. Crash-with-Lock:**
The `exclusive` context manager handles the release of the OS byte lock in the `finally` block (L73).
*   **Verdict:** When the process crashes *after* acquiring the OS lock but *before* entering the `with tlock:` block, the physical file handle (`fh`) is never explicitly released. This can leave the lock byte file handle in a potentially indeterminate state, although the `finally` block's attempt to run `_unlock_byte(fh)` attempts to clean it up. If the system exits abnormally (e.g., SIGKILL) *right* after `_lock_byte(fh)` succeeds, the OS might clean up the lock, but the resource management relies heavily on the `try/finally` structure, which is insufficient for process termination signals.

**c. Reader Starvation:**
*   **Verdict:** The current design (L101), where `atomic_write_text` retries on `PermissionError` (a common race condition indicator, especially in Windows using `os.replace`), is susceptible to livelock/starvation if a dedicated, high-frequency stream of minor writes constantly delays the replacement, forcing the writer into endless exponential backoff near the timeout. This affects the writer, not the reader, but a persistent failure here could be interpreted as starvation.

**d. NFS/WSL Semantics:**
*   **Verdict:** Reliance on `fcntl.flock` (POSIX, L30) assumes strict POSIX file locking behavior. NFS implementations often treat `flock` poorly or inconsistently across different clients. The byte-level locking implemented via `msvcrt.locking` (Windows, L18) is generally more guaranteed but non-portable. The codebase lacks abstraction for these semantic differences, making cross-platform transactional guarantees suspect outside highly controlled networking environments.

#### (2) os.replace Atomicity on Windows NTFS

**Verdict:** The atomicity of the rename operation `os.replace` (L101) is generally maintained in NTFS even when a lockless reader holds the old file handle.
*   **Evidence:** The atomic swap relies on the OS guaranteeing that renaming a file (the target `path`) from a new name (`tmp_name`) makes the new content instantly visible, while simultaneously ensuring that other concurrently reading processes cannot observe a partial write. Since the writer explicitly calls `os.fsync(fh.fileno())` (L82) *before* the rename, the data integrity is guaranteed when the rename completes.
*   **Caveat:** The exception path handles `PermissionError` (L102). While this is done because Windows handles might briefly block the rename, the core atomicity premise (Read *always* gets old bytes, Write *always* gets new bytes) is maintained by the OS guarantee of `os.replace` being a single atomic transaction.

#### (3) The Worst Remaining Hole Test

**Test:** Concurrent Writer Race on Initial Lock Acquisition and State Corruption.

**Setup:** Two processes, $P_1$ and $P_2$, attempt to modify the same file path $P$:
1.  $P_1$ starts `exclusive(P)`.
2.  $P_2$ starts `exclusive(P)`.
3.  $P_1$ acquires the thread lock $tlock$ (L69) and succeeds in acquiring the OS lock $os\_lock$ (L70).
4.  $P_1$ performs its read-modify-write sequence, succeeds, and yields.
5.  $P_1$ exits the `with exclusive(P)` block, releasing the $os\_lock$ (L73).
6.  **Critical Race:** $P_2$ is blocked on OS lock acquisition. Due to a system-level scheduling hiccup, $P_2$ loses the OS lock acquisition, but *before* $P_2$ can re-acquire it, a third process $P_3$ performs unrelated write/cleanup activity on the directory structure of $P$.
7.  $P_1$ is delayed exiting the function. $P_2$ eventually acquires the lock *after* $P_3$'s activity and proceeds.

**Vulnerability Focus:** The sequence assumes the state of the directory structure and the existence of the lock-file (L68) are stable. If the lock-file or the directory is modified or deleted by an external process ($P_3$) while a process is attempting to maintain atomicity across multiple operations (e.g., creating the lock file, or the subsequent `os.replace`), the `_validated` function (L41) might fail unnecessarily, or worse, the lock file operation might silently revert to an insecure state outside the intent of the API.

---

**Landable Deliverable: Defensive Locking Patch (spec)**

Implement a `try_with_validated_lock` context manager wrapping `exclusive`. This patch explicitly checks the file system state relative to the lock file's parent directory and performs a quick, read-only check of the target file's existence *under* the established OS lock. If the target file is missing, the operation should fail immediately with a specific `FileMustExistError`, preventing an attacker from using absence of state as a signal to bypass the lock, or preventing corrupted state recovery.

**Falsifier:**
The patch is vulnerable if the filesystem provider allows a successful operation (e.g., read) on the path $P$ *after* acquiring the lock $os\_lock$, but *before* the `try_with_validated_lock` check runs, due to a high-frequency metadata update from an external process $P_3$ changing the path's actual inode content.
