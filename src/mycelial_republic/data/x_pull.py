"""
Pull public posts into posts.jsonl (best-effort).

Sources:
  1. Manual/agent-fed status IDs or JSONL rows (primary)
  2. Per-status fetch via fxtwitter / syndication (same stack as sovereign-mirror)

Full 3-month timelines need either:
  - Official X archive export (complete), or
  - X API bearer + user timeline, or
  - Agent harvest via X search tools writing into this format

This module does NOT scrape login walls. It normalizes what you can get.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


def _get_json(url: str, timeout: float = 25.0) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MycelialRepublic/0.1 (+local; research)"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_status(status_id: str) -> dict[str, Any] | None:
    status_id = str(status_id).strip()
    # fxtwitter
    try:
        data = _get_json(f"https://api.fxtwitter.com/status/{status_id}")
        tweet = data.get("tweet") or data
        text = (tweet.get("text") or tweet.get("raw_text") or "").strip()
        if text:
            author = ""
            user = tweet.get("author") or {}
            if isinstance(user, dict):
                sn = user.get("screen_name") or ""
                author = sn
            created = tweet.get("created_at") or tweet.get("date") or ""
            return {
                "id": status_id,
                "text": text,
                "created_at": str(created),
                "author": author,
                "source": "x_fxtwitter",
                "url": f"https://x.com/i/status/{status_id}",
                "meta": {
                    "likes": tweet.get("likes") or tweet.get("favorite_count"),
                    "reposts": tweet.get("retweets") or tweet.get("retweet_count"),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                },
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError):
        pass
    # syndication
    try:
        url = (
            "https://cdn.syndication.twimg.com/tweet-result?"
            + urllib.parse.urlencode({"id": status_id, "lang": "en"})
        )
        data = _get_json(url)
        text = (data.get("text") or "").strip()
        if text:
            user = data.get("user") or {}
            sn = user.get("screen_name") if isinstance(user, dict) else ""
            return {
                "id": status_id,
                "text": text,
                "created_at": str(data.get("created_at") or ""),
                "author": sn or "",
                "source": "x_syndication",
                "url": f"https://x.com/i/status/{status_id}",
                "meta": {"fetched_at": datetime.now(timezone.utc).isoformat()},
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError):
        pass
    return None


def load_seed_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def merge_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for r in rows:
        rid = str(r.get("id") or "")
        if not rid:
            rid = f"hash-{hash(r.get('text', '')) & 0xFFFFFFFF:x}"
        text = (r.get("text") or "").strip()
        if len(text) < 20:
            continue
        # Prefer longer text if duplicate
        if rid not in by_id or len(text) > len(by_id[rid].get("text") or ""):
            by_id[rid] = {
                "id": rid,
                "source": r.get("source") or "x_public",
                "text": text,
                "created_at": r.get("created_at") or "",
                "meta": {
                    **(r.get("meta") or {}),
                    "author": r.get("author") or (r.get("meta") or {}).get("author") or "",
                    "url": r.get("url") or f"https://x.com/i/status/{rid}",
                },
            }
    return list(by_id.values())


def write_posts(rows: list[dict[str, Any]], out: Path) -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def run_pull_ids(ids: list[str], out: str, seed_jsonl: str | None = None) -> int:
    rows: list[dict[str, Any]] = []
    if seed_jsonl:
        rows.extend(load_seed_jsonl(Path(seed_jsonl)))
    ok, fail = 0, 0
    for sid in ids:
        sid = re.sub(r"\D", "", sid) or sid
        if not sid:
            continue
        got = fetch_status(sid)
        if got:
            rows.append(got)
            ok += 1
        else:
            fail += 1
            print(f"fetch fail: {sid}", file=sys.stderr)
    merged = merge_rows(rows)
    n = write_posts(merged, Path(out))
    print(f"Wrote {n} posts → {out} (fetched ok={ok} fail={fail})", file=sys.stderr)
    return 0 if n else 2


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Normalize / fetch X posts into posts.jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ids", default="", help="Comma-separated status IDs to fetch")
    ap.add_argument("--ids-file", default="", help="File with one status id per line")
    ap.add_argument("--seed", default="", help="Existing JSONL to merge")
    a = ap.parse_args(argv)
    ids: list[str] = []
    if a.ids:
        ids.extend(a.ids.split(","))
    if a.ids_file:
        p = Path(a.ids_file)
        if p.is_file():
            ids.extend(p.read_text(encoding="utf-8").splitlines())
    return run_pull_ids(ids, a.out, seed_jsonl=a.seed or None)


if __name__ == "__main__":
    raise SystemExit(main())
