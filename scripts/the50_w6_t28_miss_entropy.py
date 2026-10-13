"""THE 50 W6 T28: miss-entropy dashboard - minimal JSON data path.

Reads the three real miss corpora on disk and computes the G13 panels
(GPS battery row 13, cache_os: "The health metric is not hit rate but
the ENTROPY of misses"):

  1. prophecy_called_shot : verdict-filed misses in the called-shot ledgers
  2. ops_fkb_failures     : fkb_failure events in training/events.jsonl
  3. jev_meter            : meter_correct=false packets in the JEV trail

Writes memory/runs/the50/w6_t28_miss_entropy.json (the data path the
dashboard would read). All numbers are computed here, never hand-counted.

Run: .venv\\Scripts\\python.exe scripts\\the50_w6_t28_miss_entropy.py
"""
import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = ROOT / "memory" / "runs" / "the50" / "w6_t28_miss_entropy.json"
CUTOFF = "2026-09-25"  # expired/open boundary, stated, not hidden (re-filed 2026-09-25)


def rows(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def entropy(counter):
    """Shannon H in bits over a bucket counter, plus normalization inputs."""
    n = sum(counter.values())
    if n == 0:
        return {"H_bits": None, "K": 0, "H_max_bits": None, "H_norm": None,
                "top1_share": None, "top5_share": None, "n": 0}
    k = len(counter)
    h = -sum((c / n) * math.log2(c / n) for c in counter.values())
    hmax = math.log2(k) if k > 1 else 0.0
    counts = sorted(counter.values(), reverse=True)
    top5 = sum(counts[:5])
    return {"H_bits": round(h, 4), "K": k, "H_max_bits": round(hmax, 4),
            "H_norm": round(h / hmax, 4) if hmax > 0 else 0.0,
            "top1_share": round(counts[0] / n, 4),
            "top5_share": round(top5 / n, 4),
            "n": n}


def month_of(ts):
    return ts[:7] if ts else None


# ---------------------------------------------------------------- 1. prophecy
v1 = rows(ROOT / "watch/inbox/mrpool_export/called_shot_ledger.jsonl")
v2 = rows(ROOT / "watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl")
qled = rows(ROOT / "watch/inbox/qdrop_export/called_shot_ledger.jsonl")

# miss-key = target_date; only verdict-filed rows enter miss entropy
v1_miss = Counter(r["target_date"] for r in v1 if r.get("verdict") == "BROKEN")
v1_stats = entropy(v1_miss)
v1_stats["buckets"] = dict(v1_miss)

verdicts_v2 = Counter(r.get("verdict") for r in v2)
v2_expired, v2_open = 0, 0
v2_expired_targets = Counter()
for r in v2:
    td = r.get("target_date", "")
    if td and td < CUTOFF:
        v2_expired += 1
        v2_expired_targets[td] += 1
    else:
        v2_open += 1

q_expired_targets = Counter(r["target_date"] for r in qled if r["target_date"] < CUTOFF)

prophecy = {
    "surface": "prophecy_called_shot",
    "miss_definition": "verdict-filed BROKEN row in a called-shot ledger; miss-key = target_date (the staked horizon)",
    "sources": [
        "watch/inbox/mrpool_export/called_shot_ledger.jsonl",
        "watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl",
        "watch/inbox/qdrop_export/called_shot_ledger.jsonl",
        "watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json",
    ],
    "pool_v1_misses": v1_stats,
    "pool_v1_verdicts": dict(Counter(r.get("verdict") for r in v1)),
    "pool_v2": {
        "rows": len(v2),
        "verdicts_filed": dict(verdicts_v2),
        "pending_note": "no verdict field filed in this file; pending rows are excluded from miss entropy by design",
        "expired_unverdicted": v2_expired,
        "open_at_cutoff": v2_open,
        "expired_unverdicted_targets_top5": dict(v2_expired_targets.most_common(5)),
        "expired_target_entropy": entropy(v2_expired_targets),
    },
    "q_ledger": {
        "rows": len(qled),
        "targets": dict(Counter(r["target_date"] for r in qled)),
        "expired_unverdicted": sum(q_expired_targets.values()),
        "expired_target_entropy": entropy(q_expired_targets),
    },
}

# ------------------------------------------------------- 2. ops fkb failures
kind_total = Counter()
tool_total = Counter()
provider_total = Counter()
by_month_kind = defaultdict(Counter)
n_fkb = 0
with open(ROOT / "training/events.jsonl", encoding="utf-8") as f:
    for line in f:
        if '"fkb_failure"' not in line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("pattern") != "fkb_failure":
            continue
        n_fkb += 1
        kind = (r.get("input") or {}).get("kind") or "unknown"
        tool = (r.get("action") or {}).get("tool") or "unknown"
        provider = (r.get("action") or {}).get("provider") or "unknown"
        kind_total[kind] += 1
        tool_total[tool] += 1
        provider_total[provider] += 1
        by_month_kind[month_of(r.get("ts"))][kind] += 1

kstats = entropy(kind_total)
kstats["buckets"] = dict(kind_total.most_common(12))
tstats = entropy(tool_total)
tstats["buckets"] = dict(tool_total.most_common(12))
pstats = entropy(provider_total)
pstats["buckets"] = dict(provider_total.most_common(12))
curve = []
for m in sorted(by_month_kind):
    s = entropy(by_month_kind[m])
    curve.append({"month": m, "n": s["n"], "H_bits": s["H_bits"],
                  "H_norm": s["H_norm"], "top1_share": s["top1_share"]})

ops = {
    "surface": "ops_fkb_failures",
    "miss_definition": "fkb_failure event in training/events.jsonl; miss-key = input.kind (secondary keys: action.tool, action.provider)",
    "source": "training/events.jsonl",
    "n_events": n_fkb,
    "by_kind": kstats,
    "by_tool": tstats,
    "by_provider": pstats,
    "monthly_curve": curve,
}

# ---------------------------------------------------------------- 3. jev meter
trail = rows(ROOT / "queue/lanes/jev/trail.jsonl")
miss_events = Counter()
waves_out = []
ever_missed = set()
for tr in trail:
    w = tr.get("wave") or {}
    pk = w.get("packets") or []
    wave_miss = Counter(p["id"] for p in pk if p.get("meter_correct") is False)
    for pid in wave_miss:
        miss_events[pid] += wave_miss[pid]
        ever_missed.add(pid)
    s = entropy(wave_miss)
    waves_out.append({"ts": tr.get("ts"), "n_packets": len(pk),
                      "n_miss": s["n"], "K_missed": s["K"],
                      "H_bits": s["H_bits"], "H_norm": s["H_norm"]})

mstats = entropy(miss_events)
mstats["buckets"] = dict(miss_events)
latest = (trail[-1].get("wave") or {})
jev = {
    "surface": "jev_meter",
    "miss_definition": "packet with meter_correct=false in queue/lanes/jev/trail.jsonl; miss-key = packet id",
    "source": "queue/lanes/jev/trail.jsonl",
    "n_waves": len(trail),
    "n_meter_rows_total": sum(len((tr.get("wave") or {}).get("packets") or []) for tr in trail),
    "miss_events": mstats,
    "unique_packets_ever_missed": len(ever_missed),
    "unique_packets_ever_missed_ids": sorted(ever_missed),
    "per_wave": waves_out,
    "latest_wave": {
        "ts": trail[-1].get("ts"),
        "trigger": latest.get("trigger"),
        "note": "meter_record is idempotent by packet id (standing drive re-fires); re-fires are separate miss events above, deduped view given by unique_packets_ever_missed",
    },
}

# ------------------------------------------------------------------- assemble
doc = {
    "schema": "the50.w6.t28.miss_entropy.v1",
    "filed": "2026-09-25",
    "g13_source": {
        "battery_row": "watch/inbox/GPS_BATTERY_20260918.jsonl:13 (id G13, family cache_os)",
        "gps_answer": "memory/runs/gps_50/GPS_PACK.md:515 (section 'G13 via groq-oss', MISS-ENTROPY DASHBOARD table)",
        "claim": "99 percent prefix cache hit rate is necessary but dangerous: it proves stability but also proves nothing new is being asked. The health metric is not hit rate but the ENTROPY of misses.",
    },
    "cutoff": CUTOFF,
    "panels": {
        "entropy_score": "H = -sum p_i log2 p_i over miss-key buckets; comparable index is H_norm = H / log2(K)",
        "bucket_distribution": "top1_share and top5_share of miss volume",
        "temporal_variance": "per-window H curve (monthly for ops, per wave for jev, single campaign for prophecy v1)",
        "miss_rate_delta": "left to the per-window consumer: delta n between consecutive windows, carried in monthly_curve / per_wave order",
    },
    "series": [prophecy, ops, jev],
    "computed_by": "scripts/the50_w6_t28_miss_entropy.py",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)

# ------------------------------------------------------------------- print
print("filed:", OUT)
p1 = prophecy["pool_v1_misses"]
print("prophecy v1: n=%s K=%s H=%s bits H_norm=%s top1=%s" % (p1["n"], p1["K"], p1["H_bits"], p1["H_norm"], p1["top1_share"]))
print("prophecy v2: rows=%s expired_unverdicted=%s open=%s" % (len(v2), v2_expired, v2_open))
o = ops
print("ops fkb: n=%s by_kind H=%s H_norm=%s top1=%s K=%s" % (o["n_events"], o["by_kind"]["H_bits"], o["by_kind"]["H_norm"], o["by_kind"]["top1_share"], o["by_kind"]["K"]))
print("ops by_tool: H=%s H_norm=%s K=%s ; by_provider: H=%s H_norm=%s K=%s" % (
    o["by_tool"]["H_bits"], o["by_tool"]["H_norm"], o["by_tool"]["K"],
    o["by_provider"]["H_bits"], o["by_provider"]["H_norm"], o["by_provider"]["K"]))
print("ops months:", len(curve), "first:", curve[0] if curve else None, "last:", curve[-1] if curve else None)
j = jev
print("jev: waves=%s miss_events n=%s K=%s H=%s H_norm=%s ever_missed=%s" % (
    j["n_waves"], mstats["n"], mstats["K"], mstats["H_bits"], mstats["H_norm"], j["unique_packets_ever_missed"]))
print("jev latest trigger:", latest.get("trigger"))
