"""safe_ssh - egress tripwire wrapper for ssh/scp/sftp/rsync/adb used by repo tools.

    python tools/safe_ssh.py [--stdin-file F] -- ssh host 'cat > /sdcard/x'
    from tools.safe_ssh import run; run(["scp", "a.txt", "t90:/sdcard/"], input=b"...")

Before launching, scans argv, the stdin payload, and every local file named in argv
(scp/rsync sources, adb push sources) for secret values loaded via secret_guard (compared
in memory; only sha8 is logged). A hit blocks (exit 3) unless Nacho approves at a real TTY
with a fresh nonce. Non-interactive/agent contexts always deny.
"""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.secret_guard import audit, guard  # noqa: E402

EGRESS = {"ssh", "scp", "sftp", "rsync", "adb", "plink", "pscp"}


class EgressBlocked(PermissionError):
    pass


def _dest(cmd) -> str:
    return " ".join(str(c) for c in cmd)[:300]


def run(cmd, input: bytes | str | None = None, fps=None, caller: str | None = None, **kw):
    cmd = [os.fspath(c) for c in cmd]
    name = os.path.basename(cmd[0]).lower().removesuffix(".exe")
    caller = caller or guard._caller()
    if name not in EGRESS:
        raise ValueError(f"safe_ssh only wraps {sorted(EGRESS)}, got {name}")
    fps = guard.fingerprints() if fps is None else fps
    hits = []
    hits += guard.payload_hits(" ".join(cmd), fps)
    if input is not None:
        hits += guard.payload_hits(input, fps)
    for c in cmd[1:]:
        if os.path.isfile(c):
            if guard.is_secret_path(c):
                hits.append(("path", c, "<secret file>"))
                continue
            try:
                with guard._guarded(), io.open(c, "rb") as f:
                    hits += guard.payload_hits(f.read(2_000_000), fps)
            except OSError:
                pass
    dest = _dest(cmd)
    if hits:
        audit.log("egress_secret_hit", caller=caller, destination=dest,
                  sha8=[h[0] for h in hits], sources=[f"{h[1]}:{h[2]}" for h in hits])
        keys = ",".join(sorted({h[2] for h in hits}))
        if not guard.request_transfer(keys, dest, caller=caller):
            audit.log("egress_blocked", caller=caller, destination=dest, sha8=[h[0] for h in hits])
            raise EgressBlocked(f"safe_ssh: payload contains secret(s) {[h[0] for h in hits]} -> blocked")
    audit.log("egress_allowed", caller=caller, destination=dest, approved_secret=bool(hits))
    if isinstance(input, str):
        input = input.encode("utf-8")
    with guard._guarded():
        return subprocess.run(cmd, input=input, **kw)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="safe_ssh")
    ap.add_argument("--stdin-file")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    cmd = a.cmd[1:] if a.cmd[:1] == ["--"] else a.cmd
    data = None
    if a.stdin_file:
        with io.open(a.stdin_file, "rb") as f:
            data = f.read()
    elif not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
    try:
        return run(cmd, input=data, caller="safe_ssh-cli").returncode
    except EgressBlocked as e:
        print(str(e), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
