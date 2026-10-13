"""Regression: CR at env-key load must never reach a Bearer header (TS-11 cure 2).

Cause: the elder lane's 14-cycle daily-429 outage (2026-09-20..2026-10-03) was
a CRLF .env gluing a literal \r onto the OPENROUTER key at mag-sovereign start
(compose env_file carried it into the container env); urllib rejects
"Bearer <key>\r" as an invalid header, and the CYCLE_FAIL echo of that
exception leaked the key (KEY_SCRUB_20261004). Law landed 2026-10-05: strip
\r\n at every env-key LOAD, never trust the load path. Fix cause/evidence
cites watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md (root cause chain
items 1-2). One test, three cage-side load paths: lane_runner.flash_call,
watch/march_228._load_dotenv, mag/art_forge._env_or_dotenv.
"""
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

import mag.lane_runner as lr
from mag.art_forge import _env_or_dotenv

REPO = Path(__file__).resolve().parent.parent


class _FakeResp:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return json.dumps({"choices": [{"message": {"content": "ok"}}]}).encode("utf-8")


def test_crlf_env_key_never_reaches_bearer_or_key_load(monkeypatch, tmp_path):
    """One law, three load paths: a key carrying a literal \r from a CRLF env
    value or CRLF .env file is stripped at the LOAD, so the Bearer header and
    every derived module key carry zero CR/LF bytes."""
    # (1) lane_runner.flash_call: CR-laden os.environ value never reaches the
    #     Authorization header. No network: the opener and SSRF check are
    #     swapped, the thought bank is a no-op.
    captured = {}

    class _FakeOpener:
        def open(self, req, timeout=120):
            captured["auth"] = req.get_header("Authorization")
            return _FakeResp()

    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-crfixture0123456789\r")
    monkeypatch.setenv("OPENROUTER_FLASH_MODEL", "fixture/model\r\n")
    monkeypatch.setattr(lr, "_OPENER", _FakeOpener())
    monkeypatch.setattr(lr, "_safe_https_url", lambda url: True)
    monkeypatch.setattr("mag.thought_bank.bank_response", lambda *a, **k: None)
    assert lr.flash_call("system", "user") == "ok"
    auth = captured["auth"]
    assert auth == "Bearer sk-or-v1-crfixture0123456789"
    assert "\r" not in auth and "\n" not in auth

    # (2) watch/march_228._load_dotenv: a CRLF .env parses to CR-free values.
    #     The real module file is executed with its two module-level mag/
    #     organ imports stubbed (neither is needed by the loader under test).
    for name in ("bay_organs", "flight_recorder"):
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))
    spec = importlib.util.spec_from_file_location(
        "march_228_cr_cure", REPO / "watch" / "march_228.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    env_file = tmp_path / ".env"
    env_file.write_bytes(b"ZAI_API_KEY_Pro=fixture-march-key-123\r\nOTHER=ok\r\n")
    loaded = mod._load_dotenv(env_file)
    assert loaded["ZAI_API_KEY_Pro"] == "fixture-march-key-123"
    assert "\r" not in loaded["ZAI_API_KEY_Pro"]
    assert "\n" not in loaded["ZAI_API_KEY_Pro"]

    # (3) mag.art_forge._env_or_dotenv: both branches, file then environ.
    root = tmp_path / "forge"
    root.mkdir()
    (root / ".env").write_bytes(b"XAI_API_KEY=fixture-forge-key\r\n")
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    assert _env_or_dotenv(root, "XAI_API_KEY") == "fixture-forge-key"
    monkeypatch.setenv("XAI_API_KEY", "fixture-forge-env\r")
    assert _env_or_dotenv(root, "XAI_API_KEY") == "fixture-forge-env"


def test_march_loader_skips_missing_env_file(monkeypatch, tmp_path):
    """The night-cage shape (no .env) still yields an empty dict, no crash:
    the 2026-10-04 rc=2 honest-skip cure keeps working on the refactored
    loader."""
    for name in ("bay_organs", "flight_recorder"):
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))
    spec = importlib.util.spec_from_file_location(
        "march_228_cr_cure_missing", REPO / "watch" / "march_228.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod._load_dotenv(tmp_path / "absent.env") == {}
