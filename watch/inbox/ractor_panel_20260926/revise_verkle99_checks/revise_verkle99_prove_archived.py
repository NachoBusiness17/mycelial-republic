"""verkle99 revision, bullet 1: prove() at ARCHIVED folded indexes against the
archived pre-fold chain, at live scale, through the LANDED module.

Copies the live chain/tip/evolution into a scratch sandbox (live files never
opened for write), monkeypatches module paths the way the estate's own tests
do, runs mag.verkle_compaction.apply(execute=True) (the real migration), then
runs prove_archived_leaf at the FIRST, a MIDDLE, and the LAST folded index.
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

from mag import chain_guard, verkle_compaction as vc  # noqa: E402
from mag import verkle_knot as vk  # noqa: E402

SIM = ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "revise_verkle99_checks" / "_sandbox"
LIVE = ROOT / "memory" / "biography"

if SIM.exists():
    shutil.rmtree(SIM)
SIM.mkdir(parents=True)
shutil.copy2(LIVE / "verkle_chain.jsonl", SIM / "verkle_chain.jsonl")
shutil.copy2(LIVE / "verkle_tip.json", SIM / "verkle_tip.json")
if (LIVE / "topic_evolution.json").is_file():
    shutil.copy2(LIVE / "topic_evolution.json", SIM / "topic_evolution.json")

vk.CHAIN = SIM / "verkle_chain.jsonl"
vk.TIP = SIM / "verkle_tip.json"
vk.EVOLUTION = SIM / "topic_evolution.json"
vk.LOCK = SIM / ".verkle.lock"
# KNOTS deliberately stays the LIVE dir: knot existence checks are read-only
chain_guard.CHAIN = vk.CHAIN
chain_guard.TIP = vk.TIP
chain_guard.KNOTS = vk.KNOTS
chain_guard.MARKER = SIM / "verkle_repair_state.json"

out: dict = {"utc": datetime.now(timezone.utc).isoformat()}

res = vc.apply(execute=True)
out["apply"] = {k: res.get(k) for k in (
    "ok", "changed", "folded", "kept_rows", "pre_fold_root", "new_root",
    "counter_leaf_hash", "counter_index", "archive_dir", "archived_chain_sha256")}
out["prove_counter"] = res.get("prove_counter")
out["archive_anchor"] = res.get("archive_anchor")
assert res["ok"] is True, res
assert res["changed"] is True

# the folded ORIGINAL indexes come from the IN-LOCK scan apply committed into
# its result (the live knots dir drifts: a knot file can vanish while amends
# run, so a post-lock re-derivation can disagree by a row — reported below,
# never asserted equal)
arch_rows = [json.loads(l) for l in
             (Path(res["archive_dir"]) / "verkle_chain.jsonl").read_text(encoding="utf-8").splitlines()
             if l.strip()]
folded_idx = res["folded_indexes"]
assert len(folded_idx) == res["folded"]
out["drift_note"] = {
    "re_derived_candidates_at_read_time": sum(1 for r in arch_rows if vc.is_fold_candidate(r)),
    "in_lock_folded": res["folded"],
    "cause": "live knot-dir drift while the chain amends (superseded knot files are deleted); the proofs below use the in-lock committed indexes",
}

# THE CHECK THE JUDGE NAMED: actual prove() at archived folded indexes,
# first + middle + last, against the archived pre-fold chain
picks = {
    "first": folded_idx[0],
    "middle": folded_idx[len(folded_idx) // 2],
    "last": folded_idx[-1],
}
out["archived_proofs"] = {}
for name, idx in picks.items():
    p = vc.prove_archived_leaf(Path(res["archive_dir"]), idx)
    out["archived_proofs"][name] = p
    assert p["ok"] is True and p["verified"] is True, (name, p)
    assert p["root_matches_archive"] is True
    assert p["proof_root"] == res["pre_fold_root"]

# and the live counter's folded witness commits exactly the proven set
counter = next(r for r in vk._load_chain_rows() if r.get("session_id") == vc.COUNTER_SESSION_ID)
folded_hashes = [str(arch_rows[i]["leaf_hash"]) for i in folded_idx]
out["witness"] = {
    "counter_folded_root": counter.get("folded_root"),
    "recomputed_folded_root": vk._merkle_root(folded_hashes),
    "match": counter.get("folded_root") == vk._merkle_root(folded_hashes),
    "counter_folded_leaf_hashes_sha256": counter.get("folded_leaf_hashes_sha256"),
    "recomputed_sha": hashlib.sha256("\n".join(folded_hashes).encode("utf-8")).hexdigest(),
    "proven_leaf_in_folded_set": {
        name: arch_rows[idx]["leaf_hash"] in folded_hashes for name, idx in picks.items()},
}
assert out["witness"]["match"]
assert out["witness"]["counter_folded_leaf_hashes_sha256"] == out["witness"]["recomputed_sha"]

# idempotence on the sandbox
res2 = vc.apply(execute=True)
out["second_apply"] = {k: res2.get(k) for k in ("ok", "changed", "reason", "n_rows")}
assert res2["changed"] is False

print(json.dumps(out, indent=2, default=str))
