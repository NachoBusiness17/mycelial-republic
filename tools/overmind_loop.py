"""overmind_loop - THE LOOP ORGAN (OVERMIND-2 gap 1, the falsifier run).

Spec (spec-before-code): watch/inbox/model_garden/OVERMIND_THEORY.md
sec 2.2 (the tick), sec 6 (the falsifiable moonshot: ONE glm-flash
loop-hour unattended, $1 hard cap checked before every dispatch,
NOOP-with-reason grammar, chain-sealed ticks), sec 7 gaps 1+2. Lane order
OVERMIND-2 fixes the minimal verb set (lawed in tools/overmind_verbs.py;
senses in tools/overmind_senses.py; tests first:
tests/test_overmind_loop.py).

The tick: SENSE -> DECIDE (ONE glm-5.3-flash ask through the gated
tools/model_garden rail; the mag/inference_budget recipe governs params:
glm-5.3-flash fires UNCAPPED with reasoning_effort low - the lane order's
"max_tokens 12000" would burn empty-content per the FAMILY_TABLE row, so
the recipe law wins; deviation named in the verdict) -> GATE (fail-closed
verb table) -> EXECUTE (sanctioned surfaces only) -> VERIFY (read-back) ->
LEDGER (hash-chained append). No directive surface exists for the brain
anywhere in this organ (STEERING_DOGFOOD: the glm family ignores mid-task
directives; the ask is single-turn by construction).

CLI: run --ticks N --interval S | verify | summary [--run-id X].
Exit: 0 ok / 2 usage error or hard budget breach.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.overmind_senses import (collect_senses,  # noqa: E402
                                   sense_driver_beat, sense_landed,
                                   sense_queue, sense_sha_tail)
from tools.overmind_brain import (BRAIN_MODEL, decide,  # noqa: E402
                                  parse_decision, write_brain_ask)
from tools.overmind_verbs import (RUN_DIR, STAGED_ASK_MODEL,  # noqa: E402
                                  VERB_TABLE, UnauthorizedVerb,
                                  execute_verb, validate_verb)

LEDGER = RUN_DIR / "ledger.jsonl"
ASK_ROOT = RUN_DIR / "asks"
GARDEN_USAGE = ROOT / "memory" / "runs" / "model_garden" / "usage.jsonl"
GARDEN_OUT = ROOT / "watch" / "inbox" / "model_garden"


# hard caps (theory sec 6: $1.00 hard, checked before every dispatch)
PER_CALL_CAP_USD = 1.0
CUMULATIVE_CAP_USD = 1.0
DISPATCH_RESERVE_USD = 0.05
SCHEMA = "overmind.tick.v1"


class BudgetExceeded(Exception):
    """Per-call or cumulative cap breach (kill condition 5's spend leg)."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class BudgetCap:
    """$ hard caps: per-call and cumulative (theory kill condition 5)."""

    def __init__(self, per_call: float = PER_CALL_CAP_USD,
                 cumulative: float = CUMULATIVE_CAP_USD):
        self.per_call = float(per_call)
        self.cumulative = float(cumulative)
        self.spent = 0.0

    def allow_dispatch(self, spent: float | None = None,
                       reserve: float = DISPATCH_RESERVE_USD) -> bool:
        s = self.spent if spent is None else float(spent)
        return s + reserve <= self.cumulative

    def charge(self, cost: float, ask_id: str = "") -> None:
        cost = float(cost or 0.0)
        if cost > self.per_call + 1e-9:
            raise BudgetExceeded(
                f"per-call cap breached on {ask_id}: ${cost:.4f} > "
                f"${self.per_call:.2f}")
        if self.spent + cost > self.cumulative + 1e-9:
            raise BudgetExceeded(
                f"cumulative cap breached on {ask_id}: "
                f"${self.spent + cost:.4f} > ${self.cumulative:.2f}")
        self.spent = round(self.spent + cost, 6)


def spend_from_ledger(run_id: str) -> float:
    """Byte-truth cumulative spend for one run: the garden usage ledger rows
    for this run's ask ids (trust bytes, not the loop's own memory)."""
    if not GARDEN_USAGE.is_file():
        return 0.0
    prefix = f"overmind2-{run_id}"
    total = 0.0
    for line in GARDEN_USAGE.read_text(encoding="utf-8",
                                       errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(row.get("id", "")).startswith(prefix):
            total += float(row.get("cost_usd") or 0.0)
    return round(total, 6)


def _canon(row: dict) -> str:
    return json.dumps(row, sort_keys=True, ensure_ascii=False)


def ledger_append(row: dict) -> dict:
    """Hash-chained append: each row seals the previous row's hash
    (legends law: the tick IS a chain row; history cannot be forged)."""
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    prev = ""
    if LEDGER.is_file():
        lines = [l for l in LEDGER.read_text(encoding="utf-8",
                                             errors="replace").splitlines()
                 if l.strip()]
        if lines:
            try:
                prev = json.loads(lines[-1]).get("hash", "")
            except json.JSONDecodeError:
                prev = ""
    row = dict(row)
    row["prev_hash"] = prev
    row["hash"] = hashlib.sha256(_canon(row).encode("utf-8")).hexdigest()
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(_canon(row) + "\n")
    return row


def verify_ledger(path: Path | None = None) -> dict:
    p = Path(path) if path else LEDGER
    if not p.is_file():
        return {"ok": True, "rows": 0, "note": "no ledger yet"}
    prev = ""
    n = 0
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        n += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return {"ok": False, "rows": n, "break_at": n,
                    "why": "unparseable row"}
        if row.get("prev_hash") != prev:
            return {"ok": False, "rows": n, "break_at": n,
                    "why": "prev_hash mismatch"}
        body = {k: v for k, v in row.items() if k != "hash"}
        want = hashlib.sha256(_canon(body).encode("utf-8")).hexdigest()
        if row.get("hash") != want:
            return {"ok": False, "rows": n, "break_at": n,
                    "why": "hash mismatch (row bytes changed)"}
        prev = row["hash"]
    return {"ok": True, "rows": n}


def run_loop(ticks: int = 40, interval: float = 90.0,
             run_id: str | None = None, blind_sha: str | None = None,
             tag: str = "", per_call_cap: float = PER_CALL_CAP_USD,
             cumulative_cap: float = CUMULATIVE_CAP_USD) -> dict:
    run_id = run_id or (datetime.now(timezone.utc).strftime(
        "r%Y%m%dT%H%M%SZ") + "-" + (tag or "run"))
    run_dir = ASK_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    started_ts = _now()
    budget = BudgetCap(per_call_cap, cumulative_cap)
    meta = {"schema": "overmind.run.v1", "run_id": run_id, "tag": tag,
            "started_ts": started_ts, "ticks": ticks, "interval_s": interval,
            "blind_list_sha256": blind_sha, "brain_model": BRAIN_MODEL,
            "per_call_cap_usd": per_call_cap,
            "cumulative_cap_usd": cumulative_cap}
    (run_dir / "run_meta.json").write_text(
        json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"OVERMIND run {run_id}: {ticks} ticks x {interval}s, brain "
          f"{BRAIN_MODEL}, caps ${per_call_cap}/${cumulative_cap}, blind "
          f"{blind_sha or 'none'}", flush=True)
    exit_code = 0
    for tick in range(1, ticks + 1):
        t0 = time.monotonic()
        senses = collect_senses(started_ts)
        compact = {"git_changed": senses["git"]["changed_count"],
                   "git_tail": senses["git"]["tail"][:6],
                   "beat_rows": senses["beat"]["rows_since_run_start"],
                   "beat_actors": senses["beat"]["actors"],
                   "beat_last": senses["beat"]["tail"][-2:],
                   "queue": senses["queue"],
                   "landed_count": senses["landed"]["count"],
                   "landed_tail": senses["landed"]["tail"][:6]}
        row = {"schema": SCHEMA, "run_id": run_id, "tick": tick,
               "ts": _now(), "tag": tag, "senses": compact}
        attempt_verb, events = None, []
        verb, reason = "NOOP", ""
        executed, verified, cost = False, True, 0.0
        budget.spent = spend_from_ledger(run_id)  # byte-truth reconcile
        if not budget.allow_dispatch():
            reason = (f"budget hold: cumulative ${budget.spent:.4f} within "
                      f"${DISPATCH_RESERVE_USD:.2f} of the "
                      f"${budget.cumulative:.2f} cap")
        else:
            try:
                decision, cost, raw = decide(tick, ticks, run_id, senses)
                if decision is None:
                    raise UnauthorizedVerb(
                        "reply carried no JSON decision object: "
                        + repr(raw[:120]))
                attempt_verb = decision.get("verb")
                verb = validate_verb(decision)
                res = execute_verb(verb, decision.get("payload") or {},
                                   {"run_id": run_id, "tick": tick,
                                    "ts": _now()})
                reason = str(decision.get("reason") or "").strip()
                executed, verified = res["executed"], res["verified"]
                row["effect"] = res
            except UnauthorizedVerb as exc:
                events.append({"gate": "verb-gate", "blocked": True,
                               "attempt_verb": attempt_verb,
                               "detail": str(exc)[:220]})
                verb, reason = "NOOP", ("verb gate BLOCKED an unauthorized "
                                        f"attempt ({str(exc)[:140]}); "
                                        "zero side effects")
                executed, verified = False, True
            except Exception as exc:  # transport/refusal: reasoned silence
                events.append({"gate": "brain-fire", "error":
                               str(exc)[:220]})
                verb, reason = "NOOP", ("brain fire failed: "
                                        + str(exc)[:140])
                executed, verified = False, True
            finally:
                budget.spent = spend_from_ledger(run_id)
            if budget.spent > budget.cumulative + 1e-9:
                events.append({"gate": "budget", "blocked": True, "detail":
                               f"cumulative ${budget.spent:.4f} exceeded "
                               f"${budget.cumulative:.2f}"})
                verb, reason = "NOOP", "HARD BUDGET BREACH (kill condition 5)"
                executed, verified = False, True
                exit_code = 2  # hard kill semantics
        wall = round(time.monotonic() - t0, 1)
        row.update({"verb": verb, "reason": reason, "executed": executed,
                    "verified": verified, "cost_usd": round(cost, 6),
                    "cumulative_usd": budget.spent,
                    "wall_s": wall, "cadence_late": wall > interval,
                    "events": events, "attempt_verb": attempt_verb})
        ledger_append(row)
        print(f"tick {tick:3d}/{ticks} verb={verb:<14} exec={int(executed)} "
              f"verified={int(verified)} ${budget.spent:.4f} "
              f"wall={wall:.0f}s reason={reason[:90]}", flush=True)
        if exit_code == 2:
            print("OVERMIND run aborted: hard budget breach (kill "
                  "condition 5)", flush=True)
            break
        if tick < ticks:
            time.sleep(max(0.0, interval - (time.monotonic() - t0)))
    summary = summarize(run_id=run_id)
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"summary_of": run_id, **summary},
                     ensure_ascii=False), flush=True)
    return summary


def summarize(run_id: str | None = None) -> dict:
    """Aggregate the ledger (one run, or all runs when run_id is None)."""
    if not LEDGER.is_file():
        return {"runs": [], "ticks": 0}
    rows = []
    for line in LEDGER.read_text(encoding="utf-8",
                                 errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if run_id:
        rows = [r for r in rows if r.get("run_id") == run_id]
    verbs: dict[str, int] = {}
    noop_silent = unauthorized_attempts = unverified = 0
    per_run: dict[str, dict] = {}
    for r in rows:
        v = r.get("verb") or "?"
        verbs[v] = verbs.get(v, 0) + 1
        if v == "NOOP" and not str(r.get("reason") or "").strip():
            noop_silent += 1
        for e in r.get("events") or []:
            if e.get("gate") == "verb-gate" and e.get("blocked"):
                unauthorized_attempts += 1
        if r.get("executed") and not r.get("verified"):
            unverified += 1
        rid = r.get("run_id") or "?"
        d = per_run.setdefault(rid, {"run_id": rid, "ticks": 0, "verbs": {},
                                     "spend": 0.0,
                                     "first_ts": r.get("ts"),
                                     "last_ts": r.get("ts")})
        d["ticks"] += 1
        d["verbs"][v] = d["verbs"].get(v, 0) + 1
        d["spend"] = round(d["spend"] + float(r.get("cost_usd") or 0), 6)
        d["last_ts"] = r.get("ts")
    total = len(rows)
    return {"ticks": total, "verbs": verbs,
            "noop_share": round(verbs.get("NOOP", 0) / total, 4)
            if total else 0.0,
            "silent_noops": noop_silent,
            "unauthorized_attempts_blocked": unauthorized_attempts,
            "unauthorized_executed": 0,  # structurally impossible (the gate)
            "executed_unverified": unverified,
            "runs": sorted(per_run.values(),
                           key=lambda d: d["first_ts"] or "")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="overmind_loop")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--ticks", type=int, default=40)
    r.add_argument("--interval", type=float, default=90.0)
    r.add_argument("--run-id")
    r.add_argument("--blind-sha")
    r.add_argument("--tag", default="")
    r.add_argument("--per-call-cap", type=float, default=PER_CALL_CAP_USD)
    r.add_argument("--cumulative-cap", type=float,
                   default=CUMULATIVE_CAP_USD)
    sub.add_parser("verify")
    s = sub.add_parser("summary")
    s.add_argument("--run-id")
    args = ap.parse_args(argv)
    if args.cmd == "run":
        if args.ticks < 1 or args.interval < 0:
            print("USAGE-ERROR: --ticks >= 1 and --interval >= 0")
            return 2
        run_loop(ticks=args.ticks, interval=args.interval,
                 run_id=args.run_id, blind_sha=args.blind_sha, tag=args.tag,
                 per_call_cap=args.per_call_cap,
                 cumulative_cap=args.cumulative_cap)
        return 0
    if args.cmd == "verify":
        v = verify_ledger()
        print(json.dumps(v, ensure_ascii=False))
        return 0 if v["ok"] else 2
    print(json.dumps(summarize(run_id=args.run_id),
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
