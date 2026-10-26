#!/usr/bin/env python3
"""invariant_percolator_audit -- does the invariant registry hold invariants?

WAVE: invariant-percolator, 2026-10-20. Read-only. Stdlib only. $0.

The experiment's own claim (mag/percolator.py:1-10): signal that can be REPEATED is
compiled into an invariant; novel signal goes to the explore queue instead. The
audit tests that claim against the registry's own bytes, not against the docstring.

Exit ladder (self-stolen from tools/claim_drift_patrol.py):
  0 green   -- every invariant in the registry is actually invariant
  1 VIOLATED -- at least one invariant broke; each row names its evidence
  2 CANNOT-VERIFY -- registry/queue missing or unreadable (never a guess)

Self-steal ledger:
  - exit ladder + "cannot-verify is not failure": tools/claim_drift_patrol.py
  - recurrence-as-truth critique:      memory/percolator/invariants.json (Z15 count laws)
  - promotion gate shape:              memory/percolator/candidates.jsonl (promoted=False)
  - failure-signature vocabulary:      mag/failure_kb.py

Gates (all measured, thresholds are operator dials at the top):
  I1 NO_UNREPEATED_INVARIANTS  count >= min_count for every registry row
  I2 NO_SELF_REFERENTIAL_TOP   top-decile by count is not dominated by fleet failure strings
  I3 NO_PROBE_DOMINANCE        probe_* share of the registry <= probe_share_max
  I4 EXPLORE_BACKLOG           open explore rows <= open_share_max of all explore rows
  I5 DEPENDENCY_HONEST         promoted rows are declared OR leaves (never depended-on but silent)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("memory") / "percolator" / "invariants.json"
EXPLORE = Path("memory") / "percolator" / "explore.jsonl"
LEDGER = Path("memory") / "percolator" / "promotion_ledger.jsonl"
FALSIFIERS = Path("memory") / "percolator" / "falsifiers.jsonl"
DECAY = Path("memory") / "percolator" / "explore_decay.jsonl"
STALE_DAYS = 14.0
STALE_UNCLASSIFIED_MAX = 0.05

try:  # self-steal: one promotion policy, two readers
    from tools.invariant_promote import load_ledger as _load_promotion_ledger
except ImportError:  # direct script execution (python tools/...)
    from invariant_promote import load_ledger as _load_promotion_ledger

OK_PREFIX = "PERCOLATOR-AUDIT: ok"
FAIL_PREFIX = "PERCOLATOR-AUDIT: VIOLATED"
UNVER_PREFIX = "PERCOLATOR-AUDIT: UNVERIFIABLE"

# operator dials
MIN_COUNT = 2
PROBE_SHARE_MAX = 0.25
OPEN_SHARE_MAX = 0.25
DEPENDENCY_SHARE_MIN = 0.10
SELF_REFERENTIAL_SHARE_MAX = 0.50

# the fleet's own failure vocabulary -- recurrence here measures the loop, not the world
FLEET_FAILURE_RE = re.compile(
    r"backend reported failure|backend not reachable|backend timeout|not allowlisted|"
    r"false-success|identical tool calls|identical run_python|does not exist: /app/",
    re.IGNORECASE,
)
PROBE_DOMAIN_RE = re.compile(r"^probe_", re.IGNORECASE)


def _pct(n: int, d: int) -> float:
    return 0.0 if not d else 100.0 * n / d


def load(root: Path | None = None) -> tuple[dict, list[dict]]:
    root = root or ESTATE_ROOT
    reg_path = root / REGISTRY
    ex_path = root / EXPLORE
    if not reg_path.is_file():
        raise FileNotFoundError(f"registry missing: {reg_path}")
    if not ex_path.is_file():
        raise FileNotFoundError(f"explore queue missing: {ex_path}")
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    if not isinstance(reg.get("invariants"), dict):
        raise ValueError("registry has no 'invariants' object")
    rows = []
    for line in ex_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return reg, rows


def audit(reg: dict, explore: list[dict], *,
          promoted_keys: set[str] | None = None,
          falsifier_keys: set[str] | None = None,
          decayed: set[str] | None = None) -> tuple[list[dict], dict]:
    inv = reg["invariants"]
    total = len(inv)
    counts = [int(v.get("count", 1)) for v in inv.values()]
    unrep = [(k, v) for k, v in inv.items() if int(v.get("count", 1)) < MIN_COUNT]

    probes = [v for v in inv.values() if PROBE_DOMAIN_RE.match(str(v.get("domain", "")))]
    dep = [v for v in inv.values() if v.get("depends_on")]
    open_rows = sum(1 for r in explore if r.get("status") == "open")

    top_n = max(1, total // 10)
    top = sorted(inv.values(), key=lambda v: -int(v.get("count", 1)))[:top_n]
    selfref = [v for v in top if FLEET_FAILURE_RE.search(str(v.get("text", "")))]

    results = []

    def gate(gid: str, ok: bool, detail: str, **extra) -> None:
        results.append({"id": gid, "ok": ok, "detail": detail, **extra})

    gate(
        "I1", not unrep,
        f"{len(unrep)}/{total} registry rows have count < {MIN_COUNT} "
        f"({_pct(len(unrep), total):.1f}% compiled before the stated repeat condition)",
        offenders=[{"canonical": k, "text": str(v.get("text", ""))[:90],
                    "count": v.get("count"), "first_seen": v.get("first_seen")}
                   for k, v in unrep[:5]],
    )
    gate(
        "I2", _pct(len(selfref), len(top)) <= 100 * SELF_REFERENTIAL_SHARE_MAX,
        f"{len(selfref)}/{len(top)} top-decile invariants are fleet failure strings "
        f"({_pct(len(selfref), len(top)):.1f}%, cap {SELF_REFERENTIAL_SHARE_MAX*100:.0f}%)",
        offenders=[{"count": v.get("count"), "text": str(v.get("text", ""))[:90]}
                   for v in selfref[:5]],
    )
    gate(
        "I3", _pct(len(probes), total) <= 100 * PROBE_SHARE_MAX,
        f"{len(probes)}/{total} rows are probe_* model chatter "
        f"({_pct(len(probes), total):.1f}%, cap {PROBE_SHARE_MAX*100:.0f}%)",
    )
    # I4 (wave 6, 2026-10-21): the queue only grows, so "open share" measured
    # age, not backlog. The meaningful law is that dead rows are CLASSIFIED:
    # open rows past the age bar that the decay ledger has not marked stale.
    decayed = decayed or set()
    now_dt = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    def _age_days(value):
        try:
            t = __import__("datetime").datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except Exception:
            return 0.0
        return (now_dt - t).total_seconds() / 86400.0
    late = [r for r in explore
            if r.get("status") == "open"
            and r.get("canonical") not in decayed
            and _age_days(r.get("ts")) > STALE_DAYS]
    gate(
        "I4", _pct(len(late), open_rows) <= 100 * STALE_UNCLASSIFIED_MAX,
        f"{len(late)}/{open_rows} open rows are older than {STALE_DAYS:.0f}d and "
        f"unclassified ({_pct(len(late), open_rows):.1f}%, cap "
        f"{STALE_UNCLASSIFIED_MAX*100:.0f}%) - run tools/explore_decay.py --apply",
        offenders=[{"canonical": r.get("canonical"), "age_days": round(_age_days(r.get("ts")), 1)}
                   for r in late[:5]],
    )
    # I5 (wave 7, 2026-10-24): DEPENDENCY_DECLARED demanded edges from every row.
    # But the promoted surface is mostly LEAVES - 0/17 declare depends_on while
    # 963 edges exist elsewhere - and a leaf is exactly where an observation is
    # supposed to land. Demanding edges from a leaf is demanding fiction.
    # New law: a promoted row must be DECLARED or a LEAF. The failure class is
    # the middle: something already depends on it, yet it declares nothing.
    rows = reg.get("invariants", reg) if isinstance(reg, dict) else {}
    inbound: dict[str, int] = {}
    for key, row in rows.items():
        for parent in row.get("depends_on") or []:
            inbound[parent] = inbound.get(parent, 0) + 1
    promoted_ids = (promoted_keys & set(rows)) if promoted_keys else set(rows)
    declared = [k for k in promoted_ids if rows[k].get("depends_on")]
    leaves = [k for k in promoted_ids if not rows[k].get("depends_on")
              and inbound.get(k, 0) == 0]
    orphaned = [k for k in promoted_ids if not rows[k].get("depends_on")
                and inbound.get(k, 0) > 0]
    gate(
        "I5", not orphaned,
        f"{len(declared)} declared, {len(leaves)} leaf, {len(orphaned)} depended-on "
        f"but undeclared (of {len(promoted_ids)} promoted; {len(inbound)} nodes carry inbound edges)",
        offenders=[{"canonical": k, "inbound": inbound.get(k, 0),
                    "text": str(rows[k].get("text", ""))[:80]} for k in orphaned[:5]],
    )

    if promoted_keys and falsifier_keys is not None:
        covered = [k for k in promoted_keys if k in falsifier_keys]
        missing = sorted(set(promoted_keys) - set(covered))
        gate(
            "I6", not missing,
            f"{len(covered)}/{len(promoted_keys)} promoted rows carry a falsifier entry",
            offenders=[{"canonical": k} for k in missing[:5]],
        )

    stats = {
        "invariants": total,
        "repeat_rows": total - len(unrep),
        "repeat_share_pct": round(_pct(total - len(unrep), total), 1),
        "probe_rows": len(probes),
        "dependency_rows": len(dep),
        "explore_rows": len(explore),
        "explore_open": open_rows,
        "explore_stale_classified": sum(1 for r in explore
                                        if r.get("status") == "open"
                                        and r.get("canonical") in (decayed or set())),
        "explore_live": open_rows - sum(1 for r in explore
                                        if r.get("status") == "open"
                                        and r.get("canonical") in (decayed or set())),
        "max_count": max(counts) if counts else 0,
        "median_count": sorted(counts)[len(counts) // 2] if counts else 0,
        "sum_count": sum(counts),
    }
    return results, stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Audit the invariant percolator registry")
    ap.add_argument("--json", action="store_true", help="emit the machine receipt only")
    ap.add_argument("--root", default=None, help="estate root (default: this repo)")
    ap.add_argument("--promoted-only", action="store_true",
                    help="audit only rows the promotion ledger marks promoted")
    ap.add_argument("--ledger", default=None,
                    help="promotion ledger path (default: memory/percolator/promotion_ledger.jsonl)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ESTATE_ROOT
    surface = "registry"

    try:
        reg, explore = load(root)
        ledger_path = Path(args.ledger).resolve() if args.ledger else root / LEDGER
        latest = _load_promotion_ledger(ledger_path) if ledger_path.is_file() else {}
        if args.promoted_only:
            if not ledger_path.is_file():
                print(f"{UNVER_PREFIX}: promotion ledger missing: {ledger_path}")
                return 2
            promoted = {c for c, r in latest.items() if r.get("promoted")}
            reg = {"invariants": {k: v for k, v in reg["invariants"].items() if k in promoted}}
            surface = f"promoted ({len(reg['invariants'])} rows)"
        else:
            promoted = {c for c, r in latest.items() if r.get("promoted")}
        falsifier_keys: set[str] = set()
        falsifiers_path = root / FALSIFIERS
        if falsifiers_path.is_file():
            for line in falsifiers_path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("schema") == "invariant_falsifier.v1" and row.get("canonical"):
                    falsifier_keys.add(row["canonical"])
        decayed: set[str] = set()
        decay_path = root / DECAY
        if decay_path.is_file():
            for line in decay_path.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("schema") == "explore_decay.v1" and row.get("canonical"):
                    decayed.add(row["canonical"])
        results, stats = audit(reg, explore,
                               promoted_keys=promoted & set(reg["invariants"]),
                               falsifier_keys=falsifier_keys,
                               decayed=decayed)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"{UNVER_PREFIX}: {exc}")
        return 2

    failed = [r for r in results if not r["ok"]]
    receipt = {"schema": "percolator_audit.v1", "ts": __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z"),
        "surface": surface, "status": "green" if not failed else "violated",
        "stats": stats, "gates": results}

    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        head = OK_PREFIX if not failed else FAIL_PREFIX
        print(f"{head} -- {len(results) - len(failed)}/{len(results)} gates green "
              f"[surface: {surface}]")
        print(f"  registry: {stats['invariants']} invariants, "
              f"{stats['repeat_share_pct']}% meet the repeat gate, "
              f"median count {stats['median_count']}, max {stats['max_count']}")
        for r in results:
            mark = "PASS" if r["ok"] else "FAIL"
            print(f"  [{mark}] {r['id']} {r['detail']}")
            for o in r.get("offenders", []):
                print(f"         - {o}")
        if failed:
            print(f"\n{FAIL_PREFIX}: {', '.join(r['id'] for r in failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
