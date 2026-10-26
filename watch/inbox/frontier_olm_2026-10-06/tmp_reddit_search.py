"""Reddit search via safereddit.com (redlib proxies Reddit search) for the
quantization-compression sweep pass 1.

Fetches /r/<sub>/search?q=<term>&restrict_sr=on&t=month&sort=top through the
Anubis-gated redlib door and extracts post rows.

Security posture: literal https URLs against the fixed instance host; search
terms from the module constant; output paths resolved inside the sweep dir.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tmp_anubis_read import read_page, OUT_DIR  # noqa: E402

INST = "safereddit.com"
SEARCHES = [
    ("LocalLLaMA", "quantization"),
    ("LocalLLaMA", "KV cache quantization"),
    ("LocalLLaMA", "Q4_K_M"),
    ("LocalLLaMA", "IQ2"),
    ("LocalLLaMA", "ternary"),
    ("LocalLLM", "quantization"),
    ("LocalLLM", "quantized accuracy"),
    ("ollama", "quantization"),
    ("ollama", "KV cache"),
    ("MachineLearning", "quantization"),
]

POST_SPLIT = re.compile(r'<div class="post"[^>]*>')
TITLE_RE = re.compile(r'<a href="(/r/[^"]+/comments/[^"]+)"[^>]*>(.*?)</a>', re.S)
COMM_RE = re.compile(r'class="post_comments"[^>]*>[\s\S]*?(\d+)\s*comments?')
TIME_RE = re.compile(r'<time[^>]*datetime="([^"]+)"')
FLAIR_RE = re.compile(r'<span class="post_flair[^"]*"[^>]*>([\s\S]*?)</span>')
BODY_RE = re.compile(r'<div class="post_body[^"]*">([\s\S]*?)</div>')
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(s):
    import html as _h
    return re.sub(r"\s+", " ", TAG_RE.sub("", _h.unescape(s))).strip()


def parse_posts(body, label):
    rows = []
    for p in POST_SPLIT.split(body)[1:]:
        tm = TITLE_RE.search(p)
        if not tm:
            continue
        cm = COMM_RE.search(p)
        tim = TIME_RE.search(p)
        bm = BODY_RE.search(p)
        fl = FLAIR_RE.search(p)
        rows.append({
            "src": label,
            "title": strip_tags(tm.group(2)),
            "comments": int(cm.group(1)) if cm else 0,
            "date": (tim.group(1)[:10] if tim else "unknown"),
            "flair": strip_tags(fl.group(1)) if fl else "",
            "selftext_head": strip_tags(bm.group(1))[:300] if bm else "",
            "redlib_url": "https://" + INST + tm.group(1),
            "reddit_url": "https://old.reddit.com" + tm.group(1),
        })
    return rows


def main():
    rows = []
    for sub, term in SEARCHES:
        url = (f"https://{INST}/r/{sub}/search?q={term.replace(' ', '+')}"
               f"&restrict_sr=on&t=month&sort=top")
        status, body = read_page(url)
        stamp = re.sub(r"[^A-Za-z0-9]+", "_", f"{sub}_{term}")[:40]
        (OUT_DIR / f"search_{stamp}.html").write_text(body, encoding="utf-8")
        got = parse_posts(body, f"{sub}:{term}")
        rows.extend(got)
        print(f"== r/{sub} q='{term}': status={status} bytes={len(body)} posts={len(got)}")
    # dedupe by reddit_url
    seen, uniq = set(), []
    for r in rows:
        if r["reddit_url"] in seen:
            continue
        seen.add(r["reddit_url"])
        uniq.append(r)
    uniq.sort(key=lambda r: -r["comments"])
    (OUT_DIR / "search_candidates.json").write_text(
        json.dumps(uniq, indent=1), encoding="utf-8")
    print(f"\nTOTAL search candidates (deduped): {len(uniq)}")
    for i, r in enumerate(uniq, 1):
        print(f"{i:2d}. [{r['src']}|{r['flair'][:10]}] {r['comments']:4d}c "
              f"{r['date']} | {r['title'][:95]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
