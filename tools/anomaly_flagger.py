"""anomaly_flagger.py - IMP6 last-mile anomaly sweep (2026-09-30).

Mission (operator, watch/inbox/last_mile_20260930): flag byte-level
anomalies on three estate streams, name the offending rows, and exit
0 clean / 1 anomalies. Spec filed here BEFORE the code per the build
discipline (spec-before-behavior; this tool introduces new behavior,
it changes none).

Q36 amendment (2026-10-01, watch/inbox/mountain_climb/
FIFTY_QUESTIONS_ANSWERED.md Q36 FAIL): the steps surface was shape-only
- mutated text under a shape-valid 16-hex hash read "clean" (clean
meant well-formed, not intact). It gains an integrity arm (spec below).
The tool REPORTS; it never repairs or rewrites any stream.

Surfaces and checks (contract fixed by the mission):

1. memory/trajectory/steps.jsonl  (the mag.trajectory_step STREAM,
   mag/trajectory_step.py:50; live append-only, so row counts are a
   census of one moment, never a constant - AGENTS.md census law):
   - malformed_json: any line that is not exactly one JSON object
     (blank lines count as malformed rows: the stream contract is one
     row per line, mag/trajectory_step.py append_row).
   - hash_shape: step_hash must fullmatch [0-9a-f]{16} (the writer emits
     sha256(basis)[:16], mag/trajectory_step.py:152). Shape only.
   - hash_integrity (Q36): where a row's bytes allow it, recompute the
     basis sha256(session_id|ts|command|result.output_excerpt)[:16] -
     OWNED by mag.trajectory_step make_row/verify, READ here, never
     rewritten - and compare: shape-valid hash + complete basis +
     mismatch = TAMPERED (clean now means intact, not just well-formed);
     match = verified.
   - hash_unverifiable (Q36): rows whose bytes cannot be compared
     (step_hash not a comparable [0-9a-f]{16} literal, or any basis
     field not a str) - never silently clean, never guessed tampered.
     Malformed lines stay owned by malformed_json; a row may be named by
     hash_shape AND hash_unverifiable (a None hash violates shape AND
     comparison; the classes measure different things and both stay).
   - ts_non_monotonic: the stream is appended under wall-clock UTC
     (make_row -> _utcnow), so ts must be non-decreasing in file order;
     every strict descent names its row. A "run" is a stretch of
     descents on adjacent rows. Equal ts is legal (concurrent writers).

2. watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl:
   - ts_sort: same non-decreasing contract. Root cause note: the miner
     (watch/inbox/mates_leave_protocol/oral_law_mine_20260930.py:145)
     shuffles its thread sample with a fixed seed, so descents here
     measure distance-from-sorted against the ascending source index
     (corpus/oral_history/seat_pools/session_index.jsonl); they are
     structural, named row-by-row for the operator to judge.
   - dup_thread_id: thread_id must be unique (the miner skips done_ids);
     every duplicated id names all its rows.

3. memory/burns/LEDGER.jsonl joined to memory/burns/verdict_enum_map.json:
   - Per the map's own join law, ledger.verdict -> census[verdict]; a
     verdict absent from the census (younger than the map) falls back to
     tools.burns_verdict_enum.normalize() live.
   - Reported counts: OTHER (canonical enum OTHER) and REVIEW
     (review=true). These are census lines, not anomalies: the map's
     exact/prefix rules deliberately flag many known verdicts for
     review triage.
   - ANOMALY classes: fallback_unknown (verdict known to neither census
     nor rules - map-age drift) and evidence paths missing on a
     deterministic evenly-spaced sample (default 50 rows; --sample 0 =
     all rows). landing is repo-relative.

Exit codes: 0 clean, 1 anomalies (rows named on stdout), 2 usage/IO.
Steps integrity counts print as one informational census line per run
(verified=N tampered=T unverifiable=U); both Q36 classes are anomalies
and drive exit 1 like every other finding.
Budget: full live sweep well under 60s (~2s at 37k+ rows on 2026-09-30;
the integrity arm adds one sha256 per recomputable row).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent

STEPS_PATH = TOOL_ROOT / "memory" / "trajectory" / "steps.jsonl"
ORAL_PATH = TOOL_ROOT / "watch" / "inbox" / "operator_model" / "ORAL_LAW_INDEX.jsonl"
LEDGER_PATH = TOOL_ROOT / "memory" / "burns" / "LEDGER.jsonl"
ENUM_MAP_PATH = TOOL_ROOT / "memory" / "burns" / "verdict_enum_map.json"

# Writer contract: hashlib.sha256(basis).hexdigest()[:16] -> 16 lowercase hex.
STEP_HASH_RE = re.compile(r"[0-9a-f]{16}")

EXIT_CLEAN = 0
EXIT_ANOMALIES = 1
EXIT_USAGE = 2


class Finding:
    """One anomaly class on one surface, with its named rows."""

    def __init__(self, surface: str, check: str, rows: list[str], summary: str,
                 anomaly: bool = True):
        self.surface = surface
        self.check = check
        self.rows = rows          # one rendered name per offending row
        self.summary = summary
        self.anomaly = anomaly    # False = informational census line

    def render(self, max_rows: int) -> str:
        head = f"[{'x' if self.anomaly else ' '}] {self.check}: {self.summary}"
        if not self.rows:
            return head
        shown = self.rows[:max_rows]
        more = len(self.rows) - len(shown)
        tail = f" (+{more} more)" if more > 0 else ""
        return f"{head} -> {', '.join(shown)}{tail}"


def parse_ts(value) -> datetime | None:
    """ISO-8601 ts -> aware datetime, else None (Z and +00:00 both live
    in these streams; fromisoformat handles both on this venv's 3.11)."""
    if not isinstance(value, str) or not value:
        return None
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def iter_jsonl(path: Path):
    """Yield (lineno, row-or-None, reason) for every physical line.

    Blank lines are yielded as malformed (reason 'blank line'); parse
    failures carry the JSONDecodeError text. Never raises on content.
    """
    with path.open(encoding="utf-8", errors="replace") as handle:
        for lineno, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                yield lineno, None, "blank line"
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                yield lineno, None, str(exc)
                continue
            yield lineno, row, None


def group_runs(events: list[int]) -> int:
    """Count maximal runs of adjacent line numbers (descent events that
    sit on consecutive rows form one non-monotonic run)."""
    if not events:
        return 0
    runs = 1
    for prev, cur in zip(events, events[1:]):
        if cur != prev + 1:
            runs += 1
    return runs


def scan_monotonic_ts(path: Path, surface: str, check: str) -> list[Finding]:
    """Shared engine for steps ts_non_monotonic and oral ts_sort:
    malformed lines, then strict descents against the previous parsed
    ts (comparison survives malformed rows - the stream is append-only,
    so a descent across a gap is still a descent)."""
    findings: list[Finding] = []
    malformed: list[str] = []
    descents: list[str] = []
    descent_rows: list[int] = []
    unparseable: list[str] = []
    prev: datetime | None = None
    prev_raw = ""
    total = 0
    for lineno, row, reason in iter_jsonl(path):
        total += 1
        if row is None:
            malformed.append(f"{lineno} ({reason})")
            continue
        ts = parse_ts(row.get("ts"))
        if ts is None:
            unparseable.append(f"{lineno} (ts={row.get('ts')!r})")
            continue
        if prev is not None and ts < prev:
            descents.append(f"{lineno} ({prev_raw} -> {row.get('ts')})")
            descent_rows.append(lineno)
        prev, prev_raw = ts, row.get("ts")
    if malformed:
        findings.append(Finding(surface, "malformed_json", malformed,
                                f"{len(malformed)} of {total} rows"))
    if unparseable:
        findings.append(Finding(surface, check + "_unparseable_ts", unparseable,
                                f"{len(unparseable)} rows lack a comparable ISO ts"))
    if descents:
        runs = group_runs(descent_rows)
        findings.append(Finding(surface, check, descents,
                                f"{len(descents)} descent(s) in {runs} run(s) of {total} rows"))
    if not findings:
        findings.append(Finding(surface, "malformed_json+ts", [],
                                f"0 of {total} rows", anomaly=False))
    return findings


# Q36 integrity arm: basis OWNED by mag.trajectory_step (make_row joins
# session_id|ts|command|excerpt; verify recomputes the same four) - READ
# here, never rewritten. Local, not imported, so the sweep stays
# stdlib-only; if the owner's basis ever changes, this arm fails LOUD
# (mass tampered), never silently clean.
_BASIS_TOP = ("session_id", "ts", "command")


def integrity_of(row) -> tuple[str | None, list[str]]:
    """One pass: (recomputed step_hash | None, named basis gaps)."""
    if not isinstance(row, dict):
        return None, ["row not a JSON object"]
    gaps = [name for name in _BASIS_TOP if not isinstance(row.get(name), str)]
    result = row.get("result")
    if not (isinstance(result, dict)
            and isinstance(result.get("output_excerpt"), str)):
        gaps.append("result.output_excerpt")
    if gaps:
        return None, gaps
    basis = "|".join([row[name] for name in _BASIS_TOP]
                     + [result["output_excerpt"]])
    return hashlib.sha256(basis.encode("utf-8", "replace")).hexdigest()[:16], []


def scan_steps(path: Path) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    bad_hash: list[str] = []
    tampered: list[str] = []
    unverifiable: list[str] = []
    verified = 0
    total = 0
    for lineno, row, reason in iter_jsonl(path):
        total += 1
        if row is None:
            continue  # malformed_json owns it (ts scan below, same iter)
        step_hash = row.get("step_hash") if isinstance(row, dict) else None
        comparable = (isinstance(step_hash, str)
                      and bool(STEP_HASH_RE.fullmatch(step_hash)))
        if not comparable:
            bad_hash.append(f"{lineno} (step_hash={step_hash!r})")
        # Q36: TAMPERED only on comparable hash + complete basis +
        # mismatch; UNVERIFIABLE when either side of the comparison is
        # missing - never silently clean, never guessed tampered.
        recomputed, gaps = integrity_of(row)
        if gaps or not comparable:
            why = gaps + ([f"step_hash not comparable ({step_hash!r})"]
                          if not comparable else [])
            unverifiable.append(f"{lineno} ({'; '.join(why)})")
        elif recomputed == step_hash:
            verified += 1
        else:
            tampered.append(f"{lineno} (stored {step_hash} "
                            f"!= recomputed {recomputed})")
    if bad_hash:
        findings.append(Finding("steps", "hash_shape", bad_hash,
                                f"{len(bad_hash)} row(s) violate [0-9a-f]{{16}}"))
    if tampered:
        findings.append(Finding("steps", "hash_integrity", tampered,
                                f"{len(tampered)} row(s) TAMPERED: shape-valid "
                                f"hash, recomputed basis mismatch"))
    if unverifiable:
        findings.append(Finding("steps", "hash_unverifiable", unverifiable,
                                f"{len(unverifiable)} row(s) cannot be compared "
                                f"(never silently clean)"))
    # Census line carries the denominator (census law: one instrument,
    # one moment).
    findings.append(Finding("steps", "hash_integrity_census", [],
                            f"verified={verified} tampered={len(tampered)} "
                            f"unverifiable={len(unverifiable)} "
                            f"(malformed rows excluded)", anomaly=False))
    findings.extend(scan_monotonic_ts(path, "steps", "ts_non_monotonic"))
    return findings, total


def scan_oral(path: Path) -> tuple[list[Finding], int]:
    seen: dict[str, list[int]] = {}
    total = 0
    for lineno, row, reason in iter_jsonl(path):
        total += 1
        if row is None:
            continue
        thread_id = row.get("thread_id") if isinstance(row, dict) else None
        if isinstance(thread_id, str):
            seen.setdefault(thread_id, []).append(lineno)
    findings = scan_monotonic_ts(path, "oral_law_index", "ts_sort")
    dups = {tid: rows for tid, rows in seen.items() if len(rows) > 1}
    if dups:
        rows_named = [f"{tid} at {','.join(map(str, rows))}"
                      for tid, rows in sorted(dups.items())]
        findings.append(Finding("oral_law_index", "dup_thread_id", rows_named,
                                f"{len(dups)} duplicated id(s) over {sum(len(r) for r in dups.values())} rows"))
    else:
        findings.append(Finding("oral_law_index", "dup_thread_id", [],
                                f"0 duplicated id(s) over {total} rows", anomaly=False))
    return findings, total


def _default_normalize(verdict: str) -> dict:
    # Local import so the module imports cleanly even when the sibling
    # tool is being refactored; the join law names it explicitly.
    import tools.burns_verdict_enum as bve
    return bve.normalize(verdict)


def scan_burns(ledger_path: Path, map_path: Path, sample: int = 50,
               normalize=_default_normalize) -> tuple[list[Finding], int]:
    enum_map = json.loads(map_path.read_text(encoding="utf-8"))
    census = enum_map.get("census", {})
    rows = []
    with ledger_path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            row = json.loads(stripped)
            row["_lineno"] = lineno
            rows.append(row)

    other: list[str] = []
    review: list[str] = []
    fallback: list[str] = []
    for row in rows:
        verdict = row.get("verdict", "")
        entry = census.get(verdict)
        if entry is not None:
            enum, flagged, via = entry.get("enum"), bool(entry.get("review")), "census"
        else:
            norm = normalize(verdict)
            enum, flagged, via = norm.get("canonical"), bool(norm.get("review")), norm.get("rule")
        name = f"{row['_lineno']} ({verdict[:40]!r})"
        if enum == "OTHER":
            other.append(name)
        if flagged:
            review.append(name)
        if via == "fallback_unknown":
            fallback.append(name)

    # Informational census line (anomaly=False): counts plus bounded row
    # names for OTHER/REVIEW so the operator can spot-check triage rows;
    # render() bounds what actually prints via --max-rows.
    findings = [
        Finding("burns_ledger", "verdict_enum", other + review,
                f"rows={len(rows)} OTHER={len(other)} REVIEW={len(review)} "
                f"fallback_unknown={len(fallback)}", anomaly=False),
    ]
    if fallback:
        findings.append(Finding("burns_ledger", "fallback_unknown", fallback,
                                f"{len(fallback)} verdict(s) unknown to census and rules"))
    if sample == 0:
        sampled = rows
    else:
        step = max(1, len(rows) // max(1, sample))
        sampled = rows[::step][:sample]
    missing = []
    no_field = []
    for row in sampled:
        landing = row.get("landing")
        if not landing:
            no_field.append(f"{row['_lineno']} (no landing field)")
        elif not (TOOL_ROOT / landing).exists():
            missing.append(f"{row['_lineno']} ({landing})")
    scope = f"sample {len(sampled)}/{len(rows)}"
    if missing:
        findings.append(Finding("burns_ledger", "evidence_missing", missing,
                                f"{len(missing)} landing path(s) absent, {scope}"))
    if no_field:
        findings.append(Finding("burns_ledger", "evidence_no_field", no_field,
                                f"{len(no_field)} row(s) lack landing, {scope}"))
    if not missing and not no_field:
        findings.append(Finding("burns_ledger", "evidence_paths", [],
                                f"0 missing, {scope}", anomaly=False))
    return findings, len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sample", type=int, default=50,
                        help="burns evidence sample size (0 = all rows, default 50)")
    parser.add_argument("--max-rows", type=int, default=10,
                        help="max named rows printed per class (default 10)")
    parser.add_argument("--steps", type=Path, default=STEPS_PATH,
                        help="override steps.jsonl path (tests, frozen snapshots)")
    parser.add_argument("--oral", type=Path, default=ORAL_PATH,
                        help="override ORAL_LAW_INDEX.jsonl path")
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH,
                        help="override burns LEDGER.jsonl path")
    parser.add_argument("--enum-map", type=Path, default=ENUM_MAP_PATH,
                        help="override verdict_enum_map.json path")
    args = parser.parse_args(argv)

    started = time.perf_counter()
    for name, path in (("steps", args.steps), ("oral_law_index", args.oral),
                       ("burns_ledger", args.ledger), ("burns_enum_map", args.enum_map)):
        if not path.exists():
            print(f"IO-ERROR: {name} stream missing: {path}", file=sys.stderr)
            return EXIT_USAGE

    all_findings: list[Finding] = []
    for name, path, scan in (("steps", args.steps, scan_steps),
                             ("oral_law_index", args.oral, scan_oral)):
        findings, total = scan(path)
        print(f"SURFACE {name} {path} ({total} rows)")
        for finding in findings:
            print("  " + finding.render(args.max_rows))
        all_findings.extend(findings)
    findings, total = scan_burns(args.ledger, args.enum_map, sample=args.sample)
    print(f"SURFACE burns_ledger {args.ledger} ({total} rows)")
    for finding in findings:
        print("  " + finding.render(args.max_rows))
    all_findings.extend(findings)

    anomalies = [f for f in all_findings if f.anomaly]
    elapsed = time.perf_counter() - started
    named = sum(len(f.rows) for f in anomalies)
    if anomalies:
        print(f"ANOMALIES: {len(anomalies)} class(es), {named} row(s) named, "
              f"{elapsed:.2f}s -> exit {EXIT_ANOMALIES}")
        return EXIT_ANOMALIES
    print(f"CLEAN: 0 anomaly classes, {elapsed:.2f}s -> exit {EXIT_CLEAN}")
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
