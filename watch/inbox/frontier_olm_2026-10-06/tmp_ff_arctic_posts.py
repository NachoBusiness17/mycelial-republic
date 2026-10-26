"""tmp_ff_arctic_posts.py - inference-efficiency reddit sweep, pass 1 (2026-10-06).

Lists every post in the 30-day window for 4 subreddits via the arctic-shift
archive API (the listing door that answered for frontier_olm_2026-10-05).
Fetcher drives curl.exe per page via subprocess with CREATE_NO_WINDOW
(win32 estate law; python-urllib UA was soft-banned by this API in the
2026-10-05 sweep, curl passed).

Output: sweep/doors/ff_arctic_posts.jsonl (one post per row).
Prints: per-sub counts + top-60 by score with created dates.
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000
REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "ff_arctic_posts.jsonl"

SUBS = ["LocalLLaMA", "LocalLLM", "ollama", "MachineLearning"]
FIELDS = "id,subreddit,title,score,num_comments,created_utc,link_flair_text,selftext"
LIMIT = 100
MAX_PAGES = 40
WINDOW_DAYS = 30

NOW = int(time.time())
AFTER = NOW - WINDOW_DAYS * 86400


def curl_json(url):
    for attempt in range(3):
        r = subprocess.run(
            ["curl.exe", "-s", "--max-time", "45", "-A",
             "frontier-sweep/1.0 (research; local-sovereign-agent)", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=CREATE_NO_WINDOW)
        body = (r.stdout or "").strip()
        if body:
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                pass
        time.sleep(2 + attempt * 3)
    return None


def page_url(sub, before):
    return (f"https://arctic-shift.photon-reddit.com/api/posts/search"
            f"?subreddit={sub}&after={AFTER}&before={before}&limit={LIMIT}"
            f"&sort=desc&fields={FIELDS}")


def main():
    total = 0
    with OUT_FILE.open("a", encoding="utf-8") as fh:
        for sub in SUBS:
            n = 0
            skipped = 0
            before = NOW
            for _ in range(MAX_PAGES):
                data = None
                for attempt in range(4):
                    data = curl_json(page_url(sub, before))
                    if isinstance(data, dict) and not data.get("error"):
                        break
                    err = (data or {}).get("error") if isinstance(data, dict) else "no-json"
                    print(f"{sub}: retry {attempt + 1} after error: {err}",
                          file=sys.stderr)
                    time.sleep(6 + attempt * 6)
                    data = None
                if data is None:
                    # give up on this cursor: skip a day forward instead of dying
                    before = max(AFTER, before - 86400)
                    skipped = skipped + 1
                    if skipped > 40:
                        break
                    continue
                posts = (data or {}).get("data") or []
                if not posts:
                    break
                for p in posts:
                    fh.write(json.dumps(p, ensure_ascii=False) + "\n")
                    n += 1
                last = posts[-1].get("created_utc")
                if last is None or len(posts) < LIMIT:
                    break
                before = int(last)
                time.sleep(2.0)
            print(f"{sub}: {n} posts")
            total += n
    print(f"TOTAL {total} -> {OUT_FILE}")

    # rank locally by score, print the head for reading
    rows = [json.loads(l) for l in OUT_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows.sort(key=lambda r: (r.get("score") or 0), reverse=True)
    print("\nTOP 60 BY SCORE")
    for r in rows[:60]:
        d = datetime.fromtimestamp(r.get("created_utc", 0), tz=timezone.utc).strftime("%m-%d")
        print(f"{r.get('score',0):>5} {d} {r.get('num_comments',0):>4}c "
              f"r/{r.get('subreddit','')[:14]:14} {r.get('id')} {r.get('title','')[:110]}")


if __name__ == "__main__":
    sys.exit(main())
