"""tests for swarm_local_drain — the ROOT-CAUSE fix: a LOCAL drainer for the swarm queue (the k8s
CronJob drainer never runs on Windows). Deterministic coordinator + bounded swarm work.

RIB (frozen spec):
  key_reconcile() -> reconcile the key env: provider reads DEEPSEEK_SWARM_API_KEY, local .env sets
      DEEPSEEK_API_KEY; alias the present key into the provider env (in-process). Never logs the
      value. Honest resolved_provider_key flag.
  drain_pass(limit) -> run the EXISTING swarm_worker.run_once() LOCALLY (bounded) with the key
      reconciled. If no key resolves, honest ok:False (does NOT silently queue-fail).
  run_cadence(per_beat, daily_cap) -> bounded + daily-capped self-healing drain beat; skips when the
      daily cap is hit.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import swarm_local_drain as sld  # noqa: E402


def test_status_contract_and_fixes():
    st = sld.status()
    assert st["ok"] is True
    assert st["schema"] == "swarm_local_drain.v1"
    # it names the two things it fixes
    assert "dead k8s CronJob drain" in st["fixes"]
    assert "key env mismatch" in st["fixes"]
    assert "swarm_worker" in st["reuses"]


def test_key_reconcile_never_logs_value():
    kr = sld.key_reconcile()
    assert kr["ok"] is True
    assert kr["resolved_provider_key"] in (True, False)
    # the key VALUE must never appear in the output (name only)
    import json
    blob = json.dumps(kr).lower()
    for secret_marker in ("sk-", "deepseek_swarm_api_key=sk"):
        assert secret_marker not in blob


def test_drain_pass_does_not_require_deepseek_for_local_work(monkeypatch):
    # A missing DeepSeek key must not block local/free rightsized work.
    monkeypatch.setattr(
        sld, "key_reconcile",
        lambda: {"ok": True, "resolved_provider_key": False, "note": "test"},
    )

    monkeypatch.setattr(
        "mag.swarm_worker.run_rightsized_once",
        lambda **kwargs: {"done": 0, "failed": 0, "skipped": 0},
    )
    r = sld.drain_pass(limit=1)
    assert r["ok"] is True
    assert r["done"] == 0



# a current backup_chain exposes these; run_cadence refuses a copy without them (2026-10-15)
_CURRENT = "COMPLETE_MANIFEST = 'BACKUP_COMPLETE.json'\nPINNED = frozenset({'biography_backup_20261004'})\n"


def _stub_backup(tmp_path, body):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "memory").mkdir()
    (tmp_path / "scripts" / "backup_chain.py").write_text(body, encoding="utf-8")


def test_run_cadence_daily_cap_guard(monkeypatch, tmp_path):
    # the drain is bounded: it never exceeds the daily cap. The beat's backup step is stubbed so
    # this test never reaches memory/biography (2026-10-15: it used to run the real backup).
    _stub_backup(tmp_path, _CURRENT + "def backup(*, force=False):\n    return {'ok': True, 'skipped': 'test-stub'}\n")
    monkeypatch.setattr(sld, "ROOT", tmp_path)
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["ok"] is True
    assert r["skipped"] == "daily-cap"
    assert r["daily_cap"] == 0
    assert r["backup"] == {"ok": True, "skipped": "test-stub"}


def test_run_cadence_backup_failure_is_loud(monkeypatch, tmp_path, capsys):
    # 2026-10-15: truncated chain backups (3,370 and 219 of ~48k knots) were swallowed by
    # `except Exception: pass`. A failure is now printed and alarmed through backup_chain.alarm()
    # (memory/attention.md, the census/meter patrol channel); the drain beat still runs.
    _stub_backup(tmp_path, _CURRENT + (
        "from pathlib import Path\n"
        "def alarm(verdict, detail=None):\n"
        "    p = Path(__file__).resolve().parent.parent / 'memory' / 'attention.md'\n"
        "    with p.open('a', encoding='utf-8') as f:\n"
        "        f.write('### Chain backup patrol fired\\n- verdict: ' + verdict + '\\n')\n"
        "def backup(*, force=False):\n"
        "    raise RuntimeError('chain backup INCOMPLETE: knots 221/48032 files')\n"))
    monkeypatch.setattr(sld, "ROOT", tmp_path)
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["ok"] is True and r["skipped"] == "daily-cap"
    assert r["backup"]["ok"] is False and "INCOMPLETE" in r["backup"]["error"]
    assert "CHAIN BACKUP FAILED" in capsys.readouterr().out
    att = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert "Chain backup patrol fired" in att and "221/48032" in att


def test_run_cadence_backup_module_missing_still_alarms(monkeypatch, tmp_path):
    (tmp_path / "memory").mkdir()
    monkeypatch.setattr(sld, "ROOT", tmp_path)
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["backup"]["ok"] is False
    att = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert "Chain backup patrol fired" in att and "did not load" in att


def test_run_cadence_refuses_stale_backup_chain(monkeypatch, tmp_path):
    # the mag-sovereign image bakes an Aug-25 backup_chain.py (no completeness check, no
    # 20261004 pin); run_cadence must refuse to run it and alarm instead
    _stub_backup(tmp_path, "CALLED = []\ndef backup(*, force=False):\n    raise SystemExit('stale backup ran')\n")
    monkeypatch.setattr(sld, "ROOT", tmp_path)
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["backup"]["ok"] is False and "stale backup_chain.py" in r["backup"]["error"]
    att = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert "Chain backup patrol fired" in att
