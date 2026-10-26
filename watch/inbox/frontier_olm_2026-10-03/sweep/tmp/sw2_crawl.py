# Evening window-2 crawl: swarm-orchestration-reddit, frontier_olm 2026-10-03.
# Sharp keywords mapped to the 5 evening research questions. Door: Arctic Shift
# (the working reddit engine per lens/burns.md:107-111; do not rediscover doors).
# Disposable tool. urllib direct, no subprocess spawn.
import json, time, datetime, urllib.request, sys

BASE = "https://arctic-shift.photon-reddit.com/api"
FIELDS = "id,subreddit,created_utc,title,score,num_comments,author,selftext"
# epoch ints everywhere: the API 400s when a date-string `after` is mixed with
# an int `before` cursor (first-hand, this crawl's page-2 failures).
AFTER = str(int(datetime.datetime(2026, 9, 3, tzinfo=datetime.timezone.utc).timestamp()))
BEFORE = str(int(datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc).timestamp()))
SUBS = ["LocalLLaMA", "ClaudeCode", "ClaudeAI", "AI_Agents", "aiagents", "LLMDevs",
        "LocalLLM", "ollama", "claudeskills", "LangChain", "Anthropic", "cursor",
        "codex", "hermesagent"]
W1_BANKED = {"1wb35xo", "1wg442g", "1w6gg8v", "1wmafge", "1wbc03f", "1w67g8k",
             "1wbifl0", "1w950fw", "1wsuag0", "1wdasar", "1wv1u54", "1wv05u1",
             "1wsq0pa", "1wu6reb"}
KW = ["retry", "backoff", "resume", "resum", "checkpoint", "fault", "failover",
      "takeover", "supervisor", "restart", "salvage", "idempot", "quota", "429",
      "rate limit", "rate-limit", "overload", "529", "throttle", "queue",
      "swarm", "mesh", "orchestrat", "multi-agent", "multi agent", "agent team",
      "subagent", "sub-agent", "fan out", "fan-out", "parallel agent", "handoff",
      "hand-off", "root cause", "diagnos", "attribution", "cascade", "postmortem",
      "post-mortem", "failure mode", "consensus", "majority vote",
      "self-consistency", "ensemble", "flock", "quorum", "calibration",
      "confidence", "hallucination"]

def get(url, tries=4):
    delay = 4
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("  try %d failed: %s; backoff %ds" % (i + 1, e, delay), flush=True)
            time.sleep(delay)
            delay *= 2
    return None

ts_after = int(datetime.datetime(2026, 9, 3, tzinfo=datetime.timezone.utc).timestamp())
all_rows = []
per_sub = {}
for sub in SUBS:
    cursor = None
    got = 0
    for page in range(25):
        # ONE before param only: page 1 carries the window edge, page 2+ carries
        # the cursor. Appending a second &before= 400s (duplicate param).
        edge = BEFORE if cursor is None else str(cursor)
        url = ("%s/posts/search?subreddit=%s&after=%s&before=%s&limit=100&fields=%s"
               % (BASE, sub, AFTER, edge, FIELDS))
        d = get(url)
        if not d or not d.get("data"):
            break
        posts = d["data"]
        for p in posts:
            all_rows.append(p)
        got += len(posts)
        if len(posts) < 100:
            break
        # advance FORWARD: before=newest-of-batch (ascending order). A cursor of
        # min() sends before <= after and the API 400s (first-hand, twice).
        cursor = posts[-1]["created_utc"]
        time.sleep(0.7)
    per_sub[sub] = got
    print("%s: %d posts" % (sub, got), flush=True)

print("TOTAL fetched: %d" % len(all_rows), flush=True)
full_path = sys.argv[1]
with open(full_path, "w", encoding="utf-8") as f:
    for p in all_rows:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

hits = []
for p in all_rows:
    blob = ((p.get("title") or "") + " " + (p.get("selftext") or "")[:400]).lower()
    if any(k in blob for k in KW):
        p["_kw"] = sorted({k for k in KW if k in blob})
        p["_w1"] = p["id"] in W1_BANKED
        hits.append(p)
hits.sort(key=lambda p: -((p.get("score") or 0) + 5 * (p.get("num_comments") or 0)))
print("keyword hits: %d" % len(hits), flush=True)
for p in hits[:60]:
    dt = datetime.datetime.fromtimestamp(p["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
    gist = (p.get("selftext") or "").replace("\n", " ")[:110]
    tag = " W1-BANKED" if p["_w1"] else ""
    print("%s | s=%s c=%s | r/%s | id=%s%s | %s | %s" % (
        dt, p.get("score"), p.get("num_comments"), p["subreddit"], p["id"], tag,
        p["title"][:95], gist), flush=True)
