# T1W2_S5_stores (anthropic/claude-opus-5.5, turn 1, channel: content)

# STRANGER AUDIT: server/store_io.py

**Conditions.** Line numbers come from a hand count of the pasted EVIDENCE block, assuming it begins at file line 1. Nothing was executed. Claims about OS semantics are marked UNVERIFIED.

## (1) Remaining lock-class bugs

**A. Re-entry self-deadlock (worst).**
- The RLock at :113 lets the same thread re-enter.
- :114 then opens a *second* handle (`open(lock_file, "a+b")`) and locks it again.
- On POSIX, `flock` belongs to the open file description, so the second `LOCK_EX` at :60 blocks on our own first handle.
- On Windows, `msvcrt.locking` locks are per handle, so the loop at :47-50 spins forever.
- Positive: two sequential `with exclusive(p)` blocks work.
- Negative: `with exclusive(p): with exclusive(p):` hangs. (OS semantics UNVERIFIED.)

**B. The timeout is dead code on both platforms.**
- The Windows `_lock_byte` swallows `OSError` and loops internally (:49-50), so it never returns to the deadline check at :119-123.
- On POSIX, `LOCK_EX` without `LOCK_NB` (:60) blocks in the kernel.
- Result: a hung (not dead) holder stalls every waiter forever, and all same-process threads queue behind `tlock` (:113).

**C. No lock ordering.**
- Nested `exclusive(a)` then `exclusive(b)` against another caller doing `b` then `a` deadlocks (:113-117).
- No canonical order is enforced, and because of B no timeout rescues it.

**D. Crash while holding the lock.**
- A dead process loses its OS locks, so that case is fine (UNVERIFIED, OS behavior).
- A crash between write and replace leaves a `.tmp-*` file. The cleanup at :157-161 only runs in-process.

**E. Writer starvation by readers (Windows).**
- Readers take no lock. Each open handle can make `os.replace` fail.
- After 5 s the write raises (:153-155) after the mutation was already computed. The write fails loudly rather than being lost silently.

**F. NFS and WSL.**
- The allowlist (:72-73) still admits a repo that lives on NFS or on `/mnt/c` under WSL.
- `flock` from WSL and `msvcrt.locking` from Windows do not see each other, so there is no cross-OS serialization (UNVERIFIED).

## (2) Is os.replace atomic on NTFS?

**Verdict: visibility-atomic under conditions** (UNVERIFIED, no probe).

Conditions:
- The temp file and target are on the same local NTFS volume. mkstemp in `path.parent` (:142) guarantees the same directory.
- No foreign handle holds the target without `FILE_SHARE_DELETE`. That case raises `PermissionError`, which the retry at :153 handles.

Not guaranteed:
- Durability after power loss, because there is no directory fsync (:27-28).
- Success while antivirus or the search indexer holds the file. Those handles can outlast the 5 s budget (:68).

## (3) The one test

```python
def test_exclusive_reentry_does_not_hang(tmp_path):
    p = tmp_path / "users.json"
    done = threading.Event()
    def body():
        with exclusive(p):
            with exclusive(p):
                done.set()
    t = threading.Thread(target=body, daemon=True)
    t.start()
    t.join(timeout=5)
    assert done.is_set(), "re-entrant exclusive() self-deadlocked"
```

**Patch direction:**
- Hold a per-path reentrancy counter beside the RLock, and take the OS lock only on depth 0.
- Use `LK_NBLCK` and `LOCK_EX|LOCK_NB` inside the deadline loop.

**Falsifier:** if this test passes unmodified on both win32 and Linux against the current code, findings A and B are wrong.
