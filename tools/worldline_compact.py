#!/usr/bin/env python3
"""worldline_compact - inventory and operator-gated compaction of worldline seeds.

The disease (2026-10-03, watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md finding 3
"worldline seed spray"): knot_at_close's W1 death rite emitted one full SEED.json
per closing session, and the flash-window workflow fleet closes every actor child
as a session - 2,107 dwf-* seeds (~39 MB of SEED.json bytes) minted inside one
~78-minute window on 2026-10-03, near-identical in their genome+invariants slabs.
The writer is now gated (mag/knot_at_close.py `_worldline_seed_hook`, tested by
tests/test_worldline_seed_gate.py); this tool is the read-side answer: measure the
spray, plan the fold, compact only under operator GO.

Estate law this tool obeys (operator brief, night shift 2026-10-04): NEVER delete
sibling data without operator GO. Therefore --check is the default and read-only;
--plan writes ONE markdown plan into watch/inbox and touches no seed; --execute is
fail-closed behind BOTH env WORLDLINE_COMPACT_GO=1 AND --plan <file>, and even
then it only MOVES member seed dirs into memory/worldline/_compact_archive/
(never unlink; every move lands a MANIFEST.jsonl row in the archive). Model text
can propose; only the operator authorizes effects.

Dedupe criterion (byte truth, not reports): two dwf seeds are identical material
when the canonical JSON bytes (sort_keys, tight separators) of their genome and
invariants slabs hash equal; a seed is compactable when it matches the NEWEST
seed of its created_utc minute (ties broken by session_id, so keeper choice is
deterministic across runs and machines). record/position slabs differ per actor
and are never compared. Seat seeds (any non-dwf- dir name) are inventoried and
never compacted. A seed whose slabs cannot be keyed is counted "unkeyed" and
never compacted (cannot verify identity -> do not touch).

Inventory scope: top-level dirs of memory/worldline that hold a SEED.json.
_compact_archive is cold storage and is skipped by every mode. Loose files
(REGISTRY.jsonl, readings.jsonl, ...) are counted in "other_files" and never
touched. Bytes are SEED.json file bytes (every real seed dir holds exactly one).

Exit contract: 0 = check reported / plan written / execute moved what the plan
named (0 groups is an honest "nothing to compact"); 2 = cannot verify - operator
gate closed, --plan missing or unreadable, plan target exists (never overwrite an
inbox artifact), plan root does not match the live root, a plan row no longer
matches the live tree (stale plan; regenerate), or an archive collision. Execute
is two-phase verify-then-move: any mismatch aborts BEFORE the first move; a
mid-move I/O failure stops, reports the partial trail honestly, and exits 2 (the
manifest keeps per-move truth).

The byte layer (scan, slab keying, report/table, plan render/parse) lives in
tools/worldline_compact_io.py - the split keeps both files under the ratchet's
400-line cap (census_drift_patrol B2-248/B2-365 precedent). One-way import.

CLI (repo interpreter only, .venv/Scripts/python.exe - never bare python):
  python tools/worldline_compact.py                          # --check (default)
  python tools/worldline_compact.py --check --root PATH
  python tools/worldline_compact.py --plan                   # -> watch/inbox/worldline_compaction_plan_<date>.md
  WORLDLINE_COMPACT_GO=1 python tools/worldline_compact.py --execute --plan <plan.md>
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLDLINE = ROOT / "memory" / "worldline"
INBOX = ROOT / "watch" / "inbox"
GO_ENV = "WORLDLINE_COMPACT_GO"

sys.path.insert(0, str(ROOT))
from tools.worldline_compact_io import (  # noqa: E402
    ARCHIVE_NAME,
    DWF_PREFIX,
    JSON_BEGIN,
    JSON_END,
    build_plan,
    build_report,
    file_sha256,
    now_iso,
    parse_plan_file,
    render_plan_md,
    render_table,
    read_seed,
    slab_key,
)


def _operator_ask(why: list[str], plan_ref: str) -> None:
    print("WORLDLINE-COMPACT: REFUSED (fail-closed)")
    for w in why:
        print(f"  why: {w}")
    print("  nothing has been moved; --check and --plan never touch seed files.")
    print(f"  THE ASK (operator): review {plan_ref} - lineage rows, one keeper per")
    print("  identical genome+invariants group, members listed with sha256s.")
    print("  To compact, run BOTH gates:")
    print("    WORLDLINE_COMPACT_GO=1 .venv/Scripts/python.exe tools/worldline_compact.py --execute --plan <plan file>")
    print("  execute only MOVES member seeds to memory/worldline/_compact_archive/ - it never deletes.")


def cmd_check(worldline: Path) -> int:
    if not worldline.is_dir():
        print(f"WORLDLINE-COMPACT: ERROR cannot verify - worldline dir missing: {worldline}")
        return 2
    report = build_report(worldline)
    print(render_table(report))
    print(JSON_BEGIN)
    print(json.dumps(report, indent=1))
    print(JSON_END)
    return 0


def cmd_plan(plan_arg: str, worldline: Path) -> int:
    if not worldline.is_dir():
        print(f"WORLDLINE-COMPACT: ERROR cannot verify - worldline dir missing: {worldline}")
        return 2
    if plan_arg:
        path = Path(plan_arg)
    else:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
        path = INBOX / f"worldline_compaction_plan_{stamp}.md"
    if path.exists():
        print(f"WORLDLINE-COMPACT: ERROR cannot verify - plan target already exists (never overwrite an "
              f"inbox artifact): {path}")
        print("  pass an explicit --plan <new path> with a fresh name.")
        return 2
    plan = build_plan(worldline)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_plan_md(plan), encoding="utf-8")
    n = sum(len(g["members"]) for g in plan["groups"])
    b = sum(m["bytes"] for g in plan["groups"] for m in g["members"])
    print(f"WORLDLINE-COMPACT PLAN ok -> {path}")
    print(f"  groups: {len(plan['groups'])}; members to archive: {n} seed dirs ({b / 1e6:.2f} MB); seeds touched: 0")
    print(f"  execute gate: WORLDLINE_COMPACT_GO=1 + --execute --plan \"{path}\"")
    return 0


def cmd_execute(plan_arg: str, worldline: Path) -> int:
    why: list[str] = []
    if os.environ.get(GO_ENV) != "1":
        why.append(f"env {GO_ENV} is not \"1\" (operator GO missing)")
    if not plan_arg:
        why.append("--plan <file> is required so the executed bytes are the reviewed bytes")
    if why:
        _operator_ask(why, plan_arg or "watch/inbox/worldline_compaction_plan_<date>.md")
        return 2
    plan_path = Path(plan_arg)
    plan = parse_plan_file(plan_path) if plan_path.is_file() else None
    if plan is None:
        _operator_ask([f"plan file missing or machine block unusable: {plan_path}"], plan_arg)
        return 2
    if Path(plan["worldline_dir"]).resolve() != worldline.resolve():
        _operator_ask([f"plan root {plan['worldline_dir']} does not match live root "
                       f"{worldline.resolve().as_posix()} (regenerate the plan against this tree)"], plan_arg)
        return 2
    archive_root = worldline / ARCHIVE_NAME
    dest_root = archive_root / str(plan.get("stamp") or plan["generated_utc"][:10])
    plan_sha = file_sha256(plan_path)
    seen: set[str] = set()
    moves: list[tuple[Path, Path, dict]] = []
    # phase 1: verify every row against the live tree BEFORE the first move
    for g in plan["groups"]:
        keeper_dir = str(g.get("keeper", {}).get("dir_name") or "")
        if not keeper_dir or keeper_dir in seen:
            _operator_ask([f"malformed group (bad/duplicate keeper {keeper_dir})"], plan_arg)
            return 2
        seen.add(keeper_dir)
        kdoc = read_seed(worldline / keeper_dir / "SEED.json")
        if kdoc is None or slab_key(kdoc) != g.get("slab_key"):
            _operator_ask([f"keeper no longer matches the plan (stale tree): {keeper_dir}"], plan_arg)
            return 2
        for m in g["members"]:
            d = str(m.get("dir_name") or "")
            if not d or d == keeper_dir or d in seen or not d.startswith(DWF_PREFIX):
                _operator_ask([f"malformed member row (bad/duplicate/non-dwf: {d})"], plan_arg)
                return 2
            seen.add(d)
            sj = worldline / d / "SEED.json"
            doc = read_seed(sj)
            if doc is None or slab_key(doc) != g.get("slab_key") or file_sha256(sj) != m.get("seed_sha256"):
                _operator_ask([f"member no longer matches the plan (stale tree): {d}"], plan_arg)
                return 2
            dest = dest_root / d
            if dest.exists():
                _operator_ask([f"archive target already exists (never overwrite): {dest}"], plan_arg)
                return 2
            moves.append((worldline / d, dest, {"slab_key": g["slab_key"], **m}))
    # phase 2: move (archive-only; never unlink)
    dest_root.mkdir(parents=True, exist_ok=True)
    manifest = archive_root / "MANIFEST.jsonl"
    done = done_bytes = 0
    for src, dest, m in moves:
        try:
            shutil.move(str(src), str(dest))
            if not (dest / "SEED.json").is_file():
                raise OSError(f"post-move verify failed: no SEED.json at {dest}")
        except (OSError, shutil.Error) as exc:
            print(f"WORLDLINE-COMPACT: ERROR move failed mid-batch at {src.name}: {exc}")
            print(f"  partial truth: {done} moved so far; manifest: {manifest}; fix + regenerate plan for the rest")
            return 2
        row = {"ts": now_iso(), "op": "worldline-compact-move", "session_id": m.get("session_id"),
               "from": src.as_posix(), "to": dest.as_posix(), "slab_key": m["slab_key"],
               "seed_sha256": m.get("seed_sha256"), "bytes": m.get("bytes"),
               "plan_path": plan_path.resolve().as_posix(), "plan_sha256": plan_sha}
        with manifest.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
        done += 1
        done_bytes += int(m.get("bytes") or 0)
    print("WORLDLINE-COMPACT EXECUTE ok")
    print(f"  plan: {plan_path} (sha256 {plan_sha[:16]})")
    print(f"  moved: {done} seed dirs ({done_bytes} B) -> {dest_root.as_posix()}")
    print(f"  keepers left in place: {len(plan['groups'])}; seat seeds untouched; "
          "nothing deleted (move, not copy+unlink)")
    print(f"  manifest: {manifest.as_posix()} (+{done} rows)")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="inventory + operator-gated compaction of worldline seeds (dry-run by default)")
    ap.add_argument("--check", action="store_true",
                    help="read-only inventory: per-prefix counts, bytes, ages, dedupe potential (default)")
    ap.add_argument("--plan", nargs="?", const="", default=None, metavar="PATH",
                    help="plan mode: write the compaction plan (default watch/inbox/worldline_compaction_plan_<date>.md); "
                         "with --execute: NAME the plan file whose bytes were reviewed")
    ap.add_argument("--execute", action="store_true",
                    help="apply a plan (requires WORLDLINE_COMPACT_GO=1 AND --plan; moves to _compact_archive, never deletes)")
    ap.add_argument("--root", default=str(WORLDLINE), metavar="PATH",
                    help="worldline root to operate on (default: repo memory/worldline)")
    args = ap.parse_args(argv)
    worldline = Path(args.root)
    if args.execute:
        return cmd_execute(args.plan or "", worldline)
    if args.plan is not None:
        return cmd_plan(args.plan, worldline)
    return cmd_check(worldline)


if __name__ == "__main__":
    sys.exit(main())
