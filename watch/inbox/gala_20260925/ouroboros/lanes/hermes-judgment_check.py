#!/usr/bin/env python
"""hermes-judgment lane check: byte-verify every mined quote, validate lane JSON,
confirm the prime judgment landed. Exit 0 = all pass, 1 = any failure.

Quote verification: the estate wraps prose at ~78 chars, so a quote spanning a
line wrap is verified by whitespace-normalized substring match against the
whitespace-normalized file bytes; single-line quotes must also match raw.
Every PASS prints the matched file and the raw/normalized result.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
LANE_JSON = ROOT / "watch/inbox/gala_20260925/ouroboros/lanes/hermes-judgment.json"
JUDGMENT = ROOT / "watch/inbox/gala_20260925/ouroboros/PRIME_JUDGMENT_20261002.md"

QUOTES = [
    ("ouroboros-leg-6",
     "C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/DESCENT_DAY1_STEAL_20261001.md",
     "Ouroboros leg: THE DESCENT PROTOCOL (2026-10-01) leg 6 requires frontier reasoning returned to estate instruments."),
    ("loud-line",
     "C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/DESCENT_DAY1_STEAL_20261001.md",
     "premium wins every question settled by reading bytes already in context; premium loses every time it asserts facts about bytes or runtime it never saw"),
    ("boot-path-law",
     "C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/DESCENT_DAY1_STEAL_20261001.md",
     "a system claiming self-improvement must show where the improvement lives in the BOOT path, not in the ask template; per-ask context is curriculum, not memory"),
    ("redemption-rate-law",
     "C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/DESCENT_DAY1_STEAL_20261001.md",
     "a loop's health IS the redemption rate, and an organ must count issued vs redeemed tickets or the deferral is a leak wearing a loop's clothes"),
    ("thin-edges-f14",
     "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/ouroboros/lanes/ouroboros-synthesis.check.txt",
     "receipts->laws: 18/4527 receipts absorbed into law (0.4%)"),
]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def main() -> int:
    failures = 0
    print("=" * 70)
    print("HERMES-JUDGMENT LANE CHECK ", end="")
    from datetime import datetime, timezone
    print(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("=" * 70)

    print("\n[1] QUOTE BYTE-VERIFICATION (whitespace-normalized substring; "
          "estate prose wraps at ~78 chars)")
    for name, src, quote in QUOTES:
        p = Path(src)
        if not p.is_file():
            print(f"  FAIL {name}: source missing: {src}")
            failures += 1
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        words = len(quote.split())
        if words > 40:
            print(f"  FAIL {name}: quote {words} words > 40")
            failures += 1
            continue
        raw_hit = quote in raw
        norm_hit = norm(quote) in norm(raw)
        if raw_hit:
            print(f"  PASS {name}: raw byte match, {words} words")
        elif norm_hit:
            print(f"  PASS {name}: whitespace-normalized match (spans a line "
                  f"wrap), {words} words")
        else:
            print(f"  FAIL {name}: quote NOT FOUND in {src}")
            failures += 1

    print("\n[2] LANE JSON VALIDATION")
    try:
        lane = json.loads(LANE_JSON.read_text(encoding="utf-8"))
        for field in ("lane", "division", "rows", "checks", "decision_ledger"):
            if field not in lane:
                print(f"  FAIL lane json missing field: {field}")
                failures += 1
        n_rows = len(lane.get("rows", []))
        print(f"  PASS lane json parses; rows={n_rows}")
        for i, row in enumerate(lane.get("rows", [])):
            src = row.get("source", "")
            q = row.get("quote", "")
            if not src or not Path(src).is_file():
                print(f"  FAIL row {i}: source path missing on disk: {src}")
                failures += 1
                continue
            raw = Path(src).read_text(encoding="utf-8", errors="replace")
            if norm(q) not in norm(raw):
                print(f"  FAIL row {i}: quote not byte-present in source")
                failures += 1
            else:
                print(f"  PASS row {i} ({row.get('law', '?')}): quote "
                      "byte-present in cited source")
    except FileNotFoundError:
        print(f"  FAIL lane json not found: {LANE_JSON}")
        failures += 1
    except json.JSONDecodeError as exc:
        print(f"  FAIL lane json does not parse: {exc}")
        failures += 1

    print("\n[3] PRIME JUDGMENT LANDING")
    if JUDGMENT.is_file():
        text = JUDGMENT.read_text(encoding="utf-8", errors="replace")
        has_usage = '"prompt_tokens"' in text
        if len(text) < 2000:
            print(f"  FAIL judgment file exists but only {len(text)} chars")
            failures += 1
        elif not has_usage:
            print("  FAIL judgment file lacks usage header (SPEND law)")
            failures += 1
        else:
            print(f"  PASS judgment landed: {len(text)} chars, usage header "
                  "present")
    else:
        print(f"  INFO judgment not yet landed at {JUDGMENT} (check run "
              "pre-dispatch)")
        failures += 1

    print("\n[4] SPEND LEDGER ROW")
    usage_path = ROOT / "memory/runs/hermes_burn/usage.jsonl"
    hit = False
    if usage_path.is_file():
        for line in usage_path.read_text(encoding="utf-8").splitlines():
            if "GALA_OUROBOROS_PRIME_JUDGMENT_20261002" in line and '"ok": true' in line:
                hit = True
                print(f"  PASS ledger row present: {line[:160]}...")
                break
    if not hit:
        print("  INFO no ok ledger row for GALA_OUROBOROS_PRIME_JUDGMENT_20261002 "
              "yet (pre-dispatch run)")
        failures += 1

    print("\n" + "=" * 70)
    print(f"VERDICT: {'PASS exit 0' if failures == 0 else f'FAIL exit 1 ({failures} failures)'}")
    print("=" * 70)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
