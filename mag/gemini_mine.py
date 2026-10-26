"""gemini_mine — mine the GOOGLE/Gemini vendor corpus as STATELESS research (frozen job).

Frozen spec (chord-missing-handoff-honesty-001, next-window-handoff): route each GOOGLE/Gemini
vendor prompt through the ONE primitive (swarm_surface.route_novel -> dedupe by content anchor +
enqueue to the swarm), record anchors to memory/arxiv_mine/ledger.jsonl, reuse mag/arxiv_mine.
LOW tier, $0 (deepseek default), stateless, no scarce seat. Deterministic + pure stdlib.

Schema: gemini_mine.v1
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "gemini_mine.v1"

# Stateless material: Gemini vendor system prompts (sibling trees under projects/).
_SOURCE_DIRS = [
    ROOT.parent / "research" / "cl4r1t4s" / "GOOGLE",
    ROOT.parent / "field-strike-the-chord" / "GOOGLE",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sources() -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    seen = set()
    for d in _SOURCE_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*")):
            if p.is_file() and p.suffix.lower() in (".txt", ".md", ".mkd", ""):
                if p.resolve() in seen:
                    continue
                seen.add(p.resolve())
                out.append((p.name, p))
    return out


def _candidate_rows(max_papers: int) -> list[dict[str, Any]]:
    rows = []
    for name, p in _sources()[: max(1, max_papers)]:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        title_line = ""
        for ln in text.splitlines():
            ln = ln.strip()
            if len(ln) > 16:
                title_line = ln[:180]
                break
        rows.append({
            "claim": f"arXiv/rss: GOOGLE/Gemini vendor prompt — {title_line or name}",
            "detail": text[:1400],
            "source_urls": [str(p)],
        })
    return rows


def mine(*, max_papers: int = 12, dry: bool = False) -> dict[str, Any]:
    """The frozen job: route each GOOGLE/Gemini vendor prompt through the ONE primitive
    (route_novel via arxiv_mine.route_candidates), recording anchors to the arxiv_mine ledger."""
    rows = _candidate_rows(max_papers)
    if not rows:
        return {"ok": True, "schema": SCHEMA, "action": "skip", "reason": "no GOOGLE/Gemini material"}
    # steer via RIB files in memory: mount the RIB instruction set (rib_bus) and inject it into
    # what we route — research direction + our own shape + the good-work ledger — so the frozen
    # job is steered by memory-resident RIBs (by default, like every worker/seat).
    try:
        from mag import rib_bus
        _lines = []
        for _dom in ("research", "self-shape", "good-work"):
            _m = rib_bus.mount(_dom)
            _lines.extend(f"- STEER[{_dom}]: {r}" for r in (_m.get("ribs") or []))
        _steer = "\n".join(_lines)
    except Exception:
        _steer = ""
    if _steer:
        for _r in rows:
            _r["detail"] = (_steer + "\n" + _r.get("detail", ""))[:3000]
    try:
        from mag import arxiv_mine
        r = arxiv_mine.route_candidates(rows, max_papers=max_papers, dry=dry)
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "action": "error", "error": str(e)[:160]}
    return {"ok": bool(r.get("ok")), "schema": SCHEMA, "action": "mined",
            "source": "GOOGLE/Gemini vendor corpus (stateless)",
            "papers": r.get("papers"), "mined": r.get("mined"), "deduped": r.get("deduped"),
            "results": r.get("results")}


def run_cadence(*, dry: bool = False) -> dict[str, Any]:
    """Cadence hook: execute the frozen job through the architecture (idempotent by anchor)."""
    try:
        r = mine(max_papers=12, dry=dry)
    except Exception as e:
        return {"ok": False, "action": "error", "error": str(e)[:120]}
    return {"ok": bool(r.get("ok")), "action": r.get("action", "skip"),
            "mined": r.get("mined"), "deduped": r.get("deduped"),
            "note": "routes through route_novel -> swarm; anchors in memory/arxiv_mine/ledger.jsonl"}


def status() -> dict[str, Any]:
    n_files = len(_sources())
    return {"ok": True, "schema": SCHEMA,
            "contract": "mine() = route each GOOGLE/Gemini vendor prompt via "
                        "arxiv_mine.route_candidates -> swarm_surface.route_novel (dedupe by anchor "
                        "+ enqueue to swarm); anchors -> memory/arxiv_mine/ledger.jsonl. $0, LOW tier.",
            "reuse": "arxiv_mine + swarm_surface.route_novel",
            "n_gemini_files": n_files}


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="gemini_mine")
    sub = p.add_subparsers(dest="cmd")
    m = sub.add_parser("mine")
    m.add_argument("--max", type=int, default=12)
    m.add_argument("--dry", action="store_true")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "mine":
        print(json.dumps(mine(max_papers=a.max, dry=a.dry), indent=2, ensure_ascii=False, default=str))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
