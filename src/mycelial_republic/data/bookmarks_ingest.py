"""
Ingest browser bookmarks / saved-URL folders into posts JSONL.

Supports:
  - Chrome / Edge Bookmarks JSON (User Data/Default/Bookmarks)
  - Netscape bookmarks.html export
  - Plain text or JSONL: one URL per line, or {\"url\",\"title\",\"text\"?}

X (Twitter) in-app Bookmarks are NOT on disk — export via browser HTML
or paste URLs into data/bookmarks/urls.txt.

Threadreader URLs (threadreaderapp.com/thread/ID) are fetched as full unrolls
when network allows.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlparse


STATUS_RE = re.compile(
    r"(?:twitter\.com|x\.com)/(?:#!/)?(?:\w+)/status(?:es)?/(\d+)", re.I
)
THREADREADER_RE = re.compile(
    r"threadreaderapp\.com/(?:thread|scrolly)/(\d+)", re.I
)


def walk_chrome(node: dict, path: str = "", out: list | None = None) -> list:
    if out is None:
        out = []
    name = node.get("name", "")
    t = node.get("type")
    p = f"{path}/{name}" if path else name
    if t == "url":
        out.append({"title": name, "url": node.get("url", ""), "folder": path})
    for c in node.get("children") or []:
        walk_chrome(c, p, out)
    return out


def load_chrome_bookmarks(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: list[dict[str, str]] = []
    for k, v in (data.get("roots") or {}).items():
        if isinstance(v, dict):
            walk_chrome(v, k, out)
    return out


class _NetscapeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict[str, str]] = []
        self._folder_stack: list[str] = []
        self._pending_href: str | None = None
        self._capture = False
        self._buf = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag.lower() == "h3":
            self._capture = True
            self._buf = ""
            self._pending_href = None
        elif tag.lower() == "a":
            self._pending_href = ad.get("href", "")
            self._capture = True
            self._buf = ""

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "h3" and self._capture:
            self._folder_stack.append(self._buf.strip())
            self._capture = False
        elif tag.lower() == "a" and self._pending_href is not None:
            self.items.append(
                {
                    "title": self._buf.strip(),
                    "url": self._pending_href,
                    "folder": "/".join(self._folder_stack),
                }
            )
            self._pending_href = None
            self._capture = False

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf += data


def load_netscape_html(path: Path) -> list[dict[str, str]]:
    p = _NetscapeParser()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p.items


def load_urls_txt(path: Path) -> list[dict[str, str]]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("{"):
            d = json.loads(line)
            items.append(
                {
                    "title": d.get("title") or d.get("name") or "",
                    "url": d.get("url") or "",
                    "folder": d.get("folder") or "urls_txt",
                    "text": d.get("text") or "",
                }
            )
        else:
            items.append({"title": "", "url": line, "folder": "urls_txt"})
    return items


def load_bookmark_sources(path: Path) -> list[dict[str, str]]:
    """path: file or directory of bookmark dumps."""
    files: list[Path] = []
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = list(path.rglob("*"))
    items: list[dict[str, str]] = []
    for f in files:
        if not f.is_file():
            continue
        name = f.name.lower()
        try:
            if name == "bookmarks" or name.endswith(".json"):
                # Chrome JSON often has no extension
                raw = f.read_text(encoding="utf-8", errors="replace")
                if '"roots"' in raw[:500]:
                    items.extend(load_chrome_bookmarks(f))
                    continue
            if name.endswith(".html") or name.endswith(".htm"):
                items.extend(load_netscape_html(f))
                continue
            if name.endswith(".txt") or name.endswith(".jsonl"):
                items.extend(load_urls_txt(f))
        except (json.JSONDecodeError, OSError, UnicodeError) as e:
            print(f"skip {f}: {e}", file=sys.stderr)
    return items


def _get(url: str, timeout: float = 30.0) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MycelialRepublic/0.1 (+local; research)"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_threadreader(thread_id: str) -> str:
    html = _get(f"https://threadreaderapp.com/thread/{thread_id}")
    # crude text extract
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    # trim chrome
    if "Subscribe" in text:
        text = text.split("Subscribe", 1)[-1]
    if "Missing some Tweet" in text:
        text = text.split("Missing some Tweet")[0]
    return text.strip()


def fetch_status_text(status_id: str) -> str:
    try:
        data = json.loads(_get(f"https://api.fxtwitter.com/status/{status_id}"))
        tweet = data.get("tweet") or data
        return (tweet.get("text") or tweet.get("raw_text") or "").strip()
    except Exception:
        return ""


def item_to_row(item: dict[str, str], fetch: bool = True) -> dict[str, Any] | None:
    url = (item.get("url") or "").strip()
    title = (item.get("title") or "").strip()
    folder = item.get("folder") or ""
    text = (item.get("text") or "").strip()
    source = "bookmarks"
    rid = ""

    m = THREADREADER_RE.search(url)
    if m:
        rid = m.group(1)
        source = "threadreader_bookmark"
        if fetch and len(text) < 80:
            try:
                text = fetch_threadreader(rid)
            except Exception as e:
                print(f"threadreader fail {rid}: {e}", file=sys.stderr)
    else:
        m2 = STATUS_RE.search(url)
        if m2:
            rid = m2.group(1)
            source = "x_bookmark"
            if fetch and len(text) < 40:
                text = fetch_status_text(rid)

    if not text and title and url:
        text = f"{title}\n{url}"
    if len(text) < 25:
        return None

    return {
        "id": rid or f"bm-{abs(hash(url or text)) & 0xFFFFFFFF:x}",
        "source": source,
        "text": text,
        "created_at": "",
        "meta": {
            "url": url,
            "title": title,
            "folder": folder,
            "exported_at": datetime.now(timezone.utc).isoformat(),
        },
    }


def run_bookmarks_ingest(
    path: str,
    out: str,
    seed: str | None = None,
    fetch: bool = True,
    folder_filter: str = "",
) -> int:
    items = load_bookmark_sources(Path(path))
    if folder_filter:
        fl = folder_filter.lower()
        items = [i for i in items if fl in (i.get("folder") or "").lower()]
    print(f"bookmark items loaded: {len(items)}", file=sys.stderr)

    rows: list[dict[str, Any]] = []
    if seed and Path(seed).is_file():
        for line in Path(seed).read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))

    for it in items:
        row = item_to_row(it, fetch=fetch)
        if row:
            rows.append(row)

    # dedupe by id / text
    by_id: dict[str, dict] = {}
    for r in rows:
        rid = str(r.get("id"))
        if rid not in by_id or len(r.get("text") or "") > len(by_id[rid].get("text") or ""):
            by_id[rid] = r
    merged = list(by_id.values())
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as fh:
        for r in merged:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(merged)} → {outp}", file=sys.stderr)
    return 0 if merged else 2


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="Bookmarks file or folder drop-zone")
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", default="")
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--folder", default="", help="Only this folder name substring")
    a = ap.parse_args(argv)
    return run_bookmarks_ingest(
        a.path, a.out, seed=a.seed or None, fetch=not a.no_fetch, folder_filter=a.folder
    )


if __name__ == "__main__":
    raise SystemExit(main())
