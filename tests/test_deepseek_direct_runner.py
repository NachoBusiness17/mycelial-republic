"""Offline tests for mag/deepseek_direct_runner.py (no network, no API key needed).

Run with MAG_ALLOW_LIVE_WRITES unset; every write goes to tmp_path.
Fake secrets are assembled by concatenation so this file holds no token-shaped literal.
"""
from __future__ import annotations

import io
import json
import socket
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from mag import deepseek_direct_runner as ddr

FAKE_SK = "sk-" + "Zq9" * 8
FAKE_XAI = "xai-" + "Ab1" * 8
FAKE_GHP = "ghp_" + "Cd2" * 10
FAKE_AKIA = "AKIA" + "QWERTYUIOPASDFGH"
FAKE_B64 = "aGVsbG8" + "9" * 30 + "=="
FAKE_KEY_ENV = "unit-test-" + "not-a-real-key-" + "0000"


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Any real socket connect or urlopen during a test is a failure."""
    def _boom(*a, **k):
        raise AssertionError("network access attempted in an offline test")
    monkeypatch.setattr(socket.socket, "connect", _boom)
    monkeypatch.setattr(urllib.request, "urlopen", _boom)


# ----------------------------------------------------------------- denylist
@pytest.mark.parametrize("rel", [
    ".env", "configs/.env.local", "deploy/.env.production", "free_keys/a.txt",
    "memory/secret_gate_results/r.json", "memory/trajectory/steps.jsonl", "x/steps.jsonl",
    "tools/api_key.txt", "configs/KEYS.md", "certs/server.pem", "home/.ssh/id_rsa",
    "../outside.py", "C:/Users/x/.env", "/etc/passwd", ".git/config", "memory/trajectory/x.md",
])
def test_denylist_blocks_secret_paths(rel):
    assert ddr.is_denied(rel) is not None


@pytest.mark.parametrize("rel", ["mag/context_pack.py", "scripts/backup_chain.py",
                                 "tools/gps_mcp/providers.py", "tests/test_ack_reaper.py"])
def test_denylist_allows_normal_paths(rel):
    assert ddr.is_denied(rel) is None


def test_denied_file_is_never_opened(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("DEEPSEEK_API_KEY=" + FAKE_SK + "\n", encoding="utf-8")
    (tmp_path / "free_keys").mkdir()
    (tmp_path / "free_keys" / "k.txt").write_text(FAKE_SK, encoding="utf-8")
    opened: list[str] = []
    real = Path.read_bytes

    def spy(self):
        opened.append(str(self))
        return real(self)
    monkeypatch.setattr(Path, "read_bytes", spy)
    for rel in (".env", "free_keys/k.txt"):
        pf, why = ddr.pack_file(tmp_path, rel)
        assert pf is None and why.startswith("denylist")
    assert opened == []


def test_globs_pass_through_denylist(tmp_path):
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / ".env").write_text("A=1\n", encoding="utf-8")
    (tmp_path / "free_keys").mkdir()
    (tmp_path / "free_keys" / "k.py").write_text("k = 1\n", encoding="utf-8")
    (tmp_path / "my_key_store.py").write_text("k = 1\n", encoding="utf-8")
    rels, skipped = ddr.resolve_steal_paths(tmp_path, {"files": [], "globs": ["**/*"]})
    assert rels == ["ok.py"]
    assert {s["path"] for s in skipped} >= {".env", "free_keys/k.py", "my_key_store.py"}


# ----------------------------------------------------------------- redaction
def test_redaction_removes_secret_shapes_and_keeps_line_count():
    lines = [
        "client = make(" + repr(FAKE_SK) + ")",
        "XAI = '" + FAKE_XAI + "'",
        "gh = " + FAKE_GHP,
        "aws = " + FAKE_AKIA,
        "api_key: " + FAKE_B64,
        "headers['Authorization'] = 'Bearer " + "abcDEF1234567890abcdefXYZ" + "'",
        "-----BEGIN " + "RSA PRIVATE KEY-----",
        "MIIEowIBAAKCAQEA" + "x" * 40,
        "-----END " + "RSA PRIVATE KEY-----",
        "token = compute_token_from_something_long(x)",
        "def keep_me(): return 42",
    ]
    out, counts = ddr.redact_lines(lines)
    assert len(out) == len(lines)
    blob = "\n".join(out)
    for secret in (FAKE_SK, FAKE_XAI, FAKE_GHP, FAKE_AKIA, FAKE_B64, "MIIEowIBAAKCAQEA"):
        assert secret not in blob
    assert out[9] == lines[9], "code identifiers next to 'token' must not be redacted"
    assert out[10] == lines[10]
    assert counts.get("pem") == 1 and counts.get("sk") == 1


def test_packed_file_is_redacted_and_line_numbered(tmp_path):
    (tmp_path / "m.py").write_text("a = 1\nk = '" + FAKE_SK + "'\nb = 2\n", encoding="utf-8")
    pf, why = ddr.pack_file(tmp_path, "m.py")
    assert why is None and pf.total_lines == 3
    text = pf.render()
    assert FAKE_SK not in text
    assert "    2| k = '[REDACTED]'" in text
    assert "<<<FILE m.py | lines 1-3 of 3" in text


# ----------------------------------------------------------------- citations
def test_citation_checker_catches_bad_line_and_unpacked_path():
    packed = {"mag/a.py": (1, 50), "tools/b.py": (1, 10)}
    text = ("Uses mag/a.py:12 and `tools/b.py:3-9`; also mag/a.py:51 (beyond) and "
            "tools/b.py:8-11 (straddles) and mag/ghost_file.py:4 (never packed).")
    r = ddr.check_citations(text, packed)
    assert r["citations_ok"] == 2
    assert r["citations_bad"] == 3
    reasons = sorted(b["reason"].split(" ")[0] for b in r["bad"])
    assert reasons == ["not_packed", "out_of_range", "out_of_range"]


def test_truncated_file_range_is_enforced(tmp_path):
    (tmp_path / "big.py").write_text("".join(f"x{i} = {i}\n" for i in range(4000)), encoding="utf-8")
    (tmp_path / "small.py").write_text("y = 1\n", encoding="utf-8")
    files = [ddr.pack_file(tmp_path, r)[0] for r in ("big.py", "small.py")]
    notes = ddr.fit_budget(files, 5000)
    big = files[0]
    assert big.truncated and 0 < big.last_line < 4000
    assert not files[1].truncated
    assert sum(f.est_tokens() for f in files) <= 5000
    assert notes and "big.py" in notes[0]
    r = ddr.check_citations(f"big.py:{big.last_line + 1}", {f.path: (1, f.last_line) for f in files})
    assert r["citations_bad"] == 1


# ----------------------------------------------------------------- dry run (real STEALS table)
def test_dry_run_writes_manifest_with_no_network(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    rc = ddr.run(["--steal", "all", "--out-root", str(tmp_path), "--no-pointer"])
    assert rc == 0
    runs = list(tmp_path.iterdir())
    assert len(runs) == 1
    out = runs[0]
    man = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert man["mode"] == "dry-run" and man["model"] == "deepseek-flash"
    assert [s["steal"] for s in man["steals"]] == [1, 2, 3, 4, 5]
    for s in man["steals"]:
        assert (out / s["prompt_file"]).is_file()
        assert s["files"], f"steal {s['steal']} packed nothing"
        assert s["prompt_est_tokens"] <= man["budget_tokens"] + 2000
        for f in s["files"]:
            assert (ddr.ROOT / f["path"]).is_file(), f"cited path not on disk: {f['path']}"
            assert ddr.is_denied(f["path"]) is None
    assert (out / "SUMMARY.md").is_file()
    assert not list(out.glob("*_receipt.json")) and not list(out.glob("*_response.md"))


def test_every_steal_table_path_exists_on_disk():
    for n, steal in ddr.STEALS.items():
        for rel in steal["files"]:
            assert (ddr.ROOT / rel).is_file(), f"steal {n}: {rel} missing"
            assert ddr.is_denied(rel) is None


# ----------------------------------------------------------------- live path, mocked
class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def _mini_root(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    (root / "mag").mkdir(parents=True)
    (root / "mag" / "a.py").write_text("".join(f"line{i}\n" for i in range(1, 21)), encoding="utf-8")
    monkeypatch.setattr(ddr, "STEALS", {1: {"name": "t", "goal": "g", "files": ["mag/a.py"],
                                            "globs": [], "gaps": []}})
    return root


def test_live_missing_key_fails_cleanly(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    root = _mini_root(tmp_path, monkeypatch)
    rc = ddr.run(["--live", "--steal", "1", "--out-root", str(tmp_path / "out"), "--no-pointer"],
                 root=root)
    assert rc == 2
    assert not (tmp_path / "out").exists()


def test_live_mocked_flags_failed_falsifier_and_never_writes_key(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY_ENV)
    root = _mini_root(tmp_path, monkeypatch)
    seen: dict = {}

    def fake_urlopen(req, timeout=None):
        seen["url"] = req.full_url
        seen["auth_ok"] = req.get_header("Authorization") == "Bearer " + FAKE_KEY_ENV
        body = {"id": "x", "model": "deepseek-flash",
                "choices": [{"finish_reason": "stop", "message": {
                    "content": "## 1. Existing organs\nmag/a.py:3 ok, mag/a.py:99 bad\n## 5. UNKNOWN\nUNKNOWN"}}],
                "usage": {"prompt_tokens": 1000, "prompt_cache_hit_tokens": 0,
                          "prompt_cache_miss_tokens": 1000, "completion_tokens": 200}}
        return _Resp(json.dumps(body).encode())
    out_root = tmp_path / "out"
    rc = ddr.run(["--live", "--steal", "1", "--out-root", str(out_root), "--no-pointer"],
                 root=root, urlopen=fake_urlopen)
    assert rc == 3
    assert seen["url"] == ddr.ENDPOINT and seen["auth_ok"]
    run_dir = next(out_root.iterdir())
    rec = json.loads((run_dir / "steal_1_receipt.json").read_text(encoding="utf-8"))
    assert rec["status"] == "FAILED_FALSIFIER"
    assert rec["citations_ok"] == 1 and rec["citations_bad"] == 1
    assert rec["cost_estimate"]["usd"] > 0
    for p in run_dir.rglob("*"):
        if p.is_file():
            assert FAKE_KEY_ENV not in p.read_text(encoding="utf-8", errors="replace")


def test_retry_on_429_then_success():
    calls = {"n": 0}
    sleeps: list[float] = []

    def flaky(req, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise urllib.error.HTTPError(req.full_url, 429 if calls["n"] == 1 else 503, "busy",
                                         {}, io.BytesIO(b'{"error":"busy"}'))
        return _Resp(b'{"choices": []}')
    data, attempts = ddr.call_deepseek(FAKE_KEY_ENV, {"model": "m"}, urlopen=flaky,
                                       sleep=sleeps.append, retries=4)
    assert attempts == 3 and len(sleeps) == 2 and data == {"choices": []}


def test_400_is_not_retried_and_error_has_no_key():
    def bad(req, timeout=None):
        raise urllib.error.HTTPError(req.full_url, 400, "bad", {}, io.BytesIO(b'{"error":"bad"}'))
    with pytest.raises(ddr.LiveCallError) as ei:
        ddr.call_deepseek(FAKE_KEY_ENV, {"model": "m"}, urlopen=bad, sleep=lambda s: None)
    assert "HTTP 400" in str(ei.value) and FAKE_KEY_ENV not in str(ei.value)


def test_peak_window():
    from datetime import datetime, timezone
    assert ddr.is_peak(datetime(2026, 10, 19, 7, 0, tzinfo=timezone.utc))      # Mon 07Z
    assert not ddr.is_peak(datetime(2026, 10, 19, 5, 0, tzinfo=timezone.utc))  # Mon 05Z
    assert not ddr.is_peak(datetime(2026, 10, 17, 7, 0, tzinfo=timezone.utc))  # Sat
