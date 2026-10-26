"""48 GB worktree byte-class accounting — parent seat, wave 2.

Lane 1's walker crashed on a `\\\\.\\nul` device path (Windows reserved device
name; `os.path.relpath` raises ValueError across mounts). This version skips
device paths and reserved names, and streams results to a TSV so a timeout
does not lose the work.

Classes reported:
  tracked      - git-tracked files (the only class git can restore)
  tape         - untracked append-only ledgers/receipts (fleet DNA: durable)
  cache        - .mimosa snapshot cache + regenerable derived data
  unknown      - everything else untracked

Run: .venv/Scripts/python.exe memory/audit_20260926/disk_classes.py
"""
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".pytest_cache",
             ".mypy_cache", ".ruff_cache"}
RESERVED = {"nul", "con", "prn", "aux", "com1", "com2", "lpt1", "lpt2"}
BIG = 50 * 1024 * 1024  # 50 MB


def bad(p: Path) -> bool:
    """Windows device names and UNC-ish paths break relpath/stat."""
    if p.name.lower().split(".")[0] in RESERVED:
        return True
    s = str(p)
    return s.startswith("\\\\.\\") or s.startswith("\\\\?\\")


def walk(root: Path):
    for dp, dn, fn in os.walk(root, onerror=lambda e: None):
        d = Path(dp)
        dn[:] = [x for x in dn if x not in SKIP_DIRS and x.lower() not in RESERVED]
        for f in fn:
            if f.lower().split(".")[0] in RESERVED:
                continue
            p = d / f
            if bad(p):
                continue
            try:
                st = p.stat()
            except (OSError, ValueError):
                continue
            try:
                rel = str(p.relative_to(root)).replace(os.sep, "/")
            except ValueError:
                rel = str(p).replace(os.sep, "/")
            yield rel, st.st_size


def main():
    # git-tracked set (fast, one call)
    print("building tracked set...", flush=True)
    tracked = set()
    try:
        out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z"],
                             capture_output=True, timeout=300).stdout
        tracked = {x.decode("utf-8", "replace") for x in out.split(b"\0") if x}
    except Exception as e:  # noqa: BLE001
        print("  git ls-files failed:", e)
    print(f"  tracked files: {len(tracked):,}", flush=True)

    totals = {"tracked": 0, "tape": 0, "cache": 0, "unknown": 0}
    counts = dict.fromkeys(totals, 0)
    by_top = {}
    bigfiles = []
    n = 0
    for rel, size in walk(REPO):
        n += 1
        top = rel.split("/")[0] if "/" in rel else "(root)"
        b = by_top.setdefault(top, [0, 0])
        b[0] += size
        b[1] += 1
        if size >= BIG:
            bigfiles.append((size, rel))
        if rel in tracked:
            k = "tracked"
        elif rel.startswith(".mimosa/"):
            k = "cache"
        elif rel.startswith(("watch/", "memory/", "attic/", "state/", "catalog/")) \
                and rel.endswith((".jsonl", ".md", ".json", ".enc", ".sha256")):
            k = "tape"
        else:
            k = "unknown"
        totals[k] += size
        counts[k] += 1
        if n % 200000 == 0:
            print(f"   ...{n:,} files", flush=True)

    G = 1e9
    print(f"\nwalked {n:,} files (excl .git)\n")
    print(f"{'class':10} {'files':>10} {'GB':>8}  meaning")
    mean = {"tracked": "git can restore this",
            "tape": "untracked append-only ledger/receipt",
            "cache": "regenerable snapshot cache (.mimosa)",
            "unknown": "untracked, unclassified — needs a human"}
    for k in ("tracked", "tape", "cache", "unknown"):
        print(f"{k:10} {counts[k]:>10,} {totals[k]/G:>8.2f}  {mean[k]}")
    print(f"{'TOTAL':10} {n:>10,} {sum(totals.values())/G:>8.2f}")

    print(f"\nTOP 15 DIRS BY SIZE")
    for d, (s, c) in sorted(by_top.items(), key=lambda kv: -kv[1][0])[:15]:
        print(f"  {d:22} {s/G:>7.2f} GB  {c:>9,} files")

    print(f"\nTOP 20 FILES >= 50 MB")
    for s, r in sorted(bigfiles, reverse=True)[:20]:
        print(f"  {s/1e6:>9.1f} MB  {r[:88]}")

    out = REPO / "memory" / "audit_20260926" / "disk_classes.json"
    import json
    out.write_text(json.dumps(
        {"counts": counts, "bytes": totals,
         "by_top": {k: v for k, v in sorted(by_top.items(), key=lambda kv: -kv[1][0])[:25]},
         "big_files": [{"bytes": s, "path": r} for s, r in sorted(bigfiles, reverse=True)[:40]],
         "tracked_count": len(tracked), "walked": n}, indent=1), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    sys.exit(main())
