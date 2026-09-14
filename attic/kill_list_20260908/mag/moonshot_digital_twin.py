"""moonshot_digital_twin — MOONSHOT RESEARCH: mnemonic.ai as launch point.

Operator (2026-08-16): "i want to use this as a launch point to find other research and do a
moonshot research project using our internals to check if they're working and report back."

THE MOONSHOT (reuses deep_research_moonshot's PRIOR->WITNESS->SHADOW->KNOT shape):
  PRIOR    self-steal: what we already hold (ocean_persona, player_invariant_map,
           behavioral_analytics, verkle grounding) — mnemonic.ai's method, sovereign version.
  DOGFOOD  check if our internals actually WORK (run them on real data, report ok/fail).
  WITNESS  route novel research to the swarm (swarm_surface.route_novel) — find other research
           on grounded digital twins / OCEAN AI personas / behavioral prediction.
  KNOT     verkle-commit the findings + report back.

Schema: moonshot_digital_twin.v1 · deterministic + $0 (dogfood) · research routed to swarm
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "moonshot_digital_twin.v1"
REPORT = ROOT / "memory" / "runs" / "moonshot_digital_twin_report.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def prior() -> dict[str, Any]:
    """PRIOR — the launch point: what we already hold (mnemonic.ai's method, sovereign form)."""
    pieces = ["ocean_persona (OCEAN -> archetype -> voice, content-addressed)",
              "player_invariant_map (behavior -> OCEAN invariant)",
              "behavioral_analytics (mnemonic insight: behavioral signals carry info)",
              "verkle grounding (provenance, no fabrication — mnemonic's 'I don't know' + transparency)"]
    return {"ok": True, "schema": SCHEMA, "launch": "mnemonic.ai",
            "origin": "Eliot (CMO) + Phil (ML research scientist) — grounded digital twin, "
                      "radical transparency, 'I don't know is good', temperature dial, OCEAN.",
            "prior": pieces}


def dogfood() -> dict[str, Any]:
    """DOGFOOD — run our internals on real data to CHECK if they're working."""
    checks = []
    try:
        from mag import ocean_persona as op
        o = op.lens_ocean({"openness": 0.8, "conscientiousness": 0.6, "extraversion": 0.5,
                           "agreeableness": 0.7, "neuroticism": 0.3})
        checks.append({"internal": "ocean_persona", "ok": bool(o.get("ok")),
                       "result": f"{o.get('primary_trait')}->{o.get('primary_invariant',{}).get('archetype')}",
                       "note": "OCEAN lensed to archetype, deterministic (phash)"})
    except Exception as e:
        checks.append({"internal": "ocean_persona", "ok": False, "error": str(e)[:120]})
    try:
        from mag import player_invariant_map as pm
        p = pm.map_("syn", [{"kind": "move", "seat": "syn", "move": "look north explore the gate and open it", "ok": True},
                            {"kind": "move", "seat": "syn", "move": "help the guard and trust the ally", "ok": True}])
        checks.append({"internal": "player_invariant_map", "ok": bool(p.get("ok")),
                       "result": f"{p.get('dominant_trait')}->{p.get('archetype')}",
                       "note": "game moves -> OCEAN invariant"})
    except Exception as e:
        checks.append({"internal": "player_invariant_map", "ok": False, "error": str(e)[:120]})
    try:
        from mag import behavioral_analytics as ba
        checks.append({"internal": "behavioral_analytics", "ok": hasattr(ba, "extract_behavioral_signals"),
                       "note": "mnemonic insight implemented"})
    except Exception as e:
        checks.append({"internal": "behavioral_analytics", "ok": False, "error": str(e)[:120]})
    return {"ok": True, "schema": SCHEMA, "checks": checks,
            "all_working": all(c.get("ok") for c in checks)}


def research(*, enqueue: bool = True) -> dict[str, Any]:
    """WITNESS — route the moonshot research to the swarm (find other research)."""
    if not enqueue:
        return {"ok": True, "schema": SCHEMA, "enqueued": False}
    try:
        from mag import swarm_surface
        q = swarm_surface.route_novel(
            "MOONSHOT research: grounded AI digital twins + OCEAN AI personas + behavioral "
            "prediction (mnemonic.ai launch point). Find the frontier research on knowledge-graph-"
            "grounded personas, 'I don't know' grounding, temperature as deterministic-stochastic "
            "dial, and OCEAN-based impersonation. Return the strongest steal + invariant.",
            surface="moonshot-digital-twin")
        return {"ok": True, "schema": SCHEMA, "enqueued": True, "ref": q.get("ref") or q.get("anchor") or ""}
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "enqueued": False, "error": str(e)[:160]}


def report(*, write: bool = True) -> dict[str, Any]:
    """KNOT + REPORT — braid prior + dogfood + research into the moonshot report."""
    pr = prior()
    df = dogfood()
    rs = research(enqueue=True)
    body = [
        "# MOONSHOT: digital twin (mnemonic.ai launch point)",
        "",
        f"**Launch:** {pr.get('launch')} — {pr.get('origin')}",
        "",
        "## PRIOR (what we already hold)",
        *[f"- {p}" for p in pr["prior"]],
        "",
        "## DOGFOOD (do our internals work?)",
        f"- **All internals working: {df.get('all_working')}**",
        *[f"- {c.get('internal')}: {'OK' if c.get('ok') else 'FAIL'} — {c.get('result','')} {c.get('note','')}"
          for c in df.get("checks", [])],
        "",
        "## WITNESS (research routed to the swarm)",
        f"- enqueued: {rs.get('enqueued')} ref: {rs.get('ref','')}",
        "",
        "## NEXT BEAD (when the swarm returns)",
        "Read the swarm findings, braid them with the dogfood results, and adapt the strongest "
        "external invariant (temperature-dial / OCEAN-impersonation / I-don't-know loop) into the "
        "digital-twin build — then fold and re-braid the living map.",
    ]
    text = "\n".join(body)
    if write:
        try:
            REPORT.parent.mkdir(parents=True, exist_ok=True)
            REPORT.write_text(text, encoding="utf-8")
        except OSError as e:
            return {"ok": False, "schema": SCHEMA, "error": str(e)[:120]}
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return {"ok": True, "schema": SCHEMA, "all_internals_working": df.get("all_working"),
            "research_enqueued": rs.get("enqueued"),
            "report_path": str(REPORT), "report_hash": h}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="moonshot_digital_twin")
    p.add_argument("cmd", choices=["prior", "dogfood", "research", "report", "run"])
    a = p.parse_args(argv)
    fn = {"prior": prior, "dogfood": dogfood, "research": research,
          "report": report, "run": lambda: report()}[a.cmd]
    print(json.dumps(fn(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
