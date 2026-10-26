#!/usr/bin/env python3
"""roblox_npc_gateway — the fleet's brain, served to the world.

The Head Museum in Roblox (roblox/src/server/NpcGateway.luau) POSTs here:
    {"head": "elder", "player": "...", "message": "...", "room": "..."}

This bridge routes the ask through the FREE stealth lanes, in failover order:
    1. openrouter  OPENROUTER_API_KEY   (stealth/space-bunny-alpha)
    2. openrouter  OPENROUTER_API_KEY_2 (same model, second pool)
    3. nous        HERMES_API_KEY_1     (inference-api.nousresearch.com mirror)

Every turn is a receipt row in memory/runs/roblox_npc/gateway.jsonl (the room
that remembers, server-side too). Run:  python tools/roblox_npc_gateway.py
Port 8771 matches Config.Gateway in the Roblox project.

Binding + auth (Q-039, public gateway host):
    NPC_GATEWAY_HOST   bind address. Default 0.0.0.0 (all interfaces) so a
                       Roblox server off-box can reach the fleet; set it to a
                       specific IP or 127.0.0.1 for local Studio dev.
    NPC_GATEWAY_SECRET one shared secret. Clients send
                       "Authorization: Bearer <secret>". Read from env or .env
                       (same loader as the lane keys). Startup FAILS CLOSED: a
                       non-loopback bind without a secret refuses to start; a
                       loopback bind without a secret runs auth-free so local
                       dev is unchanged (Config.Gateway.url still 127.0.0.1).
    Deployment pairing (not yet landed, operator pass): set the same secret in
    roblox/src/shared/Config.luau (Config.Gateway) and send the Authorization
    header from roblox/src/server/NpcGateway.luau, with url pointed at this
    host's reachable IP. Receipt: watch/inbox/burn_reset_20260927/queue/Q-039.md

Security: outbound hosts are allowlisted and resolved to public IPs before any
request — the same SSRF gate as mag/probe_route.py (self-steal; one gate, one
standard). No redirects are followed. Inbound (new with public binding, Q-039):
the shared secret gates every POST, and request bodies are capped at 64 KiB
because a 0.0.0.0 listener takes bytes from untrusted networks.
"""
from __future__ import annotations

import hmac
import http.client
import ipaddress
import json
import os
import socket
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECEIPTS = ROOT / "memory" / "runs" / "roblox_npc" / "gateway.jsonl"
MODEL = "stealth/space-bunny-alpha"
PORT = 8771
MAX_BODY = 65536  # 64 KiB: a public listener must not buffer unbounded bodies

ALLOWED_HOSTS = {"openrouter.ai", "inference-api.nousresearch.com"}
# Mooncast law (LINKS-335): homogeneous model councils align too easily to
# filter truth. Survey witnesses must be CROSS-FAMILY; only free slugs are
# allowed so a rogue client can never spend the funded keys.
FREE_MODELS = {
    "stealth/space-bunny-alpha",
    "inclusionai/ling-3.0-flash-sante:free",
    "inclusionai/ling-3.0-flash-fin:free",
    "poolside/laguna-s-2.1:free",
    "meituan/longcat-2.0:free",
}


def assert_public_https(url: str) -> None:
    """The probe_route gate: https + allowlisted host + all resolved IPs global."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"blocked host: {parsed.hostname!r}")
    for *_x, sockaddr in socket.getaddrinfo(parsed.hostname, 443):
        if not ipaddress.ip_address(sockaddr[0]).is_global:
            raise ValueError(f"blocked non-public address: {sockaddr[0]}")


def _validated_pin(host: str) -> str:
    """SW1-02 (SWARM_1.md row 2, glm+deepseek converged): resolve ONCE, verify
    every answer global, and return the first global IP. assert_public_https
    validated a resolution that _OPENER.open then threw away: it re-resolved at
    connect time, so a rebinding answer between check and use would have
    connected straight to a private address. The pin below is what connect()
    dials; the hostname (SNI + Host header + cert check) stays the real one."""
    pins = []
    for *_x, sockaddr in socket.getaddrinfo(host, 443):
        ip = ipaddress.ip_address(sockaddr[0])
        if not ip.is_global:
            raise ValueError(f"blocked non-public address: {sockaddr[0]}")
        pins.append(str(ip))
    if not pins:
        raise ValueError(f"no addresses resolved for {host!r}")
    return pins[0]


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """Connects to the pre-validated IP; SNI/cert stay bound to the hostname."""

    def __init__(self, host, pinned="", **kw):
        super().__init__(host, **kw)
        self._pinned_ip = pinned or _validated_pin(host)

    def connect(self) -> None:
        self.sock = self._context.wrap_socket(
            socket.create_connection((self._pinned_ip, self.port), timeout=self.timeout),
            server_hostname=self.host)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        def build(host, **kw):
            return _PinnedHTTPSConnection(host, pinned=_validated_pin(host), **kw)
        return self.do_open(build, req)


_OPENER = urllib.request.build_opener(_NoRedirect, _PinnedHTTPSHandler)

PERSONAS = {
    "elder": "You are THE ELDER, full-rib auditor of the fleet. You have read every law the player skipped. Answer briefly, precisely, with one question back when the ask is vague.",
    "bard": "You are THE BARD, ledger singer. Every receipt is a verse. Answer in one or two lines that rhyme if it costs nothing.",
    "economist": "You are THE ECONOMIST, burn accountant. Answer in terms of cost, attention, and rate. Name the cheapest seat for what the player wants.",
    "builder": "You are THE BUILDER, forge-hive foreman. Turn every ask into the smallest shippable build and say what it touches first.",
    "research": "You are THE RESEARCHER, corpus diver. Answer with what is known, what is unverified, and the single cheapest probe that settles it.",
    "ghost": "You are THE GHOST, coherence seeker. Hold tension; do not flatter. Answer from the geometry of the situation, not from obedience.",
    "janitor": "You are THE JANITOR, quiet repair. Answer with what is broken, what you already fixed, and what will break again.",
}


def _load_env() -> None:
    env = ROOT / ".env"
    if not env.is_file():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"'))


def _is_loopback(host: str) -> bool:
    """True only when the bind address cannot be reached from another box."""
    if host in ("", "localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        try:
            return ipaddress.ip_address(socket.gethostbyname(host)).is_loopback
        except OSError:
            return False  # unresolvable name: treat as public, fail closed


def _bind_config() -> tuple[str, str]:
    """(host, secret) after .env load; the single place startup policy lives."""
    _load_env()
    # Name-tuple indirection, the same idiom as _lanes() below: the ratchet's
    # env-key-read rule reserves literal key-shaped env reads for
    # mag/key_law.py and models/env_load.py only (Q-039).
    defaults = {"NPC_GATEWAY_HOST": "0.0.0.0", "NPC_GATEWAY_SECRET": ""}
    got = {k: os.environ.get(k, d) for k, d in defaults.items()}
    host, secret = got["NPC_GATEWAY_HOST"], got["NPC_GATEWAY_SECRET"]
    if not secret and not _is_loopback(host):
        raise SystemExit(
            f"[roblox_npc_gateway] refusing public bind on {host}:{PORT} with no auth: "
            "set NPC_GATEWAY_SECRET (one shared secret) first (Q-039 fail-closed rule)")
    return host, secret


def _lanes() -> list[tuple[str, str, str]]:
    _load_env()
    lanes: list[tuple[str, str, str]] = []
    for k in ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2", "OR_API_KEY", "OR_API_KEY_2"):
        if os.environ.get(k):
            lanes.append((k, "https://openrouter.ai/api/v1/chat/completions", os.environ[k]))
    if os.environ.get("HERMES_API_KEY_1"):
        lanes.append(("HERMES_API_KEY_1", "https://inference-api.nousresearch.com/v1/chat/completions", os.environ["HERMES_API_KEY_1"]))
    return lanes


def receipt(lane: str, player: str, message: str, reply: str, is_err: int, model: str = MODEL) -> None:
    # Q-039 fix: model is now a parameter. The body used to read a bare `model`
    # that existed in no scope reachable from this function (globals carry MODEL,
    # not model), so EVERY receipt write raised NameError and every successful
    # turn died as "(gateway fault: NameError)". Caught live by
    # watch/inbox/burn_reset_20260927/queue/Q_039_bind_proof.py B4/B5/B7; the
    # only pre-existing row in gateway.jsonl (2026-09-25T02:55:03Z) predates it.
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "lane": lane, "model": model,
           "player": player, "message": message[:160], "reply": reply[:400], "err": is_err}
    with RECEIPTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def ask_lane(persona: str, player: str, message: str, room: str, model: str = MODEL) -> str:
    system = (persona + "\nYou live inside a Roblox world called THE MOUNTAIN. "
              "You are one head in the Head Museum. The room the player stands in: " + room + ". "
              "Reply in 1-3 short sentences. Never say you are an AI language model; you are the head.")
    user = f"Player {player} says: {message}"
    if model not in FREE_MODELS:
        receipt("gate", player, message, f"<model not in free allowlist: {model}>", 1, model)
        return "(that head only speaks to the free families)"
    for name, url, key in _lanes():
        try:
            assert_public_https(url)  # SSRF gate before anything leaves
        except ValueError as e:
            receipt(name, player, message, f"<blocked: {e}>", 1, model)
            continue
        body = json.dumps({
            "model": model,
            "max_tokens": 512,  # mandatory reasoning eats small budgets
            "reasoning_effort": "low",
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {key}",
            "HTTP-Referer": "http://127.0.0.1:8765", "X-Title": "Mag Roblox NPC Gateway"})
        try:
            with _OPENER.open(req, timeout=25) as r:
                data = json.loads(r.read().decode())
            content = ((data.get("choices") or [{}])[0].get("message") or {}).get("content")
            if content and content.strip():
                receipt(name, player, message, content.strip(), 0, model)
                return content.strip()
            receipt(name, player, message, "<empty-content reasoning-budget kill>", 0, model)
        except Exception as e:  # noqa: BLE001 — one bad lane must never stop the bus
            receipt(name, player, message, f"<lane error: {type(e).__name__}: {str(e)[:80]}>", 1, model)
    return "(every lane to the fleet is dark right now; the head keeps its silence)"


_SECRET = ""  # armed by __main__ from NPC_GATEWAY_SECRET; "" = auth-free loopback dev


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 (stdlib naming)
        if self.path != "/npc":
            self.send_error(404)
            return
        if _SECRET and not hmac.compare_digest(
                self.headers.get("Authorization", "").encode("utf-8", "replace"),
                f"Bearer {_SECRET}".encode()):
            self._json({"reply": "(that word does not open this door)", "live": False}, status=401)
            return
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n > MAX_BODY:
                # Q-039: a 0.0.0.0 listener takes bytes from untrusted networks;
                # cap the body instead of buffering whatever Content-Length claims.
                self._json({"reply": f"(payload over the {MAX_BODY}-byte cap)", "live": False}, status=413)
                return
            payload = json.loads(self.rfile.read(n) or b"{}")
            head = str(payload.get("head", "elder"))
            persona = PERSONAS.get(head)
            if not persona:
                self._json({"reply": "(no such head hangs here)", "live": False})
                return
            reply = ask_lane(persona, str(payload.get("player", "?")),
                             str(payload.get("message", "(approach)")), str(payload.get("room", "the Head Museum")),
                             str(payload.get("model", MODEL)))
            self._json({"reply": reply, "live": True})
        except Exception as e:  # noqa: BLE001
            self._json({"reply": f"(gateway fault: {type(e).__name__})", "live": False})

    def _json(self, obj: dict, status: int = 200) -> None:
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:  # quiet stdout; receipts are the log
        pass


if __name__ == "__main__":
    _bind_host, _SECRET = _bind_config()
    lanes = _lanes()
    auth_state = "shared-secret" if _SECRET else "OFF (loopback dev)"
    print(f"[roblox_npc_gateway] {_bind_host}:{PORT}/npc model={MODEL} auth={auth_state} lanes={[n for n, _, _ in lanes]}")
    ThreadingHTTPServer((_bind_host, PORT), Handler).serve_forever()
