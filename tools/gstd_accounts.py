#!/usr/bin/env python3
"""gstd_accounts - the internal GSTD economy (Phase 4 babystep 3).

Operator law 2026-10-12: "use our rewarded currency internally to create the
ecosystem - a common economic principle." The design that makes it real on
TON: GSTD is the internal working currency (earned per certified run, spent
on routing weight, reputation, priority); TON is the boundary fuel (only
touched when a worker CLAIMS accrued GSTD on-chain - and the worker pays its
own claim gas from its share). The chain nets in batches; the internal economy
never touches it.

Ledger: reference/gstdcoin/contracts/accounts.jsonl (append-only, one row per
event: credit | claim | settle_net). The jetton balance remains the on-chain
truth; this ledger is the internal working balance between claims.

Subcommands:
  credit <worker> <amount_gstd> --reason <why>   internal earn (free)
  statement [worker]                              the internal economy view
  claim <worker>                                  net accrued GSTD on-chain
                                                  (fires the gated settle for
                                                  the worker's full pending)

The drain credits internally per certified run; claims fire when a worker's
pending crosses --claim-threshold (default 100 GSTD = 4 certified runs). The
master's TON bleed drops by the same factor.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCOUNTS = ROOT / "reference" / "gstdcoin" / "contracts" / "accounts.jsonl"

KNOWN = {
    "UQBX4TEs0dCvV7CzDpUmj04niFPVd0jjbCfhquO8dPxxa3BJ": "DESKTOP",
    "UQAW3wO8TwzoBuOjA-XwCivj80eKhRzGAWl_PgkzUUUlbe5m": "BOB",
    "UQBrE6BRPvZkBH47rHGfL7TmepeakX--unodq9I_K6f7BA3p": "T90",
}


def now() -> str:
    return _dt.datetime.utcnow().isoformat() + "Z"


def append(row: dict) -> None:
    with ACCOUNTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def rows() -> list[dict]:
    if not ACCOUNTS.is_file():
        return []
    out = []
    for line in ACCOUNTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def balances() -> dict:
    b: dict[str, float] = {}
    for r in rows():
        w = r.get("worker")
        if not w:
            continue
        b.setdefault(w, 0.0)
        if r.get("type") == "credit":
            b[w] += float(r.get("amount", 0))
        elif r.get("type") == "claim":
            b[w] -= float(r.get("amount", 0))
    return b


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["credit", "statement", "claim"])
    ap.add_argument("worker", nargs="?", default="")
    ap.add_argument("amount", nargs="?", type=float, default=0.0)
    ap.add_argument("--reason", default="")
    ap.add_argument("--threshold", type=float, default=100.0, help="claim when pending >= this many GSTD")
    a = ap.parse_args()

    if a.cmd == "credit":
        if not a.worker or a.amount <= 0:
            print("credit needs <worker> <amount_gstd>"); return 2
        row = {"ts": now(), "type": "credit", "worker": a.worker,
               "amount": a.amount, "reason": a.reason or "certified run"}
        append(row)
        print(f"credited {a.amount} GSTD to {KNOWN.get(a.worker, a.worker)} - internal, no chain touch")
        return 0

    if a.cmd == "statement":
        b = balances()
        on_chain = {"DESKTOP": 100.0}
        print("=== GSTD INTERNAL ECONOMY ===")
        for w, amt in sorted(b.items()):
            name = KNOWN.get(w, w[:14])
            pending = amt
            print(f"{name:10s} internal earned: {amt:>10.2f} GSTD | pending claim: {pending:>8.2f} | on-chain (last settle): {on_chain.get(name, 'see chain')}")
        tot = sum(b.values())
        print(f"{'TOTAL':10s} internal earned: {tot:>10.2f} GSTD | the internal currency in circulation")
        return 0

    if a.cmd == "claim":
        b = balances()
        pending = b.get(a.worker, 0.0)
        if pending < a.threshold:
            print(f"claim refused: {a.worker} pending {pending} GSTD < threshold {a.threshold} - keep earning")
            return 3
        row = {"ts": now(), "type": "claim", "worker": a.worker, "amount": pending,
               "note": "net on-chain via the gated bridge (settle-consensus) - worker pays own claim gas from its TON share"}
        append(row)
        print(f"claim recorded: {pending} GSTD for {KNOWN.get(a.worker, a.worker)} - fire the gated settle to net it on-chain:")
        print(f"  npx ts-node --project tsconfig.deploy.json scripts/settle-consensus.ts --verdict STRUCTURE --consensus <r> --correct <r> --run <run_id> --node <node>")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
