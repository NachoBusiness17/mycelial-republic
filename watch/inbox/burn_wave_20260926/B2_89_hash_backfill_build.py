#!/usr/bin/env python
"""B2-89 hash backfill for media_full (append-only addendum to media_register.jsonl).

State at lane start (verified against bytes 2026-09-26):
  watch/inbox/mrpool_export/media_register.jsonl  2407 rows
    rows 1..32   media_matched/msg_NNNN.ext  sha256 present
    rows 33..2407 media_full/msg_NNNN.ext    sha256 ABSENT (hashless), bytes present
  disk: media_full/ 2375 files, media_matched/ 32 files, register covers both exactly

What this script does:
  pass 1  compute sha256 from disk bytes for every media_full file (2375) and
          every media_matched file (32, re-verifying the register's 32 shas)
  append  one dated addendum row per media_full file AFTER row 2407, in the
          same order the hashless rows appear in the register (addendum row
          2408+i maps 1:1 onto hashless register row 33+i), carrying
          msg_id, date, file, sha256, bytes, computed_at, lane, provenance
  verify  rows 1..2407 byte-identical (file prefix equal to pre-append bytes),
          row count 4782, exactly one addendum row per media_full basename,
          addendum bytes == disk size, and pass 2 recomputes the sha256 of all
          2407 sha-bearing rows against disk bytes, any mismatch aborts

Never rewrites rows 1..2407: the append is done in 'ab' mode and the prefix is
verified byte-for-byte after the write.

Output: watch/inbox/burn_wave_20260926/B2_89_hash_backfill_results.json
Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_89_hash_backfill_build.py
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "watch" / "inbox" / "mrpool_export"
REG = EXPORT / "media_register.jsonl"
RESULTS = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_89_hash_backfill_results.json"
LANE = "B2-89"
PROVENANCE = "hash_backfill_addendum_20260926"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pre_bytes = REG.read_bytes()
    pre_sha = hashlib.sha256(pre_bytes).hexdigest()
    pre_lines = pre_bytes.decode("utf-8").splitlines()
    pre_rows = [json.loads(l) for l in pre_lines if l.strip()]
    assert len(pre_rows) == 2407, f"expected 2407 register rows, found {len(pre_rows)}"

    hashless = [r for r in pre_rows if not r.get("sha256")]
    matched = [r for r in pre_rows if r.get("sha256")]
    assert all(r["file"].startswith("media_full/") for r in hashless), "hashless row outside media_full"
    assert all(r["file"].startswith("media_matched/") for r in matched), "sha row outside media_matched"
    assert len(hashless) == 2375 and len(matched) == 32, (len(hashless), len(matched))

    # pass 1: hash every media_full file from disk bytes
    addendum = []
    disk_full = {f: EXPORT / "media_full" / f for f in os.listdir(EXPORT / "media_full")}
    assert len(disk_full) == 2375, len(disk_full)
    hash_total = 0
    for r in hashless:
        base = r["file"].split("/", 1)[1]
        fp = disk_full.pop(base)  # exactly-once: pops, so a dup register row would KeyError
        size = fp.stat().st_size
        assert size == r["bytes"], f"size mismatch {r['file']}: register {r['bytes']} disk {size}"
        digest = sha256_file(fp)
        hash_total += size
        addendum.append({
            "msg_id": r["msg_id"],
            "date": r["date"],
            "file": r["file"],
            "sha256": digest,
            "bytes": size,
            "computed_at": ts,
            "lane": LANE,
            "provenance": PROVENANCE,
        })
    assert not disk_full, f"disk files with no register row: {sorted(disk_full)[:5]}"

    # cross-check: the 32 register sha256 values recompute clean against matched bytes
    for r in matched:
        fp = EXPORT / r["file"]
        assert fp.stat().st_size == r["bytes"], f"matched size mismatch {r['file']}"
        assert sha256_file(fp) == r["sha256"], f"register sha mismatch {r['file']}"

    # append-only write: 'ab' mode, then verify the prefix is byte-identical
    blob = "".join(json.dumps(a, ensure_ascii=True, sort_keys=True) + "\n" for a in addendum).encode("utf-8")
    with open(REG, "ab") as f:
        f.write(blob)
    post_bytes = REG.read_bytes()
    assert post_bytes[: len(pre_bytes)] == pre_bytes, "FATAL: rows 1..2407 bytes changed"
    assert post_bytes[len(pre_bytes):] == blob, "appended bytes differ from drafted blob"
    post_lines = post_bytes.decode("utf-8").splitlines()
    post_rows = [json.loads(l) for l in post_lines if l.strip()]
    assert len(post_rows) == 4782, len(post_rows)
    for old, new in zip(pre_rows, post_rows[:2407]):
        assert old == new, f"row mutated: {old['file']}"
    basenames = [a["file"].split("/", 1)[1] for a in addendum]
    assert len(set(basenames)) == 2375, "duplicate addendum basename"

    # pass 2: recompute every sha-bearing row (2407) against disk bytes, independent read
    mismatches = []
    for r in post_rows:
        if not r.get("sha256"):
            continue
        fp = EXPORT / r["file"]
        if fp.stat().st_size != r["bytes"] or sha256_file(fp) != r["sha256"]:
            mismatches.append(r["file"])
    assert not mismatches, f"pass-2 sha mismatches: {mismatches[:10]}"

    results = {
        "ts": ts,
        "lane": LANE,
        "register_pre_sha256": pre_sha,
        "register_post_sha256": hashlib.sha256(post_bytes).hexdigest(),
        "register_rows_before": 2407,
        "register_rows_after": 4782,
        "addendum_rows_appended": len(addendum),
        "addendum_first_row": post_lines[2407][:160],
        "addendum_last_row": post_lines[-1][:160],
        "bytes_hashed_pass1": hash_total,
        "bytes_hashed_pass2": hash_total + sum(r["bytes"] for r in matched),
        "sha_mismatches_pass2": 0,
        "rows_1_to_2407_byte_identical": True,
    }
    RESULTS.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
