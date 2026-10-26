import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
catalog = os.path.join(ROOT, "catalog", "catalog.jsonl")

phrases = [
    ("2610.02142", ["Keyword Harnesses Fail Open", "2610.02142", "diagnostic ladder for tool-use"]),
    ("2610.11482", ["Evaluating Local Language Model Agents", "2610.11482", "mobility-workflow"]),
    ("2610.07781", ["Quantization Effects on Tool-Failure Recovery", "2610.07781", "tool-failure recovery"]),
    ("2610.07026", ["Offline AI Modules", "2610.07026", "Voice-First Offline Architecture"]),
    ("2601.14277", ["Which Quantization Should I Use", "2601.14277", "Unified Evaluation of llama.cpp Quantization"]),
    ("2610.07070", ["Turnslide", "2610.07070", "Finite-State Machine"]),
    ("2610.09346", ["OnlineQAT", "2610.09346", "on-policy distillation"]),
    ("ollama-releases", ["ollama/ollama/releases", "v0.40.0", "MLX on Apple Silicon by default"]),
]

def hits(path, needle, limit=3):
    out = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if needle.lower() in line.lower():
                    out.append((i, line.strip()[:200]))
                    if len(out) >= limit:
                        break
    except FileNotFoundError:
        return [("missing", "file not found")]
    return out

cat_lines = []
try:
    with open(catalog, "r", encoding="utf-8", errors="replace") as fh:
        cat_lines = fh.readlines()
except FileNotFoundError:
    print("CATALOG MISSING:", catalog)

memory_hits = {}
mem_root = os.path.join(ROOT, "memory")
for dirpath, dirnames, filenames in os.walk(mem_root):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                memory_hits[p] = fh.read()
        except OSError:
            pass

for item_id, keys in phrases:
    print("###", item_id)
    for key in keys:
        c = [(i, l) for i, l in enumerate(cat_lines, 1) if key.lower() in l.lower()]
        m = [(p, memory_hits[p].count(key)) for p in memory_hits if key.lower() in memory_hits[p].lower()]
        print("  [%s] catalog:%d memory_files:%d" % (key, len(c), len(m)))
        for i, l in c[:2]:
            print("    cat L%d: %s" % (i, l.strip()[:180]))
        for p, n in m[:3]:
            print("    mem %s x%d" % (os.path.relpath(p, ROOT), n))
print("DONE catalog_lines=%d memory_files=%d" % (len(cat_lines), len(memory_hits)))
