"""tests/test_ah5_warmboot.py — AH5 (audit §2.3, 2026-09-30).

hermes_warm_boot._deployments hardcoded the Vercel URL inline (old L86-89).
The known-URL list now resolves env MAG_DEPLOYMENTS > configs/deployments.json
> the old inline literal as the default fallback. Pinned here: config load
(tmp config + the real repo config), env override (list shape, object shape,
invalid JSON falling through with a note), the default fallback keeping the
exact old URL, the --check-deployments HEAD probe (200 / 302+Location /
transport error) against stubbed openers — no real network in tests — and the
CLI exit code + no-state-write for the flag.
"""
from __future__ import annotations

import email.message
import json
import sys
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import hermes_warm_boot as hw  # noqa: E402

_OLD_INLINE_URL = "https://vercel-deploy-7jx41m3r3-mag-d961.vercel.app/public/soul_frontier.html"


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("MAG_DEPLOYMENTS", raising=False)


def _write_config(tmp_path: Path, urls: list[str]) -> Path:
    cfg = tmp_path / "deployments.json"
    cfg.write_text(json.dumps({"schema": "mag.deployments.v1", "known_urls": urls}),
                   encoding="utf-8")
    return cfg


# ── config load ──────────────────────────────────────────────────────────────

def test_urls_load_from_configs_file(tmp_path, monkeypatch) -> None:
    cfg = _write_config(tmp_path, ["https://cfg.example/a.html"])
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", cfg)
    urls, source, notes = hw._deployment_urls()
    assert source == "configs" and urls == ["https://cfg.example/a.html"] and notes == []


def test_real_repo_config_loads_and_keeps_the_url() -> None:
    """The shipped configs/deployments.json parses and carries the old inline URL."""
    cfg = json.loads(hw.DEPLOYMENTS_CONFIG.read_text(encoding="utf-8"))
    assert cfg["known_urls"], "configs/deployments.json lost its known_urls"
    urls, source, _ = hw._deployment_urls()
    assert source == "configs"
    assert _OLD_INLINE_URL in urls


def test_broken_config_file_falls_back_with_note(tmp_path, monkeypatch) -> None:
    cfg = tmp_path / "deployments.json"
    cfg.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", cfg)
    urls, source, notes = hw._deployment_urls()
    assert source == "default" and urls == [_OLD_INLINE_URL]
    assert any("deployments.json" in n for n in notes)


# ── env override ─────────────────────────────────────────────────────────────

def test_env_override_list_shape(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", tmp_path / "absent.json")
    monkeypatch.setenv("MAG_DEPLOYMENTS", json.dumps(["https://env.example/b.html"]))
    urls, source, notes = hw._deployment_urls()
    assert source == "env" and urls == ["https://env.example/b.html"] and notes == []


def test_env_override_object_shape(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", tmp_path / "absent.json")
    monkeypatch.setenv("MAG_DEPLOYMENTS",
                       json.dumps({"known_urls": ["https://env.example/c.html"]}))
    urls, source, _ = hw._deployment_urls()
    assert source == "env" and urls == ["https://env.example/c.html"]


def test_env_override_beats_configs_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", _write_config(tmp_path, ["https://cfg.example/a.html"]))
    monkeypatch.setenv("MAG_DEPLOYMENTS", json.dumps(["https://env.example/wins.html"]))
    urls, source, _ = hw._deployment_urls()
    assert source == "env" and urls == ["https://env.example/wins.html"]


def test_env_invalid_json_falls_through_with_note(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", _write_config(tmp_path, ["https://cfg.example/a.html"]))
    monkeypatch.setenv("MAG_DEPLOYMENTS", "not json at all")
    urls, source, notes = hw._deployment_urls()
    assert source == "configs" and urls == ["https://cfg.example/a.html"]
    assert any("MAG_DEPLOYMENTS" in n for n in notes)


def test_env_wrong_shape_falls_through_with_note(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", tmp_path / "absent.json")
    monkeypatch.setenv("MAG_DEPLOYMENTS", json.dumps({"urls": ["https://env.example/x.html"]}))
    urls, source, notes = hw._deployment_urls()
    assert source == "default" and urls == [_OLD_INLINE_URL]
    assert any("MAG_DEPLOYMENTS" in n for n in notes)


# ── default fallback + payload shape ─────────────────────────────────────────

def test_default_fallback_keeps_the_old_inline_url(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", tmp_path / "absent.json")
    urls, source, notes = hw._deployment_urls()
    assert source == "default" and notes == []
    assert urls == [_OLD_INLINE_URL], "the AH5 fallback must keep the old hardcoded URL"


def test_deployments_dict_carries_urls_and_source(monkeypatch) -> None:
    monkeypatch.setattr(hw, "DEPLOY", ROOT / "no-such-vercel-deploy-dir")
    monkeypatch.setattr(hw, "DEPLOYMENTS_CONFIG", ROOT / "no-such-config.json")
    dep = hw._deployments()
    assert dep["ok"] is True and dep["files"] == []
    assert dep["known_urls"] == [_OLD_INLINE_URL]
    assert dep["known_urls_source"] == "default"


# ── --check-deployments: HEAD probe (stubbed openers, no network) ────────────

class _FakeResp:
    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _http_error(code: int, location: str | None = None) -> urllib.error.HTTPError:
    headers = email.message.Message()
    if location:
        headers["Location"] = location
    return urllib.error.HTTPError("https://probe.example", code, "probe", headers, None)


def test_head_reports_200(monkeypatch) -> None:
    import urllib.request
    monkeypatch.setattr(urllib.request, "build_opener",
                        lambda *h: type("O", (), {"open": lambda self, req, timeout: _FakeResp(200)})())
    r = hw._head_no_redirect("https://probe.example/ok")
    assert r == {"url": "https://probe.example/ok", "status": 200, "redirect": None}


def test_head_reports_302_with_location(monkeypatch) -> None:
    import urllib.request

    def raise_302(self, req, timeout):
        raise _http_error(302, "https://vercel.com/sso")

    monkeypatch.setattr(urllib.request, "build_opener",
                        lambda *h: type("O", (), {"open": raise_302})())
    r = hw._head_no_redirect("https://probe.example/redirect")
    assert r["status"] == 302 and r["redirect"] == "https://vercel.com/sso"


def test_head_reports_transport_error(monkeypatch) -> None:
    import urllib.request

    def raise_timeout(self, req, timeout):
        raise TimeoutError("timed out")

    monkeypatch.setattr(urllib.request, "build_opener",
                        lambda *h: type("O", (), {"open": raise_timeout})())
    r = hw._head_no_redirect("https://probe.example/dead")
    assert r["status"] is None and "TimeoutError" in r["error"]


def test_check_deployments_ok_only_needs_a_status(monkeypatch) -> None:
    monkeypatch.setattr(hw, "_deployment_urls",
                        lambda: (["https://a.example", "https://b.example"], "configs", []))
    monkeypatch.setattr(hw, "_head_no_redirect",
                        lambda u, timeout=10.0: {"url": u, "status": 302,
                                                 "redirect": "https://sso.example"})
    report = hw.check_deployments()
    assert report["ok"] is True and report["source"] == "configs"
    assert all(r["status"] == 302 for r in report["results"])


def test_check_deployments_fails_on_transport_error(monkeypatch) -> None:
    monkeypatch.setattr(hw, "_deployment_urls", lambda: (["https://a.example"], "env", []))
    monkeypatch.setattr(hw, "_head_no_redirect",
                        lambda u, timeout=10.0: {"url": u, "status": None, "error": "URLError: dead"})
    report = hw.check_deployments()
    assert report["ok"] is False


def test_main_check_deployments_exit_code_and_no_write(monkeypatch, capsys, tmp_path) -> None:
    state = tmp_path / "warm_state.json"
    monkeypatch.setattr(hw, "STATE", state)
    monkeypatch.setattr(hw, "_deployment_urls", lambda: (["https://a.example"], "default", ["note1"]))
    monkeypatch.setattr(hw, "_head_no_redirect",
                        lambda u, timeout=10.0: {"url": u, "status": 302,
                                                 "redirect": "https://sso.example"})
    monkeypatch.setattr(sys, "argv", ["hermes_warm_boot", "--check-deployments"])
    rc = hw.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert not state.exists(), "--check-deployments must not write warm_state.json"
    assert "302 redirect=https://sso.example" in out
    assert "verify with curl -I" in out
    assert "note: note1" in out

    monkeypatch.setattr(hw, "_head_no_redirect",
                        lambda u, timeout=10.0: {"url": u, "status": None, "error": "URLError: dead"})
    assert hw.main() == 1
