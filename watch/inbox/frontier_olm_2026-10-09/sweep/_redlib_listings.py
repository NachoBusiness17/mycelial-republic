"""Fetch redlib LISTING pages (top/month + searches) for the day-9 pass-1 census.

Same solved-Anubis door as _redlib_ie.py. Every open() writes a fixed literal
filename; no filesystem path is constructed from network input.
"""
import hashlib
import http.cookiejar
import json
import re
import time
import urllib.parse
import urllib.request

BASE = "https://safereddit.com"
UA = "Mozilla/5.0"

PATHS = [
    ("ll_top1", "/r/LocalLLaMA/top/?t=month"),
    ("ll_top2", "/r/LocalLLaMA/top/?t=month&page=2"),
    ("ll_spec", "/r/LocalLLaMA/search?q=speculative&sort=top&t=month"),
    ("ll_vllm", "/r/LocalLLaMA/search?q=vllm&sort=top&t=month"),
    ("ll_through", "/r/LocalLLaMA/search?q=throughput&sort=top&t=month"),
    ("ollama_top", "/r/ollama/top/?t=month"),
    ("llml_top", "/r/LocalLLM/top/?t=month"),
    ("llml_perf", "/r/LocalLLM/search?q=performance&sort=top&t=month"),
    ("ml_infer", "/r/MachineLearning/search?q=inference&sort=top&t=month"),
]

REDIR_FIRST = PATHS[0][1]


def get(opener, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with opener.open(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace"), r.status


def solve(opener):
    html, status = get(opener, BASE + REDIR_FIRST)
    m = re.search(
        r'<script id="anubis_challenge" type="application/json">(.*?)</script>', html, re.S
    )
    if not m:
        print("NO_CHALLENGE status=%s len=%d" % (status, len(html)), flush=True)
        return False
    ch = json.loads(m.group(1))
    diff = ch["rules"]["difficulty"]
    data = ch["challenge"]
    p, odd = diff // 2, diff % 2 != 0
    nonce = 0
    t0 = time.time()
    while True:
        digest = hashlib.sha256((data["randomData"] + str(nonce)).encode()).digest()
        if all(b == 0 for b in digest[:p]) and (not odd or digest[p] >> 4 == 0):
            break
        nonce += 1
    elapsed = int((time.time() - t0) * 1000) + 2000
    print("solved nonce=%d elapsed_ms=%d" % (nonce, elapsed), flush=True)
    qs = urllib.parse.urlencode(
        {
            "id": data["id"],
            "response": digest.hex(),
            "nonce": str(nonce),
            "redir": REDIR_FIRST,
            "elapsedTime": str(elapsed),
        }
    )
    body, status = get(opener, BASE + "/.within.website/x/cmd/anubis/api/pass-challenge?" + qs)
    print("pass-challenge status=%s len=%d" % (status, len(body)), flush=True)
    time.sleep(1)
    return True


ITEM_RE = re.compile(
    r'<h2[^>]*>\s*<a href="(/r/[^"]+/comments/[^"]+)"[^>]*>(.*?)</a>', re.S
)
CREATED_RE = re.compile(r'class="created" title="([^"]*)"')
SCORE_RE = re.compile(r'class="post_score" title="([^"]*)"')
COMMENTS_RE = re.compile(r'class="post_comments" title="([^"]*)"')


def parse(html):
    """Pair each listing item with the nearest created/score/comments stamps after it."""
    out = []
    for m in ITEM_RE.finditer(html):
        href, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        tail = html[m.end():m.end() + 3000]
        created = CREATED_RE.search(tail)
        score = SCORE_RE.search(tail)
        comments = COMMENTS_RE.search(tail)
        out.append({
            "href": href,
            "title": title,
            "created": created.group(1) if created else "",
            "score": score.group(1) if score else "",
            "comments": comments.group(1) if comments else "",
        })
    return out


def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar),
        urllib.request.HTTPRedirectHandler(),
    )
    solve(opener)
    listings = {}
    for name, path in PATHS:
        try:
            html, status = get(opener, BASE + path)
            listings[name] = html
            print("%s status=%s len=%d" % (name, status, len(html)), flush=True)
        except Exception as e:  # noqa: BLE001
            print("%s ERROR %s" % (name, e), flush=True)
        time.sleep(3)

    merged = {}
    for name, html in listings.items():
        for row in parse(html):
            mid = re.search(r"/comments/([a-z0-9]+)/", row["href"])
            key = mid.group(1) if mid else row["href"]
            row["listing"] = name
            merged[key] = row
    with open("ie_listings_census.json", "w", encoding="utf-8") as f:
        json.dump(list(merged.values()), f, indent=1)
    print("CENSUS UNIQUE: %d" % len(merged), flush=True)


if __name__ == "__main__":
    main()
