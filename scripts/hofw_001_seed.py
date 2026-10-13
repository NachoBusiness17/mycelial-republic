#!/usr/bin/env python3
# scripts/hofw_001_seed.py — driver for HOFW-001 seed build (robust paths)
import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "seat_fork.json"
RECEIPT_DIR = ROOT / "memory" / "runs" / "hermes_jobs"
BRIEF_DIR = ROOT / "memory" / "briefs"
RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
BRIEF_DIR.mkdir(parents=True, exist_ok=True)


def main():
    if not CONFIG.exists():
        print(f"ERROR: config not found at {CONFIG}", file=sys.stderr)
        sys.exit(1)

    config = json.loads(CONFIG.read_text())
    frozen_tip_hash = config["frozen_tip_hash"]
    persona = config["persona"]
    session_domain = config["session_domain"]
    wave_width = config.get("wave_width", 8)

    import hashlib
    payload = {
        "frozen_tip": frozen_tip_hash,
        "persona": persona,
        "session_domain": session_domain,
        "wave_width": wave_width,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    seat_branch_tip = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    seat_id = f"hofw_{session_domain}"
    brief_path = BRIEF_DIR / f"{seat_id}_brief.md"
    brief_path.write_text(
        f"# Seat Brief — {seat_id}\n"
        f"\n"
        f"- Forked from frozen tip: `{frozen_tip_hash}`\n"
        f"- Persona: `{persona}`\n"
        f"- Session domain: `{session_domain}`\n"
        f"- Wave width: {wave_width}\n"
        f"- Seat branch tip: `{seat_branch_tip}`\n"
        f"- Created: {payload['timestamp']}\n"
    )

    receipt = {
        "seat_id": seat_id,
        "frozen_tip_hash": frozen_tip_hash,
        "persona": persona,
        "session_domain": session_domain,
        "wave_width": wave_width,
        "seat_branch_tip": seat_branch_tip,
        "start_time": payload["timestamp"],
        "end_time": None,
        "artifact_hash": None,
        "status": "started"
    }
    receipt_path = RECEIPT_DIR / f"{seat_id}_receipt.jsonl"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")

    # Update start_time in-place
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")

    print(seat_branch_tip)
    print(f"Seat ID: {seat_id}")
    print(f"Frozen tip: {frozen_tip_hash}")
    print(f"Persona: {persona}")
    print(f"Wave width: {wave_width}")
    print(f"Receipt: {receipt_path}")
    print(f"Brief: {brief_path}")


if __name__ == "__main__":
    main()
