#!/usr/bin/env python3
"""burns_verdict_enum.py - verdict pseudo-enum normalizer for memory/burns/LEDGER.jsonl (AH13, 2026-09-30).

The disease this cures (AE5 tabular census, watch/inbox/last_mile_20260930/
AE5_TABULAR_CENSUS.md row 5 + Notes): the burns ledger verdict column is a
free-text pseudo-enum - a 2026-09-30 census read 693 rows carrying 114 distinct
verdict strings, 62 of them one-off prose paragraphs - so no query can group
burns by outcome without hand-parsing every row.

Design laws (operator order, AH13):

  1. The ledger is append-only history. REWRITING IT IN PLACE IS FORBIDDEN.
     --apply never touches LEDGER.jsonl; it writes the join sidecar
     memory/burns/verdict_enum_map.json and readers JOIN on it. The ledger
     sha256 is asserted byte-identical across every apply as a hard guarantee,
     not a promise.
  2. Never silently reclassify. Every distinct string gets an explicit
     disposition: curated exact table (confidence 1.0), ordered prefix/keyword
     rule (confidence 0.80-0.90, review=true), or the fallback OTHER bucket
     (confidence 0.30, review=true). review=true means "a human should confirm
     this mapping" - fuzzy and unknown verdicts are flagged, never absorbed.
  3. The original verdict string is always preserved verbatim alongside the
     canonical value; the enum is additive, never a replacement.

Canonical set: LANDED, PARTIAL, REJECTED, DECLINED, SUPERSEDED, OPEN, ERRATUM,
OTHER. ERRATUM is promoted from the suggested seven because 20+ rows are
amendments to PRIOR rows (ERRATUM/CORRECTION/self-feed renumberings) - a
different speech act from a new burn's outcome, and collapsing it into LANDED
or OTHER would erase the ledger's self-correction trail.

Join contract for readers:

    map = json.load(open("memory/burns/verdict_enum_map.json"))
    entry = map["census"].get(row["verdict"])          # exact join first
    if entry is None:                                   # verdict newer than map
        entry = normalize(row["verdict"])               # live fallback
    enum = entry["enum"]

Exit codes: 0 = audit/apply succeeded; 2 = ledger unreadable/unparseable or
ledger bytes changed during apply (fail-closed, never a guess).

Receipt: watch/inbox/last_mile_20260930/AH13_BURNS_ENUM.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = REPO_ROOT / "memory" / "burns" / "LEDGER.jsonl"
DEFAULT_MAP = REPO_ROOT / "memory" / "burns" / "verdict_enum_map.json"

MAP_SCHEMA = "burns.verdict_enum_map.v1"

CANONICAL_SET = [
    "LANDED",
    "PARTIAL",
    "REJECTED",
    "DECLINED",
    "SUPERSEDED",
    "OPEN",
    "ERRATUM",
    "OTHER",
]

# Curated exact table. Keys are the verdict string run through _key() (upper,
# whitespace-collapsed). An entry maps to (enum, review, rationale). Everything
# here is confidence 1.0 by construction. review=true marks a judgment call a
# human can flip without touching code - the rationale names the evidence
# (sampled ledger one_line, 2026-09-30 census).
EXACT_TABLE: dict[str, tuple[str, bool, str]] = {
    # --- LANDED: work completed / finding banked -------------------------
    "LANDED": ("LANDED", False, "canonical head token"),
    "STEAL": ("LANDED", False, "burns idiom: harvest succeeded, receipt filed"),
    "GREEN": ("LANDED", False, "patrol verdict: all green, theses hold"),
    "BUILT": ("LANDED", False, "build landed, falsifier PASS (sampled close)"),
    "DONE": ("LANDED", False, "work banked"),
    "RESOLVED": ("LANDED", False, "hold resolved on act-item condition"),
    "CONFIRMED": ("LANDED", False, "claim confirmed"),
    "PROVEN": ("LANDED", False, "proven on bytes"),
    "HOLDS": ("LANDED", False, "gate/thesis holds"),
    "DISCHARGED": ("LANDED", False, "owed item proven discharged"),
    "RECOVERED": ("LANDED", False, "recovered"),
    "APPLIED": ("LANDED", False, "amendment applied"),
    "ADOPTED": ("LANDED", False, "gate adopted, probe-clean"),
    "BACKFILLED": ("LANDED", False, "retro row repaired the gap"),
    "AMENDED": ("LANDED", False, "protocol amended per law"),
    "LANDED BOUNDED": ("LANDED", False, "landed with bounded scope"),
    "LANDED-FINAL": ("LANDED", False, "final landing"),
    "LANDED-ALTERNATE-ROUTE": ("LANDED", False, "landed via alternate route"),
    "LANDED-CENSUS-AS-RECORD": ("LANDED", False, "census stands as the record"),
    "PASS (FILED 14 DAYS EARLY)": ("LANDED", False, "gate pass, filed early"),
    "BOARDFIX": ("LANDED", False, "board repair executed in place"),
    "LANDED WITH ONE OWED ALARM": ("LANDED", True, "landed; one alarm disclosed owed"),
    "LANDED WITH INCIDENT (DISCLOSED)": ("LANDED", True, "landed; incident disclosed"),
    "FILED": ("LANDED", True, "disposition filed; one_line also names a regression"),
    "DECIDED": ("LANDED", True, "design decision landed spec-first"),
    "RETIRED": ("LANDED", True, "retirement executed, backlog resolved"),
    "ROAM": ("LANDED", True, "sensing sweep recorded, nothing owed"),
    "REAL": ("LANDED", True, "judge ruling: findings real"),
    "ACCEPT": ("LANDED", True, "judge accepted the prereg attack"),
    # --- PARTIAL: some landed, some owed/defective ------------------------
    "PARTIAL": ("PARTIAL", False, "canonical head token"),
    "PILOT": ("PARTIAL", True, "pilot fire 1 of N complete, amendment owed"),
    "PROBE LANDED, CLAUSE REJECTED (FALSIFIER BRANCH)": (
        "PARTIAL",
        True,
        "split verdict: probe landed, clause rejected",
    ),
    "FALSIFIER FIRED, LOCK OWED": (
        "PARTIAL",
        True,
        "falsifier fired (work landed), lock still owed",
    ),
    "LANDED-PARTIAL-FIT": (
        "PARTIAL",
        True,
        "landed but only partially fit; curated so the LANDED prefix rule cannot absorb it",
    ),
    # --- REJECTED ----------------------------------------------------------
    "REJECTED": ("REJECTED", False, "canonical head token"),
    "VACUOUS": ("REJECTED", False, "built then reverted by its own falsifier"),
    "NOT_CLEAN_NO_EDIT": ("REJECTED", True, "probe unclean, edit refused"),
    # --- DECLINED ----------------------------------------------------------
    "DECLINED": ("DECLINED", False, "canonical head token"),
    "NO_ERRATUM": ("DECLINED", True, "erratum declined on bytes (receipt exists)"),
    # --- SUPERSEDED --------------------------------------------------------
    "LANDED-SUPERSEDED-EXECUTED": (
        "SUPERSEDED",
        True,
        "already executed by concurrent lanes; this ask superseded",
    ),
    # --- OPEN: unresolved, parked, owed ------------------------------------
    "OWED": ("OPEN", False, "canonical head token: work still owed"),
    "HOLD": ("OPEN", False, "parked (meter exhausted), retry later"),
    "UNDECIDABLE-OWED": ("OPEN", False, "judge could not decide; stays owed"),
    # --- ERRATUM: amendment to a PRIOR row ---------------------------------
    "ERRATUM": ("ERRATUM", False, "canonical head token"),
    "LANDED-CORRECTION": ("ERRATUM", True, "correction row amending a prior landing"),
}

# Ordered fuzzy rules, applied only on an exact-table miss. Prefix rules are
# negation-immune by construction (rule 4 is prefix-OWED, never contains-OWED:
# the census carries "gap DISSOLVES, nothing owed" and a contains rule would
# flip that resolution prose into OPEN).
RULES: list[dict] = [
    {
        "id": "prefix_landed",
        "kind": "prefix_any",
        "prefixes": ["LANDED", "LANDING"],
        "enum": "LANDED",
        "confidence": 0.90,
        "review": True,
        "note": "landed:/landing prose one-liners (census carries ~15)",
    },
    {
        "id": "prefix_erratum",
        "kind": "prefix_any",
        "prefixes": ["ERRATUM", "CORRECTION"],
        "enum": "ERRATUM",
        "confidence": 0.90,
        "review": True,
        "note": "amendments to prior rows, prose form",
    },
    {
        "id": "prefix_partial",
        "kind": "prefix_any",
        "prefixes": ["PARTIAL"],
        "enum": "PARTIAL",
        "confidence": 0.90,
        "review": True,
        "note": "PARTIAL-OWED / PARTIAL-UNKNOWN-FILED / PARTIAL_BLOCKED",
    },
    {
        "id": "prefix_owed",
        "kind": "prefix_any",
        "prefixes": ["OWED"],
        "enum": "OPEN",
        "confidence": 0.85,
        "review": True,
        "note": "OWED-* family; prefix-only so 'nothing owed' never matches",
    },
    {
        "id": "contains_blocked",
        "kind": "word_any",
        "words": ["BLOCKED"],
        "enum": "OPEN",
        "confidence": 0.85,
        "review": True,
        "note": "blocked on source/operator, unresolvable from this seat yet",
    },
    {
        "id": "prefix_hold",
        "kind": "prefix_any",
        "prefixes": ["HOLD"],
        "enum": "OPEN",
        "confidence": 0.85,
        "review": True,
        "note": "hold: prose (meter/GO pending)",
    },
    {
        "id": "prefix_confirmed",
        "kind": "prefix_any",
        "prefixes": ["CONFIRMED", "PROVEN"],
        "enum": "LANDED",
        "confidence": 0.85,
        "review": True,
        "note": "confirmed:/proven: prose",
    },
    {
        "id": "prefix_wired",
        "kind": "prefix_any",
        "prefixes": ["WIRED"],
        "enum": "LANDED",
        "confidence": 0.80,
        "review": True,
        "note": "wired-into-code closes ('probe landed ... proven live')",
    },
    {
        "id": "contains_erratum",
        "kind": "word_any",
        "words": ["ERRATUM"],
        "enum": "ERRATUM",
        "confidence": 0.80,
        "review": True,
        "note": "self-feed numbering erratum prose; NO_ERRATUM is exact-curated first",
    },
]

FALLBACK = {
    "enum": "OTHER",
    "confidence": 0.30,
    "review": True,
    "rule": "fallback_unknown",
}

_WORD_RE = re.compile(r"[A-Z0-9]+")
_WS_RE = re.compile(r"\s+")


def _key(verdict: str) -> str:
    """Uppercase + collapse internal whitespace: the join key form."""
    return _WS_RE.sub(" ", verdict.strip()).upper()


def normalize(verdict: str) -> dict:
    """Map one free-text verdict to its canonical enum.

    Returns {"original", "canonical", "confidence", "review", "rule"}.
    The original string is preserved verbatim; the mapping is pure and
    deterministic (no I/O, no clock).
    """
    original = str(verdict)
    k = _key(original)
    if k in EXACT_TABLE:
        enum, review, _rationale = EXACT_TABLE[k]
        return {
            "original": original,
            "canonical": enum,
            "confidence": 1.0,
            "review": review,
            "rule": "exact",
        }
    for rule in RULES:
        hit = False
        if rule["kind"] == "prefix_any":
            hit = any(k.startswith(p) for p in rule["prefixes"])
        elif rule["kind"] == "word_any":
            words = set(_WORD_RE.findall(k))
            hit = any(w in words for w in rule["words"])
        if hit:
            return {
                "original": original,
                "canonical": rule["enum"],
                "confidence": rule["confidence"],
                "review": rule["review"],
                "rule": rule["id"],
            }
    # Fallback: never silently absorbed - OTHER + review means a human looks.
    return {
        "original": original,
        "canonical": FALLBACK["enum"],
        "confidence": FALLBACK["confidence"],
        "review": FALLBACK["review"],
        "rule": FALLBACK["rule"],
    }


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def census(ledger_path: Path) -> tuple[Counter, int, int]:
    """Stream the ledger; return (verdict->count, total rows, malformed lines).

    Fail-closed: a malformed JSON line raises (callers exit 2), never skipped.
    """
    counts: Counter = Counter()
    rows = 0
    malformed = 0
    with open(ledger_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{ledger_path}:{lineno}: malformed JSON ({exc}); refusing to census"
                ) from exc
            rows += 1
            verdict = row.get("verdict")
            if verdict is None:
                malformed += 1
                continue
            counts[str(verdict)] += 1
    return counts, rows, malformed


def audit(ledger_path: Path) -> tuple[Counter, int, int, list[dict]]:
    counts, rows, malformed = census(ledger_path)
    entries = []
    for verdict, count in counts.most_common():
        n = normalize(verdict)
        entries.append(
            {
                "original": verdict,
                "count": count,
                "enum": n["canonical"],
                "confidence": n["confidence"],
                "review": n["review"],
                "via": n["rule"],
            }
        )
    return counts, rows, malformed, entries


def build_map(ledger_path: Path) -> dict:
    counts, rows, malformed = census(ledger_path)
    census_out: dict[str, dict] = {}
    summary: dict[str, dict] = {
        e: {"rows": 0, "distinct": 0} for e in CANONICAL_SET
    }
    review_queue: list[str] = []
    for verdict, count in counts.most_common():
        n = normalize(verdict)
        census_out[verdict] = {
            "enum": n["canonical"],
            "confidence": n["confidence"],
            "review": n["review"],
            "count": count,
            "via": n["rule"],
        }
        summary[n["canonical"]]["rows"] += count
        summary[n["canonical"]]["distinct"] += 1
        if n["review"]:
            review_queue.append(verdict)
    return {
        "schema": MAP_SCHEMA,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ledger": str(ledger_path.relative_to(REPO_ROOT)),
        "ledger_rows": rows,
        "ledger_rows_missing_verdict": malformed,
        "ledger_distinct_verdicts": len(counts),
        "ledger_sha256": _sha256_file(ledger_path),
        "canonical_set": CANONICAL_SET,
        "exact_table": {
            k: {"enum": v[0], "review": v[1], "rationale": v[2]}
            for k, v in sorted(EXACT_TABLE.items())
        },
        "rules": RULES,
        "fallback": dict(FALLBACK),
        "join": (
            "readers JOIN ledger.verdict -> census[verdict].enum; a verdict "
            "string absent from census (younger than this map) falls back to "
            "tools.burns_verdict_enum.normalize() live; the ledger itself is "
            "never rewritten (AH13 law: enum is additive, join-side only)"
        ),
        "census": census_out,
        "summary": summary,
        "review_queue": review_queue,
    }


def write_map(ledger_path: Path, map_path: Path) -> dict:
    """Build and atomically write the join map. The ledger is never opened for
    writing; its sha256 is asserted unchanged across the whole operation (the
    AH13 no-rewrite law, enforced in bytes, not promised in prose)."""
    before = _sha256_file(ledger_path)
    m = build_map(ledger_path)
    after = _sha256_file(ledger_path)
    if before != after:
        raise RuntimeError(
            f"LEDGER {ledger_path} changed during apply (sha {before} -> {after}); "
            "map write aborted, ledger integrity suspect"
        )
    map_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = map_path.with_suffix(map_path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(m, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")
    tmp.replace(map_path)
    return m


def _fmt_original(s: str, width: int = 64) -> str:
    s = s.replace("\n", " ")
    return s if len(s) <= width else s[: width - 1] + "…"


def print_audit(entries: list[dict], rows: int, malformed: int, distinct: int) -> None:
    print(f"ledger: {rows} rows, {distinct} distinct verdicts, {malformed} missing verdict")
    print()
    hdr = f"{'count':>5}  {'enum':<10} {'conf':>4}  {'via':<18} {'rv':<2} original"
    print(hdr)
    print("-" * len(hdr))
    for e in entries:
        print(
            f"{e['count']:>5}  {e['enum']:<10} {e['confidence']:>4.2f}  "
            f"{e['via']:<18} {'Y' if e['review'] else '-':<2} "
            f"{_fmt_original(e['original'])}"
        )
    print()
    print("summary (rows):")
    total = 0
    for enum, n in sorted(
        ((e, sum(x["count"] for x in entries if x["enum"] == e)) for e in CANONICAL_SET),
        key=lambda kv: -kv[1],
    ):
        d = sum(1 for x in entries if x["enum"] == enum)
        print(f"  {enum:<11} {n:>5} rows / {d:>3} distinct")
        total += n
    n_review = sum(1 for e in entries if e["review"])
    print(
        f"\nreview queue: {n_review}/{distinct} distinct strings flagged review=true "
        f"({sum(e['count'] for e in entries if e['review'])} rows)"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--audit", action="store_true", help="print the mapping table with live counts")
    ap.add_argument("--apply", action="store_true", help="write the join map (--apply writes the map ONLY; the ledger is never rewritten)")
    ap.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    ap.add_argument("--map", type=Path, default=DEFAULT_MAP)
    args = ap.parse_args(argv)

    if not args.audit and not args.apply:
        args.audit = True  # default posture: look, don't write

    if not args.ledger.exists():
        print(f"FAIL ledger not found: {args.ledger}", file=sys.stderr)
        return 2
    try:
        if args.apply:
            m = write_map(args.ledger, args.map)
            print(
                f"map written: {args.map} ({m['ledger_rows']} rows, "
                f"{m['ledger_distinct_verdicts']} distinct, "
                f"ledger sha256 unchanged {m['ledger_sha256'][:12]}...)"
            )
            entries = [
                {"original": v, **{k: c[k] for k in ("enum", "confidence", "review", "via", "count")}}
                for v, c in m["census"].items()
            ]
            entries.sort(key=lambda e: (-e["count"], e["enum"]))
            print_audit(entries, m["ledger_rows"], m["ledger_rows_missing_verdict"], m["ledger_distinct_verdicts"])
        elif args.audit:
            counts, rows, malformed, entries = audit(args.ledger)
            print_audit(entries, rows, malformed, len(counts))
    except (ValueError, json.JSONDecodeError, RuntimeError, OSError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
