"""verkle_dangling_repair.py — marker-backfill repair for dangling chain rows.

THE FINDING (W3 ledger registry, 2026-09-29): chain_guard reports state=regression
— 371 dangling rows, 300 of them WITHOUT the evidence_lost flag (marker pinned
2026-09-26 at 620 expected). The POWER_RESTORE_20260825 precedent repaired this
class by writing flags INTO chain rows — a chain rewrite. That path is now
operator-gated (Q-001: anything that rewrites the chain needs the operator),
because a row's leaf_hash covers the whole row JSON: setting evidence_lost=true
on a row changes its hash and invalidates every merkle proof above it.

THE REPAIR HERE (this tool) never touches the chain:
  1. enumerate dangling rows (chain_guard's own predicate: row.filename set and
     knots/<filename> not a file);
  2. classify each —
       recoverable_by_hash        a byte copy exists SOMEWHERE on disk whose
                                  canonical leaf content recomputes to the
                                  row's leaf_hash (verified, not name-trusted);
       truly_lost                 no hash-matching copy exists anywhere
                                  searchable → evidence_lost marker;
       already_flagged_in_chain   row carries evidence_lost already;
  3. append classification + evidence_lost markers to an APPEND-ONLY side
     ledger (default memory/verkle/repair_20260930.jsonl) keyed by
     (session_id, leaf_hash) so chain_guard can merge flags without mutation.

OPERATOR GATE (Q-001): if any row's repair would require chain mutation, this
tool STOPS at classification — it writes the ledger and reports
chain_mutation_required rows; it never rewrites the chain, knots, tip, or the
repair-state marker. Restoring recoverable knot files into the live knots dir
is a separate, deliberately unimplemented step (disk mutation of a live
single-writer surface; runs under verkle_lock when the operator calls it).

CLI:
  python tools/verkle_dangling_repair.py classify [--root PATH] [--ledger PATH]
  python tools/verkle_dangling_repair.py check   [--root PATH] [--ledger PATH]

Exit codes: 0 ok; 1 regression remains after ledger merge (check only);
2 cannot-verify (chain unreadable / tool misuse); 3 operator gate tripped.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# The hash law is the chain's own — reuse the live implementation, never a
# second referee (W3 ledger registry law: the registry runs each chain's OWN
# verify). For --root fixtures the import still works: _leaf_hash is pure.
from mag.verkle_knot import build_leaf_from_dossier, _leaf_hash  # noqa: E402

# Canonical leaf fields covered by leaf_hash (build_leaf_from_dossier field
# set; fold() adds filename/pdf_path AFTER hashing, so verification ignores
# them). Kept explicit here so a knot file carrying foreign extra fields
# cannot smuggle a match.
CANONICAL_LEAF_FIELDS = frozenset(build_leaf_from_dossier({}).keys()) - {"leaf_hash"}

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache",
             ".zcode", ".mypy_cache", ".ruff_cache"}

SCHEMA = "verkle_dangling_repair.v1"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


class Estate:
    """Paths of one verkle estate (live repo or a test fixture)."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.chain = self.root / "memory" / "biography" / "verkle_chain.jsonl"
        self.knots = self.root / "memory" / "biography" / "knots"
        self.tip = self.root / "memory" / "biography" / "verkle_tip.json"
        self.marker = self.root / "memory" / "biography" / "verkle_repair_state.json"
        self.default_ledger = self.root / "memory" / "verkle" / "repair_20260930.jsonl"

    def load_chain_rows(self) -> list[dict]:
        if not self.chain.is_file():
            raise FileNotFoundError(f"chain not found: {self.chain}")
        rows = []
        for line in self.chain.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def dangling_rows(self, rows: list[dict] | None = None) -> list[dict]:
        """chain_guard's exact predicate (mag/chain_guard.py check):
        a row is dangling iff filename is set and knots/<filename> is not a file."""
        rows = self.load_chain_rows() if rows is None else rows
        return [r for r in rows
                if r.get("filename") and not (self.knots / str(r["filename"])).is_file()]


def verify_candidate(doc: dict, leaf_hash: str) -> bool:
    """True iff doc's canonical leaf content recomputes to leaf_hash and the
    file's own leaf_hash field agrees (content proof, never a name match)."""
    if not isinstance(doc, dict) or not CANONICAL_LEAF_FIELDS <= set(doc):
        return False
    probe = {k: doc[k] for k in CANONICAL_LEAF_FIELDS}
    try:
        recomputed = _leaf_hash(probe)
    except (TypeError, ValueError):
        return False
    return recomputed == leaf_hash == doc.get("leaf_hash")


def index_knot_candidates(root: Path, knots_dir: Path) -> dict[str, list[Path]]:
    """filename -> copies found anywhere under root except the live knots dir
    (dangling already proved the live copy absent). Backups, watch copies,
    dist_audit snapshots are all legitimate recovery sources."""
    found: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        here = Path(dirpath)
        if here == knots_dir:
            dirnames[:] = []
            continue
        for f in filenames:
            if f.endswith(".knot.json"):
                found.setdefault(f, []).append(here / f)
    return found


def _pointer_witness(estate: Estate, session_id) -> bool:
    """by-session_v2 pointer on disk corroborates the knot existed; witness
    only — a pointer carries the hash, not the content."""
    digest = hashlib.sha256(str(session_id or "").encode("utf-8")).hexdigest()[:32]
    return (estate.knots / f"by-session_v2_{digest}.json").is_file()


def _row_key(row: dict) -> str:
    return f"{row.get('session_id')}|{row.get('leaf_hash')}"


def load_ledger(ledger: Path) -> list[dict]:
    if not ledger.is_file():
        return []
    out = []
    for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # a torn tail line never blocks an append-only ledger
    return out


def classified_keys(entries: list[dict]) -> set[str]:
    return {f"{e.get('session_id')}|{e.get('leaf_hash')}"
            for e in entries if e.get("kind") == "dangling_classification"}


def _postcondition_problems(classified: list[dict], rows_after: list[dict]) -> list[tuple]:
    """Refusal detector for a LIVE estate. The tool has no write path to the
    chain/tip/marker/knots, but the estate folds concurrently — the first real
    run watched a live append move chain+tip mid-walk (the B2-387 motion law:
    tail appends are legitimate). The real invariant: every row this run
    classified must survive byte-identical (same leaf_hash, filename, flag).
    A vanished/altered classified row = mutation or stripping = REFUSE."""
    after = {f"{r.get('session_id')}|{r.get('leaf_hash')}": r for r in rows_after}
    problems = []
    for row in classified:
        key = _row_key(row)
        later = after.get(key)
        if later is None:
            problems.append(("classified_row_vanished", key))
        elif (later.get("filename") != row.get("filename")
              or bool(later.get("evidence_lost")) != bool(row.get("evidence_lost"))):
            problems.append(("classified_row_altered", key))
    return problems


def classify(estate: Estate, ledger_path: Path, by: str = "verkle_dangling_repair") -> dict:
    """The repair: enumerate, classify, append markers. Chain stays byte-exact."""
    # Guard rails: hash every chain-visible surface before we start.
    before = {
        "chain": _sha256_file(estate.chain),
        "tip": _sha256_file(estate.tip),
        "marker": _sha256_file(estate.marker),
    }

    rows = estate.load_chain_rows()
    dangling = estate.dangling_rows(rows)
    candidates = index_knot_candidates(estate.root, estate.knots)

    existing = load_ledger(ledger_path)
    done = classified_keys(existing)
    new_entries: list[dict] = []
    counts = {"dangling_total": len(dangling), "recoverable_by_hash": 0,
              "truly_lost": 0, "already_flagged_in_chain": 0,
              "skipped_in_ledger": 0}
    # recount what the ledger already holds so a re-run reports the WHOLE
    # ledger's classification, not just the delta it appended
    for e in existing:
        if e.get("kind") != "dangling_classification":
            continue
        c = e.get("classification")
        if c in counts:
            counts[c] += 1

    for row in dangling:
        key = _row_key(row)
        if key in done:
            counts["skipped_in_ledger"] += 1
            continue
        entry = {
            "schema": SCHEMA,
            "kind": "dangling_classification",
            "chain_index": row.get("index"),
            "session_id": row.get("session_id"),
            "filename": row.get("filename"),
            "leaf_hash": row.get("leaf_hash"),
            "row_ts": row.get("ts"),
            "row_amended": bool(row.get("amended")),
            "pointer_witness": _pointer_witness(estate, row.get("session_id")),
            "classified_at": _utc(),
            "classified_by": by,
        }
        if row.get("evidence_lost"):
            entry["classification"] = "already_flagged_in_chain"
            entry["evidence_lost"] = None  # chain already carries the flag
            counts["already_flagged_in_chain"] += 1
        else:
            verified: list[str] = []
            for cand in candidates.get(str(row.get("filename")), []):
                try:
                    doc = json.loads(cand.read_text(encoding="utf-8", errors="replace"))
                except (OSError, json.JSONDecodeError):
                    continue
                if verify_candidate(doc, str(row.get("leaf_hash"))):
                    verified.append(str(cand.relative_to(estate.root)))
            if verified:
                entry["classification"] = "recoverable_by_hash"
                entry["evidence_lost"] = False  # evidence exists, hash-proven
                entry["recovered_from"] = sorted(verified)
                counts["recoverable_by_hash"] += 1
            else:
                entry["classification"] = "truly_lost"
                entry["evidence_lost"] = True  # the marker chain_guard merges
                counts["truly_lost"] += 1
        new_entries.append(entry)

    summary = {
        "schema": SCHEMA,
        "kind": "run_summary",
        "ran_at": _utc(),
        "ran_by": by,
        "chain_rows": len(rows),
        "chain_sha256_before": before["chain"],
        "ledger": str(ledger_path),
        "counts": counts,
        # No row's repair needs chain mutation: recoverable rows need only a
        # knot-file restore (disk, operator-gated separately); truly-lost rows
        # get their evidence_lost marker HERE, not in the row (Q-001 law).
        "chain_mutation_required": False,
        "operator_gate": "Q-001: in-chain flag backfill or knot restore into the "
                         "live knots dir is operator-gated; this run classified only.",
    }

    # Post-conditions FIRST, summary AFTER: a refused run's ledger record must
    # name the refusal, so the summary line lands only once the run's verdict
    # is known.
    rows_after = estate.load_chain_rows()
    problems = _postcondition_problems(dangling, rows_after)
    after = {
        "chain": _sha256_file(estate.chain),
        "tip": _sha256_file(estate.tip),
        "marker": _sha256_file(estate.marker),
    }
    live_motion = sorted(k for k in before if before[k] != after[k])
    summary["classified_rows_intact"] = not problems
    summary["live_chain_motion"] = live_motion or None
    summary["refusals"] = [list(p) for p in problems[:5]] if problems else None

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    # APPEND-ONLY, LF-only byte law (B2-393): newline="" stops Windows
    # text-mode translating our \n into \r\n inside the ledger too.
    # Classifications dedupe by (session_id, leaf_hash); every run appends
    # exactly one run_summary — the journal shape, not a rewrite.
    with ledger_path.open("a", encoding="utf-8", newline="") as fh:
        for e in new_entries:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
        fh.write(json.dumps(summary, ensure_ascii=False) + "\n")

    result = {
        "ok": not problems,
        "estate": str(estate.root),
        **counts,
        "ledger": str(ledger_path),
        "chain_mutation_required": False,
        "classified_rows_intact": not problems,
        "live_chain_motion": live_motion or None,
        "chain_rows_before": len(rows),
        "chain_rows_after": len(rows_after),
    }
    if problems:
        result["error"] = f"REFUSING RESULT: classified row(s) changed mid-run: {problems[:5]}"
    return result


def merge_check(estate: Estate, ledger_path: Path) -> dict:
    """chain_guard's regression law with the side ledger merged in.

    The guard alarms on a SILENT loss: a dangling row with no honest record.
    With the ledger merged, a row is accounted-for iff the chain row carries
    evidence_lost OR the ledger holds a classification for its
    (session_id, leaf_hash) — a truly_lost marker or a hash-verified
    recoverable classification. The raw guard number stays in the output so
    drift is visible; the alarm keys on the unclassified remainder."""
    rows = estate.load_chain_rows()
    dangling = estate.dangling_rows(rows)
    entries = [e for e in load_ledger(ledger_path)
               if e.get("kind") == "dangling_classification"]
    markers = {f"{e.get('session_id')}|{e.get('leaf_hash')}"
               for e in entries if e.get("evidence_lost") is True}
    classified = {f"{e.get('session_id')}|{e.get('leaf_hash')}" for e in entries}
    unflagged_raw = [r for r in dangling if not r.get("evidence_lost")]
    unclassified_effective = [r for r in unflagged_raw if _row_key(r) not in classified]
    return {
        "ok": not unclassified_effective,
        "state": "healthy_with_side_ledger" if not unclassified_effective else "regression",
        "rows": len(rows),
        "dangling": len(dangling),
        "dangling_unflagged_raw": len(unflagged_raw),
        "dangling_unflagged_markers_only": sum(1 for r in unflagged_raw if _row_key(r) not in markers),
        "dangling_unclassified_effective": len(unclassified_effective),
        "ledger_classifications": len(classified),
        "ledger_evidence_lost_markers": len(markers),
        "ledger": str(ledger_path),
        "alarm": None if not unclassified_effective else
                 "REGRESSION survives the side ledger: dangling row(s) lack both "
                 "the chain flag and any ledger classification — silent loss.",
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(
        prog="verkle-dangling-repair",
        description="Marker-backfill repair for dangling verkle rows (no chain writes)")
    ap.add_argument("cmd", choices=["classify", "check"],
                    help="classify+append ledger | verify effective regression state")
    ap.add_argument("--root", default=str(ROOT), help="estate root (default: repo root)")
    ap.add_argument("--ledger", default=None,
                    help="side ledger path (default: <root>/memory/verkle/repair_20260930.jsonl)")
    a = ap.parse_args(argv)
    estate = Estate(Path(a.root))
    ledger = Path(a.ledger) if a.ledger else estate.default_ledger
    try:
        if a.cmd == "classify":
            result = classify(estate, ledger)
        else:
            result = merge_check(estate, ledger)
    except FileNotFoundError as exc:
        print(json.dumps({"ok": False, "error": f"cannot-verify: {exc}"}, indent=2))
        return 2
    print(json.dumps(result, indent=2, default=str))
    if not result.get("ok"):
        return 3 if a.cmd == "classify" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
