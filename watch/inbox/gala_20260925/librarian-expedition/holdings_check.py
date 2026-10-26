#!/usr/bin/env python
# cited-missing lane: dedupe citations, check estate holdings.
# Holdings test: (a) catalog path/title contains the id; (b) any file under
# corpus/, papers dirs, watch/, memory/ has the id in its FILENAME.
# Emits unique_citations.json. No em-dashes in emitted records.
import os, re, json

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
LANES = os.path.join(ROOT, "watch", "inbox", "gala_20260925", "librarian-expedition", "lanes")

with open(os.path.join(LANES, "citations_raw.json"), encoding="utf-8") as f:
    raw = json.load(f)

# 1) dedupe by (kind, value), keep all cite locations
uniq = {}
errors = [r for r in raw if "error" in r]
for r in raw:
    if "error" in r:
        continue
    key = (r["kind"], r["value"])
    u = uniq.setdefault(key, {"kind": r["kind"], "value": r["value"], "cites": []})
    u["cites"].append({"file": r["file"], "line": r["line"], "group": r["group"]})

# 2) build holding-surface indexes
# 2a) catalog: id substring in path or title
cat_hits = {}   # id -> [catalog paths]
with open(os.path.join(ROOT, "catalog", "catalog.jsonl"), encoding="utf-8", errors="replace") as f:
    for ln in f:
        try:
            row = json.loads(ln)
        except Exception:
            continue
        p = row.get("path", "") or ""
        t = row.get("title", "") or ""
        for (kind, val), u in uniq.items():
            if val in p or val in t:
                cat_hits.setdefault(val, []).append("catalog:" + p)

# 2b) filename scan over corpus/, memory/, watch/, state/ (loose bytes + arxiv archive)
SCAN_ROOTS = ["corpus", "watch", "memory", "docs", "mag", "tools", "state"]
fn_hits = {}
for sub in SCAN_ROOTS:
    base = os.path.join(ROOT, sub)
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            for (kind, val), u in uniq.items():
                if val in fn:
                    full = os.path.join(dirpath, fn)
                    fn_hits.setdefault(val, []).append(os.path.relpath(full, ROOT))

for (kind, val), u in uniq.items():
    u["catalog_hits"] = cat_hits.get(val, [])
    u["filename_hits"] = fn_hits.get(val, [])
    u["held"] = bool(u["catalog_hits"] or u["filename_hits"])

# 3) merge same-id rows across kinds (arxiv vs arxiv-bare), mark weak holdings
merged = {}
for u in uniq.values():
    m = merged.setdefault(u["value"], {"kind": u["kind"], "value": u["value"], "cites": [],
                                       "catalog_hits": u["catalog_hits"],
                                       "filename_hits": u["filename_hits"],
                                       "held": u["held"]})
    m["kind"] = "arxiv" if "arxiv" in (m["kind"], u["kind"]) else m["kind"]
    for c in u["cites"]:
        if c not in m["cites"]:
            m["cites"].append(c)
    m["catalog_hits"] = sorted(set(m["catalog_hits"]) | set(u["catalog_hits"]))
    m["filename_hits"] = sorted(set(m["filename_hits"]) | set(u["filename_hits"]))
    m["held"] = bool(m["catalog_hits"] or m["filename_hits"])
    # weak holding: only reference is a temp-path file (%TEMP%, tmpdir)
    if m["held"]:
        durable = [h for h in (m["catalog_hits"] + m["filename_hits"])
                   if "temp" not in h.lower() and "tmp" not in h.lower()]
        m["held_durable"] = bool(durable)
    else:
        m["held_durable"] = False

result = {"unique_count": len(merged), "error_rows": len(errors), "citations": list(merged.values())}
with open(os.path.join(LANES, "unique_citations.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1)

held = [u for u in merged.values() if u["held"]]
held_durable = [u for u in merged.values() if u.get("held_durable")]
print(json.dumps({
    "unique_citations": len(merged),
    "held_any": len(held),
    "held_durable": len(held_durable),
    "not_held": len(merged) - len(held),
    "error_rows": len(errors),
    "held_durable_values": sorted(u["value"] for u in held_durable),
    "weak_only_values": sorted(u["value"] for u in held if not u.get("held_durable")),
}, indent=2))
