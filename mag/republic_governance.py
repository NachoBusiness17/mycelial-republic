"""republic_governance — the Mycelial Republic's governance law (Ostrom + stigmergy).

STEAL (research-grounded, 2026-08-10):
  * Stigmergy (Grasse 1959): coordination is INDIRECT through the environment — each agent leaves a
    trace others respond to; the traces ARE the shared external memory. Our verkle/mycelium graph IS
    that environment. consent_first: no permission to propose. no_throne: no planner.
  * Ostrom's 8 design principles (Governing the Commons, Nobel 2009): how a self-governing republic
    manages shared common-pool resources WITHOUT a king — clear boundaries, congruence, collective-
    choice, accountable monitoring, graduated sanctions, conflict arenas, self-organization, nested
    enterprises. Each maps onto the Republic's shared resources + existing invariants.

This module:
  resources()    — the shared commons inventory (compute, tokens, GPU, memory, free-tier pools) + who
                   may withdraw each (the boundaries, principle 1).
  audit()        — governance-health score: how many of Ostrom's 8 our architecture satisfies, and
                   which principles are partial/gaps (the real steal: graduated sanctions, collective-
                   choice, explicit boundaries).
  constitution() — emit the Republic's governance constitution (markdown) as case law.

Schema: republic_governance.v1 · deterministic · $0
CLI: python -m mag.republic_governance resources | audit | constitution | status
"""
from __future__ import annotations

import argparse
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
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "republic_governance.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# ── Ostrom's 8 principles mapped to the Republic ────────────────────────────────
# each: number, name, resource/invariant/mechanism, status (satisfied/partial/gap), gap note.
PRINCIPLES: list[dict[str, Any]] = [
    {"n": 1, "name": "Clearly defined boundaries",
     "maps_to": "swarm roster (swarm_health AGENTS); allowlists (browser_env); cost caps (cost_enforcer); budget tiers (grok_rightsize); the queue/pools as the commons",
     "status": "partial", "gap": "no single inventory of shared resources + who may withdraw each (resources())"},
    {"n": 2, "name": "Congruence with local conditions",
     "maps_to": "rightsize / queue_rightsize / cost_learn — cheapest-capable tier per task, adapts to local cost",
     "status": "satisfied", "gap": ""},
    {"n": 3, "name": "Collective-choice (affected can modify rules)",
     "maps_to": "consent_first + case-law fold + operator steer inbox; beads co-author rules",
     "status": "partial", "gap": "make bead co-authorship of case-law explicit (not just implicit fold)"},
    {"n": 4, "name": "Accountable monitoring",
     "maps_to": "ghost_ledger (source of truth) + behavioral_analytics (leak) + swarm_health (health) + ghost watching",
     "status": "satisfied", "gap": ""},
    {"n": 5, "name": "Graduated sanctions",
     "maps_to": "Trust Ratchet (capability only narrows) + cost_enforcer (kill at cap)",
     "status": "partial", "gap": "no explicit PROPORTIONAL ladder: warn -> restrict -> suspend -> expel, per offense"},
    {"n": 6, "name": "Conflict-resolution arenas",
     "maps_to": "loop_breaker / doctor / error_healer / oh_fuck / lens divergence-preserving",
     "status": "satisfied", "gap": ""},
    {"n": 7, "name": "Right to self-organize (not challenged)",
     "maps_to": "no_throne + local_first + self-advance + Republic sovereignty",
     "status": "satisfied", "gap": ""},
    {"n": 8, "name": "Nested enterprises (multi-layer governance)",
     "maps_to": "queue -> drainer -> governor -> ghost -> overseer -> republic -> fleet/worktrees",
     "status": "satisfied", "gap": ""},
]

# The shared commons of the Republic: resource -> who may withdraw (boundaries).
RESOURCES: list[dict[str, Any]] = [
    {"name": "compute (CPU)", "withdraw": "all beads", "governed_by": "cost_enforcer / swarm_health", "cap": "per-task budget"},
    {"name": "tokens (LLM)", "withdraw": "routed beads", "governed_by": "grok_rightsize / cache_router", "cap": "budget tiers + cache-hit discipline"},
    {"name": "GPU (free/local)", "withdraw": "free-tier loops", "governed_by": "gpu_ghost / free-tier frontier loop", "cap": "free pool"},
    {"name": "memory (verkle/mycelium)", "withdraw": "all beads (append-only)", "governed_by": "verkle_knot / schema_registry", "cap": "content-addressed, amend-not-erase"},
    {"name": "free-tier pools (grok/deepseek)", "withdraw": "cheap swarms", "governed_by": "grok_free / flock_steal", "cap": "rate limits"},
    {"name": "bandwidth / browser", "withdraw": "allowlisted", "governed_by": "browser_env (allowlist)", "cap": "host allowlist"},
]


def resources() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA, "commons": RESOURCES,
            "note": "the Republic's shared common-pool resources + who may withdraw each (boundaries)"}


def audit() -> dict[str, Any]:
    """Governance-health: how many of Ostrom's 8 the architecture satisfies; list the gaps."""
    satisfied = [p for p in PRINCIPLES if p["status"] == "satisfied"]
    partial = [p for p in PRINCIPLES if p["status"] == "partial"]
    gaps = [p for p in PRINCIPLES if p["gap"]]
    return {"ok": True, "schema": SCHEMA, "ts": _now(),
            "n_principles": len(PRINCIPLES), "satisfied": len(satisfied),
            "partial": len(partial), "governance_score": f"{len(satisfied)}/{len(PRINCIPLES)}",
            "satisfied_names": [p["name"] for p in satisfied],
            "partial_names": [p["name"] for p in partial],
            "gaps": [{"n": p["n"], "name": p["name"], "gap": p["gap"]} for p in gaps],
            "n_resources": len(RESOURCES),
            "law": "coordinate by stigmergy (traces in the verkle/mycelium environment); govern shared "
                   "resources by Ostrom's 8; under no_throne / local_first / consent_first / residual_is_dna"}


def constitution() -> str:
    """Emit the Republic's governance constitution (markdown case law)."""
    lines = [
        "# The Mycelial Republic — governance constitution",
        "**Coordination law (stigmergy):** agents leave traces in the shared environment (verkle / "
        "mycelium / artifacts); others respond to the traces. No planner, no permission to propose "
        "(consent_first), no throne (no_throne). The traces ARE the shared external memory.",
        "",
        "**Governance law (Ostrom's 8 principles):**",
    ]
    for p in PRINCIPLES:
        lines.append(f"{p['n']}. **{p['name']}** ({p['status']}) — {p['maps_to']}"
                     + (f" [GAP: {p['gap']}]" if p["gap"] else ""))
    lines.append("")
    lines.append("**The shared commons (boundaries):**")
    for r in RESOURCES:
        lines.append(f"- **{r['name']}** — withdraw: {r['withdraw']} · governed by {r['governed_by']} · cap: {r['cap']}")
    lines.append("")
    lines.append("Under the standing invariants: no_throne · local_first · consent_first · residual_is_dna.")
    return "\n".join(lines)


def status() -> dict[str, Any]:
    a = audit()
    return {"ok": True, "schema": SCHEMA, "governance_score": a["governance_score"],
            "partial": a["partial"], "n_resources": a["n_resources"]}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="republic_governance", description="Mycelial Republic governance law")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("resources")
    sub.add_parser("audit")
    sub.add_parser("constitution")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "resources":
        print(json.dumps(resources(), indent=2, ensure_ascii=False))
    elif a.cmd == "audit":
        print(json.dumps(audit(), indent=2, ensure_ascii=False))
    elif a.cmd == "constitution":
        print(constitution())
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    else:
        p.print_help(); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
