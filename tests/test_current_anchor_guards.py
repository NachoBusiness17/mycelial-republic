"""AG6 guards (audit finding #5, 2026-09-29): CURRENT scratch routing + ANCHOR staleness refusal.

Two diseases, two guards, same receipt (watch/inbox/last_mile_20260930/AG6_CURRENT_GUARD.md):

1. The gala old-files probe ran escalate_grok_node against a fake harness and
   its "probe run (fake harness)" stub became the LIVE brief in
   state/CURRENT.md. Guard: MAG_CURRENT_SCRATCH=1 routes every
   audit.sync_current write to state/CURRENT.scratch.md; production writers
   (which set nothing) keep CURRENT.md.
2. memory/plans/ANCHOR.md carried a 2026-08-03 Status block injected into
   EVERY agent session. Guard: _anchor_injection refuses anchors whose
   "## Status YYYY-MM-DD" stamp is older than PACK_STALE_DAYS (7) — or that
   carry no stamp — and injects a loud ANCHOR-STALE marker + one router log
   line instead. Anchor content refresh stays an operator call.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

import pytest

import audit
import config
from mag import agent_cli


@pytest.fixture(autouse=True)
def _isolate_current(tmp_path, monkeypatch):
    """Point the CURRENT contract at tmp so these tests never touch the real one."""
    state = tmp_path / "state"
    state.mkdir(parents=True, exist_ok=True)
    prod = state / "CURRENT.md"
    monkeypatch.setattr(config, "STATE_DIR", state)
    monkeypatch.setattr(config, "CURRENT_MD", prod)
    monkeypatch.setattr(audit, "CURRENT_MD", prod)
    # scratch routing fires a router log line — capture instead of writing logs/
    events: list[dict] = []
    monkeypatch.setattr(audit, "log_event", lambda ev: events.append(ev))
    yield {"prod": prod, "scratch": state / "CURRENT.scratch.md", "events": events}


# --- guard 1: scratch routing -------------------------------------------------


def test_scratch_env_routes_probe_writes_off_the_live_brief(monkeypatch):
    prod = config.CURRENT_MD
    scratch = config.STATE_DIR / "CURRENT.scratch.md"
    monkeypatch.setenv("MAG_CURRENT_SCRATCH", "1")
    assert config.current_md() == scratch
    assert audit._current_target() == scratch

    audit.sync_current(
        {
            "status": "escalated_grok_ran",
            "tier": "T3",
            "goal": "old-files probe",
            "last_result": "Grok harness ran: probe run (fake harness)",
        }
    )

    # the stub landed in scratch, never in the live brief
    assert scratch.is_file()
    assert "probe run (fake harness)" in scratch.read_text(encoding="utf-8")
    assert not prod.exists()


def test_scratch_log_event_fires(_isolate_current, monkeypatch):
    monkeypatch.setenv("MAG_CURRENT_SCRATCH", "1")
    audit.sync_current({"status": "probe", "goal": "g"})
    routed = [e for e in _isolate_current["events"] if e.get("event") == "current-scratch-write"]
    assert routed and "CURRENT.scratch.md" in routed[0]["path"]


def test_production_writers_keep_current_md(_isolate_current, monkeypatch):
    monkeypatch.delenv("MAG_CURRENT_SCRATCH", raising=False)
    assert config.current_md() == _isolate_current["prod"]
    audit.sync_current({"status": "running", "goal": "prod goal"})
    prod = _isolate_current["prod"]
    assert prod.is_file()
    assert "prod goal" in prod.read_text(encoding="utf-8")
    assert not _isolate_current["scratch"].exists()
    # production writes log nothing new (same silent contract as before AG6)
    assert not _isolate_current["events"]


def test_explicit_override_wins_when_no_scratch_env(_isolate_current, monkeypatch):
    """The pre-AG6 test-redirection seam (audit.CURRENT_MD override) still works."""
    monkeypatch.delenv("MAG_CURRENT_SCRATCH", raising=False)
    override = config.STATE_DIR / "OVERRIDE.md"
    monkeypatch.setattr(audit, "CURRENT_MD", override)
    audit.sync_current({"status": "running", "goal": "override goal"})
    assert override.is_file() and "override goal" in override.read_text(encoding="utf-8")


# --- guard 2: ANCHOR staleness refusal ----------------------------------------


@pytest.fixture
def anchor_env(tmp_path, monkeypatch):
    """Route MAG_ANCHORED_PLAN at a fixture file + capture the router log."""
    events: list[dict] = []
    monkeypatch.setattr(audit, "log_event", lambda ev: events.append(ev))

    def _anchor(status_line: str | None):
        p = tmp_path / "ANCHOR.md"
        body = "# Anchored plan (fixture)\n\n## Goal\nfixture goal\n"
        if status_line is not None:
            body += f"\n{status_line}\n- fixture status bullet\n"
        p.write_text(body, encoding="utf-8")
        monkeypatch.setenv("MAG_ANCHORED_PLAN", str(p))
        monkeypatch.setattr(agent_cli, "_anchor_stale_logged", False)
        return p, events

    return _anchor


def _prompt() -> str:
    return agent_cli._system_prompt("pack text", goal="g")


def test_fresh_anchor_injects(anchor_env):
    today = date.today().isoformat()
    _p, events = anchor_env(f"## Status {today}")
    prompt = _prompt()
    assert "## Anchored plan (survives repack - re-read before acting)" in prompt
    assert "fixture goal" in prompt
    assert "ANCHOR-STALE" not in prompt
    assert not [e for e in events if e.get("event") == "ANCHOR-STALE"]


def test_stale_anchor_refused_with_fixture(anchor_env):
    stale_date = (date.today() - timedelta(days=57)).isoformat()  # 2026-08-03 shape
    p, events = anchor_env(f"## Status {stale_date}")
    prompt = _prompt()
    # refused: the anchored-plan header and content are NOT injected
    assert "## Anchored plan (survives repack" not in prompt
    assert "fixture goal" not in prompt
    # loud instead: ANCHOR-STALE <days> marker names the age and the file
    m = re.search(r"ANCHOR-STALE (\d+)", prompt)
    assert m and int(m.group(1)) == 57
    assert str(p) in prompt
    assert "operator call" in prompt
    # exactly one router log line, not one per provider call
    stale_events = [e for e in events if e.get("event") == "ANCHOR-STALE"]
    assert len(stale_events) == 1 and stale_events[0]["days"] == 57
    _prompt()
    _prompt()
    assert len([e for e in events if e.get("event") == "ANCHOR-STALE"]) == 1
    assert agent_cli._anchor_stale_logged is True


def test_unstamped_anchor_refused_as_minus_one(anchor_env):
    p, events = anchor_env(None)  # no '## Status <date>' line at all
    prompt = _prompt()
    assert "## Anchored plan (survives repack" not in prompt
    assert "ANCHOR-STALE -1" in prompt
    assert [e for e in events if e.get("event") == "ANCHOR-STALE"][0]["days"] is None


def test_anchor_age_days_parser():
    text = "# plan\n\n## Status 2026-08-03\n- bullet\n"
    age = agent_cli._anchor_age_days(text)
    assert age == (date.today() - date(2026, 8, 3)).days
    assert agent_cli._anchor_age_days("# no status header\n") is None
