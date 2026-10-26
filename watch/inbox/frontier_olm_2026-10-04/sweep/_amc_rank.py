"""Rank harvested candidates, excluding every id prior siblings banked, listed as removed,
carried as OWED, or date-verified as out-of-window traps. Provenance:
- 10-01 banked: 1wqv98w 1wu345p 1wu0miw 1wldl38 1wldz7u ; removed Hindsight wave 1wt*
- 10-02 banked: 1w9sklm 1wahqm2 ; OWED: 1ws8d1x 1wi6j25 1wjm9ez 1w5l182 1whlop5 1w5w3xi 1w0o56a 1wghnq7
- 10-03 banked: 1wbgqnp 1wtgyzm 1wlbqnl 1wpvr1u 1wvmps7 1wi0som 1wh7ti0 1wklq52 ; removed: 1wanjup 1wak3fy 1wezs4q
- 09-30 read: 1wl3828 ; 10-02 traps: 1ts3nq2 1ts3s21 1tvjdkj 1te3fb0 1pn803k 1pkwgwy 1tgm63n
  1ujp3pq 1uy6yht 1uzyuna 1uexvvy 1rlv0mp 1rz2oo3 1tjfhat 1vufvvk 1veeix3 1sna5kb 1qrbs69 1r5q7xd 1su00hm 1se7k1o
"""
import json, datetime

SRC = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-04\sweep\_amc_reddit_harvest.jsonl"
CLAIMED = set("""1wqv98w 1wu345p 1wu0miw 1wldl38 1wldz7u 1w9sklm 1wahqm2 1ws8d1x 1wi6j25 1wjm9ez
1w5l182 1whlop5 1w5w3xi 1w0o56a 1wghnq7 1wbgqnp 1wtgyzm 1wlbqnl 1wpvr1u 1wvmps7 1wi0som 1wh7ti0
1wklq52 1wanjup 1wak3fy 1wezs4q 1wl3828 1ts3nq2 1ts3s21 1tvjdkj 1te3fb0 1pn803k 1pkwgwy 1tgm63n
1ujp3pq 1uy6yht 1uzyuna 1uexvvy 1rlv0mp 1rz2oo3 1tjfhat 1vufvvk 1veeix3 1sna5kb 1qrbs69 1r5q7xd
1su00hm 1se7k1o""".split())

STRONG = ["knowledge graph", "graphrag", "graphiti", "mem0", "zep", "letta", "memgpt",
          "compaction", "consolidat", "entity resolution", "dedup", "identity",
          "sleep-time", "sleep time", "unlinked", "orphan", "re-deriv", "rederiv",
          "regenerat", "append-only", "append only", "warm boot", "handoff", "hand-off",
          "memory benchmark", "longmem", "locomo", "memory graph", "agent memory",
          "memory system", "memory layer", "forgetting", "decay", "supersede"]

rows = []
with open(SRC, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r["id"] in CLAIMED:
            continue
        text = (r["title"] + " " + r["selftext"]).lower()
        s = sum(3 if k in text else 0 for k in STRONG)
        if s <= 0:
            continue
        engagement = (r["score"] or 0) + 3 * (r["num_comments"] or 0)
        rows.append((s * 10 + engagement, r))

rows.sort(key=lambda t: -t[0])
for rank, (sc, r) in enumerate(rows[:60], 1):
    d = datetime.datetime.fromtimestamp(r["created_utc"], datetime.timezone.utc).strftime("%m-%d")
    title = (r["title"] or "")[:110].replace("\n", " ")
    print(f"{rank:2d} [{r['id']}] {d} {r['subreddit'][:12]:12s} sc={r['score']} c={r['num_comments']} kws={sc} :: {title}")
