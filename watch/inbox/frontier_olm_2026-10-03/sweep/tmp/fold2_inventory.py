import json, os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03"

reg_path = os.path.join(ROOT, "register.jsonl")
rows = [json.loads(l) for l in open(reg_path, encoding="utf-8") if l.strip()]
print("register rows:", len(rows))
print("row1 keys:", sorted(rows[0].keys()))
print("row-last keys:", sorted(rows[-1].keys()))
print("first title:", rows[0].get("title", "")[:90])
print("last title:", rows[-1].get("title", "")[:90])
print("last url:", rows[-1].get("url", ""))

per_path = os.path.join(ROOT, "percolator_candidates.jsonl")
prows = [json.loads(l) for l in open(per_path, encoding="utf-8") if l.strip()]
print("percolator rows:", len(prows))
print("percolator keys row1:", sorted(prows[0].keys()))
for i, r in enumerate(prows, 1):
    print("  row", i, "area:", r.get("area"), "| steal_card:", str(r.get("steal_card", ""))[:70])

entries = []
total = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        sz = os.path.getsize(p)
        entries.append((rel, sz))
        total += sz
entries.sort()
out = os.path.join(ROOT, "sweep", "tmp", "fold2_inventory_current.txt")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    for rel, sz in entries:
        f.write("%9d  %s\n" % (sz, rel))
    f.write("TOTAL files=%d bytes=%d\n" % (len(entries), total))
print("walked files:", len(entries), "bytes:", total)
print("inventory written:", out)

# claim-vs-measured cross-check candidates named in the round-2 inputs
claims = {
    "steal/agent-memory-and-continuity.md": ("chars", 16124),
    "steal/open-and-local-language-models-arxiv-hf.md": ("bytes", 24852),
    "steal/quantization-and-compression.md": ("chars", 22856),
    "sweep/open-and-local-language-models-arxiv.md": ("bytes", 18525),
    "sweep/quantization-and-compression-hn.md": ("bytes", 34342),
    "sweep/agent-memory-and-continuity-hn.md": ("bytes", 15259),
    "sweep/swarm-orchestration-hn.md": ("bytes", 16729),
    "sweep/swarm-orchestration-reddit.md": ("bytes", 35621),
    "sweep/swarm-orchestration-x.md": ("bytes", 31487),
    "sweep/evals-and-self-improvement-x.md": ("bytes", 21603),
}
size_map = dict(entries)
print("\ncross-check (claimed by round-2 lanes vs measured now):")
for rel, (unit, claimed) in sorted(claims.items()):
    measured = size_map.get(rel)
    print("  %-55s claimed %s=%s measured=%s match=%s" % (rel, unit, claimed, measured, measured == claimed))
