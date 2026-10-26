#!/usr/bin/env python3
"""invariant_promote -- the promotion gate the percolator never had (wave 2).

WAVE: invariant-percolator, 2026-10-20, wave 2 (fold of wave 1).
Read-only on the registry. Appends to a ledger. Stdlib only. $0.

WHY: `_compile_invariant` writes `count: 1` on first sighting
(mag/percolator.py:421-424), so the registry admits everything and calls it an
invariant. Wave 1 measured it: 90.6% of rows below the stated repeat condition,
42.9% probe chatter. Wave 1's fold: keep admission append-only (no data loss)
and add a PROMOTION surface for consumers.

WHAT THIS DOES:
  - computes, from live bytes, which rows qualify as invariants under
    policy promotion.v1 (count, recurrence across cycles or sources, source
    domain, failure vocabulary);
  - appends one ledger row per changed verdict to
    memory/percolator/promotion_ledger.jsonl (append-only; never rewrites);
  - never edits invariants.json. The ledger is a join key, not a mutation.

Idempotent: a row is re-emitted only when its content hash or the policy hash
changed. `--apply` writes; the default is a dry run.

Exit ladder (self-stolen from tools/claim_drift_patrol.py):
  0 ok / nothing to do
  1 policy refused a row that claims invariant status (reported, not fatal)
  2 cannot-verify (registry missing or unreadable)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("memory") / "percolator" / "invariants.json"
LEDGER = Path("memory") / "percolator" / "promotion_ledger.jsonl"
EXPORT = Path("memory") / "percolator" / "PROMOTED_INVARIANTS.md"
FALSIFIERS = Path("memory") / "percolator" / "falsifiers.jsonl"

SCHEMA = "invariant_promotion.v1"
POLICY = "promotion.v2"
POLICY_SPEC = {
    "min_count": 2,
    "min_span_days": 1.0,
    "min_cycle_sources": 2,
    "blocked_domain_prefix": "probe_",
    "blocked_text_regex": (
        r"backend reported failure|backend not reachable|backend timeout|not allowlisted|"
        r"false-success|identical tool calls|identical run_python|identical run_shell|"
        r"identical write_file|does not exist: /app/|banned pattern|\[Errno|"
        r"path outside jail|not a file: /app/|improve_queued=|"
        r"write_file missing path|emit flat JSON|sibling keys|\[REMEDY"
    ),
}
POLICY_SHA = hashlib.sha256(
    json.dumps(POLICY_SPEC, sort_keys=True).encode()).hexdigest()[:16]
BLOCKED_TEXT = re.compile(POLICY_SPEC["blocked_text_regex"], re.IGNORECASE)

OK_PREFIX = "PERCOLATOR-PROMOTE: ok"
REFUSED_PREFIX = "PERCOLATOR-PROMOTE: REFUSED"
UNVER_PREFIX = "PERCOLATOR-PROMOTE: UNVERIFIABLE"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def row_hash(canonical: str, row: dict) -> str:
    """Content identity of a registry row, independent of dict ordering."""
    blob = json.dumps(
        {"canonical": canonical, "text": row.get("text", ""), "count": row.get("count"),
         "first_seen": row.get("first_seen"), "last_seen": row.get("last_seen"),
         "domain": row.get("domain")},
        sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def assess(canonical: str, row: dict) -> dict:
    """Pure verdict for one registry row. Reasons say why; blockers say why not."""
    reasons: list[str] = []
    blockers: list[str] = []
    count = int(row.get("count", 1))
    domain = str(row.get("domain", ""))
    text = str(row.get("text", ""))

    if count >= POLICY_SPEC["min_count"]:
        reasons.append(f"count={count}")
    else:
        blockers.append(f"count<{POLICY_SPEC['min_count']}")

    first = _parse_ts(row.get("first_seen"))
    last = _parse_ts(row.get("last_seen")) or first
    span = (last - first).total_seconds() / 86400.0 if first and last else 0.0
    cycles = len(row.get("cycle_hits") or {})
    if span >= POLICY_SPEC["min_span_days"] or cycles >= POLICY_SPEC["min_cycle_sources"]:
        reasons.append(f"recurred(span_days={span:.2f},sources={cycles})")
    else:
        blockers.append("no-recurrence")

    if domain.startswith(POLICY_SPEC["blocked_domain_prefix"]):
        blockers.append("probe-domain")

    if BLOCKED_TEXT.search(text):
        blockers.append("instrumentation-vocabulary")

    return {"promoted": not blockers, "reasons": reasons, "blockers": blockers,
            "count": count, "span_days": round(span, 3)}


def load_registry(root: Path) -> dict:
    path = root / REGISTRY
    if not path.is_file():
        raise FileNotFoundError(f"registry missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("invariants"), dict):
        raise ValueError("registry has no 'invariants' object")
    return data["invariants"]


def load_ledger(path: Path) -> dict[str, dict]:
    """latest verdict per canonical; malformed lines are skipped, never fatal."""
    latest: dict[str, dict] = {}
    if not path.is_file():
        return latest
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("schema") == SCHEMA and row.get("canonical"):
            latest[row["canonical"]] = row
    return latest


def plan(invariants: dict, latest: dict[str, dict], now: str) -> list[dict]:
    """Rows that need a ledger entry.

    Emit when the row's bytes changed, when the verdict flipped, or when the policy
    changed AND the row is promoted (a claim we stand behind must be re-confirmed
    under the new policy). A blocked row that stays blocked under a new policy is
    not re-emitted: nothing at stake changes, and the ledger stays readable.
    """
    out: list[dict] = []
    for canonical, row in invariants.items():
        verdict = assess(canonical, row)
        rh = row_hash(canonical, row)
        prev = latest.get(canonical)
        if prev is not None and prev.get("row_hash") == rh:
            same_verdict = bool(prev.get("promoted")) == verdict["promoted"]
            policy_changed = prev.get("policy_sha") != POLICY_SHA
            if same_verdict and not (policy_changed and verdict["promoted"]):
                continue
        out.append({"schema": SCHEMA, "policy": POLICY, "policy_sha": POLICY_SHA,
                    "ts": now, "canonical": canonical, "row_hash": rh,
                    **verdict})
    return out


def summarise(invariants: dict, latest: dict[str, dict]) -> dict:
    promoted = sum(1 for c, r in invariants.items()
                   if (latest.get(c) or {}).get("promoted"))
    blockers: dict[str, int] = {}
    for canonical, row in invariants.items():
        rec = latest.get(canonical)
        if rec is None:
            blockers["unassessed"] = blockers.get("unassessed", 0) + 1
            continue
        for b in rec.get("blockers") or []:
            key = b.split("=")[0].split("<")[0]
            blockers[key] = blockers.get(key, 0) + 1
    return {"invariants": len(invariants), "promoted": promoted,
            "not_promoted": len(invariants) - promoted, "blockers": blockers,
            "policy": POLICY, "policy_sha": POLICY_SHA}


def load_falsifiers(path: Path) -> dict[str, dict]:
    """canonical -> falsifier entry. Malformed lines are skipped, never fatal."""
    out: dict[str, dict] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("schema") == "invariant_falsifier.v1" and row.get("canonical"):
            out[row["canonical"]] = row
    return out


def _falsifier_label(entry: dict | None) -> str:
    if not entry:
        return "MISSING"
    kind = str(entry.get("kind", "?"))
    if kind == "log_zero":
        return f"log_zero/{entry.get('window_days', '?')}d"
    if kind == "field_complete":
        return f"field_complete/{entry.get('field', '?')}"
    if kind == "manual":
        return f"manual/{entry.get('review_by', '?')}"
    return kind


def export_markdown(invariants: dict, latest: dict[str, dict], path: Path, now: str,
                    falsifiers: dict[str, dict] | None = None) -> dict:
    """Human-readable surface for seats: the promoted rows with their kill conditions.

    Reads the ledger (latest verdict per row) and the falsifier file, never
    recomputes promotion, so the export cannot disagree with `--promoted-only`.
    """
    falsifiers = falsifiers or {}
    rows = []
    for canonical, rec in latest.items():
        if not rec.get("promoted"):
            continue
        row = invariants.get(canonical)
        if row is None:
            continue
        text = " ".join(str(row.get("text", "")).split()).replace("|", "\\|")
        rows.append((int(row.get("count", 1)), str(row.get("domain", "")), canonical, text,
                     _falsifier_label(falsifiers.get(canonical))))
    rows.sort(key=lambda r: (-r[0], r[1], r[2]))

    missing = sum(1 for r in rows if r[4] == "MISSING")
    manual = sum(1 for r in rows if r[4].startswith("manual/"))
    checkable = len(rows) - missing - manual

    lines = [
        "# Promoted invariants",
        "",
        f"generated: {now}",
        f"policy: {POLICY} ({POLICY_SHA})",
        f"surface: {len(rows)} of {len(invariants)} registry rows promoted",
        "",
        "A promoted row met the repeat gate (count >= 2 and recurrence across UTC",
        "cycles or sources), is not probe chatter, and is not instrumentation",
        "vocabulary. Admission is untouched: every row still exists in",
        "`memory/percolator/invariants.json`; this is the readable subset.",
        "",
        f"Kill conditions: {checkable} checkable, {manual} manual debts, {missing} missing.",
        "Run `python tools/falsifier_lint.py` for PASS/FAIL/UNMEASURED on each.",
        "",
        "| count | domain | invariant | falsifier |",
        "| ---: | --- | --- | --- |",
    ]
    for count, domain, _canonical, text, falsifier in rows:
        lines.append(f"| {count} | {domain} | {text} | {falsifier} |")
    body = "\n".join(lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return {"path": str(path), "promoted": len(rows), "bytes": len(body.encode()),
            "checkable": checkable, "manual": manual, "missing": missing}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Promotion gate for the invariant registry")
    ap.add_argument("--root", default=None, help="estate root (default: this repo)")
    ap.add_argument("--apply", action="store_true", help="append verdicts to the ledger")
    ap.add_argument("--export", action="store_true",
                    help="write memory/percolator/PROMOTED_INVARIANTS.md from the ledger")
    ap.add_argument("--json", action="store_true", help="machine receipt only")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ESTATE_ROOT
    ledger_path = root / LEDGER

    try:
        invariants = load_registry(root)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"{UNVER_PREFIX}: {exc}")
        return 2

    latest = load_ledger(ledger_path)
    now = _now()
    rows = plan(invariants, latest, now)
    stats = summarise(invariants, latest)
    exported = None

    if args.apply and rows:
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with ledger_path.open("a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        latest = load_ledger(ledger_path)
        stats = summarise(invariants, latest)

    if args.export:
        exported = export_markdown(invariants, latest, root / EXPORT, now,
                                   load_falsifiers(root / FALSIFIERS))

    receipt = {"schema": "percolator_promote_receipt.v1", "ts": now,
               "applied": bool(args.apply), "written": len(rows) if args.apply else 0,
               "pending": 0 if args.apply else len(rows),
               "ledger": str(ledger_path), "stats": stats,
               "export": exported, "policy_spec": POLICY_SPEC}

    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        verb = "applied" if args.apply else "dry-run"
        print(f"{OK_PREFIX} ({verb}) -- policy {POLICY} ({POLICY_SHA})")
        print(f"  registry: {stats['invariants']} rows | promoted: {stats['promoted']} "
              f"| not promoted: {stats['not_promoted']}")
        print(f"  blockers: {stats['blockers']}")
        print(f"  ledger rows {'written' if args.apply else 'pending'}: "
              f"{len(rows)} -> {ledger_path}")
        if exported:
            print(f"  export: {exported['promoted']} rows, {exported['bytes']} bytes "
                  f"-> {exported['path']}")
        if not args.apply and rows:
            print("  rerun with --apply to append (registry is never edited)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
