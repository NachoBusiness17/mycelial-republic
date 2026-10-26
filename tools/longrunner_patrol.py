#!/usr/bin/env python3
"""longrunner_patrol: enforce the longrunners-caged law (configs/longrunner_policy.json).

Law: any process expected to outlive one sitting runs inside a compose service
with resource caps (configs/longrunner_policy.json tiers A). Bare-host
interpreter processes older than the policy's max age whose command lines are
not allowlisted are violations (tier C): the patrol alerts memory/attention.md
and exits 1 so a scheduled task or pre-push-style hook can fail loudly.

Founding incident: run_armC.py (interference_replication_20260925) burned
24.4 CPU-hours over 11 days at ~1 live core before a human noticed; a capped
container with a timeout makes that class structurally impossible.

The patrol only READS process tables and APPENDS one alert file. It never
kills: killing is an operator or seat judgment (a live seat's work must never
die to a patrol; see the sibling-stash class).

ML advisory head (--ml, ml-moonshot-20261007):
  Behind the flag the patrol also classifies hung / storm / dead sequences in
  an event ledger series (JSONL rows with a ts field). Classes and their
  labeled positives (memory/attention.md rows, 2026-10-07):
    storm - sklearn over windowed features: GradientBoostingClassifier
            supervised on the labeled storm day (default 2026-09-24: the
            FullScan 429 burst, 18,489 failing events in one day vs a
            50-431/day baseline in state/fuel/full_scan_ledger.jsonl) or
            IsolationForest one-class (no labels needed).
    hung  - per-key sequence silence: an internal gap or a tail age reaching
            ml-hung-mult x the key's median cadence (labeled positive: the
            5h hung cycle, fleet --cycle twins age 295min vs a 10min design
            cadence, attention.md 2026-10-07T00:38Z).
    dead  - per-key span past the design horizon (labeled positive: the
            11-day runaway, run_armC.py alive 11 days vs an hour-scale arm,
            attention.md 2026-10-07T00:30Z).
  Advisory law: ML rows go to stdout and the --ml-out JSONL file. They NEVER
  append to memory/attention.md and NEVER change the exit code. The patrol
  stays rule-based by default: without --ml nothing here runs and sklearn is
  never imported.

Usage:
  python -m tools.longrunner_patrol                        # rule scan, alert, exit 1 on findings
  python -m tools.longrunner_patrol --dry                  # print, no alert append
  python -m tools.longrunner_patrol --ml                   # rule scan + ML advisory rows
  python -m tools.longrunner_patrol --ml-only --ml-model iforest
                                                           # ledger audit only, always exit 0
Exit: 0 clean / 1 violations found / 2 usage. (--ml-only always exits 0:
advisory surfaces must never fail a scheduled task.)
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "configs" / "longrunner_policy.json"
ALERT = ROOT / "memory" / "attention.md"

ML_DEFAULT_LEDGER = ROOT / "state" / "fuel" / "full_scan_ledger.jsonl"
ML_DEFAULT_OUT = ROOT / "logs" / "longrunner_ml_advisory.jsonl"
ML_RUN = "ml-moonshot-20261007"
# Features per time window, fixed order for the sklearn models.
ML_FEATURES = ["n_events", "ev_per_min", "fail_frac", "marker_frac",
               "median_gap_min", "max_gap_min", "key_count"]
# An internal silence must also clear this absolute floor before it counts as
# hung, so a 3-tick key with a noisy cadence cannot fire on a 25x of nothing.
ML_HUNG_ABS_FLOOR_MIN = 30.0


def _age_minutes(created_wmi: str, now: datetime) -> float:
    # WMI CreationDate: YYYYMMDDHHMMSS.ffffff+PPP (UTC when +000)
    raw = created_wmi.split(".")[0]
    try:
        # fixit 2026-10-24: honor the WMI +/-UUU minute offset (local time, e.g. -240 = ET)
        off = 0
        tail = created_wmi.split(".", 1)[1] if "." in created_wmi else ""
        if len(tail) >= 4 and tail[-4] in "+-":
            off = int(tail[-4:])
        created = datetime.strptime(raw, "%Y%m%d%H%M%S").replace(tzinfo=timezone(timedelta(minutes=off)))
    except ValueError:
        return -1.0
    return (now - created).total_seconds() / 60.0


def disk_floor_rows(policy: dict) -> list[dict]:
    """Disk-free floor (disk-crisis-20261008). A watch-path volume under the
    floor is a violation the same class as a bare longrunner: the founding
    incident had C: at 6.1GB free / 100 percent with ledgers live and the
    patrol blind to it (receipt watch/inbox/DISK_INVENTORY_20261008.md).
    Reads policy['disk_free_floor_gb']; absent key = check off (old policy
    files still work)."""
    cfg = policy.get("disk_free_floor_gb")
    if not cfg:
        return []
    import shutil
    floor = float(cfg["floor_gb"])
    rows = []
    for path in cfg.get("watch_paths", ["."]):
        target = ROOT / path if path != "." else ROOT
        usage = shutil.disk_usage(target)
        free_gb = usage.free / 2**30
        if free_gb < floor:
            rows.append({
                "path": str(path),
                "free_gb": round(free_gb, 1),
                "floor_gb": floor,
                "total_gb": round(usage.total / 2**30, 1),
            })
    return rows


def _rule_scan(args) -> int:
    """The founding behavior, unchanged: WMI process table vs the policy."""
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    max_age = float(policy["bare_longrunner_max_age_min"])
    watch = {n.lower() for n in policy["watch_process_names"]}
    allow = [re.compile(p, re.I) for p in policy["allowlist_cmdline_regex"]]
    now = datetime.now(timezone.utc)

    import win32com.client  # repo venv carries pywin32 (scheduled tasks use it)
    wmi = win32com.client.GetObject("winmgmts:{impersonationLevel=impersonate}!//./root/cimv2")
    violations = []
    for proc in wmi.InstancesOf("Win32_Process"):
        name = str(proc.Name or "").lower()
        if name not in watch:
            continue
        cmdline = str(proc.CommandLine or "")
        if any(rx.search(cmdline) for rx in allow):
            continue
        age = _age_minutes(str(proc.CreationDate or ""), now)
        if age < 0 or age <= max_age:
            continue
        violations.append({
            "pid": int(proc.ProcessId),
            "name": name,
            "age_min": round(age),
            "cmdline": cmdline[:200],
        })

    disk_rows = disk_floor_rows(policy)

    if not violations and not disk_rows:
        floor_note = ""
        if policy.get("disk_free_floor_gb"):
            floor_note = (f"; disk free above "
                          f"{float(policy['disk_free_floor_gb']['floor_gb']):.0f}GB floor")
        print("LONGRUNNER PATROL: clean (no bare-host interpreter older than "
              f"{max_age:.0f} min outside the allowlist{floor_note})")
        return 0
    stamp = now.isoformat().replace("+00:00", "Z")
    lines = [f"- {stamp} LONGRUNNER VIOLATIONS ({len(violations)} process, "
             f"{len(disk_rows)} disk): the longrunners-caged law found "
             "bare-host interpreters past the "
             f"{max_age:.0f} min age fence - kill or cage, refire through the "
             "burners container per configs/longrunner_policy.json; disk rows "
             "follow the reversible relief playbook in the policy, never "
             "delete live ledgers"]
    for v in violations:
        lines.append(f"    - PID {v['pid']} {v['name']} age {v['age_min']}min: "
                     f"{v['cmdline']}")
    for d in disk_rows:
        lines.append(f"    - DISK FLOOR {d['path']}: {d['free_gb']}GB free of "
                     f"{d['total_gb']}GB, floor {d['floor_gb']:.0f}GB - "
                     "relief playbook: docker builder prune, ollama rotation "
                     "with modelfile receipts, cold-artifact offload "
                     "(watch/inbox/DISK_INVENTORY_20261008.md)")
    body = "\n".join(lines) + "\n"
    print(body)
    if not args.dry:
        ALERT.parent.mkdir(parents=True, exist_ok=True)
        with open(ALERT, "a", encoding="utf-8") as fh:
            fh.write(body)
    return 1


# --------------------------------------------------------------------------
# ML advisory head (ml-moonshot-20261007). Everything below only runs with
# --ml / --ml-only, only reads, and never touches ALERT or the exit code.
# --------------------------------------------------------------------------

def _parse_ts(value) -> datetime | None:
    if value is None:
        return None
    s = str(value).strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        ts = datetime.fromisoformat(s)
    except ValueError:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


def _load_series(path: Path):
    """Read a JSONL event ledger: rows need one of ts/timestamp/time/when."""
    events, bad = [], 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except ValueError:
                bad += 1
                continue
            if not isinstance(raw, dict):
                bad += 1
                continue
            ts = None
            for k in ("ts", "timestamp", "time", "when"):
                if k in raw:
                    ts = _parse_ts(raw[k])
                    if ts is not None:
                        break
            if ts is None:
                bad += 1
                continue
            key = str(raw.get("lane") or raw.get("name") or raw.get("key") or "series")
            text = " ".join(str(raw[f]) for f in ("brief", "why", "note", "msg", "error")
                            if raw.get(f))
            ok = raw["ok"] if isinstance(raw.get("ok"), bool) else None
            events.append({"ts": ts, "key": key, "ok": ok, "text": text})
    return events, bad


def _iter_windows(events, window_min: float):
    """Regular grid of [t0, t0+window) buckets covering the series span."""
    t0 = min(e["ts"] for e in events)
    t1 = max(e["ts"] for e in events)
    step = timedelta(minutes=window_min)
    cur = t0.replace(second=0, microsecond=0)
    while cur <= t1:
        yield cur, cur + step
        cur += step


def _window_features(win_events, t0: datetime, t1: datetime, marker: str) -> dict:
    n = len(win_events)
    span = (t1 - t0).total_seconds() / 60.0
    fails = sum(1 for e in win_events if e["ok"] is False)
    marked = sum(1 for e in win_events if marker and marker in e["text"])
    tss = sorted(e["ts"] for e in win_events)
    gaps = [(b - a).total_seconds() / 60.0 for a, b in zip(tss, tss[1:])]
    return {
        "n_events": n,
        "ev_per_min": round(n / span, 4) if span > 0 else 0.0,
        "fail_frac": round(fails / n, 4) if n else 0.0,
        "marker_frac": round(marked / n, 4) if n else 0.0,
        "median_gap_min": round(statistics.median(gaps), 4) if gaps else 0.0,
        "max_gap_min": round(max(gaps), 4) if gaps else 0.0,
        "key_count": len({e["key"] for e in win_events}),
    }


def _advisory_row(now: datetime, model: str, **fields) -> dict:
    row = {"kind": "ml_advisory", "run": ML_RUN, "run_ts": now.isoformat().replace("+00:00", "Z"),
           "model": model}
    row.update(fields)
    return row


def _storm_rows(model: str, wins, feats, labels, now: datetime, ledger: str):
    """sklearn storm classifier over windowed features.

    gbm: GradientBoostingClassifier supervised on the labeled storm day
    (event-bearing windows only; a window is a positive when it carries
    events AND its date is the labeled storm day). iforest: IsolationForest
    one-class, no labels; outliers with the storm signature (rate at or above
    the series' nonzero median and marker-heavy) are classified storm, other
    outliers are only counted, never classified.
    Returns (rows, metrics_note).
    """
    rows, note = [], "model skipped: no event-bearing windows"
    idx = [i for i, f in enumerate(feats) if f["n_events"] > 0]
    if not idx:
        return rows, note
    try:
        import numpy as np
        from sklearn.ensemble import GradientBoostingClassifier, IsolationForest
        from sklearn.model_selection import StratifiedKFold, cross_val_score
    except ImportError:
        return rows, "sklearn unavailable: ML head skipped (rule-based patrol unaffected)"
    X = np.array([[feats[i][f] for f in ML_FEATURES] for i in idx], dtype=float)
    if model == "iforest":
        iso = IsolationForest(random_state=7)
        pred = iso.fit_predict(X)
        med_rate = float(np.median([feats[i]["ev_per_min"] for i in idx]))
        n_storm = n_other = 0
        for j, i in enumerate(idx):
            if pred[j] != -1:
                continue
            if feats[i]["ev_per_min"] >= med_rate and feats[i]["marker_frac"] >= 0.5:
                n_storm += 1
                rows.append(_advisory_row(now, model, surface="window", klass="storm",
                                          t0=wins[i][0].isoformat(), t1=wins[i][1].isoformat(),
                                          score=-1.0, features=feats[i], ledger=ledger))
            else:
                n_other += 1
        return rows, (f"iforest outliers: {n_storm} storm + {n_other} "
                      "below storm signature (counted, not classified)")
    y = np.array([labels[i] for i in idx], dtype=int)
    if len(set(y.tolist())) < 2:
        return rows, ("gbm skipped: one label class present "
                      "(pass --ml-storm-day with the labeled storm date)")
    clf = GradientBoostingClassifier(random_state=7)
    note_parts = []
    if min(int((y == c).sum()) for c in set(y.tolist())) >= 5:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)
        cv = cross_val_score(GradientBoostingClassifier(random_state=7), X, y,
                             cv=skf, scoring="accuracy")
        note_parts.append(f"cv_acc={cv.mean():.3f}")
    clf.fit(X, y)
    p = clf.predict_proba(X)[:, 1]
    storm_idx = [k for k in range(len(y)) if y[k] == 1]
    recall = float(sum(1 for k in storm_idx if p[k] >= 0.5) / len(storm_idx))
    fp = int(sum(1 for k in range(len(y)) if y[k] == 0 and p[k] >= 0.5))
    note_parts.append(f"storm_recall={recall:.3f} nominal_flagged={fp}")
    for k, i in enumerate(idx):
        if p[k] < 0.5:
            continue
        rows.append(_advisory_row(now, model, surface="window", klass="storm",
                                  t0=wins[i][0].isoformat(), t1=wins[i][1].isoformat(),
                                  score=round(float(p[k]), 4), features=feats[i],
                                  ledger=ledger))
    return rows, "gbm " + ", ".join(note_parts)


def _key_rows(model: str, events, now: datetime, hung_mult: float,
              dead_horizon_min: float, min_key_events: int, ledger: str):
    """Keyed hung/dead sequence classifiers (cadence multiples, advisory).

    hung: an internal gap or a tail age reaching hung_mult x the key's median
    cadence (and the absolute floor). dead: the key's span past the design
    horizon while still emitting events.
    """
    rows = []
    by_key = defaultdict(list)
    for e in events:
        by_key[e["key"]].append(e)
    for key in sorted(by_key):
        evs = sorted(by_key[key], key=lambda e: e["ts"])
        if len(evs) < min_key_events:
            continue
        tss = [e["ts"] for e in evs]
        gaps = [(b - a).total_seconds() / 60.0 for a, b in zip(tss, tss[1:])]
        med = statistics.median(gaps) if gaps else 0.0
        max_gap = max(gaps) if gaps else 0.0
        if med > 0 and max_gap >= hung_mult * med and max_gap >= ML_HUNG_ABS_FLOOR_MIN:
            rows.append(_advisory_row(now, model, surface="key", klass="hung", key=key,
                                      detail={"kind": "internal", "max_gap_min": round(max_gap, 1),
                                              "median_gap_min": round(med, 1),
                                              "hung_mult": hung_mult}, ledger=ledger))
        if tss[-1] <= now and med > 0:
            tail = (now - tss[-1]).total_seconds() / 60.0
            if tail >= hung_mult * med and tail >= ML_HUNG_ABS_FLOOR_MIN:
                rows.append(_advisory_row(now, model, surface="key", klass="hung", key=key,
                                          detail={"kind": "tail", "tail_min": round(tail, 1),
                                                  "median_gap_min": round(med, 1),
                                                  "hung_mult": hung_mult}, ledger=ledger))
        span = (tss[-1] - tss[0]).total_seconds() / 60.0
        if span >= dead_horizon_min:
            rows.append(_advisory_row(now, model, surface="key", klass="dead", key=key,
                                      detail={"span_min": round(span, 1),
                                              "horizon_min": dead_horizon_min,
                                              "events": len(evs)}, ledger=ledger))
    return rows


def ml_head(args) -> dict:
    """Run the ML advisory head over the ledger. Read-only + one advisory file."""
    now = _parse_ts(getattr(args, "ml_now", None)) or datetime.now(timezone.utc)
    ledger = str(args.ml_ledger)
    out: dict = {"rows": [], "summary": ""}
    try:
        events, bad = _load_series(Path(ledger))
    except OSError as exc:
        out["summary"] = f"ML ADVISORY: ledger unreadable ({exc}); nothing classified"
        return out
    if not events:
        out["summary"] = (f"ML ADVISORY: ledger has 0 parsable events "
                          f"({bad} bad lines); nothing classified")
        return out
    wins = list(_iter_windows(events, args.ml_window_min))
    feats, labels = [], []
    for t0, t1 in wins:
        win_events = [e for e in events if t0 <= e["ts"] < t1]
        feats.append(_window_features(win_events, t0, t1, args.ml_marker))
        labels.append(1 if (win_events and t0.date().isoformat() == args.ml_storm_day) else 0)
    storm_rows, metrics = _storm_rows(args.ml_model, wins, feats, labels, now, ledger)
    key_rows = _key_rows(args.ml_model, events, now, args.ml_hung_mult,
                         args.ml_dead_horizon_min, args.ml_min_key_events, ledger)
    rows = storm_rows + key_rows
    if not args.dry:
        args.ml_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.ml_out, "a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    n_hung = sum(1 for r in key_rows if r["klass"] == "hung")
    n_dead = sum(1 for k_r in key_rows if k_r["klass"] == "dead")
    out["rows"] = rows
    out["summary"] = (
        f"ML ADVISORY (model={args.ml_model}, ledger={ledger}): {len(events)} events, "
        f"{len(wins)} windows ({sum(1 for f in feats if f['n_events'] > 0)} with events), "
        f"{bad} bad lines; storm rows {len(storm_rows)} ({metrics}); "
        f"hung rows {n_hung}; dead rows {n_dead}; "
        f"advisory only: exit code and memory/attention.md untouched")
    return out


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--ml", action="store_true",
                    help="run the ML advisory head after the rule scan (advisory rows only)")
    ap.add_argument("--ml-only", action="store_true",
                    help="skip the WMI rule scan; ledger audit only, always exit 0")
    ap.add_argument("--ml-model", choices=["gbm", "iforest"], default="gbm")
    ap.add_argument("--ml-ledger", type=Path, default=ML_DEFAULT_LEDGER)
    ap.add_argument("--ml-window-min", type=float, default=60.0)
    ap.add_argument("--ml-storm-day", default="2026-09-24",
                    help="labeled storm date for the supervised head (FullScan 429 burst)")
    ap.add_argument("--ml-marker", default="429",
                    help="failure marker searched in brief/why/note/msg/error text")
    ap.add_argument("--ml-hung-mult", type=float, default=25.0,
                    help="hung fires at mult x median cadence (5h incident: 295min vs 10min)")
    ap.add_argument("--ml-dead-horizon-min", type=float, default=1440.0,
                    help="dead fires when a key span passes this horizon (11d runaway: 15840)")
    ap.add_argument("--ml-min-key-events", type=int, default=3)
    ap.add_argument("--ml-out", type=Path, default=ML_DEFAULT_OUT)
    ap.add_argument("--ml-now", default=None,
                    help="override analysis now (ISO ts) for reproducible tail checks")
    return ap


def main() -> int:
    args = _build_parser().parse_args()

    exit_code = 0
    if not args.ml_only:
        exit_code = _rule_scan(args)
    if args.ml or args.ml_only:
        result = ml_head(args)
        print(result["summary"])
        for row in result["rows"][:20]:
            print(json.dumps(row, ensure_ascii=False))
        if len(result["rows"]) > 20:
            print(f"... {len(result['rows']) - 20} more advisory rows in {args.ml_out}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
