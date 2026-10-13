"""corpus_fts_rebuild -- the one sanctioned writer for catalog/catalog_fts.sqlite.

tools/corpus.py is read-only by law ("nothing here writes"), so the FTS5
index its corpus_search prefers gets its own rebuild entry point. This module
is that entry point (B2-102, 2026-09-26; builds the exact shape the B2-22
spike measured, watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md
and B2_22_fts5_spike.py: external-content fts5 `corpus` over a `crows` row
table, rowid = catalog line order). Measured over the Sep-18 map (757,667
rows, 214,470,472 bytes): 12.35s build, 217,686,016 db bytes.

The meta table this build writes is the freshness contract corpus_search
gates on: catalog_bytes and catalog_mtime_utc record what the index was
built over, so a stale index is detected by bytes even when a restore or a
touch lies with mtimes. catalog_sha256 is recorded for the --deep check;
the per-search gate stays cheap (bytes + mtime), the hash is the audit tier.

Usage:
    .venv/Scripts/python.exe tools/corpus_fts_rebuild.py            rebuild
    .venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check    gate state only, no write
    .venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep
                                                                    + sha256 verify

Exit codes for --check follow the freshness house pattern (0 fresh, 2
otherwise). The rebuild itself builds into catalog_fts.sqlite.tmp and
os.replace()s it into place, so a crashed build never leaves a half index
and a concurrent mode=ro reader keeps serving the old file.
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def _load_corpus():
    """Hermetic single-source load of the read-only surface: the freshness
    gate lives in tools/corpus.py and this tool reuses it rather than keeping
    a second copy of the rule."""
    spec = importlib.util.spec_from_file_location("corpus_readonly", HERE / "corpus.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_index(catalog_path: Path, db_path: Path) -> dict:
    """Build the external-content FTS5 index (+ meta) into tmp, then replace.
    Read-only over the catalog; the tmp db and the final replace are this
    module's only writes."""
    catalog_path = Path(catalog_path)
    db_path = Path(db_path)
    tmp_path = db_path.with_name(db_path.name + ".tmp")
    if tmp_path.exists():
        tmp_path.unlink()
    con = sqlite3.connect(str(tmp_path))
    con.executescript(
        "PRAGMA journal_mode=OFF;\n"
        "PRAGMA synchronous=OFF;\n"
        "CREATE TABLE crows(rowid INTEGER PRIMARY KEY, id TEXT, path TEXT,"
        " bytes INTEGER, mtime TEXT, zone TEXT, ext TEXT, title TEXT);\n"
        "CREATE VIRTUAL TABLE corpus USING fts5(path, title,"
        " content='crows', content_rowid='rowid');\n"
        "CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);\n")
    rows = 0
    malformed = 0
    batch = []
    t0 = time.perf_counter()
    with open(catalog_path, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            batch.append((r.get("id"), r.get("path"), r.get("bytes"),
                          r.get("mtime"), r.get("zone"), r.get("ext"),
                          r.get("title")))
            rows += 1
            if len(batch) >= 50000:
                con.executemany("INSERT INTO crows VALUES (NULL,?,?,?,?,?,?,?)", batch)
                batch = []
    if batch:
        con.executemany("INSERT INTO crows VALUES (NULL,?,?,?,?,?,?,?)", batch)
    con.commit()
    t1 = time.perf_counter()
    con.execute("INSERT INTO corpus(corpus) VALUES('rebuild')")
    t2 = time.perf_counter()
    sha = _sha256_file(catalog_path)
    con.executemany(
        "INSERT INTO meta(key, value) VALUES (?, ?)",
        [("catalog_bytes", str(catalog_path.stat().st_size)),
         ("catalog_sha256", sha),
         ("catalog_mtime_utc", datetime.datetime.utcfromtimestamp(
             catalog_path.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")),
         ("rows_indexed", str(rows)),
         ("built_utc", datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
         ("builder", "tools/corpus_fts_rebuild.py (B2-102, shape of B2-22 spike)")])
    con.commit()
    db_bytes = tmp_path.stat().st_size
    con.close()
    os.replace(str(tmp_path), str(db_path))
    return {"rows_indexed": rows, "malformed_lines": malformed,
            "rows_table_s": round(t1 - t0, 3), "fts_rebuild_s": round(t2 - t1, 3),
            "total_build_s": round(t2 - t0, 3), "db_bytes": db_bytes,
            "catalog_bytes": catalog_path.stat().st_size,
            "catalog_sha256": sha,
            "db": str(db_path)}


def check(deep: bool = False) -> dict:
    """Report the freshness gate corpus_search will apply, without writing.
    deep adds the sha256 verify against meta.catalog_sha256 (the audit tier
    the cheap per-search gate skips)."""
    corpus = _load_corpus()
    state, note = corpus._fts_state()
    out = {"db": str(corpus.FTS_DB), "index_state": state, "note": note,
           "catalog": str(corpus.CATALOG)}
    if state == "fresh" and deep:
        if not corpus.FTS_DB.exists():
            out["deep"] = "refused: no index"
            out["index_state"] = "absent"
            return out
        meta = None
        try:
            con = sqlite3.connect(
                "file:%s?mode=ro" % corpus.FTS_DB.as_posix(), uri=True)
            try:
                meta = dict(con.execute("SELECT key, value FROM meta"))
            finally:
                con.close()
        except sqlite3.Error as e:
            out["deep"] = ("no meta table (spike-era build): nothing to "
                           "audit; run a rebuild for the byte contract"
                           if "no such table" in str(e)
                           else "unreadable meta: %s" % e)
            return out
        sha = _sha256_file(corpus.CATALOG)
        out["catalog_sha256"] = sha
        out["deep"] = ("match" if meta.get("catalog_sha256") == sha
                       else "MISMATCH: catalog bytes moved past meta; run a rebuild")
        if out["deep"] != "match":
            out["index_state"] = "stale"
    return out


def main() -> int:
    argv = [a for a in sys.argv[1:]]
    deep = "--deep" in argv
    if "--check" in argv:
        out = check(deep=deep)
        print(json.dumps(out, indent=1))
        return 0 if out["index_state"] == "fresh" else 2
    corpus = _load_corpus()
    stats = build_index(corpus.CATALOG, corpus.FTS_DB)
    print(json.dumps(stats))
    state, note = corpus._fts_state()
    print(json.dumps({"index_state": state, "note": note}))
    return 0 if state == "fresh" else 1


if __name__ == "__main__":
    sys.exit(main())
