"""Round 3: RQ3 (TRL/verl/RL shelf) + LocalLLM/ollama doors. Long spacing to dodge 429s."""
import json, time, urllib.request, urllib.parse, sys, io, os

ALLOWED_ORIGIN = "https://arctic-shift.photon-reddit.com"
ALLOWED_HOST = "arctic-shift.photon-reddit.com"
OUT_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "_ft_candidates.json"))
AFTER = "2026-09-10"

QUERIES = [
    ("LocalLLaMA", "title", "PPO"),
    ("LocalLLaMA", "title", "reward model"),
    ("LocalLLaMA", "title", "post-training"),
    ("LocalLLaMA", "title", "RL framework"),
    ("MachineLearning", "selftext", "verl"),
    ("MachineLearning", "title", "RLHF"),
    ("LocalLLM", "title", "fine-tuning"),
    ("ollama", "title", "fine-tuning"),
    ("LocalLLaMA", "selftext", "ten minutes"),
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("redirect blocked by allowlist policy")

def fetch(sub, param, val):
    qs = urllib.parse.urlencode({
        "subreddit": sub, param: val, "limit": 100,
        "sort": "desc", "sort_type": "created_utc", "after": AFTER})
    url = f"{ALLOWED_ORIGIN}/api/posts/search?{qs}"
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != ALLOWED_HOST:
        raise ValueError("blocked non-allowlisted origin")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 mag-harness-sweep/1.0"})
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=30) as r:
        return json.load(r).get("data") or []

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    seen = {}
    for sub, param, val in QUERIES:
        try:
            rows = fetch(sub, param, val)
        except Exception as e:
            print(f"ERR {sub} [{param}={val}]: {e}", file=sys.stderr)
            rows = []
        for p in rows:
            seen[p["id"]] = p
        print(f"# {sub} [{param}={val}] -> {len(rows)}", file=sys.stderr)
        time.sleep(10.0)
    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                for p in json.load(f):
                    seen.setdefault(p["id"], p)
        except Exception:
            pass
    out = sorted(seen.values(), key=lambda p: -(p.get("score") or 0))
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f)
    import datetime
    for p in out[:70]:
        d = datetime.datetime.fromtimestamp(p["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
        print(f'{p.get("score",0):5} | {p.get("num_comments",0):4}c | {d} | r/{p["subreddit"]} | {p["title"][:130]} | https://reddit.com{p["permalink"]}')
    print(f"TOTAL {len(out)}", file=sys.stderr)

if __name__ == "__main__":
    main()
