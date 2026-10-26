"""Unit tests for the 2026-10-17 permanent invariant registry minted via Ractor.

Verifies:
1. All 7 permanent invariants (INVARIANT-20261017-01 through 07) are defined and documented.
2. Invariant documents contain strictly zero em-dashes.
3. Every invariant maps to a physical repo enforcement anchor.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX_RACTOR = ROOT / "watch" / "inbox" / "ractor"
EM_DASH = re.compile(r"[\u2010\u2011\u2012\u2013\u2014\u2015]")

EXPECTED_INVARIANTS = [
    ("INVARIANT-20261017-01", "Navi10 Offload Envelope"),
    ("INVARIANT-20261017-02", "Longitudinal Memory Law"),
    ("INVARIANT-20261017-03", "Paced Width Envelope"),
    ("INVARIANT-20261017-04", "Single-Writer Lease Law"),
    ("INVARIANT-20261017-05", "Hydraulic Dual-Engine Dispatch Law"),
    ("INVARIANT-20261017-06", "Two-Tier Provenance Topology Law"),
    ("INVARIANT-20261017-07", "Headless Contract Sovereignty Law"),
]


def test_invariants_documented_and_clean():
    files = [
        INBOX_RACTOR / "DISPUTES_RESOLVED_20261017.md",
        INBOX_RACTOR / "DOGFOOD_RACTOR_SYSTEMS_20261017.md",
    ]
    for f in files:
        assert f.exists(), f"Missing file: {f}"
        content = f.read_text(encoding="utf-8")
        matches = EM_DASH.findall(content)
        assert len(matches) == 0, f"Found {len(matches)} em-dashes in {f.name}"


def test_all_seven_invariants_present():
    dogfood = (INBOX_RACTOR / "DOGFOOD_RACTOR_SYSTEMS_20261017.md").read_text(encoding="utf-8")
    for inv_id, inv_name in EXPECTED_INVARIANTS:
        assert inv_id in dogfood, f"Missing invariant ID: {inv_id}"
        assert inv_name in dogfood, f"Missing invariant Name: {inv_name}"


def test_enforcement_anchors_exist():
    # INVARIANT-01 & 05: local GPU offload anchor
    assert (ROOT / "tools" / "box_burn_fire.py").exists()

    # INVARIANT-03: paced width anchor in tools/full_scan.py
    full_scan = (ROOT / "tools" / "full_scan.py").read_text(encoding="utf-8")
    assert "INVARIANT-20261017-03" in full_scan

    # INVARIANT-04: single-writer leases & out-of-process evaluators anchor
    assert (ROOT / "watch" / "inbox" / "HN_SWARM_HARNESS_STEAL_20261017.md").exists()

    # INVARIANT-06: two-tier provenance anchor
    assert (ROOT / "watch" / "inbox" / "index_events.jsonl").exists()

    # INVARIANT-07: headless contract sovereignty anchor
    assert (ROOT / "tests" / "test_df_residuals.py").exists()
    assert (ROOT / "roblox" / "src" / "shared" / "Temptation.luau").exists()
    assert (ROOT / "roblox" / "src" / "shared" / "ProceduralBody.luau").exists()
    assert (ROOT / "roblox" / "src" / "shared" / "Worldgen.luau").exists()
