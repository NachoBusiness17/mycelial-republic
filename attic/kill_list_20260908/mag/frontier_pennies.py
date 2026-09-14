"""frontier_pennies — frontier intelligence distributed for pennies.

OPERATOR (2026-08-12): "frontier intelligence distributed for pennies."

DOCTRINE (already ours, agent_corpus verified lesson): "100 cheap quantized workers < 1 frontier
token for reproducible verifiable work." Spend the scarce frontier allowance ONCE to produce an
insight, QUANTIZE it into a cheap distributable form, DISTRIBUTE it to the penny-cheap swarm, and
MEASURE the multiplier. Recordable + deterministic.

SELF-STEAL (reuse, not invent): frontier_gravity (C attractors from folded advice), attractor_tools
(roshomon core -> memlang chord -> swarm attractor), frontier_intake (missing-only, k8s-only),
rib_action (three-body, $0 local), swarm_worker (cheap deepseek queue), agent_corpus verified cost
lessons.

ADAPTATION (deterministic, pure stdlib; enqueue is dry-by-default):
  1. CAPTURE    one frontier insight (folded frontier-advice / roshomon core / verified lesson).
  2. QUANTIZE   -> memlang chord + a compact pennies seed (the cheap distributable form).
  3. DISTRIBUTE -> deploy the attractor to the swarm three-body ($0 local) + enqueue ONE cheap
                  deepseek task that applies/expands the insight (pennies).
  4. MEASURE    penny math: one frontier spend vs N cheap executions -> multiplier. Recorded.

Schema: frontier_pennies.v1 · deterministic + $0 (routing) · pure stdlib
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "frontier_pennies.v1"
PENNIES_DIR = ROOT / "memory" / "frontier_pennies"
LEDGER = PENNIES_DIR / "pennies.jsonl"
SEED_FILE = PENNIES_DIR / "latest_seed.md"

# grounded cost references (USD per ~1M tokens, (in,out)) — agent_corpus verified + cache_map.
FRONTIER_COST: dict[str, tuple[float, float]] = {
    "gpt-4o": (2.50, 10.00), "claude-4": (3.00, 15.00), "grok-4.5": (3.00, 15.00),
    "gpt-5": (5.00, 20.00), "claude-opus": (15.00, 75.00),
}
CHEAP_COST: dict[str, tuple[float, float]] = {
    "deepseek-v4-flash": (0.00013, 0.00028),  # pennies per call-scale
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append(row: dict[str, Any]) -> None:
    PENNIES_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def frontier_insights(*, top: int = 4) -> dict[str, Any]:
    """CAPTURE candidate frontier insights from our cheapest-available sources of frontier thought:
    folded frontier-advice (scarce, already spent) -> roshomon core attractors (swarm witnesses)."""
    rows: list[dict[str, Any]] = []
    try:
        from mag import frontier_gravity
        a = frontier_gravity.advice_attractors(top=top)
        for d in a.get("attractors") or []:
            rows.append({"insight": str(d.get("steer") or "")[:240], "source": "frontier-advice",
                         "surface": d.get("surface"), "surface_kind": "frontier"})
    except Exception:
        pass
    try:
        from mag import attractor_tools
        at = attractor_tools.strongest_attractors(top=top)
        for d in at.get("attractors") or []:
            rows.append({"insight": str(d.get("invariant") or "")[:240],
                         "source": "roshomon-core", "surface": "swarm",
                         "surface_kind": "frontier-witness", "witnesses": d.get("witnesses")})
    except Exception:
        pass
    # dedupe + cap
    seen = set()
    out = []
    for r in rows:
        k = r["insight"].lower()[:60]
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return {"ok": True, "schema": SCHEMA, "n_insights": len(out), "insights": out[:top]}


def quantize(insight: str, *, source: str = "frontier") -> dict[str, Any]:
    """QUANTIZE one frontier insight into a cheap distributable form: a memlang chord (deniable,
    compact) + a pennies seed (the form the cheap swarm executes for pennies)."""
    chord_token = ""
    try:
        from mag import memlang
        r = memlang.compile_token("plant", f"[pennies:{source}] {insight}",
                                  {"source": source, "kind": "pennies-quantized"})
        chord_token = str(r.get("token") or r.get("token_hex") or "")[:40]
    except Exception:
        chord_token = ""
    seed = (
        f"# Frontier pennies seed\n"
        f"source: {source}\nchord: {chord_token}\ninsight: {insight}\n"
        f"contract: distribute this ONE insight to the penny-cheap swarm; reproducible, verifiable.\n"
    )
    return {"ok": True, "schema": SCHEMA, "insight": insight[:240], "chord": chord_token,
            "source": source, "seed": seed}


def penny_math(*, frontier: str = "grok-4.5", cheap: str = "deepseek-v4-flash",
               n: int = 100) -> dict[str, Any]:
    """MEASURE the multiplier: one frontier call vs N cheap executions of the quantized insight."""
    fi = FRONTIER_COST.get(frontier, (3.0, 15.0))
    ci = CHEAP_COST.get(cheap, (0.00013, 0.00028))
    # representative: ~2k in / ~1k out for one insight call
    frontier_cost = (fi[0] * 0.002) + (fi[1] * 0.001)
    cheap_cost = (ci[0] * 0.002) + (ci[1] * 0.001)
    n_cheap = n
    cheap_total = cheap_cost * n_cheap
    multiplier = (cheap_total / max(frontier_cost, 1e-9)) if frontier_cost > 0 else 0.0
    return {
        "ok": True, "schema": SCHEMA, "frontier_model": frontier, "cheap_model": cheap,
        "frontier_cost_usd": round(frontier_cost, 6),
        "cheap_per_exec_usd": round(cheap_cost, 6),
        "n_cheap": n_cheap, "cheap_total_usd": round(cheap_total, 6),
        "multiplier": round(multiplier, 1),
        "doctrine": "100 cheap quantized workers < 1 frontier token for reproducible verifiable work",
    }


def distribute(insight: str, *, source: str = "frontier", dry: bool = True) -> dict[str, Any]:
    """DISTRIBUTE the quantized insight for pennies: deploy the attractor to the swarm three-body
    ($0 local) + enqueue ONE cheap deepseek task. Enqueue is dry-by-default."""
    out = {"ok": True, "schema": SCHEMA, "insight": insight[:180], "source": source}
    # 1) deploy attractor into the swarm three-body (local, $0) — direct, deterministic
    try:
        from mag import rib_action as ra
        rib = ra.declare([{"id": "penny_0", "action": insight[:180], "radius": 0.3, "weight": 1.5}])
        ra.influence(rib, action=insight[:180], strength=1.5)
        run = ra.run_three_body(rib, steps=30, seed=3)
        out["swarm_deploy"] = "deployed"
        out["swarm_collective"] = run.get("goal")
    except Exception as e:
        out["swarm_deploy"] = "error"
        out["swarm_error"] = str(e)[:120]
    # 2) enqueue ONE cheap deepseek task (pennies) — dry by default
    if dry:
        out["cheap_task"] = "dry"
        out["note"] = "dry by default — pass dry=False to enqueue the cheap deepseek expansion"
        return out
    try:
        from mag import swarm_worker
        q = swarm_worker.enqueue_task(
            f"Apply/expand this quantized frontier insight for pennies (source={source}):\n{insight[:1200]}",
            provider="deepseek", domain="research", tag="frontier-pennies")
        out["cheap_task"] = q.get("task_id", "")
        out["cheap_provider"] = "deepseek"
    except Exception as e:
        out["cheap_task"] = "error"
        out["cheap_error"] = str(e)[:120]
    return out


def run(*, dry: bool = True, n_cheap: int = 100) -> dict[str, Any]:
    """The whole pennies pipeline: capture one frontier insight -> quantize -> distribute -> measure.
    Records each run to the pennies ledger (recordable)."""
    cap = frontier_insights(top=1)
    insights = cap.get("insights") or []
    if not insights:
        return {"ok": True, "schema": SCHEMA, "action": "skip",
                "reason": "no frontier insight captured yet (dispatch frontier-advice / roshomon)"}
    ins = insights[0]
    q = quantize(ins["insight"], source=ins.get("source", "frontier"))
    d = distribute(ins["insight"], source=ins.get("source", "frontier"), dry=dry)
    pm = penny_math(n=n_cheap)
    row = {"schema": SCHEMA, "ts": _now(), "insight": q.get("insight"), "source": q.get("source"),
           "chord": q.get("chord"), "swarm_deploy": d.get("swarm_deploy"),
           "cheap_task": d.get("cheap_task"),
           "frontier_cost_usd": pm.get("frontier_cost_usd"),
           "cheap_total_usd": pm.get("cheap_total_usd"), "multiplier": pm.get("multiplier")}
    _append(row)
    PENNIES_DIR.mkdir(parents=True, exist_ok=True)
    SEED_FILE.write_text(q.get("seed", ""), encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "action": "distributed", "captured": ins,
            "quantized": q, "distributed": d, "penny_math": pm, "recorded": row}


def run_cadence(*, dry: bool = True) -> dict[str, Any]:
    """Cadence hook: distribute a frontier insight for pennies when one is available (idempotent,
    dry by default so it never enqueues on cadence without an explicit gate)."""
    try:
        r = run(dry=dry)
    except Exception as e:
        return {"ok": False, "action": "error", "error": str(e)[:120]}
    return {"ok": bool(r.get("ok")), "action": r.get("action", "skip"),
            "source": (r.get("captured") or {}).get("source"),
            "multiplier": (r.get("penny_math") or {}).get("multiplier")}


def status() -> dict[str, Any]:
    rows = []
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    total_multiplier = sum(r.get("multiplier") or 0 for r in rows) / max(1, len(rows))
    return {"ok": True, "schema": SCHEMA,
            "contract": "run(dry) = capture 1 frontier insight -> quantize (memlang chord + seed) "
                        "-> distribute (swarm three-body $0 + cheap deepseek) -> penny_math. "
                        "'100 cheap quantized workers < 1 frontier token for reproducible work.'",
            "reuse": "frontier_gravity + attractor_tools + rib_action + swarm_worker",
            "n_distributed": len(rows), "avg_multiplier": round(total_multiplier, 1),
            "seed": str(SEED_FILE.relative_to(ROOT)).replace("\\", "/"),
            "ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/")}


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="frontier_pennies")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("insights")
    sub.add_parser("math")
    r = sub.add_parser("run")
    r.add_argument("--live", action="store_true", help="enqueue the cheap deepseek task (else dry)")
    sub.add_parser("cadence")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "insights":
        print(json.dumps(frontier_insights(top=8), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "math":
        print(json.dumps(penny_math(), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "run":
        print(json.dumps(run(dry=not a.live), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "cadence":
        print(json.dumps(run_cadence(dry=True), indent=2, ensure_ascii=False, default=str))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
