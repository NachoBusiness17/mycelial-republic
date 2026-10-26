"""B2-83 one-off repair (2026-09-26 flash-lane burn, lane B2-83). REV 2.

Row 6868 flag metadata restore. The 04:17Z re-fold of knot
2026-09-03_1518_biography_mag-agen_cf523773.knot.json replaced the flagged
original row (filename 52737592, ts 2026-09-22) with a re-folded leaf row
(ts 2026-09-26T04:17:03Z, dossier cf523773) and kept evidence_lost=true but
dropped evidence_lost_reason + flagged_at. Pointer:
watch/inbox/burn_wave_20260926/B2_18_stone2b_20260926.md (Evidence F2).

Procedure copied from mag/_flag_dangling_20260925.py (the 031523Z flag run
that wrote the metadata being restored): backup first, single-writer
verkle_lock, row-scoped edit, integrity check after.

Merkle safety: chain verification consumes the stored leaf_hash field per row
(mag/verkle_knot.py:408-418 _rewrite uses row["leaf_hash"] directly), so this
edit, which appends two keys and touches no leaf_hash / verkle_root / index /
n_leaves value, leaves the merkle commitment and the (stale) tip unchanged by
construction.

Restored values are byte-derived at runtime from the surviving sibling row of
the same 031523Z flag run (verkle_chain.jsonl line 346, filename ff2435af),
which carries the exact reason string the flag run wrote
(mag/_flag_dangling_20260925.py:83-85) and flagged_at 20260926T031523Z, also
corroborated by the backup dir name memory/biography_backup_flag_20260926T031523Z.

REV 2 (fix comment carries the receipt): rev 1 restored the fields but its
Path.write_text call used default newline translation and rewrote every LF in
the 9873-line chain to CRLF on Windows (pre a43950f0 pure LF vs post 53b0224d
CRLF on all lines), caught by the post-run raw-byte diff against the backup.
This rev does byte-exact I/O only (read_bytes, split on b"\n", write_bytes via
tmp + os.replace) and first restores the pristine pre-state from the rev-1
backup memory/biography_backup_flag_20260926T164036Z/verkle_chain.jsonl
(sha256 a43950f0ebbe4b21d79fdd2464d5e06ecbf37bf1dc29d72d819f00cba67cadfa)
whenever the live bytes differ from it, so the net effect of this script over
the pristine bytes is exactly one changed line: line 6868.
"""
import hashlib
import json
import os
import shutil
import sys
import time
from contextlib import suppress
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
TIP = ROOT / "memory" / "biography" / "verkle_tip.json"
LOCK = ROOT / "memory" / "biography" / ".verkle.lock"
PRISTINE = ROOT / "memory" / "biography_backup_flag_20260926T164036Z" / "verkle_chain.jsonl"
PRISTINE_SHA = "a43950f0ebbe4b21d79fdd2464d5e06ecbf37bf1dc29d72d819f00cba67cadfa"
TARGET_FILENAME = "2026-09-03_1518_biography_mag-agen_cf523773.knot.json"
EXPECTED_LEAF_HASH = "14826f79dd210e7d08d1ee6b537ad5d00d21d776133ebd7708b72ca95625f3b0"
SIBLING_FILENAME = "2026-08-09_0343_biography_mag-agen_ff2435af.knot.json"
EXPECTED_FLAGGED_AT = "20260926T031523Z"

ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

sys.path.insert(0, str(ROOT))
from mag import verkle_knot as vk  # noqa: E402


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def merkle_over_column(raw: bytes) -> str:
    hashes = [
        json.loads(ln.decode("utf-8"))["leaf_hash"]
        for ln in raw.rstrip(b"\n").split(b"\n")
        if ln.strip()
    ]
    return vk._merkle_root(hashes)


# 0) restore pristine pre-state if a prior rev damaged it, else back up first
live = CHAIN.read_bytes()
if b"\r" in live:
    if sha(PRISTINE.read_bytes()) != PRISTINE_SHA:
        sys.exit("pristine backup hash mismatch - aborting, no write done")
    shutil.copy2(PRISTINE, CHAIN)
    print("restored pristine pre-state from", PRISTINE.name, sha(PRISTINE.read_bytes()))
    live = CHAIN.read_bytes()
else:
    bak = ROOT / "memory" / f"biography_backup_flag_{ts}"
    bak.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CHAIN, bak / "verkle_chain.jsonl")
    shutil.copy2(TIP, bak / "verkle_tip.json")
    print("backup ->", bak)

before_verify = vk._verify_chain_consistent()
before_merkle = merkle_over_column(live)
before_sha = sha(live)
print("before_verify:", before_verify)
print("before_merkle:", before_merkle)
print("before_sha256:", before_sha)

# 1) single-writer lock (precedent step 1, verbatim timings)
wait_until = time.time() + 600
while LOCK.is_file():
    if time.time() > wait_until:
        sys.exit("lock held >10min by another writer - aborting, no write done")
    if time.time() - LOCK.stat().st_mtime > 900:
        LOCK.unlink()  # crashed holder
        break
    time.sleep(1.0)
acquired = False
for _ in range(1200):
    try:
        fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"pid={os.getpid()} ts={ts}".encode())
        os.close(fd)
        acquired = True
        break
    except FileExistsError:
        if LOCK.is_file() and time.time() - LOCK.stat().st_mtime > 900:
            LOCK.unlink()
        time.sleep(0.05)
if not acquired:
    sys.exit("verkle_lock timeout - aborting, no write done")

try:
    # fresh bytes INSIDE the lock (claim law: re-read before edit)
    raw = CHAIN.read_bytes()
    if b"\r" in raw:
        sys.exit("live chain carries CR bytes - aborting, no write done")
    lines = raw.rstrip(b"\n").split(b"\n")
    sibling_reason = None
    sibling_flagged_at = None
    target_idx = None
    for i, ln in enumerate(lines):
        row = json.loads(ln.decode("utf-8"))
        if row.get("filename") == SIBLING_FILENAME:
            sibling_reason = row.get("evidence_lost_reason")
            sibling_flagged_at = row.get("flagged_at")
        if row.get("filename") == TARGET_FILENAME:
            if target_idx is not None:
                sys.exit("multiple target rows - aborting, no write done")
            target_idx = i
    if target_idx is None:
        sys.exit("target row not found - aborting, no write done")
    if sibling_reason is None or sibling_flagged_at != EXPECTED_FLAGGED_AT:
        sys.exit("sibling flag row lacks the 031523Z metadata - aborting, no write done")

    row = json.loads(lines[target_idx].decode("utf-8"))
    if row.get("leaf_hash") != EXPECTED_LEAF_HASH:
        sys.exit("target leaf_hash is not the pinned value - aborting, no write done")
    if not row.get("evidence_lost"):
        sys.exit("target row not flagged evidence_lost - aborting, no write done")
    if "evidence_lost_reason" in row or "flagged_at" in row:
        sys.exit("target row already carries the metadata - aborting, no write done")

    # the restore itself: append the two dropped keys, touch nothing else
    row["evidence_lost_reason"] = sibling_reason
    row["flagged_at"] = sibling_flagged_at
    new_line = json.dumps(row, ensure_ascii=False).encode("utf-8")
    out_lines = list(lines)
    out_lines[target_idx] = new_line
    out_raw = b"\n".join(out_lines) + b"\n"

    # structural safety: exactly one line differs, leaf_hash column untouched
    changed = [i for i, (a, b) in enumerate(zip(lines, out_lines)) if a != b]
    if changed != [target_idx]:
        sys.exit(f"unexpected changed lines {changed} - aborting, no write done")
    if merkle_over_column(out_raw) != before_merkle:
        sys.exit("leaf_hash merkle would change - aborting, no write done")

    # byte-exact atomic write (rev 2; see module docstring)
    tmp = CHAIN.with_name(CHAIN.name + f".b2_83_tmp_{ts}")
    tmp.write_bytes(out_raw)
    os.replace(tmp, CHAIN)
    print(f"RESTORED row line {target_idx + 1}: evidence_lost_reason + flagged_at={sibling_flagged_at}")
finally:
    if acquired:
        with suppress(OSError):
            LOCK.unlink()

# 2) integrity check after the edit (precedent step 2)
after_raw = CHAIN.read_bytes()
after_verify = vk._verify_chain_consistent()
after_merkle = merkle_over_column(after_raw)
after_sha = sha(after_raw)
after_row = json.loads(after_raw.rstrip(b"\n").split(b"\n")[target_idx].decode("utf-8"))
print("after_verify:", after_verify)
print("after_merkle:", after_merkle)
print("after_sha256:", after_sha)
print("cr_bytes_on_disk:", b"\r" in after_raw)
print("merkle_unchanged:", after_merkle == before_merkle)
print("verify_unchanged:", after_verify == before_verify)
print("leaf_hash_unchanged:", after_row["leaf_hash"] == EXPECTED_LEAF_HASH)
print("reason_on_row:", after_row.get("evidence_lost_reason"))
print("flagged_at_on_row:", after_row.get("flagged_at"))
