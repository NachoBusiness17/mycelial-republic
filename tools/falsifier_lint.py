#!/usr/bin/env python3
"""falsifier_lint -- every promoted invariant needs a stated kill condition.

WAVE: invariant-percolator, wave 4 (2026-10-20). Read-only. Stdlib only. $0.

Wave 3 produced a clean surface of 17 promoted invariants and printed its own
weakness in the header: "Falsifier: none declared". This tool closes that: each
promoted row must carry an entry in memory/percolator/falsifiers.jsonl, and the
entry must be one of four checkable kinds or an explicit `manual` debt.

Kinds:
  log_zero        rows matching <pattern> in <target> within <window_days> must be 0
  file_absent     <target> must not exist
  field_complete  every row in <target> must carry a non-empty <field>
  manual          unmeasured by design: names an owner and a review date

Tri-state is the point: PASS, FAIL, UNMEASURED. A manual entry is never counted
as a pass, and coverage (every promoted row has SOME entry) is reported apart
from correctness (the entry's check passes).

Exit ladder (self-stolen from tools/claim_drift_patrol.py):
  0 ok        no FAIL and full coverage
  1 FAILED    a falsifier fired, or a promoted row has no falsifier at all
  2 UNVERIFY  ledger, registry or falsifier file missing/unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("memory") / "percolator" / "invariants.json"
LEDGER = Path("memory") / "percolator" / "promotion_ledger.jsonl"
FALSIFIERS = Path("memory") / "percolator" / "falsifiers.jsonl"

SCHEMA = "invariant_falsifier.v1"
OK_PREFIX = "FALSIFIER-LINT: ok"
FAIL_PREFIX = "FALSIFIER-LINT: FAILED"
UNVER_PREFIX = "FALSIFIER-LINT: UNVERIFIABLE"
PASS, FAIL, UNMEASURED = "PASS", "FAIL", "UNMEASURED"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ts(value) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _rows(path: Path):
    """Yield parsed JSON rows from .jsonl, or from a JSON list/object of rows."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            yield from data
        elif isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    yield from value
        return
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _dedupe_stamps(stamps: list[datetime], dedupe_ms: float) -> list[datetime]:
    """Collapse duplicate log rows: same event written twice within dedupe_ms."""
    if dedupe_ms <= 0:
        return sorted(stamps)
    out: list[datetime] = []
    for stamp in sorted(stamps):
        if not out or (stamp - out[-1]).total_seconds() * 1000.0 > dedupe_ms:
            out.append(stamp)
    return out


def check_log_zero(root: Path, entry: dict, now: datetime) -> dict:
    target = root / entry["target"]
    if not target.is_file():
        return {"status": UNMEASURED, "detail": f"log missing: {entry['target']}"}
    pattern = re.compile(entry["pattern"], re.IGNORECASE)
    window = timedelta(days=float(entry.get("window_days", 7)))
    hits = []
    for row in _rows(target):
        stamp = _ts(row.get("ts") or row.get("timestamp") or row.get("time"))
        if stamp is None or (now - stamp) > window:
            continue
        blob = json.dumps(row, ensure_ascii=False)
        if pattern.search(blob):
            hits.append(stamp)
    unique = _dedupe_stamps(hits, float(entry.get("dedupe_ms", 0)))
    if unique:
        return {"status": FAIL, "count": len(unique), "raw": len(hits),
                "detail": f"{len(unique)} event(s) in {entry['window_days']}d "
                          f"(raw rows {len(hits)}), latest {unique[-1].isoformat()}",
                "latest": unique[-1].isoformat()}
    return {"status": PASS, "count": 0, "raw": len(hits),
            "detail": f"0 hits in {entry['window_days']}d"}


def check_nudge_budget(root: Path, entry: dict, now: datetime) -> dict:
    """A loop is handled if the detector's nudge budget was never exceeded.

    The collapse detector allows `max_nudges` (code default 2) then escalates
    (mag/agent_cli.py:1718-1790). Exceeding the budget means the designed path
    did not hold; staying inside it means the rule fired as written, whatever
    the raw row count says.
    """
    target = root / entry["target"]
    if not target.is_file():
        return {"status": UNMEASURED, "detail": f"log missing: {entry['target']}"}
    pattern = re.compile(entry.get("pattern", "identical"), re.IGNORECASE)
    window = timedelta(days=float(entry.get("window_days", 30)))
    budget = int(entry.get("max_nudges", 2))
    dedupe_ms = float(entry.get("dedupe_ms", 1000))
    per_pair: dict[tuple, list[datetime]] = {}
    for row in _rows(target):
        if row.get("phase") != "collapse_nudge":
            continue
        stamp = _ts(row.get("ts") or row.get("timestamp") or row.get("time"))
        if stamp is None or (now - stamp) > window:
            continue
        detail = str(row.get("detail") or "")
        if not pattern.search(detail):
            continue
        key = (row.get("sig"), row.get("session_id"))
        per_pair.setdefault(key, []).append(stamp)
    over = []
    for key, stamps in per_pair.items():
        unique = _dedupe_stamps(stamps, dedupe_ms)
        if len(unique) > budget:
            over.append({"sig": key[0], "session": key[1], "nudges": len(unique)})
    if over:
        return {"status": FAIL, "count": len(over),
                "detail": f"{len(over)} session/loop pair(s) exceeded {budget} nudges",
                "offenders": over[:5]}
    pairs = len(per_pair)
    return {"status": PASS, "count": 0,
            "detail": f"{pairs} loop pair(s) in {entry['window_days']}d, "
                      f"none exceeded {budget} nudges"}


def check_file_absent(root: Path, entry: dict, _now: datetime) -> dict:
    target = root / entry["target"]
    if target.exists():
        size = target.stat().st_size if target.is_file() else 0
        return {"status": FAIL, "detail": f"present: {entry['target']} ({size} bytes)"}
    return {"status": PASS, "detail": f"absent: {entry['target']}"}


def check_field_complete(root: Path, entry: dict, _now: datetime) -> dict:
    target = root / entry["target"]
    if not target.is_file():
        return {"status": UNMEASURED, "detail": f"ledger missing: {entry['target']}"}
    field = entry["field"]
    total = missing = 0
    for row in _rows(target):
        total += 1
        value = row.get(field)
        if value is None or (isinstance(value, (str, list, dict)) and len(value) == 0):
            missing += 1
    if missing:
        return {"status": FAIL, "detail": f"{missing}/{total} rows missing '{field}'"}
    return {"status": PASS, "detail": f"{total}/{total} rows carry '{field}'"}


def check_manual(_root: Path, entry: dict, _now: datetime) -> dict:
    return {"status": UNMEASURED,
            "detail": f"manual debt, owner={entry.get('owner', '?')}, review_by={entry.get('review_by', '?')}"}


CHECKS = {"log_zero": check_log_zero, "file_absent": check_file_absent,
          "field_complete": check_field_complete, "nudge_budget": check_nudge_budget,
          "manual": check_manual}


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"missing: {path}")
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def promoted_canonicals(ledger_rows: list[dict]) -> set[str]:
    latest: dict[str, dict] = {}
    for row in ledger_rows:
        if row.get("schema") == "invariant_promotion.v1" and row.get("canonical"):
            latest[row["canonical"]] = row
    return {c for c, r in latest.items() if r.get("promoted")}


def lint(root: Path) -> dict:
    invariants = json.loads((root / REGISTRY).read_text(encoding="utf-8")).get("invariants")
    if not isinstance(invariants, dict):
        raise ValueError("registry has no 'invariants' object")
    promoted = promoted_canonicals(load_jsonl(root / LEDGER))
    entries = load_jsonl(root / FALSIFIERS)
    by_canonical: dict[str, dict] = {}
    for entry in entries:
        if entry.get("schema") == SCHEMA and entry.get("canonical"):
            by_canonical[entry["canonical"]] = entry

    now = _now()
    results = []
    for canonical in sorted(promoted):
        entry = by_canonical.get(canonical)
        text = str((invariants.get(canonical) or {}).get("text", ""))[:90]
        if entry is None:
            results.append({"canonical": canonical, "claim": text, "kind": None,
                            "status": FAIL, "detail": "no falsifier entry"})
            continue
        fn = CHECKS.get(entry.get("kind"))
        if fn is None:
            results.append({"canonical": canonical, "claim": text,
                            "kind": entry.get("kind"), "status": UNMEASURED,
                            "detail": f"unknown kind: {entry.get('kind')}"})
            continue
        verdict = fn(root, entry, now)
        results.append({"canonical": canonical, "claim": text, "kind": entry["kind"],
                        **verdict, "owner": entry.get("owner"),
                        "review_by": entry.get("review_by")})

    counts = {PASS: 0, FAIL: 0, UNMEASURED: 0}
    for row in results:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    orphans = sorted(set(by_canonical) - promoted)
    return {"schema": "falsifier_lint.v1", "ts": now.isoformat().replace("+00:00", "Z"),
            "promoted": len(promoted), "entries": len(by_canonical),
            "counts": counts, "results": results,
            "orphan_entries": orphans,
            "coverage_pct": round(100.0 * (len(promoted) - sum(
                1 for r in results if r["kind"] is None)) / len(promoted), 1) if promoted else 100.0}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint falsifiers for promoted invariants")
    ap.add_argument("--root", default=None, help="estate root (default: this repo)")
    ap.add_argument("--json", action="store_true", help="machine receipt only")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ESTATE_ROOT

    try:
        report = lint(root)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"{UNVER_PREFIX}: {exc}")
        return 2

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        c = report["counts"]
        head = OK_PREFIX if c[FAIL] == 0 else FAIL_PREFIX
        print(f"{head} -- {report['promoted']} promoted, "
              f"{c[PASS]} PASS / {c[FAIL]} FAIL / {c[UNMEASURED]} UNMEASURED "
              f"(coverage {report['coverage_pct']}%)")
        for row in report["results"]:
            mark = {"PASS": "PASS", "FAIL": "FAIL", "UNMEASURED": "--  "}[row["status"]]
            print(f"  [{mark}] {row['canonical'][:8]} {str(row.get('kind') or 'none'):15s} "
                  f"{row['detail']}")
            print(f"          {row['claim']}")
        if report["orphan_entries"]:
            print(f"  note: {len(report['orphan_entries'])} falsifier entr(y/ies) "
                  f"for non-promoted rows")
    return 0 if report["counts"][FAIL] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
