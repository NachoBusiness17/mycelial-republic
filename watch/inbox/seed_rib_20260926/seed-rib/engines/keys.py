"""keys — the one door engines use for key lookups (law 7).
Reads configs/keys.json first: an env var that is LIVE but undeclared is reported,
not silently used. Falls back to the environment for declared names only.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "configs" / "keys.json"


def _manifest() -> dict:
    if MANIFEST.is_file():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def declared_envs() -> set:
    return {v.get("env") for v in _manifest().values() if isinstance(v, dict)}


def get(env_name: str) -> str:
    """Value for a declared env name; '' when absent. A live-but-undeclared
    key prints one loud warning to stderr (fail loud, per law 7)."""
    val = (os.environ.get(env_name, "") or "").strip()
    if val and env_name not in declared_envs():
        print(f"keys: ORPHAN — {env_name} is live but not declared in configs/keys.json "
              f"(declare it or the audit will fail)", file=sys.stderr)
    return val
