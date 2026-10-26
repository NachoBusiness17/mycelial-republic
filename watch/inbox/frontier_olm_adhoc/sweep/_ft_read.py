"""Pass 2 deep reads: fetch full comment trees for shortlisted threads from arctic-shift.

Writes one markdown file per thread (_read_<id>.md) with selftext + top comments,
so every banked quote is byte-backed by content fetched this session.
"""
import json, time, urllib.request, urllib.parse, sys, io, os
import datetime

ALLOWED_ORIGIN = "https://arctic-shift.photon-reddit.com"
ALLOWED_HOST = "arctic-shift.photon-reddit.com"
HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(HERE, "_ft_candidates.json")

# shortlist: (post_id, tag)
SHORTLIST = [
    ("1wdhb24", "zebra-6.5min-finetune"),
    ("1wv05u1", "jeff-9-lora-router"),
    ("1wjkt47", "ml-ttt-loop"),
    ("1wgii3h", "deepseek-rsi-reflections"),
    ("1wyvc8k", "molt-fit-tests"),
    ("1wr469w", "lora-serving-11to90"),
    ("1wtqpjt", "sftmill-distill"),
    ("1wu9zkn", "cost-before-burning-money"),
    ("1wsgrma", "imajev-15days"),
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("redirect blocked by allowlist policy")

def get(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != ALLOWED_HOST:
        raise ValueError("blocked non-allowlisted origin")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 mag-harness-sweep/1.0"})
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=30) as r:
        return json.load(r)

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    posts = {p["id"]: p for p in json.load(open(CAND, encoding="utf-8"))}
    # pull shortlist posts missing from the pool by id
    missing = [pid for pid, _ in SHORTLIST if pid not in posts]
    if missing:
        try:
            qs = urllib.parse.urlencode({"ids": ",".join("t3_" + m for m in missing)})
            extra = (get(f"{ALLOWED_ORIGIN}/api/posts/search?{qs}") or {}).get("data") or []
            for p in extra:
                posts[p["id"]] = p
            print(f"fetched {len(extra)} missing posts by id: {[p['id'] for p in extra]}", file=sys.stderr)
            time.sleep(5.0)
        except Exception as e:
            print(f"ERR fetching missing posts {missing}: {e}", file=sys.stderr)
    for pid, tag in SHORTLIST:
        p = posts.get(pid)
        if not p:
            print(f"MISSING post {pid} in candidate pool", file=sys.stderr)
            continue
        qs = urllib.parse.urlencode({"link_id": f"t3_{pid}", "limit": 100,
                                     "sort": "desc", "sort_type": "created_utc"})
        try:
            comments = (get(f"{ALLOWED_ORIGIN}/api/comments/search?{qs}") or {}).get("data") or []
            comments.sort(key=lambda c: -(c.get("score") or 0))
        except Exception as e:
            print(f"ERR comments {pid}: {e}", file=sys.stderr)
            comments = []
        out = os.path.join(HERE, f"_read_{tag}.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"# {p['title']}\n\n")
            f.write(f"- url: https://reddit.com{p['permalink']}\n")
            f.write(f"- id: {p['id']} | score: {p.get('score')} | comments: {p.get('num_comments')} | "
                    f"created: {datetime.datetime.fromtimestamp(p['created_utc'], datetime.timezone.utc).isoformat()}\n")
            f.write(f"- author: {p.get('author')} | domain: {p.get('domain')}\n")
            st = (p.get("selftext") or "").strip()
            f.write(f"- url_in_post: {p.get('url')}\n\n## SELFTEXT\n\n{st or '(empty)'}\n\n")
            f.write(f"## COMMENTS ({len(comments)} fetched, ranked by score)\n\n")
            for c in comments:
                body = (c.get("body") or "").strip()
                if body in ("[removed]", "[deleted]"):
                    continue
                f.write(f"--- u/{c.get('author')} (score {c.get('score')}):\n\n{body}\n\n")
        total = sum(len((c.get('body') or '')) for c in comments)
        print(f"READ {tag}: selftext {len(st)} chars, {len(comments)} comments {total} chars -> {os.path.basename(out)}", file=sys.stderr)
        time.sleep(8.0)

if __name__ == "__main__":
    main()
