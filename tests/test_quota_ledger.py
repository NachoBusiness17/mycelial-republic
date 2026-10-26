"""tests/test_quota_ledger.py — fixture-estate tests for the window-quota
ledger (tools/quota_ledger.py, 2026-09-30).

The law under test: lane fires are read from harness bytes (subagent
metadata createdAt/usage), wall moments are clusters of 1302/1308-coded
deaths with the 1308 reset time parsed verbatim from the payload, token
numbers separate recorded bytes from extrapolation, and the verdict shape
follows the measured envelopes (8-12 green, ~15 first 1302s, 19+ red) —
never a vibe.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import quota_ledger as ql  # noqa: E402

DAY = "2026-09-30"


def _write_fire(agents_root: Path, session: str, agent: str, *, created: str,
                completed: str | None = None, status: str = "completed",
                tokens: int | None = 1000, output: str = "", mtime=None) -> Path:
    d = agents_root / session / agent
    d.mkdir(parents=True)
    meta = {
        "agentId": agent,
        "createdAt": created,
        "completedAt": completed,
        "updatedAt": completed,
        "parentSessionId": session,
        "description": agent.replace("agent_", "").replace("-", " "),
        "status": status,
    }
    if tokens is not None:
        meta["usage"] = {"inputTokens": tokens - 10, "outputTokens": 10,
                         "totalTokens": tokens}
    (d / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    (d / "output.txt").write_text(output, encoding="utf-8")
    if mtime is not None:
        os.utime(d, (mtime, mtime))
    return d


def _fake_agents(tmp_path: Path) -> Path:
    root = tmp_path / "agents"
    # session mtime inside the day window so the prefilter keeps it
    now = datetime.now(timezone.utc).timestamp()
    os.utime(root, (now, now)) if root.exists() else None
    return root


def test_load_fires_filters_to_day_and_reads_usage(tmp_path):
    agents = tmp_path / "agents"
    _write_fire(agents, "sess_a", "agent_1", created="2026-09-30T01:00:00Z",
                completed="2026-09-30T01:05:00Z", tokens=5000)
    _write_fire(agents, "sess_a", "agent_2", created="2026-09-29T23:00:00Z",
                completed="2026-09-29T23:05:00Z")
    # prefilter: session dir mtime must be >= day-1
    now = datetime.now(timezone.utc).timestamp()
    os.utime(agents / "sess_a", (now, now))
    fires = ql.load_fires(agents, DAY)
    assert [f.lane for f in fires] == ["1"]
    assert fires[0].tokens == 5000
    assert fires[0].ts == datetime(2026, 9, 30, 1, 0, tzinfo=timezone.utc)


def test_wall_payload_parses_code_reset_and_provider_stamp(tmp_path):
    agents = tmp_path / "agents"
    out = ("[1308][Usage limit reached for 5 hour. "
           "Your limit will reset at 2026-09-30 20:54:52]"
           "[202609302013252ffd3407af7d46b2]")
    _write_fire(agents, "sess_a", "agent_dead", created="2026-09-30T12:00:33Z",
                completed="2026-09-30T12:13:28Z", status="failed",
                tokens=None, output=out)
    now = datetime.now(timezone.utc).timestamp()
    os.utime(agents / "sess_a", (now, now))
    f = ql.load_fires(agents, DAY)[0]
    assert f.code == "1308"
    assert f.reset_at == "2026-09-30 20:54:52"
    assert f.provider_stamp == datetime(2026, 9, 30, 20, 13, 25)
    assert f.wall_coded  # failed status + coded death payload = a wall death


def test_cluster_walls_merges_one_burst_and_splits_distant_deaths(tmp_path):
    agents = tmp_path / "agents"
    base = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
    for i in range(15):
        _write_fire(agents, "sess_a", f"agent_ah{i}", created=base.isoformat(),
                    completed=(base + timedelta(minutes=13)).isoformat(),
                    status="failed", tokens=None,
                    output="[1308][Usage limit reached for 5 hour. "
                           "Your limit will reset at 2026-09-30 20:54:52][x]")
    # separate 1302 contact hours later
    _write_fire(agents, "sess_a", "agent_late", created="2026-09-30T17:32:31Z",
                completed="2026-09-30T17:37:03Z", status="failed",
                tokens=None, output="[1302][Rate limit reached for requests][x]")
    # a completed agent that merely NARRATES 1302 in prose is not a wall death
    _write_fire(agents, "sess_a", "agent_narrator", created="2026-09-30T18:00:00Z",
                completed="2026-09-30T18:01:00Z", status="completed",
                tokens=10, output="the lane died on 1302 earlier")
    now = datetime.now(timezone.utc).timestamp()
    os.utime(agents / "sess_a", (now, now))
    fires = ql.load_fires(agents, DAY)
    walls = ql.cluster_walls(fires)
    assert len(walls) == 2
    burst = walls[0]
    assert len(burst.lanes) == 15
    assert burst.codes == {"1308"}
    assert "15:54->20:54 provider" in burst.window_ended
    assert walls[1].codes == {"1302"} and len(walls[1].lanes) == 1


def test_peak_concurrency_counts_overlapping_lanes(tmp_path):
    t0 = datetime(2026, 9, 30, 10, 0, tzinfo=timezone.utc)
    fires = []
    for i in range(4):
        fires.append(ql.Fire(ts=t0 + timedelta(minutes=i * 2),
                             done_ts=t0 + timedelta(minutes=i * 2 + 30),
                             lane=f"l{i}", session="s", status="completed",
                             tokens=1, code=None, reset_at=None,
                             provider_stamp=None))
    # sequential lane: ends before the next starts
    fires.append(ql.Fire(ts=t0 + timedelta(hours=2),
                         done_ts=t0 + timedelta(hours=2, minutes=5),
                         lane="seq", session="s", status="completed",
                         tokens=1, code=None, reset_at=None, provider_stamp=None))
    peak, _ = ql.peak_concurrency(fires)
    assert peak == 4


def test_token_estimate_separates_recorded_from_extrapolated():
    fires = [
        ql.Fire(ts=datetime(2026, 9, 30, tzinfo=timezone.utc), done_ts=None,
                lane="a", session="s", status="completed", tokens=1000,
                code=None, reset_at=None, provider_stamp=None),
        ql.Fire(ts=datetime(2026, 9, 30, tzinfo=timezone.utc), done_ts=None,
                lane="b", session="s", status="completed", tokens=3000,
                code=None, reset_at=None, provider_stamp=None),
        ql.Fire(ts=datetime(2026, 9, 30, tzinfo=timezone.utc), done_ts=None,
                lane="c", session="s", status="failed", tokens=None,
                code="1308", reset_at=None, provider_stamp=None),
    ]
    est = ql.token_estimate(fires)
    assert est["recorded_tokens"] == 4000
    assert est["unrecorded_fires"] == 1
    assert est["mean_per_recorded"] == 2000
    assert est["estimated_total"] == 6000


def test_verdict_red_on_1308_in_current_window():
    wall = ql.WallMoment(ts=datetime.now(timezone.utc), codes={"1308"}, lanes=["x"])
    verdict, hold = ql.verdict_for(10, 4, [wall], 20, 8, 5)
    assert verdict == "RED"
    assert "HOLD" in hold and "8-12" in hold


def test_verdict_green_inside_proven_envelope():
    verdict, _ = ql.verdict_for(11, 11, [], 13, 11, 5)
    assert verdict == "GREEN"


def test_verdict_amber_at_first_1302_width():
    verdict, _ = ql.verdict_for(14, 15, [], 18, 15, 5)
    assert verdict == "AMBER"


def test_current_shape_ignores_stale_walls_but_holds_fresh_1308():
    fresh = datetime.now(timezone.utc) - timedelta(minutes=5)
    stale = datetime.now(timezone.utc) - timedelta(hours=3)
    w8 = ql.WallMoment(ts=fresh, codes={"1308"}, lanes=["x"])
    w2 = ql.WallMoment(ts=stale, codes={"1302"}, lanes=["y"])
    assert ql.current_shape(6, [w8]) == "RED"
    assert ql.current_shape(6, [w2]) == "GREEN"   # 3h-old wall does not HOLD a clean window
    assert ql.current_shape(15, []) == "AMBER"
    assert ql.current_shape(11, []) == "GREEN"


def test_main_exit_codes_and_markdown(tmp_path, capsys):
    agents = tmp_path / "agents"
    repo = tmp_path / "repo"
    (repo / "watch" / "inbox").mkdir(parents=True)
    (repo / "watch" / "inbox" / "DROP_LEDGER.jsonl").write_text(
        json.dumps({"ts": "2026-09-30", "drop_type": "wave",
                    "lanes_fired": ["AH1", "AH2"], "spend": 0.18}) + "\n",
        encoding="utf-8")
    receipt = repo / "watch" / "inbox" / "WALL_20260930.md"
    receipt.write_text("lane died [1308] mid-wave\n", encoding="utf-8")
    # receipt mtime today so grep_receipts sees it
    now = datetime.now(timezone.utc).timestamp()
    os.utime(receipt, (now, now))
    # green shape: 10 fires, no deaths
    for i in range(10):
        _write_fire(agents, "sess_a", f"agent_g{i}",
                    created=f"2026-09-30T0{i}:00:00Z",
                    completed=f"2026-09-30T0{i}:10:00Z", tokens=100)
    os.utime(agents / "sess_a", (now, now))
    rc = ql.main(["--day", DAY, "--agents-root", str(agents),
                  "--repo-root", str(repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Day-shape verdict: **GREEN**" in out
    assert "wall moments **0**" in out  # merged into the fires bullet
    assert "WALL_20260930.md:1" in out
    assert "ROUGH" in out and "1,000" in out  # 10 x 100 recorded
    # cannot-verify: empty day
    rc2 = ql.main(["--day", "2020-01-01", "--agents-root", str(agents),
                   "--repo-root", str(repo)])
    assert rc2 == 2
