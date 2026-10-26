"""verkle_restore_prep.py — Q-001 restore prep for hash-recoverable dangling rows.

THE STATE (W3n classification, 2026-09-30): the side ledger
(memory/verkle/repair_20260930.jsonl) holds 300 rows classified
recoverable_by_hash — for each, a byte copy exists on disk whose canonical
leaf content recomputes to the chain row's leaf_hash (verified against
bytes, never name-trusted). tools/verkle_dangling_repair.py deliberately
stopped there: restoring knot files into the live knots dir is disk mutation
of a live single-writer surface, operator-gated as Q-001.

THIS TOOL is the restore the operator would run:
  1. re-verify every ledger recoverable row against TODAY's bytes (trust
     bytes, not reports — recovered_from is a hint; the copy must still
     hash-match the still-dangling, still-unflagged chain row);
  2. re-embed the knot: byte-exact copy of the verified backup into
     knots/<filename> (tmp + os.replace — LF bytes stay LF);
  3. re-link: row.filename -> knots/<filename> must resolve and the dest
     must recompute to the row's leaf_hash;
  4. verify the full chain post-restore: merkle root over ALL leaf hashes,
     last row's verkle_root + tip bookmark agreement (the
     _verify_chain_consistent law, re-rooted), and chain_guard's regression
     predicate cleared (no unaccounted unflagged dangling row).

THE GATE (Q-001): --dry reports everything it would do and writes nothing.
--confirm requires the literal string OPERATOR-GO-Q001 as its argument; any
other value refuses with exit 3 before a single byte moves. Confirm holds
the estate verkle lock (same file, same law as mag.verkle_knot.verkle_lock
on the live estate) and NEVER writes the chain, tip, marker, or ledger —
restoring moves knot bytes only, so chain and tip shas must be byte-identical
before and after, under the lock.

CLI:
  python tools/verkle_restore_prep.py --dry   [--root PATH] [--ledger PATH]
  python tools/verkle_restore_prep.py --confirm OPERATOR-GO-Q001 [--root PATH] [--ledger PATH]

Exit codes: 0 dry ok / restore complete + chain verified;
            1 restore incomplete or post-restore verification failed;
            2 cannot-verify (chain unreadable, lock timeout, tool misuse);
            3 operator gate refusal (wrong confirm string).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Hash laws are the chain's own; the estate layout, ledger reader, row key and
# content-proof predicate are the classify tool's — the restore consumes
# exactly what the classification produced.
from mag.verkle_knot import _h, _merkle_root  # noqa: E402
from tools.verkle_dangling_repair import (  # noqa: E402
    Estate, _row_key, load_ledger, verify_candidate,
)

SCHEMA = "verkle_restore_prep.v1"
OPERATOR_GO = "OPERATOR-GO-Q001"

_LOCK_STALE_SECONDS = 900.0
_LOCK_POLL_SECONDS = 0.05


def _sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


@contextlib.contextmanager
def estate_lock(estate: Estate, timeout: float = 60.0):
    """Estate-rooted twin of mag.verkle_knot.verkle_lock (same O_CREAT|O_EXCL
    law, pid+ts content, 900s stale break), rooted at the estate's biography
    dir: on the live estate the path IS the live .verkle.lock, so a restore
    can never interleave with a live fold. Not imported from verkle_knot
    because that lock's path is pinned to config.ROOT — a --root fixture
    would take the LIVE lock."""
    lock = estate.tip.parent / ".verkle.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout
    fd = None
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            # a racing holder's stat/unlink must not kill the poll loop
            with contextlib.suppress(OSError):
                if time.time() - lock.stat().st_mtime > _LOCK_STALE_SECONDS:
                    lock.unlink()  # crashed holder — same stale law as verkle_lock
            if time.time() > deadline:
                raise TimeoutError(
                    f"estate verkle lock timeout after {timeout}s ({lock})")
            time.sleep(_LOCK_POLL_SECONDS)
    try:
        os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}".encode("utf-8"))
        yield
    finally:
        try:
            os.close(fd)
        finally:
            with contextlib.suppress(OSError):
                lock.unlink()


def _latest_knot(estate: Estate) -> Path:
    return estate.tip.with_name("latest.knot.json")


def _tip_root(estate: Estate) -> str | None:
    try:
        return str(json.loads(estate.tip.read_text(encoding="utf-8")).get("root") or "") or None
    except (OSError, json.JSONDecodeError):
        return None


def _recompute_root(rows: list[dict]) -> tuple[str | None, int]:
    hashes = [str(r.get("leaf_hash")) for r in rows if r.get("leaf_hash")]
    return (_merkle_root(hashes) if hashes else _h(b"empty")), len(hashes)


def _pick_verified_source(entry: dict, row: dict, root_dir: Path) -> str | None:
    """Newest backup copy whose bytes STILL recomputes to the row's leaf_hash.
    The ledger's recovered_from is a report; this re-proves it from bytes."""
    for cand in sorted(entry.get("recovered_from") or [], reverse=True):
        p = root_dir / str(cand)
        if not p.is_file():
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        if verify_candidate(doc, str(row.get("leaf_hash"))):
            return str(cand)
    return None


def plan_restore(estate: Estate, ledger_path: Path) -> dict:
    """Partition the ledger's recoverable rows against TODAY's chain + disk.
    Read-only: --dry prints this and stops; --confirm recomputes it under the
    lock and then executes the copies."""
    rows = estate.load_chain_rows()
    by_key = {_row_key(r): r for r in rows}
    entries = [e for e in load_ledger(ledger_path)
               if e.get("kind") == "dangling_classification"
               and e.get("classification") == "recoverable_by_hash"]

    to_restore: list[dict] = []
    already: list[str] = []
    gone: list[str] = []
    unverifiable: list[str] = []
    claimed_filenames: dict[str, str] = {}

    for entry in entries:
        key = _row_key(entry)
        row = by_key.get(key)
        if row is None:
            gone.append(key)
            continue
        filename = str(row.get("filename"))
        dest = estate.knots / filename
        if dest.is_file():
            already.append(key)
            continue
        source = _pick_verified_source(entry, row, estate.root)
        if source is None:
            unverifiable.append(key)
            continue
        if filename in claimed_filenames:
            # two rows, one filename: a collision REFUSES both rather than
            # guess which copy links (cannot fire on a hash-verified ledger).
            gone.append(f"{key}|collides-with {claimed_filenames[filename]}")
            continue
        claimed_filenames[filename] = key
        to_restore.append({
            "chain_index": row.get("index"),
            "session_id": entry.get("session_id"),
            "filename": filename,
            "leaf_hash": str(row.get("leaf_hash")),
            "source": source,
            "dest": str(dest.relative_to(estate.root)),
        })

    root, n_leaves = _recompute_root(rows)
    dangling = estate.dangling_rows(rows)
    restored_keys = {f"{c['session_id']}|{c['leaf_hash']}" for c in to_restore}
    dangling_after = [r for r in dangling
                      if _row_key(r) not in restored_keys]
    live_tip = _tip_root(estate)
    return {
        "rows_recoverable_in_ledger": len(entries), "rows_to_restore": len(to_restore),
        "knot_copies": to_restore, "rows_already_present": len(already),
        "rows_gone_from_chain": len(gone), "rows_source_unverifiable": len(unverifiable),
        "_gone_keys": gone, "_unverifiable_keys": unverifiable,
        "expected_tip": {
            "root": root, "n_leaves": n_leaves, "live_tip_root": live_tip,
            "live_tip_matches_chain": (None if root is None or live_tip is None
                                       else live_tip == root),
            "note": "restore copies knot bytes only — the chain and tip must not move",
        },
        "post_restore": {
            "dangling_before": len(dangling),
            "dangling_after_expected": len(dangling_after),
            "dangling_unflagged_after_expected": sum(1 for r in dangling_after
                                                     if not r.get("evidence_lost")),
        },
        "chain_sha256": _sha256_file(estate.chain),
    }


def verify_full_chain(estate: Estate, restored_copies: list[dict],
                      ledger_path: Path | None = None) -> dict:
    """Post-restore gate: root law + re-linked knots + chain_guard's
    regression predicate with the side ledger merged (merge_check's view)."""
    rows = estate.load_chain_rows()
    root, n_leaves = _recompute_root(rows)
    problems: list[str] = []
    if rows and n_leaves and rows[-1].get("verkle_root") != root:
        problems.append(f"last row verkle_root mismatch "
                        f"({str(rows[-1].get('verkle_root'))[:16]} vs {str(root)[:16]})")
    tip_root = _tip_root(estate)
    if tip_root and tip_root != root:
        problems.append(f"tip root mismatch ({tip_root[:16]} vs {str(root)[:16]})")

    # the re-link proof: every restored dest must recompute to its row's hash
    by_key = {_row_key(r): r for r in rows}
    links_verified = 0
    for copy in restored_copies:
        dest = estate.root / str(copy["dest"])
        try:
            doc = json.loads(dest.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            problems.append(f"restored knot unreadable: {copy['dest']}")
            continue
        if not verify_candidate(doc, copy["leaf_hash"]):
            problems.append(f"restored knot hash-link broken: {copy['dest']}")
            continue
        links_verified += 1

    dangling = estate.dangling_rows(rows)
    unflagged = [r for r in dangling if not r.get("evidence_lost")]
    classified: set[str] = set()
    if ledger_path is not None:
        classified = {_row_key(e)
                      for e in load_ledger(ledger_path)
                      if e.get("kind") == "dangling_classification"}
    # effective remainder: unflagged rows the side ledger does not account
    # for either (merge_check's law) — a silent loss survives the restore.
    unaccounted = [r for r in unflagged
                   if _row_key(r) not in classified]
    return {
        "ok": not problems and not unaccounted, "problems": problems,
        "root": root, "n_leaves": n_leaves,
        "restored_links_verified": links_verified, "dangling": len(dangling),
        "dangling_unflagged_raw": len(unflagged),
        "dangling_unaccounted_effective": len(unaccounted),
        "unaccounted_remainder": [f"{r.get('session_id')}|{str(r.get('leaf_hash'))[:16]}"
                                  for r in unaccounted[:5]],
    }


def dry_run(estate: Estate, ledger_path: Path) -> dict:
    plan = plan_restore(estate, ledger_path)
    return {
        "schema": SCHEMA, "mode": "dry",
        "ok": not plan["rows_gone_from_chain"] and not plan["rows_source_unverifiable"],
        "estate": str(estate.root), "ledger": str(ledger_path),
        "rows_recoverable_in_ledger": plan["rows_recoverable_in_ledger"],
        "rows_to_restore": plan["rows_to_restore"],
        "rows_already_present": plan["rows_already_present"],
        "rows_gone_from_chain": plan["rows_gone_from_chain"],
        "rows_source_unverifiable": plan["rows_source_unverifiable"],
        "knot_copies": plan["knot_copies"], "expected_tip": plan["expected_tip"],
        "post_restore": plan["post_restore"],
        "chain_sha256_will_stay": plan["chain_sha256"],
        "writes": "NONE — dry reports only",
        "gate": f"Q-001: re-run with --confirm {OPERATOR_GO} to execute; "
                "any other confirm string refuses",
    }


def confirm_restore(estate: Estate, ledger_path: Path) -> dict:
    """The gated execution. Writes ONLY knot bytes (plus latest.knot.json if
    the chain tail itself was restored); chain/tip/marker/ledger untouched."""
    before = {"chain": _sha256_file(estate.chain), "tip": _sha256_file(estate.tip),
              "marker": _sha256_file(estate.marker), "ledger": _sha256_file(ledger_path)}
    with estate_lock(estate):
        plan = plan_restore(estate, ledger_path)  # re-planned under the lock
        restored: list[dict] = []
        copy_failures: list[str] = []
        for copy in plan["knot_copies"]:
            src = estate.root / str(copy["source"])
            dst = estate.knots / str(copy["filename"])
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                tmp = dst.with_name(f"{dst.name}.{os.getpid()}.restore.tmp")
                tmp.write_bytes(src.read_bytes())  # byte-exact: no newline translation
                os.replace(tmp, dst)
            except OSError as exc:
                copy_failures.append(f"{copy['dest']}: {exc}")
                continue
            restored.append(copy)

        # latest.knot.json mirrors the chain tail (mag.verkle_knot
        # _sync_latest_knot's law): refresh it only if the tail knot itself
        # was one of the restored files.
        tail = str((json.loads(estate.tip.read_text(encoding="utf-8"))
                    if estate.tip.is_file() else {}).get("last_filename") or "")
        latest_refreshed = None
        if tail and any(c["filename"] == tail for c in restored):
            _latest_knot(estate).write_bytes((estate.knots / tail).read_bytes())
            latest_refreshed = str(_latest_knot(estate).relative_to(estate.root))

        after = {"chain": _sha256_file(estate.chain), "tip": _sha256_file(estate.tip),
                 "marker": _sha256_file(estate.marker), "ledger": _sha256_file(ledger_path)}
        moved = sorted(k for k in before if before[k] != after[k])
        chain_check = verify_full_chain(estate, restored, ledger_path)

        # postcondition: planned rows survive byte-identical (the classify
        # tool's motion law — a vanished/altered row under our lock is a rogue
        # writer, exactly the 2026-08-25 incident shape).
        rows_after = estate.load_chain_rows()
        by_key = {_row_key(r): r for r in rows_after}
        row_problems = []
        for copy in plan["knot_copies"]:
            later = by_key.get(_row_key(copy))
            if later is None:
                row_problems.append(f"planned row vanished mid-run: {copy['session_id']}")
            elif str(later.get("filename")) != copy["filename"]:
                row_problems.append(f"planned row filename moved: {copy['session_id']}")

    ok = (not copy_failures and not moved and not row_problems and chain_check["ok"]
          and len(restored) == plan["rows_to_restore"]
          # a ledger that promised N recoverable rows must account for all N:
          # any row that went unverifiable or vanished from the chain is a
          # degraded run the operator sees on the exit ladder, never a green.
          and plan["rows_source_unverifiable"] == 0 and plan["rows_gone_from_chain"] == 0)
    return {
        "schema": SCHEMA, "mode": "confirm", "ok": ok,
        "estate": str(estate.root), "ledger": str(ledger_path),
        "rows_recoverable_in_ledger": plan["rows_recoverable_in_ledger"],
        "rows_to_restore": plan["rows_to_restore"], "restored": len(restored),
        "already_present": plan["rows_already_present"],
        "rows_source_unverifiable": plan["rows_source_unverifiable"],
        "unverifiable_keys": plan["_unverifiable_keys"][:5],
        "rows_gone_from_chain": plan["rows_gone_from_chain"],
        "gone_keys": plan["_gone_keys"][:5],
        "copy_failures": copy_failures, "latest_knot_refreshed": latest_refreshed,
        "chain_moved_under_lock": moved or None,   # must be None (rogue writer if set)
        "planned_rows_intact": not row_problems, "row_problems": row_problems,
        "full_chain_verify": chain_check, "expected_tip": plan["expected_tip"],
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(
        prog="verkle-restore-prep",
        description="Q-001-gated restore of hash-recoverable dangling verkle knots")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry", action="store_true",
                      help="report what a restore would do; write nothing")
    mode.add_argument("--confirm", metavar="GATE", default=None,
                      help=f"execute the restore; GATE must be the literal {OPERATOR_GO}")
    ap.add_argument("--root", default=str(ROOT), help="estate root (default: repo root)")
    ap.add_argument("--ledger", default=None,
                    help="side ledger path (default: <root>/memory/verkle/repair_20260930.jsonl)")
    a = ap.parse_args(argv)

    # THE GATE, before anything that could tempt a write: a wrong confirm
    # string refuses here, exit 3, zero bytes touched.
    if a.confirm is not None and a.confirm != OPERATOR_GO:
        print(json.dumps({
            "schema": SCHEMA, "ok": False, "refused": True,
            "error": f"operator gate Q-001 refused: --confirm must be the literal "
                     f"string {OPERATOR_GO} (got {a.confirm!r}); nothing was written",
        }, indent=2))
        return 3
    estate = Estate(Path(a.root))
    ledger = Path(a.ledger) if a.ledger else estate.default_ledger
    try:
        result = dry_run(estate, ledger) if a.dry else confirm_restore(estate, ledger)
    except (FileNotFoundError, TimeoutError) as exc:
        print(json.dumps({"schema": SCHEMA, "ok": False,
                          "error": f"cannot-verify: {exc}"}, indent=2))
        return 2
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
