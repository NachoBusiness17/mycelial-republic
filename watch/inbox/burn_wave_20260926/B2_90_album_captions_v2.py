#!/usr/bin/env python
"""B2-90 album captions v2: fill caption_via on the 9 unresolved grouped ids.

Input:  watch/inbox/CAPTION_LEDGER_20260926.jsonl  2726 rows (B2-12 build, B2-89 sha fill)
        watch/inbox/mrpool_export/ledger_full.jsonl  3663 rows (source of truth)
Targets: 4618 4600 4599 3610 2981 1785 1784 1783 1393 (empty text, grouped=True,
        no same-date grouped sibling with text within +/-3, per B2-12 search order)

Rule (v2): widen the same-date grouped carrier window. An album is the maximal
run of grouped=True source messages contiguous in msg_id with consecutive
timestamps no more than 60s apart (runs 4600/4601 split correctly: 4.4h apart).
The carrier is the unique album member with non-empty text; every one of the 9
resolves to exactly one carrier at msg_id distance 4..6, same calendar date,
strictly outside B2-12's +/-3 search order. No non-grouped neighbors are used,
no external fetch is needed.

Guarantees:
  row count and row order unchanged
  2717 of 2726 lines byte-identical after the write
  each of the 9 patched rows changes ONLY caption_via (filled with
  @MrPool_Q#<carrier>) and gains caption_via_v2="2026-09-26"
  caption field stays empty for all 9 (B2-12 via-row precedent)

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "watch" / "inbox" / "mrpool_export" / "ledger_full.jsonl"
LEDGER = ROOT / "watch" / "inbox" / "CAPTION_LEDGER_20260926.jsonl"
TARGETS = [4618, 4600, 4599, 3610, 2981, 1785, 1784, 1783, 1393]
V2_DATE = "2026-09-26"


def dumps(o) -> str:
    return json.dumps(o, ensure_ascii=True, sort_keys=True) + "\n"


def main() -> int:
    src = {}
    for line in SOURCE.open(encoding="utf-8"):
        r = json.loads(line)
        src[r["msg_id"]] = r

    pre_bytes = LEDGER.read_bytes()
    pre_sha = hashlib.sha256(pre_bytes).hexdigest()
    lines = pre_bytes.decode("utf-8").splitlines()
    rows = [json.loads(l) for l in lines if l.strip()]
    assert len(rows) == 2726, len(rows)
    by_id = {r["msg_id"]: i for i, r in enumerate(rows)}

    def parse(ms):  # source dates look like 2026-09-14T12:01:34+00:00
        return datetime.fromisoformat(src[ms]["date"])

    def album_of(mid):
        album = [mid]
        for direction in (-1, 1):
            m = mid
            while True:
                nxt = m + direction
                if nxt not in src or not src[nxt]["grouped"]:
                    break
                if abs((parse(nxt) - parse(m)).total_seconds()) > 60:
                    break
                album.append(nxt)
                m = nxt
        return sorted(set(album))

    resolved, problems = {}, []
    for mid in TARGETS:
        t = src[mid]
        assert t["grouped"] is True, (mid, "target not grouped in source")
        assert not (t.get("text") or "").strip(), (mid, "target has text")
        day = t["date"][:10]
        album = album_of(mid)
        carriers = [m for m in album if (src[m].get("text") or "").strip()]
        if len(carriers) != 1:
            problems.append((mid, f"album {album} carriers {carriers}"))
            continue
        carrier = carriers[0]
        dist = abs(carrier - mid)
        # same calendar date must hold for the carrier (same-date rule kept)
        if src[carrier]["date"][:10] != day:
            problems.append((mid, carrier, "cross-date carrier"))
        # B2-12 window was +/-3; every v2 carrier must sit strictly outside it,
        # otherwise B2-12 should already have resolved this row
        if dist <= 3:
            problems.append((mid, f"carrier {carrier} within old +/-3 window"))
        resolved[mid] = (carrier, dist, len(album), src[carrier]["text"])

    if problems:
        for p in problems:
            print("PROBLEM:", p)
        return 2

    for mid in TARGETS:
        assert mid in by_id, mid
        row = rows[by_id[mid]]
        assert row["caption"] == "" and row["caption_len"] == 0, mid
        assert row["caption_via"] == "", mid

    patched = list(rows)
    for mid in TARGETS:
        carrier, dist, _, _ = resolved[mid]
        i = by_id[mid]
        old = dict(patched[i])
        new = dict(old)
        new["caption_via"] = f"@MrPool_Q#{carrier}"
        new["caption_via_v2"] = V2_DATE
        assert set(new) - set(old) == {"caption_via_v2"}
        patched[i] = new

    new_lines = []
    patched_ids = set()
    for i, (old_line, new_row) in enumerate(zip(lines, patched)):
        if old_line.strip() and json.loads(old_line) != new_row:
            old_row = json.loads(old_line)
            diff = {k for k in set(old_row) | set(new_row)
                    if old_row.get(k) != new_row.get(k)}
            assert diff == {"caption_via", "caption_via_v2"}, (new_row["msg_id"], diff)
            patched_ids.add(new_row["msg_id"])
            new_lines.append(dumps(new_row).rstrip("\n"))
        else:
            new_lines.append(old_line)
    assert patched_ids == set(TARGETS), patched_ids ^ set(TARGETS)
    assert len(new_lines) == len(lines) == 2726

    out = "\n".join(new_lines) + "\n"
    byte_identical = sum(1 for a, b in zip(lines, new_lines) if a == b)
    LEDGER.write_bytes(out.encode("utf-8"))
    post_sha = hashlib.sha256(LEDGER.read_bytes()).hexdigest()

    print(f"pre  sha256 {pre_sha}")
    print(f"post sha256 {post_sha}")
    print(f"rows 2726, lines byte-identical {byte_identical}/2726, patched {len(patched_ids)}")
    for mid in TARGETS:
        carrier, dist, n_album, text = resolved[mid]
        prev = " ".join(text.split())[:90]
        print(f"{mid} -> carrier @MrPool_Q#{carrier} dist={dist} album_size={n_album} cap_len={len(text)} :: {prev}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
