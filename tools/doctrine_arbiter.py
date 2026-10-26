"""doctrine_arbiter v0 - doctrine is measured, not obeyed (R10, 2026-09-30).

The frontier interrogation's #1 structural finding (ASK6): "a single
verdict can reach every lane before anything measures whether the doctrine
itself improved outcomes." A rib, spec amendment, or route pitch lands as
law the moment a verdict blesses it, and nothing ever asks whether the
world it predicted arrived. This tool is the missing measurement: a
pre-registration ledger for doctrine plus a check pass that scores every
active item against the estate's own instruments. Implementation modules:
tools/doctrine_arbiter_core.py (law/fold/check/scorecard),
tools/doctrine_arbiter_instruments.py (instrument adapters).

THREE LAWS (fixed by the mission):

1. PRE-REGISTRATION LAW. A doctrine item registers the four-tuple
   {id, source_verdict, predicted_outcome, deadline}. A registration
   whose predicted_outcome is missing, empty, or uncheckable (unknown
   instrument / metric / selector / op) is VOID at registration: the row
   is still appended (audit trail) but carries status VOID, is never
   checked, and never counts as active doctrine. The same holds for a
   missing id / source_verdict / unparseable deadline - the four-tuple is
   the contract, any broken member voids the item. Duplicate ids refuse
   hard (an id is a doctrine identity; reregistration rewrites history).

2. OPERATOR RETIREMENT GATE. The check pass only SCORES. EXPIRED items
   are flagged retire candidates; nothing is ever auto-removed, reworded,
   or rewritten. Retirement is a separate explicit `retire` subcommand
   and is refused on PENDING items - retiring an unmeasured prediction
   would dodge exactly the measurement this tool exists to force.

3. APPEND-ONLY LEDGER. memory/doctrine/LEDGER.jsonl is an event stream
   (registration / check / retirement rows); current state is always a
   fold, never an in-place edit. History is the evidence.

PREDICTED OUTCOMES are structured, not prose - that is what makes the
check pass mechanical (no judge model in the loop):

    predicted_outcome = {
      "instrument": "gps_ledger | duel_table | parity_gate | anomaly_counts",
      "metric":     see table,        "selector": instrument-specific
      "op":         "== != < <= > >=", "value":   number or bool }

    gps_ledger     pass_rate, sample_size   sel: model_id, task_shape
                   (tools/gps_mcp gps_ledger.db3; unmeasured pair = no data)
    duel_table     win_rate, decided, ties  sel: model
                   (logs/duel/duels.jsonl; winner already logical A/B;
                   TIE/UNPARSED excluded from decided; v0 counts all rows
                   incl. altjudge; zero decided -> win_rate undefined)
    parity_gate    parity_ok, diverged_seqs sel: mode (optional; mismatch
                   = no data)  (tools/rule_parity_out/latest.json, D2)
    anomaly_counts anomaly_count            sel: surface (optional)
                   (tools/anomaly_flagger.py; the anomalous ROW is the unit)

VERDICTS per item:
    PENDING     active; deadline not passed and prediction not yet
                materialized (instrument says no, or has no data yet)
    VINDICATED  measured true on a check that ran ON OR BEFORE the
                deadline (a truth first measured after the term is a
                late arrival, not a vindication); terminal and permanent
                - later drift does not un-vindicate; if doctrine must
                keep holding, a NEW item with a NEW deadline registers it
    EXPIRED     deadline passed without the prediction materializing;
                terminal; flagged RETIRE CANDIDATE (operator gate)
    VOID        never was doctrine (pre-registration law)
    RETIRED     operator closed a terminal item via `retire`

A dark instrument surface (missing stream) is an InstrumentError -> exit
2, distinct from no-data (PENDING). Exit codes overall: 0 ok; 1 attention
(check/scorecard: EXPIRED items exist; register: item voided); 2 error.

Usage:
    python tools/doctrine_arbiter.py register --id rib-driving-ladder \\
        --kind rib --source-verdict "memory/rib/RIB_DRIVING_LADDER_20260928.md" \\
        --claim "only Hermes funded improves judgment routing" \\
        --instrument duel_table --metric win_rate --op ">=" --value 0.55 \\
        --sel model=z-ai/glm-5.3-prime --deadline 2026-10-15
    python tools/doctrine_arbiter.py check       # score pass + artifact
    python tools/doctrine_arbiter.py scorecard   # read-only view
    python tools/doctrine_arbiter.py retire --id rib-driving-ladder --note "..."

Spec filed in this docstring BEFORE the modules below (build discipline:
spec-before-behavior; this tool introduces new behavior, it changes
none). Receipt: watch/inbox/last_mile_20260930/R10_DOCTRINE_ARBITER.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:  # direct-script execution: tools/ is cwd-path
    sys.path.insert(0, str(_ROOT))

from tools.doctrine_arbiter_core import (
    EXIT_ATTENTION, EXIT_ERROR, EXIT_OK, KINDS, OPS, INSTRUMENTS, TERMINAL,
    LEDGER_PATH, SCORECARD_PATH, append_row, fold_ledger, prediction_void_reasons,
    read_rows, render_scorecard, run_check, scorecard_document, utc_now_iso)
from tools.doctrine_arbiter_instruments import (
    InstrumentError, InstrumentPaths)

# Re-exports so callers (and tests) can treat this module as the surface.
from tools.doctrine_arbiter_core import (  # noqa: F401
    DoctrineItem, compare, parse_deadline)
from tools.doctrine_arbiter_instruments import (  # noqa: F401
    MEASURERS, measure_duel_table)


# -------------------------------------------------------------------- CLI ---

def _parse_value(text: str) -> Any:
    low = text.strip().lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text


def build_registration(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "type": "registration",
        "id": args.id or "",
        "kind": args.kind or "",
        "claim": args.claim or "",
        "source_verdict": args.source_verdict or "",
        "deadline": args.deadline or "",
        "predicted_outcome": {
            "instrument": args.instrument or "",
            "metric": args.metric or "",
            "selector": dict(args.selector or {}),
            "op": args.op or "",
            "value": None if args.value is None else _parse_value(args.value)},
        "registered_ts": utc_now_iso(),
    }


def cmd_register(args: argparse.Namespace) -> int:
    if args.from_json:
        try:
            item = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read --from-json: {exc}", file=sys.stderr)
            return EXIT_ERROR
        item.setdefault("type", "registration")
        item.setdefault("registered_ts", utc_now_iso())
    else:
        item = build_registration(args)
    existing = {str(r.get("id")) for r in read_rows(args.ledger)
                if r.get("type") == "registration"}
    if item.get("id") in existing:
        # an id is a doctrine identity; a second registration would
        # rewrite history silently. Refuse hard, write nothing.
        print(f"ERROR: duplicate doctrine id {item.get('id')!r}; "
              f"ledger already holds it", file=sys.stderr)
        return EXIT_ERROR
    reasons = prediction_void_reasons(item)
    if reasons:
        item["status"] = "VOID"
        item["void_reasons"] = reasons
        append_row(args.ledger, item)
        print(f"VOID {item.get('id')}: " + "; ".join(reasons))
        print("  (pre-registration law: the item is recorded but never "
              "active; register a four-tuple with a checkable prediction)")
        return EXIT_ATTENTION
    item["status"] = "PENDING"
    append_row(args.ledger, item)
    pred = item["predicted_outcome"]
    print(f"REGISTERED {item['id']} ({item.get('kind') or 'untyped'}) "
          f"PENDING deadline {item['deadline']}")
    print(f"  prediction: {pred['instrument']}.{pred['metric']} "
          f"{pred['op']} {pred['value']!r} on {pred.get('selector') or {}}")
    print(f"  source verdict: {item['source_verdict']}")
    return EXIT_OK


def _instrument_paths(args: argparse.Namespace) -> InstrumentPaths:
    return InstrumentPaths(
        gps_db=args.gps_db, duels=args.duels,
        parity_latest=args.parity_latest,
        anomaly_steps=args.anomaly_steps, anomaly_oral=args.anomaly_oral,
        anomaly_ledger=args.anomaly_ledger,
        anomaly_enum_map=args.anomaly_enum_map)


def cmd_check(args: argparse.Namespace) -> int:
    rows = read_rows(args.ledger)
    if not rows:
        print(f"NO DOCTRINE: ledger empty or missing: {args.ledger}")
        return EXIT_OK
    try:
        ordered, exit_code = run_check(fold_ledger(rows), args.ledger,
                                       _instrument_paths(args))
    except InstrumentError as exc:
        print(f"INSTRUMENT ERROR: {exc}", file=sys.stderr)
        return EXIT_ERROR
    print(render_scorecard(ordered, utc_now_iso(), args.ledger))
    doc = scorecard_document(ordered, args.ledger)
    args.scorecard_out.parent.mkdir(parents=True, exist_ok=True)
    args.scorecard_out.write_text(
        json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"scorecard artifact: {args.scorecard_out}")
    return exit_code


def cmd_scorecard(args: argparse.Namespace) -> int:
    rows = read_rows(args.ledger)
    if not rows:
        print(f"NO DOCTRINE: ledger empty or missing: {args.ledger}")
        return EXIT_OK
    items = list(fold_ledger(rows).values())
    print(render_scorecard(items, utc_now_iso(), args.ledger))
    return EXIT_ATTENTION if any(i.retire_candidate for i in items) else EXIT_OK


def cmd_retire(args: argparse.Namespace) -> int:
    items = fold_ledger(read_rows(args.ledger))
    item = items.get(args.id)
    if item is None:
        print(f"ERROR: unknown doctrine id {args.id!r}", file=sys.stderr)
        return EXIT_ERROR
    if item.status not in TERMINAL:
        # PENDING: dodges the measurement. VOID: never was doctrine.
        print(f"ERROR: {args.id} is {item.status}; only terminal items "
              f"({', '.join(TERMINAL)}) can retire - the operator gate "
              f"exists to close measured doctrine, not skip measuring it",
              file=sys.stderr)
        return EXIT_ERROR
    append_row(args.ledger, {"type": "retirement", "id": args.id,
                             "ts": utc_now_iso(), "from_status": item.status,
                             "note": args.note or ""})
    print(f"RETIRED {args.id} (was {item.status})"
          + (f": {args.note}" if args.note else ""))
    return EXIT_OK


def add_instrument_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH,
                        help=f"doctrine ledger (default {LEDGER_PATH})")
    parser.add_argument("--gps-db", type=Path,
                        default=InstrumentPaths.gps_db, help="gps ledger db")
    parser.add_argument("--duels", type=Path,
                        default=InstrumentPaths.duels, help="duel ledger jsonl")
    parser.add_argument("--parity-latest", type=Path,
                        default=InstrumentPaths.parity_latest,
                        help="rule_parity latest.json")
    parser.add_argument("--anomaly-steps", type=Path, default=None)
    parser.add_argument("--anomaly-oral", type=Path, default=None)
    parser.add_argument("--anomaly-ledger", type=Path, default=None)
    parser.add_argument("--anomaly-enum-map", type=Path, default=None)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="doctrine arbiter v0: pre-registered doctrine, "
                    "measured against the estate's instruments")
    sub = parser.add_subparsers(dest="cmd", required=True)

    reg = sub.add_parser("register", help="pre-register one doctrine item")
    # --id is deliberately not argparse-required: --from-json carries its
    # own id, and a flag-path id gap is a void reason (four-tuple law),
    # not a usage crash.
    reg.add_argument("--id", default="", help="unique doctrine id")
    reg.add_argument("--kind", choices=KINDS, default="",
                     help="rib | spec_amendment | route_pitch")
    reg.add_argument("--source-verdict", default="",
                     help="the verdict/receipt this doctrine descended from")
    reg.add_argument("--claim", default="",
                     help="human-readable statement of the doctrine")
    reg.add_argument("--instrument", default="",
                     help="one of: " + " ".join(INSTRUMENTS))
    reg.add_argument("--metric", default="")
    reg.add_argument("--op", default="", help="one of: " + " ".join(OPS))
    reg.add_argument("--value", default=None,
                     help="number or true/false the metric is compared to")
    reg.add_argument("--sel", dest="selector", action="append", default=[],
                     metavar="KEY=VALUE",
                     help="instrument selector pair (repeatable)")
    reg.add_argument("--deadline", default="",
                     help="ISO date YYYY-MM-DD the prediction must hold by")
    reg.add_argument("--from-json", default="",
                     help="register from a full JSON document instead")
    add_instrument_args(reg)
    reg.set_defaults(func=cmd_register)

    for name, help_text, fn in (
            ("check", "run the check pass, update the ledger, print "
                      "scorecard (writes check rows)", cmd_check),
            ("scorecard", "read-only scorecard (no ledger writes)",
             cmd_scorecard)):
        p = sub.add_parser(name, help=help_text)
        add_instrument_args(p)
        p.set_defaults(func=fn)
    sub.choices["check"].add_argument(
        "--scorecard-out", type=Path, default=SCORECARD_PATH,
        help=f"scorecard artifact path (default {SCORECARD_PATH})")

    ret = sub.add_parser("retire", help="operator gate: close a terminal item")
    ret.add_argument("--id", required=True)
    ret.add_argument("--note", default="")
    add_instrument_args(ret)
    ret.set_defaults(func=cmd_retire)

    args = parser.parse_args(argv)
    if getattr(args, "selector", None):
        selector: dict[str, str] = {}
        for pair in args.selector:
            if "=" not in pair:
                print(f"ERROR: --sel expects KEY=VALUE, got {pair!r}",
                      file=sys.stderr)
                return EXIT_ERROR
            key, value = pair.split("=", 1)
            selector[key.strip()] = value.strip()
        args.selector = selector
    else:
        args.selector = {}
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
