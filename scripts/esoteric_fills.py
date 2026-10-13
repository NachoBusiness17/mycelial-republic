#!/usr/bin/env python3
"""esoteric_fills.py — Steiner Higher Worlds + Duncan's Ritual corpus fills.

Session-close queue item (2026-09-19): "rsarchive/sacred-texts URL-pattern fills
(throttled tonight)". The exact pattern died with the updated session, so this
crawler re-derives it from the index pages: fetch index, discover chapter hrefs,
fetch each with a polite sleep, save raw text into the esoteric canon.

Throttle: >=2.5s between remote hits, https-only, host-pinned (same SSRF
posture as scripts/vision_triage_pool.py), bounded crawl.

Output: memory/corpus/esoteric_canon/steiner_higher_worlds/*.txt
        memory/corpus/esoteric_canon/duncans_ritual/*.txt
        memory/runs/the50/esoteric_fills.json (honest log: fetched vs failed)
"""
from __future__ import annotations

import ipaddress
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "memory" / "corpus" / "esoteric_canon"
RUNS = ROOT / "memory" / "runs" / "the50"
SLEEP = 2.5
UA = {"User-Agent": "mag-esoteric-fills/1.0 (local research corpus; throttled)"}

WORKS = [
    {
        "name": "steiner_higher_worlds",
        "index": "https://rsarchive.org/Books/GA010/",
        "allowed_host": "rsarchive.org",
        "link_filter": re.compile(r"English/.*\.php$|English/[^/]+/$", re.I),
        "chapter_filter": re.compile(r"\.php$|/[^/]+/$", re.I),
    },
    {
        "name": "duncans_ritual",
        "index": "https://www.sacred-texts.com/mas/dun/",
        "allowed_host": "www.sacred-texts.com",
        "link_filter": re.compile(r"dun\d+\.htm$", re.I),
        "chapter_filter": re.compile(r"dun\d+\.htm$", re.I),
    },
]


def guarded_get(url: str, allowed_host: str, timeout: int = 60) -> str:
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname != allowed_host:
        raise ValueError("host not allowed")
    for _f, _s, _pr, _c, sa in socket.getaddrinfo(p.hostname, 443):
        if not ipaddress.ip_address(sa[0]).is_global:
            raise ValueError("resolved to non-global address")
    req = urllib.request.Request(url, headers=UA)
    opener = urllib.request.build_opener(_NoRedirect())
    with opener.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def strip_html(html: str) -> str:
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags = re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"&nbsp;?", " ", txt)
    txt = re.sub(r"&amp;", "&", txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n\n", txt)
    return txt.strip()


def crawl(work: dict, log: dict) -> None:
    out_dir = OUT / work["name"]
    out_dir.mkdir(parents=True, exist_ok=True)
    idx_url = work["index"]
    try:
        idx_html = guarded_get(idx_url, work["allowed_host"])
    except Exception as e:
        log["failed"].append({"step": "index", "url": idx_url, "error": str(e)[:160]})
        return
    time.sleep(SLEEP)
    base = idx_url if idx_url.endswith("/") else idx_url.rsplit("/", 1)[0] + "/"
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', idx_html, flags=re.I)
    chapters = []
    seen = set()
    for h in hrefs:
        if not work["link_filter"].search(h):
            continue
        full = urllib.parse.urljoin(base, h)
        if full in seen:
            continue
        seen.add(full)
        chapters.append(full)
    log["index"].append({"url": idx_url, "chapters_found": len(chapters)})
    for i, ch in enumerate(chapters[:24]):
        slug = re.sub(r"[^a-z0-9]+", "_", ch.rsplit("/", 2)[-2] if ch.endswith("/")
                      else ch.rsplit("/", 1)[-1]).strip("_")[:60] or f"ch_{i:02d}"
        try:
            html = guarded_get(ch, work["allowed_host"])
            txt = strip_html(html)
            if len(txt) < 400:
                raise RuntimeError(f"too short after strip ({len(txt)} chars)")
            (out_dir / f"{i:02d}_{slug}.txt").write_text(txt, encoding="utf-8")
            log["fetched"].append({"url": ch, "chars": len(txt)})
        except Exception as e:
            log["failed"].append({"step": "chapter", "url": ch, "error": str(e)[:160]})
        time.sleep(SLEEP)


def main() -> int:
    RUNS.mkdir(parents=True, exist_ok=True)
    log = {"fetched": [], "failed": [], "index": [],
           "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    for w in WORKS:
        print(f"=== {w['name']} from {w['index']}", flush=True)
        crawl(w, log)
        print(f"    fetched={len(log['fetched'])} failed={len(log['failed'])}", flush=True)
    (RUNS / "esoteric_fills.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"DONE fetched={len(log['fetched'])} failed={len(log['failed'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
