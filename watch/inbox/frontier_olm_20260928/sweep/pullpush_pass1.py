"""Pullpush Pass 1 enumerator: recent top submissions per subreddit.

Door note: old.reddit.com and www.reddit.com content fetches are blocked in this
session (WebFetch returns only the welcome placeholder; webReader hits
'blocked by network security'). api.pullpush.io via curl/urllib works and is
paced 45s between calls with 429 backoff. This is the degraded door per the
sweep recipe.
"""
import json
import time
import urllib.request
import urllib.error
import sys

SUBS = ["LocalLLaMA", "LocalLLM", "ollama", "MachineLearning"]
AFTER = "1788048000"  # 2026-08-30T00:00:00Z, 30-day window back from 2026-09-29
BASE = ("https://api.pullpush.io/reddit/search/submission/?subreddit={sub}"
        "&after=" + AFTER + "&sort=desc&sort_type=score&size=100")
HDRS = {"User-Agent": "frontier-sweep-quant-compression/0.1 (research; one-shot)"}


def fetch(url, tries=4):
    delay = 40
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(delay)
                delay *= 1.6
                continue
            raise
        except Exception as e:
            sys.stderr.write("err %s try %d: %r\n" % (url, i, e))
            time.sleep(delay)
            delay *= 1.6
    return None


for sub in SUBS:
    data = fetch(BASE.format(sub=sub))
    if not data or not data.get("data"):
        print("== %s: NO DATA" % sub)
        continue
    print("== %s: %d rows" % (sub, len(data["data"])))
    for d in data["data"]:
        ts = time.strftime("%Y-%m-%d", time.gmtime(d.get("created_utc", 0)))
        print("%s | %s | %sc | %s | %s" % (
            ts, d.get("score", 0), d.get("num_comments", 0),
            d.get("title", "").replace("\n", " "), d.get("id", "")))
    sys.stdout.flush()
    time.sleep(45)
print("DONE")
