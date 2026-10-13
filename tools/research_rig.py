"""Research rig — multi-tier research with right-sized output (T0/T1).

The "nugget, not novel" pipeline: take what's worthwhile, log where it came
from, keep a copy for the museum, keep truckin'.

  T0 RECALL   local, zero cost — answer from the codebase/manifest/memory
  T1 FOCUSED  local + ONE source (URL/file) — fetch → nugget → museum

Every result carries provenance {source, ts, tier} and the full source is
archived to the museum (memory/research_packs/raw/). Only the nugget (≤200
chars) returns to working memory. T2+ (flash synth / pro deep) hook in later.

Run:
  python tools/research_rig.py recall "where is the false-success guard?"
  python tools/research_rig.py focused "deepseek cache pricing" --url <url>
  python tools/research_rig.py recall "q" --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ROOT  # noqa: E402

MUSEUM = ROOT / "memory" / "research_packs" / "raw"
MANIFEST = ROOT / "memory" / "capability_manifest.md"
NUGGET_LIMIT = 200


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(s: str, n: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "q").lower()).strip("-")
    return (s or "q")[:n]


def nugget(text: str, *, limit: int = NUGGET_LIMIT) -> str:
    """Extractive right-sizing: first real sentence(s) up to the limit."""
    t = (text or "").strip()
    if len(t) <= limit:
        return t
    # keep first 1-2 sentences
    parts = re.split(r"(?<=[.!?])\s+", t)
    out = ""
    for p in parts:
        if len(out) + len(p) + 1 > limit:
            break
        out += p + " "
    return (out or t[:limit]).strip()[:limit]


def _museum(slug: str, text: str, *, source: str, tier: str) -> Path:
    """Archive the FULL source to the museum; return the archived path."""
    MUSEUM.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = MUSEUM / f"{ts}_{slug}.raw.txt"
    p.write_text(f"# source: {source}\n# tier: {tier}\n# ts: {ts}\n\n{text}", encoding="utf-8")
    return p


# ---------------------------------------------------------------- T0 recall
def recall(query: str, *, limit: int = 6) -> dict[str, Any]:
    """Zero-cost local recall: grep manifest + memory/research_packs for the
    question, return the best-matching nuggets with provenance."""
    hits: list[dict[str, Any]] = []
    q = " ".join(re.findall(r"[a-z0-9]{3,}", query.lower()))
    terms = set(q.split())
    roots = [MANIFEST] + sorted((ROOT / "memory" / "research_packs").glob("*.md"))
    for path in roots:
        if not path.is_file():
            continue
        try:
            txt = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = txt.lower()
        score = sum(1 for t in terms if t in low)
        if score >= 2:
            # first line with a term as the nugget
            n = next((l.strip()[:NUGGET_LIMIT] for l in txt.splitlines()
                      if any(t in l.lower() for t in terms) and len(l.strip()) > 20), txt[:NUGGET_LIMIT])
            hits.append({"source": str(path.relative_to(ROOT)), "score": score, "nugget": n})
    hits.sort(key=lambda h: h["score"], reverse=True)
    hits = hits[:limit]
    return {
        "ok": True, "tier": "T0", "query": query, "hits": hits,
        "verdict": "recall found local knowledge" if hits else "no local hit — escalate to T1/T2",
        "provenance": [h["source"] for h in hits],
    }


# ---------------------------------------------------------------- T1 focused
def focused(query: str, url: str, *, timeout: float = 25.0) -> dict[str, Any]:
    """Fetch ONE source, extract the nugget, archive the full source to the
    museum, return with provenance."""
    try:
        import httpx

        with httpx.Client(follow_redirects=True, timeout=timeout,
                          headers={"User-Agent": "MagResearchRig/1.0"}) as client:
            r = client.get(url)
        raw = r.text
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "tier": "T1", "error": str(e)[:160], "url": url}
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()[:4000]
    n = nugget(text)
    archived = _museum(_slug(query), text, source=url, tier="T1")
    return {
        "ok": True, "tier": "T1", "query": query, "url": url,
        "nugget": n, "museum": str(archived.relative_to(ROOT)),
        "provenance": [url, str(archived.relative_to(ROOT))],
        "verdict": "nugget extracted; full source archived to museum",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="research-rig", description="Multi-tier research with right-sized output (T0/T1).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_rec = sub.add_parser("recall", help="T0 local recall (zero cost)")
    p_rec.add_argument("query")
    p_rec.add_argument("--json", action="store_true")
    p_foc = sub.add_parser("focused", help="T1 one-source fetch → nugget → museum")
    p_foc.add_argument("query")
    p_foc.add_argument("--url", required=True)
    p_foc.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "recall":
        out = recall(args.query)
    else:
        out = focused(args.query, args.url)
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"{out.get('tier')} · {out.get('verdict')}")
        for h in out.get("hits", []):
            print(f"  - [{h['source']}] {h['nugget']}")
        if out.get("nugget"):
            print(f"  nugget: {out['nugget']}")
            print(f"  museum: {out.get('museum')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
