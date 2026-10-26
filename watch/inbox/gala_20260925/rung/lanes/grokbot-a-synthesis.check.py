#!/usr/bin/env python
"""grokbot-a-synthesis head check.

Polls all sibling lane JSONs in this directory, validates the typed GalaLaneOut
shape, byte-verifies every row quote against its cited source file (fixed-string
substring on raw bytes, whitespace-normalized), and prints the synthesis digest.

Exit 0 = all 7 sibling lanes present, valid, and every quote byte-verified.
Exit 1 = a lane missing / invalid / a quote fails byte verification.
Exit 2 = fewer than 7 sibling lanes present (still polling is pointless).
"""
import json
import re
import sys
from pathlib import Path

LANES_DIR = Path(__file__).resolve().parent
SELF = "grokbot-a-synthesis.json"
REQUIRED = 7
REQUIRED_FIELDS = ["lane", "division", "ok", "note", "rows", "checks", "decision_changed", "artifact"]
ROW_FIELDS = ["law", "claim", "quote", "source", "steal", "falsifier", "leverage"]


def norm(s: str) -> str:
    """Whitespace-normalize for byte comparison (quotes may wrap across lines)."""
    return re.sub(r"\s+", " ", s).strip()


def verify_quote(quote: str, source: str):
    """Return (ok, detail). Byte-check = raw bytes of the source file contain the quote."""
    # sibling lanes cite path:line or path:N-M; split the line suffix off
    m = re.match(r"^(.*?)(:\d+(?:-\d+)?)$", source)
    path_part = m.group(1) if m else source
    line_part = m.group(2) if m else ""
    p = Path(path_part)
    if not p.is_absolute():
        return False, f"source not absolute: {source}"
    if not p.exists():
        return False, f"source missing: {source}"
    raw = p.read_bytes()
    try:
        text = raw.decode("utf-8", errors="replace")
    except Exception as e:  # pragma: no cover
        return False, f"source undecodable: {e}"
    hay = norm(text)
    needle = norm(quote)
    if needle in hay:
        return True, f"exact substring (whitespace-normalized){', cite' + line_part if line_part else ''}"
    # fallback: dash/apostrophe normalization, disclosed like the 48h-synthesis precedent
    def soft(x):
        x = norm(x)
        for a, b in (("\u2014", "-"), ("\u2013", "-"), ("\u2018", "'"), ("\u2019", "'"),
                     ("\u201c", '"'), ("\u201d", '"'), ("\u00a0", " ")):
            x = x.replace(a, b)
        return x
    if soft(needle) in soft(hay):
        return True, "substring after dash/apostrophe normalization (disclosed)"
    return False, "quote NOT found in source bytes"


def main():
    lane_files = sorted(
        p for p in LANES_DIR.glob("grokbot-*.json")
        if p.name != SELF and not p.name.endswith(".checks.json")
    )
    print(f"sibling lane jsons found: {len(lane_files)} (required {REQUIRED})")
    for p in lane_files:
        print(f"  - {p.name}")
    if len(lane_files) < REQUIRED:
        print(f"EXIT 2: only {len(lane_files)}/{REQUIRED} sibling lanes present")
        return 2

    all_ok = True
    total_rows = 0
    byte_fail = 0
    for p in lane_files:
        print(f"\n=== {p.name} ===")
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  INVALID JSON: {e}")
            all_ok = False
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in doc]
        if missing:
            print(f"  MISSING FIELDS: {missing}")
            all_ok = False
            continue
        print(f"  lane={doc['lane']} division={doc['division']} ok={doc['ok']}")
        print(f"  rows={len(doc['rows'])} checks={len(doc['checks'])}")
        total_rows += len(doc["rows"])
        for i, row in enumerate(doc["rows"], 1):
            rmiss = [f for f in ROW_FIELDS if f not in row]
            if rmiss:
                print(f"  row {i} MISSING ROW FIELDS: {rmiss}")
                all_ok = False
                continue
            words = len(row["quote"].split())
            if words > 40:
                print(f"  row {i} QUOTE OVER 40 WORDS ({words})")
                all_ok = False
            if "\u2014" in json.dumps(row, ensure_ascii=False):
                print(f"  row {i} CONTAINS EM-DASH (law violation)")
                all_ok = False
            ok, detail = verify_quote(row["quote"], row["source"])
            if ok:
                print(f"  row {i} [{row['law'][:48]}] quote OK ({words}w, {detail})")
            else:
                print(f"  row {i} [{row['law'][:48]}] quote FAIL: {detail}")
                byte_fail += 1
                all_ok = False
        if not doc["ok"]:
            print(f"  lane self-reports ok=false: {doc.get('note', '')[:120]}")

    print(f"\ntotal sibling rows: {total_rows}; quote byte-fails: {byte_fail}")
    if not all_ok:
        print("EXIT 1: validation or byte-verification failures above")
        return 1
    print("EXIT 0: all sibling lanes valid, every quote byte-verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
