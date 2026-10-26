"""Overlap scan for finetuning-adaptation X sweep, 2026-10-09.
Scans catalog/catalog.jsonl (full, 384MB) and memory/ text files (cap 30MB/file)
for finetuning-topic terms, and decodes X snowflake status IDs to UTC dates.
Run: .venv\\Scripts\\python.exe watch\\inbox\\frontier_olm_2026-10-09\\sweep\\overlap_scan.py
"""
import os, re, sys, json

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
TERMS = {
    "lora": re.compile(r"\blora\b", re.I),
    "qlora": re.compile(r"\bqlora\b", re.I),
    "peft": re.compile(r"\bpeft\b", re.I),
    "unsloth": re.compile(r"unsloth", re.I),
    "finetune": re.compile(r"fine[-_ ]?tun", re.I),
    "gguf": re.compile(r"\bgguf\b", re.I),
    "adapter_tuning": re.compile(r"adapter[- ]tun", re.I),
}

def scan_catalog():
    cat = os.path.join(ROOT, "catalog", "catalog.jsonl")
    counts = {k: 0 for k in TERMS}
    samples = []
    with open(cat, encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f):
            hits = [k for k, rx in TERMS.items() if rx.search(line)]
            if not hits:
                continue
            for k in hits:
                counts[k] += 1
            if len(samples) < 40:
                m = re.search(r'"(?:title|name)"\s*:\s*"([^"]{0,160})"', line)
                p = re.search(r'"(?:path|url|source|file)"\s*:\s*"([^"]{0,160})"', line)
                samples.append((n + 1, ",".join(hits), m.group(1) if m else "", p.group(1) if p else ""))
    print("CATALOG_COUNTS(line_hits):", json.dumps(counts))
    for s in samples:
        print("CAT_SAMPLE:", json.dumps(s))

def scan_memory():
    mem = os.path.join(ROOT, "memory")
    counts = {k: 0 for k in TERMS}
    samples = []
    skipped_big = 0
    bytes_read = 0
    lens_hits = []
    lens_rx = re.compile(r"day-?8|unbanked|skills_pack|case_law", re.I)
    for dirpath, dirs, files in os.walk(mem):
        for fn in files:
            if not fn.lower().endswith((".md", ".json", ".jsonl", ".txt")):
                continue
            full = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(full)
            except OSError:
                continue
            if sz > 30_000_000:
                skipped_big += 1
                continue
            try:
                with open(full, encoding="utf-8", errors="replace") as f:
                    data = f.read(5_000_000)
            except OSError:
                continue
            bytes_read += len(data)
            for k, rx in TERMS.items():
                c = len(rx.findall(data))
                if c:
                    counts[k] += 1
                    if len(samples) < 60:
                        samples.append((os.path.relpath(full, ROOT), k, c))
            if lens_rx.search(data) and "frontier" in full.lower():
                lens_hits.append(os.path.relpath(full, ROOT))
    print("MEMORY_COUNTS(files_matched):", json.dumps(counts), "skipped_big:", skipped_big, "bytes_read:", bytes_read)
    for s in samples:
        print("MEM_SAMPLE:", json.dumps(s))
    print("LENS_FRONTIER_FILES:", lens_hits[:20])

def decode_snowflakes(ids):
    for sid in ids:
        ms = (int(sid) >> 22) + 1288834974657
        import datetime
        print("SNOWFLAKE:", sid, datetime.datetime.utcfromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%SZ"))

if __name__ == "__main__":
    scan_catalog()
    scan_memory()
    ids = sys.argv[1:] if len(sys.argv) > 1 else []
    if ids:
        decode_snowflakes(ids)
