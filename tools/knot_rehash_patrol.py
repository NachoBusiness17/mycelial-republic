"""knot_rehash_patrol.py — leaf-hash rehash patrol for the verkle knot chain
(AH3, audit finding #9, last_mile 2026-09-30).

THE FINDING: the chain gate (mag/verkle_knot._verify_chain_consistent) only
recomputes the MERKLE root over the row leaf_hash STRINGS — it never
re-derives a leaf_hash from the knot FILE on disk, so an edited knot body
sails through the gate while the row string sits untouched. Separately, the
chain carries dangling rows (filename set, knots/<filename> gone; ~372 at
audit time, chain_guard's census).

WHAT THIS PATROL DOES (and refuses to do):
  1. sample N rows (default 200, --all for every row) from
     memory/biography/verkle_chain.jsonl;
  2. for each sampled PRESENT row, read knots/<filename> and recompute the
     leaf hash with the chain's OWN hashers — imported, never reimplemented
     (W3 registry law: one referee per chain):
       session/usage-digest leaves → mag.verkle_knot._leaf_hash over the
         knot body minus {leaf_hash, filename, pdf_path} (fold adds those
         AFTER hashing; mag/verkle_artifact.verify_leaf strip-set);
       leaf_kind == "diary_node" → mag.diary_node._leaf_hash (b"diary-leaf:"
         prefix) over the body minus {leaf_hash, filename, type, schema,
         leaf_kind} with schema restored to "mag_diary_node.v1" (the append
         path overwrites schema/type/leaf_kind post-hash);
  3. census dangling rows over the WHOLE chain (chain_guard's exact
     predicate: row.filename set and knots/<filename> not a file);
  4. print REHASHED n/m MATCH, DANGLING d, MISMATCH list.

A MISMATCH is an incident (knot body edited, knot/chain hash disagreement,
or an unparseable knot): row ids land in the output and the receipt, and the
patrol repairs NOTHING — Q-001 operator gate owns every repair
(tools/verkle_dangling_repair.py precedent: evidence classification only).

Exit codes: 0 clean sample; 1 mismatch found; 2 cannot-run (chain
missing/unreadable, bad arguments, diary hasher unavailable).

Usage:
  python tools/knot_rehash_patrol.py [--root PATH] [--sample N] [--all]
         [--seed S] [--json]

The default sample is deterministic (fixed seed) so a receipt can name the
exact rows a run rehashed; --all rehashes every present row.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# The hash law is the chain's own — reuse the live implementation, never a
# second referee. For --root fixtures the import still works: _leaf_hash is
# pure (same note as tools/verkle_dangling_repair.py).
from mag.verkle_knot import _leaf_hash as _session_leaf_hash  # noqa: E402

SCHEMA = "knot_rehash_patrol.v1"
DEFAULT_SAMPLE = 200
DEFAULT_SEED = 20260930  # AH3 lane date: receipts name its exact sample

# Audit finding #9's census claim, carried so every run reads its live count
# against it (census denominator law: name instrument + moment, then compare).
AUDIT_DANGLING_CLAIM = 372

# Fields fold()/append paths add AFTER hashing — verification strips them.
SESSION_STRIP = frozenset({"leaf_hash", "filename", "pdf_path"})
DIARY_STRIP = frozenset({"leaf_hash", "filename", "type", "schema", "leaf_kind"})
DIARY_SCHEMA = "mag_diary_node.v1"  # schema value the diary body hashed under


class Estate:
    """Paths of one verkle estate (live repo or a test fixture)."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.chain = self.root / "memory" / "biography" / "verkle_chain.jsonl"
        self.knots = self.root / "memory" / "biography" / "knots"

    def load_chain_rows(self) -> list[dict]:
        """Fail-closed chain read: a torn/unparseable line is cannot-run
        (exit 2), never silently skipped evidence (census_drift_patrol law)."""
        if not self.chain.is_file():
            raise FileNotFoundError(f"chain not found: {self.chain}")
        rows: list[dict] = []
        for lineno, line in enumerate(
            self.chain.read_text(encoding="utf-8", errors="strict").splitlines(), 1
        ):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"chain line {lineno} unparseable: {exc}") from exc
        return rows


def is_dangling(row: dict, knots: Path) -> bool:
    """chain_guard's exact predicate (mag/chain_guard.py check):
    a row is dangling iff filename is set and knots/<filename> is not a file."""
    fname = row.get("filename")
    return bool(fname) and not (knots / str(fname)).is_file()


def recompute_leaf_hash(doc: dict, row: dict) -> str:
    """Recompute a knot file's leaf hash with the chain's own hasher.

    Dispatch on leaf kind: diary seals hash under b"diary-leaf:"
    (mag/diary_node.py) with their original schema restored; every other
    leaf (session knots, usage-digest day leaves) hashes under verkle_knot's
    b"leaf:" law. Raises ImportError only if the diary module is unavailable.
    """
    if str(row.get("leaf_kind") or "") == "diary_node" or doc.get("leaf_kind") == "diary_node":
        from mag.diary_node import _leaf_hash as _diary_leaf_hash  # lazy: rare branch

        body = {k: v for k, v in doc.items() if k not in DIARY_STRIP}
        body["schema"] = DIARY_SCHEMA
        return _diary_leaf_hash(body)
    body = {k: v for k, v in doc.items() if k not in SESSION_STRIP}
    return _session_leaf_hash(body)


def _mismatch(row: dict, kind: str, detail: str) -> dict:
    """One incident row — id triple (index, session_id, filename) + cause."""
    return {
        "kind": kind,
        "index": row.get("index"),
        "session_id": row.get("session_id"),
        "filename": row.get("filename"),
        "detail": detail,
    }


def run(estate: Estate, sample: int | None, seed: int, as_json: bool) -> int:
    try:
        rows = estate.load_chain_rows()
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": f"cannot-run: {exc}"}, indent=2))
        return 2

    dangling_rows = [r for r in rows if is_dangling(r, estate.knots)]
    no_filename = [r for r in rows if not r.get("filename")]
    present = [r for r in rows if r.get("filename") and not is_dangling(r, estate.knots)]

    if sample is None:  # --all
        chosen = present
        sampled_of = len(present)
    else:
        sampled_of = min(sample, len(present))
        rng = random.Random(seed)  # deterministic: the receipt names its sample
        chosen = rng.sample(present, sampled_of) if sampled_of else []

    mismatches: list[dict] = []
    checked = 0
    vanished_mid_run = 0  # live-estate motion (B2-387): folds land concurrently

    for row in chosen:
        knot_path = estate.knots / str(row["filename"])
        if not knot_path.is_file():
            vanished_mid_run += 1  # census saw it, read didn't — motion, not incident
            continue
        checked += 1
        try:
            doc = json.loads(knot_path.read_text(encoding="utf-8"))
            if not isinstance(doc, dict):
                raise ValueError("knot file is not a JSON object")
        except (OSError, ValueError) as exc:
            mismatches.append(_mismatch(row, "knot_unreadable", str(exc)))
            continue
        claimed_knot = str(doc.get("leaf_hash") or "")
        claimed_row = str(row.get("leaf_hash") or "")
        if not claimed_knot or not claimed_row:
            mismatches.append(
                _mismatch(row, "missing_leaf_hash",
                          f"knot leaf_hash={claimed_knot!r} row leaf_hash={claimed_row!r}")
            )
            continue
        try:
            recomputed = recompute_leaf_hash(doc, row)
        except ImportError as exc:
            print(json.dumps({"ok": False, "error": f"cannot-run: {exc}"}, indent=2))
            return 2
        if recomputed != claimed_knot:
            # THE incident class (audit #9): the knot BODY was edited after commit.
            mismatches.append(
                _mismatch(row, "body_vs_knot",
                          f"recomputed {recomputed[:16]}… != knot leaf_hash {claimed_knot[:16]}…")
            )
        if claimed_knot != claimed_row:
            mismatches.append(
                _mismatch(row, "knot_vs_row",
                          f"knot leaf_hash {claimed_knot[:16]}… != row leaf_hash {claimed_row[:16]}…")
            )

    verdict = {
        "schema": SCHEMA,
        "ok": not mismatches,
        "chain_rows": len(rows),
        "rehashed": checked,
        "rehash_target": len(chosen),
        "present_rows": len(present),
        "sampled": sampled_of,
        "dangling": len(dangling_rows),
        "dangling_audit_claim": AUDIT_DANGLING_CLAIM,
        "dangling_delta_vs_claim": len(dangling_rows) - AUDIT_DANGLING_CLAIM,
        "rows_without_filename": len(no_filename),
        "vanished_mid_run": vanished_mid_run,
        "mismatches": mismatches,
        "seed": seed,
        "estate": str(estate.root),
        "operator_gate": "Q-001: repairs are operator-GO; this patrol rehashes "
                         "and reports only (audit #9 instruction: do NOT repair).",
    }

    if as_json:
        print(json.dumps(verdict, indent=2, default=str))
    else:
        match_word = "MATCH" if not mismatches else "MISMATCH"
        delta = len(dangling_rows) - AUDIT_DANGLING_CLAIM
        print(f"REHASHED {checked}/{len(chosen)} {match_word}, DANGLING {len(dangling_rows)} "
              f"(audit claim {AUDIT_DANGLING_CLAIM}, delta {delta:+d})")
        if no_filename:
            print(f"note: {len(no_filename)} row(s) carry no filename (excluded from both checks)")
        if vanished_mid_run:
            print(f"note: {vanished_mid_run} sampled knot(s) vanished mid-run (live motion, not incident)")
        if mismatches:
            print(f"MISMATCH {len(mismatches)}")
            for m in mismatches:
                print(f"  [index={m['index']}] session_id={m['session_id']} "
                      f"file={m['filename']} kind={m['kind']} {m['detail']}")

    return 1 if mismatches else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="knot-rehash-patrol",
        description="Rehash sampled knot files against chain leaf_hash + census dangling rows "
                    "(audit #9: the chain gate never re-derives leaf hashes from disk)")
    parser.add_argument("--root", default=str(ROOT), help="estate root (default: repo root)")
    parser.add_argument("--sample", type=int, default=None,
                        help=f"rows to rehash (default {DEFAULT_SAMPLE}, capped at present rows)")
    parser.add_argument("--all", action="store_true", help="rehash every present row")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help=f"sampling seed (default {DEFAULT_SEED}, deterministic receipts)")
    parser.add_argument("--json", action="store_true", help="machine-readable verdict")
    args = parser.parse_args(argv)

    if args.all and args.sample is not None:
        print(json.dumps({"ok": False, "error": "cannot-run: --all and --sample are exclusive"}),
              file=sys.stderr)
        return 2
    if not args.all and (args.sample is not None and args.sample < 1):
        print(json.dumps({"ok": False, "error": "cannot-run: --sample must be >= 1"}),
              file=sys.stderr)
        return 2

    estate = Estate(Path(args.root))
    sample = None if args.all else (args.sample if args.sample is not None else DEFAULT_SAMPLE)
    return run(estate, sample, args.seed, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
