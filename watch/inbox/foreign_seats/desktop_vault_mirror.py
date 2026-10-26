#!/usr/bin/env python3
"""tools/sovereign/desktop_vault_mirror.py — Sovereign Desktop Treasure Trove & ArXiv Vault Mirror.

Automates the synchronization of the primary desktop estate's massive research holdings
directly into the 10TB dual-cloud vaults (gdrive_sd: and gdrive_nacho:):

1. TREASURE TROVES MIRRORED:
   - arXiv Research PDFs & Preprints: local_sovereign_agent/memory/corpus/training_pdfs/
   - Frontier System Prompt Leaks & Lenses: research/cl4r1t4s/
   - Foundational Research Kernels: research/aiTruthCode/
   - Catalog FTS & Snapshots: local_sovereign_agent/catalog/ (2,006,883 indexed assets)
   - Agent Game & Simulation Repositories: the-mountain/, ractor-salon/

2. ZERO-LOCAL-BLOAT INVARIANT:
   Executes directly on node desktop (foste@100.96.161.76).
   Uploads directly to cloud vaults using desktop fiber; zero bytes downloaded to node bob.
   Guarantees bob's NVMe SSD remains > 15.0 GB free floor.

3. DUAL-CLOUD REDUNDANCY:
   Mirrors to both Google Drive accounts:
     - Primary: gdrive_sd:corpus/
     - Secondary / Mirror: gdrive_nacho:corpus/
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DESKTOP_PROJECTS = Path(r"C:\Users\foste\Documents\projects")

MIRROR_TARGETS = [
    {
        "name": "arxiv_training_pdfs",
        "source": DESKTOP_PROJECTS / "local_sovereign_agent" / "memory" / "corpus" / "training_pdfs",
        "cloud_dest": "corpus/papers/arxiv_training_pdfs",
        "description": "arXiv preprints, neuromorphic and biological computing research papers"
    },
    {
        "name": "cl4r1t4s_system_prompts",
        "source": DESKTOP_PROJECTS / "research" / "cl4r1t4s",
        "cloud_dest": "corpus/research/cl4r1t4s_prompt_leaks",
        "description": "Frontier AI system prompts and model behavioral lenses (Anthropic, OpenAI, Cursor, etc.)"
    },
    {
        "name": "aiTruthCode_kernels",
        "source": DESKTOP_PROJECTS / "research" / "aiTruthCode",
        "cloud_dest": "corpus/research/aiTruthCode_kernels",
        "description": "56 foundational research kernels, harmonic architectures, and multi-agent systems"
    },
    {
        "name": "the_mountain_simulation",
        "source": DESKTOP_PROJECTS / "the-mountain",
        "cloud_dest": "corpus/repos/the_mountain_game",
        "description": "Agent simulation, hooks, and multi-user game server"
    },
    {
        "name": "estate_catalog_snapshot",
        "source": DESKTOP_PROJECTS / "local_sovereign_agent" / "catalog",
        "cloud_dest": "estate_snapshots/catalog",
        "description": "Full estate catalog (2M records, FTS sqlite, tag ledgers)"
    }
]


def run_rclone_sync(src: Path, dest_remote: str, dry_run: bool = False) -> Dict[str, Any]:
    """Execute rclone copy with high concurrency."""
    if not src.exists():
        return {"status": "SKIPPED", "reason": f"Source path {src} does not exist"}

    cmd = [
        "rclone", "copy",
        str(src), dest_remote,
        "--transfers=8",
        "--checkers=16",
        "--fast-list",
        "-v"
    ]
    if dry_run:
        cmd.append("--dry-run")

    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        dur = round(time.time() - t0, 1)
        if proc.returncode == 0:
            return {"status": "SUCCESS", "duration_s": dur, "remote": dest_remote}
        else:
            return {"status": "ERROR", "error": proc.stderr[-300:], "duration_s": dur}
    except Exception as e:
        return {"status": "FAILED", "error": str(e), "duration_s": round(time.time() - t0, 1)}


def execute_mirror(remotes: List[str] = None, dry_run: bool = False) -> Dict[str, Any]:
    remotes = remotes or ["gdrive_sd:", "gdrive_nacho:"]
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "host": "desktop (foste@100.96.161.76)",
        "results": []
    }

    print(f"=== SOVEREIGN DESKTOP VAULT MIRROR ({len(MIRROR_TARGETS)} targets -> {remotes}) ===")
    for target in MIRROR_TARGETS:
        t_name = target["name"]
        src_path = target["source"]
        print(f"\n[Target: {t_name}] -> {src_path}")
        print(f"  Description: {target['description']}")

        for remote in remotes:
            cloud_path = f"{remote}{target['cloud_dest']}"
            print(f"  Streaming to: {cloud_path} ...", end=" ", flush=True)
            res = run_rclone_sync(src_path, cloud_path, dry_run=dry_run)
            print(res["status"])
            manifest["results"].append({
                "target": t_name,
                "remote": remote,
                "result": res
            })

    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desktop Vault Mirror Automation")
    parser.add_argument("--dry-run", action="store_true", help="Simulate rclone transfer")
    parser.add_argument("--primary-only", action="store_true", help="Sync only to primary gdrive_sd:")
    args = parser.parse_args()

    rems = ["gdrive_sd:"] if args.primary_only else ["gdrive_sd:", "gdrive_nacho:"]
    out = execute_mirror(rems, dry_run=args.dry_run)
    print("\n=== MIRROR MANIFEST SUMMARY ===")
    print(json.dumps(out, indent=2))
