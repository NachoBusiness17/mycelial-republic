"""warm_rib — dump the FROZEN_RIB for the zcode CLI seat + warm its cache prefix.

Moved from mag/_warm_rib.py (AH4, audit finding #15, 2026-09-30): that file was a
script named like a module (leading underscore, mag/ package) that made a METERED
rib_chat call AT IMPORT TIME with hardcoded absolute paths — any accidental
`import mag._warm_rib` paid the call and only worked on one machine. Here it is a
plain script: everything runs under main() behind an explicit __main__ guard, and
paths derive from the repo root via this file's location.

Run:
  .venv\\Scripts\\python.exe scripts\\warm_rib.py             # dump RIB.md + one metered cache-warm call
  .venv\\Scripts\\python.exe scripts\\warm_rib.py --skip-warm # dump only, zero metered calls
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def dump_rib(dest: Path | None = None) -> tuple[Path, int]:
    """Write the FROZEN_RIB to queue/handoff/zcode/RIB.md; returns (dest, chars)."""
    from mag.rib_cache import FROZEN_RIB

    dest = dest or (ROOT / "queue" / "handoff" / "zcode" / "RIB.md")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(FROZEN_RIB + "\n", encoding="utf-8")
    return dest, len(FROZEN_RIB)


def warm_call(task: str = "Cache-warm handshake for the zcode CLI session. "
                          "Reply with exactly: warm") -> dict:
    """One metered rib_chat with the frozen prefix; returns cached_tokens for proof."""
    from mag.rib_cache import rib_chat

    return rib_chat(task)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="scripts/warm_rib.py",
        description="dump the FROZEN_RIB for the zcode seat + warm the cache prefix")
    ap.add_argument("--skip-warm", action="store_true",
                    help="dump the RIB only; make zero metered calls")
    a = ap.parse_args(argv)

    dest, chars = dump_rib()
    print("RIB written -> " + str(dest.relative_to(ROOT)))
    print("chars=" + str(chars) + " tokens_est=" + str(chars // 4))
    if a.skip_warm:
        return 0
    w = warm_call()
    print("warm_call ok=" + str(w.get("ok")) + " cached=" + str(w.get("cached_tokens"))
          + "/" + str(w.get("prompt_tokens")) + " text=" + str(w.get("text"))[:40])
    return 0 if w.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
