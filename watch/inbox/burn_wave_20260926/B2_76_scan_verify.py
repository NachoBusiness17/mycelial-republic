"""B2-76 estate verify: scan_tree over the real catalog root, read-only.

Proves the codified v3 junction policy reproduces the 2026-09-18 inline
walk's behavior on live bytes: the local_sovereign_agent/training junction
is recorded and pruned, nothing is emitted under its path, and the walk
row count lands in the 757K v3 band (not the 946K v2 band). No file in
catalog/ is written (scan_tree streams; only main() writes).
Run with .venv/Scripts/python.exe.
"""
import json
import os
import sys

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")

from mag.catalog_scan import ROOT, scan_tree

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "B2_76_scan_verify.json")


def main():
    stats = {}
    rows = 0
    under_junction = 0
    records = []
    for kind, payload in scan_tree(ROOT, stats, onerror=lambda e: None):
        if kind == "row":
            rows += 1
            p = payload["path"].replace("\\", "/").lower()
            if p.startswith("local_sovereign_agent/training/"):
                under_junction += 1
        else:
            records.append(payload)

    doc = {
        "probe": "B2_76_scan_verify.py",
        "ts": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": ROOT,
        "python": sys.version.split()[0],
        "stats": stats,
        "rows_total": rows,
        "rows_under_training_junction_prefix": under_junction,
        "reparse_records": records,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(json.dumps(doc, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
