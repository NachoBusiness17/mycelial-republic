"""Confirmation pass, part 2: 2609.17848 full text + 8 HN-door items.

SSRF-hardened fetcher: https only, host allowlist, redirects re-checked
against the same allowlist. HN threads via Algolia items API; external
pages fetched directly. Verdicts come only from this run's bytes.
"""
import json
import re
import urllib.request
import urllib.error
import time

ALLOWED_HOSTS = {
    "arxiv.org", "www.arxiv.org", "export.arxiv.org",
    "hn.algolia.com",
    "duane.sh", "www.duane.sh",
    "dirac.run", "www.dirac.run",
    "raw.githubusercontent.com",
    "blog.cloudflare.com",
    "www.raspberrypi.com",
    "api.fxtwitter.com",
    "www.reddit.com", "old.reddit.com",
}


def _host_ok(host):
    host = (host or "").lower()
    return host in ALLOWED_HOSTS


class GuardedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = urllib.parse.urlsplit(newurl).hostname
        if not _host_ok(host):
            raise urllib.error.URLError(f"redirect to non-allowlisted host blocked: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(GuardedRedirect)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(url, timeout=45):
    scheme, host = urllib.parse.urlsplit(url)[:2]
    if scheme != "https" or not _host_ok(host):
        raise urllib.error.URLError(f"blocked non-allowlisted url: {url}")
    req = urllib.request.Request(url, headers=UA)
    with OPENER.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


import urllib.parse  # noqa: E402  (used by guard + fetch)


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).lower()


def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s)


def full_text(obj):
    out = [obj.get("title") or "", obj.get("story_title") or "", obj.get("comment_text") or "", obj.get("story_text") or ""]
    for ch in obj.get("children", []) or []:
        out.append(full_text(ch))
    return " ".join(o for o in out if o)


print("=== 2609.17848 html full text ===")
try:
    html = fetch("https://arxiv.org/html/2609.17848v1", timeout=60)
    blob = norm(strip_html(html))
    for n in ["88.0% versus 80.4% on xlam", "lora outperforms full-parameter fine-tuning", "47.6% versus 44.1% on glaive"]:
        print(f"  needle {n[:40]!r}: {'HIT' if norm(n) in blob else 'MISS'}")
    print(f"  fetched {len(html)} bytes")
except Exception as e:
    print(f"  DEAD: {type(e).__name__}: {e}")

HN_ITEMS = [
    ("49807413", ["cost-effective infra to host it", "almost never worth it"]),
    ("49748553", ["360b tokens"]),
    ("49966238", ["401,975", "apache-2.0"]),
    ("49897103", []),
    ("49627340", []),
    ("49807276", []),
    ("49923692", []),
    ("49826663", []),
]

print()
print("=== HN threads via Algolia ===")
for hid, needles in HN_ITEMS:
    try:
        data = json.loads(fetch(f"https://hn.algolia.com/api/v1/items/{hid}"))
        title = data.get("title", "")
        url = data.get("url", "")
        blob = norm(full_text(data))
        hits = [n for n in needles if norm(n) in blob]
        verdict = "ALIVE" if not needles else ("CONFIRMED" if len(hits) == len(needles) else f"PARTIAL {len(hits)}/{len(needles)}")
        print(f"{hid} | {verdict} | pts={data.get('points')} | title={title[:70]!r} | url={url[:90]}")
    except Exception as e:
        print(f"{hid} | DEAD | {type(e).__name__}: {e}")
    time.sleep(1)

EXTERNAL = [
    ("duane.sh RAG post", "https://duane.sh/2026/09/28/fine-tuning-qwen35-4b-rag/",
     ["71% less cost", "rank 32", "position"]),
    ("dirac.run EasyCommand", "https://dirac.run/",
     ["401,975", "212/300"]),
    ("shrewd readme", "https://raw.githubusercontent.com/sshah03/shrewd/main/README.md",
     ["locked test set", "statistical bound"]),
    ("Clef blog", "https://blog.cloudflare.com/clef-open-weight-decision-models/",
     ["rank-256", "qwen3.8-27b"]),
    ("Needle article", "https://www.raspberrypi.com/news/turn-text-into-actions-with-needle-a-14mb-function-calling-ai-model/",
     ["14mb function-calling model", "apache 2.0"]),
    ("FrogNano abs", "https://export.arxiv.org/abs/2609.07925",
     ["online task synthesis", "1,500"]),
]

print()
print("=== External pages (deep-read receipts of the HN sweep) ===")
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
