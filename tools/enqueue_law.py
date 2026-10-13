#!/usr/bin/env python3
"""enqueue_law.py - zombie-enqueue census + graveyard (Mickey17 W3J, 2026-09-29).

The disease this meters (wave ledger return 18,
watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md): nomic_rules_patch was enqueued
week after week to mag/game_rules.py, a module that never existed, while
FLOW_IMAGE kept freezing it as the next piece. The ledger re-promised a dead
clone instead of burying it.

Bar stated before reading anything (the disposable-clone law): every enqueue
lands or dies+epitaph within one cadence. A ZOMBIE entry is an enqueue
(enqueued: true) strictly older than the cadence (default 7 days) whose target
module does not exist on disk. A piece is a zombie when it holds at least one
zombie entry. Enqueues to a missing module that are still inside the cadence
are GRACE, evidence only (the clone may still land); enqueues whose module
exists are healthy regardless of age (the promise was satisfied).

Effects:
  (a) census: print every zombie piece with stale count, total enqueues,
      first/last enqueue ts, the missing module, and whether the loop is still
      promising fresh enqueues past the epitaph;
  (b) epitaphs: append one row per zombie (piece, module) to the graveyard
      memory/game/GRAVEYARD.jsonl. Append-only and idempotent: a pair already
      carrying an epitaph is never re-filed, and existing rows are never
      rewritten. Row shape is frozen by spec: {piece, module, times_enqueued,
      first_ts, epitaph: "module never existed"};
  (c) --prune: write a COPY of the ledger minus the zombie entries to
      memory/game/flow_ledger.pruned.jsonl. The original ledger is never
      touched (read-only); the operator merges the copy. Only zombie entries
      (stale + missing module) leave; fresh enqueues inside the cadence stay,
      and enqueued:false rows stay.

Fail-closed by construction (exit 2, never a guess): a missing ledger, an
unparseable JSON line, a row missing ts/piece/module/enqueued keys, a naive
timestamp, an absolute or traversing module path, or a graveyard that cannot
be read. A skipped row would silently under-count the census, so none are
skipped.

Exit codes: 0 = no zombies; 1 = zombies found (census printed, epitaphs
appended, and with --prune the merge candidate written); 2 = cannot verify.

Usage: python tools/enqueue_law.py [--ledger PATH] [--graveyard PATH]
       [--pruned PATH] [--root PATH] [--days N] [--prune]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = ESTATE_ROOT / "memory" / "game" / "FLOW_LEDGER.jsonl"
DEFAULT_GRAVEYARD = ESTATE_ROOT / "memory" / "game" / "GRAVEYARD.jsonl"
DEFAULT_PRUNED = ESTATE_ROOT / "memory" / "game" / "flow_ledger.pruned.jsonl"

CADENCE_DAYS = 7
EPITAPH_TEXT = "module never existed"
REQUIRED_KEYS = ("ts", "piece", "module", "enqueued")


class EnqueueLawError(Exception):
    """Cannot-verify condition; main() maps this to exit 2."""


def parse_ts(raw: str, where: str) -> datetime:
    """Parse an ISO-8601 ts, 'Z' suffix included. Naive ts are refused.

    A naive timestamp would force a timezone guess and a wrong age at the
    cadence boundary, so it is exit 2 naming the row, never normalized.
    """
    if not isinstance(raw, str):
        raise EnqueueLawError(f"{where}: ts is not a string ({raw!r})")
    text = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        ts = datetime.fromisoformat(text)
    except ValueError as exc:
        raise EnqueueLawError(f"{where}: unparseable ts {raw!r} ({exc})") from exc
    if ts.tzinfo is None:
        raise EnqueueLawError(f"{where}: naive ts {raw!r} needs an explicit offset")
    return ts


def load_jsonl(path: Path, kind: str) -> list[dict]:
    """Read a JSONL file into rows. Blank lines are tolerated; anything else
    that does not parse is exit 2 naming the line number."""
    if not path.is_file():
        raise EnqueueLawError(f"{kind} missing: {path}")
    rows: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EnqueueLawError(f"{kind} {path.name}:{lineno}: unparseable JSON ({exc})") from exc
        if not isinstance(row, dict):
            raise EnqueueLawError(f"{kind} {path.name}:{lineno}: row is not an object")
        rows.append(row)
    return rows


def load_ledger(path: Path) -> list[dict]:
    """Ledger rows with shape enforced: ts/piece/module/enqueued present, ts
    aware, module a relative posix path that stays inside the root."""
    rows = load_jsonl(path, "ledger")
    checked: list[dict] = []
    for lineno, row in enumerate(rows, 1):
        where = f"ledger {path.name} row {lineno}"
        missing = [k for k in REQUIRED_KEYS if k not in row]
        if missing:
            raise EnqueueLawError(f"{where}: missing key(s) {', '.join(missing)}")
        parse_ts(row["ts"], where)  # aware-or-exit-2, per row
        module = row["module"]
        if not isinstance(module, str) or not module:
            raise EnqueueLawError(f"{where}: module is not a non-empty string")
        module_path = Path(module)
        if module_path.is_absolute() or ".." in module_path.parts:
            raise EnqueueLawError(f"{where}: module {module!r} must be root-relative")
        checked.append(row)
    return checked


def module_exists(root: Path, module: str) -> bool:
    """Does the ledger's target module exist on disk under the estate root?"""
    return (root / module).is_file() or (root / module).is_dir()


def zombie_census(rows: list[dict], root: Path, days: int = CADENCE_DAYS,
                  now: datetime | None = None) -> dict:
    """Pure verdict core. Groups enqueued rows by (piece, module) and classes
    each pair: zombie (stale enqueue + missing module), grace (missing module,
    every enqueue still inside the cadence), healthy (module exists)."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    pairs: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        if row.get("enqueued") is True:
            pairs.setdefault((row["piece"], row["module"]), []).append(row)

    zombies: list[dict] = []
    grace: list[dict] = []
    landed = 0
    for (piece, module), enq in sorted(pairs.items()):
        ts = [parse_ts(r["ts"], f"census {piece}") for r in enq]
        stale = [r for r, t in zip(enq, ts) if t < cutoff]
        fresh = [r for r, t in zip(enq, ts) if t >= cutoff]
        if module_exists(root, module):
            landed += 1
            continue
        entry = {
            "piece": piece,
            "module": module,
            "zombie_entries": len(stale),
            "total_enqueues": len(enq),
            "fresh_enqueues": len(fresh),
            "first_enqueued": min(ts).isoformat(),
            "last_enqueued": max(ts).isoformat(),
        }
        if stale:
            zombies.append(entry)
        else:
            grace.append(entry)
    zombies.sort(key=lambda z: (z["first_enqueued"], z["piece"]))
    return {"zombies": zombies, "grace": grace, "landed_pairs": landed,
            "cutoff": cutoff.isoformat()}


def is_zombie_entry(row: dict, root: Path, cutoff: datetime) -> bool:
    """Entry-level law: an enqueue past the cadence to a missing module."""
    return (row.get("enqueued") is True
            and parse_ts(row["ts"], f"entry {row.get('piece')}") < cutoff
            and not module_exists(root, row["module"]))


def write_epitaphs(graveyard: Path, zombies: list[dict]) -> list[dict]:
    """Append one epitaph per zombie (piece, module), skipping pairs already
    buried. Existing rows are never read back for rewrite: append-only."""
    buried: set[tuple[str, str]] = set()
    if graveyard.is_file():
        for lineno, row in enumerate(load_jsonl(graveyard, "graveyard"), 1):
            for key in ("piece", "module"):
                if key not in row:
                    raise EnqueueLawError(
                        f"graveyard {graveyard.name} row {lineno}: missing key {key}")
            buried.add((row["piece"], row["module"]))
    fresh = [z for z in zombies if (z["piece"], z["module"]) not in buried]
    if fresh:
        with graveyard.open("a", encoding="utf-8") as fh:
            for z in fresh:
                # Shape frozen by the W3J spec; key order is part of the row.
                fh.write(json.dumps({
                    "piece": z["piece"],
                    "module": z["module"],
                    "times_enqueued": z["total_enqueues"],
                    "first_ts": z["first_enqueued"],
                    "epitaph": EPITAPH_TEXT,
                }) + "\n")
    return fresh


def prune_to_copy(ledger: Path, pruned: Path, rows: list[dict], root: Path,
                  days: int = CADENCE_DAYS, now: datetime | None = None) -> dict:
    """Write the merge candidate: the ledger minus zombie entries. The
    original is opened read-only (it was loaded in load_ledger and is never
    reopened for write here); fresh enqueues inside the cadence and
    enqueued:false rows survive."""
    if pruned.resolve() == ledger.resolve():
        raise EnqueueLawError("pruned copy path must differ from the ledger path")
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    kept = [r for r in rows if not is_zombie_entry(r, root, cutoff)]
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kept)
    pruned.write_text(body, encoding="utf-8")
    return {"pruned": pruned, "removed": len(rows) - len(kept), "kept": len(kept)}


def run(ledger: Path = DEFAULT_LEDGER, graveyard: Path = DEFAULT_GRAVEYARD,
        pruned: Path = DEFAULT_PRUNED, root: Path = ESTATE_ROOT,
        days: int = CADENCE_DAYS, prune: bool = False,
        now: datetime | None = None) -> int:
    """Gather bytes, print the census, file epitaphs, maybe write the pruned
    copy. Returns the process exit code (0 clean, 1 zombies, 2 cannot verify)."""
    try:
        rows = load_ledger(ledger)
    except EnqueueLawError as exc:
        print(f"ENQUEUE-LAW: cannot verify, {exc}")
        return 2
    try:
        census = zombie_census(rows, root, days, now)
    except EnqueueLawError as exc:
        print(f"ENQUEUE-LAW: cannot verify, {exc}")
        return 2
    print(f"ENQUEUE-LAW: {len(rows)} ledger rows, cadence {days}d "
          f"(cutoff {cutoff_format(census['cutoff'])}), "
          f"{census['landed_pairs']} landed pair(s)")
    for z in census["zombies"]:
        still = ""
        if z["fresh_enqueues"]:
            still = f"; STILL PROMISING {z['fresh_enqueues']} fresh enqueue(s) past the epitaph"
        print(f"  ZOMBIE {z['piece']} -> {z['module']}: "
              f"{z['zombie_entries']} stale of {z['total_enqueues']} enqueues; "
              f"first {z['first_enqueued']}; last {z['last_enqueued']}{still}")
    for g in census["grace"]:
        print(f"  grace {g['piece']} -> {g['module']}: {g['total_enqueues']} enqueue(s) "
              f"inside the cadence, module missing, not yet zombie "
              f"(last {g['last_enqueued']})")
    if not census["zombies"]:
        print("ENQUEUE-LAW: ok - no zombie enqueues")
        return 0
    try:
        filed = write_epitaphs(graveyard, census["zombies"])
    except EnqueueLawError as exc:
        print(f"ENQUEUE-LAW: cannot verify graveyard, {exc}")
        return 2
    already = len(census["zombies"]) - len(filed)
    print(f"  epitaphs: {len(filed)} filed, {already} already buried -> {graveyard}")
    if prune:
        try:
            result = prune_to_copy(ledger, pruned, rows, root, days, now)
        except EnqueueLawError as exc:
            print(f"ENQUEUE-LAW: cannot prune, {exc}")
            return 2
        print(f"  pruned copy: {result['pruned']} (removed {result['removed']} zombie "
              f"entries, kept {result['kept']}; ORIGINAL UNTOUCHED, operator merges)")
    return 1


def cutoff_format(iso: str) -> str:
    """Compact cutoff for the head line (date + hh:mm)."""
    return iso.replace("+00:00", "Z")[:16]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="zombie-enqueue census + graveyard (Mickey17 W3J)")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER,
                        help=f"flow ledger to census (default {DEFAULT_LEDGER})")
    parser.add_argument("--graveyard", type=Path, default=DEFAULT_GRAVEYARD,
                        help=f"append-only epitaph file (default {DEFAULT_GRAVEYARD})")
    parser.add_argument("--pruned", type=Path, default=DEFAULT_PRUNED,
                        help=f"prune copy destination (default {DEFAULT_PRUNED})")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root module paths resolve against (default: this repo)")
    parser.add_argument("--days", type=int, default=CADENCE_DAYS,
                        help=f"cadence in days before an enqueue is a zombie (default {CADENCE_DAYS})")
    parser.add_argument("--prune", action="store_true",
                        help="write the zombie-free COPY for the operator to merge "
                             "(the original ledger is never modified)")
    args = parser.parse_args(argv)
    return run(ledger=args.ledger, graveyard=args.graveyard, pruned=args.pruned,
               root=args.root, days=args.days, prune=args.prune)


if __name__ == "__main__":
    sys.exit(main())
