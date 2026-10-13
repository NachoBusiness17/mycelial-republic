"""leave_dispatcher exit-contract tests (night shift 2026-10-04; receipt
watch/inbox/night_shift_20261004/leave_dispatcher_cured.md).

The MagLeaveProtocolDaily exit-1-every-day disease (2026-09-30 through
2026-10-03, 8/8 nonzero runners each fire, zero receipts ever filed) had two
harness-level root causes, both cured inside scripts/run_mate.ps1:

  1. MODEL WALL: with no model pinned, opencode resolved its built-in default
     to zai/glm-5v-turbo, which the z.ai coding plan does not include
     ("Your current subscription plan does not yet include access to
     GLM-5V-Turbo", logs/mates/runs/run_20260930_*.log and
     run_20261002_*.log). Cure: the literal `-m zai/glm-4.7` flag.
  2. DB LOCK: all concurrent runners open the one shared
     ~/.local/share/opencode/opencode.db and the slow openers die "database
     is locked" (7 of 8 on 2026-10-03, 1 of 8 on 2026-10-02). Cure: per-run
     XDG_DATA_HOME isolation under logs/mates/ocdata/.

These bands pin both cures as source guards (a regression back to the
unpinned default or the shared storage is exactly the daily exit-1 disease)
and pin the dispatcher's honest exit contract: a clean/no-op day is 0, any
nonzero runner is 1, dry mode writes idempotent packs and exits 0.

Bands mirror tests/test_census_zero_collect.py house style: module import
(never from-imports of test helpers), real tmp trees, no live opencode.
"""
from __future__ import annotations

from pathlib import Path

import tools.leave_dispatcher as ld

# Module import, not from-imports (house rule from the sibling census tests):
# a from-import of a test_-prefixed helper would drop it into this module's
# namespace for pytest to mis-collect. Call everything as ld.<name>.
RUNNER_PS1 = Path(__file__).resolve().parents[1] / "scripts" / "run_mate.ps1"


def _patch(tmp_path, monkeypatch, runner_code: int | None):
    """Point the dispatcher's write surfaces at tmp, neutralize the live edges
    (path guard, STEER read, actual opencode invocation), and stamp the
    controlled runner exit code. run_one is resolved from module globals at
    main() call time, so monkeypatching it is enough."""
    missions = tmp_path / "missions"
    receipts = tmp_path / "receipts"
    logs = tmp_path / "logs"
    monkeypatch.setattr(ld, "MISSIONS_DIR", missions)
    monkeypatch.setattr(ld, "RECEIPTS_DIR", receipts)
    monkeypatch.setattr(ld, "LOG_DIR", logs)
    monkeypatch.setattr(ld, "_steer_block", lambda mate_id: "- (test steer row)")
    monkeypatch.setattr(ld, "_runner_path_guard", lambda: None)
    if runner_code is not None:
        monkeypatch.setattr(ld, "run_one", lambda _index: runner_code)
    return missions


def test_runner_pins_coding_plan_model_literal():
    """Guard: the opencode invocation carries the -m literal pin (cure 1).

    Evidence it guards: the unpinned default resolved to zai/glm-5v-turbo and
    every plan-authenticated mate died on the subscription wall."""
    src = RUNNER_PS1.read_text(encoding="utf-8-sig")
    assert "run -m zai/glm-4.7 $Prompt" in src


def test_runner_isolates_storage_and_serializes_log():
    """Guard: per-run XDG_DATA_HOME isolation (cure 2) and the named mutex on
    the shared runner_<date>.log (the 8-way Add-Content collision that kept
    only 2 of 24 lines in runner_20261003.log)."""
    src = RUNNER_PS1.read_text(encoding="utf-8-sig")
    assert "XDG_DATA_HOME" in src
    assert 'Join-Path $MatesDir ("ocdata\\" + $Mission.BaseName)' in src
    assert "MagLeaveRunnerLog" in src


def test_clean_day_exits_zero(tmp_path, monkeypatch):
    missions = _patch(tmp_path, monkeypatch, runner_code=0)
    assert ld.main([]) == 0
    packs = sorted(missions.glob("mission_*.md"))
    assert len(packs) == 8  # configs/mates.yaml ships 8 mates
    assert all(p.stat().st_size > 0 for p in packs)


def test_runner_failure_surfaces_as_exit_one(tmp_path, monkeypatch):
    _patch(tmp_path, monkeypatch, runner_code=1)
    assert ld.main([]) == 1  # honest: any nonzero runner is a nonzero day


def test_dry_mode_is_idempotent_and_exits_zero(tmp_path, monkeypatch):
    missions = _patch(tmp_path, monkeypatch, runner_code=None)
    assert ld.main(["--dry"]) == 0
    packs = sorted(missions.glob("mission_*.md"))
    assert len(packs) == 8
    before = {p.name: p.read_bytes() for p in packs}
    assert ld.main(["--dry"]) == 0
    after = {p.name: p.read_bytes() for p in sorted(missions.glob("mission_*.md"))}
    assert before == after  # existing packs are never rewritten (claims sacred)
