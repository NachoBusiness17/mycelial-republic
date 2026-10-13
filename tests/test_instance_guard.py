"""instance_guard tests (dogfood-48h ractor moves 1+4, 2026-10-02).

Covers the three shapes: process singleton (exit-3 semantics + stale
reclaim), per-ask O_EXCL claim (held / stale-steal / release), and the
doubled-key ingest tripwire. Evidence for the disease being cured:
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md moves 1+4.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import instance_guard as ig  # noqa: E402


def test_claim_process_fresh_then_busy(tmp_path):
    pidfile = ig.claim_process("gtest", pid_dir=tmp_path)
    assert pidfile.is_file()
    assert int(pidfile.read_text().strip()) == os.getpid()
    with pytest.raises(ig.InstanceBusy):
        ig.claim_process("gtest", pid_dir=tmp_path)


def test_claim_process_stale_reclaim(tmp_path, monkeypatch):
    pidfile = tmp_path / "gtest2.pid"
    pidfile.write_text("4000000", encoding="utf-8")  # not-alive pid
    ig.claim_process("gtest2", pid_dir=tmp_path)
    assert int(pidfile.read_text().strip()) == os.getpid()
    # unparseable pidfile is equally reclaimable
    (tmp_path / "gtest3.pid").write_text("not-a-pid", encoding="utf-8")
    ig.claim_process("gtest3", pid_dir=tmp_path)


def test_guard_or_exit_exit3(tmp_path, capsys):
    ig.claim_process("gtest4", pid_dir=tmp_path)
    with pytest.raises(SystemExit) as ei:
        ig.guard_or_exit("gtest4", pid_dir=tmp_path)
    assert ei.value.code == 3
    assert "already running" in capsys.readouterr().err


def test_claim_ask_fresh_held_stale_steal(tmp_path):
    m1 = ig.claim_ask(tmp_path, "A1")
    assert m1 is not None and (tmp_path / "CLAIM").is_file()
    # fresh claim held by a live pid (ours) -> second racer refused
    assert ig.claim_ask(tmp_path, "A1") is None
    ig.release_ask(m1)
    assert not (tmp_path / "CLAIM").exists()
    # stale by age: holder ts far in the past -> stolen even though pid live
    (tmp_path / "CLAIM").write_text(
        json.dumps({"pid": os.getpid(), "ts": 0, "id": "A1"}), encoding="utf-8")
    m2 = ig.claim_ask(tmp_path, "A1")
    assert m2 is not None
    holder = json.loads((tmp_path / "CLAIM").read_text(encoding="utf-8"))
    assert holder["pid"] == os.getpid()


def test_release_ask_leaves_foreign_claim(tmp_path):
    foreign = tmp_path / "CLAIM"
    foreign.write_text(json.dumps({"pid": 4000000, "ts": 0}), encoding="utf-8")
    ig.release_ask(foreign)
    assert foreign.is_file()  # not ours: untouched


def test_ledger_key_exists_tail(tmp_path):
    ledger = tmp_path / "usage.jsonl"
    rows = [{"id": f"X{i}", "turn": 1} for i in range(5)]
    ledger.write_text("\n".join(json.dumps(r) for r in rows) + "\n",
                      encoding="utf-8")
    assert ig.ledger_key_exists(ledger, "X3", 1)
    assert not ig.ledger_key_exists(ledger, "X3", 2)
    assert not ig.ledger_key_exists(ledger, "missing", 1)
    assert not ig.ledger_key_exists(tmp_path / "nope.jsonl", "X3", 1)


def test_doubled_key_check_flags_and_alarms(tmp_path, monkeypatch):
    monkeypatch.setattr(ig, "ROOT", tmp_path)
    ledger = tmp_path / "usage.jsonl"
    ledger.write_text(json.dumps({"id": "A1", "turn": 1}) + "\n",
                      encoding="utf-8")
    clean = ig.doubled_key_check(ledger, {"id": "B1", "turn": 1})
    assert "doubled_key" not in clean
    flagged = ig.doubled_key_check(ledger, {"id": "A1", "turn": 1})
    assert flagged["doubled_key"] is True
    attention = tmp_path / "memory" / "attention.md"
    assert "doubled-key alarm" in attention.read_text(encoding="utf-8")
    assert "(id=A1, turn=1)" in attention.read_text(encoding="utf-8")


def test_hermes_burn_run_ask_claim_skip(tmp_path, monkeypatch):
    """The wrapper shape: a held CLAIM makes run_ask skip BEFORE any fire
    (the money race the twins won twice)."""
    from tools import hermes_burn
    ask = tmp_path / "askdir"
    ask.mkdir()
    (ask / "ask.json").write_text(
        json.dumps({"id": "T1", "model": next(iter(hermes_burn.PRICING)),
                    "contract": "x"}), encoding="utf-8")
    # a fresh claim held by a live pid (this test process)
    held = ig.claim_ask(ask, "T1")
    assert held is not None
    row = hermes_burn.run_ask(ask, key="", execute=False)
    assert row["ok"] is True and "CLAIM" in row["skipped"]
    # our own claim must not have been stolen or released by the skip
    assert (ask / "CLAIM").is_file()
    ig.release_ask(held)


def test_hermes_burn_bank_doubled_key(tmp_path, monkeypatch):
    from tools import hermes_burn
    monkeypatch.setattr(hermes_burn, "USAGE", tmp_path / "usage.jsonl")
    monkeypatch.setattr(ig, "ROOT", tmp_path)  # alarm lands in tmp attention
    hermes_burn._bank({"id": "D1", "turn": 1, "cost_usd": 0.1})
    hermes_burn._bank({"id": "D1", "turn": 1, "cost_usd": 0.1})
    lines = (tmp_path / "usage.jsonl").read_text(encoding="utf-8").splitlines()
    assert "doubled_key" not in lines[0]
    assert json.loads(lines[1])["doubled_key"] is True


def test_doubled_key_alarm_dedups_per_key(tmp_path, monkeypatch):
    """2026-10-03 cure: one alarm LINE per (id, turn). The 2026-10-03
    cross-session id collisions (DND0_*/TAVERN_* beats) appended an alarm
    every ~5s for hours and buried the attention surface; repeat fires must
    still STAMP the row, just not re-alarm."""
    monkeypatch.setattr(ig, "ROOT", tmp_path)
    ledger = tmp_path / "usage.jsonl"
    ledger.write_text(json.dumps({"id": "K1", "turn": 1}) + "\n" +
                      json.dumps({"id": "K2", "turn": 1}) + "\n",
                      encoding="utf-8")
    for _ in range(3):
        row = ig.doubled_key_check(ledger, {"id": "K1", "turn": 1})
        assert row["doubled_key"] is True  # every fire stamps
    attention = tmp_path / "memory" / "attention.md"
    alarms = [ln for ln in attention.read_text(encoding="utf-8").splitlines()
              if "doubled-key alarm" in ln and "(id=K1, turn=1)" in ln]
    assert len(alarms) == 1  # but alarms exactly once
    # a DIFFERENT key still alarms fresh
    ig.doubled_key_check(ledger, {"id": "K2", "turn": 1})
    alarms2 = [ln for ln in attention.read_text(encoding="utf-8").splitlines()
               if "doubled-key alarm" in ln and "(id=K2, turn=1)" in ln]
    assert len(alarms2) == 1
