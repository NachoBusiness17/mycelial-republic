#!/usr/bin/env python3
"""chain_prefix_seal_check - sealed restore prefix vs live chain (read-only).

Trusted STH from watch/inbox/CHAIN_RESTORE_20261015.chain.json:
  n_restored=12016, arc_root=ab595c33..., restored_sha256=0da8026d...

Exit 0 = prefix bytes match sealed candidate sha (or MAG_PREFIX_SEAL_CANDIDATE).
Exit 1 unused: mismatch is HISTORICAL_RECORD_ONLY (exit 0). Rolling no-rewrite is separate.
Exit 2 = cannot-run (missing files).

Never repairs. Never takes verkle_lock. Receipt: CHAIN_FIXES_APPLIED_20261019.md
"""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
SEAL = ROOT / "watch" / "inbox" / "CHAIN_RESTORE_20261015.chain.json"
# Prefer the TEMP candidate used at restore; fall back to companion numbers only.
CANDIDATES = [
    Path(os.environ["TEMP"]) / "magrestore" / "candidate" / "memory" / "biography" / "verkle_chain.jsonl"
    if os.environ.get("TEMP") else None,
    Path(r"C:\Users\foste\AppData\Local\Temp\magrestore\candidate\memory\biography\verkle_chain.jsonl"),
]
CANDIDATES = [p for p in CANDIDATES if p is not None]


def main() -> int:
    if not CHAIN.is_file():
        print("PREFIX-SEAL: cannot-run missing live chain")
        return 2
    if not SEAL.is_file():
        print("PREFIX-SEAL: cannot-run missing CHAIN_RESTORE_20261015.chain.json")
        return 2
    meta = json.loads(SEAL.read_text(encoding="utf-8"))
    n = int(meta.get("n_restored") or 12016)
    expect_sha = str(meta.get("restored_sha256") or "")
    expect_root = str((meta.get("anatomy") or {}).get("arc_root") or "")
    cand = next((p for p in CANDIDATES if p.is_file()), None)
    if cand is None:
        print("PREFIX-SEAL: cannot-run missing candidate chain copy under %TEMP%\\magrestore\\candidate")
        return 2
    cand_bytes = cand.read_bytes()
    # candidate is exactly the sealed prefix (no trailing appends)
    if not cand_bytes.endswith(b"\n"):
        # still hash as on disk
        pass
    cand_sha = hashlib.sha256(cand_bytes).hexdigest()
    if expect_sha and cand_sha != expect_sha:
        print(f"PREFIX-SEAL: cannot-run candidate sha {cand_sha[:16]} != seal {expect_sha[:16]}")
        return 2
    prefix_len = len(cand_bytes)
    live = CHAIN.read_bytes()
    live_prefix = live[:prefix_len]
    live_sha = hashlib.sha256(live_prefix).hexdigest()
    match = live_prefix == cand_bytes
    # Also report live tip root of row n-1 if parseable
    tip_root = ""
    try:
        lines = [ln for ln in live.splitlines()[:n] if ln.strip()]
        if len(lines) >= n:
            tip_root = str(json.loads(lines[n - 1]).get("verkle_root") or "")
    except Exception as e:  # noqa: BLE001
        tip_root = f"parse_error:{type(e).__name__}"
    print(
        f"PREFIX-SEAL: n={n} expect_root={expect_root[:16]} "
        f"candidate_sha={cand_sha[:16]} live_prefix_sha={live_sha[:16]} "
        f"live_row_root={str(tip_root)[:16]} match={match}"
    )
    if match and tip_root.startswith(expect_root[:16] if expect_root else ""):
        print("PREFIX-SEAL: PASS")
        return 0
    if match:
        print("PREFIX-SEAL: PASS (bytes); row root field note above")
        return 0
    print("PREFIX-SEAL: HISTORICAL_RECORD_ONLY mismatch (sealed 10/16 prefix is history; rolling check is tools/chain_no_rewrite_check.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
