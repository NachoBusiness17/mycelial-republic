#!/usr/bin/env python3
"""trajectory_minimizer.py - D11 last-mile trajectory minimizer (2026-09-30).

Mission (operator, watch/inbox/last_mile_20260930): "derive the trajectory
and minimize it... learn as we go". The trajectory (memory/trajectory/
steps.jsonl, 38K+ live rows - the raw standing wave) is compressed to its
signal core using the receipts as ground truth. Spec before code (build
discipline; new behavior only).

SIGNAL RULE (byte-backed; a row is signal if ANY prong holds):
  P1 receipt_minute: the step's ts (UTC) falls inside a minute cited by a
     receipt under watch/inbox (recursive *.md). Citations are regex-extracted
     only: ISO minute 'YYYY-MM-DDTHH:MM' tokens with optional tz marker (Z /
     +00:00 -> UTC; EDT -> UTC-4; EST -> UTC-5; wave = September 2026 = EDT;
     a bare token is UTC, the estate log convention), plus local 'H:MM
     EDT|EST|UTC' tokens anchored to the receipt FILENAME's date only when it
     carries exactly one date (ambiguous anchor -> skip). PRECISION LAW:
     day-only or hour-only citations make NO row signal - a citation too
     coarse to contain a step cannot cite a step's timeframe (receipts exist
     on every wave day; day granularity would mark the whole wave signal).
  P2 anomaly_named: the row is named by tools/anomaly_flagger.py's steps
     checks (malformed_json, hash_shape, ts_non_monotonic), IMPORTED live -
     never copied - so "named row" stays owned by one tool.
  P3 milestone: face == 'milestone' - the stream's own doctrine mark; these
     rows are the stream's built-in receipts. Everything else is noise
     (routine reads, standard writes).

OUTPUTS: --output minimal-trajectory JSONL (one entry per signal CLUSTER -
same session, ts contiguous within --cluster-gap minutes, same reason
family; carries WHAT WAS LEARNED: verb mix, exits, bounded gists, bounded
receipt pointers, not the raw bytes); --report JSON (coverage stat +
differentiator, the LEARNING); stdout summary. Census law: counts are
snapshots of one moment - the stream is live append-only; the report stamps
stream mtime + counts. Exit 0 classified; exit 2 usage/IO (missing stream
or inbox, or an inbox yielding ZERO minute citations - fail-closed: the
ground truth itself would be silently gone).
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parent.parent

# Dogfood: the anomaly flagger owns "named row" - import it, never copy it.
sys.path.insert(0, str(TOOL_ROOT))
import tools.anomaly_flagger as af  # noqa: E402

STEPS_PATH = TOOL_ROOT / "memory" / "trajectory" / "steps.jsonl"
INBOX_ROOT = TOOL_ROOT / "watch" / "inbox"
DEFAULT_OUTPUT = TOOL_ROOT / "watch" / "inbox" / "last_mile_20260930" / "TRAJECTORY_MINIMAL.jsonl"
DEFAULT_REPORT = TOOL_ROOT / "watch" / "inbox" / "last_mile_20260930" / "TRAJECTORY_MIN_REPORT.json"

EXIT_OK = 0
EXIT_USAGE = 2

# Year-anchored to 2026: the wave is a 2026 stream; a loose \d{4} would
# drag in receipts quoting foreign logs (2026-03 citations live here).
ISO_MIN_RE = re.compile(r"(2026-\d\d-\d\dT\d\d:\d\d)(Z|\+00:00|\s*(?:EDT|EST))?", re.IGNORECASE)
LOCAL_RE = re.compile(r"\b(\d{1,2}):(\d{2})\s*(EDT|EST|UTC)\b")
DATE_RE = re.compile(r"2026-\d\d-\d\d")
TZ_HOURS = {"EDT": 4, "EST": 5, "UTC": 0, "Z": 0, "+00:00": 0}  # EDT=-4 => UTC=local+4

RECEIPT_SUFFIXES = {".md"}
CITED_BY_BOUND = 3      # bounded pointers: at most 3 receipts named per minute
GISTS_PER_ENTRY = 5     # bounded gists: at most 5 named, then "+N more"
GIST_TEXT = 110         # gist line squash length


def _to_utc_minute(base_naive: datetime, marker: str) -> str:
    """Naive datetime + tz marker -> UTC minute (UTC = local + offset; EDT
    is UTC-4: 10:02 EDT -> 14:02 UTC - the first draft inverted the sign
    and the unit test caught it: west-of-Greenwich ADDs)."""
    return (base_naive + timedelta(hours=TZ_HOURS.get(marker, 0))
            ).strftime("%Y-%m-%dT%H:%M")


def extract_citations(inbox_root: Path) -> dict:
    """Receipt text -> cited UTC minutes + bounded receipt paths + stats
    (reads every *.md under inbox_root recursively)."""
    minutes: set[str] = set()
    cited_by: dict[str, list[str]] = defaultdict(list)
    stats = dict.fromkeys(("receipts_read", "tokens_iso", "tokens_local",
                           "tokens_local_anchored", "tokens_local_ambiguous_skipped"), 0)

    def note(minute: str, rel: str) -> None:
        minutes.add(minute)
        holders = cited_by[minute]
        if len(holders) < CITED_BY_BOUND or holders[-1] == rel:
            holders.append(rel)

    for path in sorted(inbox_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in RECEIPT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue  # unreadable receipt: it cannot cite anything
        stats["receipts_read"] += 1
        rel = str(path.relative_to(inbox_root))
        for match in ISO_MIN_RE.finditer(text):
            stats["tokens_iso"] += 1
            base, marker = match.group(1), (match.group(2) or "").strip().upper().replace(" ", "")
            note(_to_utc_minute(datetime.fromisoformat(base), marker or "UTC"), rel)
        days = set(DATE_RE.findall(path.name))
        if len(days) == 1:
            day = days.pop()
            for match in LOCAL_RE.finditer(text):
                stats["tokens_local"] += 1
                hour, mins, zone = int(match.group(1)), match.group(2), match.group(3).upper()
                try:
                    naive = datetime.fromisoformat(f"{day}T{hour:02d}:{mins}:00")
                except ValueError:
                    stats["tokens_local_ambiguous_skipped"] += 1  # e.g. 25:61
                    continue
                stats["tokens_local_anchored"] += 1
                note(_to_utc_minute(naive, zone), rel)
        elif LOCAL_RE.search(text):
            stats["tokens_local_ambiguous_skipped"] += len(LOCAL_RE.findall(text))
    return {**stats, "minutes": minutes, "cited_by": dict(cited_by)}


def anomaly_named_lines(steps_path: Path) -> dict[int, str]:
    """lineno -> check name, live anomaly_flagger definition on this stream."""
    findings, _total = af.scan_steps(steps_path)
    named: dict[int, str] = {}
    for finding in findings:
        for row in finding.rows:
            named[int(row.split(" ", 1)[0])] = finding.check
    return named


def coarse_shape(command: str | None) -> str:
    """Coarse instrument shape (head + subcommand for git / python -m / venv
    python): parameter detail is noise, instrument choice is substance (D11
    finding: instruments separate signal from noise, parameters do not)."""
    tokens = (command or "").replace("\\", " ").replace("/", " ").split()
    if not tokens:
        return "(empty)"
    head = tokens[0].strip('"')
    if head in (".venv", "..", ".") and len(tokens) > 1:
        return " ".join(tokens[:2])[:48]
    if head == "python" and len(tokens) > 1:
        sub = f"-m {tokens[2]}" if tokens[1] == "-m" and len(tokens) > 2 else tokens[1]
        return f"python {sub}"[:48]
    if head == "git" and len(tokens) > 1:
        return f"git {tokens[1]}"[:48]
    return head[:48]


def squash(text: str, bound: int = GIST_TEXT) -> str:  # one line, bounded
    return " ".join((text or "").split())[:bound]


def classify_stream(steps_path: Path, minutes: set[str],
                    anomaly_rows: dict[int, str]) -> tuple[list[dict], dict]:
    """One pass -> (rows, totals); malformed lines survive as bare rows."""
    rows: list[dict] = []
    totals = {"lines": 0, "parsed": 0, "malformed": 0}
    for lineno, row, _reason in af.iter_jsonl(steps_path):
        totals["lines"] += 1
        if row is None:
            totals["malformed"] += 1
            check = anomaly_rows.get(lineno)
            rows.append({"lineno": lineno, "parsed": False, "signal": bool(check),
                         "reasons": [f"anomaly:{check}"] if check else []})
            continue
        totals["parsed"] += 1
        ts = row.get("ts") or ""
        result = row.get("result") if isinstance(row.get("result"), dict) else {}
        reasons = []
        if ts[:16] in minutes:
            reasons.append("receipt_minute")
        if row.get("face") == "milestone":
            reasons.append("milestone")
        if lineno in anomaly_rows:
            reasons.append(f"anomaly:{anomaly_rows[lineno]}")
        rows.append({"lineno": lineno, "parsed": True, "ts": ts,
                     "session_id": row.get("session_id") or "", "face": row.get("face") or "",
                     "coarse": coarse_shape(row.get("command")), "command": row.get("command") or "",
                     "exit": result.get("exit"), "truncated": bool(result.get("truncated")),
                     "output": result.get("output_excerpt") or "",
                     "signal": bool(reasons), "reasons": reasons})
    return rows, totals


def cluster_signals(rows: list[dict], cited_by: dict[str, list[str]],
                    gap_minutes: int = 2) -> list[dict]:
    """Signal rows -> cluster entries: same session, ts contiguous within
    gap_minutes, same reason family; a noise row breaks the cluster. Entries
    carry what was learned (verbs, exits, gists) + receipt pointers."""
    entries: list[dict] = []
    current: dict | None = None
    prev_ts: datetime | None = None

    def close() -> None:
        nonlocal current
        if current is not None and current["count"]:
            gists = current["_gists"]
            entries.append({
                "ts_start": current["ts_start"], "ts_end": current["ts_end"],
                "session_id": current["session_id"], "rows": current["count"],
                "reason": current["reason"], "receipts": current["receipts"][:CITED_BY_BOUND],
                "verbs": dict(Counter(dict(current["_verbs"])).most_common(5)),
                "exits": dict(Counter(current["_exits"]).most_common(4)),
                "gists": gists[:GISTS_PER_ENTRY] + ([f"+{len(gists) - GISTS_PER_ENTRY} more"]
                            if len(gists) > GISTS_PER_ENTRY else [])})

    for row in rows:
        if not row.get("signal"):
            close()
            current, prev_ts = None, None
            continue
        reason = row["reasons"][0].split(":", 1)[0]
        ts = af.parse_ts(row.get("ts")) if row.get("ts") else None
        contiguous = (current is not None and row.get("session_id") == current["session_id"]
                      and reason == current["reason"] and ts is not None and prev_ts is not None
                      and abs((ts - prev_ts).total_seconds()) <= gap_minutes * 60)
        if not contiguous:
            close()
            current = {"ts_start": row.get("ts"), "ts_end": row.get("ts"),
                       "session_id": row.get("session_id") or "", "count": 0,
                       "reason": reason, "receipts": [], "_verbs": {},
                       "_exits": [], "_gists": []}
        current["count"] += 1
        current["ts_end"] = row.get("ts")
        verb = row.get("coarse") or "?"
        current["_verbs"][verb] = current["_verbs"].get(verb, 0) + 1
        if row.get("exit") is not None:
            current["_exits"].append(str(row["exit"]))
        if row.get("face") == "milestone":
            current["_gists"].append(f"MILESTONE: {squash(row.get('command'))}")
        elif row.get("parsed"):
            current["_gists"].append(f"{verb} exit={row.get('exit')} :: {squash(row.get('output'))}")
        else:  # unparseable anomaly-named row
            current["_gists"].append(f"unparseable row (anomaly-named) at line {row.get('lineno')}")
        for receipt in cited_by.get(row.get("ts", "")[:16], []):
            if receipt not in current["receipts"] and len(current["receipts"]) < CITED_BY_BOUND * 2:
                current["receipts"].append(receipt)
        prev_ts = ts or prev_ts
    close()
    return entries


def coverage(rows: list[dict], totals: dict, entries: list[dict],
             anomaly_rows: dict[int, str]) -> dict:
    """Coverage stat: what % of the wave's substance lives in what % of the
    rows (milestones + anomaly rows + cited minutes complete by construction;
    + distinct coarse instrument shapes carried by the signal rows)."""
    parsed = [r for r in rows if r.get("parsed")]
    signals = [r for r in rows if r.get("signal")]
    all_shapes = {r["coarse"] for r in parsed}
    signal_shapes = {r["coarse"] for r in signals if r.get("parsed")}
    n_rows = totals["lines"]
    ms_total = sum(1 for r in parsed if r.get("face") == "milestone")
    ms_signal = sum(1 for r in signals if r.get("face") == "milestone")
    anomaly_signal = sum(1 for r in signals if any(
        x.startswith("anomaly:") for x in r.get("reasons", [])))
    sessions_total = {r.get("session_id") for r in parsed}
    sessions_signal = {r.get("session_id") for r in signals if r.get("parsed")}
    pct = lambda a, b: round(100.0 * a / b, 2) if b else 0.0  # noqa: E731
    return {
        "snapshot": {"stream_lines": n_rows, "parsed_rows": totals["parsed"],
                     "malformed_rows": totals["malformed"]},
        "signal_rows": len(signals),
        "signal_rows_pct": pct(len(signals), n_rows),
        "substance": {
            "milestones": f"{ms_signal}/{ms_total}",
            "anomaly_named_rows": f"{anomaly_signal}/{len(anomaly_rows)}",
            "distinct_coarse_shapes": f"{len(signal_shapes)}/{len(all_shapes)}",
            "distinct_coarse_shapes_pct": pct(len(signal_shapes), len(all_shapes))},
        "sessions": {"total": len(sessions_total), "with_signal": len(sessions_signal),
                     "pure_noise": len(sessions_total - sessions_signal)},
        "compression": {"signal_rows": len(signals), "cluster_entries": len(entries),
                        "rows_per_entry": round(len(signals) / len(entries), 2) if entries else 0.0},
    }


def differentiate(rows: list[dict], min_count: int = 20) -> dict:
    """The LEARNING: feature shares in signal vs noise (enrichment = share
    ratio; only shapes with >= min_count rows rank - a 2-row shape carries
    no pattern). Features that FAIL to separate are honest negatives."""
    parsed = [r for r in rows if r.get("parsed")]
    signals = [r for r in parsed if r.get("signal")]
    noise = [r for r in parsed if not r.get("signal")]
    n_sig, n_noise = len(signals), len(noise)
    if not n_sig or not n_noise:
        return {"error": "degenerate split (empty signal or noise set)"}
    sig_verbs, noise_verbs = Counter(r["coarse"] for r in signals), Counter(r["coarse"] for r in noise)
    enriched, depleted = [], []
    for verb in set(sig_verbs) | set(noise_verbs):
        s_rows, n_rows_v = sig_verbs.get(verb, 0), noise_verbs.get(verb, 0)
        if s_rows + n_rows_v < min_count:
            continue
        s_share, n_share = s_rows / n_sig, n_rows_v / n_noise
        ratio = s_share / n_share if n_share > 0 else float("inf")
        row = {"verb": verb, "signal_rows": s_rows, "signal_pct": round(100 * s_share, 2),
               "noise_rows": n_rows_v, "noise_pct": round(100 * n_share, 2),
               "enrichment": round(ratio, 2) if ratio != float("inf") else None}
        if ratio >= 1.5:
            enriched.append(row)
        elif ratio <= 0.5:
            depleted.append(row)
    enriched.sort(key=lambda r: -r["signal_pct"])
    depleted.sort(key=lambda r: r["signal_pct"])

    def rate(subset: list[dict], predicate) -> float:
        return round(100.0 * sum(1 for r in subset if predicate(r)) / len(subset), 2)

    def local_hour(r: dict) -> int | None:  # operator-local hour (EDT = UTC-4)
        try:
            return (int(r["ts"][11:13]) - 4) % 24
        except (TypeError, ValueError, KeyError):
            return None

    hours = lambda subset: Counter(h for r in subset  # noqa: E731
                                   if (h := local_hour(r)) is not None)
    lens = lambda subset: [len(r.get("command") or "") for r in subset]  # noqa: E731
    both = lambda pred: {"signal": rate(signals, pred), "noise": rate(noise, pred)}  # noqa: E731
    return {
        "enriched_in_signal": enriched[:12],
        "depleted_in_signal": depleted[:12],
        "honest_negatives": {
            "exit_nonzero_pct": both(lambda r: r.get("exit") not in (0, None)),
            "truncated_pct": both(lambda r: r.get("truncated")),
            "command_len_median": {"signal": statistics.median(lens(signals)),
                                   "noise": statistics.median(lens(noise))}},
        "operator_local_hours_top": {"signal": hours(signals).most_common(5),
                                     "noise": hours(noise).most_common(5)},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--steps", type=Path, default=STEPS_PATH)
    parser.add_argument("--inbox", type=Path, default=INBOX_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--cluster-gap", type=int, default=2)      # minutes inside a cluster
    parser.add_argument("--min-shape-count", type=int, default=20)  # differentiator floor
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    for label, path, present in (("steps stream", args.steps, args.steps.is_file()),
                                 ("receipts inbox", args.inbox, args.inbox.is_dir())):
        if not present:
            print(f"IO-ERROR: {label} not found: {path}", file=sys.stderr)
            return EXIT_USAGE
    citations = extract_citations(args.inbox)
    if not citations["minutes"]:
        print("IO-ERROR: receipts yielded ZERO minute citations - ground truth "
              "missing; refusing to classify everything as noise", file=sys.stderr)
        return EXIT_USAGE

    anomaly_rows = anomaly_named_lines(args.steps)
    rows, totals = classify_stream(args.steps, citations["minutes"], anomaly_rows)
    entries = cluster_signals(rows, citations["cited_by"], gap_minutes=args.cluster_gap)
    cov = coverage(rows, totals, entries, anomaly_rows)
    cov["citations"] = {k: (len(v) if k == "minutes" else v)
                        for k, v in citations.items() if k != "cited_by"}
    cov["stream_mtime_utc"] = datetime.fromtimestamp(
        args.steps.stat().st_mtime, tz=timezone.utc).isoformat()
    report = {"coverage": cov,
              "differentiator": differentiate(rows, min_count=args.min_shape_count)}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if not args.quiet:
        sub, comp, snap = cov["substance"], cov["compression"], cov["snapshot"]
        print(f"MINIMAL TRAJECTORY: {cov['signal_rows']}/{snap['stream_lines']} rows signal "
              f"({cov['signal_rows_pct']}%) -> {comp['cluster_entries']} cluster entries "
              f"({comp['rows_per_entry']} rows/entry)")
        print(f"substance: milestones {sub['milestones']}, anomaly rows "
              f"{sub['anomaly_named_rows']}, coarse shapes {sub['distinct_coarse_shapes']} "
              f"({sub['distinct_coarse_shapes_pct']}%)")
        print(f"sessions: {cov['sessions']['with_signal']}/{cov['sessions']['total']} carry "
              f"signal; {cov['sessions']['pure_noise']} pure-noise sessions")
        diff = report["differentiator"]
        if "error" not in diff:
            print("top signal-enriched verbs: " + ", ".join(
                f"{t['verb']} (x{t['enrichment']}, {t['signal_pct']}% vs {t['noise_pct']}%)"
                for t in diff["enriched_in_signal"][:3]))
        print(f"output: {args.output}\nreport: {args.report}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
