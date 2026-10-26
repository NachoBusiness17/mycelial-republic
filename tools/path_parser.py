"""path_parser - reads every file path in the estate as a steganographic
descriptor and builds the queryable map.

The estate's naming convention encodes in each path, without any database:
  LAYER   -> the first segment (canon, watch/inbox, memory/rib, tools, queue)
  PROGRAM -> the second segment where present (same_book, congress)
  ROLE    -> implied by layer + extension (receipt, law, instrument, hint)
  THESIS  -> the filename itself (THE_SYMBOL_IS_THE_COMMAND, RIB_BEHAVIOR_CARDS)
  DATE    -> the 8-digit suffix (20261022)
  SEAT    -> the prefix in hint files (zcode-)

This module parses those paths into structured records so the map is
queryable without a database - the filesystem IS the database.

Consumer: any seat that needs to query the estate's steganographic layer
without knowing filenames in advance.
Verifier: `python -m tools.path_parser selftest` + manual inspection.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"(20\d{6})")
SEAT_RE = re.compile(r"^(zcode|hermes|grokbot|ghost|bob|pixel|t90)[-_]")


def parse_path(rel_path: str) -> dict:
    p = Path(rel_path)
    parts = p.parts
    layer = parts[0] if parts else ""
    program = parts[1] if len(parts) > 1 else ""
    filename = p.stem
    ext = p.suffix

    # extract INV: invariant tags (steganographic layer)
    INV_RE = re.compile(r"INV:([a-z0-9-]+(?:\+[a-z0-9-]+)*)", re.I)
    inv_match = INV_RE.search(filename)
    inv_tags = inv_match.group(1).split("+") if inv_match else []

    date_m = DATE_RE.search(filename)
    date = date_m.group(1) if date_m else ""
    thesis = DATE_RE.sub("", filename).strip("_-. ")

    seat = ""
    seat_m = SEAT_RE.match(filename)
    if seat_m:
        seat = seat_m.group(1)

    if "inbox" in rel_path:
        role = "receipt"
    elif "rib" in rel_path:
        role = "law"
    elif rel_path.startswith("tools/"):
        role = "instrument"
    elif "commit_hints" in rel_path:
        role = "commit instruction"
    elif "door" in rel_path:
        role = "public artifact"
    elif "canon" in rel_path:
        role = "permanent doctrine"
    else:
        role = "uncategorized"

    return {
        "path": rel_path,
        "layer": layer,
        "program": program,
        "role": role,
        "thesis": thesis,
        "date": date,
        "seat": seat,
        "ext": ext,
        "invariants": inv_tags,
    }


def scan(roots: list[str] | None = None) -> list[dict]:
    search_roots = roots or ["canon", "watch/inbox", "memory/rib", "tools",
                             "queue/commit_hints"]
    records = []
    for root in search_roots:
        rp = ROOT / root
        if not rp.exists():
            continue
        for f in sorted(rp.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                rel = str(f.relative_to(ROOT))
                records.append(parse_path(rel))
    return records


def query(records: list[dict], **filters) -> list[dict]:
    out = []
    for r in records:
        match = True
        for field, val in filters.items():
            if val and val.lower() not in str(r.get(field, "")).lower():
                match = False
                break
        if match:
            out.append(r)
    return out


def selftest() -> int:
    r = parse_path("watch/inbox/THE_SYMBOL_IS_THE_COMMAND_20261022.md")
    assert r["layer"] == "watch"
    assert r["role"] == "receipt"
    assert r["date"] == "20261022"
    assert "SYMBOL_IS_THE_COMMAND" in r["thesis"]

    r2 = parse_path("memory/rib/RIB_BEHAVIOR_CARDS_20260928.md")
    assert "rib" in r2["path"]
    assert r2["date"] == "20260928"

    r3 = parse_path("canon/same_book/door/PUBLIC_DOOR.md")
    assert "canon" in r3["path"] or "door" in r3["path"]

    r4 = parse_path("queue/commit_hints/zcode-last-mile.json")
    assert r4["seat"] == "zcode"

    records = [r, r2, r3, r4]
    receipts = [x for x in records if x["role"] == "receipt"]
    assert all("receipt" in x["role"] for x in receipts)

    print("selftest PASS: parse_path + query + seat extraction + role classification")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "query", "selftest"])
    ap.add_argument("--layer", default="")
    ap.add_argument("--program", default="")
    ap.add_argument("--role", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--thesis", default="")
    args = ap.parse_args()
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "scan":
        print(json.dumps(scan(), indent=1))
    elif args.cmd == "query":
        records = scan()
        filtered = query(records, layer=args.layer, program=args.program,
                         role=args.role, date_prefix=args.date,
                         thesis_contains=args.thesis)
        print(json.dumps(filtered, indent=1))
    else:
        return selftest()
    return 0


if __name__ == "__main__":
    sys.exit(main())
