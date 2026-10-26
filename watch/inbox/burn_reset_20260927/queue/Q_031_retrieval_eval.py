"""Q-031 held-out 50-question retrieval eval against catalog/catalog.jsonl.

Protocol (held-out, stated so it can be attacked):
  - Surface under test: tools/corpus.py corpus_search (the sanctioned
    read-only catalog retrieval surface; FTS5 path+title index at
    catalog/catalog_fts.sqlite when its freshness gate passes, JSONL scan
    otherwise). The module landed 2026-09-26 and was NOT changed for this
    eval. The tags v2 owner column is outside the query path (corpus_search
    only reads tags.jsonl when a kind filter is passed; none is here).
  - Gold set: 50 rows drawn once with random.Random(20260928).sample over
    the 581,477 catalog rows that carry a path. Both surfaces were frozen
    before the draw; no query was tuned per row; all 50 gold ids and every
    per-question verdict are published next to this script.
  - Questions: built ONLY from the gold row's own stored fields. If the
    row's title differs from its basename the question is the title, else
    the basename stem; tokenized to [a-z0-9]{3,}, deduped, order kept.
    This mirrors "find the file I half-remember by name/title", the lookup
    a catalog map actually promises; it is lexical retrieval, not semantic.
  - Engine semantics being scored: AND of quoted prefix terms over
    path+title, hits returned in catalog line order (the engine's real
    order, parity with the scan path). accuracy@1 = first hit is the gold
    id; accuracy@10 = gold id within the first 10 hits.
  - "Held out" here means: seeded draw after the code was frozen, zero
    per-question tuning, full publication of the gold set. It is not a
    human-written query set; nobody annotated relevance beyond id equality.

Usage:
    .venv/Scripts/python.exe watch/inbox/burn_reset_20260927/queue/Q_031_retrieval_eval.py
    .venv/Scripts/python.exe ... --out PATH --n 50 --seed 20260928

No subprocess is spawned; the corpus module is loaded in-process.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_corpus_module():
    spec = importlib.util.spec_from_file_location(
        "corpus_readonly", REPO / "tools" / "corpus.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def question_terms(row):
    """Query terms from the gold row's own stored fields only."""
    path = str(row.get("path", ""))
    base = path.rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0] if "." in base else base
    title = str(row.get("title", "") or "").strip()
    src = title if title and title.lower() != base.lower() else stem
    terms = []
    for t in re.split(r"[^a-z0-9]+", src.lower()):
        if len(t) >= 3 and t not in terms:
            terms.append(t)
    if not terms:  # degenerate title; fall back to the basename stem
        for t in re.split(r"[^a-z0-9]+", stem.lower()):
            if len(t) >= 3 and t not in terms:
                terms.append(t)
    return terms


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20260928)
    ap.add_argument("--out", default=str(
        REPO / "watch/inbox/burn_reset_20260927/queue/"
               "Q_031_retrieval_eval_results.json"))
    a = ap.parse_args()

    cat_path = REPO / "catalog" / "catalog.jsonl"
    rows = []
    base_counts = Counter()
    with open(cat_path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("path"):
                r["_line"] = i
                rows.append(r)
                base_counts[str(r["path"]).rsplit("/", 1)[-1].lower()] += 1

    gold = random.Random(a.seed).sample(rows, a.n)
    corpus = load_corpus_module()

    per_q = []
    top1 = top10 = no_terms = 0
    engines = Counter()
    hit_lines_gold = []
    uniq_hits = Counter()   # gold basename unique in catalog vs shared
    for g in gold:
        gid = g.get("id")
        rec = {"gold_id": gid, "gold_path": g.get("path"),
               "gold_line": g["_line"], "gold_title": g.get("title")}
        terms = question_terms(g)
        rec["question_terms"] = terms
        if not terms:
            no_terms += 1
            rec["verdict"] = "unanswerable_no_terms"
            per_q.append(rec)
            continue
        rec["question"] = " ".join(terms)
        res = corpus.corpus_search(query=rec["question"], limit=10)
        engine = "%s/%s" % (res.get("engine"), res.get("index_state"))
        engines[engine] += 1
        rec["engine"] = engine
        ids = [h.get("id") for h in res.get("hits", [])]
        rec["top10_ids"] = ids
        hit_at = ids.index(gid) + 1 if gid in ids else None
        rec["hit_at"] = hit_at
        if hit_at == 1:
            top1 += 1
        if hit_at is not None:
            top10 += 1
            hit_lines_gold.append(g["_line"])
            key = ("basename_unique" if
                   base_counts[str(g["path"]).rsplit("/", 1)[-1].lower()] == 1
                   else "basename_shared")
            uniq_hits[key] += 1
        rec["verdict"] = ("top1" if hit_at == 1 else
                          ("top10" if hit_at else "miss"))
        per_q.append(rec)

    n_ans = a.n - no_terms
    summary = {
        "item": "Q-031",
        "eval": "held-out 50-question retrieval eval vs catalog/catalog.jsonl",
        "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "catalog": "catalog/catalog.jsonl",
        "catalog_bytes": cat_path.stat().st_size,
        "catalog_sha256": sha256_file(cat_path),
        "catalog_rows_with_path": len(rows),
        "seed": a.seed,
        "n_questions": a.n,
        "answerable": n_ans,
        "accuracy_at_1": round(top1 / n_ans, 4) if n_ans else None,
        "accuracy_at_10": round(top10 / n_ans, 4) if n_ans else None,
        "top1_hits": top1,
        "top10_hits": top10,
        "unanswerable_no_terms": no_terms,
        "engine_counts": dict(engines),
        "top10_by_basename": dict(uniq_hits),
        "gold_line_numbers": hit_lines_gold,
        "protocol": (__doc__ or "").strip(),
    }
    out = {"summary": summary, "per_question": per_q}
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=True, indent=1)
        fh.write("\n")

    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ("protocol", "gold_line_numbers")},
                     indent=2))
    print("results file:", a.out)


if __name__ == "__main__":
    main()
