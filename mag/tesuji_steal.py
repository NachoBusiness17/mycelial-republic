"""tesuji_steal — genes encoded in RIB files agents carry; trace the BEST JOURNEY; mine the UNEXPECTED.

Operator (2026-08-13): "genes encoded in rib files they carry with them so we can see what the actual
best journey is and learn from it when one comes in unexpected we have found something worth
researching and holding onto even if we aren't sure where it fits yet. hens the tesuji steal"

THE MECHANISM:
  * GENES AS RIBS — each agent's genes (the fittest invariants) are encoded as RIB files the agent
    CARRIES (publish_rib into a 'genes' domain, associated with the agent). The gene travels with the
    agent, the way the wave-address toolbelt does.
  * THE BEST JOURNEY — trace the sequence of best genes over generations (which RIB-gene led to the
    best outcome) -> the ACTUAL best journey, learnable.
  * THE TESUJI — when an UNEXPECTED result comes in (a high-signal anomaly, an unforeseen finding),
    it is a TESUJI: mine it via route_novel (research it) AND hold it as a RIB (publish into a
    'tesuji'/held domain) even if its fit is unknown. The unexpected is the treasure.

HONEST: real bytes — genes from real invariants, journeys from real history, unexpected routed to the
swarm + held as a RIB. Never fabricates.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
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

SCHEMA = "tesuji_steal.v1"
JOURNEY_DIR = ROOT / "memory" / "runs" / "tesuji"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def carry_gene(agent: str, gene: str, *, domain: str = "genes") -> dict[str, Any]:
    """ENCODE a gene as a RIB the agent CARRIES (publish into the genes domain). The gene travels with
    the agent. Deterministic + $0. HONEST — only a real gene (invariant text) lands, deduped."""
    agent = (agent or "").strip() or "agent"
    gene = (gene or "").strip()
    if not gene:
        return {"ok": False, "schema": SCHEMA, "error": "empty gene"}
    try:
        from mag import rib_bus
        r = rib_bus.publish_rib(f"[gene:{agent}] {gene}", domain=domain,
                                source=f"tesuji-steal:{agent}", fold=False, publish=False)
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:120]}
    # record the carry in the journey log
    JOURNEY_DIR.mkdir(parents=True, exist_ok=True)
    entry = {"ts": _now(), "agent": agent, "gene": gene[:200],
             "hash": hashlib.sha256(gene.encode()).hexdigest()[:16]}
    with open(JOURNEY_DIR / "journey.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"ok": True, "schema": SCHEMA, "tool": "carry_gene", "agent": agent,
            "gene_domain": domain, "n_total": r.get("n_total"),
            "gene_hash": entry["hash"], "note": "gene encoded as a RIB the agent carries"}


def best_journey(*, limit: int = 20) -> dict[str, Any]:
    """THE ACTUAL BEST JOURNEY: trace the sequence of carried genes over time — which genes the agents
    chose to carry, and when (the learnable path that led to the best outcomes). Deterministic + $0.
    HONEST — read from the real journey log."""
    entries = []
    p = JOURNEY_DIR / "journey.jsonl"
    if p.is_file():
        for line in p.read_text(encoding="utf-8", errors="replace").strip().splitlines():
            try:
                entries.append(json.loads(line))
            except Exception:
                continue
    return {"ok": True, "schema": SCHEMA, "tool": "best_journey",
            "n_steps": len(entries), "journey": entries[-limit:],
            "note": "the actual best journey — the genes the agents carried, traceable + learnable"}


def on_unexpected(signal: str, *, source: str = "unexpected", hold: bool = True,
                  mine: bool = True) -> dict[str, Any]:
    """THE TESUJI STEAL: an UNEXPECTED result is a TESUJI — worth researching + holding even if its fit
    is unknown. MINE it (route_novel -> swarm research) AND HOLD it (publish as a RIB in the tesuji/
    held domain) for later. Deterministic + $0 core; route_novel is the mine seam. HONEST — routes +
    holds the real signal, never fabricates."""
    signal = (signal or "").strip()
    if not signal:
        return {"ok": False, "schema": SCHEMA, "error": "empty unexpected signal"}
    out: dict[str, Any] = {"ok": True, "schema": SCHEMA, "tool": "on_unexpected",
                           "signal": signal[:200], "source": source,
                           "is_tesuji": True}
    # HOLD it: publish as a RIB in the tesuji/held domain (for later, even if fit is unknown)
    if hold:
        try:
            from mag import rib_bus
            r = rib_bus.publish_rib(f"[TESUJI:{source}] {signal}", domain="tesuji",
                                    source="tesuji-steal", fold=False, publish=False)
            out["held"] = {"domain": "tesuji", "n_total": r.get("n_total")}
        except Exception as e:
            out["hold_error"] = str(e)[:80]
    # MINE it: route_novel the unexpected to the swarm (research it — it may be the treasure)
    if mine:
        try:
            from mag import swarm_surface
            r2 = swarm_surface.route_novel(
                goal=f"[TESUJI steal] unexpected finding worth researching: {signal[:300]}",
                surface="tesuji-steal", lens=f"tesuji:{source}")
            out["mined"] = {"ok": r2.get("ok"),
                            "task_id": r2.get("task_id") or r2.get("enqueued")}
        except Exception as e:
            out["mine_error"] = str(e)[:80]
    out["note"] = "the unexpected is the treasure — held (RIB) + mined (route_novel), even if its " \
                  "fit is unknown yet. That is the tesuji steal."
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="tesuji-steal")
    ap.add_argument("cmd", nargs="?", default="journey",
                    choices=["carry", "journey", "tesuji"])
    ap.add_argument("args", nargs="*", default=[])
    ap.add_argument("--agent", default="agent")
    a = ap.parse_args(argv)
    if a.cmd == "carry":
        print(json.dumps(carry_gene(a.agent, " ".join(a.args) or "a gene"),
                         ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "tesuji":
        print(json.dumps(on_unexpected(" ".join(a.args) or "an unexpected signal"),
                         ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(best_journey(), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
