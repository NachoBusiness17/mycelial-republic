"""Confirmation pass, part 2b: corrected canonical URLs from Algolia + 49807413 debug."""
import json
import re
import urllib.request
import urllib.error
import urllib.parse
import time

ALLOWED_HOSTS = {
    "arxiv.org", "www.arxiv.org", "export.arxiv.org", "hn.algolia.com",
    "duane.sh", "www.duane.sh", "dirac.run", "www.dirac.run",
    "raw.githubusercontent.com", "blog.cloudflare.com", "www.raspberrypi.com",
    "api.fxtwitter.com", "www.reddit.com", "old.reddit.com", "cactuscompute.com",
}


def _host_ok(host):
    return (host or "").lower() in ALLOWED_HOSTS


class GuardedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _host_ok(urllib.parse.urlsplit(newurl).hostname):
            raise urllib.error.URLError(f"redirect blocked: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(GuardedRedirect)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(url, timeout=45):
    scheme, host = urllib.parse.urlsplit(url)[:2]
    if scheme != "https" or not _host_ok(host):
        raise urllib.error.URLError(f"blocked url: {url}")
    req = urllib.request.Request(url, headers=UA)
    with OPENER.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).lower()


def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s)


def full_text(obj):
    if not isinstance(obj, dict):
        return ""
    parts = []
    for k in ("title", "story_title", "comment_text", "story_text", "text"):
        v = obj.get(k)
        if isinstance(v, str):
            parts.append(v)
    for ch in obj.get("children") or []:
        parts.append(full_text(ch))
    return " ".join(parts)


print("=== 49807413 Ask HN retry ===")
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/items/49807413"))
    blob = norm(full_text(data))
    print(f"  blob {len(blob)} chars; children={len(data.get('children') or [])}")
    for n in ["cost-effective infra to host it", "almost never worth it", "few-shot prompt"]:
        print(f"  needle {n[:36]!r}: {'HIT' if norm(n) in blob else 'MISS'}")
except Exception as e:
    print(f"  DEAD {type(e).__name__}: {e}")

print()
print("=== Cactus Needle 3 author comment probe ===")
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/items/49748553"))
    blob = norm(full_text(data))
    for n in ["360b", "n-gram", "engram"]:
        print(f"  needle {n!r}: {'HIT' if norm(n) in blob else 'MISS'}")
except Exception as e:
    print(f"  DEAD {type(e).__name__}: {e}")

EXTERNAL = [
    ("duane.sh post (Algolia URL)", "https://duane.sh/a/fine-tuning-qwen-local-minutes",
     ["71% less cost", "rank 32", "every position equally often"]),
    ("dirac.run EasyCommand post", "https://dirac.run/posts/easycommand",
     ["401,975", "212/300", "apache-2.0"]),
    ("Clef blog (Algolia URL)", "https://blog.cloudflare.com/clef-decision-models/",
     ["rank-256", "qwen3.8-27b"]),
]

print()
print("=== External pages, corrected URLs ===")
results = {}
for label, url, needles in EXTERNAL:
    try:
        html = fetch(url)
        blob = norm(strip_html(html))
        hits = [n for n in needles if norm(n) in blob]
        verdict = "CONFIRMED" if len(hits) == len(needles) else ("PARTIAL" if hits else "QUOTE_ABSENT")
        print(f"{label} | {verdict} | hits {len(hits)}/{len(needles)} | {len(html)} bytes")
    except Exception as e:
        print(f"{label} | DEAD | {type(e).__name__}: {e}")
    time.sleep(1)

print()
print("=== Needle article (exact Algolia URL) ===")
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/items/49826663"))
    url = data.get("url", "")
    print(f"  story url: {url}")
    html = fetch(url)
    blob = norm(strip_html(html))
    for n in ["14mb function-calling model", "apache 2.0", "empty function_calls list", "fine-tuned locally on a laptop"]:
        print(f"  needle {n[:38]!r}: {'HIT' if norm(n) in blob else 'MISS'}")
except Exception as e:
    print(f"  DEAD {type(e).__name__}: {e}")
