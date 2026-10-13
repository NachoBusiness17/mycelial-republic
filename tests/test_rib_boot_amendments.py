"""R4-L2 (2026-10-05 ouroboros memory fold): amendment tails ride the mounted law.

The founding defect: mag/rib_boot.py LAW_HEAD_CHARS=1200 cut every POST-DATUM/
AMENDMENT section off the mounted law heads (byte-measured offsets 5905/6397/2836,
all beyond the cut), so the only law-byte surface in the estate served
PRE-amendment doctrine and the d4 thinking law was invisible to the one organ
built to carry it. These tests fail if the mount ever serves pre-amendment law
again, if the ouroboros driver regresses to bus-only boot, or if context_pack
stops consuming the vault block (the 25KB write-only orphan disease).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

D4_MARKER = "omission is a MEASURED ON state"


def test_mount_vault_carries_amendment_markers_in_law_heads():
    from mag.rib_boot import mount_vault

    v = mount_vault()
    laws = [l for l in v["law_ribs"] if l.get("mounted")]
    assert laws, "no law ribs mounted"
    amended = [l for l in laws if l.get("amendment_count")]
    assert amended, "zero amendments mounted -- the 1200-char cut is back"
    for l in amended:
        assert ("POST-DATUM" in l["law_head"]) or ("AMENDMENT" in l["law_head"]), (
            f"{l['file']} claims amendments but its law_head carries no marker")


def test_mount_vault_d4_marker_rides_a_law_head():
    from mag.rib_boot import mount_vault

    v = mount_vault()
    heads = [l["law_head"] for l in v["law_ribs"] if l.get("mounted")]
    assert any(D4_MARKER in h for h in heads), (
        "the d4 thinking law (omission is a MEASURED ON state) is not mounted -- "
        "the founding defect of the 1200-char cut has regressed")


def test_mount_vault_head_prefix_is_untouched_amendments_append():
    """Amend-never-rewrite applies to the mount: the first 1200 normalized chars
    of each rib still lead the law_head; amendments ride AFTER them."""
    from mag.rib_boot import LAW_HEAD_CHARS, VAULT, VAULT_RIBS, mount_vault

    v = mount_vault()
    for l in v["law_ribs"]:
        if not l.get("mounted"):
            continue
        f = VAULT / l["file"]
        raw_head = " ".join(f.read_text(encoding="utf-8", errors="replace").split())[:LAW_HEAD_CHARS]
        assert l["law_head"].startswith(raw_head), (
            f"{l['file']}: the 1200-char head was rewritten, not appended to")


def test_mount_vault_amendment_list_matches_count():
    from mag.rib_boot import mount_vault

    v = mount_vault()
    for l in v["law_ribs"]:
        if l.get("mounted"):
            assert l["amendment_count"] == len(l.get("law_amendments") or []), (
                f"{l['file']}: amendment_count disagrees with law_amendments")


def test_main_boot_artifact_carries_divert_anchor_and_register(tmp_path, monkeypatch):
    """main() must (a) divert the FROZEN brief to state/CURRENT.md, (b) anchor
    the chain block at verkle_tip.json with an age-debt line, (c) point at the
    demotion register. Written to a tmp OUT so the test never clobbers the
    live boot artifact."""
    from mag import rib_boot

    monkeypatch.setattr(rib_boot, "OUT", tmp_path / "rib_boot.json")
    monkeypatch.setattr(sys, "argv", ["mag.rib_boot"])  # argparse must not see pytest's argv
    assert rib_boot.main() == 0
    j = json.loads((tmp_path / "rib_boot.json").read_text(encoding="utf-8"))
    # (a) brief divert: the 2026-09-26 fossil head must not ride verbatim
    assert j["brief"].get("diverted_from_frozen") is True, (
        "FROZEN brief served verbatim -- the lanes.py Q1 divert is missing from rib_boot")
    assert "# FROZEN" not in j["brief"]["head"][:60]
    # (b) chain anchor at the tail itself, with a visible age line
    assert j["chain"].get("anchor") == "memory/biography/verkle_tip.json", (
        "chain block not anchored at verkle_tip.json (warm_state snapshot disease)")
    assert j["chain"].get("age_debt"), "no age-debt line on the chain anchor"
    # (c) demotion register pointer
    assert j["superseded_register"]["path"] == "memory/fold_history/SUPERSEDED.md"
    assert j["superseded_register"]["exists"] is True


def test_ouroboros_driver_mounts_the_vault_with_amendments():
    """The ouroboros rib_boot_mount() must EXECUTE mag.rib_boot (not the bus
    alone) and surface the amendment markers in what it mounts."""
    from mag.rib_boot import VAULT_RIBS
    from tools.ouroboros import rib_boot_mount

    r = rib_boot_mount()
    assert r.get("ok") is True, f"vault boot failed under the driver: {r}"
    assert r.get("doctrine_ribs"), "bus rib count lost in the rewrite"
    # R4b (2026-10-05): asserted == 5 until the behavior-cards deck mounted as a
    # sixth rib (consumer-or-strike, ouroboros R4 move 6); a hard-coded count is a
    # census constant that rots on every deliberate mount change, so the assertion
    # now pins the mechanism (every named rib mounts) against the live list.
    assert r.get("vault_law_ribs_mounted") == len(VAULT_RIBS), (
        f"expected {len(VAULT_RIBS)} law ribs mounted, got {r.get('vault_law_ribs_mounted')}")
    assert r.get("amendment_marker_hits", 0) >= 1, (
        "driver-mounted law carries zero POST-DATUM/AMENDMENT markers -- bus-only regression")
    assert r.get("d4_marker_mounted") is True, (
        "the driver-mounted law lacks the d4 marker (omission is a MEASURED ON state)")


def test_context_pack_consumes_the_vault_block():
    """rib_boot.json's first code consumer: the pack carries rib_vault with the
    digest, the d4 law, and the demotion-register pointer."""
    from mag.context_pack import _rib_vault_law

    rv = _rib_vault_law()
    assert rv["digest"].startswith("[rib vault:"), f"unexpected digest: {rv['digest'][:80]}"
    assert "memory/fold_history/SUPERSEDED.md" in rv["digest"]
    assert D4_MARKER in rv["body"], "vault body lost the d4 amendment under its caps"
    assert "POST-DATUM" in rv["body"]


def test_context_pack_renders_vault_block_when_budget_allows(tmp_path, monkeypatch):
    """With headroom, the vault block renders; tight budgets shed it AFTER
    L1 bonds (visible in PACK_OFFLOAD), never a hard clip on its account."""
    from mag import context_pack as cp

    pack = cp.build_context_pack(mode="plan", fast=True)
    assert "rib_vault" in pack, "vault block not mounted into the pack dict"
    offload = tmp_path / "PACK_OFFLOAD.jsonl"
    monkeypatch.setattr(cp, "PACK_OFFLOAD_FILE", offload)
    text = cp.format_context_pack_text(pack, mode="plan", max_chars=30000)
    assert "L0d RIB vault amendments" in text, (
        "vault block never renders even with ample budget")
    assert D4_MARKER in text, "rendered vault block lost the d4 law"
    # and under a forced shed, the block goes AFTER bonds do (p1a-L0d-fix
    # 2026-10-07, pheromone-swarm: the R4-L2 ahead-of-bonds placement let the
    # carrier die at stage 3 ahead of skills/trail -- d01 dogfood2 measured
    # 9471 > 7200 with POST-DATUM law never reaching fresh seats; law
    # outlives convenience context now)
    cp.format_context_pack_text(pack, mode="plan", max_chars=11000)
    rows = [json.loads(l) for l in offload.read_text(encoding="utf-8").splitlines() if l.strip()]
    shed_names = [s for r in rows for s in r["shed_sections"]]
    if "L0d rib vault amendments" in shed_names:
        assert "L1 bonds" in shed_names and (
            shed_names.index("L1 bonds") < shed_names.index("L0d rib vault amendments")), (
            "vault law shed before bonds/skills/trail -- the old stage-3 amputation is back")


def test_context_pack_vault_debt_pointer_when_artifact_missing(tmp_path, monkeypatch):
    """A missing/stale rib_boot.json renders as debt, never as silence or law."""
    from mag import context_pack as cp

    monkeypatch.setattr(cp, "ROOT", tmp_path)
    rv = cp._rib_vault_law()
    assert "regen owed" in rv["digest"]
    assert rv["body"] == rv["digest"]
