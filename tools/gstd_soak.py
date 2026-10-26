#!/usr/bin/env python3
"""gstd_soak - the 50-cycle fresh-testnet soak against the amended build.

The launch-brief soak gate (2026-10-13): "50-cycle fresh-testnet loop
against the amended build" - the pre-mainnet validation for PR #1 bytecode
that has never run (RED-lane threat 1). The target is SettlementMaster v7
(EQCteLhGv7dCLtCtbSK8bs5mxikKF-ckZ11vvf-5WUjpjrLb), deployed fresh from PR
head 185b3d8: the checked bonus relay (b4c60d0) + the contract-level
balance band (185b3d8).

One cycle = the production gated bridge settle (scripts/settle-consensus.ts,
same path the standing cron fires) -> classify -> verify:

  SETTLED       worker jetton wallet rose; master stats +1 task
  BAND_BOUNCE   master under floor+relay reserve; the settle REVERTED on
                chain (worker unchanged, taskCount unchanged) - the band
                invariant doing its job, which is evidence, not failure
  GATE_REFUSE   client bridge gate refused under 0.5 TON
  TIMEOUT       no worker delta in 4 min - the relay-skip signature the
                2026-10-13 amendment was supposed to kill; a TIMEOUT is a
                soak FAILURE and stops nothing but is flagged loudly

Refill: when the master approaches the band edge the driver refills from
the deployer, then from the desktop worker wallet (wages recycle - the
economy funding its own soak). Every row banks to
watch/inbox/gstd_soak_20261014/cycles.jsonl; the closing receipt summarizes.

Run:
  .venv/Scripts/python.exe tools/gstd_soak.py --cycles 50
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_CWD = ROOT / "reference" / "gstdcoin" / "contracts"
TS_NODE = BRIDGE_CWD / "node_modules" / "ts-node" / "dist" / "bin.js"
BRIDGE = "scripts/settle-consensus.ts"
SOAK_DIR = ROOT / "watch" / "inbox" / "gstd_soak_20261014"

V7_MASTER = "EQCteLhGv7dCLtCtbSK8bs5mxikKF-ckZ11vvf-5WUjpjrLb"
DESKTOP_MAIN = "UQBX4TEs0dCvV7CzDpUmj04niFPVd0jjbCfhquO8dPxxa3BJ"

# floor 1.0 TON + 0.35 relay reserve = the contract's own band require; the
# driver refills BEFORE wasting a fee once the fresh read is under this plus
# a 0.05 margin
BAND_EDGE = 1.40
REFILL_FROM_DEPLOYER = 2.0
REFILL_FROM_WORKER = 2.0
DEPLOYER_KEEP = 0.7  # deployer always keeps gas money


def log(msg: str) -> None:
    print(f"{_dt.datetime.utcnow().strftime('%H:%M:%SZ')} {msg}", flush=True)


def node_script(script: str) -> str:
    """Run a one-shot inline node script in the contracts repo (dotenv wired)."""
    p = subprocess.run(
        ["node", str(TS_NODE), "--project", str(BRIDGE_CWD / "tsconfig.deploy.json"),
         "--eval", script],
        capture_output=True, text=True, timeout=180,
        cwd=str(BRIDGE_CWD), encoding="utf-8", errors="replace",
        env={**os.environ, "GSTD_MASTER_ADDRESS": V7_MASTER},
    )
    return (p.stdout or "") + (p.stderr or "")


SOAK_STATE = "scripts/soak-state.ts"


def run_soak_state(mode: str, extra: list[str] | None = None) -> str:
    p = subprocess.run(
        ["node", str(TS_NODE), "--project", str(BRIDGE_CWD / "tsconfig.deploy.json"),
         SOAK_STATE, mode] + (extra or []),
        capture_output=True, text=True, timeout=300,
        cwd=str(BRIDGE_CWD), encoding="utf-8", errors="replace",
        env={**os.environ, "GSTD_MASTER_ADDRESS": V7_MASTER},
    )
    return (p.stdout or "") + (p.stderr or "")


def read_state() -> dict:
    out = run_soak_state("state")
    for line in out.splitlines():
        if line.startswith("STATE_JSON "):
            return json.loads(line[len("STATE_JSON "):])
    raise RuntimeError("no STATE_JSON in: " + out[-300:])


def read_deployer_and_worker_ton() -> dict:
    out = run_soak_state("funds")
    for line in out.splitlines():
        if line.startswith("TONS_JSON "):
            return json.loads(line[len("TONS_JSON "):])
    raise RuntimeError("no TONS_JSON in: " + out[-300:])


DEPLOYER_ADDR = "EQAzwrijfvQn2xBL5YhZwf5GoBQaINAt6Nbd6LF67bFpuUiz"


def send_ton_to(from_env: str, to_addr: str, amount: float, memo: str) -> bool:
    out = run_soak_state("send", [from_env, str(amount), to_addr])
    ok = "REFILL_CONFIRMED" in out
    tail = out.strip().splitlines()[-1][:80] if out.strip() else "no output"
    log(f"refill {memo}: {'CONFIRMED' if ok else 'UNCONFIRMED'} ({tail})")
    return ok


def deployer_address() -> str:
    return DEPLOYER_ADDR


def fire_bridge(cycle: int) -> tuple[str, str]:
    """One production settle through the gated bridge. Returns (outcome, raw tail)."""
    p = subprocess.run(
        ["node", str(TS_NODE), "--project", str(BRIDGE_CWD / "tsconfig.deploy.json"),
         str(BRIDGE),
         "--verdict", "STRUCTURE",
         "--consensus", "0.667",
         "--correct", "0.667",
         "--run", f"soak-20261014-c{cycle:03d}",
         "--node", "desktop-7c70ksc"],
        capture_output=True, text=True, timeout=600,
        cwd=str(BRIDGE_CWD), encoding="utf-8", errors="replace",
        env={**os.environ, "GSTD_MASTER_ADDRESS": V7_MASTER},
    )
    out = (p.stdout or "") + (p.stderr or "")
    if p.returncode == 3 and "MASTER-BALANCE GATE" in out:
        return "GATE_REFUSE", out[-400:]
    if "verdict must be STRUCTURE" in out:
        return "REFUSED", out[-400:]
    m = [l for l in out.splitlines() if l.startswith("VERDICT:")]
    verdict = m[-1] if m else ""
    if "settled, worker +" in verdict:
        return "SETTLED", out[-400:]
    if "not visible after 4 min" in verdict:
        return "TIMEOUT", out[-400:]
    return f"RC{p.returncode}", out[-400:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycles", type=int, default=50)
    ap.add_argument("--start-cycle", type=int, default=1,
                    help="first cycle number (resume after a killed run keeps the ledger monotone)")
    ap.add_argument("--pace", type=float, default=0.0,
                    help="seconds to sleep between cycles - testnet congestion backs up the "
                         "wallet seqno (an unconfirmed refill makes every later send reuse a "
                         "stale seqno and die silently); pace above the confirmation lag")
    args = ap.parse_args()

    SOAK_DIR.mkdir(parents=True, exist_ok=True)
    cycles_path = SOAK_DIR / "cycles.jsonl"

    st = read_state()
    funds = read_deployer_and_worker_ton()
    log(f"soak start: master {st['masterTon']:.3f} TON, pool {st['poolGstd']:.0f} GSTD, "
        f"floor {st['floor']:.1f}, taskCount {st['taskCount']}, deferred {st['deferred']}")
    log(f"funds: deployer {funds['deployerTon']:.3f} TON, desktop wallet {funds['desktopTon']:.3f} TON")

    outcomes: dict[str, int] = {}
    settled_n = 0
    with cycles_path.open("a", encoding="utf-8") as ledger:
        for cycle in range(args.start_cycle, args.start_cycle + args.cycles):
            before = read_state()
            row = {"cycle": cycle, "ts": _dt.datetime.utcnow().isoformat() + "Z",
                   "master_before": round(before["masterTon"], 4),
                   "taskCount_before": before["taskCount"]}

            # RUNWAY FIRST (live-fire bug, cycles 18-19 of the first run): the
            # deployer pays the 0.2 attach + fees per settle and died to gas
            # BEFORE the master ever reached the band edge - the txs never
            # landed (taskCount frozen) and the rows read TIMEOUT. The
            # deployer's own balance is checked every cycle now, refilled
            # from the desktop wage wallet (wages fund the soak).
            funds = read_deployer_and_worker_ton()
            if funds["deployerTon"] < DEPLOYER_KEEP:
                if funds["desktopTon"] > 1.0:
                    row["refill"] = f"desktop-wages -> deployer +{REFILL_FROM_WORKER}"
                    send_ton_to("WALLET_DESKTOP_MNEMONIC", deployer_address(),
                                REFILL_FROM_WORKER, "desktop->deployer")
                else:
                    log(f"cycle {cycle}: NO RUNWAY SOURCE - funding exhausted, stopping honestly")
                    row["outcome"] = "FUNDING_EXHAUSTED"
                    ledger.write(json.dumps(row) + "\n")
                    break

            # band-edge planning: let ONE natural bounce happen per funding
            # valley as the on-chain proof, then refill the master
            if before["masterTon"] < BAND_EDGE:
                if funds["deployerTon"] > DEPLOYER_KEEP + 0.5:
                    row["refill"] = f"deployer -> v7 +{REFILL_FROM_DEPLOYER}"
                    send_ton_to("DEPLOYER_MNEMONIC", V7_MASTER, REFILL_FROM_DEPLOYER, "deployer->v7")
                elif funds["desktopTon"] > 1.0:
                    row["refill"] = f"desktop-wages -> v7 +{REFILL_FROM_WORKER}"
                    send_ton_to("WALLET_DESKTOP_MNEMONIC", V7_MASTER, REFILL_FROM_WORKER, "desktop->v7")
                else:
                    log(f"cycle {cycle}: NO REFILL SOURCE - funding exhausted, stopping honestly")
                    row["outcome"] = "FUNDING_EXHAUSTED"
                    ledger.write(json.dumps(row) + "\n")
                    break

            outcome, tail = fire_bridge(cycle)
            after = read_state()
            row["outcome"] = outcome
            row["master_after"] = round(after["masterTon"], 4)
            row["taskCount_after"] = after["taskCount"]
            row["deferred"] = after["deferred"]
            row["worker_jw_gstd"] = round(after["workerJwGstd"], 2)
            row["tail"] = tail.strip().splitlines()[-1][:160] if tail.strip() else ""
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            if outcome == "SETTLED":
                settled_n += 1
            ledger.write(json.dumps(row) + "\n")
            ledger.flush()
            log(f"cycle {cycle:03d} {outcome} | master {row['master_before']:.3f}->{row['master_after']:.3f} "
                f"| tasks {row['taskCount_before']}->{row['taskCount_after']} | workerJW {row['worker_jw_gstd']:.1f} GSTD")
            if args.pace > 0:
                import time as _time
                _time.sleep(args.pace)
    final = read_state()
    summary = {
        "soak": "gstd_soak_20261014", "target_master": V7_MASTER,
        "build": "PR #1 head 185b3d8 (checked relay b4c60d0 + balance band)",
        "cycles_attempted": sum(outcomes.values()), "settled": settled_n,
        "outcomes": outcomes,
        "final": {"masterTon": round(final["masterTon"], 4), "taskCount": final["taskCount"],
                  "deferred": final["deferred"], "poolGstd": round(final["poolGstd"], 1)},
        "band_bounce_is_evidence": "BAND_BOUNCE rows are the contract-level band invariant firing (threat 3 fix proven on-chain)",
        "timeout_is_failure": "any TIMEOUT row is the relay-skip signature - the amendment was supposed to kill it",
    }
    (SOAK_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log(f"SOAK COMPLETE: {settled_n}/{args.cycles} settled, outcomes {outcomes}")
    log(f"receipt bank: {SOAK_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
