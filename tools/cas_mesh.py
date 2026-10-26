#!/usr/bin/env python3
"""tools/cas_mesh.py - Content-Addressable Storage (CAS) Mesh & EPGM Provenance.

Mandate:
Replaces Git-bound transport and single-site repositories with an invariant,
peer-to-peer Content-Addressable Storage (CAS) slab pool backed by EPGM
(Execution Provenance Graph) headers.

Research Lineage:
- EPGM: Execution Provenance for Budgeted Agent Memory Retrieval (arXiv:2609.25913)
- Anti-Compaction Laundering: Provenance Destruction in Coding Agents (arXiv:2610.29869)
- Distributed CAS / BitTorrent Slabs: Content is addressed by SHA-256; zero central forge.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only; pure functions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

DEFAULT_CAS_DIR = os.path.join(ROOT, "memory", "cas")


def compute_sha256(content: bytes) -> str:
    """Compute standard SHA-256 digest in hex."""
    return hashlib.sha256(content).hexdigest()


class CasMesh:
    """Content-Addressable Storage mesh with EPGM provenance sidecars."""

    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = base_dir or DEFAULT_CAS_DIR
        self.slabs_dir = os.path.join(self.base_dir, "slabs")
        self.epgm_dir = os.path.join(self.base_dir, "epgm")
        self.manifest_dir = os.path.join(self.base_dir, "manifests")
        self._known_dirs: set[str] = set()
        self._known_slabs: set[str] = set()
        self._dir_lock = threading.Lock()
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in (self.slabs_dir, self.epgm_dir, self.manifest_dir):
            os.makedirs(d, exist_ok=True)
            self._known_dirs.add(d)

    def _ensure_dir(self, dirpath: str) -> None:
        if dirpath not in self._known_dirs:
            with self._dir_lock:
                if dirpath not in self._known_dirs:
                    os.makedirs(dirpath, exist_ok=True)
                    self._known_dirs.add(dirpath)

    def _slab_path(self, content_hash: str) -> str:
        prefix1 = content_hash[:2]
        prefix2 = content_hash[2:4]
        return os.path.join(self.slabs_dir, prefix1, prefix2, f"{content_hash}.slab")

    def _epgm_path(self, content_hash: str) -> str:
        prefix1 = content_hash[:2]
        prefix2 = content_hash[2:4]
        return os.path.join(self.epgm_dir, prefix1, prefix2, f"{content_hash}.epgm.json")

    def has_slab(self, content_hash: str) -> bool:
        """Check if a slab exists in storage."""
        if content_hash in self._known_slabs:
            return True
        exists = os.path.isfile(self._slab_path(content_hash))
        if exists:
            self._known_slabs.add(content_hash)
        return exists

    def put_slab(
        self,
        content: bytes,
        actor_seat: str = "unknown-seat",
        causal_parent: Optional[str] = None,
        labels: Optional[List[str]] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Store content and its EPGM provenance record into CAS."""
        content_hash = compute_sha256(content)
        slab_path = self._slab_path(content_hash)
        epgm_path = self._epgm_path(content_hash)

        self._ensure_dir(os.path.dirname(slab_path))
        self._ensure_dir(os.path.dirname(epgm_path))

        # Write slab content if not present
        if content_hash not in self._known_slabs and not os.path.isfile(slab_path):
            temp_slab = f"{slab_path}.tmp.{os.getpid()}_{time.time_ns()}"
            with open(temp_slab, "wb") as fp:
                fp.write(content)
            os.replace(temp_slab, slab_path)
            self._known_slabs.add(content_hash)

        # Build EPGM record
        now_iso = datetime.now(timezone.utc).isoformat()
        epgm_record: Dict[str, Any] = {
            "schema": "cas_epgm.v1",
            "content_hash": content_hash,
            "byte_size": len(content),
            "created_utc": now_iso,
            "actor_seat": actor_seat,
            "causal_parent": causal_parent,
            "labels": labels or [],
            "extra": extra or {},
        }

        # Save EPGM sidecar atomically
        temp_epgm = f"{epgm_path}.tmp.{os.getpid()}_{time.time_ns()}"
        with open(temp_epgm, "w", encoding="utf-8") as fp:
            json.dump(epgm_record, fp, indent=2, sort_keys=True)
        os.replace(temp_epgm, epgm_path)

        return epgm_record

    def get_slab(self, content_hash: str) -> Tuple[bytes, Dict[str, Any]]:
        """Retrieve slab content and its EPGM provenance record."""
        slab_path = self._slab_path(content_hash)
        epgm_path = self._epgm_path(content_hash)

        if not os.path.isfile(slab_path):
            raise KeyError(f"Slab not found for hash: {content_hash}")

        with open(slab_path, "rb") as fp:
            content = fp.read()

        actual_hash = compute_sha256(content)
        if actual_hash != content_hash:
            raise ValueError(f"Slab corrupted! Expected {content_hash}, got {actual_hash}")

        epgm_record: Dict[str, Any] = {}
        if os.path.isfile(epgm_path):
            with open(epgm_path, "r", encoding="utf-8") as fp:
                epgm_record = json.load(fp)

        return content, epgm_record

    def _find_files_parallel(self, base_dir: str, suffix: str) -> List[Tuple[str, str]]:
        """Fast parallel scanner across prefix sharding (standard library only)."""
        if not os.path.isdir(base_dir):
            return []
        items: List[Tuple[str, str]] = []
        p1_dirs: List[str] = []
        try:
            for e in os.scandir(base_dir):
                if e.is_file() and e.name.endswith(suffix):
                    items.append((e.name[:-len(suffix)], e.path))
                elif e.is_dir():
                    p1_dirs.append(e.path)
        except Exception:
            return []

        def _scan_p1(p1: str) -> List[Tuple[str, str]]:
            sub_items: List[Tuple[str, str]] = []
            try:
                for p2 in os.scandir(p1):
                    if p2.is_file() and p2.name.endswith(suffix):
                        sub_items.append((p2.name[:-len(suffix)], p2.path))
                    elif p2.is_dir():
                        for f in os.scandir(p2.path):
                            if f.name.endswith(suffix):
                                sub_items.append((f.name[:-len(suffix)], f.path))
            except Exception:
                pass
            return sub_items

        with ThreadPoolExecutor(max_workers=32) as pool:
            for sub in pool.map(_scan_p1, p1_dirs):
                items.extend(sub)

        return items

    def verify_mesh(self) -> Dict[str, Any]:
        """Perform a full integrity sweep across all stored CAS slabs."""
        total = 0
        valid = 0
        corrupted: List[str] = []
        missing_epgm: List[str] = []
        missing_parents: List[Dict[str, str]] = []

        # First pass: collect slab files in parallel
        slab_items = self._find_files_parallel(self.slabs_dir, ".slab")
        known_hashes = set()

        def _verify_slab(item: Tuple[str, str]) -> Tuple[str, bool]:
            expected_hash, slab_path = item
            try:
                with open(slab_path, "rb") as fp:
                    data = fp.read()
                return expected_hash, (compute_sha256(data) == expected_hash)
            except Exception:
                return expected_hash, False

        with ThreadPoolExecutor(max_workers=32) as pool:
            for exp_hash, ok in pool.map(_verify_slab, slab_items):
                total += 1
                if ok:
                    valid += 1
                    known_hashes.add(exp_hash)
                else:
                    corrupted.append(exp_hash)

        # Second pass: verify EPGM sidecars & causal links
        epgm_items = self._find_files_parallel(self.epgm_dir, ".epgm.json")

        def _check_epgm(item: Tuple[str, str]) -> Tuple[str, Optional[Dict[str, Any]]]:
            chash, epath = item
            try:
                with open(epath, "r", encoding="utf-8") as fp:
                    return chash, json.load(fp)
            except Exception:
                return chash, None

        with ThreadPoolExecutor(max_workers=32) as pool:
            for chash, rec in pool.map(_check_epgm, epgm_items):
                if chash not in known_hashes:
                    missing_epgm.append(chash)
                    continue
                if rec:
                    parent = rec.get("causal_parent")
                    if parent and parent not in known_hashes:
                        missing_parents.append({"child": chash, "missing_parent": parent})

        return {
            "schema": "cas_verify_report.v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_slabs": total,
            "valid_slabs": valid,
            "corrupted_count": len(corrupted),
            "corrupted_slabs": corrupted,
            "orphaned_epgm_count": len(missing_epgm),
            "missing_parent_links": missing_parents,
            "integrity_ok": (len(corrupted) == 0 and total == valid),
        }

    def export_mesh_manifest(self) -> Dict[str, Any]:
        """Generate a lightweight torrent/mesh broadcast manifest of all CAS slabs."""
        epgm_items = self._find_files_parallel(self.epgm_dir, ".epgm.json")

        def _load_manifest_item(item: Tuple[str, str]) -> Optional[Dict[str, Any]]:
            _, path = item
            try:
                with open(path, "r", encoding="utf-8") as fp:
                    rec = json.load(fp)
                return {
                    "hash": rec.get("content_hash"),
                    "bytes": rec.get("byte_size"),
                    "actor": rec.get("actor_seat"),
                    "parent": rec.get("causal_parent"),
                    "labels": rec.get("labels", []),
                }
            except Exception:
                return None

        slabs_list: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=32) as pool:
            for item in pool.map(_load_manifest_item, epgm_items):
                if item:
                    slabs_list.append(item)

        slabs_list.sort(key=lambda x: str(x.get("hash")))
        root_digest = hashlib.sha256(
            "".join(s["hash"] for s in slabs_list if s.get("hash")).encode("utf-8")
        ).hexdigest()

        manifest = {
            "schema": "cas_mesh_manifest.v1",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "slab_count": len(slabs_list),
            "mesh_root_hash": root_digest,
            "slabs": slabs_list,
        }

        # Bank manifest file
        stamp = int(time.time())
        mpath = os.path.join(self.manifest_dir, f"manifest_{stamp}_{root_digest[:8]}.json")
        with open(mpath, "w", encoding="utf-8") as fp:
            json.dump(manifest, fp, indent=2, sort_keys=True)

        return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Content-Addressable Storage Mesh CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # put
    p_put = subparsers.add_parser("put", help="Store content into CAS")
    p_put.add_argument("path", help="Path to file to store (or '-' for stdin)")
    p_put.add_argument("--actor", default="cli-operator", help="Actor seat id")
    p_put.add_argument("--parent", default=None, help="Causal parent hash")
    p_put.add_argument("--label", action="append", dest="labels", help="Labels for slab")

    # get
    p_get = subparsers.add_parser("get", help="Retrieve slab by hash")
    p_get.add_argument("hash", help="SHA-256 hash of slab")
    p_get.add_argument("--out", default=None, help="Output destination file")

    # verify
    subparsers.add_parser("verify", help="Verify integrity of all CAS slabs")

    # manifest
    subparsers.add_parser("manifest", help="Export CAS mesh manifest")

    args = parser.parse_args()
    mesh = CasMesh()

    if args.command == "put":
        if args.path == "-":
            data = sys.stdin.buffer.read()
        else:
            with open(args.path, "rb") as fp:
                data = fp.read()
        rec = mesh.put_slab(data, actor_seat=args.actor, causal_parent=args.parent, labels=args.labels)
        print(json.dumps(rec, indent=2))
        return 0

    elif args.command == "get":
        try:
            data, rec = mesh.get_slab(args.hash)
            if args.out:
                with open(args.out, "wb") as fp:
                    fp.write(data)
                print(f"Slab {args.hash} written to {args.out}")
            else:
                sys.stdout.buffer.write(data)
            return 0
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            return 1

    elif args.command == "verify":
        res = mesh.verify_mesh()
        print(json.dumps(res, indent=2))
        return 0 if res.get("integrity_ok") else 1

    elif args.command == "manifest":
        m = mesh.export_mesh_manifest()
        print(json.dumps(m, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
