# PA-S5stores-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

**Audit of `00__store_io.py`**

**(1) Lock-class bugs**

- **Reader starvation / torn reads on POSIX:** `atomic_write_text` uses `os.replace` (line ~"os.replace(tmp_name, path)"), which is atomic; readers never see partial. But readers are *not* under `exclusive()`. A reader using plain `open(path).read()` on Windows can race `os.replace` and must retry (the code admits this in the docstring and retries the *writer*, not the reader). No reader-side lock means a reader can still fail with `PermissionError` on NTFS. **Gap: no `shared()` reader entry point.**
- **Crash-with-lock:** POSIX `flock` releases on fd close (process death). Windows `msvcrt.locking` byte lock is also released on handle close. OK. But `_THREAD_LOCKS` grows unbounded (line `_THREAD_LOCKS[key] = lock`) - a leak, not a correctness bug.
- **Lock ordering:** only one lock acquired per call, no nesting. No deadlock ordering issue. `_THREAD_LOCKS_GUARD` is held briefly. Fine.
- **NFS:** `flock` on NFS is advisory and historically racy; the docstring claims cross-process safety but doesn't scope out NFS. `_ALLOWED_ROOTS` refuses non-temp non-repo paths, which incidentally blocks remote shares - so NFS is *excluded by policy*, but the comment doesn't say so; UNVERIFIED against an actual NFS mount.
- **WSL:** `/mnt/c` is 9p/drvfs; `flock` semantics are known-imperfect and `os.replace` atomicity across the 9p boundary is not guaranteed. Temp dir on WSL is `/tmp` (drvfs? no, ext4) so probably fine, but the store path in the repo tree under `/mnt/c/...` is not.
- **Real bug:** the `time.sleep(0.01)` busy-wait under `tlock` holds the *thread* RLock while waiting for the *byte* lock. Two threads in the same process serialize correctly, but the inner retry loop blocks the thread. Contrast: not a correctness hole.

**(2) `os.replace` on NTFS**

Yes, `os.replace` maps to `MoveFileEx(..., MOVEFILE_REPLACE_EXISTING)`, atomic for same-volume renames. `mkstemp(dir=path.parent)` guarantees same volume. **Caveat:** if `path` is opened by another handle with `FILE_SHARE_DELETE` absent (the default for Python `open`), the replace fails with `PermissionError` - hence the retry loop. If a reader holds the handle >5s (e.g., a hung reader, antivirus scan), the writer raises after `_REPLACE_TIMEOUT_S`. That is a **liveness** failure, not corruption, but it means a slow reader can DOS writers. Falsifier: hold `open(path,'rb')` in another process for 10s, call `atomic_write_text`, observe `PermissionError`.

**(3) The one test**

```
def test_slow_reader_does_not_block_writer(tmp_path):
    p = tmp_path/"s.json"; p.write_text("{}")
    reader = subprocess.Popen([sys.executable,"-c",
        f"import time;f=open({str(p)!r},'rb');time.sleep(8)"])
    time.sleep(0.5)
    t0=time.monotonic()
    with pytest.raises(TimeoutError):
        # writer starves on NTFS
        ...
```

Simpler and sharpest: **two threads, one holds the byte lock and calls `os._exit(0)` from a child process; assert the parent can reacquire within 1s** (crash-with-lock). And **two writer threads through `exclusive()` each doing read-modify-write 100x; assert final count == 200** (the Q21 regression, at the API level, not the store level).

Deliverable falsifier: if a seat applies this test and it passes against the pre-fix code (whole-file save, no lock), the test is wrong.
