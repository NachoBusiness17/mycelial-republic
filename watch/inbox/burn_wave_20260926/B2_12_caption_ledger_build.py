#!/usr/bin/env python
"""B2-12 caption ledger builder (metadata only, zero model calls, zero media reads).

Sources (existing metadata only):
  watch/inbox/mrpool_export/ledger_full.jsonl   3663 rows, msg_id 1..4633, channel @MrPool_Q
  watch/inbox/mrpool_export/media_register.jsonl 2407 rows (2375 media_full + 32 media_matched), sha256
  disk: media_full/ (2375 files), media_matched/ (32 files), media/ (empty)

Row schema (one row per media id, sorted by date then msg_id):
  cite         handle + anchor per the dual-numbering rule, never bare msg_id
  msg_id       anchor in the @MrPool_Q harvest sequence (1..4633)
  date         post date YYYY-MM-DD (ledger row date, date part)
  datetime     full ledger date string
  kind         photo | video | pdf | webpage | poll
  media_type   raw ledger media_type (preserved, no lossy mapping)
  file_ext     raw ledger file_ext or null
  bytes        ledger file_size or null
  path         current storage path relative to mrpool_export/ (empty if no file)
  path_alt     sibling copy path (media_matched ids also live in media_full)
  sha256       register sha256 of path, re-verified against disk bytes at build
  caption      first 240 chars of the ledger row text (existing metadata only)
  caption_len  full length of the ledger row text
  caption_via  anchor of the same-date grouped album sibling carrying the
               album caption, when own text is empty (search order -1,+1,-2,+2,-3,+3)
  B2-423 POSITION LAW (2026-09-26, byte-verified): the album caption carrier
  sits on the FIRST member in 5 of the 6 B2-90 v2 albums (4595 in 4595..4600,
  3606 in 3606..3610, 2977 in 2977..2981, 1779 in 1779..1785, 1389 in
  1389..1393) and on the LAST member in 1 (4622 in 4618..4622): real sender
  variance, not a fold artifact. NO attribution rule may assume first-member;
  search the whole album run for the unique non-empty-text member. Falsifier
  executed live: a first-member-only rule re-empties msg 4618 while the other
  8 v2 targets still resolve (watch/inbox/burn_wave_20260926/
  B2_423_position_falsifier.json).
  status       have          file verified on disk (size match, sha256 match)
               metadata-only ledger metadata exists, file absent from export
               missing      file on disk with no ledger row (none found)

Output: watch/inbox/CAPTION_LEDGER_20260926.jsonl
Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "watch" / "inbox" / "mrpool_export"
OUT = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
HANDLE = "@MrPool_Q"
CAPTION_PREVIEW = 240
SIBLING_ORDER = (-1, 1, -2, 2, -3, 3)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    rows = []
    with open(EXPORT / "ledger_full.jsonl", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    byid = {r["msg_id"]: r for r in rows}

    reg = []
    with open(EXPORT / "media_register.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                reg.append(json.loads(line))
    # register row per exact path; matched copy wins as canonical (curated dedup target)
    reg_by_path = {r["file"]: r for r in reg}
    reg_ids = {}
    for r in reg:
        reg_ids.setdefault(r["msg_id"], []).append(r["file"])

    # disk truth
    disk = {}
    for d in ("media_full", "media_matched"):
        p = EXPORT / d
        if not p.exists():
            continue
        for fn in os.listdir(p):
            m = re.match(r"msg_(\d+)(\.\w+)$", fn)
            if m:
                disk[int(m.group(1))] = f"{d}/{fn}"

    ledger_file_ids = {r["msg_id"] for r in rows if r.get("media_type") and r.get("file_ext")}
    orphans = sorted(set(disk) - ledger_file_ids)

    def kind_of(r):
        ext = r.get("file_ext")
        if ext == ".jpg":
            return "photo"
        if ext in (".mp4", ".mov"):
            return "video"
        if ext == ".pdf":
            return "pdf"
        if r.get("media_type") == "MessageMediaPoll":
            return "poll"
        return "webpage"

    out_rows = []
    sha_mismatch = []
    size_mismatch = []
    unresolved_album = []
    for r in rows:
        if not r.get("media_type"):
            continue  # text-only message, not a media id
        mid = r["msg_id"]
        text = r.get("text") or ""
        cap = text.strip()
        cap_via = ""
        if not cap and r.get("grouped"):
            for d in SIBLING_ORDER:
                s = byid.get(mid + d)
                if s and s.get("grouped") and (s.get("text") or "").strip() \
                        and (s.get("date") or "")[:10] == (r.get("date") or "")[:10]:
                    cap_via = f"{HANDLE}#{s['msg_id']}"
                    break
            if not cap_via:
                unresolved_album.append(mid)
        ext = r.get("file_ext")
        path = ""
        path_alt = ""
        sha = None
        status = "missing"
        if ext:
            if mid in disk:
                path = disk[mid]
                alt = ("media_matched" if path.startswith("media_full/") else "media_full")
                if mid in reg_ids:
                    alts = [f for f in reg_ids[mid] if f != path]
                    if alts:
                        path_alt = alts[0]
                    # canonical preference: matched copy when it exists
                    matched = [f for f in reg_ids[mid] if f.startswith("media_matched/")]
                    if matched and path.startswith("media_full/"):
                        path, path_alt = matched[0], path
                rr = reg_by_path.get(path)
                if rr:
                    sha = rr.get("sha256")
                fp = EXPORT / path
                dsize = fp.stat().st_size
                if r.get("file_size") is not None and r["file_size"] != dsize:
                    size_mismatch.append(mid)
                if sha is not None and sha256_file(fp) != sha:
                    sha_mismatch.append(mid)
                status = "have"
            else:
                status = "metadata-only"
        else:
            status = "metadata-only"  # webpage preview / poll: ledger metadata only, no file in export
        out_rows.append({
            "cite": f"{HANDLE}#{mid}",
            "msg_id": mid,
            "date": (r.get("date") or "")[:10],
            "datetime": r.get("date"),
            "kind": kind_of(r),
            "media_type": r.get("media_type"),
            "file_ext": ext,
            "bytes": r.get("file_size"),
            "path": path,
            "path_alt": path_alt or None,
            "sha256": sha,
            "caption": cap[:CAPTION_PREVIEW],
            "caption_len": len(cap),
            "caption_via": cap_via,
            "status": status,
        })

    out_rows.sort(key=lambda x: (x["date"], x["msg_id"]))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for o in out_rows:
            f.write(json.dumps(o, ensure_ascii=True, sort_keys=True) + "\n")

    from collections import Counter
    print("rows:", len(out_rows))
    print("status:", dict(Counter(o["status"] for o in out_rows)))
    print("kind:", dict(Counter(o["kind"] for o in out_rows)))
    print("caption_via resolved:", sum(1 for o in out_rows if o["caption_via"]),
          "unresolved grouped:", len(unresolved_album), unresolved_album[:12])
    print("empty caption (caption_len==0):", sum(1 for o in out_rows if o["caption_len"] == 0))
    print("orphans (disk without ledger file-row):", len(orphans), orphans[:10])
    print("size mismatches ledger vs disk:", len(size_mismatch), size_mismatch[:10])
    print("sha256 mismatches register vs disk:", len(sha_mismatch), sha_mismatch[:10])
    print("sha256 covered:", sum(1 for o in out_rows if o["sha256"]))
    print("out:", OUT)

    # B2-421 caption_via verify pin (2026-09-26): a plain rebuild of this
    # builder cannot re-derive the 9 B2-90 v2 carriers (its +/-3 search order
    # is narrower than the v2 album-run rule), so the post-write gate below
    # turns that silent regression into a nonzero exit. Cause: B2-421 brief;
    # evidence: watch/inbox/burn_wave_20260926/B2_421_regressed_copy run
    # (exit 1 naming exactly the 9 rows) vs the landed ledger (111/111 green).
    # Keep the pin fixture (B2_421_caption_via_pin.json) in sync only with a
    # receipt naming why a carrier moved.
    import subprocess
    gate = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_421_caption_via_verify.py"
    rc = subprocess.call([sys.executable, str(gate), "--ledger", str(OUT)])
    if rc != 0:
        print("caption_via verify pin FAILED; rebuild output is regressed vs the pin")
        return rc
    # B2-409 have-row sha gate (2026-09-26): every have-row's sha256 must
    # recompute clean from disk bytes after any rebuild. The build-time
    # register-sha verification does not cover post-build drift; this gate
    # names any drifted path and fails the rebuild. Falsifier replay: flip
    # one byte in a scratch copy of a hashed file and the check exits 1
    # naming the DRIFT line (watch/inbox/burn_wave_20260926/
    # B2_409_caption_sha_pin_20260926.md).
    sha_gate = ROOT / "tools" / "caption_ledger_sha_check.py"
    rc = subprocess.call([sys.executable, str(sha_gate), "--ledger", str(OUT)])
    if rc != 0:
        print("have-row sha check FAILED; a hashed file drifted from its ledger sha")
        return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
