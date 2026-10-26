import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
catalog = os.path.join(ROOT, "catalog", "catalog.jsonl")

needles = [
    "2610.11482", "Evaluating Local Language Model Agents", "mobility",
    "2610.07026", "Offline AI Modules", "gemma-4", "gemma4",
    "2601.14277", "Which Quantization", "Q4_K_S", "Kurt",
    "2610.07070", "Turnslide", "Finite-State Machine",
    "2610.02142", "Keyword Harnesses",
    "2610.07781", "Tool-Failure",
    "ollama", "Ollama", "v0.40", "MLX on Apple Silicon",
    "frontier_olm_2026-10-02", "frontier_olm_2026-10-07",
]
low = [n.lower() for n in needles]
counts = {n: 0 for n in needles}
rows = {n: [] for n in needles}

with open(catalog, "r", encoding="utf-8", errors="replace") as fh:
    for i, line in enumerate(fh, 1):
        ll = line.lower()
        for n, l in zip(needles, low):
            if l in ll:
                counts[n] += 1
                if len(rows[n]) < 4:
                    rows[n].append("L%d: %s" % (i, line.strip()[:190]))

for n in needles:
    print("[%s] total=%d" % (n, counts[n]))
    for r in rows[n]:
        print("   ", r)
