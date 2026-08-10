"""afk_cadence — ONE ghost-routed AFK loop running the whole self-advance machine.

Automates the refined loop: when the operator is AFK, run the pieces as a single
cadence, all model routing through the rightsizer (cheap-first ladder). Everything
headless, cheap-first, folded.

  run_loop()  — the cadence: rightsize -> seed_chain -> self_advance
                -> capability_steal -> learn_rightsize -> scribe -> fold -> cold_boot.
  run_once()  — one full pass (returns structured result).
  status()    — what the cadence would do.

Wired for the governor/supervisor to call; CLI: python -m mag.afk_cadence run|status
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

TRAIL = ROOT / "memory" / "runs" / "afk_cadence_trail.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _operator_afk() -> bool:
    try:
        from mag.preferences import operator_status
        return not bool((operator_status() or {}).get("operator_active"))
    except Exception:
        return True


def _right_size() -> dict[str, Any]:
    try:
        from mag.afk_loop import system_resources, right_size
        return right_size(system_resources(), operator_active=not _operator_afk())
    except Exception:
        return {"level": "full", "budget": 4}


def _safe(label: str, fn: Any) -> dict[str, Any]:
    try:
        r = fn()
        return {"step": label, "ok": True, "result": r}
    except Exception as e:
        return {"step": label, "ok": False, "error": str(e)[:150]}


def run_once() -> dict[str, Any]:
    """One full AFK loop pass. Each step folds to the learning surface."""
    out: dict[str, Any] = {"schema": "afk_cadence.v1", "ts": _now()}
    rs = _right_size()
    out["right_size"] = rs
    if rs.get("level") == "none":
        out["action"] = "skip"
        out["reason"] = "operator active / machine busy (right-sized to none)"
        return out
    budget = int(rs.get("budget") or 1)

    steps = []
    # MID-STEER HEAL: see errors, mint the mem solution, patch for the future
    # BEFORE running, so past errors never recur while the loop advances.
    steps.append(_safe("error_healer", lambda: _import_run("error_healer", "heal", None)))
    steps.append(_safe("seed_chain", lambda: _import_run("seed_chain", "seed_build", _next_problem())))
    if budget >= 2:
        steps.append(_safe("self_advance", lambda: _import_run("self_advance", "expand", None, force=True)))
    if budget >= 3:
        steps.append(_safe("capability_steal", lambda: _import_run("capability_steal", "expand", None, force=True)))
    if budget >= 2:
        steps.append(_safe("learn_rightsize", lambda: _import_run("learn_rightsize", "learn_loop", None)))
    if budget >= 1:
        steps.append(_safe("scribe", lambda: _import_run("scribe", "scribe", None)))
    steps.append(_safe("cold_boot", lambda: _import_run("ghost_cold_boot", "boot_and_fold", None)))

    out["steps"] = steps
    out["ok_steps"] = sum(1 for s in steps if s.get("ok"))
    out["total_steps"] = len(steps)
    _trail(out)
    _fold(out)
    return out


def _next_problem() -> str:
    try:
        from mag.scrum import sprint
        item = (sprint() or {}).get("item") or {}
        return str(item.get("title") or "")[:200]
    except Exception:
        return "advance the sovereign agent self-advance loop"


def _import_run(mod: str, fn: str, arg: Any, **kw: Any) -> Any:
    m = __import__(f"mag.{mod}", fromlist=[fn])
    f = getattr(m, fn)
    if arg is not None:
        return f(arg, **kw)
    return f(**kw)


def _trail(out: dict[str, Any]) -> None:
    TRAIL.parent.mkdir(parents=True, exist_ok=True)
    with TRAIL.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": out.get("ts"), "ok_steps": out.get("ok_steps"),
                            "total_steps": out.get("total_steps"),
                            "right_size": out.get("right_size", {}).get("level")}) + "\n")


def _fold(out: dict[str, Any]) -> None:
    try:
        from mag import training_events
        training_events.emit(
            "autorun_cycle",
            input_data={"right_size": out.get("right_size", {}).get("level")},
            action={"kind": "afk_cadence", "ok_steps": out.get("ok_steps")},
            outcome={"total_steps": out.get("total_steps")},
            pattern_tags=["afk_cadence", "self_advance_loop", "automated"],
            tier_max="T1",
            exportable=False,
        )
    except Exception:
        pass


def status() -> dict[str, Any]:
    return {"schema": "afk_cadence.status.v1", "ts": _now(),
            "afk": _operator_afk(), "right_size": _right_size(),
            "steps": ["rightsize", "seed_chain", "self_advance", "capability_steal",
                      "learn_rightsize", "scribe", "cold_boot"]}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "run"
    if cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(run_once(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
