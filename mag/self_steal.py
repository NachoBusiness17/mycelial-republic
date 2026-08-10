"""Self-steal audit — surface where operating surfaces aren't utilizing our own systems.

Part of doctor/maintenance. The self-steal protocol applied to OUR OWN architecture:
detect capabilities (modules/ledgers/surfaces) that exist but aren't being utilized —
either not wired, or their evidence/state is stale (not used recently). For flagged gaps
that warrant deep analysis, LAUNCH/RESUME a research project by enqueueing it to the queue
(the drainer runs it). Example: if the verkle-knot anchoring evidence is stale, enqueue a
verkle deep-analysis research task.

Deterministic ($0, no LLM). Schema: self_steal.v1

CLI:  python -m mag.self_steal              (audit, print)
      python -m mag.self_steal --cadence    (idempotent: audit + leaf + enqueue research for new gaps)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT

STATE_DIR = ROOT / "memory" / "runs" / "self_steal"
STATE = STATE_DIR / "state.json"
SCHEMA = "self_steal.v1"

# Internal capabilities we should be utilizing. Each: existence + freshness of evidence
# (state/ledger updated recently = utilized). research_goal = research task to LAUNCH/RESUME
# when this capability is found under-utilized (deep-analysis worth paying for).
CAPABILITIES: list[dict[str, Any]] = [
    {
        "name": "verkle_knot",
        "module": "mag/verkle_knot.py",
        "evidence": "memory/biography/verkle_tip.json",
        "stale_s": 86400,  # 24h — knot not anchored/advanced recently
        "research_goal": ("RESEARCH-PACK self_steal verkle deep-analysis: resume deep analysis of the "
                          "verkle knot — the verkle_tip has not advanced recently, meaning surfaces may "
                          "not be anchoring state. Research how to make verkle anchoring automatic on "
                          "every state write and where surfaces bypass it. Read memory/biography/verkle_tip.json "
                          "+ memory/design/cost_learning_loop.md, produce a concrete wiring plan."),
    },
    {
        "name": "cache_map",
        "module": "mag/cache_map.py",
        "evidence": "memory/runs/cache_map",
        "stale_s": 172800,
        "research_goal": None,  # tracked; report-only
    },
    {
        "name": "cost_learn",
        "module": "mag/cost_learn.py",
        "evidence": "memory/improve/daily",
        "stale_s": 172800,
        "research_goal": None,
    },
    {
        "name": "usage_forecast",
        "module": "mag/usage_forecast.py",
        "evidence": "memory/runs/cost_learn",
        "stale_s": 172800,
        "research_goal": None,
    },
    {
        "name": "session_maze",
        "module": "mag/session_maze.py",
        "evidence": "memory/graph/session_maze.json",
        "stale_s": 86400,
        "research_goal": None,
    },
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _mtime(rel: str) -> float:
    p = ROOT / rel
    if p.is_file():
        return p.stat().st_mtime
    if p.is_dir():
        newest = 0.0
        for f in p.rglob("*"):
            try:
                newest = max(newest, f.stat().st_mtime)
            except OSError:
                continue
        return newest
    return 0.0


def _wired(name: str) -> bool:
    """True if the capability's module is referenced anywhere in the framework."""
    for base in ("main.py", "mag", "dashboard", "watch", "tools"):
        bp = ROOT / base if base != "main.py" else ROOT / "main.py"
        if not bp.exists():
            continue
        files = [bp] if bp.is_file() else list(bp.rglob("*.py"))
        for f in files:
            try:
                if name in f.read_text(encoding="utf-8", errors="replace"):
                    return True
            except OSError:
                continue
    return False


def audit() -> dict[str, Any]:
    """Scan each internal capability for utilization: not wired, or evidence stale/absent."""
    now = _now()
    findings: list[dict[str, Any]] = []
    for cap in CAPABILITIES:
        name = cap["name"]
        module_ok = (ROOT / cap["module"]).is_file()
        mtime = _mtime(cap["evidence"])
        age = (now.timestamp() - mtime) if mtime else None
        stale = age is not None and age > cap["stale_s"]
        absent = age is None
        wired = _wired(name) if module_ok else False
        utilization = "ok"
        if absent:
            utilization = "absent"
        elif stale:
            utilization = "stale"
        if not wired and module_ok:
            utilization = "unwired"
        if utilization != "ok":
            findings.append({
                "capability": name,
                "utilization": utilization,
                "age_s": int(age) if age is not None else None,
                "module": cap["module"],
                "wired": wired,
                "research_goal": cap.get("research_goal"),
                "recommendation": ("research/launch" if cap.get("research_goal") else "report-only"),
            })
    return {
        "schema": SCHEMA,
        "ts": now.isoformat(),
        "n_capabilities": len(CAPABILITIES),
        "n_findings": len(findings),
        "findings": findings,
    }


def _research_already_queued(goal: str) -> bool:
    try:
        from mag.orchestrator import queue_has_goal
        return bool(queue_has_goal(goal[:100]))
    except Exception:
        return False


def enqueue_research(finding: dict[str, Any]) -> dict[str, Any]:
    """Launch/resume the research task for a flagged gap (enqueue to queue -> drainer runs it)."""
    goal = finding.get("research_goal")
    if not goal:
        return {"ok": False, "action": "no_research_goal", "capability": finding["capability"]}
    if _research_already_queued(goal):
        return {"ok": True, "action": "already_queued", "capability": finding["capability"]}
    try:
        from mag.orchestrator import enqueue
        r = enqueue(goal, provider="deepseek", model="deepseek-v4-flash", tag="self-steal-research")
        return {"ok": bool(r.get("ok")), "action": "enqueued", "queue_id": r.get("queue_id"),
                "capability": finding["capability"]}
    except Exception as e:
        return {"ok": False, "action": "error", "error": str(e)[:200], "capability": finding["capability"]}


def run_cadence() -> dict[str, Any]:
    """Idempotent maintenance pass: audit -> leaf + launch/resume research for NEW gaps only."""
    a = audit()
    launches = []
    last_seen: set[str] = set()
    if STATE.is_file():
        try:
            last_seen = set((json.loads(STATE.read_text(encoding="utf-8")) or {}).get("seen", []))
        except Exception:
            last_seen = set()
    seen = set()
    for f in a["findings"]:
        key = f"{f['capability']}:{f['utilization']}"
        seen.add(key)
        if key in last_seen:
            continue  # already surfaced; don't re-enqueue
        if f.get("research_goal") and f["utilization"] in ("stale", "absent", "unwired"):
            launches.append(enqueue_research(f))
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"ts": _now().isoformat(), "seen": sorted(seen)}, indent=2), encoding="utf-8")
    leaf = STATE_DIR / f"self_steal_{a['ts'][:10]}.md"
    lines = [f"# Self-Steal Audit ({a['ts'][:10]})", "",
             f"- Capabilities scanned: {a['n_capabilities']} · findings: {a['n_findings']}", "",
             "| capability | utilization | age_s | wired | action |", "|---|---|---|---|---|"]
    for f in a["findings"]:
        lines.append(f"| {f['capability']} | {f['utilization']} | {f.get('age_s') or '-'} | {f['wired']} | {f['recommendation']} |")
    leaf.write_text("\n".join(lines), encoding="utf-8")
    return {"ok": True, "action": "ran", "findings": a["n_findings"], "launches": launches, "leaf": str(leaf)}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="self-steal", description="Self-steal capability-utilization audit")
    ap.add_argument("--cadence", action="store_true", help="idempotent: audit + leaf + launch/resume research")
    args = ap.parse_args(argv)
    res = run_cadence() if args.cadence else audit()
    print(json.dumps(res, indent=2, default=str)[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
