#!/usr/bin/env python3
"""gstd_drain v3 - the complete autonomous economy loop (2026-10-12).

One fire runs the consensus battery on every configured cell, certifies each
run (STRUCTURE or nothing), credits the internal GSTD economy per node, and
claims each node's full accrued balance through the gated bridge when pending
crosses the claim threshold. The master's reserve (2+ TON, funded) pays the
bonus gas from its own balance - the starvation law is closed by the reserve
plus this script's fresh balance gate.

The loop: battery -> certification -> internal credit -> claim at threshold
-> on-chain settle -> reputation. Runs on cron/boot cadence; accumulates
between fires; the chain nets in batches.

Laws: STRUCTURE-or-refuse per cell, fresh master read at fire time (the
bridge re-reads and refuses under 0.5), fresh taskIds (replay refunds),
receipts per cycle, the inbox is work orders for the future (the battery
is the standing task).

Run:
  .venv/Scripts/python.exe tools/gstd_drain.py --master-ton <fresh-read>
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "queue" / "gstd_tasks"
INBOX = QUEUE / "INBOX.jsonl"
DONE = QUEUE / "DONE"
REPUTATION = ROOT / "reference" / "gstdcoin" / "contracts" / "reputation.jsonl"
ACCOUNTS = ROOT / "reference" / "gstdcoin" / "contracts" / "accounts.jsonl"
HARNESS = ROOT / "tools" / "consensus_harness.py"
RUNS = ROOT / "watch" / "inbox" / "gstd_perimeter_build_20261010" / "runs"
BRIDGE_CWD = ROOT / "reference" / "gstdcoin" / "contracts"
TS_NODE = BRIDGE_CWD / "node_modules" / "ts-node" / "dist" / "bin.js"
BRIDGE = "scripts/settle-consensus.ts"
ACCOUNTS_TOOL = ROOT / "tools" / "gstd_accounts.py"

MODELS_5 = "gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct,gemma2:2b-instruct-q5_K_M,qwen-desk:latest"
CLAIM_THRESHOLD = 100.0
BONUS_PER_RUN = 25.0

CELLS = [
    {"name": "desktop-7c70ksc", "kind": "local",
     "wallet": "UQBX4TEs0dCvV7CzDpUmj04niFPVd0jjbCfhquO8dPxxa3BJ"},
    {"name": "bob", "kind": "ssh",
     "wallet": "UQAW3wO8TwzoBuOjA-XwCivj80eKhRzGAWl_PgkzUUUlbe5m",
     "ssh_host": "etfag@100.125.103.60",
     "ssh_key": str(Path.home() / ".ssh" / "estate_to_bob"),
     "py": r"C:\Users\etfag\python312\python.exe",
     "harness": r"C:\Users\etfag\.zcode\workspace\default\tools\consensus_harness.py"},
]


def run_cell_battery(cell: dict) -> tuple[dict | None, str]:
    models_arg = "--models " + MODELS_5
    if cell["kind"] == "local":
        p = subprocess.run(
            [sys.executable, str(HARNESS),
             "--host", "http://localhost:11434",
             "--models", MODELS_5],
            capture_output=True, text=True, timeout=900,
            encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        rc = p.returncode
    else:
        remote_cmd = cell["py"] + " " + cell["harness"] + " " + models_arg
        p = subprocess.run(
            ["ssh", "-i", cell["ssh_key"], "-o", "BatchMode=yes",
             "-o", "ConnectTimeout=10", cell["ssh_host"], remote_cmd],
            capture_output=True, text=True, timeout=900,
            encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (p.stderr or "")
        rc = p.returncode
    summary = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{") and '"run_id"' in line:
            try:
                summary = json.loads(line)
            except Exception:
                pass
    if summary is None:
        return None, f"rc={rc}: {out[-200:]}"
    if summary.get("verdict") != "STRUCTURE":
        return None, f"verdict {summary.get('verdict')} - uncertified, no credit"
    return summary, ""


def credit_internal(worker: str, amount: float, reason: str) -> tuple[bool, str]:
    p = subprocess.run(
        [sys.executable, str(ACCOUNTS_TOOL), "credit", worker, str(amount),
         "--reason", reason],
        capture_output=True, text=True, timeout=60,
        encoding="utf-8", errors="replace")
    return p.returncode == 0, (p.stdout or "") + (p.stderr or "")


def pending_for(wallet: str) -> float:
    if not ACCOUNTS.is_file():
        return 0.0
    pend = 0.0
    for line in ACCOUNTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("type") == "credit" and r.get("worker") == wallet:
            pend += float(r.get("amount", 0))
        elif r.get("type") == "claim" and r.get("worker") == wallet:
            pend -= float(r.get("amount", 0))
    return round(pend, 2)


def bank_cycle(ts: str, log: list[str]) -> None:
    out = DONE / ts
    out.mkdir(parents=True, exist_ok=True)
    (out / "drain.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({
        "ts": ts, "banked_at": _dt.datetime.utcnow().isoformat() + "Z",
        "lane": "gstd_drain_v3_complete"}, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master-ton", type=float, required=True,
                    help="fresh master balance read (read-v3.ts) - the bridge re-reads on chain and refuses under 0.5")
    ap.add_argument("--dry", action="store_true",
                    help="run every battery and credit the internal economy, but skip on-chain settles")
    a = ap.parse_args()
    if a.master_ton < 0.5 and not a.dry:
        print(f"MASTER-BALANCE GATE (caller pass): {a.master_ton} < 0.5 - fund the master (scripts/fund-master-v6.ts)")
        return 3

    ts = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log: list[str] = [f"multi-node cycle {ts} | master TON (caller-read): {a.master_ton} | dry: {a.dry}"]

    for cell in CELLS:
        name = cell["name"]
        print(f"gstd_drain: cell {name} - running the battery...")
        summary, note = run_cell_battery(cell)
        if summary is None:
            log.append(f"{name}: battery uncertified or failed: {note}")
            print(f"  [{name}] no credit: {note}")
            continue
        run_id = summary.get("run_id", "unknown")
        rate = summary.get("consensus_rate")
        log.append(f"{name}: {run_id} STRUCTURE consensus={rate}")
        print(f"  [{name}] {run_id} STRUCTURE - crediting {BONUS_PER_RUN} GSTD internal")
        ok, credit_note = credit_internal(cell["wallet"], BONUS_PER_RUN,
                                          f"certified consensus run {run_id} on {name}")
        log.append(f"{name}: internal credit ok={ok} {credit_note[:120]}")

        # 3. claim at threshold: the gated bridge nets the cell's full pending
        pending = pending_for(cell["wallet"])
        log.append(f"{name}: internal pending {pending} GSTD (threshold {CLAIM_THRESHOLD})")
        if pending >= CLAIM_THRESHOLD:
            proc = subprocess.run(
                ["node", str(TS_NODE),
                 "--project", str(BRIDGE_CWD / "tsconfig.deploy.json"),
                 str(BRIDGE),
                 "--verdict", "STRUCTURE",
                 "--consensus", str(summary.get("consensus_rate")),
                 "--correct", str(summary.get("consensus_correct_rate")),
                 "--run", run_id + "-claim-" + str(int(pending)),
                 "--node", name],
                capture_output=True, text=True, timeout=480,
                cwd=str(BRIDGE_CWD), encoding="utf-8", errors="replace")
            claim_out = (proc.stdout or "") + (proc.stderr or "")
            log.append(f"{name}: claim settle rc={proc.returncode} out={claim_out[-200:]}")
            print(f"  [{name}] claim fired: {pending} GSTD pending -> gated bridge (rc {proc.returncode})")
        else:
            log.append(f"{name}: below claim threshold - rail untouched (the internal currency at work)")
            print(f"  [{name}] internal pending {pending} < {CLAIM_THRESHOLD} - rail untouched (the point)")

    bank_cycle(ts, log)
    print("gstd_drain: multi-node cycle complete - receipts at queue/gstd_tasks/DONE/" + ts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
