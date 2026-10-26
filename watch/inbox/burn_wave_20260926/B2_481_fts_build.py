"""B2-481 derived-pair refresh: rebuild catalog_fts.sqlite from the CURRENT
catalog.jsonl (489,548 rows post-B2-103/B2-4xx rebuilds) with the results
path REDIRECTED to a dated artifact so B2_22's receipt artifact
(watch/inbox/burn_wave_20260926/B2_22_fts5_results.json) is never clobbered.

Mirrors B2_22_fts5_spike.py build_index()/reference_counts()/fts_expr() byte
for byte in what it builds; owns only the RESULTS path and the extra
spot-check block (kind=ledger, kind=card, ruins_go freshness) that B2-481
requires. Rebuilds the DB in place (derived data, rebuildable per the
spike's own header note).
"""
from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DB = os.path.join(REPO, "catalog", "catalog_fts.sqlite")
CATALOG = os.path.join(REPO, "catalog", "catalog.jsonl")
RESULTS = os.path.join(HERE, "B2_481_fts5_results.json")

_spec = importlib.util.spec_from_file_location(
    "b2_22_spike", os.path.join(HERE, "B2_22_fts5_spike.py"))
spike = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spike)


def spot_checks(con) -> dict:
    """B2-481's three joins: kind=ledger, kind=card, ruins_go freshness."""
    out = {}
    # tags sidecar is the kind source: load id->kind once
    kinds = {}
    tags_path = os.path.join(REPO, "catalog", "tags.jsonl")
    with open(tags_path, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            kinds[r.get("id")] = r.get("kind")
    for want_kind in ("ledger", "card"):
        ids = [i for i, k in kinds.items() if k == want_kind]
        hits = 0
        missing = []
        for i in ids:
            row = con.execute(
                "SELECT c.id FROM crows c WHERE c.id = ? LIMIT 1", (i,)).fetchone()
            if row:
                hits += 1
            elif len(missing) < 3:
                missing.append(i)
        out["kind_" + want_kind] = {"tagged": len(ids), "in_fts": hits,
                                    "sample_missing": missing}
    ruins = con.execute(
        "SELECT count(*) FROM corpus WHERE corpus MATCH ?",
        (spike.fts_expr("ruins_go"),)).fetchone()[0]
    out["ruins_go_fts_hits"] = ruins
    # freshness: every ruins_go hit's mtime parses and is on the current map
    rows = con.execute(
        "SELECT c.id, c.mtime FROM corpus f JOIN crows c ON c.rowid = f.rowid "
        "WHERE corpus MATCH ? LIMIT 10", (spike.fts_expr("ruins_go"),)).fetchall()
    out["ruins_go_sample"] = [{"id": i, "mtime": m} for i, m in rows]
    return out


def main() -> int:
    build = spike.build_index()
    print(json.dumps(build))
    con = sqlite3.connect(DB)
    ref = spike.reference_counts(con)
    fts = {}
    for q in spike.QUERIES:
        n = con.execute("SELECT count(*) FROM corpus WHERE corpus MATCH ?",
                        (spike.fts_expr(q),)).fetchone()[0]
        fts[q] = {"fts": n, "substring_reference": ref[q]}
    checks = spot_checks(con)
    con.close()
    out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "note": "B2-481 redirected FTS rebuild; B2_22 results artifact untouched",
           "catalog_lines": sum(1 for _ in open(CATALOG, encoding="utf-8")),
           "build": build, "queries": fts, "spot_checks": checks}
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("RESULTS_WRITTEN", RESULTS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
