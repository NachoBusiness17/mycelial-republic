#!/usr/bin/env python
"""B2-89 caption ledger sha256 fill (have-rows only, from recomputed disk bytes).

Input:  watch/inbox/CAPTION_LEDGER_20260926.jsonl  2726 rows (B2-12 build)
        have 2375 (path on disk; 32 carry register sha from media_matched,
        2343 media_full paths carry sha256 null), metadata-only 351
Source: sha256 recomputed from disk bytes of each have-row path; the 32
        pre-existing shas are re-verified before anything is written; the
        media_register.jsonl addendum rows (B2-89, rows 2408..4782) are the
        provenance for the 2343 media_full hashes.

Guarantees:
  row count and row order unchanged
  every non-sha field of every row byte-value identical
  rows that already carried sha256 keep the identical serialized line
  after the write every have-row's sha256 recomputes clean from disk

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_89_caption_ledger_sha_fill.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "watch" / "inbox" / "mrpool_export"
LEDGER = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dumps(o) -> str:
    return json.dumps(o, ensure_ascii=True, sort_keys=True) + "\n"


def main() -> int:
    pre_bytes = LEDGER.read_bytes()
    pre_lines = pre_bytes.decode("utf-8").splitlines()
    rows = [json.loads(l) for l in pre_lines if l.strip()]
    assert len(rows) == 2726, len(rows)

    filled, verified_existing, mismatches = 0, 0, []
    for i, r in enumerate(rows):
        if r["status"] != "have":
            continue
        fp = EXPORT / r["path"]
        digest = sha256_file(fp)
        if r.get("sha256"):
            verified_existing += 1
            if r["sha256"] != digest:
                mismatches.append((r["msg_id"], r["path"]))
            continue  # line must stay byte-identical
        if fp.stat().st_size != r["bytes"]:
            mismatches.append((r["msg_id"], r["path"], "size"))
        r["sha256"] = digest
        filled += 1
        pre_lines[i] = dumps(r).rstrip("\n")
    assert not mismatches, f"mismatches: {mismatches[:10]}"

    post_bytes = "".join(l + "\n" for l in pre_lines).encode("utf-8")
    LEDGER.write_bytes(post_bytes)

    # independent verify pass: reparse, every have-row sha recomputes clean
    out = [json.loads(l) for l in LEDGER.read_bytes().decode("utf-8").splitlines() if l.strip()]
    assert len(out) == 2726
    for old, new in zip(rows, out):
        assert {k: v for k, v in old.items() if k != "sha256"} \
               == {k: v for k, v in new.items() if k != "sha256"}, f"non-sha field moved: {old['msg_id']}"
    have = [r for r in out if r["status"] == "have"]
    missing = [r["msg_id"] for r in have if not r.get("sha256")]
    assert not missing, f"have rows still hashless: {missing[:10]}"
    bad = [r["msg_id"] for r in have if sha256_file(EXPORT / r["path"]) != r["sha256"]]
    assert not bad, f"post-write sha mismatches: {bad[:10]}"

    print("rows:", len(out))
    print("have:", len(have), "have with sha256:", sum(1 for r in have if r.get("sha256")))
    print("sha filled this run:", filled, "| pre-existing re-verified:", verified_existing)
    print("ledger pre sha256:", hashlib.sha256(pre_bytes).hexdigest())
    print("ledger post sha256:", hashlib.sha256(LEDGER.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
