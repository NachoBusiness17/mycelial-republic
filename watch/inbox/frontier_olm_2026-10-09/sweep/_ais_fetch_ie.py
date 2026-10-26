"""Arctic Shift door for the inference-efficiency reddit sweep (day 9, 2026-10-09).

Door proven by the sibling sweep agent-memory-continuity-reddit.md (day-9 sweep folder):
old.reddit/www.reddit JSON walled; api.pullpush.io rate-blocks; arctic-shift.photon-reddit.com
works with ~30-90s spacing. Low-volume single-session fetch, results saved raw.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) frontier-sweep/1.0"
AFTER = "2026-09-09"
BEFORE = "2026-10-10"
SLEEP = 40

QUERIES = [
    ("ie_spec_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "speculative", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_batch_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "batching", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_vllm_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "vllm", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_llamacpp_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "llama.cpp", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_tps_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "tokens per second", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_bench_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "benchmark", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_kv_ll", "/posts/search", {"subreddit": "LocalLLaMA", "title": "kv cache", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_perf_ollama", "/posts/search", {"subreddit": "ollama", "title": "speed", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_perf_llm", "/posts/search", {"subreddit": "LocalLLM", "title": "performance", "after": AFTER, "before": BEFORE, "limit": "50"}),
    ("ie_spec_ml", "/posts/search", {"subreddit": "MachineLearning", "title": "inference", "after": AFTER, "before": BEFORE, "limit": "50"}),
]


def get(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 - log and back off
            last = e
            wait = 45 * (i + 1)
            print("RETRY %d/3 after error: %s ; sleeping %ds" % (i + 1, e, wait), flush=True)
            time.sleep(wait)
    print("FAILED %s : %s" % (url, last), flush=True)
    return None


def brief(rows):
    out = []
    for d in rows:
        out.append({
            "id": d.get("id"),
            "title": d.get("title"),
            "created": d.get("created_utc") or d.get("created"),
            "score": d.get("score"),
            "num_comments": d.get("num_comments"),
            "subreddit": d.get("subreddit"),
            "permalink": d.get("permalink"),
        })
    return out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "pass1"
    if which == "pass1":
        for name, path, params in QUERIES:
            qs = urllib.parse.urlencode(params)
            url = BASE + path + "?" + qs
            body = get(url)
            if body is not None:
                try:
                    data = json.loads(body)
                    rows = data.get("data", [])
                except Exception as e:  # noqa: BLE001
                    print("PARSE FAIL %s: %s ; head=%s" % (name, e, body[:200]), flush=True)
                    rows = []
                fn = "_ais_%s.json" % name
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(body)
                print("== %s : %d rows -> %s" % (name, len(rows), fn), flush=True)
                for b in brief(rows)[:15]:
                    print("   %s | %s | score %s | %sc | %s" % (b["created"], b["id"], b["score"], b["num_comments"], b["title"][:90]), flush=True)
            time.sleep(SLEEP)
    elif which == "ids":
        ids = sys.argv[2]
        url = BASE + "/posts/ids?ids=" + urllib.parse.quote(ids)
        body = get(url)
        if body is not None:
            fn = "_ais_ids_%s.json" % ids.replace(",", "_")[:60]
            with open(fn, "w", encoding="utf-8") as f:
                f.write(body)
            try:
                rows = json.loads(body).get("data", [])
            except Exception as e:  # noqa: BLE001
                print("PARSE FAIL: %s" % e, flush=True)
                rows = []
            print("== ids %s : %d rows -> %s" % (ids, len(rows), fn), flush=True)
            for d in rows:
                print("--- %s | %s | score %s | %s comments" % (d.get("id"), d.get("created_utc"), d.get("score"), d.get("num_comments")), flush=True)
                print("TITLE: %s" % d.get("title"), flush=True)
                st = (d.get("selftext") or "")[:1500]
                print("SELFTEXT: %s" % st, flush=True)
    elif which == "comments":
        link = sys.argv[2]  # t3_xxxx
        url = BASE + "/comments/search?link_id=" + urllib.parse.quote(link) + "&limit=100"
        body = get(url)
        if body is not None:
            fn = "_ais_comments_%s.json" % link.replace("t3_", "")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(body)
            try:
                rows = json.loads(body).get("data", [])
            except Exception as e:  # noqa: BLE001
                print("PARSE FAIL: %s" % e, flush=True)
                rows = []
            print("== comments %s : %d rows -> %s" % (link, len(rows), fn), flush=True)
            for d in rows:
                print("--- u/%s score %s" % (d.get("author"), d.get("score")), flush=True)
                print("   %s" % ((d.get("body") or "")[:900].replace("\n", " ")), flush=True)


if __name__ == "__main__":
    main()
