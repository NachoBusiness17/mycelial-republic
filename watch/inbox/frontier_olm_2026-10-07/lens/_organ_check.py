import os

paths = [
    "memory/rib/RIB_MODEL_GARDEN_ROUTING.md",
    "memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md",
    "memory/rib/RIB_DRIVING_LADDER_20260928.md",
    "memory/rib/RIB_MODEL_GATES_20261001.md",
    "memory/rib/RIB_DEEPSEEK_ELDER_SEAT.md",
    "memory/knowledge_graph.json",
    "mag/memlang.py",
    "mag/context_compression.py",
    "mag/skills_pack.py",
    "tools/workflow_gate.py",
    "memory/workflows/REGISTRY.jsonl",
    "watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl",
    "tools/citation_lint.py",
    "memory/runs/hermes_burn/usage.jsonl",
    "tools/ds_workhorse.py",
    "memory/improve",
    "watch/inbox/frontier_olm_2026-10-06/DIGEST.md",
    "watch/inbox/SHARED_SURFACE_CONTRACT.json",
    "state/arxiv",
    "catalog/catalog.jsonl",
]

for p in paths:
    print(("OK " if os.path.exists(p) else "MISSING ") + p)
