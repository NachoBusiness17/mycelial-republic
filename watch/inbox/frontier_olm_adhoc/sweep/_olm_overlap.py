import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
catalog = os.path.join(ROOT, "catalog", "catalog.jsonl")

phrases = {
    "2610.04403": ["2610.04403", "Saying, Not Knowing", "GGUF-Quantized Small Language Models Still Write Rare Words"],
    "2609.23742": ["2609.23742", "Constrained Decoding Eliminates Structural Failures", "Scale-Dependent Semantic Gap"],
    "2610.09163": ["2610.09163", "ToolRACER", "Robust Agentic Conversation Emulation"],
    "2609.21704": ["2609.21704", "SpecQuant", "Multi-Parent Quantization"],
    "2609.14144": ["2609.14144", "One Size Does Not Fit All", "Inference Depth from the Questions"],
    "2610.02516": ["2610.02516", "Student-Guided Teacher Distillation", "Jev-Style System-1 Classifiers"],
    "ollama-p3": ["v0.32.1 ", "repeat_penalty", "Gemma 4 tool calling", "Nemotron 3.5 Lightning", "Muse Glimmer"],
    "lemmy-lane": ["sh.itjust.works", "lemmy.world/api", "localllama"],
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
                        hits[n].append("%s:%d: %s" % (rel, i, line.strip()[:150]))
    except OSError:
        pass

if os.path.exists(catalog):
    scan(catalog, "catalog/catalog.jsonl")
else:
    print("CATALOG MISSING:", catalog)

for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "memory")):
    if os.sep + "runs" + os.sep in dirpath + os.sep:
        continue
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            if os.path.splitdrive(p)[0] != "C:":
                continue
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
        except (ValueError, OSError):
            continue
        scan(p, rel)

print("SCAN-DONE")
for item_id, keys in phrases.items():
    print("### %s" % item_id)
    for k in keys:
        h = hits.get(k, [])
        print("  [%s] hits=%d" % (k, len(h)))
        for x in h[:3]:
            print("    ", x)
