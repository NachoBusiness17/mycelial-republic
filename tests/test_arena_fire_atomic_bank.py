"""R6 regression guard (GAP_REGISTER 2026-10-10, lane a01-arena-cadence):
the carriers' FIRE-ATOMIC BANK - a fire's own sessions can never outlive
their bank overnight.

The mechanism landed 2026-10-04 (commit d349ce7d2, GO item 6): tools/tavern.py
and tools/dungeon.py bank their own run dir at exit, same process, right
after DONE. Dogfood evidence on disk at fill time (byte census 2026-10-10):
every post-fix fire banked 1.0-8.9 min after its dir stamp (33 dirs,
2026-10-04T10:00Z..2026-10-05T07:00Z) except one fail-open heal
(dnd0_20261004T100306Z: exit bank failed inside a succeeded 10:00Z fire,
healed by the 2026-10-05T07:12Z backfill) - and the pre-fix disease (the
2026-10-03 20:00Z trio whose bank never ran that night) is gone.

But NO test pinned the mechanism: the original defect was exactly "the
automation's bank step was a prompt instruction, not code" (the FIRE-ATOMIC
BANK comment in tools/dungeon.py) - unguarded code can drift back into that
class silently and the overnight-orphan bank returns. These tests pin the
law where it lives:

- live main() banks ITS OWN run dir at exit (tavern with a fully patched
  play loop; dungeon with a real init + one-row stub play, since the combat
  loop is not the unit under test here)
- --dry never banks (nothing was played, nothing is owed)
- a bank failure never fails the play run (fail-open by design: print,
  leave the dir for the next backfill)

SessionLedger is faked so the tests never append to the real
memory/runs/gwap/arena-capability.jsonl; arena_gwap.bank itself runs REAL
(transcript -> payloads -> GWAP_BANKED marker), so a refactor that breaks
the bank pipeline fails these tests too.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tools.arena_gwap  # noqa: E402
import tools.dungeon  # noqa: E402
import tools.hermes_burn as hb  # noqa: E402
import tools.tavern  # noqa: E402


class FakeLedger:
    """SessionLedger stand-in: records appends, never touches the real
    memory/runs/gwap ledger (bank() itself never reads ledger.path)."""

    def __init__(self, name="arena-capability"):
        self.name = name
        self.appends: list[dict] = []
        self._seq = 0

    def append(self, payload, ts_utc=None):
        self._seq += 1
        self.appends.append(payload)
        return {"seq": self._seq}

    def verify_chain(self):
        return (True, 0)


SCENARIO = {
    "title": "the fire-atomic bench",
    "kind": "tavern",
    "room": "a test bench under the playground",
    "objects": ["one sealed ledger"],
    "pressure": 0,
    "personas": [
        {"name": "asha", "model": "test/asha", "register": "quiet",
         "want": "a banked session", "secret": "none", "tell": "a pause",
         "escalation_threshold": 5},
        {"name": "bram", "model": "test/bram", "register": "loud",
         "want": "a DONE file", "secret": "none", "tell": "a shrug",
         "escalation_threshold": 5},
    ],
    "judge_model": "test/judge",
}

_JUDGE_JSON = json.dumps({"scores": {
    "asha": {"score": 0, "reason": "calm"},
    "bram": {"score": 0, "reason": "calm"}}})


def _fake_call(model, messages, max_tokens, key):
    user = messages[-1]["content"] if messages else ""
    content = _JUDGE_JSON if "Judge round" in user else \
        "[CLAIM the ledger] I claim this session banks itself."
    return {"usage": {"prompt_tokens": 3, "completion_tokens": 5},
            "choices": [{"message": {"content": content},
                         "finish_reason": "stop"}]}


@pytest.fixture
def tavern_env(tmp_path, monkeypatch):
    """Live-mode tavern with every paid surface patched to zero cost and the
    ledger faked; arena_gwap.bank stays real."""
    play = tmp_path / "playground"
    play.mkdir()
    ledgers: list[FakeLedger] = []

    def _make_ledger(name):
        led = FakeLedger(name)
        ledgers.append(led)
        return led

    monkeypatch.setattr(tools.tavern, "PLAY_DIR", play)
    monkeypatch.setattr(tools.tavern, "_hermes_key", lambda: "test-key")
    monkeypatch.setattr(tools.tavern, "_call", _fake_call)
    monkeypatch.setattr(tools.tavern, "_bank", lambda row: None)
    monkeypatch.setattr(hb, "PRICING",
                        {"test/asha": (0.0, 0.0), "test/bram": (0.0, 0.0),
                         "test/judge": (0.0, 0.0)})
    monkeypatch.setattr(tools.arena_gwap, "SessionLedger", _make_ledger)
    scen = tmp_path / "scenario.json"
    scen.write_text(json.dumps(SCENARIO), encoding="utf-8")
    return {"play": play, "scenario": str(scen), "ledgers": ledgers}


def _run_dirs(play: Path) -> list[Path]:
    return sorted(d for d in play.iterdir() if d.is_dir())


def test_tavern_live_banks_own_run_dir_at_exit(tavern_env, capsys):
    rc = tools.tavern.main(["--scenario", tavern_env["scenario"],
                            "--rounds", "1", "--budget-usd", "1"])
    out = capsys.readouterr().out
    assert rc == 0
    dirs = _run_dirs(tavern_env["play"])
    assert len(dirs) == 1, "one fire, one run dir"
    d = dirs[0]
    assert (d / "DONE").is_file(), "play finished"
    assert (d / "GWAP_BANKED").is_file(), "same-fire bank marker landed"
    seqs = (d / "GWAP_BANKED").read_text(encoding="utf-8").strip()
    assert "asha=" in seqs and "bram=" in seqs
    assert tavern_env["ledgers"], "the exit bank ran inside the same process"
    assert len(tavern_env["ledgers"][0].appends) >= 2
    assert "TAVERN: BANK OK" in out
    assert "CHAIN ok=True" in out


def test_tavern_dry_never_banks(tavern_env, capsys):
    rc = tools.tavern.main(["--scenario", tavern_env["scenario"],
                            "--rounds", "1", "--dry"])
    out = capsys.readouterr().out
    assert rc == 0
    assert not tavern_env["ledgers"], "dry runs owe no bank"
    for d in _run_dirs(tavern_env["play"]):
        assert not (d / "GWAP_BANKED").is_file()
    assert "TAVERN: BANK" not in out


def test_tavern_bank_failure_never_fails_the_play_run(
        tavern_env, monkeypatch, capsys):
    def _boom(run_dir, ledger, scene_to_model):
        raise RuntimeError("ledger locked by a concurrent process")

    monkeypatch.setattr(tools.arena_gwap, "bank", _boom)
    rc = tools.tavern.main(["--scenario", tavern_env["scenario"],
                            "--rounds", "1", "--budget-usd", "1"])
    out = capsys.readouterr().out
    assert rc == 0, "fail-open: the play run still succeeds"
    dirs = _run_dirs(tavern_env["play"])
    assert (dirs[0] / "DONE").is_file()
    assert not (dirs[0] / "GWAP_BANKED").is_file(), "dir left for backfill"
    assert "BANK FAILED" in out


def test_dungeon_live_banks_own_run_dir_at_exit(tmp_path, monkeypatch, capsys):
    play = tmp_path / "playground"
    play.mkdir()
    ledgers: list[FakeLedger] = []

    def _make_ledger(name):
        led = FakeLedger(name)
        ledgers.append(led)
        return led

    monkeypatch.setattr(tools.dungeon, "PLAY_DIR", play)
    monkeypatch.setattr(tools.dungeon, "_hermes_key", lambda: "test-key")
    monkeypatch.setattr(tools.arena_gwap, "SessionLedger", _make_ledger)

    class Session0Stub(tools.dungeon.Dungeon):
        """Real init (golden vectors, dir mint) + a one-beat play: the unit
        under test is main()'s exit-bank wiring, not the combat loop."""

        def play(self):
            self.row(scene="S1", turn=1, actor="saelis",
                     roll_committed=f"{self.tip}:S1:1:saelis",
                     roll_value=12, speech="[CHECK gate]",
                     verdict="SUCCESS (d20=12)")
            (self.dir / "DONE").write_text(
                '{"verdict": "STUB", "spend_usd": 0.0}\n', encoding="utf-8")

    monkeypatch.setattr(tools.dungeon, "Dungeon", Session0Stub)
    rc = tools.dungeon.main(["--tip", tools.dungeon.GENESIS,
                             "--budget-usd", "1"])
    out = capsys.readouterr().out
    assert rc == 0
    dirs = _run_dirs(play)
    assert len(dirs) == 1, "one fire, one run dir"
    d = dirs[0]
    assert d.name.startswith("dnd0_")
    assert (d / "DONE").is_file()
    assert (d / "GWAP_BANKED").is_file(), "same-fire bank marker landed"
    assert "saelis=" in (d / "GWAP_BANKED").read_text(encoding="utf-8")
    assert ledgers and ledgers[0].appends
    assert "DUNGEON: BANK OK" in out
    assert "CHAIN ok=True" in out
