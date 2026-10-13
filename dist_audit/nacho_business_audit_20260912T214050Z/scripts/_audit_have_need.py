"""_audit_have_need.py — have-vs-need gap analysis (bones-not-cows, with bytes).

Operator (2026-08-15): "can we better understand what tools we have and what tools we need and build the
right ones?" -> "yes". Cross the HAVE inventory against the NEED gap-detectors, self-steal each need
(drop the ones already covered), and emit gap-RIBs for the TRUE gaps only.

HAVE  = steal_tools.tools() + mag/ modules (what we hold)
NEED  = the real gap-detectors (health.gap_report, invariant_ledger.gaps_at_glance, gap_frontier.gaps)
       + the named gaps from the session
MATCH = reach_loop.self_steal(need) -> already-have (don't build) vs true-gap (build)
OUT   = gap_task.write() dry gap-RIBs for the true gaps

Schema: _audit_have_need.v1 · deterministic + $0 · read-only
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# the NEEDs named in this session (real gaps, from the audit + doctrine)
NAMED_NEEDS = [
    "running night-shift drain worker that actually drains the swarm queue (stateless, headless)",
    "live game loot: pull real invariants from the verkle chain instead of a hardcoded array",
    "tool-quantization: corpus-to-tools-to-k8s fabricator for deterministic swarm capabilities",
    "orphan_sense rate-limit + dedupe so it stops flooding the swarm queue",
    "human-readable consequences wired into the game log (narrator, not debug console)",
    "reach-loop wired into the cadence so the agent self-steals before building",
    "memweave of the steal tools: content-addressed dedupe of the redundant families",
]


def _gather_detector_gaps() -> list[str]:
    out: list[str] = []
    probes = [
        ("health.gap_report", lambda: __import__("mag.health", fromlist=["gap_report"]).gap_report()),
        ("invariant_ledger.gaps_at_glance", lambda: __import__("mag.invariant_ledger", fromlist=["gaps_at_glance"]).gaps_at_glance()),
        ("gap_frontier.gaps", lambda: __import__("mag.gap_frontier", fromlist=["gaps"]).gaps()),
    ]
    for name, fn in probes:
        try:
            r = fn()
        except Exception:
            continue
        # tolerate dict/list shapes; pull out strings
        if isinstance(r, dict):
            for v in r.values():
                if isinstance(v, str) and len(v) > 20:
                    out.append(v)
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, str) and len(x) > 20:
                            out.append(x)
        elif isinstance(r, list):
            for x in r:
                if isinstance(x, str) and len(x) > 20:
                    out.append(x)
    return out[:20]


def main() -> None:
    from mag import steal_tools, reach_loop

    have = steal_tools.tools()
    have_names = {t["name"].lower() for t in have}

    needs = list(NAMED_NEEDS)
    needs += _gather_detector_gaps()

    print(f"HAVE: {len(have)} steal-tools + mag/ modules")
    print(f"NEED candidates: {len(needs)}\n")

    true_gaps = []
    print("== NEED -> self-steal verdict ==")
    for need in needs:
        hits = reach_loop.self_steal(need)   # returns the list of hits directly
        tag = "TRUE-GAP" if not hits else "HAVE"
        print(f"  [{tag}] {need[:80]}")
        if tag == "TRUE-GAP":
            true_gaps.append(need)

    print(f"\n== TRUE GAPS TO BUILD: {len(true_gaps)} ==")
    from mag import gap_task
    for gap in true_gaps:
        r = gap_task.write(gap=gap, deliverable=f"build a working solution for: {gap}", enqueue=False)
        print(f"  - {gap[:90]}  [{r.get('skipped') or 'spec-ready'}]")


if __name__ == "__main__":
    main()
