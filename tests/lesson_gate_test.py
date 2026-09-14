#!/usr/bin/env python3
"""lesson_gate_test.py — self-test for scripts/lesson_gate.py (stdlib only).

Covers the admission gate's five gates with a temp registry:
  2 valid lessons (ACCEPT x2), 1 duplicate (BUMP, count+1, no re-add),
  1 no-provenance reject, 1 evidence-less reject, 1 conflict (queued for
  operator review, never admitted), 1 expiry via sweep (silent drop) and
  the re-earn revival path.

Run: python tests/lesson_gate_test.py
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from lesson_gate import Gate, SCHEMA, lesson_id, normalize  # noqa: E402

T0 = "2026-06-01T00:00:00Z"   # admitted_at for the expiry lesson only
T_MID = "2026-09-10T00:00:00Z"   # fresh admissions — stay active past sweep
T_LATE = "2026-09-11T00:00:00Z"  # 102 days after T0 — past the 90d default ttl

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}"
          + (f"  [{detail}]" if detail and not cond else ""))


def lesson(statement, evidence="watch/SELF_STEAL_DAY_FOLD_20260909.md#anchor",
           **kw):
    d = {"statement": statement,
         "provenance": kw.pop("provenance",
                              {"lane": "zcode-t2", "run": "trailer-wave"}),
         "evidence": evidence}
    d.update(kw)
    return d


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="lesson_gate_test_"))
    try:
        gate = Gate(path=tmp / "registry.json")

        # -- 1) two valid lessons: ACCEPT --
        a = gate.admit(lesson("backup-first before ground-truth surgery"), now=T_MID)
        check("valid lesson A accepted", a["decision"] == "ACCEPT", json.dumps(a))
        b = gate.admit(lesson("route bulk work to the free lanes",
                              evidence="memory/runs/refeed/receipt.json"),
                       now=T_MID)
        check("valid lesson B accepted", b["decision"] == "ACCEPT", json.dumps(b))
        reg = gate.load()
        check("registry holds exactly 2 lessons", len(reg["lessons"]) == 2)
        check("schema is " + SCHEMA, reg["schema"] == SCHEMA)

        # -- 2) duplicate: BUMP, not re-added --
        dup = gate.admit(lesson(
            "Backup-First before ground-truth surgery!",
            provenance="copilot/night-wave"), now=T_MID)
        check("duplicate bumped", dup["decision"] == "BUMP"
              and dup["count"] == 2, json.dumps(dup))
        reg = gate.load()
        check("duplicate not re-added", len(reg["lessons"]) == 2)
        held = next(l for l in reg["lessons"] if l["id"] == dup["id"])
        check("duplicate merged provenance stays the first earner",
              held["provenance"]["lane"] == "zcode-t2")
        check("bump visible in history",
              held["history"][-1]["event"] == "bumped")

        # -- 3) no provenance: REJECT --
        r1 = gate.admit(lesson("verify against the operator's surface",
                               provenance=None), now=T_MID)
        check("no-provenance rejected",
              r1["decision"] == "REJECT" and r1["reason"] == "no_provenance",
              json.dumps(r1))
        r2 = gate.admit(lesson("verify against the operator's surface",
                               evidence=None), now=T_MID)
        check("no-evidence rejected",
              r2["decision"] == "REJECT" and r2["reason"] == "no_evidence",
              json.dumps(r2))
        reg = gate.load()
        check("rejects never touch the registry",
              len(reg["lessons"]) == 2 and reg["stats"]["rejected"] == 2)

        # -- 4) conflict: queued for operator review, never auto-promoted --
        c = gate.admit(lesson("never edit own credentials"), now=T_MID)
        check("negation lesson accepted",
              c["decision"] == "ACCEPT", json.dumps(c))
        c2 = gate.admit(lesson("edit own credentials freely"), now=T_MID)
        check("contradiction goes to conflict queue",
              c2["decision"] == "CONFLICT", json.dumps(c2))
        reg = gate.load()
        check("conflicted lesson NOT in registry",
              lesson_id(normalize("edit own credentials freely"))
              not in {l["id"] for l in reg["lessons"]})
        check("conflict pending operator review",
              reg["conflicts"][0]["status"] == "pending_operator_review"
              and reg["conflicts"][0]["reason"] == "polarity_flip")

        # -- 5) expiry: silent drop, then re-earn revives --
        e = gate.admit(lesson("two-strike bail on desktop GUI control"),
                       now=T0)
        check("expiry-candidate admitted", e["decision"] == "ACCEPT")
        sw = gate.sweep(now=T_LATE)
        reg = gate.load()
        expired = [l for l in reg["lessons"] if l["status"] == "expired"]
        active = [l for l in reg["lessons"] if l["status"] == "active"]
        check("past-ttl lesson expired silently", sw["expired"] == 1
              and len(expired) == 1, json.dumps(sw))
        check("active view drops expired",
              len(active) == 3 and all(
                  l["id"] != e["id"] for l in active))
        check("expired lesson kept in registry (re-earnable)",
              len(reg["lessons"]) == 4)
        re_earn = gate.admit(lesson("two-strike bail on desktop GUI control"),
                             now=T_LATE)
        check("re-earn revives expired lesson",
              re_earn["decision"] == "REEARNED" and re_earn["count"] == 2,
              json.dumps(re_earn))
        reg = gate.load()
        revived = next(l for l in reg["lessons"] if l["id"] == re_earn["id"])
        check("revived lesson is active again",
              revived["status"] == "active")

        gate.sweep(now=T_LATE)  # idempotent
        sw2 = gate.sweep(now=T_LATE)
        check("sweep is idempotent", sw2["expired"] == 0)

        failed = [n for n, ok, _ in RESULTS if not ok]
        print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed"
              + (f" — FAILURES: {failed}" if failed else " — ALL GREEN"))
        return 1 if failed else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
