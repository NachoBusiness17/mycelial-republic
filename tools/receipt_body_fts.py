#!/usr/bin/env python3
r"""receipt_body_fts -- full-text index over watch/inbox receipt BODIES (Q4, 2026-09-27).

The catalog FTS (catalog/catalog_fts.sqlite) indexes only path + title, so the
105 burn receipts and the rest of the intake zone (10,331 cataloged files,
2,084 md/txt bodies, 22.3 MB) were findable by name but not by content: a seat
searching "weeping-angel" or "PROBE-C" got nothing unless the word sat in a
title. This was fix-queue Q4 from the atlas self-steal
(watch/inbox/ATLAS_SELF_STEAL_20260927.md): the biggest retrieval unlock.

Shape (self-steal from tools/corpus_fts_rebuild.py, the B2-22 spike heir):
  external-content FTS5 over a rows table carrying the body text;
  atomic tmp-then-replace build; meta table holding build stats;
  --check compares a fresh walk's stats against meta (exit 0 fresh,
  exit 2 stale, mirroring the catalog FTS freshness contract);
  stdlib only.

Commands:
  .venv/Scripts/python.exe tools/receipt_body_fts.py build
  .venv/Scripts/python.exe tools/receipt_body_fts.py check
  .venv/Scripts/python.exe tools/receipt_body_fts.py query "terms here" [--limit 10]
  from tools.receipt_body_fts import search_receipt_bodies
      rows = search_receipt_bodies("weeping-angel", limit=5)

Scope: watch/inbox .md/.txt bodies only (receipts + filings). JSON/JSONL
ledgers stay out: they are row-addressed surfaces with their own gates, not
prose to reread. Machinery dirs are pruned. Files over 2 MB are indexed from
their first 2 MB (no known receipt exceeds this; the cap bounds pathological
strays).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO / "watch" / "inbox"
DB_PATH = REPO / "catalog" / "receipt_fts.sqlite"
TEXT_EXTS = {".md", ".txt"}
MAX_BODY_BYTES = 2_000_000
PRUNE_DIRS = {".git", "node_modules", "__pycache__", ".mimosa", ".venv"}


def _now_z() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _walk_files() -> list[Path]:
    out: list[Path] = []
    for dp, dns, fns in os.walk(SOURCE_ROOT):
        dns[:] = [d for d in dns if d not in PRUNE_DIRS]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                out.append(Path(dp) / fn)
    out.sort()
    return out


def _title_of(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        return re.sub(r"^#+\s*", "", s)[:120]
    return ""


def _read_body(p: Path) -> str:
    with p.open("r", encoding="utf-8", errors="replace") as f:
        return f.read(MAX_BODY_BYTES)


def _walk_stats() -> dict:
    files = _walk_files()
    total = 0
    max_mtime = 0.0
    for p in files:
        st = p.stat()
        total += st.st_size
        max_mtime = max(max_mtime, st.st_mtime)
    return {"files": len(files), "bytes": total,
            "max_mtime": _dt.datetime.fromtimestamp(
                max_mtime, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


def build() -> dict:
    files = _walk_files()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(DB_PATH.parent), suffix=".receipt_fts.tmp")
    os.close(fd)
    os.unlink(tmp)
    con = sqlite3.connect(tmp)
    try:
        con.executescript(
            "CREATE TABLE rrows(rowid INTEGER PRIMARY KEY, relpath TEXT, "
            "mtime TEXT, bytes INTEGER, title TEXT, body TEXT);\n"
            "CREATE VIRTUAL TABLE receipts USING fts5(relpath, title, body, "
            "content='rrows', content_rowid='rowid');\n"
            "CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);\n")
        batch = []
        for p in files:
            rel = str(p.relative_to(REPO)).replace("\\", "/")
            body = _read_body(p)
            st = p.stat()
            batch.append((rel,
                          _dt.datetime.fromtimestamp(
                              st.st_mtime, _dt.timezone.utc).strftime(
                                  "%Y-%m-%dT%H:%M:%SZ"),
                          st.st_size, _title_of(body), body))
            if len(batch) >= 500:
                con.executemany("INSERT INTO rrows(relpath, mtime, bytes, title, body) "
                                "VALUES (?,?,?,?,?)", batch)
                batch = []
        if batch:
            con.executemany("INSERT INTO rrows(relpath, mtime, bytes, title, body) "
                            "VALUES (?,?,?,?,?)", batch)
        con.execute("INSERT INTO receipts(receipts) VALUES('rebuild')")
        meta = {"built_at": _now_z(), "source_root": "watch/inbox",
                "files": str(len(files))}
        con.executemany("INSERT INTO meta(key, value) VALUES (?, ?)",
                        list(meta.items()))
        con.commit()
    finally:
        con.close()
    os.replace(tmp, DB_PATH)
    return {"ok": True, "built": meta["built_at"], "files": len(files),
            "db": str(DB_PATH), "db_bytes": os.path.getsize(DB_PATH)}


def check() -> tuple[int, str]:
    if not DB_PATH.is_file():
        return 2, "no index on disk; run build"
    con = sqlite3.connect(str(DB_PATH))
    try:
        meta = dict(con.execute("SELECT key, value FROM meta").fetchall())
    finally:
        con.close()
    stats = _walk_stats()
    if str(stats["files"]) != meta.get("files"):
        return 2, (f"stale: walk sees {stats['files']} files, index holds "
                   f"{meta.get('files')} (built {meta.get('built_at')})")
    if stats["max_mtime"] > meta.get("built_at", ""):
        return 2, (f"stale: newest body mtime {stats['max_mtime']} is newer than "
                   f"build {meta.get('built_at')}")
    return 0, f"fresh: {stats['files']} files, built {meta.get('built_at')}"


def search_receipt_bodies(query: str, limit: int = 10) -> list[dict]:
    """FTS5 MATCH over receipt bodies; returns relpath, title, mtime, snippet."""
    if not DB_PATH.is_file():
        raise RuntimeError("receipt body index missing; run "
                           "tools/receipt_body_fts.py build")
    expr = " ".join(f'"{t}"' for t in query.split() if t.strip())
    con = sqlite3.connect(str(DB_PATH))
    try:
        rows = con.execute(
            "SELECT r.relpath, r.title, r.mtime, snippet(receipts, 2, '«', '»', '…', 24) "
            "FROM receipts JOIN rrows r ON r.rowid = receipts.rowid "
            "WHERE receipts MATCH ? ORDER BY rank LIMIT ?",
            (expr, limit)).fetchall()
    finally:
        con.close()
    return [{"relpath": r[0], "title": r[1], "mtime": r[2], "snippet": r[3]}
            for r in rows]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="receipt_body_fts",
                                 description="FTS5 over watch/inbox md/txt bodies")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="walk watch/inbox, (re)build the body index")
    sub.add_parser("check", help="freshness gate: exit 0 fresh, 2 stale")
    q = sub.add_parser("query", help="FTS5 MATCH over bodies")
    q.add_argument("terms")
    q.add_argument("--limit", type=int, default=10)
    args = ap.parse_args(argv)

    if args.cmd == "build":
        print(json.dumps(build(), ensure_ascii=False))
        return 0
    if args.cmd == "check":
        code, note = check()
        print(json.dumps({"state": "fresh" if code == 0 else "stale", "note": note}))
        return code
    rows = search_receipt_bodies(args.terms, args.limit)
    for r in rows:
        print(f"{r['relpath']}  ({r['mtime']})")
        print(f"  title: {r['title']}")
        print(f"  {r['snippet']}")
    print(f"-- {len(rows)} hit(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
