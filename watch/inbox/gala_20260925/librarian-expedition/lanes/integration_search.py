"""Integration-lane search driver (read-only).

Runs tools/corpus.py corpus_search -- the estate's real search surface -- for
each gathered primary, through the same hermetic load pattern
tools/corpus_fts_rebuild.py uses. Prints one JSON line per query:
query, engine, index_state, index_note, hit_count, hits (max 5).
Also prints the raw _fts_state() verdict first.

Usage:
    .venv/Scripts/python.exe integration_search.py [before|after] [tag]
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]

spec = importlib.util.spec_from_file_location("corpus_readonly", REPO / "tools" / "corpus.py")
corpus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corpus)

# One query per gathered primary (10 gathered files):
# 7 persona prior-art PDFs by arxiv id, 2 early-computing texts by author
# token, 1 descent steal by path phrase. Chosen so the same tokens match in
# BOTH engines (scan = substring AND; fts5 = quoted prefix phrase AND).
QUERIES = [
    "2310.10158",
    "2405.07248",
    "2506.11798",
    "2506.12657",
    "2508.06149",
    "2508.06950",
    "2511.17813",
    "wilkes",
    "godfrey edvac",
    "descent_day1",
]

# Parity probe: a multi-word query whose FTS phrase tokens are not adjacent
# in the target path (wilkes W wheeler) -- documents the B2-22 parity law.
PARITY_QUERY = "wilkes wheeler"


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "run"
    tag = sys.argv[2] if len(sys.argv) > 2 else ""
    state, note = corpus._fts_state()
    print(json.dumps({"probe": "fts_state", "phase": phase, "tag": tag,
                      "index_state": state, "note": note}))
    for q in QUERIES + [PARITY_QUERY]:
        res = corpus.corpus_search(q, limit=5)
        hits = [{"path": h.get("path"), "zone": h.get("zone"),
                 "mtime": h.get("mtime")} for h in res.get("hits", [])]
        print(json.dumps({"query": q, "engine": res.get("engine"),
                          "index_state": res.get("index_state"),
                          "hit_count": res.get("hit_count"), "hits": hits}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
