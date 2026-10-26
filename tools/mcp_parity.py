"""mcp_parity — standing manifest parity across the estate's MCP transports.

Law MCP-2 (watch/inbox/ractor50/mcp.md section 7, 2026-10-01): an always-on
MCP surface without a parity check is a stale surface with a green heartbeat.
On 2026-10-01 mag-mcp still ran the 2026-09-26 image while mag-sovereign:local
pointed at the 2026-09-30 rebuild; the port healthcheck stayed green the whole
time. This check catches that class.

Each transport gets a real JSON-RPC initialize + tools/list for the profile
it ACTUALLY serves (self-declared via _meta.mag.profile): stdio host venv
(--profile), gateway POST /mcp on 8001 (X-API-Key via the gateway's own
api_key(), never printed), docker TCP bridge 8766, plus the mag-mcp image
digest vs the current mag-sovereign:local tag. Baseline is a live gated
stdio probe of THIS tree: name-set + content digest.
Pin-gate withholds are named and verdict-neutral (MCP-1's alarm); divergence
in names, digest, served profile, or container image is exit 1, fail loud.
EXIT 0 = parity (named SKIPs/withholds allowed); 2 = cannot verify (all
probes skipped; a down transport is a NAMED SKIP, never silent or fatal).

RUN: .venv/Scripts/python.exe tools/mcp_parity.py [--profile bridge] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
SCHEMA = "mcp_parity.v1"
_HANDSHAKE = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
              {"jsonrpc": "2.0", "method": "notifications/initialized"},
              {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}]


class Skip(Exception):
    """Named, non-fatal unavailability of one transport (docker down, etc)."""


def _names(tools: list[dict[str, Any]]) -> list[str]:
    return sorted(str(t.get("name") or "") for t in tools)


def _served_profile(tools: list[dict[str, Any]]) -> str | None:
    for t in tools:
        if p := (t.get("_meta") or {}).get("mag", {}).get("profile"):
            return str(p)
    return None


def manifest_digest(tools: list[dict[str, Any]]) -> str:
    """Content fingerprint: name + description + inputSchema, _meta excluded."""
    core = [{"name": t.get("name"), "description": t.get("description"),
             "inputSchema": t.get("inputSchema")}
            for t in sorted(tools, key=lambda t: str(t.get("name") or ""))]
    canonical = json.dumps(core, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _tools_from_text(text: str, who: str, tail: str = "") -> list[dict[str, Any]]:
    """tools/list out of newline-delimited JSON-RPC output; Skip on absence."""
    replies: dict[Any, dict[str, Any]] = {}
    for line in text.splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and msg.get("id") is not None and (
                "result" in msg or "error" in msg):
            replies[msg["id"]] = msg
    if 2 not in replies:
        detail = (replies.get(1) or {}).get("error", {}).get("message", "")
        extra = f" (initialize said: {detail})" if detail else f"; {tail}"
        raise Skip(f"{who} produced no tools/list reply{extra}")
    tools = (replies[2].get("result") or {}).get("tools")
    if not isinstance(tools, list):
        raise Skip(f"{who} tools/list reply not tools-shaped")
    return tools


def probe_stdio(python_exe: str, profile: str, timeout: float) -> list[dict[str, Any]]:
    """Host stdio: spawn mag.mcp_server; write the handshake, read the replies."""
    try:
        proc = subprocess.Popen(
            [python_exe, "-u", "-m", "mag.mcp_server", "--profile", profile],
            cwd=str(ROOT), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace")
    except OSError as e:
        raise Skip(f"stdio spawn failed ({python_exe}): {e}") from e
    payload = "".join(json.dumps(m) + "\n" for m in _HANDSHAKE)
    try:
        out, _err = proc.communicate(payload, timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.communicate()
        raise Skip(f"stdio probe timed out after {timeout:.0f}s (profile {profile})")
    return _tools_from_text(out, f"stdio (profile {profile})",
                            f"rc={proc.returncode}")


def probe_http(url: str, api_key: str, timeout: float) -> list[dict[str, Any]]:
    """Gateway POST /mcp: stateless streamable HTTP, one message per POST."""
    def post(msg: dict[str, Any]) -> dict[str, Any]:
        req = urllib.request.Request(url, json.dumps(msg).encode("utf-8"),
            {"Content-Type": "application/json", "X-API-Key": api_key},
            method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    try:
        init = post(_HANDSHAKE[0])
        listing = post(_HANDSHAKE[2])
    except urllib.error.HTTPError as e:
        hint = ("; X-API-Key mismatch: export the gateway key as MAG_API_KEY"
                if e.code == 401 else "")
        raise Skip(f"{url} answered HTTP {e.code}{hint}") from e
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise Skip(f"{url} unreachable ({type(e).__name__}: "
                   f"{getattr(e, 'reason', e)}) — gateway down?") from e
    if init.get("error"):
        raise Skip(f"initialize error from gateway: {init['error'].get('message')}")
    tools = (listing.get("result") or {}).get("tools")
    if not isinstance(tools, list):
        raise Skip("http tools/list reply not tools-shaped "
                   f"(got: {json.dumps(listing)[:160]})")
    return tools


def probe_docker(host: str, port: int, timeout: float) -> list[dict[str, Any]]:
    """TCP bridge: newline JSON-RPC; write all lines, shutdown write, read all."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
    except OSError as e:  # ConnectionRefusedError included
        raise Skip(f"{host}:{port} unreachable ({type(e).__name__}) — "
                   "docker down or mag-mcp not running") from e
    payload = "".join(json.dumps(m) + "\n" for m in _HANDSHAKE)
    chunks: list[bytes] = []
    try:
        sock.settimeout(timeout)
        sock.sendall(payload.encode("utf-8"))
        sock.shutdown(socket.SHUT_WR)  # bridge closes the server stdin at EOF
        while True:
            data = sock.recv(65536)
            if not data:
                break
            chunks.append(data)
    except OSError as e:  # socket.timeout is an OSError subclass
        kind = ("read timed out" if isinstance(e, socket.timeout)
                else f"wire error ({type(e).__name__}: {e})")
        raise Skip(f"{host}:{port} {kind} after connect "
                   f"(timeout {timeout:.0f}s) — check docker logs") from e
    finally:
        sock.close()
    text = b"".join(chunks).decode("utf-8", "replace")
    return _tools_from_text(text, f"{host}:{port}",
                            "bridge closed early — check docker logs")


def probe_image(container: str, image_ref: str, timeout: float) -> dict[str, Any]:
    """Container image digest vs the current tag digest (the R2.0 defect class)."""
    def docker(*args: str) -> str:
        try:
            r = subprocess.run(["docker", *args], capture_output=True,
                               text=True, timeout=timeout)
        except FileNotFoundError:
            raise Skip("docker CLI not on PATH — image parity unverifiable here")
        except subprocess.TimeoutExpired:
            raise Skip(f"docker {' '.join(args)} timed out")
        if r.returncode != 0:
            raise Skip(f"docker {' '.join(args)} rc={r.returncode}: "
                       f"{r.stderr.strip()[:160]}")
        return r.stdout.strip()
    d = {"match": None, "container": container, "image_ref": image_ref}
    d["container_image"] = docker("inspect", container, "--format", "{{.Image}}")
    d["tagged_image"] = docker("image", "inspect", image_ref,
                               "--format", "{{.Id}}")
    return d


def _short(digest: str) -> str:
    return digest.removeprefix("sha256:")[:12]


def compare_transport(name: str, expected_profile: str,
                      served_tools: list[dict[str, Any]],
                      host_truth: list[dict[str, Any]] | None,
                      declared_names: list[str]) -> dict[str, Any]:
    """Compare one transport's served manifest against host truth (pure).

    host_truth None means the baseline probe itself skipped; the transport is
    then a named SKIP (not comparable), never a silent pass.
    """
    if host_truth is None:
        return {"transport": name, "status": "skip",
                "skip_reason": "host baseline probe unavailable for profile "
                               f"{expected_profile} — nothing to compare against"}
    served_names, truth_names = _names(served_tools), _names(host_truth)
    missing = sorted(set(truth_names) - set(served_names))
    extra = sorted(set(served_names) - set(truth_names))
    reasons = []
    served_prof = _served_profile(served_tools)
    if served_prof not in (None, expected_profile):
        reasons.append(f"served profile {served_prof!r} but expected "
                       f"{expected_profile!r}")
    if missing:
        reasons.append(f"missing {len(missing)}: {', '.join(missing)}")
    if extra:
        reasons.append(f"extra {len(extra)}: {', '.join(extra)}")
    digest_match = (manifest_digest(served_tools)
                    == manifest_digest(host_truth))
    if not digest_match:
        reasons.append("content digest differs from host truth for the same "
                       "profile (name+description+inputSchema bytes)")
    return {
        "transport": name, "status": "diverge" if reasons else "ok",
        "reasons": reasons, "expected_profile": expected_profile,
        "served_profile": served_prof,
        "profile_match": served_prof in (None, expected_profile),
        "served_count": len(served_names), "host_truth_count": len(truth_names),
        "declared_count": len(declared_names), "missing": missing,
        "extra": extra,
        # pin-gate residue (declared but withheld on host): named, verdict-neutral
        "withheld": sorted(set(declared_names) - set(truth_names)),
        "digest_match": digest_match,
    }


def evaluate(transports: list[dict[str, Any]],
             baseline_profiles: list[str]) -> dict[str, Any]:
    """Fold rows into the verdict (pure): 1 any diverge, 0 any ok, else 2."""
    rows = [r for r in transports if r.get("status") != "baseline"]
    diverged = [r for r in rows if r.get("status") == "diverge"]
    oks = [r for r in rows if r.get("status") == "ok"]
    skips = [r for r in rows if r.get("status") == "skip"]
    if diverged:
        verdict, exit_code = "FAIL", 1
    elif oks:
        verdict, exit_code = "PASS", 0
    else:
        verdict, exit_code = "CANNOT-VERIFY", 2
    return {"schema": SCHEMA, "verdict": verdict, "exit": exit_code,
            "counts": {"ok": len(oks), "diverge": len(diverged), "skip": len(skips)},
            "baseline_profiles": baseline_profiles, "transports": rows}


def format_report(report: dict[str, Any]) -> str:
    """Human-readable verdict block; every SKIP and withhold is named."""
    c = report["counts"]
    lines = [f"MCP-PARITY {report['verdict']} (ok={c['ok']} "
             f"diverge={c['diverge']} skip={c['skip']})"]
    for row in report["transports"]:
        head = f"  {row['transport']:<6}: profile={row.get('expected_profile')}"
        if row["status"] == "skip":
            lines.append(f"{head} SKIP — {row.get('skip_reason', 'unavailable')}")
            continue
        state = "OK" if row["status"] == "ok" else "DIVERGE"
        lines.append(f"{head} served={row.get('served_count', '-')} "
                     f"host_truth={row.get('host_truth_count', '-')} "
                     f"declared={row.get('declared_count', '-')} -> {state}")
        lines.extend(f"         {reason}" for reason in row.get("reasons", []))
        if row.get("withheld"):
            lines.append("         withheld (pin gate, alarm standing, repin "
                         f"owed): {', '.join(row['withheld'])}")
        if row.get("image"):
            img = row["image"]
            tag = "match" if img["match"] else "STALE IMAGE"
            fix = (" (recreate owed: docker compose up -d "
                   "--force-recreate mcp)") if not img["match"] else ""
            lines.append(f"         image: container "
                         f"{_short(img['container_image'])} vs "
                         f"{img['image_ref']} {_short(img['tagged_image'])} "
                         f"-> {tag}{fix}")
    lines.append(f"MCP-PARITY exit={report['exit']}")
    return "\n".join(lines)


def _declared_manifests(profiles: list[str]) -> dict[str, list[str]]:
    """Ungated declared names per profile, from THIS tree (baseline import)."""
    from mag.mcp_server import ROLE_TOOLSETS, tools_manifest  # lazy

    for profile in profiles:
        if profile not in ROLE_TOOLSETS:
            raise SystemExit(f"mcp_parity: unknown profile {profile!r} "
                             f"(known: {sorted(ROLE_TOOLSETS)})")
    return {p: _names(tools_manifest(p)) for p in profiles}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="mcp_parity", description="MCP-2 parity check: stdio + gateway"
        " + docker bridge")
    ap.add_argument("--profile", default="bridge",
                    help="stdio transport profile (default: bridge)")
    ap.add_argument("--http-profile", default="full",
                    help="gateway /mcp profile (default: full)")
    ap.add_argument("--docker-profile", default="archivist",
                    help="docker bridge profile (default: archivist)")
    ap.add_argument("--http-url", default="http://127.0.0.1:8001/mcp")
    ap.add_argument("--docker-host", default="127.0.0.1")
    ap.add_argument("--docker-port", type=int, default=8766)
    ap.add_argument("--container", default="mag-mcp")
    ap.add_argument("--image-ref", default="mag-sovereign:local")
    ap.add_argument("--python", default=sys.executable,
                    help="stdio probe interpreter (default: running one)")
    ap.add_argument("--timeout", type=float, default=45.0)
    ap.add_argument("--json", action="store_true", help="JSON report")
    args = ap.parse_args(argv)

    profiles = list(dict.fromkeys(
        (args.profile, args.http_profile, args.docker_profile)))
    try:
        declared = _declared_manifests(profiles)
    except SystemExit:
        raise  # unknown profile: argparse-style hard error, not CANNOT-VERIFY
    except Exception as e:  # baseline unavailable: nothing is comparable
        print(f"MCP-PARITY CANNOT-VERIFY: declared baseline unavailable: "
              f"{type(e).__name__}: {e}")
        return 2

    # One gated host-stdio probe per distinct profile = the parity baseline.
    host_truth: dict[str, list[dict[str, Any]] | None] = {}
    host_skip: dict[str, str] = {}
    for profile in profiles:
        try:
            host_truth[profile] = probe_stdio(args.python, profile, args.timeout)
        except Skip as e:
            host_truth[profile], host_skip[profile] = None, str(e)

    rows: list[dict[str, Any]] = []

    def skip_row(name: str, profile: str, reason: str) -> dict[str, Any]:
        return {"transport": name, "status": "skip", "skip_reason": reason,
                "expected_profile": profile}

    def probe_row(name, expected_profile, served):
        return compare_transport(name, expected_profile, served,
                                 host_truth[expected_profile],
                                 declared[expected_profile])

    if host_truth[args.profile] is None:
        rows.append(skip_row("stdio", args.profile, host_skip[args.profile]))
    else:
        rows.append(probe_row("stdio", args.profile,
                              host_truth[args.profile]))
    try:
        from mag.api_gateway import api_key as gateway_key  # the gate's own door
        rows.append(probe_row("http", args.http_profile,
                              probe_http(args.http_url, gateway_key(),
                                         args.timeout)))
    except Skip as e:
        rows.append(skip_row("http", args.http_profile, str(e)))
    docker_row: dict[str, Any] | None = None
    try:
        docker_row = probe_row("docker", args.docker_profile, probe_docker(
            args.docker_host, args.docker_port, args.timeout))
    except Skip as e:
        rows.append(skip_row("docker", args.docker_profile, str(e)))
    try:
        image = probe_image(args.container, args.image_ref, args.timeout)
        image["match"] = (image["container_image"] == image["tagged_image"])
        target = docker_row if docker_row is not None else {
            "transport": "docker-image", "status": "ok", "reasons": [],
            "expected_profile": "-"}
        target["image"] = image
        if not image["match"]:
            target["status"] = "diverge"
            target.setdefault("reasons", []).append(
                f"container {args.container} runs {_short(image['container_image'])} "
                f"but {args.image_ref} is {_short(image['tagged_image'])} — image "
                "rebuilt, container never recreated")
        if docker_row is None:
            rows.append(target)
    except Skip as e:
        if docker_row is None:
            rows.append(skip_row("docker-image", "-", str(e)))
        else:
            docker_row["image_skip"] = str(e)
    if docker_row is not None:
        rows.append(docker_row)

    report = evaluate(rows, profiles)
    report["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report["probe"] = {"stdio_profile": args.profile, "http_url": args.http_url,
                       "container": args.container, "image_ref": args.image_ref,
                       "docker": f"{args.docker_host}:{args.docker_port}"}
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json
          else format_report(report))
    return report["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
