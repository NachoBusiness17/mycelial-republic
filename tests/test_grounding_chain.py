"""Tests for scripts/grounding_chain.py: the B2-56 returncode law.

CAUSE: the chain discarded the child returncode and appended its WHY row
before firing, so a driver that died mid-fire still left a row claiming a
fire over stranded state. EVIDENCE: the 2026-09-26 KeyError fire crashed
the research child, stranded run.lock + state.json, while the 11:28:14Z
grounding_chain.jsonl row claimed the fire
(watch/inbox/burn_wave_20260926/B2_07_grounding_20260926.md).

The law under test: every fired action in the row carries the child exit
code (or fire_error) plus the lane state read before and after the child
exited, and the row is appended only after the fires settle.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import grounding_chain as gc  # noqa: E402


def _setup(tmp_path, monkeypatch, actions):
    """Point the chain at a temp log, freeze evaluate(), fake the lane state."""
    log = tmp_path / "grounding_chain.jsonl"
    monkeypatch.setattr(gc, "CHAIN_LOG", log)
    monkeypatch.setattr(gc, "evaluate", lambda: actions)
    monkeypatch.setattr(gc, "queue_remaining", lambda: 13)
    monkeypatch.setattr(gc, "build_remaining", lambda: 2)
    monkeypatch.setattr(gc, "lock_age", lambda p: None)
    return log


def _rows(log: Path) -> list[dict]:
    return [json.loads(ln) for ln in log.read_text(encoding="utf-8").splitlines()
            if ln.strip()]


def _research_action() -> dict:
    return {"action": "research", "cmd": ["sentinel-python", "--batch", "16"],
            "why": "research queue 13, lock clear/stale",
            "condition": "queue_nonempty + lock_clear"}


def test_nonzero_exit_recorded_with_state_delta(tmp_path, monkeypatch):
    tender = {"action": "tender_signal", "cmd": None,
              "why": "research queue 13 below tender threshold",
              "condition": "queue_low"}
    log = _setup(tmp_path, monkeypatch, [_research_action(), tender])

    def fake_run(cmd, **kw):
        # marker line proves record() runs after the fire, not before it
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"marker": "fired"}) + "\n")
        return subprocess.CompletedProcess(cmd, 3)

    monkeypatch.setattr(gc.subprocess, "run", fake_run)
    assert gc.main(["--once"]) == 0

    rows = _rows(log)
    assert rows[0] == {"marker": "fired"}
    row = rows[1]
    fired = row["actions"][0]
    assert fired["exit_code"] == 3
    assert fired["state_before"] == {"remaining": 13, "lock_age_s": None}
    assert fired["state_after"] == {"remaining": 13, "lock_age_s": None}
    assert "fire_error" not in fired
    # non-fired actions stay untouched (no outcome invented for them)
    assert "exit_code" not in row["actions"][1]
    assert "state_after" not in row["actions"][1]


def test_row_after_fire_ordering(tmp_path, monkeypatch):
    log = _setup(tmp_path, monkeypatch, [_research_action()])
    monkeypatch.setattr(gc.subprocess, "run",
                        lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0))
    assert gc.main(["--once"]) == 0
    rows = _rows(log)
    assert len(rows) == 1
    assert rows[0]["schema"] == "grounding_chain.v1"


def test_exception_recorded(tmp_path, monkeypatch):
    log = _setup(tmp_path, monkeypatch, [_research_action()])

    def boom(cmd, **kw):
        raise FileNotFoundError(2, "no such file")

    monkeypatch.setattr(gc.subprocess, "run", boom)
    assert gc.main(["--once"]) == 0
    fired = _rows(log)[0]["actions"][0]
    assert fired["exit_code"] is None
    assert fired["fire_error"].startswith("FileNotFoundError")


def test_timeout_recorded(tmp_path, monkeypatch):
    log = _setup(tmp_path, monkeypatch, [_research_action()])

    def slow(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd=["sentinel-python"], timeout=900)

    monkeypatch.setattr(gc.subprocess, "run", slow)
    assert gc.main(["--once"]) == 0
    fired = _rows(log)[0]["actions"][0]
    assert fired["exit_code"] is None
    assert fired["fire_error"] == "timeout after 900s"


def test_dry_fires_nothing_and_invents_no_outcome(tmp_path, monkeypatch):
    log = _setup(tmp_path, monkeypatch, [_research_action()])

    def must_not_fire(cmd, **kw):
        raise AssertionError("dry mode must not fire")

    monkeypatch.setattr(gc.subprocess, "run", must_not_fire)
    assert gc.main(["--dry", "--once"]) == 0
    fired = _rows(log)[0]["actions"][0]
    assert "exit_code" not in fired
    assert "state_after" not in fired


def test_lane_state_build(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, [])
    assert gc.lane_state("build") == {"remaining": 2, "lock_age_s": None}
    assert gc.lane_state("tender_signal") == {}


def test_live_dead_child_end_to_end_injected_base(tmp_path, monkeypatch):
    """B2-290: the live-dead-child proof. A REAL scratch child (no mocks) that
    exits 3 runs against an injected scratch base via --base/--log; the row
    must record exit 3 with an unchanged state delta, and the production
    grounding_chain.jsonl must stay byte-untouched (the injection falsifier:
    if this run writes the production log, injection is broken)."""
    scratch_base = tmp_path / "scratch_base"
    scratch_base.mkdir()
    (scratch_base / "state.json").write_text(
        json.dumps({"done": [], "dead": {}, "attempts": {}}), encoding="utf-8")
    (scratch_base / "queue.jsonl").write_text(
        json.dumps({"id": "scratch-1"}) + "\n", encoding="utf-8")
    scratch_log = tmp_path / "scratch_chain.jsonl"

    prod_log = Path(gc.__file__).resolve().parents[1] / "watch" / "inbox" / \
        "union_fullsend_20260917" / "grounding_chain.jsonl"
    prod_before = prod_log.read_bytes() if prod_log.is_file() else None

    child = tmp_path / "dead_child.py"
    child.write_text("import sys\nsys.exit(3)\n", encoding="utf-8")
    monkeypatch.setattr(gc, "CMD_RESEARCH",
                        [gc.PY, str(child)])
    # real evaluate() on real scratch bytes must produce the research action
    monkeypatch.setattr(gc, "lock_age", lambda p: 9999)

    assert gc.main(["--once", "--base", str(scratch_base),
                    "--log", str(scratch_log)]) == 0

    if prod_before is None:
        assert not prod_log.is_file(), "injected run created the production log"
    else:
        assert prod_log.read_bytes() == prod_before, \
            "injected run wrote the production grounding_chain.jsonl"

    rows = [json.loads(ln) for ln in
            scratch_log.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(rows) == 1
    fired = rows[0]["actions"][0]
    assert fired["action"] == "research"
    assert fired["exit_code"] == 3
    assert fired["state_before"] == fired["state_after"]
    assert fired["state_after"]["remaining"] == 1
    assert "fire_error" not in fired
