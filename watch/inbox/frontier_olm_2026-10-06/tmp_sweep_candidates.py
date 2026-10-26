"""Pass-1 candidate extraction for the quantization-compression reddit sweep.

Fetches each subreddit's top-month listing through safereddit.com (redlib
instance, Anubis PoW passed honestly per its public protocol) and extracts
post rows from redlib HTML markup. Saves raw HTML evidence + candidates.json.

Security posture: literal https URLs, instance host fixed to safereddit.com;
output paths resolved inside the sweep evidence dir; no user input.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tmp_anubis_read import read_page, OUT_DIR  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
INST = "safereddit.com"
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]

POST_SPLIT = re.compile(r'<div class="post"[^>]*>')
TITLE_RE = re.compile(r'<a href="(/r/[^"]+/comments/[^"]+)"[^>]*>(.*?)</a>', re.S)
SCORE_RE = re.compile(r'<p class="post_score"[^>]*title="(\d+)"[^>]*>[\s\S]*?</p>', re.S)
COMM_RE = re.compile(r'<a href="(/r/[^"]+/comments/[^"]+)"[^>]*class="post_comments"[^>]*>[\s\S]*?(\d+)\s*comments?')
FLAIR_RE = re.compile(r'<span class="post_flair[^"]*"[^>]*>([\s\S]*?)</span>')
BODY_RE = re.compile(r'<div class="post_body[^"]*">([\s\S]*?)</div>')
TIME_RE = re.compile(r'<time datetime="([^"]+)"')
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(s):
    return re.sub(r"\s+", " ", TAG_RE.sub("", html_unescape(s))).strip()


def html_unescape(s):
    import html as _h
    return _h.unescape(s)


def main():
    rows = []
    for sub in SUBS:
        dest = OUT_DIR / f"{sub}_top_month.html"
        status, body = read_page(f"https://{INST}/r/{sub}/top?t=month")
        dest.write_text(body, encoding="utf-8")
        posts = POST_SPLIT.split(body)[1:]
        n_ok = 0
        for p in posts:
            tm = TITLE_RE.search(p)
            if not tm:
                continue
            href = "https://" + INST + tm.group(1)
            title = strip_tags(tm.group(2))
            sm = SCORE_RE.search(p)
            cm = COMM_RE.search(p)
            tim = TIME_RE.search(p)
            bm = BODY_RE.search(p)
            rows.append({
                "sub": sub,
                "title": title,
                "score": int(sm.group(1)) if sm else None,
                "comments": int(cm.group(2)) if cm else 0,
                "date": (tim.group(1)[:10] if tim else "unknown"),
                "flair": strip_tags(FLAIR_RE.search(p).group(1)) if FLAIR_RE.search(p) else "",
                "selftext_head": strip_tags(bm.group(1))[:300] if bm else "",
                "redlib_url": href,
                "reddit_url": "https://old.reddit.com" + tm.group(1),
            })
            n_ok += 1
        print(f"== r/{sub}: status={status} bytes={len(body)} posts={n_ok}")
    rows.sort(key=lambda r: ((r["score"] or 0) + r["comments"]), reverse=True)
    (OUT_DIR / "candidates.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"\nTOTAL candidates: {len(rows)}")
    for i, r in enumerate(rows, 1):
        print(f"{i:2d}. [{r['sub']}|{r['flair'][:12]}] {str(r['score']):>5}pts "
              f"{r['comments']:4d}c {r['date']} | {r['title'][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
