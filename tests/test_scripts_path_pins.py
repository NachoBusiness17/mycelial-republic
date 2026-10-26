"""B2-438 fixture pins: the runner-driven scripts refuse repo-external
paths and URLs.

Falsifier contract from the brief: a test that passes a repo-external path
or URL to any of the four entry points must NOT land a write or a request
after the fix. The drivers (mag/coding_session_loop.py, mag/
governor_autorun.py, mag/lane_runner.py) execute these scripts with
config-derived inputs, so the pins hold the input surfaces the triage named
(B2_96_scripts_triage_20260926.md must-fix set).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- desk probe
def test_desk_probe_get_refuses_external_url_without_request(monkeypatch):
    import urllib.request

    mod = _load("desk_probe", "scripts/desk_baseline_probe.py")

    def _boom(*a, **k):
        raise AssertionError("urlopen must not be called for a refused URL")

    monkeypatch.setattr(urllib.request, "urlopen", _boom)
    out, err = mod._http_get_json("http://evil.example/steal")
    assert out is None
    assert "allowlist" in err
    out2, err2 = mod._http_get_text("http://evil.example/steal")
    assert out2 is None and "allowlist" in err2


def test_desk_probe_allows_localhost_target(monkeypatch):
    import urllib.request

    mod = _load("desk_probe2", "scripts/desk_baseline_probe.py")

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b'{"ok": true}'

    seen = {}

    def fake_urlopen(req, timeout=None):
        seen["url"] = req.full_url
        return _Resp()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    out, err = mod._http_get_json("http://127.0.0.1:8765/api/v1/agent-desk")
    assert err is None and out == {"ok": True}
    assert seen["url"].startswith("http://127.0.0.1:8765")


# ---------------------------------------------------------------- wave driver
def test_wave_driver_path_args_refuse_external_board(monkeypatch):
    mod = _load("wave_driver", "scripts/wave_driver.py")

    # genuinely external: a sibling of the repo, NOT pytest tmp_path (this
    # box redirects the pytest tmp root INSIDE the repo, agents/pytest-tmp-*,
    # which the pin must and does treat as internal)
    external = str(Path(mod.ROOT).resolve().parent / "_b2_438_external" / "wave.json")

    class Args:
        board = external
        steers = mod.STEERS_DEFAULT
        key = mod.KEY_DEFAULT
        kb = mod.KB_DEFAULT
        telemetry = mod.TELEMETRY_DEFAULT
        ground = mod.GROUND_DEFAULT
        state = mod.STATE_DEFAULT
        lanes_root = mod.LANES_ROOT_DEFAULT

    monkeypatch.delenv("MAG_ALLOW_EXTERNAL_PATH", raising=False)
    with pytest.raises(SystemExit) as ei:
        mod.validate_path_args(Args(), mod.ROOT)
    assert ei.value.code == 2
    # nothing was written
    assert not (Path(mod.ROOT).resolve().parent / "_b2_438_external").exists()


def test_wave_driver_path_args_accept_defaults_and_escape_hatch(tmp_path, monkeypatch):
    mod = _load("wave_driver2", "scripts/wave_driver.py")

    class Args:
        board = mod.BOARD_DEFAULT
        steers = mod.STEERS_DEFAULT
        key = mod.KEY_DEFAULT
        kb = mod.KB_DEFAULT
        telemetry = mod.TELEMETRY_DEFAULT
        ground = mod.GROUND_DEFAULT
        state = mod.STATE_DEFAULT
        lanes_root = mod.LANES_ROOT_DEFAULT

    monkeypatch.delenv("MAG_ALLOW_EXTERNAL_PATH", raising=False)
    mod.validate_path_args(Args(), mod.ROOT)  # defaults live under ROOT

    # named escape hatch: explicit env allows a genuinely external target
    monkeypatch.setenv("MAG_ALLOW_EXTERNAL_PATH", "1")
    external = str(Path(mod.ROOT).resolve().parent / "_b2_438_external" / "wave.json")

    class Args2(Args):
        board = external

    mod.validate_path_args(Args2(), mod.ROOT)  # must NOT raise under the env


# ------------------------------------------------------- hunger_ledger + m12
def test_hunger_ledger_derivation_is_repo_pinned():
    mod = _load("hunger", "scripts/hunger_ledger.py")
    ledger = Path(mod.LEDGER).resolve()
    assert ledger.is_relative_to(Path(mod.REPO).resolve())
    assert ledger.name == "HUNGER_LEDGER.md"


def test_m12_run_default_is_repo_pinned():
    mod = _load("m12", "scripts/m12_pairing.py")
    run = Path(mod.RUN_DEFAULT).resolve()
    assert run.is_relative_to(ROOT)
    assert run.name == "m12_pairing_run.json"
