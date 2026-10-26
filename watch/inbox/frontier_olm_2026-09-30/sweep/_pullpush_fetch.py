"""Sweep gopher helper: fetch reddit thread content via pullpush archive API.

Only public reddit content; read-only GETs with a descriptive User-Agent.
"""
import json
import sys
import time
import urllib.request
import urllib.error

BASE = "https://api.pullpush.io/reddit/search/"
UA = {"User-Agent": "frontier-sweep-research/0.1 (local research script; contact: operator)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:500]
    except Exception as e:  # noqa: BLE001
        return -1, repr(e)[:500]


def fetch_subs(ids):
    url = BASE + "submission/?ids=" + ",".join(ids) + "&size=100"
    st, body = get(url)
    print(f"== submissions status={st} bytes={len(body)}")
    if st != 200:
        print(body)
        return
    data = json.loads(body).get("data", [])
    for d in data:
        out = {
            "id": d.get("id"),
            "title": d.get("title"),
            "subreddit": d.get("subreddit"),
            "created_utc": d.get("created_utc"),
            "score": d.get("score"),
            "num_comments": d.get("num_comments"),
            "permalink": d.get("permalink"),
            "selftext_head": (d.get("selftext") or "")[:1500],
        }
        print(json.dumps(out, ensure_ascii=False))
        time.sleep(1)


def fetch_comments(link_id, limit=40):
    url = BASE + f"comment/?link_id={link_id}&size={limit}&sort=desc&sort_type=score"
    st, body = get(url)
    print(f"== comments {link_id} status={st}")
    if st != 200:
        print(body)
        return
    data = json.loads(body).get("data", [])
    print(f"n_comments_fetched={len(data)}")
    for d in data[:12]:
        print(json.dumps({
            "author": d.get("author"),
            "score": d.get("score"),
            "body_head": (d.get("body") or "")[:900],
        }, ensure_ascii=False))
        time.sleep(0.5)


def search_window(sub, after_epoch, keyword, size=100):
    url = (BASE + f"submission/?subreddit={sub}&after={after_epoch}"
           f"&size={size}&sort=desc&sort_type=score")
    if keyword:
        url += "&title=" + urllib.request.quote(keyword)
    st, body = get(url)
    print(f"== search {sub} after={after_epoch} kw={keyword!r} status={st}")
    if st != 200:
        print(body)
        return
    data = json.loads(body).get("data", [])
    print(f"n={len(data)}")
    for d in data:
        print(json.dumps({
            "id": d.get("id"),
            "title": d.get("title"),
            "created_utc": d.get("created_utc"),
            "score": d.get("score"),
            "num_comments": d.get("num_comments"),
        }, ensure_ascii=False))
        time.sleep(0.5)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "subs":
        fetch_subs(sys.argv[2].split(","))
    elif mode == "comments":
        fetch_comments(sys.argv[2])
    elif mode == "search":
        search_window(sys.argv[2], int(sys.argv[3]), sys.argv[4])
