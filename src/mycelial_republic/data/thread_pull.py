"""
Full-thread + media ingest for high-signal X roots.

For each status ID:
  1) fxtwitter: root text, note-tweet body, media catalog (photos/video URLs, duration)
  2) threadreader (via jina reader when needed): full multi-tweet unroll text
  3) Assemble training rows:
       - one stitched thread document (preferred for LoRA)
       - optional per-segment rows
       - media manifest (URLs + type) embedded as text for the model

Video/image *pixels* are not transcribed here (no Whisper/OCR by default);
URLs + structure are kept so multimodal fine-tunes or later OCR can attach.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _get(url: str, timeout: float = 45.0) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MycelialRepublic/0.2",
            "Accept": "*/*",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str) -> dict[str, Any]:
    return json.loads(_get(url).decode("utf-8", errors="replace"))


def _get_text(url: str) -> str:
    return _get(url).decode("utf-8", errors="replace")


def fetch_fxtwitter(status_id: str) -> dict[str, Any] | None:
    try:
        data = _get_json(f"https://api.fxtwitter.com/status/{status_id}")
        return data.get("tweet") or data
    except Exception as e:
        print(f"fxtwitter fail {status_id}: {e}", file=sys.stderr)
        return None


def extract_media(tweet: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    media = tweet.get("media") or {}
    for item in media.get("all") or []:
        if not isinstance(item, dict):
            continue
        mtype = item.get("type") or "unknown"
        entry = {
            "type": mtype,
            "id": str(item.get("id") or ""),
            "url": item.get("url") or item.get("thumbnail_url") or "",
            "thumbnail_url": item.get("thumbnail_url") or "",
            "alt": item.get("altText") or item.get("alt_text") or item.get("alt") or "",
            "duration_s": item.get("duration"),
            "width": item.get("width"),
            "height": item.get("height"),
        }
        # best mp4 if variants
        for v in item.get("formats") or item.get("variants") or []:
            if not isinstance(v, dict):
                continue
            u = v.get("url") or ""
            if "mp4" in (v.get("container") or "") or u.endswith(".mp4") or "video/mp4" in (
                v.get("content_type") or ""
            ):
                # prefer higher bitrate
                if not entry.get("url") or (v.get("bitrate") or 0) > 500_000:
                    entry["url"] = u
        out.append(entry)
    return out


def media_to_text_block(media: list[dict[str, Any]]) -> str:
    if not media:
        return ""
    lines = ["", "### Media attached"]
    for i, m in enumerate(media, 1):
        alt = (m.get("alt") or "").strip()
        dur = m.get("duration_s")
        dur_s = f" duration={dur}s" if dur is not None else ""
        lines.append(
            f"[{m.get('type','media').upper()} {i}{dur_s}] {m.get('url','')}"
            + (f"\n  alt: {alt}" if alt else "")
        )
    return "\n".join(lines)


def _is_noise_unroll(text: str, root: str) -> bool:
    """Detect jina/threadreader sidebar pollution (wrong thread / author index)."""
    if not text or len(text) < 400:
        return True
    # Classic wrong-page fingerprints from user index dumps
    noise_hits = 0
    for sig in (
        "Barry Soetoro",
        "Black Nobility families represent",
        "More from @NachoQuixotic",
        "Did Thread Reader help you today",
        "Become a Premium Member",
    ):
        if sig in text:
            noise_hits += 1
    if noise_hits >= 2:
        return True
    # Unroll should share some content with root (when root is long enough)
    root_words = {w.lower() for w in re.findall(r"[A-Za-z]{5,}", root or "")[:40]}
    if len(root_words) >= 8:
        body_l = text.lower()
        overlap = sum(1 for w in root_words if w in body_l)
        if overlap < max(3, len(root_words) // 5):
            return True
    return False


def fetch_threadreader_text(status_id: str, root_text: str = "") -> str:
    """Best-effort full unroll via jina → threadreader."""
    urls = [
        f"https://r.jina.ai/http://threadreaderapp.com/thread/{status_id}",
        f"https://r.jina.ai/https://threadreaderapp.com/thread/{status_id}",
    ]
    for url in urls:
        try:
            text = _get_text(url)
            # strip jina header noise
            if "Markdown Content:" in text:
                text = text.split("Markdown Content:", 1)[-1]
            # Prefer content before "More from" if present after real body
            if "\n## More from" in text:
                head, tail = text.split("\n## More from", 1)
                if len(head) > 800:
                    text = head
            text = re.sub(r"!\[.*?\]\(.*?\)", " ", text)
            text = re.sub(r"\[Image \d+.*?\]\(.*?\)", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            if _is_noise_unroll(text, root_text):
                print(f"threadreader noise skipped {status_id}", file=sys.stderr)
                continue
            if len(text) > 400:
                return text
        except Exception as e:
            print(f"threadreader fail {status_id}: {e}", file=sys.stderr)
    return ""


def assemble_document(
    status_id: str,
    tweet: dict[str, Any],
    thread_extra: str,
    media: list[dict[str, Any]],
) -> str:
    author = ""
    a = tweet.get("author") or {}
    if isinstance(a, dict):
        author = a.get("screen_name") or a.get("name") or ""
    root = (tweet.get("text") or "").strip()
    parts = [
        f"# Thread root {status_id}",
        f"Author: @{author}" if author else "",
        f"URL: https://x.com/i/status/{status_id}",
        f"Created: {tweet.get('created_at') or ''}",
        "",
        "## Root text",
        root,
    ]
    # if threadreader gave longer body, append as full unroll
    if thread_extra and len(thread_extra) > len(root) + 200:
        parts += ["", "## Full thread unroll (subposts)", thread_extra[:120_000]]
    parts.append(media_to_text_block(media))
    if media:
        parts += [
            "",
            "## Media note",
            "Images/videos are linked above. Visual content is high-signal; "
            "treat attached media as part of the argument (screenshots, primary docs, cuts).",
        ]
    return "\n".join(p for p in parts if p is not None).strip()


def pull_one(status_id: str, sleep_s: float = 0.35) -> dict[str, Any] | None:
    status_id = re.sub(r"\D", "", status_id)
    if not status_id:
        return None
    tweet = fetch_fxtwitter(status_id)
    if not tweet:
        return None
    media = extract_media(tweet)
    # Threadreader often better for multi-post threads
    extra = ""
    # Prefer unroll when many replies or short root relative to thread nature
    replies = int(tweet.get("replies") or 0)
    root_len = len(tweet.get("text") or "")
    root_txt = (tweet.get("text") or "").strip()
    if replies >= 2 or root_len < 800 or tweet.get("is_note_tweet"):
        extra = fetch_threadreader_text(status_id, root_text=root_txt)
        time.sleep(sleep_s)
    doc = assemble_document(status_id, tweet, extra, media)
    author = ""
    a = tweet.get("author") or {}
    if isinstance(a, dict):
        author = a.get("screen_name") or ""
    return {
        "id": status_id,
        "source": "x_thread_full",
        "text": doc,
        "created_at": str(tweet.get("created_at") or ""),
        "meta": {
            "author": author,
            "url": f"https://x.com/i/status/{status_id}",
            "likes": tweet.get("likes"),
            "replies": tweet.get("replies"),
            "views": tweet.get("views"),
            "is_note_tweet": tweet.get("is_note_tweet"),
            "media": media,
            "media_count": len(media),
            "thread_unroll_chars": len(extra),
            "root_chars": len(tweet.get("text") or ""),
            "exported_at": datetime.now(timezone.utc).isoformat(),
        },
    }


def run_thread_pull(
    ids: list[str],
    out: str,
    seed: str | None = None,
    sleep_s: float = 0.4,
) -> int:
    rows: list[dict[str, Any]] = []
    if seed and Path(seed).is_file():
        for line in Path(seed).read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))

    ok, fail = 0, 0
    for i, sid in enumerate(ids):
        print(f"[{i+1}/{len(ids)}] {sid}", file=sys.stderr)
        row = pull_one(sid, sleep_s=sleep_s)
        if row:
            rows.append(row)
            ok += 1
            print(
                f"  ok root={row['meta']['root_chars']} unroll={row['meta']['thread_unroll_chars']} "
                f"media={row['meta']['media_count']} total_text={len(row['text'])}",
                file=sys.stderr,
            )
        else:
            fail += 1
        time.sleep(sleep_s)

    # dedupe: prefer longer text for same id
    by: dict[str, dict] = {}
    for r in rows:
        rid = str(r.get("id"))
        if rid not in by or len(r.get("text") or "") > len(by[rid].get("text") or ""):
            by[rid] = r
    merged = list(by.values())
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as fh:
        for r in merged:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(merged)} (ok={ok} fail={fail}) → {outp}", file=sys.stderr)
    return 0 if merged else 2


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Pull full threads + media into JSONL")
    ap.add_argument("--ids-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", default="")
    ap.add_argument("--sleep", type=float, default=0.4)
    a = ap.parse_args(argv)
    ids = [
        ln.strip()
        for ln in Path(a.ids_file).read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    return run_thread_pull(ids, a.out, seed=a.seed or None, sleep_s=a.sleep)


if __name__ == "__main__":
    raise SystemExit(main())
