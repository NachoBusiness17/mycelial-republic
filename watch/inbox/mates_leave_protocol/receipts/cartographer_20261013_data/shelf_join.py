#!/usr/bin/env python3
"""Join the rg-collected corpus references against the corpus inventory.

Input: logs/mates/cartographer/shelf_refs_raw.txt (262,280 reference strings,
one per line, collected by ripgrep over live text surfaces).
Output: corpus_shelf_citations.json + printed table.
Proxy instrument, not a receipt registry: basename-level distinct matching.
"""
import io, json, os, sys, re
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
RAW = os.path.join(ROOT, r"logs\mates\cartographer\shelf_refs_raw.txt")

def shelf_inventory():
    shelves = {}
    corpus_root = os.path.join(ROOT, "corpus")
    for shelf in os.listdir(corpus_root):
        p = os.path.join(corpus_root, shelf)
        if not os.path.isdir(p):
            continue
        n = 0; b = 0; names = set()
        for dp, dn, fn in os.walk(p):
            for name in fn:
                fp = os.path.join(dp, name)
                try:
                    bb = os.path.getsize(fp)
                except OSError:
                    continue
                n += 1; b += bb; names.add(name)
        shelves[shelf] = (n, b, names)
    return shelves

def main():
    refs = defaultdict(set)
    hits = defaultdict(int)
    tail_re = re.compile(r"[A-Za-z0-9_\-][A-Za-z0-9_\- .()\[\]]*\.[A-Za-z0-9]{1,8}$")
    with open(RAW, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or "/" not in line:
                continue
            parts = line.split("/", 2)
            if len(parts) < 3:
                continue
            shelf, rest = parts[1], parts[2]
            cand = rest.rstrip("/\\").split("/")[-1]
            if not tail_re.search(cand):
                # reference names a directory, not a file: count as a hit, no basename credit
                hits[shelf] += 1
                continue
            refs[shelf].add(cand)
            hits[shelf] += 1
    inv = shelf_inventory()
    rows = []
    for shelf in sorted(inv):
        files, byts, names = inv[shelf]
        cited = refs.get(shelf, set())
        rate = (len(cited) / files * 100.0) if files else 0.0
        rows.append({"shelf": "corpus/" + shelf, "files": files, "bytes": byts,
                     "distinct_cited_proxy": len(cited),
                     "citation_rate_pct": round(rate, 2),
                     "reference_instances": hits.get(shelf, 0)})
    out = os.path.join(ROOT, r"logs\mates\cartographer\corpus_shelf_citations.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"instrument": "basename-level proxy: rg over live text dirs "
                   "(watch memory docs mag tools queue state configs scripts tests .agents handoff window work dashboard/static); "
                   "distinct referenced basenames / shelf file count; directory mentions counted as hits without basename credit",
                   "raw_reference_lines": sum(hits.values()), "shelves": rows},
                  f, ensure_ascii=False, indent=1)
    rows.sort(key=lambda r: r["citation_rate_pct"])
    print("%-44s %8s %14s %8s %7s %9s" % ("shelf", "files", "bytes", "cited", "rate%", "refhits"))
    for r in rows:
        print("%-44s %8d %14d %8d %7.2f %9d" % (
            r["shelf"], r["files"], r["bytes"], r["distinct_cited_proxy"],
            r["citation_rate_pct"], r["reference_instances"]))
    print("total corpus files:", sum(r["files"] for r in rows))
    print("wrote", out)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
