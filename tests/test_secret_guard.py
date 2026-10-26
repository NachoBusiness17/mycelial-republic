"""Tests for tools/secret_guard + tools/safe_ssh. SYNTHETIC fake secrets only; never touches
the real .env (MAG_SECRET_GUARD_ROOT points at a tmp fake repo)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKE = "fake-zai-lite-0000SYNTHETIC0000abcdef"


@pytest.fixture()
def fake_repo(tmp_path, monkeypatch):
    lines = [f"FAKE_VAR_{i}=x" for i in range(1, 44)]
    lines.append(f"# ZAI_LITE_API_KEY={FAKE}")       # line 44, commented-out, like the incident
    (tmp_path / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")
    audit = tmp_path / "state" / "secret_guard" / "audit.jsonl"
    monkeypatch.setenv("MAG_SECRET_GUARD_ROOT", str(tmp_path))
    monkeypatch.setenv("MAG_SECRET_GUARD_AUDIT", str(audit))
    for m in ("MAG_AGENT", "CI", "CURSOR_AGENT"):
        monkeypatch.delenv(m, raising=False)
    return tmp_path, audit


def _rows(audit):
    return [json.loads(l) for l in audit.read_text(encoding="utf-8").splitlines()]


def _child(code, tmp, audit):
    env = dict(os.environ, MAG_SECRET_GUARD="1", MAG_SECRET_GUARD_ROOT=str(tmp),
               MAG_SECRET_GUARD_AUDIT=str(audit), PYTHONPATH=REPO)
    return subprocess.run([sys.executable, "-c", textwrap.dedent(code)], env=env,
                          capture_output=True, text=True, cwd=str(tmp))


def test_open_env_line_blocked_under_hook(fake_repo):
    tmp, audit = fake_repo
    r = _child("""
        from tools.secret_guard import install_hook
        assert install_hook()
        try:
            line = open('.env').read().splitlines()[43]
            print('LEAKED', len(line))
        except PermissionError as e:
            print('BLOCKED')
        """, tmp, audit)
    assert "BLOCKED" in r.stdout, r.stderr
    assert "LEAKED" not in r.stdout
    assert any(x["event"] == "open_blocked" for x in _rows(audit))
    assert FAKE not in audit.read_text(encoding="utf-8")


def test_pathlib_and_os_open_blocked(fake_repo):
    tmp, audit = fake_repo
    r = _child("""
        import os, pathlib
        from tools.secret_guard import install_hook; install_hook()
        n = 0
        for f in (lambda: pathlib.Path('.env').read_text(), lambda: os.open('.env', os.O_RDONLY)):
            try: f()
            except PermissionError: n += 1
        print('BLOCKED', n)
        """, tmp, audit)
    assert "BLOCKED 2" in r.stdout, r.stderr


def test_raw_subprocess_ssh_blocked_under_hook(fake_repo):
    tmp, audit = fake_repo
    r = _child("""
        import subprocess
        from tools.secret_guard import install_hook; install_hook()
        try:
            subprocess.run(['ssh', 't90', 'cat > /sdcard/lite.key'], input=b'x')
            print('RAN')
        except PermissionError:
            print('BLOCKED')
        """, tmp, audit)
    assert "BLOCKED" in r.stdout, r.stderr
    assert any(x["event"] == "egress_blocked_unwrapped" for x in _rows(audit))


def test_guard_loads_in_process_and_logs_sha8_only(fake_repo):
    tmp, audit = fake_repo
    from tools.secret_guard import guard
    v = guard.load_secret(tmp / ".env", "ZAI_LITE_API_KEY", caller="test")
    assert v == FAKE
    rows = _rows(audit)
    assert rows[-1]["event"] == "load" and rows[-1]["sha8"] == guard.sha8(FAKE)
    assert FAKE not in audit.read_text(encoding="utf-8")
    with pytest.raises(guard.SecretExportDenied):
        guard.export_secret(v, destination="t90:/sdcard/x")


def test_safe_ssh_blocks_secret_on_stdin_and_logs(fake_repo):
    tmp, audit = fake_repo
    from tools import safe_ssh
    from tools.secret_guard import guard
    with pytest.raises(safe_ssh.EgressBlocked):
        safe_ssh.run(["ssh", "t90", "cat > /sdcard/zai_lite.txt"], input=FAKE + "\n", caller="test")
    rows = _rows(audit)
    hit = [x for x in rows if x["event"] == "egress_secret_hit"][-1]
    assert guard.sha8(FAKE) in hit["sha8"] and "t90" in hit["destination"]
    assert any(x["event"] == "transfer_denied_noninteractive" for x in rows)
    assert any(x["event"] == "egress_blocked" for x in rows)
    assert FAKE not in audit.read_text(encoding="utf-8")


def test_safe_ssh_blocks_secret_in_scp_source_file(fake_repo):
    tmp, audit = fake_repo
    from tools import safe_ssh
    p = tmp / "innocent_name.txt"
    p.write_text("note: " + FAKE, encoding="utf-8")
    with pytest.raises(safe_ssh.EgressBlocked):
        safe_ssh.run(["scp", str(p), "t90:/sdcard/"], caller="test")


def test_safe_ssh_clean_payload_passes_scan(fake_repo, monkeypatch):
    tmp, audit = fake_repo
    from tools import safe_ssh
    called = {}
    monkeypatch.setattr(safe_ssh.subprocess, "run", lambda cmd, **kw: called.setdefault("cmd", cmd))
    safe_ssh.run(["ssh", "t90", "echo hi"], input=b"hello", caller="test")
    assert called["cmd"][0] == "ssh"


def test_approval_requires_tty_and_fresh_nonce(fake_repo, monkeypatch):
    tmp, audit = fake_repo
    from tools.secret_guard import guard
    # non-interactive: denied without ever prompting
    asked = []
    assert guard.request_transfer("K", "t90:/x", caller="t", _input=lambda p: asked.append(p) or "",
                                  _isatty=lambda: False) is False
    assert asked == []
    # TTY but wrong nonce: denied
    assert guard.request_transfer("K", "t90:/x", caller="t", _input=lambda p: "000000",
                                  _isatty=lambda: True) is False
    # TTY + nonce typed back: approved; prompt shows destination
    seen = {}
    def typist(prompt):
        seen["p"] = prompt
        return prompt.split("Type ")[1].split(" ")[0]
    assert guard.request_transfer("K", "t90:/sdcard/x", caller="t", _input=typist,
                                  _isatty=lambda: True) is True
    assert "t90:/sdcard/x" in seen["p"]
    # agent env marker forces deny even if a TTY is present
    monkeypatch.setenv("MAG_AGENT", "1")
    assert guard._interactive() is False
