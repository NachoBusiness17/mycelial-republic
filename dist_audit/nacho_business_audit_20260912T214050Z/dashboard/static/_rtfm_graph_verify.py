"""Verify the served rtfm_graph.html: extract inline JSON, parse, check edge integrity."""
import json
import re
import io
import sys
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 1) served-200 check (localhost dashboard only)
with urllib.request.urlopen("http://127.0.0.1:8765/static/rtfm_graph.html", timeout=10) as r:
    served = r.read().decode("utf-8")
print("served bytes:", len(served))

# 2) extract the inline GRAPH JSON block and parse it
m = re.search(r"const GRAPH = (\{.*?\});\n", served, re.S)
assert m, "GRAPH block not found"
raw = m.group(1).replace("<\\/", "</")
g = json.loads(raw)
print("embedded JSON parses: OK —", len(g["nodes"]), "nodes,", len(g["edges"]), "edges, schema", g["schema"])

# 3) edge integrity: every endpoint exists
ids = {n["id"] for n in g["nodes"]}
missing = [(e["from"], e["to"]) for e in g["edges"] if e["from"] not in ids or e["to"] not in ids]
assert not missing, missing
print("edge integrity: OK — every from/to exists in nodes")

# 4) kinds + rels
kinds = {}
for n in g["nodes"]:
    kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
rels = {}
for e in g["edges"]:
    rels[e["rel"]] = rels.get(e["rel"], 0) + 1
print("kinds:", kinds)
print("rels:", rels)

# 5) source file parity
src = json.load(open("memory/rtfm_graph.json", encoding="utf-8"))
assert len(src["nodes"]) == len(g["nodes"]) and len(src["edges"]) == len(g["edges"])
print("source parity: OK — served embed matches memory/rtfm_graph.json")
