"""Pins for tools/provider_error_tally.py against a synthetic CLI log."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import provider_error_tally  # noqa: E402

SESS = "sess_testsession"


def _line(ts, event, session, turn, attempt, extra_ctx=None, parent=None):
    ctx = {
        "providerId": "account:zai-individual-coding-plan",
        "modelId": "GLM-5.3-Flash",
        "querySource": "subagent",
        "attempt": attempt,
        "maxAttempts": 11,
    }
    if parent:
        ctx["parentSessionId"] = parent
    if extra_ctx:
        ctx.update(extra_ctx)
    return {
        "timestamp": ts,
        "level": "info" if event.endswith("completed") else "warn",
        "event": event,
        "sessionId": session,
        "turnId": turn,
        "status": "completed" if event.endswith("completed") else "failed",
        "context": ctx,
    }


def _write_log(path: Path) -> None:
    lines = [
        # plain clean completion, no absorption
        _line("2026-09-26T10:00:00Z", "model.network.completed", "sess_subagent_agent_a", "turn_1", 1, parent=SESS),
        # two absorbed failures then a completion on attempt 3, 429/1302 shaped
        _line(
            "2026-09-26T10:00:05Z",
            "model.network.failed",
            "sess_subagent_agent_a",
            "turn_2",
            1,
            {"statusCode": 429, "reason": "rate_limited", "statusMessage": "[1302][Rate limit reached][x1]"},
            parent=SESS,
        ),
        _line(
            "2026-09-26T10:00:08Z",
            "model.network.failed",
            "sess_subagent_agent_a",
            "turn_2",
            2,
            {"statusCode": 429, "reason": "rate_limited", "statusMessage": "[1302][Rate limit reached][x2]"},
            parent=SESS,
        ),
        _line("2026-09-26T10:00:20Z", "model.network.completed", "sess_subagent_agent_a", "turn_2", 3, parent=SESS),
        # a turn that fails and never completes: surfaced terminal failure
        _line(
            "2026-09-26T10:00:30Z",
            "model.network.failed",
            "sess_subagent_agent_b",
            "turn_3",
            1,
            {"statusCode": 503, "reason": "overloaded", "statusMessage": "no marker here", "maxAttempts": 0},
            parent=SESS,
        ),
        # other session family: must not count
        _line(
            "2026-09-26T10:00:40Z",
            "model.network.failed",
            "sess_other_subagent_agent_z",
            "turn_4",
            1,
            {"statusCode": 429, "reason": "rate_limited", "statusMessage": "[1302][Rate limit reached][x3]"},
            parent="sess_other",
        ),
        # unknown network event shape: counted as other, not as failure
        _line("2026-09-26T10:00:50Z", "model.network.started", "sess_subagent_agent_a", "turn_5", 1, parent=SESS),
        # child attributable only through parentSessionId
        _line(
            "2026-09-26T10:01:00Z",
            "model.network.completed",
            "sess_dwf_testrun-actor_1_1",
            "turn_6",
            1,
            {"querySource": "workflow_child", "maxAttempts": 0},
            parent=SESS,
        ),
    ]
    path.write_text("\n".join(json.dumps(l) for l in lines) + "\n", encoding="utf-8")


@pytest.fixture()
def env(tmp_path: Path):
    log = tmp_path / "zcode-2026-09-26.jsonl"
    _write_log(log)
    sess_dir = tmp_path / "agents" / SESS
    (sess_dir / "agent_a").mkdir(parents=True)
    (sess_dir / "agent_a" / "metadata.json").write_text(
        json.dumps({"agentId": "agent_a", "childSessionId": "sess_subagent_agent_a", "description": "B2-98 pin", "createdAt": "2026-09-26T10:00:00Z"}),
        encoding="utf-8",
    )
    return log, sess_dir


def test_counts_absorbed_surfaced_and_1302(env):
    log, sess_dir = env
    result = provider_error_tally.tally_session(SESS, [str(log)], session_dir=str(sess_dir))
    totals = result["totals"]
    assert totals["network_completed"] == 3  # turn_1, turn_2, dwf child via parent
    assert totals["network_failed_events"] == 3  # two absorbed + one terminal, other session excluded
    assert totals["absorbed_retries"] == 2  # turn_2 completed at attempt 3
    assert totals["terminal_failed_turns"] == 1  # turn_3 never completed
    assert totals["statusCode_counts"] == {"429": 2, "503": 1}
    assert totals["reason_counts"] == {"overloaded": 1, "rate_limited": 2}
    assert totals["count_1302_statusmessage"] == 2
    assert totals["other_network_events"] == 1  # model.network.started
    assert totals["maxAttempts_counts"] == {"0": 2, "11": 4}
    assert totals["querySource_counts"] == {"subagent": 5, "workflow_child": 1}


def test_per_agent_registry_join(env):
    log, sess_dir = env
    result = provider_error_tally.tally_session(SESS, [str(log)], session_dir=str(sess_dir))
    by_child = {row["childSessionId"]: row for row in result["per_agent"]}
    a = by_child["sess_subagent_agent_a"]
    assert a["description"] == "B2-98 pin"
    assert a["absorbed_retries"] == 2
    assert a["max_attempt_seen"] == 3
    assert a["terminal_failed_turns"] == 0
    b = by_child["sess_subagent_agent_b"]
    assert b["terminal_failed_turns"] == 1
    assert b["absorbed_retries"] == 0


def test_window_filter_and_cli_out(env, tmp_path: Path, capsys):
    log, sess_dir = env
    result = provider_error_tally.tally_session(
        SESS, [str(log)], session_dir=str(sess_dir), since="2026-09-26T10:00:30Z"
    )
    assert result["totals"]["network_failed_events"] == 1  # only the terminal turn_3 failure
    assert result["totals"]["network_completed"] == 1  # only the dwf child completion

    out = tmp_path / "tally.json"
    rc = provider_error_tally.main(
        ["--session", SESS, "--log", str(log), "--out", str(out), "--cli-root", str(tmp_path), "--quiet"]
    )
    assert rc == 0
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["session"] == SESS
    assert written["totals"]["count_1302_statusmessage"] == 2
    assert "provider_error_tally" not in capsys.readouterr().out.strip()  # quiet mode prints only the path
