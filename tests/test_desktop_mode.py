"""tests for mag/desktop_mode.py - genetic burn G1 lane i06-mode-build.

HARD RULE OF THIS FILE: no test may pause, unpause, or inspect a real container,
and no test may touch real repo state. Every docker touch goes through a
FakeDocker, the machine log is a no-op, receipts land under tmp_path, the lease
config points at tmp files, and operator_mode is a stub. The one real-mag.leases
integration test points leases.CONFIG_PATH at a tmp config (read-only, no
ledger writes under pytest).
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mag import desktop_mode as dm
from mag import leases as leases_mod


# ───────────────────────────── fakes ─────────────────────────────

T0 = 1000.0


class FakeClock:
    """Deterministic time: clock() reads, sleep() advances."""

    def __init__(self) -> None:
        self.t = T0

    def clock(self) -> float:
        return self.t

    def sleep(self, s: float) -> None:
        self.t += s


class FakeDocker:
    """Routes docker_ops._run calls without ever touching docker.

    ps_outputs: popped per `ps` call; dict name->status (joined verbatim) or
    raw string. health_values: popped per `inspect` call (per container).
    """

    def __init__(self, ps_outputs=None, health_values=None, version_ok=True):
        self.calls: list[list[str]] = []
        self.ps_outputs = list(ps_outputs or [])
        self.health = list(health_values or [])
        self.version_ok = version_ok

    def run(self, args, cwd=None, timeout=60):
        self.calls.append(list(args))
        head = args[0]
        if head == "version":
            return {"ok": self.version_ok, "code": 0 if self.version_ok else 1,
                    "out": "24.0.7" if self.version_ok else "", "err": ""}
        if head == "ps":
            out = self.ps_outputs.pop(0) if self.ps_outputs else ""
            if isinstance(out, dict):
                out = "\n".join(f"{n}\t{s}" for n, s in out.items())
            return {"ok": True, "code": 0, "out": out, "err": ""}
        if head in ("pause", "unpause"):
            return {"ok": True, "code": 0, "out": "", "err": ""}
        if head == "inspect":
            val = self.health.pop(0) if self.health else "healthy"
            return {"ok": True, "code": 0, "out": val, "err": ""}
        return {"ok": False, "code": 1, "out": "", "err": f"unexpected docker {head}"}

    def argv_of(self, head):
        return [c for c in self.calls if c and c[0] == head]


class OMStub:
    """operator_mode double; records every set_paused/resume."""

    def __init__(self):
        self.paused: list[dict] = []
        self.resumed: list[dict] = []

    def set_paused(self, **kw):
        self.paused.append(kw)
        return {"mode": "paused", **kw}

    def resume(self, **kw):
        self.resumed.append(kw)
        return {"mode": "running", **kw}

    def read(self):
        return {"schema": "operator_mode.v1", "mode": "running", "exists": False}


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(dm, "RECEIPT_DIR", tmp_path / "watch" / "inbox")
    monkeypatch.setattr(dm.docker_ops, "_log", lambda *a, **k: None)
    return tmp_path


def allow_guard(ops_log, holder="lane-test"):
    def g(op, **kw):
        ops_log.append(op)
        return {"allowed": True, "reason": "test", "holder": holder,
                "until": "2026-10-19T00:00:00Z", "op": op}
    return g


def refuse_guard(ops_log):
    def g(op, **kw):
        ops_log.append(op)
        return {"allowed": False, "refused": True, "op": op,
                "reason": f"REFUSED {op}: proc:desktop held by grok until 2026-10-19T02:00:00Z (UTC)",
                "how": "python scripts/lease.py acquire proc:desktop ..."}
    return g


PAUSED_PRE = {"mag-sovereign": "Up 5 hours (healthy)", "mag-worker": "Up 2 days (healthy)"}
PAUSED_POST = {"mag-sovereign": "Up 5 hours (Paused)", "mag-worker": "Up 2 days (Paused)"}


# ───────────────────── mode game: command construction ─────────────────────

def test_game_issues_exactly_one_pause_argv_in_order(sandbox, monkeypatch):
    fd = FakeDocker(ps_outputs=[PAUSED_PRE, PAUSED_POST])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    ops: list[str] = []
    monkeypatch.setattr(dm, "_lease_guard", allow_guard(ops))
    om = OMStub()
    monkeypatch.setattr(dm, "operator_mode", om)
    ck = FakeClock()

    res = dm.mode_game(until="4h", sleep=ck.sleep, crons_tasks=[], ps_rows=[])

    assert res["ok"] is True and res["exit_code"] == 0
    assert ops == ["mode.game"]
    pauses = fd.argv_of("pause")
    assert len(pauses) == 1
    assert pauses[0] == ["pause", "mag-sovereign", "mag-worker"]
    assert fd.argv_of("unpause") == []
    assert fd.argv_of("ps") == [dm.STATUS_ARGV, dm.STATUS_ARGV]
    # software pause at the source, scope all_agents, with the --until deadline
    assert len(om.paused) == 1
    assert om.paused[0]["scope"] == "all_agents"
    assert om.paused[0]["reason"] == "game session"
    got = datetime.fromisoformat(om.paused[0]["until"].replace("Z", "+00:00"))
    want = datetime.fromisoformat(dm.parse_until("4h").replace("Z", "+00:00"))
    assert abs((got - want).total_seconds()) < 5  # same +4h deadline, not byte-equal


def test_game_dry_runs_nothing(sandbox, monkeypatch):
    fd = FakeDocker()
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    ops: list[str] = []
    monkeypatch.setattr(dm, "_lease_guard", allow_guard(ops))

    res = dm.mode_game(dry=True, crons_tasks=[], ps_rows=[])

    assert fd.calls == []
    assert res["dry"] is True and res["ok"] is True
    assert res["plan"]["docker"] == [["pause", "mag-sovereign", "mag-worker"]]
    assert not (sandbox / "watch").exists()


def test_game_missing_twin_aborts_with_receipt(sandbox, monkeypatch):
    fd = FakeDocker(ps_outputs=[{"mag-sovereign": "Up 5 hours (healthy)"}])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))

    res = dm.mode_game(crons_tasks=[], ps_rows=[])

    assert res["exit_code"] == 1 and res["ok"] is False
    assert fd.argv_of("pause") == []
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "MISSING mag-worker" in text
    assert "half-twin" in text


def test_game_engine_down_aborts(sandbox, monkeypatch):
    fd = FakeDocker(version_ok=False)
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm.docker_ops, "ensure_engine",
                        lambda: {"ok": False, "launched": False,
                                 "engine_reachable": False, "waited_s": 120})
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))

    res = dm.mode_game(crons_tasks=[], ps_rows=[])

    assert res["exit_code"] == 1
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "STILL DOWN" in text


def test_game_anomaly_repause_once_never_loops(sandbox, monkeypatch):
    # pre-state, then at +60s mag-worker found unpaused (the 10-17 anomaly),
    # confirm read after the single re-pause shows both Paused again.
    fd = FakeDocker()
    fd.ps_outputs = [PAUSED_PRE,
                     {"mag-sovereign": "Up 5 hours (Paused)", "mag-worker": "Up 2 days (healthy)"},
                     PAUSED_POST]
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    om = OMStub()
    monkeypatch.setattr(dm, "operator_mode", om)
    ck = FakeClock()

    res = dm.mode_game(sleep=ck.sleep, crons_tasks=[], ps_rows=[])

    pauses = fd.argv_of("pause")
    assert len(pauses) == 2
    assert pauses[0] == ["pause", "mag-sovereign", "mag-worker"]
    assert pauses[1] == ["pause", "mag-worker"]
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "anomaly: unpauser anomaly: mag-worker found unpaused at +60s; re-paused ONCE" in text


# ───────────────────── mode game: receipt format ─────────────────────

def test_game_receipt_format_verbatim(sandbox, monkeypatch):
    fd = FakeDocker(ps_outputs=[PAUSED_PRE, PAUSED_POST])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    monkeypatch.setattr(dm, "operator_mode", OMStub())
    rows = [{"name": "chrome", "pid": 32204, "title": "fullscreen thief", "ppid": "",
             "cmdline": "chrome.exe"}]

    res = dm.mode_game(until="90m", sleep=FakeClock().sleep, crons_tasks=[], ps_rows=rows)

    text = Path(res["receipt"]).read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines[0].startswith("# MODE GAME - ")
    assert lines[0].endswith("(operator ask)")
    assert lines[1] == "schema: mode_receipt.v1"
    assert "seat: operator  lease: proc:desktop holder=lane-test" in text
    assert "  mag-sovereign: Up 5 hours (healthy) -> Paused" in text
    assert "  mag-worker:    Up 2 days (healthy) -> Paused" in text
    m = re.search(r"software: operator_mode paused scope=all_agents until=(\S+)", text)
    assert m is not None
    got = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
    want = datetime.fromisoformat(dm.parse_until("90m").replace("Z", "+00:00"))
    assert abs((got - want).total_seconds()) < 5
    assert "surface: 1 findings" in text
    assert 'chrome pid 32204 window "fullscreen thief" parent exited -> left' in text
    assert text.count("left_running: gstd-node, tortoise-db, mag-mcp, mag-redis, "
                      "cluster-factorio, host ollama, llama-server, scheduled tasks "
                      "(hidden-wrapped)") == 1
    assert "crons in window: none inside window" in text
    assert "anomaly: none observed at +60s recheck" in text


def test_game_cron_window_listing(sandbox, monkeypatch):
    fd = FakeDocker(ps_outputs=[PAUSED_PRE, PAUSED_POST])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    monkeypatch.setattr(dm, "operator_mode", OMStub())
    nr = (datetime.now().astimezone() + timedelta(hours=1)).strftime("%m/%d/%Y %I:%M:%S %p")
    tasks = [{"name": "\\MagImproveDaily", "next_run": nr}]

    res = dm.mode_game(until="4h", sleep=FakeClock().sleep, crons_tasks=tasks, ps_rows=[])

    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert f"MagImproveDaily @ {nr}" in text


def test_crons_wave_note_unit():
    # 07:30 start with a 4h window crosses the 08:00 EDT cron wave: the receipt
    # must name the no-op expectation from the CSV row, not from memory.
    start = datetime(2026, 10, 18, 7, 30).astimezone()
    until = (start + timedelta(hours=4)).isoformat()
    tasks = [{"name": "\\MagImproveDaily", "next_run": start.strftime("%m/%d/%Y %I:%M:%S %p")}]
    note = dm._crons_note(start, until, tasks=tasks)
    assert "MagImproveDaily" in note
    assert "drain/improve no-op expected, self-heal next cycle" in note
    assert dm._crons_note(start, until, tasks=[]) == "none inside window"


# ───────────────────── mode burn ─────────────────────

def _open_receipt() -> Path:
    dm.RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    p = dm.RECEIPT_DIR / "MODE_GAME_20261018_2145.md"
    p.write_text("# MODE GAME - 2026-10-18 21:45 EDT (operator ask)\n"
                 "schema: mode_receipt.v1\ncontainers:\n"
                 "  mag-sovereign:  Up 5 hours (healthy) -> Paused\n", encoding="utf-8")
    return p


def test_burn_unpause_polls_health_then_resumes_and_appends(sandbox, monkeypatch):
    p = _open_receipt()
    # ps pre-state once; health: poll 1 both starting, poll 2 both healthy
    fd = FakeDocker(ps_outputs=[PAUSED_POST],
                    health_values=["starting", "starting", "healthy", "healthy"])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    ops: list[str] = []
    monkeypatch.setattr(dm, "_lease_guard", allow_guard(ops))
    om = OMStub()
    monkeypatch.setattr(dm, "operator_mode", om)
    ck = FakeClock()

    res = dm.mode_burn(sleep=ck.sleep, clock=ck.clock, ps_rows=[])

    assert res["ok"] is True and res["exit_code"] == 0
    assert ops == ["mode.burn"]
    assert fd.argv_of("unpause") == [["unpause", "mag-sovereign", "mag-worker"]]
    assert res["health"] == {"mag-sovereign": 10, "mag-worker": 10}
    assert len(om.resumed) == 1
    assert om.resumed[0]["reason"] == "game session over"
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert text is not None and Path(res["receipt"]) == p
    assert "## RESUMED - " in text
    assert "unpause ok" in text
    assert "health: mag-sovereign healthy in 10s; mag-worker healthy in 10s" in text
    assert "software: operator_mode resumed" in text
    assert "surface after: 0 findings" in text


def test_burn_health_timeout_exits_1_never_resumes(sandbox, monkeypatch):
    _open_receipt()
    fd = FakeDocker(ps_outputs=[PAUSED_POST], health_values=["starting"] * 64)
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    om = OMStub()
    monkeypatch.setattr(dm, "operator_mode", om)
    ck = FakeClock()

    res = dm.mode_burn(sleep=ck.sleep, clock=ck.clock, ps_rows=[])

    assert res["ok"] is False and res["exit_code"] == 1
    assert om.resumed == []
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "## RESUMED - " in text
    assert f"NOT healthy within {dm.HEALTH_BUDGET_S}s" in text
    assert "mag-sovereign=starting; mag-worker=starting" in text
    assert "never restarts anything" in text
    assert "software: operator_mode resumed" not in text


def test_burn_requires_open_receipt(sandbox, monkeypatch):
    fd = FakeDocker()
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    dm.RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    res = dm.mode_burn()
    assert res["exit_code"] == 2
    assert "no open game-session receipt" in res["reason"]

    closed = dm.RECEIPT_DIR / "MODE_GAME_20261017_2100.md"
    closed.write_text("# MODE GAME - closed\n## RESUMED - earlier\n", encoding="utf-8")
    res2 = dm.mode_burn()
    assert res2["exit_code"] == 2
    assert fd.calls == []


def test_burn_dry_runs_nothing(sandbox, monkeypatch):
    fd = FakeDocker()
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))

    res = dm.mode_burn(dry=True)

    assert fd.calls == []
    assert res["dry"] is True
    assert res["plan"]["docker"] == [["unpause", "mag-sovereign", "mag-worker"]]


def test_burn_idempotent_when_already_running(sandbox, monkeypatch):
    _open_receipt()
    running = {"mag-sovereign": "Up 5 hours (healthy)", "mag-worker": "Up 2 days (healthy)"}
    fd = FakeDocker(ps_outputs=[running], health_values=["healthy", "healthy"])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", allow_guard([]))
    monkeypatch.setattr(dm, "operator_mode", OMStub())

    res = dm.mode_burn(sleep=FakeClock().sleep, clock=FakeClock().clock, ps_rows=[])

    assert res["ok"] is True
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "already Running (not Paused) on entry" in text


# ───────────────────── lease fail-closed + escapes ─────────────────────

_MISSING_ROW_CFG = {"schema": "restricted_leases.v1", "resources": {"proc:lab": {}}}
_ROW_CFG = {"schema": "restricted_leases.v1", "resources": {
    "proc:desktop": {"description": "the desktop twin", "paths": [],
                     "enforce": "conflict", "default_ttl_s": 7200, "max_ttl_s": 86400}}}


def test_missing_lease_row_fails_closed_with_named_error(sandbox, monkeypatch):
    cfg = sandbox / "restricted_leases.json"
    cfg.write_text(json.dumps(_MISSING_ROW_CFG), encoding="utf-8")
    monkeypatch.setattr(dm, "LEASE_CONFIG", cfg)
    fd = FakeDocker()
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)

    res = dm.mode_game()

    assert res["exit_code"] == 3 and res["refused"] is True
    # the NAMED error: message names the config file AND the missing row
    assert "configs/restricted_leases.json" in res["reason"]
    assert "proc:desktop" in res["reason"]
    assert fd.calls == []  # nothing ran, not even a probe


def test_lease_guard_refused_exit_3(sandbox, monkeypatch):
    cfg = sandbox / "restricted_leases.json"
    cfg.write_text(json.dumps(_ROW_CFG), encoding="utf-8")
    monkeypatch.setattr(dm, "LEASE_CONFIG", cfg)
    fd = FakeDocker()
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "_lease_guard", refuse_guard([]))

    res = dm.mode_game()
    assert res["exit_code"] == 3 and "held by grok" in res["reason"]
    assert fd.calls == []

    res2 = dm.mode_burn()
    assert res2["exit_code"] == 3 and fd.calls == []


def test_no_lease_escape_is_operator_gated_and_recorded(sandbox, monkeypatch):
    cfg = sandbox / "restricted_leases.json"
    cfg.write_text(json.dumps(_MISSING_ROW_CFG), encoding="utf-8")
    monkeypatch.setattr(dm, "LEASE_CONFIG", cfg)
    fd = FakeDocker(ps_outputs=[PAUSED_PRE, PAUSED_POST])
    monkeypatch.setattr(dm.docker_ops, "_run", fd.run)
    monkeypatch.setattr(dm, "operator_mode", OMStub())

    res = dm.mode_game(no_lease=True, sleep=FakeClock().sleep, crons_tasks=[], ps_rows=[])

    assert res["ok"] is True  # the escape proceeds past the missing row
    assert res["lease"]["no_lease"] is True
    text = Path(res["receipt"]).read_text(encoding="utf-8")
    assert "--no-lease operator-gated" in text


def test_real_leases_guard_integration_with_row(sandbox, monkeypatch):
    cfg = sandbox / "restricted_leases.json"
    cfg.write_text(json.dumps(_ROW_CFG), encoding="utf-8")
    monkeypatch.setattr(dm, "LEASE_CONFIG", cfg)
    monkeypatch.setattr(leases_mod, "CONFIG_PATH", cfg)

    assert dm.lease_row_exists() is True
    g = dm._lease_guard("mode.game")  # no other holder -> conflict tier allows with a warn
    assert g["allowed"] is True

    monkeypatch.setattr(dm, "LEASE_CONFIG", sandbox / "absent.json")
    assert dm.lease_row_exists() is False  # unreadable config = fail closed
    g2 = dm._lease_guard("mode.game")
    assert g2["allowed"] is False and "proc:desktop" in g2["reason"]


# ───────────────────── Part A detection rules ─────────────────────

def test_vbs_style0_rule():
    assert dm.audit_vbs("sh.Run(cmd, 0, True)")["verdict"] == "pass"
    assert dm.audit_vbs("WshShell.Run cmd, 1, False")["verdict"] == "flag"
    assert dm.audit_vbs("x = 1")["verdict"] == "flag"


def test_cmd_detached_vs_foreground():
    ok = dm.audit_cmd('start "" /b python tools/a.py\r\nstart "" /b python tools/b.py\r\n')
    assert ok["verdict"] == "pass"
    flag = dm.audit_cmd('python run_armC.py\n'
                        'rem start "" /b looks detached but is a comment\n'
                        ':: also a comment\n'
                        '# and this one\n')
    assert flag["verdict"] == "flag"
    assert "run_armC.py" in flag["reason"]


def _task_xml(command, arguments, enabled=True):
    return ('<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">'
            f'<Settings><Enabled>{"true" if enabled else "false"}</Enabled></Settings>'
            '<Actions Context="Author">'
            f'<Exec><Command>{command}</Command><Arguments>{arguments}</Arguments></Exec>'
            '</Actions></Task>')


def test_task_xml_rules(tmp_path):
    hidden = _task_xml("wscript.exe",
                       "//B //Nologo C:\\repo\\run_hidden.vbs powershell.exe -NoProfile -Command x")
    parsed = dm.audit_task_xml(hidden)
    assert parsed["enabled"] is True
    assert parsed["rows"][0]["verdict"] == "pass"

    direct = dm.audit_task_xml(_task_xml("powershell.exe", "-NoProfile -Command x"))
    assert direct["rows"][0]["verdict"] == "flag"

    bare = dm.audit_task_xml(_task_xml("cmd.exe", "/c sc thing"))
    assert bare["rows"][0]["verdict"] == "flag"

    disabled = dm.audit_task_xml(_task_xml("powershell.exe", "-Command x", enabled=False))
    assert disabled["enabled"] is False

    noargs = dm.audit_task_xml(_task_xml("wscript.exe", "//B"))
    assert noargs["rows"][0]["verdict"] == "manual"


def test_task_xml_referenced_vbs_style_check(tmp_path):
    good = tmp_path / "docker_watchdog.vbs"
    good.write_text("sh.Run(cmd, 0, True)", encoding="utf-8")
    row = dm.audit_task_xml(_task_xml("wscript.exe", f"//B //Nologo {good}"))["rows"][0]
    assert row["verdict"] == "pass"

    bad = tmp_path / "loud.vbs"
    bad.write_text("WshShell.Run cmd, 1, False", encoding="utf-8")
    row2 = dm.audit_task_xml(_task_xml("wscript.exe", f"//B //Nologo {bad}"))["rows"][0]
    assert row2["verdict"] == "flag"


def test_launcher_audit_end_to_end(tmp_path):
    startup = tmp_path / "Startup"
    startup.mkdir()
    (startup / "mag_boot_lane.cmd").write_text('start "" /b python q.py\n', encoding="utf-8")
    (startup / "bad.vbs").write_text("WshShell.Run cmd, 1, False", encoding="utf-8")
    (startup / "Ollama.lnk").write_bytes(b"")
    (startup / "old.cmd.disabled").write_text("python x.py\n", encoding="utf-8")
    tasks = [
        {"name": "\\MagHermesBurn247",
         "xml": _task_xml("wscript.exe",
                          "//B //Nologo C:\\repo\\run_hidden.vbs powershell.exe -NoProfile -Command x")},
        {"name": "\\MagLabKit8765", "status": "Disabled"},
    ]
    rows = dm.launcher_audit(startup_dirs=[startup], tasks=tasks)
    verdicts = {r["name"]: r["verdict"] for r in rows}
    assert verdicts["mag_boot_lane.cmd"] == "pass"
    assert verdicts["bad.vbs"] == "flag"
    assert verdicts["Ollama.lnk"] == "manual"
    assert "old.cmd.disabled" not in verdicts
    assert verdicts["\\MagHermesBurn247"] == "pass"
    assert verdicts["\\MagLabKit8765"] == "skipped"


def test_mode_status_strict_exit(sandbox, monkeypatch):
    monkeypatch.setattr(dm, "operator_mode", OMStub())
    empty = sandbox / "empty_startup"
    empty.mkdir()
    flag_task = [{"name": "\\MagLoud", "xml": _task_xml("powershell.exe", "-Command x")}]
    out = dm.mode_status(strict=True, startup_dirs=[empty], tasks=flag_task, statuses=PAUSED_POST)
    assert out["exit_code"] == 1 and out["flag_count"] == 1
    out2 = dm.mode_status(strict=True, startup_dirs=[empty], tasks=[], statuses=PAUSED_POST)
    assert out2["exit_code"] == 0 and out2["flag_count"] == 0


# ───────────────────── Part B classification + never-kill ─────────────────────

def test_classify_surface_rules():
    headless = dm.classify_surface({"name": "chrome", "pid": 33732, "title": "about:blank",
                                    "ppid": 4, "cmdline": "chrome --headless "
                                    "--remote-debugging-port=9222"})
    assert headless["verdict"] == "pass" and headless["action"] == "left"

    headed = dm.classify_surface({"name": "chrome", "pid": 32204, "title": "X",
                                  "ppid": "", "cmdline": "chrome.exe"})
    assert headed["verdict"] == "flag" and headed["action"] == "kill-candidate"

    overlay = dm.classify_surface({"name": "Cua.AgentCursorOverlay.default", "pid": 7700,
                                   "title": "overlay", "ppid": 5, "cmdline": "cua-driver"})
    assert overlay["action"] == "minimize-candidate"

    console = dm.classify_surface({"name": "powershell", "pid": 9, "title": "Console",
                                   "ppid": 5, "cmdline": "powershell.exe"})
    assert console["verdict"] == "flag" and console["action"] == "review"

    plain = dm.classify_surface({"name": "explorer", "pid": 4, "title": "", "ppid": "",
                                 "cmdline": ""})
    assert plain["verdict"] == "pass"


def test_sweep_never_touches_protected():
    assert dm._protected({"name": "gstd-node", "pid": 1, "title": "t", "cmdline": ""})
    assert dm._protected({"name": "tortoise-db", "pid": 1, "title": "t", "cmdline": ""})
    assert dm._protected({"name": "chrome", "pid": 1, "title": "t",
                          "cmdline": "wscript run_hidden.vbs chrome"})
    assert dm._protected({"name": "chrome", "pid": 1, "title": "t",
                          "cmdline": "--remote-debugging-port=9222"})
    assert dm._protected({"name": "chrome", "pid": 1, "title": "t", "cmdline": ""}) is None


def test_surface_scan_report_only_records_actions(sandbox):
    rows = [{"name": "chrome", "pid": 32204, "title": "X", "ppid": "", "cmdline": "chrome.exe"}]
    surf = dm.surface_scan(sweep=False, ps_rows=rows)
    assert surf["count"] == 1
    assert surf["findings"][0]["action"] == "left"  # report-only default


# ───────────────────── receipts + misc ─────────────────────

def test_find_open_receipt_newest_only(sandbox):
    dm.RECEIPT_DIR.mkdir(parents=True)
    older = dm.RECEIPT_DIR / "MODE_GAME_20261017_2100.md"
    newer = dm.RECEIPT_DIR / "MODE_GAME_20261018_2200.md"
    older.write_text("open session", encoding="utf-8")
    newer.write_text("closed\n## RESUMED - earlier\n", encoding="utf-8")
    os.utime(older, (1000, 1000))
    os.utime(newer, (2000, 2000))
    # newest receipt is closed -> no open session, refuse
    assert dm.find_open_receipt() is None
    os.utime(newer, (500, 500))  # make the open one the newest
    assert dm.find_open_receipt() == older


def test_parse_until_durations_and_iso():
    iso = dm.parse_until("90m")
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    assert abs((dt - datetime.now(timezone.utc) - timedelta(minutes=90)).total_seconds()) < 5
    fixed = dm.parse_until("2026-10-19T02:00:00Z")
    assert fixed == "2026-10-19T02:00:00Z"
    assert dm.parse_until("4h").endswith("Z")
