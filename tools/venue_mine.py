#!/usr/bin/env python3
"""venue_mine -- mine free venues for signal that maps to an estate law.

Operator order, 2026-10-21: "free venue mining on x and hackernews reddit etc...
create a keyword list so we can use that for future automation mining and signal
detection as mapped to invariants so they can be detected across discipline."

Design laws:
  - FREE venues only, stdlib only, no keys: HN (Algolia), Lobsters (RSS),
    Reddit (RSS), arXiv (Atom). X has no anonymous API and is deliberately
    absent rather than scraped - a seat that scrapes a walled venue is a
    liability, not a miner.
  - Every hit must ROUTE: configs/signal_lexicon.json binds each family to an
    artifact that would consume it. A family with no binding is not mined.
  - Dedupe by URL; a story matched by three families is one story with three
    reasons, not three stories.

    python tools/venue_mine.py --days 7 --venues hn,lobsters --json
    python tools/venue_mine.py --out memory/runs/venue_mine/2026-10-21
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "configs" / "signal_lexicon.json"
UA = "sovereign-mag-signal-miner/1.0 (+local estate; contact: operator)"
VENUE_WEIGHT = {"hn": 1.0, "lobsters": 0.9, "reddit": 0.9, "arxiv": 1.1}
VENUE_RATE_S = {"hn": 1.0, "lobsters": 1.0, "reddit": 2.0, "arxiv": 3.0}


def _get(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed venues
        return resp.read()


def load_lexicon(path: Path = LEXICON) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for fam in data["families"]:
        for key in ("id", "law", "triggers", "estate_binding", "weight"):
            if key not in fam:
                raise ValueError(f"family {fam.get('id', '?')} missing {key}")
    return data


def build_queries(lexicon: dict, per_family: int = 2, families: set[str] | None = None) -> list[tuple[str, str]]:
    """(family_id, query) pairs - the first triggers carry the family's weight."""
    out = []
    for fam in lexicon["families"]:
        if families and fam["id"] not in families:
            continue
        for term in fam["triggers"][:per_family]:
            out.append((fam["id"], term))
    return out


def match_terms(text: str, fam: dict) -> list[str]:
    low = text.lower()
    hits = []
    for term in fam["triggers"]:
        if term.lower() in low:
            hits.append(term)
    for bad in fam.get("anti", []):
        if bad.lower() in low:
            return []
    return hits


def context_hits(text: str, fam: dict) -> list[str]:
    low = text.lower()
    return [c for c in fam.get("context", []) if c.lower() in low]


def accepts(fam: dict, hits: list[str], ctx: list[str]) -> bool:
    """Precision gate. Single-word triggers are noise magnets: "criticality"
    pulled two nuclear reactors, "lease" pulled an OpenSSL release. Accept when
    a multiword trigger matched, or two distinct triggers did, or one trigger
    plus one domain context word."""
    if not hits:
        return False
    if any(" " in h for h in hits):
        return True
    if any(h in fam.get("strong", []) for h in hits):
        return True
    if len(hits) >= int(fam.get("min_hits", 2)):
        return True
    return bool(ctx)


def score(fam: dict, hits: list[str], venue: str, points: int, published: datetime | None,
          now: datetime) -> float:
    match = min(len(hits), 3) / 3.0
    base = float(fam.get("weight", 1.0)) * VENUE_WEIGHT.get(venue, 0.8) * (0.4 + 0.6 * match)
    if points:
        base += math.log1p(points) / 8.0
    if published:
        age_d = max(0.0, (now - published).total_seconds() / 86400.0)
        base *= max(0.35, 1.0 - age_d / 30.0)   # a month-old story is context, not signal
    return round(base, 3)


# ── venues ----------------------------------------------------------------

def _iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def mine_hn(query: str, days: float, per_query: int = 30) -> list[dict]:
    # No date filter: venue data can lag the local clock (2026-10-24: HN's newest
    # "backpressure" story was 2026-08-26, so a 14-day local window matched
    # nothing while the venue had material). Window relative to the venue.
    url = ("https://hn.algolia.com/api/v1/search_by_date?"
           + urllib.parse.urlencode({
               "query": query, "tags": "story", "hitsPerPage": per_query}))
    rows = json.loads(_get(url).decode("utf-8"))
    out = []
    for hit in rows.get("hits", []):
        out.append({
            "venue": "hn",
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "title": (hit.get("title") or "").strip(),
            "author": hit.get("author"),
            "points": hit.get("points") or 0,
            "comments": hit.get("num_comments") or 0,
            "published": hit.get("created_at"),
        })
    return out


def _rss_items(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for item in root.iter():
        tag = item.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        title = link = date = ""
        for child in item:
            name = child.tag.split("}")[-1]
            if name == "title":
                title = (child.text or "").strip()
            elif name == "link":
                link = (child.text or "").strip() or child.attrib.get("href", "")
            elif name in ("pubDate", "published", "updated"):
                date = (child.text or "").strip()
        if title and link:
            out.append({"url": link, "title": title, "published": date or None})
    return out


def mine_lobsters(days: float) -> list[dict]:
    items = _rss_items(_get("https://lobste.rs/rss"))
    out = []
    for it in items:
        stamp = _iso(it["published"]) or None
        out.append({"venue": "lobsters", "url": it["url"], "title": it["title"],
                    "author": None, "points": 0, "comments": 0,
                    "published": stamp.isoformat() if stamp else None})
    return out


def mine_reddit(subreddits: list[str], days: float) -> list[dict]:
    # One multi-sub request: per-sub fetches hit 429 immediately (2026-10-24).
    joined = "+".join(s.strip() for s in subreddits if s.strip())
    items = _rss_items(_get(f"https://www.reddit.com/r/{joined}/.rss"))
    return [{"venue": "reddit", "url": it["url"], "title": it["title"],
             "author": None, "points": 0, "comments": 0,
             "published": it["published"]} for it in items]


def mine_arxiv(query: str, days: float, per_query: int = 10) -> list[dict]:
    q = urllib.parse.quote(f'all:"{query}"')
    url = (f"http://export.arxiv.org/api/query?search_query={q}"
           f"&sortBy=submittedDate&sortOrder=descending&max_results={per_query}")
    out = []
    for it in _rss_items(_get(url)):
        out.append({"venue": "arxiv", "url": it["url"], "title": it["title"],
                    "author": None, "points": 0, "comments": 0,
                    "published": it["published"]})
    return out


# ── scoring loop ----------------------------------------------------------

def mine(lexicon: dict, venues: set[str], days: float, per_family: int,
         families: set[str] | None, reddit_subs: list[str],
         verbose: bool = False) -> tuple[list[dict], list[dict]]:
    now = datetime.now(timezone.utc)
    fams = {f["id"]: f for f in lexicon["families"]}
    errors: list[dict] = []
    seen: dict[str, dict] = {}

    def absorb(item: dict, fam_id: str) -> None:
        fam = fams[fam_id]
        hits = match_terms(item["title"], fam)
        ctx = context_hits(item["title"], fam)
        if not accepts(fam, hits, ctx):
            return
        published = _iso(item.get("published"))
        key = hashlib.sha1(item["url"].encode("utf-8", "replace")).hexdigest()[:16]
        row = seen.get(key)
        if row is None:
            row = {**item, "id": key, "families": [], "matched": {},
                   "score": 0.0, "estate_binding": fam["estate_binding"],
                   "law": fam["law"], "action": fam.get("action", "")}
            seen[key] = row
        if fam_id not in row["families"]:
            row["families"].append(fam_id)
            row["matched"][fam_id] = hits + [f"~{c}" for c in ctx]
            row["score"] = round(row["score"] + score(fam, hits, item["venue"],
                                                      int(item.get("points") or 0),
                                                      published, now), 3)

    queries = build_queries(lexicon, per_family=per_family, families=families)

    if "hn" in venues:
        for fam_id, q in queries:
            try:
                for item in mine_hn(q, days):
                    absorb(item, fam_id)
            except Exception as exc:  # noqa: BLE001
                errors.append({"venue": "hn", "query": q, "error": str(exc)[:120]})
            if verbose:
                print(f"  hn {q!r} -> {len(seen)} unique", file=sys.stderr)
            time.sleep(VENUE_RATE_S["hn"])

    if "lobsters" in venues:
        try:
            items = mine_lobsters(days)
            for item in items:
                for fam_id in fams:
                    absorb(item, fam_id)
        except Exception as exc:  # noqa: BLE001
            errors.append({"venue": "lobsters", "error": str(exc)[:120]})

    if "reddit" in venues:
        try:
            items = mine_reddit(reddit_subs, days)
            for item in items:
                for fam_id in fams:
                    absorb(item, fam_id)
        except Exception as exc:  # noqa: BLE001
            errors.append({"venue": "reddit", "error": str(exc)[:120]})

    if "arxiv" in venues:
        for fam_id, q in queries[: max(1, len(queries) // 3)]:
            try:
                for item in mine_arxiv(q, days):
                    absorb(item, fam_id)
            except Exception as exc:  # noqa: BLE001
                errors.append({"venue": "arxiv", "query": q, "error": str(exc)[:120]})
            time.sleep(VENUE_RATE_S["arxiv"])

    # Venue-relative window: keep items within `days` of the NEWEST item that
    # venue returned. Honest about clock skew: the digest states each venue's
    # newest stamp instead of pretending the local date is shared.
    windows: dict[str, dict] = {}
    kept: list[dict] = []
    for row in seen.values():
        stamp = _iso(row.get("published"))
        venue = row["venue"]
        if stamp is None:
            kept.append(row)
            continue
        w = windows.setdefault(venue, {"newest": stamp})
        if stamp > w["newest"]:
            w["newest"] = stamp
    for row in seen.values():
        stamp = _iso(row.get("published"))
        if stamp is None:
            continue
        newest = windows[row["venue"]]["newest"]
        if (newest - stamp) <= timedelta(days=days):
            kept.append(row)
    for venue, w in windows.items():
        w["newest"] = w["newest"].isoformat()
        w["kept"] = sum(1 for r in kept if r["venue"] == venue)
    rows = sorted(kept, key=lambda r: (-r["score"], r["title"]))
    return rows, errors, windows


def digest(rows: list[dict], errors: list[dict], lexicon: dict, top: int = 4) -> str:
    by_fam: dict[str, list[dict]] = {}
    for r in rows:
        for fam in r["families"]:
            by_fam.setdefault(fam, []).append(r)
    lines = [f"# Signal digest - {datetime.now(timezone.utc).date()}",
             "",
             f"{len(rows)} unique stories carried at least one estate law. "
             f"Venues: free only (HN, Lobsters, Reddit RSS, arXiv). X excluded: no anonymous API.",
             ""]
    for fam_id in [f["id"] for f in lexicon["families"]]:
        items = by_fam.get(fam_id, [])
        if not items:
            continue
        fam = next(f for f in lexicon["families"] if f["id"] == fam_id)
        lines.append(f"## {fam_id} - {fam['law']}")
        lines.append(f"_binds to:_ `{fam['estate_binding']}`")
        for r in sorted(items, key=lambda x: -x["score"])[:top]:
            pts = f" · {r['points']}pts" if r.get("points") else ""
            lines.append(f"- **{r['title']}** [{r['venue']}{pts}] {r['url']}")
            lines.append(f"  - matched {', '.join(r['matched'][fam_id])}; score {r['score']}")
        lines.append("")
    if errors:
        lines.append("## venue errors")
        for e in errors[:10]:
            lines.append(f"- {e['venue']}: {e.get('query', '')} {e['error']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mine free venues against the estate signal lexicon")
    ap.add_argument("--lexicon", default=str(LEXICON))
    ap.add_argument("--venues", default="hn,lobsters")
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--per-family", type=int, default=2)
    ap.add_argument("--families", default=None, help="comma list of family ids")
    ap.add_argument("--reddit-subs", default="MachineLearning,LocalLLaMA,compsci,devops")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None, help="prefix for .jsonl and .md outputs")
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    lexicon = load_lexicon(Path(args.lexicon))
    families = set(args.families.split(",")) if args.families else None
    rows, errors, windows = mine(lexicon, set(args.venues.split(",")), args.days,
                        args.per_family, families, args.reddit_subs.split(","),
                        verbose=args.verbose)
    md = digest(rows, errors, lexicon, top=args.top)

    if args.out:
        base = Path(args.out)
        base.parent.mkdir(parents=True, exist_ok=True)
        with base.with_suffix(".jsonl").open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        base.with_suffix(".md").write_text(md, encoding="utf-8")

    if args.json:
        print(json.dumps({"schema": "venue_mine.v1", "rows": len(rows),
                          "windows": windows, "errors": errors,
                          "items": rows[:200]}, indent=2))
    else:
        print(md)
        if windows:
            print("\nvenue windows (relative, not local-clock):")
            for venue, w in windows.items():
                print(f"  {venue}: newest {w['newest'][:10]}, kept {w['kept']} within {args.days:g}d")
        print(f"{len(rows)} unique / {len(errors)} venue errors")
    return 0 if rows else 2


if __name__ == "__main__":
    sys.exit(main())
