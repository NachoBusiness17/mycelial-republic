"""CLI: python -m tools.secret_guard {check PATH | fingerprint-count | scan FILE | audit-tail N}
Never prints a secret value. There is deliberately no 'get' or 'export' subcommand: a CLI
that prints a value would put it on stdout, which an agent can pipe anywhere."""
from __future__ import annotations

import argparse
import io
import json
import sys

from tools.secret_guard import guard, audit


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="secret_guard")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").add_argument("path")
    sub.add_parser("fingerprint-count")
    sub.add_parser("scan").add_argument("file")
    sub.add_parser("audit-tail").add_argument("n", type=int, nargs="?", default=20)
    a = ap.parse_args(argv)
    if a.cmd == "check":
        print("SECRET" if guard.is_secret_path(a.path) else "not-secret")
        return 0
    if a.cmd == "fingerprint-count":
        print(len(guard.fingerprints()))
        return 0
    if a.cmd == "scan":
        with io.open(a.file, "rb") as f:
            hits = guard.payload_hits(f.read())
        for s8, rel, key in hits:
            print(f"HIT sha8={s8} source={rel} key={key}")
        audit.log("scan", caller="cli", file=a.file, hits=[h[0] for h in hits])
        return 3 if hits else 0
    if a.cmd == "audit-tail":
        with io.open(audit.audit_path(), "r", encoding="utf-8") as f:
            for line in f.readlines()[-a.n:]:
                sys.stdout.write(line)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
