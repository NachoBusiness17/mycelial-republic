"""Paced arctic-shift pull for swarm-orchestration-reddit sweep (2026-09-28 ask).

Queries the arctic-shift API one request at a time with sleeps (the server
answers {"error":"Timeout. Maybe slow down a bit"} on bursts). Saves each raw
response under _raw/ and prints a compact candidate list with dates converted
from raw created_utc by this script (never by a summarizer model).
"""
import json
import time
import urllib.request
import urllib.parse
import datetime
import os
import sys

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
OUT = os.path.dirname(os.path.abspath(__file__))
AFTER = 1788048000  # 2026-08-30 00:00 UTC; window end 2026-09-29

QUERIES = [
    ("LocalLLaMA", "mcp"),
    ("LocalLLaMA", "multi-agent"),
    ("LocalLLaMA", "rate limit"),
    ("LocalLLaMA", "swarm"),
    ("ClaudeCode", "subagent"),
    ("ClaudeCode", "rate limit"),
    ("ClaudeAI", "subagent"),
    ("ClaudeAI", "rate limit"),
    ("LocalLLM", "multi-agent"),
    ("ollama", "multi-agent"),
    ("mcp", "orchestration"),
    ("AI_Agents", "handoff"),
    ("AI_Agents", "A2A"),
    ("AI_Agents", "orchestration"),
]


def fetch(sub, kw, tries=4):
    params = urllib.parse.urlencode(
        {"subreddit": sub, "query": kw, "after": AFTER, "limit": 100, "sort": "desc"}
    )
    url = f"{BASE}?{params}"
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                d = json.load(r)
            if isinstance(d, dict) and d.get("data") is None:
                print(f"    slow:{d.get('error','?')[:40]} retry {attempt}", flush=True)
                time.sleep(18)
                continue
            return d
        except Exception as e:  # noqa: BLE001
            print(f"    err:{type(e).__name__}:{str(e)[:60]} retry {attempt}", flush=True)
            time.sleep(18)
    return None


def main():
    total = 0
    for sub, kw in QUERIES:
        slug = kw.replace(" ", "_")
        path = os.path.join(OUT, f"pull_{sub}_{slug}.json")
        print(f"[{sub} / {kw}]", flush=True)
        if os.path.exists(path) and os.path.getsize(path) > 100:
            try:
                d = json.load(open(path, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                d = None
            if d and d.get("data"):
                print("    cached", flush=True)
        else:
            d = fetch(sub, kw)
            if d is None:
                print("    FAILED after retries", flush=True)
                continue
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f)
        rows = d.get("data") or []
        rows.sort(key=lambda p: p.get("created_utc", 0), reverse=True)
        for p in rows:
            dt = datetime.datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d")
            print(
                f"  {p['id']} | {dt} | {p.get('score')} | {p.get('num_comments')}"
                f" | {p.get('title','')[:95]}",
                flush=True,
            )
        total += len(rows)
        time.sleep(12)
    print(f"TOTAL_ROWS={total}")


if __name__ == "__main__":
    sys.exit(main())
