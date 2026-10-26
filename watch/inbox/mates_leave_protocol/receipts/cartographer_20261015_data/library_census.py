#!/usr/bin/env python3
"""Library sub-shelf citation fold: 10-13 shelf_join instrument re-pointed.

Input: logs/mates/cartographer/library_refs_raw.txt (rg -o over the 15 live
text surfaces, collected 2026-10-15, cmd-redirected UTF-8).
Output: library_subshelf_citations.json + printed tables.
Same proxy semantics as cartographer_20261013_data/shelf_join.py:
basename-level distinct matching, directory mentions = hits without credit.
Raw refs regen (cmd redirect keeps UTF-8, the 10-13 UTF-16 lesson):
  cmd /c "rg -o -I --no-filename ""corpus/[A-Za-z0-9_\-./]+"" watch memory docs mag tools queue state configs scripts tests .agents handoff window work dashboard/static > logs\mates\cartographer\library_refs_raw.txt 2>nul"
"""
import io, json, os, sys, re
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
RAW = os.path.join(ROOT, r"logs\mates\cartographer\library_refs_raw.txt")
TAIL_RE = re.compile(r"[A-Za-z0-9_\-][A-Za-z0-9_\- .()\[\]]*\.[A-Za-z0-9]{1,8}$")

def dir_inventory(root):
    out = {}
    for entry in os.listdir(root):
        p = os.path.join(root, entry)
        if not os.path.isdir(p):
            continue
        n = 0; b = 0; names = set(); exts = defaultdict(int)
        for dp, dn, fn in os.walk(p):
            for name in fn:
                fp = os.path.join(dp, name)
                try:
                    bb = os.path.getsize(fp)
                except OSError:
                    continue
                n += 1; b += bb; names.add(name)
                exts[os.path.splitext(name)[1].lower() or "(none)"] += 1
        out[entry] = (n, b, names, exts)
    return out

def main():
    # parse raw refs once; keep shelf-level and library-sub-level credits
    shelf_refs = defaultdict(set)
    shelf_hits = defaultdict(int)
    sub_refs = defaultdict(set)      # key: library sub-shelf name
    sub_hits = defaultdict(int)
    sub_files_cited = defaultdict(set)  # full relpath under library, distinct
    with open(RAW, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or "/" not in line:
                continue
            parts = line.split("/", 2)
            if len(parts) < 3:
                continue
            shelf, rest = parts[1], parts[2]
            shelf_hits[shelf] += 1
            cand = rest.rstrip("/\\").split("/")[-1]
            if TAIL_RE.search(cand):
                shelf_refs[shelf].add(cand)
            if shelf == "library":
                sub = rest.split("/")[0] if "/" in rest else None
                if sub:
                    sub_hits[sub] += 1
                    if TAIL_RE.search(cand):
                        sub_refs[sub].add(cand)
                        sub_files_cited[sub].add(rest.rstrip("/\\").lower())

    # whole-corpus shelf table (today's moment, for comparability with 10-13)
    corpus_inv = dir_inventory(os.path.join(ROOT, "corpus"))
    shelf_rows = []
    for shelf, (files, byts, names, _e) in corpus_inv.items():
        cited = shelf_refs.get(shelf, set())
        rate = (len(cited) / files * 100.0) if files else 0.0
        shelf_rows.append({"shelf": "corpus/" + shelf, "files": files, "bytes": byts,
                           "distinct_cited_proxy": len(cited),
                           "citation_rate_pct": round(rate, 2),
                           "reference_instances": shelf_hits.get(shelf, 0)})

    # library sub-shelf table
    lib_inv = dir_inventory(os.path.join(ROOT, "corpus", "library"))
    sub_rows = []
    for sub, (files, byts, names, exts) in lib_inv.items():
        cited = sub_refs.get(sub, set())
        rate = (len(cited) / files * 100.0) if files else 0.0
        top_exts = sorted(exts.items(), key=lambda kv: -kv[1])[:4]
        sub_rows.append({
            "subshelf": "corpus/library/" + sub, "files": files, "bytes": byts,
            "distinct_cited_proxy": len(cited),
            "citation_rate_pct": round(rate, 2),
            "reference_instances": sub_hits.get(sub, 0),
            "never_cited_files": files - len(cited),
            "top_extensions": top_exts,
        })

    out = os.path.join(ROOT, r"logs\mates\cartographer\library_subshelf_citations.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "instrument": "basename-level proxy, 10-13 shelf_join semantics: rg -o over live "
                          "text dirs (watch memory docs mag tools queue state configs scripts "
                          "tests .agents handoff window work dashboard/static) 2026-10-15, "
                          "cmd-redirected UTF-8, 0 null bytes; distinct referenced basenames / "
                          "shelf file count; directory mentions counted as hits without credit; "
                          "raw_reference_lines today vs 262,280 on 2026-10-13",
            "raw_reference_lines": sum(shelf_hits.values()),
            "corpus_shelves_today": sorted(shelf_rows, key=lambda r: r["citation_rate_pct"]),
            "library_subshelves": sorted(sub_rows, key=lambda r: r["citation_rate_pct"]),
        }, f, ensure_ascii=False, indent=1)

    print("== corpus shelves today (ranked blank-first) ==")
    print("%-40s %8s %14s %7s %8s %9s" % ("shelf", "files", "bytes", "cited", "rate%", "refhits"))
    for r in sorted(shelf_rows, key=lambda r: r["citation_rate_pct"]):
        print("%-40s %8d %14d %7d %8.2f %9d" % (
            r["shelf"], r["files"], r["bytes"], r["distinct_cited_proxy"],
            r["citation_rate_pct"], r["reference_instances"]))
    print("total corpus files:", sum(r["files"] for r in shelf_rows))
    print()
    print("== library sub-shelves (ranked blank-first) ==")
    print("%-44s %7s %13s %6s %8s %8s %8s" % ("subshelf", "files", "bytes", "cited", "rate%", "refhits", "nevercit"))
    for r in sorted(sub_rows, key=lambda r: r["citation_rate_pct"]):
        print("%-44s %7d %13d %6d %8.2f %8d %8d" % (
            r["subshelf"].replace("corpus/library/", ""), r["files"], r["bytes"],
            r["distinct_cited_proxy"], r["citation_rate_pct"],
            r["reference_instances"], r["never_cited_files"]))
    print("library files total:", sum(r["files"] for r in sub_rows))
    print("wrote", out)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
