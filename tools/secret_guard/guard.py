"""secret_guard core: in-process secret loading, export refusal, TTY+nonce transfer approval,
in-memory fingerprinting for the egress tripwire."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import secrets as _secrets
import sys
import threading

from tools.secret_guard import audit
from tools.secret_guard.policy import is_secret_path, load_policy, repo_root

_RAW_OPEN = io.open
_TLS = threading.local()

AGENT_ENV_MARKERS = ("MAG_AGENT", "CI", "CURSOR_AGENT", "CLAUDECODE", "GEMINI_CLI",
                     "CODEX_SANDBOX", "GROK_AGENT", "SSH_ORIGINAL_COMMAND")


class SecretAccessDenied(PermissionError):
    pass


class SecretExportDenied(PermissionError):
    pass


def sha8(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


@contextlib.contextmanager
def _guarded():
    prev = getattr(_TLS, "inside", False)
    _TLS.inside = True
    try:
        yield
    finally:
        _TLS.inside = prev


def inside_guard() -> bool:
    return getattr(_TLS, "inside", False)


def _caller(depth: int = 2) -> str:
    f = sys._getframe(depth)
    return f"{os.path.relpath(f.f_code.co_filename, repo_root())}:{f.f_lineno}"


_DOTENV = re.compile(r"^\s*#?\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")


def _parse(path: str, text: str) -> dict:
    """name -> value. Commented-out dotenv lines ARE included (the incident key was commented)."""
    out = {}
    if path.lower().endswith(".json"):
        try:
            def walk(o, pre=""):
                if isinstance(o, dict):
                    for k, v in o.items():
                        walk(v, f"{pre}{k}.")
                elif isinstance(o, list):
                    for i, v in enumerate(o):
                        walk(v, f"{pre}{i}.")
                elif isinstance(o, str):
                    out[pre.rstrip(".")] = o
            walk(json.loads(text))
            return out
        except ValueError:
            pass
    hit = False
    for line in text.splitlines():
        m = _DOTENV.match(line)
        if m:
            hit = True
            v = m.group(2).strip().strip('"').strip("'")
            if v:
                out.setdefault(m.group(1), v)
    if not hit and text.strip():
        out["<file>"] = text.strip()
    return out


def _read(path: str) -> str:
    with _guarded():
        with _RAW_OPEN(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()


def load_secret(path, name: str, caller: str | None = None) -> str:
    """Return one secret value, in-process only. Logs sha8, never the value."""
    path = os.fspath(path)
    caller = caller or _caller()
    if not is_secret_path(path):
        audit.log("load_refused_not_policy_path", caller=caller, path=path, key=name)
        raise SecretAccessDenied(f"{path} is not a policy secret source")
    vals = _parse(path, _read(path))
    if name not in vals:
        audit.log("load_missing", caller=caller, path=path, key=name)
        raise KeyError(name)
    v = vals[name]
    audit.log("load", caller=caller, path=path, key=name, sha8=sha8(v))
    return v


def export_secret(*_a, **kw) -> None:
    """Writing a secret to a file / clipboard / another device is never allowed via the guard."""
    audit.log("export_denied", caller=kw.get("caller") or _caller(), destination=str(kw.get("destination")))
    raise SecretExportDenied("secret_guard never writes or exports secret values")


def _interactive() -> bool:
    if any(os.environ.get(m) for m in AGENT_ENV_MARKERS):
        return False
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


def request_transfer(name: str, destination: str, caller: str | None = None,
                     _input=input, _isatty=None) -> bool:
    """In-the-moment approval: real TTY + Nacho types a fresh nonce. Anything else denies."""
    caller = caller or _caller()
    interactive = _isatty() if _isatty else _interactive()
    if not interactive:
        audit.log("transfer_denied_noninteractive", caller=caller, key=name, destination=destination)
        return False
    nonce = _secrets.token_hex(3)
    prompt = (f"\n[secret_guard] {caller} wants to send secret '{name}' to:\n"
              f"    {destination}\n"
              f"Type {nonce} to approve this ONE transfer (anything else denies): ")
    try:
        ans = _input(prompt)
    except (EOFError, KeyboardInterrupt):
        ans = ""
    ok = ans.strip() == nonce
    audit.log("transfer_approved" if ok else "transfer_denied_nonce", caller=caller,
              key=name, destination=destination)
    return ok


def fingerprints(extra_paths=()) -> dict:
    """{value: (sha8, relpath, key)} for every policy secret under repo root (+extra).
    Lives in memory only; used by safe_ssh to compare payloads."""
    pol = load_policy()
    mn = int(pol.get("min_secret_len", 12))
    root = repo_root()
    found = {}
    cands = list(extra_paths)
    skip = {".git", "node_modules", ".venv", "__pycache__", "corpus", "canon", "watch", "memory", "dist_audit"}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in skip]
        for fn in files:
            p = os.path.join(d, fn)
            if is_secret_path(p):
                cands.append(p)
    for p in cands:
        try:
            if os.path.getsize(p) > 1_000_000:
                continue
            for k, v in _parse(p, _read(p)).items():
                if len(v) >= mn:
                    found[v] = (sha8(v), os.path.relpath(p, root), k)
        except OSError:
            continue
    audit.log("fingerprint_scan", caller=_caller(), files=len(cands), values=len(found))
    return found


def payload_hits(data, fps: dict | None = None) -> list:
    """Return [(sha8, relpath, key)] of secret values contained in data (str/bytes)."""
    if isinstance(data, bytes):
        data = data.decode("utf-8", "replace")
    fps = fingerprints() if fps is None else fps
    return [meta for v, meta in fps.items() if v in data]
