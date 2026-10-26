#!/usr/bin/env python3
"""_s220_scan.py - s2-20 raw evidence: seed-gap census for SEED-RIB 09-28.

Builds the should-universe grounded in (a) tools/seed_rib.py classify_role
run over the whole repo, (b) SEED_RIB_FORMAT_v0_20260926.md sections 2/4,
(c) AGENTS.md load-order + clippy named files, (d) tools/freshness_check.py
boot-doc list, then diffs against watch/inbox/seed_rib_20260928/seed-rib/seed.json.
Writes _s220_raw.json beside this script. No subprocess spawns.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".").resolve()
SEED = ROOT / "watch/inbox/seed_rib_20260928/seed-rib/seed.json"
OUT = Path(__file__).resolve().parent / "_s220_raw.json"

EXCLUDE = {".git", ".venv", "node_modules", "__pycache__", "agents", "logs",
           "corpus", "third_party", ".ruff_cache", ".pytest_cache", "dist", "build"}

seed = json.loads(SEED.read_text(encoding="utf-8"))
seed_paths = {e["path"]: e for e in seed["entries"]}
INLINE_MAX = seed.get("inline_max_bytes", 8192)


def classify_role(rel: str) -> str:
    # byte-faithful port of tools/seed_rib.py classify_role (lines 40-51)
    if rel.startswith("memory/law/"):
        return "law"
    if rel.startswith("docs/") or rel in ("CONSTITUTION.md",):
        return "doctrine"
    if rel == "AGENTS.md" or rel.startswith("state/") or "handoff" in rel.lower():
        return "boot"
    if rel.startswith("watch/inbox/"):
        return "receipt"
    if rel.endswith(".jsonl"):
        return "ledger"
    return "pointer"


def info(rel: str) -> dict:
    p = ROOT / rel
    row = {"path": rel, "exists": p.is_file()}
    if p.is_file():
        raw = p.read_bytes()
        row["bytes"] = len(raw)
        row["sha256"] = hashlib.sha256(raw).hexdigest()
        row["mtime"] = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        row["would_inline"] = len(raw) <= INLINE_MAX
    row["in_seed"] = rel in seed_paths
    if rel in seed_paths:
        e = seed_paths[rel]
        row["seed_carrier"] = e["carrier"]
        row["seed_seal_match"] = (e["sha256"] == row.get("sha256"))
    row["classify_role"] = classify_role(rel)
    return row


candidates: dict[str, list[str]] = {}

# A. spec-mandated (SEED_RIB_FORMAT_v0_20260926.md s2/s4 + "pointers fused here")
candidates["A_spec_law_surface"] = sorted(
    p.relative_to(ROOT).as_posix() for p in (ROOT / "memory/law").glob("*") if p.is_file())
candidates["A_spec_fused_pointers"] = [
    "watch/inbox/ESSENTIALS_RESTORE.md",
    "watch/inbox/TWO_MACHINE_SYNC_20260919.md",
    "watch/inbox/SEED_RIB_FORMAT_v0_20260926.md",
]

# B. AGENTS.md load-order table + build-discipline boot docs
candidates["B_load_order"] = [
    "docs/FRAMEWORK_LOAD.md",
    "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
    "docs/ref/MYCELIAL_SCIENCE_MAP.md",
    "docs/ref/MAG_DIRECTION_ARTIFACT_v2.md",
    "docs/ref/MAG_PROJECT_PROPOSAL.md",
    "docs/ref/OPERATOR_CARD.md",
    "AGENTS.md",
    "docs/ref/releases/VERSION_REGISTRY.md",
    "configs/version_roadmap.yaml",
    "state/CURRENT.md",
    "queue/todo.md",
    "HANDOFF_MAG_AGENT_TODOS.md",
    "CONSTITUTION.md",
    "docs/DNA.md",
]
candidates["B_freshness_boot_docs"] = [
    "BOOT_4_7.md", "state/CURRENT.md", "state/START_BRIEF.md", "state/HANDOFF.md",
]
candidates["B_queue_handoffs"] = sorted(
    p.relative_to(ROOT).as_posix() for p in (ROOT / "queue/handoff").glob("*") if p.is_file())

# C. AGENTS.md clippy / when-a-specialist-seat-is-used named files
candidates["C_operator_named"] = [
    "memory/rib/RIB_FREE_USAGE_POLICY_20260823.md",
    "memory/rib/RIB_DRIVING_LADDER_20260928.md",
    "watch/inbox/INDEX.json",
    "watch/inbox/SHARED_SURFACE_CONTRACT.json",
    "memory/attention.md",
    "memory/live_from_grok.md",
    "memory/warm_state.json",
    "configs/lanes.yaml",
]

# D. the full rib surface
candidates["D_rib_surface"] = sorted(
    p.relative_to(ROOT).as_posix() for p in (ROOT / "memory/rib").glob("*.md") if p.is_file())

# E. prior seed (09-26) coverage that the 09-28 seed dropped
old = json.loads((ROOT / "watch/inbox/SEED_RIB_CURRENT_20260926.json").read_text(encoding="utf-8"))
candidates["E_dropped_from_0926_seed"] = [e["path"] for e in old["entries"]]

result = {
    "generated_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "seed_path": "watch/inbox/seed_rib_20260928/seed-rib/seed.json",
    "seed_created_ts": seed.get("created_ts"),
    "seed_entries": len(seed["entries"]),
    "seed_inline_max": INLINE_MAX,
    "groups": {},
}

all_rows = []
for gname, paths in candidates.items():
    rows = [info(p) for p in paths]
    result["groups"][gname] = {
        "count": len(rows),
        "in_seed": sum(1 for r in rows if r["in_seed"]),
        "missing": [r["path"] for r in rows if not r["in_seed"] and r["exists"]],
        "missing_bytes_if_under_inline_max": sum(
            r["bytes"] for r in rows if not r["in_seed"] and r["exists"] and r.get("would_inline")),
        "rows": rows,
    }
    all_rows.extend(rows)

# kernel-surface classify_role rollup: the dirs classify_role's boot-kernel
# universe lives in. NOT whole-repo: a full walk is infeasible here (.mimosa
# holds 3,193,880 files, memory/ 318,623, mine/ 98,524 - counted separately
# by os.walk with dirnames prune, see _s220_dircounts.json). Scope stated in
# the deliverable.
rollup: dict[str, dict] = {}
ROLLUP_DIRS = ["memory/law", "memory/rib", "docs", "state", "queue",
               "configs", "scripts", "tools", "mag", "githooks", "tests",
               "watch/inbox", "watch/board", "."]
for rd in ROLLUP_DIRS:
    base = ROOT / rd
    if rd == ".":
        it = (ROOT / fn for fn in os.listdir(ROOT) if (ROOT / fn).is_file())
        for p in it:
            rel = p.relative_to(ROOT).as_posix()
            role = classify_role(rel)
            slot = rollup.setdefault(role, {"files": 0, "bytes": 0, "under_inline_max": 0})
            n = p.stat().st_size
            slot["files"] += 1
            slot["bytes"] += n
            if n <= INLINE_MAX:
                slot["under_inline_max"] += 1
        continue
    if not base.is_dir():
        continue
    for dirpath, dirnames, filenames in os.walk(base):
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = p.relative_to(ROOT).as_posix()
            role = classify_role(rel)
            slot = rollup.setdefault(role, {"files": 0, "bytes": 0, "under_inline_max": 0})
            try:
                n = p.stat().st_size
            except OSError:
                continue
            slot["files"] += 1
            slot["bytes"] += n
            if n <= INLINE_MAX:
                slot["under_inline_max"] += 1
result["repo_role_rollup_excluded_dirs"] = sorted(EXCLUDE)
result["repo_role_rollup_scope"] = ROLLUP_DIRS
result["repo_role_rollup"] = rollup

# seed coverage per role
seed_roles: dict[str, int] = {}
for e in seed["entries"]:
    seed_roles[e["role"]] = seed_roles.get(e["role"], 0) + 1
result["seed_role_coverage"] = seed_roles

OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
print("wrote", OUT, OUT.stat().st_size, "bytes")
for gname, g in result["groups"].items():
    print(f"{gname}: {g['count']} candidates, {g['in_seed']} in seed, {len(g['missing'])} missing")
print("repo rollup:", json.dumps(rollup))
print("seed role coverage:", seed_roles)
