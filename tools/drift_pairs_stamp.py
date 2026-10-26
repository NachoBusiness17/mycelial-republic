"""drift_pairs_stamp -- weekly auto-stamp of the teleological drift pairs (T1-T6).

THE 50 program, item 26 (W6 INSTRUMENTS, [LANE]): "Teleological drift pairs:
weekly auto-stamp". Born from TIME_TRAVEL_QSTAR_20260918.md section 5: every
drift pair stamped before 2026-09-18 paired a metric with a HISTORICAL referent;
the real referent is teleological, the filed future-state. The first three
teleological pairs (first stamps: memory/runs/adv_arc_50/teleo_drift_stamps.jsonl) are:

  T1  lane_activity_vs_filed_knowledge    teleo: Sep-20/October readiness
      metric  = daily count of lane trail rows (queue/lanes/*/trail.jsonl)
      referent = daily count of filed knowledge rows (memory/corpus/LINKS.jsonl)
  T2  mrpool_video_density_vs_message_density
      teleo: does the spoken layer track the filed urgency?
      metric  = daily count of MrPool media-register rows (the media layer;
                2,011 of 2,407 are .jpg, so "video density" is media density)
      referent = daily count of MrPool messages (watch/inbox/mrpool_export/ledger.jsonl)
  T3  anchored_proofs_vs_lane_activity    teleo: work -> verified receipts
      metric  = daily count of externally anchored LINKS rows (rows carrying a
                src/source/author field: the verified-receipt layer)
      referent = daily count of lane trail rows (same source as T1's metric)

Three more teleological pairs landed 2026-09-26 (burn wave B2-05), each pairing
a fleet metric with a FILED FUTURE DOCUMENT as referent:

  T4  lane_grind_vs_release_gates        teleo: VERSION_REGISTRY arc
      metric  = daily count of lane trail rows (queue/lanes/*/trail.jsonl)
      referent = daily count of release-gate rows
                (memory/improve/releases/gates.jsonl, the registry's own
                "behavioral trail"; window 60d so it reaches back over the
                registry's as_of 2026-08-06 era)
  T5  training_motion_vs_release_milestones
      teleo: the registry's per-version contract "one pass + release gate +
                training event + distill"
      metric  = daily count of training events (memory/training/events.jsonl)
      referent = daily count of release_milestone events (same file,
                pattern == "release_milestone"; window 60d, same reach)
  T6  fold_steps_vs_burn_receipts        teleo: receipts DNA (filed workdays)
      metric  = daily count of fold step rows (memory/trajectory/steps.jsonl)
      referent = daily count of burn-ledger receipt rows (memory/burns/
                LEDGER.jsonl; window 21d, the burn-wave program window)

Each pair feeds tools/drift.py drift_check(), which answers corr(dM, dR) with a
verdict: VACUOUS / ALIGNED / DRIFTING / INVERTED / DEGENERATE / INSUFFICIENT.

WEEKLY + IDEMPOTENT: one stamp per (ISO week, pair). The stamp week is the
ISO week of the run date. Re-running in the same week is a no-op (rows are
appended to memory/runs/adv_arc_50/teleo_drift_stamps.jsonl only when the
week+pair key is absent). Wire it weekly with any scheduler; it is safe to
fire daily because it writes at most once per week per pair.

REFERENT-AGE GUARD (spec written 2026-09-26, burn wave B2-66, BEFORE the
code below; pre-registered from the B2-05 receipt, which stamped T6
ALIGNED corr 0.6387 and then named it fragile: "ALIGNED on a 2-day-old
referent is fragile, not proven"):

  What the age is. Every stamp row carries referent_age_days: the
  referent layer's calendar days of observed life at stamp time,
  (run_date - earliest referent ts date).days + 1, first day counts as
  day 1 (the B2-05 counting: the burn ledger's first row is 2026-09-25,
  so its 2026-09-26 stamp is day 2). Rows also carry referent_first_date
  and referent_last_date so both youth and staleness stay auditable.
  Byte note: B2-05's "2 days old" is layer youth, not last-move recency
  (the ledger already held same-day rows at that stamp's write time,
  memory/burns/LEDGER.jsonl rows from 2026-09-26T00:06:31Z); the guard
  keys on what makes a young ALIGNED fragile: a correlation whose
  referent has less history than the stamp's own cadence is not proven,
  it is provisional.

  The threshold. REFERENT_MATURE_DAYS = 7: ALIGNED stands only when the
  referent layer is at least 7 calendar days old, one full weekly stamp
  period of referent life. Chosen so the named boundary case fires: the
  W39 T6 stamp (age 2) would have stamped FRAGILE-ALIGNED. For the burn
  ledger (first row 2026-09-25) the threshold turns on 2026-10-01.

  The downgrade. Only ALIGNED downgrades, to FRAGILE-ALIGNED, with the
  original verdict preserved in the row's verdict_guard (threshold_days,
  original_verdict, downgraded). DRIFTING / INVERTED / VACUOUS /
  DEGENERATE / INSUFFICIENT already mean what they mean at any referent
  age and pass through untouched. A referent with no dated rows (age
  None) is not mature.

  History. memory/runs/adv_arc_50/teleo_drift_stamps.jsonl is
  append-only: W39 rows keep their original verdicts, no backfill; the
  guard binds stamps from the next run on. Schema stays
  teleo_drift_stamp.v2 (additive fields only); readers keyed on
  verdict.verdict must treat FRAGILE-ALIGNED as ALIGNED's provisional
  cousin (ok flag and corr fields unchanged).

Deterministic: bucket edges and window ends derive from the data, never from
wall-clock beyond the run date's ISO week key. All counts are UTC dates.

Usage:
  .venv\\Scripts\\python.exe tools\\drift_pairs_stamp.py            # stamp if due
  .venv\\Scripts\\python.exe tools\\drift_pairs_stamp.py --status   # show ledger state
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from tools.drift import drift_check  # noqa: E402

LEDGER = ROOT / "memory" / "runs" / "adv_arc_50" / "teleo_drift_stamps.jsonl"
RECEIPT = ROOT / "watch" / "inbox" / "THE50_W6_T26_DRIFT_STAMP.receipt.json"

LANE_GLOB = "queue/lanes/*/trail.jsonl"
LINKS = ROOT / "memory" / "corpus" / "LINKS.jsonl"
POOL_MEDIA = ROOT / "watch" / "inbox" / "mrpool_export" / "media_register.jsonl"
POOL_MSGS = ROOT / "watch" / "inbox" / "mrpool_export" / "ledger.jsonl"
RELEASE_GATES = ROOT / "memory" / "improve" / "releases" / "gates.jsonl"
TRAINING = ROOT / "memory" / "training" / "events.jsonl"
STEPS = ROOT / "memory" / "trajectory" / "steps.jsonl"
BURNS = ROOT / "memory" / "burns" / "LEDGER.jsonl"

# B2-208 (2026-09-26): the regime-trail staleness tripwire. The B2-65 revival
# named this weekly stamp as the T4/T5 tripwire, but nothing here ever read
# gates.jsonl FRESHNESS: the referent could die by silence while the metric
# (memory/training/events.jsonl) kept growing, and every weekly stamp would
# keep filing FRAGILE verdicts against a corpse. Alarm rule: no gate row whose
# gate_id starts regime_ or graduation within STALENESS_TRIPWIRE_DAYS while
# the training tail has rows newer than the last such gate.
STALENESS_TRIPWIRE_DAYS = 14.0
_GATE_CLASS_RE = re.compile(r"^(regime_|graduation)", re.IGNORECASE)

LAW = ("a rate metric answers 'is it moving'; only corr(delta-M, delta-R) "
       "answers 'is it moving north'")

# Spec: module docstring, REFERENT-AGE GUARD (written before this code,
# B2-66 2026-09-26). 7 = one full weekly stamp period of referent life; the
# boundary case it must fire on is the W39 T6 stamp, whose burn-ledger
# referent was 2 days old (first row 2026-09-25) when B2-05 named its
# ALIGNED fragile. For that ledger the threshold turns on 2026-10-01.
REFERENT_MATURE_DAYS = 7


# ---------------------------------------------------------------- data plumbing

def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _utc_date(ts: Any) -> date | None:
    if not ts or not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc).date()
    except ValueError:
        return None


def _dates_of(rows: list[dict], key: str) -> list[date]:
    out = []
    for r in rows:
        d = _utc_date(r.get(key))
        if d is not None:
            out.append(d)
    return out


def _buckets(end: date, n_days: int) -> list[date]:
    return [end - timedelta(days=i) for i in range(n_days - 1, -1, -1)]


def _counts(dates: list[date], span: list[date]) -> list[int]:
    c = Counter(dates)
    return [c.get(d, 0) for d in span]


# ---------------------------------------------------------------- pair builders
# each returns (metric_series, referent_series, span_dates, source_provenance)

def _lane_rows() -> list[dict]:
    rows = []
    for f in sorted(glob.glob(str(ROOT / LANE_GLOB))):
        rows.extend(_read_jsonl(Path(f)))
    return rows


def _link_rows() -> list[dict]:
    return _read_jsonl(LINKS)


def _anchored_link_rows() -> list[dict]:
    return [r for r in _link_rows() if r.get("src") or r.get("source") or r.get("author")]


def _aligned_window(metric_dates: list[date], referent_dates: list[date],
                    n_days: int) -> list[date]:
    """Shared span: n daily buckets ending at the pair's latest observed date."""
    candidates = [d for d in (metric_dates + referent_dates) if d]
    end = max(candidates)
    return _buckets(end, n_days)


def pair_t1() -> dict:
    lanes, links = _lane_rows(), _link_rows()
    lane_d = _dates_of(lanes, "ts")
    link_d = _dates_of(links, "ts")
    span = _aligned_window(lane_d, link_d, 21)
    metric = _counts(lane_d, span)
    referent = _counts(link_d, span)
    src = {
        "metric": {"path": LANE_GLOB, "rows": len(lanes), "key": "ts"},
        "referent": {"path": "memory/corpus/LINKS.jsonl", "rows": len(links), "key": "ts"},
        "window_days": 21,
        "note": "referent is the filed-future layer (LINKS rows carry the Sep-20/October filings)",
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(link_d) if link_d else None,
            "referent_last": max(link_d) if link_d else None}


def pair_t2() -> dict:
    media = _read_jsonl(POOL_MEDIA)
    msgs = _read_jsonl(POOL_MSGS)
    media_d = _dates_of(media, "date")
    msg_d = _dates_of(msgs, "date")
    span = _aligned_window(media_d, msg_d, 13)
    metric = _counts(media_d, span)
    referent = _counts(msg_d, span)
    src = {
        "metric": {"path": "watch/inbox/mrpool_export/media_register.jsonl",
                   "rows": len(media), "key": "date"},
        "referent": {"path": "watch/inbox/mrpool_export/ledger.jsonl",
                     "rows": len(msgs), "key": "date"},
        "window_days": 13,
        "note": ("'video density' = the MrPool media layer; the register is mostly "
                 ".jpg stills with .mp4 video, counted whole"),
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(msg_d) if msg_d else None,
            "referent_last": max(msg_d) if msg_d else None}


def pair_t3() -> dict:
    anchors, lanes = _anchored_link_rows(), _lane_rows()
    anch_d = _dates_of(anchors, "ts")
    lane_d = _dates_of(lanes, "ts")
    span = _aligned_window(anch_d, lane_d, 21)
    metric = _counts(anch_d, span)
    referent = _counts(lane_d, span)
    src = {
        "metric": {"path": "memory/corpus/LINKS.jsonl",
                   "rows": len(anchors),
                   "filter": "rows carrying src/source/author (externally anchored)"},
        "referent": {"path": LANE_GLOB, "rows": len(lanes), "key": "ts"},
        "window_days": 21,
        "note": "anchored proofs = LINKS rows with an external anchor field",
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(lane_d) if lane_d else None,
            "referent_last": max(lane_d) if lane_d else None}


_TS_DATE_RE = re.compile(r'"ts": "(\d{4})-(\d{2})-(\d{2})')
_MILESTONE_RE = re.compile(r'"pattern": "release_milestone"')


def _training_dates():
    """Stream memory/training/events.jsonl (241 MB, ~548K rows) exactly once.

    Returns (all_event_dates, release_milestone_dates, rows_without_ts).
    Regex extraction instead of json.loads per row: the weekly stamp needs
    only the ts date and the pattern field, and the regex pass measured
    2.3 s vs roughly a minute for full per-row parsing (2026-09-26).
    Rows whose ts is unparseable are skipped and COUNTED, not silently
    dropped: the counts are reported in the stamp's source provenance.
    """
    all_d: list = []
    mile_d: list = []
    skipped = 0
    with TRAINING.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _TS_DATE_RE.search(line)
            if not m:
                skipped += 1
                continue
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            all_d.append(d)
            if _MILESTONE_RE.search(line):
                mile_d.append(d)
    return all_d, mile_d, skipped


def pair_t4() -> dict:
    lanes, gates = _lane_rows(), _read_jsonl(RELEASE_GATES)
    lane_d = _dates_of(lanes, "ts")
    gate_d = _dates_of(gates, "ts")
    span = _aligned_window(lane_d, gate_d, 60)
    metric = _counts(lane_d, span)
    referent = _counts(gate_d, span)
    src = {
        "metric": {"path": LANE_GLOB, "rows": len(lanes), "key": "ts"},
        "referent": {"path": "memory/improve/releases/gates.jsonl",
                     "rows": len(gates), "key": "ts",
                     "doc": "docs/ref/releases/VERSION_REGISTRY.md behavioral trail"},
        "window_days": 60,
        "note": ("referent is the VERSION_REGISTRY behavioral trail "
                 "(mag_release_gate.v1); the 60-day window reaches back over "
                 "the registry's as_of 2026-08-06 era"),
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(gate_d) if gate_d else None,
            "referent_last": max(gate_d) if gate_d else None}


def pair_t5() -> dict:
    all_d, mile_d, skipped = _training_dates()
    span = _aligned_window(all_d, mile_d, 60)
    metric = _counts(all_d, span)
    referent = _counts(mile_d, span)
    src = {
        "metric": {"path": "memory/training/events.jsonl",
                   "rows": len(all_d), "key": "ts",
                   "rows_skipped_no_ts": skipped},
        "referent": {"path": "memory/training/events.jsonl",
                     "rows": len(mile_d),
                     "filter": 'pattern == "release_milestone" (the version arc)',
                     "doc": "docs/ref/releases/VERSION_REGISTRY.md training-event leg"},
        "window_days": 60,
        "note": ("teleological referent: the registry contract files one "
                 "release_milestone training event per version gate; the metric "
                 "is the loop's whole daily motion"),
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(mile_d) if mile_d else None,
            "referent_last": max(mile_d) if mile_d else None}


def pair_t6() -> dict:
    steps, burns = _read_jsonl(STEPS), _read_jsonl(BURNS)
    step_d = _dates_of(steps, "ts")
    burn_d = _dates_of(burns, "ts")
    span = _aligned_window(step_d, burn_d, 21)
    metric = _counts(step_d, span)
    referent = _counts(burn_d, span)
    src = {
        "metric": {"path": "memory/trajectory/steps.jsonl",
                   "rows": len(steps), "key": "ts"},
        "referent": {"path": "memory/burns/LEDGER.jsonl",
                     "rows": len(burns), "key": "ts",
                     "doc": "filed receipts layer (docs/DNA.md: filed workdays)"},
        "window_days": 21,
        "note": ("teleological referent: burn-ledger receipts are the filed "
                 "workday layer; the metric is the fold's recorded step motion"),
    }
    return {"metric": metric, "referent": referent, "span": span, "sources": src,
            "referent_first": min(burn_d) if burn_d else None,
            "referent_last": max(burn_d) if burn_d else None}


PAIRS: dict[str, dict] = {
    "T1": {"pair": "lane_activity_vs_filed_knowledge",
           "teleo": "Sep-20/October readiness: do the lanes grind toward the filed future?",
           "build": pair_t1},
    "T2": {"pair": "mrpool_video_density_vs_message_density",
           "teleo": "does the spoken layer track the filed urgency?",
           "build": pair_t2},
    "T3": {"pair": "anchored_proofs_vs_lane_activity",
           "teleo": "work -> verified receipts",
           "build": pair_t3},
    "T4": {"pair": "lane_grind_vs_release_gates",
           "teleo": "VERSION_REGISTRY arc: does daily lane grind move the "
                    "release-gate behavioral trail?",
           "build": pair_t4},
    "T5": {"pair": "training_motion_vs_release_milestones",
           "teleo": "the registry's per-version contract (one pass + release "
                    "gate + training event + distill): does loop motion track "
                    "filed version milestones?",
           "build": pair_t5},
    "T6": {"pair": "fold_steps_vs_burn_receipts",
           "teleo": "receipts DNA (residual + registry + leaf = filed workdays): "
                    "does the fold's step motion track filed burn receipts?",
           "build": pair_t6},
}


# ---------------------------------------------------------------- stamping

def _referent_age_days(referent_first: date | None, run_date: date) -> int | None:
    """Calendar days of the referent layer's observed life at stamp time.

    Inclusive counting, the B2-05 counting: a layer whose first row is
    yesterday is 2 days old at a today stamp (burn ledger first row
    2026-09-25, W39 stamp 2026-09-26 = day 2). None if the referent has
    no dated rows. Spec: module docstring, REFERENT-AGE GUARD.
    """
    if referent_first is None:
        return None
    return (run_date - referent_first).days + 1


def _apply_aging_guard(verdict: dict, age: int | None) -> dict:
    """ALIGNED downgrades to FRAGILE-ALIGNED while its referent is immature.

    Spec: module docstring, REFERENT-AGE GUARD (B2-66, 2026-09-26), the
    mechanical form of B2-05's "ALIGNED on a 2-day-old referent is
    fragile, not proven". Only ALIGNED downgrades: DRIFTING / INVERTED /
    VACUOUS / DEGENERATE / INSUFFICIENT mean what they mean at any
    referent age. A referent with no dated rows (age None) is not
    mature. Returns a copy when downgrading; the input dict is never
    mutated.
    """
    original = verdict.get("verdict")
    mature = age is not None and age >= REFERENT_MATURE_DAYS
    if original == "ALIGNED" and not mature:
        guarded = dict(verdict)
        guarded["verdict"] = "FRAGILE-ALIGNED"
        guarded["note"] = (
            "downgraded from ALIGNED: referent_age_days "
            f"{age if age is not None else 'unknown'} < "
            f"REFERENT_MATURE_DAYS {REFERENT_MATURE_DAYS} "
            "(B2-05: aligned on a young referent is fragile, not proven)"
        )
        return guarded
    return verdict


def _week_key(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def _stamped_keys(ledger_rows: list[dict]) -> set[tuple[str, str]]:
    out = set()
    for r in ledger_rows:
        if r.get("schema") == "teleo_drift_stamp.v2" and r.get("verdict", {}).get("ok"):
            out.add((r.get("week_key", ""), r.get("pair_id", "")))
    return out


def stamp(today: date | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date()
    week = _week_key(today)
    ledger_rows = _read_jsonl(LEDGER)
    done = _stamped_keys(ledger_rows)
    stamped_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    results = []
    added = skipped = 0
    new_rows = []
    for pid, spec in PAIRS.items():
        built = spec["build"]()
        verdict = drift_check(built["metric"], built["referent"], label=f"teleological drift pair {pid}")
        ref_first = built.get("referent_first")
        ref_last = built.get("referent_last")
        age = _referent_age_days(ref_first, today)
        guarded = _apply_aging_guard(verdict, age)
        row = {
            "schema": "teleo_drift_stamp.v2",
            "week_key": week,
            "pair_id": pid,
            "pair": spec["pair"],
            "teleo": spec["teleo"],
            "stamped_at": stamped_at,
            "generator": "tools/drift_pairs_stamp.py",
            "verdict": guarded,
            "referent_first_date": ref_first.isoformat() if ref_first else None,
            "referent_last_date": ref_last.isoformat() if ref_last else None,
            "referent_age_days": age,
            "verdict_guard": {
                "rule": ("ALIGNED downgrades to FRAGILE-ALIGNED while "
                         "referent_age_days < REFERENT_MATURE_DAYS"),
                "threshold_days": REFERENT_MATURE_DAYS,
                "original_verdict": verdict.get("verdict"),
                "downgraded": guarded is not verdict,
            },
            "window": {
                "start": built["span"][0].isoformat(),
                "end": built["span"][-1].isoformat(),
                "buckets": len(built["span"]),
                "metric_total": sum(built["metric"]),
                "referent_total": sum(built["referent"]),
            },
            "sources": built["sources"],
            "law": LAW,
        }
        results.append(row)
        if (week, pid) in done:
            skipped += 1
            row["appended"] = False
        else:
            new_rows.append(row)
            row["appended"] = True
            added += 1

    if new_rows:
        with LEDGER.open("a", encoding="utf-8") as f:
            for row in new_rows:
                f.write(json.dumps(row, ensure_ascii=True) + "\n")

    # the receipt always reflects what the ledger holds for this week
    ledger_now = [r for r in _read_jsonl(LEDGER)
                  if r.get("schema") == "teleo_drift_stamp.v2" and r.get("week_key") == week]
    ledger_now.sort(key=lambda r: r.get("pair_id", ""))

    receipt = {
        "receipt": "THE 50 W6 T26: weekly auto-stamp of the teleological drift pairs (T1-T6)",
        "filed": stamped_at,
        "week_key": week,
        "generator": "tools/drift_pairs_stamp.py",
        "ledger": "memory/runs/adv_arc_50/teleo_drift_stamps.jsonl",
        "run": {"stamps_appended": added, "stamps_skipped_already_stamped": skipped},
        "week_stamps_in_ledger": [
            {
                "pair_id": r.get("pair_id"),
                "pair": r.get("pair"),
                "verdict": r.get("verdict", {}).get("verdict"),
                "corr_dm_dr": r.get("verdict", {}).get("corr_dm_dr"),
                "deltas_used": r.get("verdict", {}).get("deltas_used"),
                "referent_age_days": r.get("referent_age_days"),
                "window": r.get("window"),
                "stamped_at": r.get("stamped_at"),
            }
            for r in ledger_now
        ],
        "wiring": ("idempotent by ISO week: safe to schedule daily or weekly; it writes "
                   "each pair at most once per week. Example weekly registration "
                   "(operator-gated, not run here): schtasks /Create /SC WEEKLY /D MON "
                   "/ST 08:15 /TN THE50_W6_T26_drift_pairs_stamp /TR "
                   "\"C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.venv\\Scripts\\python.exe "
                   "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\tools\\drift_pairs_stamp.py\""),
        "first_stamps_provenance": ("T1-T3 pair definitions and first stamps: "
                                    "memory/runs/adv_arc_50/teleo_drift_stamps.jsonl "
                                    "(bare drift_check rows on disk: no schema field, "
                                    "no timestamp field, so the 2026-09-18/19 stamp "
                                    "dates are receipt-attested only, not row-attested; "
                                    "corrected 2026-09-26, cause: wave-2 audit batch 5.1); "
                                    "T4-T6 landed with "
                                    "burn wave B2-05 2026-09-26 (filed-future referents: "
                                    "VERSION_REGISTRY behavioral trail, release_milestone "
                                    "training events, burn-ledger receipts); "
                                    "instrument: tools/drift.py"),
        "no_em_dash": True,
    }
    # B2-208: the tripwire rides every stamp so referent death files itself.
    trip = staleness_tripwire()
    receipt["staleness_tripwire"] = trip
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=1, ensure_ascii=True), encoding="utf-8")

    return {"week_key": week, "added": added, "skipped": skipped, "results": results,
            "staleness_tripwire": trip}


def _last_training_ts(training_tail_bytes: int = 2_000_000) -> date | None:
    """Last ts date in memory/training/events.jsonl without a full scan.

    The file is ~241 MB and grows; the staleness question only needs the NEWEST
    row, so read a bounded tail, drop the (likely partial) first line, and take
    the last parseable ts.
    """
    try:
        size = TRAINING.stat().st_size
    except OSError:
        return None
    with TRAINING.open("rb") as f:
        f.seek(max(0, size - training_tail_bytes))
        chunk = f.read(training_tail_bytes)
    lines = chunk.split(b"\n")
    if size > training_tail_bytes:
        lines = lines[1:]  # first line is a likely-partial row
    last = None
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line.decode("utf-8", errors="replace"))
        except Exception:
            continue
        last = _utc_date(row.get("ts"))
        if last is not None:
            break
    return last


def staleness_tripwire(now: date | None = None) -> dict:
    """B2-208 (2026-09-26): alarm when the regime trail goes silent mid-growth.

    Alarm = no gate row of class regime_* / graduation* within
    STALENESS_TRIPWIRE_DAYS while memory/training/events.jsonl has rows newer
    than the last such gate (T4/T5 referent death filing itself, per the B2-65
    revival law). Advisory output, never an exception: callers (status, stamp,
    main) attach the dict verbatim.
    """
    today = now or _utc_date(datetime.now(timezone.utc).isoformat())
    gates = [r for r in _read_jsonl(RELEASE_GATES)
             if _GATE_CLASS_RE.match(str(r.get("gate_id") or ""))]
    gate_d = _dates_of(gates, "ts")
    out: dict = {
        "tripwire": "regime_trail_staleness",
        "threshold_days": STALENESS_TRIPWIRE_DAYS,
        "gate_class": "gate_id startswith regime_ | graduation",
        "gate_rows_considered": len(gates),
        "last_gate_date": max(gate_d).isoformat() if gate_d else None,
    }
    if not gate_d:
        out.update(alarm=True,
                   reason="no regime_*/graduation gate rows at all: referent "
                          "silence since birth while the metric may still grow")
        return out
    last_training = _last_training_ts()
    out["last_training_date"] = last_training.isoformat() if last_training else None
    days_since_gate = (today - max(gate_d)).days
    out["days_since_last_gate"] = days_since_gate
    grew = bool(last_training and last_training > max(gate_d))
    out["training_grew_since_last_gate"] = grew
    if days_since_gate >= STALENESS_TRIPWIRE_DAYS and grew:
        out.update(alarm=True,
                   reason=("no regime_*/graduation gate in %d days while "
                           "training events keep landing: T4/T5 referent death "
                           "is live" % days_since_gate))
    elif days_since_gate >= STALENESS_TRIPWIRE_DAYS:
        out.update(alarm=False,
                   reason=("stale %d days past the last gate, but training has "
                           "nothing newer than it: no growth to measure against "
                           "a dead referent" % days_since_gate))
    else:
        out.update(alarm=False, reason="fresh (%d days since last gate)" % days_since_gate)
    return out


def status() -> dict:
    ledger_rows = _read_jsonl(LEDGER)
    v2 = [r for r in ledger_rows if r.get("schema") == "teleo_drift_stamp.v2"]
    weeks = sorted({r.get("week_key", "") for r in v2})
    return {"ledger": str(LEDGER), "v1_rows": len(ledger_rows) - len(v2),
            "v2_rows": len(v2), "weeks_stamped": weeks,
            "staleness_tripwire": staleness_tripwire()}


def main(argv: list[str]) -> int:
    if "--status" in argv:
        print(json.dumps(status(), indent=2))
        return 0
    out = stamp()
    print(f"week {out['week_key']}: {out['added']} stamped, "
          f"{out['skipped']} already stamped (idempotent no-op)")
    for r in out["results"]:
        v = r["verdict"]
        state = "appended" if r["appended"] else "skipped (already stamped this week)"
        print(f"  {r['pair_id']} {r['pair']}: {v['verdict']} "
              f"corr={v.get('corr_dm_dr')} deltas={v.get('deltas_used')} [{state}]")
    trip = out.get("staleness_tripwire") or {}
    if trip.get("alarm"):
        print(f"TRIPWIRE ALARM: {trip.get('reason')} "
              f"(last gate {trip.get('last_gate_date')}, "
              f"days {trip.get('days_since_last_gate')})")
    print(f"receipt: {RECEIPT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
