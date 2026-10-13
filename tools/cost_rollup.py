#!/usr/bin/env python3
"""cost_rollup.py — one read-only rollup over every scattered cost surface.

Cost truth lives in five schemas that nothing aggregates:
  logs/duel/duels.jsonl            a_cost/b_cost/judge_cost per duel row (ts in row)
  logs/mates/*.jsonl               cost_usd + model (day from filename YYYYMMDD)
  logs/hermes_gopher_burn_*/*.jsonl cost_usd + model (day from dir/file YYYYMMDD)
  memory/runs/hermes_burn/usage.jsonl  cost_usd + model (the Nous burn carrier
                                   ledger; fifth surface, ops-triage move 2
                                   2026-10-07 - the estate's biggest single-
                                   surface spend ledger previously priced at
                                   zero by this rollup)
  training/cost_ledger.jsonl       cost_ledger.v1: actual.usd_est+usd_fixed,
                                   actual.calls, platform.model (falls back to
                                   estimate.model then platform.seat)

This tool scans all five, rolls up per (day, model): calls, total_usd and the
contributing surfaces, plus grand total and a trailing 7-day trend. Unparseable
surfaces (bad JSON line, unreadable file, missing required surface) are NAMED
in the output with path + line + error and never dropped silently.

Every completed run also writes memory/runs/spend_balance.json
(spend_balance.v1: as_of, spent per ledger path, grand totals, the recorded
pot/armed figures with their sources, and the provider balance marked
unknown-with-evidence-pointer). This is the twice-owed Oct 2 move
(watch/inbox/ractor_engine/ractor-topic/economics.md:128 "mint
memory/runs/spend_balance.json {pot, armed, as_of, spent per ledger path,
balance} written by cost_rollup on every run"; re-owed by
break-economics.md:377 after the 10-06 premium wall).

Usage:
  python tools/cost_rollup.py            # text report
  python tools/cost_rollup.py --json     # dashboard payload
  python tools/cost_rollup.py --days 14  # wider trend window
  python tools/cost_rollup.py --root P   # scan a different tree (tests)

Exit codes: 0 always for a completed scan (unparseable rows are reported in
band, not as a crash); 2 only when the scan itself cannot run at all.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TREND_DAYS = 7
DATE_IN_NAME = re.compile(r"(20\d{6})")

SURFACE_DUELS = "logs/duel/duels.jsonl"
SURFACE_MATES_GLOB = "logs/mates/*.jsonl"
SURFACE_GOPHER_GLOB = "logs/hermes_gopher_burn_*/*.jsonl"
SURFACE_HERMES_BURN = "memory/runs/hermes_burn/usage.jsonl"
SURFACE_LEDGER = "training/cost_ledger.jsonl"

SPEND_BALANCE_RELPATH = "memory/runs/spend_balance.json"
# Recorded funding figures, carried with their sources (never reconciled
# here; the economics finding named "three coexisting armed figures, one
# unanchored balance"):
RECORDED_FUNDING = {
    "hermes_order_2026_10_01_usd": 70.0,   # "70+$ hermes credits", tools/hermes_burn.py order header
    "driving_ladder_2026_09_28_usd": 180.0,  # "$180 Nous credits", RIB_DRIVING_LADDER_20260928
    "agents_md_armed_2026_09_14_usd": 220.0,  # "$220 armed - audit 2026-09-14", AGENTS.md boot recap
}
BALANCE_NOTE = (
    "no balance endpoint on inference-api.nousresearch.com (8 candidate GET "
    "paths 404, 2026-10-07 probe); provider returns usage.cost per call "
    "(rate_source openrouter_list). Key-2 balance bounded [0.16, 0.17) USD "
    "by the max_tokens reserve ladder (usage.jsonl PROBE_LADDER_* rows: "
    "mt=16000 pays, mt=17000 402s); key-1 < 0.16 (mt=16000 402) and > 0 "
    "(1-token pays). A 402 is reserve-cost vs remaining balance, not "
    "account death and not per-model.")


@dataclass
class CostRow:
    day: str  # YYYY-MM-DD (UTC)
    model: str
    calls: int
    usd: float
    surface: str


@dataclass
class SurfaceStat:
    surface: str
    rows: int = 0
    cost_rows: int = 0


@dataclass
class ScanResult:
    rows: list[CostRow] = field(default_factory=list)
    stats: list[SurfaceStat] = field(default_factory=list)
    unparseable: list[dict] = field(default_factory=list)


def _fail(unparseable: list[dict], surface: str, error: str, line: int | None = None) -> None:
    item = {"surface": surface, "error": error}
    if line is not None:
        item["line"] = line
    unparseable.append(item)


def _day_from_name(path: Path) -> str | None:
    m = DATE_IN_NAME.search(path.name) or DATE_IN_NAME.search(str(path.parent))
    if not m:
        return None
    raw = m.group(1)
    try:
        return dt.date(int(raw[:4]), int(raw[4:6]), int(raw[6:8])).isoformat()
    except ValueError:
        return None


def _day_from_mtime(path: Path) -> str | None:
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).date().isoformat()
    except OSError:
        return None


def _day_for(path: Path, row: dict) -> str | None:
    ts = row.get("ts") or row.get("timestamp") or row.get("created_at")
    if isinstance(ts, str) and len(ts) >= 10:
        raw = ts[:10]
        try:
            return dt.date.fromisoformat(raw).isoformat()
        except ValueError:
            pass
    return _day_from_name(path) or _day_from_mtime(path)


def _num(value) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _scan_jsonl(path: Path, surface: str, row_costs, out: ScanResult) -> None:
    """row_costs(path, row) -> list[(model, calls, usd)] ; schema adapter seam."""
    stat = SurfaceStat(surface=surface)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        _fail(out.unparseable, surface, f"unreadable: {exc}")
        out.stats.append(stat)
        return
    for lineno, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            _fail(out.unparseable, surface, f"bad JSON: {exc.msg}", line=lineno)
            continue
        if not isinstance(row, dict):
            _fail(out.unparseable, surface, "row is not a JSON object", line=lineno)
            continue
        stat.rows += 1
        day = _day_for(path, row)
        costs = row_costs(path, row)
        if day is None and costs:
            _fail(out.unparseable, surface, "cost row without a resolvable day (no ts, no date in name, no mtime)", line=lineno)
            continue
        if costs:
            stat.cost_rows += 1
            for model, calls, usd in costs:
                out.rows.append(CostRow(day=day, model=model or "unknown", calls=calls, usd=usd, surface=surface))
    out.stats.append(stat)


def _duel_costs(_path: Path, row: dict):
    costs = []
    for model_key, cost_key in (("a_model", "a_cost"), ("b_model", "b_cost"), ("judge", "judge_cost")):
        usd = _num(row.get(cost_key))
        if usd is not None:
            costs.append((row.get(model_key), 1, usd))
    usd = _num(row.get("cost_usd"))  # simplified single-model duel rows, if they appear
    if usd is not None and not costs:
        costs.append((row.get("model"), 1, usd))
    return costs


def _simple_costs(_path: Path, row: dict):
    usd = _num(row.get("cost_usd"))
    if usd is None:
        usd = _num(row.get("cost"))
    if usd is None:
        return []
    return [(row.get("model"), 1, usd)]


def _ledger_costs(_path: Path, row: dict):
    actual = row.get("actual") or {}
    usd = _num(actual.get("usd_est")) or 0.0
    usd += _num(actual.get("usd_fixed")) or 0.0
    calls = actual.get("calls")
    calls = calls if isinstance(calls, int) and calls >= 0 else 0
    platform = row.get("platform") or {}
    estimate = row.get("estimate") or {}
    model = platform.get("model") or estimate.get("model") or platform.get("seat")
    if usd == 0.0 and calls == 0:
        return []  # route-only no-op rows carry no cost truth
    return [(model, calls, usd)]


def scan(root: Path) -> ScanResult:
    out = ScanResult()
    root = Path(root)

    duels = root / SURFACE_DUELS
    if duels.exists():
        _scan_jsonl(duels, SURFACE_DUELS, _duel_costs, out)
    else:
        _fail(out.unparseable, SURFACE_DUELS, "required surface missing")

    for path in sorted(root.glob(SURFACE_MATES_GLOB)):
        _scan_jsonl(path, path.relative_to(root).as_posix(), _simple_costs, out)

    for path in sorted(root.glob(SURFACE_GOPHER_GLOB)):
        _scan_jsonl(path, path.relative_to(root).as_posix(), _simple_costs, out)

    hermes_burn = root / SURFACE_HERMES_BURN
    if hermes_burn.exists():
        _scan_jsonl(hermes_burn, SURFACE_HERMES_BURN, _simple_costs, out)
    else:
        _fail(out.unparseable, SURFACE_HERMES_BURN, "required surface missing")

    ledger = root / SURFACE_LEDGER
    if ledger.exists():
        _scan_jsonl(ledger, SURFACE_LEDGER, _ledger_costs, out)
    else:
        _fail(out.unparseable, SURFACE_LEDGER, "required surface missing")

    return out


def rollup(rows: list[CostRow]) -> list[dict]:
    cells: dict[tuple[str, str], dict] = {}
    for r in rows:
        if r.calls == 0 and r.usd == 0.0:
            continue
        cell = cells.setdefault(
            (r.day, r.model),
            {"day": r.day, "model": r.model, "calls": 0, "total_usd": 0.0, "surfaces": set()},
        )
        cell["calls"] += r.calls
        cell["total_usd"] += r.usd
        cell["surfaces"].add(r.surface)
    return [
        {
            "day": c["day"],
            "model": c["model"],
            "calls": c["calls"],
            "total_usd": round(c["total_usd"], 4),
            "surfaces": sorted(c["surfaces"]),
        }
        for c in sorted(cells.values(), key=lambda c: (c["day"], c["model"]))
    ]


def trend(cells: list[dict], days: int) -> list[dict]:
    daily: dict[str, float] = defaultdict(float)
    for c in cells:
        daily[c["day"]] += c["total_usd"]
    if not daily:
        return []
    latest = max(dt.date.fromisoformat(d) for d in daily)
    window = []
    for offset in range(days - 1, -1, -1):
        day = (latest - dt.timedelta(days=offset)).isoformat()
        window.append({"day": day, "total_usd": round(daily.get(day, 0.0), 4)})
    return window


def build_report(root: Path, days: int = TREND_DAYS) -> dict:
    scan_res = scan(root)
    cells = rollup(scan_res.rows)
    grand_usd = round(sum(c["total_usd"] for c in cells), 4)
    grand_calls = sum(c["calls"] for c in cells)
    return {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "root": str(Path(root).resolve()),
        "trend_days": days,
        "surfaces": [
            {"surface": s.surface, "rows": s.rows, "cost_rows": s.cost_rows} for s in scan_res.stats
        ],
        "rollup": cells,
        "grand_total_usd": grand_usd,
        "grand_total_calls": grand_calls,
        "trend": trend(cells, days),
        "unparseable": sorted(scan_res.unparseable, key=lambda u: (u["surface"], u.get("line", 0))),
    }


def build_spend_balance(root: Path, report: dict) -> dict:
    """spend_balance.v1 (the Oct 2 economics move, landed 2026-10-07): spent
    per ledger path + grand totals + the recorded funding figures with their
    sources + the provider balance marked unknown with its evidence pointer.
    The balance note is a stamped probe verdict, not a live figure: no
    balance endpoint exists on the provider, so the honest value is the
    bound carried in BALANCE_NOTE until an operator top-up receipt lands."""
    spent: dict[str, dict] = {}
    for s in report["surfaces"]:
        usd = round(sum(c["total_usd"] for c in report["rollup"]
                        if s["surface"] in c["surfaces"]), 4)
        spent[s["surface"]] = {"rows": s["rows"], "cost_rows": s["cost_rows"],
                               "usd": usd}
    return {
        "schema": "spend_balance.v1",
        "as_of": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "writer": "tools/cost_rollup.py",
        "spent_per_ledger_path": spent,
        "grand_total_usd": report["grand_total_usd"],
        "grand_total_calls": report["grand_total_calls"],
        "recorded_funding_usd": dict(RECORDED_FUNDING),
        "balance": {"provider_api_usd": None, "note": BALANCE_NOTE},
        "unparseable_surfaces": len(report["unparseable"]),
    }


def write_spend_balance(root: Path, report: dict) -> Path:
    path = Path(root) / SPEND_BALANCE_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_spend_balance(root, report), indent=2,
                   ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def render_text(report: dict) -> str:
    lines = []
    lines.append(f"COST ROLLUP  generated {report['generated_utc']}  root {report['root']}")
    lines.append("")
    lines.append("surfaces scanned:")
    if report["surfaces"]:
        for s in report["surfaces"]:
            lines.append(f"  {s['surface']}  rows={s['rows']} cost_rows={s['cost_rows']}")
    else:
        lines.append("  (none found)")
    lines.append("")
    lines.append("per day x model:")
    lines.append("  day         model                          calls        usd  surfaces")
    for c in report["rollup"]:
        surf = ",".join(c["surfaces"])
        lines.append(f"  {c['day']}  {c['model'][:30]:<30} {c['calls']:>6}  {c['total_usd']:>9.4f}  {surf}")
    if not report["rollup"]:
        lines.append("  (no cost rows)")
    lines.append("")
    lines.append(f"GRAND TOTAL  ${report['grand_total_usd']:.4f}  over {report['grand_total_calls']} calls")
    tr = report["trend"]
    if tr:
        lines.append(f"{report['trend_days']}-day trend ({tr[0]['day']} .. {tr[-1]['day']}):")
        peak = max(t["total_usd"] for t in tr) or 1.0
        for t in tr:
            bar = "#" * int(round(t["total_usd"] / peak * 30))
            lines.append(f"  {t['day']}  {t['total_usd']:>9.4f}  {bar}")
    lines.append("")
    lines.append("UNPARSEABLE (named, never dropped):")
    if report["unparseable"]:
        for u in report["unparseable"]:
            where = f" line {u['line']}" if "line" in u else ""
            lines.append(f"  {u['surface']}{where}: {u['error']}")
    else:
        lines.append("  (none)")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Roll up scattered cost surfaces (duels, mates, gopher burn, cost ledger).")
    parser.add_argument("--json", action="store_true", help="emit the dashboard JSON payload instead of text")
    parser.add_argument("--days", type=int, default=TREND_DAYS, help=f"trend window in days (default {TREND_DAYS})")
    parser.add_argument("--root", default=str(REPO_ROOT), help="repository root to scan (default: this repo)")
    args = parser.parse_args(argv)

    report = build_report(Path(args.root), days=max(1, args.days))
    sb_path = write_spend_balance(Path(args.root), report)
    if args.json:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
        print(f"spend_balance written: {sb_path}", file=sys.stderr)
    else:
        sys.stdout.write(render_text(report))
        print(f"spend_balance written: {sb_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
