"""B2-378 landing edit: _fold_training passes the row status through.

Hot-file surgery on mag/icon_drop.py with an mtime guard (the board is hot:
the concurrent B2-377 escaping lane wrote this file twice during this lane's
17:58-18:01Z window, so plain editor writes kept losing the freshness check).
The claim line for this file was filed under Open (QUEUE.md 17:58:30Z) before
these bytes were read. Replaces only the _fold_training header through the
record_decision close paren; the training_events.emit block is untouched.
Refuses to double-apply.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

TARGET = Path(__file__).resolve().parents[3] / "mag" / "icon_drop.py"

OLD = '''def _fold_training(row: dict[str, Any]) -> None:
    """Surface the lesson: operator-only action -> icon dropped, not a chat nag."""
    try:
        from mag import skill_ledger, training_events
        skill_ledger.record_decision(
            goal="human-only action routing",
            task_shape="operator_action",
            provider="local",
            model="icon_drop",
            reasoning_level="none",
            source="icon_drop",
            outcome="ok",
            detail=f"dropped icon {row.get('name')} for operator click (no chat nag)",
        )
'''

NEW = '''def _fold_training(row: dict[str, Any]) -> None:
    """Surface the lesson: operator-only action -> icon dropped, not a chat nag.

    B2-378 2026-09-26: outcome is the row status passed through, "ok" only
    when the status is "dropped", otherwise the status string verbatim
    ("failed", "skipped_no_powershell"). Cause: the hardcoded outcome "ok"
    folded every icon_drop row as a win in the operator_behavior case law
    (skill_ledger ok_rate counts outcome == "ok"), so the failed and skipped
    drop_shortcut rows that B2-354 made honest in the icons ledger were still
    counted as wins here; fixed on the brief
    watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md, falsifier
    probe watch/inbox/burn_wave_20260926/B2_378_falsifier_probe.py.
    """
    try:
        from mag import skill_ledger, training_events
        status = str(row.get("status") or "unknown")
        skill_ledger.record_decision(
            goal="human-only action routing",
            task_shape="operator_action",
            provider="local",
            model="icon_drop",
            reasoning_level="none",
            source="icon_drop",
            outcome="ok" if status == "dropped" else status,
            detail=f"icon {row.get('name')} status {status} for operator click (no chat nag)",
        )
'''


def main() -> int:
    for attempt in range(8):
        mtime_before = TARGET.stat().st_mtime_ns
        text = TARGET.read_text(encoding="utf-8")
        if "B2-378 2026-09-26: outcome is the row status passed through" in text:
            print("already applied by a prior run; nothing to do")
            return 0
        if text.count(OLD) != 1:
            raise SystemExit(f"fold anchor not unique (count={text.count(OLD)}); re-read bytes")
        text = text.replace(OLD, NEW, 1)
        time.sleep(0.2)
        if TARGET.stat().st_mtime_ns != mtime_before:
            print(f"attempt {attempt}: file moved mid-edit, re-reading")
            continue
        TARGET.write_text(text, encoding="utf-8", newline="")
        print(f"B2-378 fold edit applied on attempt {attempt}")
        return 0
    print("FAILED: file too hot after 8 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
