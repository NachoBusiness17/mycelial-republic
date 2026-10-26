#!/usr/bin/env python3
"""B2-96 scripts/ mimosa ssrf/path triage: register verified one-shot/dormant
scripts/ ssrf/path findings as accepted debt in configs/violation_baseline.json,
BY NAME, with date+reason, per the B2-11 pattern.

Scope: exactly the 26 occurrences (20 (file, class) claims) from sealed scan
scan-2026-09-26T04-10-04.918Z-41fc75fa84c4 whose path is scripts/ AND whose
file is on the ACCEPT list below. Every accepted file was classified
2026-09-26: one-shot probe/fetcher or manual/dormant tool, NO Windows
scheduler entry (schtasks /query /fo csv: 332 tasks, zero stems), zero rows in
configs/lanes.yaml, nothing in mag/ tools/ configs/ main.py imports or
subprocess-runs it. Exceptions named on the entries: ack_reaper.py and
k17_pilot.py are executed by their own test modules only
(tests/ack_reaper_test.py, tests/test_k17_holds.py), handoff_escalation_watcher
is a manual-launch watcher with no driver, vision_bench is a manual receipt
bench documented on dashboard-deploy/static/operator_board.html.

The live runner-driven set is NOT baselined here and files as must-fix:
scripts/wave_driver.py (7, tick-loop driver exercised by tests/test_wave_driver.py
plus tests/wave_driver_test.py, imports m12_pairing), scripts/m12_pairing.py (4,
imported by scripts/wave_driver.py:84), scripts/desk_baseline_probe.py (4,
configs/coding_session_loop.yaml:23 gate cmd plus mag/coding_session_loop.py:241
live import plus mag/governor_autorun.py:374), scripts/hunger_ledger.py (2,
mag/lane_runner.py:545 canonical fallback).

Fingerprints reuse tools/violation_ratchet.py's fingerprint(rule, file, detail)
scheme with namespaced rules (mimosa-ssrf / mimosa-path-traversal) so they can
never collide with scanner-emitted claims. Per B2-95 (2026-09-26) external debt
leaves the register only by explicit re-triage, never a silent reap.
"""
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = Path(r"C:\Users\foste\.mimosa\security-scans"
                r"\project-8af8c49a6c1b0282e16b1e73"
                r"\scan-2026-09-26T04-10-04.918Z-41fc75fa84c4\findings.json")
BASELINE = ROOT / "configs" / "violation_baseline.json"
SCAN_ID = "scan-2026-09-26T04-10-04.918Z-41fc75fa84c4"
BY = "agent:B2-96 flash-lane burn 2026-09-26 (scripts/ ssrf/path triage)"
TODAY = "2026-09-26"

RULE_NAME = {"ssrf": "mimosa-ssrf", "path-traversal": "mimosa-path-traversal"}

# (file, note) for every file this lane verified one-shot/dormant. The note
# carries the acceptance evidence so the claim stands alone.
ACCEPT = {
    "scripts/fetch_training_pdfs.py":
        "one-shot fixed-URL PDF fetcher (mtime 2026-09-16), repo refs are catalog/"
        "index inventories and a docstring mention only, no driver",
    "scripts/fetch_founding_law.py":
        "one-shot founder-law fetcher paired with scripts/finalize_founding_law.py "
        "(docstring: no network, pairs with), no driver",
    "scripts/ack_reaper.py":
        "one-shot re-ack tool, no scheduler or mag/config driver, executed only by "
        "its own self-test module tests/ack_reaper_test.py",
    "scripts/the50_t08_spectro.py":
        "THE50 T08 one-shot probe (mtime 2026-09-19), refs are ESTATE_INDEX/steps "
        "inventories only, no driver",
    "scripts/the50_t23_reaction_sigs.py":
        "THE50 T23 one-shot probe, refs are inventories only, no driver",
    "scripts/the50_t24_symbol_correlation.py":
        "THE50 T24 one-shot probe, refs are inventories only, no driver",
    "scripts/the50_w6_t28_miss_entropy.py":
        "THE50 W6 T28 one-shot probe (mtime 2026-09-25, no main guard, top-level "
        "one-shot), refs are inventories only, no driver",
    "scripts/the50_w7_t32_gstd_probe2.py":
        "THE50 W7 T32 one-shot probe, refs are inventories only, no driver",
    "scripts/tg_harvest.py":
        "one-shot telegram harvest (mtime 2026-09-05), inventory refs only, no driver",
    "scripts/vision_endowment.py":
        "one-shot vision endowment (mtime 2026-09-04), dashboard estate_walk data "
        "blob mentions are data not calls, no driver",
    "scripts/chain_index_completion.py":
        "one-shot chain index completion (mtime 2026-09-04), inventory refs only, "
        "no driver",
    "scripts/council_runner.py":
        "manual council runner (mtime 2026-08-27), zero repo code refs, no driver",
    "scripts/roadmap_gap_probe.py":
        "one-shot roadmap probe (mtime 2026-08-06), inventory refs only, no driver",
    "scripts/steering_suite.py":
        "manual steering suite (mtime 2026-08-27), zero repo code refs, no driver",
    "scripts/vision_bench.py":
        "manual vision receipt bench, operator_board.html documents manual run "
        "python scripts/vision_bench.py, not scheduled",
    "scripts/handoff_escalation_watcher.py":
        "manual-launch handoff watcher (mtime 2026-08-07, --once/--loop modes in "
        "docstring), zero scheduler or mag/config drivers today (dormant)",
    "scripts/k17_pilot.py":
        "K.17 hold-state pilot CLI, executed only by tests/test_k17_holds.py (5 "
        "tests, subprocess real CLI), no production driver",
}

NOTE_TAIL = ("mimosa-sourced claim, scanner never scans scripts/ (ratchet roots "
             "mag+tools, tools/violation_ratchet.py DEFAULT_ROOTS), external debt "
             "leaves the register only by explicit re-triage per B2-95, re-accept "
             "from watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md")


def fingerprint(rule: str, file: str, detail: str) -> str:
    return hashlib.sha256(f"{rule}\0{file}\0{detail}".encode("utf-8")).hexdigest()[:16]


def main() -> int:
    data = json.loads(FINDINGS.read_text(encoding="utf-8"))
    sel = [f for f in data["findings"]
           if f.get("identity", {}).get("publicClass") in RULE_NAME
           and f.get("location", {}).get("path") in ACCEPT]
    grouped = defaultdict(list)
    for f in sel:
        grouped[(f["location"]["path"], f["identity"]["publicClass"])].append(f)

    all_scripts = [f for f in data["findings"]
                   if f.get("identity", {}).get("publicClass") in RULE_NAME
                   and str(f.get("location", {}).get("path", "")).replace("\\", "/")
                   .startswith("scripts/")]
    print(f"scripts/ ssrf/path occurrences in scan: {len(all_scripts)}; "
          f"accepted subset: {len(sel)}; live must-fix left unregistered: "
          f"{len(all_scripts) - len(sel)}")
    assert len(all_scripts) == 43, f"expected 43, got {len(all_scripts)}"
    assert len(sel) == 26, f"expected 26 accepted, got {len(sel)}"
    assert len(grouped) == 20, f"expected 20 file-class claims, got {len(grouped)}"

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
                        "accepted": TODAY, "by": BY,
                        "note": f"{ACCEPT[path]}; {NOTE_TAIL}"}
        added += 1
    baseline["updated"] = datetime.now().isoformat(timespec="seconds")
    BASELINE.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"B2-96 baseline-update: occurrences={len(sel)}; claims={len(grouped)}; "
          f"ADDED={added}; already-registered={skipped}; register now "
          f"{len(accepted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
