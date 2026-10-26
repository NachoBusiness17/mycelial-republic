"""Final overlap grep for the remaining banked items (Mozilla benchmark, Step 5)."""
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")
MEMORY = os.path.join(ROOT, "memory")
PATTERNS = [
    "llamafile",
    "benchmarking local llm servers",
    "blog.mozilla.ai",
    "stepfun",
    "step-5-preview",
    "step 5 preview",
]

counts, files = {}, {}
def scan(path):
    try:
        text = open(path, "r", encoding="utf-8", errors="replace").read()
    except OSError:
        return
    low = text.lower()
    for p in PATTERNS:
        if p in low:
            counts[p] = counts.get(p, 0) + low.count(p)
            files.setdefault(p, set()).add(os.path.relpath(path, ROOT))

scan(CATALOG)
for dirpath, _dn, fns in os.walk(MEMORY):
    for name in fns:
        if name.endswith((".md", ".json", ".jsonl", ".txt")):
            scan(os.path.join(dirpath, name))

for p in PATTERNS:
    print(p, "->", counts.get(p, 0), "hits;", len(files.get(p, set())), "files;")
    for f in sorted(files.get(p, set()))[:4]:
        print("   ", f)
