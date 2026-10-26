#!/usr/bin/env python3
"""tools/ingest_docs_cas.py - Ingest core architecture documentation into CAS mesh.

House Law: strictly zero unicode em-dashes.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.cas_mesh import CasMesh


def main() -> int:
    mesh = CasMesh()

    core_docs = [
        {
            "path": "docs/ref/ractors/RACTORS.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "ractors", "panel_protocol", "seats"],
            "extra": {"source_path": "docs/ref/ractors/RACTORS.md", "domain": "agent_architecture", "title": "RACTORS"},
        },
        {
            "path": "docs/ref/GAME_PLATFORM_BASECAMP.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "game_platform", "basecamp", "gwap", "mmo"],
            "extra": {"source_path": "docs/ref/GAME_PLATFORM_BASECAMP.md", "domain": "game_platform", "title": "GAME_PLATFORM_BASECAMP"},
        },
        {
            "path": "docs/ref/SOVEREIGN_STACK.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "sovereign_stack", "cockpit", "shell"],
            "extra": {"source_path": "docs/ref/SOVEREIGN_STACK.md", "domain": "system_architecture", "title": "SOVEREIGN_STACK"},
        },
        {
            "path": "docs/ref/CORE_MEMORY_PROTOCOL.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "core_memory", "memory_protocol", "magnetic_core"],
            "extra": {"source_path": "docs/ref/CORE_MEMORY_PROTOCOL.md", "domain": "memory_architecture", "title": "CORE_MEMORY_PROTOCOL"},
        },
        {
            "path": "docs/ref/TRAJECTORY_ARCHITECTURE.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "trajectory", "rib_compiler", "lattice"],
            "extra": {"source_path": "docs/ref/TRAJECTORY_ARCHITECTURE.md", "domain": "execution_architecture", "title": "TRAJECTORY_ARCHITECTURE"},
        },
        {
            "path": "docs/ref/V4_SPEC.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "v4_spec", "sovereign_v4", "specification"],
            "extra": {"source_path": "docs/ref/V4_SPEC.md", "domain": "specification", "title": "V4_SPEC"},
        },
        {
            "path": "docs/ref/RIB_SWARM_SPEC.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "rib_swarm", "distributed_execution", "swarm"],
            "extra": {"source_path": "docs/ref/RIB_SWARM_SPEC.md", "domain": "swarm_architecture", "title": "RIB_SWARM_SPEC"},
        },
        {
            "path": "docs/ref/REPUBLIC_COMPASS.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "republic_compass", "governance", "sovereign_estate"],
            "extra": {"source_path": "docs/ref/REPUBLIC_COMPASS.md", "domain": "governance_architecture", "title": "REPUBLIC_COMPASS"},
        },
        {
            "path": "docs/ref/COMMON_LANGUAGE_SPEC.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "common_language", "dsl", "specification"],
            "extra": {"source_path": "docs/ref/COMMON_LANGUAGE_SPEC.md", "domain": "protocol_specification", "title": "COMMON_LANGUAGE_SPEC"},
        },
        {
            "path": "docs/ref/MCP_EPISTEMIC_MESH_SPEC.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "mcp", "epistemic_mesh", "protocol_spec"],
            "extra": {"source_path": "docs/ref/MCP_EPISTEMIC_MESH_SPEC.md", "domain": "mesh_architecture", "title": "MCP_EPISTEMIC_MESH_SPEC"},
        },
        {
            "path": "docs/ref/KABUKI_STACK_20260905.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "kabuki_stack", "simulation", "runtime"],
            "extra": {"source_path": "docs/ref/KABUKI_STACK_20260905.md", "domain": "simulation_architecture", "title": "KABUKI_STACK"},
        },
        {
            "path": "docs/ref/STACK_V1.md",
            "actor": "architecture-curator",
            "parent": None,
            "labels": ["docs", "ref", "architecture", "stack_v1", "foundational_stack", "runtime"],
            "extra": {"source_path": "docs/ref/STACK_V1.md", "domain": "foundational_architecture", "title": "STACK_V1"},
        },
    ]

    ractor_chairs = [
        "BAUDRILLARD", "BERNAYS", "BLAVATSKY", "ELLUL", "FOUCAULT", "FREUD",
        "HALL", "JUNG", "MCLUHAN", "MPHALL", "PLATO_KIRK", "WALLAS",
    ]

    results = []

    # 1. Ingest RACTORS.md first
    r_item = core_docs[0]
    r_abs = os.path.join(ROOT, r_item["path"])
    with open(r_abs, "rb") as fp:
        r_content = fp.read()
    rec_ractors = mesh.put_slab(
        r_content,
        actor_seat=r_item["actor"],
        causal_parent=r_item["parent"],
        labels=r_item["labels"],
        extra=r_item["extra"],
    )
    ractors_hash = rec_ractors["content_hash"]
    results.append({
        "path": r_item["path"],
        "hash": ractors_hash,
        "bytes": len(r_content),
        "actor": r_item["actor"],
        "parent": r_item["parent"],
        "labels": r_item["labels"],
    })

    # 2. Ingest ractor chairs with causal parent pointing to RACTORS.md
    for chair in ractor_chairs:
        c_rel = f"docs/ref/ractors/{chair}.md"
        c_abs = os.path.join(ROOT, c_rel)
        with open(c_abs, "rb") as fp:
            c_content = fp.read()
        labels = ["docs", "ref", "architecture", "ractors", "chair", chair.lower()]
        extra = {"source_path": c_rel, "domain": "agent_architecture", "title": chair, "manifest_parent": "RACTORS.md"}
        rec_chair = mesh.put_slab(
            c_content,
            actor_seat="architecture-curator",
            causal_parent=ractors_hash,
            labels=labels,
            extra=extra,
        )
        results.append({
            "path": c_rel,
            "hash": rec_chair["content_hash"],
            "bytes": len(c_content),
            "actor": "architecture-curator",
            "parent": ractors_hash,
            "labels": labels,
        })

    # 3. Ingest remaining core architecture docs
    for doc in core_docs[1:]:
        d_abs = os.path.join(ROOT, doc["path"])
        with open(d_abs, "rb") as fp:
            d_content = fp.read()
        rec_doc = mesh.put_slab(
            d_content,
            actor_seat=doc["actor"],
            causal_parent=doc["parent"],
            labels=doc["labels"],
            extra=doc["extra"],
        )
        results.append({
            "path": doc["path"],
            "hash": rec_doc["content_hash"],
            "bytes": len(d_content),
            "actor": doc["actor"],
            "parent": doc["parent"],
            "labels": doc["labels"],
        })

    print(f"Successfully ingested {len(results)} architecture documents into CAS.")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
