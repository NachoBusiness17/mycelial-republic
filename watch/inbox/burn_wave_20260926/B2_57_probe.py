"""B2-57 probe: byte-check UF-119 attack claims against tools/corpus.py live.
Read-only probes. Runs each numbered claim's exact scenario."""
import json
import sys

sys.path.insert(0, r"C:/Users/foste/Documents/projects/local_sovereign_agent")
from tools.corpus import corpus_search, corpus_get, corpus_tail, corpus_stats, _zone_of, _confine  # noqa: E402

out = {}

# Claim 1: zone filter bypass -- does zone="code" leak rows of other zones?
r = corpus_search(query="grounding", zone="code", limit=100)
zones = sorted({h["zone"] for h in r.get("hits", [])})
out["c1_zone_filter"] = {"hit_count": r.get("hit_count"), "zones_seen": zones}
# does a zone named "public" exist at all?
s = corpus_stats()
out["c1_zone_names"] = sorted(s.get("zones", {}).keys())

# Claim 3: is "a b" tokenized AND or single substring?
r = corpus_search(query="grounding chain resync", limit=5)
out["c3_token_and"] = {"hit_count": r.get("hit_count"),
                       "first_paths": [h["path"] for h in r.get("hits", [])[:3]]}
# counter-probe: exact phrase that never appears as a substring but both tokens exist
r2 = corpus_search(query="resync grounding", limit=5)
out["c3_order_swap"] = {"hit_count": r2.get("hit_count")}

# Claim 5: corpus_tail lines=500 on catalog.jsonl (long JSONL rows, 256KB window)
r = corpus_tail("catalog/catalog.jsonl", lines=500)
out["c5_tail_catalog"] = {"lines_served": r.get("lines_served"),
                          "bytes_total": r.get("bytes_total"),
                          "ok": r.get("ok")}

# Claim 7: truncation invisibility -- common term, limit=100
r = corpus_search(query="md", limit=100)
out["c7_truncation"] = {"hit_count": r.get("hit_count"),
                        "rows_scanned": r.get("rows_scanned"),
                        "keys": sorted(r.keys())}

# Claim 8: path traversal refusals
out["c8_traversal"] = {
    "dotdot": corpus_get("../../etc/passwd"),
    "abs": corpus_get("C:/Windows/win.ini"),
    "confine_escape": _confine("../../foste") is None,
}
# claim 8 nuance: uncatalogued-but-on-disk file served?
import os.path
probe_rel = "watch/inbox/burn_wave_20260926/QUEUE.md"
in_catalog = False
with open(r"C:/Users/foste/Documents/projects/local_sovereign_agent/catalog/catalog.jsonl", encoding="utf-8") as fh:
    for ln in fh:
        if probe_rel in ln:
            in_catalog = True
            break
g = corpus_get(probe_rel, max_bytes=200)
out["c8_uncatalogued"] = {"path": probe_rel, "in_catalog": in_catalog,
                          "get_ok": g.get("ok"), "sha256": g.get("sha256", "")[:12]}

# Claim 2/6: staleness -- search vs get for a file created today
r = corpus_search(query="B2_57_probe", limit=10)
out["c2_staleness_search"] = {"hit_count": r.get("hit_count")}
g = corpus_get("watch/inbox/burn_wave_20260926/B2_57_probe.py", max_bytes=100)
out["c2_staleness_get"] = {"ok": g.get("ok"), "bytes_total": g.get("bytes_total")}

# Claim 4: binary refusal exists; sniff is 8KB null-byte head
bg = corpus_get("catalog/tags.jsonl", max_bytes=50)  # text sanity
out["c4_text_serve_ok"] = bg.get("ok")
# craft no file; just verify the guard source line
import inspect
from tools import corpus as C
src = inspect.getsource(C._is_text)
out["c4_sniff_src"] = " ".join(src.split())
src_get = [l.strip() for l in inspect.getsource(C.corpus_get).splitlines() if "binary refused" in l]
out["c4_binary_refusal_line"] = src_get

# UF-122: do the spec's example anchor files exist?
anchors = ["intake/sla_policy.md", "astra/config_reference.md", "watch/detector_rules.py",
           "doctrine/core_principles.md", "runs/error_codes.json", "memory/retention_policy.md",
           "code/defaults.py", "games/rules.md", "dashboard/widget_config.yaml",
           "research/sources.md", "ext/dependencies.txt"]
out["uf122_anchors_exist"] = {a: os.path.isfile(os.path.join(r"C:/Users/foste/Documents/projects/local_sovereign_agent", a)) for a in anchors}

# UF-122: zone arithmetic -- real zone census
out["uf122_zone_census"] = s.get("zones")

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
