"""Confirmation pass, part 1: 6 X items (fxtwitter) + 8 arXiv items (export.arxiv.org API).

Checks each 10-05 finetuning-adaptation sweep item's URL still resolves and its
verbatim quote still appears in the fetched bytes. Survives = CONFIRMED,
quote absent = PARTIAL, fetch fail = DEAD. No fabrication: verdicts come only
from this run's bytes.
"""
import json
import re
import urllib.request
import sys

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"').replace("&gt;", ">").replace("&lt;", "<")
    return re.sub(r"\s+", " ", s).lower()


X_ITEMS = [
    ("omarsar0", "2097958286146605446",
     ["performance dropped on all seven tasks", "adopts the expert's planning strategy without the competence to execute it"]),
    ("zafstojano", "2097689256961466486",
     ["recursive synthetic improvement"]),
    ("ArtificialAnlys", "2098148674203488422",
     ["license: mit", "552b parameters"]),
    ("Sumanth_077", "2098053941800100294",
     ["34 of 64 harness changes moved in the same direction", "2 of 9 final harness versions"]),
    ("shikibmehri", "2098233059242099175",
     ["army of agents", "optimal reward signal for each token of training"]),
    ("ValsAI", "2098125177116848591",
     ["1m context window and 384 max output tokens", "temperature 1, default top-p"]),
]

ARXIV_ITEMS = [
    ("2609.17848", ["lora outperforms full-parameter fine-tuning", "88.0% versus 80.4% on xlam"]),
    ("2610.02142", ["diagnostic ladder costs minutes of cpu time", "0.959"]),
    ("2609.10750", ["catastrophic forgetting", "13.98"]),
    ("2609.23916", ["thirteen-task suite stays within 0.01 of the base", "time-incremental continued pretraining"]),
    ("2609.24115", ["fully automated closed-loop system that requires no human annotation", "edgegen"]),
    ("2609.35259", ["on-policy rollouts are inherently preferable", "kl direction"]),
    ("2609.19513", ["qvac", "28.57"]),
    ("2502.06659", ["reliable teacher inference may have practical implications", "terms of service"]),
]

print("=== X items via fxtwitter ===")
for user, sid, needles in X_ITEMS:
    url = f"https://api.fxtwitter.com/{user}/status/{sid}"
    try:
        raw = fetch(url)
        data = json.loads(raw)
        tweet = data.get("tweet", {})
        text = tweet.get("text", "") or ""
        article = ""
        art = tweet.get("article") or {}
        if isinstance(art, dict):
            article = json.dumps(art)[:4000]
        created = tweet.get("created_at", "?")
        blob = norm(text + " " + article)
        hits = [n for n in needles if norm(n) in blob]
        verdict = "CONFIRMED" if len(hits) == len(needles) else ("PARTIAL" if hits else "QUOTE_ABSENT")
        print(f"{user}/{sid} | {created} | {verdict} | hits {len(hits)}/{len(needles)} | text[:110]={text[:110]!r}")
    except Exception as e:
        print(f"{user}/{sid} | DEAD | fetch error: {type(e).__name__}: {e}")

print()
print("=== arXiv items via export.arxiv.org API ===")
ids = ",".join(i for i, _ in ARXIV_ITEMS)
try:
    raw = fetch(f"https://export.arxiv.org/api/query?id_list={ids}&max_results=20", timeout=60)
except Exception as e:
    print(f"API fetch failed: {e}")
    sys.exit(1)
entries = re.findall(r"<entry>(.*?)</entry>", raw, re.S)
by_id = {}
for ent in entries:
    m = re.search(r"<id>https?://arxiv.org/abs/([^<v]+)", ent)
    if not m:
        continue
    aid = m.group(1).strip()
    title = re.search(r"<title>(.*?)</title>", ent, re.S)
    summ = re.search(r"<summary>(.*?)</summary>", ent, re.S)
    pub = re.search(r"<published>(.*?)</published>", ent, re.S)
    by_id[aid] = (norm(title.group(1)) if title else "", norm(summ.group(1)) if summ else "", pub.group(1) if pub else "?")

for aid, needles in ARXIV_ITEMS:
    if aid not in by_id:
        print(f"{aid} | DEAD | not returned by API")
        continue
    title, summ, pub = by_id[aid]
    blob = norm(title) + " " + summ
    hits = [n for n in needles if norm(n) in blob]
    verdict = "CONFIRMED(abs)" if len(hits) == len(needles) else ("PARTIAL" if hits else "QUOTE_ABSENT_IN_ABS")
    print(f"{aid} | {pub[:10]} | {verdict} | hits {len(hits)}/{len(needles)} | title={title[:80]}")
