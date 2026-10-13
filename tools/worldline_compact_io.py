"""worldline_compact_io - scan, report, plan bytes for tools/worldline_compact.py.

Split law (same bar as census_drift_patrol's B2-248/B2-365 splits, 2026-09-26):
the parent tool stayed under the ratchet's 400-line cap by moving the pure
byte-layer - inventory scan, slab keying, dedupe metric, report/table render,
plan build/render/parse - into this sibling. One-way import: the parent imports
this module; this module imports nothing from the parent. The laws + operator
gate contract live in the parent's docstring (tools/worldline_compact.py).

Everything here is READ-ONLY over memory/worldline except render_plan_md (it
only returns a string; the parent decides where it lands).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from collections import defaultdict
from pathlib import Path

DWF_PREFIX = "dwf-"
ARCHIVE_NAME = "_compact_archive"
JSON_BEGIN = "WORLDLINE-COMPACT-JSON-BEGIN"
JSON_END = "WORLDLINE-COMPACT-JSON-END"
PLAN_VERSION = 1
CRITERION = ("canonical JSON bytes of genome+invariants slabs hash-equal to the "
             "newest dwf seed of the same created_utc minute (tie-break session_id)")
AGE_BUCKETS = ("<1d", "1-7d", "7-30d", ">30d")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slab_key(doc: dict) -> str | None:
    """sha256 over canonical genome + invariants slab bytes, or None when unkeyable."""
    slabs = doc.get("slabs")
    if not isinstance(slabs, dict):
        return None
    try:
        g = json.dumps(slabs["genome"], sort_keys=True, separators=(",", ":")).encode("utf-8")
        i = json.dumps(slabs["invariants"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (KeyError, TypeError, ValueError):
        return None
    return hashlib.sha256(g + b"\x00" + i).hexdigest()


def read_seed(path: Path) -> dict | None:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return doc if isinstance(doc, dict) else None


def _run_of(dir_name: str, prefix: str) -> str | None:
    """dwfrun id for dwf-dwfrun-<uuid>-actor_N_M dirs; None for seat seeds."""
    if prefix != "dwf" or not dir_name.startswith("dwf-dwfrun-"):
        return None
    parts = dir_name.split("-")
    return parts[2] if len(parts) > 3 else dir_name


def scan(worldline: Path) -> dict:
    """Read-only inventory of top-level seed dirs. Never raises on bad seeds."""
    seeds: list[dict] = []
    other_files: list[dict] = []
    errors: list[str] = []
    if not worldline.is_dir():
        return {"seeds": [], "other_files": [], "errors": [f"worldline dir missing: {worldline}"]}
    for p in sorted(worldline.iterdir()):
        if p.name == ARCHIVE_NAME:
            continue  # cold storage, never inventory material
        if not p.is_dir():
            try:
                other_files.append({"name": p.name, "bytes": p.stat().st_size})
            except OSError as exc:
                errors.append(f"unstattable file {p.name}: {exc}")
            continue
        sj = p / "SEED.json"
        if not sj.is_file():
            errors.append(f"seed dir without SEED.json: {p.name}")
            continue
        doc = read_seed(sj)
        if doc is None:
            errors.append(f"unreadable SEED.json {p.name}")
            continue
        prefix = "dwf" if p.name.startswith(DWF_PREFIX) else "seat"
        created = str(doc.get("created_utc") or "")
        seeds.append({
            "dir_name": p.name,
            "session_id": str(doc.get("session_id") or p.name),
            "prefix": prefix,
            "created_utc": created,
            "minute": created[:16],
            "bytes": sj.stat().st_size,
            "slab_key": slab_key(doc),
            "seed_hash": str(doc.get("seed_hash") or ""),
            "run": _run_of(p.name, prefix),
        })
    return {"seeds": seeds, "other_files": other_files, "errors": errors}


def age_bucket(created_utc: str, now: dt.datetime) -> str:
    try:
        t = dt.datetime.fromisoformat(created_utc.replace("Z", "+00:00"))
    except ValueError:
        return "unparseable"
    days = (now - t).total_seconds() / 86400.0
    for edge, label in ((1, "<1d"), (7, "1-7d"), (30, "7-30d")):
        if days < edge:
            return label
    return ">30d"


def minute_buckets(dwf: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for s in dwf:
        buckets[s["minute"]].append(s)
    return buckets


def dedupe_potential(dwf: list[dict]) -> dict:
    """The --check metric: identical to the newest seed of the same minute."""
    buckets = minute_buckets(dwf)
    compactable = compactable_bytes = keepers = multi = 0
    dwf_bytes = sum(s["bytes"] for s in dwf)
    for items in buckets.values():
        keyed = [s for s in items if s["slab_key"]]
        newest = max(keyed or items, key=lambda s: (s["created_utc"], s["session_id"]))
        if len({s["slab_key"] for s in keyed}) > 1:
            multi += 1
        same = [s for s in keyed if s["slab_key"] == newest["slab_key"]]
        compactable += len(same) - 1
        compactable_bytes += sum(s["bytes"] for s in same if s["dir_name"] != newest["dir_name"])
        keepers += 1
    sizes = sorted(len(v) for v in buckets.values())
    return {
        "criterion": CRITERION,
        "dwf_seeds": len(dwf),
        "dwf_bytes": dwf_bytes,
        "compactable_seeds": compactable,
        "compactable_bytes": compactable_bytes,
        "keepers": keepers,
        "multi_variant_minutes": multi,
        "unkeyed_dwf_seeds": sum(1 for s in dwf if not s["slab_key"]),
        "pct_seeds": round(100.0 * compactable / len(dwf), 1) if dwf else 0.0,
        "pct_bytes": round(100.0 * compactable_bytes / dwf_bytes, 1) if dwf else 0.0,
        "minute_buckets": len(buckets),
        "median_bucket": sizes[len(sizes) // 2] if sizes else 0,
        "max_bucket": sizes[-1] if sizes else 0,
    }


def build_report(worldline: Path) -> dict:
    result = scan(worldline)
    seeds = result["seeds"]
    now = dt.datetime.now(dt.timezone.utc)
    prefixes: dict[str, dict] = {}
    for name in ("dwf", "seat"):
        rows = [s for s in seeds if s["prefix"] == name]
        ages = {b: 0 for b in AGE_BUCKETS}
        ages["unparseable"] = 0
        for s in rows:
            ages[age_bucket(s["created_utc"], now)] += 1
        prefixes[name] = {
            "count": len(rows),
            "bytes": sum(s["bytes"] for s in rows),
            "runs": len({s["run"] for s in rows if s["run"]}),
            "oldest": min((s["created_utc"] for s in rows), default=""),
            "newest": max((s["created_utc"] for s in rows), default=""),
            "age_buckets": ages,
        }
    return {
        "tool": "worldline_compact",
        "mode": "check",
        "moment_utc": now_iso(),
        "root": worldline.resolve().as_posix(),
        "criterion": CRITERION,
        "totals": {"seed_dirs": len(seeds), "bytes": sum(s["bytes"] for s in seeds)},
        "prefixes": prefixes,
        "dedupe": dedupe_potential([s for s in seeds if s["prefix"] == "dwf"]),
        "other_files": result["other_files"],
        "scan_errors": result["errors"],
    }


def render_table(r: dict) -> str:
    lines = [f"WORLDLINE-COMPACT CHECK  moment={r['moment_utc']}  root={r['root']}",
             f"{'prefix':7}{'seeds':>6}{'bytes':>12}{'runs':>6}  {'oldest':>20}  {'newest':>20}"]
    for name in ("dwf", "seat"):
        p = r["prefixes"][name]
        runs = str(p["runs"]) if name == "dwf" else "-"
        lines.append(f"{name:7}{p['count']:>6}{p['bytes'] / 1e6:>10.2f}MB{runs:>6}"
                     f"  {p['oldest'] or '-':>20}  {p['newest'] or '-':>20}")
    t = r["totals"]
    lines.append(f"{'total':7}{t['seed_dirs']:>6}{t['bytes'] / 1e6:>10.2f}MB")
    for name in ("dwf", "seat"):
        ages = r["prefixes"][name]["age_buckets"]
        lines.append(f"age buckets {name}: " + " | ".join(f"{k} {v}" for k, v in ages.items()))
    d = r["dedupe"]
    lines.append(f"dwf minute buckets: {d['minute_buckets']} (median {d['median_bucket']} seeds/min, max {d['max_bucket']})")
    lines.append(f"dedupe potential: {d['compactable_seeds']}/{d['dwf_seeds']} dwf seeds ({d['pct_seeds']}%) "
                 f"identical genome+invariants to their minute's newest")
    lines.append(f"  compactable bytes: {d['compactable_bytes'] / 1e6:.2f}MB of {d['dwf_bytes'] / 1e6:.2f}MB dwf bytes "
                 f"({d['pct_bytes']}%); keepers: {d['keepers']}; multi-variant minutes: {d['multi_variant_minutes']}; "
                 f"unkeyed: {d['unkeyed_dwf_seeds']}")
    if r["other_files"]:
        lines.append("other files (inventoried, never touched): "
                     + ", ".join(f"{o['name']} ({o['bytes']}B)" for o in r["other_files"]))
    if r["scan_errors"]:
        lines.append("scan errors: " + "; ".join(r["scan_errors"][:5]))
    return "\n".join(lines)


def build_plan(worldline: Path) -> dict:
    """Lineage groups: per minute, per identical-slab cluster (>=2 seeds), keeper = newest."""
    result = scan(worldline)
    dwf = [s for s in result["seeds"] if s["prefix"] == "dwf" and s["slab_key"]]
    groups: list[dict] = []
    buckets = minute_buckets(dwf)
    for minute in sorted(buckets):
        clusters: dict[str, list[dict]] = defaultdict(list)
        for s in buckets[minute]:
            clusters[s["slab_key"]].append(s)
        for key in sorted(clusters):
            pool = clusters[key]
            if len(pool) < 2:
                continue  # a singleton is its own keeper; nothing to compact
            keeper = max(pool, key=lambda s: (s["created_utc"], s["session_id"]))
            members = sorted((s for s in pool if s["dir_name"] != keeper["dir_name"]),
                             key=lambda s: s["dir_name"])
            sj_sha = {s["dir_name"]: file_sha256(worldline / s["dir_name"] / "SEED.json") for s in pool}
            groups.append({
                "minute": minute,
                "slab_key": key,
                "keeper": {"dir_name": keeper["dir_name"], "session_id": keeper["session_id"],
                           "seed_sha256": sj_sha[keeper["dir_name"]], "bytes": keeper["bytes"]},
                "members": [{"dir_name": s["dir_name"], "session_id": s["session_id"],
                             "seed_sha256": sj_sha[s["dir_name"]], "seed_hash": s["seed_hash"],
                             "bytes": s["bytes"]} for s in members],
            })
    return {"plan_version": PLAN_VERSION, "tool": "worldline_compact", "generated_utc": now_iso(),
            "stamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"),
            "worldline_dir": worldline.resolve().as_posix(), "criterion": CRITERION,
            "groups": groups, "scan_errors": result["errors"]}


def render_plan_md(plan: dict) -> str:
    n_members = sum(len(g["members"]) for g in plan["groups"])
    b_members = sum(m["bytes"] for g in plan["groups"] for m in g["members"])
    lines = [
        f"# WORLDLINE COMPACTION PLAN {plan['stamp']}",
        "",
        f"Generated: {plan['generated_utc']} by `tools/worldline_compact.py --plan` (read-only over the seeds).",
        f"Root: `{plan['worldline_dir']}`",
        f"Criterion: {plan['criterion']}.",
        "",
        "## Law block (read before GO)",
        "",
        "- Producing this file touched NOTHING in memory/worldline.",
        "- Executing requires operator GO: env `WORLDLINE_COMPACT_GO=1` AND `--plan <this file>`. Both, or refusal.",
        "- Execute only MOVES member seed dirs to `memory/worldline/_compact_archive/<stamp>/` - it never deletes.",
        "- Keepers stay in place. Seat seeds are never compacted. Every move lands a MANIFEST.jsonl row.",
        "",
        "## Summary",
        "",
        f"- lineage groups: {len(plan['groups'])}; keepers: {len(plan['groups'])}",
        f"- members to archive: {n_members} seed dirs, {b_members} bytes ({b_members / 1e6:.2f} MB)",
        "",
        "## Lineage rows",
        "",
        "| # | minute | keeper | slab_key[:12] | members | member bytes |",
        "|---|--------|--------|---------------|---------|--------------|",
    ]
    for i, g in enumerate(plan["groups"], 1):
        mb = sum(m["bytes"] for m in g["members"])
        lines.append(f"| {i} | {g['minute']} | `{g['keeper']['dir_name']}` | {g['slab_key'][:12]} | "
                     f"{len(g['members'])} | {mb} |")
    lines += ["", "## Members (sha256 = whole SEED.json file bytes at plan time)", ""]
    for i, g in enumerate(plan["groups"], 1):
        lines.append(f"### G{i} minute {g['minute']} keeper `{g['keeper']['dir_name']}` "
                     f"(keeper sha256 {g['keeper']['seed_sha256']})")
        for m in g["members"]:
            lines.append(f"- `{m['dir_name']}` sha256:{m['seed_sha256']} seed_hash:{m['seed_hash']} {m['bytes']} B")
        lines.append("")
    lines += ["## Machine block (parsed by --execute; do not hand-edit)", "", "```json",
              json.dumps(plan, indent=1), "```", ""]
    return "\n".join(lines)


def parse_plan_file(path: Path) -> dict | None:
    """Extract and validate the fenced ```json machine block. None = unusable."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    buf: list[str] = []
    inside = False
    for ln in text.splitlines():
        stripped = ln.strip()
        if stripped == "```json" and not inside:
            inside = True
            continue
        if inside and stripped == "```":
            break
        if inside:
            buf.append(ln)
    if not buf:
        return None
    try:
        plan = json.loads("\n".join(buf))
    except ValueError:
        return None
    if (not isinstance(plan, dict) or plan.get("plan_version") != PLAN_VERSION
            or not isinstance(plan.get("groups"), list) or not plan.get("worldline_dir")):
        return None
    return plan
