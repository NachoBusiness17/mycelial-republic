"""B2_22_fts5_spike -- UF-120 corpus FTS5 spike (2026-09-26, lane B2-22).

Builds an external-content SQLite FTS5 index over catalog/catalog.jsonl and
measures per-query latency of the production substring scan
(tools/corpus.py corpus_search, the real tool path) against FTS5 on 10 real
queries verified against the current map this session.

Facts this script trusts (verified from bytes 2026-09-26):
  - current map: 757,667 rows, 214,470,472 bytes, built 2026-09-18 by the
    inline v3 walk (the 947K figure in the brief is the Sep-16 v2 snapshot)
  - row schema: {id, path, bytes, mtime, zone, ext, title, age_days}
  - UF-120 ask + numbers: watch/inbox/union_fullsend_20260917/queue.jsonl:120
    (full-file substring scan measured 3.5s; FTS5 predicted 30-80ms)

The db written (catalog/catalog_fts.sqlite) is derived data, rebuildable by
rerunning this script. Read-only over the catalog. Run with
.venv/Scripts/python.exe from anywhere; REPO derives from __file__.
"""
import datetime
import importlib.util
import json
import os
import sqlite3
import statistics
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CATALOG = os.path.join(REPO, "catalog", "catalog.jsonl")
DB = os.path.join(REPO, "catalog", "catalog_fts.sqlite")
RESULTS = os.path.join(HERE, "B2_22_fts5_results.json")

# 10 real queries, each probed against the current map this session before
# selection (hit-count class mix: wide early-break, partial, full-scan, zero).
QUERIES = [
    "verkle",         # wide (1140 substring hits): scan early-breaks at limit
    "hermes",         # wide (914)
    "corpus",         # very wide (65,628)
    "falsifier",      # partial (69): scan breaks somewhere mid-file
    "grounding",      # partial-ish (410)
    "garden",         # narrow (17): forces full scan
    "referee",        # narrow (4): full scan
    "ruins_go",       # narrow (4): full scan; the C6 freshness demo term
    "adventure_2d6",  # narrow (1): full scan; exercises phrase translation
    "qdrop",          # zero (0): full scan; the honest worst case
]


def fts_expr(q: str) -> str:
    """Substring-AND -> FTS5: each whitespace term becomes a quoted prefix
    phrase (underscore splits into adjacent tokens under unicode61), ANDed."""
    return " AND ".join('"%s"*' % t.replace('"', '""') for t in q.split())


def load_tool():
    """Load tools/corpus.py directly (hermetic, no tools/__init__ side effects)."""
    spec = importlib.util.spec_from_file_location(
        "b2_22_corpus", os.path.join(REPO, "tools", "corpus.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_index():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript(
        "PRAGMA journal_mode=OFF;\n"
        "PRAGMA synchronous=OFF;\n"
        "CREATE TABLE crows(rowid INTEGER PRIMARY KEY, id TEXT, path TEXT,"
        " bytes INTEGER, mtime TEXT, zone TEXT, ext TEXT, title TEXT);\n"
        "CREATE VIRTUAL TABLE corpus USING fts5(path, title,"
        " content='crows', content_rowid='rowid');\n")
    rows = 0
    malformed = 0
    batch = []
    t0 = time.perf_counter()
    with open(CATALOG, encoding="utf-8") as fh:
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
                con.executemany("INSERT INTO crows VALUES (NULL,?,?,?,?,?,?,?)",
                                batch)
                batch = []
    if batch:
        con.executemany("INSERT INTO crows VALUES (NULL,?,?,?,?,?,?,?)", batch)
    con.commit()
    t1 = time.perf_counter()
    con.execute("INSERT INTO corpus(corpus) VALUES('rebuild')")
    con.commit()
    t2 = time.perf_counter()
    page_count = con.execute("PRAGMA page_count").fetchone()[0]
    page_size = con.execute("PRAGMA page_size").fetchone()[0]
    con.close()
    return {
        "rows_indexed": rows,
        "malformed_lines": malformed,
        "rows_table_s": round(t1 - t0, 3),
        "fts_rebuild_s": round(t2 - t1, 3),
        "total_build_s": round(t2 - t0, 3),
        "db_bytes": os.path.getsize(DB),
        "db_pages": page_count,
        "db_page_size": page_size,
        "db_bytes_human_mb": round(os.path.getsize(DB) / 1048576, 1),
    }


def reference_counts(con):
    """One full pass: true substring-AND hit counts per query (parity column)."""
    ref = {q: 0 for q in QUERIES}
    terms = {q: [t for t in q.lower().split() if t] for q in QUERIES}
    with open(CATALOG, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            hay = (str(r.get("path", "")) + "\n" + str(r.get("title", ""))).lower()
            for q in QUERIES:
                if all(t in hay for t in terms[q]):
                    ref[q] += 1
    return ref


def main():
    out = {"ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "catalog_bytes": os.path.getsize(CATALOG),
           "sqlite_version": sqlite3.sqlite_version}
    print("[1/4] building external-content FTS5 index over", CATALOG)
    out["build"] = build_index()
    print(json.dumps(out["build"]))

    con = sqlite3.connect(DB)
    tool = load_tool()

    print("[2/4] reference substring counts (one full pass)")
    out["reference_substring_counts"] = reference_counts(con)

    print("[3/4] baseline: production corpus_search FORCED to the scan arm "
          "(B2-504: FTS_DB pointed at an absent path in-process, the B2-102 "
          "A/B pattern, so post-wiring runs still measure the scan arm), "
          "3 runs/query")
    out["queries"] = []
    fts_db_saved = tool.FTS_DB
    tool.FTS_DB = tool.Path(os.path.dirname(str(fts_db_saved)) or ".",
                            "__absent_forced_scan__.sqlite")
    assert not tool.FTS_DB.exists()
    try:
        for q in QUERIES:
            times = []
            hit_count = rows_scanned = None
            engine = None
            for _ in range(3):
                t0 = time.perf_counter()
                res = tool.corpus_search(query=q, limit=20)
                times.append(round((time.perf_counter() - t0) * 1000, 1))
                hit_count = res.get("hit_count")
                rows_scanned = res.get("rows_scanned")
                engine = res.get("engine")
            out["queries"].append({"q": q, "engine": engine,
                                   "index_state": res.get("index_state"),
                                   "times_ms": times,
                                   "min_ms": min(times),
                                   "median_ms": statistics.median(times),
                                   "hit_count": hit_count,
                                   "rows_scanned": rows_scanned})
            print(json.dumps(out["queries"][-1]))
    finally:
        tool.FTS_DB = fts_db_saved

    print("[4/4] FTS5: match + join for the tool row shape, 5 runs/query")
    fts_rows = []
    for i, q in enumerate(QUERIES):
        expr = fts_expr(q)
        # MATCH must name the fts table itself; the alias form (c MATCH ?)
        # fails with "no such column" in a join (measured 2026-09-26).
        sql = ("SELECT r.id, r.path, r.zone, r.ext, r.bytes, r.mtime, r.title"
               " FROM corpus AS c JOIN crows AS r ON r.rowid = c.rowid"
               " WHERE corpus MATCH ? LIMIT 20")
        times = []
        sample = None
        for _ in range(5):
            t0 = time.perf_counter()
            cur = con.execute(sql, (expr,))
            rows = cur.fetchall()
            times.append(round((time.perf_counter() - t0) * 1000, 2))
            sample = rows[:3]
        n = con.execute("SELECT count(*) FROM corpus WHERE corpus MATCH ?",
                        (expr,)).fetchone()[0]
        entry = {"q": q, "engine": "fts5", "expr": expr,
                 "times_ms": times, "min_ms": min(times),
                 "median_ms": statistics.median(times),
                 "fts5_count": n, "sample_paths": [r[1] for r in sample]}
        out["queries"].append(entry)
        fts_rows.append(entry)
        print(json.dumps(entry))

    # Class medians: full-scan class = queries whose scan walked all rows.
    # B2-504: classification reads the ACTUAL engine each arm reported plus
    # the parity note, never a hardcoded label; the full-scan class stays
    # "scan walked all rows" (rows_scanned >= rows_indexed) computed on the
    # measured value.
    scan_by_q = {e["q"]: e for e in out["queries"] if e.get("engine") == "scan"
                 and e.get("rows_scanned") is not None}
    full = [q for q in QUERIES
            if q in scan_by_q
            and scan_by_q[q]["rows_scanned"] >= out["build"]["rows_indexed"]]
    partial = [q for q in QUERIES if q not in full]
    out["classes"] = {
        "full_scan_queries": full,
        "partial_or_early_queries": partial,
        "full_scan_median_ms": statistics.median(
            [scan_by_q[q]["median_ms"] for q in full]) if full else None,
        "full_scan_best_ms": min(
            [scan_by_q[q]["min_ms"] for q in full]) if full else None,
        "fts5_same_queries_median_ms": statistics.median(
            [e["median_ms"] for e in fts_rows if e["q"] in full]) if full else None,
        "fts5_same_queries_best_ms": min(
            [e["min_ms"] for e in fts_rows if e["q"] in full]) if full else None,
        "fts5_all10_max_ms": max(e["max_ms"] for e in
                                 [{"max_ms": max(e["times_ms"])} for e in fts_rows]),
    }
    con.close()
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("RESULTS_WRITTEN", RESULTS)
    print(json.dumps(out["classes"]))


if __name__ == "__main__":
    main()
