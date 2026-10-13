"""_audit_swarm_queue.py — audit the queued swarm tasks: age, surface, domain, staleness.

The operator (2026-08-15): "can we audit those 954 tasks" — apply the bones-not-sacred-cows doctrine:
separate LIVE work from STALE holdovers that never drained. Read-only, deterministic, $0.

Schema: _audit_swarm_queue.v1 · deterministic + $0 · honest (real bytes from the queue dir)
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "memory" / "runs" / "swarm_worker" / "queue"


def _dt(s: str):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def main() -> None:
    tasks = []
    for p in sorted(QDIR.glob("*.json")):
        try:
            o = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        created = _dt(o.get("created_at"))
        tasks.append({
            "id": o.get("task_id", p.stem),
            "tag": str(o.get("tag") or ""),
            "domain": str(o.get("domain") or ""),
            "provider": str(o.get("provider") or ""),
            "created": created,
            "age_days": (datetime.now(timezone.utc) - created).days if created else None,
        })

    n = len(tasks)
    print(f"TOTAL QUEUED: {n}")
    if not n:
        return

    # by age (staleness)
    by_day = Counter(t["created"].strftime("%Y-%m-%d") for t in tasks if t["created"])
    print("\n== BY CREATED DAY ==")
    for day in sorted(by_day):
        print(f"  {day}: {by_day[day]}")

    # stale = older than 3 days (never drained from an earlier era)
    stale = [t for t in tasks if t["age_days"] is not None and t["age_days"] > 3]
    recent = [t for t in tasks if t["age_days"] is not None and t["age_days"] <= 3]
    print(f"\n== STALENESS ==  >3 days old (stale bones): {len(stale)}  |  <=3 days (live): {len(recent)}")

    # by tag (surface)
    print("\n== TOP TAGS (surface) ==")
    for tag, c in Counter(t["tag"] for t in tasks).most_common(15):
        print(f"  {tag}: {c}")

    # by domain
    print("\n== BY DOMAIN ==")
    for dom, c in Counter(t["domain"] for t in tasks).most_common(10):
        print(f"  {dom}: {c}")

    # distinct-ish goals sample (from stale, to show what the bones are)
    goals = []
    for p in sorted(QDIR.glob("*.json"))[:400]:
        try:
            o = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        g = str(o.get("goal") or "")[:90]
        if g:
            goals.append(g)
    print("\n== SAMPLE GOALS (first 6) ==")
    for g in goals[:6]:
        print(f"  - {g}")


if __name__ == "__main__":
    main()
