#!/usr/bin/env python3
"""B2-11 mimosa L3 close: register verified-dead watch/inbox ssrf/path findings
as accepted debt in configs/violation_baseline.json, BY NAME, with date+reason.

Scope: exactly the 30 occurrences (25 (file, class) claims) the sealed Mimosa
scans report under watch/inbox/ with publicClass ssrf or path-traversal.
Every covered file was verified 2026-09-26: one-shot script, no __init__.py in
its directory, zero code references repo-wide (git grep -w stem: only catalog
inventories and prose receipts), nothing in mag/ tools/ scripts/ configs/
main.py imports or executes it. Live-code findings (tools/ 9, models/ 5) are
NOT baselined here.

Fingerprints reuse tools/violation_ratchet.py's fingerprint(rule, file, detail)
scheme with namespaced rules (mimosa-ssrf / mimosa-path-traversal) so they can
never collide with scanner-emitted claims. Caveat, recorded on every entry:
violation_ratchet.py prune reaps claims it cannot re-derive, and its scanner
never scans watch/inbox, so a future prune will reap these by design. If reaped,
re-accept from this receipt; do not widen the scanner roots to swallow watch/.
"""
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = Path(r"C:\Users\foste\.mimosa\security-scans"
                r"\project-8af8c49a6c1b0282e16b1e73"
                r"\scan-2026-09-26T04-10-04.918Z-41fc75fa84c4\findings.json")
BASELINE = ROOT / "configs" / "violation_baseline.json"
SCAN_ID = "scan-2026-09-26T04-10-04.918Z-41fc75fa84c4"
BY = "agent:B2-11 flash-lane burn 2026-09-26 (mimosa L3 close)"
TODAY = "2026-09-26"

RULE_NAME = {"ssrf": "mimosa-ssrf", "path-traversal": "mimosa-path-traversal"}
NOTE = ("archived 09-16 one-shot scripts in watch/inbox (moonshot_20260916, "
        "wave_20260916) plus sibling one-shots (physical_computing/receipts, "
        "four_condition_battery); verified dead code 2026-09-26: no __init__.py, "
        "zero repo code refs, nothing in mag/tools/scripts/configs/main.py "
        "imports or runs them; urlopen targets are hardcoded provider endpoints, "
        "open() targets are script-local constants; mimosa-sourced claim, scanner "
        "never re-derives it, prune will reap by design, re-accept from "
        "watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md")


def fingerprint(rule: str, file: str, detail: str) -> str:
    return hashlib.sha256(f"{rule}\0{file}\0{detail}".encode("utf-8")).hexdigest()[:16]


def main() -> int:
    data = json.loads(FINDINGS.read_text(encoding="utf-8"))
    sel = [f for f in data["findings"]
           if f.get("identity", {}).get("publicClass") in RULE_NAME
           and f.get("location", {}).get("path", "").startswith("watch/inbox/")]
    grouped = defaultdict(list)
    for f in sel:
        grouped[(f["location"]["path"], f["identity"]["publicClass"])].append(f)

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    accepted = baseline.setdefault("accepted", {})
    added, skipped = 0, 0
    for (path, cls), occ in sorted(grouped.items()):
        occ_ids = ",".join(sorted({o["findingId"].split(":", 1)[1][:12] for o in occ}))
        detail = (f"{len(occ)} occurrence(s) at lines "
                  f"{','.join(str(o['location']['line']) for o in sorted(occ, key=lambda o: o['location']['line']))};"
                  f" findingIds {occ_ids}; {SCAN_ID}")
        rule = RULE_NAME[cls]
        fp = fingerprint(rule, path, detail)
        if fp in accepted:
            skipped += 1
            continue
        accepted[fp] = {"rule": rule, "file": path, "detail": detail,
                        "accepted": TODAY, "by": BY, "note": NOTE}
        added += 1
    baseline["updated"] = datetime.now().isoformat(timespec="seconds")
    BASELINE.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"B2-11 baseline-update: occurrences={len(sel)}; claims={len(grouped)}; "
          f"ADDED={added}; already-registered={skipped}; register now "
          f"{len(accepted)} -> {BASELINE.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
