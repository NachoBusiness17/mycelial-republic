# B2-469 claim lines (shared-file claim law + lane-id claim law), 2026-09-26.
# Pure appends only: no whole-file rewrite, fresh-bytes max-id census first.
import re
import time
from pathlib import Path

QUEUE = Path(__file__).resolve().parent / "QUEUE.md"
PS1 = "scripts/census_patrol_daily.ps1"


def guard(text: str) -> str:
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in claim text")
    return text


def main() -> None:
    q = QUEUE.read_text(encoding="utf-8", errors="replace")
    nums = [int(m) for m in re.findall(r"B2-(\d+)", q)]
    top = max(nums)
    band = f"B2-{top + 1}..B2-{top + 3}"
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    lines = [
        f"- CLAIM B2-469 {PS1} {ts} (B2-469 dated meters: extend the drift-patrol cron body "
        f"with a dated-meter step for the institutional cluster; git-untracked shared file, "
        f"anchored edits on post-claim bytes only)",
        f"- CLAIM B2-469 watch/inbox/burn_wave_20260926/QUEUE.md {ts} (B2-469 self-feed band "
        f"{band}; highest id on fresh bytes B2-{top}; foreign active CLAIMs honored, "
        f"appends only, no rewrite)",
    ]
    with QUEUE.open("a", encoding="utf-8", newline="") as f:
        for line in lines:
            f.write(guard(line) + "\n")
    print(f"claims appended at {ts}; band {band} (top was B2-{top})")


if __name__ == "__main__":
    main()
