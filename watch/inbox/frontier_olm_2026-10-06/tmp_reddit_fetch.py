"""Reddit JSON door fetcher for the quantization-compression reddit sweep (2026-10-06).

Security posture: fetch targets are restricted to an explicit https host allowlist
(old.reddit.com) with literal API paths; subreddit names are validated against a
strict identifier regex before interpolation. Output paths are resolved and
asserted to stay inside the sweep evidence directory (no user input anywhere).
"""
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_HOST = "old.reddit.com"
SUB_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,30}$")
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
if not str(OUT_DIR).startswith(str(REPO_ROOT)):
    print("refusing: resolved output dir escaped repo root", file=sys.stderr)
    sys.exit(2)

HDRS = {
    "User-Agent": "windows:local-sovereign-agent-frontier-sweep:v0.1 (research)",
    "Accept": "application/json",
}


def fetch(url):
    parsed_host = urllib.parse.urlsplit(url).hostname or ""
    if urllib.parse.urlsplit(url).scheme != "https" or parsed_host != ALLOWED_HOST:
        return -2, "blocked: host not in allowlist"
    req = urllib.request.Request(url, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:200]
    except Exception as e:
        return -1, repr(e)


def main():
    import urllib.parse  # local import after allowlist constants defined

    rows = []
    for sub in SUBS:
        if not SUB_PATTERN.match(sub):
            print(f"refusing non-identifier sub name: {sub!r}", file=sys.stderr)
            sys.exit(2)
        url = f"https://{ALLOWED_HOST}/r/{sub}/top.json?t=month&limit=50"
        status, body = fetch(url)
        out_path = (OUT_DIR / f"{sub}_top_month.json").resolve()
        if not str(out_path).startswith(str(OUT_DIR)):
            print("refusing path escape", file=sys.stderr)
            sys.exit(2)
        ok = False
        children = []
        try:
            data = json.loads(body)
            children = data.get("data", {}).get("children", [])
            ok = True
            out_path.write_text(body, encoding="utf-8")
        except Exception:
            (OUT_DIR / f"{sub}_top_month.json.err").write_text(
                f"status={status}\n{body[:2000]}", encoding="utf-8"
            )
        print(f"== r/{sub}: HTTP {status}, children={len(children)} "
              f"({'saved json' if ok else 'saved .err'})")
        for c in children:
            d = c.get("data", {})
            created = datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc)
            rows.append({
                "sub": sub,
                "title": d.get("title", ""),
                "score": d.get("score", 0),
                "comments": d.get("num_comments", 0),
                "date": created.strftime("%Y-%m-%d"),
                "permalink": "https://old.reddit.com" + d.get("permalink", ""),
                "flair": d.get("link_flair_text", ""),
                "selftext_len": len(d.get("selftext", "") or ""),
                "selftext_head": (d.get("selftext", "") or "")[:200].replace("\n", " "),
                "url": d.get("url", ""),
            })
    rows.sort(key=lambda r: (r["score"] + r["comments"]), reverse=True)
    cand_path = (OUT_DIR / "candidates.json").resolve()
    if str(cand_path).startswith(str(OUT_DIR)):
        cand_path.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"\nTOTAL candidates: {len(rows)}")
    for i, r in enumerate(rows, 1):
        print(f"{i:2d}. [{r['sub']}] {r['score']:5d}pts {r['comments']:4d}c "
              f"{r['date']} | {r['title'][:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
