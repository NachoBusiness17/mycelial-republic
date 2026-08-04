"""
Fetch X Bookmarks via official API (user OAuth).

Requires env:
  X_BEARER_TOKEN or X_ACCESS_TOKEN  — user-context token with bookmark.read
  X_USER_ID                         — numeric user id

Docs: GET https://api.x.com/2/users/:id/bookmarks

Does nothing useful without credentials — fails loudly instead of faking data.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _token() -> str:
    return (
        os.environ.get("X_ACCESS_TOKEN")
        or os.environ.get("X_BEARER_TOKEN")
        or os.environ.get("TWITTER_BEARER_TOKEN")
        or ""
    ).strip()


def _user_id() -> str:
    return (os.environ.get("X_USER_ID") or os.environ.get("TWITTER_USER_ID") or "").strip()


def _get(url: str, token: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "MycelialRepublic/0.1",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_bookmarks(user_id: str, token: str, max_pages: int = 50) -> list[dict[str, Any]]:
    """Paginate bookmarks. Fields: text, created_at, id."""
    rows: list[dict[str, Any]] = []
    params = {
        "max_results": "100",
        "tweet.fields": "created_at,lang,public_metrics,entities",
    }
    pagination_token: str | None = None
    base = f"https://api.x.com/2/users/{user_id}/bookmarks"

    for _ in range(max_pages):
        q = dict(params)
        if pagination_token:
            q["pagination_token"] = pagination_token
        url = base + "?" + urllib.parse.urlencode(q)
        try:
            data = _get(url, token)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if e.fp else ""
            raise RuntimeError(f"X API HTTP {e.code}: {body[:500]}") from e

        for t in data.get("data") or []:
            text = (t.get("text") or "").strip()
            if len(text) < 15:
                continue
            tid = str(t.get("id") or "")
            rows.append(
                {
                    "id": tid,
                    "source": "x_bookmarks_api",
                    "text": text,
                    "created_at": t.get("created_at") or "",
                    "meta": {
                        "url": f"https://x.com/i/status/{tid}",
                        "public_metrics": t.get("public_metrics") or {},
                        "exported_at": datetime.now(timezone.utc).isoformat(),
                    },
                }
            )

        meta = data.get("meta") or {}
        pagination_token = meta.get("next_token")
        if not pagination_token:
            break

    return rows


def run_x_bookmarks_api(out: str) -> int:
    token = _token()
    uid = _user_id()
    if not token or not uid:
        print(
            "X Bookmarks API needs credentials.\n"
            "  Set X_USER_ID and X_ACCESS_TOKEN (or X_BEARER_TOKEN) with bookmark.read.\n"
            "  Or use the manual path: paste bookmark URLs into data/bookmarks/urls.txt\n"
            "  then: mycelia bookmarks --path data/bookmarks/urls.txt --out ...",
            file=sys.stderr,
        )
        return 2

    rows = fetch_all_bookmarks(uid, token)
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} X bookmarks → {outp}", file=sys.stderr)
    return 0 if rows else 1


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Export X Bookmarks via API")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    return run_x_bookmarks_api(a.out)


if __name__ == "__main__":
    raise SystemExit(main())
