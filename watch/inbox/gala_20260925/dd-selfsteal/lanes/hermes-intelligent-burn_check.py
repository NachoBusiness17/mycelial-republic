#!/usr/bin/env python
"""hermes-intelligent-burn lane finish-line check.

Verifies, from bytes on disk:
[1] the prime verdict receipt exists, is over the substance floor, and carries
    the SPEND-law usage header
[2] both stage ledger rows banked ok (stage A reasoning-dump + stage B content)
[3] no em-dash / en-dash anywhere in the verdict (the no-fabrication family law)
[4] the five contract sections present with exact headers
[5] verdict code-citations spot-verified against source bytes
[6] the one known citation defect (intel doc date digits) reported as the
    banked erratum, not silently edited
[7] sibling receipts the dispatch consumed exist non-empty
Exit 0 = all pass / 1 = any failure.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
VERDICT = ROOT / "watch/inbox/dd_dogfood/hermes-verdict.md"
DUMP = ROOT / "watch/inbox/dd_dogfood/hermes-verdict.reasoning-dump.md"
USAGE = ROOT / "memory/runs/hermes_burn/usage.jsonl"
LANE_JSON = ROOT / "watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-intelligent-burn.json"

SIBLINGS = [
    "watch/inbox/dd_dogfood/mountain-bridge.md",
    "watch/inbox/dd_dogfood/selfsteal-builds.md",
    "watch/inbox/dd_dogfood/games-audit.md",
    "watch/inbox/dd_dogfood/hermes-patterns.md",
    "watch/inbox/dd_dogfood/selfsteal-laws.md",
    "watch/inbox/dd_dogfood/corpus-holdings.md",
    "watch/inbox/gala_20260925/dd-selfsteal/lanes/dd-actualplay-intel.json",
]

SECTIONS = [
    "1. THE BURN LEDGER VERDICT (economics)",
    "2. THE PLAY CARRIER VERDICT (D&D corpus + live-fire)",
    "3. THE BUILD VERDICT (24h self-steal + games audit)",
    "4. THE NEXT-24H CARD",
    "5. WHAT WOULD CHANGE YOUR MIND",
]

# (name, file, expected substring in the cited lines)
CODE_CITES = [
    ("tavern.py:73-76 heat law", "tools/tavern.py",
     "self.heat = 18 - 2 * self.pressure"),
    ("tavern.py:157 run-stamp emit", "tools/tavern.py",
     'f"TAVERN_r{rnd}_{p[\'name\']}"'),
    ("tavern.py docstring line 10 id shape", "tools/tavern.py",
     "id TAVERN_<run>_r<round>_<actor>"),
    ("dungeon.py:102-107 strip_and_cap", "tools/dungeon.py",
     'replace("\\u2014", "-")'),
    ("STANDING_RAILS:10-12 default-to-rails", "queue/STANDING_RAILS.md",
     "A bespoke model-call path requires a written reason"),
    ("STANDING_RAILS:13-16 hollow-batch", "queue/STANDING_RAILS.md",
     "outputs without their material are VOID"),
    ("STANDING_RAILS:46-50 migrate debt", "queue/STANDING_RAILS.md",
     "each migrates to\n  route_chat or documents its reason"),
]


def main() -> int:
    failures = 0
    print("=" * 70)
    print("HERMES-INTELLIGENT-BURN LANE CHECK ",
          end="")
    print(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("=" * 70)

    print("\n[1] VERDICT RECEIPT (existence, size, SPEND-law header)")
    if not VERDICT.is_file():
        print("  FAIL verdict missing:", VERDICT)
        return 1
    text = VERDICT.read_text(encoding="utf-8", errors="replace")
    if len(text) < 2000:
        print(f"  FAIL verdict only {len(text)} chars (substance floor 2000)")
        failures += 1
    else:
        print(f"  PASS verdict {len(text)} chars (floor 2000)")
    if '"prompt_tokens"' in text and '"cost"' in text:
        print("  PASS usage header present (SPEND law)")
    else:
        print("  FAIL usage header missing")
        failures += 1
    if "finish_reason=stop" in text:
        print("  PASS finish_reason=stop footer present")
    else:
        print("  FAIL finish footer missing")
        failures += 1

    print("\n[2] LEDGER ROWS (stage A + stage B)")
    ids = {"GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003": False,
           "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B": False}
    if USAGE.is_file():
        for line in USAGE.read_text(encoding="utf-8").splitlines():
            for ask_id in ids:
                if ask_id + '"' in line and '"ok": true' in line:
                    row = json.loads(line)
                    if not ids[ask_id]:
                        ids[ask_id] = True
                        print(f"  PASS {ask_id}: cost={row.get('cost_usd')} "
                              f"finish={row.get('finish_reason')} "
                              f"channel={row.get('channel')}")
    for ask_id, hit in ids.items():
        if not hit:
            print(f"  FAIL no ok ledger row for {ask_id}")
            failures += 1

    print("\n[3] EM-DASH / EN-DASH SCAN (verdict content, after the --- body "
          "marker and headers)")
    body = text.split("\n---\n", 1)[-1]
    em = body.count("\u2014")
    en = body.count("\u2013")
    if em == 0 and en == 0:
        print("  PASS zero em-dashes, zero en-dashes in verdict body")
    else:
        print(f"  FAIL em={em} en={en}")
        failures += 1

    print("\n[4] CONTRACT SECTIONS (exact headers, in order)")
    pos = -1
    for sec in SECTIONS:
        found = text.find(sec)
        if found == -1:
            print(f"  FAIL section header not found: {sec}")
            failures += 1
        elif found < pos:
            print(f"  FAIL section out of order: {sec}")
            failures += 1
        else:
            pos = found
            print(f"  PASS {sec}")
    card_rows = len(re.findall(r"\*\*Row \d", text))
    if 1 <= card_rows <= 5:
        print(f"  PASS next-24h card rows <= 5 (found {card_rows})")
    else:
        print(f"  FAIL card rows {card_rows} outside 1..5")
        failures += 1

    print("\n[5] CODE-CITATION SPOT CHECKS (verdict claims vs source bytes)")
    for name, rel, needle in CODE_CITES:
        p = ROOT / rel
        if not p.is_file():
            print(f"  FAIL {name}: source missing {rel}")
            failures += 1
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        needle_in_src = needle.replace("\\n", "\n") if "\\n" in needle else needle
        if needle_in_src in src:
            print(f"  PASS {name}")
        else:
            print(f"  FAIL {name}: expected bytes not found in {rel}")
            failures += 1

    print("\n[6] KNOWN CITATION DEFECT + ERRATUM (20260903 vs 20261003)")
    if "DND_ACTUALPLAY_INTEL_20260903.md" in text:
        print("  INFO defect present in verdict body (model typo): "
              "DND_ACTUALPLAY_INTEL_20260903.md")
        if "ERRATUM (lane seat, not model output)" in text and \
                "DND_ACTUALPLAY_INTEL_20261003.md" in text:
            print("  PASS erratum banked in the receipt, correct filename "
                  "stated")
        else:
            print("  FAIL erratum missing")
            failures += 1
    else:
        print("  INFO no 20260903 defect present (nothing to erratum)")

    print("\n[7] SIBLING RECEIPTS CONSUMED (exist, non-empty)")
    for rel in SIBLINGS:
        p = ROOT / rel
        if p.is_file() and p.stat().st_size > 0:
            print(f"  PASS {rel} ({p.stat().st_size} bytes)")
        else:
            print(f"  FAIL {rel} missing or empty")
            failures += 1

    print("\n[8] STAGE A DUMP PRESERVED (PROPOSED provenance)")
    if DUMP.is_file() and DUMP.stat().st_size > 2000:
        dtext = DUMP.read_text(encoding="utf-8", errors="replace")
        if "PROPOSED" in dtext and "REASONING-CHANNEL DUMP" in dtext:
            print(f"  PASS dump preserved {DUMP.stat().st_size} bytes, "
                  "PROPOSED-marked")
        else:
            print("  FAIL dump lacks PROPOSED markers")
            failures += 1
    else:
        print("  FAIL stage A dump missing or tiny")
        failures += 1

    print("\n[9] LANE JSON PARSES")
    try:
        lane = json.loads(LANE_JSON.read_text(encoding="utf-8"))
        print(f"  PASS lane json parses; steps={len(lane.get('steps', []))}")
    except Exception as exc:
        print(f"  FAIL lane json: {exc}")
        failures += 1

    print("\n" + "=" * 70)
    print(f"VERDICT: {'PASS exit 0' if failures == 0 else f'FAIL exit 1 ({failures} failures)'}")
    print("=" * 70)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
