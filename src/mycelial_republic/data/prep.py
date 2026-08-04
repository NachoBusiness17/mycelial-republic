"""Extract high-signal posts from an X (Twitter) archive export."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


def _find_tweet_js(root: Path) -> Path | None:
    candidates = [
        root / "data" / "tweets.js",
        root / "tweets.js",
        root / "data" / "tweet.js",
    ]
    for c in candidates:
        if c.is_file():
            return c
    # Recursive fallback
    for p in root.rglob("tweets.js"):
        return p
    for p in root.rglob("tweet.js"):
        return p
    return None


def _extract_zip(zip_path: Path, dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest)
    return dest


def _load_tweets_js(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Typical: window.YTD.tweets.part0 = [ ... ];
    m = re.search(r"=\s*(\[.*\])\s*;?\s*$", raw, re.DOTALL)
    if not m:
        # Some exports are pure JSON array
        raw_stripped = raw.strip()
        if raw_stripped.startswith("["):
            return json.loads(raw_stripped)
        raise ValueError(f"Could not parse tweets.js format: {path}")
    return json.loads(m.group(1))


def _tweet_body(obj: dict[str, Any]) -> dict[str, Any]:
    """Normalize tweet object from archive shapes."""
    t = obj.get("tweet") or obj
    text = t.get("full_text") or t.get("text") or ""
    # Unescape common entities lightly
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )
    return {
        "id": str(t.get("id_str") or t.get("id") or ""),
        "created_at": t.get("created_at") or "",
        "text": text,
        "retweeted": bool(t.get("retweeted")) or text.startswith("RT @"),
        "in_reply_to": t.get("in_reply_to_status_id_str") or t.get("in_reply_to_status_id"),
        "favorite_count": int(t.get("favorite_count") or 0),
        "retweet_count": int(t.get("retweet_count") or 0),
        "lang": t.get("lang") or "",
    }


def _is_high_signal(post: dict[str, Any], min_chars: int) -> bool:
    text = (post.get("text") or "").strip()
    if post.get("retweeted"):
        return False
    if len(text) < min_chars:
        return False
    # Drop pure link dumps
    if re.fullmatch(r"https?://\S+", text):
        return False
    return True


def iter_posts_from_raw(raw: Path, min_chars: int = 40) -> Iterator[dict[str, Any]]:
    raw = Path(raw)
    work = raw
    if raw.is_file() and raw.suffix.lower() == ".zip":
        extract_dir = raw.parent / f".extract_{raw.stem}"
        work = _extract_zip(raw, extract_dir)

    tweet_js = _find_tweet_js(work)
    if tweet_js is None:
        # Allow a plain JSONL or JSON of posts for non-X sources
        for name in ("posts.jsonl", "posts.json"):
            p = work / name if work.is_dir() else None
            if p and p.is_file():
                if p.suffix == ".jsonl":
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip():
                            yield json.loads(line)
                    return
                data = json.loads(p.read_text(encoding="utf-8"))
                for item in data:
                    yield item
                return
        raise FileNotFoundError(
            f"No tweets.js or posts.jsonl under {work}. "
            "Export your X archive and place it under data/raw/."
        )

    for obj in _load_tweets_js(tweet_js):
        post = _tweet_body(obj)
        if _is_high_signal(post, min_chars=min_chars):
            yield post


def run_prep(raw: str, out: str, min_chars: int = 40) -> int:
    raw_path = Path(raw)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for post in iter_posts_from_raw(raw_path, min_chars=min_chars):
            row = {
                "id": post.get("id") or f"row-{count}",
                "source": "x_archive",
                "text": post.get("text", ""),
                "created_at": post.get("created_at", ""),
                "meta": {
                    "favorite_count": post.get("favorite_count", 0),
                    "retweet_count": post.get("retweet_count", 0),
                    "in_reply_to": post.get("in_reply_to"),
                    "lang": post.get("lang", ""),
                    "exported_at": datetime.now(timezone.utc).isoformat(),
                },
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1

    print(f"Wrote {count} posts → {out_path}", file=sys.stderr)
    if count == 0:
        print("WARNING: zero posts extracted. Check archive path.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    # python -m mycelial_republic.data.prep --raw ... --out ...
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-chars", type=int, default=40)
    a = ap.parse_args()
    raise SystemExit(run_prep(a.raw, a.out, min_chars=a.min_chars))
