#!/usr/bin/env python3
"""tools/cas_ingest_beta.py - CAS Mesh Ingestion Partition Beta.

Squadron A, Unit 2 of 24.
Mandate:
Ingest partition 2 of research reports from watch/inbox/burn_reset_20260927/work/
(filenames starting with g through m1999) into the CAS mesh.
Actor seat: cas_ingestion_beta.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only; pure functions.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.cas_mesh import CasMesh


def scan_beta_partition(work_dir: str) -> List[str]:
    """Scan and select files matching [g-m]*.md up through m1999."""
    if not os.path.isdir(work_dir):
        return []
    matched: List[str] = []
    for entry in os.scandir(work_dir):
        if not entry.is_file() or not entry.name.endswith(".md"):
            continue
        fname = entry.name
        c = fname[0].lower()
        if "g" <= c <= "l":
            matched.append(entry.path)
        elif c == "m":
            m = re.match(r"^m(\d+)", fname)
            if m and int(m.group(1)) <= 1999:
                matched.append(entry.path)
    matched.sort()
    return matched


def run_ingest_beta() -> Dict[str, Any]:
    """Ingest partition 2 into CAS mesh with actor_seat=cas_ingestion_beta."""
    mesh = CasMesh()
    work_dir = os.path.join(ROOT, "watch", "inbox", "burn_reset_20260927", "work")

    t0 = time.time()
    file_paths = scan_beta_partition(work_dir)
    total_files = len(file_paths)

    print(f"Scanned partition: {total_files} files matching [g-m]*.md (through m1999)", flush=True)

    tasks: List[Tuple[str, str]] = []
    for p in file_paths:
        tasks.append((p, os.path.basename(p)))

    unique_hashes: set[str] = set()
    total_bytes = 0
    done_count = 0

    def _worker(item: Tuple[str, str]) -> Tuple[str, int]:
        filepath, filename = item
        with open(filepath, "rb") as fp:
            data = fp.read()
        rel_path = os.path.relpath(filepath, ROOT)
        extra = {
            "source_path": rel_path,
            "filename": filename,
            "source_category": "work",
        }
        labels = ["work", "receipt", "burn_reset_20260927", "cas_ingestion_beta"]
        rec = mesh.put_slab(
            content=data,
            actor_seat="cas_ingestion_beta",
            labels=labels,
            extra=extra,
        )
        return rec["content_hash"], len(data)

    print(f"Starting parallel ingestion with 32 worker threads...", flush=True)
    with ThreadPoolExecutor(max_workers=32) as pool:
        for chash, bsize in pool.map(_worker, tasks):
            unique_hashes.add(chash)
            total_bytes += bsize
            done_count += 1
            if done_count % 500 == 0 or done_count == total_files:
                print(f"Ingested {done_count}/{total_files} files ({time.time()-t0:.2f}s elapsed)...", flush=True)

    elapsed = time.time() - t0
    print(f"Partition ingestion completed in {elapsed:.2f}s.", flush=True)
    print(f"Total files: {total_files}, Unique slabs: {len(unique_hashes)}, Total bytes: {total_bytes}", flush=True)

    return {
        "status": "COMPLETED",
        "actor_seat": "cas_ingestion_beta",
        "partition": "g through m1999",
        "total_files_scanned": total_files,
        "unique_slabs": len(unique_hashes),
        "total_bytes_stored": total_bytes,
        "elapsed_seconds": elapsed,
    }


def main() -> int:
    try:
        res = run_ingest_beta()
        print(json.dumps(res, indent=2))
        return 0
    except Exception as exc:
        sys.stderr.write(f"Ingestion error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
