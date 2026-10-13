"""Tests for the key_wizard mirror-authorization babystep.

The token endpoint and device endpoint are MOCKED at the poster seam -
no live OAuth in this suite (no live OAuth without operator, ever).
Covered: the RFC 8628 poll loop (default interval 5, wait-before-each-
request, slow_down +5 for all subsequent, authorization_pending repeat,
expired_token/access_denied/expires_in aborts), the endpoint fence
(https-only, allowlisted host, private/loopback resolution refusal -
including against a LIVE local http.server), and the storage fence
(CR-strip at load, preserve-and-replace writes, kit-root confinement,
token never printed).

Run: pytest starter-kit/tests/test_key_wizard.py -q
"""
import http.server
import importlib.util
import socket
import threading
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1]
PROV = KIT / "tools" / "providers.json"

_spec = importlib.util.spec_from_file_location(
    "kit_key_wizard", KIT / "tools" / "key_wizard.py")
kw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kw)


@pytest.fixture
def github():
    return kw.load_providers(PROV)["github"]


@pytest.fixture
def timed():
    """Injected sleeper/clock pair: sleeps are recorded and advance the
    fake clock, so the poll loop's time behavior is fully observable."""
    calls: list[int] = []
    state = {"t": 0.0}

    def sleep(seconds):
        calls.append(seconds)
        state["t"] += seconds

    def now():
        return state["t"]

    return sleep, now, calls


# ------------------------------------------------------- storage fence

def test_load_env_cr_strip(tmp_path):
    p = tmp_path / ".env"
    p.write_bytes(b"GITHUB_TOKEN= ghp_abc123\r\nOTHER=x\r\nBARE=1\rLAST=2")
    env = kw.load_env(p)
    assert env["GITHUB_TOKEN"] == "ghp_abc123"
    assert "\r" not in env["GITHUB_TOKEN"]
    assert env["BARE"] == "1" and env["LAST"] == "2"


def test_load_env_strips_quotes_and_comments(tmp_path):
    p = tmp_path / ".env"
    p.write_bytes(b'K1="v1"\nK2=\'v2\'\nK3=v3\n# comment\nBROKEN\n')
    assert kw.load_env(p) == {"K1": "v1", "K2": "v2", "K3": "v3"}


def test_save_env_replaces_and_preserves(tmp_path, monkeypatch):
    monkeypatch.setattr(kw, "KIT_ROOT", tmp_path)
    p = tmp_path / ".env"
    p.write_bytes(b"# header\r\nA=1\r\nGITHUB_TOKEN=old\r\nB=2\r\n")
    kw.save_env_key(p, "GITHUB_TOKEN", "ghp_new")
    text = p.read_text(encoding="utf-8")
    assert "GITHUB_TOKEN=ghp_new" in text
    assert "old" not in text
    assert "A=1" in text and "B=2" in text and "# header" in text
    assert "\r" not in text and text.endswith("\n")


def test_save_env_fence_refuses_outside_kit(tmp_path):
    outside = tmp_path / "elsewhere" / ".env"
    with pytest.raises(kw.StorageFenceError):
        kw.save_env_key(outside, "K", "v")


def test_mask_never_reveals_full_token():
    m = kw.mask("ghp_1234567890abcdef")
    assert m != "ghp_1234567890abcdef"
    assert "1234567890" not in m


# ------------------------------------------------------- endpoint fence

def test_fence_refuses_non_https(github):
    with pytest.raises(kw.EndpointFenceError):
        kw.fence_url("http://github.com/login/device/code",
                     github["allowed_hosts"])


def test_fence_refuses_off_allowlist_host():
    with pytest.raises(kw.EndpointFenceError):
        kw.fence_url("https://evil.example.com/x", ["github.com"])


def test_fence_refuses_private_resolution(monkeypatch):
    def fake_getaddrinfo(host, port, **_):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "",
                 ("10.0.0.5", port))]
    monkeypatch.setattr(socket, "getaddrinfo", fake_getaddrinfo)
    with pytest.raises(kw.EndpointFenceError):
        kw.assert_public_host("github.com")


def test_fence_refuses_live_loopback_server():
    """Against a REAL local http.server: allowlisting the host cannot save
    it - the resolution half of the fence refuses loopback IPs."""
    srv = http.server.HTTPServer(("127.0.0.1", 0),
                                 http.server.BaseHTTPRequestHandler)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        with pytest.raises(kw.EndpointFenceError):
            kw.fence_url(f"https://127.0.0.1:{port}/token", ["127.0.0.1"])
    finally:
        srv.shutdown()


# ------------------------------------------------------------ poll loop

def test_poll_default_interval_5_and_pending_repeat(github, timed):
    sleep, now, calls = timed
    responses = [{"error": "authorization_pending"},
                 {"error": "authorization_pending"},
                 {"access_token": "ghp_tok"}]
    bodies = []

    def poster(url, data, hosts):
        bodies.append(dict(data))
        return responses.pop(0)

    tok = kw.poll_for_token(github, "devcode", "cid", interval=None,
                            expires_in=900, poster=poster,
                            sleeper=sleep, clock=now)
    assert tok == "ghp_tok"
    assert calls == [5, 5, 5]  # RFC 8628: MUST use 5 when server sent none
    assert bodies[0]["grant_type"] == kw.GRANT_DEVICE
    assert bodies[0]["device_code"] == "devcode"
    assert bodies[0]["client_id"] == "cid"


def test_poll_slow_down_grows_all_subsequent(github, timed):
    sleep, now, calls = timed
    responses = [{"error": "authorization_pending"},
                 {"error": "slow_down"},
                 {"error": "authorization_pending"},
                 {"access_token": "t"}]
    kw.poll_for_token(github, "d", "c", interval=None, expires_in=900,
                      poster=lambda *a: responses.pop(0),
                      sleeper=sleep, clock=now)
    assert calls == [5, 5, 10, 10]  # +5 for this and ALL subsequent requests


def test_poll_expired_token_aborts(github, timed):
    sleep, now, calls = timed
    hits = {"n": 0}

    def poster(url, data, hosts):
        hits["n"] += 1
        return {"error": "expired_token"}

    with pytest.raises(kw.FlowError, match="expired"):
        kw.poll_for_token(github, "d", "c", interval=None, expires_in=900,
                          poster=poster, sleeper=sleep, clock=now)
    assert hits["n"] == 1


def test_poll_access_denied_aborts(github, timed):
    sleep, now, _ = timed
    with pytest.raises(kw.FlowError, match="denied"):
        kw.poll_for_token(github, "d", "c", interval=None, expires_in=900,
                          poster=lambda *a: {"error": "access_denied"},
                          sleeper=sleep, clock=now)


def test_poll_expires_in_budget_stops_loop(github, timed):
    sleep, now, calls = timed
    hits = {"n": 0}

    def poster(url, data, hosts):
        hits["n"] += 1
        return {"error": "authorization_pending"}

    with pytest.raises(kw.FlowError, match="budget"):
        kw.poll_for_token(github, "d", "c", interval=None, expires_in=12,
                          poster=poster, sleeper=sleep, clock=now)
    assert hits["n"] == 2
    assert calls == [5, 5, 5]


def test_poll_unexpected_error_is_loud(github, timed):
    sleep, now, _ = timed
    with pytest.raises(kw.FlowError, match="unsupported_grant_type"):
        kw.poll_for_token(github, "d", "c", interval=None, expires_in=900,
                          poster=lambda *a: {"error": "unsupported_grant_type"},
                          sleeper=sleep, clock=now)


# -------------------------------------------------- end-to-end (mocked)

def test_device_flow_end_to_end_mocked(github, tmp_path, monkeypatch,
                                       capsys, timed):
    sleep, now, calls = timed
    monkeypatch.setattr(kw, "KIT_ROOT", tmp_path)
    env = tmp_path / ".env"
    opened = []
    responses = {
        github["device_code_endpoint"]: [
            {"device_code": "DEV", "user_code": "ABCD-1234",
             "verification_uri": "https://github.com/login/device",
             "interval": 5, "expires_in": 900}],
        github["token_endpoint"]: [
            {"error": "authorization_pending"},
            {"access_token": "ghp_SECRETVALUE123"}],
    }
    urls = []

    def poster(url, data, hosts):
        urls.append(url)
        return responses[url].pop(0)

    token = kw.run_device_flow(github, "cid123", env, live=True,
                               poster=poster, opener=opened.append)
    assert token == "ghp_SECRETVALUE123"
    assert opened == ["https://github.com/login/device"]
    assert urls == [github["device_code_endpoint"],
                    github["token_endpoint"], github["token_endpoint"]]
    assert kw.load_env(env)["GITHUB_TOKEN"] == "ghp_SECRETVALUE123"
    out = capsys.readouterr().out
    assert "ABCD-1234" in out          # the user code IS printed (operator needs it)
    assert "ghp_SECRETVALUE123" not in out  # the token is NEVER printed
    assert "ghp_...18" in out               # only the masked form


def test_device_flow_dry_run_zero_network(github, tmp_path, capsys):
    def bomb(*a, **k):
        raise AssertionError("network call in dry-run")
    token = kw.run_device_flow(github, "cid", tmp_path / ".env",
                               live=False, poster=bomb, opener=bomb)
    assert token == ""
    out = capsys.readouterr().out
    assert "https://github.com/login/device/code" in out
    assert "fence" in out


def test_device_flow_refuses_unimplemented_flow(tmp_path):
    google = kw.load_providers(PROV)["google"]
    with pytest.raises(kw.FlowError, match="later stretch"):
        kw.run_device_flow(google, "cid", tmp_path / ".env", live=True)


def test_manual_flow_hides_paste_and_stores(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(kw, "KIT_ROOT", tmp_path)
    monkeypatch.setattr(kw.getpass, "getpass",
                        lambda prompt="": "gsk_SECRETKEY99\r\n")
    groq = kw.load_providers(PROV)["groq"]
    env = tmp_path / ".env"
    key = kw.run_manual_flow(groq, env, live=True)
    assert key == "gsk_SECRETKEY99"
    assert kw.load_env(env)["GROQ_API_KEY"] == "gsk_SECRETKEY99"
    assert "gsk_SECRETKEY99" not in capsys.readouterr().out


def test_manual_flow_disabled_row_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(kw, "KIT_ROOT", tmp_path)
    groq = dict(kw.load_providers(PROV)["groq"], enabled=False)
    with pytest.raises(kw.FlowError, match="disabled"):
        kw.run_manual_flow(groq, tmp_path / ".env", live=True)


# ------------------------------------------------------- providers table

def test_providers_table_is_data_not_code():
    table = kw.load_providers(PROV)
    assert set(table) == {"github", "google", "openrouter", "groq"}
    gh = table["github"]
    assert gh["flow"] == "device" and gh["enabled"] is True
    assert gh["device_code_endpoint"] == "https://github.com/login/device/code"
    assert gh["token_endpoint"] == "https://github.com/login/oauth/access_token"
    assert gh["allowed_hosts"] == ["github.com"]
    assert gh["interval_default"] == 5 and gh["expires_in_default"] == 900
    for row in table.values():
        if row.get("enabled"):
            assert row.get("env_key"), row["name"]
            if row["flow"] == "device":
                assert row.get("allowed_hosts") and row.get("device_code_endpoint")


# ------------------------------------------------------------------ cli

def test_cli_list_prints_table(capsys):
    assert kw.main(["list", "--providers", str(PROV)]) == 0
    out = capsys.readouterr().out
    assert "github" in out and "groq" in out


def test_cli_dry_run_is_the_default(capsys):
    """No --live: plan printed, exit 0, zero packets (the run_device_flow
    dry-run test bombs the poster; here the real default path is used)."""
    assert kw.main(["github", "--providers", str(PROV)]) == 0
    assert "flow     : device" in capsys.readouterr().out


def test_cli_unknown_provider_exit_2(capsys):
    assert kw.main(["nosuchprovider", "--providers", str(PROV)]) == 2


def test_cli_refuses_unimplemented_flow_exit_2(capsys):
    assert kw.main(["google", "--providers", str(PROV)]) == 2


def test_cli_device_live_without_client_id_exits_1(capsys, monkeypatch,
                                                   tmp_path):
    """Sealed: no env var, empty .env - the live attempt can only fail at
    the client_id gate, never reach the network."""
    monkeypatch.delenv("KEY_WIZARD_GITHUB_CLIENT_ID", raising=False)
    empty = tmp_path / ".env"
    empty.write_bytes(b"")
    assert kw.main(["github", "--live", "--providers", str(PROV),
                    "--env", str(empty)]) == 1
    assert "client_id" in capsys.readouterr().err
