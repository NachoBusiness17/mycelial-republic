"""Fetch old.reddit top-month HTML pages via curl (browser UA, follow redirects)
for the quantization-compression reddit sweep. Saves raw HTML + extracts candidate
post rows (title, score, comments, date, permalink) by regex on old.reddit markup.

Security posture: literal https URLs against host allowlist old.reddit.com only;
output paths resolved inside the sweep evidence dir; no user input.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_HOST = "old.reddit.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]

TITLE_RE = re.compile(
    r'<a class="title[^"]*"\s+href="([^"]+)"[^>]*>(.*?)</a>', re.S)
SCORE_RE = re.compile(
    r'<div class="score unvoted"[^>]*title="(\d+)"')
COMMENTS_RE = re.compile(
    r'<a[^>]*class="comments[^"]*"[^>]*href="([^"]+)"[^>]*>\s*(\d+)\s*comments', re.S)
TIME_RE = re.compile(r'<time[^>]*datetime="([^"]+)"')
TAGLINE_RE = re.compile(
    r'<p class="tagline ">.*?<a[^>]*class="author[^"]*"[^>]*>([^<]*)</a>.*?'
    r'<time[^>]*title="([^"]*)"[^>]*datetime="([^"]*)"', re.S)


def curl_fetch(url, dest):
    if url.split("/")[2] != ALLOWED_HOST:
        raise ValueError("blocked non-allowlist host")
    cp = subprocess.run(
        ["curl", "-s", "-L", "-m", "40", "-A", UA, url, "-o", str(dest)],
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return cp.returncode


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    all_rows = []
    for sub in SUBS:
        dest = OUT_DIR / f"{sub}_top_month.html"
        rc = curl_fetch(f"https://{ALLOWED_HOST}/r/{sub}/top/?t=month", dest)
        html = dest.read_text(encoding="utf-8", errors="replace") if dest.exists() else ""
        size = len(html)
        blocked = "Welcome to Reddit" in html[:3000] and "thing" not in html[:20000]
        rows = []
        # split into thing blocks
        things = html.split('<div class=" thing')
        for t in things[1:]:
            tm = TITLE_RE.search(t)
            if not tm:
                continue
            href, title = tm.group(1), strip_tags(tm.group(2))
            if href.startswith("/r/"):
                href = f"https://{ALLOWED_HOST}{href}"
            elif href.startswith("/"):
                href = f"https://{ALLOWED_HOST}{href}"
            cm = COMMENTS_RE.search(t)
            tmm = TIME_RE.search(t)
            sm = SCORE_RE.search(t)
            rows.append({
                "sub": sub,
                "title": title,
                "score": int(sm.group(1)) if sm else None,
                "comments": int(cm.group(2)) if cm else 0,
                "date": (tmm.group(1)[:10] if tmm else "unknown"),
                "permalink": cm.group(1) if cm else href,
                "link": href,
            })
        all_rows.extend(rows)
        print(f"== r/{sub}: curl rc={rc}, html_bytes={size}, blocked_page={blocked}, posts={len(rows)}")
    all_rows.sort(key=lambda r: ((r["score"] or 0) + r["comments"]), reverse=True)
    (OUT_DIR / "candidates.json").write_text(json.dumps(all_rows, indent=1), encoding="utf-8")
    print(f"\nTOTAL candidates: {len(all_rows)}")
    for i, r in enumerate(all_rows, 1):
        print(f"{i:2d}. [{r['sub']}] {str(r['score']):>5}pts {r['comments']:4d}c "
              f"{r['date']} | {r['title'][:105]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
