"""corpus -- read-only surfacing tools over the estate catalog (2026-09-18).

The salon fold (watch/inbox/CORPUS_MAP_SALON_20260918.md) ruled: the map
already exists (catalog/catalog.jsonl, ~947K rows); the missing organ was the
consumer. These four tools are that consumer surface -- search the map, get
the bytes, tail the ledgers, count the zones.

LAW (the operator's anchor, 2026-09-18): our estimation of the thing must not
replace the thing. Every byte-serving tool echoes the sha256 of exactly the
bytes served, plus the catalog id derived the same way the scanner derives
it (sha256 of the relative path, first 12 hex), so any seat can re-verify
the map against the disk. Read-only by law: nothing here writes.

FTS5 (B2-102, 2026-09-26, wiring the B2-22 spike): corpus_search prefers the
external-content FTS5 index at catalog/catalog_fts.sqlite and falls back to
the JSONL scan whenever the index is absent, stale, or erroring, saying so in
the result (engine + index_state + index_note): never silently stale. The
freshness gate is mtime first (an index older than catalog.jsonl is stale,
the exact law the brief names), then bytes (the index meta table records the
catalog_bytes it was built over; a size mismatch is stale even when mtimes
look right), and a db that will not open as sqlite is stale too. Semantics
differ honestly: the scan is substring-AND over lowercased path+title, FTS5
is token/phrase-prefix (unicode61), which can MISS mid-token substring hits
the scan finds -- the spike measured 3 of 10 queries short (hermes 914 to
912, falsifier 69 to 68, garden 17 to 14, each delta a mid-token match, e.g.
"garden" inside noblegarden.cpp), so every fts5 result carries that parity
note and rows_scanned on the fts5 engine counts matched rows walked, not
lines read. Term-less queries never touch the index (the scan early-breaks
at limit anyway). The index is opened mode=ro; this module still writes
nothing. Rebuild entry point, the one sanctioned writer:
    .venv/Scripts/python.exe tools/corpus_fts_rebuild.py [--check] [--deep]
Same shape as the spike build (crows + corpus fts5 + meta): 12.35s and
217,686,016 bytes over the Sep-18 map. Spike receipt:
watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md.

Confined: every path resolves under the repo root or is refused.
Text only: a null byte in the sniffed head refuses the serve (no binary dumps).

Map-plane disclosure (B2-104, 2026-09-26): the index gate above answers "is
the INDEX current with the MAP"; it cannot answer "is the MAP current with
the DISK" -- that is the C6 disease (the Sep-18 map answered every tool with
a week-old estate; qdrop scored 0 on scan AND fts5 while
watch/inbox/qdrop_export sat on disk, watch/inbox/burn_wave_20260926/
B2_22_fts5_spike_20260926.md). So every MAP-derived answer (corpus_search
both engines, corpus_stats) attaches the verdict from mag.catalog_freshness
(the C6 policy's disclosure arm): map_asof, map_age_hours, map_stale against
the policy's 48h budget. Byte-serving tools (get/tail) stay unstamped: they
hash the live bytes they serve and never quote the map.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from mag.catalog_freshness import map_freshness as _map_freshness

CATALOG = REPO / "catalog" / "catalog.jsonl"
TAGS = REPO / "catalog" / "tags.jsonl"
FTS_DB = REPO / "catalog" / "catalog_fts.sqlite"
REBUILD_CLI = "tools/corpus_fts_rebuild.py"
_MAX_BYTES = 262144  # hard cap for any single serve
_LAW = "pointers only -- corpus_get the bytes before quoting any as fact"
_PARITY_NOTE = (
    "fts5 is token/phrase-prefix (unicode61), not substring: it can miss "
    "mid-token matches the scan finds (B2-22 measured 3 of 10 queries short: "
    "hermes 914 to 912, falsifier 69 to 68, garden 17 to 14; "
    "watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md)")


def _confine(rel: str) -> Path | None:
    """Resolved absolute path under REPO, or None when it escapes."""
    if not rel or os.path.isabs(rel):
        return None
    # B2-184 path-seam fix: the scanner (mag/catalog_scan.py:83) walks the
    # PROJECTS dir, so catalog rows and corpus_search hits carry the
    # "local_sovereign_agent/" prefix while this surface is repo-relative;
    # strip that exact prefix so corpus_get(corpus_search hit) serves bytes
    # instead of resolving a nonexistent nested path. Confinement is
    # unchanged: the strip is literal, everything still resolves under REPO.
    norm = str(rel).replace("\\", "/")
    if norm.startswith("local_sovereign_agent/"):
        norm = norm[len("local_sovereign_agent/"):]
    if not norm or norm.endswith("/"):
        return None
    real = os.path.realpath(str(REPO / norm))
    root_s = str(REPO)
    if real == root_s or not real.startswith(root_s + os.sep):
        return None
    return Path(real)


def _catalog_id(rel: str) -> str:
    return hashlib.sha256(rel.encode("utf-8", "replace")).hexdigest()[:12]


def _zone_of(rel: str) -> str:
    p = rel.replace("\\", "/").lower()
    prefixes = [
        ("watch/inbox", "intake"), ("watch/astra_hold0", "astra"),
        ("watch/", "watch"), ("basecamp", "basecamp"),
        ("campaigns", "campaigns"), ("docs/", "doctrine"),
        ("memory/runs", "runs"), ("memory/", "memory"), ("mag/", "code"),
        ("tests/", "code"), ("scripts/", "code"), ("configs/", "code"),
        ("dashboard/static/games", "games"), ("dashboard/", "dashboard"),
        ("research/", "research"), ("queue/", "queue"), ("catalog/", "catalog"),
    ]
    for prefix, zone in prefixes:
        if p.startswith(prefix):
            return zone
    if p.startswith("local_sovereign_agent/"):
        return "lsa"
    top = p.split("/")[0] if "/" in p else p
    return "ext:" + top[:16]


def _is_text(path: Path) -> bool:
    try:
        with open(path, "rb") as fh:
            return b"\x00" not in fh.read(8192)
    except OSError:
        return False


def _fts_expr(terms: list[str]) -> str:
    """Substring-AND -> FTS5 MATCH: each term a quoted prefix phrase, ANDed.
    Kept verbatim from the B2-22 spike (watch/inbox/burn_wave_20260926/
    B2_22_fts5_spike.py fts_expr) so the wired numbers are the measured ones."""
    return " AND ".join('"%s"*' % t.replace('"', '""') for t in terms)


def _fts_state() -> tuple[str, str]:
    """Freshness gate for the FTS5 index: fresh | stale | absent, plus a note
    naming the reason and the rebuild command. Gate order (B2-102, spec above):
    mtime (db older than catalog.jsonl is stale), then bytes (meta
    catalog_bytes vs current catalog size; catches restored or rotated files
    whose mtimes lie), then a read probe (a db that will not open mode=ro is
    stale, never a silent crash later). No meta table means the spike-era
    build: fresh only by mtime, and the note says the gate is weaker.
    """
    if not FTS_DB.exists():
        return "absent", "no index at catalog/catalog_fts.sqlite; run " + REBUILD_CLI
    try:
        cat_mtime = CATALOG.stat().st_mtime
        db_mtime = FTS_DB.stat().st_mtime
        cat_bytes = CATALOG.stat().st_size
    except OSError as e:
        return "absent", "stat failed on index or catalog: %s" % e
    if db_mtime < cat_mtime:
        return "stale", ("index older than catalog.jsonl; run " + REBUILD_CLI)
    meta: dict[str, str] = {}
    try:
        con = sqlite3.connect("file:%s?mode=ro" % FTS_DB.as_posix(), uri=True)
        try:
            try:
                for k, v in con.execute("SELECT key, value FROM meta"):
                    meta[str(k)] = str(v)
            except sqlite3.Error:
                meta = {}  # spike-era build: no meta table, the mtime gate stands
            con.execute("SELECT 1 FROM corpus LIMIT 1").fetchone()
        finally:
            con.close()
    except sqlite3.Error as e:
        return "stale", "index unreadable (%s); run %s" % (e, REBUILD_CLI)
    if meta.get("catalog_bytes", "").isdigit() \
            and int(meta["catalog_bytes"]) != cat_bytes:
        return "stale", (
            "index was built over %s catalog bytes, catalog.jsonl is now %d; "
            "run %s" % (meta["catalog_bytes"], cat_bytes, REBUILD_CLI))
    if not meta:
        return ("fresh", "index fresh by mtime only (spike-era build, no meta "
                        "table); run %s for the byte-gated rebuild" % REBUILD_CLI)
    return "fresh", "index fresh: mtime and meta catalog_bytes both current"


def _search_fts(terms: list[str], zone: str, ext: str,
                tag_ids: set[str] | None, since: str,
                limit: int) -> tuple[dict | None, str]:
    """FTS5 pass over the index, filters applied post-match in catalog order
    (rowid order = catalog.jsonl line order, so the first-limit rows line up
    with the scan path). Returns (result, "") or (None, fallback_reason) --
    None means the caller falls back to the scan and says why."""
    expr = _fts_expr(terms)
    hits: list[dict] = []
    walked = 0
    try:
        con = sqlite3.connect("file:%s?mode=ro" % FTS_DB.as_posix(), uri=True)
        try:
            cur = con.execute(
                "SELECT r.id, r.path, r.zone, r.ext, r.bytes, r.mtime, r.title"
                " FROM corpus AS c JOIN crows AS r ON r.rowid = c.rowid"
                " WHERE corpus MATCH ?", (expr,))
            for rid, path, rzone, rext, rbytes, mtime, title in cur:
                walked += 1
                if zone and rzone != zone:
                    continue
                if ext and rext != ext:
                    continue
                if tag_ids is not None and rid not in tag_ids:
                    continue
                if since and str(mtime or "")[:10] < since:
                    continue
                hits.append({"id": rid, "path": path, "zone": rzone,
                             "bytes": rbytes, "mtime": mtime, "title": title})
                if len(hits) >= limit:
                    break
        finally:
            con.close()
    except sqlite3.Error as e:
        return None, "fts5 match failed (%s); scanned instead" % e
    return ({"ok": True, "tool": "corpus_search", "engine": "fts5",
             "index_state": "fresh", "hits": hits, "hit_count": len(hits),
             "rows_scanned": walked, "parity_note": _PARITY_NOTE,
             **_map_freshness(),
             "law": _LAW}, "")


def corpus_search(query: str = "", zone: str = "", ext: str = "",
                  kind: str = "", since: str = "", limit: int = 20) -> dict:
    """Search the catalog map (never the bytes): substring on path/title.

    Prefers the FTS5 index per the module spec; falls back to the JSONL scan
    when the index is absent, stale, or erroring and names that in the result
    (engine, index_state, index_note). zone: exact zone filter. ext: e.g.
    '.md'. kind: joins catalog/tags.jsonl
    (card/receipt/ledger/brief/corpus/test/code/image/prose/config/other/state)
    when the tag pass has run. since: YYYY-MM-DD, mtime lower bound.
    Returns rows (id, path, zone, bytes, mtime, title) -- pointers, not bodies.
    """
    limit = max(1, min(int(limit), 100))
    terms = [t for t in (query or "").lower().split() if t]
    tag_ids: set[str] | None = None
    if kind:
        tag_ids = set()
        try:
            with open(TAGS, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if row.get("kind") == kind:
                        tag_ids.add(row.get("id"))
        except OSError:
            pass
        if not tag_ids:
            return {"ok": False, "error": "no tags.jsonl or kind unmatched; run the tag pass"}
    if terms:
        state, note = _fts_state()
        if state == "fresh":
            fts_res, fts_err = _search_fts(terms, zone, ext, tag_ids, since, limit)
            if fts_res is not None:
                return fts_res
            state, note = "error", fts_err
    else:
        state, note = ("bypassed",
                       "no query terms: the scan early-breaks at limit; "
                       "the index only engages for term queries")
    hits = []
    scanned = 0
    try:
        with open(CATALOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                scanned += 1
                hay = str(row.get("path", "")) + "\n" + str(row.get("title", ""))
                hay = hay.lower()
                if terms and not all(t in hay for t in terms):
                    continue
                if zone and row.get("zone") != zone:
                    continue
                if ext and row.get("ext") != ext:
                    continue
                if tag_ids is not None and row.get("id") not in tag_ids:
                    continue
                if since and str(row.get("mtime", ""))[:10] < since:
                    continue
                hits.append({k: row.get(k) for k in
                             ("id", "path", "zone", "bytes", "mtime", "title")})
                if len(hits) >= limit:
                    break
    except OSError as e:
        return {"ok": False, "error": f"catalog unreadable: {e}"}
    return {"ok": True, "tool": "corpus_search", "engine": "scan",
            "index_state": state, "index_note": note,
            "hits": hits, "hit_count": len(hits), "rows_scanned": scanned,
            **_map_freshness(),
            "law": _LAW}


def corpus_get(path: str, max_bytes: int = 65536) -> dict:
    """Serve real bytes (capped, text-only) with their sha256 -- byte-true get."""
    real = _confine(path)
    if real is None or not real.is_file():
        return {"ok": False, "error": f"refused or missing: {path}"}
    max_bytes = max(1, min(int(max_bytes), _MAX_BYTES))
    size = real.stat().st_size
    if not _is_text(real):
        return {"ok": False, "error": "binary refused",
                "path": path, "bytes": size,
                "hint": "read binary through a domain tool, not the corpus surface"}
    data = real.read_bytes()[:max_bytes]
    rel = str(real.relative_to(REPO)).replace(os.sep, "/")
    return {"ok": True, "tool": "corpus_get", "path": rel,
            "catalog_id": _catalog_id(rel), "zone": _zone_of(rel),
            "bytes_served": len(data), "bytes_total": size,
            "truncated": size > len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "mtime": datetime.datetime.utcfromtimestamp(
                real.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "content": data.decode("utf-8", "replace")}


def corpus_tail(path: str, lines: int = 40) -> dict:
    """Tail the last N lines of a text ledger, hashed as served."""
    real = _confine(path)
    if real is None or not real.is_file():
        return {"ok": False, "error": f"refused or missing: {path}"}
    lines = max(1, min(int(lines), 500))
    size = real.stat().st_size
    if not _is_text(real):
        return {"ok": False, "error": "binary refused", "path": path}
    chunk = min(size, _MAX_BYTES)
    with open(real, "rb") as fh:
        fh.seek(size - chunk)
        data = fh.read(chunk)
    tail = data.decode("utf-8", "replace").splitlines()[-lines:]
    return {"ok": True, "tool": "corpus_tail", "path": path,
            "lines_served": len(tail), "bytes_total": size,
            "sha256_served": hashlib.sha256("\n".join(tail).encode("utf-8")).hexdigest(),
            "lines": tail}


def corpus_stats(zone: str = "", kind: str = "") -> dict:
    """Count the map: rows per zone (optionally per kind for one zone)."""
    by_zone: dict[str, int] = {}
    by_ext: dict[str, int] = {}
    total = 0
    by_kind: dict[str, int] = {}
    try:
        with open(CATALOG, encoding="utf-8") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                total += 1
                z = str(row.get("zone", "?"))
                by_zone[z] = by_zone.get(z, 0) + 1
                e = str(row.get("ext", "") or "none")
                by_ext[e] = by_ext.get(e, 0) + 1
    except OSError as e:
        return {"ok": False, "error": f"catalog unreadable: {e}"}
    if kind:
        try:
            with open(TAGS, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if row.get("kind") == kind:
                        k = str(row.get("zone", "?"))
                        by_kind[k] = by_kind.get(k, 0) + 1
        except OSError:
            return {"ok": False, "error": "tags.jsonl missing; run the tag pass for kind stats"}
    top_ext = sorted(by_ext.items(), key=lambda kv: -kv[1])[:12]
    return {"ok": True, "tool": "corpus_stats", "total_rows": total,
            "zone": zone or None, "kind": kind or None,
            "zones": by_zone if not zone else {zone: by_zone.get(zone, 0)},
            "top_ext": dict(top_ext), "kind_by_zone": by_kind or None,
            **_map_freshness()}
