"""Purge pass for the exec forest - 2026-10-09, operator GO.

One walk, two kill classes (the CLEAN_RUNBOOK P1+P2 combined to keep the
one-disk-process-at-a-time bound):
  A) giant-junk: size > 1GiB AND first 2KB matches the measured junk signature
     (full-disk find dump: starts with b'/c\\n'; or FINDSTR error loop)
  B) aged: mtime older than RETENTION_DAYS (7)

Modes: --dry prints classes + top list, deletes nothing. --apply deletes and
writes the receipt. Containment guards identical to harvest_exec_forest.py
(safe_child/safe_dir; the only join is inside safe_child). Files that fail to
delete (e.g. locked by a live seat) are counted and listed, never fatal.
"""
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

EXEC_ROOT = Path(r"C:\Users\foste\.zcode\cli\exec")
OUT_DIR = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\disk_audit_20261009\cleanup")
RETENTION_DAYS = 7
GIANT_BYTES = 2**30            # 1 GiB
NOW = time.time()

def safe_child(dirpath: Path, name: str, allowroot: Path):
    if name in ("", ".", "..") or "/" in name or "\\" in name:
        return None
    p = dirpath / name
    try:
        if not p.resolve().is_relative_to(allowroot.resolve()):
            return None
    except OSError:
        return None
    return p

def safe_dir(dirpath: Path, allowroot: Path) -> bool:
    try:
        return dirpath.resolve().is_relative_to(allowroot.resolve())
    except OSError:
        return False

def junk_signature(head: bytes) -> str:
    if head.startswith(b"/c\n") or head.startswith(b"/c\r\n"):
        return "find-dump"
    if b"FINDSTR: Cannot open" in head:
        return "findstr-loop"
    return ""

def main():
    apply = "--apply" in sys.argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    kill = []          # (path, size, cls)
    nfiles = nbytes = errors = 0
    for dirpath, _dn, fns in os.walk(EXEC_ROOT):
        dpath = Path(dirpath)
        if not safe_dir(dpath, EXEC_ROOT):
            continue
        for fn in fns:
            nfiles += 1
            p = safe_child(dpath, fn, EXEC_ROOT)
            if p is None:
                errors += 1
                continue
            try:
                st = p.stat()
            except OSError:
                errors += 1
                continue
            nbytes += st.st_size
            cls = ""
            if st.st_size > GIANT_BYTES:
                try:
                    with open(p, "rb") as f:
                        head = f.read(2048)
                    sig = junk_signature(head)
                    if sig:
                        cls = f"giant-{sig}"
                except OSError:
                    pass
            if not cls and (NOW - st.st_mtime) > RETENTION_DAYS * 86400:
                cls = "aged-7d"
            if cls:
                kill.append((str(p), st.st_size, cls))
    gbytes = sum(s for _, s, c in kill if c.startswith("giant"))
    abytes = sum(s for _, s, c in kill if c == "aged-7d")
    print(f"scanned {nfiles} files {nbytes/2**30:.2f}GiB errors {errors}")
    print(f"KILL LIST: giant-junk {sum(1 for c in (c for _,_,c in kill if c.startswith('giant')))} files {gbytes/2**30:.2f}GiB | aged-7d {sum(1 for _,_,c in kill if c=='aged-7d')} files {abytes/2**30:.2f}GiB | total {(gbytes+abytes)/2**30:.2f}GiB")
    for pth, s, c in sorted(kill, key=lambda k: -k[1])[:20]:
        print(f"  {s/2**30:7.2f}GiB {c:14s} {Path(pth).name[:70]}")
    if not apply:
        print("DRY RUN - nothing deleted. Re-run with --apply.")
        return
    deleted = failed = 0
    freed = 0
    fail_list = []
    for pth, s, c in kill:
        try:
            os.remove(pth)
            deleted += 1
            freed += s
        except OSError:
            failed += 1
            fail_list.append(pth)
    ts = datetime.now(timezone.utc).isoformat()
    receipt = {"ts": ts, "mode": "apply", "scanned_files": nfiles, "scanned_bytes": nbytes,
               "killed_giant_bytes": gbytes, "killed_aged_bytes": abytes,
               "deleted": deleted, "freed_bytes": freed, "failed": failed,
               "fail_list": fail_list[:50]}
    out = safe_child(OUT_DIR, "PURGE_RECEIPT.json", OUT_DIR)
    if out is None:
        raise SystemExit("receipt path containment failed")
    out.write_text(json.dumps(receipt, indent=1))
    print(f"APPLIED: deleted {deleted} files, freed {freed/2**30:.2f}GiB, failed {failed}")
    print("receipt:", out)

if __name__ == "__main__":
    main()
