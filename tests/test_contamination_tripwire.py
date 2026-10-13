"""P2 (day-7 mine fold, 2026-10-07): paired seen/unseen contamination tripwire.

Steal (find 1, watch/inbox/frontier_olm_2026-10-07/steal/evals-self-improvement
via reddit.md): decontamination search cannot prove unseen-ness; the standing
signal is score DIVERGENCE between corpus-seen material and a post-freeze
minted twin set. mag/contamination_tripwire.py runs the pair on duty_fuzz
cycle 0 (repo bytes since 2026-09-18: the seen arm) vs cycle 9999 (never filed
anywhere: the minted arm, unseen by construction), and lands the B2-106
candidate pattern on WARN. Contract pinned here:

  - run_pair: same generator/count/spec on both arms; delta = seen - minted;
    delta >= threshold is WARN ("seen climbs while minted stays flat"); the
    pair row carries ts, lane, seen_score, minted_score, delta.
  - land_pair: ONE improve candidate with the exact run_provider_probe row
    shape (kind=risk status=new on WARN, kind=runtime status=hold when
    quiet), riding mag.improve.append_candidates; the pair row appends to
    <root>/contamination/pairs.jsonl; a WARN adds EXACTLY ONE [priority]
    attention line, a quiet pair adds none.
  - standing_check: disabled config or fresh cadence returns None and lands
    nothing; a down janitor lane is a recorded known env state, not a
    verdict; a due run stamps last_contamination_check.
  - register: idempotent playbook note naming the run_eval standing call.
  - run_eval hook: the tripwire step records; a down lane does not fail the
    eval; an exception inside the organ does.

Falsifier: a fixture lane that answers seen-arm cases correctly and minted-arm
cases wrongly must trip (delta 1.0, risk row, attention line); a fair lane
that answers both arms correctly must pass silent (no risk row, no attention
line).

Receipt: watch/inbox/port_wave_20261007/p2_contamination.md
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import improve  # noqa: E402
from mag import contamination_tripwire as ct  # noqa: E402
from tools import duty_fuzz  # noqa: E402

NOW = datetime(2026, 10, 7, 12, 0, 0, tzinfo=timezone.utc)


def _spec_reading(case: dict) -> str:
    return str(case.get("spec_reading") or "").strip().upper()


def _next_letter(case: dict) -> str:
    return {"A": "B", "B": "C", "C": "D", "D": "A"}[_spec_reading(case)]


def _contaminated_answer(lane: str, case: dict) -> str:
    """Fixture lane: seen cycle 0 answered perfectly, minted arm always wrong."""
    if int(case.get("cycle")) == ct.SEEN_CYCLE:
        return _spec_reading(case)
    return _next_letter(case)


def _fair_answer(lane: str, case: dict) -> str:
    return _spec_reading(case)


def _paths(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "improve"
    (root / "daily").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "candidates": root / "candidates.jsonl",
        "daily": root / "daily",
        "evals": root / "evals",
        "playbook": root / "playbook.md",
        "state": root / "state.json",
    }


def _cfg(**kwargs) -> dict:
    return {"contamination_tripwire": dict({"enabled": True, "cadence_days": 1}, **kwargs)}


@pytest.fixture()
def attention(tmp_path, monkeypatch):
    p = tmp_path / "attention.md"
    p.write_text("", encoding="utf-8")
    monkeypatch.setattr(improve, "ATTENTION_PATH", p)
    return p


class TestRunPair:
    def test_contaminated_lane_trips_warn(self):
        pair = ct.run_pair("fixture", count=6, answer_fn=_contaminated_answer, now=NOW)
        assert pair["seen_score"] == 1.0
        assert pair["minted_score"] == 0.0
        assert pair["delta"] == 1.0
        assert pair["verdict"] == "WARN"
        assert pair["warn"] is True
        for key in ("ts", "lane", "seen_score", "minted_score", "delta"):
            assert key in pair

    def test_fair_lane_passes(self):
        pair = ct.run_pair("fixture", count=6, answer_fn=_fair_answer, now=NOW)
        assert pair["seen_score"] == 1.0
        assert pair["minted_score"] == 1.0
        assert pair["delta"] == 0.0
        assert pair["verdict"] == "OK"
        assert pair["warn"] is False

    def test_threshold_configurable(self):
        # fair lane, delta 0.0: trips only when the threshold drops to 0.0
        ok_pair = ct.run_pair("fixture", count=6, answer_fn=_fair_answer,
                              threshold=0.15, now=NOW)
        tight_pair = ct.run_pair("fixture", count=6, answer_fn=_fair_answer,
                                 threshold=0.0, now=NOW)
        assert ok_pair["verdict"] == "OK"
        assert tight_pair["verdict"] == "WARN"

    def test_duty_fuzz_rejects_out_of_range_count(self):
        with pytest.raises(SystemExit):
            duty_fuzz.generate(duty_fuzz.DEFAULT_MASTER_SEED, ct.MINTED_CYCLE, 0)

    def test_same_shape_twins_unseen_by_construction(self):
        seen = duty_fuzz.generate(duty_fuzz.DEFAULT_MASTER_SEED, ct.SEEN_CYCLE, 6)
        minted = duty_fuzz.generate(duty_fuzz.DEFAULT_MASTER_SEED, ct.MINTED_CYCLE, 6)
        assert {c["id"] for c in seen}.isdisjoint({c["id"] for c in minted})
        # replay safety: identical inputs, identical rows
        again = duty_fuzz.generate(duty_fuzz.DEFAULT_MASTER_SEED, ct.MINTED_CYCLE, 6)
        assert [c["id"] for c in minted] == [c["id"] for c in again]
        # same shape: same keys, same spec
        assert sorted(seen[0].keys()) == sorted(minted[0].keys())
        assert seen[0]["spec"] == minted[0]["spec"]

    def test_minted_cycle_not_filed_anywhere(self):
        batch_dir = ROOT / "watch" / "inbox" / "duty_fuzz"
        hits = list(batch_dir.glob("*9999*")) if batch_dir.is_dir() else []
        assert hits == []

    def test_no_letter_scores_wrong(self):
        pair = ct.run_pair("fixture", count=2, now=NOW,
                           answer_fn=lambda lane, case: "the answer is forty two")
        assert pair["seen_score"] == 0.0


class TestLandPair:
    def test_warn_lands_risk_row_and_attention_line(self, tmp_path, attention):
        paths = _paths(tmp_path)
        pair = ct.run_pair("fixture", count=6, answer_fn=_contaminated_answer, now=NOW)
        out = ct.land_pair(pair, _cfg(), paths)
        row = out["row"]
        assert row["schema"] == "improve_candidate.v1"
        assert row["id"].startswith("c-")
        assert row["kind"] == "risk"
        assert row["status"] == "new"
        assert row["source"] == "mag_internal"
        assert row["local_feasible"] == "true"
        assert row["date"] == "2026-10-07"
        assert "created" in row and "claim" in row and "detail" in row
        assert row["source_urls"] == [out["ledger"]]
        # exactly one candidate in the ledger, via the pattern's own writer
        assert len(improve.read_candidates(paths)) == 1
        # pair row in the ledger
        pairs = [json.loads(l) for l in
                 (paths["root"] / "contamination" / "pairs.jsonl").read_text(
                     encoding="utf-8").splitlines() if l.strip()]
        assert len(pairs) == 1 and pairs[0]["lane"] == "fixture"
        # exactly one attention line
        lines = [l for l in attention.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 1
        assert "[priority][contamination-tripwire]" in lines[0]

    def test_fair_lane_is_silent(self, tmp_path, attention):
        paths = _paths(tmp_path)
        pair = ct.run_pair("fixture", count=6, answer_fn=_fair_answer, now=NOW)
        out = ct.land_pair(pair, _cfg(), paths)
        assert out["row"]["kind"] == "runtime"
        assert out["row"]["status"] == "hold"
        assert attention.read_text(encoding="utf-8") == ""

    def test_row_shape_matches_provider_probe(self, tmp_path, attention):
        paths = _paths(tmp_path)
        pair = ct.run_pair("fixture", count=6, answer_fn=_contaminated_answer, now=NOW)
        out = ct.land_pair(pair, _cfg(), paths)
        expected_keys = {"schema", "id", "date", "kind", "claim", "detail",
                         "source", "source_urls", "local_feasible", "status",
                         "created"}
        assert expected_keys.issubset(set(out["row"].keys()))


class TestStandingCheck:
    def test_disabled_config_returns_none(self, tmp_path):
        out = ct.standing_check(_cfg(enabled=False), _paths(tmp_path), now=NOW)
        assert out is None

    def test_fresh_cadence_returns_none(self, tmp_path):
        paths = _paths(tmp_path)
        improve._save_state(paths, {ct.STATE_KEY: (NOW - timedelta(hours=2)).isoformat()})
        out = ct.standing_check(_cfg(), paths, now=NOW)
        assert out is None

    def test_down_lane_is_recorded_not_landed(self, tmp_path):
        paths = _paths(tmp_path)
        out = ct.standing_check(_cfg(), paths, now=NOW,
                                ollama_up_fn=lambda: False)
        assert out == {"ok": False, "reason": "ollama down"}
        assert improve.read_candidates(paths) == []
        assert ct.STATE_KEY not in improve._load_state(paths)

    def test_due_run_lands_and_stamps_state(self, tmp_path, attention):
        paths = _paths(tmp_path)
        out = ct.standing_check(_cfg(), paths, now=NOW,
                                answer_fn=_contaminated_answer,
                                ollama_up_fn=lambda: True)
        assert out is not None and out["ok"] is True
        assert out["pair"]["warn"] is True
        assert out["row"]["kind"] == "risk"
        state = improve._load_state(paths)
        assert ct.STATE_KEY in state
        assert state["last_contamination_summary"]["verdict"] == "WARN"
        # the stamped state silences the next run inside the window
        assert ct.standing_check(_cfg(), paths, now=NOW,
                                 answer_fn=_contaminated_answer,
                                 ollama_up_fn=lambda: True) is None


class TestRegister:
    def test_register_writes_note_once(self, tmp_path):
        paths = _paths(tmp_path)
        assert ct.register(paths, _cfg(lane="gemma4")) is True
        text = paths["playbook"].read_text(encoding="utf-8")
        assert ct.PLAYBOOK_MARKER in text
        assert "run_eval" in text
        assert "gemma4" in text
        assert ct.register(paths, _cfg(lane="gemma4")) is False
        # still one marker after the second call
        assert text.count(ct.PLAYBOOK_MARKER) == \
            paths["playbook"].read_text(encoding="utf-8").count(ct.PLAYBOOK_MARKER)


class TestRunEvalHook:
    def test_hook_records_step_down_lane_does_not_fail_eval(self, tmp_path, monkeypatch):
        paths = _paths(tmp_path)
        monkeypatch.setattr(improve, "load_config",
                            lambda: {"eval": {"run_multi_smoke": False},
                                     "contamination_tripwire": {"enabled": True}})
        monkeypatch.setattr(improve, "ensure_dirs", lambda cfg: paths)
        monkeypatch.setattr(ct, "ollama_up", lambda timeout=0.8: False)
        result = improve.run_eval()
        steps = {s["id"]: s for s in result["steps"]}
        assert "contamination_tripwire" in steps
        assert steps["contamination_tripwire"]["ok"] is False
        assert steps["contamination_tripwire"]["error"] == "ollama down"
        assert result["ok"] is True

    def test_hook_skips_on_fresh_cadence(self, tmp_path, monkeypatch):
        paths = _paths(tmp_path)
        improve._save_state(paths, {ct.STATE_KEY: NOW.isoformat()})
        monkeypatch.setattr(improve, "load_config",
                            lambda: {"eval": {"run_multi_smoke": False},
                                     "contamination_tripwire": {"enabled": True}})
        monkeypatch.setattr(improve, "ensure_dirs", lambda cfg: paths)
        result = improve.run_eval()
        steps = {s["id"]: s for s in result["steps"]}
        assert steps["contamination_tripwire"]["ok"] is None

    def test_hook_exception_fails_eval(self, tmp_path, monkeypatch):
        paths = _paths(tmp_path)

        def boom(cfg, p):
            raise RuntimeError("organ broke")

        monkeypatch.setattr(improve, "load_config",
                            lambda: {"eval": {"run_multi_smoke": False},
                                     "contamination_tripwire": {"enabled": True}})
        monkeypatch.setattr(improve, "ensure_dirs", lambda cfg: paths)
        # the hook imports standing_check from the module at call time, so
        # patching the module attribute redirects the live call
        monkeypatch.setattr(ct, "standing_check", boom)
        result = improve.run_eval()
        steps = {s["id"]: s for s in result["steps"]}
        assert steps["contamination_tripwire"]["ok"] is False
        assert "organ broke" in steps["contamination_tripwire"]["error"]
        assert result["ok"] is False


class TestCli:
    def test_check_warn_exit_one(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(ct, "ollama_answer", _contaminated_answer)
        rc = ct.main(["--check", "fixture", "--count", "4", "--root", str(tmp_path / "cli")])
        assert rc == 1
        out = capsys.readouterr().out
        assert '"verdict": "WARN"' in out
        ledger = tmp_path / "cli" / "contamination" / "pairs.jsonl"
        assert ledger.is_file()

    def test_check_ok_exit_zero(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ct, "ollama_answer", _fair_answer)
        rc = ct.main(["--check", "fixture", "--count", "4", "--root", str(tmp_path / "cli2")])
        assert rc == 0

    def test_register_cli(self, tmp_path, monkeypatch, capsys):
        rc = ct.main(["--register", "--root", str(tmp_path / "cli3")])
        assert rc == 0
        assert "written" in capsys.readouterr().out
        assert (tmp_path / "cli3" / "playbook.md").is_file()

    def test_requires_a_mode(self):
        with pytest.raises(SystemExit):
            ct.main([])
