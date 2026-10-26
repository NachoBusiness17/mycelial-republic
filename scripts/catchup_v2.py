#!/usr/bin/env python3
"""Reconcile v2 with v1: append v1 rows N+1..end (and any v1 amend) to the v2 chain, idempotently.

For every v1 session, its LAST v1 row must be that session's latest mirrored v1 leaf in v2;
otherwise one knot (new session) or amend (known session) row is appended. Running it twice
appends nothing the second time. Reads v1 WITHOUT the v1 lock (a torn tail is ignored);
writes only memory/biography_v2 under its own lock. This is the healer for a crash between
the v1 write and the shadow write.

usage: python scripts/catchup_v2.py [--check] [--checkpoint] [--v2-dir DIR] [--v1-bio DIR] [--knots-dir DIR ...]
Exit 0 = ok (and --check: nothing pending), 3 = --check found pending rows, 2 = no seed yet.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from mag import bintree_v2 as bt  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report pending rows; write nothing")
    ap.add_argument("--checkpoint", action="store_true", help="write an (unsigned) checkpoint after catching up")
    ap.add_argument("--v2-dir")
    ap.add_argument("--v1-bio")
    ap.add_argument("--v1-chain", help="override the v1 chain file (read only)")
    ap.add_argument("--knots-dir", action="append")
    a = ap.parse_args(argv)
    st = bt.Store(a.v2_dir, a.v1_bio, a.knots_dir)
    rep = bt.reconcile(st, Path(a.v1_chain) if a.v1_chain else None, check_only=a.check)
    if not rep.get("ok"):
        print(json.dumps(rep, indent=2))
        return 2
    if a.check and rep.get("pending"):
        st.log_mismatch({"event": "catchup_check_pending", "pending": rep["pending"]})
    if a.checkpoint and not a.check:
        with bt.v2_lock(st, timeout=60):
            cp = bt.make_checkpoint(st, st.load())
        rep["checkpoint"] = {"n": cp["n"], "root": cp["root"], "status": cp["status"]}
    print(json.dumps(rep, indent=2))
    return 3 if a.check and rep.get("pending") else 0


if __name__ == "__main__":
    sys.exit(main())
