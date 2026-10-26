"""B2-385 promote: fill path/bytes/sha256/status into CAPTION_LEDGER rows
matched by cite from media_recovered_register_20260926.jsonl.

Fail-closed: every recovered file must exist and its on-disk sha256 must equal
the register sha BEFORE any ledger byte is written. In-place line patch
(B2-89/B2-90 precedent); row order and all other fields untouched.
Status semantics (decided in writing, see receipt): "have-recovered" = a file
on disk whose bytes hash to the recorded sha256, but the bytes are the
t.me/s web-preview thumb, not the original export media (register field
size_matches_export_metadata false throughout); "have" stays reserved for
original export media.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LEDGER = REPO / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
REGISTER = REPO / "watch" / "inbox" / "mrpool_export" / "media_recovered_register_20260926.jsonl"
MEDIA_DIR = REPO / "watch" / "inbox" / "mrpool_export"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    reg = [json.loads(l) for l in REGISTER.read_text(encoding="utf-8").splitlines() if l.strip()]
    # pass 1: verify every recovered file against the register before writing
    verified = {}
    for r in reg:
        f = MEDIA_DIR / r["file"]
        if not f.is_file():
            raise SystemExit(f"FAIL closed: recovered file missing: {f}")
        got = sha256_file(f)
        if got != r["sha256"]:
            raise SystemExit(f"FAIL closed: sha mismatch for {f}: disk {got} != register {r['sha256']}")
        verified[r["cite"]] = r

    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    patched = 0
    unmatched = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        row = json.loads(line)
        cite = row.get("cite", "")
        if cite in verified and (row.get("sha256") is None or row.get("sha256") == ""):
            r = verified[cite]
            row["path"] = r["file"]
            row["bytes"] = r["bytes"]
            row["sha256"] = r["sha256"]
            row["status"] = "have-recovered"
            row["recovered_provenance"] = r["provenance"]
            lines[i] = json.dumps(row, ensure_ascii=False)
            patched += 1
    unmatched = [c for c in verified if c not in {json.loads(l).get("cite", "") for l in lines if l.strip()}]

    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"patched": patched, "register_rows": len(reg),
                      "register_cites_absent_from_ledger": unmatched[:5],
                      "absent_count": len(unmatched)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
