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

Confined: every path resolves under the repo root or is refused.
Text only: a null byte in the sniffed head refuses the serve (no binary dumps).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog" / "catalog.jsonl"
TAGS = REPO / "catalog" / "tags.jsonl"
_MAX_BYTES = 262144  # hard cap for any single serve


def _confine(rel: str) -> Path | None:
    """Resolved absolute path under REPO, or None when it escapes."""
    if not rel or os.path.isabs(rel):
        return None
    real = os.path.realpath(str(REPO / rel))
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


def corpus_search(query: str = "", zone: str = "", ext: str = "",
                  kind: str = "", since: str = "", limit: int = 20) -> dict:
    """Search the catalog map (never the bytes): substring on path/title.

    zone: exact zone filter. ext: e.g. '.md'. kind: joins catalog/tags.jsonl
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
    return {"ok": True, "tool": "corpus_search", "hits": hits,
            "hit_count": len(hits), "rows_scanned": scanned,
            "law": "pointers only -- corpus_get the bytes before quoting any as fact"}


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
            "top_ext": dict(top_ext), "kind_by_zone": by_kind or None}
