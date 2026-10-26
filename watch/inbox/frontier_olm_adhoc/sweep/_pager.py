"""Page arctic-shift for the quant census (last 30 days). Polite: 1.5s sleep, max pages guard."""
import json, time, urllib.request, urllib.parse, datetime, sys

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
AFTER = 1789152920  # 30d before 2026-10-11
UA = {"User-Agent": "mag-estate-frontier-gopher/1.0 (research sweep)"}
OUT = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_adhoc/sweep"

def fetch(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r).get("data") or []
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"{e.code} {url} :: {body}")

def page_all(sub, extra=None, max_pages=8):
    rows, before = [], None
    for i in range(max_pages):
        p = {"subreddit": sub, "after": AFTER, "limit": 100, "sort": "desc"}
        if before:
            p["before"] = before
        if extra:
            p.update(extra)
        batch = fetch(p)
        if not batch:
            break
        rows.extend(batch)
        before = min(x["created_utc"] for x in batch)
        if len(batch) < 100:
            break
        time.sleep(1.5)
    return rows

def main():
    jobs = [
        ("LocalLLaMA", None),
        ("LocalLLaMA", {"title": "quant"}),
        ("LocalLLM", None),
        ("ollama", {"title": "quant"}),
        ("MachineLearning", {"title": "quantization"}),
        ("LocalLLaMA", {"title": "GGUF"}),
        ("LocalLLaMA", {"title": "Q4"}),
    ]
    seen_ids = set()
    all_rows = []
    for sub, extra in jobs:
        label = sub + ("/" + extra["title"] if extra else "")
        rows = []
        for attempt in range(3):
            try:
                rows = page_all(sub, extra)
                break
            except Exception as e:
                print("ERR", label, "attempt", attempt + 1, str(e)[:200])
                time.sleep(5 + attempt * 5)
        fresh = [r for r in rows if r["id"] not in seen_ids]
        for r in fresh:
            seen_ids.add(r["id"])
        all_rows.extend(fresh)
        print("OK", label, len(rows), "fresh", len(fresh))
        time.sleep(3)
    with open(OUT + "/_census.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f)
    print("TOTAL", len(all_rows))

if __name__ == "__main__":
    main()
