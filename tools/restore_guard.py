#!/usr/bin/env python3
"""restore_guard.py - stale-base whole-file restore tripwire (B2-343, 2026-09-26).

The disease this meters (brief: watch/inbox/burn_wave_20260926/QUEUE.md row
B2-343): B2-328's byte-identical host restore at 16:35:35Z (snapshot sha
F60955A2D8E0085B..., recorded in its receipt and LEDGER row) wrote
scripts/index_fold_host.mjs back to a pre-claim snapshot and erased B2-329's
landed edit for about two minutes. The shared-file claim law had no detection
surface for it: the restore is a whole-file write the claim law never gates,
and B2-329's claim line was already retired to CLAIMED, which drops it from
the replay probe's active-claim detection, so nothing named the restore at
write time. The erase was caught two minutes late by a pin test going red.

Two arms, one law (the restore-guard paragraph in the QUEUE.md header):

  check   Pre-write arm. Run BEFORE a whole-file restore lands:

            python tools/restore_guard.py check --path <repo-relative-path> \
                --file <absolute-path-to-target> --snapshot-sha <sha256> \
                --snapshot-ts <ISO8601Z> [--board QUEUE.md]

          Fails (exit 1) when any claim line on the board for --path was
          filed AFTER --snapshot-ts and the current --file bytes differ from
          --snapshot-sha, i.e. the write would move the file to a snapshot
          older than a claim filed after it. RETIRED (CLAIMED) lines count:
          a restore is exactly the case where retired claims still own bytes
          on disk. Passes as a no-op when the current bytes already equal the
          snapshot sha (nothing can be erased). On green it reminds the
          restorer to record the pre-write sha in the landing note.

  audit   Post-hoc arm (the patrol / refold-gate shape). Reads restore
          records from memory/burns/LEDGER.jsonl rows and fails when a
          recorded restore's bytes STILL STAND (current file sha equals the
          recorded pre-write sha, full or recorded prefix) while a claim for
          that path was filed after the record's snapshot ts. Records:

            structured  row["restore"] = {"path", "pre_write_sha",
                        "snapshot_ts"} (the law for new restores)
            legacy      prose "restored byte-identical sha256 <8..64 hex>"
                        in the row's one_line (B2-328's row shape); a legacy
                        record has no path and no snapshot ts, so it is
                        attributed to --path when one is given (disclosed in
                        the output) and printed informational-only when not;
                        a STANDING legacy record cannot prove its snapshot
                        postdates the claims, so it fails closed.

Exit codes: 0 = guard holds; 1 = stale-base restore named; 2 = cannot verify
(missing board, ledger, or target file). Line contract: prints
"RESTORE-GUARD: ok (...)" or "RESTORE-GUARD: FAIL ..."; tools/refold_gate.py
runs the audit for the fold host and folds a FAIL into its own FAIL channel
so the B2-328 pre-push gate names a stale-base restore.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BOARD = _REPO_ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
DEFAULT_LEDGER = _REPO_ROOT / "memory" / "burns" / "LEDGER.jsonl"

# Claim grammar per the QUEUE.md header law: - CLAIM <lane> <path> <ts> (<reason>)
# The restore guard ALSO matches retired lines: "- CLAIMED ..." is the same
# claim after in-place retirement, and its bytes still own the disk until a
# rebase lands. The B2-250 replay probe's active-only regex is the surface
# that was blind to the 16:35:35Z restore; this one is not.
CLAIM_LINE_RE = re.compile(
    r"(?m)^- (CLAIM|CLAIMED) (\S+) (\S+) (\S+)(?: \(([^)]*)\))?"
)

# Legacy restore record: B2-328's LEDGER one_line carries the restored sha as
# prose. 8 hex chars (the short form) up to a full 64-char sha256.
LEGACY_RESTORE_RE = re.compile(
    r"restored byte-identical sha256 ([0-9A-Fa-f]{8,64})"
)

TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")


class CannotVerify(Exception):
    """Board, ledger, or target bytes are missing: exit 2, never a green lie."""


def parse_ts(text):
    """Parse an ISO8601 Z timestamp into an aware UTC datetime."""
    if not TS_RE.match(text or ""):
        raise ValueError("not an ISO8601 Z timestamp: %r" % (text,))
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def norm_path(text):
    """Normalize a repo-relative path key to forward slashes."""
    return (text or "").replace("\\", "/").strip()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_board_claims(board_path):
    """All claim lines (active and retired) from the board bytes."""
    data = Path(board_path).read_bytes().decode("utf-8", errors="replace")
    claims = []
    for m in CLAIM_LINE_RE.finditer(data):
        claims.append(
            {
                "kind": m.group(1),
                "lane": m.group(2),
                "path": norm_path(m.group(3)),
                "ts": m.group(4),
                "reason": (m.group(5) or "").strip(),
            }
        )
    return claims


def claims_for_path(claims, path):
    """Claims for one repo-relative path, ts-parsable ones first."""
    good, bad = [], []
    for c in claims:
        if c["path"] != path:
            continue
        try:
            c["when"] = parse_ts(c["ts"])
            good.append(c)
        except ValueError:
            bad.append(c)
    return good, bad


def is_standing(current_sha, recorded_sha):
    """Current bytes carry the recorded restore sha (full or prefix)."""
    cur, rec = current_sha.lower(), recorded_sha.lower()
    if len(rec) == 64:
        return cur == rec
    return cur.startswith(rec)


def load_records(ledger_path):
    """Restore records from LEDGER rows: structured objects plus legacy prose."""
    records = []
    with open(ledger_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            slug = row.get("slug") or row.get("ts") or "?"
            rec = row.get("restore")
            if isinstance(rec, dict) and rec.get("path") and rec.get("pre_write_sha"):
                records.append(
                    {
                        "kind": "structured",
                        "slug": slug,
                        "path": norm_path(rec.get("path")),
                        "sha": str(rec.get("pre_write_sha")),
                        "snapshot_ts": rec.get("snapshot_ts"),
                        "line_no": len(records) + 1,
                    }
                )
                continue
            text = " ".join(
                str(row.get(k) or "") for k in ("one_line", "notes", "landing")
            )
            for m in LEGACY_RESTORE_RE.finditer(text):
                records.append(
                    {
                        "kind": "legacy",
                        "slug": slug,
                        "path": None,
                        "sha": m.group(1),
                        "snapshot_ts": None,
                        "line_no": len(records) + 1,
                    }
                )
    return records


def cmd_check(args):
    board = Path(args.board)
    target = Path(args.file)
    if not board.is_file():
        raise CannotVerify("board not found: %s" % board)
    if not target.is_file():
        raise CannotVerify("target file not found: %s" % target)
    snap_ts = parse_ts(args.snapshot_ts)
    snap_sha = args.snapshot_sha.strip().lower()
    if len(snap_sha) != 64 or not re.fullmatch(r"[0-9a-f]{64}", snap_sha):
        raise CannotVerify("--snapshot-sha must be a full 64-char sha256")
    current = sha256_file(target)
    path = norm_path(args.path)
    if current == snap_sha:
        print(
            "RESTORE-GUARD: ok (no-op restore: current bytes of %s already "
            "equal the snapshot sha %s; nothing can be erased)" % (path, snap_sha[:8])
        )
        return 0
    claims = read_board_claims(board)
    good, bad = claims_for_path(claims, path)
    for c in bad:
        print(
            "RESTORE-GUARD: note, unparsable claim ts on %s line skipped: %s"
            % (path, c["ts"])
        )
    stale = [c for c in good if c["when"] > snap_ts]
    if stale:
        print(
            "RESTORE-GUARD: FAIL, stale-base whole-file restore named before "
            "it lands:"
        )
        print(
            "  target %s: current sha %s would move back to snapshot sha %s "
            "taken %s" % (path, current[:8], snap_sha[:8], args.snapshot_ts)
        )
        for c in stale:
            print(
                "  %s %s filed %s (%s): the snapshot predates this claim; "
                "re-read the current bytes and rebase per the claim law, or "
                "land first and make the restore a rebase"
                % (
                    "active CLAIM" if c["kind"] == "CLAIM" else "retired CLAIMED",
                    c["lane"],
                    c["ts"],
                    c["reason"] or "no reason given",
                )
            )
        return 1
    print(
        "RESTORE-GUARD: ok (no claim for %s filed after snapshot ts %s; "
        "restore may proceed, record the pre-write sha %s in the landing "
        "note and LEDGER row)" % (path, args.snapshot_ts, snap_sha[:8])
    )
    return 0


def cmd_audit(args):
    root = Path(args.root).resolve()
    board = Path(args.board)
    ledger = Path(args.ledger)
    if not board.is_file():
        raise CannotVerify("board not found: %s" % board)
    if not ledger.is_file():
        raise CannotVerify("ledger not found: %s" % ledger)
    path_filter = norm_path(args.path) if args.path else None
    claims = read_board_claims(board)
    records = load_records(ledger)
    checked, historical, standing_stale = 0, 0, 0
    informational = 0
    for rec in records:
        if rec["kind"] == "structured":
            if path_filter and rec["path"] != path_filter:
                continue
            attributed_to = rec["path"]
        else:
            if not path_filter:
                informational += 1
                print(
                    "RESTORE-GUARD: note, legacy restore record %s (row %s) "
                    "has no path; pass --path to attribute and check it"
                    % (rec["sha"][:8], rec["slug"])
                )
                continue
            attributed_to = path_filter
        checked += 1
        target = root / attributed_to
        if not target.is_file():
            print(
                "RESTORE-GUARD: note, restore record %s target %s not on "
                "disk, skipped" % (rec["sha"][:8], attributed_to)
            )
            continue
        current = sha256_file(target)
        if not is_standing(current, rec["sha"]):
            historical += 1
            print(
                "RESTORE-GUARD: note, restore record %s (%s, %s) is "
                "historical: current sha %s no longer carries it"
                % (rec["sha"][:8], rec["slug"], attributed_to, current[:8])
            )
            continue
        good, _ = claims_for_path(claims, attributed_to)
        if rec["snapshot_ts"]:
            snap_ts = parse_ts(rec["snapshot_ts"])
            stale = [c for c in good if c["when"] > snap_ts]
            reason = "claims filed after snapshot ts %s" % rec["snapshot_ts"]
        else:
            stale = good
            reason = (
                "legacy record carries no snapshot ts, so it cannot prove "
                "the snapshot postdates these claims (fail-closed)"
            )
        if stale:
            standing_stale += 1
            print(
                "RESTORE-GUARD: FAIL, a restored snapshot's bytes still stand "
                "on claimed work:"
            )
            print(
                "  record %s (%s row %s) stands on %s (current sha %s); %s"
                % (rec["sha"][:8], rec["kind"], rec["slug"], attributed_to,
                   current[:8], reason)
            )
            for c in stale:
                print(
                    "  %s %s filed %s (%s): rebase the file past the claim or "
                    "re-record the restore with its true snapshot ts"
                    % (
                        "active CLAIM"
                        if c["kind"] == "CLAIM"
                        else "retired CLAIMED",
                        c["lane"],
                        c["ts"],
                        c["reason"] or "no reason given",
                    )
                )
    if standing_stale:
        print(
            "RESTORE-GUARD: FAIL, %d standing stale restore(s) over %d "
            "checked (%d historical, %d informational)"
            % (standing_stale, checked, historical, informational)
        )
        return 1
    print(
        "RESTORE-GUARD: ok (audit: %d record(s) checked, %d historical, "
        "%d informational, 0 standing stale)" % (checked, historical, informational)
    )
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="pre-write arm: name a stale-base restore before it lands")
    p_check.add_argument("--path", required=True, help="repo-relative board path key")
    p_check.add_argument("--file", required=True, help="absolute path to the bytes about to be written")
    p_check.add_argument("--snapshot-sha", required=True, help="sha256 of the snapshot bytes")
    p_check.add_argument("--snapshot-ts", required=True, help="ISO8601 Z ts the snapshot was taken")
    p_check.add_argument("--board", default=str(DEFAULT_BOARD), help="board path (default %(default)s)")
    p_check.set_defaults(func=cmd_check)

    p_audit = sub.add_parser("audit", help="post-hoc arm: name a landed restore standing on claimed work")
    p_audit.add_argument("--path", default=None, help="restrict to and attribute pathless legacy records to this repo-relative path")
    p_audit.add_argument("--board", default=str(DEFAULT_BOARD), help="board path (default %(default)s)")
    p_audit.add_argument("--ledger", default=str(DEFAULT_LEDGER), help="ledger path (default %(default)s)")
    p_audit.add_argument("--root", default=str(_REPO_ROOT), help="repo root (default: script parent)")
    p_audit.set_defaults(func=cmd_audit)

    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except CannotVerify as exc:
        print("RESTORE-GUARD: FAIL, cannot verify: %s" % exc)
        return 2
    except ValueError as exc:
        print("RESTORE-GUARD: FAIL, cannot verify: %s" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
