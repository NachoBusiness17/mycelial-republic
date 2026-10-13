#!/usr/bin/env python3
"""rollup_delta.py - rollup metabolism meter (hydrology Z17, 2026-09-29).

The disease this meters is the one the gap sentinel proved (MICKEY17 wave 3:
the estate grew +25.41 GiB in 2.02 days = 12.59 GiB/day and NOTHING diffed the
snapshots): rollup.json lands every index run, the sentinel ALERTS on it, but
no instrument PUBLISHES the per-lane metabolism. This tool is it: diff the
current rollup against recorded snapshots, emit ROLLUP_DELTA.json beside
rollup.json for one dashboard fetch().

Bar stated in numbers BEFORE reading anything:

  GROWTH: flagged when bytes/day exceeds the bar (default 5.0 GiB/day, sized
  to the 12.59 GiB/day finding class). Windows shorter than MIN_WINDOW_DAYS
  (0.25d) are evidence only, never a flag (the census patrol's same-window
  law, B2-215, inherited from the gap sentinel).
  SHRINK: flagged when the byte delta is negative past the shrink floor
  (default 1.0 MiB rewrite-noise floor) - a deletion event. A lane absent
  from the current snapshot counts its full prior size as one deletion
  event; absent from the prior snapshot counts as appeared.

History, byte-truth sources in priority order:
  1. logs/rollup_delta/history.jsonl - this tool's own rich snapshots (bytes,
     files, HOT/WARM/COLD/FROZEN per lane, one row per rollup run ts, deduped).
  2. logs/gap_sentinel/history.jsonl - the sentinel's bytes-only rows: byte
     deltas byte-true, files/temps deltas null and named unmetered.
  3. --bootstrap-from INDEX_DATA_DIR - an older rollup.json+last_run.json pair
     (e.g. dashboard-deploy/static/index_data) for a first reading before any
     history accumulates; diff-only, named in window.source, never recorded.

Exit codes: 0 = deltas computed, no flags (baseline and evidence-only windows
included); 1 = GROWTH/SHRINK flags fired; 2 = cannot verify (missing or
unparsable inputs - fail-closed, never a guess). Usage:
python tools/rollup_delta.py [--root PATH] [--growth-gib N] [--shrink-mib N]
[--min-window-days N] [--bootstrap-from INDEX_DATA_DIR] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent

GIB = 1024 ** 3
MIB = 1024 ** 2
DEFAULT_GROWTH_GIB = 5.0
DEFAULT_SHRINK_MIB = 1.0
DEFAULT_MIN_WINDOW_DAYS = 0.25

INDEX_DATA_RELPATH = "dashboard/static/index_data"
ROLLUP_RELPATH = f"{INDEX_DATA_RELPATH}/rollup.json"
LASTRUN_RELPATH = f"{INDEX_DATA_RELPATH}/last_run.json"
OUT_RELPATH = f"{INDEX_DATA_RELPATH}/ROLLUP_DELTA.json"
OWN_HISTORY_RELPATH = "logs/rollup_delta/history.jsonl"
SENTINEL_HISTORY_RELPATH = "logs/gap_sentinel/history.jsonl"
RUNLOG_RELPATH = "logs/rollup_delta/run.log"

TEMP_KEYS = ("HOT", "WARM", "COLD", "FROZEN")


class DeltaError(Exception):
    """Cannot-verify condition; run() maps this to exit 2."""


def parse_iso(raw: str) -> datetime:
    """ISO-8601 to aware UTC datetime; DeltaError on garbage (fail-closed)."""
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise DeltaError(f"unparsable timestamp {raw!r}: {exc}") from exc
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def _lanes_from_rollup(rollup: dict) -> dict:
    """rollup.json mapping -> rich lanes; malformed rows skipped (the gap
    sentinel's loader leniency), a rollup that is not a dict fails closed."""
    if not isinstance(rollup, dict):
        raise DeltaError("rollup.json shape is not the snapshot contract")
    lanes: dict[str, dict] = {}
    for name, row in rollup.items():
        if not isinstance(row, dict) or not isinstance(row.get("bytes"), int):
            continue
        temps = row.get("temps") if isinstance(row.get("temps"), dict) else {}
        lane = {"bytes": row["bytes"],
                "files": row["files"] if isinstance(row.get("files"), int) else None}
        for key in TEMP_KEYS:
            lane[key.lower()] = temps[key] if isinstance(temps.get(key), int) else None
        lanes[name] = lane
    return lanes


def load_index_snapshot(idx_dir: Path) -> dict:
    """index_data dir (rollup.json + last_run.json) -> rich current snapshot."""
    rollup_p, lastrun_p = idx_dir / "rollup.json", idx_dir / "last_run.json"
    for p in (rollup_p, lastrun_p):
        if not p.is_file():
            raise DeltaError(f"missing input: {p}")
    try:
        rollup = json.loads(rollup_p.read_text(encoding="utf-8"))
        lastrun = json.loads(lastrun_p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DeltaError(f"unparsable input: {exc}") from exc
    if not isinstance(lastrun.get("ts"), str):
        raise DeltaError("last_run.json shape is not the snapshot contract")
    lanes = _lanes_from_rollup(rollup)
    total = lastrun.get("total_bytes") if isinstance(lastrun.get("total_bytes"), int) \
        else sum(l["bytes"] for l in lanes.values())
    return {"ts": parse_iso(lastrun["ts"]), "ts_raw": lastrun["ts"],
            "source": "rollup", "total_bytes": total, "lanes": lanes}


DIM_KEYS = ("files",) + tuple(k.lower() for k in TEMP_KEYS)


def _history_row(raw: dict, i: int, rich: bool) -> dict:
    """One history row -> snapshot; rich rows carry dims, sentinel rows bytes only."""
    key = "lanes" if rich else "projects"
    if not isinstance(raw.get("ts"), str) or not isinstance(raw.get(key), dict):
        raise DeltaError(f"history row {i} is not the snapshot contract")
    lanes: dict[str, dict] = {}
    for name, val in raw[key].items():
        if rich:
            if isinstance(val, dict) and isinstance(val.get("bytes"), int):
                lanes[name] = {"bytes": val["bytes"], **{d: val[d] if isinstance(
                    val.get(d), int) else None for d in DIM_KEYS}}
        elif isinstance(val, int):
            lanes[name] = {"bytes": val, **{d: None for d in DIM_KEYS}}
    return {"ts": parse_iso(raw["ts"]), "ts_raw": raw["ts"],
            "source": "history" if rich else "sentinel",
            "total_bytes": raw.get("total_bytes"), "lanes": lanes}


def load_own_history(path: Path) -> list[dict]:
    """logs/rollup_delta/history.jsonl rows oldest-first, ts parsed."""
    return _load_history_rows(path, lambda r, i: _history_row(r, i, True))


def load_sentinel_history(path: Path) -> list[dict]:
    """logs/gap_sentinel/history.jsonl rows normalized to bytes-only snapshots."""
    return _load_history_rows(path, lambda r, i: _history_row(r, i, False))


def _load_history_rows(path: Path, shape) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DeltaError(f"history row {i} unparsable: {exc}") from exc
        rows.append(shape(raw, i))
    rows.sort(key=lambda r: r["ts"])
    return rows


def compute_delta(prev: dict, cur: dict) -> dict:
    """Pure diff of two snapshots -> window days + per-lane daily deltas.

    Dimensions the prior snapshot does not carry (sentinel rows are bytes-only)
    come out None: unmetered, never fabricated. A lane present on only one
    side is appeared/gone with the full size as its delta.
    """
    days = (cur["ts"] - prev["ts"]).total_seconds() / 86400.0

    def per_day(delta):
        if delta is None:
            return None
        return delta / days if days > 0 else (float("inf") if delta > 0
                                              else float("-inf") if delta < 0 else 0.0)

    lanes: dict[str, dict] = {}
    for name in sorted(set(prev["lanes"]) | set(cur["lanes"])):
        p, c = prev["lanes"].get(name), cur["lanes"].get(name)
        row: dict = {"appeared": p is None, "gone": c is None}
        for dim in ("bytes", "files", "hot", "warm", "cold", "frozen"):
            pv = p.get(dim) if p else None
            cv = c.get(dim) if c else None
            if p is None or c is None:
                delta = cv if p is None else (-pv if pv is not None else None)
            elif pv is None or cv is None:
                delta = None
            else:
                delta = cv - pv
            row[f"{dim}_delta"] = delta
            row[f"{dim}_per_day"] = per_day(delta)
        lanes[name] = row
    return {"days": days, "lanes": lanes,
            "total_bytes_delta": (cur.get("total_bytes") or 0)
            - (prev.get("total_bytes") or 0)}


def lane_flags(delta: dict, growth_bytes: float, shrink_bytes: float) -> list[dict]:
    """GROWTH over the bar, SHRINK past the floor. Caller gates the window."""
    flags: list[dict] = []
    for name, row in delta["lanes"].items():
        bd, bpd = row["bytes_delta"], row["bytes_per_day"]
        if bd is None or bpd is None:
            continue
        if bpd > growth_bytes:
            flags.append({"lane": name, "flag": "GROWTH",
                          "bytes_delta": bd, "bytes_per_day": bpd,
                          "evidence": "appeared (absent from prior snapshot)"
                          if row["appeared"] else "grown"})
        elif bd < 0 and abs(bd) >= shrink_bytes:
            flags.append({"lane": name, "flag": "SHRINK",
                          "bytes_delta": bd, "bytes_per_day": bpd,
                          "evidence": "gone (absent from current snapshot)"
                          if row["gone"] else "deletion event"})
    flags.sort(key=lambda f: -f["bytes_delta"])
    return flags


def gib(n) -> str | None:
    return None if n is None else f"{n / GIB:.2f} GiB"


def build_report(cur: dict, prev: dict | None, delta: dict | None, flags: list[dict],
                 evidence_only: bool, bars: dict, now: datetime) -> dict:
    """The ROLLUP_DELTA.json document the dashboard renders (one fetch, no math)."""
    if prev is None:
        status = "baseline"
        window = None
    else:
        window = {"prev_ts": prev["ts_raw"], "cur_ts": cur["ts_raw"],
                  "days": round(delta["days"], 4), "source": prev["source"],
                  "evidence_only": evidence_only}
        status = "evidence_only" if evidence_only else ("flags" if flags else "ok")
    lanes_out = []
    prev_names = set(prev["lanes"]) if prev else set()
    for name in sorted(set(cur["lanes"]) | prev_names):
        c = cur["lanes"].get(name)
        d = delta["lanes"].get(name, {}) if delta else {}
        lane: dict = {"lane": name}
        if c:
            lane.update(bytes=c["bytes"], bytes_gib=gib(c["bytes"]),
                        files=c["files"], hot=c["hot"])
        else:
            lane.update(bytes=None, bytes_gib=None, files=None, hot=None)
        for dim in ("bytes", "files", "hot"):
            lane[f"{dim}_delta"] = d.get(f"{dim}_delta")
            lane[f"{dim}_per_day"] = d.get(f"{dim}_per_day")
        lane["bytes_delta_gib"] = gib(lane["bytes_delta"])
        lane["bytes_per_day_gib"] = gib(lane["bytes_per_day"])
        lane.update(appeared=d.get("appeared"), gone=d.get("gone"),
                    flags=[f["flag"] for f in flags if f["lane"] == name])
        lanes_out.append(lane)
    lanes_out.sort(key=lambda l: (-(l["bytes_delta"] if l["bytes_delta"] is not None
                                    else float("-inf")), l["lane"]))
    growing = [l for l in lanes_out if (l["bytes_delta"] or 0) > 0]
    shrinking = [l for l in lanes_out if (l["bytes_delta"] or 0) < 0]
    unmetered = bool(prev and any(
        l["files_delta"] is None for l in lanes_out if not l["appeared"] and not l["gone"]))
    return {
        "tool": "tools/rollup_delta.py",
        "generated": now.isoformat(),
        "status": status,
        "bars": bars,
        "window": window,
        "totals": {
            "total_bytes": cur["total_bytes"],
            "total_bytes_gib": gib(cur["total_bytes"]),
            "total_bytes_delta": delta["total_bytes_delta"] if delta else None,
            "total_bytes_delta_gib": gib(delta["total_bytes_delta"]) if delta else None,
        },
        "unmetered_note": ("files/temps deltas are null this window: the prior snapshot "
                           "is bytes-only (gap sentinel history row)") if unmetered else None,
        "flags": flags,
        "top_growing": [l["lane"] for l in growing[:3]],
        "top_shrinking": [l["lane"] for l in reversed(shrinking[-3:])],
        "lanes": lanes_out,
    }


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def record_snapshot(history: list[dict], snap: dict, path: Path) -> bool:
    """Append the rich snapshot when its rollup-run ts is unseen (dedupe on ts)."""
    if any(r["ts"] == snap["ts"] for r in history):
        return False
    append_jsonl(path, {"ts": snap["ts_raw"], "source": "rollup",
                        "total_bytes": snap["total_bytes"], "lanes": snap["lanes"]})
    return True


def run(root: Path, growth_bytes: float = DEFAULT_GROWTH_GIB * GIB,
        shrink_bytes: float = DEFAULT_SHRINK_MIB * MIB,
        min_window_days: float = DEFAULT_MIN_WINDOW_DAYS,
        bootstrap: Path | None = None, dry_run: bool = False,
        now: datetime | None = None) -> int:
    """One metabolism pass. Returns the process exit code (0/1/2)."""
    now = now or datetime.now(timezone.utc)
    try:
        cur = load_index_snapshot(root / INDEX_DATA_RELPATH)
        own = load_own_history(root / OWN_HISTORY_RELPATH)
        sentinel = load_sentinel_history(root / SENTINEL_HISTORY_RELPATH)
        boot = load_index_snapshot(bootstrap) if bootstrap else None
    except DeltaError as exc:
        print(f"ROLLUP-DELTA: cannot verify, {exc}")
        return 2

    history = sorted(own + sentinel, key=lambda r: r["ts"])
    prev = next((r for r in reversed(history) if r["ts"] != cur["ts"]), None)
    if prev is None and boot is not None and boot["ts"] != cur["ts"]:
        prev = {**boot, "source": "bootstrap"}  # diff-only, never recorded

    evidence_only = False
    flags: list[dict] = []
    delta = None
    if prev is None:
        print(f"ROLLUP-DELTA: baseline - no prior snapshot to diff, run {cur['ts_raw']} "
              "recorded (diffs start on the next index run)")
    else:
        delta = compute_delta(prev, cur)
        evidence_only = delta["days"] < min_window_days
        if not evidence_only:
            flags = lane_flags(delta, growth_bytes, shrink_bytes)
        head = (f"window {prev['ts_raw']} -> {cur['ts_raw']} ({delta['days']:.2f}d via "
                f"{prev['source']}), total {gib(delta['total_bytes_delta'])}")
        if evidence_only:
            print(f"ROLLUP-DELTA: evidence only - window under {min_window_days}d, "
                  f"no flags: {head}")
        elif flags:
            named = ", ".join(f"{f['flag']} {f['lane']} {gib(f['bytes_delta'])} "
                              f"({gib(f['bytes_per_day'])}/day, {f['evidence']})"
                              for f in flags[:8])
            print(f"ROLLUP-DELTA: FLAGS - {len(flags)} lane(s) in {head}: {named}")
        else:
            print(f"ROLLUP-DELTA: ok - no lane over {gib(growth_bytes)}/day growth bar "
                  f"or {shrink_bytes / MIB:.1f} MiB shrink floor in {head}")

    bars = {"growth_gib_per_day": growth_bytes / GIB,
            "shrink_mib": shrink_bytes / MIB, "min_window_days": min_window_days}
    report = build_report(cur, prev, delta, flags, evidence_only, bars, now)

    growing = [l for l in report["lanes"] if (l["bytes_delta"] or 0) > 0]
    shrinking = [l for l in report["lanes"] if (l["bytes_delta"] or 0) < 0]
    triples = (("grow", growing[:3]), ("shrink", list(reversed(shrinking[-3:]))))
    for label, lanes3 in triples:
        for lane in lanes3:
            print(f"  {label}: {lane['lane']} {lane['bytes_delta_gib']} "
                  f"({lane['bytes_per_day_gib']}/day, files {lane['files_delta']}, "
                  f"hot {lane['hot_delta']})")

    if dry_run:
        print("  dry-run: would write "
              f"{(root / OUT_RELPATH).relative_to(root).as_posix()} + history row")
        return 1 if flags else 0
    out_p = root / OUT_RELPATH
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(report, indent=1), encoding="utf-8")
    recorded = record_snapshot(own, cur, root / OWN_HISTORY_RELPATH)
    append_jsonl(root / RUNLOG_RELPATH,
                 {"ts": now.isoformat(), "exit": 1 if flags else 0,
                  "flags": [f"{f['flag']} {f['lane']}" for f in flags],
                  "window_days": round(delta["days"], 4) if delta else None,
                  "prev_source": prev["source"] if prev else None,
                  "recorded_snapshot": recorded})
    print(f"ROLLUP-DELTA: wrote {OUT_RELPATH} (status {report['status']}, "
          f"{len(report['lanes'])} lanes)")
    return 1 if flags else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="rollup metabolism meter (hydrology Z17)")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root holding dashboard/static and logs/")
    parser.add_argument("--growth-gib", type=float, default=DEFAULT_GROWTH_GIB,
                        help="growth bar in GiB/day")
    parser.add_argument("--shrink-mib", type=float, default=DEFAULT_SHRINK_MIB,
                        help="shrink floor in MiB of absolute byte loss")
    parser.add_argument("--min-window-days", type=float, default=DEFAULT_MIN_WINDOW_DAYS,
                        help="shorter windows are evidence only")
    parser.add_argument("--bootstrap-from", type=Path, default=None, metavar="INDEX_DATA_DIR",
                        help="older rollup.json+last_run.json dir for a first reading; "
                             "diff-only, never recorded")
    parser.add_argument("--dry-run", action="store_true",
                        help="compute and print only; no history row, no ROLLUP_DELTA.json")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), growth_bytes=args.growth_gib * GIB,
               shrink_bytes=args.shrink_mib * MIB,
               min_window_days=args.min_window_days,
               bootstrap=args.bootstrap_from.resolve() if args.bootstrap_from else None,
               dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
