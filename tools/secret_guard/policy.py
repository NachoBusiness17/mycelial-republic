"""Policy loading + path matching for secret_guard."""
from __future__ import annotations

import fnmatch
import functools
import io
import os

_RAW_OPEN = io.open
_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_ROOT = os.path.dirname(os.path.dirname(_HERE))


def repo_root() -> str:
    return os.path.abspath(os.environ.get("MAG_SECRET_GUARD_ROOT", _DEFAULT_ROOT))


def policy_file() -> str:
    return os.environ.get("MAG_SECRET_GUARD_POLICY",
                          os.path.join(_DEFAULT_ROOT, "configs", "secrets_policy.yaml"))


@functools.lru_cache(maxsize=4)
def _load(path: str) -> dict:
    import yaml
    with _RAW_OPEN(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_policy() -> dict:
    return _load(policy_file())


def _norm(p: str) -> str:
    return os.path.normcase(os.path.abspath(os.path.expanduser(p))).replace("\\", "/")


def is_secret_path(path) -> bool:
    try:
        path = os.fspath(path)
    except TypeError:
        return False
    if isinstance(path, bytes):
        path = path.decode("utf-8", "replace")
    if not isinstance(path, str) or not path:
        return False
    pol = load_policy()
    ap = _norm(path)
    base = ap.rsplit("/", 1)[-1]
    root = _norm(repo_root())
    rel = ap[len(root) + 1:] if ap.startswith(root + "/") else None
    for pat in pol.get("allow", []):
        if fnmatch.fnmatch(base, pat.lower()):
            return False
    for pat in pol.get("secret_sources", []):
        pl = pat.lower()
        if pl.startswith("~"):
            if fnmatch.fnmatch(ap, _norm(pl)):
                return True
            continue
        if fnmatch.fnmatch(base, pl):
            return True
        if rel is not None and fnmatch.fnmatch(rel, pl):
            return True
        if "/" in pl and fnmatch.fnmatch(ap, "*/" + pl):
            return True
    return False
