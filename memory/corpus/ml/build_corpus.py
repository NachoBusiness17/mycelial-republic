"""Build the labeled ML training corpus from estate history (lane ml1-ledger-corpus, ml-moonshot-20261007).

One parquet + one csv per source under memory/corpus/ml/training/:
  gauntlet, usage, registry, gps_capability, gps_verdicts, trail_events, incidents
plus build_manifest.json (sha256 + row counts per source) so every downstream
trainer can verify the byte origin of what it trains on.

Run: .venv/Scripts/python.exe memory/corpus/ml/build_corpus.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "memory" / "corpus" / "ml" / "training"
OUT.mkdir(parents=True, exist_ok=True)

SRC_GAUNTLET = ROOT / "watch" / "inbox" / "gauntlet" / "GAUNTLET_REGISTER.jsonl"
SRC_USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
SRC_REGISTRY = ROOT / "memory" / "workflows" / "REGISTRY.jsonl"
SRC_GPS = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
SRC_TRAILS = ROOT / "dashboard" / "static" / "trails"

# Receipt anchors for the incident table. Each tuple: (class, path, grep regex, label)
RECEIPT_ANCHORS = {
    "elder_429_streak": (
        ROOT / "watch" / "inbox" / "go_wave_20261004" / "CSV_VERDICT_20261004.md",
        r"trailing",
    ),
    "dwf_429_1302_storm": (
        ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_443_dwf_error_census_20260926.md",
        r"896 model\.network\.failed",
    ),
    "stash_sweep": (
        ROOT / "watch" / "inbox" / "DAWN_REPORT_20261006.md",
        r"stash-sweeps as a defect class",
    ),
    "stash_sweep_cure": (
        ROOT / "watch" / "inbox" / "DRIFT_PATROL_20261007.md",
        r"stash-sweep-watch detector",
    ),
    "phantom_191_8": (
        ROOT / "watch" / "inbox" / "gala_20260925" / "fillball-1001" / "lanes" / "_191_8_grep_raw.txt",
        r"191\.8M",
    ),
    "output_dead_lanes": (
        ROOT / "corpus" / "steal" / "MASTER_READ_ESTATE.md",
        r"Mechanically-alive, output-dead lanes",
    ),
}

# Register errata counts (corpus/steal/MASTER_READ_ESTATE.md section 10, D6/D7/D8).
REGISTER_ERRATA = {
    "errno22_by_lane": {"builder": 370, "research": 513, "night": 26, "prose": 1, "day_work": 0},
    "elder_429_streak": 14,
    "night_march_rc1": 28,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_both(df: pd.DataFrame, name: str) -> None:
    df.to_parquet(OUT / f"{name}.parquet", index=False)
    df.to_csv(OUT / f"{name}.csv", index=False, encoding="utf-8")


def build_gauntlet() -> pd.DataFrame:
    rows = read_jsonl(SRC_GAUNTLET)
    out = []
    # A row is superseded when a later row (higher file line) with the same
    # work_id carries a CORRECTED note; the register appends corrections,
    # never rewrites (GAUNTLET_FREE_LANDED_20261006.md, grader self-strike).
    later_corrected = {}
    for i, r in enumerate(rows):
        if "CORRECTED" in r.get("note", ""):
            later_corrected.setdefault(r["work_id"], i)
    for i, r in enumerate(rows):
        note = r.get("note", "")
        m_onset = re.search(r"(\d+)/(\d+) onsets", note)
        m_overlap = re.search(r"overlap ([\d.]+)/([\d.]+)/([\d.]+)", note)
        out.append(
            {
                "source_line": i + 1,
                "ts": r.get("ts"),
                "work_id": r.get("work_id"),
                "family": r.get("family"),
                "provider": r.get("provider"),
                "animal": r.get("model"),
                "verdict": r.get("verdict"),
                "pass_label": {"PASS": 1, "FAIL": 0}.get(r.get("verdict")),
                "onsets_made": int(m_onset.group(1)) if m_onset else None,
                "onsets_total": int(m_onset.group(2)) if m_onset else None,
                "onsets_frac": (int(m_onset.group(1)) / int(m_onset.group(2))) if m_onset else None,
                "overlap_1": float(m_overlap.group(1)) if m_overlap else None,
                "overlap_2": float(m_overlap.group(2)) if m_overlap else None,
                "overlap_3": float(m_overlap.group(3)) if m_overlap else None,
                "corrected": "CORRECTED" in note,
                "superseded": i < later_corrected.get(r.get("work_id"), -1),
                "note": note,
                "expensive_ref": r.get("expensive_ref"),
            }
        )
    df = pd.DataFrame(out)
    df["ts"] = pd.to_datetime(df["ts"], format="ISO8601", utc=True, errors="coerce")
    return df


def build_usage() -> pd.DataFrame:
    rows = read_jsonl(SRC_USAGE)
    out = []
    for r in rows:
        pt = r.get("prompt_tokens")
        ct = r.get("completion_tokens")
        total = (pt or 0) + (ct or 0) if (pt is not None or ct is not None) else None
        out.append(
            {
                "ts": r.get("ts"),
                "id": r.get("id"),
                "model": r.get("model"),
                "turn": r.get("turn"),
                "prompt_tokens": pt,
                "completion_tokens": ct,
                "reasoning_tokens": r.get("reasoning_tokens"),
                "total_tokens": total,
                "cost_usd": r.get("cost_usd"),
                "ok": r.get("ok"),
                "ok_label": int(r["ok"]) if isinstance(r.get("ok"), bool) else None,
                "http_status": r.get("http_status"),
                "finish_reason": r.get("finish_reason"),
                "transport_error": r.get("transport_error"),
                "refused": r.get("refused"),
                "channel": r.get("channel"),
                "error": r.get("error"),
            }
        )
    df = pd.DataFrame(out)
    df["ts"] = pd.to_datetime(df["ts"], format="ISO8601", utc=True, errors="coerce")
    return df


def build_registry() -> pd.DataFrame:
    rows = read_jsonl(SRC_REGISTRY)
    check_ids = sorted({c["id"] for r in rows for c in r.get("checks", [])})
    seen_digest: dict[tuple, int] = {}
    out = []
    for r in rows:
        checks = {c["id"]: bool(c.get("ok")) for c in r.get("checks", [])}
        key = (r.get("name"), r.get("digest"))
        seen_digest[key] = seen_digest.get(key, 0) + 1
        attempt = seen_digest[key]
        new_digest = attempt == 1
        out.append(
            {
                "ts": r.get("ts"),
                "name": r.get("name"),
                "digest": r.get("digest"),
                "script": r.get("script"),
                "verdict": r.get("verdict"),
                "pass_label": {"PASS": 1, "FAIL": 0}.get(r.get("verdict")),
                "n_checks": len(checks),
                "n_checks_failed": sum(1 for v in checks.values() if not v),
                "new_digest": new_digest,
                **{f"check_{cid.replace('-', '_').lower()}": checks.get(cid) for cid in check_ids},
            }
        )
    df = pd.DataFrame(out)
    df["ts"] = pd.to_datetime(df["ts"], format="ISO8601", utc=True, errors="coerce")
    return df


def build_gps() -> tuple[pd.DataFrame, pd.DataFrame]:
    con = sqlite3.connect(SRC_GPS)
    try:
        v = pd.read_sql_query(
            "SELECT ts, model_id, task_shape, verdict, evidence_hash, evidence_resolved,"
            " evidence_source, evidence_bytes FROM verdict_log ORDER BY ts",
            con,
        )
        c = pd.read_sql_query(
            "SELECT model_id, task_shape, pass_rate, sample_size, cost_usd_per_call,"
            " last_measured, updated_at FROM capability ORDER BY model_id, task_shape",
            con,
        )
    finally:
        con.close()
    v["ts"] = pd.to_datetime(v["ts"], format="ISO8601", utc=True, errors="coerce")
    v = v.rename(columns={"verdict": "verdict_label"})
    return c, v


RC_RE = re.compile(r"\brc=(\d+)")
MARCH_RE = re.compile(r"march rc=(\d+)")
MONITOR_RE = re.compile(r"monitor rc=(\d+)")
ERRNO_RE = re.compile(r"\[Errno (\d+)\]|errno (\d+)", re.IGNORECASE)
HTTP429_RE = re.compile(r"\b429\b")
HTTP1302_RE = re.compile(r"\b1302\b")


def build_trail_events() -> pd.DataFrame:
    out = []
    for f in sorted(SRC_TRAILS.glob("*.jsonl")):
        lane = f.stem
        for i, line in enumerate(f.open("r", encoding="utf-8", errors="replace")):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                out.append({"lane": lane, "source_line": i + 1, "ts": None, "parse_error": True})
                continue
            detail = str(r.get("detail", ""))
            m_errno = ERRNO_RE.search(detail)
            m_rc = RC_RE.search(detail)
            m_march = MARCH_RE.search(detail)
            m_monitor = MONITOR_RE.search(detail)
            out.append(
                {
                    "lane": lane,
                    "source_line": i + 1,
                    "ts": r.get("ts"),
                    "actor": r.get("actor"),
                    "event": r.get("event"),
                    "errno": int(m_errno.group(1) or m_errno.group(2)) if m_errno else None,
                    "errno22": bool(m_errno) and int(m_errno.group(1) or m_errno.group(2)) == 22,
                    "rc": int(m_rc.group(1)) if m_rc else None,
                    "monitor_rc": int(m_monitor.group(1)) if m_monitor else None,
                    "march_rc": int(m_march.group(1)) if m_march else None,
                    "is_429": bool(HTTP429_RE.search(detail)),
                    "is_1302": bool(HTTP1302_RE.search(detail)),
                    "is_cycle_fail": r.get("event") == "CYCLE_FAIL",
                    "detail_len": len(detail),
                    "detail": detail,
                    "artifacts": ";".join(r.get("artifacts", [])),
                    "parse_error": False,
                }
            )
    df = pd.DataFrame(out)
    df["ts"] = pd.to_datetime(df["ts"], format="ISO8601", utc=True, errors="coerce")
    return df


def quote_from(path: Path, pattern: str, max_words: int = 38) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.search(pattern, line):
            words = line.strip().split()
            q = " ".join(words[:max_words])
            return q + (" ..." if len(words) > max_words else "")
    return None


def build_incidents(trail: pd.DataFrame) -> pd.DataFrame:
    rows = []

    def add(incident_id, cls, surface, first_seen, last_seen, measured, basis,
            register_count, evidence_path, quote, cured):
        rows.append({
            "incident_id": incident_id,
            "class": cls,
            "surface": surface,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "measured_count": measured,
            "count_basis": basis,
            "register_count": register_count,
            "evidence_path": evidence_path,
            "quote": quote,
            "cured": cured,
            "label": 1,
        })

    # 1. errno-22 runner_state family, per trail lane (bytes) vs register D6.
    e22 = trail[trail["errno22"] == True]  # noqa: E712
    for lane in sorted(set(e22["lane"]) | set(REGISTER_ERRATA["errno22_by_lane"])):
        sub = e22[e22["lane"] == lane]
        reg = REGISTER_ERRATA["errno22_by_lane"].get(lane)
        if len(sub) == 0 and (reg is None or reg == 0):
            continue
        first = sub["ts"].min() if len(sub) else None
        last = sub["ts"].max() if len(sub) else None
        q = None
        if len(sub):
            raw = str(sub.iloc[0]["detail"])
            q = " ".join(raw.split()[:38])
        add(
            f"errno22_{lane}", "errno22_runner_state", f"dashboard/static/trails/{lane}.jsonl",
            first, last, int(len(sub)), "bytes", reg,
            "dashboard/static/trails (trail_events errno22=1)",
            q,
            "owed: trail cure pack unit 1, single-writer-guard or path-fix (MASTER_READ row 7)",
        )

    # 2. elder 429 streak (bytes + receipt).
    elder429 = trail[(trail["lane"] == "elder") & (trail["is_429"] == True)]  # noqa: E712
    add(
        "elder_429_streak", "http_429_storm", "dashboard/static/trails/elder.jsonl",
        elder429["ts"].min() if len(elder429) else None,
        elder429["ts"].max() if len(elder429) else None,
        int(len(elder429)), "bytes", REGISTER_ERRATA["elder_429_streak"],
        "watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md",
        quote_from(*RECEIPT_ANCHORS["elder_429_streak"]),
        "cured 2026-10-04T08:20:40Z: CR-in-Bearer, strip at key load (trail cure pack unit 2)",
    )

    # 3. research-lane 429s (monitor source-down).
    res429 = trail[(trail["lane"] == "research") & (trail["is_429"] == True)]  # noqa: E712
    add(
        "research_429_monitor", "http_429_storm", "dashboard/static/trails/research.jsonl",
        res429["ts"].min() if len(res429) else None,
        res429["ts"].max() if len(res429) else None,
        int(len(res429)), "bytes", None,
        "dashboard/static/trails/research.jsonl (trail_events is_429=1)", None, None,
    )

    # 4. dwf workflow-child 429/1302 storm (receipt census).
    add(
        "dwf_429_1302_storm", "http_429_storm",
        "~/.zcode/cli/log/zcode-2026-09-2*.jsonl", None, None, 896, "receipt", None,
        "watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md",
        quote_from(*RECEIPT_ANCHORS["dwf_429_1302_storm"]),
        "gated: workflow max_concurrency cap (dispatch-shape gate card)",
    )

    # 5. night march rc=1 composites (bytes vs register D8).
    night = trail[trail["lane"] == "night"]
    march = night[night["march_rc"] == 1]
    add(
        "night_march_rc1", "hung_cycle", "dashboard/static/trails/night.jsonl",
        march["ts"].min() if len(march) else None,
        march["ts"].max() if len(march) else None,
        int(len(march)), "bytes", REGISTER_ERRATA["night_march_rc1"],
        "dashboard/static/trails/night.jsonl (trail_events march_rc=1, lane night)",
        None, "owed: trail cure pack unit 3, sanctioned env door for the night march",
    )

    # 6. mechanically-alive, output-dead lanes (receipt).
    add(
        "output_dead_lanes", "hung_cycle", "dashboard/static/trails/*.jsonl", None, None,
        6, "receipt", None,
        "corpus/steal/MASTER_READ_ESTATE.md (curiosity findings row 6)",
        quote_from(*RECEIPT_ANCHORS["output_dead_lanes"]), None,
    )

    # 7. stash sweep (receipt + cure).
    add(
        "stash_sweep", "stash_sweep", "git working tree (shared single tree)", None, None,
        3, "receipt", None,
        "watch/inbox/DAWN_REPORT_20261006.md",
        quote_from(*RECEIPT_ANCHORS["stash_sweep"]),
        "cured overnight 2026-10-07: stash-sweep-watch detector (DOGFOOD2 15/15 lanes)",
    )
    add(
        "stash_sweep_cure", "stash_sweep", "watch/inbox/DRIFT_PATROL_20261007.md", None, None,
        1, "receipt", None,
        "watch/inbox/DRIFT_PATROL_20261007.md",
        quote_from(*RECEIPT_ANCHORS["stash_sweep_cure"]),
        "detector landed (the R3 incident cure)",
    )

    # 8. phantom number 191.8M (receipt + grep raw + gate).
    add(
        "phantom_191_8", "phantom_number",
        ".agents/skills/frontier-mine/SKILL.md", None, None, 1, "receipt", None,
        "watch/inbox/gala_20260925/fillball-1001/lanes/_191_8_grep_raw.txt",
        quote_from(*RECEIPT_ANCHORS["phantom_191_8"]),
        "gated: tools/citation_lint.py PHANTOM-NUMBER check at pre-push",
    )

    return pd.DataFrame(rows)


def main() -> None:
    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {"build_ts": built, "python": "3.11.15", "pandas": pd.__version__, "sources": []}

    gauntlet = build_gauntlet()
    write_both(gauntlet, "gauntlet")

    usage = build_usage()
    write_both(usage, "usage")

    registry = build_registry()
    write_both(registry, "registry")

    gps_cap, gps_ver = build_gps()
    write_both(gps_cap, "gps_capability")
    write_both(gps_ver, "gps_verdicts")

    trail = build_trail_events()
    write_both(trail, "trail_events")

    incidents = build_incidents(trail)
    write_both(incidents, "incidents")

    sources = [
        ("gauntlet", SRC_GAUNTLET, gauntlet),
        ("usage", SRC_USAGE, usage),
        ("registry", SRC_REGISTRY, registry),
        ("gps_capability", SRC_GPS, gps_cap),
        ("gps_verdicts", SRC_GPS, gps_ver),
        ("trail_events", SRC_TRAILS, trail),
        ("incidents", None, incidents),
    ]
    for name, src, df in sources:
        entry = {
            "table": name,
            "rows": int(len(df)),
            "columns": list(map(str, df.columns)),
            "source": str(src.relative_to(ROOT)) if src and src != SRC_TRAILS else (
                "dashboard/static/trails/*.jsonl" if src == SRC_TRAILS else
                "derived: trail_events + receipts (see incidents.evidence_path)"
            ),
        }
        if src is not None and src.is_file():
            entry["sha256"] = sha256_file(src)
            entry["bytes"] = src.stat().st_size
        if src == SRC_TRAILS:
            # The trails are live (rows appended between builds); pin each
            # lane file this build read so trainers can verify their snapshot.
            entry["sha256_by_file"] = {
                f.name: sha256_file(f) for f in sorted(SRC_TRAILS.glob("*.jsonl"))
            }
        manifest["sources"].append(entry)

    (OUT / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    for entry in manifest["sources"]:
        print(f"{entry['table']}: {entry['rows']} rows from {entry['source']}")
    print(f"manifest: {OUT / 'build_manifest.json'}")


if __name__ == "__main__":
    main()
