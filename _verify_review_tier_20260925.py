"""End-to-end verification of the trust_gate.v2 REVIEW tier (agent-memory-sota#0).

Backs up the live operator inbox + trust_gate state, exercises the REAL live paths,
asserts what the fold row requires, then restores everything byte-for-byte.
Scratch harness for watch/INGEST_REVIEW_TIER_20260925.md; safe to delete.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

INBOX = ROOT / "memory" / "operator_inbox.json"
GATE_DIR = ROOT / "memory" / "trust_gate"

backup_dir = Path(tempfile.mkdtemp(prefix="review_tier_backup_"))
shutil.copy2(INBOX, backup_dir / "operator_inbox.json")
shutil.copytree(GATE_DIR, backup_dir / "trust_gate")

try:
    from mag import trust_gate
    from mag import operator_inbox

    before = operator_inbox.status()

    # 1. REVIEW on the live path: trusted source + suspicious content
    r = trust_gate.gate("review tier live probe " + "pad " * 30, source="frontier", domain="verify")
    assert r["verdict"] == "REVIEW", f"expected REVIEW, got {r['verdict']}: {r['reason']}"
    assert r["trusted_source"] is True
    assert r["review"] and r["review"]["routed"] is True, f"advisory not routed: {r['review']}"
    after = operator_inbox.status()
    assert after["pending_n"] == before["pending_n"] + 1, \
        f"pending_n {before['pending_n']} -> {after['pending_n']}"
    latest = after["pending"][0] if after["pending"] else None
    assert latest and "trust_gate REVIEW" in (latest.get("text") or ""), str(latest)
    assert latest.get("source") == "trust_gate"
    print("LIVE REVIEW ROUTE OK:", json.dumps({"pending_n": after["pending_n"],
                                               "advisory_id": latest["id"],
                                               "trust_score": r["trust"]["score"]}))

    # 2. ACCEPT stamps trust_score into the live register
    r2 = trust_gate.gate("accept register probe with enough bytes to be grounded",
                         source="operator", domain="verify")
    assert r2["verdict"] == "ACCEPT", r2["reason"]
    seen = trust_gate._load_seen()
    entry = seen["seen"][r2["novelty"]["hash"]]
    assert "trust_score" in entry, entry
    print("REGISTER TRUST_SCORE OK:", json.dumps(entry))

    # 3. swarm_tools: a trusted-source REVIEW must gate the verkle write (fail-closed).
    #    owner="worker" -> source "swarm-worker" (rep 0.6 = trusted); repeated token -> poison flag.
    from mag import swarm_tools
    w = swarm_tools.verkle_write(summary="probe probe probe probe " * 5,
                                 owner="worker", theme="verify")
    assert (not w.get("ok")) and w.get("gated") == "REVIEW", f"verkle_write not REVIEW-gated: {w}"
    print("SWARM TOOLS GATE OK:", json.dumps({k: w.get(k) for k in ("ok", "gated", "reason")}))
finally:
    shutil.copy2(backup_dir / "operator_inbox.json", INBOX)
    shutil.rmtree(GATE_DIR)
    shutil.copytree(backup_dir / "trust_gate", GATE_DIR)
    shutil.rmtree(backup_dir)
    print("live state restored")
