"""Log a chord strike: rope named, loops audited, moves committed."""

from __future__ import annotations

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path


def commitment_hash(*parts: str) -> str:
    blob = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def run_strike(
    target: str,
    rope: str = "",
    loops: str = "",
    moves: str = "",
    out_path: str | None = None,
) -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rope = rope or "(unnamed rope)"
    loops = loops or "(none logged)"
    moves = moves or "(none logged)"
    h = commitment_hash(target, rope, loops, moves, now)

    body = f"""# Chord Strike

**When:** {now}  
**Target:** {target}  
**Commitment:** `{h}`

## Plain English

Strike the chord on **{target}**. Name the rope. Surface the loops. Commit the moves.

## Rope (personal impact)

{rope}

## Loops audited

{loops}

## Disentangled moves

{moves}

## Verifiable commitment hash

`{h}`

---
*Mycelial Republic — continuous chord auditing*
"""
    print(body)

    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        print(f"Wrote {p}", file=sys.stderr)
    else:
        # Default log under logs/chord_strikes if cwd is project root
        default_dir = Path("logs/chord_strikes")
        if default_dir.parent.is_dir() or Path("src/mycelial_republic").is_dir():
            default_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            p = default_dir / f"strike_{stamp}_{h}.md"
            p.write_text(body, encoding="utf-8")
            print(f"Wrote {p}", file=sys.stderr)

    return 0
