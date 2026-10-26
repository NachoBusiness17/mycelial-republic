"""B2-78 read-only census of the B2-73 secret-scan scope.

Mirrors B2_73_secret_scan.py iter_files + is_binary + 10MB cap exactly,
touches nothing, writes nothing except this lane's JSON print. The B2-73 run
printed its census to stdout and persisted only the findings array (empty),
so the scanned-files denominator is re-derived here from bytes.
"""
from __future__ import annotations
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCOPES = [os.path.join(ROOT, "corpus"), os.path.join(ROOT, "watch", "inbox")]
SKIP_DIR_PARTS = {".git", "node_modules", "__pycache__", ".venv"}
MAX_FILE_BYTES = 10 * 1024 * 1024
SNIFF_BYTES = 8192


def is_binary(chunk: bytes) -> bool:
    if b"\x00" in chunk or not chunk:
        return True
    textish = sum(1 for b in chunk if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return textish / len(chunk) < 0.85


def main():
    census = {"files_seen": 0, "scanned": 0, "binary_skipped": 0, "large_skipped": 0}
    per_scope = {}
    for scope in SCOPES:
        seen = scanned = 0
        for dirpath, dirnames, filenames in os.walk(scope):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_PARTS]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                seen += 1
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if st.st_size > MAX_FILE_BYTES:
                    census["large_skipped"] += 1
                    continue
                try:
                    with open(p, "rb") as fh:
                        chunk = fh.read(SNIFF_BYTES)
                except OSError:
                    continue
                if is_binary(chunk):
                    census["binary_skipped"] += 1
                    continue
                scanned += 1
        per_scope[os.path.basename(scope)] = {"files_seen": seen, "scanned": scanned}
        census["files_seen"] += seen
        census["scanned"] += scanned
    out = {"probe": "B2_78_scanscope_census.py", "mirror_of": "B2_73_secret_scan.py iter_files/is_binary",
           "scopes": [os.path.relpath(s, ROOT).replace(os.sep, "/") for s in SCOPES],
           "census": census, "per_scope": per_scope,
           "findings_in_B2_73_results_json": 0}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
