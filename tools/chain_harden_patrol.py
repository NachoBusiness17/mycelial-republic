#!/usr/bin/env python3
"""chain_harden_patrol - lab /proc check + MAG_ALLOW_CHAIN_REWRITE config scan.

Reused by scripts/ratchet_daily.ps1 (no new schedule). Writes
state/chain_harden_alerts.json for tools/redboard.py section.
Never touches the chain file. Never reads .env secret values (scans keys only
in compose/scripts/cmd/ps1/yml; skips .env).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALERTS = ROOT / "state" / "chain_harden_alerts.json"
APPROVAL = ROOT / "state" / "chain_rewrite_approval.json"
FLAG = "MAG_ALLOW_CHAIN_REWRITE"
SCAN_GLOBS = [
    "docker-compose.yml",
    "docker-compose.*.yml",
    "scripts/*.ps1",
    "scripts/*.cmd",
    "scripts/*.bat",
    "mag_launch.py",
    "main.py",
]


def scan_flag_files() -> list[dict]:
    hits = []
    paths: list[Path] = []
    for g in SCAN_GLOBS:
        paths.extend(ROOT.glob(g))
    # scheduled-task style launchers under scripts/container
    paths.extend((ROOT / "scripts" / "container").glob("*.py"))
    pat = re.compile(rf"{FLAG}\s*[=:]\s*[\"']?1[\"']?")
    for p in paths:
        if not p.is_file():
            continue
        if p.name == ".env" or p.suffix == ".env":
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if pat.search(text) or (FLAG in text and re.search(rf"{FLAG}.*\b1\b", text)):
            # allow comments that document the flag without setting it
            for i, ln in enumerate(text.splitlines(), 1):
                if FLAG in ln and re.search(r'[=:]\s*[\"\']?1[\"\']?', ln) and not ln.strip().startswith("#"):
                    hits.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "line": i, "snippet": ln.strip()[:120]})
    return hits


def lab_off_via_proc() -> dict:
    """Container has no ps; use /proc/*/cmdline via docker exec (or docker top)."""
    out = {"ok": None, "method": None, "lab_hits": [], "disable_env": None, "error": None}
    try:
        env = subprocess.run(
            ["docker", "exec", "mag-sovereign", "printenv", "MAG_DISABLE_LAB"],
            capture_output=True, text=True, timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        out["disable_env"] = (env.stdout or "").strip()
    except Exception as e:  # noqa: BLE001
        out["error"] = f"printenv: {type(e).__name__}"
        return out
    script = (
        "for p in /proc/[0-9]*; do "
        "cmd=$(tr '\\0' ' ' < \"$p/cmdline\" 2>/dev/null); "
        "[ -n \"$cmd\" ] && echo \"$cmd\"; done"
    )
    try:
        r = subprocess.run(
            ["docker", "exec", "mag-sovereign", "bash", "-c", script],
            capture_output=True, text=True, timeout=60,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        lines = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
        out["method"] = "/proc/cmdline"
        hits = [ln for ln in lines if re.search(r"(^|[^\w])lab([^\w]|$)|mag_launch.*lab|python.*\blab\b", ln, re.I)
                and "list_procs" not in ln and "chain_harden" not in ln]
        # narrower: process whose cmdline is clearly the lab worker
        hits = [ln for ln in lines if re.search(r"\blab\b", ln, re.I)
                and not re.search(r"MAG_DISABLE_LAB|chain_harden|list_procs", ln)]
        out["lab_hits"] = hits[:20]
        out["ok"] = (out["disable_env"] == "1") and (len(hits) == 0)
    except Exception as e:  # noqa: BLE001
        out["error"] = f"proc: {type(e).__name__}: {e}"
        # fallback docker top
        try:
            t = subprocess.run(
                ["docker", "top", "mag-sovereign"],
                capture_output=True, text=True, timeout=30,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            out["method"] = "docker top"
            hits = [ln for ln in (t.stdout or "").splitlines() if re.search(r"\blab\b", ln, re.I)]
            out["lab_hits"] = hits[:20]
            out["ok"] = (out["disable_env"] == "1") and (len(hits) == 0)
        except Exception as e2:  # noqa: BLE001
            out["error"] = f"{out.get('error')}; top: {type(e2).__name__}"
            out["ok"] = False
    return out


def approval_fresh() -> dict:
    if not APPROVAL.is_file():
        return {"present": False, "fresh": False}
    try:
        doc = json.loads(APPROVAL.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"present": True, "fresh": False, "error": "unreadable"}
    exp = str(doc.get("expires_utc") or "")
    fresh = bool(doc.get("allow")) and bool(exp)
    if fresh:
        try:
            # accept Z
            from datetime import datetime as dt
            exp_dt = dt.fromisoformat(exp.replace("Z", "+00:00"))
            fresh = exp_dt > dt.now(timezone.utc) if exp_dt.tzinfo else False
        except Exception:  # noqa: BLE001
            fresh = False
    return {"present": True, "fresh": fresh, "expires_utc": exp, "by": doc.get("by")}


def main() -> int:
    flags = scan_flag_files()
    lab = lab_off_via_proc()
    appr = approval_fresh()
    alerts = []
    if flags:
        alerts.append({"kind": "MAG_ALLOW_CHAIN_REWRITE_in_config", "count": len(flags), "hits": flags[:20]})
    if lab.get("ok") is False:
        alerts.append({"kind": "lab_not_off", "lab": lab})
    if os.environ.get(FLAG, "0").strip() == "1" and not appr.get("fresh"):
        alerts.append({"kind": "rewrite_flag_set_without_fresh_approval", "approval": appr})
    doc = {
        "schema": "chain_harden_alerts.v1",
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "alerts": alerts,
        "lab": lab,
        "flag_hits": flags,
        "approval": appr,
        "red": bool(alerts),
    }
    ALERTS.parent.mkdir(parents=True, exist_ok=True)
    ALERTS.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"HARDEN-PATROL: red={doc['red']} alerts={len(alerts)} lab_ok={lab.get('ok')} flag_hits={len(flags)}")
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
