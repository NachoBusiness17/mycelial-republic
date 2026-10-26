"""Patient arctic-shift puller: browser UA, 50s spacing, retry on soft timeout."""
import json
import time
import subprocess
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AFTER = 1788048000
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
QUERIES = [
    ("LocalLLaMA", "mcp"),
    ("LocalLLaMA", "multi-agent"),
    ("LocalLLaMA", "rate limit"),
    ("LocalLLaMA", "swarm"),
    ("ClaudeCode", "subagent"),
    ("ClaudeCode", "rate limit"),
    ("ClaudeCode", "agent teams"),
    ("ClaudeAI", "subagent"),
    ("ClaudeAI", "rate limit"),
    ("LocalLLM", "multi-agent"),
    ("ollama", "multi-agent"),
    ("mcp", "orchestration"),
    ("mcp", "gateway"),
    ("AI_Agents", "handoff"),
    ("AI_Agents", "A2A"),
    ("AI_Agents", "orchestration"),
    ("ClaudeCode", "orchestration"),
]


def fetch(sub, kw, tries=5):
    url = (
        "https://arctic-shift.photon-reddit.com/api/posts/search?"
        f"subreddit={sub}&query={urllib.parse.quote(kw)}&after={AFTER}&limit=100&sort=desc"
    )
    for attempt in range(1, tries + 1):
        r = subprocess.run(
            ["curl", "-s", "-m", "60", "-A", UA, url],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        try:
            d = json.loads(r.stdout)
        except Exception:
            d = None
        if isinstance(d, dict) and isinstance(d.get("data"), list):
            return d
        err = (d or {}).get("error", r.stdout[:60] if r.stdout else f"curl rc={r.returncode}")
        print(f"    soft-fail {attempt}: {str(err)[:60]}", flush=True)
        time.sleep(50)
    return None


def main():
    import urllib.parse  # noqa: F401 (used in fetch)
    globals()["urllib"] = __import__("urllib")
    total = 0
    for sub, kw in QUERIES:
        slug = kw.replace(" ", "_")
        path = os.path.join(HERE, f"pull2_{sub}_{slug}.json")
        print(f"[{sub} / {kw}]", flush=True)
        if not (os.path.exists(path) and os.path.getsize(path) > 100):
            d = fetch(sub, kw)
            if d is None:
                print("    FAILED", flush=True)
                continue
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f)
            time.sleep(20)
        else:
            d = json.load(open(path, encoding="utf-8"))
        rows = d.get("data") or []
        rows = sorted(rows, key=lambda p: p.get("created_utc", 0), reverse=True)
        for p in rows:
            dt = datetime.datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d")
            print(
                f"  {p['id']} | {dt} | {p.get('score')} | {p.get('num_comments')}"
                f" | {p.get('title','')[:95]}",
                flush=True,
            )
        total += len(rows)
    print(f"TOTAL_ROWS={total}")


if __name__ == "__main__":
    sys.exit(main())
