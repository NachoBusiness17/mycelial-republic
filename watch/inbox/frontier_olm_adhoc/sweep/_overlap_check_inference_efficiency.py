"""Overlap check for the inference-efficiency-hn sweep (2026-10-11).

Greps catalog/catalog.jsonl and memory/ (recursively) for each banked item's
distinctive phrase. Prints match counts + files so the overlap field of each
banked item is byte-backed, not guessed. Receipt for the sweep write-up.
"""
import json
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")
MEMORY = os.path.join(ROOT, "memory")

PATTERNS = [
    "DeepSeek 4.1 Flash",
    "dgt.is",
    "Cactus Needle",
    "cactuscompute",
    "cactus-compute",
    "Magnitude",
    "magnitudedev",
    "planetscale",
    "Windows ML",
    "winml",
    "foundry-on-windows",
    "prompt lookup",
    "jadidbourbaki",
    "zartbot",
    "dsv41flash",
    "890 bytes",
    "better prompt caching",
    "prompt caching",
    "GPT-6",
    "Leviathan",
    "terrydjony",
    "bestmodelforyourbudget",
    "FunctionGemma",
]


def scan_file(path, patterns, counts, files):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return
    low = text.lower()
    for p in patterns:
        if p.lower() in low:
            counts[p] = counts.get(p, 0) + low.count(p.lower())
            files.setdefault(p, set()).add(os.path.relpath(path, ROOT))


def main():
    counts, files = {}, {}
    scan_file(CATALOG, PATTERNS, counts, files)
    mem_files = 0
    for dirpath, _dirnames, filenames in os.walk(MEMORY):
        for name in filenames:
            if name.endswith((".md", ".json", ".jsonl", ".txt")):
                mem_files += 1
                scan_file(os.path.join(dirpath, name), PATTERNS, counts, files)
    out = {"catalog_lines": None, "memory_files_scanned": mem_files, "patterns": {}}
    with open(CATALOG, "r", encoding="utf-8", errors="replace") as fh:
        out["catalog_lines"] = sum(1 for _ in fh)
    for p in PATTERNS:
        hit_files = sorted(files.get(p, []))[:6]
        out["patterns"][p] = {
            "count": counts.get(p, 0),
            "files": hit_files,
            "total_files": len(files.get(p, set())),
        }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
