"""D24 sweep 2 — non-code reference check for the 175 pure-dead candidates.

Scans docs/, configs/, scripts/ (all types), queue/, root *.md/*.yaml/*.toml/*.cfg,
tests non-py, for word-boundary mentions of each candidate's short name.
Also collects line counts. Read-only except its own output JSON.
"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
os.chdir(ROOT)

probe = json.load(open("watch/inbox/wave_20260916/d24_triage_probe_out.json", encoding="utf-8"))
pure_dead = probe["pure_dead"]

def file_text(fp):
    try:
        return open(fp, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""

# ---- corpus: non-code operational surfaces ----
corpus = []  # (relpath, text)
for rel in ["docs", "configs", "scripts", "queue", "tests"]:
    for dirpath, dirnames, filenames in os.walk(rel):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules")]
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            corpus.append((os.path.relpath(fp, ROOT).replace("\\", "/"), file_text(fp)))
for fn in os.listdir(ROOT):
    if os.path.isfile(fn) and (fn.endswith(".md") or fn.endswith(".yaml") or fn.endswith(".yml")
                               or fn.endswith(".toml") or fn.endswith(".cfg") or fn.endswith(".json")
                               or fn.endswith(".ps1") or fn.endswith(".sh") or fn.endswith(".bat")):
        corpus.append((fn, file_text(fn)))
# dashboard non-py (html/js may embed command names)
for dirpath, dirnames, filenames in os.walk("dashboard"):
    dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "data", "static/estate_walk.html")]
    for fn in filenames:
        if not fn.endswith(".py"):
            fp = os.path.join(dirpath, fn)
            corpus.append((os.path.relpath(fp, ROOT).replace("\\", "/"), file_text(fp)))

names = {}
for dotted in pure_dead:
    short = dotted.split(".")[-1]
    names.setdefault(short, []).append(dotted)

results = {}
for short, dotted_list in names.items():
    pat = re.compile(r"\b%s\b" % re.escape(short))
    hits = []
    for rel, text in corpus:
        if pat.search(text):
            hits.append(rel)
    for dotted in dotted_list:
        fp = dotted.replace(".", "/") + ".py"
        n = len(file_text(fp).splitlines())
        results[dotted] = {"lines": n, "noncode_refs": sorted(set(hits))}

still_dead = [d for d, r in results.items() if not r["noncode_refs"]]
doc_only = [d for d, r in results.items() if r["noncode_refs"]]

json.dump(results, open("watch/inbox/wave_20260916/d24_sweep2_out.json", "w", encoding="utf-8"), indent=1)
print("candidates:", len(pure_dead), "| still zero-ref:", len(still_dead), "| doc/shell-referenced:", len(doc_only))
print()
print("DOC/SHELL-REFERENCED (demote to review):")
for d in sorted(doc_only):
    print(" ", d, "->", results[d]["noncode_refs"][:4])
