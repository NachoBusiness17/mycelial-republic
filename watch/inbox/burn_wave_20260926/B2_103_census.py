"""B2-103 path-anchoring census over catalog/catalog.jsonl (read-only, 2026-09-26).

Classifies every row's path anchor and measures the drift disease named in the
brief: bare projects-root paths (AGENTS.md), local_sovereign_agent/-prefixed
paths, sibling-project tops, one-physical-file-two-ids signatures, and whether
the classes seam by line range (multi-run append) or interleave (single walk).
Emits JSON on stdout. Never writes.
"""
from __future__ import annotations

import collections
import json
import sys

CATALOG = r"C:\Users\foste\Documents\projects\local_sovereign_agent\catalog\catalog.jsonl"
PREF = "local_sovereign_agent"


def classify(path):
    parts = path.split("/")
    top = parts[0]
    if top == PREF:
        if len(parts) > 1 and parts[1] == PREF:
            return "prefixed_nested_mirror"
        return "prefixed_repo"
    return "bare_projects_root:" + top


def main():
    rows = 0
    bad = 0
    classes = collections.Counter()
    dup_path = collections.Counter()
    dup_id = collections.Counter()
    bare_pref_pair = {}          # bare rel -> (bytes, mtime) ; repo twin check
    head_hist = collections.Counter()
    tail_hist = collections.Counter()
    first_line_of_class = {}
    bare_first = []              # (line, path) first 10 bare rows
    pair_collisions = []         # bare X + prefixed repo X, bytes+mtime equal
    pair_examples = []
    total = 0
    with open(CATALOG, encoding="utf-8") as fh:
        for line in fh:
            total += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            rows += 1
            path = str(row.get("path", ""))
            cls = classify(path)
            if cls.startswith("bare_projects_root:"):
                top = cls.split(":", 1)[1]
                classes["bare:" + top] += 1
                if len(bare_first) < 10:
                    bare_first.append([total, path])
                if "/" not in path:
                    bare_pref_pair[path] = (row.get("bytes"), row.get("mtime"),
                                            total)
            else:
                classes[cls] += 1
            if cls == "prefixed_repo" and row.get("id"):
                rel = path[len(PREF) + 1:]
                if "/" not in rel and rel in bare_pref_pair:
                    bb, bm, _ = bare_pref_pair[rel]
                    if bb == row.get("bytes") and bm == row.get("mtime"):
                        pair_collisions.append(rel)
                    elif len(pair_examples) < 8:
                        pair_examples.append(
                            {"rel": rel, "bare": [bb, bm],
                             "repo": [row.get("bytes"), row.get("mtime")]})
            dup_path[path] += 1
            dup_id[str(row.get("id", ""))] += 1
            if total <= 50000:
                head_hist[cls.split(":")[0] if cls.startswith("bare") else cls] += 1
            if cls not in first_line_of_class:
                first_line_of_class[cls] = total
    tail_n = 0
    with open(CATALOG, encoding="utf-8") as fh:
        for line in reversed(fh.readlines()[-50000:]):
            tail_n += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            cls = classify(str(row.get("path", "")))
            tail_hist[cls.split(":")[0] if cls.startswith("bare") else cls] += 1

    dup_paths = {p: c for p, c in dup_path.items() if c > 1}
    dup_ids = {i: c for i, c in dup_id.items() if c > 1}
    top_counts = collections.Counter()
    for k, v in classes.items():
        top_counts[k.split(":")[0] if k.startswith("bare") else k] += v
    bare_tops = collections.Counter()
    for k, v in classes.items():
        if k.startswith("bare:"):
            bare_tops[k.split(":", 1)[1]] += v

    out = {
        "catalog": CATALOG,
        "total_lines": total,
        "rows_parsed": rows,
        "bad_lines": bad,
        "class_groups": dict(top_counts),
        "sibling_and_bare_tops": {
            "bare_projects_root_tops": dict(
                sorted(bare_tops.items(), key=lambda kv: -kv[1])[:20]),
        },
        "dup_path_strings": {"count": len(dup_paths),
                             "examples": dict(list(sorted(
                                 dup_paths.items(), key=lambda kv: -kv[1]))[:10])},
        "dup_ids": {"count": len(dup_ids),
                    "examples": dict(list(sorted(
                        dup_ids.items(), key=lambda kv: -kv[1]))[:10])},
        "bare_vs_repo_twin_same_bytes_mtime": {
            "count": len(pair_collisions), "rels": pair_collisions[:10]},
        "bare_vs_repo_tune_differs": {"count": len(pair_examples),
                                      "examples": pair_examples},
        "first_10_bare_rows": bare_first,
        "first_line_of_class": {k: v for k, v in
                                sorted(first_line_of_class.items(),
                                       key=lambda kv: kv[1])},
        "head_50k_class_hist": dict(head_hist),
        "tail_50k_class_hist": dict(tail_hist),
    }
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
