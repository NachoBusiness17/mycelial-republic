"""B2-26: field-only backfill of canonical_sha256 over PENDING-URL rows in
watch/inbox/LINKS.jsonl, per the 2026-09-26 amendment in mag/link_library.py.

Laws honored:
  - only the canonical_sha256 value changes on touched lines; every other byte
    is preserved verbatim (surgical regex replace, no re-serialization).
  - shas come from mag.link_library.canonical_sha256(canonical) only.
  - aborts without writing if the file changed between snapshot and writeback.
  - never touches row 256's file-bytes sha (image-drop schema, verified
    separately) or any row whose sha is already a real hex digest.

Run: .venv\\Scripts\\python.exe watch\\inbox\\burn_wave_20260926\\B2_26_sha_backfill.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from mag.link_library import canonical_sha256, canonicalize  # noqa: E402

LEDGER = ROOT / "watch" / "inbox" / "LINKS.jsonl"
MANIFEST = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_26_sha_backfill_rows.json"
MARKER = re.compile(r'"canonical_sha256"\s*:\s*"PENDING-URL"')

raw = LEDGER.read_bytes().decode("utf-8")
snapshot = raw
lines = raw.split("\n")

fixed: list[dict] = []
errors: list[str] = []
drift_rows: list[dict] = []
for idx, line in enumerate(lines):
    if "PENDING-URL" not in line:
        continue
    lineno = idx + 1
    row = json.loads(line)
    canon = row["canonical"]
    sha = canonical_sha256(canon)
    # drift note: canonical field vs canonicalize(url) (x-post source rows are
    # a known convention: url = where found, canonical = the resource)
    try:
        recomputed = canonicalize(row["url"])
        if recomputed != canon:
            drift_rows.append({"line": lineno, "canonical": canon, "canonicalize_url": recomputed})
    except Exception as exc:  # noqa: BLE001
        drift_rows.append({"line": lineno, "canonical": canon, "error": str(exc)})
    new_line, n = MARKER.subn(f'"canonical_sha256": "{sha}"', line)
    if n != 1:
        errors.append(f"line {lineno}: marker matched {n} times")
        continue
    old_row = json.loads(line)
    new_row = json.loads(new_line)
    old_row.pop("canonical_sha256")
    new_row.pop("canonical_sha256")
    if old_row != new_row:
        errors.append(f"line {lineno}: non-sha bytes would change")
        continue
    lines[idx] = new_line
    fixed.append({
        "line": lineno,
        "seq": row["seq"],
        "ts": row["ts"],
        "writer": row.get("writer", ""),
        "canonical": canon,
        "canonical_sha256": sha,
    })

# true hash-collision check: a sha shared by two DIFFERENT canonicals
by_sha: dict[str, set[str]] = {}
for entry in fixed:
    by_sha.setdefault(entry["canonical_sha256"], set()).add(entry["canonical"])
true_collisions = {s: c for s, c in by_sha.items() if len(c) > 1}
if true_collisions:
    errors.append(f"true sha collisions across distinct canonicals: {true_collisions}")

if errors:
    print("ABORT, no write:", *errors, sep="\n")
    raise SystemExit(1)

out = "\n".join(lines)
if LEDGER.read_bytes().decode("utf-8") != snapshot:
    print("ABORT, no write: LINKS.jsonl changed underneath this run")
    raise SystemExit(1)
LEDGER.write_bytes(out.encode("utf-8"))

MANIFEST.write_text(json.dumps({
    "lane": "B2-26",
    "date": "2026-09-26",
    "fixed_count": len(fixed),
    "rows": fixed,
    "drift_rows_canonical_vs_canonicalize_url": drift_rows,
}, indent=1), encoding="utf-8")
print(f"fixed {len(fixed)} rows; drift rows noted: {len(drift_rows)}; manifest: {MANIFEST.name}")
