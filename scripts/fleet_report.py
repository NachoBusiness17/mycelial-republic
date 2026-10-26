#!/usr/bin/env python3
"""fleet_report — CLI for fleet_report.v1 (SPOTREP/SITREP/NOTICE/RELIEF/ACK) and notices.

  python scripts/fleet_report.py file SITREP --seat grok --field status="green, 3 tasks" --field readiness="ready"
  python scripts/fleet_report.py file SPOTREP --seat grok --json report.json
  python scripts/fleet_report.py validate report.json            # full report incl. schema/kind/dtg/seat
  python scripts/fleet_report.py ack --seat grok --of N-20261017-opencode-console-breach [--note "rotated"]
  python scripts/fleet_report.py notices                         # in force + acks
  python scripts/fleet_report.py file NOTICE --seat grok --json notice.json --dry   # validate, file nothing

--field k=v sets a string field; --list-field k=a,b sets a list field (affects,
names, leases); --field stand_relieved=true is coerced to the boolean.
Filing goes through estate_bridge.shared_receipt_append (watch/receipts/seat_*.json).
Exit: 0 ok, 1 invalid report, 2 bad call.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import fleet_report as fr  # noqa: E402


def _fields(a: argparse.Namespace) -> dict:
    out: dict = {}
    if getattr(a, "json", None):
        out.update(json.loads(Path(a.json).read_text(encoding="utf-8")))
    for kv in getattr(a, "field", None) or []:
        k, _, v = kv.partition("=")
        out[k.strip()] = True if (k.strip() == "stand_relieved" and v.lower() == "true") else v
    for kv in getattr(a, "list_field", None) or []:
        k, _, v = kv.partition("=")
        out[k.strip()] = [x.strip() for x in v.split(",") if x.strip()]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="fleet_report", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("file")
    f.add_argument("kind", choices=fr.KINDS)
    f.add_argument("--seat", required=True)
    f.add_argument("--model", default="")
    f.add_argument("--title", default="")
    f.add_argument("--json", help="JSON file with the kind's fields")
    f.add_argument("--field", action="append", help="k=v string field")
    f.add_argument("--list-field", action="append", help="k=a,b list field")
    f.add_argument("--dry", action="store_true", help="validate and print; file nothing")
    v = sub.add_parser("validate"); v.add_argument("path")
    k = sub.add_parser("ack")
    k.add_argument("--seat", required=True); k.add_argument("--of", required=True)
    k.add_argument("--note", default=""); k.add_argument("--model", default="")
    sub.add_parser("notices")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "validate":
            errs = fr.validate(json.loads(Path(a.path).read_text(encoding="utf-8")))
            print(json.dumps({"ok": not errs, "errors": errs}, indent=1))
            return 0 if not errs else 1
        if a.cmd == "notices":
            print(json.dumps(fr.notices(), indent=1, ensure_ascii=False))
            return 0
        if a.cmd == "ack":
            fields = {"ack_of": a.of, **({"note": a.note} if a.note else {})}
            out = fr.file_report(seat=a.seat, kind="ACK", report=fields, model=a.model)
        else:
            fields = _fields(a)
            if a.dry:
                rep = fr.build_report(a.kind, a.seat, fields, model=a.model)
                errs = fr.validate(rep)
                print(json.dumps({"ok": not errs, "errors": errs, "report": rep}, indent=1,
                                 ensure_ascii=False))
                return 0 if not errs else 1
            out = fr.file_report(seat=a.seat, kind=a.kind, report=fields, model=a.model,
                                 title=a.title)
    except fr.ReportInvalid as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=1))
        return 1
    except (ValueError, OSError) as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}, indent=1))
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
