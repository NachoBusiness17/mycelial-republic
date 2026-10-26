"""Append-only JSONL audit for secret_guard. Never records a value: sha256[:8] only."""
from __future__ import annotations

import datetime as _dt
import io
import json
import os
import threading

_LOCK = threading.Lock()
# Captured before any audit hook is installed; the audit file is not a secret path.
_RAW_OPEN = io.open


def audit_path() -> str:
    env = os.environ.get("MAG_SECRET_GUARD_AUDIT")
    if env:
        return env
    from tools.secret_guard.policy import repo_root, load_policy
    return os.path.join(repo_root(), load_policy().get("audit_log", "state/secret_guard/audit.jsonl"))


def log(event: str, **fields) -> None:
    row = {"ts": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
           "event": event, "pid": os.getpid()}
    for k, v in fields.items():
        if k in ("value", "secret", "payload"):
            raise ValueError("audit refuses raw values")
        row[k] = v
    p = audit_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    line = json.dumps(row, sort_keys=True) + "\n"
    with _LOCK:
        with _RAW_OPEN(p, "a", encoding="utf-8") as f:   # append-only
            f.write(line)
