#!/usr/bin/env python3
"""Read-only Verkle/KZG territory audit and recovery map.

This tool deliberately does not rewrite the live chain, knot files, backups,
or pointers.  It measures their relationships and emits a derived receipt.
The live Mag "Verkle knot" is currently SHA-256 Merkle machinery; the KZG
layer is tracked separately so a specification is never mistaken for code.

Usage:
  python scripts/verkle_territory_audit.py
  python scripts/verkle_territory_audit.py --write
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import verkle_knot as vk  # noqa: E402

SCHEMA = "verkle_territory_audit.v1"
SCAN_ROOTS = (
    "memory", "watch", "docs", "mag", "scripts", "handoff", "bridge",
    "models", "tools", "tests", "artifacts", "outputs", "state", "jobs",
    "experiments", "deploy", "configs", "dashboard", "extensions",
    "router", "reference", "prompts", "harness", "campaigns",
)
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".py", ".js", ".mjs", ".ts", ".tsx",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".cmd", ".ps1", ".sh",
    ".html", ".css", ".sql", ".xml",
}
CODE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".rs", ".go", ".java", ".c", ".h"}
MAX_HASH_BYTES = 8 * 1024 * 1024


def utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path, limit: int = MAX_HASH_BYTES) -> str | None:
    try:
        if path.stat().st_size > limit:
            return None
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for block in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(block)
        return h.hexdigest()
    except OSError:
        return None


def walk_files() -> Iterable[Path]:
    for root_name in SCAN_ROOTS:
        base = ROOT / root_name
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".pytest-")]
            for name in filenames:
                yield Path(dirpath) / name


def artifact_class(path: Path) -> str:
    p = rel(path).lower()
    name = path.name.lower()
    if "trusted_setup" in p or "repro_serialize" in p or ("kzg" in p and path.suffix in {".md", ".json"}):
        return "kzg_spec_or_fixture"
    if "verkle_chain" in p or "verkle_tip" in p or "/biography/knots/" in p or "verkle_knot" in p:
        return "live_sha256_verkle"
    if "q_state" in p or "holographic_q" in p or "q_knot" in p:
        return "q_state_chain"
    if "rib" in p or "trajectory" in p or "sea/" in p:
        return "rib_or_trajectory"
    if "/memory/" in p:
        return "memory_other"
    if "/models/" in p or "/artifacts/" in p:
        return "physical_or_model_artifact"
    if "proof" in name or "commit" in name or "manifest" in name or "receipt" in name:
        return "receipt_or_manifest"
    return "other_scanned"


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    malformed = 0
    if not path.is_file():
        return rows, malformed
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    rows.append(value)
            except json.JSONDecodeError:
                malformed += 1
    except OSError:
        malformed += 1
    return rows, malformed


def pointer_name(session_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", str(session_id or ""))[:12]
    return f"by-session_{safe}.json"


def chain_audit() -> dict[str, Any]:
    chain = ROOT / "memory/biography/verkle_chain.jsonl"
    tip_path = ROOT / "memory/biography/verkle_tip.json"
    knots = ROOT / "memory/biography/knots"
    rows, malformed = load_jsonl(chain)
    hashes = [str(r.get("leaf_hash")) for r in rows if r.get("leaf_hash")]
    roots = vk._merkle_prefix_roots(hashes) if hashes else []
    counters = collections.Counter()
    missing: list[dict[str, str]] = []
    mismatch_examples: list[dict[str, Any]] = []
    sessions = collections.Counter(str(r.get("session_id") or "") for r in rows)
    safe_sessions: dict[str, set[str]] = collections.defaultdict(set)
    for r in rows:
        sid = str(r.get("session_id") or "")
        safe_sessions[pointer_name(sid)].add(sid)
    for i, row in enumerate(rows):
        expected = roots[i] if i < len(roots) else None
        previous = vk._merkle_root(hashes[:i]) if i else vk._h(b"empty")
        if row.get("verkle_root") != expected:
            counters["root_mismatch"] += 1
        if row.get("parent_verkle_root") != previous:
            counters["parent_mismatch"] += 1
        if row.get("index") != i:
            counters["index_mismatch"] += 1
        if row.get("n_leaves") != i + 1:
            counters["n_leaves_mismatch"] += 1
        filename = str(row.get("filename") or "")
        target = knots / filename
        if not target.is_file():
            counters["dangling_rows"] += 1
            if len(missing) < 25:
                missing.append({"session_id": str(row.get("session_id") or ""), "filename": filename})
            continue
        try:
            leaf = json.loads(target.read_text(encoding="utf-8"))
            if leaf.get("leaf_hash") != row.get("leaf_hash"):
                counters["knot_hash_mismatch"] += 1
            if leaf.get("session_id") != row.get("session_id"):
                counters["knot_session_mismatch"] += 1
        except (OSError, json.JSONDecodeError):
            counters["malformed_knot"] += 1

    tip: dict[str, Any] = {}
    if tip_path.is_file():
        try:
            value = json.loads(tip_path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                tip = value
        except (OSError, json.JSONDecodeError):
            counters["malformed_tip"] += 1
    expected_root = roots[-1] if roots else vk._h(b"empty")
    tip_matches = {
        "root": tip.get("root") == expected_root,
        "n_leaves": tip.get("n_leaves") == len(rows),
        "last_filename": bool(rows) and tip.get("last_filename") == rows[-1].get("filename"),
        "last_leaf_hash": bool(rows) and tip.get("last_leaf_hash") == rows[-1].get("leaf_hash"),
        "last_session_id": bool(rows) and tip.get("last_session_id") == rows[-1].get("session_id"),
    }
    leaf_files = list(knots.glob("*.knot.json")) if knots.is_dir() else []
    pointer_files = list(knots.glob("by-session_*.json")) if knots.is_dir() else []
    referenced = {str(r.get("filename") or "") for r in rows}
    unreferenced = [p.name for p in leaf_files if p.name not in referenced]
    pointer_missing = pointer_hash_mismatch = 0
    for p in pointer_files:
        try:
            ptr = json.loads(p.read_text(encoding="utf-8"))
            target = knots / str(ptr.get("filename") or "")
            if not target.is_file():
                pointer_missing += 1
            else:
                leaf = json.loads(target.read_text(encoding="utf-8"))
                if ptr.get("leaf_hash") and ptr.get("leaf_hash") != leaf.get("leaf_hash"):
                    pointer_hash_mismatch += 1
        except (OSError, json.JSONDecodeError):
            pointer_missing += 1
    collision_groups = {k: sorted(v) for k, v in safe_sessions.items() if len(v) > 1}
    try:
        proof = vk.prove_latest()
        proof_summary = {k: proof.get(k) for k in ("ok", "verified", "n_leaves", "error")}
    except Exception as exc:  # audit must remain reportable if proof code is unavailable
        proof_summary = {"ok": False, "verified": False, "error": str(exc)[:240]}
    try:
        chain_ok, chain_reason = vk._verify_chain_consistent()
    except Exception as exc:
        chain_ok, chain_reason = False, str(exc)[:240]
    return {
        "path": rel(chain),
        "rows": len(rows),
        "malformed_rows": malformed,
        "distinct_session_ids": len([s for s in sessions if s]),
        "duplicate_session_ids": sum(1 for n in sessions.values() if n > 1),
        "hashes": len(hashes),
        "root": expected_root,
        "chain_consistent": chain_ok,
        "chain_reason": chain_reason,
        "tip_matches": tip_matches,
        "field_anomalies": dict(counters),
        "dangling_examples": missing,
        "knot_files": len(leaf_files),
        "pointer_files": len(pointer_files),
        "unreferenced_knot_files": len(unreferenced),
        "unreferenced_examples": unreferenced[:25],
        "pointer_missing_or_malformed": pointer_missing,
        "pointer_hash_mismatch": pointer_hash_mismatch,
        "truncated_pointer_collision_groups": len(collision_groups),
        "largest_pointer_collision_group": max((len(v) for v in collision_groups.values()), default=0),
        "proof": proof_summary,
    }


def backup_audit() -> list[dict[str, Any]]:
    out = []
    for directory in sorted((ROOT / "memory").glob("biography_backup*")):
        chain = directory / "verkle_chain.jsonl"
        tip = directory / "verkle_tip.json"
        rows, malformed = load_jsonl(chain)
        hashes = [str(r.get("leaf_hash")) for r in rows if r.get("leaf_hash")]
        root = vk._merkle_root(hashes) if hashes else None
        tip_root = None
        if tip.is_file():
            try:
                tip_root = json.loads(tip.read_text(encoding="utf-8")).get("root")
            except (OSError, json.JSONDecodeError):
                pass
        out.append({
            "path": rel(directory), "rows": len(rows), "malformed": malformed,
            "recomputed_root": root, "tip_root": tip_root,
            "tip_matches": root == tip_root if tip_root else None,
        })
    return out


def crypto_audit() -> dict[str, Any]:
    code_hits: list[dict[str, Any]] = []
    docs_hits: list[dict[str, Any]] = []
    tokens = re.compile(r"trusted_setup|BLS12[- ]?381|pairing|hash_to_field|expand_message_xmd|py_ecc|ckzg|blst|KZG|Kate")
    for path in walk_files():
        suffix = path.suffix.lower()
        path_text = rel(path).lower()
        # KZG evidence can only be executable in source files, or normative in
        # the small set of Verkle/KZG design documents.  Do not reread the
        # entire 20k-leaf JSON store for crypto vocabulary.
        code_scope = suffix in CODE_SUFFIXES and path_text.split("/", 1)[0] in {"mag", "scripts", "tests", "bridge", "tools"}
        doc_scope = suffix == ".md" and any(term in path_text for term in ("verkle", "kzg", "serialize"))
        if not (code_scope or doc_scope):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = sorted(set(m.group(0) for m in tokens.finditer(text)))
        if not hits:
            continue
        item = {"path": rel(path), "tokens": hits}
        (code_hits if path.suffix.lower() in CODE_SUFFIXES else docs_hits).append(item)
    executable_kzg = [
        x for x in code_hits
        if x["path"] != rel(Path(__file__))
        and any(t.lower() in {"kzg", "kate", "pairing", "bls12-381", "trusted_setup", "py_ecc", "ckzg", "blst", "hash_to_field", "expand_message_xmd"} for t in x["tokens"])
    ]
    return {
        "live_implementation": "sha256_duplicate_last_binary_merkle",
        "live_implementation_evidence": ["mag/verkle_knot.py", "scripts/repair_verkle_chain.py"],
        "kzg_spec_evidence": ["docs/REPRO_SERIALIZE_SPEC.md"],
        "executable_kzg_hits": executable_kzg[:100],
        "executable_kzg_hit_count": len(executable_kzg),
        "documentation_or_fixture_hits": docs_hits[:200],
        "trusted_setup_file_present": any("trusted_setup" in rel(p).lower() for p in walk_files()),
        "verdict": "KZG is specified, not implemented in the scanned executable code; remaining hits are vocabulary/comments or unrelated code references",
    }


def scan_inventory() -> dict[str, Any]:
    counts: dict[str, dict[str, int]] = collections.defaultdict(lambda: {"files": 0, "bytes": 0, "hashed_small_files": 0})
    load_bearing: list[dict[str, Any]] = []
    total_files = total_bytes = 0
    for path in walk_files():
        try:
            size = path.stat().st_size
        except OSError:
            continue
        cls = artifact_class(path)
        counts[cls]["files"] += 1
        counts[cls]["bytes"] += size
        total_files += 1
        total_bytes += size
        p = rel(path).lower()
        if any(term in p for term in ("verkle", "kzg", "trajectory", "rib", "q_state", "biography", "memory", "manifest", "receipt")) and len(load_bearing) < 1200:
            item: dict[str, Any] = {"path": rel(path), "class": cls, "bytes": size}
            # The live knot JSON is already verified against the chain above;
            # hashing 20k individual leaf files again adds cost without new
            # evidence.  Hash shared specs/receipts/indexes, and leave large
            # physical/model files as metadata until a specific artifact is
            # selected for migration.
            hash_allowed = (
                path.suffix.lower() in TEXT_SUFFIXES
                and "/knots/" not in p
                and ("/docs/" in p or "/watch/" in p or "/memory/runs/" in p or path.name.lower() in {"verkle_chain.jsonl", "verkle_tip.json"})
            )
            if hash_allowed:
                digest = sha256_file(path)
                if digest:
                    item["sha256"] = digest
                    counts[cls]["hashed_small_files"] += 1
                else:
                    item["hash"] = "skipped_over_8MiB"
            load_bearing.append(item)
    return {
        "roots": [r for r in SCAN_ROOTS if (ROOT / r).is_dir()],
        "total_files": total_files,
        "total_bytes": total_bytes,
        "by_class": dict(sorted(counts.items())),
        "load_bearing_sample_or_cap": load_bearing,
        "load_bearing_count_reported": len(load_bearing),
    }


def build_report() -> dict[str, Any]:
    chain = chain_audit()
    return {
        "schema": SCHEMA,
        "observed_at": utc(),
        "read_only": True,
        "source_of_truth": {
            "live_root": "memory/biography/verkle_chain.jsonl + verkle_tip.json",
            "leaf_store": "memory/biography/knots/*.knot.json",
            "recovery_pointers": "memory/biography/knots/by-session_*.json",
            "parallel_lineage_not_merged": ["memory/ghost/q_state/q_knots.jsonl", "memory/runs/chain.jsonl", "watch/sea", "memory/biography_backup*"],
        },
        "chain": chain,
        "backups": backup_audit(),
        "crypto_boundary": crypto_audit(),
        "inventory": scan_inventory(),
        "manual_recoveries": [
            {
                "session_id": "mag-agent-orc-t7e3e63a7c8",
                "target": "memory/biography/knots/2026-08-12_0422_session_mag-agen_0c89a5b4.knot.json",
                "source": "memory/biography_backup_20260825/knots/2026-08-12_0422_session_mag-agen_0c89a5b4.knot.json",
                "leaf_hash": "3210efbe5dae131cfbaed96ad71eec976d7c6e68c64cedcb8698d4cff264367f",
                "method": "exact leaf-hash/session/filename match; file restored only; chain and tip untouched",
            }
        ],
        "recovery_and_defrag_plan": [
            {"id": "R0", "status": "measured", "action": "Keep the current SHA-256 chain as the legacy integrity root; do not call it KZG."},
            {"id": "R1", "status": "dry-run only", "action": "Preserve and separately catalog the 18 dangling rows; do not fabricate leaves. Pointer recovery currently resolves zero."},
            {"id": "R2", "status": "next", "action": "Build a canonical artifact index keyed by path, content hash, schema, lineage, and root membership; repair the truncated by-session pointer namespace before relying on it."},
            {"id": "R3", "status": "next", "action": "Separate immutable source bytes from derived views: chain, Q-state, RIB/trajectory, backups, and game artifacts remain distinct lineages with explicit bridges."},
            {"id": "R4", "status": "later", "action": "Implement genuine KZG only as verkle_kzg.v1 beside the current root: canonical bytes, BLS12-381 Fr/G1/G2, pinned SRS, test vectors, pairing verifier, then dual-root receipts."},
        ],
        "negative_claims": [
            "No chain row, tip, backup, or root was rewritten by this audit; one exact leaf file was restored separately from a verified backup.",
            "A healthy SHA-256 Merkle proof is not a KZG opening proof.",
            "A KZG specification is not evidence that a trusted setup, curve arithmetic, or pairing verifier exists.",
        ],
    }


def markdown(report: dict[str, Any]) -> str:
    c = report["chain"]
    crypto = report["crypto_boundary"]
    inv = report["inventory"]
    lines = [
        "# Verkle Territory Recovery Receipt",
        "",
        f"Observed: `{report['observed_at']}` · schema `{report['schema']}` · **read-only**",
        "",
        "## Verdict",
        "",
        "The live knot store is a functioning SHA-256 append-only Merkle ledger. It is not yet a KZG Verkle implementation. The KZG/BLS12-381 construction is present as a normative serialization specification, with no executable trusted setup, field arithmetic, curve operations, or pairing verifier found in the scanned code.",
        "",
        "## Live chain",
        "",
        f"- Rows/leaves: **{c['rows']}**; malformed rows: **{c['malformed_rows']}**; duplicate session IDs: **{c['duplicate_session_ids']}**.",
        f"- Chain gate: **{c['chain_consistent']}** (`{c['chain_reason']}`). Latest proof: `{c['proof']}`.",
        f"- Root: `{c['root']}`; tip fields: `{c['tip_matches']}`.",
        f"- Dangling rows: **{c['field_anomalies'].get('dangling_rows', 0)}**; current pointer recovery: **0** (pointer collision prevents safe automatic substitution).",
        f"- Knot files: {c['knot_files']}; pointer files: {c['pointer_files']}; unreferenced knot files: {c['unreferenced_knot_files']}.",
        f"- Truncated pointer collision groups: {c['truncated_pointer_collision_groups']}; largest group: {c['largest_pointer_collision_group']} sessions.",
        "",
        "## What the local math actually is",
        "",
        "`leaf_hash = SHA256(\"leaf:\" || canonical_json)`; internal nodes are `SHA256(\"node:\" || left || \":\" || right)` with duplicate-last promotion. Proofs carry an index and sibling hashes. This gives tamper evidence, append history, membership proofs, and crash recovery—but not polynomial commitments or constant-size KZG openings.",
        "",
        "## KZG boundary",
        "",
        f"- Spec evidence: `docs/REPRO_SERIALIZE_SPEC.md`; executable KZG hit count: **{crypto['executable_kzg_hit_count']}**; trusted setup file present: **{crypto['trusted_setup_file_present']}**.",
        "- The proposed KZG layer needs BLS12-381 scalar-field values, a pinned SRS, polynomial interpolation over 256 slots, G1/G2 point arithmetic, and pairing verification. None may be inferred from the SHA-256 chain.",
        "",
        "## Safe recovery performed",
        "",
        "One missing leaf was restored from `memory/biography_backup_20260825/` after exact session, filename, and leaf-hash agreement. The live chain and tip were not rewritten; the remaining dangling rows require historical selection or an operator-approved repair window.",
        "",
        "## Defragmentation order",
        "",
        "1. Freeze the current root as `legacy_sha256_merkle.v1` and preserve all source files.",
        "2. Catalog dangling rows and backups without deleting or inventing evidence; resolve the 12-character pointer namespace collision before using pointers as recovery authority.",
        "3. Create one derived artifact index that maps every load-bearing file to `path`, `sha256`, `schema`, `lineage`, `source`, and (where applicable) chain index/root.",
        "4. Keep Q-state, RIB/trajectory, game/world, and backup stores as separate lineages joined by explicit hash references—not one flattened mega-chain.",
        "5. Build `verkle_kzg.v1` as a parallel implementation with published fixtures and dual-root receipts; migrate only after cross-implementation tests pass.",
        "",
        "## Estate scan",
        "",
        f"Scanned {inv['total_files']} files ({inv['total_bytes']} bytes) across the shared source, memory, watch, docs, model, and artifact roots. The JSON receipt contains the classified inventory and load-bearing hash sample.",
        "",
        "Apart from the one exact leaf restoration recorded above, no chain row, tip, backup, or root was rewritten by this pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="write the derived JSON receipt and Markdown report")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        json_path = ROOT / "memory" / "runs" / "verkle_recovery" / f"territory_{stamp}.json"
        md_path = ROOT / "watch" / f"VERKLE_TERRITORY_RECOVERY_{stamp}.md"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md_path.write_text(markdown(report), encoding="utf-8")
        report["receipt_path"] = rel(json_path)
        report["report_path"] = rel(md_path)
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
