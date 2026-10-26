"""estate_smith v1 - the Smith chart of the Turing-castle water computer.

One row appended to estate_smith.jsonl per run. Six blocks:
STORAGE (disk + last disk_smith row), PRESSURE (RAM/pagefile, allocated vs
used), COMPUTE (per-exe CPU-seconds stock + RSS + counts), FLOW (events +
burn-ledger rows last 24h), LOSS (zcode_cache delta between smith rows),
RESONANCE (rates from the prior estate_smith row).

Single process, psutil + tiny tails only, NO disk walks (one-disk-process
bound). Receipt-space v1; promotion path in SPEC.md.
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import psutil

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
LEDGER = ROOT / "watch" / "inbox" / "smith_chart_estate_20260109" / "estate_smith.jsonl"
DISK_SMITH = ROOT / "logs" / "disk_smith.jsonl"
EVENTS = ROOT / "training" / "events.jsonl"
BURN_LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
ALERT_RAM_AVAIL_GB = 8.0
ALERT_FREE_GB = 15.0
ALERT_PAGEFILE_FILE_GB = 40.0
SEAT_BUCKETS = ("python", "ollama", "docker", "node", "git", "codex", "grok", "claude", "java")

def tail_json(path: Path, n=1):
    try:
        lines = path.read_text(errors="replace").strip().splitlines()
        return [json.loads(x) for x in lines[-n:] if x.strip()]
    except Exception:
        return []

def count_rows_last_24h(path: Path):
    """Count jsonl rows whose ts field is within 24h. Reads tail-bounded."""
    try:
        if not path.exists():
            return None
        size = path.stat().st_size
        with open(path, "rb") as f:
            if size > 2_000_000:
                f.seek(-2_000_000, 2)
                f.readline()  # skip partial line
            chunk = f.read().decode("utf-8", "replace")
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        n = 0
        for line in chunk.splitlines():
            if not line.strip():
                continue
            try:
                ts = json.loads(line).get("ts")
                if ts and datetime.fromisoformat(str(ts).replace("Z", "+00:00")) > cutoff:
                    n += 1
            except Exception:
                continue
        return n
    except Exception:
        return None

def main():
    now = datetime.now(timezone.utc)
    row = {"ts": now.isoformat()}
    alerts = []

    # STORAGE
    du = psutil.disk_usage("C:\\")
    smith_rows = tail_json(DISK_SMITH, 2)
    row["storage"] = {
        "free_gb": round(du.free / 2**30, 1),
        "total_gb": round(du.total / 2**30, 1),
        "used_pct": round(100 * du.used / du.total, 1),
        "disk_smith_rows": len(smith_rows),
        "last_smith_free": smith_rows[-1].get("free_gb") if smith_rows else None,
    }
    if row["storage"]["free_gb"] < ALERT_FREE_GB:
        alerts.append(f"FREE FLOOR: {row['storage']['free_gb']}GB < {ALERT_FREE_GB}GB")

    # PRESSURE
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    row["pressure"] = {
        "ram_total_gb": round(vm.total / 2**30, 1),
        "ram_avail_gb": round(vm.available / 2**30, 1),
        "ram_used_pct": vm.percent,
        "pagefile_alloc_gb": round(sm.total / 2**30, 1),
        "pagefile_used_gb": round(sm.used / 2**30, 1),
        "balloon_note": "allocated-vs-used gap IS the balloon gauge",
    }
    if row["pressure"]["ram_avail_gb"] < ALERT_RAM_AVAIL_GB:
        alerts.append(f"RAM PRESSURE: avail {row['pressure']['ram_avail_gb']}GB < {ALERT_RAM_AVAIL_GB}GB")
    if smith_rows and smith_rows[-1].get("monsters", {}).get("pagefile", 0) > ALERT_PAGEFILE_FILE_GB:
        alerts.append(f"PAGEFILE FILE BALLOON: {smith_rows[-1]['monsters']['pagefile']}GB > {ALERT_PAGEFILE_FILE_GB}GB")

    # COMPUTE (instantaneous stock: per-bucket CPU-seconds + RSS)
    cpu_buckets = {}
    top = []
    for p in psutil.process_iter(["name", "cpu_times", "memory_info"]):
        try:
            ni = p.info
            name = (ni["name"] or "?").lower()
            if name.endswith(".exe"):
                name = name[:-4]
            cpu = sum(ni["cpu_times"] or ()) if ni["cpu_times"] else 0.0
            rss = (ni["memory_info"].rss if ni["memory_info"] else 0) / 2**30
            bucket = next((b for b in SEAT_BUCKETS if b in name), "other")
            b = cpu_buckets.setdefault(bucket, {"procs": 0, "cpu_seconds": 0.0, "rss_gb": 0.0})
            b["procs"] += 1
            b["cpu_seconds"] += cpu
            b["rss_gb"] += rss
            top.append((rss, name, p.pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    row["compute"] = {
        "buckets": {k: {"procs": v["procs"], "cpu_hours": round(v["cpu_seconds"] / 3600, 1),
                        "rss_gb": round(v["rss_gb"], 1)}
                    for k, v in sorted(cpu_buckets.items(), key=lambda kv: -kv[1]["cpu_seconds"])},
        "top_rss_procs": [{"gb": round(r, 2), "name": n, "pid": pid} for r, n, pid in sorted(top, reverse=True)[:5]],
    }

    # FLOW (last 24h)
    row["flow"] = {
        "events_24h": count_rows_last_24h(EVENTS),
        "burn_ledger_rows_24h": count_rows_last_24h(BURN_LEDGER),
    }

    # LOSS (disk-flow from smith rows)
    loss = None
    if len(smith_rows) >= 2:
        try:
            a, b = smith_rows[-2], smith_rows[-1]
            za = a.get("seats", {}).get("zcode_cache")
            zb = b.get("seats", {}).get("zcode_cache")
            if za is not None and zb is not None:
                loss = {"zcode_delta_gb": round(zb - za, 2),
                        "window": f"{a.get('ts','?')} -> {b.get('ts','?')}"}
        except Exception:
            pass
    row["loss"] = loss

    # RESONANCE (rates vs prior estate_smith row)
    prior = tail_json(LEDGER, 1)
    res = {"rows_before": len(prior)}
    if prior:
        try:
            p0 = prior[0]
            dt_h = max(0.001, (now - datetime.fromisoformat(p0["ts"])).total_seconds() / 3600)
            res["gb_filled_per_h"] = round((row["storage"]["free_gb"] - p0["storage"]["free_gb"]) * -1 / dt_h, 2)
        except Exception:
            pass
    row["resonance"] = res

    row["alerts"] = alerts
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")

    print(json.dumps(row, indent=1))
    for a in alerts:
        print("ALERT:", a)

if __name__ == "__main__":
    main()
