# filer: append GALA dd-selfsteal LINKS rows to memory/corpus/LINKS.jsonl
# single-writer append, dedupe by src first, em/en-dash scan on decoded values
import json, os, sys
from datetime import datetime, timezone

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
LANES = os.path.join(ROOT, "watch/inbox/gala_20260925/dd-selfsteal/lanes")
LINKS = os.path.join(ROOT, "memory/corpus/LINKS.jsonl")

LANE_ORDER = [
    "dd-mountain-bridge", "dd-actualplay-intel", "dd-games-audit",
    "selfsteal-24h-builds", "synthesis", "hermes-burn-patterns",
    "dd-corpus-holdings", "hermes-burn-economics", "hermes-intelligent-burn",
    "selfsteal-24h-laws",
]
SLUG = "dd-selfsteal"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- load lanes ---
lanes = {}
for lid in LANE_ORDER:
    p = os.path.join(LANES, lid + ".json")
    with open(p, "r", encoding="utf-8") as f:
        lanes[lid] = json.load(f)
print("lanes loaded:", len(lanes), "| ts:", TS)

# --- pre-append dedupe checks ---
with open(LINKS, "r", encoding="utf-8") as f:
    raw = f.read()
assert raw.endswith("\n"), "LINKS.jsonl does not end with newline; refusing to append"
pre_lines = raw.splitlines()
pre_count = len(pre_lines)
pre_srcs = set()
for l in pre_lines:
    r = json.loads(l)
    if "src" in r:
        pre_srcs.add(r["src"])
    assert SLUG not in l, "pre-append ledger already references dd-selfsteal: " + l[:200]
print("pre-append ledger lines:", pre_count, "| dd-selfsteal hits under any field: 0")

# --- build rows ---
rows = []
for lid in LANE_ORDER:
    lane = lanes[lid]
    lidiv = lane["division"]
    lane_rows = lane.get("rows", [])
    src = "watch/inbox/gala_20260925/dd-selfsteal/lanes/%s.json" % lid
    assert src not in pre_srcs, "src already in ledger: " + src
    if lane_rows:
        title = lane_rows[0]["law"]
    else:
        assert lane.get("decision_changed"), "no rows and no decision_changed: " + lid
        title = lane["decision_changed"]
    assert lane.get("decision_changed"), "missing decision_changed: " + lid
    row = {
        "ts": TS,
        "id": "GALA-%s-%s" % (SLUG, lid),
        "kind": "gala",
        "slug": SLUG,
        "src": src,
        "author": "gala lane %s (dd-selfsteal, division %s)" % (lid, lidiv),
        "title": title,
        "load_bearing": [r["law"] for r in lane_rows],
        "decision_changed": lane["decision_changed"],
        "lane": "gala-20260925/dd-selfsteal/%s" % lidiv,
    }
    rows.append(row)

# --- em/en-dash scan on every decoded value we are about to file ---
bad = []
for row in rows:
    for k, v in row.items():
        if isinstance(v, str) and ("\u2014" in v or "\u2013" in v):
            bad.append((row["id"], k))
        if isinstance(v, list):
            for item in v:
                if isinstance(item, str) and ("\u2014" in item or "\u2013" in item):
                    bad.append((row["id"], k))
if bad:
    print("EM-DASH FOUND, aborting:", bad)
    sys.exit(2)
print("em/en-dash scan on decoded row values: 0")

# --- append (single writer, sequential) ---
with open(LINKS, "a", encoding="utf-8", newline="\n") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
print("appended rows:", len(rows))

# --- post-append whole-ledger verification ---
with open(LINKS, "r", encoding="utf-8") as f:
    post_lines = f.read().splitlines()
parsed = [json.loads(l) for l in post_lines]
print("post-append ledger lines:", len(post_lines), "| whole-ledger re-parse:", len(parsed), "/", len(post_lines), "OK")
new_ids = [r["id"] for r in rows]
assert len(set(new_ids)) == len(new_ids), "duplicate ids in appended set"
id_counts = {}
src_counts = {}
for r in parsed:
    id_counts[r["id"]] = id_counts.get(r["id"], 0) + 1
    if "src" in r:
        src_counts[r["src"]] = src_counts.get(r["src"], 0) + 1
for row in rows:
    assert id_counts[row["id"]] == 1, "id not unique: " + row["id"]
    assert src_counts[row["src"]] == 1, "src not exactly once: " + row["src"]
print("appended ids unique:", len(new_ids), "| appended srcs each exactly once:", len(rows))

# --- per-lane facts for the STATE entry ---
print("--- per-lane facts ---")
for row in rows:
    lane = lanes[row["id"].replace("GALA-dd-selfsteal-", "")]
    ok = lane.get("ok", "<no ok key>")
    status = lane.get("status", "")
    nrows = len(lane.get("rows", []))
    print("%s | division %s | ok=%s status=%s | rows=%d | title=%s" % (
        row["id"], row["lane"].split("/")[-1], ok, status, nrows, row["title"][:60]))
print("total mined law rows:", sum(len(lanes[l].get("rows", [])) for l in LANE_ORDER))
print("decision_changed keys present:", sum(1 for l in LANE_ORDER if lanes[l].get("decision_changed")))
