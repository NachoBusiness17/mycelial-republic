"""Pass 2 deep reads: post selftext + full comment trees via arctic-shift.

Hook-hardened per Mimosa findings: pinned host allowlist, alnum-only id validation,
output filename built by string concat from a regex-validated id (no traversal chars
possible), confined under the fixed sweep directory.
"""
import json, os, re, time, urllib.request, urllib.parse, sys

OUTDIR = os.path.realpath(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_2026-10-11/sweep")
ALLOWED_HOST = "arctic-shift.photon-reddit.com"
IDS = sys.argv[1:]
BASE_P = "https://arctic-shift.photon-reddit.com/api/posts/ids?ids="
BASE_C = "https://arctic-shift.photon-reddit.com/api/comments/search?limit=100&sort=desc&link_id=t3_"

def build_url(base, param):
    if not re.fullmatch(r"[A-Za-z0-9,_-]{1,100}", param):
        raise ValueError(f"bad param: {param!r}")
    url = urllib.parse.urlsplit(base + urllib.parse.quote(param))
    if url.scheme != "https" or url.netloc != ALLOWED_HOST:
        raise ValueError(f"host not allowed: {url.netloc}")
    return urllib.parse.urlunsplit(url)

def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-11"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(4)
    return None

for pid in IDS:
    if not re.fullmatch(r"[a-z0-9]{6,10}", pid):
        raise ValueError(f"bad thread id: {pid!r}")
    p = get(build_url(BASE_P, pid))
    post = ((p or {}).get("data") or [None])[0]
    c = get(build_url(BASE_C, pid))
    comments = (c or {}).get("data") or []
    lines = [f"# THREAD {pid}", ""]
    if post:
        for k in ("title", "subreddit", "score", "num_comments", "created_utc", "author", "permalink"):
            lines.append(f"{k}: {post.get(k)}")
        lines.append("")
        lines.append("== SELFTEXT ==")
        lines.append(post.get("selftext") or "(no selftext)")
        lines.append("")
    else:
        lines.append("(POST NOT FOUND)")
    lines.append(f"== COMMENTS ({len(comments)} fetched) ==")
    comments.sort(key=lambda x: (x.get("score") or 0), reverse=True)
    for cm in comments:
        body = (cm.get("body") or "").replace("\r", "")
        lines.append(f"--- [{cm.get('score')}] u/{cm.get('author')} ({cm.get('id')}):")
        lines.append(body[:2500])
        lines.append("")
    fname = "_ftr_read_" + pid + ".md"  # pid is [a-z0-9]{6,10}, no separators possible
    out = os.path.realpath(OUTDIR + "/" + fname)
    if not out.startswith(OUTDIR):
        raise ValueError("output escaped sweep dir")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{pid}: post={'ok' if post else 'MISSING'}, {len(comments)} comments -> {out}", flush=True)
    time.sleep(1.5)
