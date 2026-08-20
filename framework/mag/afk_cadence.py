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
    # FRONTIER REACH BY DEFAULT (operator 2026-08-15: "how do we do that by default"): ensure the
    # host-loopback CDP seat (mag.host_browser on 127.0.0.1:9222 — the PROVEN transport that
    # browser_driver connects to by default, bypassing the broken Docker CDP forwarding) is up
    # every cycle, so the operator-safe frontier surfaces (grok/chatgpt/deepseek via browser_driver)
    # are reachable without a manual step and without ever touching the desktop keyboard.
    steps.append(_safe("frontier_reach", lambda: _import_run("host_browser", "ensure", None)))
    # FREE-COMPUTE HUNT (legacy afk_loop) — always: scan free tiers for running/more freebies, $0.
    steps.append(_safe("freebie_scan", lambda: _import_run("afk_loop", "freebie_scan", None)))
    # DOGFOOD SENTINEL (this is why we dogfood): probe the real systems every cycle so failures
    # (cache-miss waste, broken grok dispatch, graph persistence) SURFACE instead of hiding.
    steps.append(_safe("dogfood_audit", lambda: _import_run("dogfood_audit", "audit", None)))
    steps.append(_safe("seed_chain", lambda: _import_run("seed_chain", "seed_build", _next_problem())))
    if budget >= 2:
        steps.append(_safe("self_advance", lambda: _import_run("self_advance", "expand", None, force=True)))
    # GHOST AUTO (bounded, cheap): synthesize the tesuji leaf, record sizing, and dispatch a bounded
    # frontier-steered stateless agent (cap=1/day) to mine the untagged shadow corpus.
    steps.append(_safe("ghost_auto", lambda: _import_run("ghost_auto", "run_cadence", None)))
    # AUTO HANDOFF: keep a current handoff persisted every cycle so any new chat picks up cleanly
    # without asking (the operator wants handoffs automatic, not on request).
    steps.append(_safe("auto_handoff", lambda: _import_run("auto_handoff", "run", None)))
    # VS CODE SEAT: auto-prepare a ready-to-paste controlled task spec from the pending backlog,
    # so the next chat (or a fresh executor seat) has an opener ready — no re-explaining.
    steps.append(_safe("vscode_seat", lambda: _import_run("vscode_seat", "cadence_generate", None)))
    if budget >= 3:
        steps.append(_safe("capability_steal", lambda: _import_run("capability_steal", "expand", None, force=True)))
        # THE BUS SWARM (legacy emergent_harvest) — full-time, rightsized: the flock hunts
        # emergent tesuji across free compute + shared invariants. Full blast, not runaway.
        steps.append(_safe("emergent_harvest", lambda: _import_run("emergent_harvest", "tesuji_harvest", None, n_agents=40, steps=120)))
    if budget >= 2:
        steps.append(_safe("learn_rightsize", lambda: _import_run("learn_rightsize", "learn_loop", None)))
    if budget >= 1:
        steps.append(_safe("scribe", lambda: _import_run("scribe", "scribe", None)))
    # GPU AFK inference-training: if operator AFK + GPU free + local models up, run FREE local
    # inference on curated seed prompts -> training rows -> folded. Free compute -> training data.
    steps.append(_safe("gpu_afk_train", lambda: _import_run("gpu_ghost", "afk_train", None)))
    steps.append(_safe("cold_boot", lambda: _import_run("ghost_cold_boot", "boot_and_fold", None)))
    # ---- SELF-RUNNING AUGMENTATION (operator 2026-08-10: 'wire the full autonomous loop') ----
    # DOCTRINE DEDUPE: consolidate structural-template doctrine families (template = invariant,
    # instances = data) so the graph never bloats. $0.
    steps.append(_safe("doctrine_dedupe", lambda: _import_run("template_invariant", "consolidate_all", None)))
    # MEMORY CONSOLIDATE (2026-08-18, the missing half of persistence): fold the shared mem_lands
    # layer — importance + recursive summary + decayed retrieval + active layer — so retrieval
    # stays sharp and long sessions don't bloat. Deterministic $0; the 4B/frontier scorer is a
    # pluggable hook. The republic's memory sleeps here.
    steps.append(_safe("memory_consolidate", lambda: _import_run("memory_consolidate", "run_sleep_step", None)))
    # CORPUS MINE: mine the leaked-prompt corpus for invariants (expand the knowledge corpus). $0.
    steps.append(_safe("corpus_mine", lambda: _import_run("leaked_prompt_mine", "mine", None)))
    # GHOST PLAY: the ghost experiments on the swarms/tools -> training rows + steer-protocol learning.
    steps.append(_safe("ghost_play", lambda: _import_run("ghost_experimenter", "ghost_play", None, iterations=2)))
    # READOUT FOLD: close the reservoir loop — read the liquid, curate + inject the readout back.
    steps.append(_safe("readout_fold", lambda: _import_run("readout_controller", "control_loop", None, iterations=1)))
    # RIB RECONCILE: report how the k8s cluster conforms to the RIB invariants (read-only; no auto-apply).
    steps.append(_safe("rib_reconcile", lambda: _import_run("rib_k8s", "reconcile", None, apply=False)))
    # STEER RESUME: process any pinned tasks from the steer protocol (pop the pin stack).
    steps.append(_safe("steer_resume", lambda: _import_run("steer_router", "resume", None)))
    # ---- HONESTY EVERYWHERE (operator 2026-08-10): the ponytail grounding audit runs every cycle
    # so ungrounded doctrine (incl. mislabeled 'grok/frontier' claims) is CHALLENGED, not trusted.
    steps.append(_safe("ponytail_grounding", lambda: _import_run("ponytail_audit", "run_audit", None)))

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
            "steps": ["rightsize", "freebie_scan", "seed_chain", "self_advance",
                      "capability_steal", "emergent_harvest", "learn_rightsize", "scribe", "cold_boot"]}


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
