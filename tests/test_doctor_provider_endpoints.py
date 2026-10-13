"""t86 (2026-09-25): route-correct provider health surface in mag/doctor.

The operator probed saelis (connection refused) and ollama (404 on GET /v1)
in a browser and could not tell dead from alive. These tests pin the probe
matrix in check_provider_endpoints():

  - a refused local TCP endpoint classifies DOWN (the saelis case)
  - an ollama-shaped local endpoint is judged by native /api/tags only
    (served here by a real loopback HTTP server), and the probe never
    touches GET /v1, the POST-only route that caused the false alarm
  - a dormant provider is a declared state: not probed, never an alarm
  - probes dedupe on (style, base_url)

Fixture is a tmp providers.yaml parsed with the estate load pattern.
"""
from __future__ import annotations

import http.server
import json
import socket
import sys
import threading
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import doctor  # noqa: E402


class _TagsHandler(http.server.BaseHTTPRequestHandler):
    requested_paths: list[str] = []

    def do_GET(self):  # noqa: N802
        type(self).requested_paths.append(self.path)
        if self.path == "/api/tags":
            body = json.dumps({"models": [{"name": "gemma:2b"}]}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):  # silence the test run
        pass


@pytest.fixture()
def tags_server():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _TagsHandler)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:%d/v1" % srv.server_address[1]
    srv.shutdown()
    srv.server_close()
    _TagsHandler.requested_paths.clear()


@pytest.fixture()
def dead_port():
    """A loopback port that reliably refuses: bind one, then close it.

    Low fixed ports (e.g. :1) are silently dropped on some Windows boxes
    (connect times out instead of refusing), so the DOWN-by-refusal case
    needs a port the TCP stack itself just released.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _write_fixture(path: Path, ollama_base: str, dead_port: int) -> Path:
    path.write_text(
        "# tmp fixture\n"
        "providers:\n"
        "  ollama:\n"
        "    kind: openai_compat\n"
        "    base_url: %s\n"
        "  deadlocal:\n"
        "    kind: openai_compat\n"
        "    base_url: http://127.0.0.1:%d/v1\n"
        "  deadlocal2:\n"
        "    kind: openai_compat\n"
        "    base_url: http://127.0.0.1:%d/v1\n"
        "  saelis:\n"
        "    kind: openai_compat\n"
        "    dormant: true\n"
        "    base_url: http://127.0.0.1:%d/v1\n"
        "  paidremote:\n"
        "    kind: openai_compat\n"
        "    base_url: https://api.example.invalid/v1\n"
        "    api_key_env: T86_NO_SUCH_KEY_ENV\n" % (ollama_base, dead_port, dead_port, dead_port),
        encoding="utf-8",
    )
    return path


def _statuses(result):
    return result["statuses"]


def test_refused_local_tcp_is_down(tmp_path, tags_server, dead_port):
    cfg = _write_fixture(tmp_path / "providers.yaml", tags_server, dead_port)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = _statuses(r)
    assert s["deadlocal"] == "DOWN"
    assert r["ok"] is False
    dead = [p for p in r["providers"] if p["provider"] == "deadlocal"][0]
    assert ("refused" in dead["detail"]) or ("timed out" in dead["detail"]), "DOWN must name its failure mode; this box SYN-drops closed ports (timeout) instead of refusing [t86 close fix 09-26]"
    assert dead["probe"] == "tcp+models"
    assert any("deadlocal" in i for i in r["issues"])


def test_ollama_tags_shape_is_alive(tmp_path, tags_server, dead_port):
    cfg = _write_fixture(tmp_path / "providers.yaml", tags_server, dead_port)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = _statuses(r)
    assert s["ollama"] == "ALIVE"
    row = [p for p in r["providers"] if p["provider"] == "ollama"][0]
    assert row["probe"] == "api_tags"
    assert "1 models tagged" in row["detail"]
    # Negative made explicit: the probe hit the native route only. GET /v1
    # (POST-only route, the operator's false alarm) was never sent.
    assert _TagsHandler.requested_paths == ["/api/tags"]


def test_dormant_is_state_not_alarm(tmp_path, tags_server, dead_port):
    cfg = _write_fixture(tmp_path / "providers.yaml", tags_server, dead_port)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = _statuses(r)
    assert s["saelis"] == "DORMANT"
    row = [p for p in r["providers"] if p["provider"] == "saelis"][0]
    assert row["probe"] == "none(dormant)"
    # Its base_url is a dead port; had it been probed it would read DOWN.
    # DORMANT must therefore come from the marker, not from a probe.
    assert "declared state" in row["detail"]
    assert not any("saelis" in i for i in r["issues"])


def test_remote_lanes_config_only_and_probes_dedupe(tmp_path, tags_server, dead_port):
    cfg = _write_fixture(tmp_path / "providers.yaml", tags_server, dead_port)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = _statuses(r)
    assert s["paidremote"] == "REMOTE-UNVERIFIED"
    row = [p for p in r["providers"] if p["provider"] == "paidremote"][0]
    assert row["probe"] == "none(config-only)"
    assert "paidremote" in r["unverified"]
    # deadlocal + deadlocal2 share one base_url: one tcp probe total,
    # plus the single ollama api_tags probe.
    assert r["probes_run"] == 2


def test_wired_into_examine():
    report = doctor.examine()
    names = [c["check"] for c in report.checks]
    assert "provider_endpoints" in names


# ═══════════════════════════════════════════════════════════════════
# B2-04 (2026-09-26): the DEEP remote probe (MAG_PROBE_REMOTE=1).
# A models-only GET 200 is NOT liveness: cerebras (402), nvidia (410),
# gemini (401) and mistral (429 with x-ratelimit limits literally 0) all
# served /models 200 with zero usable inference. These tests replay each
# measured response shape off a fake lane server and pin the class map.
# Receipt: watch/inbox/PROVIDER_HEALTH_20260926.md.
# ═══════════════════════════════════════════════════════════════════

_PONG = {"choices": [{"message": {"content": "pong"}, "finish_reason": "stop"}]}

# lane-name -> chat response shape (models always 200 unless models_status)
DEEP_SCENARIOS = {
    "alive": {"chat": (200, _PONG, {})},
    "cerebras": {"chat": (402, "", {})},
    "nvidia": {"chat": (410, "", {})},
    "gemini": {"chat": (401, '{ "error": { "code": 401, "message": "API keys are not '
                       'supported by this API.", "status": "UNAUTHENTICATED" } }', {})},
    "mistral": {"chat": (429, "", {"x-ratelimit-limit-req-minute": "0",
                                   "x-ratelimit-remaining-req-minute": "0"})},
    "zai": {"chat": (429, '{"error":{"code":"1305","message":"The service may be '
                    'temporarily overloaded, please try again later"}}', {})},
    "budget": {"chat": (200, {"choices": [{"message": {"content": ""},
                                           "finish_reason": "length"}]}, {})},
    "modelsdead": {"models_status": 500, "chat": (200, _PONG, {})},
    "pair": {"chat": (200, _PONG, {})},
}


class _DeepLaneHandler(http.server.BaseHTTPRequestHandler):
    """Fake remote lanes under /sim/<name>/; logs every request."""
    scenarios: dict = {}
    requests: list = []
    post_bodies: list = []

    def do_GET(self):  # noqa: N802
        type(self).requests.append(("GET", self.path))
        name, suffix = _split_sim(self.path)
        if name is None:
            self.send_response(404)
            self.end_headers()
            return
        sc = type(self).scenarios.get(name, {})
        if suffix == "models":
            code = int(sc.get("models_status", 200))
            body = json.dumps({"data": [{"id": "test-model-a"}]}).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):  # noqa: N802
        type(self).requests.append(("POST", self.path))
        length = int(self.headers.get("Content-Length") or 0)
        type(self).post_bodies.append(self.rfile.read(length))
        name, suffix = _split_sim(self.path)
        if name is None or suffix != "chat/completions":
            self.send_response(404)
            self.end_headers()
            return
        sc = type(self).scenarios.get(name, {})
        code, body, headers = sc.get("chat", (200, _PONG, {}))
        raw = body.encode("utf-8") if isinstance(body, str) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):  # silence the test run
        pass


def _split_sim(path: str):
    parts = path.strip("/").split("/")
    if len(parts) >= 3 and parts[0] == "sim":
        return parts[1], "/".join(parts[2:])
    return None, None


@pytest.fixture()
def deep_server(monkeypatch):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _DeepLaneHandler)
    _DeepLaneHandler.scenarios = dict(DEEP_SCENARIOS)
    _DeepLaneHandler.requests = []
    _DeepLaneHandler.post_bodies = []
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    # The fake lanes must classify as REMOTE for the probe matrix to route
    # them through the deep probe; drop loopback from the local-host set so
    # 127.0.0.1 test servers stand in for api.<provider> hosts.
    monkeypatch.setattr(doctor, "_LOCAL_HOSTS", {"localhost", "::1", "0.0.0.0"})
    monkeypatch.setenv("T86_DEEP_KEY", "test-key-1-never-log-me")
    monkeypatch.setenv("T86_DEEP_KEY_2", "test-key-2-never-log-me")
    monkeypatch.delenv("T86_NO_SUCH_KEY_ENV", raising=False)
    yield "http://127.0.0.1:%d" % srv.server_address[1]
    srv.shutdown()
    srv.server_close()


def _write_deep_fixture(path: Path, root: str) -> Path:
    def lane(name, key_env="T86_DEEP_KEY", extra="", sim=None):
        return (
            "  %s:\n"
            "    kind: openai_compat\n"
            "    base_url: %s/sim/%s\n"
            "    api_key_env: %s\n"
            "    default_model: test-model-a\n"
            "%s" % (name, root, sim or name, key_env, extra)
        )

    path.write_text(
        "# tmp deep fixture (B2-04)\n"
        "providers:\n"
        + lane("alive")
        + lane("cerebras")
        + lane("nvidia")
        + lane("gemini")
        + lane("mistral")
        + lane("zai")
        + lane("budget")
        + lane("modelsdead")
        + lane("fenced", extra="    opencode_only: true\n")
        + lane("nokey", key_env="T86_NO_SUCH_KEY_ENV")
        + lane("nomodel").replace("    default_model: test-model-a\n", "")
        # pair1 + pair2: DIFFERENT provider ids sharing ONE base_url, model
        # and key -> the deep probe must dedupe them to a single ping.
        # pair3: same base_url + model, DIFFERENT key -> its own probe.
        + lane("pair1", sim="pair")
        + lane("pair2", sim="pair")
        + lane("pair3", key_env="T86_DEEP_KEY_2", sim="pair"),
        encoding="utf-8",
    )
    return path


def test_default_stays_config_only_no_deep_bytes(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    assert set(r["statuses"].values()) == {"REMOTE-UNVERIFIED"}
    assert r["probes_run"] == 0
    assert _DeepLaneHandler.requests == [], "default path must send zero bytes to remote lanes"


def test_deep_probe_alive_and_ping_shape(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["alive"] == "ALIVE"
    row = [p for p in r["providers"] if p["provider"] == "alive"][0]
    assert row["probe"] == "remote_models+chat"
    assert "chat ping 200" in row["detail"]
    # ping law: exactly one POST per probed triple, 1-token budget, the
    # synthetic public prompt only (never repo or private content).
    posts = [(m, p) for m, p in _DeepLaneHandler.requests if m == "POST" and "/sim/alive/" in p]
    assert len(posts) == 1
    payload = json.loads(_DeepLaneHandler.post_bodies[-1]) if _DeepLaneHandler.post_bodies else {}
    for body in _DeepLaneHandler.post_bodies:
        pl = json.loads(body)
        assert pl["max_tokens"] == 1
        assert pl["messages"][0]["content"] == "Reply with the single word: pong."
    # The fixture deliberately contains quota/auth-dead lanes, so the check
    # as a whole is red; the alive lane itself must raise no issue.
    assert not any("'alive'" in i for i in r["issues"])
    # key values never leak into any detail string
    assert "never-log-me" not in json.dumps(r)


def test_deep_quota_dead_classes(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["cerebras"] == "QUOTA-DEAD"
    row = [p for p in r["providers"] if p["provider"] == "cerebras"][0]
    assert "402" in row["detail"] and "cerebras class" in row["detail"]
    assert s["nvidia"] == "QUOTA-DEAD"
    row = [p for p in r["providers"] if p["provider"] == "nvidia"][0]
    assert "410" in row["detail"]
    # zero-limit 429 is the mistral shape: 429 but QUOTA-DEAD, not DEGRADED
    assert s["mistral"] == "QUOTA-DEAD"
    row = [p for p in r["providers"] if p["provider"] == "mistral"][0]
    assert "zero rate-limit" in row["detail"]
    assert r["ok"] is False
    assert sum(1 for i in r["issues"] if i.startswith("PROVIDER QUOTA DEAD")) == 3


def test_deep_auth_dead_class(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["gemini"] == "AUTH-DEAD"
    row = [p for p in r["providers"] if p["provider"] == "gemini"][0]
    assert "401" in row["detail"] and "gemini class" in row["detail"]
    assert r["ok"] is False
    assert any(i.startswith("PROVIDER AUTH DEAD") and "'gemini'" in i for i in r["issues"])


def test_deep_1305_is_degraded_not_alarm(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["zai"] == "DEGRADED"
    row = [p for p in r["providers"] if p["provider"] == "zai"][0]
    assert "1305" in row["detail"] and "z_ai" in row["detail"]
    # DEGRADED is a state, not an alarm (should_burst owns 1305 retry at
    # call time): the zai lane raises no issue even though the fixture's
    # quota/auth-dead lanes keep the check red overall.
    assert not any("'zai'" in i for i in r["issues"])
    assert "zai" in r["degraded"]


def test_deep_fences_and_keyless(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["fenced"] == "FENCED"
    assert "fenced" in r["fenced"]
    assert s["nokey"] == "REMOTE-UNVERIFIED"
    assert s["nomodel"] == "REMOTE-UNVERIFIED"
    row = [p for p in r["providers"] if p["provider"] == "nokey"][0]
    assert row["probe"] == "none(no-key)"
    row = [p for p in r["providers"] if p["provider"] == "nomodel"][0]
    assert row["probe"] == "none(no-model)"
    # fences judged BEFORE any byte leaves: no request ever hit those lanes
    touched = {p.split("/")[2] for _, p in _DeepLaneHandler.requests if "/sim/" in p}
    assert "fenced" not in touched
    assert "nokey" not in touched
    assert "nomodel" not in touched


def test_deep_models_dead_is_down(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["modelsdead"] == "DOWN"
    assert r["ok"] is False
    assert any(i.startswith("PROVIDER ENDPOINT DOWN") and "'modelsdead'" in i for i in r["issues"])


def test_deep_empty_reasoning_budget_is_alive(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["budget"] == "ALIVE"
    row = [p for p in r["providers"] if p["provider"] == "budget"][0]
    assert "finish=length" in row["detail"] and "reasoning" in row["detail"]


def test_deep_dedupe_on_base_model_key_triple(deep_server, tmp_path):
    cfg = _write_deep_fixture(tmp_path / "providers.yaml", deep_server)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    # pair1 + pair2 share base/model/key -> ONE probe; pair3 has its own key
    # -> its own probe. lanes probed: alive cerebras nvidia gemini mistral
    # zai budget modelsdead pair(x2 keys) = 10 probes for 13 remote rows.
    assert s["pair1"] == s["pair2"] == s["pair3"] == "ALIVE"
    assert r["probes_run"] == 10
    pair_posts = [p for _, p in _DeepLaneHandler.requests if "/sim/pair/" in p and "chat" in p]
    assert len(pair_posts) == 2


# ═══════════════════════════════════════════════════════════════════
# B2-107 (2026-09-26): the OLLAMA_HOST locality law.
# The trap, measured live on the host before this pin existed:
# OLLAMA_HOST=http://ollama:11434 (a docker-network name) made the free
# local eye classify REMOTE, so the default path read REMOTE-UNVERIFIED
# with the api_tags probe never firing, and MAG_PROBE_REMOTE=1 read a
# generic DOWN "GET /models failed URLError" that named no disease. A
# local-declared lane on an unresolvable host must read DOWN none(locality)
# in the default path, zero bytes; a RESOLVABLE non-local ollama (LAN box)
# must stay REMOTE-UNVERIFIED. Receipt:
# watch/inbox/burn_wave_20260926/B2_107_ollama_trap_20260926.md
# ═══════════════════════════════════════════════════════════════════


def _write_locality_fixture(path: Path) -> Path:
    path.write_text(
        "# tmp locality fixture (B2-107)\n"
        "providers:\n"
        "  ollama:\n"
        "    kind: openai_compat\n"
        "    base_url_env: OLLAMA_HOST\n"
        "    api_key_default: ollama\n"
        "  relay:\n"
        "    kind: openai_compat\n"
        "    base_url: http://lane-relay.invalid:11434/v1\n"
        "  freelocal:\n"
        "    kind: openai_compat\n"
        "    base_url: http://lane-free.invalid/v1\n"
        "    free_local: true\n"
        "  paidremote:\n"
        "    kind: openai_compat\n"
        "    base_url: https://api.example.invalid/v1\n"
        "    api_key_env: T86_NO_SUCH_KEY_ENV\n"
        "  saelis:\n"
        "    kind: openai_compat\n"
        "    dormant: true\n"
        "    base_url: http://lane-dormant.invalid/v1\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture()
def no_dns(monkeypatch):
    """Every name fails to resolve unless the test says otherwise."""
    monkeypatch.setattr(doctor, "_host_resolves", lambda host: False, raising=False)
    return monkeypatch


def test_b2_107_docker_name_locality_down(no_dns, tmp_path, monkeypatch):
    cfg = _write_locality_fixture(tmp_path / "providers.yaml")
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama:11434")
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = r["statuses"]
    # All three local-declared arms (id, :11434 port, free_local) read DOWN.
    assert s["ollama"] == "DOWN"
    assert s["relay"] == "DOWN"
    assert s["freelocal"] == "DOWN"
    row = [p for p in r["providers"] if p["provider"] == "ollama"][0]
    assert row["probe"] == "none(locality)"
    assert row["base_url"] == "http://ollama:11434", "law must judge the base_url_env resolution"
    assert "does not resolve" in row["detail"] and "locality" in row["detail"]
    assert r["ok"] is False
    assert any(i.startswith("PROVIDER ENDPOINT DOWN") and "'ollama'" in i for i in r["issues"])
    # Default path, zero network probes: the law is config-only (getaddrinfo).
    assert r["probes_run"] == 0
    assert set(r["unverified"]) == {"paidremote"}
    # Dormant stays a declared state; the law never wakes it.
    assert s["saelis"] == "DORMANT"


def test_b2_107_law_bites_before_deep_probe_bytes(no_dns, tmp_path, monkeypatch):
    cfg = _write_locality_fixture(tmp_path / "providers.yaml")
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama:11434")
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0, probe_remote=True)
    s = r["statuses"]
    assert s["ollama"] == "DOWN"
    row = [p for p in r["providers"] if p["provider"] == "ollama"][0]
    assert row["probe"] == "none(locality)", (
        "deep probe must never spend bytes on a host this seat cannot resolve"
    )
    assert r["probes_run"] == 0


def test_b2_107_resolvable_lan_ollama_stays_remote(no_dns, tmp_path, monkeypatch):
    cfg = _write_locality_fixture(tmp_path / "providers.yaml")
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama:11434")
    # A name that DOES resolve (LAN ollama, tunnel) is a genuine remote lane:
    # the law must not eat it, the pre-B2-04 config-only contract stands.
    no_dns.setattr(doctor, "_host_resolves", lambda host: True, raising=False)
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    s = r["statuses"]
    assert s["ollama"] == "REMOTE-UNVERIFIED"
    row = [p for p in r["providers"] if p["provider"] == "ollama"][0]
    assert row["probe"] == "none(config-only)"
    assert "ollama" in r["unverified"]
    assert r["probes_run"] == 0


# ═══════════════════════════════════════════════════════════════════
# B2-489 (2026-09-26): the resolver bound.
# The B2-107 pins monkeypatch _host_resolves whole, so nothing pinned the
# seam's own socket layer: a resolver that BLACKHOLES a lookup (accepts
# the query, never answers) makes socket.getaddrinfo block past every
# documented timeout, because Windows DNS resolution is not covered by
# urllib timeouts (the exact disease models.registry.ollama_tags names
# for its daemon-thread probe). These pins patch socket.getaddrinfo one
# layer down and pin the bound itself: a blackholed lookup reads
# unresolvable in bounded time at the seam, and check_provider_endpoints
# completes with the locality classification instead of holding the
# whole examine() report hostage. Pre-bound measurement (red run, this
# lane): both deadline pins took >= 30s with the 30s sleeper, zero red
# pins before. Receipt:
# watch/inbox/burn_wave_20260926/B2_489_resolver_bound_20260926.md
# ═══════════════════════════════════════════════════════════════════


def _blackhole_resolver(host, *args, **kwargs):
    """Stand-in for a DNS server that accepts the query and never answers.

    Returns a real-looking answer AFTER 30s; the deadline must fire long
    before the answer arrives. Signature absorbs the None port kwarg.
    """
    time.sleep(30.0)
    return [(2, 1, 6, "", ("10.255.255.1", 0))]


def test_b2_489_blackholed_resolver_reads_unresolvable_bounded(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", _blackhole_resolver)
    t0 = time.monotonic()
    ok = doctor._host_resolves("b2-489-blackhole.invalid")
    elapsed = time.monotonic() - t0
    assert ok is False, "a lookup that never answers inside the deadline reads unresolvable"
    assert elapsed < 10.0, "seam must return inside its deadline, took %.1fs" % elapsed


def test_b2_489_check_completes_under_blackholed_dns(tmp_path, monkeypatch):
    cfg = tmp_path / "providers.yaml"
    cfg.write_text(
        "# tmp blackhole fixture (B2-489)\n"
        "providers:\n"
        "  ollama:\n"
        "    kind: openai_compat\n"
        "    base_url_env: OLLAMA_HOST\n"
        "    api_key_default: ollama\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama:11434")
    monkeypatch.setattr(socket, "getaddrinfo", _blackhole_resolver)
    t0 = time.monotonic()
    r = doctor.check_provider_endpoints(config_path=cfg, timeout=2.0)
    elapsed = time.monotonic() - t0
    # The brief's falsifier: pre-bound this exact shape took >= 30s (the
    # sleeper answered inside the call) and the lane misread as reachable.
    assert elapsed < 15.0, "doctor must not hold the report hostage on DNS, took %.1fs" % elapsed
    s = r["statuses"]
    assert s["ollama"] == "DOWN", "bounded-time unresolvable reads the same as unresolvable"
    row = [p for p in r["providers"] if p["provider"] == "ollama"][0]
    assert row["probe"] == "none(locality)"
    assert r["probes_run"] == 0


def test_b2_489_seam_socket_paths_green_side(monkeypatch):
    # Regression guard for the live socket contract under the deadline
    # wrapper: a fast answer resolves True, a resolver error reads False.
    # Green on both sides by design (pre-bound code had the same mapping).
    monkeypatch.setattr(socket, "getaddrinfo", lambda h, *a, **k: [(2, 1, 6, "", (h, 0))])
    assert doctor._host_resolves("b2-489-fast.invalid") is True

    def _gaierror(host, *args, **kwargs):
        raise socket.gaierror(11001, "getaddrinfo failed")

    monkeypatch.setattr(socket, "getaddrinfo", _gaierror)
    assert doctor._host_resolves("b2-489-gaierror.invalid") is False


def test_b2_457_403_tier_not_allowed_reads_auth_dead():
    # B2-457: the mistral-large-latest body (B2-105 live bytes) is the
    # defining byte for the 403 arm: a per-key tier fact with AUTH-DEAD
    # semantics, not the generic DOWN outage catch-all it used to fall to.
    body = ('{"object":"error","message":"This model is not available in your '
            'subscription tier","type":"tier_not_allowed","param":null,'
            '"code":"1910","raw_status_code":403}')
    verdict = doctor._classify_chat_failure(403, body, {})
    assert verdict["status"] == "AUTH-DEAD"
    assert "tier not allowed" in verdict["detail"]
    assert "waiting never fixes it" in verdict["detail"]
    assert "1910" in verdict["detail"] or "tier_not_allowed" in verdict["detail"] or "subscription" in verdict["detail"]
    # a 403 with an unrelated body still lands in the same per-key class
    verdict2 = doctor._classify_chat_failure(403, "forbidden by policy", {})
    assert verdict2["status"] == "AUTH-DEAD"
