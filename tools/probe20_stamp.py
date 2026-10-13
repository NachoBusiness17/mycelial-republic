"""probe20_stamp -- the probe20-to-dashboard stamp bridge (B2-64 board).

Spec: watch/inbox/BURN_steering-theory_20260926_c.md (filed before this
code): the single missing link between
memory/runs/probe20/<lane>_<pair>_series.jsonl (tools/probe20_run.py output)
and memory/runs/adv_arc_50/teleo_drift_stamps.jsonl (the
teleo_drift_stamp.v2 ledger tools/drift_dashboard.py renders).

One writer, two stamps (pair A, pair B), two REFERENTS rows. The verdict is
NOT recomputed here from raw fields: this bridge imports probe20_run and
calls its evaluate(), so every stamp carries the runner's own enforced
verdict (native VACUOUS kill + BURN _c noise-floor override) with
byte-identical semantics to the series organ.

DEFAULT IS DRY: prints the stamps it would append, writes nothing. --apply
is the operator-gated append to the live ledger (model text proposes; only
the switchboard/effect broker authorizes effects; the ledger is a live
dashboard surface per BURN _d). --apply refuses when a pair's series file is
absent: a bridge either bridges real data or files nothing, never a
synthesized stamp.

Idempotent by (week_key, pair_id) exactly like tools/drift_pairs_stamp.py.
The two REFERENTS rows land in the same ledger under schema
drift_referent.v1: drift_dashboard.load_stamps skips unknown schemas, so
they are inert until the board is wired to read them (ref_age renders n/a
until then, exactly as BURN _c line 19 predicted). No dashboard change is
required to render the stamps themselves: build_table derives pair ids from
ledger stamps (pre-registered falsifier check, BURN _c).

Usage:
  .venv\\Scripts\\python.exe tools\\probe20_stamp.py --dry   # print stamps, write nothing
  .venv\\Scripts\\python.exe tools\\probe20_stamp.py --demo  # synthetic in-memory series, same stamp path
  .venv\\Scripts\\python.exe tools\\probe20_stamp.py --apply # operator-gated append (idempotent)
"""

import argparse
import glob
import json
import os
import sys
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import probe20_run  # noqa: E402  (series format owner: evaluate/derive/PAIRS)

LEDGER = os.path.join(REPO, "memory", "runs", "adv_arc_50", "teleo_drift_stamps.jsonl")
SERIES_DIR = probe20_run.SERIES_DIR
GENERATOR = "tools/probe20_stamp.py"
LAW = ("a rate metric answers 'is it moving'; only corr(delta-M, delta-R) "
       "answers 'is it moving north'")

PAIR_IDS = {"A": "P20A", "B": "P20B"}
PAIR_NAMES = {
    "A": "probe20_conf_margin_vs_correctness",
    "B": "probe20_escalate_rate_vs_overturn_rate",
}
PAIR_TELEO = {
    "A": ("steering drift: does probe confidence movement (verdict-token "
          "logprob margin) track correctness movement?"),
    "B": ("steering drift: does escalation-rate movement track "
          "overturn-rate movement on the same escalations?"),
}
DERIVED = {
    "A": {"metric": "margin (verdict-token logprob margin)",
          "referent": "correct/20"},
    "B": {"metric": "escalated/total",
          "referent": "overturns/escalated"},
}


def _parse_ts(v):
    if not v or not isinstance(v, str):
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return None


def _utc_date(v):
    dt = _parse_ts(v)
    return dt.astimezone(timezone.utc).date() if dt else None


def _week_key(rows, today: date) -> str:
    """ISO week of the newest series row ts (data-derived first, the
    drift_pairs_stamp deterministic law); run date only as fallback."""
    for r in reversed(rows):
        d = _utc_date(r.get("ts"))
        if d:
            y, w, _ = d.isocalendar()
            return "%04d-W%02d" % (y, w)
    y, w, _ = today.isocalendar()
    return "%04d-W%02d" % (y, w)


def series_files(pair: str, lane=None):
    hits = sorted(glob.glob(os.path.join(SERIES_DIR, "*_%s_series.jsonl" % pair)))
    if lane:
        want = "%s_%s_series.jsonl" % (lane, pair)
        hits = [h for h in hits if os.path.basename(h) == want]
    return hits


def _lane_of(path: str, pair: str) -> str:
    return os.path.basename(path)[: -len("_%s_series.jsonl" % pair)]


def load_series(path: str):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    rows.sort(key=lambda r: int(r.get("cycle", 0)))
    return rows


def _newest(files):
    """Pick the lane whose series has the newest last-row ts, mtime as tiebreak."""
    def key(p):
        rows = []
        try:
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
        except (OSError, json.JSONDecodeError):
            return (datetime.min.replace(tzinfo=timezone.utc), 0.0)
        last_ts = max((dt for dt in (_parse_ts(r.get("ts")) for r in rows)
                       if dt is not None),
                      default=datetime.min.replace(tzinfo=timezone.utc))
        return (last_ts, os.path.getmtime(p))
    return max(files, key=key)


def build_stamp(pair, lane, series_rel, rows, window, stamped_at, today):
    """One teleo_drift_stamp.v2 row from one series, verdict via probe20_run.evaluate."""
    out = probe20_run.evaluate(pair, rows, window=window)
    verdict = dict(out["enforced"])
    # the dashboard reads verdict.deltas_used (drift.py's key); probe20_run's
    # inline fallback names it "deltas", so normalize without dropping either
    if "deltas_used" not in verdict and "deltas" in verdict:
        verdict["deltas_used"] = verdict["deltas"]
    verdict.setdefault("ok", True)
    verdict.setdefault("label", probe20_run.PAIRS[pair]["label"])
    verdict.setdefault("law", LAW)

    derived = [probe20_run.derive(pair, r) for r in rows]
    ts_dates = [d for d in (_utc_date(r.get("ts")) for r in rows) if d]
    return {
        "schema": "teleo_drift_stamp.v2",
        "week_key": _week_key(rows, today),
        "pair_id": PAIR_IDS[pair],
        "pair": PAIR_NAMES[pair],
        "teleo": PAIR_TELEO[pair],
        "stamped_at": stamped_at,
        "generator": GENERATOR,
        "verdict": verdict,
        "window": {
            "start": min(ts_dates).isoformat() if ts_dates else None,
            "end": max(ts_dates).isoformat() if ts_dates else None,
            "buckets": len(rows),
            "metric_total": round(sum(m for m, _ in derived), 4),
            "referent_total": round(sum(r for _, r in derived), 4),
            "unit": "probe20 cycles (not calendar days)",
        },
        "sources": {
            "metric": {"path": series_rel, "rows": len(rows),
                       "derived": DERIVED[pair]["metric"]},
            "referent": {"path": series_rel, "rows": len(rows),
                         "derived": DERIVED[pair]["referent"]},
            "runner": "tools/probe20_run.py evaluate()",
            "lane": lane,
            "probe_version_hash": rows[-1].get("probe_version_hash"),
            "raw_verdict": out["raw"].get("verdict"),
            "runner_override": out["enforced"].get("runner_override"),
            "net_referent_delta": out["net_referent_delta"],
            "note": ("verdict is the runner's enforced verdict (native VACUOUS "
                     "kill + BURN _c noise-floor override), not recomputed here"),
        },
        "law": LAW,
    }


def referents_row(pair, lane, series_rel, stamped_at):
    return {
        "schema": "drift_referent.v1",
        "pair_id": PAIR_IDS[pair],
        "paths": [series_rel],
        "key": "ts",
        "lane": lane,
        "note": ("live referent-age source for the B2-64 board; inert until "
                 "drift_dashboard.REFERENTS is wired to read drift_referent.v1 "
                 "rows (ref_age renders n/a until then, BURN _c line 19)"),
        "generator": GENERATOR,
        "stamped_at": stamped_at,
    }


def _stamped_keys(ledger_rows):
    """(week_key, pair_id) already stamped, drift_pairs_stamp._stamped_keys rule."""
    out = set()
    for r in ledger_rows:
        if r.get("schema") == "teleo_drift_stamp.v2" and r.get("verdict", {}).get("ok"):
            out.add((r.get("week_key", ""), r.get("pair_id", "")))
    return out


def _referent_keys(ledger_rows):
    return {r.get("pair_id") for r in ledger_rows
            if r.get("schema") == "drift_referent.v1"}


def _read_ledger():
    if not os.path.exists(LEDGER):
        return []
    rows = []
    with open(LEDGER, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def run_demo():
    """Synthetic in-memory series through the same stamp path, mirrors
    probe20_run --demo: dry by construction, clearly labeled, files nothing."""
    now = datetime.now(timezone.utc)
    stamped_at = now.isoformat().replace("+00:00", "Z")
    today = now.date()
    a = [{"cycle": i, "ts": "2026-09-26T00:%02d:00Z" % i, "lane": "demo",
          "probe_version_hash": "demo-hash", "margin": m, "correct": c}
         for i, (m, c) in enumerate(zip([1.0, 1.5, 1.8, 2.3, 2.6, 2.9],
                                        [10, 12, 13, 15, 16, 17]))]
    b = [{"cycle": i, "ts": "2026-09-26T01:%02d:00Z" % i, "lane": "demo",
          "probe_version_hash": "demo-hash",
          "escalated": e, "total": 20, "overturns": o}
         for i, (e, o) in enumerate(zip([5, 6, 8, 9, 11, 12],
                                        [1, 2, 2, 3, 4, 5]))]
    print("probe20_stamp --demo (synthetic in-memory series, dry, writes nothing, "
          "drift import from tools/drift.py: %s)" % probe20_run.HAVE_DRIFT)
    for pair, rows in (("A", a), ("B", b)):
        row = build_stamp(pair, "demo", "memory/runs/probe20/demo_%s_series.jsonl (in memory)"
                          % pair, rows, 0, stamped_at, today)
        print(json.dumps(row, sort_keys=True))
        print(json.dumps(referents_row(pair, "demo",
                                       "memory/runs/probe20/demo_%s_series.jsonl" % pair,
                                       stamped_at), sort_keys=True))


def main(argv=None):
    ap = argparse.ArgumentParser(description="probe20 series -> teleo_drift_stamp.v2 bridge")
    ap.add_argument("--dry", action="store_true", default=True,
                    help="print stamps, write nothing (the default; explicit flag for receipts)")
    ap.add_argument("--apply", action="store_true",
                    help="operator-gated append to the live ledger (idempotent by week+pair)")
    ap.add_argument("--window", type=int, default=0,
                    help="delta-window tail passed to the runner's evaluate()")
    ap.add_argument("--lane", default=None,
                    help="restrict to one lane's series (default: newest lane per pair)")
    ap.add_argument("--demo", action="store_true",
                    help="synthetic in-memory series, dry by construction")
    args = ap.parse_args(argv)

    if args.demo:
        run_demo()
        return 0

    today = datetime.now(timezone.utc).date()
    stamped_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    found, missing = {}, []
    for pair in ("A", "B"):
        files = series_files(pair, args.lane)
        if not files:
            missing.append(pair)
            continue
        path = _newest(files)
        rows = load_series(path)
        if not rows:
            missing.append(pair)
            continue
        alternates = sorted(_lane_of(p, pair) for p in files if p != path)
        found[pair] = (path, rows, alternates)

    stamps, refs = [], []
    for pair in ("A", "B"):
        pid = PAIR_IDS[pair]
        if pair not in found:
            print("SKIP %s: no series on disk (nothing to bridge; refusing to "
                  "synthesize)" % pid)
            continue
        path, rows, alternates = found[pair]
        lane = _lane_of(path, pair)
        series_rel = os.path.relpath(path, REPO).replace(os.sep, "/")
        row = build_stamp(pair, lane, series_rel, rows, args.window, stamped_at, today)
        row["appended"] = False
        if alternates:
            row["sources"]["alternate_lanes_not_stamped"] = alternates
        stamps.append((pair, lane, series_rel, row))
        refs.append((pair, lane, referents_row(pair, lane, series_rel, stamped_at)))

    ledger = _read_ledger()
    done = _stamped_keys(ledger)
    ref_done = _referent_keys(ledger)

    new_stamps = [s for (_, _, _, s) in stamps
                  if (s["week_key"], s["pair_id"]) not in done]
    new_refs = [r for (_, _, r) in refs if r["pair_id"] not in ref_done]

    for (pair, lane, series_rel, row) in stamps:
        already = (row["week_key"], row["pair_id"]) in done
        row["appended"] = bool(args.apply) and not already
        print("%s stamp (%s %s, series %s):"
              % ("WOULD APPEND" if (not args.apply and not already)
                 else ("SKIP, already stamped this week" if already else "APPENDING"),
                 lane, series_rel, row["pair_id"]))
        print(json.dumps(row, sort_keys=True))
    for (pair, lane, r) in refs:
        already = r["pair_id"] in ref_done
        print("%s referents row %s:" % ("SKIP, already registered" if already
                                        else ("WOULD APPEND" if not args.apply
                                              else "APPENDING"), r["pair_id"]))
        print(json.dumps(r, sort_keys=True))

    if args.apply:
        if not stamps:
            print("APPLY REFUSED: no series on disk; nothing appended "
                  "(a bridge either bridges real data or files nothing)")
            return 1
        with open(LEDGER, "a", encoding="utf-8") as f:
            for row in new_stamps:
                f.write(json.dumps(row, ensure_ascii=True) + "\n")
            for r in new_refs:
                f.write(json.dumps(r, ensure_ascii=True) + "\n")
        print("applied: %d stamp(s) + %d referents row(s) appended to %s"
              % (len(new_stamps), len(new_refs), os.path.relpath(LEDGER, REPO)))
    else:
        print("dry: %d stamp(s) + %d referents row(s) printed, nothing written "
              "(--apply is the operator-gated append; %d pair(s) missing series)"
              % (len(new_stamps), len(new_refs), len(missing)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
