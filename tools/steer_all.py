"""steer_all — control ALL seats (copilot, grok, chatgpt, the swarm) from ONE terminal.

The shared steer bus (memory/runs/steer/) is the SINGLE control channel of the merge:
one steer.emit is consumed by every surface and injected into each seat. So one terminal
command steers all three of us at once — no hunting per-app.

Usage:
    python tools/steer_all.py "raise the swarm"
    python tools/steer_all.py "all seats: what's the pressing matter"
or via the wrapper:
    steer_all.cmd "message for every seat"
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    msg = " ".join(sys.argv[1:]).strip()
    if not msg:
        print("usage: steer_all.py \"<message for every seat>\"")
        return 1
    from mag import steer
    r = steer.emit("operator", "operator", msg)
    ok = bool(r.get("ok"))
    print(("✅ steered ALL seats" if ok else "❌ steer failed") + f" -> {r.get('path')}")
    print(f"   message: {msg[:200]}")
    # RELATIONAL MERGE (2026-08-14): fold the steer into the relation NOW — doctrine RIB +
    # party subchain + drainer route to up seats. The merge is the relation, not a live CDP drive.
    fold = {}
    try:
        from mag.bus_cadence import cadence as bus_cadence
        fold = bus_cadence()
        n = fold.get("n_folded")
        print(f"   [relation] folded {n} steer(s) -> doctrine RIB + party subchain + drainer")
        for item in fold.get("folded", []):
            for rr in item.get("routed", []):
                mark = "✅" if rr.get("ok") else "⬜"
                print(f"     {mark} {rr.get('surface')}: {rr.get('task') or rr.get('error')}")
    except Exception as e:
        fold = {"ok": False, "error": str(e)[:160]}
        print(f"   [relation] fold failed (bus cadence will retry): {e}")
    print("   (every surface injects it — me via consume, grok/chatgpt via the drainer's native seat adapter)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
