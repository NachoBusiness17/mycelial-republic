import os, sys, traceback

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
catalog = os.path.join(ROOT, "catalog", "catalog.jsonl")

phrases = {
    "2610.02142": ["Keyword Harnesses Fail Open", "2610.02142", "diagnostic ladder"],
    "2610.11482": ["Evaluating Local Language Model Agents", "2610.11482", "mobility-workflow"],
    "2610.07781": ["Quantization Effects on Tool-Failure", "2610.07781", "tool-failure recovery"],
    "2610.07026": ["Offline AI Modules", "2610.07026", "Voice-First Offline"],
    "2601.14277": ["Which Quantization Should I Use", "2601.14277", "llama.cpp Quantization on Llama-3.1-8B"],
    "2610.07070": ["Turnslide", "2610.07070"],
    "2610.09346": ["OnlineQAT", "2610.09346"],
    "ollama-releases": ["MLX on Apple Silicon by default", "v0.40.0"],
    "airllm-hn": ["AirLLM"],
}

needles = sorted({n for v in phrases.values() for n in v})
low = {n: n.lower() for n in needles}
hits = {n: [] for n in needles}

def scan(path, rel):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                ll = line.lower()
                for n in needles:
                    if low[n] in ll and len(hits[n]) < 5:
                        hits[n].append("%s:%d: %s" % (rel, i, line.strip()[:140]))
                        print("HIT [%s] %s" % (n, hits[n][-1]), flush=True)
    except OSError:
        pass

if os.path.exists(catalog):
    scan(catalog, "catalog/catalog.jsonl")
else:
    print("CATALOG MISSING:", catalog, flush=True)

for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "memory")):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            if os.path.splitdrive(p)[0] != "C:":
                continue
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
        except (ValueError, OSError):
            continue
        scan(p, rel)

print("SCAN-DONE", flush=True)
for item_id, keys in phrases.items():
    print("### %s" % item_id, flush=True)
    for k in keys:
        h = hits.get(k, [])
        print("  [%s] hits=%d" % (k, len(h)), flush=True)
        for x in h[:3]:
            print("    ", x, flush=True)
