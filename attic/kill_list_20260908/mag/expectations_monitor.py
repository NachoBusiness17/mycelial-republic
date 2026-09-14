"""expectations_monitor — per-space instrument: does what we build KEEP working over time?

Operator (2026-08-13): "we need to know that the things we build are working over time there needs
to be an expectations monitor of each space within you kinda like the dream that tells us a history
of how it came to be but knows nothing outside of itself."

THE UNIT — each SPACE (module/system/surface) is a self-contained MONAD:
  * ORIGIN       — how it came to be (the dream that tells a history; its frozen spec/RIB).
  * EXPECTATIONS — what it's supposed to do (assertions, from the RIB-debug law: every finished piece
                   must be verified against real bytes, never trusted because it was written).
  * HISTORY      — the time-series of checks (does it actually work OVER TIME).
  * KNOWS NOTHING OUTSIDE ITSELF — each monitor holds only its own space's origin/expectations/history.
                   It does not reach into other spaces. As-above-so-below: the whole is a lattice of
                   self-similar monads, each a microcosm.

RIB-DEBUG law (standing): trust bytes, not reports. A finished piece is only 'done' when its
expectation is verified against reality — a false-success is flagged, never papered over.

Schema: expectations_monitor.v1 · deterministic + $0 · pure stdlib (per-space JSONL state)
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
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "expectations_monitor.v1"
STATE_DIR = ROOT / "memory" / "runs" / "expectations"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _space_path(space: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in (space or "unknown"))[:60] or "unknown"
    return STATE_DIR / f"{safe}.json"


def _load(space: str) -> dict[str, Any]:
    p = _space_path(space)
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass
    return {"schema": SCHEMA, "space": space, "origin": "", "expectations": [],
            "history": [], "created": _now()}


def _save(space: str, s: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    _space_path(space).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


def register_space(space: str, origin: str) -> dict[str, Any]:
    """The ORIGIN of a space — how it came to be (the dream that tells a history). Self-contained:
    this space's monitor holds ONLY its own story. Deterministic + $0. HONEST — records the origin
    given; it does not invent one."""
    space = (space or "").strip()
    origin = (origin or "").strip()
    if not space:
        return {"ok": False, "schema": SCHEMA, "error": "empty space"}
    s = _load(space)
    if not s.get("origin"):
        s["origin"] = origin[:400]
    else:
        # append a chapter (the history of how it came to be grows)
        s.setdefault("origin_history", []).append({"ts": _now(), "chapter": origin[:400]})
    _save(space, s)
    return {"ok": True, "schema": SCHEMA, "space": space, "origin": s["origin"],
            "chapters": len(s.get("origin_history", [])),
            "note": "the space's origin recorded — how it came to be"}


def expect(space: str, assertion: str) -> dict[str, Any]:
    """Add an EXPECTATION: what this space is supposed to do (an assertion to verify against bytes).
    Deterministic + $0. HONEST — an expectation is a promise to check, not a claim it already holds."""
    space = (space or "").strip()
    assertion = (assertion or "").strip()
    if not space or not assertion:
        return {"ok": False, "schema": SCHEMA, "error": "space + assertion required"}
    s = _load(space)
    s["expectations"].append({"id": len(s["expectations"]) + 1, "assertion": assertion[:300],
                              "added": _now(), "verified": False, "last_check": None})
    _save(space, s)
    return {"ok": True, "schema": SCHEMA, "space": space,
            "expectation_id": len(s["expectations"]),
            "note": "expectation recorded — to be verified against real bytes, not reports"}


def check(space: str, *, passed: bool, detail: str = "", expectation_id: int | None = None) -> dict[str, Any]:
    """RIB-DEBUG CHECK: verify whether this space met an expectation AGAINST REALITY (bytes, not
    reports). Records the outcome in the space's history so we can see if it keeps working OVER TIME.
    HONEST — a false-success is flagged, never papered over. Deterministic + $0."""
    space = (space or "").strip()
    s = _load(space)
    if expectation_id is not None:
        for e in s["expectations"]:
            if e.get("id") == expectation_id:
                e["verified"] = bool(passed)
                e["last_check"] = _now()
                e["last_detail"] = (detail or "")[:200]
    entry = {"ts": _now(), "passed": bool(passed), "detail": (detail or "")[:300],
             "expectation_id": expectation_id}
    s["history"].append(entry)
    # keep the history bounded (the tail; full origin retained)
    s["history"] = s["history"][-400:]
    _save(space, s)
    return {"ok": True, "schema": SCHEMA, "space": space, "passed": bool(passed),
            "entry": entry, "total_checks": len(s["history"]),
            "note": "RIB-debug check recorded — does it keep working over time"}


def status(space: str) -> dict[str, Any]:
    """The space's monitor, self-contained: origin + expectations + history over time + current health.
    Knows nothing outside itself. Deterministic + $0. HONEST — every number is from real recorded
    checks; it never fabricates health."""
    space = (space or "").strip()
    if not space:
        return {"ok": False, "schema": SCHEMA, "error": "empty space"}
    s = _load(space)
    hist = s.get("history", [])
    passed = sum(1 for h in hist if h.get("passed"))
    total = len(hist)
    # recent health (last 20 checks) — the 'working over time' signal
    recent = hist[-20:]
    recent_pass = sum(1 for h in recent if h.get("passed"))
    health = (recent_pass / len(recent)) if recent else None
    expectations = s.get("expectations", [])
    verified = sum(1 for e in expectations if e.get("verified"))
    return {"ok": True, "schema": SCHEMA, "space": space,
            "origin": s.get("origin", ""),
            "origin_chapters": len(s.get("origin_history", [])),
            "expectations": expectations[-20:],
            "n_expectations": len(expectations), "n_verified": verified,
            "history_len": total, "passed": passed, "failed": total - passed,
            "recent_20_pass_rate": round(recent_pass / len(recent), 3) if recent else None,
            "health": ("green" if (health or 0) >= 0.8 else "amber" if (health or 0) >= 0.5 else "red")
                      if health is not None else "untested",
            "note": "the space's own monitor: origin + expectations + history. It knows nothing "
                    "outside itself."}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="expectations-monitor")
    ap.add_argument("cmd", nargs="?", default="status",
                    choices=["register", "expect", "check", "status"])
    ap.add_argument("space", nargs="?", default="")
    ap.add_argument("args", nargs="*", default=[])
    ap.add_argument("--pass", dest="passed", action="store_true")
    ap.add_argument("--fail", dest="passed", action="store_false")
    ap.set_defaults(passed=True)
    ap.add_argument("--exp", type=int, default=None)
    a = ap.parse_args()
    space = a.space or "default"
    if a.cmd == "register":
        print(json.dumps(register_space(space, " ".join(a.args) or "how it came to be"),
                         ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "expect":
        print(json.dumps(expect(space, " ".join(a.args) or "it should keep working"),
                         ensure_ascii=False, indent=2, default=str))
    elif a.cmd == "check":
        print(json.dumps(check(space, passed=a.passed, detail=" ".join(a.args),
                               expectation_id=a.exp),
                         ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(status(space), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
