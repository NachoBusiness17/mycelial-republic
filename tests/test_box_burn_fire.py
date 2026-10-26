"""Unit tests for tools/box_burn_fire.py (Stone 7 job-firing engine)."""
import subprocess
import sys
from datetime import time as dtime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.box_burn_fire import parse_stop, past_stop, read_backlogs, burn, main


def test_parse_stop():
    t = parse_stop("07:00")
    assert isinstance(t, dtime)
    assert t.hour == 7
    assert t.minute == 0


def test_read_backlogs_nonexistent(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.box_burn_fire.PILE_QUEUE", tmp_path / "missing_pile.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.BRIEF_BACKLOG", tmp_path / "missing_brief.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.TRAIN_BACKLOG", tmp_path / "missing_train.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.WHISPER_BACKLOG", tmp_path / "missing_whisper.jsonl")
    jobs = read_backlogs()
    assert jobs == []


def test_read_backlogs_populated(tmp_path, monkeypatch):
    p = tmp_path / "pile.jsonl"
    p.write_text('{"cmd": "python test.py"}\n{"cmd": "echo 1"}\n', encoding="utf-8")
    monkeypatch.setattr("tools.box_burn_fire.PILE_QUEUE", p)
    monkeypatch.setattr("tools.box_burn_fire.BRIEF_BACKLOG", tmp_path / "missing.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.TRAIN_BACKLOG", tmp_path / "missing.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.WHISPER_BACKLOG", tmp_path / "missing.jsonl")
    jobs = read_backlogs()
    assert len(jobs) == 2
    assert jobs[0]["source"] == "pile"
    assert jobs[0]["cmd"] == "python test.py"


def test_burn_dry_run(tmp_path, monkeypatch):
    p = tmp_path / "pile.jsonl"
    p.write_text('{"cmd": "echo test1"}\n{"cmd": "echo test2"}\n', encoding="utf-8")
    monkeypatch.setattr("tools.box_burn_fire.PILE_QUEUE", p)
    monkeypatch.setattr("tools.box_burn_fire.BRIEF_BACKLOG", tmp_path / "missing.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.TRAIN_BACKLOG", tmp_path / "missing.jsonl")
    monkeypatch.setattr("tools.box_burn_fire.WHISPER_BACKLOG", tmp_path / "missing.jsonl")
    # Set stop time to tomorrow so it doesn't immediately abort
    stop_t = dtime(23, 59)
    monkeypatch.setattr("tools.box_burn_fire.past_stop", lambda t: False)
    monkeypatch.setattr("tools.box_burn_fire.cpu_percent", lambda: 10.0)
    monkeypatch.setattr("tools.box_burn_fire.gpu_percent", lambda: 10.0)
    spawned = burn(target_cpu=99.0, target_gpu=99.0, stop_t=stop_t, dry_run=True, max_concurrency=2)
    assert spawned == 2


def test_main_cli_dry_run(monkeypatch):
    monkeypatch.setattr("tools.box_burn_fire.past_stop", lambda t: False)
    monkeypatch.setattr("tools.box_burn_fire.cpu_percent", lambda: 10.0)
    monkeypatch.setattr("tools.box_burn_fire.gpu_percent", lambda: 10.0)
    rc = main(["--dry-run", "--stop", "23:59"])
    assert rc == 0


def test_past_stop_overnight_wrap():
    stop_t = parse_stop("07:00")
    assert past_stop(stop_t, now=dtime(22, 0)) is False
    assert past_stop(stop_t, now=dtime(2, 30)) is False
    assert past_stop(stop_t, now=dtime(7, 0)) is True
    assert past_stop(stop_t, now=dtime(14, 0)) is True
