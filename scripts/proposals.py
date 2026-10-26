#!/usr/bin/env python3
"""proposals: CLI over signed seat-to-seat proposals (mag/proposals.py), 2026-10-17.

  list                               every proposal with author / votes / ready
  show  <id>                         all signed messages + tally
  tally <id>                         quorum view (distinct seats, author excluded)
  sign  proposal|review|promotion --payload FILE.json [--key PATH] [--submit]
                                     sign with your seat key (or env
                                     MAG_SEAT_KEY_PATH); prints the message, or
                                     files it with --submit
  promote <id> [--key PATH]          sign + file a promotion marker; refused
                                     unless the tally says ready

Ready is a MARK only. Nothing here applies a diff, branches, commits or
merges: git belongs to the operator's git window.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import proposals as P  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="proposals", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    for name in ("show", "tally"):
        sub.add_parser(name).add_argument("id")
    s = sub.add_parser("sign")
    s.add_argument("kind", choices=P.KINDS)
    s.add_argument("--payload", type=Path, required=True)
    s.add_argument("--key")
    s.add_argument("--submit", action="store_true")
    pr = sub.add_parser("promote")
    pr.add_argument("id")
    pr.add_argument("--key")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        out = P.list_proposals()
    elif a.cmd == "show":
        out = P.show(a.id)
    elif a.cmd == "tally":
        out = P.tally(a.id)
    elif a.cmd == "sign":
        payload = json.loads(a.payload.read_text(encoding="utf-8"))
        msg = P.sign_message(a.kind, payload, key_path=a.key)
        out = P.submit(msg) if a.submit else msg
    else:
        t = P.tally(a.id)
        if not t["ready"]:
            print(json.dumps({"refused": "quorum not met", "tally": t}, indent=1))
            return 1
        msg = P.sign_message("promotion", {"proposal_id": a.id, "state": "ready",
                                           "tally": {"approvers": t["approvers"],
                                                     "quorum": t["quorum"]}}, key_path=a.key)
        out = P.submit(msg)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
