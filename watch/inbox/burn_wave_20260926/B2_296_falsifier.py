"""B2-296 falsifier: exact-case mistral key lookup across OS surfaces.

Law: stdlib only, no repo imports, so the same bytes run under Windows python
and WSL POSIX python (the brief's falsifier: "an exact-case lookup run under
WSL finds no mistral key"). Parses the repo .env the same way
models/env_load.py does (strip, split '=', strip quotes), then answers:

  exact_canonical   - exact-case dict lookup of MISTRAL_API_KEY / _2
                      (POSIX semantics, what WSL/docker resolve)
  exact_mixed       - exact-case lookup of the old mixed-case spellings
  winlike_canonical - case-insensitive lookup of the canonical name
                      (what Windows os.environ resolves)
  spellings_in_env  - the literal key names present in the file

Before the B2-296 fix: exact_canonical must be False under POSIX while
exact_mixed is True and winlike_canonical is True (the Windows-only lane).
After the fix: exact_canonical must be True on every surface.

Usage: python B2_296_falsifier.py [repo_root]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CANONICAL = ("MISTRAL_API_KEY", "MISTRAL_API_KEY_2")
MIXED = ("Mistral_API_KEY", "Mistral_API_KEY_2")


def parse_env(repo_root: Path) -> dict[str, str]:
    env_path = repo_root / ".env"
    out: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


def main() -> int:
    default_root = Path(__file__).resolve().parents[3]
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default_root
    env = parse_env(repo_root)
    exact = dict(env)  # plain dict = POSIX case-sensitive semantics

    result = {
        "repo_root": str(repo_root),
        "spellings_in_env": {k: "(set)" for k in env if "MISTRAL" in k.upper()},
        "exact_canonical": {k: bool(exact.get(k, "").strip()) for k in CANONICAL},
        "exact_mixed": {k: bool(exact.get(k, "").strip()) for k in MIXED},
        "winlike_canonical": {
            k: any(ka.upper() == k and env[ka].strip() for ka in env)
            for k in CANONICAL
        },
        "posix_lane_resolves": any(exact.get(k, "").strip() for k in CANONICAL),
        "windows_lane_resolves": any(
            any(ka.upper() == k.upper() and env[ka].strip() for ka in env)
            for k in CANONICAL
        ),
    }
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
