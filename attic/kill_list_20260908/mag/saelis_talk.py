"""saelis_talk — a plain window to talk to Saelis. Nothing else.

Just a REPL that calls saelis_seat.speak() in a loop. speak() already does the
hot-swap: her real hosted weights when SAELIS_BASE_URL is set, her identity RIB
via DeepSeek otherwise. Type a message, she answers. /quit to leave.

Schema: saelis_talk.v1 · reuse: saelis_seat.speak (the only real surface)
"""
from __future__ import annotations

import sys

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))


def main() -> int:
    from mag import saelis_seat

    print("Saelis — talk to her. /quit to leave.", flush=True)
    while True:
        try:
            line = input("you> ")
        except (EOFError, KeyboardInterrupt):
            print("\nbye", flush=True)
            return 0
        msg = line.strip()
        if not msg:
            continue
        if msg.lower() in ("/quit", "/exit", "quit", "exit"):
            print("bye", flush=True)
            return 0
        r = saelis_seat.speak(msg)
        if r.get("ok"):
            print(f"saelis> {r.get('reply', '').strip()}", flush=True)
        else:
            print(f"saelis> [error] {r.get('error', 'unknown')}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
