"""provider_snapshot_differ - week-over-week differ for provider-probe snapshots.

B2-492 (2026-09-26): the B2-106 cadence lands memory/improve/provider_health/
<day>.json daily-when-due, but nothing reads two of them together, so lane
status flips (mistral 429-zero-quota -> 403-wrong-default within one day;
mistral 403 -> DORMANT after the B2-105 surgery) have to be re-discovered by a
human diffing JSON. This differ reads the two newest snapshots and prints ONE
LINE per lane-status transition:

  FLIP <lane>: <old class> -> <new class>  (snapshots <old day> -> <new day>)

Status class = result.statuses[lane] (a string) when present, else "(absent)".
A lane appearing or disappearing counts as a transition to/from "(absent)".

Usage:
  python tools/provider_snapshot_differ.py              # two newest snapshots
  python tools/provider_snapshot_differ.py A.json B.json  # explicit pair

Exit 0 always on a successful diff (a flip is information, not an error);
exit 2 when fewer than two snapshots exist.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP_DIR = ROOT / "memory" / "improve" / "provider_health"


def _load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    result = data.get("result") if isinstance(data, dict) else None
    statuses = result.get("statuses") if isinstance(result, dict) else None
    return statuses if isinstance(statuses, dict) else {}


def _two_newest() -> tuple[Path, Path] | None:
    files = sorted(SNAP_DIR.glob("*.json"))
    if len(files) < 2:
        return None
    return files[-2], files[-1]


def diff(old_path: Path, new_path: Path) -> list[str]:
    old, new = _load(old_path), _load(new_path)
    lines = []
    for lane in sorted(set(old) | set(new)):
        was = old.get(lane, "(absent)")
        now = new.get(lane, "(absent)")
        if was != now:
            lines.append(
                f"FLIP {lane}: {was} -> {now}  "
                f"(snapshots {old_path.stem} -> {new_path.stem})")
    return lines


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        old_path, new_path = Path(argv[0]), Path(argv[1])
    else:
        pair = _two_newest()
        if pair is None:
            print(f"need two snapshots under {SNAP_DIR}", file=sys.stderr)
            return 2
        old_path, new_path = pair
    for line in diff(old_path, new_path):
        print(line)
    if not any(True for _ in diff(old_path, new_path)):
        print(f"no lane-status transitions {old_path.stem} -> {new_path.stem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
