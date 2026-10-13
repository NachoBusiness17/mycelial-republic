"""B2-106: pinned contract for the provider-health cadence (mag/improve.py).

Lane state used to be measured only during burn waves: the B2-04 morning
scoreboard was stale by the afternoon, when mistral flipped from the
429-zero-quota shape (x-ratelimit limits literally 0) to 403-wrong-default
(tier_not_allowed on the stale default id). The improve scout now owns the
cadence: the first non-dry scout that finds state["last_provider_probe"]
older than configs/improve.yaml provider_probe.cadence_days runs
mag.doctor.check_provider_endpoints() under MAG_PROBE_REMOTE=1, the B2-04
deep probe (ONE one-token ping per deduped (base_url, model, key) triple).
Contract pinned here:

  - provider_probe_due: missing/empty/unparseable ts is DUE (a broken
    clock must not silence the probe forever); a fresh ISO ts inside the
    window is not due; a naive ts is treated as UTC; cadence_days <= 0 is
    always due (operator knob, not a footgun).
  - run_provider_probe: disabled config and fresh cadence return None and
    never touch the probe; a due run sets MAG_PROBE_REMOTE=1 for the call
    and restores the prior env after (removed when it was absent, kept
    when the caller had set it); the snapshot lands under
    <root>/provider_health/<day>.json with the full result; ONE candidate
    row lands with kind=risk status=new on alarm issues and kind=runtime
    status=hold on a quiet week (evidence, not a ticket); the state key
    is stamped so the next scout inside the window skips.

Falsifier: with a state ts 8 days old, run_provider_probe must call the
probe exactly once with MAG_PROBE_REMOTE=1 visible inside the call, and a
second call with the freshly stamped state must be a no-op returning None.

Receipt: watch/inbox/burn_wave_20260926/B2_106_probe_cadence_20260926.md.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import improve  # noqa: E402

NOW = datetime(2026, 9, 26, 12, 0, 0, tzinfo=timezone.utc)

ALARM_RESULT = {
    "check": "provider_endpoints",
    "ok": False,
    "statuses": {"cerebras": "QUOTA-DEAD", "groq": "ALIVE", "mistral": "DOWN",
                 "z_ai2": "DEGRADED", "z_ai": "FENCED", "nvidia": "REMOTE-UNVERIFIED"},
    "providers": [],
    "issues": [
        "PROVIDER QUOTA DEAD: 'cerebras' https://api.cerebras.ai/v1 (chat 402)",
        "PROVIDER ENDPOINT DOWN: 'mistral' https://api.mistral.ai/v1 (chat 403)",
    ],
    "unverified": ["nvidia"],
    "degraded": ["z_ai2"],
    "fenced": ["z_ai"],
    "probes_run": 15,
}

QUIET_RESULT = dict(ALARM_RESULT, ok=True, issues=[], statuses={"groq": "ALIVE"},
                    unverified=[], degraded=[], fenced=[], probes_run=15)


def _paths(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "improve"
    return {"root": root, "state": root / "state.json", "candidates": root / "candidates.jsonl"}


def _cfg(**probe_kwargs) -> dict:
    return {"provider_probe": dict({"enabled": True, "cadence_days": 7}, **probe_kwargs)}


class TestProviderProbeDue:
    def test_missing_state_key_is_due(self):
        assert improve.provider_probe_due({}, 7, now=NOW) is True
        assert improve.provider_probe_due(None, 7, now=NOW) is True

    def test_fresh_ts_not_due(self):
        state = {improve._PROVIDER_PROBE_STATE_KEY: (NOW - timedelta(days=3)).isoformat()}
        assert improve.provider_probe_due(state, 7, now=NOW) is False

    def test_stale_ts_due(self):
        state = {improve._PROVIDER_PROBE_STATE_KEY: (NOW - timedelta(days=8)).isoformat()}
        assert improve.provider_probe_due(state, 7, now=NOW) is True

    def test_boundary_exactly_cadence_days_is_due(self):
        state = {improve._PROVIDER_PROBE_STATE_KEY: (NOW - timedelta(days=7)).isoformat()}
        assert improve.provider_probe_due(state, 7, now=NOW) is True

    def test_garbage_ts_is_due_never_silenced(self):
        state = {improve._PROVIDER_PROBE_STATE_KEY: "not-a-timestamp"}
        assert improve.provider_probe_due(state, 7, now=NOW) is True

    def test_naive_ts_treated_as_utc(self):
        naive = (NOW - timedelta(days=1)).replace(tzinfo=None).isoformat()
        state = {improve._PROVIDER_PROBE_STATE_KEY: naive}
        assert improve.provider_probe_due(state, 7, now=NOW) is False

    def test_zero_or_negative_cadence_always_due(self):
        state = {improve._PROVIDER_PROBE_STATE_KEY: NOW.isoformat()}
        assert improve.provider_probe_due(state, 0, now=NOW) is True
        assert improve.provider_probe_due(state, -1, now=NOW) is True


class TestRunProviderProbe:
    def test_disabled_config_never_probes(self, tmp_path):
        calls = []
        out = improve.run_provider_probe(
            _cfg(enabled=False), _paths(tmp_path), day="2026-09-26", now=NOW,
            probe_fn=lambda: calls.append(1),
        )
        assert out is None
        assert calls == []

    def test_fresh_cadence_never_probes(self, tmp_path):
        calls = []
        paths = _paths(tmp_path)
        paths["root"].mkdir(parents=True)
        paths["state"].write_text(json.dumps(
            {improve._PROVIDER_PROBE_STATE_KEY: (NOW - timedelta(days=1)).isoformat()}))
        out = improve.run_provider_probe(
            _cfg(), paths, day="2026-09-26", now=NOW, probe_fn=lambda: calls.append(1),
        )
        assert out is None
        assert calls == []

    def test_due_run_probes_once_env_hygiene_snapshot_and_row(self, tmp_path):
        seen_env = []
        calls = []

        def probe_fn():
            seen_env.append(os.environ.get("MAG_PROBE_REMOTE"))
            calls.append(1)
            return ALARM_RESULT

        os.environ.pop("MAG_PROBE_REMOTE", None)
        try:
            out = improve.run_provider_probe(
                _cfg(), _paths(tmp_path), day="2026-09-26", now=NOW, probe_fn=probe_fn,
            )
            assert calls == [1]
            assert seen_env == ["1"], "MAG_PROBE_REMOTE=1 must be set for the call"
            assert os.environ.get("MAG_PROBE_REMOTE") is None, "env must be restored (removed)"
        finally:
            os.environ.pop("MAG_PROBE_REMOTE", None)

        snap = tmp_path / "improve" / "provider_health" / "2026-09-26.json"
        assert snap.is_file()
        payload = json.loads(snap.read_text(encoding="utf-8"))
        assert payload["result"]["probes_run"] == 15

        rows = [json.loads(l) for l in
                (tmp_path / "improve" / "candidates.jsonl").read_text(encoding="utf-8").splitlines()]
        probe_rows = [r for r in rows if r["date"] == "2026-09-26" and "Provider probe" in r["claim"]]
        assert len(probe_rows) == 1
        row = probe_rows[0]
        assert row["kind"] == "risk"
        assert row["status"] == "new"
        assert "cerebras" in row["claim"]
        assert "groq=ALIVE" in row["detail"]

        state = json.loads(paths_state(tmp_path).read_text(encoding="utf-8"))
        assert improve._PROVIDER_PROBE_STATE_KEY in state
        assert state["last_provider_probe_summary"]["probes_run"] == 15

        assert out is not None and out["row"]["id"] == row["id"]

    def test_quiet_week_is_runtime_hold_evidence_not_ticket(self, tmp_path):
        out = improve.run_provider_probe(
            _cfg(), _paths(tmp_path), day="2026-09-26", now=NOW, probe_fn=lambda: QUIET_RESULT,
        )
        assert out is not None
        assert out["row"]["kind"] == "runtime"
        assert out["row"]["status"] == "hold"

    def test_prior_env_value_preserved_and_restored(self, tmp_path):
        os.environ["MAG_PROBE_REMOTE"] = "0"
        try:
            improve.run_provider_probe(
                _cfg(), _paths(tmp_path), day="2026-09-26", now=NOW,
                probe_fn=lambda: ALARM_RESULT,
            )
            assert os.environ.get("MAG_PROBE_REMOTE") == "0"
        finally:
            os.environ.pop("MAG_PROBE_REMOTE", None)

    def test_second_call_after_stamp_is_noop(self, tmp_path):
        calls = []

        def probe_fn():
            calls.append(1)
            return ALARM_RESULT

        paths = _paths(tmp_path)
        improve.run_provider_probe(_cfg(), paths, day="2026-09-26", now=NOW, probe_fn=probe_fn)
        out2 = improve.run_provider_probe(_cfg(), paths, day="2026-09-26", now=NOW, probe_fn=probe_fn)
        assert len(calls) == 1, "cadence gate must hold inside the window"
        assert out2 is None

    def test_probe_fn_exception_still_restores_env(self, tmp_path):
        os.environ.pop("MAG_PROBE_REMOTE", None)
        try:
            def boom():
                raise RuntimeError("lane down")

            with pytest.raises(RuntimeError):
                improve.run_provider_probe(
                    _cfg(), _paths(tmp_path), day="2026-09-26", now=NOW, probe_fn=boom,
                )
            assert os.environ.get("MAG_PROBE_REMOTE") is None
        finally:
            os.environ.pop("MAG_PROBE_REMOTE", None)


def paths_state(tmp_path: Path) -> Path:
    return tmp_path / "improve" / "state.json"


class TestAlarmSurfaceB2_494:
    def test_alarm_run_gains_exactly_one_priority_line(self, tmp_path, monkeypatch):
        attention = tmp_path / "attention.md"
        attention.write_text("", encoding="utf-8")
        monkeypatch.setattr(improve, "ATTENTION_PATH", attention)
        paths = _paths(tmp_path)
        out = improve.run_provider_probe(
            _cfg(), paths, day="2026-09-26", now=NOW,
            probe_fn=lambda: ALARM_RESULT)
        assert out is not None and out["row"]["kind"] == "risk"
        lines = [l for l in attention.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 1, lines
        assert "[priority][probe-alarm]" in lines[0]
        assert "provider_probe" in lines[0]
        assert "DOWN" in lines[0] and "QUOTA-DEAD" in lines[0]
        assert "provider_health/2026-09-26.json" in lines[0]

    def test_quiet_run_gains_nothing(self, tmp_path, monkeypatch):
        attention = tmp_path / "attention.md"
        attention.write_text("", encoding="utf-8")
        monkeypatch.setattr(improve, "ATTENTION_PATH", attention)
        paths = _paths(tmp_path)
        out = improve.run_provider_probe(
            _cfg(), paths, day="2026-09-26", now=NOW,
            probe_fn=lambda: QUIET_RESULT)
        assert out is not None and out["row"]["kind"] == "runtime"
        assert attention.read_text(encoding="utf-8") == ""

    def test_attention_write_failure_never_breaks_the_probe(self, tmp_path, monkeypatch):
        class Bursty:
            def open(self, *a, **k):
                raise OSError("disk full")
        monkeypatch.setattr(improve, "ATTENTION_PATH", Bursty())
        paths = _paths(tmp_path)
        out = improve.run_provider_probe(
            _cfg(), paths, day="2026-09-26", now=NOW,
            probe_fn=lambda: ALARM_RESULT)
        assert out is not None and out["row"]["kind"] == "risk"
