"""tg_harvest — sessionless Telegram public-channel harvest via t.me/s/ preview doors.

Doctrine door #1 (X_HARVEST_DOCTRINE_20260905): no login, no session, no account
surface — the public preview pages only. Paginates backwards with ?before=<id>.

Usage: python scripts/tg_harvest.py <slug> [max_posts]
Output: corpus/telegram/<slug>.jsonl  ({id, dt, text} per line, chronological)
"""

import json
import re
import subprocess
import sys
import time
from html import unescape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ALLOWED_HOST = "t.me"
SLUG_RE = re.compile(r"^[A-Za-z0-9_]{3,64}$")  # channel slug charset — no dots, no slashes
OUT_DIR = (REPO / "corpus" / "telegram").resolve()


def guard_url(url: str) -> None:
    from urllib.parse import urlparse
    p = urlparse(url)
    if p.scheme != "https" or p.hostname != ALLOWED_HOST or not p.path.startswith("/s/"):
        raise ValueError("outside preview-door allowlist: %r" % url)


def fetch(url: str) -> str:
    guard_url(url)
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", "Mozilla/5.0", url],
                       capture_output=True, text=True, timeout=40)
    return r.stdout


def safe_out(slug: str) -> Path:
    if not SLUG_RE.match(slug):
        raise ValueError("slug fails charset allowlist: %r" % slug)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = (OUT_DIR / (slug + ".jsonl")).resolve()
    if OUT_DIR.resolve() not in dest.parents:
        raise ValueError("resolved path escaped out dir: %r" % str(dest))
    return dest


def harvest(slug: str, max_posts: int) -> int:
    dest = safe_out(slug)
    posts, before = {}, None
    base = f"https://t.me/s/{slug}"
    while len(posts) < max_posts:
        html = fetch(base if not before else f"{base}?before={before}")
        ids = re.findall(r'data-post="([^"]+)"', html)
        times = re.findall(r'<time datetime="([^"]+)"', html)
        texts = re.findall(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', html, re.S)
        if not ids:
            break
        new = 0
        for i, pid in enumerate(ids):
            if pid in posts:
                continue
            txt = texts[i] if i < len(texts) else ""
            clean = unescape(re.sub(r"<br/?>", "\n", txt))
            clean = re.sub(r"<[^>]+>", "", clean).strip()
            posts[pid] = {"id": pid, "dt": times[i] if i < len(times) else "", "text": clean[:3000]}
            new += 1
        numeric = sorted(int(p.split("/")[-1]) for p in posts)
        before = numeric[0] if numeric else None
        if new == 0:
            break
        time.sleep(0.6)
    with open(dest, "w", encoding="utf-8") as f:
        for pid in sorted(posts, key=lambda p: int(p.split("/")[-1])):
            f.write(json.dumps(posts[pid], ensure_ascii=False) + "\n")
    return len(posts)


if __name__ == "__main__":
    slug = sys.argv[1]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    print(f"{slug}: {harvest(slug, cap)} posts banked -> corpus/telegram/{slug}.jsonl")
