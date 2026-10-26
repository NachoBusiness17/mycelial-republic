#!/usr/bin/env python3
"""key_wizard - the mirror-authorization babystep for the starter kit.

The operator clicks okay ONCE in the provider's own consent screen and the
seat gets the key. v0 implements the OAuth 2.0 Device Flow (RFC 8628) for
GitHub, driven by the providers table in tools/providers.json: new
providers are data rows, never new code.

The agent-navigates-the-console version (browser automation clicking
through provider consoles) is the LATER stretch - fragile and
ToS-sensitive per provider. The sanctioned mirror is the provider's own
OAuth/device grant with user consent.

Prior attempt on record: watch/inbox/salon_mine/m16.md (2026-09-07)
"OAuth device flow attempted and stopped" in the Hermes Nous-lane - that
attempt died on wiring, not law; this wizard is the sanctioned redo at
the kit level.

LAWS THIS MODULE ENFORCES
- NO LIVE OAUTH WITHOUT OPERATOR: any network call requires --live; the
  default invocation prints the plan (endpoints, scopes, fence) and exits
  with zero packets sent.
- ENDPOINT FENCE (shape copied from tools/hermes_burn.py:45-48, the
  Mimosa SSRF rulings): https only, host must be in the provider row's
  allowed_hosts, asserted per call, AND the host resolved with
  private/loopback/link-local/reserved/multicast IPs refused. The
  endpoints come from an editable data table, so the fence is what stops
  a tampered table from aiming this tool at internal surfaces.
- STORAGE FENCE: the token is written only to a path inside the kit root
  (the kit's .env, gitignored from birth per starter-kit/.gitignore THE
  NEVER-COMMIT LAW). .env is loaded with CR-strip (CRLF and bare CR
  normalized to LF before parsing) so a Windows-edited file can never
  hand a token a trailing \\r. The token is never printed - only a
  masked form. No token bytes in output, logs, or exception text.
- FLOW REFUSAL IS LOUD: the wizard refuses any flow it does not
  implement (google/openrouter rows are data for the later stretch) with
  exit 2, instead of improvising one.
"""
from __future__ import annotations

import argparse
import getpass
import ipaddress
import json
import os
import socket
import sys
import time
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
PROVIDERS_PATH = Path(__file__).resolve().parent / "providers.json"
DEFAULT_ENV = KIT_ROOT / ".env"

# RFC 8628 Section 3.4: the device grant at the token endpoint.
GRANT_DEVICE = "urn:ietf:params:oauth:grant-type:device_code"
# RFC 8628 Section 3.2: "If no value is provided, clients MUST use 5 as
# the default." Same 5 seconds is the slow_down growth (Section 3.5).
POLL_DEFAULT = 5
SLOW_DOWN_STEP = 5


class FlowError(RuntimeError):
    """Loud, operator-readable failure; text must never carry the token."""


class EndpointFenceError(FlowError):
    """A URL or resolved IP the fence refuses."""


class StorageFenceError(FlowError):
    """A write target outside the kit root."""


# ---------------------------------------------------------------- fence

def assert_public_host(host: str) -> None:
    """Endpoint fence, resolution half: the host must not resolve to a
    private/loopback/link-local/reserved/multicast IP (DNS or hosts-file
    re-pointing cannot aim the wizard at internal surfaces)."""
    infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    if not infos:
        raise EndpointFenceError(f"endpoint fence: {host} did not resolve")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            raise EndpointFenceError(
                f"endpoint fence: {host} resolves to non-public {ip}")


def fence_url(url: str, allowed_hosts: list[str]) -> None:
    """Endpoint fence, URL half: https on an allowlisted host, asserted
    per call - then the resolution half."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in (allowed_hosts or []):
        raise EndpointFenceError(
            f"endpoint fence: refusing non-allowlisted URL (host={parsed.hostname!r})")
    assert_public_host(parsed.hostname)


def http_post_form(url: str, data: dict, allowed_hosts: list[str]) -> dict:
    """The one network verb in the module. Fence asserted per call."""
    fence_url(url, allowed_hosts)
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Accept": "application/json",
                 "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ------------------------------------------------------------- storage

def load_env(path: Path) -> dict:
    """Parse a .env with CR-strip at load: CRLF and bare CR are normalized
    to LF BEFORE parsing, so a Windows-edited .env can never hand a token
    a trailing carriage return (the silent-401 disease). Quotes stripped;
    comments and blank lines skipped."""
    try:
        raw = Path(path).read_bytes()
    except FileNotFoundError:
        return {}
    text = raw.decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out: dict[str, str] = {}
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("\"", "'"):
            val = val[1:-1]
        out[key.strip()] = val
    return out


def save_env_key(path: Path, key: str, value: str) -> None:
    """Store KEY=value into the .env, preserving every other line, LF
    endings, best-effort 0600 perms. STORAGE FENCE: refuses any path
    outside the kit root (the kit's .gitignore NEVER-COMMIT law is what
    makes .env the right home). Never logs the value."""
    path = Path(path).resolve()
    if not path.is_relative_to(KIT_ROOT):
        raise StorageFenceError(
            f"storage fence: refusing to write outside the kit root: {path}")
    lines: list[str] = []
    if path.exists():
        text = path.read_bytes().decode("utf-8", errors="replace")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")
        while lines and not lines[-1].strip():
            lines.pop()
    replaced = False
    for i, line in enumerate(lines):
        if line.strip().startswith(key + "="):
            lines[i] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        if lines:
            lines.append("")
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass  # best-effort; some filesystems (Windows FAT et al) refuse


def mask(token: str) -> str:
    """The only legal printable form of a secret in this module."""
    if len(token) <= 8:
        return "*" * len(token)
    return token[:4] + "..." + str(len(token))


# ----------------------------------------------------------- providers

def load_providers(path: Path) -> dict[str, dict]:
    """Load the providers table. Malformed table fails loud with the path."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FlowError(f"providers table missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FlowError(f"providers table is not valid JSON ({path}): {exc}") from exc
    return {row["name"]: row for row in data.get("providers", [])}


def plan_lines(entry: dict) -> list[str]:
    """The dry-run plan: what WOULD happen, zero network."""
    lines = [f"provider : {entry['name']}",
             f"flow     : {entry.get('flow')} (enabled={entry.get('enabled')})"]
    if entry.get("device_code_endpoint"):
        lines.append(f"codes    : POST {entry['device_code_endpoint']}")
    if entry.get("token_endpoint"):
        lines.append(f"token    : POST {entry['token_endpoint']} "
                      f"(grant {GRANT_DEVICE})")
    if entry.get("scopes"):
        lines.append(f"scopes   : {' '.join(entry['scopes'])}")
    lines.append(f"env_key  : {entry.get('env_key')} -> {DEFAULT_ENV}")
    if entry.get("allowed_hosts"):
        lines.append(f"fence     : hosts {' '.join(entry['allowed_hosts'])}, "
                      f"https only, private-IP resolution refused")
    lines.append("run with --live to perform the flow (operator consent is "
                 "the click in the provider's own page)")
    return lines


# ---------------------------------------------------------- the flows

def request_device_code(entry: dict, client_id: str, poster) -> dict:
    """RFC 8628 Section 3.1: request the device + user codes."""
    resp = poster(entry["device_code_endpoint"],
                  {"client_id": client_id,
                   "scope": " ".join(entry.get("scopes") or [])},
                  entry["allowed_hosts"])
    for field in ("device_code", "user_code", "verification_uri"):
        if not resp.get(field):
            raise FlowError(
                f"device code response lacked {field} (keys={sorted(resp)})")
    return resp


def poll_for_token(entry: dict, device_code: str, client_id: str, *,
                   interval: int | None, expires_in: int | None,
                   poster, sleeper=time.sleep, clock=time.monotonic) -> str:
    """RFC 8628 Section 3.5 poll loop. Before EACH new request the client
    waits at least the interval seconds (default 5 when the server sent
    none); slow_down raises the interval by 5 for this and all subsequent
    requests; authorization_pending repeats; expired_token, access_denied
    or the expires_in budget abort loud. poster/sleeper/clock are injected
    so tests own the wire and time."""
    interval = int(interval) if interval and int(interval) > 0 else POLL_DEFAULT
    budget = int(expires_in) if expires_in and int(expires_in) > 0 else 900
    deadline = clock() + budget
    while True:
        sleeper(interval)
        if clock() >= deadline:
            raise FlowError("device code expired: expires_in budget spent")
        resp = poster(entry["token_endpoint"],
                      {"grant_type": GRANT_DEVICE,
                       "device_code": device_code,
                       "client_id": client_id},
                      entry["allowed_hosts"])
        err = resp.get("error")
        if not err:
            token = resp.get("access_token")
            if not token:
                raise FlowError(
                    f"token response lacked access_token (keys={sorted(resp)})")
            return token
        if err == "authorization_pending":
            continue
        if err == "slow_down":
            interval += SLOW_DOWN_STEP
            continue
        if err == "expired_token":
            raise FlowError("device code expired (provider said expired_token)")
        if err == "access_denied":
            raise FlowError("user denied the authorization at the consent page")
        raise FlowError(f"unexpected token-endpoint error: {err!r}")


def run_device_flow(entry: dict, client_id: str, env_path: Path, *,
                    live: bool, poster=http_post_form,
                    opener=webbrowser.open) -> str:
    """The full mirror: codes -> consent page -> poll -> .env. Returns the
    token (for tests); the printed output never carries it."""
    if entry.get("flow") != "device":
        raise FlowError(
            f"flow {entry.get('flow')!r} is not implemented in this wizard "
            "(v0 = device + manual; the console-navigating agent is the "
            "later stretch)")
    if not entry.get("enabled"):
        raise FlowError(f"provider {entry['name']} is disabled in the table")
    if not live:
        print("\n".join(plan_lines(entry)))
        return ""
    if not client_id:
        raise FlowError(
            "no client_id: create an OAuth App (Enable Device Flow) at "
            f"{entry.get('console_url')} and pass --client-id or set "
            f"{entry.get('client_id_env')}")
    dev = request_device_code(entry, client_id, poster)
    print(f"user code : {dev['user_code']}")
    print(f"open      : {dev['verification_uri']}  (enter the code there)")
    if opener:
        opener(dev["verification_uri"])
    token = poll_for_token(
        entry, dev["device_code"], client_id,
        interval=dev.get("interval") or entry.get("interval_default"),
        expires_in=dev.get("expires_in") or entry.get("expires_in_default"),
        poster=poster)
    save_env_key(env_path, entry.get("env_key") or "PROVIDER_TOKEN", token)
    print(f"stored    : {entry.get('env_key')} = {mask(token)} in {env_path}")
    return token


def run_manual_flow(entry: dict, env_path: Path, *, live: bool) -> str:
    """Console-key mirror: the provider's own page issues the key, the
    paste is hidden, storage rides the same fence. Zero network here."""
    if entry.get("flow") != "manual":
        raise FlowError(f"flow {entry.get('flow')!r} is not the manual flow")
    if not entry.get("enabled"):
        raise FlowError(f"provider {entry['name']} is disabled in the table")
    if not live:
        print("\n".join(plan_lines(entry)))
        return ""
    print(f"1. open   : {entry.get('console_url')}")
    print(f"2. create a key"
          + (f" (scopes: {' '.join(entry['scopes'])})"
             if entry.get("scopes") else ""))
    key = getpass.getpass(
        f"3. paste the {entry.get('env_key')} value (input hidden): ")
    key = key.strip().replace("\r", "").replace("\n", "")
    if not key:
        raise FlowError("empty key pasted; nothing stored")
    save_env_key(env_path, entry.get("env_key") or "PROVIDER_TOKEN", key)
    print(f"stored    : {entry.get('env_key')} = {mask(key)} in {env_path}")
    return key


FLOWS = {"device": run_device_flow, "manual": run_manual_flow}


# ----------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="key_wizard",
        description="Mirror-authorization babystep: provider-issued keys "
                    "into the kit .env, device flow (RFC 8628) for GitHub, "
                    "manual paste for console-key providers.")
    ap.add_argument("provider", nargs="?", default="list",
                    help="provider name from tools/providers.json "
                         "(omit or 'list' to print the table)")
    ap.add_argument("--live", action="store_true",
                    help="perform the flow (default: dry-run plan, zero network)")
    ap.add_argument("--client-id", default=None,
                    help="OAuth App client ID for device flow")
    ap.add_argument("--env", default=str(DEFAULT_ENV),
                    help=".env target (default: <kit>/.env)")
    ap.add_argument("--providers", default=str(PROVIDERS_PATH),
                    help="providers table path")
    args = ap.parse_args(argv)

    table = load_providers(Path(args.providers))
    if args.provider == "list":
        for name in sorted(table):
            row = table[name]
            print(f"{name:12s} {row.get('flow', '?'):20s} "
                  f"enabled={str(row.get('enabled')):5s} "
                  f"env={row.get('env_key', '?')}")
        return 0
    entry = table.get(args.provider)
    if entry is None:
        print(f"unknown provider {args.provider!r}; known: "
              f"{', '.join(sorted(table))}", file=sys.stderr)
        return 2

    env_path = Path(args.env)
    client_id = (args.client_id
                 or os.environ.get(entry.get("client_id_env") or "", "")
                 or load_env(env_path).get(entry.get("client_id_env") or "", ""))
    flow_fn = FLOWS.get(entry.get("flow"))
    if flow_fn is None:
        print(f"flow {entry.get('flow')!r} is data for the later stretch; "
              "this wizard implements only: " + ", ".join(sorted(FLOWS)),
              file=sys.stderr)
        return 2
    try:
        if flow_fn is run_device_flow:
            flow_fn(entry, client_id, env_path, live=args.live)
        else:
            flow_fn(entry, env_path, live=args.live)
    except FlowError as exc:
        print(f"key_wizard: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
