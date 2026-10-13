"""seed_init — lay down a fresh estate skeleton in a target folder (the salon's #1).

Usage:  python engines/seed_init.py <target-dir>

Creates: records/ logs/ watch/inbox/ configs/ + copies the laws and a starter .env
template, then prints the first three commands. The first smith run will show every
organ DARK — that is not an error; that is the method telling the truth about a
zero state (law 4). The key audit will pass on the template's "awaiting" entries and
fail loud the moment you add a live key without declaring it (law 7).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python engines/seed_init.py <target-dir>")
        return 2
    target = Path(sys.argv[1]).resolve()
    if target.exists() and any(target.iterdir()):
        print(f"refusing: {target} exists and is not empty (pick a fresh folder)")
        return 1
    target.mkdir(parents=True, exist_ok=True)
    for sub in ("records", "logs", "watch/inbox", "configs"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    for doc in ("THE_METHOD.md", "FIRST_BOOT.md", "SETUP.md", "DATA_TIERS.md",
                "MORNING_LOOP.md", "SALON.md", "TOUR.md", "AGENTS.md", "SKILLS.md"):
        src = SEED / doc
        if src.is_file():
            shutil.copyfile(src, target / doc)
    for cfg in ("keys.json", "chores.json"):
        src = SEED / "configs" / cfg
        if src.is_file():
            shutil.copyfile(src, target / "configs" / cfg)
    env_t = target / ".env.template"
    env_t.write_text(
        "# provider keys go here as NAME=value (see ACCOUNTS.md for the 2x playbook)\n"
        "# whatever you put here, also declare it in configs/keys.json\n", encoding="utf-8")
    print(f"estate skeleton laid down at {target}")
    print("your first three commands (from inside the folder):")
    print("  1. python <seed>/engines/estate_smith_chart.py --no-plot   # your honest zero state: all DARK")
    print("  2. python <seed>/engines/key_law.py --audit                # passes on 'awaiting'; fails loud on live-undeclared")
    print("  3. python <seed>/engines/cooker.py status                  # your free-lane reset table")
    print("then read FIRST_BOOT.md and start one record. The method demonstrates itself by failing loud.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
