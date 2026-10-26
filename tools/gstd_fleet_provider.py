#!/usr/bin/env python3
"""gstd_fleet_provider: the gstd mesh as the fleet's 8th lane (gated skeleton).

P3 FLEET LANE of docs/ref/GSTD_DOGFOOD_PLAN.md; spec:
docs/ref/GSTD_FLEET_LANE_SPEC.md. The mesh is the only fleet lane that PAYS
(GSTD credits settle to our per-device wallets). Until P0 lands those wallets,
this module is a sealed skeleton: every live verb returns a WALLET GATE
BLOCKED verdict and no byte touches the network. The wire into
tools/free_lane_fleet.py (PROVIDERS entry + gstd branch in fire()) lands on
wallet paste per the spec's wire plan, never before.

Laws carried from tools/free_lane_fleet.py:
  keys strip()ed at load (CR law, CSV_VERDICT_20261004.md); every banked
  string passes _scrub (KEY_SCRUB_20261004.md); SSRF guard (urlopen sees only
  fixed platform literals through a redirect-refusing opener; the single
  variable task-id URL segment is regex-gated before join); retry never (one
  submit, one poll window, failures bank).

GPS row law: completions bank a gps_mesh_row.v1 keyed
(node_device, task_shape, evidence_hash); evidence_hash is the sha256 of the
completion text bytes computed at poll time, and empty evidence never banks
(Q28 gate, tools/gps_mcp/ledger.py: dedupe on the triple, evidence never on
trust).

Usage:
  .venv\\Scripts\\python.exe -m tools.gstd_fleet_provider --status
  .venv\\Scripts\\python.exe -m tools.gstd_fleet_provider --cycle   # gated, exit 3 while blocked
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# SSRF law: fixed literals only. The base is a code constant, never an env
# override (spec section 3); changing it is a code edit at wire time.
PLATFORM = "https://platform.gstdtoken.com"
SUBMIT_URL = PLATFORM + "/api/v1/tasks/submit"
STATS_URL = PLATFORM + "/api/v1/stats"
POLL_BASE = PLATFORM + "/api/v1/tasks/"
_ALLOWED_URLS = frozenset({SUBMIT_URL, STATS_URL})

# P0 ruling request: one wallet PER DEVICE so the GPS ledger grows real
# per-node capability rows, not one pooled lane.
WALLET_ENV: tuple[tuple[str, str], ...] = (
    ("desktop", "GSTD_WALLET_DESKTOP"),
    ("bob", "GSTD_WALLET_BOB"),
    ("pixel", "GSTD_WALLET_PIXEL"),
)
TASK_SHAPES = ("probe", "corridor", "queue")

MESH_RUNS = ROOT / "memory" / "runs" / "gstd_fleet_lane"
MESH_LEDGER = MESH_RUNS / "mesh_ledger.jsonl"

POLL_TRIES = 30
POLL_SLEEP_S = 10.0
GATE_EXIT = 3
# The only non-literal allowed in any URL this module opens.
TASK_ID_RE = re.compile(r"^[A-Za-z0-9_:-]{1,80}$")

scrub_re = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|xai-[A-Za-z0-9]{16,}|AIza[A-Za-z0-9_-]{16,}|"
    r"gsk_[A-Za-z0-9]{16,}|nvapi-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9_\-\.]{15,})")


def _scrub(text: str) -> str:
    # KEY_SCRUB_20261004 law: banked strings never carry credential shapes.
    return scrub_re.sub(lambda m: m.group(0)[:12] + "[REDACTED]", str(text or ""))


def _env(name: str) -> str:
    # CR law (CSV_VERDICT_20261004.md): strip at load forever.
    try:
        for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return ""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def wallets() -> dict[str, str]:
    """Devices whose wallet is present in .env. Absent/empty/whitespace all
    read as absent: the gate is fail-closed."""
    out: dict[str, str] = {}
    for dev, env in WALLET_ENV:
        v = _env(env)
        if v:
            out[dev] = v
    return out


def wallet_gate(op: str) -> tuple[bool, str]:
    ws = wallets()
    if not ws:
        return False, ("WALLET GATE BLOCKED: no per-device wallets in .env (owed: "
                       + ", ".join(e for _, e in WALLET_ENV)
                       + "); P0 INPUTS OWED; live " + op + " refused")
    return True, "gate open: devices " + ", ".join(sorted(ws))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """SSRF guard half 2: a platform endpoint must never bounce us elsewhere."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect())


def _post_json(url: str, body: dict, token: str) -> tuple[int, dict]:
    if url not in _ALLOWED_URLS:
        return 0, {"error": "url not in fixed allowlist"}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
    try:
        with _OPENER.open(req, timeout=30) as r:
            raw = r.read().decode("utf-8", errors="replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": "HTTP " + str(e.code) + " " + str(e.reason)[:80]}
    except Exception as e:
        return 0, {"error": type(e).__name__ + ": " + str(e)[:80]}


def _get_json(url: str, token: str) -> tuple[int, dict]:
    # Poll URLs are POLL_BASE + a regex-gated task id; everything else must
    # byte-match the fixed literals (SSRF: variable segment validated first).
    var = url[len(POLL_BASE):] if url.startswith(POLL_BASE) else ""
    if url not in _ALLOWED_URLS and not (var and TASK_ID_RE.match(var)):
        return 0, {"error": "url refused by allowlist gate"}
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "Authorization": "Bearer " + token})
    try:
        with _OPENER.open(req, timeout=30) as r:
            raw = r.read().decode("utf-8", errors="replace")
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": "HTTP " + str(e.code) + " " + str(e.reason)[:80]}
    except Exception as e:
        return 0, {"error": type(e).__name__ + ": " + str(e)[:80]}


def _task_id_from(body: dict) -> str:
    # Response shapes verify at wire time against the live platform; parse
    # defensively until then (spec section 6).
    for k in ("task_id", "id"):
        v = body.get(k)
        if isinstance(v, (str, int)) and str(v).strip():
            return str(v).strip()
    inner = body.get("task")
    if isinstance(inner, dict):
        return _task_id_from(inner)
    return ""


def submit_task(*, work_id: str, prompt: str, task_shape: str, device: str) -> dict:
    """SUBMIT leg. Gate first, always: a closed gate is a blocked verdict with
    zero network calls."""
    if task_shape not in TASK_SHAPES:
        return {"ok": False, "why": "unknown task_shape: " + str(task_shape)}
    ok, why = wallet_gate("submit " + work_id)
    if not ok:
        return {"ok": False, "blocked": True, "why": why}
    ws = wallets()
    token = ws.get(device) or next(iter(ws.values()))
    code, body = _post_json(
        SUBMIT_URL,
        {"id": "gstd-" + work_id, "kind": task_shape,
         "prompt": str(prompt)[:4000], "device_hint": device},
        token)
    tid = _task_id_from(body if isinstance(body, dict) else {})
    if code != 200 or not tid:
        return {"ok": False, "http": code,
                "why": "submit failed: " + str(body.get("error", body))[:160]}
    return {"ok": True, "task_id": tid, "http": code, "device": device}


def poll_task(task_id: str, *, device: str = "", task_shape: str = "",
              work_id: str = "") -> dict:
    """POLL leg. Computes evidence_hash at poll time from the completion text
    (the falsifier clause, spec section 8)."""
    ok, why = wallet_gate("poll " + str(task_id))
    if not ok:
        return {"ok": False, "blocked": True, "why": why}
    if not TASK_ID_RE.match(task_id or ""):
        return {"ok": False, "why": "task id refused by allowlist regex"}
    ws = wallets()
    token = ws.get(device) or next(iter(ws.values()))
    for _ in range(POLL_TRIES):
        code, body = _get_json(POLL_BASE + task_id, token)
        status = str(body.get("status", "")) if isinstance(body, dict) else ""
        if code == 200 and status in ("complete", "completed", "done"):
            text = str(body.get("result") or body.get("output") or body.get("text") or "")
            ev = hashlib.sha256(text.encode("utf-8")).hexdigest()
            return {"ok": bool(text.strip()), "task_id": task_id, "http": code,
                    "completion": text[:1200], "evidence_hash": ev,
                    "model": str(body.get("model", ""))}
        if code == 200 and status in ("failed", "error", "cancelled"):
            return {"ok": False, "task_id": task_id,
                    "why": "mesh task " + status}
        time.sleep(POLL_SLEEP_S)
    return {"ok": False, "task_id": task_id,
            "why": "poll window expired (%d x %ds)" % (POLL_TRIES, POLL_SLEEP_S)}


def gps_mesh_row(*, node_device: str, task_shape: str, evidence_hash: str,
                 work_id: str = "", task_id: str = "", ok: bool = False,
                 chars: int = 0, model: str = "", latency_ms: int = 0,
                 detail: str = "") -> dict:
    """The gps_mesh_row.v1 shape keyed (node_device, task_shape, evidence_hash).
    Raises on an incomplete key or empty evidence: mesh rows never bank on
    trust (Q28 gate)."""
    if not node_device or not task_shape:
        raise ValueError("gps mesh row key incomplete: node_device and task_shape required")
    if not evidence_hash:
        raise ValueError("evidence_hash empty: mesh rows never bank on trust "
                         "(Q28 gate, tools/gps_mcp/ledger.py)")
    return {
        "schema": "gps_mesh_row.v1",
        "node_device": node_device,
        "task_shape": task_shape,
        "evidence_hash": evidence_hash,
        "key": [node_device, task_shape, evidence_hash],
        "work_id": work_id,
        "task_id": task_id,
        "provider": "gstd-mesh:" + node_device,
        "ok": bool(ok),
        "chars": int(chars),
        "model": model,
        "latency_ms": int(latency_ms),
        "ts": _now(),
        "detail": _scrub(detail)[:1200],
    }


def to_verdict_log_args(row: dict) -> dict:
    """Wire adapter: gps_mesh_row.v1 into GpsLedger.record_verdict kwargs.
    Per-device wallets make node_device a real GPS capability row."""
    return {"model_id": "gstd-mesh:" + str(row["node_device"]),
            "task_shape": str(row["task_shape"]),
            "verdict": bool(row.get("ok")),
            "evidence_hash": str(row["evidence_hash"]),
            "evidence_source": "gstd mesh task " + str(row.get("task_id") or row.get("work_id") or "")}


def bank_mesh(row: dict) -> None:
    """Append one row to the mesh ledger. Every row scrubs before landing."""
    MESH_RUNS.mkdir(parents=True, exist_ok=True)
    row = dict(row)
    row["detail"] = _scrub(str(row.get("detail", "")))
    with MESH_LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def cycle_gstd(max_tasks: int = 2) -> str:
    """The 8th lane burn cycle: submit fleet work to the mesh, poll, bank.
    Work order: free lane queue items first, then probes, then corridors;
    devices rotate round-robin over wallet-carrying devices only."""
    ok, why = wallet_gate("cycle")
    if not ok:
        return why
    from tools import free_lane_fleet as flf
    queue = flf.queue_items()
    probes = flf.probe_items(max_tasks * 2)
    devices = sorted(wallets())
    fired = 0
    banked = 0
    for i in range(max_tasks):
        dev = devices[i % len(devices)]
        if queue:
            item = queue.pop(0)
            wid, prompt, shape = str(item["id"]), str(item["prompt"]), "queue"
        elif probes:
            pr = probes[i % len(probes)]
            wid, prompt, shape = pr["id"], pr["prompt"], "probe"
        else:
            area = flf.CORRIDOR_AREAS[i % len(flf.CORRIDOR_AREAS)]
            wid, prompt, shape = "corridor:" + area, flf.corridor_ask(area), "corridor"
        sub = submit_task(work_id=wid, prompt=prompt, task_shape=shape, device=dev)
        fired += 1
        if not sub.get("ok"):
            bank_mesh({"ts": _now(), "class": "cycle", "work_id": wid,
                       "node_device": dev, "task_shape": shape,
                       "stage": "submit", "ok": False, "why": sub.get("why", "")})
            continue
        t0 = time.time()
        done = poll_task(sub["task_id"], device=dev, task_shape=shape, work_id=wid)
        latency = int((time.time() - t0) * 1000)
        if done.get("ok"):
            row = gps_mesh_row(node_device=dev, task_shape=shape,
                               evidence_hash=done["evidence_hash"], work_id=wid,
                               task_id=done["task_id"], ok=True,
                               chars=len(done.get("completion", "")),
                               model=done.get("model", ""), latency_ms=latency,
                               detail=done.get("completion", ""))
            bank_mesh(row)
            flf.bank({"ts": _now(), "provider": "gstd-mesh:" + dev,
                      "model": done.get("model", "") or "mesh:auto", "work_id": wid,
                      "ok": True, "chars": len(done.get("completion", "")),
                      "detail": done.get("completion", "")})
            banked += 1
        else:
            bank_mesh({"ts": _now(), "class": "cycle", "work_id": wid,
                       "node_device": dev, "task_shape": shape,
                       "stage": "poll", "task_id": done.get("task_id", ""),
                       "ok": False, "why": done.get("why", "")})
        time.sleep(1.0)
    return ("GSTD-MESH CYCLE: fired %d, banked %d completions, devices %s"
            % (fired, banked, ",".join(devices)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--cycle", action="store_true")
    a = ap.parse_args()
    if a.status:
        ws = wallets()
        print("WALLET GATE:", "OPEN" if ws else "BLOCKED",
              "(devices with wallets: " + (", ".join(sorted(ws)) or "none") + ")")
        print("provider: gstd-mesh | platform:", PLATFORM)
        print("submit:", SUBMIT_URL)
        print("poll base:", POLL_BASE, "| task id gate:", TASK_ID_RE.pattern)
        print("mesh ledger:", MESH_LEDGER)
        print("task shapes:", ", ".join(TASK_SHAPES))
        return 0
    if a.cycle:
        out = cycle_gstd()
        print(out)
        return GATE_EXIT if out.startswith("WALLET GATE BLOCKED") else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
