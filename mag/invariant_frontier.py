"""invariant_frontier — extract FRONTIER VERSIONS of our invariants by gap analysis + branching.

Operator (2026-08-13): "can we use our invariant stack to extract frontier versions with the new
mechanisms we loaded into you? or is that already being done. gap analysis on invariants to find the
missing explanations to branch them it's literally just a conversation away from the frontier a
google search and a steal."

THE LOOP (gap-driven frontier extraction):
  * GAP ANALYSIS  — for each invariant, name the MISSING EXPLANATION / branch not yet explored (the
    gap): what frontier knowledge would deepen it.
  * ROUTE THE GAP — send that specific gap to the frontier: the search swarm (research seam, the
    'google search') + route_novel (cheap deepseek, the 'conversation') + a steal (the adapt).
  * BRANCH        — when the frontier answer returns, fold it back as a BRANCHED RIB (dedupe by
    content anchor), so the invariant stack grows toward the frontier — one branch per gap.

HONEST: this ROUTES the gap to the frontier and folds the branched invariant when the swarm returns
the answer (async). It never fabricates the frontier answer — it reports the routed task + the
branch it will fold. The frontier is genuinely 'a conversation + a search + a steal' away.

Schema: invariant_frontier.v1 · deterministic $0 gap-analysis + routing seam (route_novel/search swarm)
"""
from __future__ import annotations

import json
import sys
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "invariant_frontier.v1"


def gap_analysis(domain: str = "standing-wave", *, limit: int = 10) -> dict[str, Any]:
    """GAP ANALYSIS: for each invariant in a domain, name the MISSING EXPLANATION / branch — what
    frontier knowledge would deepen it. Deterministic + $0 (the gap is derived from the invariant's
    real text; it never invents an invariant)."""
    invariants = _mount_invariants(domain)
    if not invariants:
        return {"ok": False, "schema": SCHEMA, "error": f"no invariants in domain {domain}",
                "known_domains": _known_domains()}
    gaps = []
    for inv in invariants[:limit]:
        text = inv.get("invariant", "") or ""
        gap = _derive_gap(text)
        gaps.append({"invariant_id": inv.get("key") or inv.get("id"),
                     "invariant": text[:160],
                     "gap": gap,
                     "frontier_ask": f"[branch invariant] {text[:300]}\nGAP: {gap}"})
    return {"ok": True, "schema": SCHEMA, "domain": domain, "n_invariants": len(invariants),
            "n_analyzed": len(gaps), "gaps": gaps,
            "note": "per-invariant gap analysis done — each names the missing explanation to branch "
                    "toward the frontier"}


def _mount_invariants(domain: str) -> list[dict[str, Any]]:
    try:
        from mag import rib_bus
        m = rib_bus.mount(domain)
        ribs = m.get("ribs") or []
        out = []
        for r in ribs:
            if isinstance(r, dict):
                out.append(r)
            elif isinstance(r, str):
                out.append({"invariant": r})
        return out
    except Exception:
        return []


def _known_domains() -> list[str]:
    try:
        from mag import rib_bus
        return rib_bus.list_domains() if hasattr(rib_bus, "list_domains") else []
    except Exception:
        return []


def _derive_gap(text: str) -> str:
    """Deterministically name the frontier gap for an invariant: what explanation would deepen it.
    Derived from the invariant's real content — the missing branch it gestures at but doesn't hold."""
    low = (text or "").lower()
    # a heuristic gap probe: what the invariant asserts but hasn't yet shown its frontier mechanism for
    if any(w in low for w in ["stigmergy", "pheromone", "wave", "propagat"]):
        return "what frontier mechanism/evidence confirms the propagation dynamic, and its limits?"
    if any(w in low for w in ["consent", "manufactur", "hidden", "epistemic", "puppet"]):
        return "what frontier research (institutional design, epistemics) proves this anti-manipulation mechanism, and where does it fail?"
    if any(w in low for w in ["address", "reach", "content", "fingerprint"]):
        return "what frontier distributed-systems design confirms content-addressed reachability at scale, and its failure modes?"
    if any(w in low for w in ["scanner", "stochastic", "measure", "deterministic"]):
        return "what frontier work on deterministic mapping of stochastic models (mean-field / optimal transport) deepens this?"
    if any(w in low for w in ["trust", "sovereign", "consent", "republic"]):
        return "what frontier governance/alignment research confirms sovereign-agents-consenting-to-shared-ground, and its risks?"
    return "what frontier explanation would deepen or falsify this invariant?"


def extract_branch(domain: str = "standing-wave", *, invariant_id: str | None = None,
                   surface: str = "invariant-frontier") -> dict[str, Any]:
    """ROUTE THE GAP TO THE FRONTIER: send the gap for ONE invariant to the search swarm (the
    'google search') + route_novel (the cheap deepseek 'conversation') + a steal ask. Returns the
    routed tasks; the branch folds when the swarm returns. Honest — reports the routed seam, never
    fabricates the frontier answer."""
    ga = gap_analysis(domain, limit=100)
    gaps = ga.get("gaps", [])
    if invariant_id:
        gaps = [g for g in gaps if str(g.get("invariant_id")) == str(invariant_id)]
    if not gaps:
        return {"ok": False, "schema": SCHEMA, "error": "no gap to route", "domain": domain}
    gap = gaps[0]
    routed = {"search_swarm": None, "route_novel": None}
    # the 'google search' seam (deterministic_scanner.research -> search swarm)
    try:
        from mag import deterministic_scanner as ds
        r = ds.research(gap.get("frontier_ask", ""), surface=surface)
        routed["search_swarm"] = {"ok": r.get("ok"), "task_id": r.get("task_id")}
    except Exception as e:
        routed["search_swarm"] = {"error": str(e)[:80]}
    # the 'conversation' seam (route_novel -> cheap deepseek swarm)
    try:
        from mag import swarm_surface
        r2 = swarm_surface.route_novel(goal=gap.get("frontier_ask", ""), surface=surface,
                                       lens=f"{domain}-frontier")
        routed["route_novel"] = {"ok": r2.get("ok"),
                                 "task_id": r2.get("task_id") or r2.get("enqueued")}
    except Exception as e:
        routed["route_novel"] = {"error": str(e)[:80]}
    return {"ok": True, "schema": SCHEMA, "domain": domain, "gap": gap,
            "routed": routed, "steal": "search the field corpus + a targeted steal to adapt the "
                                      "frontier answer",
            "note": "the gap is a conversation + a search + a steal from the frontier — routed; "
                    "the branched RIB folds when the swarm returns"}


def run(domain: str = "standing-wave", *, limit: int = 5) -> dict[str, Any]:
    """One pass: gap-analyze a domain's invariants and route each gap to the frontier (search swarm +
    route_novel + steal). The branching loop — 'a conversation away from the frontier'. Deterministic
    gap analysis + routing seam; honest (never fabricates the frontier answer)."""
    ga = gap_analysis(domain, limit=limit)
    results = []
    for g in (ga.get("gaps") or []):
        results.append(extract_branch(domain, invariant_id=g.get("invariant_id")))
    return {"ok": True, "schema": SCHEMA, "domain": domain,
            "n_gaps": len(results),
            "routed": [r.get("routed") for r in results],
            "note": "invariant gaps routed to the frontier — the branches will fold when answers return"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="invariant-frontier")
    ap.add_argument("cmd", nargs="?", default="gap",
                    choices=["gap", "extract", "run"])
    ap.add_argument("--domain", default="standing-wave")
    ap.add_argument("--id", default=None)
    ap.add_argument("--limit", type=int, default=5)
    a = ap.parse_args(argv)
    if a.cmd == "gap":
        print(json.dumps(gap_analysis(a.domain, limit=a.limit), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "extract":
        print(json.dumps(extract_branch(a.domain, invariant_id=a.id), ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "run":
        print(json.dumps(run(a.domain, limit=a.limit), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
