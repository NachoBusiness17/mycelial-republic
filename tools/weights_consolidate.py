"""WEIGHTS CONSOLIDATE — one tracked home for all model weights.

Operator order, 2026-09-22: get rid of saelis, download the newest athena, keep all
weights in one place, trackable, no sacred cows. Use HF/LM Studio as tools, not masters.

Phase AUDIT (default): enumerate ollama blobs (content-addressed: the filename IS the
sha256) and LM Studio GGUFs; match pairs by exact size; sha256 the LM Studio side to
prove equality; hash every keeper; emit plan + manifest.
Phase --execute: delete verified duplicates + the saelis grave (replaced by athena),
write MANIFEST.json. Nothing deletes without hash-proof in this audit file.

Output: C:/Users/foste/models/MANIFEST.json (+ AUDIT file in watch/inbox).
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE", str(Path.home())))
OLLAMA = HOME / ".ollama" / "models"
LMSTUDIO = HOME / ".lmstudio" / "models"
CANON = HOME / "models"
ESTATE_INBOX = Path("C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox")
GRAVE = {"saelis-31b/v12d_athena_class_Q8_0_19JUL2026.gguf": "replaced by athena-class-model-a (same lineage, newer build 2026-09-22); operator order: get rid of saelis"}


def sha256_file(p: Path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="delete verified duplicates + graves after hash-proof")
    a = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    CANON.mkdir(parents=True, exist_ok=True)

    # ollama blobs: name is sha256-<hex>
    blobs = {}
    bdir = OLLAMA / "blobs"
    for p in bdir.glob("sha256-*"):
        blobs[p.stat().st_size] = p.name.removeprefix("sha256-")

    # lm studio ggufs
    lms = sorted(LMSTUDIO.rglob("*.gguf"))
    entries = []
    dup_bytes = 0
    for p in lms:
        rel = p.relative_to(LMSTUDIO).as_posix()
        size = p.stat().st_size
        e = {"file": rel, "size": size, "status": "keeper", "sha256": None}
        blob = blobs.get(size)
        if blob:
            e["suspect_pair"] = f"ollama:{blob[:16]}"
            e["sha256"] = sha256_file(p)
            if e["sha256"] == blob:
                e["status"] = "verified_duplicate"
                e["keep_blob"] = f"ollama:{blob[:16]}"
                dup_bytes += size
        if rel in GRAVE:
            e["status"] = "grave"
            e["reason"] = GRAVE[rel]
            if e["sha256"] is None:
                e["sha256"] = sha256_file(p)
        entries.append(e)

    manifest = {
        "schema": "weights_manifest.v1",
        "ts": now,
        "canonical_root": str(CANON),
        "stores": {
            "ollama_blobs": str(OLLAMA),
            "lmstudio": str(LMSTUDIO),
        },
        "weights": entries,
        "duplicates_verified_bytes": dup_bytes,
        "graves": [e for e in entries if e["status"] == "grave"],
        "downloads": [
            {
                "file": "athena/Athena-Class-31B-Model-A-Q8_0.gguf",
                "size_bytes": 30697345596,
                "source": "https://huggingface.co/slashreboot/athena-class-model-a/resolve/main/Athena-Class-31B-Model-A-Q8_0.gguf",
                "license": "apache-2.0",
                "status": "pending_download",
            }
        ],
    }

    out = CANON / "MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"WEIGHTS CONSOLIDATE {now}  execute={a.execute}")
    for e in entries:
        print(f"  {e['status']:20s} {e['file']:70s} {e['size']:>13,}")
    print(f"verified duplicate bytes: {dup_bytes:,}")
    if a.execute:
        for e in entries:
            if e["status"] in ("verified_duplicate", "grave"):
                p = LMSTUDIO / e["file"]
                if p.exists():
                    p.unlink()
                    print(f"  deleted {e['file']}")
        print(f"manifest: {out}")
    else:
        print("audit only — rerun with --execute to delete verified duplicates + graves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
