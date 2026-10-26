"""B2-167 queue-number double-claim census over QUEUE.md (read-only, 2026-09-26).

Verifies the final post-janitor census: every row-start id (strict and tolerant
forms) counted, ids claimed by more than one brief reported, B2-92/B2-93 (the
brief's own pair) verified single-claimed, CLAIM/CLAIMED lines censused with the
law's ghost check (an active CLAIM whose lane already has a receipt on disk),
highest row id, malformed row-start forms the strict regex misses. Emits JSON to
stdout and to B2_167_census_results.json next to this script. Never writes to
QUEUE.md.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD = HERE / "QUEUE.md"
OUT = HERE / "B2_167_census_results.json"

STRICT_ROW = re.compile(r"^- \[([ x])\] B2-(\d+) ", re.M)
TOLERANT_ROW = re.compile(r"^-[ \t]+\[[ x]\] B2-(\d+)\b", re.M)
CLAIM_RE = re.compile(r"^- CLAIM B2-([\d.]+)", re.M)
CLAIMED_RE = re.compile(r"^- CLAIMED B2-([\d.]+)", re.M)
B2_NUM = re.compile(r"B2-(\d+)")


def main() -> int:
    raw = BOARD.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    strict = [(int(m.group(2)), m.start()) for m in STRICT_ROW.finditer(text)]
    tolerant = [(int(m.group(1)), m.start()) for m in TOLERANT_ROW.finditer(text)]

    strict_ids = Counter(i for i, _ in strict)
    tolerant_ids = Counter(i for i, _ in tolerant)

    # a tolerant hit whose span does not match the strict form is malformed
    malformed = []
    for lineno, line in enumerate(lines, 1):
        if TOLERANT_ROW.match(line) and not STRICT_ROW.match(line):
            malformed.append({"line": lineno, "prefix": line[:40]})

    # ids claimed by more than one brief (tolerant superset of strict)
    dupes = sorted(i for i, c in tolerant_ids.items() if c > 1)
    strict_dupes = sorted(i for i, c in strict_ids.items() if c > 1)

    # section split
    dispensed_end = text.find("\n## Open")
    dispensed_ids = Counter(
        int(m.group(2)) for m in STRICT_ROW.finditer(text[:dispensed_end])
    )
    open_ids = tolerant_ids - dispensed_ids

    # B2-92 / B2-93, the brief's own pair
    pair = {}
    for want in (92, 93):
        rows = [
            {"line": n, "prefix": l[:120]}
            for n, l in enumerate(lines, 1)
            if re.match(r"^-[ \t]+\[[ x]\] B2-%d " % want, l)
        ]
        pair["B2-%d" % want] = rows

    # CLAIM census + ghost check (active CLAIM whose lane has a receipt on disk)
    active_claims = sorted(set(m.group(1) for m in CLAIM_RE.finditer(text)))
    retired_claims = sorted(set(m.group(1) for m in CLAIMED_RE.finditer(text)))
    ghosts = []
    for lane in active_claims:
        nums = [int(x) for x in B2_NUM.findall(lane)]
        for n in nums:
            pat = "B2_%s_*" % str(n).zfill(2)
            hits = sorted(HERE.glob(pat + ".md"))
            if hits:
                ghosts.append({"claim_lane": lane, "id": n, "receipts": [h.name for h in hits]})

    result = {
        "ts_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "board": "watch/inbox/burn_wave_20260926/QUEUE.md",
        "bytes": len(raw),
        "lines": len(lines),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "rows_strict": sum(strict_ids.values()),
        "rows_tolerant": sum(tolerant_ids.values()),
        "distinct_ids": len(tolerant_ids),
        "highest_row_id": max(tolerant_ids) if tolerant_ids else None,
        "checked_rows": sum(1 for m in STRICT_ROW.finditer(text) if m.group(1) == "x"),
        "unchecked_rows_strict": sum(1 for m in STRICT_ROW.finditer(text) if m.group(1) == " "),
        "dispensed_rows": sum(dispensed_ids.values()),
        "open_rows": sum(open_ids.values()),
        "dupes_tolerant": dupes,
        "dupes_strict": strict_dupes,
        "double_claimed_count": len(dupes),
        "b2_92_b2_93_rows": pair,
        "malformed_row_starts": malformed,
        "active_claim_lanes": active_claims,
        "retired_claim_lanes": retired_claims,
        "ghost_claims": ghosts,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
