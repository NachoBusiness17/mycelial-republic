"""Unit tests for golem_shabbat.py (Golem kill switch, Shabbat cycle, Ghost residuals).

Verifies:
1. Zero em-dashes invariant across mag/golem_shabbat.py and this test file.
2. GolemKillSwitch life/death single-character diff ('EMET' -> 'MET') and halt assertions.
3. ShabbatCycle periodic dormancy calculation and emergency override validation.
4. GhostResidual cryptographic hashing and dead-end hypothesis collision rejection.
"""
import re
import tempfile
from pathlib import Path

from mag.golem_shabbat import (
    GolemKillSwitch,
    GolemHaltError,
    ShabbatCycle,
    ShabbatDormancyError,
    GhostResidual,
    GhostResidualRegistry,
    TOKEN_EMET,
    TOKEN_MET,
)

ROOT = Path(__file__).resolve().parent.parent
EM_DASH = re.compile(r"[\u2010\u2011\u2012\u2013\u2014\u2015]")


def test_zero_em_dashes():
    targets = [
        ROOT / "mag" / "golem_shabbat.py",
        ROOT / "tests" / "test_golem_shabbat.py",
        ROOT / "watch" / "inbox" / "FICTION_CANON_SCI_FI_SYSTEM_STEALS_20261017.md",
        ROOT / "watch" / "inbox" / "falsifier_audits" / "THESES_AUDIT_PART4_20261017.md",
        ROOT / "memory" / "runs" / "mickey17_v2" / "runs" / "afternoon-block-20261017" / "lanes" / "m4-falsifier-truths.json",
        ROOT / "watch" / "inbox" / "SEAT_CENSUS_AND_WHY_GAP_ANALYSIS_20261017.md",
        ROOT / "watch" / "inbox" / "SPACE_BUNNY_INTEGER_MULT_STEAL_20261017.md",
    ]
    for target in targets:
        assert target.exists(), f"Target missing: {target}"
        content = target.read_text(encoding="utf-8")
        matches = EM_DASH.findall(content)
        assert len(matches) == 0, f"Found {len(matches)} em-dashes in {target.name}"


def test_golem_kill_switch_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        token_file = Path(tmpdir) / "golem_token.txt"
        switch = GolemKillSwitch(token_path=token_file)

        # Initial state: ensure_initialized writes EMET
        assert switch.ensure_initialized() == TOKEN_EMET
        assert switch.is_alive() is True
        switch.assert_alive()  # does not raise

        # Kill: exactly 1 char removed ('EMET' -> 'MET')
        res, reason = switch.kill(reason="test_drift_detected")
        assert res == TOKEN_MET
        assert reason == "test_drift_detected"
        assert switch.is_alive() is False

        # Verify exact diff: length drops by 1, suffix matches
        assert len(TOKEN_EMET) - len(TOKEN_MET) == 1
        assert TOKEN_EMET[1:] == TOKEN_MET

        # Assert alive raises GolemHaltError
        try:
            switch.assert_alive()
            assert False, "Expected GolemHaltError"
        except GolemHaltError:
            pass

        # Revive: restores EMET
        assert switch.revive() == TOKEN_EMET
        assert switch.is_alive() is True
        switch.assert_alive()


def test_shabbat_cycle_dormancy_and_override():
    # 100-hour interval, 20-hour dormancy, starting at 0
    cycle = ShabbatCycle(interval_hours=100, dormancy_hours=20, anchor_epoch=0.0)

    # At t=10 hours (36000s): inside dormancy window (0 < 10 < 20)
    t_inside = 10 * 3600.0
    assert cycle.is_shabbat(t_inside) is True

    # At t=50 hours (180000s): outside dormancy window (20 <= 50 < 100)
    t_outside = 50 * 3600.0
    assert cycle.is_shabbat(t_outside) is False
    assert cycle.check_clearance(t_outside) is True

    # Clearance inside without override raises ShabbatDormancyError
    try:
        cycle.check_clearance(t_inside)
        assert False, "Expected ShabbatDormancyError"
    except ShabbatDormancyError:
        pass

    # Clearance inside with pikuach nefesh override succeeds
    cleared = cycle.check_clearance(
        t_inside, pikuach_nefesh_override="critical database corruption recovery"
    )
    assert cleared is True


def test_ghost_residual_and_registry():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger = Path(tmpdir) / "ghosts.jsonl"
        registry = GhostResidualRegistry(ledger_path=ledger)

        # Create wisp for Mickey-17 iteration 3
        wisp = GhostResidual.create(
            seat_id="seat-mickey-17",
            iteration=3,
            parent_hash="0000000000000000",
            dead_end_hypothesis="Verkle knot collision via direct linear search",
            next_probable_vector="Sparse polynomial evaluation over sub-branch",
        )
        assert len(wisp.residual_hash) == 64
        registry.append(wisp)

        # Successor seat proposes hypotheses
        # Repeating the dead end is rejected
        assert (
            registry.validate_hypothesis_not_repeated(
                "seat-mickey-17", "Verkle knot collision via direct linear search"
            )
            is False
        )
        # Clean case-insensitive match check
        assert (
            registry.validate_hypothesis_not_repeated(
                "seat-mickey-17", "verkle knot collision via direct linear search"
            )
            is False
        )

        # New hypothesis is accepted
        assert (
            registry.validate_hypothesis_not_repeated(
                "seat-mickey-17", "KZG commitment evaluation over BLS12-381"
            )
            is True
        )
