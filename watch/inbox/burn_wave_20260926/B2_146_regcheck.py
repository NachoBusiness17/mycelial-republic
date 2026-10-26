"""B2-146: fold index_events.jsonl and check registration state of target files."""
import json
import hashlib

root = "watch/inbox"
log = open(root + "/index_events.jsonl", encoding="utf-8").read().splitlines()
print("event rows:", len(log))
active = {}
ops = {}
for i, line in enumerate(log):
    line = line.strip()
    if not line:
        continue
    try:
        e = json.loads(line)
    except json.JSONDecodeError:
        print("unparsable row at line", i + 1, ":", line[:120])
        continue
    op = e.get("op")
    ops[op] = ops.get(op, 0) + 1
    f = e.get("file")
    if not f:
        continue
    if op == "register":
        active[f] = e
    elif op in ("invalidate", "deregister", "retire"):
        active.pop(f, None)
print("ops:", ops)

targets = [
    "EVENTS.jsonl",
    "ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc",
    "BURN_doctrine-owed-chase_20260926_b.md",
    "BURN_free-resource-landscape_20260926_e.md",
    "BURN_judge-lane-spec_20260926_e.md",
    "INDEX.md",
    "SHARED_SURFACE_CONTRACT.json",
    "ESSENTIALS_PACK_20260926.tar.gz.enc",
]
for t in targets:
    reg = None
    for kv in ("/board/inbox/" + t, t):
        if kv in active:
            reg = active[kv]
            break
    hist = []
    for i, line in enumerate(log):
        if t in line:
            e = json.loads(line)
            hist.append((i + 1, e.get("op"), e.get("ts", "")))
    h = hashlib.sha256(open(root + "/" + t, "rb").read()).hexdigest().upper()
    print("---", t)
    print("  sha256:", h)
    print("  active registration:", ("YES class=" + str(reg.get("class", ""))) if reg else "NO")
    print("  history rows (line,op,ts):", hist[:8])
