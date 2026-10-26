"""Opt-in audit hook (MAG_SECRET_GUARD=1): blocks open() of policy secret paths unless
through secret_guard, and blocks launching egress commands (ssh/scp/adb...) unless through
tools/safe_ssh.py. Python audit hooks cannot be removed once installed (by design)."""
from __future__ import annotations

import os
import sys

_INSTALLED = False


def _egress_name(exe) -> str | None:
    from tools.secret_guard.policy import load_policy
    try:
        exe = os.fspath(exe)
    except TypeError:
        return None
    if isinstance(exe, bytes):
        exe = exe.decode("utf-8", "replace")
    b = os.path.basename(str(exe)).lower()
    for suf in (".exe", ".cmd", ".bat"):
        if b.endswith(suf):
            b = b[: -len(suf)]
    return b if b in load_policy().get("egress_commands", []) else None


def _hook(event, args):
    from tools.secret_guard import guard, audit
    if guard.inside_guard():
        return
    if event == "open":
        path = args[0]
        if isinstance(path, int):
            return
        from tools.secret_guard.policy import is_secret_path
        if is_secret_path(path):
            with guard._guarded():
                audit.log("open_blocked", caller=_where(), path=str(path))
            raise PermissionError(f"secret_guard: direct open of {path} blocked; use tools.secret_guard.load_secret")
    elif event in ("subprocess.Popen", "os.system", "os.posix_spawn", "os.spawn", "os.exec"):
        cmd = args[1] if event == "subprocess.Popen" else args[0]
        first = args[0] if event == "subprocess.Popen" else None
        names = []
        for c in (first, cmd):
            if isinstance(c, (list, tuple)) and c:
                names.append(c[0])
            elif isinstance(c, (str, bytes)) and c:
                s = c.decode() if isinstance(c, bytes) else c
                names.append(s.split()[0] if s.split() else s)
        for n in names:
            hit = _egress_name(n)
            if hit:
                with guard._guarded():
                    audit.log("egress_blocked_unwrapped", caller=_where(), command=hit)
                raise PermissionError(f"secret_guard: '{hit}' must go through tools/safe_ssh.py")


def _where() -> str:
    f = sys._getframe(2)
    while f and ("secret_guard" in f.f_code.co_filename or "subprocess" in f.f_code.co_filename):
        f = f.f_back
    return f"{f.f_code.co_filename}:{f.f_lineno}" if f else "?"


def install_hook(force: bool = False) -> bool:
    global _INSTALLED
    if _INSTALLED:
        return True
    if not force and os.environ.get("MAG_SECRET_GUARD") != "1":
        return False
    # warm imports/policy BEFORE the hook, so the hook never recurses on its own loads
    from tools.secret_guard import guard, audit, policy  # noqa: F401
    import yaml  # noqa: F401
    policy.load_policy()
    sys.addaudithook(_hook)
    _INSTALLED = True
    return True
