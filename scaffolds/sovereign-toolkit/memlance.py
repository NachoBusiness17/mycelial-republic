"""memlance — selective GROUNDED memory, distilled to a forkable pure-stdlib tool.

THE MECHANISM (our working implementation of this pattern):
  Don't "load everything." SELECT the memory to surface per-task (Quicksort-style
  selection), then lance only the relevant leaves. A memory economy: the right bytes at
  the right moment — not the whole chain.

WHY THIS KILLS HALLUCINATION:
  * select() returns only states read as REAL bytes from disk, each with provenance
    (path) and a deterministic `verified` verdict (derived from explicit grounding
    markers). It never fabricates content.
  * Anything recalled from "memory-of-memory" is NOT a state here; only files that exist
    are candidates. If a state lacks a grounding marker it is returned flagged
    `verified: false` (conservative) — carry it forward only as hypothesis, never truth.

PURE STDLIB — no dependencies. Runs with:  python -m pytest tests/ -q
Schema: memlance.v1
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

SCHEMA = "memlance.v1"
# RIB: grounded selective memory (real bytes + verified/derived verdict) · verify: grounding_verdict tri-state + select relevance · tests: test_toolkit

# A state is VERIFIED only if it carries a real-data / RIB / measured / frozen marker.
# Absent one, it is DERIVED (unverified) — conservative, anti-hallucination.
VERIFIED_MARKERS = (
    "verified", "grounded", "measured", "billed", "rib_", "frozen", "rib-", "rib:",
    "real data", "real billing", "trust bytes", "frozen spec", "verified-in-file",
    "rib-debug", "validated", "confirmed", "shipped",
)
# Explicitly-unverified markers override and force verdict false.
UNVERIFIED_MARKERS = (
    "unverified", "derived", "estimated", "handwave", "not verified", "not grounded",
    "assumption", "plan only", "never runtime-proven", "not runtime-proven",
    "unmeasured", "does not exist",
)

_TOKEN_RE = re.compile(r"[a-z0-9_]+")
_TITLE_RE = re.compile(r"^#\s+(.+)$", re.M)
_DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def grounding_verdict(text: str) -> dict[str, Any]:
    """Deterministic grounding verdict from a state's own bytes."""
    low = (text or "").lower()
    unverified = [m for m in UNVERIFIED_MARKERS if m in low]
    verified = [m for m in VERIFIED_MARKERS if m in low]
    if unverified:
        return {"verified": False, "reason": "unverified_marker",
                "markers": unverified[:5], "verified_markers": verified[:5]}
    if verified:
        return {"verified": True, "reason": "grounding_marker",
                "markers": verified[:5], "verified_markers": []}
    return {"verified": False, "reason": "no_grounding_marker",
            "markers": [], "verified_markers": []}


def _title(path: Path, text: str) -> str:
    m = _TITLE_RE.search(text)
    if m:
        return m.group(1).strip()[:120]
    return path.name


def _ts(path: Path, text: str) -> str:
    m = _DATE_RE.search(text)
    if m:
        return m.group(1)
    try:
        from datetime import datetime
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        return ""


def _tags(kind: str, title: str) -> list[str]:
    return re.findall(_TOKEN_RE, (f"{kind} {title}").lower())


def _read(path: Path, max_chars: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def index(roots: list[tuple[str, str]], *, max_files: int = 4000) -> list[dict[str, Any]]:
    """Index real memory states from disk: (path, kind, title, ts, tags, verified).

    roots: list of (kind, path-or-''); '' means the CWD. Only files that EXIST are
    candidates — nothing is synthesized.
    """
    entries: list[dict[str, Any]] = []
    for kind, rel in roots:
        base = Path(rel) if rel else Path(".")
        if base.is_file():
            text = _read(base)
            entries.append(_entry(kind, base, text))
        elif base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file() and not p.name.startswith("."):
                    text = _read(p)
                    entries.append(_entry(kind, p, text))
                    if len(entries) >= max_files:
                        return entries
    return entries


def _entry(kind: str, path: Path, text: str) -> dict[str, Any]:
    v = grounding_verdict(text)
    title = _title(path, text)
    return {
        "path": str(path),
        "kind": kind,
        "title": title,
        "ts": _ts(path, text),
        "tags": _tags(kind, title),
        "verified": v["verified"],
        "verdict": v,
    }


def _score(goal: str, entry: dict[str, Any]) -> int:
    """Deterministic keyword relevance: goal tokens x (tags + title)."""
    goal_tokens = {t for t in _TOKEN_RE.findall((goal or "").lower()) if len(t) > 2}
    if not goal_tokens:
        return 0
    body_tokens = set(entry.get("tags") or [])
    return len(goal_tokens & body_tokens)


def select(goal: str, entries: list[dict[str, Any]], *, top_k: int = 5,
           prefer_verified: bool = True) -> list[dict[str, Any]]:
    """Select the RELEVANT, GROUNDED states for a context.

    Sorts by relevance; verified states rank above unverified of equal score.
    Every returned entry carries its path (provenance) and a deterministic verdict.
    """
    scored = []
    for e in entries:
        s = _score(goal, e)
        if s > 0:
            # verified ties break in favour of grounded bytes (anti-hallucination)
            scored.append((s, 1 if (prefer_verified and e["verified"]) else 0, e))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [e for _, _, e in scored[:top_k]]


if __name__ == "__main__":
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "note.md"
        p.write_text("# cache economics\nMeasured 98% hit, verified against the real bill.\n",
                     encoding="utf-8")
        idx = index([("mem", str(p))])
        print(json.dumps(select("cache economics", idx), indent=2))
