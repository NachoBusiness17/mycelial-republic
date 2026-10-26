# Single-pass overlap scan for the window-2 finetuning-and-adaptation-reddit sweep.
# One read of each file under catalog/ + memory/, all terms tested per file.
# Disposable tool; repo venv interpreter per AGENTS.md python-env law.
import os, sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
TERMS = ["1wkorli", "1wjnklv", "1wkwz69", "1wgvfpr", "1wefk8o", "1wgxzvw",
         "1wavhij", "1w7umnd", "1wcqa03", "1weum85", "1wj6c4l",
         "bonsai", "tppo", "oui-1", "mql5", "lorivo", "2608.27448",
         "2610.02199", "ternary"]

hits = {t: [] for t in TERMS}
cat_count = {t: 0 for t in TERMS}

cat = os.path.join(ROOT, "catalog", "catalog.jsonl")
with open(cat, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        low = line.lower()
        for t in TERMS:
            if t in low:
                cat_count[t] += 1

mem = os.path.join(ROOT, "memory")
nfiles = 0
for dirpath, dirnames, filenames in os.walk(mem):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                low = f.read().lower()
        except Exception:
            continue
        nfiles += 1
        for t in TERMS:
            if t in low:
                hits[t].append(os.path.relpath(p, ROOT))

print("memory files scanned: %d" % nfiles)
for t in TERMS:
    fl = hits[t]
    print("%s | catalog=%d | memory=%d %s" % (t, cat_count[t], len(fl), "; ".join(fl[:4])))
