#!/usr/bin/env python3
"""lab_ctl — the ONE sanctioned path to restart / stop / start / freeze the lab (lease-gated).

The lab = compose service `mag`, container `mag-sovereign` (main.py lab, spawned
by mag_launch). Before 2026-10-17 seats ran `docker compose restart mag` (the
advice string in mag/health.py, mag/guard.py, mag/nervous_system.py,
mag/checkin_route.py, mag/boot.py, mag/os_v2.py) or froze it with a bare
SIGSTOP, with no record of who or why. This script REQUIRES a live proc:lab
lease held by the caller (configs/restricted_leases.json, mag/leases.py):

  python scripts/lease.py acquire proc:lab --seat grok --purpose "restart after compose edit"
  set MAG_LEASE_SEAT=grok & set MAG_LEASE_TOKEN=<lease_token>
  python scripts/lab_ctl.py restart --dry      # show the command, run nothing
  python scripts/lab_ctl.py restart            # run it (lease-checked)
  python scripts/lease.py release proc:lab --seat grok

Actions: restart | stop | start (compose, service mag) | freeze | unfreeze
(docker pause/unpause mag-sovereign; the honest freeze: cgroup freezer, visible
in `docker ps` as Paused, instead of a SIGSTOP nobody can see).
`status` is read-only and needs no lease.
Exit: 0 ok, 3 refused (no lease / held by another seat), 1 docker failed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SERVICE = "mag"
CONTAINER = "mag-sovereign"
ACTIONS: dict[str, list[str]] = {
    "restart": ["compose", "restart", SERVICE],
    "stop": ["compose", "stop", SERVICE],
    "start": ["compose", "start", SERVICE],
    "freeze": ["pause", CONTAINER],
    "unfreeze": ["unpause", CONTAINER],
}
STATUS = ["ps", "-a", "--filter", f"name=^{CONTAINER}$", "--format", "{{.Names}}\t{{.Status}}"]


def run(action: str, *, dry: bool = False, seat: str | None = None,
        lease_token: str | None = None) -> dict:
    from mag import docker_ops
    from mag.leases import guard

    if action == "status":
        return {"ok": True, "action": action, "cmd": ["docker", *STATUS],
                **({} if dry else {"result": docker_ops._run(STATUS, timeout=30)})}
    if action not in ACTIONS:
        return {"ok": False, "action": action, "error": f"unknown action; one of {sorted(ACTIONS)}"}
    cmd = ACTIONS[action]
    g = guard("proc:lab", f"lab_ctl.{action}", enforce="require", seat=seat, lease_token=lease_token)
    if not g.get("allowed"):
        return {"ok": False, "refused": True, "action": action, "cmd": ["docker", *cmd],
                "reason": g.get("reason"), "how": g.get("how")}
    if dry:
        return {"ok": True, "dry": True, "action": action, "cmd": ["docker", *cmd],
                "lease": {k: g.get(k) for k in ("holder", "until")}}
    r = docker_ops._run(cmd, timeout=180)
    docker_ops._log(f"lab-{action}", ok=r["ok"], seat=g.get("holder"),
                    error=(r.get("err") or "")[:200] or None)
    return {"ok": r["ok"], "action": action, "cmd": ["docker", *cmd], "code": r["code"],
            "out": (r.get("out") or "")[:500], "err": (r.get("err") or "")[:300],
            "lease": {k: g.get(k) for k in ("holder", "until")}}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lab_ctl", description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=[*ACTIONS, "status"])
    ap.add_argument("--dry", action="store_true", help="check the lease, print the command, run nothing")
    ap.add_argument("--seat", default=None, help="default env MAG_LEASE_SEAT")
    ap.add_argument("--token", default=None, help="default env MAG_LEASE_TOKEN")
    a = ap.parse_args(argv)
    out = run(a.action, dry=a.dry, seat=a.seat, lease_token=a.token)
    print(json.dumps(out, indent=1, default=str))
    if out.get("refused"):
        return 3
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
