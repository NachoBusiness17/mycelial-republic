"""Pass-2 deep reads for the quantization-compression reddit sweep.

Fetches full thread pages through the safereddit.com redlib door (Anubis PoW
passed per its public protocol), extracts title, author, date, score, post
body, and top comments. Saves raw HTML + parsed JSON per thread.

Security posture: URLs built from literal comment-path constants against the
fixed instance host; output paths resolved inside the sweep evidence dir.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tmp_anubis_read import read_page, OUT_DIR  # noqa: E402

INST = "safereddit.com"

THREADS = [
    ("d1_q4_vs_q8_0p6b_decision", "/r/LocalLLM/comments/1q4cost_this_is_a_placeholder"),
]

# Real thread paths are passed in via threads.json (written by the driver step).
THREADS_FILE = Path(__file__).resolve().parent / "deep_read_urls.json"

POST_TITLE = re.compile(r'<h1 class="post_title[^"]*">\s*<a[^>]*>([\s\S]*?)</a>', re.S)
POST_AUTHOR = re.compile(r'<a class="post_author[^"]*"[^>]*>([^<]+)</a>')
POST_TIME = re.compile(r'<time datetime="([^"]+)"')
POST_SCORE = re.compile(r'<p class="post_score"[^>]*title="([^"]+)"')
POST_BODY = re.compile(r'<div class="post_body[^"]*"[\s\S]*?</div>\s*(?:</div>)?', re.S)
POST_BODY_LAZY = re.compile(r'<div class="post_body[^"]*">')
COMMENT_SCORE = re.compile(r'<p class="comment_score"[^>]*>([^<]+)</p>')
COMMENT_BODY = re.compile(r'<div class="comment_body[^"]*">([\s\S]*?)</div>')
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(s):
    import html as _h
    return re.sub(r"\s+", " ", TAG_RE.sub("", _h.unescape(s))).strip()


def parse_thread(url, body):
    title = POST_TITLE.search(body)
    author = POST_AUTHOR.search(body)
    time_m = POST_TIME.search(body)
    score = POST_SCORE.search(body)
    # post body: first post_body div; capture until the closing comments marker
    m = POST_BODY_LAZY.search(body)
    pbody = ""
    if m:
        seg = body[m.end():]
        # crude: cut at the comments divider or end of div stack
        cut = seg.find('class="comment"')
        if cut == -1:
            cut = seg.find("post_comments")
        if cut == -1:
            cut = min(len(seg), 12000)
        pbody = strip_tags(seg[:cut])[:4000]
    comments = []
    for cs, cb in zip(COMMENT_SCORE.finditer(body), COMMENT_BODY.finditer(body)):
        comments.append({"score": cs.group(1).strip(), "text": strip_tags(cb.group(1))[:1500]})
    return {
        "url": url,
        "title": strip_tags(title.group(1)) if title else "",
        "author": author.group(1) if author else "",
        "date": time_m.group(1)[:10] if time_m else "unknown",
        "score": score.group(1) if score else "",
        "post_body": pbody,
        "n_comments_parsed": len(comments),
        "comments": comments[:12],
    }


def main():
    urls = json.loads(THREADS_FILE.read_text(encoding="utf-8"))
    results = []
    for label, path in urls:
        url = f"https://{INST}{path}"
        status, body = read_page(url)
        (OUT_DIR / f"thread_{label}.html").write_text(body, encoding="utf-8")
        parsed = parse_thread(url, body)
        parsed["label"] = label
        parsed["status"] = status
        results.append(parsed)
        print(f"== {label}: status={status} bytes={len(body)} title={parsed['title'][:70]}")
        print(f"   date={parsed['date']} score={parsed['score']} body_len={len(parsed['post_body'])} comments={parsed['n_comments_parsed']}")
    Path(__file__).resolve().parent.joinpath("deep_reads.json").write_text(
        json.dumps(results, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
