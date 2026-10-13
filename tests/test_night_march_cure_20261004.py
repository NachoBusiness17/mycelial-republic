"""Night-march cure tests (2026-10-04, free-lane repair).

Covers the two defects fixed that night:
1. watch/march_228.py crashed at import with FileNotFoundError on /app/.env
   (compose passes .env as env vars only; the file is never mounted), so the
   night composite logged an opaque "march rc=1" every night since 09-26.
   Cure: no-key runs exit rc=2 with a named MARCH SKIP reason, no crash.
2. mag/lane_runner.py cycle_night persisted last_night BEFORE trailing the
   CYCLE row, so an Errno-22 state-write failure through the cage bind mount
   (lane_scheduler.log 2026-09-14..2026-10-04) lost the record of completed
   work and re-ran the cycle every ~100s (5x CYCLE_FAIL on 2026-10-03).
   Cure: trail first, persist second; _save_state is atomic tmp+replace.
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def _make_sandbox(tmp_path: Path, env_body: str | None) -> Path:
    """Sandbox mirroring the cage layout: watch/march_228.py + mag/ organs,
    with .env present only when env_body is given (the cage has none)."""
    (tmp_path / "watch").mkdir()
    (tmp_path / "mag").mkdir()
    shutil.copy2(REPO / "watch" / "march_228.py", tmp_path / "watch" / "march_228.py")
    # march imports only these two stdlib-only organs at module level.
    shutil.copy2(REPO / "mag" / "bay_organs.py", tmp_path / "mag" / "bay_organs.py")
    shutil.copy2(REPO / "mag" / "flight_recorder.py", tmp_path / "mag" / "flight_recorder.py")
    if env_body is not None:
        (tmp_path / ".env").write_text(env_body, encoding="utf-8")
    return tmp_path


def _run_march(sandbox: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(sandbox / "watch" / "march_228.py")],
        capture_output=True, text=True, timeout=60, cwd=str(sandbox))


def test_march_no_env_file_exits_2_with_named_skip(tmp_path):
    """Cage shape: .env absent -> honest rc=2 + MARCH SKIP, never a crash."""
    r = _run_march(_make_sandbox(tmp_path, env_body=None))
    assert r.returncode == 2, r.stdout + r.stderr
    assert "MARCH SKIP rc=2" in r.stdout
    assert "no env door sanctioned" in r.stdout
    assert "Traceback" not in r.stderr  # pre-cure shape died with one


def test_march_env_file_without_key_exits_2(tmp_path):
    """Key file present but carrying no ZAI key -> same honest rc=2 skip."""
    r = _run_march(_make_sandbox(tmp_path, env_body="OTHER_KEY=x\n"))
    assert r.returncode == 2, r.stdout + r.stderr
    assert "MARCH SKIP rc=2" in r.stdout


def test_march_env_file_with_key_bootstraps(tmp_path):
    """Host shape: key present -> module loads, KEY non-empty (import-only;
    the __main__ march loop would fire real API calls, so it stays closed)."""
    sandbox = _make_sandbox(tmp_path, env_body="ZAI_API_KEY_Pro=test-key-123\n")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "march_228_probe", sandbox / "watch" / "march_228.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.KEY == "test-key-123"


@pytest.fixture()
def lanes_dir(tmp_path, monkeypatch):
    import mag.lane_runner as lr
    monkeypatch.setattr(lr, "LANES", tmp_path)
    yield tmp_path
    lr.LANES = lr.ROOT / "queue" / "lanes"


def test_save_state_atomic_and_readable(lanes_dir):
    """_save_state writes valid JSON via tmp+replace and leaves no tmp dotfile."""
    import mag.lane_runner as lr
    lr._save_state("night", {"last_night": "2026-10-04"})
    p = lanes_dir / "night" / "runner_state.json"
    assert json.loads(p.read_text(encoding="utf-8"))["last_night"] == "2026-10-04"
    assert lr._state("night")["last_night"] == "2026-10-04"
    assert not [q for q in p.parent.iterdir() if q.name.startswith(".")]
    lr._save_state("night", {"last_night": "2026-10-05", "seat": "night"})
    assert lr._state("night")["last_night"] == "2026-10-05"


def _fake_now_local_hour_3():
    # Naive 03:00 interpreted as host-local, returned as aware UTC: cycle_night's
    # .astimezone().hour is 3 on any host timezone (in the 23:00-09:00 window).
    return datetime(2026, 10, 4, 3, 0, 0).astimezone(timezone.utc)


def test_cycle_night_trails_composite_even_when_state_write_fails(
        lanes_dir, monkeypatch):
    """Ordering cure: a failing _save_state must not swallow the CYCLE row
    for work that already ran (the 2026-10-03 failure shape)."""
    import mag.lane_runner as lr
    monkeypatch.setattr(lr, "_now", _fake_now_local_hour_3)

    def fake_run(path, timeout=600):
        if "monitor" in path:
            return 0, "ok"
        return 2, "MARCH SKIP rc=2: no key - /app/.env absent (probe)"
    monkeypatch.setattr(lr, "_run_script", fake_run)
    def boom(lane, st):
        raise OSError(22, "Invalid argument", "/app/queue/lanes/night/runner_state.json")
    monkeypatch.setattr(lr, "_save_state", boom)
    with pytest.raises(OSError):
        lr.cycle_night()
    trail = (lanes_dir / "night" / "trail.jsonl").read_text(encoding="utf-8")
    assert "night composite: monitor rc=0; march rc=2" in trail
    assert "MARCH SKIP rc=2" in trail  # march output tail is no longer discarded


def test_cycle_night_persists_last_night_on_green(lanes_dir, monkeypatch):
    import mag.lane_runner as lr
    monkeypatch.setattr(lr, "_now", _fake_now_local_hour_3)
    monkeypatch.setattr(lr, "_run_script", lambda path, timeout=600: (0, "ok"))
    result = lr.cycle_night()
    assert result == "monitor rc=0; march rc=0"
    assert lr._state("night")["last_night"] == "2026-10-04"
    trail = (lanes_dir / "night" / "trail.jsonl").read_text(encoding="utf-8")
    assert '"event": "CYCLE"' in trail
