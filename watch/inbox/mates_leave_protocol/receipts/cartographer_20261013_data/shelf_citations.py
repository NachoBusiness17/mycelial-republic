#!/usr/bin/env python3
"""Shelf-level citation proxy for the cartographer's hunting ground.

One pass over the live (non-corpus) text surfaces collecting every
`corpus/<shelf>/...` reference, joined against a full corpus inventory.
Output: corpus_shelf_citations.json (per shelf: files, bytes, distinct cited,
citation_rate proxy). A proxy, not a registry: references are path/basename
string matches in live text surfaces (watch, memory, docs, mag, tools, queue,
state, configs, scripts, tests, scripts, .agents, handoff, window, work,
dashboard/static). Directory-level mentions that name no file are not credits.
"""
import io, json, os, re, sys
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
LIVE_DIRS = ["watch", "memory", "docs", "mag", "tools", "queue", "state", "configs",
             "scripts", "tests", ".agents", "handoff", "window", "work",
             os.path.join("dashboard", "static")]
TEXT_EXT = {".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".html", ".js",
            ".ps1", ".cmd", ".toml", ".cfg", ".ini", ".ipynb", ".csv", ".ts", ".sql",
            ".sh", ".css", ".xml", ".svg"}
REF_RE = re.compile(r"corpus/([A-Za-z0-9_\-]+)/([A-Za-z0-9_\-./%\[\]() ]+?)(?=[\"'\s)\]:,|]|$)")

def shelf_inventory():
    shelves = defaultdict(lambda: [0, 0, set()])  # files, bytes, basenames
    corpus_root = os.path.join(ROOT, "corpus")
    for shelf in os.listdir(corpus_root):
        p = os.path.join(corpus_root, shelf)
        if not os.path.isdir(p):
            continue
        inv = shelves[shelf]
        for dp, dn, fn in os.walk(p):
            for name in fn:
                fp = os.path.join(dp, name)
                try:
                    b = os.path.getsize(fp)
                except OSError:
                    continue
                inv[0] += 1
                inv[1] += b
                inv[2].add(name)
    return shelves

def scan_live():
    refs = defaultdict(set)  # shelf -> set(cited basename)
    ref_hits = defaultdict(int)
    for d in LIVE_DIRS:
        base = os.path.join(ROOT, d)
        for dp, dn, fn in os.walk(base):
            dn[:] = [x for x in dn if x not in ("node_modules", "__pycache__", ".git")]
            for name in fn:
                ext = os.path.splitext(name)[1].lower()
                if ext not in TEXT_EXT:
                    continue
                fp = os.path.join(dp, name)
                try:
                    if os.path.getsize(fp) > 20_000_000:
                        continue
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                except OSError:
                    continue
                for m in REF_RE.finditer(text):
                    shelf, rest = m.group(1), m.group(2)
                    base2 = rest.rstrip("/\\").split("/")[-1].split("\\")[-1]
                    if base2:
                        refs[shelf].add(base2)
                        ref_hits[shelf] += 1
    return refs, ref_hits

def main():
    inv = shelf_inventory()
    refs, ref_hits = scan_live()
    rows = []
    for shelf in sorted(inv):
        files, byts, names = inv[shelf]
        cited = refs.get(shelf, set())
        rate = (len(cited) / files * 100.0) if files else 0.0
        rows.append({
            "shelf": "corpus/" + shelf,
            "files": files,
            "bytes": byts,
            "distinct_cited_proxy": len(cited),
            "citation_rate_pct": round(rate, 2),
            "reference_instances": ref_hits.get(shelf, 0),
        })
    out = os.path.join(ROOT, r"logs\mates\cartographer\corpus_shelf_citations.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"instrument": "path/basename string-match proxy over live text dirs; "
                               "distinct cited basenames / shelf files; not a receipt registry",
                   "live_dirs": LIVE_DIRS, "shelves": rows}, f, ensure_ascii=False, indent=1)
    rows.sort(key=lambda r: r["citation_rate_pct"])
    print("%-46s %8s %14s %10s %7s %9s" % ("shelf", "files", "bytes", "cited", "rate%", "refhits"))
    for r in rows:
        print("%-46s %8d %14d %10d %7.2f %9d" % (
            r["shelf"], r["files"], r["bytes"], r["distinct_cited_proxy"],
            r["citation_rate_pct"], r["reference_instances"]))
    total_files = sum(r["files"] for r in rows)
    total_cited_files = None  # per-shelf union not computed (basenames overlap across shelves)
    print("corpus file total:", total_files)
    print("wrote", out)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
