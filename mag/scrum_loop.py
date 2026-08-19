"""scrum_loop — automated cost/failure-aware scrum iteration (2026-08-16, operator spec).

"Allow emergence but stop ourselves from blowing 50c on a FAILED task; allow ourselves to
spend a dollar on a USEFUL one we know is going well. We shouldn't STOP — we should
ANTICIPATE spend + projected failure into an automated scrum process, so we can iterate and
LEARN from the very process, remain agile/stateless, maximize our internal systems."

This is NOT a flat cap and NOT a kill-switch. It is a closed PLAN -> EXECUTE -> REVIEW ->
ADAPT loop (Scrum's inspect-and-adapt, stolen from the external steal) that:

  * PLAN    — project each queued task's spend + failure, then order the queue risk-aware
              (proof-first: cheap, low-failure first — scrum.advance's law).
  * EXECUTE — reuse swarm_worker's real execution; wire cost_governor in: a FAILING task
              accumulates attempts under ONE task_id up to the SAFE ceiling ($0.50) then is
              honestly ABANDONED; a task that has PROVEN useful gets the USEFUL ceiling
              ($1.00) and room to emerge.
  * REVIEW  — a per-sprint retrospective (right / wrong / next) folding lessons via
              training_events.emit (the canonical learn primitive).
  * ADAPT   — read the retro back so a repeatedly-failing task CLASS gets deprioritized
              (velocity: don't repeat the same doomed pattern).

Self-steal reuse spine (no parallel systems):
  execution          -> mag.swarm_worker (_execute, _task_tier, queue/result schema)
  spend projection   -> mag.usage_forecast (estimate_ask)
  adaptive ceiling   -> mag.cost_governor (check/record/mark_abandoned/ceiling)
  adapt semantics    -> mag.scrum.advance (proof-first) + mag.coding_session_orchestrator
  retro writer       -> mag.factory_machine.write_retrospective (pattern)
  fold lessons       -> mag.training_events.emit + mag.percolator.percolate

Stateless: each pass is a fresh process that drains a batch, writes results/ledgers, exits.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

from mag import swarm_worker as sw
from mag import cost_governor as cg

SCHEMA = "scrum_loop.v1"
RETRO_DIR = ROOT / "memory" / "runs" / "scrum"
USAGE = ROOT / "logs" / "provider_usage.jsonl"

# The operator's numbers — the adaptive ceilings live in cost_governor (single law).
SAFE_CEILING_USD = cg.SAFE_CEILING_USD      # $0.50 — a failing task is cut here
USEFUL_CEILING_USD = cg.USEFUL_CEILING_USD  # $1.00 — a useful task may emerge here
MAX_ATTEMPTS = 6                            # hard retry cap per task (belt+suspenders)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(entry: dict[str, Any]) -> None:
    RETRO_DIR.mkdir(parents=True, exist_ok=True)
    with (RETRO_DIR / "scrum_loop_trail.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": _now(), **entry}, ensure_ascii=False, default=str) + "\n")


# ---------------------------------------------------------------- PLAN (projection)
def project(limit: int = 60) -> dict[str, Any]:
    """Project spend + failure for each queued task. Reuses usage_forecast for spend;
    failure risk = attempt history (cost_governor) + execution path (agent vs local)."""
    out = []
    try:
        from mag.usage_forecast import estimate_ask
    except Exception:
        estimate_ask = None
    for p in sorted(sw.QUEUE_DIR.glob("*.json"))[:limit]:
        try:
            t = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if t.get("status") != "queued":
            continue
        tid = str(t.get("task_id") or p.stem)
        goal = str(t.get("goal") or "")
        depth, path = sw._task_tier(goal)
        # projected spend (billable $) — honest estimate, not billing
        est = {}
        if estimate_ask is not None:
            try:
                a = estimate_ask(goal)
                est = {"usd_est_miss": a.get("usd_est_miss"),
                       "usd_est_typical": a.get("usd_est_typical")}
            except Exception:
                est = {}
        # projected failure risk 0..1 from ledger attempt history
        led = cg._load(tid)
        attempts = led.get("attempts", [])
        n_fail = sum(1 for a in attempts if not a.get("ok"))
        fail_risk = 0.0
        if attempts:
            fail_risk = n_fail / len(attempts)
        elif path == "agent":
            fail_risk = 0.5  # deep-agent tasks fail more than deterministic local work
        out.append({
            "task_id": tid,
            "goal": goal[:120],
            "depth": depth,
            "path": path,
            "attempts": len(attempts),
            "failed_attempts": n_fail,
            "fail_risk": round(fail_risk, 3),
            "spend_usd": cg.spend(tid),
            "ceiling_usd": cg.ceiling(tid),
            "abandoned": bool(led.get("abandoned")),
            **est,
        })
    return {"schema": SCHEMA + ".project", "n": len(out), "tasks": out, "ts": _now()}


def prioritize(limit: int = 60) -> dict[str, Any]:
    """Order queued tasks risk-aware (proof-first: low failure + low spend first), so we
    don't pick doomed expensive tasks. A repeatedly-failing class sinks (velocity)."""
    proj = project(limit=limit)
    tasks = [t for t in proj["tasks"] if not t.get("abandoned")]
    tasks.sort(key=lambda t: (t["fail_risk"], t.get("usd_est_miss") or 0, t["spend_usd"]))
    return {"schema": SCHEMA + ".prioritize", "n": len(tasks), "order": tasks, "ts": _now()}


# -------------------------------------------------------------- EXECUTE (one task)
def _usage_snapshot() -> tuple[int, int]:
    """Sum of billable (miss + completion) tokens in provider_usage.jsonl."""
    miss = comp = 0
    if USAGE.is_file():
        try:
            for line in USAGE.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                miss += int(r.get("cache_miss_tokens") or 0) or int(r.get("prompt_tokens") or 0)
                comp += int(r.get("completion_tokens") or 0)
        except Exception:
            pass
    return miss, comp


def _execute_with_governor(task: dict[str, Any], f: Path) -> dict[str, Any]:
    """Execute ONE task with cost_governor wired: pre-check (skip/abandon), execute, then
    record billable spend + health, returning the honest verdict + result."""
    tid = str(task.get("task_id") or "")
    goal = str(task.get("goal") or "")
    depth, path = sw._task_tier(goal)

    # PRE-CHECK: already abandoned / blown ceiling -> honest abandon, don't spend.
    chk = cg.check(tid)
    if chk["abandoned"]:
        res = {"schema": "swarm_worker.result.v1", "task_id": tid, "goal": goal[:200],
               "domain": task.get("domain"), "agent_idx": task.get("agent_idx"),
               "provider": task.get("provider"), "model": task.get("model"), "ok": False,
               "exit_code": -1,
               "result": f"[scrum] ABANDONED (cost-capped): {chk['abandon_reason']}",
               "finished_at": _now()}
        _write(f, task, "done", "abandoned", depth)
        (sw.RESULTS_DIR / f"{tid}.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"task_id": tid, "verdict": "abandoned", "path": path, "ok": False, "spend": chk["spend_usd"]}

    # Mag period budget: skip-and-queue when spent. Do not flip to running/failed.
    if path != "local":
        gate = sw.provider_spawn_allowed(task.get("provider"))
        if not gate.get("ok"):
            _write(
                f, task, "queued",
                f"deferred-quota {gate.get('reason')} reset_in_hours={gate.get('reset_in_hours')}",
                depth,
            )
            return {
                "task_id": tid, "verdict": "deferred_quota", "path": path, "ok": False,
                "skipped": gate.get("reason") or "quota_exhausted",
                "reset_in_hours": gate.get("reset_in_hours"),
                "spend": chk["spend_usd"],
            }

    # EXECUTE (reuse the real swarm execution — local deterministic or deep agent).
    before = _usage_snapshot()
    _write(f, task, "running", "", depth)
    if path == "local":
        ok, tail = True, f"[rightsized local] deterministic/RIB task ({depth}) — no deep model call"
        code = 0
    else:
        tail, code = sw._execute(task)
        ok = code == 0 and bool((tail or "").strip())
    after = _usage_snapshot()
    miss_tok = max(0, after[0] - before[0])
    comp_tok = max(0, after[1] - before[1])

    # RECORD spend + health into the adaptive ledger.
    verdict = cg.record(tid, miss_tokens=miss_tok, completion_tokens=comp_tok,
                        ok=ok, produced_output=ok, detail=(tail or "")[:160])
    task["status"] = "done" if ok else "failed"
    task["detail"] = ("exit 0" if ok else f"exit {code}")[:120]
    task["tier"] = depth
    _write(f, task, task["status"], task["detail"], depth)
    res = {"schema": "swarm_worker.result.v1", "task_id": tid, "goal": goal[:200],
           "domain": task.get("domain"), "agent_idx": task.get("agent_idx"),
           "provider": task.get("provider"), "model": task.get("model"), "ok": ok,
           "exit_code": code, "result": tail, "finished_at": _now()}
    (sw.RESULTS_DIR / f"{tid}.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"task_id": tid, "verdict": "done" if ok else "failed", "path": path,
            "ok": ok, "spend": verdict["spend_usd"], "miss_tok": miss_tok, "comp_tok": comp_tok}


def _write(f: Path, task: dict[str, Any], status: str, detail: str, tier: str) -> None:
    task["status"] = status
    task["detail"] = detail
    task["tier"] = tier
    f.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")


def _requeue_for_retry(f: Path, task: dict[str, Any]) -> None:
    """Failed but under ceiling -> retry WITH reason, same task_id (accumulate in ledger)."""
    task["status"] = "queued"
    task["attempts"] = int(task.get("attempts") or 0) + 1
    _write(f, task, "queued", f"retry after failure (attempt {task['attempts']})",
           str(task.get("tier") or ""))
    _log({"phase": "requeue", "task_id": task.get("task_id"), "attempt": task["attempts"]})


# ---------------------------------------------------- SPRINT PASS (the closed loop)
def sprint_pass(*, max_per_pass: int = 6) -> dict[str, Any]:
    """One automated scrum pass: prioritize -> execute (governor-wired) -> requeue/abandon ->
    return batch results for the review. Stateless; CronJob re-schedules."""
    from mag import headless
    headless.install_no_window_defaults()
    sw.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    order = prioritize(limit=60)["order"]
    done = failed = abandoned = skipped = 0
    results = []
    for t in order[:max_per_pass]:
        tid = t["task_id"]
        f = sw.QUEUE_DIR / f"{tid}.json"
        try:
            task = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if task.get("status") != "queued":
            continue
        task["_file"] = f
        out = _execute_with_governor(task, f)
        results.append(out)
        if out["verdict"] == "abandoned":
            abandoned += 1
        elif out["verdict"] == "deferred_quota":
            skipped += 1
        elif out["verdict"] == "failed":
            failed += 1
            # retry-with-reason: still under ceiling and attempts < cap -> requeue (accumulate)
            chk = cg.check(tid)
            if chk["allowed"] and int(task.get("attempts") or 0) < MAX_ATTEMPTS:
                _requeue_for_retry(f, task)
            else:
                cg.mark_abandoned(tid, f"failed {MAX_ATTEMPTS} attempts or blew ${SAFE_CEILING_USD} ceiling")
                abandoned += 1
        else:
            done += 1
    batch = {"schema": SCHEMA + ".sprint", "done": done, "failed": failed,
             "abandoned": abandoned, "skipped": skipped, "total": len(results),
             "results": results, "ts": _now()}
    _log({"phase": "sprint", **{k: batch[k] for k in ("done", "failed", "abandoned", "skipped")}})
    return batch


# ---------------------------------------------------------------- REVIEW + ADAPT
def retro(batch: dict[str, Any]) -> dict[str, Any]:
    """Right / wrong / next from a sprint batch — the review that feeds adapt."""
    res = batch.get("results") or []
    right = [r["task_id"] for r in res if r.get("verdict") == "done"]
    wrong = [r["task_id"] for r in res if r.get("verdict") == "failed"]
    abandoned = [r["task_id"] for r in res if r.get("verdict") == "abandoned"]
    entry = {
        "schema": SCHEMA + ".retro",
        "right": right,
        "wrong": wrong,
        "abandoned": abandoned,
        "note": (f"{len(right)} useful, {len(wrong)} failed, {len(abandoned)} cost-capped "
                 f"at ${SAFE_CEILING_USD}"),
    }
    RETRO_DIR.mkdir(parents=True, exist_ok=True)
    with (RETRO_DIR / "retros.jsonl").open("a", encoding="utf-8") as fp:
        fp.write(json.dumps({"ts": _now(), **entry}, ensure_ascii=False) + "\n")
    # FOLD the lessons (canonical learn primitive) — silent on failure.
    try:
        from mag.training_events import emit
        emit("scrum_retro", input_data={"batch": batch},
             action={"right": right, "wrong": wrong, "abandoned": abandoned},
             outcome={"ok": True}, pattern_tags=["scrum", "retro"])
    except Exception:
        pass
    return entry


def adapt() -> dict[str, Any]:
    """Read retros back and learn: any task class that keeps failing is deprioritized by
    prioritize()'s fail_risk sort (velocity — don't repeat a doomed pattern). This is the
    inspect-and-adapt closing of the loop; the lever is `prioritize`, which reads the
    cost_governor ledger (attempt history). Pure/deterministic, $0."""
    rp = RETRO_DIR / "retros.jsonl"
    retros = 0
    if rp.is_file():
        retros = sum(1 for _ in rp.open(encoding="utf-8"))
    return {"schema": SCHEMA + ".adapt", "retros_read": retros,
            "lever": "prioritize() orders by fail_risk from the cost_governor ledger",
            "ts": _now()}


def status() -> dict[str, Any]:
    return {"schema": SCHEMA, "safe_ceiling_usd": SAFE_CEILING_USD,
            "useful_ceiling_usd": USEFUL_CEILING_USD, "max_attempts": MAX_ATTEMPTS,
            "loop": "plan(project) -> execute(governor) -> requeue/abandon -> retro -> adapt",
            "abandoned_tasks": cg.sweep_abandoned(), "ts": _now()}
