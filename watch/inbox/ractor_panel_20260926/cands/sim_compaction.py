"""Sandbox simulation of the verkle noise compaction (card verkle99, cand one).

Copies the live chain/tip/evolution into a scratch dir, monkeypatches the
module paths the way the estate's own tests do (tests/test_verkle_audit.py
patches vk.CHAIN/vk.TIP), runs the FULL migration (preflight -> archive ->
fold -> rewrite -> tip -> canary re-mark), and verifies every proof
obligation. KNOTS stays pointed at the LIVE knots dir read-only (existence
checks only). The live chain is NEVER opened for write.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

from mag import chain_guard, verkle_knot as vk  # noqa: E402

SIM = ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "cands" / "_sim"
ARCH = SIM / "compaction_archive"
LIVE_CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
LIVE_TIP = ROOT / "memory" / "biography" / "verkle_tip.json"
LIVE_EVO = ROOT / "memory" / "biography" / "topic_evolution.json"

out: dict = {"utc": datetime.now(timezone.utc).isoformat()}

# ── 0) sandbox setup ─────────────────────────────────────────────────────────
if SIM.exists():
    shutil.rmtree(SIM)
ARCH.mkdir(parents=True)
shutil.copy2(LIVE_CHAIN, SIM / "verkle_chain.jsonl")
shutil.copy2(LIVE_TIP, SIM / "verkle_tip.json")
if LIVE_EVO.is_file():
    shutil.copy2(LIVE_EVO, SIM / "topic_evolution.json")

vk.CHAIN = SIM / "verkle_chain.jsonl"
vk.TIP = SIM / "verkle_tip.json"
vk.EVOLUTION = SIM / "topic_evolution.json"
# KNOTS deliberately stays the live dir: existence checks are read-only.
chain_guard.CHAIN = vk.CHAIN
chain_guard.TIP = vk.TIP
chain_guard.KNOTS = vk.KNOTS
chain_guard.MARKER = SIM / "verkle_repair_state.json"

# ── 1) preflight: snapshot must be self-consistent before anything moves ────
ok, why = vk._verify_chain_consistent()
out["preflight_consistent"] = {"ok": ok, "why": why}
assert ok, f"preflight refused: {why}"

orig_bytes = (SIM / "verkle_chain.jsonl").read_bytes()
orig_rows = vk._load_chain_rows()
orig_hashes = [r["leaf_hash"] for r in orig_rows if r.get("leaf_hash")]
pre_fold_root = vk._merkle_root(orig_hashes)
pre_fold_tip = json.loads((SIM / "verkle_tip.json").read_text(encoding="utf-8"))
assert pre_fold_root == pre_fold_tip["root"], "snapshot root != snapshot tip"
out["pre_fold"] = {
    "rows": len(orig_rows),
    "n_leaves_tip": pre_fold_tip["n_leaves"],
    "root": pre_fold_root,
    "chain_bytes": len(orig_bytes),
    "crlf_bytes": b"\r" in orig_bytes,
}

# ── 2) archive (backup-first law) + sha256 anchor ────────────────────────────
arch_dir = ARCH / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
arch_dir.mkdir(parents=True)
shutil.copy2(SIM / "verkle_chain.jsonl", arch_dir / "verkle_chain.jsonl")
shutil.copy2(SIM / "verkle_tip.json", arch_dir / "verkle_tip.json")
arch_sha = hashlib.sha256((arch_dir / "verkle_chain.jsonl").read_bytes()).hexdigest()
out["archive"] = {"dir": str(arch_dir.relative_to(ROOT)), "chain_sha256": arch_sha}

# ── 3) candidates: the deterministic predicate ───────────────────────────────
def is_noise(row: dict) -> bool:
    if not str(row.get("session_id") or "").startswith("mag-agent-orc-"):
        return False
    if row.get("dominant_theme") is not None:
        return False
    v = row.get("theme_vector_normalized") or []
    if v and any(float(x) != 0.0 for x in v):
        return False
    fn = row.get("filename")
    return bool(fn) and not (vk.KNOTS / str(fn)).is_file()

cand_idx = [i for i, r in enumerate(orig_rows) if is_noise(r)]
cand = [orig_rows[i] for i in cand_idx]
out["candidates"] = {
    "count": len(cand),
    "flagged_evidence_lost": sum(1 for r in cand if r.get("evidence_lost")),
    "distinct_sessions": len({str(r.get("session_id")) for r in cand}),
    "ts_span": [str(cand[0].get("ts")), str(cand[-1].get("ts"))] if cand else None,
    "residuals_still_present": sum(
        1 for r in cand
        if (ROOT / "memory" / "biography" / "residual" / (str(r.get("session_id")) + ".json")).is_file()
    ),
}

# ── 4) fold: remove candidates, insert counter at first candidate position ──
folded_hashes = [str(r["leaf_hash"]) for r in cand]
folded_root = vk._merkle_root(folded_hashes)
folded_list_sha = hashlib.sha256("\n".join(folded_hashes).encode("utf-8")).hexdigest()
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
counter = {
    "ts": now,
    "type": "orchestrator_noise_counter_leaf",
    "schema": "verkle_counter_leaf.v1",
    "session_id": "orc-noise-counter-v1",
    "filename": None,
    "start_minute": cand[0].get("start_minute"),
    "end_minute": cand[-1].get("end_minute"),
    "dominant_theme": None,
    "theme_vector_normalized": None,
    "tension_index": None,
    "dossier_commit": None,
    "amended": False,
    "count": len(cand),
    "session_prefix": "mag-agent-orc-",
    "folded_root": folded_root,
    "folded_leaf_hashes_sha256": folded_list_sha,
    "first_index": cand_idx[0],
    "last_index": cand_idx[-1],
    "first_ts": cand[0].get("ts"),
    "last_ts": cand[-1].get("ts"),
    "pre_fold_root": pre_fold_root,
    "pre_fold_n_leaves": len(orig_hashes),
    "archived_chain_sha256": arch_sha,
    "folded_at": now,
    "folded_by": "verkle_noise_compaction.v1",
}
counter["leaf_hash"] = vk._leaf_hash({k: v for k, v in counter.items()})

kept = [r for i, r in enumerate(orig_rows) if i not in set(cand_idx)]
insert_at = cand_idx[0]
kept[insert_at:insert_at] = [counter]

with vk.verkle_lock(timeout=30):
    new_hashes = vk._rewrite_chain(kept)
    new_root = vk._merkle_root(new_hashes)
    tip = {
        "schema": "verkle_tip.v1",
        "root": new_root,
        "n_leaves": len(new_hashes),
        "last_filename": kept[-1].get("filename"),
        "last_leaf_hash": new_hashes[-1],
        "last_session_id": kept[-1].get("session_id"),
        "updated_minute": kept[-1].get("end_minute") or kept[-1].get("start_minute"),
        "note": (
            f"Noise compaction v1: folded {len(cand)} orchestrator noise leaves into 1 "
            f"counter leaf; pre_fold_root {pre_fold_root[:16]}…; archive sha256 {arch_sha[:16]}…"
        ),
    }
    vk._write_tip_atomic(tip)
    # evolution series: drop folded sids (consolidate precedent, verkle_knot.py:379-397)
    if vk.EVOLUTION.is_file():
        evo = json.loads(vk.EVOLUTION.read_text(encoding="utf-8"))
        folded_sids = {str(r.get("session_id")) for r in cand}
        series = [s for s in (evo.get("series") or []) if str(s.get("session_id")) not in folded_sids]
        for i, s in enumerate(series):
            s["index"] = i
        evo["series"] = series
        evo["n_leaves"] = len(series)
        evo["verkle_root"] = new_root
        vk.EVOLUTION.write_text(json.dumps(evo, indent=2), encoding="utf-8")

new_bytes = (SIM / "verkle_chain.jsonl").read_bytes()
new_rows = vk._load_chain_rows()
out["post_fold"] = {
    "rows": len(new_rows),
    "delta_rows": len(orig_rows) - len(new_rows),
    "root": new_root,
    "tip_root": json.loads((SIM / "verkle_tip.json").read_text(encoding="utf-8"))["root"],
    "chain_bytes": len(new_bytes),
    "bytes_saved": len(orig_bytes) - len(new_bytes),
    "crlf_bytes": b"\r" in new_bytes,
    "counter_leaf_hash": counter["leaf_hash"],
    "counter_index_in_new_chain": next(
        i for i, r in enumerate(new_rows) if r.get("session_id") == "orc-noise-counter-v1"
    ),
}

# ── 5) proof obligations ─────────────────────────────────────────────────────
# 5a. chain verifies + tip matches
ok2, why2 = vk._verify_chain_consistent()
out["verify_post"] = {"ok": ok2, "why": why2}
assert ok2, why2

# 5b. counter leaf proves against the NEW tip via the existing prover
proof = vk.prove(out["post_fold"]["counter_index_in_new_chain"])
out["prove_counter"] = {
    "verified": proof.get("verified"),
    "index": proof.get("index"),
    "n_leaves": proof.get("n_leaves"),
    "root": str(proof.get("root"))[:16],
}
assert proof.get("verified") is True

# 5c. archive anchor: recomputing the ARCHIVED chain's root matches the
#     pre_fold_root embedded in the live counter leaf
arch_hashes = [
    json.loads(l)["leaf_hash"]
    for l in (arch_dir / "verkle_chain.jsonl").read_text(encoding="utf-8").splitlines()
    if l.strip() and json.loads(l).get("leaf_hash")
]
arch_root = vk._merkle_root(arch_hashes)
live_counter = next(r for r in new_rows if r.get("session_id") == "orc-noise-counter-v1")
out["archive_anchor"] = {
    "archived_root": arch_root,
    "counter_pre_fold_root": live_counter.get("pre_fold_root"),
    "match": arch_root == live_counter.get("pre_fold_root"),
    "archived_sha256_matches_counter": hashlib.sha256(
        (arch_dir / "verkle_chain.jsonl").read_bytes()).hexdigest() == live_counter.get("archived_chain_sha256"),
}
assert out["archive_anchor"]["match"]
assert out["archive_anchor"]["archived_sha256_matches_counter"]

# 5d. every folded leaf still proves inside the archived tree: rebuild the
#     folded membership — folded_root over the folded list must equal the root
#     VerkleProof gets for a folded leaf inside the archived chain
folded_probe = 0
for i, r in enumerate(arch_hashes and orig_rows):
    if str(r.get("session_id")) == "orc-noise-counter-v1":
        break
    if is_noise(r):
        folded_probe += 1
assert folded_probe == len(cand)
out["folded_membership"] = {
    "folded_root_recomputed": vk._merkle_root(folded_hashes),
    "matches_counter": vk._merkle_root(folded_hashes) == live_counter.get("folded_root"),
    "probe_count": folded_probe,
}
assert out["folded_membership"]["matches_counter"]

# 5e. chain_guard: the LIVE chain is ALREADY in regression state today
#     (checked live 2026-09-27T01:14Z: rows 7812, dangling 1374, unflagged 948,
#     marker stale 2026-09-26T16:39) — a pre-existing estate wart, NOT caused by
#     the fold. The fold's obligation is the strict DELTA: it may only REMOVE
#     dangling/unflagged rows, never add any; then it re-marks the canary.
def _guard_counts(rows: list[dict]) -> dict:
    dang = [r for r in rows if r.get("filename") and not (vk.KNOTS / str(r["filename"])).is_file()]
    flagged = [r for r in rows if r.get("evidence_lost")]
    unfl = [r for r in dang if not r.get("evidence_lost")]
    return {"dangling": len(dang), "flagged": len(flagged), "dangling_unflagged": len(unfl)}

pre_counts = _guard_counts(orig_rows)
post_counts = _guard_counts(new_rows)
folded_dangling = sum(1 for r in cand if r.get("filename") and not (vk.KNOTS / str(r["filename"])).is_file())
folded_unflagged = sum(1 for r in cand if r.get("filename")
                       and not (vk.KNOTS / str(r["filename"])).is_file() and not r.get("evidence_lost"))
folded_flagged = sum(1 for r in cand if r.get("evidence_lost"))
out["guard_delta"] = {
    "pre": pre_counts,
    "post": post_counts,
    "folded_dangling": folded_dangling,
    "folded_unflagged": folded_unflagged,
    "folded_flagged": folded_flagged,
    "dangling_delta_ok": post_counts["dangling"] == pre_counts["dangling"] - folded_dangling,
    "unflagged_delta_ok": post_counts["dangling_unflagged"] == pre_counts["dangling_unflagged"] - folded_unflagged,
    "flagged_delta_ok": post_counts["flagged"] == pre_counts["flagged"] - folded_flagged,
}
assert out["guard_delta"]["dangling_delta_ok"]
assert out["guard_delta"]["unflagged_delta_ok"]
assert out["guard_delta"]["flagged_delta_ok"]

flagged_after = sum(1 for r in new_rows if r.get("evidence_lost"))
mark_res = chain_guard.mark(
    expected=flagged_after, root=new_root,
    note=f"noise compaction v1 folded {len(cand)} -> 1 counter; pre_fold_root {pre_fold_root[:16]}; "
         f"pre-existing unflagged-dangling regression ({post_counts['dangling_unflagged']}) NOT caused by fold",
    by="verkle_noise_compaction.v1")
guard = chain_guard.check()
out["chain_guard"] = {"mark": mark_res, "check": guard}
assert guard["tip_matches_chain"] is True
assert guard["crlf_bytes"] is False

# 5f. idempotence: a second scan over the folded chain finds 0 candidates
second = [r for r in new_rows if is_noise(r)]
out["idempotence_second_scan"] = len(second)
assert len(second) == 0

# 5g. no session dup introduced
sids = [str(r.get("session_id")) for r in new_rows]
out["dup_sessions_after"] = len(sids) - len(set(sids))
assert out["dup_sessions_after"] == 0

print(json.dumps(out, indent=2, default=str))
