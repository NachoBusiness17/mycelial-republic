#!/usr/bin/env python3
"""B2-245 falsifier probe: parser order-fragility of census_drift_patrol.parse_carrier.

Runs parse_carrier against the REAL AGENTS.md **Tests:** line bytes, then against
a reorder mutation built only from slices of that real line (the brief's
falsifier: put the tripwire prose "31 files grown" and its "2026-09-26" lane
date, plus the retired "2026-09-14" fragment, ahead of the live claim).

Before the B2-245 fix this must print POISONED parses (files=31, date=2026-09-14);
after the fix it must print the claim parses (files=301, date=2026-09-26).

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_245_parser_order_probe.py
No repo writes, no network.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import tools.census_drift_patrol as cdp


def carrier_line(text: str) -> str:
    match = cdp.CARRIER_LINE_RE.search(text)
    assert match is not None, "no **Tests:** bullet in AGENTS.md"
    end = text.find("\n", match.start())
    return text[match.start(): end if end != -1 else len(text)]


def main() -> int:
    raw = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    line = carrier_line(raw)

    live = cdp.parse_carrier(line)
    print("LIVE LINE PARSE:")
    print(f"  date={live['date']} collected={live['collected']} files={live['files']}")

    # Reorder mutation from real byte slices only: the tripwire sentence that
    # currently trails the bullet is moved ahead of the count claim.
    trip_start = line.find("Census-carrier tripwire")
    assert trip_start != -1, "tripwire sentence not found in live carrier line"
    trip_end = line.find("operator call.", trip_start)
    assert trip_end != -1, "tripwire sentence end not found"
    tripwire = line[trip_start: trip_end + len("operator call.")]
    head = line[:trip_start].rstrip()

    # The retired-date fragment lives inside the tripwire sentence already
    # ("the retired 1,341 headline rode 12 days stale with 31 files grown").
    poisoned = (
        "- **Tests:** " + tripwire + " " + head[len("- **Tests:** "):]
    )
    poisoned_parse = cdp.parse_carrier(poisoned)
    print("REORDERED LINE PARSE (tripwire prose moved ahead of the claim):")
    print(f"  date={poisoned_parse['date']} collected={poisoned_parse['collected']} "
          f"files={poisoned_parse['files']}")

    # Order-immunity invariant: the reordered line must yield the SAME claim
    # (date, collected, files) as the live line, independent of what the
    # current census values are. The pre-fix probe read files=31 vs the live
    # claim (301 at probe time).
    same_claim = (
        poisoned_parse["date"] == live["date"]
        and poisoned_parse["collected"] == live["collected"]
        and poisoned_parse["files"] == live["files"]
    )
    print(f"VERDICT: {'IMMUNE' if same_claim else 'POISONED'} "
          f"(reordered claim {'==' if same_claim else '!='} live claim)")
    return 0 if same_claim else 1


if __name__ == "__main__":
    sys.exit(main())
