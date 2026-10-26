"""qdrop_canonical -- the local-row to canonical-numbering guard (B2-404).

Root cause being guarded (frozen trajectory bytes,
memory/runs/compaction_eval/steps_frozen_20260920.jsonl line 6423): a counter
walked qdrops.jsonl, counted Q-authored rows (`n`), and printed "Q drop #874"
at n == 874. The 874th Q-authored row was the Think Bridge post (8ch post
967331, canonical drop #1104); canonical drop #874 is the Snowden HK post
(8ch post 580331). That one conflation cost the B2-14 sourcing pass and the
B2-93 erratum wave (watch/inbox/burn_wave_20260926/B2_93_stego_erratum_20260926.md).

THE PARALLEL NUMBERINGS a fresh reader must never conflate:
  1. canonical drop_no -- the qagg/qalerts-facing "drop #N" (what receipts
     mean by "drop #874"). qdrops.jsonl's drop_no FIELD is NOT this: it is
     the local renumbering (row 1088 of the file carries field drop_no 1088
     and IS canonical #874; B2-67 proved the fields diverge: local 200 =
     q_num 174, local 235 = q_num 200).
  2. local drop_no / row order -- the qdrops.jsonl drop_no field and its
     enumerate position (6,242 rows).
  3. Q-authored ordinal -- the count of rows passing the trip/name == Q
     filter (the 874th Q-authored row is the Think Bridge post, #1104).
(media_register.jsonl rows 119-120 after the B2-367 scope-header shift carry
yet another id space: 8ch media-file post ids.)

CANONICAL ANCHORS: canonical numbers are only minted from content-match
anchors filed in receipts (B2-14/B2-93: 580331 -> #874, 967331 -> #1104;
B2-67: 14 local fields -> q_num anchors). A row with no anchor resolves to
its LOCAL number with canonical=None and a warning: the helper refuses to
dress a local number as canonical.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QDROPS = HERE / "qdrops.jsonl"

# content-match anchors (id -> canonical drop_no), byte-anchored in receipts
# and re-verified live against qdrops.jsonl text by B2-404 (2026-09-26):
# B2-14/B2-93 (qagg+qalerts live-confirmed). B2-67's further local drop_no ->
# q_num pairs (14->15, 28->28, 51->52, 75->80, 109->125, 131->149, 149->169,
# 182->210, 184->215, 192->226, 193->227, 200->174, 235->200) are NOT id-keyed
# here yet: their 8ch post ids were not verified in this lane, and an
# unverified id in this table would be a minted number, the exact disease
# this module guards against. Anchor them by content match before adding.
CANONICAL_ANCHORS: dict[str, int] = {
    "580331": 874,    # Snowden HK post (B2-14/B2-93; text at local drop_no 1088)
    "967331": 1104,   # Think Bridge / central-algorithm post (B2-14/B2-93)
}


def load_qdrops(path: Path | None = None) -> list[dict]:
    p = Path(path) if path else QDROPS
    out = []
    with p.open(encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


def canonical_drop_no(qdrops: list[dict], *, id: str | None = None,
                      ts: str | None = None) -> dict:
    """Resolve a drop's number from id plus ts (both required: id pins the
    8ch post, ts confirms it; position and ordinal lookups are refused by
    construction). Returns the LOCAL drop_no always, plus canonical_drop_no
    only when a receipt-anchored mapping exists for the id -- never None
    dressed as a number."""
    if not id or not ts:
        raise ValueError("canonical_drop_no requires BOTH id and ts (no position lookups)")
    hits = [r for r in qdrops if str(r.get("id")) == str(id)]
    if not hits:
        raise ValueError(f"unknown qdrop id {id!r}: no row in qdrops.jsonl")
    if len(hits) > 1:
        raise ValueError(f"ambiguous qdrop id {id!r}: {len(hits)} rows")
    row = hits[0]
    if not str(row.get("ts", "")).startswith(str(ts)[:19]):
        raise ValueError(f"id {id!r} ts mismatch: row has {row.get('ts')!r}, got {ts!r}")
    canonical = CANONICAL_ANCHORS.get(str(id))
    out = {"local_drop_no": int(row["drop_no"]), "id": str(id),
           "ts": row.get("ts"), "canonical_drop_no": canonical,
           "canonical_anchored": canonical is not None}
    if canonical is None:
        out["warning"] = (f"no canonical anchor for id {id}: local drop_no "
                          f"{out['local_drop_no']} is NOT confirmed canonical; "
                          "anchor it via content match before printing a "
                          "'drop #N' string (B2-404)")
    return out


def q_authored_ordinal_guard(qdrops: list[dict], nth: int) -> dict:
    """Replicates the line-6423 counter shape (nth Q-authored row by trip/name
    filter) and returns the SAFE resolution plus a mandatory guard warning:
    the ordinal is NOT a drop number. Never prints 'Q drop #<ordinal>'."""
    n = 0
    hit = None
    for r in qdrops:
        if r.get("trip") == "!!Hs1Jq13jV6" or (r.get("name") or "").strip() == "Q":
            n += 1
            if n == nth:
                hit = r
                break
    if hit is None:
        raise ValueError(f"only {n} Q-authored rows; ordinal {nth} out of range")
    resolved = canonical_drop_no(qdrops, id=str(hit.get("id")),
                                 ts=str(hit.get("ts", "")))
    warning = (f"GUARD (B2-404): 'the {nth}th Q-authored row' is a local count, "
               f"NOT canonical drop #{nth}. That row is local drop_no "
               f"{resolved['local_drop_no']} (id {hit.get('id')})"
               + (f", canonical drop #{resolved['canonical_drop_no']}"
                  if resolved["canonical_anchored"] else "")
               + ". Print numbers only from resolved drop_no "
               "(qdrop_canonical.canonical_drop_no); the line-6423 counter "
               "minted the B2-93 erratum by printing the ordinal as a drop "
               "number.")
    return {"ordinal": nth, "id": str(hit.get("id")),
            "local_drop_no": resolved["local_drop_no"],
            "canonical_drop_no": resolved["canonical_drop_no"],
            "canonical_anchored": resolved["canonical_anchored"],
            "guard_warning": warning,
            "conflated": nth != resolved["local_drop_no"]}


def drop_label(local_drop_no: int, canonical_drop_no: int | None,
               id: str, ts: str) -> str:
    """The ONLY sanctioned 'drop #N' string: built from resolved fields, never
    from a position. Without an anchored canonical number the label says so
    explicitly instead of implying one."""
    if canonical_drop_no is None:
        return (f"local drop_no {int(local_drop_no)} (id {id}, ts {ts}; "
                "canonical number unanchored)")
    return f"canonical drop #{int(canonical_drop_no)} (id {id}, ts {ts})"


def main(argv: list[str] | None = None) -> int:
    """CLI: resolve by id+ts, or demo the guard on the historical 874 shape."""
    args = sys.argv[1:] if argv is None else argv
    qdrops = load_qdrops()
    if args and args[0] == "--guard" and len(args) >= 2:
        info = q_authored_ordinal_guard(qdrops, int(args[1]))
        print(info["guard_warning"])
        return 0 if not info["conflated"] else 2
    if len(args) >= 2:
        info = canonical_drop_no(qdrops, id=args[0], ts=args[1])
        print(drop_label(info["local_drop_no"], info["canonical_drop_no"],
                         info["id"], info["ts"]))
        return 0
    print("usage: qdrop_canonical.py <id> <ts> | --guard <nth-ordinal>")
    return 2


if __name__ == "__main__":
    sys.exit(main())
