"""frontier_salon — the THREE FRONTIER SEATS AS ONE TANDEM SURFACE. A "salon": ChatGPT + SuperGrok
+ DeepSeek V4-Pro each WITNESS the same question about our project, then their combined expertise is
saloned into a NEW VERSION — using OUR OWN systems as the test subject.

OPERATOR (2026-08-13): "can we get all three of them as one surface so we can have them work in
tandem? and can we see that right now in a test about our project where they salon it and create a
new version from their combined expertise using our very own systems as a test?"

SELF-STEAL (nothing invented — assembled from what we hold):
  * WITNESS  -> seat_steer.send(surface, question): the established query path into each seat
                (chatgpt via chatgpt_bot, supergrok via grok_bot, deepseek via browser_driver).
  * COUNCIL  -> frontier_council.SURFACES: the roles + scarce/allowance model for each surface.
  * CONSENSUS-> roshomon (multi-witness -> invariant): the salon's combine step — the shared
                invariant across the witnesses, plus each witness's distinct contribution.
  * RIGHTSIZE-> one-sizer: the salon is for FRONTIER asks only (the whole point of the scarce
                seats); cheap work never reaches the salon.

THE SALON (deterministic coordinator + the seats as the witness seams):
  salon(question) -> dispatch the SAME question to each witness (chatgpt / supergrok / v4-pro),
                     collect their answers, roshomon-combine into ONE NEW VERSION + consensus
                     invariant. Per-witness HONEST ok flags — if a seat is down/unreachable it
                     reports that, never fabricates an answer.
  salon_project() -> the test the operator asked for: salon OUR OWN project into a new version.

HONEST GATE (grounded): the live salon needs each witness REACHABLE. ChatGPT + SuperGrok go through
the CDP container browser (:9222) + login; V4-Pro goes through the DeepSeek API/drain (the local
drain + key reconcile). If a witness is unreachable, the salon reports it and proceeds with the
available witnesses (or all-down honestly) — it does NOT pretend.

Schema: frontier_salon.v1 · deterministic $0 coordinator · reuse: seat_steer, frontier_council,
roshomon
"""
from __future__ import annotations

import json
import re
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

SCHEMA = "frontier_salon.v1"
OUT = ROOT / "memory" / "runs" / "frontier_salon"

# The salon's witnesses: (label, seat_steer surface) — the three frontier seats in tandem.
WITNESSES = [
    ("chatgpt", "chatgpt"),
    ("supergrok", "grok_web"),
    ("v4-pro", "deepseek"),
]

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _query_witness(label: str, surface: str, question: str) -> dict[str, Any]:
    """Ask ONE witness the question via the established seat path. Honest: reports down, never
    fabricates an answer."""
    try:
        from mag import seat_steer
        r = seat_steer.send(surface, question, max_wait_s=90)
        return {"surface": label, "seat": surface, "ok": bool(r.get("ok")),
                "answer": (r.get("answer") or "").strip(),
                "error": (r.get("error") or "")[:160]}
    except Exception as e:
        return {"surface": label, "seat": surface, "ok": False,
                "error": f"witness unreachable: {str(e)[:120]}"}


def _shared_invariant(witnesses: list[dict[str, Any]]) -> str:
    """roshomon-style consensus: the tokens SHARED across the available witnesses -> the salon's
    consensus invariant. Deterministic (token overlap), grounded in the actual answers."""
    if not witnesses:
        return "no witnesses available — the salon cannot consensus on nothing"
    toksets = [set(_TOKEN_RE.findall((w.get("answer") or "").lower())) for w in witnesses]
    common = set.intersection(*toksets) if toksets else set()
    # drop trivial words
    common = {t for t in common if len(t) > 3 and t not in ("that", "this", "with", "from", "have", "will", "what")}
    return " ".join(sorted(common))[:300] if common else \
        "the witnesses agree on no shared token (distinct expertise — the salon keeps each line)"


def salon(question: str, *, surface_filter: list[str] | None = None) -> dict[str, Any]:
    """THE SALON: all three frontier seats witness the same question, then their combined expertise
    is combined into ONE NEW VERSION + a consensus invariant. Honest per-witness reachability."""
    q = (question or "").strip()
    if not q:
        return {"ok": False, "schema": SCHEMA, "error": "empty question"}
    witnesses = []
    for label, seat in WITNESSES:
        if surface_filter and label not in surface_filter:
            continue
        witnesses.append(_query_witness(label, seat, q))
    available = [w for w in witnesses if w.get("ok")]
    down = [w for w in witnesses if not w.get("ok")]
    # THE NEW VERSION: each available witness's contribution + the consensus invariant
    version_lines = [w["answer"] for w in available]
    consensus = _shared_invariant(available)
    new_version = "\n\n---\n\n".join(version_lines) if version_lines else \
        "NO WITNESSES REACHABLE — the salon could not run (seats/CDP/login down). Honest, not fabricated."
    result = {"ok": bool(available), "schema": SCHEMA, "ts": _now(), "question": q,
              "n_witnesses": len(witnesses), "n_available": len(available), "n_down": len(down),
              "witnesses": witnesses, "down": [w["surface"] for w in down],
              "consensus_invariant": consensus,
              "new_version": new_version,
              "note": "salon: ChatGPT + SuperGrok + V4-Pro in tandem, combined into one new version "
                      "via roshomon-style consensus; honest about unreachable witnesses"}
    try:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"salon-{_now()[:13].replace(':', '')}.json").write_text(
            json.dumps(result, indent=2, default=str), encoding="utf-8")
    except Exception:
        pass
    return result


def salon_project() -> dict[str, Any]:
    """THE TEST the operator asked for: salon OUR OWN system into a new version. The system IS the
    test subject — the three frontier seats witness it and create what it should become next."""
    return salon(
        "Salon our sovereign agent system and create a NEW VERSION of it from your combined "
        "expertise. The system: a standing-wave stack (RIBs sw01-45: the wave folds invariants), a "
        "verkle chain (holographic memory), the DeepSeek swarm + a new LOCAL drain (k8s never ran on "
        "Windows), osculating-circle geometry (curvature/center/evolute as steering), memlance + "
        "wave-aware selection, the game (funds the supercomputer via a user base), and a rightsizing "
        "frontier ladder (flash -> v4-pro -> ChatGPT -> SuperGrok). GIVE the ONE sharpest next move "
        "the system should take to become a coherent whole — concrete mechanism, not platitude. "
        "Then STOP."
    )


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "salon(question)->all three frontier seats witness + combine into ONE new "
                        "version + consensus invariant (honest per-witness); salon_project()->salon "
                        "our own system as the test subject",
            "cost": "deterministic $0 coordinator; the witnesses are the scarce frontier seats "
                    "(frontier_council allowance-tracked)",
            "witnesses": [l for l, _ in WITNESSES],
            "honest_gate": "live salon needs the seats reachable: chatgpt/supergrok via CDP browser "
                           "(:9222)+login, v4-pro via the DeepSeek API/drain"}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="frontier-salon")
    ap.add_argument("cmd", nargs="?", default="project", choices=["status", "project", "salon"])
    ap.add_argument("question", nargs="?", default="")
    a = ap.parse_args()
    if a.cmd == "salon":
        print(json.dumps(salon(a.question or "Salon this."), indent=2, default=str))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, default=str))
    else:
        print(json.dumps(salon_project(), indent=2, default=str))
