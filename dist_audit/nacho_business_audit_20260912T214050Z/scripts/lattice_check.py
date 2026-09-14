#!/usr/bin/env python3
"""lattice_check — the Invariant Lattice organ, v0 (elder's next castle).

Law source: docs/ref/V4_SPEC.md addendum + invariant_npcs.py ("NPCs ARE
invariants, personified") + invariant_ledger.py ("5-W record + gaps at a
glance", Aug 11). This organ turns fleet law from prose into assertions:
each check runs against the LIVE tree, divergence is reported as a number.

    python scripts/lattice_check.py            # human card
    python scripts/lattice_check.py --json     # machine rows (reconcile reads)

$0, stdlib, deterministic. Divergence count = the wave reading.
New assertions must cite their law's receipt in the WHY field.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "state" / "vast" / "models_registry.json"
LESSONS = ROOT / "memory" / "runs" / "lineage_audit" / "lessons.jsonl"
LEDGER = ROOT / "state" / "vast" / "wedge_ledger.jsonl"
LATEST = ROOT / "memory" / "runs" / "lattice" / "latest.json"
REPORT = ROOT / "memory" / "runs" / "lattice"

CHECKS: list[dict] = []


def check(cid: str, law: str, why: str):
    def wrap(fn):
        CHECKS.append({"id": cid, "law": law, "why": why, "fn": fn})
        return fn
    return wrap


# --- LAW 11 (corrections): ONE SUPERVISOR ONLY -------------------------------
@check("single-hunter", "One supervisor only — hunters propose, never race",
       "live: double-hunter race caught 2026-08-28")
def check_single_hunter():
    r = subprocess.run(
        ["powershell", "-Command",
         "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
         "Where-Object { $_.CommandLine -match 'seeker|blade_buyer' } | "
         "ForEach-Object { if ($_.CommandLine -match '([a-z_]+)\\.py') { $Matches[1] } }"],
        capture_output=True, text=True, timeout=30)
    names = r.stdout.split()
    return {"seeker": names.count("seeker") // 2, "blade_buyer": names.count("blade_buyer") // 2}


# --- LAW 11: RETIRED Mag* scheduled tasks stay DISABLED -----------------------
# mag-docker-watchdog is the SANCTIONED host-side watcher (AGENTS.md law) —
# whitelisted; the retired supervisor-era Mag* tasks must stay Disabled.
SANCTIONED_MAG = {"mag-docker-watchdog"}


@check("mag-tasks-disabled", "Retired Mag* scheduled tasks stay disabled",
       "corrections law 11: two supervisors fought respawns")
def check_mag_tasks():
    r = subprocess.run(
        ["powershell", "-Command",
         "Get-ScheduledTask | Where-Object { $_.TaskName -like 'Mag*' -and $_.State -ne 'Disabled' } | "
         "Select-Object -ExpandProperty TaskName"],
        capture_output=True, text=True, timeout=30)
    violators = [l.strip() for l in r.stdout.splitlines()
                 if l.strip() and l.strip() not in SANCTIONED_MAG]
    return {"violators": violators}


# --- LINEAGE: hide-alive violation (Aug 12 rib vs live code) -----------------
@check("retain-context", "retainContextWhenHidden must stay false (Aug 12 rib)",
       "lineage lessons.jsonl: learned-and-lost, live violation found; FIXED 2026-08-28")
def check_retain_context():
    hits = []
    for f in (ROOT / "vscode-mag-map").rglob("*.js"):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"retainContextWhenHidden\s*:\s*true", text):
                hits.append(str(f.relative_to(ROOT)))
        except OSError:
            continue
    return {"violations": hits}


# --- COVENANT: balance floor $39 (operator, 2026-08-28) ----------------------
@check("covenant-floor", "Vast balance stays >= $39 until scale is proven",
       "operator covenant 2026-08-28, baby steps + dog food")
def check_covenant():
    r = subprocess.run(
        [sys.executable, str(ROOT / "state" / "vast" / "launch_vast.py"), "probe"],
        capture_output=True, text=True, timeout=60)
    for line in (r.stdout or "").splitlines():
        if line.startswith("balance:"):
            return {"balance": float(line.split("$")[1].split()[0])}
    return {"balance": None}


# --- ENVELOPE LAW: one resident model on the hands box -----------------------
@check("one-resident", "One resident model per box (envelope law, 08-06)",
       "HOME_HARDWARE_ENVELOPE.md: '6GB VRAM -> one resident model'; /api/ps = VRAM residents (tags = disk catalog)")
def check_one_resident():
    import urllib.request
    try:
        d = json.load(urllib.request.urlopen("http://localhost:18000/api/ps", timeout=8))
        names = [m["name"] for m in d.get("models", [])]
        return {"vram_resident": names}
    except Exception as e:  # noqa: BLE001 — tunnel down is a divergence, not a crash
        return {"error": str(e)[:80]}


# --- EPISTEMIC LABELING: every registry entry carries size_status ------------
@check("registry-provenance", "Every model registry entry cites size provenance",
       "sizer law: receipt > vendor-quoted > Unproven")
def check_registry():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unlabeled = [m["id"] for m in reg["models"]
                 if not m.get("size_status") or "unproven" not in m.get("size_status", "").lower()
                 and "receipt" not in m.get("size_status", "").lower()
                 and "incoming" not in m.get("size_status", "").lower()
                 and "quoted" not in m.get("size_status", "").lower()]
    return {"unlabeled": unlabeled, "n_models": len(reg["models"])}


# --- LINEAGE LEDGER EXISTS AND GROWS -----------------------------------------
@check("lessons-ledger", "The lineage lessons ledger exists and is non-empty",
       "lineage audit plan: lessons.jsonl is the fleet's memory of paid lessons")
def check_lessons():
    if not LESSONS.exists():
        return {"rows": 0}
    return {"rows": sum(1 for _ in LESSONS.open(encoding="utf-8"))}


def main() -> int:
    as_json = "--json" in sys.argv
    rows = []
    for c in CHECKS:
        try:
            detail = c["fn"]()
        except Exception as e:  # noqa: BLE001 — a broken check is itself a divergence
            detail = {"error": str(e)[:120]}
        diverged = _is_diverged(c["id"], detail)
        rows.append({"id": c["id"], "law": c["law"], "detail": detail, "diverged": diverged})
    n_div = sum(1 for r in rows if r["diverged"])
    LATEST.parent.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(),
        "divergence": n_div, "checks": len(rows), "rows": rows},
        indent=1, ensure_ascii=False), encoding="utf-8")
    if as_json:
        print(json.dumps({"divergence": n_div, "checks": len(rows)}))
    else:
        print(f"INVARIANT LATTICE — divergence {n_div}/{len(rows)}")
        for r in rows:
            mark = "DIVERGED" if r["diverged"] else "ok"
            print(f"  [{mark:^8}] {r['id']}: {json.dumps(r['detail'])[:90]}")
    return 0


def _is_diverged(cid: str, d: dict) -> bool:
    if cid == "single-hunter":
        return d.get("seeker", 1) > 1 or d.get("blade_buyer", 1) > 1
    if cid == "mag-tasks-disabled":
        return bool(d.get("violators"))
    if cid == "retain-context":
        return bool(d.get("violations"))
    if cid == "covenant-floor":
        b = d.get("balance")
        return b is None or b < 39.0
    if cid == "one-resident":
        return "error" in d or len(d.get("models", [])) > 2
    if cid == "registry-provenance":
        return bool(d.get("unlabeled"))
    if cid == "lessons-ledger":
        return d.get("rows", 0) < 1
    return False


if __name__ == "__main__":
    raise SystemExit(main())
