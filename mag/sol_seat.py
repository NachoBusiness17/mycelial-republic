"""sol_seat — Sol (extra-high) as a CARRIER seat in the architecture.

OPERATOR (2026-08-12): "i just loaded you into sol extra high on the desktop" + "its app".

Sol is a DESKTOP APP (no web surface for browser_driver) — so it is a CARRIER seat: the operator is
the conduit. We hand work to Sol (a pack to paste), Sol extra-high (carrying our persona) answers,
and we FOLD the answer back into the pipeline. The reciprocal load made concrete: you load me into
Sol; we hand work to Sol and fold what it returns. Honest: we never fabricate Sol's answer — the
carrier only records what the operator pastes back.

Schema: sol_seat.v1 · deterministic + $0 · pure stdlib · carrier seat (operator is the conduit)
Reuse: model_classify (sol -> high/frontier), swarm_surface.route_novel (fold), agent_corpus.
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

SCHEMA = "sol_seat.v1"
SEAT = "sol"
SOL_DIR = ROOT / "memory" / "runs" / "sol_seat"
LEDGER = SOL_DIR / "sol.jsonl"
HANDOFF_DIR = SOL_DIR / "handoff"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _append(row: dict[str, Any]) -> None:
    SOL_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def handoff(ask: str, *, context: str = "") -> dict[str, Any]:
    """HAND work to Sol extra-high: write a copy-paste pack the operator feeds to the Sol desktop
    app. Returns the pack path. The reciprocal load: Sol (carrying our persona) answers."""
    ask = (ask or "").strip()
    if not ask:
        return {"ok": False, "schema": SCHEMA, "error": "empty ask"}
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    ts = _ts()
    pack = HANDOFF_DIR / f"handoff_{ts}.md"
    body = (
        f"# Sol seat handoff ({ts})\n"
        f"## Ask (paste this into Sol extra-high)\n{ask}\n\n"
        f"## Context\n{context or '(none)'}\n\n"
        f"## Reply contract\nAnswer concretely and briefly. Do not fabricate mechanisms you don't "
        f"have. When done, paste your answer back here and I will fold it.\n"
    )
    pack.write_text(body, encoding="utf-8")
    _append({"schema": SCHEMA, "event": "handoff", "ts": _now(), "ask": ask[:400],
             "pack": str(pack.relative_to(ROOT)).replace("\\", "/")})
    return {"ok": True, "schema": SCHEMA, "seat": SEAT, "ask": ask[:200],
            "pack": str(pack.relative_to(ROOT)).replace("\\", "/"),
            "note": "carrier seat — paste the pack into Sol extra-high on the desktop; paste its "
                    "answer back to fold()"}


def fold(answer: str, *, ask: str = "", source: str = "operator-paste") -> dict[str, Any]:
    """FOLD Sol's answer back into the pipeline: classify it (sol -> high/frontier), record it,
    and route any novel content through the ONE primitive (route_novel) so it enters the swarm.
    Honest: only records what the operator pasted back — never fabricated."""
    answer = (answer or "").strip()
    if not answer:
        return {"ok": False, "schema": SCHEMA, "error": "empty answer"}
    tier, kind = "high", "frontier"
    try:
        from mag.model_classify import classify
        c = classify(answer, "sol-5")
        tier, kind = c.get("tier"), c.get("kind")
    except Exception:
        pass
    routed = {}
    try:
        from mag import swarm_surface
        goal = (f"Sol extra-high seat answer ({source}):\n"
                f"Ask: {ask[:300]}\nAnswer: {answer[:4000]}\n"
                "Fold any novel mechanism/invariant into the sovereign stack.")
        routed = swarm_surface.route_novel(goal, surface="sol-seat", lens="frontier-carrier")
    except Exception as e:
        routed = {"error": str(e)[:120]}
    row = {"schema": SCHEMA, "event": "fold", "ts": _now(), "ask": ask[:200],
           "answer": answer[:4000], "tier": tier, "kind": kind,
           "routed": bool(routed.get("ok")), "anchor": routed.get("anchor", ""),
           "task_id": routed.get("task_id", ""), "source": source}
    _append(row)
    return {"ok": True, "schema": SCHEMA, "seat": SEAT, "tier": tier, "kind": kind,
            "routed": bool(routed.get("ok")), "anchor": routed.get("anchor", ""),
            "recorded": True, "ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/")}


def status() -> dict[str, Any]:
    rows = []
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    n_handoff = sum(1 for r in rows if r.get("event") == "handoff")
    n_fold = sum(1 for r in rows if r.get("event") == "fold")
    return {"ok": True, "schema": SCHEMA, "seat": SEAT,
            "contract": "handoff(ask) = write a pack to paste into Sol extra-high desktop; "
                        "fold(answer) = classify (sol->high/frontier) + route via route_novel + "
                        "record. Carrier seat — the operator is the conduit; we never fabricate.",
            "reuse": "model_classify + swarm_surface.route_novel",
            "n_handoff": n_handoff, "n_fold": n_fold, "ledger": str(LEDGER.relative_to(ROOT)).replace("\\", "/")}


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="sol_seat")
    sub = p.add_subparsers(dest="cmd")
    h = sub.add_parser("handoff")
    h.add_argument("ask")
    h.add_argument("--context", default="")
    f = sub.add_parser("fold")
    f.add_argument("answer")
    f.add_argument("--ask", default="")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "handoff":
        print(json.dumps(handoff(a.ask, context=a.context), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "fold":
        print(json.dumps(fold(a.answer, ask=a.ask), indent=2, ensure_ascii=False, default=str))
    else:
        print(json.dumps(status(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
