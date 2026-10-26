"""queue-closes lane instrument: truly-invisible census (pre/post rebuild verb).

Mirrors the MASTER_MICKEY17_V2.md D2 census method: a top-level inbox file is
truly invisible when it carries ZERO register events in index_events.jsonl
(register-then-invalidate files are NOT invisible: the log saw them, and a
heal must never re-register a deliberate invalidation). Path normalization
mirrors the fold's normInboxFile (separator canon, board|app/inbox and
absolute-host-root strips, repeated inbox/ prefix strip).

Usage:
    python _qc_truly_invisible_census.py            # report only
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
INBOX = REPO / "watch" / "inbox"
EVENTS = INBOX / "index_events.jsonl"
INDEX = INBOX / "INDEX.json"
CONTROL = {"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json"}

# absolute host roots that normalize away (mirror of index_fold_host.mjs
# INBOX_ROOTS, lowercase compare)
HOST_ROOTS = [
    str(INBOX).replace("\\", "/").rstrip("/").lower(),
]


def norm(rel_path: str) -> str:
    p = str(rel_path or "").replace("\\", "/").strip()
    while p.startswith("/"):
        p = p[1:]
    while True:
        if p.lower().startswith("board/inbox/"):
            p = p[len("board/inbox/"):]
            continue
        if p.lower().startswith("app/inbox/"):
            p = p[len("app/inbox/"):]
            continue
        if p.lower().startswith("inbox/"):
            p = p[len("inbox/"):]
            continue
        break
    for root in HOST_ROOTS:
        low = p.lower()
        if low.startswith(root + "/"):
            p = p[len(root) + 1:]
            break
    while p.lower().startswith("inbox/"):
        p = p[len("inbox/"):]
    return p


def register_files() -> set[str]:
    regs: set[str] = set()
    if not EVENTS.is_file():
        return regs
    with EVENTS.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("op") == "register" and ev.get("file"):
                regs.add(norm(ev["file"]).lower())
    return regs


def active_items() -> set[str]:
    if not INDEX.is_file():
        return set()
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    out = set()
    for it in idx.get("items", []):
        if isinstance(it, dict) and it.get("path"):
            out.add(norm(str(it["path"])))
    return out


def main() -> int:
    regs = register_files()
    active = active_items()
    top = sorted(
        p.name for p in INBOX.iterdir() if p.is_file() and p.name not in CONTROL
    )
    invisible = [n for n in top if n.lower() not in regs]
    recursive = sorted(
        str(p.relative_to(INBOX)).replace("\\", "/")
        for p in INBOX.rglob("*")
        if p.is_file()
    )
    rec_invisible = [
        r for r in recursive
        if r.lower() not in regs and r not in active and Path(r).name not in CONTROL
    ]
    print(f"log registers (distinct files): {len(regs)}")
    print(f"active INDEX items: {len(active)}")
    print(f"top-level non-control files: {len(top)}")
    print(f"truly-invisible top-level: {len(invisible)}")
    for n in invisible:
        print(f"  INVISIBLE {n}")
    print(f"recursive files: {len(recursive)}")
    print(f"recursive non-registered (informational): {len(rec_invisible)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
