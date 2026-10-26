"""verkle99 revision, bullet 3: behavioral test of DIRECT chain-row consumers
on the post-fold sandbox chain (counter row present), vs the pre-fold archive.

Survey base (grep, production code only): every module that opens
verkle_chain.jsonl or calls vk._load_chain_rows — agent_cli, boot_check,
cache_map, chain_guard, chain_query, data_refinery, divergence_meter,
gene_pool_feeder (via aud_verkles.json), hermes_warm_boot, holographic_q,
hour_test, knot_at_close, lattice_dashboard, training_packager, usage_digest,
verkle_audit, verkle_lance, verkle_rib, voice_self, witness_snapshot,
worldline_dungeon, worldline_seed. Tip-only readers (hermes_warm_boot,
divergence_meter, witness_snapshot, verkle_rib, voice_self, worldline_*,
agent_cli) read the tip JSON, not row shapes. Row-shape readers are tested
below; tapestry is registry-fed (proven by run), gene_pool_feeder is
aud_verkles-fed (not the chain).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

from mag import chain_query, knot_at_close, verkle_knot as vk  # noqa: E402

CHECKS = ROOT / "watch" / "inbox" / "ractor_panel_20260926" / "revise_verkle99_checks"
SIM = CHECKS / "_sandbox"
arch_dirs = sorted((SIM / "compaction_archive").iterdir())
ARCH = arch_dirs[-1]
POST = SIM / "verkle_chain.jsonl"
PRE = ARCH / "verkle_chain.jsonl"

out: dict = {"utc": datetime.now(timezone.utc).isoformat(),
             "pre_fold_rows": sum(1 for l in PRE.read_text(encoding="utf-8").splitlines() if l.strip()),
             "post_fold_rows": sum(1 for l in POST.read_text(encoding="utf-8").splitlines() if l.strip())}

post_rows = [json.loads(l) for l in POST.read_text(encoding="utf-8").splitlines() if l.strip()]
pre_rows = [json.loads(l) for l in PRE.read_text(encoding="utf-8").splitlines() if l.strip()]
counter = next(r for r in post_rows if r.get("session_id") == "mag-agent-orc-noise-counter-v1")
assert counter is not None

# ── 1) boot_check._chain_tip: post-fold chain + counter-as-tail shape ──────
import mag.boot_check as bc  # noqa: E402

old_bc_chain = bc.CHAIN
try:
    bc.CHAIN = POST
    out["boot_check_post_fold"] = bc._chain_tip()
    # counter-as-tail: a one-row chain that IS the counter (worst-case shape)
    tail_file = SIM / "counter_as_tail.jsonl"
    tail_file.write_bytes((json.dumps(counter) + "\n").encode("utf-8"))
    bc.CHAIN = tail_file
    out["boot_check_counter_as_tail"] = bc._chain_tip()
finally:
    bc.CHAIN = old_bc_chain
assert "ERROR" not in str(out["boot_check_post_fold"].get("tip", ""))
assert "ERROR" not in str(out["boot_check_counter_as_tail"].get("tip", ""))

# ── 2) lattice_dashboard: (a) live-shape run — PRE-EXISTING crash check;
#      (b) sanitized run; (c) counter through the chain_tail render itself ──
import mag.lattice_dashboard as ld  # noqa: E402

old_bio = ld.BIO
lattice_result: dict = {}
try:
    ld.BIO = SIM
    try:
        summary = ld.build_lattice_summary()
        lattice_result["live_shape_run"] = {"ok": True}
        tail_sids = [row.get("session_id") for row in summary.get("chain_tail", [])]
        lattice_result["chain_n"] = summary.get("chain_n")
        lattice_result["counter_in_chain_tail_16"] = "mag-agent-orc-noise-counter-v1" in tail_sids
    except Exception as exc:  # noqa: BLE001 — the finding IS the exception
        lattice_result["live_shape_run"] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        # sanitize ONLY the poison tensions (live evolution carries 22 string
        # tension_index rows like 'fkb:amd_' — pre-existing, fold-unrelated)
        evo = json.loads((SIM / "topic_evolution.json").read_text(encoding="utf-8"))
        for s in evo.get("series", []):
            if not isinstance(s.get("tension_index"), (int, float)) and s.get("tension_index") is not None:
                s["tension_index"] = 0.0
        (SIM / "topic_evolution.json").write_text(json.dumps(evo, indent=2), encoding="utf-8")
        summary = ld.build_lattice_summary()
        lattice_result["sanitized_run"] = {"ok": True,
                                           "note": "22 live string-tension rows coerced to 0.0 for this probe only"}
        tail_sids = [row.get("session_id") for row in summary.get("chain_tail", [])]
        lattice_result["chain_n"] = summary.get("chain_n")
        lattice_result["counter_in_chain_tail_16"] = "mag-agent-orc-noise-counter-v1" in tail_sids
finally:
    ld.BIO = old_bio
# (c) worst case: the counter INSIDE the rendered tail-16 window — run the
# exact chain_tail render expression (lattice_dashboard.py:170-181 shape)
tail16 = [dict(r) for r in post_rows[:15]] + [counter]
rendered = [
    {
        "filename": row.get("filename") or row.get("leaf"),
        "session_id": row.get("session_id"),
        "verkle_root": (row.get("verkle_root") or "")[:16] or None,
        "ts": row.get("ts") or row.get("updated_minute") or row.get("start_minute"),
    }
    for row in tail16[-16:]
]
lattice_result["counter_as_tail_renders"] = rendered[-1]
out["lattice_dashboard"] = lattice_result
assert rendered[-1]["session_id"] == "mag-agent-orc-noise-counter-v1"

# ── 3) cache_map.build_map: same usage rows, pre vs post chain ─────────────
from mag import cache_map  # noqa: E402

usage_rows = None
usage_file = ROOT / "logs" / "provider_usage.jsonl"
if usage_file.is_file():
    usage_rows = [json.loads(l) for l in usage_file.read_text(encoding="utf-8").splitlines() if l.strip()]
m_pre = cache_map.build_map(usage_rows=usage_rows, chain_rows=pre_rows)
m_post = cache_map.build_map(usage_rows=usage_rows, chain_rows=post_rows)
out["cache_map"] = {
    "usage_rows": len(usage_rows or []),
    "by_theme_pre": m_pre.get("by_theme"),
    "by_theme_post": m_post.get("by_theme"),
    "by_theme_identical": m_pre.get("by_theme") == m_post.get("by_theme"),
    "totals_identical": {
        k: m_pre.get(k) == m_post.get(k)
        for k in ("total_prompt_tokens", "total_completion_tokens", "total_calls")
    },
}

# ── 4) knot_at_close._chain_session_ids: counter lands in the id set ───────
old_vk_chain = vk.CHAIN
try:
    vk.CHAIN = POST
    sids = knot_at_close._chain_session_ids()
finally:
    vk.CHAIN = old_vk_chain
out["knot_at_close"] = {
    "n_session_ids": len(sids),
    "counter_id_present": "mag-agent-orc-noise-counter-v1" in sids,
}

# ── 5) chain_query: tail/root return the row dicts; by_type finds it ───────
old_cq = chain_query.CHAIN_PATH
try:
    chain_query.CHAIN_PATH = POST
    q = chain_query.ChainQuery()
    tail = q.tail(30)
    root_row = q.root()
    by_type_counter = q.by_type("orchestrator_noise_counter_leaf")
    by_type_session = q.by_type("session_knot")
finally:
    chain_query.CHAIN_PATH = old_cq
out["chain_query"] = {
    "tail_n": len(tail),
    "root_row_sid": root_row.get("session_id"),
    "root_is_counter": root_row.get("session_id") == "mag-agent-orc-noise-counter-v1",
    "by_type_counter_rows": len(by_type_counter),
    "by_type_session_knot_rows": len(by_type_session),
}

# ── 6) verkle_audit.verkle_gaps(deep=False): numbers move, no crash ────────
import mag.verkle_audit as va  # noqa: E402

old = (va.CHAIN, va.KNOTS, va.TIP, va.LATTICE_NODES)
try:
    va.CHAIN, va.KNOTS, va.TIP = POST, vk.KNOTS, SIM / "verkle_tip.json"
    va.LATTICE_NODES = SIM / "nodes.jsonl"
    gaps_post = va.verkle_gaps(deep=False)
    va.CHAIN = PRE
    gaps_pre = va.verkle_gaps(deep=False)
finally:
    va.CHAIN, va.KNOTS, va.TIP, va.LATTICE_NODES = old
out["verkle_gaps"] = {
    "pre": [g.get("detail") for g in gaps_pre],
    "post": [g.get("detail") for g in gaps_post],
}

# ── 7) data_refinery._ingest_verkle_chain: counter near the TAIL (worst case:
#    its loop reads only the last 500 rows) must not crash and yields 1 example
import mag.data_refinery as dr  # noqa: E402

fake_root = SIM / "fake_root"
(fake_root / "memory" / "biography").mkdir(parents=True, exist_ok=True)
lines = [json.dumps({**counter, "index": 0})]
for i in range(499):
    filler = {**counter, "session_id": f"sess-filler-{i}",
              "leaf_hash": vk._leaf_hash({"filler": i}), "type": None,
              "filename": f"f{i}.knot.json", "index": i + 1}
    lines.append(json.dumps(filler))
(fake_root / "memory" / "biography" / "verkle_chain.jsonl").write_bytes(
    ("\n".join(lines) + "\n").encode("utf-8"))
old_dr_root = dr.ROOT
try:
    dr.ROOT = fake_root
    ref = dr.DataRefinery()
    stats = ref._ingest_verkle_chain()
finally:
    dr.ROOT = old_dr_root
out["data_refinery"] = {"stats": stats, "ok": stats.get("ingested", 0) == 500}

# ── 8) tapestry: registry-fed, and the counter is NOT in the registry ──────
from mag import registry as reg  # noqa: E402
from mag import tapestry  # noqa: E402

reg_rows = reg.list_registry(limit=500)
pack = tapestry.build_tapestry_pack()
pack_str = json.dumps(pack, default=str)
out["tapestry"] = {
    "registry_rows": len(reg_rows),
    "counter_in_registry": any(
        str(r.get("session_id")) == "mag-agent-orc-noise-counter-v1" for r in reg_rows),
    "pack_built": isinstance(pack, dict),
    "counter_string_in_pack": "mag-agent-orc-noise-counter-v1" in pack_str,
    "orc_rows_bucketed_untouched": sum(
        1 for r in reg_rows if str(r.get("session_id") or "").startswith("mag-agent-orc-")),
}

# ── 9) write footprint of the sandbox fold: only chain/tip/evo/marker/archive
files = sorted(str(p.relative_to(SIM)) for p in SIM.rglob("*") if p.is_file())
out["sandbox_write_footprint"] = [f for f in files if "compaction_archive" not in f]

print(json.dumps(out, indent=2, default=str))
