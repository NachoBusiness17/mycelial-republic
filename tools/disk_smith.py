#!/usr/bin/env python3
"""disk_smith: the Smith chart of the HDD (disk-crisis-20261008).

Operator order 2026-10-08: "we really should have a fucking smith chart of
the hdd" - five agent seats (zcode, opencode, grok headless, hermes, codex)
write one disk and nobody could say what grew. The founding 1.3TB-in-36h
incident (receipt watch/inbox/DISK_INVENTORY_20261008.md) had pagefile.sys
balloon to 132.9GB under fleet memory pressure, docker_data.vhdx reach
132GB with ~90GB never-compacted dead space, and no instrument attributing
any of it.

What it does (appends one JSONL row per run; the snap path is read-only):
  - snap: sizes of named system monsters (pagefile, hiberfil, every *.vhdx),
    agent homes, estate buckets, plus free space on the repo volume
  - delta: versus the previous snap row - who grew, who shrank (GB)
  - alert: free-below-floor or any monster growing past its cap appends
    memory/attention.md and exit 1, same shape as the longrunner patrol
  - prune: L2 retention sweep of the exec-forest class roots - files past
    max_age_days (default 7) hit the kill list; DRY-RUN by default,
    --apply deletes; receipts go to the sibling ledger
    logs/disk_smith_prune.jsonl (the snap delta reads the last snap row;
    LAW_PACK law L2, watch/inbox/disk_audit_20261009/).

Usage:
  python -m tools.disk_smith                 # snap + delta + alert, append row
  python -m tools.disk_smith --dry           # print, no append, no alert
  python -m tools.disk_smith --history 10    # print last N rows flat
  python -m tools.disk_smith --prune [--apply]  # L2 retention sweep

Exit: 0 clean / 1 alert / 2 usage (a refused prune contract is usage).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "logs" / "disk_smith.jsonl"
ALERT = ROOT / "memory" / "attention.md"

# Named monsters: label -> path (absolute or ROOT-relative). Sizes in GB.
SYSTEM_MONSTERS = {
    "pagefile": "C:/pagefile.sys",
    "hiberfil": "C:/hiberfil.sys",
    "docker_data_vhdx": "C:/Users/foste/AppData/Local/Docker/wsl/disk/docker_data.vhdx",
    "wsl_ext4": "C:/Users/foste/AppData/Local/wsl",
    "appdata_temp": "C:/Users/foste/AppData/Local/Temp",
}

# Per-seat write attribution: agent homes the operator named.
AGENT_HOMES = {
    "zcode_cache": "C:/Users/foste/.zcode",
    "codex": "C:/Users/foste/.codex",
    "grok": "C:/Users/foste/.grok",
    "openclaw": "C:/Users/foste/.openclaw",
    "opencode_cache": "C:/Users/foste/.cache/opencode",
    "hermes_local": "C:/Users/foste/AppData/Local/hermes",
    "ollama_garden": "C:/Users/foste/.ollama/models",
    "hf_cache": "C:/Users/foste/.cache/huggingface",
}

ESTATE_BUCKETS = {
    "repo_logs": "logs",
    "repo_watch_inbox": "watch/inbox",
    "repo_corpus": "corpus",
    "repo_dashboard_data": "dashboard/data",
    "repo_memory": "memory",
}

# L2 retention class roots (LAW_PACK law L2): the exec-forest class, the
# harness tool-call exhaust dirs. Config, not code (the L8 dot-dir shape).
PRUNE_ROOTS = {
    "zcode_exec": "C:/Users/foste/.zcode/cli/exec",
}
# Sibling ledger for prune receipts, NOT the snap ledger: the snap delta
# reads the last snap row, so a prune row there would blank its math.
PRUNE_LEDGER = ROOT / "logs" / "disk_smith_prune.jsonl"
# Four-field retention contract (Gemini CLI card 1.4 shape, ours 7d): min_age
# protects the live window; max_count lands with the lifecycle rows (L5).
RETENTION = {
    "enabled": True,
    "max_age_days": 7.0,
    "min_age_days": 1.0,
    "max_count": None,
}

DAY_SECONDS = 86400.0

GB = 2**30
DEFAULT_FLOOR_GB = 15.0
# vhdx dead-space cap: founding incident read 132GB vhdx against ~40GB live
# docker data; anything past this means compact is owed.
VHDX_WARN_GB = 100.0


def _size_gb(path: Path) -> float | None:
    try:
        if path.is_file():
            return path.stat().st_size / GB
        if path.is_dir():
            total = 0
            for p in path.rglob("*"):
                try:
                    if p.is_file():
                        total += p.stat().st_size
                except OSError:
                    continue
            return total / GB
    except OSError:
        return None
    return None


def _row_gb(path: Path) -> float | None:
    # Fix 2026-10-09 (disk_audit_20261009, L8 lock wave): snap() used to
    # compute round(_size_gb(p), 2), which crashes with "type NoneType
    # doesn't define __round__ method" when a path exists but stat or the
    # walk raises OSError (locked system paths; AppData Temp subdirs under
    # live use) - _size_gb legitimately returns None there. An unmeasurable
    # row is a None row, never a dead sweep: a smith that crashes mid-loop
    # goes blind on every seat L8 made first-class. Evidence: combined run
    # 2026-10-09 tests/test_disk_smith.py::test_snap_shape_live TypeError;
    # locked by tests/test_disk_smith_dotdir_lock.py
    # test_snap_records_none_row_for_unmeasurable_path.
    size = _size_gb(path)
    return round(size, 2) if size is not None else None


def snap(now: datetime) -> dict:
    """One Smith-chart sweep: monsters, seats, estate buckets, free space."""
    import shutil

    row: dict = {
        "ts": now.isoformat().replace("+00:00", "Z"),
        "monsters": {},
        "seats": {},
        "estate": {},
    }
    for label, raw in SYSTEM_MONSTERS.items():
        p = Path(raw)
        row["monsters"][label] = _row_gb(p) if p.exists() else None
    for label, raw in AGENT_HOMES.items():
        p = Path(raw)
        row["seats"][label] = _row_gb(p) if p.exists() else None
    for label, rel in ESTATE_BUCKETS.items():
        p = ROOT / rel
        row["estate"][label] = _row_gb(p) if p.exists() else None
    usage = shutil.disk_usage(ROOT)
    row["free_gb"] = round(usage.free / GB, 1)
    row["total_gb"] = round(usage.total / GB, 1)
    return row


def delta(curr: dict, prev: dict | None) -> dict:
    """Per-section GB deltas versus the previous snap (curr - prev)."""
    if not prev:
        return {}
    out: dict = {}
    for section in ("monsters", "seats", "estate"):
        d = {}
        for key, val in curr.get(section, {}).items():
            old = prev.get(section, {}).get(key)
            if val is not None and old is not None:
                chg = round(val - old, 2)
                if abs(chg) >= 0.01:
                    d[key] = chg
        if d:
            out[section] = d
    if curr.get("free_gb") is not None and prev.get("free_gb") is not None:
        out["free_gb"] = round(curr["free_gb"] - prev["free_gb"], 1)
    return out


def alerts(curr: dict, floor_gb: float, proj: dict | None = None) -> list[str]:
    """Rule alerts: free-below-floor, vhdx bloat, pagefile balloon, ETA warning."""
    found: list[str] = []
    free = curr.get("free_gb")
    if free is not None and free < floor_gb:
        found.append(
            f"DISK FLOOR: {free}GB free of {curr.get('total_gb')}GB, "
            f"floor {floor_gb}GB - relief playbook: docker builder prune, "
            "ollama rotation with modelfile receipts, cold-artifact offload, "
            "never delete live ledgers (watch/inbox/DISK_INVENTORY_20261008.md)"
        )
    if proj and proj.get("eta_days") is not None and proj["eta_days"] < 14:
        found.append(
            f"DISK ETA: at the median recent burn ({proj['median_daily_delta_gb']}GB/day "
            f"over {proj['n_rows']} snaps, {proj['span_hours']}h span) the floor lands in "
            f"~{proj['eta_days']} days - act inside that window, not at the floor "
            "(smith v1.1 projection; unstable if class says so)"
        )
    vhdx = curr.get("monsters", {}).get("docker_data_vhdx")
    if vhdx is not None and vhdx > VHDX_WARN_GB:
        found.append(
            f"VHDX BLOAT: docker_data.vhdx at {vhdx}GB (warn {VHDX_WARN_GB}GB) "
            "- WSL2 never auto-compacts; compact is owed: quit Docker "
            "Desktop, wsl --shutdown, Optimize-VHD -Mode Full (admin)"
        )
    page = curr.get("monsters", {}).get("pagefile")
    if page is not None and page > 40.0:
        found.append(
            f"PAGEFILE BALLOON: pagefile.sys at {page}GB - system-managed "
            "pagefile grew under fleet memory pressure; a reboot returns it; "
            "fixed-size pagefile ends the class"
        )
    return found


def safe_child(dirpath: Path, name: str, allowroot: Path):
    """The single sanctioned join (harvest_exec_forest.py pattern): reject
    empty/dot/dotdot or separator-bearing names; resolve inside allowroot."""
    if name in ("", ".", "..") or "/" in name or "\\" in name:
        return None
    p = dirpath / name
    try:
        if not p.resolve().is_relative_to(allowroot.resolve()):
            return None
    except OSError:
        return None
    return p


def safe_dir(dirpath: Path, allowroot: Path) -> bool:
    try:
        return dirpath.resolve().is_relative_to(allowroot.resolve())
    except OSError:
        return False


def prune_plan(roots: dict, max_age_days: float, now: float) -> dict:
    """Guarded metadata-only walk of the retention roots: files past
    max_age_days hit the kill list, younger ones stay; the contract keeps
    max_age >= min_age so no kill is younger than min_age (L2 falsifier)."""
    out: dict = {}
    for label, raw in roots.items():
        root = Path(raw)
        row = {"root": raw, "scanned": 0, "kill_files": 0,
               "kill_bytes": 0, "errors": 0, "kill": []}
        if root.is_dir():
            for dirpath, _dirnames, filenames in os.walk(root):
                dpath = Path(dirpath)
                if not safe_dir(dpath, root):
                    continue
                for fn in filenames:
                    row["scanned"] += 1
                    p = safe_child(dpath, fn, root)
                    if p is None:
                        row["errors"] += 1
                        continue
                    try:
                        st = p.stat()
                    except OSError:
                        row["errors"] += 1
                        continue
                    age_days = (now - st.st_mtime) / DAY_SECONDS
                    if age_days > max_age_days:
                        row["kill"].append({"path": str(p),
                                            "bytes": st.st_size,
                                            "age_days": round(age_days, 2)})
                        row["kill_files"] += 1
                        row["kill_bytes"] += st.st_size
        out[label] = row
    return out


def prune(roots: dict, max_age_days: float, min_age_days: float,
          apply: bool, ledger: Path | None = None,
          now: float | None = None) -> int:
    """L2 retention sweep: dry-run by default (kill list + totals printed,
    nothing deleted or written); apply deletes exactly the aged set, counts
    locked-file failures non-fatally, banks one receipt row; ledger resolves
    from PRUNE_LEDGER at call time so config redirects hold."""
    if ledger is None:
        ledger = PRUNE_LEDGER
    if not RETENTION.get("enabled"):
        print("retention disabled in the L2 contract; refusing to sweep")
        return 2
    if max_age_days <= 0 or max_age_days < min_age_days:
        print(f"retention contract refuses max_age_days={max_age_days} "
              f"against min_age_days={min_age_days} (0 or sub-min_age "
              "refused; min_age protects the live window)", file=sys.stderr)
        return 2
    if now is None:
        now = time.time()
    plan = prune_plan(roots, max_age_days, now)
    tot_files = sum(r["kill_files"] for r in plan.values())
    tot_bytes = sum(r["kill_bytes"] for r in plan.values())
    print(f"prune contract: max_age_days={max_age_days} min_age_days={min_age_days}")
    for label, r in plan.items():
        print(f"{label}: scanned {r['scanned']} errors {r['errors']} "
              f"kill {r['kill_files']} files {r['kill_bytes'] / GB:.2f}GiB")
        for item in sorted(r["kill"], key=lambda k: -k["bytes"]):
            print(f"  {item['bytes'] / GB:8.4f}GiB {item['age_days']:7.2f}d "
                  f"{Path(item['path']).name[:70]}")
    print(f"TOTAL: {tot_files} files {tot_bytes / GB:.2f}GiB past {max_age_days}d")
    if not apply:
        print("DRY RUN - nothing deleted. Re-run with --apply.")
        return 0
    deleted = failed = freed = 0
    fail_list = []
    for r in plan.values():
        root = Path(r["root"])
        for item in r["kill"]:
            # guard adjacent to the access: re-derive the join at delete time
            p = Path(item["path"])
            q = safe_child(p.parent, p.name, root) if safe_dir(p.parent, root) else None
            if q is None or str(q) != item["path"]:
                failed += 1
                fail_list.append(item["path"])
                continue
            try:
                os.remove(q)
                deleted += 1
                freed += item["bytes"]
            except OSError:
                failed += 1
                fail_list.append(item["path"])
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    row = {"ts": ts, "kind": "prune", "mode": "apply",
           "max_age_days": max_age_days, "min_age_days": min_age_days,
           "roots": {label: {k: r[k] for k in ("root", "scanned", "kill_files",
                                               "kill_bytes", "errors")}
                     for label, r in plan.items()},
           "deleted": deleted, "freed_bytes": freed, "failed": failed,
           "fail_list": fail_list[:50]}
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with open(ledger, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"APPLIED: deleted {deleted} freed {freed / GB:.2f}GiB failed {failed}")
    print("receipt:", ledger)
    return 0


def load_rows(limit: int = 8) -> list[dict]:
    """Last N ledger rows (oldest first). Malformed tail lines are skipped."""
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").strip().splitlines()[-limit:]:
        try:
            row = json.loads(line)
            if row.get("free_gb") is not None and row.get("ts"):
                rows.append(row)
        except json.JSONDecodeError:
            continue
    return rows


def projection(rows: list[dict], floor_gb: float) -> dict:
    """Free-space burn projection (smith v1.1: the chart that does useful stuff).

    Median of pairwise daily rates, honest about instability: when the
    interquartile spread of rates exceeds the median's magnitude the trend is
    classed unstable and no ETA is offered - a projection that hides its
    variance is a fabrication with a decimal point."""
    if len(rows) < 3:
        return {"n_rows": len(rows), "eta_days": None, "eta_class": "insufficient-history"}

    def ts_hours(r: dict) -> float:
        t = datetime.fromisoformat(r["ts"].replace("Z", "+00:00"))
        return t.timestamp() / 3600.0

    rates = []
    for i in range(len(rows) - 1):
        for j in range(i + 1, len(rows)):
            dh = ts_hours(rows[j]) - ts_hours(rows[i])
            if dh < 0.25:
                continue
            rates.append((rows[i]["free_gb"] - rows[j]["free_gb"]) / (dh / 24.0))
    if not rates:
        return {"n_rows": len(rows), "eta_days": None, "eta_class": "insufficient-history"}
    rates.sort()
    n = len(rates)
    median = rates[n // 2] if n % 2 else (rates[n // 2 - 1] + rates[n // 2]) / 2
    q1 = rates[max(0, n // 4)]
    q3 = rates[min(n - 1, 3 * n // 4)]
    span_hours = ts_hours(rows[-1]) - ts_hours(rows[0])
    out = {
        "n_rows": len(rows),
        "span_hours": round(span_hours, 1),
        "median_daily_delta_gb": round(median, 2),
        "iqr_daily_delta_gb": round(q3 - q1, 2),
    }
    if (q3 - q1) > max(abs(median), 1.0):
        out["eta_days"] = None
        out["eta_class"] = "unstable"
        return out
    if median <= 0:
        out["eta_days"] = None
        out["eta_class"] = "no-net-burn" if median >= 0 else "gaining-space"
        return out
    free_now = rows[-1]["free_gb"]
    out["eta_days"] = round((free_now - floor_gb) / median, 1)
    out["eta_class"] = "trending"
    return out


def top_movers(chg: dict) -> list[tuple[str, float]]:
    """Top |GB| movers across all delta sections, biggest first."""
    flat: list[tuple[str, float]] = []
    for section, d in chg.items():
        if section == "free_gb" or not isinstance(d, dict):
            continue
        for key, val in d.items():
            flat.append((f"{section}.{key}", val))
    flat.sort(key=lambda kv: abs(kv[1]), reverse=True)
    return flat[:3]


def main() -> int:
    ap = argparse.ArgumentParser(description="Smith chart of the HDD")
    ap.add_argument("--dry", action="store_true", help="print, no append/alert")
    ap.add_argument("--floor-gb", type=float, default=DEFAULT_FLOOR_GB)
    ap.add_argument("--history", type=int, default=0,
                    help="print last N ledger rows and exit")
    ap.add_argument("--prune", action="store_true",
                    help="L2 retention sweep of the exec-forest roots, dry-run")
    ap.add_argument("--apply", action="store_true",
                    help="with --prune: execute the kill list")
    ap.add_argument("--max-age-days", type=float, default=RETENTION["max_age_days"],
                    help="retention age for --prune (default 7)")
    args = ap.parse_args()

    if args.apply and not args.prune:
        ap.error("--apply only pairs with --prune")  # exits 2
    if args.prune:
        return prune(PRUNE_ROOTS, args.max_age_days,
                     RETENTION["min_age_days"], apply=args.apply)

    if args.history:
        if not LEDGER.exists():
            print("no ledger yet")
            return 0
        rows = LEDGER.read_text(encoding="utf-8").strip().splitlines()
        for line in rows[-args.history:]:
            print(line)
        return 0

    now = datetime.now(timezone.utc)
    curr = snap(now)

    prev = None
    if LEDGER.exists():
        lines = LEDGER.read_text(encoding="utf-8").strip().splitlines()
        if lines:
            try:
                prev = json.loads(lines[-1])
            except json.JSONDecodeError:
                prev = None
    chg = delta(curr, prev)
    curr["delta"] = chg

    proj = projection(load_rows(), args.floor_gb)
    curr["projection"] = proj
    movers = top_movers(chg)
    curr["top_movers"] = [[k, v] for k, v in movers]

    print(json.dumps(curr, ensure_ascii=False))
    if chg:
        print("delta vs previous snap:")
        print(json.dumps(chg, indent=2, ensure_ascii=False))
    if proj.get("eta_class") == "trending":
        print(f"PROJECTION: median burn {proj['median_daily_delta_gb']}GB/day "
              f"(IQR {proj['iqr_daily_delta_gb']}, {proj['n_rows']} snaps / "
              f"{proj['span_hours']}h) - floor in ~{proj['eta_days']} days")
    elif proj.get("eta_class") not in (None, "insufficient-history"):
        print(f"PROJECTION: {proj['eta_class']} (median "
              f"{proj.get('median_daily_delta_gb', 'n/a')}GB/day) - no ETA offered")
    if movers:
        print("top movers vs previous snap:")
        for k, v in movers:
            print(f"  {k}: {'+' if v > 0 else ''}{v} GB")

    fired = alerts(curr, args.floor_gb, proj)
    if fired:
        for a in fired:
            print("ALERT: " + a)
        if not args.dry:
            ALERT.parent.mkdir(parents=True, exist_ok=True)
            stamp = curr["ts"]
            with open(ALERT, "a", encoding="utf-8") as fh:
                for a in fired:
                    fh.write(f"- {stamp} DISK_SMITH {a}\n")

    if not args.dry:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(curr, ensure_ascii=False) + "\n")

    return 1 if fired else 0


if __name__ == "__main__":
    sys.exit(main())
