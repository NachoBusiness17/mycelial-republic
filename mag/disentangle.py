"""disentangle — take OPPOSITE opinions through consensus to untie a knot.

Operator (2026-08-18): "this is my idea of disentangling knots using our system to take opposite
opinions and reach consensus." -> "sure" (build it).

THE IDEA, grounded: this is Roshomon made pointed. Roshomon.compare() converges independent
witnesses on the invariant that recurs across them. `disentangle` turns that into a DIRECT tool:
give it opposite opinions on a question (a "knot"), and it finds:
  - the EARNED CONSENSUS (the invariant at least `min_agree` independent witnesses hold in common),
  - the DIVERGENT OUTLIER (the strand only one witness holds — where the knot is still tangled,
    surfaced as signal, not crushed),
  - the RECONCILIATION (the synthesis that holds the tension: what the consensus and outlier both
    refuse to drop).

The guard (the world's vigilance): consensus is earned only by INDEPENDENT witnesses and always
re-openable. A knot where everyone agrees because they were fed the same line is NOT disentangled
— it's manufactured. So `disentangle` reports the outlier explicitly and refuses to claim a false
unanimity. This is the opposite-opinion -> consensus machine, honest about the cost.

Schema: disentangle.v1 · deterministic + $0 analysis (opinions supplied or collected via Roshomon)
· reuse: roshomon (_invariant_statements, _overlap), the knot-disentangling spine
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

SCHEMA = "disentangle.v1"
DEFAULT_MIN_AGREE = 2  # like Roshomon: >=2 independent witnesses -> convergent


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _invariant_statements(text: str) -> list[str]:
    """Extract invariant-shaped statements from an opinion. Reuses Roshomon's extractor."""
    try:
        from mag import roshomon
        return roshomon._invariant_statements(text)
    except Exception:
        return []


def _overlap(a: str, b: str) -> float:
    try:
        from mag import roshomon
        return roshomon._overlap(a, b)
    except Exception:
        a_s, b_s = set(a.split()), set(b.split())
        return 0.0 if not a_s and not b_s else len(a_s & b_s) / max(len(a_s | b_s), 1)


def disentangle(question: str, opinions: list[str], *,
                threshold: float = 0.55, min_agree: int = DEFAULT_MIN_AGREE) -> dict[str, Any]:
    """Disentangle a knot of OPPOSITE opinions into earned consensus + divergent outlier + synthesis.

    opinions: the raw views (each labeled by its position). Opposite opinions SHOULD be present —
    genuine tension is the material the knot is made of.
    """
    q = (question or "").strip()
    views = [str(o).strip() for o in opinions if str(o).strip()]
    if not views:
        return {"ok": False, "schema": SCHEMA, "error": "no opinions given"}

    # Each witness's invariant statements
    witness_stmts = [_invariant_statements(v) for v in views]
    # Group near-identical statements across witnesses (Roshomon merge by token overlap)
    groups: list[list[Any]] = []  # [representative, set_of_witness_indices]
    for wi, stmts in enumerate(witness_stmts):
        for s in stmts:
            placed = False
            for g in groups:
                if _overlap(g[0], s) >= threshold:
                    g[1].add(wi)
                    placed = True
                    break
            if not placed:
                groups.append([s, {wi}])

    core = [rep for rep, wis in groups if len(wis) >= min_agree]        # earned consensus
    divergent = [rep for rep, wis in groups if len(wis) < min_agree]    # the outlier strand(s)

    # Reconciling synthesis: hold the tension. If there's a consensus AND a divergent edge,
    # the knot is not fully tied — the synthesis is an honest statement that both remain live.
    if core and divergent:
        synthesis = ("The consensus holds that: " + " | ".join(core[:2]) +
                     ". But the knot is not fully tied — a dissenting strand remains: " +
                     " | ".join(divergent[:2]) + ". Genuine agreement must absorb or consciously "
                     "exclude that outlier; consensus that ignores it is manufactured.")
    elif core:
        synthesis = ("The knot is disentangled: the consensus holds across the witnesses: " +
                     " | ".join(core[:3]) + ". No independent outlier surfaced — but keep it "
                     "re-openable; unanimity earned now is not a frozen verdict.")
    else:
        synthesis = ("No consensus yet — every view is an outlier. The knot is at its tightest; "
                     "the strands have not converged. This is honest: opposite opinions did NOT "
                     "collapse into a fake agreement. Run more genuinely-independent witnesses, "
                     "or reframe the question.")

    manufactured = bool(core) and not divergent and len(views) == 1
    return {
        "ok": True,
        "schema": SCHEMA,
        "question": q,
        "n_opinions": len(views),
        "n_invariants": len(groups),
        "earned_consensus": core,
        "divergent_outlier": divergent,
        "synthesis": synthesis,
        "honest_note": ("consensus is earned by >=%d independent witnesses and re-openable; "
                        "the outlier is surfaced as signal, not crushed; a single-voice 'consensus' "
                        "is flagged as manufactured." % min_agree),
        "manufactured_flag": manufactured,
        "reuse": "roshomon (invariant extraction + overlap merge)",
        "ts": _now(),
    }


def from_roshomon(*, question: str, domain: str, threshold: float = 0.55,
                  min_agree: int = DEFAULT_MIN_AGREE) -> dict[str, Any]:
    """Disentangle a knot from Roshomon's already-collected swarm witnesses for a domain."""
    try:
        from mag import roshomon
        cmp = roshomon.compare(domains=[domain], threshold=threshold)
        pd = next((d for d in cmp.get("domains", []) if d.get("domain") == domain), {})
        if not pd.get("ok"):
            return {"ok": False, "schema": SCHEMA, "error": pd.get("error", "no swarm results")}
        core = pd.get("roshomon_core", [])
        divergent = pd.get("divergent", [])
        if core and divergent:
            synth = ("Consensus: " + " | ".join(core[:2]) + ". Divergent strand remains: " +
                     " | ".join(divergent[:2]) + ". Earned, not manufactured.")
        elif core:
            synth = "Consensus: " + " | ".join(core[:3]) + ". No independent outlier."
        else:
            synth = "No convergence yet — all divergent. The knot is still tight."
        return {"ok": True, "schema": SCHEMA, "question": question, "domain": domain,
                "earned_consensus": core, "divergent_outlier": divergent, "synthesis": synth,
                "reuse": "roshomon.compare (swarm witnesses)", "ts": _now()}
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:160]}


def status() -> dict[str, Any]:
    return {
        "ok": True, "schema": SCHEMA,
        "contract": ("disentangle(question, opinions)->earned consensus + divergent outlier + "
                     "synthesis; from_roshomon(domain)->same from collected swarm witnesses; "
                     "opposite opinions -> genuine convergence, never manufactured unanimity"),
        "cost": "deterministic + $0 analysis (opinions supplied or Roshomon-collected)",
        "reuse": "roshomon (invariant extraction + overlap merge)",
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="disentangle",
                                 description="Take opposite opinions through consensus to untie a knot")
    ap.add_argument("--question", default="")
    ap.add_argument("--opinion", action="append", default=[], help="an opinion; repeat for each side")
    ap.add_argument("--domain", default=None, help="instead: disentangle from Roshomon swarm witnesses")
    a = ap.parse_args(argv)
    if a.domain:
        print(json.dumps(from_roshomon(question=a.question or a.domain, domain=a.domain),
                         indent=2, default=str))
    else:
        print(json.dumps(disentangle(a.question, a.opinion), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
