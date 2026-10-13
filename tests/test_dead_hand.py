"""Dead-hand watchdog tests — the trigger as code, before the operator's hand.

Contract: watch/inbox/SUCCESSION_CONTRACT_20260912.md Articles 3-5.
The drill (Article 5) will exercise this tool live; these tests are the
dry rehearsal. All filesystem effects are redirected to a tmp sandbox.
"""
from __future__ import annotations

import importlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

dead_hand = importlib.import_module("dead_hand")


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Redirect every writable surface into tmp; return (module, state_dir)."""
    state = tmp_path / "state"
    state.mkdir()
    monkeypatch.setattr(dead_hand, "STATE", state)
    monkeypatch.setattr(dead_hand, "STATE_PATH", state / "dead_hand_state.json")
    monkeypatch.setattr(dead_hand, "WITNESSES_PATH", state / "dead_hand_witnesses.json")
    monkeypatch.setattr(dead_hand, "HOLD_DIR", state / "hold_queue")
    # deterministic voice surfaces: ONLY the sandbox pulse (no real repo reads)
    monkeypatch.setattr(dead_hand, "VOICE_SURFACES",
                        [("operator_pulse", None, None)])
    monkeypatch.setattr(dead_hand, "_loud", lambda title, body: tmp_path / "loud.md")
    return dead_hand, state


def _pulse(state: Path, hours_ago: float):
    ts = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    (state / "operator_pulse.json").write_text(
        json.dumps({"ts": ts.isoformat(), "via": "test"}), encoding="utf-8"
    )


def _witnesses(state: Path, n: int, hours_ago: float = 1.0):
    ts = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    rows = [{"witness_id": f"w{i}", "ts": ts.isoformat(), "silence_confirmed": True}
            for i in range(n)]
    (state / "dead_hand_witnesses.json").write_text(json.dumps(rows), encoding="utf-8")


def _arm(dh, state: Path, interval: float = 72.0):
    st = dh._load_state()
    st.update(armed=True, armed_by="test", interval_hours=interval, status="WATCHING")
    dh._save_state(st)


def test_default_disarmed(sandbox):
    dh, state = sandbox
    r = dh.watch()
    assert "not armed" in r["action"]
    assert dh._load_state()["armed"] is False


def test_recent_word_holds_fire(sandbox):
    dh, state = sandbox
    _arm(dh, state, interval=72)
    _pulse(state, hours_ago=1.0)  # operator spoke 1h ago
    _witnesses(state, 2)
    r = dh.watch()
    assert r["action"].startswith("hold")
    assert dh._load_state()["status"] == "WATCHING"


def test_silence_without_witnesses_holds_fire(sandbox):
    dh, state = sandbox
    _arm(dh, state, interval=48)
    _pulse(state, hours_ago=72)  # long silent
    _witnesses(state, 1)          # but only one witness
    r = dh.watch()
    assert "witnesses below" in r["action"]
    assert dh._load_state()["status"] == "WATCHING"


def test_trigger_fires_seal_hold_loud(sandbox, tmp_path):
    dh, state = sandbox
    (tmp_path / "loud.md").unlink(missing_ok=True)
    monkey_card = tmp_path / "loud_card.md"
    monkey_card.unlink(missing_ok=True)
    _arm(dh, state, interval=48)
    _pulse(state, hours_ago=72)
    _witnesses(state, 2)
    r = dh.watch()
    act = r["action"]
    assert isinstance(act, dict), f"expected trigger, got {act}"
    assert "dead_hand_seal" in act["seal"]["seal"]
    assert act["seal"]["surfaces_hashed"] >= 1
    assert (state / "hold_queue" / "README.md").is_file()
    assert dh._load_state()["status"] == "TRIGGERED"


def test_revert_disarms_and_presents_hold_oldest_first(sandbox, tmp_path):
    dh, state = sandbox
    (state / "hold_queue").mkdir(parents=True)
    for name in ("b_second.md", "a_first.md"):
        (state / "hold_queue" / name).write_text("x", encoding="utf-8")
    r = dh.revert("i'm back")
    assert r["status"] == "REVERTED"
    assert r["hold_items_oldest_first"] == ["a_first.md", "b_second.md"]
    st = dh._load_state()
    assert st["armed"] is False  # revert disarms; re-arm is explicit
    assert st["status"] == "DISARMED"


def test_arm_refused_without_operator_attestation(sandbox, capsys):
    dh, state = sandbox
    sys.argv = ["dead_hand.py", "--arm", "--interval-h", "72"]
    rc = dh.main()
    assert rc == 2
    assert "REFUSED" in capsys.readouterr().out


def test_no_readable_voice_failsafe(sandbox):
    dh, state = sandbox
    _arm(dh, state)
    # no operator_pulse.json, no other surfaces in sandbox -> word_ts None
    _witnesses(state, 3)
    r = dh.watch()
    assert "fail-safe" in r["action"]


def test_steers_operator_authority_marker(tmp_path, monkeypatch):
    """Real row shape: authority starts 'operator' = his voice; FORGED rows excluded."""
    dh = importlib.import_module("dead_hand")
    steers = tmp_path / "steers.jsonl"
    now = datetime.now(timezone.utc)
    hour_ago = (now - timedelta(hours=1)).isoformat()
    day_ago = (now - timedelta(hours=24)).isoformat()
    steers.write_text("\n".join([
        json.dumps({"ts": day_ago, "authority": "operator (go)", "id": "s-1"}),
        json.dumps({"ts": hour_ago, "authority": "FORGED — no operator authorization", "id": "s-2"}),
        json.dumps({"ts": hour_ago, "authority": "seat", "id": "s-3"}),
    ]) + "\n", encoding="utf-8")
    monkeypatch.setattr(dh, "VOICE_SURFACES",
                        [("steers", steers, "steers_operator_authority")])
    ts, surface = dh.last_operator_word()
    assert surface == "steers"
    assert ts is not None and abs((now - ts).total_seconds() - 86400) < 120, (
        "FORGED and seat rows must not count; newest operator-authority row wins"
    )

