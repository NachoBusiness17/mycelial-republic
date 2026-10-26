"""ESTATE ENV — the one canonical key loader (rib.md.record.v1 companion).

Law: the estate .env at the repo root is THE key source of record. Tools do
not read os.environ for keys, do not open their own .env by cwd, and do not
keep private copies. Import this and call key().

Path is derived from this file's own location (never the caller's cwd), so
the loader cannot pretend: it either returns the real value from the real
file, or None — and status() shows set vs empty honestly.

Usage:
    from tools.estate_env import key, status
    k = key("GROQ_API_KEY")          # value or None
    print(status())                   # full honest census
"""

import functools
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = _ROOT / ".env"


@functools.lru_cache(maxsize=1)
def _load():
    rows = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8",
                                       errors="replace").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                rows[k.strip()] = v.strip()
    return rows


def key(name):
    """The real value from the real file, or None. No pretending."""
    return _load().get(name) or None


def status():
    rows = _load()
    return {"path": str(ENV_PATH), "exists": ENV_PATH.exists(),
            "set": sorted(k for k, v in rows.items() if v),
            "empty": sorted(k for k, v in rows.items() if not v)}


if __name__ == "__main__":
    import json
    print(json.dumps(status(), indent=2))
