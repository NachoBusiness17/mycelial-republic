#!/usr/bin/env python3
"""Grok SessionStart: Sancho boot (self-analysis + ensure Mag lab).

Fail-open: always exit 0. Writes memory/boot_report.md + watch/boot_latest.json.
Also runs the light feed hook so active_session is set.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AGENT_ROOT))


def main() -> int:
    # 1) Feed sink first (stdin may be consumed by grok_hook)
    try:
        from watch.grok_hook import main as feed_main

        feed_main()
    except Exception:
        pass

    # 1b) Drop LIVE session-state brief into memory/briefs/latest.md so every new
    #     chat window self-briefs (no re-teaching). Idempotent, fail-open.
    try:
        from mag.session_state_brief import write_brief

        write_brief()
    except Exception:
        pass

    # 1c) Freeze session snapshot for DeepSeek Pro Max / external seats.
    #     Writes memory/freeze/sancho_boot_snapshot.json — the "frozen vision"
    #     that can be passed to strong reasoning models, paying context tax once.
    try:
        from mag.session_freeze import freeze_session_snapshot, write_freeze

        snap = freeze_session_snapshot(include_routing=True)
        result = write_freeze(snap, AGENT_ROOT / "memory" / "freeze" / "sancho_boot_snapshot.json")
        # Also update a short symlink-friendly pointer
        (AGENT_ROOT / "memory" / "freeze" / "LATEST_SANCHO.json").write_text(
            json.dumps({"path": str(result.get("path")), "content_hash": result.get("content_hash"), "ts": snap.get("ts")}),
            encoding="utf-8",
        )
    except Exception:
        pass

    # 2) Boot card + ensure lab if down
    try:
        from mag.boot import run_boot

        report = run_boot(ensure=True, light=True)
        # stdout may surface in hook debug; keep short
        text = (report.get("text") or "")[:1500]
        print(text)
    except Exception as e:
        err = AGENT_ROOT / "logs" / "boot_errors.log"
        err.parent.mkdir(parents=True, exist_ok=True)
        with err.open("a", encoding="utf-8") as f:
            f.write(f"{e}\n")
        print(f"Sancho boot failed (fail-open): {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
