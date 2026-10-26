#!/usr/bin/env python3
"""lease — CLI for restricted-list leases (mag/leases.py, configs/restricted_leases.json).

  python scripts/lease.py list
  python scripts/lease.py status proc:lab
  python scripts/lease.py acquire proc:lab --seat grok --purpose "restart lab after compose edit" [--ttl 1800]
  python scripts/lease.py renew   proc:lab --seat grok --token <lease_token> [--ttl 1800]
  python scripts/lease.py release proc:lab --seat grok --token <lease_token>
  python scripts/lease.py transfer proc:lab --seat grok --token <lease_token> --to gemini
  python scripts/lease.py check-path memory/biography/verkle_chain.jsonl
  python scripts/lease.py break proc:lab --operator nacho --reason "holder seat died"   (operator only)

--token may be omitted when env MAG_LEASE_TOKEN is set (and --seat from MAG_LEASE_SEAT).
Gated scripts (scripts/lab_ctl.py, mag/docker_ops.py up/down, chain repair tools)
read MAG_LEASE_SEAT + MAG_LEASE_TOKEN from the environment.
Exit: 0 ok, 3 refused (held by another seat), 2 bad call.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import leases  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lease", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("status"); s.add_argument("resource")
    for name in ("acquire", "renew", "release", "transfer"):
        p = sub.add_parser(name)
        p.add_argument("resource")
        p.add_argument("--seat", default=os.environ.get(leases.ENV_SEAT))
        if name != "acquire":
            p.add_argument("--token", default=os.environ.get(leases.ENV_TOKEN))
        if name in ("acquire", "renew", "transfer"):
            p.add_argument("--ttl", type=int, default=None)
        if name in ("acquire", "transfer"):
            p.add_argument("--purpose", default="" if name == "transfer" else None,
                           required=(name == "acquire"))
        if name == "transfer":
            p.add_argument("--to", required=True)
        if name == "release":
            p.add_argument("--note", default="")
    c = sub.add_parser("check-path"); c.add_argument("path")
    b = sub.add_parser("break")
    b.add_argument("resource"); b.add_argument("--operator", required=True)
    b.add_argument("--reason", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "list":
            out = leases.list_leases()
        elif a.cmd == "status":
            out = leases.status(resource=a.resource)
        elif a.cmd == "acquire":
            out = leases.acquire(resource=a.resource, seat=a.seat, purpose=a.purpose, ttl_s=a.ttl)
        elif a.cmd == "renew":
            out = leases.renew(resource=a.resource, seat=a.seat, lease_token=a.token, ttl_s=a.ttl)
        elif a.cmd == "release":
            out = leases.release(resource=a.resource, seat=a.seat, lease_token=a.token, note=a.note)
        elif a.cmd == "transfer":
            out = leases.transfer(resource=a.resource, seat=a.seat, lease_token=a.token,
                                  to_seat=a.to, ttl_s=a.ttl, purpose=a.purpose)
        elif a.cmd == "check-path":
            out = {"path": a.path, "restricted": leases.resource_for_path(a.path)}
        else:
            out = leases.break_lease(resource=a.resource, operator=a.operator, reason=a.reason)
    except leases.LeaseError as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=1))
        return 2
    print(json.dumps(out, indent=1, default=str))
    if out.get("refused"):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
