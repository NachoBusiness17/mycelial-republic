# B2-145 probe: locate phantom absolute-path rows and their bare-path siblings in INDEX.json
import json

IDX = "watch/inbox/INDEX.json"

with open(IDX, "r", encoding="utf-8") as f:
    idx = json.load(f)

items = idx["items"]
print("schema:", idx.get("schema"))
print("fold_warnings:", json.dumps(idx.get("fold_warnings", []), indent=1)[:2000])
print("total items:", len(items))

BARE = [
    "RIDE_FAMILY_VERDICTS_20260922.md",
    "DIRECTIVE_WATCHERS_20260926.md",
    "RECAP_7D_20260926.md",
    "ESSENTIALS_RESTORE.md",
    "burn_wave_20260926/QUEUE.md",
]

PHANTOM_PREFIX = "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/"

for i, it in enumerate(items):
    p = it.get("path", "")
    if p in BARE or p.startswith(PHANTOM_PREFIX):
        body = {k: it[k] for k in it if k != "path"}
        print("-" * 70)
        print("idx", i, "path:", repr(p))
        print(json.dumps(body, ensure_ascii=False, indent=1)[:900])
