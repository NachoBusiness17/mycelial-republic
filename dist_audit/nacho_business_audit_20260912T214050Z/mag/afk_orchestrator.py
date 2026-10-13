"""afk_orchestrator — run the whole AFK advance stack as ONE ghost-routed cadence.

The operator: "we have so much scaffolding — look at what remains and rightsize it,
and build it via our systems and ghost." The rightsize finding: every AFK capability
exists (capability_steal, self_advance, learn_rightsize, scribe, data_source_watch,
cold_boot) but runs SEPARATELY. This module ties them into ONE pass that runs well:
  run_afk() — when AFK/offline, right-sized:
    1. data_source_watch.watch   — plan+observe high-quality sources (no blind ingest)
    2. capability_steal.expand   — steal-search, test local model, fold verified
    3. self_advance.expand       — socratic reflection + skill-expansion plan
    4. learn_rightsize.loop      — auto-catalog + right-size the learning corpus
    5. scribe.scribe             — the cheap model renders it all as the surface
    6. cold_boot check           — confirm the core is bootable (the material survives)
  Each folds to the learning loop. Right-sized to load (never hogs when busy),
  headless, routed through ghost. run_afk is the "make the scaffold run as one loop."

CLI:  python -m mag.afk_orchestrator run [--force] | status
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _operator_offline() -> bool:
    try:
        from mag.preferences import operator_status
        return not bool((operator_status() or {}).get("operator_active"))
    except Exception:
        return True


def _right_size() -> str:
    try:
        from mag.afk_loop import system_resources, right_size
        return right_size(system_resources(), operator_active=not _operator_offline())["level"]
    except Exception:
        return "full"


def run_afk(*, force: bool = False) -> dict[str, Any]:
    """The one-pass AFK advance cadence (right-sized, ghost-routed)."""
    try:
        from mag.operator_mode import pause_reason
        if (reason := pause_reason()):
            return {"ok": True, "action": "skip", "reason": reason}
    except Exception:
        pass
    if not force and not _operator_offline():
        return {"ok": True, "action": "skip", "reason": "operator active (AFK-only)"}
    level = _right_size()
    if level == "none":
        return {"ok": True, "action": "skip", "reason": "right-sized to none (busy/active)"}
    budget = {"light": 1, "medium": 2, "full": 4}[level]

    steps: dict[str, Any] = {}
    # 1) sources
    steps["sources"] = _safe("mag.data_source_watch", "watch", "")
    # 2) capability steal (only if budget)
    if budget >= 1:
        steps["capability_steal"] = _safe("mag.capability_steal", "expand", "")
    # 3) self-advance reflection
    if budget >= 2:
        steps["self_advance"] = _safe("mag.self_advance", "expand", "")
    # 4) learn rightsize
    if budget >= 2:
        steps["learn_rightsize"] = _safe("mag.learn_rightsize", "learn_loop", "")
    # 5) scribe renders the surface
    steps["scribe"] = _safe("mag.scribe", "scribe", "")
    # 6) cold-boot check (core bootable = the material survives)
    steps["cold_boot"] = _safe("mag.ghost_cold_boot", "cold_boot", "")

    _fold(level, len(steps))
    return {"schema": "afk_orchestrator.run.v1", "ts": _now(),
            "offline": True, "right_size": level, "n_steps": len(steps),
            "steps": {k: _brief(v) for k, v in steps.items()}}


def _safe(mod: str, fn: str, arg: str) -> dict[str, Any]:
    try:
        m = __import__(mod, fromlist=[fn])
        f = getattr(m, fn)
        try:
            res = f(arg) if arg else f()
        except TypeError:
            res = f()
        return {"ok": True, "result": res}
    except Exception as e:
        return {"ok": False, "error": str(e)[:120]}


def _brief(v: dict[str, Any]) -> dict[str, Any]:
    if not v.get("ok"):
        return {"ok": False, "error": v.get("error", "")[:120]}
    r = v.get("result") or {}
    if isinstance(r, dict):
        return {k: r.get(k) for k in ("right_size", "n_expanded", "folded", "whispers_found", "decoded") if k in r}
    return {"ok": True}


def _fold(level: str, n_steps: int) -> None:
    try:
        from mag import training_events
        training_events.emit(
            "autorun_cycle",
            input_data={"right_size": level, "n_steps": n_steps},
            action={"kind": "afk_orchestrator", "offline": True},
            outcome={"ran": True},
            pattern_tags=["afk_orchestrator", "one_pass", "ghost_cadence", "rightsized"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "status":
        print(json.dumps({"schema": "afk_orchestrator.status.v1", "ts": _now(),
                          "offline": _operator_offline(), "right_size": _right_size()},
                         indent=2, ensure_ascii=False))
        return 0
    print(json.dumps(run_afk(force="--force" in argv), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
