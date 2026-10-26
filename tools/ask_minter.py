"""ask_minter - mints free-lane asks from the estate's standing backlogs.

The feed organ for the 2,000-asks-a-day doctrine (the miner is the clock,
this is the feeder). Sources:
  explore   - one FOLD ask per unexplored row in memory/percolator/explore.jsonl
  sessions  - one FOLD ask per session rollout in corpus/oral_history/seat_pools
Every minted ask rotates across the free model families (rotation is the
norm - endpoints are perishable) and carries the identical-contract
discipline: the contract demands fold-to-nuance, SPECULATIVE marking, no
em-dashes. Daily budget is enforced by counting today's already-fired rows
in the usage ledger.

Usage:
  python tools/ask_minter.py --source explore --limit 50
  python tools/ask_minter.py --source sessions --start 0 --limit 10
  python tools/ask_minter.py --budget-today 500
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDE = ROOT / "queue" / "hermes_247_free_wide"
EXPLORE = ROOT / "memory" / "percolator" / "explore.jsonl"
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
POOLS = ROOT / "corpus" / "oral_history" / "seat_pools"

FAMILIES = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "dots-studio/dots-3-note-preview:free",
]
# PARKED 2026-10-17 with data: liquid/lfm-2.5 (22x 400-class - 2.6B model,
# stacked contract likely exceeds its context) and thinkingmachines/lab-1
# (20x 400-class - provider rejects the stacked body shape). Re-admit only
# with a per-family adapter or a shortened stack. See the morning digest.

FOLD_CONTRACT = ("FOLD THIS SIGNAL (plain text, no em-dashes, under 150 words): the row "
                 "below is a signal an estate captured. Answer three things only: "
                 "(1) TRUE-TODAY: is this signal still true given everything else you know "
                 "in the row's context - yes/no/unknown with one line of why; "
                 "(2) THE ORGAN: which kind of organ should own this signal (a law, a clock, "
                 "a gate, a memory row, or compost); "
                 "(3) THE FALSIFIER: the observation that would prove the signal wrong. "
                 "Mark unknowns UNKNOWN; do not pad.")


def fired_today() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    n = 0
    if USAGE.is_file():
        for line in USAGE.read_text(encoding="utf-8", errors="replace").splitlines():
            if today in line and "H247_" in line:
                n += 1
    return n


def mint(mid: str, model: str, contract: str, evidence: list[str]) -> None:
    d = WIDE / mid
    d.mkdir(parents=True, exist_ok=True)
    (d / "ask.json").write_text(json.dumps({
        "id": mid, "model": model, "max_tokens": 1200,
        "contract": contract, "evidence": evidence,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["explore", "sessions"], required=True)
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--budget-today", type=int, default=0,
                    help="skip minting if today's fired count already >= this")
    ap.add_argument("--stack", type=int, default=1,
                    help="group N backlog rows per stacked ask (1 = one row per ask)")
    args = ap.parse_args()

    if args.budget_today and fired_today() >= args.budget_today:
        print(f"budget reached: {fired_today()} fired today >= {args.budget_today}")
        return 0

    WIDE.mkdir(parents=True, exist_ok=True)
    minted = 0
    idx = args.start
    fam_i = 0

    if args.source == "explore":
        # Auto-advance past landed or staged asks when start is 0
        if args.start == 0:
            highest = -1
            out_burn = ROOT / "watch" / "inbox" / "hermes_burn"
            if out_burn.is_dir():
                for p in out_burn.glob("H247_FOLD_E*.md"):
                    try:
                        highest = max(highest, int(p.stem.split("_E")[-1]))
                    except ValueError:
                        pass
            for p in WIDE.glob("H247_FOLD_E*"):
                try:
                    highest = max(highest, int(p.name.split("_E")[-1]))
                except ValueError:
                    pass
            for w in WIDE.glob("_worker*"):
                if w.is_dir():
                    for p in w.glob("H247_FOLD_E*"):
                        try:
                            highest = max(highest, int(p.name.split("_E")[-1]))
                        except ValueError:
                            pass
            if highest >= 0:
                args.start = highest + 1
                idx = args.start

        rows = [json.loads(l) for l in EXPLORE.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        backlog = [r for r in rows if r.get("status") not in ("explored", "done")][args.start:]
        stack_n = max(1, args.stack)
        groups = [backlog[i:i + stack_n] for i in range(0, len(backlog), stack_n)]
        for g_idx, group in enumerate(groups):
            if minted >= args.limit:
                break
            sigs = []
            for k, r in enumerate(group, 1):
                sig = (r.get("signal") or "").strip()
                if len(sig) >= 40:
                    sigs.append(f"[{k}] CAPTURED {(r.get('ts') or '?')[:10]}: {sig}")
            if not sigs:
                idx += 1
                continue
            if stack_n == 1:
                clean_sig = sigs[0].split(": ", 1)[-1].replace("—", "--").replace("–", "-")
                contract = FOLD_CONTRACT + "\n\nSIGNAL: " + clean_sig
                mid = f"H247_FOLD_E{idx:05d}"
            else:
                contract = ("STACKED FOLD - " + str(len(sigs)) + " signals, one line each, "
                            "numbered to match. For EACH signal answer the three things only: "
                            "(1) TRUE-TODAY yes/no/unknown + one line; (2) THE ORGAN (law, clock, "
                            "gate, memory row, or compost); (3) THE FALSIFIER. No padding, no "
                            "preamble, numbered output. No em-dashes.\n\n" + "\n\n".join(sigs))
                mid = f"H247_STACK_E{idx:05d}_w{stack_n}"
            mint(mid, FAMILIES[fam_i % len(FAMILIES)], contract, ["memory/percolator/explore.jsonl"])
            fam_i += 1
            minted += 1
            idx += len(group)

    elif args.source == "sessions":
        sessions = sorted(POOLS.rglob("*.jsonl"))[args.start:]
        for s in sessions:
            if minted >= args.limit:
                break
            rel = s.relative_to(ROOT).as_posix()
            contract = (FOLD_CONTRACT + "\n\nThis signal row is a SESSION ROLLOUT of a "
                        "worker seat. Fold the session: (1) TRUE-TODAY, (2) THE ORGAN, "
                        "(3) THE FALSIFIER - about the session's work as a whole.")
            mid = f"H247_FOLD_S{args.start + minted:05d}"
            mint(mid, FAMILIES[fam_i % len(FAMILIES)], contract,
                 [rel, "memory/percolator/explore.jsonl"])
            fam_i += 1
            minted += 1

    print(f"minted {minted} asks into {WIDE.name} (source={args.source})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
